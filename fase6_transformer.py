"""
fase6_transformer.py
Fase 6 — Transformer encoder para regresión de PROMEDIO_GLOBAL.
Motor Predictivo Saber Pro — Edwin Santiago Paz Bedoya (1071010)

Restricciones:
  - CPU-only.
  - Presupuesto de tiempo: 20 minutos (1 200 s). Si no converge, se
    documentan resultados parciales y se pasa a Fase 7.
  - Sin leakage: split temporal 2020-2023 (train) / 2024 (test).
  - Normalización de features calculada SOLO sobre train.
  - Features: mismas numéricas + OHE que el baseline (sin TargetEncoder
    para simplificar la arquitectura secuencial; el LGBM pipeline ya usa
    TargetEncoder internamente, el Transformer usa codificación numérica
    directa).

Uso:
    python3 fase6_transformer.py
"""

import json
import os
import sys
import time
from datetime import datetime

import matplotlib
matplotlib.use("Agg")  # Sin GUI
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ── Paths ─────────────────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from src.models.baseline import NUMERIC_FEATURE_COLS
from src.models.transformer import train_transformer

DATA_PATH    = os.path.join(PROJECT_ROOT, "data", "processed", "saber_pro_features.csv")
OUTPUTS_DIR  = os.path.join(PROJECT_ROOT, "outputs")
REPORTS_DIR  = os.path.join(OUTPUTS_DIR, "reports")
FIGURES_DIR  = os.path.join(OUTPUTS_DIR, "figures")

os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

TARGET_COL = "PROMEDIO_GLOBAL"
TIME_BUDGET = 1200  # 20 minutos en segundos


def _log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def _rmse(y_true, y_pred):
    return float(np.sqrt(np.mean((np.asarray(y_true) - np.asarray(y_pred)) ** 2)))


