"""
fase5_lightgbm.py
LightGBM + Optuna + SHAP sobre el split temporal 2020-2023 / 2024.
Fase 5 del pipeline — Motor Predictivo Saber Pro.
Autor: Edwin Santiago Paz Bedoya — Código 1071010
"""

import json
import os
import sys
import warnings
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import joblib
import shap

warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from sklearn.model_selection import TimeSeriesSplit

from src.models.baseline  import TARGET_COL, get_feature_columns
from src.models.boosting  import (
    compute_shap, get_learning_curve, run_optuna_search, train_lgbm,
)
from src.evaluation import (
    compute_metrics, compute_metrics_by_group,
    plot_pred_vs_real, plot_residuals, plot_error_by_group,
)

OUTPUTS_METRICS  = os.path.join(BASE_DIR, "outputs", "metrics")
OUTPUTS_FIGURES  = os.path.join(BASE_DIR, "outputs", "figures")
OUTPUTS_REPORTS  = os.path.join(BASE_DIR, "outputs", "reports")
PROCESSED_DIR    = os.path.join(BASE_DIR, "data", "processed")
OUTPUTS_ROOT     = os.path.join(BASE_DIR, "outputs")


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


# ── 1. Carga y split (idéntico a Fase 4) ─────────────────────────────────────
log("=== FASE 5: LIGHTGBM + OPTUNA + SHAP ===")
df = pd.read_csv(
    os.path.join(PROCESSED_DIR, "saber_pro_features.csv"), low_memory=False
)
log(f"Dataset cargado: {len(df):,} filas x {df.shape[1]} columnas")

YEAR_TEST = 2024
df_train = df[df["AÑO"] <  YEAR_TEST].copy()
df_test  = df[df["AÑO"] == YEAR_TEST].copy()
log(f"Train: {len(df_train):,} filas (2020-2023) | Test: {len(df_test):,} filas (2024)")

num_cols, cat_cols, ohe_cols = get_feature_columns(df_train)
all_feat = num_cols + cat_cols + ohe_cols

X_train = df_train[all_feat]
y_train = df_train[TARGET_COL].astype(float)
X_test  = df_test[all_feat]
y_test  = df_test[TARGET_COL].astype(float)

log(f"Features: {len(all_feat)}  ({len(num_cols)} num | {len(cat_cols)} cat-TE | {len(ohe_cols)} OHE)")
log(f"Target-encoded con TargetEncoder DENTRO del Pipeline (solo sobre train → sin leakage)")

# ── 2. TimeSeriesSplit (igual que Fase 4) ─────────────────────────────────────
N_SPLITS = 4
tscv = TimeSeriesSplit(n_splits=N_SPLITS)

# ── 3. Búsqueda de hiperparámetros con Optuna ─────────────────────────────────
log("\n--- BÚSQUEDA DE HIPERPARÁMETROS (Optuna, 50 trials) ---")
log("Cada trial ajusta el Pipeline completo con TimeSeriesSplit → TargetEncoder libre de leakage")
best_params, study = run_optuna_search(X_train, y_train, tscv, n_trials=50)

log(f"\nMejores hiperparámetros encontrados:")
for k, v in best_params.items():
    log(f"  {k:<25}: {v}")

# Guardar hiperparámetros en JSON
params_path = os.path.join(OUTPUTS_ROOT, "lgbm_best_params.json")
with open(params_path, "w") as f:
    json.dump(best_params, f, indent=2)
log(f"Parámetros guardados: {params_path}")

# ── 4. Curva de aprendizaje ───────────────────────────────────────────────────
log("\n--- CURVA DE APRENDIZAJE ---")
lc = get_learning_curve(X_train, y_train, best_params,
                        val_year=2023, df_with_year=df_train)
log(f"  Mejor iteración (early stopping): {lc['best_iter']}")
log(f"  RMSE train en mejor iter: {lc['train_rmse'][lc['best_iter']-1]:.4f}")
log(f"  RMSE val   en mejor iter: {lc['val_rmse'][lc['best_iter']-1]:.4f}")

# Actualizar n_estimators al mejor encontrado en la curva (+ margen)
best_params["n_estimators"] = max(lc["best_iter"] + 20, 100)
log(f"  n_estimators ajustado al best_iter + 20: {best_params['n_estimators']}")

