"""Ridge and Lasso linear baseline models for Saber Pro PROMEDIO_GLOBAL prediction.

This module implements Phase 4 of the Saber Pro predictive pipeline.  It
provides Ridge and Lasso regression baselines using sklearn ``Pipeline``
objects that encapsulate preprocessing and model fitting in a single unit.
By packaging preprocessing inside the Pipeline, the TargetEncoder for
categorical columns (``NBC``, ``NOMBRE_PRUEBA``, ``ID_DEPARTAMENTO``) is
refitted on train data only for each cross-validation fold, preventing the
cross-fold label leakage that would occur if target encoding were applied to
the full dataset before splitting.

The module defines two primary functions:

- ``train_ridge``: fits a Ridge regressor with cross-validated alpha selection
  (``RidgeCV``) using ``TimeSeriesSplit`` to respect the temporal structure of
  the panel data.
- ``train_lasso``: fits a Lasso regressor with cross-validated alpha selection
  (``LassoCV``), additionally reporting which features received non-zero
  coefficients (the Lasso's built-in feature selection).

Both functions share the same column definitions (``NUMERIC_FEATURE_COLS``,
``CAT_TARGET_ENCODE_COLS``) and the same preprocessing logic
(``build_preprocessor``), which are also imported by ``models/boosting.py``
to ensure consistency across model phases.

Feature column design decisions (explicitly excluded features):

- ``PROMEDIO_PRUEBA``: concurrent with target — published in the same ICFES
  release as ``PROMEDIO_GLOBAL``.
- ``DESVIACION``, ``NIVEL1``-``NIVEL4``, ``concurrent_prop_*``: same-year
  concurrent features derived from the same data release.
- ``delta_1_global``: removed during the leakage audit (direct linear
  transformation of the target).
- ``tendencia_global``, ``tendencia_prueba``, ``desviacion_estandar_historica``,
  ``coeficiente_variacion``: corrected versions (expanding window excluding
  year t) are included; prior leaky versions were removed.

Usage example::

    from sklearn.model_selection import TimeSeriesSplit
    from src.models.baseline import train_ridge, train_lasso

    tscv = TimeSeriesSplit(n_splits=4, gap=0)

    ridge_result = train_ridge(X_train, y_train, X_test, y_test, tscv)
    print(f"Ridge alpha: {ridge_result['alpha']:.4f}")
    print(f"Test predictions shape: {ridge_result['y_pred_test'].shape}")

    lasso_result = train_lasso(X_train, y_train, X_test, y_test, tscv)
    print(f"Lasso selected {lasso_result['n_selected']} / "
          f"{lasso_result['n_total']} features")

Warning:
    ``TimeSeriesSplit`` must be constructed with the same ``n_splits`` used
    here and passed in by the calling script.  Using a random or stratified
    split instead of a time-ordered split would allow future-year information
    to appear in training folds, inflating cross-validated performance estimates
    and defeating the temporal isolation that is central to this pipeline's
    leakage-prevention strategy.
"""

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LassoCV, RidgeCV
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, TargetEncoder


# ── Definición de columnas por tipo ──────────────────────────────────────────

# Categóricas que van a TargetEncoder (calculado DENTRO del Pipeline → sin leakage)
CAT_TARGET_ENCODE_COLS = ["NBC", "NOMBRE_PRUEBA", "ID_DEPARTAMENTO"]
"""list[str]: Categorical columns encoded by TargetEncoder inside the Pipeline.

These columns are intentionally left as raw strings in ``features.build_features``
and encoded only during ``Pipeline.fit``.  Because the Pipeline's
``ColumnTransformer`` calls ``TargetEncoder.fit`` on the training data it
receives, the encoding is always computed on train-only labels regardless of
the outer cross-validation fold structure.  This prevents the cross-entity
label leakage that would occur if encoding were applied to the concatenated
train+test DataFrame.
"""

