"""
fase4_baseline.py
Split temporal estricto + entrenamiento Ridge y Lasso.
Fase 4 del pipeline — Motor Predictivo Saber Pro.
Autor: Edwin Santiago Paz Bedoya — Código 1071010
"""

import os
import sys
import warnings
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import pandas as pd
import numpy as np
import joblib

warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from sklearn.model_selection import TimeSeriesSplit

from src.models.baseline import (
    TARGET_COL, get_feature_columns, train_lasso, train_ridge,
)
from src.evaluation import (
    compute_metrics, compute_metrics_by_group,
    plot_pred_vs_real, plot_residuals, plot_error_by_group, plot_lasso_coefs,
)

OUTPUTS_METRICS  = os.path.join(BASE_DIR, "outputs", "metrics")
OUTPUTS_FIGURES  = os.path.join(BASE_DIR, "outputs", "figures")
OUTPUTS_REPORTS  = os.path.join(BASE_DIR, "outputs", "reports")
PROCESSED_DIR    = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(OUTPUTS_METRICS,  exist_ok=True)
os.makedirs(OUTPUTS_FIGURES,  exist_ok=True)
os.makedirs(OUTPUTS_REPORTS,  exist_ok=True)


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


# ── 1. Carga del dataset con features ────────────────────────────────────────
log("=== FASE 4: SPLIT TEMPORAL + BASELINE LINEAL ===")
feat_path = os.path.join(PROCESSED_DIR, "saber_pro_features.csv")
df = pd.read_csv(feat_path, low_memory=False)
log(f"Dataset cargado: {len(df):,} filas x {df.shape[1]} columnas")
log(f"Años disponibles: {sorted(df['AÑO'].unique().tolist())}")

# ── 2. Split temporal estricto ────────────────────────────────────────────────
# Train: 2020–2023  |  Test: 2024 (año más reciente)
# NUNCA split aleatorio en datos temporales → data leakage temporal garantizado.
YEAR_TEST = 2024
log(f"\nSplit temporal: TRAIN = años < {YEAR_TEST}  |  TEST = {YEAR_TEST}")

df_train = df[df["AÑO"] < YEAR_TEST].copy()
df_test  = df[df["AÑO"] == YEAR_TEST].copy()

log(f"  Train: {len(df_train):,} filas | años: {sorted(df_train['AÑO'].unique().tolist())}")
log(f"  Test : {len(df_test):,} filas  | año : {sorted(df_test['AÑO'].unique().tolist())}")
log(f"  Split ratio: {100*len(df_test)/(len(df_train)+len(df_test)):.1f}% test")

# Verificar que no haya entidades del test que ya aparezcan en train (esperado: muchas)
train_entities = set(zip(df_train["ID_INSTITUCION"], df_train["ID_PROGRAMA_ACAD"], df_train["NOMBRE_PRUEBA"]))
test_entities  = set(zip(df_test["ID_INSTITUCION"],  df_test["ID_PROGRAMA_ACAD"],  df_test["NOMBRE_PRUEBA"]))
overlap = train_entities & test_entities
log(f"  Entidades presentes en ambos conjuntos: {len(overlap):,} (tienen lags disponibles)")
log(f"  Entidades nuevas en test (sin historia): {len(test_entities - train_entities):,}")

# ── 3. Preparar X, y ─────────────────────────────────────────────────────────
num_cols, cat_cols, ohe_cols = get_feature_columns(df_train)
all_feature_cols = num_cols + cat_cols + ohe_cols

X_train = df_train[all_feature_cols]
y_train = df_train[TARGET_COL].astype(float)
X_test  = df_test[all_feature_cols]
y_test  = df_test[TARGET_COL].astype(float)

log(f"\nFeatures usadas: {len(all_feature_cols)}")
log(f"  Numéricas   : {len(num_cols)}")
log(f"  Target-enc  : {len(cat_cols)}  → {cat_cols}")
log(f"  OHE (pass)  : {len(ohe_cols)}")
log(f"  TARGET      : {TARGET_COL}")