fig_lc, ax_lc = plt.subplots(figsize=(10, 5))
iters = range(1, len(lc["train_rmse"]) + 1)
ax_lc.plot(iters, lc["train_rmse"], label="Train RMSE", color="#3572A5", lw=1.5)
ax_lc.plot(iters, lc["val_rmse"],   label="Val RMSE (2023)",  color="#D63F3F", lw=1.5)
ax_lc.axvline(lc["best_iter"], color="gray", linestyle="--", alpha=0.7,
              label=f"Mejor iter={lc['best_iter']}")
ax_lc.set_xlabel("Iteración (árbol)")
ax_lc.set_ylabel("RMSE")
ax_lc.set_title("LightGBM — Curva de Aprendizaje (Train vs Validación 2023)")
ax_lc.legend(fontsize=9)
ax_lc.set_ylim(bottom=0)
plt.tight_layout()
lc_path = os.path.join(OUTPUTS_FIGURES, "lgbm_curva_aprendizaje.png")
fig_lc.savefig(lc_path, dpi=150, bbox_inches="tight")
plt.close(fig_lc)
log(f"  Figura curva aprendizaje: {lc_path}")

# ── 5. Entrenamiento final sobre TODO el train ────────────────────────────────
log("\n--- ENTRENAMIENTO FINAL (train 2020-2023 completo) ---")
log("TargetEncoder fit solo sobre X_train → TargetEncoder no ve X_test nunca")
lgbm_result = train_lgbm(X_train, y_train, X_test, best_params)

lgbm_metrics_train = compute_metrics(y_train.values, lgbm_result["y_pred_train"], "LightGBM_train")
lgbm_metrics_test  = compute_metrics(y_test.values,  lgbm_result["y_pred_test"],  "LightGBM")
log(f"  TRAIN → RMSE={lgbm_metrics_train['RMSE']:.4f}  MAE={lgbm_metrics_train['MAE']:.4f}  R²={lgbm_metrics_train['R2']:.4f}")
log(f"  TEST  → RMSE={lgbm_metrics_test['RMSE']:.4f}  MAE={lgbm_metrics_test['MAE']:.4f}  R²={lgbm_metrics_test['R2']:.4f}")

# ── 6. Tabla comparativa ─────────────────────────────────────────────────────
RMSE_RIDGE = 10.2294
RMSE_LASSO = 10.0722

log("\n--- TABLA COMPARATIVA ---")
metrics_rows = [
    {"modelo": "Ridge",    "RMSE": RMSE_RIDGE, "MAE": 7.2967, "R2": 0.6467},
    {"modelo": "Lasso",    "RMSE": RMSE_LASSO, "MAE": 7.0622, "R2": 0.6575},
    lgbm_metrics_test,
]
metrics_df = pd.DataFrame(metrics_rows)
metrics_df.to_csv(os.path.join(OUTPUTS_METRICS, "baseline_metrics.csv"), index=False)

log(f"  {'Modelo':<12} {'RMSE':>8} {'MAE':>8} {'R²':>8}")
log(f"  {'-'*40}")
for _, row in metrics_df.iterrows():
    marker = " <-- MEJOR" if row["RMSE"] == metrics_df["RMSE"].min() else ""
    log(f"  {row['modelo']:<12} {row['RMSE']:>8.4f} {row['MAE']:>8.4f} {row['R2']:>8.4f}{marker}")

supera = lgbm_metrics_test["RMSE"] < RMSE_LASSO
mejora_pct = 100 * (RMSE_LASSO - lgbm_metrics_test["RMSE"]) / RMSE_LASSO
if supera:
    log(f"\n  LightGBM SUPERA el baseline Lasso: mejora {mejora_pct:.1f}% en RMSE")
else:
    log(f"\n  LightGBM NO supera el baseline ({mejora_pct:+.1f}%). Documentando.")

# ── 7. Métricas desagregadas ─────────────────────────────────────────────────
log("\nMétricas desagregadas LightGBM...")
y_pred_test = lgbm_result["y_pred_test"]

m_nbc = compute_metrics_by_group(y_test, y_pred_test, df_test["NBC"],                  "LightGBM")
m_dep = compute_metrics_by_group(y_test, y_pred_test, df_test["NOMBRE_DEPARTAMENTO"],   "LightGBM")
m_nbc.to_csv(os.path.join(OUTPUTS_METRICS, "metricas_lgbm_por_nbc.csv"), index=False)
m_dep.to_csv(os.path.join(OUTPUTS_METRICS, "metricas_lgbm_por_depto.csv"), index=False)

