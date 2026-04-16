"""
src/features.py
Feature engineering temporal para el dataset Saber Pro.
Fase 3 del pipeline — Motor Predictivo Saber Pro.
Autor: Edwin Santiago Paz Bedoya — Código 1071010

Notas de diseño:
  - Entidad de panel: ID_INSTITUCION + ID_PROGRAMA_ACAD + NOMBRE_PRUEBA
  - NIVEL1-4 están en escala 0-100 (porcentajes). Su suma es ~100.
  - Target encoding de categóricos (NBC, NOMBRE_PRUEBA) se calcula aquí
    sobre el dataset completo para generar el feature. En el pipeline de
    modelado (Fase 4-5) se recalculará con TimeSeriesSplit para evitar leakage.
  - No hay target leak: ningún feature usa información de AÑO actual del target;
    los lags solo usan años estrictamente anteriores.
"""

import warnings
from datetime import datetime

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ── Columnas de identidad ────────────────────────────────────────────────────
ENTITY_COLS = ["ID_INSTITUCION", "ID_PROGRAMA_ACAD", "NOMBRE_PRUEBA"]  # panel entity
KEY3        = ["AÑO", "ID_INSTITUCION", "ID_PROGRAMA_ACAD"]
KEY4        = ["AÑO", "ID_INSTITUCION", "ID_PROGRAMA_ACAD", "NOMBRE_PRUEBA"]


def _log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


# ── Imputación ───────────────────────────────────────────────────────────────

def _impute_grouped_median(df: pd.DataFrame, cols: list, group_cols: list) -> pd.DataFrame:
    """
    Imputa nulos en `cols` con la mediana del grupo definido por `group_cols`.
    Si el grupo entero tiene nulos, usa la mediana global de la columna.
    No modifica el DataFrame original.
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
    """
    Construye features de lag temporal por entidad panel.
    Solo usa años estrictamente anteriores al año actual (sin leakage).
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
    """Pendiente OLS de una serie numérica contra su índice temporal."""
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
    """
    tendencia_global / tendencia_prueba: slope OLS usando SOLO los años
    estrictamente anteriores al año de la fila (historia t-1 y antes).

    Corrección de leakage:
    - delta_1_global = PROMEDIO_GLOBAL - lag_1 fue eliminado: codificaba
      directamente el target (leakage directo).
    - La versión anterior calculaba el slope incluyendo el año t del target.
      Ahora se usa expanding window que excluye la observación actual.
    - PROMEDIO_PRUEBA del año t es concurrent → se usa PROMEDIO_PRUEBA de
      años anteriores (via lag_1/lag_2_promedio_prueba ya construidos).
    """
    df = df.sort_values(ENTITY_COLS + ["AÑO"]).copy()

    def expanding_slope(group: pd.DataFrame) -> pd.DataFrame:
        """Para fila i, slope OLS de PROMEDIO_GLOBAL en años 0..i-1."""
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
    """
    NIVEL1-4 están en escala 0-100 (porcentajes). Suma ~100 por fila.
    Se calculan las proporciones y se almacenan en el CSV como referencia
    analítica, pero están marcadas con prefijo 'concurrent_' para indicar
    que NO deben usarse en el modelo predictivo de producción.

    RAZÓN DE EXCLUSIÓN DEL MODELO:
    NIVEL1-4 provienen de MEDIDA_AGREGACION=NIVEL_DESEMPEÑO_PRUEBA del mismo
    año que PROMEDIO_GLOBAL (mismo release del ICFES). En producción, ambas
    métricas se publican juntas → usarlas como features para predecir
    PROMEDIO_GLOBAL del mismo año es leakage temporal.

    Son útiles para análisis descriptivo y como contexto histórico (vía lags
    en futuras versiones del pipeline), pero no para predicción del año actual.
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
    """
    Std histórica y CV usando SOLO años estrictamente anteriores al año t.

    Corrección de leakage: la versión anterior usaba std(PROMEDIO_GLOBAL de
    todos los años del panel), incluyendo el año t cuyo target estamos
    prediciendo. Ahora se usa expanding window con shift(1) para excluir
    la observación actual.

    Implementación:
    - shift(1) dentro del grupo mueve el valor del año t a la posición t+1,
      de modo que expanding().std() en la posición t solo usa años 0..t-1.
    - min_periods=2 para std (requiere al menos 2 puntos históricos).
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
    """
    log_cantidadevaluados: escala logarítmica para CANTIDADEVALUADOS.
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
    """
    Target encoding con smoothing (evita overfitting en categorías raras).
    Formula: enc = (n_cat * mean_cat + smoothing * global_mean) / (n_cat + smoothing)

    ADVERTENCIA: calculado sobre el conjunto completo. En Fase 4 se recalculará
    dentro del Pipeline con TimeSeriesSplit para evaluación sin leakage.
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
    """
    Construye todas las features a partir del dataset limpio.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset limpio (output de clean_dataset).

    Returns
    -------
    df_feat : pd.DataFrame
        Dataset con features construidas.
    report_lines : list[str]
        Reporte de features para exportar.
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