# ── 4. TimeSeriesSplit para CV interno ───────────────────────────────────────
# TimeSeriesSplit sobre train asegura que el CV respete el orden temporal
N_SPLITS = 4  # 4 splits sobre 4 años de train (2020-2023) → aproximadamente un año por fold
tscv = TimeSeriesSplit(n_splits=N_SPLITS)
log(f"\nTimeSeriesSplit: {N_SPLITS} folds sobre datos de train (orden cronológico)")

# ── 5. Entrenamiento Ridge ────────────────────────────────────────────────────
log("\n--- RIDGE ---")
log("Entrenando RidgeCV con TimeSeriesSplit...")
ridge_result = train_ridge(X_train, y_train, X_test, y_test, tscv)
log(f"  Alpha elegido por CV: {ridge_result['alpha']:.6f}")

ridge_metrics_train = compute_metrics(y_train.values, ridge_result["y_pred_train"], "Ridge_train")
ridge_metrics_test  = compute_metrics(y_test.values,  ridge_result["y_pred_test"],  "Ridge")
log(f"  TRAIN → RMSE={ridge_metrics_train['RMSE']:.4f}  MAE={ridge_metrics_train['MAE']:.4f}  R²={ridge_metrics_train['R2']:.4f}")
log(f"  TEST  → RMSE={ridge_metrics_test['RMSE']:.4f}  MAE={ridge_metrics_test['MAE']:.4f}  R²={ridge_metrics_test['R2']:.4f}")

# ── 6. Entrenamiento Lasso ────────────────────────────────────────────────────
log("\n--- LASSO ---")
log("Entrenando LassoCV con TimeSeriesSplit...")
lasso_result = train_lasso(X_train, y_train, X_test, y_test, tscv)
log(f"  Alpha elegido por CV: {lasso_result['alpha']:.6f}")
log(f"  Features seleccionadas: {lasso_result['n_selected']} / {lasso_result['n_total']}")
log(f"  Top 10 features por |coeficiente|:")
top_coefs = sorted(lasso_result["coefs"].items(), key=lambda x: abs(x[1]), reverse=True)[:10]
for name, coef in top_coefs:
    log(f"    {name:<35}: {coef:+.4f}")

lasso_metrics_train = compute_metrics(y_train.values, lasso_result["y_pred_train"], "Lasso_train")
lasso_metrics_test  = compute_metrics(y_test.values,  lasso_result["y_pred_test"],  "Lasso")
log(f"  TRAIN → RMSE={lasso_metrics_train['RMSE']:.4f}  MAE={lasso_metrics_train['MAE']:.4f}  R²={lasso_metrics_train['R2']:.4f}")
log(f"  TEST  → RMSE={lasso_metrics_test['RMSE']:.4f}  MAE={lasso_metrics_test['MAE']:.4f}  R²={lasso_metrics_test['R2']:.4f}")

# ── 7. Métricas desagregadas ─────────────────────────────────────────────────
log("\nCalculando métricas desagregadas...")

for model_name, y_pred in [("Ridge", ridge_result["y_pred_test"]),
                            ("Lasso", lasso_result["y_pred_test"])]:
    # Por NBC
    if "NBC" in df_test.columns:
        m_nbc = compute_metrics_by_group(y_test, y_pred, df_test["NBC"], model_name)
        m_nbc.to_csv(os.path.join(OUTPUTS_METRICS, f"metricas_{model_name.lower()}_por_nbc.csv"),
                     index=False)
    # Por departamento
    if "NOMBRE_DEPARTAMENTO" in df_test.columns:
        m_dep = compute_metrics_by_group(y_test, y_pred, df_test["NOMBRE_DEPARTAMENTO"], model_name)
        m_dep.to_csv(os.path.join(OUTPUTS_METRICS, f"metricas_{model_name.lower()}_por_depto.csv"),
                     index=False)

# ── 8. Tabla comparativa de métricas ─────────────────────────────────────────
metrics_rows = [ridge_metrics_test, lasso_metrics_test]
metrics_df = pd.DataFrame(metrics_rows)
metrics_df.to_csv(os.path.join(OUTPUTS_METRICS, "baseline_metrics.csv"), index=False)
log(f"\nTabla comparativa:")
log(f"  {'Modelo':<12} {'RMSE':>8} {'MAE':>8} {'R²':>8}")
log(f"  {'-'*40}")
for _, row in metrics_df.iterrows():
    log(f"  {row['modelo']:<12} {row['RMSE']:>8.4f} {row['MAE']:>8.4f} {row['R2']:>8.4f}")