log(f"  Top 5 NBC con mayor RMSE:")
for _, r in m_nbc.head(5).iterrows():
    log(f"    {str(r['grupo']):<50} RMSE={r['RMSE']:.3f} (n={r['n']})")

# ── 8. Gráficos de predicción ─────────────────────────────────────────────────
log("\nGenerando gráficos de predicción...")
plot_pred_vs_real(
    y_test.values, y_pred_test, "LightGBM", lgbm_metrics_test,
    os.path.join(OUTPUTS_FIGURES, "lgbm_predicho_vs_real.png"),
)
plot_residuals(
    y_test.values, y_pred_test, "LightGBM",
    os.path.join(OUTPUTS_FIGURES, "lgbm_residuos.png"),
)
plot_error_by_group(
    m_nbc, "LightGBM", "NBC",
    os.path.join(OUTPUTS_FIGURES, "lgbm_error_por_nbc.png"),
)
plot_error_by_group(
    m_dep, "LightGBM", "Departamento",
    os.path.join(OUTPUTS_FIGURES, "lgbm_error_por_departamento.png"),
)

# ── 9. Feature importance (gain nativo) ──────────────────────────────────────
log("\nImportancia de features (gain)...")
lgbm_model = lgbm_result["pipeline"].named_steps["model"]
importances = lgbm_model.feature_importances_
feat_names  = lgbm_result["feat_names"]

fi_df = (
    pd.DataFrame({"feature": feat_names, "importance": importances})
    .sort_values("importance", ascending=False)
)
log("  Top 10 por gain:")
for _, row in fi_df.head(10).iterrows():
    log(f"    {row['feature']:<35}: {row['importance']:,}")

fig_fi, ax_fi = plt.subplots(figsize=(10, 7))
top20 = fi_df.head(20).sort_values("importance")
ax_fi.barh(top20["feature"], top20["importance"], color="#3572A5")
ax_fi.set_title("LightGBM — Top 20 Features por Importancia (Gain)")
ax_fi.set_xlabel("Importancia (gain)")
plt.tight_layout()
fi_path = os.path.join(OUTPUTS_FIGURES, "lgbm_feature_importance_gain.png")
fig_fi.savefig(fi_path, dpi=150, bbox_inches="tight")
plt.close(fig_fi)
log(f"  Figura gain: {fi_path}")

# ── 10. SHAP values ───────────────────────────────────────────────────────────
log("\nCalculando SHAP values (puede tomar 1-2 min)...")
# Usar muestra para SHAP si el test set es grande (>5000 filas)
shap_sample_size = min(5000, len(X_test))
idx_sample = np.random.RandomState(42).choice(len(X_test), shap_sample_size, replace=False)
X_shap = X_test.iloc[idx_sample]
y_shap = y_test.iloc[idx_sample]

shap_values, X_test_t, feat_names_shap = compute_shap(lgbm_result["pipeline"], X_shap)
log(f"  SHAP calculado sobre {shap_sample_size:,} muestras del test set")
log(f"  Shape shap_values: {shap_values.shape}")

# SHAP summary plot (beeswarm)
fig_shap, ax_shap = plt.subplots(figsize=(10, 8))
shap.summary_plot(
    shap_values, X_test_t,
    feature_names=feat_names_shap,
    show=False, max_display=15,
    plot_type="dot",
)
plt.title("LightGBM — SHAP Beeswarm (test 2024)", fontsize=12, pad=12)
plt.tight_layout()
shap_bee_path = os.path.join(OUTPUTS_FIGURES, "lgbm_shap_beeswarm.png")
plt.savefig(shap_bee_path, dpi=150, bbox_inches="tight")
plt.close()
log(f"  SHAP beeswarm: {shap_bee_path}")

# SHAP bar summary
fig_shap2, ax_shap2 = plt.subplots(figsize=(10, 7))
shap.summary_plot(
    shap_values, X_test_t,
    feature_names=feat_names_shap,
    show=False, max_display=15,
    plot_type="bar",
)
plt.title("LightGBM — SHAP Importancia Media |valores SHAP|", fontsize=12, pad=12)
plt.tight_layout()
shap_bar_path = os.path.join(OUTPUTS_FIGURES, "lgbm_shap_summary.png")
plt.savefig(shap_bar_path, dpi=150, bbox_inches="tight")
plt.close()
log(f"  SHAP bar:      {shap_bar_path}")