def _r2(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return float(1 - ss_res / ss_tot) if ss_tot > 0 else 0.0


# ── 1. Carga de datos ─────────────────────────────────────────────────────────
_log("Cargando datos...")
df = pd.read_csv(DATA_PATH, low_memory=False)
_log(f"  Dataset: {df.shape[0]:,} filas × {df.shape[1]} columnas")

# ── 2. Split temporal ─────────────────────────────────────────────────────────
df_train = df[df["AÑO"] <= 2023].copy()
df_test  = df[df["AÑO"] == 2024].copy()
_log(f"  Train (2020-2023): {len(df_train):,} | Test (2024): {len(df_test):,}")

# ── 3. Feature columns ────────────────────────────────────────────────────────
# Usar las mismas numéricas del baseline + OHE (sin TargetEncoder categóricas).
# Los NaN en lags/tendencias de los primeros años se imputan con 0 (valor
# "sin historia disponible") ANTES de normalizar, consistente con el padding
# de la secuencia temporal.
ohe_cols     = [c for c in df.columns if c.startswith("cat_prueba_")]
feature_cols = [c for c in NUMERIC_FEATURE_COLS if c in df.columns] + ohe_cols

_log(f"  Features: {len(feature_cols)} → {feature_cols}")

# Imputar NaN con 0 antes de construir secuencias
df_train[feature_cols] = df_train[feature_cols].fillna(0.0)
df_test[feature_cols]  = df_test[feature_cols].fillna(0.0)

# ── 4. Verificar instalación de PyTorch ───────────────────────────────────────
try:
    import torch
    _log(f"  PyTorch {torch.__version__} disponible (CPU)")
except ImportError:
    _log("ERROR: PyTorch no instalado. Ejecuta:")
    _log("  python3 -m pip install torch --index-url https://download.pytorch.org/whl/cpu")
    sys.exit(1)

# ── 5. Entrenamiento Transformer ──────────────────────────────────────────────
_log(f"\n{'='*60}")
_log(f"FASE 6 — TRANSFORMER (presupuesto: {TIME_BUDGET//60} min)")
_log(f"  Arquitectura: d_model=64, nhead=4, layers=2, ffn=128")
_log(f"  max_seq_len=5, lr=3e-4, batch_size=256, max_epochs=200, patience=20")
_log(f"{'='*60}")

results = train_transformer(
    X_train=df_train[feature_cols],
    y_train=df_train[TARGET_COL],
    X_test=df_test[feature_cols],
    y_test=df_test[TARGET_COL],
    df_train=df_train,
    df_test=df_test,
    feature_cols=feature_cols,
    time_budget_seconds=TIME_BUDGET,
    d_model=64,
    nhead=4,
    num_layers=2,
    ffn_dim=128,
    dropout=0.1,
    max_seq_len=5,
    lr=3e-4,
    batch_size=256,
    max_epochs=200,
    patience=20,
)

# ── 6. Métricas finales ───────────────────────────────────────────────────────
_log(f"\n{'='*60}")
_log("MÉTRICAS FINALES — TRANSFORMER")
_log(f"  Convergió:      {'Sí' if results['converged'] else 'No (parcial)'}")
_log(f"  Tiempo total:   {results['elapsed_seconds']:.1f}s")
_log(f"  Mejor epoch:    {results['best_epoch']}")
_log(f"  Best val RMSE:  {results['best_val_rmse']:.4f}")
_log(f"  RMSE train:     {results['rmse_train']:.4f}")
_log(f"  R²   train:     {results['r2_train']:.4f}")
_log(f"  RMSE test:      {results['rmse_test']:.4f}")
_log(f"  R²   test:      {results['r2_test']:.4f}")
_log(f"{'='*60}")

# Comparativa con LightGBM
LGBM_RMSE = 9.3293
LGBM_R2   = 0.7062
_log("\nCOMPARATIVA TRANSFORMER vs LightGBM (test 2024):")
_log(f"  LightGBM  RMSE={LGBM_RMSE:.4f}  R²={LGBM_R2:.4f}")
_log(f"  Transformer RMSE={results['rmse_test']:.4f}  R²={results['r2_test']:.4f}")
delta_rmse = results['rmse_test'] - LGBM_RMSE
if delta_rmse < 0:
    _log(f"  >> Transformer SUPERA a LightGBM en RMSE por {abs(delta_rmse):.4f} puntos")
else:
    _log(f"  >> LightGBM sigue siendo MEJOR por {delta_rmse:.4f} puntos de RMSE")

# ── 7. Guardar modelo ─────────────────────────────────────────────────────────
import torch
model_path = os.path.join(OUTPUTS_DIR, "transformer_model.pt")
torch.save({
    "model_state_dict": results["model"].state_dict(),
    "feature_cols":     feature_cols,
    "d_model":          results["d_model"],
    "nhead":            results["nhead"],
    "num_layers":       results["num_layers"],
    "ffn_dim":          results["ffn_dim"],
    "max_seq_len":      results["max_seq_len"],
    "feat_mean":        results["train_ds"].feat_mean.to_dict(),
    "feat_std":         results["train_ds"].feat_std.to_dict(),
    "rmse_test":        results["rmse_test"],
    "r2_test":          results["r2_test"],
    "best_epoch":       results["best_epoch"],
    "converged":        results["converged"],
    "elapsed_seconds":  results["elapsed_seconds"],
}, model_path)
_log(f"\nModelo guardado: {model_path}")

# ── 8. Figura: Curva de aprendizaje ───────────────────────────────────────────
if results["train_losses"]:
    fig, ax = plt.subplots(figsize=(8, 4))
    epochs = range(1, len(results["train_losses"]) + 1)
    ax.plot(epochs, results["train_losses"], label="Train RMSE", color="steelblue")
    ax.plot(epochs, results["val_losses"],   label="Val RMSE",   color="coral")
    if results["best_epoch"] > 0:
        ax.axvline(results["best_epoch"], color="gray", linestyle="--",
                   alpha=0.7, label=f"Best epoch ({results['best_epoch']})")
    ax.set_xlabel("Época")
    ax.set_ylabel("RMSE (puntos Saber Pro)")
    ax.set_title("Transformer — Curva de Aprendizaje")
    ax.legend()
    ax.grid(True, alpha=0.3)
    lc_path = os.path.join(FIGURES_DIR, "transformer_learning_curve.png")
    fig.tight_layout()
    fig.savefig(lc_path, dpi=150)
    plt.close(fig)
    _log(f"Curva de aprendizaje guardada: {lc_path}")

# ── 9. Figura: Scatter predicciones vs reales (test) ─────────────────────────
fig, ax = plt.subplots(figsize=(6, 6))
y_true = results["y_true_test"]
y_pred = results["y_pred_test"]
ax.scatter(y_true, y_pred, alpha=0.3, s=8, color="steelblue")
mn = min(y_true.min(), y_pred.min()) - 5
mx = max(y_true.max(), y_pred.max()) + 5
ax.plot([mn, mx], [mn, mx], "r--", linewidth=1)
ax.set_xlabel("PROMEDIO_GLOBAL real")
ax.set_ylabel("PROMEDIO_GLOBAL predicho")
ax.set_title(f"Transformer — Test 2024\nRMSE={results['rmse_test']:.4f}  R²={results['r2_test']:.4f}")
ax.grid(True, alpha=0.3)
scatter_path = os.path.join(FIGURES_DIR, "transformer_scatter_test.png")
fig.tight_layout()
fig.savefig(scatter_path, dpi=150)
plt.close(fig)
_log(f"Scatter test guardado: {scatter_path}")

# ── 10. Reporte decision_transformer.txt ─────────────────────────────────────
status_str = "CONVERGIDO" if results["converged"] else \
             ("TIEMPO AGOTADO (resultados parciales)" if results["time_exhausted"] else "PARCIAL")

report = f"""ANÁLISIS COMPARATIVO TRANSFORMER vs MODELOS ANTERIORES — FASE 6
Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Autor: Edwin Santiago Paz Bedoya — Código 1071010
{'='*65}

1. CONFIGURACIÓN DEL TRANSFORMER
---------------------------------
  Arquitectura:
    - Tipo:           TransformerEncoder (solo encoder, sin decoder)
    - d_model:        {results['d_model']} (dimensión de embedding)
    - nhead:          {results['nhead']} (cabezas de atención multi-head)
    - num_layers:     {results['num_layers']} (capas TransformerEncoderLayer)
    - ffn_dim:        {results['ffn_dim']} (dimensión feed-forward interna)
    - dropout:        0.1
    - norm_first:     True (pre-norm, más estable en datos tabulares pequeños)
    - Positional enc: Aprendible (LearnedPositionalEncoding)
    - Pooling:        Último token de la secuencia temporal
    - Cabeza:         Linear(64→32)→GELU→Dropout→Linear(32→1)
    - Parámetros:     {results.get('n_params', 'N/A'):,}

  Dataset:
    - Tipo:           Secuencias temporales por entidad
    - Entidad:        (ID_INSTITUCION, ID_PROGRAMA_ACAD, NOMBRE_PRUEBA)
    - max_seq_len:    {results['max_seq_len']} (años)
    - Features/paso:  {len(feature_cols)} ({', '.join(feature_cols[:5])}...)
    - Train samples:  {len(results['train_ds'])} entidades
    - Test  samples:  {len(results['test_ds'])} entidades
    - NaN impute:     0.0 (sin historia = cero antes de normalizar)
    - Normalización:  μ/σ calculados SOLO sobre train → sin leakage

  Entrenamiento:
    - Optimizador:    AdamW (lr=3e-4, weight_decay=1e-4)
    - Scheduler:      CosineAnnealingLR (T_max=200, eta_min=1e-5)
    - Grad clipping:  max_norm=1.0
    - Loss:           MSELoss → RMSE para monitoreo
    - Early stopping: patience=20 épocas
    - Presupuesto:    {TIME_BUDGET}s ({TIME_BUDGET//60} minutos)

2. RESULTADOS DEL ENTRENAMIENTO
---------------------------------
  Estado:             {status_str}
  Tiempo total:       {results['elapsed_seconds']:.1f}s ({results['elapsed_seconds']/60:.1f} min)
  Épocas completadas: {len(results['train_losses'])}
  Mejor época:        {results['best_epoch']}
  Mejor val RMSE:     {results['best_val_rmse']:.4f}

  Métricas finales (mejor modelo restaurado):
    RMSE train:   {results['rmse_train']:.4f}
    R²   train:   {results['r2_train']:.4f}
    RMSE test:    {results['rmse_test']:.4f}
    R²   test:    {results['r2_test']:.4f}

3. COMPARATIVA DE MODELOS — TEST 2024
-----------------------------------------
  | Modelo           | RMSE test | R² test | Notas                          |
  |------------------|-----------|---------|--------------------------------|
  | Ridge (baseline) | 10.4142   | 0.6467  | Regularización L2              |
  | Lasso (baseline) | 10.0722   | 0.6580  | Selección de features L1       |
  | LightGBM         |  {LGBM_RMSE:.4f}   |  {LGBM_R2:.4f} | Optuna 50 trials, SHAP         |
  | Transformer      |  {results['rmse_test']:.4f}   |  {results['r2_test']:.4f} | {status_str[:30]:30s} |

4. ANÁLISIS Y DECISIÓN
-----------------------
  4.1 ¿Supera el Transformer a LightGBM?
{"      SÍ: el Transformer mejora el RMSE en " + f"{abs(delta_rmse):.4f} puntos." if delta_rmse < 0 else "      NO: LightGBM sigue siendo el mejor modelo (+{:.4f} puntos RMSE).".format(delta_rmse)}

  4.2 Ventajas del Transformer en este contexto:
      - Captura dependencias temporales entre años de forma explícita
        (self-attention sobre la secuencia t-4..t-1..t).
      - No requiere ingeniería de features de lags manuales; aprende
        patrones de tendencia directamente de la secuencia.
      - Escalable si se agregan más años o features por timestep.
      - Positional encoding aprendible se adapta a las 5 posiciones
        posibles del dataset (2020–2024).

  4.3 Desventajas observadas:
      - Dataset pequeño (≈{len(results['train_ds'])} entidades de train vs 98,954 filas en LGBM):
        el Transformer agrega por entidad, perdiendo variabilidad intra-
        entidad. Esto reduce el tamaño efectivo de muestra.
      - Alta proporción de entidades con historia corta (1-2 años):
        el left-padding introduce ruido que la attention puede amplificar.
      - Features categóricas (NBC, NOMBRE_PRUEBA, ID_DEPARTAMENTO) no
        incluidas en el Transformer (requeriría embeddings adicionales),
        lo que lo pone en desventaja informacional frente a LightGBM.
      - Más costoso en CPU que LightGBM para este volumen de datos.

  4.4 Consideración del time budget:
      {"El modelo CONVERGIÓ antes del límite de 20 min." if results['converged'] else f"El modelo NO convergió en 20 min. Se reportan resultados parciales de la época {results['best_epoch']} (mejor val RMSE={results['best_val_rmse']:.4f})."}
      Esta decisión documenta que el Transformer es factible en CPU para
      este dataset, pero la inferencia de tiempo limita la búsqueda de
      hiperparámetros.

5. MODELO FINAL SELECCIONADO PARA FASE 7
------------------------------------------
  {"TRANSFORMER (supera a LightGBM)" if delta_rmse < 0 else "LIGHTGBM (sigue siendo el mejor modelo)"}

  Justificación:
  {"El Transformer ofrece mejor RMSE en test y captura la dinámica temporal explícitamente, justificando su mayor complejidad." if delta_rmse < 0 else f"LightGBM ofrece mejor RMSE ({LGBM_RMSE:.4f} vs {results['rmse_test']:.4f}), menor complejidad, tiempo de entrenamiento << 20 min, e interpretabilidad SHAP. El Transformer no justifica su complejidad adicional para este dataset en este momento."}
  Para la Fase 7 (inferencia) y la Fase 8 (paper), el modelo primario es
  LightGBM (outputs/lgbm_model.pkl). El Transformer queda documentado
  como experimento adicional con potencial para datasets más grandes.

{'='*65}
FIN DEL REPORTE
"""

report_path = os.path.join(REPORTS_DIR, "decision_transformer.txt")
with open(report_path, "w", encoding="utf-8") as f:
    f.write(report)
_log(f"Reporte guardado: {report_path}")

# ── 11. Actualizar decision_modelo_final.txt ──────────────────────────────────
decision_path = os.path.join(REPORTS_DIR, "decision_modelo_final.txt")
final_model   = "LIGHTGBM" if delta_rmse >= 0 else "TRANSFORMER"

update_block = f"""
{'='*65}
ACTUALIZACIÓN FASE 6 — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*65}
Transformer evaluado:
  RMSE test: {results['rmse_test']:.4f}  R²: {results['r2_test']:.4f}
  Estado:    {status_str}
  Épocas:    {len(results['train_losses'])} / 200

Comparativa final (test 2024):
  Ridge:       RMSE=10.4142  R²=0.6467
  Lasso:       RMSE=10.0722  R²=0.6580
  LightGBM:    RMSE={LGBM_RMSE:.4f}  R²={LGBM_R2:.4f}  ← MEJOR MODELO PARA PRODUCCIÓN
  Transformer: RMSE={results['rmse_test']:.4f}  R²={results['r2_test']:.4f}

MODELO FINAL SELECCIONADO: {final_model}
Ruta: outputs/{'lgbm_model.pkl' if final_model == 'LIGHTGBM' else 'transformer_model.pt'}
Ver detalle: outputs/reports/decision_transformer.txt
"""

with open(decision_path, "a", encoding="utf-8") as f:
    f.write(update_block)
_log(f"decision_modelo_final.txt actualizado.")

_log(f"\n{'='*60}")
_log("FASE 6 COMPLETA")
_log(f"{'='*60}")
_log(f"  Transformer: RMSE={results['rmse_test']:.4f}  R²={results['r2_test']:.4f}")
_log(f"  LightGBM:    RMSE={LGBM_RMSE:.4f}  R²={LGBM_R2:.4f}")
_log(f"  Modelo para Fase 7: {final_model}")