# Numéricas construidas en Fase 3 — solo features sin leakage temporal
# EXCLUIDAS explícitamente (concurrent con el target del mismo año):
#   PROMEDIO_PRUEBA  → mismo release ICFES que PROMEDIO_GLOBAL
#   DESVIACION       → de PUNTAJE_PRUEBA, mismo año
#   NIVEL1-4         → de NIVEL_DESEMPEÑO_PRUEBA, mismo año
#   prop_nivel*      → derivadas de NIVEL1-4 (concurrent_prop_* en CSV)
#   delta_1_global   → = PROMEDIO_GLOBAL - lag_1 (target leak directo, eliminado)
# CORREGIDAS (tendencia y volatilidad ahora usan solo historia t-1):
#   tendencia_global, tendencia_prueba → expanding lag, excluyen año t
#   desviacion_estandar_historica, coeficiente_variacion → idem
NUMERIC_FEATURE_COLS = [
    # Lags temporales (historia t-1, t-2 — sin leakage)
    "lag_1_promedio_global", "lag_2_promedio_global",
    "lag_1_promedio_prueba",  "lag_2_promedio_prueba",
    # Tendencia (expanding lag: slope calculado con historia hasta t-1)
    "tendencia_global", "tendencia_prueba",
    # Volatilidad (expanding lag: std/CV calculados con historia hasta t-1)
    "desviacion_estandar_historica", "coeficiente_variacion",
    # Contexto (tamaño de cohorte, disponible antes de resultados)
    "log_cantidadevaluados",
    # Tendencia temporal global del sistema educativo
    "AÑO",
]
"""list[str]: Numeric feature columns used by all model phases.

This list is the single source of truth for which numeric features enter the
model.  It is imported by ``models/boosting.py`` and ``src/inference.py`` to
ensure all phases use the same feature set.  Any change to this list must be
accompanied by re-running Phases 4 through 7 and updating ``inference.py``'s
``NUMERIC_COLS`` constant.
"""

TARGET_COL = "PROMEDIO_GLOBAL"
"""str: Name of the prediction target column."""


def get_feature_columns(df: pd.DataFrame) -> tuple[list, list, list]:
    """Return the numeric, categorical, and OHE column lists present in df.

    Filters ``NUMERIC_FEATURE_COLS``, ``CAT_TARGET_ENCODE_COLS``, and any
    column starting with ``"cat_prueba_"`` against the actual columns in
    ``df``.  This guard prevents ``KeyError`` when a feature column is absent
    from a DataFrame (e.g. when running on a subset of years that does not
    have enough history to produce non-null trend features).

    Args:
        df: A wide-format feature DataFrame produced by
            ``features.build_features``.

    Returns:
        A three-element tuple ``(num_cols, cat_cols, ohe_cols)`` where each
        element is a list of column names that are both defined in the
        corresponding feature list and actually present in ``df``.

    Example:
        >>> num_cols, cat_cols, ohe_cols = get_feature_columns(df_train)
        >>> len(num_cols)
        10
        >>> cat_cols
        ['NBC', 'NOMBRE_PRUEBA', 'ID_DEPARTAMENTO']
        >>> ohe_cols
        ['cat_prueba_1', 'cat_prueba_34']
    """
    num_cols = [c for c in NUMERIC_FEATURE_COLS if c in df.columns]
    cat_cols = [c for c in CAT_TARGET_ENCODE_COLS if c in df.columns]
    # Columnas OHE ya creadas en Fase 3 (cat_prueba_*)
    ohe_cols = [c for c in df.columns if c.startswith("cat_prueba_")]
    return num_cols, cat_cols, ohe_cols


