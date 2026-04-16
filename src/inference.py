"""Inference module for the Saber Pro Predictive Engine.

This module implements Phase 7 of the Saber Pro predictive pipeline.  It
provides the production-facing API for generating ``PROMEDIO_GLOBAL``
predictions from the trained LightGBM pipeline serialised during Phase 5.

Three usage patterns are supported:

1. **Single-entity prediction** (``predict_institution``): generates a
   fully-structured result dictionary for one program-exam-year combination,
   including the predicted score, three confidence flags, and an audit trail
   of the feature values used.  Intended for interactive dashboards or REST
   API endpoints.

2. **Batch prediction** (``predict_batch``): applies the trained pipeline to
   a DataFrame with the required feature columns and appends prediction and
   confidence columns.  Intended for scoring large cohorts at once.

3. **Feature row construction** (``build_inference_row``): translates raw
   institutional inputs (NBC, exam name, year, cohort size, historical scores)
   into a one-row DataFrame with exactly the columns the sklearn Pipeline
   expects.  All unknown feature values can be left as ``None``; they will
   be imputed by the ``SimpleImputer(strategy="median")`` step inside the
   Pipeline.

Confidence assessment is based on three independent flags:

- ``BAJA_CONFIANZA_MUESTRA_PEQUEÑA``: ``CANTIDADEVALUADOS < 5``.  Programmes
  with very small cohorts have highly variable mean scores that are sensitive
  to individual outliers (documented in ``analisis_outliers.txt``).
- ``BAJA_CONFIANZA_SIN_HISTORIAL``: ``lag_1_promedio_global`` is null.
  The model's strongest feature is the prior-year score; without it the
  pipeline falls back to median imputation and accuracy degrades substantially.
- ``BAJA_CONFIANZA_EXTRAPOLACION``: ``AÑO > 2023`` (the last training year).
  Predictions for years beyond the training horizon may be inaccurate if the
  higher-education system changes materially.

Usage example::

    from src.inference import load_model, predict_institution, format_prediction_report

    model = load_model("outputs/lgbm_model.pkl")

    result = predict_institution(
        model=model,
        año=2025,
        nbc="INGENIERIA",
        nombre_prueba="RAZONAMIENTO CUANTITATIVO",
        id_departamento="11",
        cantidadevaluados=120,
        lag_1_promedio_global=158.4,
        lag_2_promedio_global=155.0,
        tendencia_global=1.7,
        nombre_institucion="UNIVERSIDAD NACIONAL",
        nombre_programa="INGENIERIA DE SISTEMAS",
    )

    print(format_prediction_report(result))

Warning:
    The pipeline expects features produced by Phase 3 (``features.build_features``).
    Passing raw or partially-engineered data to ``predict_batch`` will cause
    incorrect predictions or KeyErrors.  Always ensure that log-transformed
    cohort size (``log_cantidadevaluados``), lag features, and OHE columns
    (``cat_prueba_1``, ``cat_prueba_34``) are present or will be constructed
    by ``build_inference_row``.
"""

from __future__ import annotations

import os
import warnings
from datetime import datetime
from typing import Any, Optional

import joblib
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ── Constantes ────────────────────────────────────────────────────────────────

UMBRAL_MUESTRA_PEQUENA = 5
"""int: Minimum ``CANTIDADEVALUADOS`` before triggering the small-sample flag.

Programmes with fewer than 5 evaluated students have ``PROMEDIO_GLOBAL``
values that are highly sensitive to individual outlier scores.  A threshold
of 5 was chosen based on the outlier analysis documented in
``outputs/analisis_outliers.txt``.
"""

MAX_AÑO_TRAIN = 2023
"""int: Last year included in the training set.

Predictions for years beyond this value trigger the temporal extrapolation
flag.  The model was trained on data from 2020 through 2023 with 2024 as the
held-out test set.
"""

# Columnas que el pipeline LightGBM espera como entrada
NUMERIC_COLS = [
    "lag_1_promedio_global", "lag_2_promedio_global",
    "lag_1_promedio_prueba",  "lag_2_promedio_prueba",
    "tendencia_global",       "tendencia_prueba",
    "desviacion_estandar_historica", "coeficiente_variacion",
    "log_cantidadevaluados",  "AÑO",
]
"""list[str]: Numeric feature columns expected by the LightGBM Pipeline.

These are the same columns defined in ``NUMERIC_FEATURE_COLS`` in
``models/baseline.py``.  They are duplicated here so the inference module
has no import dependency on the training modules.
"""

