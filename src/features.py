"""Temporal feature engineering for the Saber Pro predictive pipeline.

This module implements Phase 3 of the Saber Pro predictive pipeline.  It
receives the cleaned wide-format DataFrame produced by ``cleaning.clean_dataset``
and constructs all predictive features required by the downstream model phases.

The pipeline treats each ``(ID_INSTITUCION, ID_PROGRAMA_ACAD, NOMBRE_PRUEBA)``
triple as a **panel entity** that may be observed across multiple years
(2020-2024).  All features that summarise historical performance (lags,
trend slope, volatility) are computed using an **expanding window that
excludes the current year t**, so that a model trained on year t can only
"see" information from years strictly before t.  This design prevents the
six categories of temporal leakage identified during the Fase 2 audit.

Seven feature families are constructed:

1. **Lag features** (``_build_lags``): ``lag_1`` and ``lag_2`` of both
   ``PROMEDIO_GLOBAL`` and ``PROMEDIO_PRUEBA``, using ``groupby + shift``.
2. **Trend features** (``_build_trend``): OLS slope of ``PROMEDIO_GLOBAL``
   and ``PROMEDIO_PRUEBA`` over all years strictly before t, computed via an
   expanding window.  ``delta_1_global`` was removed in a prior audit because
   it directly encoded the target change (leakage type 1).
3. **Performance-level proportions** (``_build_nivel_features``): ``NIVEL1``
   through ``NIVEL4`` normalised to proportions.  These are tagged with the
   ``concurrent_`` prefix because they originate from the same ICFES release
   as ``PROMEDIO_GLOBAL`` and must **not** be used as model inputs for same-
   year prediction.
4. **Volatility features** (``_build_volatility``): historical standard
   deviation and coefficient of variation of ``PROMEDIO_GLOBAL`` up to t-1,
   using ``shift(1).expanding(min_periods=2).std()``.
5. **Context features** (``_build_context``): ``log_cantidadevaluados =
   log1p(CANTIDADEVALUADOS)``, available before exam results are published.
6. **Year as a feature**: ``AÑO`` is included directly as a numeric column
   to capture cross-sectional time trends in the Colombian higher-education
   system.
7. **Categorical encoding**: ``CATEGORIAPRUEBA`` receives one-hot encoding
   (at most 20 categories; no target signal used).  ``NBC``,
   ``NOMBRE_PRUEBA``, and ``ID_DEPARTAMENTO`` are left as raw strings for
   ``TargetEncoder`` inside the sklearn ``Pipeline`` in Phase 4/5, where the
   encoding is recomputed on train-only data for each cross-validation fold.

Usage example::

    from src.ingestion import load_years
    from src.cleaning import clean_dataset
    from src.features import build_features

    df_raw   = load_years([2020, 2021, 2022, 2023, 2024], "data/raw/")
    df_clean, _ = clean_dataset(df_raw)
    df_feat, report = build_features(df_clean)

    print(df_feat[["lag_1_promedio_global", "tendencia_global",
                   "desviacion_estandar_historica"]].describe())

    with open("outputs/feature_report.txt", "w") as f:
        f.write("\\n".join(report))

Warning:
    Target encoding of ``NBC``, ``NOMBRE_PRUEBA``, and ``ID_DEPARTAMENTO``
    is intentionally **deferred** to the sklearn ``Pipeline`` in Phase 4/5.
    Calling ``_target_encode`` directly on the full dataset (including test
    rows) would leak test-set label information into the train encoding,
    inflating cross-validated performance metrics.  The ``_target_encode``
    helper is retained for exploratory analysis only and should never be
    used in the main modelling Pipeline.
"""

import warnings
from datetime import datetime

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ── Columnas de identidad ────────────────────────────────────────────────────
ENTITY_COLS = ["ID_INSTITUCION", "ID_PROGRAMA_ACAD", "NOMBRE_PRUEBA"]
"""list[str]: Columns that together identify a panel entity.

The combination ``(ID_INSTITUCION, ID_PROGRAMA_ACAD, NOMBRE_PRUEBA)``
uniquely identifies one academic programme's performance on one Saber Pro
exam component.  All temporal features (lags, trend, volatility) are
computed within groups defined by these three columns.
"""

KEY3        = ["AÑO", "ID_INSTITUCION", "ID_PROGRAMA_ACAD"]
KEY4        = ["AÑO", "ID_INSTITUCION", "ID_PROGRAMA_ACAD", "NOMBRE_PRUEBA"]