def build_preprocessor(num_cols: list, cat_cols: list, ohe_cols: list) -> ColumnTransformer:
    """Build a ColumnTransformer that preprocesses all three feature types.

    Constructs a three-branch transformer:

    - **Numeric branch** (``"num"``): ``SimpleImputer(strategy="median")``
      followed by ``StandardScaler``.  Median imputation handles the NaN values
      that arise naturally in lag and trend features for entities with limited
      history.  Scaling is required for Ridge and Lasso (L2/L1 penalty is not
      scale-invariant).
    - **Categorical branch** (``"cat"``): ``SimpleImputer(strategy="constant",
      fill_value="DESCONOCIDO")`` followed by ``TargetEncoder(smooth="auto",
      cv=2)``.  The imputer ensures that rare or null categories do not cause
      errors; the TargetEncoder computes smoothed mean-target encodings with
      ``cv=2`` internal cross-fitting to further reduce within-fold leakage.
    - **OHE branch** (``"ohe"``): passthrough — the binary columns produced by
      ``features.build_features`` are already 0/1 integers and require no
      further transformation.

    Any column not assigned to one of the three branches is dropped
    (``remainder="drop"``), ensuring that raw identifiers and concurrent
    features do not accidentally enter the model.

    Args:
        num_cols: List of numeric feature column names.
        cat_cols: List of categorical column names for TargetEncoder.
        ohe_cols: List of pre-computed binary OHE column names.

    Returns:
        An unfitted ``sklearn.compose.ColumnTransformer`` ready to be used
        as the first step of a ``Pipeline``.

    Example:
        >>> preprocessor = build_preprocessor(num_cols, cat_cols, ohe_cols)
        >>> type(preprocessor).__name__
        'ColumnTransformer'

    Note:
        The TargetEncoder ``cv=2`` argument enables sklearn's internal
        cross-fitting: when called within an outer ``TimeSeriesSplit`` fold,
        the encoder further splits the fold's training data into 2 sub-folds
        to estimate out-of-fold target encodings.  This reduces within-fold
        leakage for high-cardinality categoricals such as ``NOMBRE_PRUEBA``
        (which has many distinct values), at the cost of slightly longer
        training time.  For LightGBM (``models/boosting.py``), ``cv=2`` is
        retained for consistency but has a smaller practical effect because
        tree models are less sensitive to target-encoded magnitude than linear
        models.
    """
    transformers = []

    if num_cols:
        numeric_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler",  StandardScaler()),
        ])
        transformers.append(("num", numeric_pipe, num_cols))

    if cat_cols:
        # TargetEncoder de sklearn 1.3+: calcula el encoding DENTRO del fit
        # sobre los datos de train que recibe → sin leakage cuando se usa
        # dentro de un Pipeline con TimeSeriesSplit.
        te_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="constant", fill_value="DESCONOCIDO")),
            ("encoder", TargetEncoder(smooth="auto", cv=2, random_state=42)),
        ])
        transformers.append(("cat", te_pipe, cat_cols))

    if ohe_cols:
        transformers.append(("ohe", "passthrough", ohe_cols))

    return ColumnTransformer(transformers=transformers, remainder="drop")


def train_ridge(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test:  pd.DataFrame,
    y_test:  pd.Series,
    tscv:    TimeSeriesSplit,
) -> dict:
    """Train a Ridge regression Pipeline with cross-validated alpha selection.

    Builds a full sklearn Pipeline (preprocessor + RidgeCV), fits it on
    ``(X_train, y_train)``, and generates predictions on both the training
    and test sets.  Alpha is selected by ``RidgeCV`` using the supplied
    ``TimeSeriesSplit`` with negative MSE scoring, so only chronologically
    earlier folds are used to estimate performance for each test fold.

    Args:
        X_train: Feature DataFrame for training rows (years 2020-2023).
            Must contain all columns returned by ``get_feature_columns``.
        y_train: Series of ``PROMEDIO_GLOBAL`` values aligned with ``X_train``.
        X_test: Feature DataFrame for test rows (year 2024).
        y_test: Series of ``PROMEDIO_GLOBAL`` values aligned with ``X_test``.
            Not used during training; included for API symmetry with
            ``train_lasso`` and ``train_lgbm``.
        tscv: A configured ``TimeSeriesSplit`` instance.  Typically
            ``TimeSeriesSplit(n_splits=4)`` for 4-year cross-validation on the
            2020-2023 training window.

    Returns:
        A dictionary with the following keys:

        - ``"pipeline"`` (Pipeline): The fitted sklearn Pipeline.
        - ``"alpha"`` (float): The alpha selected by ``RidgeCV``.
        - ``"num_features"`` (int): Total number of features after preprocessing.
        - ``"feature_names"`` (list[str]): Ordered list of feature names passed
          to the model (numeric + categorical + OHE).
        - ``"y_pred_train"`` (np.ndarray): Training-set predictions.
        - ``"y_pred_test"`` (np.ndarray): Test-set predictions.

    Raises:
        ValueError: If ``X_train`` is empty or if ``tscv`` generates folds
            with insufficient samples for the TargetEncoder.

    Example:
        >>> from sklearn.model_selection import TimeSeriesSplit
        >>> tscv = TimeSeriesSplit(n_splits=4)
        >>> result = train_ridge(X_train, y_train, X_test, y_test, tscv)
        >>> result["alpha"]
        12.3284
        >>> result["y_pred_test"].shape
        (8012,)

    Note:
        Ridge training-set predictions are computed on the full training set
        (not out-of-fold), so ``y_pred_train`` is in-sample and will appear
        more accurate than the test-set predictions.  Use ``y_pred_test`` for
        all reported metrics.
    """
    num_cols, cat_cols, ohe_cols = get_feature_columns(X_train)
    preprocessor = build_preprocessor(num_cols, cat_cols, ohe_cols)

    alphas = np.logspace(-3, 5, 60)
    ridge = RidgeCV(alphas=alphas, cv=tscv, scoring="neg_mean_squared_error")

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model",        ridge),
    ])
    pipeline.fit(X_train, y_train)

    y_pred_train = pipeline.predict(X_train)
    y_pred_test  = pipeline.predict(X_test)

    return {
        "pipeline":      pipeline,
        "alpha":         pipeline.named_steps["model"].alpha_,
        "num_features":  len(num_cols) + len(cat_cols) + len(ohe_cols),
        "feature_names": num_cols + cat_cols + ohe_cols,
        "y_pred_train":  y_pred_train,
        "y_pred_test":   y_pred_test,
    }