CAT_COLS = ["NBC", "NOMBRE_PRUEBA", "ID_DEPARTAMENTO"]
"""list[str]: Categorical columns processed by the TargetEncoder inside the Pipeline."""

OHE_COLS = ["cat_prueba_1", "cat_prueba_34"]
"""list[str]: One-hot encoded columns derived from ``CATEGORIAPRUEBA`` in Phase 3."""

ALL_FEATURE_COLS = NUMERIC_COLS + CAT_COLS + OHE_COLS
"""list[str]: Complete ordered list of feature columns the trained Pipeline expects."""

# Mapeo de CATEGORIAPRUEBA a columnas OHE (derivado de Fase 3)
# cat_prueba_1 = CATEGORIAPRUEBA == 1, cat_prueba_34 = CATEGORIAPRUEBA in {3,4}
CATEGORIA_TO_OHE = {
    1:  {"cat_prueba_1": 1, "cat_prueba_34": 0},
    2:  {"cat_prueba_1": 0, "cat_prueba_34": 0},
    3:  {"cat_prueba_1": 0, "cat_prueba_34": 1},
    4:  {"cat_prueba_1": 0, "cat_prueba_34": 1},
}
"""dict: Mapping from integer ``CATEGORIAPRUEBA`` value to OHE column values.

Category 1 activates ``cat_prueba_1``; categories 3 and 4 jointly activate
``cat_prueba_34``; category 2 (the most common — generic Saber Pro component)
activates neither.  Unknown categories default to both zeros.
"""


# ── Carga del modelo ──────────────────────────────────────────────────────────