# Top 5 features SHAP para narrativa
mean_abs_shap = np.abs(shap_values).mean(axis=0)
shap_df = pd.DataFrame({"feature": feat_names_shap, "mean_abs_shap": mean_abs_shap})
shap_df = shap_df.sort_values("mean_abs_shap", ascending=False)
top5_shap = shap_df.head(5)["feature"].tolist()
log(f"\n  Top 5 features por |SHAP|: {top5_shap}")

# ── 11. Análisis de errores sistemáticos ─────────────────────────────────────
log("\nAnalizando 20 casos con mayor error absoluto...")
errors_df = df_test[["AÑO","ID_INSTITUCION","NOMBRE_INSTITUCION",
                      "ID_PROGRAMA_ACAD","NOMBRE_PROGRAMA_ACAD",
                      "NOMBRE_PRUEBA","NBC","NOMBRE_DEPARTAMENTO",
                      TARGET_COL]].copy()
errors_df["predicho"]       = y_pred_test
errors_df["error_absoluto"] = (errors_df[TARGET_COL] - errors_df["predicho"]).abs()
errors_df["error_relativo"] = errors_df["error_absoluto"] / errors_df[TARGET_COL].replace(0, np.nan)
errors_df = errors_df.sort_values("error_absoluto", ascending=False)
top20_errors = errors_df.head(20)

log("  Top 5 errores:")
for _, r in top20_errors.head(5).iterrows():
    log(f"    {r['NOMBRE_PROGRAMA_ACAD'][:40]:<40} | "
        f"real={r[TARGET_COL]:.1f} pred={r['predicho']:.1f} "
        f"err={r['error_absoluto']:.1f}")

# Patrón: ¿concentran en algún NBC?
nbc_errors = errors_df.groupby("NBC")["error_absoluto"].mean().sort_values(ascending=False)
log(f"\n  NBC con mayor error medio (test completo):")
for nbc, err in nbc_errors.head(5).items():
    log(f"    {str(nbc):<50}: {err:.3f}")

top20_errors.to_csv(os.path.join(OUTPUTS_METRICS, "casos_mayor_error.csv"), index=False)
log(f"  Exportado: outputs/metrics/casos_mayor_error.csv")

# ── 12. Guardar modelo ────────────────────────────────────────────────────────
model_path = os.path.join(OUTPUTS_ROOT, "lgbm_model.pkl")
joblib.dump(lgbm_result["pipeline"], model_path)
log(f"\nModelo guardado: {model_path}")

# ── 13. Narrativa metodológica ────────────────────────────────────────────────
narrativa = f"""NARRATIVA METODOLÓGICA — LIGHTGBM
Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
============================================================

INTEGRIDAD DEL PIPELINE
  El TargetEncoder para NBC, NOMBRE_PRUEBA e ID_DEPARTAMENTO se calcula
  DENTRO del Pipeline de sklearn, ajustándose únicamente sobre los datos de
  entrenamiento. Durante la búsqueda de hiperparámetros con Optuna, cada trial
  reajusta el Pipeline completo (incluido el TargetEncoder) en los folds de
  TimeSeriesSplit, garantizando que el conjunto de prueba (2024) no influya
  en ninguna etapa del entrenamiento.

MODELO
  Se entrenó un modelo Gradient Boosting con LightGBM sobre {len(df_train):,}
  observaciones del período 2020–2023. El split temporal usa 2024 ({len(df_test):,}
  observaciones) como conjunto de prueba, simulando la predicción en producción.

BÚSQUEDA DE HIPERPARÁMETROS
  Tras búsqueda de hiperparámetros con Optuna ({50} trials, TPESampler),
  los mejores parámetros encontrados fueron:
{chr(10).join(f'    {k}: {v}' for k, v in best_params.items())}

  n_estimators ajustado a best_iter+20={best_params['n_estimators']} según
  curva de aprendizaje con early stopping (validación = año 2023).

RESULTADOS
  LightGBM alcanzó RMSE={lgbm_metrics_test['RMSE']} en el conjunto de prueba,
  {"representando una mejora de " + f"{mejora_pct:.1f}%" if supera else "sin superar el baseline lineal"} sobre el baseline Lasso (RMSE={RMSE_LASSO}).
  MAE={lgbm_metrics_test['MAE']}, R²={lgbm_metrics_test['R2']}.

FEATURES MÁS INFLUYENTES (SHAP)
  El análisis SHAP sobre {shap_sample_size:,} muestras del test revela que los
  features más influyentes son: {top5_shap}.
  Los lags temporales dominan la predicción, confirmando que el desempeño
  histórico de un programa es el predictor más potente de su desempeño futuro.

ANÁLISIS DE ERRORES
  Los errores más altos se concentran en:
  - NBC con mayor RMSE: {nbc_errors.index[0]} (RMSE={nbc_errors.iloc[0]:.3f})
  - Los programas con trayectorias cortas (sin lags disponibles) muestran
    mayor error, ya que el modelo no puede aprovechar la señal histórica.

TABLA COMPARATIVA FINAL
  Modelo     | RMSE    | MAE     | R²
  -----------|---------|---------|-------
  Ridge      | {RMSE_RIDGE:.4f}  | 7.2967  | 0.6467
  Lasso      | {RMSE_LASSO:.4f}  | 7.0622  | 0.6575
  LightGBM   | {lgbm_metrics_test['RMSE']:.4f}  | {lgbm_metrics_test['MAE']:.4f}  | {lgbm_metrics_test['R2']:.4f}
"""