# ── 9. Gráficos ───────────────────────────────────────────────────────────────
log("\nGenerando gráficos...")

# 9a. Predicho vs real — Ridge
plot_pred_vs_real(
    y_test.values, ridge_result["y_pred_test"], "Ridge",
    ridge_metrics_test,
    os.path.join(OUTPUTS_FIGURES, "baseline_ridge_predicho_vs_real.png"),
)

# 9b. Predicho vs real — Lasso
plot_pred_vs_real(
    y_test.values, lasso_result["y_pred_test"], "Lasso",
    lasso_metrics_test,
    os.path.join(OUTPUTS_FIGURES, "baseline_lasso_predicho_vs_real.png"),
)

# 9c. Residuos — Ridge
plot_residuals(
    y_test.values, ridge_result["y_pred_test"], "Ridge",
    os.path.join(OUTPUTS_FIGURES, "baseline_ridge_residuos.png"),
)

# 9d. Residuos — Lasso
plot_residuals(
    y_test.values, lasso_result["y_pred_test"], "Lasso",
    os.path.join(OUTPUTS_FIGURES, "baseline_lasso_residuos.png"),
)

# 9e. Error por departamento — Ridge (solo si hay datos)
if "NOMBRE_DEPARTAMENTO" in df_test.columns:
    m_dep_ridge = compute_metrics_by_group(
        y_test, ridge_result["y_pred_test"], df_test["NOMBRE_DEPARTAMENTO"], "Ridge"
    )
    plot_error_by_group(
        m_dep_ridge, "Ridge", "Departamento",
        os.path.join(OUTPUTS_FIGURES, "baseline_error_por_depto.png"),
    )

# 9f. Coeficientes Lasso
if lasso_result["n_selected"] > 0:
    plot_lasso_coefs(
        lasso_result["coefs"],
        os.path.join(OUTPUTS_FIGURES, "baseline_coeficientes_lasso.png"),
    )

log("  Figuras exportadas.")

# ── 10. Guardar pipelines ─────────────────────────────────────────────────────
joblib.dump(ridge_result["pipeline"], os.path.join(BASE_DIR, "outputs", "ridge_model.pkl"))
joblib.dump(lasso_result["pipeline"], os.path.join(BASE_DIR, "outputs", "lasso_model.pkl"))
log("\nPipelines guardados en outputs/")

# ── 11. Narrativa metodológica ────────────────────────────────────────────────
top5_lasso = [name for name, _ in top_coefs[:5]]
lasso_selected_names = [n for n, c in lasso_result["coefs"].items() if abs(c) > 1e-10]