def load_model(model_path: str) -> Any:
    """Load a serialised LightGBM sklearn Pipeline from disk.

    Args:
        model_path: Path to the ``joblib``-serialised ``.pkl`` file produced
            by ``fase5_boosting.py`` (e.g. ``"outputs/lgbm_model.pkl"``).

    Returns:
        A fitted ``sklearn.pipeline.Pipeline`` whose steps are
        ``("preprocessor", ColumnTransformer)`` and ``("model", LGBMRegressor)``.

    Raises:
        FileNotFoundError: If no file exists at ``model_path``.  The error
            message includes a reminder to run ``fase5_boosting.py`` first.

    Example:
        >>> model = load_model("outputs/lgbm_model.pkl")
        >>> type(model).__name__
        'Pipeline'
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Modelo no encontrado en: {model_path}\n"
            "Ejecuta primero: python3 fase5_boosting.py"
        )
    pipeline = joblib.load(model_path)
    return pipeline


# ── Construcción de fila de features ─────────────────────────────────────────

def build_inference_row(
    año:                         int,
    nbc:                         str,
    nombre_prueba:               str,
    id_departamento:             Any,
    cantidadevaluados:           int,
    categoriaprueba:             int                 = 2,
    lag_1_promedio_global:       Optional[float]     = None,
    lag_2_promedio_global:       Optional[float]     = None,
    lag_1_promedio_prueba:       Optional[float]     = None,
    lag_2_promedio_prueba:       Optional[float]     = None,
    tendencia_global:            Optional[float]     = None,
    tendencia_prueba:            Optional[float]     = None,
    desviacion_estandar_historica: Optional[float]  = None,
    coeficiente_variacion:       Optional[float]     = None,
) -> pd.DataFrame:
    """Build a single-row feature DataFrame ready for the LightGBM Pipeline.

    Translates raw institutional inputs into the feature representation
    expected by the trained sklearn Pipeline.  ``cantidadevaluados`` is
    log-transformed (``log1p``) internally.  ``categoriaprueba`` is mapped to
    the two OHE binary columns via ``CATEGORIA_TO_OHE``.  All lag and trend
    values that are ``None`` are stored as ``NaN`` and will be imputed by
    the ``SimpleImputer(strategy="median")`` step inside the Pipeline.

    Args:
        año: Target prediction year (e.g. ``2025``).  Values greater than
            ``MAX_AÑO_TRAIN`` will trigger the extrapolation confidence flag
            in ``predict_institution``.
        nbc: Nucleo Basico del Conocimiento string (e.g. ``"INGENIERIA"``).
            Must match the values seen during training for accurate target
            encoding; unseen values receive the global mean encoding.
        nombre_prueba: Saber Pro component name (e.g.
            ``"RAZONAMIENTO CUANTITATIVO"``).
        id_departamento: Integer or string department ID.  Treated as a
            categorical variable by the Pipeline's TargetEncoder.
        cantidadevaluados: Number of students expected to sit the exam.
            Transformed to ``log1p(cantidadevaluados)`` before being passed
            to the model.
        categoriaprueba: Integer category of the exam component.  Valid values
            are ``1`` (generic), ``2`` (specific), ``3`` (generic with module),
            ``4`` (specific with module).  Defaults to ``2``.
        lag_1_promedio_global: ``PROMEDIO_GLOBAL`` from the previous year (t-1).
            Pass ``None`` if unavailable; the Pipeline will impute the training
            median.
        lag_2_promedio_global: ``PROMEDIO_GLOBAL`` from two years prior (t-2).
            Pass ``None`` if unavailable.
        lag_1_promedio_prueba: ``PROMEDIO_PRUEBA`` from the previous year (t-1).
            Pass ``None`` if unavailable.
        lag_2_promedio_prueba: ``PROMEDIO_PRUEBA`` from two years prior (t-2).
            Pass ``None`` if unavailable.
        tendencia_global: OLS slope of ``PROMEDIO_GLOBAL`` over historical
            years (computed by ``features._ols_slope``).  Pass ``None`` if
            the entity has fewer than 2 prior observations.
        tendencia_prueba: OLS slope of ``PROMEDIO_PRUEBA`` over historical
            years.  Pass ``None`` if unavailable.
        desviacion_estandar_historica: Historical standard deviation of
            ``PROMEDIO_GLOBAL`` up to t-1.  Pass ``None`` for new entities.
        coeficiente_variacion: Coefficient of variation of ``PROMEDIO_GLOBAL``
            up to t-1.  Pass ``None`` for new entities.

    Returns:
        A single-row ``pd.DataFrame`` with columns matching ``ALL_FEATURE_COLS``
        in the correct order.

    Example:
        >>> row = build_inference_row(
        ...     año=2025, nbc="INGENIERIA",
        ...     nombre_prueba="RAZONAMIENTO CUANTITATIVO",
        ...     id_departamento="11", cantidadevaluados=120,
        ...     lag_1_promedio_global=158.4,
        ... )
        >>> row.shape
        (1, 15)
        >>> row.columns.tolist()
        ['lag_1_promedio_global', ..., 'cat_prueba_34']
    """
    ohe = CATEGORIA_TO_OHE.get(categoriaprueba, {"cat_prueba_1": 0, "cat_prueba_34": 0})

    row = {
        # Numéricas
        "lag_1_promedio_global":        lag_1_promedio_global,
        "lag_2_promedio_global":        lag_2_promedio_global,
        "lag_1_promedio_prueba":         lag_1_promedio_prueba,
        "lag_2_promedio_prueba":         lag_2_promedio_prueba,
        "tendencia_global":              tendencia_global,
        "tendencia_prueba":              tendencia_prueba,
        "desviacion_estandar_historica": desviacion_estandar_historica,
        "coeficiente_variacion":         coeficiente_variacion,
        "log_cantidadevaluados":         np.log1p(cantidadevaluados),
        "AÑO":                           float(año),
        # Categóricas
        "NBC":                           str(nbc),
        "NOMBRE_PRUEBA":                 str(nombre_prueba),
        "ID_DEPARTAMENTO":               id_departamento,
        # OHE
        "cat_prueba_1":                  float(ohe["cat_prueba_1"]),
        "cat_prueba_34":                 float(ohe["cat_prueba_34"]),
    }

    return pd.DataFrame([row])


# ── Evaluación de flags de confianza ─────────────────────────────────────────

def _evaluate_confidence_flags(
    cantidadevaluados: int,
    lag_1_global:      Optional[float],
    año:               int,
) -> dict:
    """Evaluate the three confidence flags for a single prediction.

    Computes boolean flags for three independent sources of prediction
    uncertainty and derives an overall confidence level from their combination.

    Args:
        cantidadevaluados: Number of evaluated students.  Values below
            ``UMBRAL_MUESTRA_PEQUENA`` trigger the small-sample flag.
        lag_1_global: Prior-year ``PROMEDIO_GLOBAL`` value, or ``None`` /
            ``NaN`` if unavailable.  Absence triggers the no-history flag.
        año: Prediction year.  Values above ``MAX_AÑO_TRAIN`` trigger the
            temporal extrapolation flag.

    Returns:
        A dictionary with the following keys:

        - ``"baja_confianza_muestra_pequena"`` (bool): True when cohort is
          smaller than ``UMBRAL_MUESTRA_PEQUENA``.
        - ``"baja_confianza_sin_historial"`` (bool): True when lag_1 is
          unavailable.
        - ``"baja_confianza_extrapolacion"`` (bool): True when predicting
          beyond the training time horizon.
        - ``"confianza_global"`` (str): ``"ALTA"`` when no flags are set,
          ``"MEDIA"`` when exactly one non-sample-size flag is set, ``"BAJA"``
          in all other cases.
        - ``"advertencias"`` (list[str]): Human-readable explanations for
          each active flag.

    Example:
        >>> flags = _evaluate_confidence_flags(
        ...     cantidadevaluados=3, lag_1_global=None, año=2024
        ... )
        >>> flags["confianza_global"]
        'BAJA'
        >>> len(flags["advertencias"])
        2
    """
    flags = {
        "baja_confianza_muestra_pequeña": False,
        "baja_confianza_sin_historial":   False,
        "baja_confianza_extrapolacion":   False,
    }
    advertencias = []

    # Flag 1: Muestra pequeña — recomendado en analisis_outliers.txt
    if cantidadevaluados < UMBRAL_MUESTRA_PEQUENA:
        flags["baja_confianza_muestra_pequeña"] = True
        advertencias.append(
            f"CANTIDADEVALUADOS={cantidadevaluados} < {UMBRAL_MUESTRA_PEQUENA}. "
            f"Con muy pocos estudiantes evaluados el promedio del programa es "
            f"altamente sensible a valores individuales atípicos. "
            f"Revisar el outlier documentado en analisis_outliers.txt."
        )

    # Flag 2: Sin historial — no hay lag_1 disponible
    if lag_1_global is None or (isinstance(lag_1_global, float) and np.isnan(lag_1_global)):
        flags["baja_confianza_sin_historial"] = True
        advertencias.append(
            "lag_1_promedio_global no disponible. El modelo usará la mediana "
            "imputada del conjunto de entrenamiento. La predicción es menos "
            "precisa para programas sin historia previa."
        )

    # Flag 3: Extrapolación temporal — predicción fuera del rango de entrenamiento
    if año > MAX_AÑO_TRAIN:
        flags["baja_confianza_extrapolacion"] = True
        años_extra = año - MAX_AÑO_TRAIN
        advertencias.append(
            f"AÑO={año} está {años_extra} año(s) más allá del último año de "
            f"entrenamiento ({MAX_AÑO_TRAIN}). La precisión puede degradarse "
            f"si el sistema educativo cambia significativamente."
        )

    # Confianza global
    n_flags = sum(flags.values())
    if n_flags == 0:
        nivel = "ALTA"
    elif n_flags == 1 and not flags["baja_confianza_muestra_pequeña"]:
        nivel = "MEDIA"
    else:
        nivel = "BAJA"

    return {**flags, "confianza_global": nivel, "advertencias": advertencias}


# ── Función principal de predicción ──────────────────────────────────────────

def predict_institution(
    model:              Any,
    año:                int,
    nbc:                str,
    nombre_prueba:      str,
    id_departamento:    Any,
    cantidadevaluados:  int,
    categoriaprueba:    int              = 2,
    lag_1_promedio_global:       Optional[float] = None,
    lag_2_promedio_global:       Optional[float] = None,
    lag_1_promedio_prueba:       Optional[float] = None,
    lag_2_promedio_prueba:       Optional[float] = None,
    tendencia_global:            Optional[float] = None,
    tendencia_prueba:            Optional[float] = None,
    desviacion_estandar_historica: Optional[float] = None,
    coeficiente_variacion:       Optional[float] = None,
    nombre_institucion: Optional[str]    = None,
    nombre_programa:    Optional[str]    = None,
) -> dict:
    """Generate a PROMEDIO_GLOBAL prediction with confidence flags for one program-exam-year.

    This is the primary single-entity inference function.  It wraps
    ``build_inference_row``, ``model.predict``, and ``_evaluate_confidence_flags``
    into a single call that returns a fully structured result dictionary
    suitable for display, logging, or serialisation.

    Args:
        model: Fitted sklearn Pipeline loaded via ``load_model``.
        año: Prediction year (e.g. ``2025``).
        nbc: Nucleo Basico del Conocimiento (e.g. ``"CIENCIAS DE LA SALUD"``).
        nombre_prueba: Saber Pro component name (e.g. ``"INGLES"``).
        id_departamento: Department identifier (int or str).
        cantidadevaluados: Estimated number of students to be evaluated.
        categoriaprueba: Exam component category (1-4).  Defaults to ``2``.
        lag_1_promedio_global: PROMEDIO_GLOBAL from year t-1.
            Pass ``None`` if unknown.
        lag_2_promedio_global: PROMEDIO_GLOBAL from year t-2.
            Pass ``None`` if unknown.
        lag_1_promedio_prueba: PROMEDIO_PRUEBA from year t-1.
            Pass ``None`` if unknown.
        lag_2_promedio_prueba: PROMEDIO_PRUEBA from year t-2.
            Pass ``None`` if unknown.
        tendencia_global: OLS slope of PROMEDIO_GLOBAL history.
            Pass ``None`` for entities with fewer than 2 prior years.
        tendencia_prueba: OLS slope of PROMEDIO_PRUEBA history.
            Pass ``None`` if unknown.
        desviacion_estandar_historica: Historical std of PROMEDIO_GLOBAL.
            Pass ``None`` for new entities.
        coeficiente_variacion: CV of PROMEDIO_GLOBAL history.
            Pass ``None`` for new entities.
        nombre_institucion: Optional descriptive institution name included
            in the result for display purposes only (not used by the model).
        nombre_programa: Optional descriptive programme name included in the
            result for display purposes only.

    Returns:
        A dictionary containing:

        - ``"prediccion_promedio_global"`` (float): The model's predicted
          ``PROMEDIO_GLOBAL`` score.
        - ``"año"``, ``"nbc"``, ``"nombre_prueba"``, ``"id_departamento"``,
          ``"cantidadevaluados"``, ``"nombre_institucion"``,
          ``"nombre_programa"``: Input metadata echoed back.
        - ``"baja_confianza_muestra_pequeña"`` (bool): Small-sample flag.
        - ``"baja_confianza_sin_historial"`` (bool): No-history flag.
        - ``"baja_confianza_extrapolacion"`` (bool): Temporal extrapolation flag.
        - ``"confianza_global"`` (str): Overall confidence level
          (``"ALTA"``, ``"MEDIA"``, or ``"BAJA"``).
        - ``"advertencias"`` (list[str]): Human-readable flag explanations.
        - ``"features_usadas"`` (dict): The feature values passed to the model
          (useful for auditing and explainability).
        - ``"timestamp"`` (str): ISO 8601 timestamp of when the prediction was
          generated.

    Raises:
        ValueError: If the model pipeline raises an error during prediction
            (e.g. unexpected column type).

    Example:
        >>> model = load_model("outputs/lgbm_model.pkl")
        >>> result = predict_institution(
        ...     model=model, año=2025, nbc="INGENIERIA",
        ...     nombre_prueba="RAZONAMIENTO CUANTITATIVO",
        ...     id_departamento="11", cantidadevaluados=120,
        ...     lag_1_promedio_global=158.4,
        ... )
        >>> result["prediccion_promedio_global"]
        161.2
        >>> result["confianza_global"]
        'MEDIA'

    Note:
        For predictions on the 2024 test set the ``baja_confianza_extrapolacion``
        flag will be ``True`` because 2024 > ``MAX_AÑO_TRAIN`` (2023).  This is
        expected and does not indicate a bug; it is a deliberate design choice to
        flag all predictions beyond the training window regardless of how close
        they are to it.
    """
    # 1. Construir fila de features
    X = build_inference_row(
        año=año,
        nbc=nbc,
        nombre_prueba=nombre_prueba,
        id_departamento=id_departamento,
        cantidadevaluados=cantidadevaluados,
        categoriaprueba=categoriaprueba,
        lag_1_promedio_global=lag_1_promedio_global,
        lag_2_promedio_global=lag_2_promedio_global,
        lag_1_promedio_prueba=lag_1_promedio_prueba,
        lag_2_promedio_prueba=lag_2_promedio_prueba,
        tendencia_global=tendencia_global,
        tendencia_prueba=tendencia_prueba,
        desviacion_estandar_historica=desviacion_estandar_historica,
        coeficiente_variacion=coeficiente_variacion,
    )

    # 2. Predicción
    pred = float(model.predict(X)[0])

    # 3. Flags de confianza
    confidence = _evaluate_confidence_flags(
        cantidadevaluados=cantidadevaluados,
        lag_1_global=lag_1_promedio_global,
        año=año,
    )

    # 4. Features usadas (para auditoría / explicabilidad)
    features_dict = X.iloc[0].to_dict()

    return {
        "prediccion_promedio_global":    pred,
        "año":                           año,
        "nbc":                           nbc,
        "nombre_prueba":                 nombre_prueba,
        "id_departamento":               id_departamento,
        "cantidadevaluados":             cantidadevaluados,
        "nombre_institucion":            nombre_institucion,
        "nombre_programa":               nombre_programa,
        # Flags
        "baja_confianza_muestra_pequeña": confidence["baja_confianza_muestra_pequeña"],
        "baja_confianza_sin_historial":   confidence["baja_confianza_sin_historial"],
        "baja_confianza_extrapolacion":   confidence["baja_confianza_extrapolacion"],
        "confianza_global":               confidence["confianza_global"],
        "advertencias":                   confidence["advertencias"],
        # Auditoría
        "features_usadas":               features_dict,
        "timestamp":                     datetime.now().isoformat(),
    }


# ── Predicción en lote ────────────────────────────────────────────────────────

def predict_batch(
    df:    pd.DataFrame,
    model: Any,
) -> pd.DataFrame:
    """Generate predictions and confidence flags for all rows in a DataFrame.

    Vectorised version of ``predict_institution`` intended for scoring large
    DataFrames in a single pass.  If the OHE columns (``cat_prueba_1``,
    ``cat_prueba_34``) are absent from ``df``, they are added with a default
    value of 0.0 (equivalent to ``CATEGORIAPRUEBA == 2``).

    The confidence flags are computed element-wise using pandas operations
    rather than the scalar helper, making this function suitable for DataFrames
    of arbitrary size without a Python loop.

    Args:
        df: DataFrame whose rows represent program-exam-year entities to score.
            Must contain at minimum all columns in ``ALL_FEATURE_COLS``.
            ``CANTIDADEVALUADOS`` and ``AÑO`` are also required for confidence
            flag computation (they may overlap with ``ALL_FEATURE_COLS``).
        model: Fitted sklearn Pipeline loaded via ``load_model``.

    Returns:
        A copy of ``df`` with five new columns appended:

        - ``"prediccion_promedio_global"`` (float): Model prediction for each row.
        - ``"baja_confianza_muestra_pequeña"`` (bool): Vectorised small-sample flag.
        - ``"baja_confianza_sin_historial"`` (bool): Vectorised no-history flag.
        - ``"baja_confianza_extrapolacion"`` (bool): Vectorised extrapolation flag.
        - ``"confianza_global"`` (str): Overall confidence level per row.

    Raises:
        KeyError: If any column in ``ALL_FEATURE_COLS`` is absent from ``df``
            (and not one of the OHE columns auto-filled with 0.0).

    Example:
        >>> model = load_model("outputs/lgbm_model.pkl")
        >>> df_test_feats = df_feat[df_feat["AÑO"] == 2024].copy()
        >>> df_scored = predict_batch(df_test_feats, model)
        >>> df_scored[["NOMBRE_PRUEBA", "prediccion_promedio_global",
        ...             "confianza_global"]].head()

    Note:
        ``predict_batch`` does not generate per-row ``advertencias`` text.
        Use ``predict_institution`` when a human-readable explanation of each
        flag is required (e.g. for dashboard tooltips or API responses).
    """
    df = df.copy()

    # Asegurar columnas OHE si no están (ej. input limpio sin OHE pre-calculado)
    if "cat_prueba_1" not in df.columns:
        df["cat_prueba_1"] = 0.0
    if "cat_prueba_34" not in df.columns:
        df["cat_prueba_34"] = 0.0

    # Predicciones
    X = df[ALL_FEATURE_COLS]
    preds = model.predict(X)
    df["prediccion_promedio_global"] = preds

    # Flags de confianza vectorizados
    cant = df["CANTIDADEVALUADOS"] if "CANTIDADEVALUADOS" in df.columns else pd.Series(
        [UMBRAL_MUESTRA_PEQUENA] * len(df), index=df.index
    )
    lag1 = df.get("lag_1_promedio_global", pd.Series([np.nan] * len(df), index=df.index))
    año_col = df["AÑO"] if "AÑO" in df.columns else pd.Series([MAX_AÑO_TRAIN] * len(df))

    df["baja_confianza_muestra_pequeña"] = cant < UMBRAL_MUESTRA_PEQUENA
    df["baja_confianza_sin_historial"]   = lag1.isna()
    df["baja_confianza_extrapolacion"]   = año_col > MAX_AÑO_TRAIN

    # Nivel de confianza global
    n_flags = (
        df["baja_confianza_muestra_pequeña"].astype(int)
        + df["baja_confianza_sin_historial"].astype(int)
        + df["baja_confianza_extrapolacion"].astype(int)
    )
    df["confianza_global"] = np.where(
        n_flags == 0, "ALTA",
        np.where(
            (n_flags == 1) & (~df["baja_confianza_muestra_pequeña"]),
            "MEDIA",
            "BAJA"
        )
    )

    return df


# ── Helpers de formato ────────────────────────────────────────────────────────

def format_prediction_report(result: dict) -> str:
    """Format the output of predict_institution as a human-readable text report.

    Produces a fixed-width text block summarising the prediction, its
    confidence level, all active warning flags, and a timestamp.  Long
    warning messages are word-wrapped to 56 characters.

    Args:
        result: Dictionary returned by ``predict_institution``.  Must contain
            at minimum the keys ``"prediccion_promedio_global"``,
            ``"confianza_global"``, ``"advertencias"``, and ``"timestamp"``.

    Returns:
        A multi-line string suitable for printing to stdout or writing to a
        log file.  Lines are separated by ``"\\n"``.

    Example:
        >>> model = load_model("outputs/lgbm_model.pkl")
        >>> result = predict_institution(model=model, año=2025,
        ...     nbc="INGENIERIA", nombre_prueba="INGLES",
        ...     id_departamento="11", cantidadevaluados=80)
        >>> print(format_prediction_report(result))
        ============================================================
        PREDICCION MOTOR SABER PRO
        ============================================================
        NBC          : INGENIERIA
        ...
        PROMEDIO_GLOBAL predicho : 155.32
        Confianza global         : MEDIA
        ...
    """
    flag_si_no = lambda b: "SÍ ⚠" if b else "no"

    lines = [
        "=" * 60,
        "PREDICCIÓN MOTOR SABER PRO",
        "=" * 60,
    ]
    if result.get("nombre_institucion"):
        lines.append(f"Institución  : {result['nombre_institucion']}")
    if result.get("nombre_programa"):
        lines.append(f"Programa     : {result['nombre_programa']}")
    lines += [
        f"NBC          : {result['nbc']}",
        f"Prueba       : {result['nombre_prueba']}",
        f"Año          : {result['año']}",
        f"N evaluados  : {result['cantidadevaluados']}",
        "",
        f"PROMEDIO_GLOBAL predicho : {result['prediccion_promedio_global']:.2f}",
        f"Confianza global         : {result['confianza_global']}",
        "",
        "Flags de confianza:",
        f"  Muestra pequeña (N<{UMBRAL_MUESTRA_PEQUENA}): "
            f"{flag_si_no(result['baja_confianza_muestra_pequeña'])}",
        f"  Sin historial previo:   "
            f"{flag_si_no(result['baja_confianza_sin_historial'])}",
        f"  Extrapolación temporal: "
            f"{flag_si_no(result['baja_confianza_extrapolacion'])}",
    ]
    if result["advertencias"]:
        lines.append("")
        lines.append("Advertencias:")
        for i, adv in enumerate(result["advertencias"], 1):
            # Wrap a 56 chars
            words = adv.split()
            line, wrapped = [], []
            for w in words:
                if sum(len(x) + 1 for x in line) + len(w) > 54:
                    wrapped.append("  " + " ".join(line))
                    line = [w]
                else:
                    line.append(w)
            if line:
                wrapped.append("  " + " ".join(line))
            lines.append(f"  [{i}] {wrapped[0].strip()}")
            for l in wrapped[1:]:
                lines.append(f"      {l.strip()}")

    lines += ["", f"Timestamp: {result['timestamp']}", "=" * 60]
    return "\n".join(lines)