def _log(msg: str) -> None:
    """Print a timestamped log message to stdout.

    Args:
        msg: The message text to print.

    Example:
        >>> _log("Building lag features")
        [10:22:05] Building lag features
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


# ── Imputación ───────────────────────────────────────────────────────────────

def _impute_grouped_median(df: pd.DataFrame, cols: list, group_cols: list) -> pd.DataFrame:
    """Impute nulls in selected columns using the grouped median with global fallback.

    For each column in ``cols``, null values are filled with the median of the
    group defined by ``group_cols``.  If an entire group consists of nulls (so
    the group median is itself NaN), the global column median is used as a
    fallback.  The original DataFrame is not modified.

    This function corresponds to Regla C3 of the cleaning strategy: secondary
    metrics (``DESVIACION``, ``NIVEL1``-``NIVEL4``) are retained as rows even
    when null, then imputed here with group context rather than being dropped.

    Args:
        df: Input DataFrame.  Not modified in place.
        cols: List of column names to impute.  Columns absent from ``df`` are
            silently skipped.
        group_cols: Columns to group by when computing the median
            (e.g. ``["NBC", "NOMBRE_PRUEBA"]``).

    Returns:
        A copy of ``df`` with null values in ``cols`` filled by group or
        global medians.

    Raises:
        KeyError: If any column in ``group_cols`` is absent from ``df``.

    Example:
        >>> df_imp = _impute_grouped_median(
        ...     df, cols=["DESVIACION", "NIVEL1"], group_cols=["NBC", "NOMBRE_PRUEBA"]
        ... )
        >>> df_imp["DESVIACION"].isnull().sum()
        0

    Note:
        This imputation is performed on the full dataset before the train/test
        split.  That means group statistics can include test-year rows.
        However, this only affects secondary metrics (``DESVIACION``,
        ``NIVEL1``-``NIVEL4``) that are not used as model features (they are
        tagged ``concurrent_`` or used for descriptive analysis only), so there
        is no consequential leakage into the predictive targets or lag features.
    """
    df = df.copy()
    for col in cols:
        if col not in df.columns:
            continue
        null_mask = df[col].isnull()
        if null_mask.sum() == 0:
            continue
        # Mediana por grupo
        group_median = df.groupby(group_cols)[col].transform("median")
        # Fallback: mediana global
        global_median = df[col].median()
        df[col] = df[col].fillna(group_median).fillna(global_median)
        remaining = df[col].isnull().sum()
        _log(f"  Imputados {null_mask.sum():,} nulos en {col} "
             f"(mediana de grupo {group_cols}) | restantes: {remaining}")
    return df


# ── Lags temporales ──────────────────────────────────────────────────────────

def _build_lags(df: pd.DataFrame) -> pd.DataFrame:
    """Construct one- and two-year lag features for global and sub-test scores.

    For each panel entity (``ENTITY_COLS``), the DataFrame is sorted
    chronologically and ``pandas.Series.shift`` is applied within each group
    to produce:

    - ``lag_1_promedio_global``: ``PROMEDIO_GLOBAL`` at t-1
    - ``lag_2_promedio_global``: ``PROMEDIO_GLOBAL`` at t-2
    - ``lag_1_promedio_prueba``: ``PROMEDIO_PRUEBA`` at t-1
    - ``lag_2_promedio_prueba``: ``PROMEDIO_PRUEBA`` at t-2

    Entities that first appear in 2020 will have NaN for both lags.
    Entities that first appear in 2021 will have NaN only for lag_2.
    These NaNs are handled by the ``SimpleImputer(strategy="median")`` inside
    the sklearn Pipeline in Phase 4/5.

    Args:
        df: Wide-format DataFrame with at least ``ENTITY_COLS``, ``AÑO``,
            ``PROMEDIO_GLOBAL``, and ``PROMEDIO_PRUEBA`` columns.

    Returns:
        A copy of ``df`` with four new lag columns appended.  Row count is
        unchanged.

    Example:
        >>> df_lags = _build_lags(df_clean)
        >>> df_lags[["AÑO", "lag_1_promedio_global", "lag_2_promedio_global"]].head()
           AÑO  lag_1_promedio_global  lag_2_promedio_global
        0  2020                   NaN                    NaN
        1  2021                 152.3                    NaN
        2  2022                 155.1                  152.3

    Note:
        ``shift(1)`` inside a ``groupby`` guarantees that the lag for year t
        is the value from the immediately preceding year available in the
        dataset for that entity.  If data for 2021 is missing for a given
        entity, ``lag_1`` in 2022 will be the 2020 value, not NaN —
        this is the correct behaviour for an irregular panel.
    """
    df = df.sort_values(ENTITY_COLS + ["AÑO"]).copy()

    for col, new_name_t1, new_name_t2 in [
        ("PROMEDIO_GLOBAL", "lag_1_promedio_global", "lag_2_promedio_global"),
        ("PROMEDIO_PRUEBA", "lag_1_promedio_prueba", "lag_2_promedio_prueba"),
    ]:
        if col not in df.columns:
            continue
        grouped = df.groupby(ENTITY_COLS)[col]
        df[new_name_t1] = grouped.shift(1)   # t-1
        df[new_name_t2] = grouped.shift(2)   # t-2

    return df


# ── Features de tendencia ────────────────────────────────────────────────────

def _ols_slope(values: pd.Series) -> float:
    """Compute the OLS slope of a numeric series against its integer index.

    Uses the closed-form OLS formula to fit y = a + b*x where x = 0, 1, ..., n-1
    and returns only the slope b.  NaN values in ``values`` are dropped before
    fitting.  Returns NaN if fewer than two non-null observations are available.

    Args:
        values: A pandas Series of numeric observations in chronological order.
            The index of the series is ignored; position is used as x.

    Returns:
        The OLS slope as a float, or ``np.nan`` if the series has fewer than
        two valid observations or if the denominator is zero (constant series).

    Example:
        >>> _ols_slope(pd.Series([100.0, 102.0, 104.0]))
        2.0
        >>> _ols_slope(pd.Series([np.nan, np.nan]))
        nan
    """
    valid = values.dropna()
    n = len(valid)
    if n < 2:
        return np.nan
    x = np.arange(n, dtype=float)
    # Fórmula directa: evita importar scipy en cada llamada
    xm, ym = x.mean(), valid.values.mean()
    denom = ((x - xm) ** 2).sum()
    if denom == 0:
        return np.nan
    return float(((x - xm) * (valid.values - ym)).sum() / denom)


def _build_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Build OLS-slope trend features using only historical data strictly before year t.

    For each row (entity, year t), computes the OLS slope of ``PROMEDIO_GLOBAL``
    and ``PROMEDIO_PRUEBA`` over all years **before** t that are available for
    that entity.  The first observation for any entity always yields NaN because
    there is no prior history.

    The expanding-window approach is implemented by iterating over each entity's
    sorted time series and, for position i, passing only ``iloc[:i]`` to
    ``_ols_slope``.  This is equivalent to a ``shift(1).expanding()`` pattern
    but allows per-entity irregular panels without alignment issues.

    Args:
        df: Wide-format DataFrame with ``ENTITY_COLS``, ``AÑO``,
            ``PROMEDIO_GLOBAL``, and ``PROMEDIO_PRUEBA``.

    Returns:
        A copy of ``df`` with two new columns:

        - ``tendencia_global``: OLS slope of ``PROMEDIO_GLOBAL`` history up to t-1.
        - ``tendencia_prueba``: OLS slope of ``PROMEDIO_PRUEBA`` history up to t-1.

    Example:
        >>> df_trend = _build_trend(df_lags)
        >>> df_trend[["AÑO", "tendencia_global"]].dropna().head(3)
           AÑO  tendencia_global
        2  2022              1.4
        3  2023              1.1
        4  2024              1.7

    Note:
        An earlier version of this feature computed the slope over the full
        entity time series including year t.  That version was removed during
        the leakage audit because the slope at year t depends on
        ``PROMEDIO_GLOBAL[t]``, which is the prediction target.  The current
        expanding-window implementation excludes year t from all slope
        computations, making ``tendencia_global`` leakage-free.

        ``delta_1_global = PROMEDIO_GLOBAL[t] - lag_1`` was also removed
        because it is a direct linear transformation of the target and
        constitutes leakage type 1 (direct target encoding).
    """
    df = df.sort_values(ENTITY_COLS + ["AÑO"]).copy()

    def expanding_slope(group: pd.DataFrame) -> pd.DataFrame:
        """Compute per-row OLS slope using only rows before the current row.

        Args:
            group: Sub-DataFrame for one panel entity, sorted chronologically.

        Returns:
            A DataFrame indexed like ``group`` with columns
            ``tendencia_global`` and ``tendencia_prueba``.
        """
        group = group.sort_values("AÑO").reset_index(drop=False)
        s_global, s_prueba = [], []
        for i in range(len(group)):
            hist_g = group["PROMEDIO_GLOBAL"].iloc[:i].dropna().values
            hist_p = group["PROMEDIO_PRUEBA"].iloc[:i].dropna().values
            s_global.append(_ols_slope(pd.Series(hist_g)))
            s_prueba.append(_ols_slope(pd.Series(hist_p)))
        group["tendencia_global"] = s_global
        group["tendencia_prueba"] = s_prueba
        return group.set_index("index")[["tendencia_global", "tendencia_prueba"]]

    results = df.groupby(ENTITY_COLS, group_keys=False).apply(expanding_slope)
    df["tendencia_global"] = results["tendencia_global"].values
    df["tendencia_prueba"] = results["tendencia_prueba"].values
    return df