narrativa = f"""NARRATIVA METODOLÓGICA — MODELOS BASELINE (RIDGE Y LASSO)
Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
============================================================

SPLIT TEMPORAL
  Estrategia: split estricto por año (nunca aleatorio en series temporales).
  Train: años 2020–2023 ({len(df_train):,} observaciones).
  Test:  año 2024 ({len(df_test):,} observaciones, {100*len(df_test)/(len(df_train)+len(df_test)):.1f}% del total).
  Justificación: un split aleatorio en datos temporales introduce leakage temporal
  al permitir que observaciones futuras informen el entrenamiento. Al usar el año
  más reciente como test se simula la tarea de predicción real: dado el histórico
  hasta 2023, predecir el desempeño de 2024.

PREPROCESAMIENTO (dentro del Pipeline)
  - Variables numéricas: imputación por mediana + StandardScaler.
  - Variables categóricas (NBC, NOMBRE_PRUEBA, ID_DEPARTAMENTO): TargetEncoder
    de scikit-learn, calculado únicamente sobre datos de train en cada fold
    de TimeSeriesSplit (N={N_SPLITS} folds). Esto garantiza que las targets del
    conjunto de test no influyan en el encoding durante el entrenamiento.
  - Variables OHE (CATEGORIAPRUEBA): passthrough (ya codificadas en Fase 3).
  - Validación cruzada interna: TimeSeriesSplit({N_SPLITS} folds) sobre train,
    respetando el orden cronológico en la selección de hiperparámetros.

MODELO RIDGE
  Se evaluó Ridge Regression con regularización L2. La constante de
  regularización alpha se eligió mediante RidgeCV con búsqueda en 60 valores
  logarítmicamente espaciados entre 1e-3 y 1e5.
  Alpha óptimo: {ridge_result['alpha']:.6f}
  Ridge obtuvo RMSE={ridge_metrics_test['RMSE']} y R²={ridge_metrics_test['R2']} en el
  conjunto de prueba, con MAE={ridge_metrics_test['MAE']} puntos en la escala Saber Pro.

MODELO LASSO
  Se evaluó Lasso Regression con regularización L1, que actúa simultáneamente
  como selector de features al llevar coeficientes irrelevantes exactamente a cero.
  Alpha óptimo: {lasso_result['alpha']:.6f}
  Lasso seleccionó {lasso_result['n_selected']} de {lasso_result['n_total']} features disponibles.
  Features seleccionadas: {lasso_selected_names}
  Lasso obtuvo RMSE={lasso_metrics_test['RMSE']} y R²={lasso_metrics_test['R2']} en el
  conjunto de prueba, con MAE={lasso_metrics_test['MAE']} puntos.
  Los features más influyentes según Lasso fueron: {top5_lasso}

CONCLUSIÓN
  Los modelos lineales regularizados establecen el piso de referencia
  (RMSE_baseline = {min(ridge_metrics_test['RMSE'], lasso_metrics_test['RMSE']):.4f}).
  El mejor modelo lineal fue {'Ridge' if ridge_metrics_test['RMSE'] <= lasso_metrics_test['RMSE'] else 'Lasso'}
  con RMSE={min(ridge_metrics_test['RMSE'], lasso_metrics_test['RMSE']):.4f}.
  Todo modelo no lineal entrenado en las siguientes fases deberá superar
  este umbral en el conjunto de prueba para justificar su mayor complejidad.
"""

narrativa_path = os.path.join(OUTPUTS_REPORTS, "narrativa_baseline.txt")
with open(narrativa_path, "w", encoding="utf-8") as f:
    f.write(narrativa)
log(f"Narrativa exportada: {narrativa_path}")

# ── 12. Resumen final ─────────────────────────────────────────────────────────
log("")
log("=" * 60)
log("RESUMEN FASE 4 — BASELINE LINEAL")
log("=" * 60)
log(f"  Split: TRAIN 2020-2023 ({len(df_train):,})  |  TEST 2024 ({len(df_test):,})")
log(f"  Features totales: {len(all_feature_cols)}")
log(f"  {'Modelo':<10} {'RMSE':>8} {'MAE':>8} {'R²':>8}")
log(f"  {'-'*36}")
for _, row in metrics_df.iterrows():
    log(f"  {row['modelo']:<10} {row['RMSE']:>8.4f} {row['MAE']:>8.4f} {row['R2']:>8.4f}")
log(f"\n  RMSE de referencia para LightGBM: "
    f"{min(ridge_metrics_test['RMSE'], lasso_metrics_test['RMSE']):.4f}")
log("")
log("Artefactos generados:")
log(f"  outputs/metrics/baseline_metrics.csv")
log(f"  outputs/figures/baseline_ridge_predicho_vs_real.png")
log(f"  outputs/figures/baseline_lasso_predicho_vs_real.png")
log(f"  outputs/figures/baseline_ridge_residuos.png")
log(f"  outputs/figures/baseline_lasso_residuos.png")
log(f"  outputs/figures/baseline_error_por_depto.png")
log(f"  outputs/figures/baseline_coeficientes_lasso.png")
log(f"  outputs/reports/narrativa_baseline.txt")
log(f"  outputs/ridge_model.pkl")
log(f"  outputs/lasso_model.pkl")
log("")

print()
print('FASE 4 COMPLETADA -- Revisa los resultados anteriores y escribe "ok" para continuar con la Fase 5.')
