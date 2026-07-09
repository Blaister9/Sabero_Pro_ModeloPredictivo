"""
demo_inference.py
Demostración del módulo de inferencia — Motor Predictivo Saber Pro.
Fase 7 del pipeline — Edwin Santiago Paz Bedoya (1071010)

Escenarios demostrados:
  1. Programa con historial completo en test 2024 → confianza MEDIA
     (activa extrapolacion porque 2024 no pertenece al train 2020-2023)
  2. Programa con muestra pequeña (N<5)       → flag BAJA_CONFIANZA_MUESTRA_PEQUEÑA
  3. Programa nuevo sin historial             → flag BAJA_CONFIANZA_SIN_HISTORIAL
  4. Predicción para año 2025 (extrapolación) → flag BAJA_CONFIANZA_EXTRAPOLACION
  5. Outlier documentado: UMB prog 742        → flags múltiples
  6. Predicción en lote (batch) sobre test 2024

Uso:
    python3 demo_inference.py
"""

import os
import sys

import numpy as np
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from src.inference import (
    format_prediction_report,
    load_model,
    predict_batch,
    predict_institution,
)

MODEL_PATH   = os.path.join(PROJECT_ROOT, "outputs", "lgbm_model.pkl")
DATA_PATH    = os.path.join(PROJECT_ROOT, "data", "processed", "saber_pro_features.csv")
OUTPUTS_DIR  = os.path.join(PROJECT_ROOT, "outputs")
REPORTS_DIR  = os.path.join(OUTPUTS_DIR, "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)

print("=" * 60)
print("MOTOR PREDICTIVO SABER PRO — DEMO DE INFERENCIA")
print("=" * 60)

# ── Carga del modelo ──────────────────────────────────────────────────────────
if not os.path.exists(MODEL_PATH):
    print("\nERROR: no se encontro el modelo entrenado.")
    print(f"Ruta esperada: {MODEL_PATH}")
    print("Este archivo no se versiona en Git. Genere el modelo con:")
    print("  python main.py --only 5")
    print("o ejecute las fases 4-5 despues de tener data/processed/saber_pro_features.csv.")
    sys.exit(2)

if not os.path.exists(DATA_PATH):
    print("\nERROR: no se encontro el CSV de features.")
    print(f"Ruta esperada: {DATA_PATH}")
    print("Genere este archivo con:")
    print("  python main.py --only 3")
    print("o ejecute el pipeline desde la fase 3 si ya existe saber_pro_limpio.csv.")
    sys.exit(2)

print("\nCargando modelo LightGBM...")
model = load_model(MODEL_PATH)
print("  Modelo cargado correctamente.")

# ── CASO 1: Programa con historial completo ───────────────────────────────────
print("\n" + "-" * 60)
print("CASO 1: Historial completo — Confianza MEDIA esperada")
print("-" * 60)
print("Institución: TECNOLÓGICO DE ANTIOQUIA")
print("Programa   : INGENIERÍA AMBIENTAL")
print("Prueba     : INGLÉS | Año objetivo: 2024")
print("Nota       : 2024 es test temporal; el train termina en 2023.")

r1 = predict_institution(
    model=model,
    año=2024,
    nbc="INGENIERÍA AMBIENTAL, SANITARIA Y AFINES",
    nombre_prueba="INGLÉS",
    id_departamento=1,
    cantidadevaluados=91,
    categoriaprueba=2,
    # Historial real del programa (lags de 2022 y 2021)
    lag_1_promedio_global=142.0,    # PROMEDIO_GLOBAL 2023
    lag_2_promedio_global=141.0,    # PROMEDIO_GLOBAL 2022
    lag_1_promedio_prueba=152.0,    # PROMEDIO_PRUEBA 2023
    lag_2_promedio_prueba=147.0,    # PROMEDIO_PRUEBA 2022
    tendencia_global=0.5,
    tendencia_prueba=3.0,
    desviacion_estandar_historica=0.577,
    coeficiente_variacion=0.004,
    nombre_institucion="TECNOLÓGICO DE ANTIOQUIA",
    nombre_programa="INGENIERÍA AMBIENTAL",
)
print(format_prediction_report(r1))

# ── CASO 2: Muestra pequeña (N < 5) ──────────────────────────────────────────
print("\n" + "-" * 60)
print("CASO 2: Muestra pequeña (N=3) — BAJA_CONFIANZA_MUESTRA_PEQUEÑA esperado")
print("-" * 60)
print("Institución: POLITÉCNICO COLOMBIANO")
print("Programa   : INGENIERÍA AGROPECUARIA")
print("Prueba     : FORMULACIÓN DE PROYECTOS DE INGENIERÍA | Año: 2024")

r2 = predict_institution(
    model=model,
    año=2024,
    nbc="INGENIERÍA AGRONÓMICA, PECUARIA Y AFINES",
    nombre_prueba="FORMULACIÓN DE PROYECTOS DE INGENIERÍA",
    id_departamento=1,
    cantidadevaluados=3,            # ← N < 5 → flag activado
    categoriaprueba=2,
    lag_1_promedio_global=142.0,
    lag_2_promedio_global=None,     # Solo tiene 1 año de historia anterior
    lag_1_promedio_prueba=137.0,
    lag_2_promedio_prueba=None,
    tendencia_global=None,
    tendencia_prueba=None,
    desviacion_estandar_historica=None,
    coeficiente_variacion=None,
    nombre_institucion="POLITÉCNICO COLOMBIANO",
    nombre_programa="INGENIERÍA AGROPECUARIA",
)
print(format_prediction_report(r2))

# ── CASO 3: Sin historial (primer año del programa) ───────────────────────────
print("\n" + "-" * 60)
print("CASO 3: Sin historial — BAJA_CONFIANZA_SIN_HISTORIAL esperado")
print("-" * 60)
print("Institución: TECNOLÓGICO DE ANTIOQUIA")
print("Programa   : INGENIERÍA AMBIENTAL (prueba nueva, sin historia previa)")

r3 = predict_institution(
    model=model,
    año=2024,
    nbc="INGENIERÍA AMBIENTAL, SANITARIA Y AFINES",
    nombre_prueba="DISEÑO DE SISTEMAS DE MANEJO DEL IMPACTO AMBIENTAL",
    id_departamento=1,
    cantidadevaluados=143,
    categoriaprueba=2,
    # Sin historia → todo None
    lag_1_promedio_global=None,
    lag_2_promedio_global=None,
    lag_1_promedio_prueba=None,
    lag_2_promedio_prueba=None,
    tendencia_global=None,
    tendencia_prueba=None,
    desviacion_estandar_historica=None,
    coeficiente_variacion=None,
    nombre_institucion="TECNOLÓGICO DE ANTIOQUIA",
    nombre_programa="INGENIERÍA AMBIENTAL (nueva prueba)",
)
print(format_prediction_report(r3))

# ── CASO 4: Extrapolación a 2025 ─────────────────────────────────────────────
print("\n" + "-" * 60)
print("CASO 4: Extrapolación a AÑO=2025 — BAJA_CONFIANZA_EXTRAPOLACION esperado")
print("-" * 60)
print("Escenario: misma institución del Caso 1, prediciendo para 2025")

r4 = predict_institution(
    model=model,
    año=2025,                       # ← más allá de train (2020-2023)
    nbc="INGENIERÍA AMBIENTAL, SANITARIA Y AFINES",
    nombre_prueba="INGLÉS",
    id_departamento=1,
    cantidadevaluados=95,
    categoriaprueba=2,
    lag_1_promedio_global=142.0,    # PROMEDIO_GLOBAL 2024 (hipotético)
    lag_2_promedio_global=141.0,    # PROMEDIO_GLOBAL 2023
    lag_1_promedio_prueba=150.0,
    lag_2_promedio_prueba=152.0,
    tendencia_global=0.5,
    tendencia_prueba=2.5,
    desviacion_estandar_historica=1.2,
    coeficiente_variacion=0.008,
    nombre_institucion="TECNOLÓGICO DE ANTIOQUIA",
    nombre_programa="INGENIERÍA AMBIENTAL — Proyección 2025",
)
print(format_prediction_report(r4))

# ── CASO 5: Outlier documentado — UMB Programa 742 ───────────────────────────
print("\n" + "-" * 60)
print("CASO 5: Outlier documentado (N=1, PROMEDIO=31.0 en 2024)")
print("-" * 60)
print("Institución: UNIVERSIDAD MANUELA BELTRÁN")
print("Programa   : LIC. ED. BÁSICA ÉNFASIS TECNOLOGÍA E INFORMÁTICA")
print("Nota: PROMEDIO_GLOBAL=31.0 en 2024 fue N=1. Ver analisis_outliers.txt")

r5 = predict_institution(
    model=model,
    año=2025,                       # Predicción para 2025 usando historial real
    nbc="EDUCACIÓN",
    nombre_prueba="INGLÉS",
    id_departamento=11,             # Bogotá D.C.
    cantidadevaluados=1,            # ← N=1 → BAJA_CONFIANZA_MUESTRA_PEQUEÑA
    categoriaprueba=1,
    lag_1_promedio_global=31.0,     # Último valor reportado (outlier 2024)
    lag_2_promedio_global=154.0,    # Valor confiable de 2023
    lag_1_promedio_prueba=None,
    lag_2_promedio_prueba=None,
    tendencia_global=None,
    tendencia_prueba=None,
    desviacion_estandar_historica=None,
    coeficiente_variacion=None,
    nombre_institucion="UNIVERSIDAD MANUELA BELTRÁN",
    nombre_programa="LIC. ED. BÁSICA ÉNFASIS TECNOLOGÍA E INFORMÁTICA",
)
print(format_prediction_report(r5))
print("NOTA ANALÍTICA: El lag_1=31.0 es el outlier documentado (N=1 en 2024).")
print("El modelo lo usa como input, por lo que la predicción puede estar")
print("sesgada. Recomendar usar lag_2=154.0 como mejor estimador del nivel")
print("real del programa. En producción: flag automático activa revisión manual.")

# ── CASO 6: Predicción en lote (batch) sobre test 2024 ───────────────────────
print("\n" + "-" * 60)
print("CASO 6: Predicción en lote — Muestra aleatoria del test 2024")
print("-" * 60)

df = pd.read_csv(DATA_PATH, low_memory=False)
df_test = df[df["AÑO"] == 2024].copy()
sample = df_test.sample(n=10, random_state=42)

batch_result = predict_batch(sample, model)

display_cols = [
    "NOMBRE_INSTITUCION", "NOMBRE_PRUEBA", "CANTIDADEVALUADOS",
    "PROMEDIO_GLOBAL", "prediccion_promedio_global",
    "baja_confianza_muestra_pequeña", "baja_confianza_sin_historial",
    "confianza_global",
]
print(batch_result[display_cols].to_string(index=False))

# Métricas de lote
y_true = batch_result["PROMEDIO_GLOBAL"].values
y_pred = batch_result["prediccion_promedio_global"].values
rmse       = float(np.sqrt(np.mean((y_true - y_pred) ** 2)))
r2_sample  = float(1 - np.sum((y_true - y_pred)**2) / np.sum((y_true - np.mean(y_true))**2))
print(f"\nMétricas muestra (n=10): RMSE={rmse:.4f}  R²={r2_sample:.4f}")
print("(Nota: muestra aleatoria de 10 — no comparable con RMSE global=9.3293)")

# ── Métricas completas sobre test 2024 ───────────────────────────────────────
print("\n" + "-" * 60)
print("MÉTRICAS COMPLETAS — TEST 2024 (n=28,762)")
print("-" * 60)

full_batch = predict_batch(df_test, model)
y_tr = full_batch["PROMEDIO_GLOBAL"].values
y_pr = full_batch["prediccion_promedio_global"].values
rmse_full = float(np.sqrt(np.mean((y_tr - y_pr) ** 2)))
r2_full   = float(1 - np.sum((y_tr - y_pr)**2) / np.sum((y_tr - np.mean(y_tr))**2))


n_alta  = (full_batch["confianza_global"] == "ALTA").sum()
n_media = (full_batch["confianza_global"] == "MEDIA").sum()
n_baja  = (full_batch["confianza_global"] == "BAJA").sum()
n_mues  = full_batch["baja_confianza_muestra_pequeña"].sum()
n_sinhis= full_batch["baja_confianza_sin_historial"].sum()
n_extrap= full_batch["baja_confianza_extrapolacion"].sum()

print(f"  RMSE test:           {rmse_full:.4f}")
print(f"  R²   test:           {r2_full:.4f}")
print(f"  Confianza ALTA:      {n_alta:,} ({n_alta/len(full_batch)*100:.1f}%)")
print(f"  Confianza MEDIA:     {n_media:,} ({n_media/len(full_batch)*100:.1f}%)")
print(f"  Confianza BAJA:      {n_baja:,} ({n_baja/len(full_batch)*100:.1f}%)")
print(f"  Flag muestra pequeña:{n_mues:,} ({n_mues/len(full_batch)*100:.2f}%)")
print(f"  Flag sin historial:  {n_sinhis:,} ({n_sinhis/len(full_batch)*100:.1f}%)")
print(f"  Flag extrapolación:  {n_extrap:,} (2024 es test temporal fuera del train 2020-2023)")

# RMSE solo sobre predicciones de confianza ALTA
alta_mask = full_batch["confianza_global"] == "ALTA"
if alta_mask.sum() > 0:
    y_a = full_batch.loc[alta_mask, "PROMEDIO_GLOBAL"].values
    p_a = full_batch.loc[alta_mask, "prediccion_promedio_global"].values
    rmse_alta = float(np.sqrt(np.mean((y_a - p_a) ** 2)))
    r2_alta   = float(1 - np.sum((y_a - p_a)**2) / np.sum((y_a - np.mean(y_a))**2))
    print(f"\n  RMSE (solo ALTA confianza, n={alta_mask.sum():,}): {rmse_alta:.4f}")
    print(f"  R²   (solo ALTA confianza):                       {r2_alta:.4f}")

# ── Guardar reporte de inferencia ─────────────────────────────────────────────
report_lines = [
    "REPORTE DEMO INFERENCIA — MOTOR PREDICTIVO SABER PRO",
    f"Fecha: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}",
    "=" * 60,
    "",
    "CASOS INDIVIDUALES:",
    "",
    f"Caso 1 — Historial completo:",
    f"  Predicción: {r1['prediccion_promedio_global']:.2f} | Confianza: {r1['confianza_global']}",
    f"  Flags: muestra_pequeña={r1['baja_confianza_muestra_pequeña']}, "
    f"sin_historial={r1['baja_confianza_sin_historial']}, "
    f"extrapolacion={r1['baja_confianza_extrapolacion']}",
    "",
    f"Caso 2 — Muestra pequeña (N=3):",
    f"  Predicción: {r2['prediccion_promedio_global']:.2f} | Confianza: {r2['confianza_global']}",
    f"  Flags: muestra_pequeña={r2['baja_confianza_muestra_pequeña']}, "
    f"sin_historial={r2['baja_confianza_sin_historial']}, "
    f"extrapolacion={r2['baja_confianza_extrapolacion']}",
    "",
    f"Caso 3 — Sin historial:",
    f"  Predicción: {r3['prediccion_promedio_global']:.2f} | Confianza: {r3['confianza_global']}",
    f"  Flags: muestra_pequeña={r3['baja_confianza_muestra_pequeña']}, "
    f"sin_historial={r3['baja_confianza_sin_historial']}, "
    f"extrapolacion={r3['baja_confianza_extrapolacion']}",
    "",
    f"Caso 4 — Extrapolación 2025:",
    f"  Predicción: {r4['prediccion_promedio_global']:.2f} | Confianza: {r4['confianza_global']}",
    f"  Flags: muestra_pequeña={r4['baja_confianza_muestra_pequeña']}, "
    f"sin_historial={r4['baja_confianza_sin_historial']}, "
    f"extrapolacion={r4['baja_confianza_extrapolacion']}",
    "",
    f"Caso 5 — Outlier UMB prog 742 (N=1):",
    f"  Predicción: {r5['prediccion_promedio_global']:.2f} | Confianza: {r5['confianza_global']}",
    f"  Flags: muestra_pequeña={r5['baja_confianza_muestra_pequeña']}, "
    f"sin_historial={r5['baja_confianza_sin_historial']}, "
    f"extrapolacion={r5['baja_confianza_extrapolacion']}",
    "",
    "=" * 60,
    "BATCH TEST 2024 (n=28,762):",
    f"  RMSE:           {rmse_full:.4f}",
    f"  R²:             {r2_full:.4f}",
    f"  Confianza ALTA: {n_alta:,} ({n_alta/len(full_batch)*100:.1f}%)",
    f"  Confianza MEDIA:{n_media:,} ({n_media/len(full_batch)*100:.1f}%)",
    f"  Confianza BAJA: {n_baja:,} ({n_baja/len(full_batch)*100:.1f}%)",
    f"  Muestra pequeña:{n_mues:,} predicciones con flag BAJA_CONFIANZA_MUESTRA_PEQUEÑA",
    f"  Sin historial:  {n_sinhis:,} predicciones con flag BAJA_CONFIANZA_SIN_HISTORIAL",
]

if alta_mask.sum() > 0:
    report_lines += [
        f"  RMSE ALTA confianza: {rmse_alta:.4f}",
        f"  R²   ALTA confianza: {r2_alta:.4f}",
    ]

report_path = os.path.join(REPORTS_DIR, "demo_inferencia.txt")
with open(report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))

print(f"\nReporte guardado: {report_path}")
print("\n" + "=" * 60)
print("FASE 7 COMPLETA — Módulo de inferencia verificado.")
print("=" * 60)