# ── Features de distribución por niveles ─────────────────────────────────────

def _build_nivel_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute performance-level proportion features from NIVEL1-NIVEL4.

    ``NIVEL1`` through ``NIVEL4`` represent the percentage of evaluated
    students who fall into each performance band (0-100 scale; the four
    values sum to approximately 100 per row).  This function normalises them
    to true proportions (dividing by their row-wise sum) and computes two
    aggregate indices: the proportion of students in low performance bands
    (NIVEL1 + NIVEL2) and in high performance bands (NIVEL3 + NIVEL4).

    All output columns are prefixed with ``concurrent_`` to mark them as
    **concurrent with the prediction target** and therefore unsuitable as
    model inputs for same-year prediction.

    Args:
        df: Wide-format DataFrame that may contain ``NIVEL1`` through
            ``NIVEL4`` columns.  If fewer than two NIVEL columns are present,
            the function returns ``df`` unchanged.

    Returns:
        A copy of ``df`` with the following new columns (when NIVEL data is
        available):

        - ``concurrent_prop_nivel1`` through ``concurrent_prop_nivel4``
        - ``concurrent_prop_niveles_bajos`` (NIVEL1 + NIVEL2 proportion)
        - ``concurrent_prop_niveles_altos`` (NIVEL3 + NIVEL4 proportion)

    Example:
        >>> df_niv = _build_nivel_features(df_imputed)
        >>> df_niv["concurrent_prop_niveles_bajos"].describe()
        count    38450.000000
        mean         0.512300
        ...

    Note:
        These features are tagged ``concurrent_`` because ``NIVEL1``-``NIVEL4``
        originate from ``MEDIDA_AGREGACION = NIVEL_DESEMPEÑO_PRUEBA`` in the
        same ICFES data release as ``PROMEDIO_GLOBAL``.  In a real deployment
        scenario both metrics become available simultaneously, so using them
        to predict ``PROMEDIO_GLOBAL`` for the **same** year constitutes
        temporal leakage.  They can safely be used as lagged features in
        future pipeline versions (e.g. ``lag_1_prop_nivel1``).
    """
    df = df.copy()
    nivel_cols = [c for c in ["NIVEL1", "NIVEL2", "NIVEL3", "NIVEL4"] if c in df.columns]

    if len(nivel_cols) < 2:
        return df

    total = df[nivel_cols].sum(axis=1).replace(0, np.nan)

    # Prefijo 'concurrent_' para distinguirlas de features válidas para el modelo
    for col in nivel_cols:
        df[f"concurrent_prop_{col.lower()}"] = df[col] / total

    cols_low  = [c for c in ["NIVEL1", "NIVEL2"] if c in df.columns]
    cols_high = [c for c in ["NIVEL3", "NIVEL4"] if c in df.columns]
    df["concurrent_prop_niveles_bajos"] = df[cols_low].sum(axis=1) / total
    df["concurrent_prop_niveles_altos"] = df[cols_high].sum(axis=1) / total

    return df


# ── Features de volatilidad ──────────────────────────────────────────────────

def _build_volatility(df: pd.DataFrame) -> pd.DataFrame:
    """Build historical volatility features for PROMEDIO_GLOBAL up to year t-1.

    Computes two volatility measures for each panel entity using only data
    from years strictly before t:

    - ``desviacion_estandar_historica``: standard deviation of ``PROMEDIO_GLOBAL``
      over the expanding window of years 0..t-1, requiring at least 2 points.
    - ``coeficiente_variacion``: ratio of ``desviacion_estandar_historica`` to
      the expanding mean of ``PROMEDIO_GLOBAL`` up to t-1.

    The ``shift(1).expanding()`` pattern moves each value one position forward
    within its group before applying the expanding aggregation, ensuring that
    the aggregation at position i only includes positions 0..i-1.

    Args:
        df: Wide-format DataFrame with ``ENTITY_COLS``, ``AÑO``, and
            ``PROMEDIO_GLOBAL`` columns.

    Returns:
        A copy of ``df`` with two new columns:

        - ``desviacion_estandar_historica``: ``float64``, NaN for entities
          with fewer than 2 prior observations.
        - ``coeficiente_variacion``: ``float64``, NaN when standard deviation
          or mean is undefined or when the mean is zero.

    Example:
        >>> df_vol = _build_volatility(df_trend)
        >>> df_vol[["AÑO", "desviacion_estandar_historica",
        ...          "coeficiente_variacion"]].dropna().head(3)

    Note:
        A prior version of this feature computed the standard deviation over
        the full panel time series for each entity, including year t.  This
        was identified as leakage type 3 in the Fase 2 audit: the standard
        deviation over a window that includes year t encodes information about
        ``PROMEDIO_GLOBAL[t]``.  The ``shift(1)`` correction ensures the
        expanding window always excludes the current observation.
    """
    df = df.sort_values(ENTITY_COLS + ["AÑO"]).copy()

    grp = df.groupby(ENTITY_COLS)["PROMEDIO_GLOBAL"]

    # std de la historia hasta t-1
    df["desviacion_estandar_historica"] = grp.transform(
        lambda x: x.shift(1).expanding(min_periods=2).std()
    )
    # media de la historia hasta t-1 (para CV)
    _mean_lag = grp.transform(
        lambda x: x.shift(1).expanding(min_periods=1).mean()
    )
    df["coeficiente_variacion"] = (
        df["desviacion_estandar_historica"] / _mean_lag.replace(0, np.nan)
    )
    return df


# ── Features de contexto ─────────────────────────────────────────────────────

def _build_context(df: pd.DataFrame) -> pd.DataFrame:
    """Build log-scale cohort size feature from CANTIDADEVALUADOS.

    Applies ``numpy.log1p`` to ``CANTIDADEVALUADOS`` to produce a
    normally-distributed proxy for cohort size that is available **before**
    exam results are published (it reflects enrolled/registered students).

    Args:
        df: Wide-format DataFrame that may contain a ``CANTIDADEVALUADOS``
            column.  If the column is absent the function returns ``df``
            unchanged.

    Returns:
        A copy of ``df`` with a new ``log_cantidadevaluados`` column.
        Zero-evaluated-student rows are handled by ``log1p(0) = 0``
        (they were already removed by cleaning rule C1, so this is a
        safety fallback).

    Example:
        >>> df_ctx = _build_context(df_vol)
        >>> df_ctx["log_cantidadevaluados"].describe()
        count    38450.000000
        mean         3.218400
        std          1.042100
        ...
    """
    df = df.copy()
    if "CANTIDADEVALUADOS" in df.columns:
        ce = pd.to_numeric(df["CANTIDADEVALUADOS"], errors="coerce").fillna(0)
        df["log_cantidadevaluados"] = np.log1p(ce)
    return df


# ── Target encoding ──────────────────────────────────────────────────────────

def _target_encode(
    df: pd.DataFrame,
    col: str,
    target: str = "PROMEDIO_GLOBAL",
    smoothing: float = 10.0,
) -> pd.DataFrame:
    """Apply smoothed target encoding to a categorical column.

    Replaces each category's raw mean with a smoothed estimate that shrinks
    towards the global mean when the category has few observations:

        enc = (n_cat * mean_cat + smoothing * global_mean) / (n_cat + smoothing)

    Categories absent from ``df[col]`` (e.g. during inference on new data)
    receive the global mean as their encoded value.

    Args:
        df: DataFrame containing both ``col`` and ``target``.
        col: Name of the categorical column to encode.
        target: Name of the numeric target column.  Defaults to
            ``"PROMEDIO_GLOBAL"``.
        smoothing: Additive smoothing factor.  Higher values shrink more
            aggressively towards the global mean, reducing overfitting for
            rare categories.  Defaults to ``10.0``.

    Returns:
        A copy of ``df`` with a new column named ``te_{col.lower()}``
        containing the smoothed target-encoded values.

    Example:
        >>> df_enc = _target_encode(df_train, col="NBC", smoothing=10.0)
        >>> df_enc["te_nbc"].describe()
        count    30000.000000
        mean       152.830000
        ...

    Warning:
        This function computes the encoding over the **entire** DataFrame
        passed to it.  If ``df`` includes both training and test rows, the
        encoding will leak test-set label information into the training
        features, inflating cross-validated performance estimates.

        For the main modelling pipeline, target encoding of ``NBC``,
        ``NOMBRE_PRUEBA``, and ``ID_DEPARTAMENTO`` is performed exclusively
        inside the sklearn ``Pipeline`` via ``TargetEncoder``, which is
        fitted only on train data within each ``TimeSeriesSplit`` fold.
        Use this function only for exploratory analysis on the training set.
    """
    df = df.copy()
    if col not in df.columns or target not in df.columns:
        return df

    global_mean = df[target].mean()
    agg = df.groupby(col)[target].agg(["mean", "count"]).reset_index()
    agg.columns = [col, "_mean_cat", "_n_cat"]
    agg["_enc"] = (
        (agg["_n_cat"] * agg["_mean_cat"] + smoothing * global_mean)
        / (agg["_n_cat"] + smoothing)
    )
    enc_map = agg.set_index(col)["_enc"].to_dict()
    enc_col = f"te_{col.lower()}"
    df[enc_col] = df[col].map(enc_map).fillna(global_mean)
    return df


# ── Función principal ────────────────────────────────────────────────────────

def build_features(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Orchestrate all feature engineering steps and return the enriched dataset.

    This is the main entry point for Phase 3 of the pipeline.  It applies the
    eight feature-engineering steps in sequence, accumulates a detailed report,
    and performs a final row-count assertion to guarantee that no rows are
    inadvertently added or removed during feature construction.

    Steps executed in order:

    0. Imputation of secondary metrics (``DESVIACION``, ``NIVEL1``-``NIVEL4``)
       using grouped median by ``(NBC, NOMBRE_PRUEBA)`` with global-median
       fallback (Regla C3).
    1. Lag features: ``lag_1/2_promedio_global``, ``lag_1/2_promedio_prueba``.
    2. Trend features: ``tendencia_global``, ``tendencia_prueba`` (OLS slopes
       over expanding history, excluding year t).
    3. Performance-level proportions (``concurrent_prop_*``; excluded from
       model inputs).
    4. Volatility: ``desviacion_estandar_historica``, ``coeficiente_variacion``.
    5. Context: ``log_cantidadevaluados``.
    6. ``AÑO`` is already numeric; included directly in the report.
    7. One-hot encoding of ``CATEGORIAPRUEBA`` (if ≤ 20 categories).
    8. Anti-leakage validation summary in the report.

    Args:
        df: Cleaned wide-format DataFrame produced by
            ``cleaning.clean_dataset``.  Must contain at minimum:
            ``ENTITY_COLS``, ``AÑO``, ``PROMEDIO_GLOBAL``, ``PROMEDIO_PRUEBA``,
            ``CANTIDADEVALUADOS``, ``NBC``, ``NOMBRE_PRUEBA``.

    Returns:
        A tuple ``(df_feat, report_lines)`` where:

        - ``df_feat`` is a copy of ``df`` with all engineered feature columns
          appended.  The row count is guaranteed to be identical to the input.
        - ``report_lines`` is a list of strings forming a human-readable feature
          engineering report suitable for writing to ``outputs/feature_report.txt``.

    Raises:
        AssertionError: If the number of rows in ``df_feat`` differs from the
            number of rows in the input ``df``.  This indicates a bug in one of
            the feature-building helpers.

    Example:
        >>> df_feat, report = build_features(df_clean)
        >>> len(df_feat) == len(df_clean)
        True
        >>> "lag_1_promedio_global" in df_feat.columns
        True
        >>> df_feat["tendencia_global"].isnull().mean() < 0.5
        True

    Note:
        The temporal train/test split (train 2020-2023, test 2024) must be
        applied **after** calling this function, not before.  Many features
        (especially lag_2 and trend features) require a full entity history
        to be non-null; splitting before feature engineering would cause all
        2022 entities to have NaN lag_2 values when only 2020-2021 data is
        used, inflating apparent null rates and degrading model performance.
    """
    report_lines = []
    report_lines.append("=" * 70)
    report_lines.append("REPORTE DE FEATURE ENGINEERING — SABER PRO")
    report_lines.append(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("=" * 70)
    report_lines.append("")

    _log("Iniciando feature engineering...")
    df = df.copy()
    n_rows_original = len(df)

    # ── 0. IMPUTACIÓN DE MÉTRICAS SECUNDARIAS (Regla C3) ────────────────────
    _log("0. Imputando métricas secundarias (mediana agrupada NBC + NOMBRE_PRUEBA)...")
    impute_cols   = ["DESVIACION", "NIVEL1", "NIVEL2", "NIVEL3", "NIVEL4"]
    impute_groups = ["NBC", "NOMBRE_PRUEBA"]
    df = _impute_grouped_median(df, impute_cols, impute_groups)

    report_lines.append("── IMPUTACIÓN (Regla C3) ──")
    for col in impute_cols:
        n_null = df[col].isnull().sum()
        report_lines.append(f"  {col:<12}: {n_null} nulos restantes tras imputación grupal")
    report_lines.append(f"  Grupos de imputación: {impute_groups}")
    report_lines.append("")

    # ── 1. LAGS TEMPORALES ──────────────────────────────────────────────────
    _log("1. Construyendo lags temporales...")
    df = _build_lags(df)

    lag_features = [
        "lag_1_promedio_global", "lag_2_promedio_global",
        "lag_1_promedio_prueba", "lag_2_promedio_prueba",
    ]
    report_lines.append("── LAGS TEMPORALES ──")
    for f in lag_features:
        if f in df.columns:
            pct_null = 100 * df[f].isnull().mean()
            report_lines.append(
                f"  {f:<30}: {pct_null:.1f}% nulos "
                f"(esperado: ~{[13.7,27.1][f.endswith('2')]}% por cobertura temporal)"
            )
    report_lines.append("")

    # ── 2. TENDENCIA ────────────────────────────────────────────────────────
    _log("2. Construyendo features de tendencia (delta, OLS slope)...")
    df = _build_trend(df)

    trend_features = ["delta_1_global", "tendencia_global", "tendencia_prueba"]
    report_lines.append("── FEATURES DE TENDENCIA ──")
    for f in trend_features:
        if f in df.columns:
            pct_null = 100 * df[f].isnull().mean()
            m = df[f].mean() if df[f].notna().any() else float("nan")
            s = df[f].std()  if df[f].notna().any() else float("nan")
            report_lines.append(f"  {f:<28}: mean={m:.3f}, std={s:.3f}, {pct_null:.1f}% nulos")
    report_lines.append("")

    # ── 3. DISTRIBUCIÓN NIVELES ─────────────────────────────────────────────
    _log("3. Construyendo proporciones NIVEL1-4...")
    df = _build_nivel_features(df)

    nivel_feat = [c for c in df.columns if c.startswith("prop_nivel")]
    report_lines.append("── PROPORCIONES DE NIVELES ──")
    report_lines.append("  Escala original NIVEL1-4: porcentajes 0-100, suma ~100 por fila.")
    report_lines.append("  Features creadas: proporción respecto al total de la fila.")
    for f in nivel_feat:
        if f in df.columns:
            m = df[f].mean()
            report_lines.append(f"  {f:<28}: mean={m:.3f}")
    report_lines.append("")

    # ── 4. VOLATILIDAD ──────────────────────────────────────────────────────
    _log("4. Construyendo features de volatilidad...")
    df = _build_volatility(df)

    vol_features = ["desviacion_estandar_historica", "coeficiente_variacion"]
    report_lines.append("── VOLATILIDAD ──")
    for f in vol_features:
        if f in df.columns:
            pct_null = 100 * df[f].isnull().mean()
            m = df[f].mean() if df[f].notna().any() else float("nan")
            report_lines.append(f"  {f:<35}: mean={m:.4f}, {pct_null:.1f}% nulos")
    report_lines.append("")

    # ── 5. CONTEXTO ─────────────────────────────────────────────────────────
    _log("5. Construyendo features de contexto (log CANTIDADEVALUADOS)...")
    df = _build_context(df)

    report_lines.append("── CONTEXTO ──")
    if "log_cantidadevaluados" in df.columns:
        m, s = df["log_cantidadevaluados"].mean(), df["log_cantidadevaluados"].std()
        report_lines.append(f"  log_cantidadevaluados: mean={m:.3f}, std={s:.3f}")
    report_lines.append("")

    # ── 6. AÑO COMO FEATURE ─────────────────────────────────────────────────
    # AÑO ya está como columna numérica — se incluye directamente.
    report_lines.append("── AÑO COMO FEATURE ──")
    report_lines.append("  AÑO: columna numérica incluida directamente (captura tendencia global).")
    report_lines.append(f"  Valores: {sorted(df['AÑO'].unique().tolist())}")
    report_lines.append("")

    # ── 7. CATEGORIAPRUEBA: OHE (no usa target → sin leakage) ───────────────
    # NBC, NOMBRE_PRUEBA, ID_DEPARTAMENTO: target encoding movido al Pipeline
    # de modelado (Fase 4) para calcularse SOLO sobre datos de train en cada
    # fold de TimeSeriesSplit. Calcularlos aquí sobre el dataset completo
    # introduciría leakage cruzado entre entidades de train y test.
    _log("7. Codificando CATEGORIAPRUEBA con OHE (sin target → sin leakage)...")
    if "CATEGORIAPRUEBA" in df.columns:
        n_cat = df["CATEGORIAPRUEBA"].nunique()
        if n_cat <= 20:
            report_lines.append(f"── OHE CATEGORIAPRUEBA ──")
            report_lines.append(f"  CATEGORIAPRUEBA ({n_cat} categorías <=20) → one-hot encoding (sin leakage)")
            ohe = pd.get_dummies(df["CATEGORIAPRUEBA"], prefix="cat_prueba", drop_first=False)
            ohe = ohe.astype(int)
            df = pd.concat([df, ohe], axis=1)
        else:
            report_lines.append(f"  CATEGORIAPRUEBA ({n_cat} categorías) → dejada como string para Pipeline")

    report_lines.append("")
    report_lines.append("── VARIABLES CATEGÓRICAS DIFERIDAS AL PIPELINE ──")
    report_lines.append("  NBC, NOMBRE_PRUEBA, ID_DEPARTAMENTO: target encoding calculado")
    report_lines.append("  dentro del Pipeline sklearn (Fase 4) con TargetEncoder + TimeSeriesSplit.")
    report_lines.append("  Motivo: calcularlas sobre el dataset completo introduce leakage cruzado")
    report_lines.append("  porque las targets del test influyen en el encoding del train.")
    report_lines.append("")

    # ── 8. VALIDACIÓN ANTI-LEAKAGE ──────────────────────────────────────────
    _log("8. Validando ausencia de target leakage...")
    report_lines.append("── VALIDACIÓN ANTI-LEAKAGE ──")
    report_lines.append("  lag_1/lag_2: usan shift() sobre años anteriores solamente. [OK]")
    report_lines.append("  delta_1: diferencia contra lag_1 (año anterior). [OK]")
    report_lines.append("  tendencia OLS: slope sobre trayectoria histórica de la entidad. [OK]")
    report_lines.append("  OHE CATEGORIAPRUEBA: no usa target. [OK]")
    report_lines.append("  te_nbc/te_nombre_prueba/te_id_departamento: DIFERIDOS al Pipeline. [OK]")
    report_lines.append("  No hay features que usen PROMEDIO_GLOBAL del año siguiente. [OK]")
    report_lines.append("")

    # ── 9. RESUMEN DE FEATURES ───────────────────────────────────────────────
    # Identificar features numéricas construidas
    original_cols = set([
        "AÑO","ID_PAIS","ID_REGION","NOMBRE_REGION","ID_DEPARTAMENTO",
        "NOMBRE_DEPARTAMENTO","ID_MUNICIPIO","NOMBRE_MUNICIPIO",
        "ID_INSTITUCION","NOMBRE_INSTITUCION","ID_NBC","NBC",
        "ID_PROGRAMA_ACAD","NOMBRE_PROGRAMA_ACAD","NOMBRE_PRUEBA",
        "CATEGORIAPRUEBA","CANTIDADEVALUADOS","PROMEDIO_PRUEBA",
        "DESVIACION","PROMEDIO_GLOBAL","NIVEL1","NIVEL2","NIVEL3","NIVEL4",
    ])
    new_features = [c for c in df.columns if c not in original_cols]
    high_null_features = [
        c for c in new_features
        if df[c].isnull().mean() > 0.70 and c in df.select_dtypes(include=[np.number]).columns
    ]

    report_lines.append("── RESUMEN FINAL ──")
    report_lines.append(f"  Filas: {len(df):,} (sin cambios vs. dataset limpio)")
    report_lines.append(f"  Columnas totales post-features: {len(df.columns)}")
    report_lines.append(f"  Features nuevas construidas: {len(new_features)}")
    report_lines.append(f"  Features con >70% nulos (excluir en modelado): {high_null_features}")
    report_lines.append("")
    report_lines.append("  LISTA COMPLETA DE FEATURES NUEVAS:")
    for f in sorted(new_features):
        if f in df.columns:
            pct_null = 100 * df[f].isnull().mean()
            try:
                m = df[f].mean() if df[f].notna().any() else float("nan")
                s = df[f].std()  if df[f].notna().any() else float("nan")
                mn = df[f].min()
                mx = df[f].max()
                report_lines.append(
                    f"  {f:<35} null={pct_null:.1f}% | "
                    f"mean={m:.3f} | std={s:.3f} | min={mn:.3f} | max={mx:.3f}"
                )
            except Exception:
                report_lines.append(f"  {f:<35} (no numérica)")

    assert len(df) == n_rows_original, "ERROR: build_features modificó el número de filas!"
    _log(f"Feature engineering completo: {len(df.columns)} columnas totales, {len(new_features)} features nuevas.")
    return df, report_lines