def train_lasso(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test:  pd.DataFrame,
    y_test:  pd.Series,
    tscv:    TimeSeriesSplit,
) -> dict:
    """Train a Lasso regression Pipeline with cross-validated alpha and feature selection.

    Builds a full sklearn Pipeline (preprocessor + LassoCV), fits it on
    ``(X_train, y_train)``, and identifies which features received non-zero
    coefficients (the Lasso's implicit feature selection).  Alpha is selected
    by ``LassoCV`` using ``TimeSeriesSplit`` to respect temporal ordering.

    Args:
        X_train: Feature DataFrame for training rows (years 2020-2023).
        y_train: Series of ``PROMEDIO_GLOBAL`` values aligned with ``X_train``.
        X_test: Feature DataFrame for test rows (year 2024).
        y_test: Series of ``PROMEDIO_GLOBAL`` values aligned with ``X_test``.
            Not used during training; included for API symmetry.
        tscv: A configured ``TimeSeriesSplit`` instance.

    Returns:
        A dictionary with the following keys:

        - ``"pipeline"`` (Pipeline): The fitted sklearn Pipeline.
        - ``"alpha"`` (float): The alpha selected by ``LassoCV``.
        - ``"coefs"`` (dict): Mapping of feature name to its Lasso coefficient.
          Features excluded by L1 regularisation have coefficient 0.0.
        - ``"selected_features"`` (list[str]): Feature names with
          ``|coef| > 1e-10`` (non-zero after L1 shrinkage).
        - ``"n_selected"`` (int): Count of selected features.
        - ``"n_total"`` (int): Total number of features before selection.
        - ``"feature_names"`` (list[str]): All feature names in order.
        - ``"y_pred_train"`` (np.ndarray): Training-set predictions.
        - ``"y_pred_test"`` (np.ndarray): Test-set predictions.

    Raises:
        ValueError: If ``X_train`` is empty or LassoCV does not converge
            within ``max_iter=10_000`` iterations.

    Example:
        >>> tscv = TimeSeriesSplit(n_splits=4)
        >>> result = train_lasso(X_train, y_train, X_test, y_test, tscv)
        >>> result["n_selected"]
        8
        >>> result["selected_features"]
        ['lag_1_promedio_global', 'lag_1_promedio_prueba', 'AÑO', ...]

    Note:
        Lasso coefficients are computed on the standardised feature space
        (after ``StandardScaler``), so the raw coefficient magnitudes reflect
        relative importance on the same scale but not the original feature
        units.  Use ``plot_lasso_coefs`` from ``evaluation.py`` to visualise
        the top features by absolute coefficient value.
    """
    num_cols, cat_cols, ohe_cols = get_feature_columns(X_train)
    preprocessor = build_preprocessor(num_cols, cat_cols, ohe_cols)

    lasso = LassoCV(
        n_alphas=100,
        cv=tscv,
        max_iter=10_000,
        random_state=42,
        n_jobs=-1,
    )

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model",        lasso),
    ])
    pipeline.fit(X_train, y_train)

    coefs = pipeline.named_steps["model"].coef_
    all_names = num_cols + cat_cols + ohe_cols
    selected = [n for n, c in zip(all_names, coefs) if abs(c) > 1e-10]

    y_pred_train = pipeline.predict(X_train)
    y_pred_test  = pipeline.predict(X_test)

    return {
        "pipeline":          pipeline,
        "alpha":             pipeline.named_steps["model"].alpha_,
        "coefs":             dict(zip(all_names, coefs)),
        "selected_features": selected,
        "n_selected":        len(selected),
        "n_total":           len(all_names),
        "feature_names":     all_names,
        "y_pred_train":      y_pred_train,
        "y_pred_test":       y_pred_test,
    }