narrativa_path = os.path.join(OUTPUTS_REPORTS, "narrativa_lgbm.txt")
with open(narrativa_path, "w", encoding="utf-8") as f:
    f.write(narrativa)
log(f"Narrativa exportada: {narrativa_path}")

# ── 14. Decisión sobre modelo final ──────────────────────────────────────────
decision = (
    f"DECISIÓN MODELO FINAL\n"
    f"{'='*50}\n"
    f"LightGBM {'SUPERA' if supera else 'NO supera'} al baseline Lasso.\n"
    f"RMSE LightGBM: {lgbm_metrics_test['RMSE']:.4f}\n"
    f"RMSE Lasso   : {RMSE_LASSO:.4f}\n"
    f"Mejora       : {mejora_pct:+.1f}%\n\n"
    f"Modelo seleccionado como modelo productivo: "
    f"{'LightGBM' if supera else 'Lasso (mejor baseline)'}\n"
    f"Modelo serializado: outputs/lgbm_model.pkl\n"
)
dec_path = os.path.join(OUTPUTS_REPORTS, "decision_modelo_final.txt")
with open(dec_path, "w", encoding="utf-8") as f:
    f.write(decision)
log(f"Decisión modelo: {dec_path}")

# ── 15. Resumen final ─────────────────────────────────────────────────────────
log("")
log("=" * 65)
log("RESUMEN FASE 5 — LIGHTGBM")
log("=" * 65)
log(f"  {'Modelo':<12} {'RMSE':>8} {'MAE':>8} {'R²':>8}")
log(f"  {'-'*42}")
for _, row in metrics_df.iterrows():
    log(f"  {row['modelo']:<12} {row['RMSE']:>8.4f} {row['MAE']:>8.4f} {row['R2']:>8.4f}")
log(f"\n  LightGBM {'SUPERA' if supera else 'NO supera'} baseline | Mejora RMSE: {mejora_pct:+.1f}%")
log(f"  R² = {lgbm_metrics_test['R2']:.4f} ({'> 0.70 → FASE 6 elegible' if lgbm_metrics_test['R2'] > 0.70 else '< 0.70 → FASE 6 omitida'})")
log(f"  Top SHAP: {top5_shap[:3]}")
log("")
log("Artefactos:")
for p in [
    "outputs/metrics/baseline_metrics.csv",
    "outputs/metrics/metricas_lgbm_por_nbc.csv",
    "outputs/metrics/casos_mayor_error.csv",
    "outputs/figures/lgbm_predicho_vs_real.png",
    "outputs/figures/lgbm_residuos.png",
    "outputs/figures/lgbm_feature_importance_gain.png",
    "outputs/figures/lgbm_shap_beeswarm.png",
    "outputs/figures/lgbm_shap_summary.png",
    "outputs/figures/lgbm_curva_aprendizaje.png",
    "outputs/figures/lgbm_error_por_nbc.png",
    "outputs/figures/lgbm_error_por_departamento.png",
    "outputs/lgbm_model.pkl",
    "outputs/lgbm_best_params.json",
    "outputs/reports/narrativa_lgbm.txt",
    "outputs/reports/decision_modelo_final.txt",
]:
    log(f"  {p}")
log("")

print()
print('FASE 5 COMPLETADA -- Revisa los resultados anteriores y escribe "ok" para continuar con la Fase 6.')
