"""
fase2_limpieza.py
Ejecuta el pivot y la limpieza completa del dataset Saber Pro (2020–2024).
Fase 2 del pipeline — Motor Predictivo Saber Pro.
Autor: Edwin Santiago Paz Bedoya — Código 1071010
"""

import os
import sys
import warnings
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from src.ingestion import load_years
from src.cleaning import clean_dataset, KEY3, KEY4, AGREGACION_TARGET

OUTPUTS_REPORTS  = os.path.join(BASE_DIR, "outputs", "reports")
OUTPUTS_FIGURES  = os.path.join(BASE_DIR, "outputs", "figures")
PROCESSED_DIR    = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(OUTPUTS_REPORTS, exist_ok=True)
os.makedirs(OUTPUTS_FIGURES, exist_ok=True)
os.makedirs(PROCESSED_DIR,  exist_ok=True)


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


# ── 1. Carga multianual ──────────────────────────────────────────────────────
log("=== FASE 2: LIMPIEZA Y PIVOT ===")
YEARS = [2020, 2021, 2022, 2023, 2024]
log(f"Cargando años: {YEARS}")
df_raw = load_years(YEARS, data_dir=os.path.join(BASE_DIR, "data", "raw"))
log(f"Dataset raw consolidado: {len(df_raw):,} filas × {len(df_raw.columns)} columnas")

# ── 2. Distribución pre-pivot por MEDIDA_AGREGACION y AGREGACION ─────────────
log("Distribución de filas por MEDIDA_AGREGACION (todos los años):")
medida_counts = df_raw.groupby(["MEDIDA_AGREGACION", "AGREGACION"]).size()
log(f"\n{medida_counts.to_string()}\n")

# ── 3. Pivot + Limpieza ──────────────────────────────────────────────────────
log("Ejecutando pivot y limpieza...")
df_clean, log_lines = clean_dataset(df_raw)

# ── 4. Validaciones post-limpieza ────────────────────────────────────────────
log("\nValidaciones post-limpieza:")

# 4a. No hay nulos en targets
assert df_clean["PROMEDIO_GLOBAL"].isnull().sum() == 0, "ERROR: PROMEDIO_GLOBAL tiene nulos!"
assert df_clean["PROMEDIO_PRUEBA"].isnull().sum() == 0, "ERROR: PROMEDIO_PRUEBA tiene nulos!"
log("  [OK] PROMEDIO_GLOBAL: 0 nulos")
log("  [OK] PROMEDIO_PRUEBA: 0 nulos")

# 4b. No hay CANTIDADEVALUADOS == 0
ce = pd.to_numeric(df_clean["CANTIDADEVALUADOS"], errors="coerce")
assert (ce == 0).sum() == 0, "ERROR: hay filas con CANTIDADEVALUADOS == 0!"
assert ce.isnull().sum() == 0, "ERROR: hay CANTIDADEVALUADOS nulos!"
log("  [OK] CANTIDADEVALUADOS: sin ceros ni nulos")

# 4c. No hay duplicados en clave pivot
dup_key = [c for c in KEY4 if c in df_clean.columns]
n_dups = df_clean.duplicated(subset=dup_key).sum()
assert n_dups == 0, f"ERROR: {n_dups} duplicados en clave pivot!"
log(f"  [OK] Clave {dup_key}: 0 duplicados")

# 4d. Distribución por año
log("\n  Filas limpias por año:")
yr_dist = df_clean["AÑO"].value_counts().sort_index()
for yr, cnt in yr_dist.items():
    log(f"    {yr}: {cnt:,}")

# 4e. Distribución por NOMBRE_PRUEBA
log(f"\n  Pruebas únicas: {df_clean['NOMBRE_PRUEBA'].nunique()}")
log(f"  Entidades únicas (AÑO+INST+PROG): {df_clean.groupby(KEY3).ngroups:,}")

# ── 5. Análisis de niveles de agregación elegido ─────────────────────────────
agg_info = [
    "",
    "── DECISIÓN DE NIVEL DE AGREGACIÓN ──",
    f"Nivel elegido: {AGREGACION_TARGET}",
    "",
    "Justificación metodológica:",
    "  El nivel PROGRAMA_ACÁDEMICO es el más granular que simultáneamente:",
    "  (a) contiene ID_INSTITUCION e ID_PROGRAMA_ACAD (identificadores únicos del programa),",
    "  (b) tiene PUNTAJE_GLOBAL disponible (target del modelo),",
    "  (c) tiene PUNTAJE_PRUEBA por prueba (features de desempeño específico),",
    "  (d) tiene NIVEL_DESEMPEÑO_PRUEBA para distribución de niveles.",
    "",
    "  Otros niveles excluidos y razón:",
    "  - PAIS, REGION, DEPARTAMENTO, MUNICIPIO: demasiado agregados, pierden",
    "    identidad de institución y programa.",
    "  - NBC_INSTITUCION, NBC_SEDE: agrupan múltiples programas bajo el mismo",
    "    Núcleo Básico del Conocimiento, perdiendo granularidad de programa.",
    "  - SEDE: subunidad de institución, puede duplicar información.",
    "  - INSTITUCION: no discrimina por programa académico.",
    "",
    "  PERCENTIL_PRUEBA: no disponible al nivel PROGRAMA_ACÁDEMICO → excluido del pivot.",
    "  NIVEL5: 99.42% nulos en todo el dataset → excluido.",
]
log_lines.extend(agg_info)

# ── 6. Figura de distribución post-pivot ─────────────────────────────────────
log("\nGenerando figuras de distribución post-limpieza...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Dataset Saber Pro — Post-Pivot y Limpieza (Fase 2)", fontsize=14, y=1.01)

# a) Distribución de PROMEDIO_GLOBAL
ax = axes[0, 0]
df_clean["PROMEDIO_GLOBAL"].hist(bins=50, ax=ax, color="#3572A5", edgecolor="white")
ax.set_title("Distribución PROMEDIO_GLOBAL (target)")
ax.set_xlabel("Puntaje global")
ax.set_ylabel("Frecuencia")
ax.axvline(df_clean["PROMEDIO_GLOBAL"].mean(), color="red", linestyle="--",
           label=f'Media={df_clean["PROMEDIO_GLOBAL"].mean():.1f}')
ax.legend(fontsize=9)

# b) Filas por año
ax = axes[0, 1]
yr_dist.plot(kind="bar", ax=ax, color="#3572A5", edgecolor="white")
ax.set_title("Filas limpias por año")
ax.set_xlabel("Año")
ax.set_ylabel("Cantidad de registros")
ax.tick_params(axis="x", rotation=0)
for i, v in enumerate(yr_dist.values):
    ax.text(i, v + 50, f"{v:,}", ha="center", fontsize=8)

# c) Top 20 pruebas por frecuencia
ax = axes[1, 0]
top_pruebas = df_clean["NOMBRE_PRUEBA"].value_counts().head(15)
top_pruebas.plot(kind="barh", ax=ax, color="#3572A5")
ax.set_title("Top 15 NOMBRE_PRUEBA (frecuencia)")
ax.set_xlabel("Cantidad de registros")
ax.tick_params(axis="y", labelsize=7)

# d) Top 15 NBC (Núcleo Básico del Conocimiento)
ax = axes[1, 1]
nbc_counts = df_clean["NBC"].value_counts().head(15)
nbc_counts.plot(kind="barh", ax=ax, color="#5F7A9D")
ax.set_title("Top 15 NBC (frecuencia)")
ax.set_xlabel("Cantidad de registros")
ax.tick_params(axis="y", labelsize=7)

plt.tight_layout()
fig_path = os.path.join(OUTPUTS_FIGURES, "distribucion_post_limpieza.png")
fig.savefig(fig_path, dpi=150, bbox_inches="tight")
plt.close(fig)
log(f"Figura exportada: {fig_path}")

# ── 7. Nulidad post-limpieza ─────────────────────────────────────────────────
try:
    import missingno as msno
    df_sample = df_clean.sample(min(20_000, len(df_clean)), random_state=42)
    fig2, ax2 = plt.subplots(figsize=(14, 6))
    msno.matrix(df_sample, ax=ax2, sparkline=False, fontsize=8)
    ax2.set_title("Nulidad post-limpieza — Saber Pro (muestra 20k)", fontsize=12)
    plt.tight_layout()
    fig2_path = os.path.join(OUTPUTS_FIGURES, "nulidad_post_limpieza.png")
    fig2.savefig(fig2_path, dpi=150, bbox_inches="tight")
    plt.close(fig2)
    log(f"Heatmap nulidad post-limpieza exportado: {fig2_path}")
except Exception as e:
    log(f"  (heatmap missingno omitido: {e})")

# ── 8. Exportar dataset limpio ───────────────────────────────────────────────
clean_path = os.path.join(PROCESSED_DIR, "saber_pro_limpio.csv")
df_clean.to_csv(clean_path, index=False, encoding="utf-8")
log(f"\nDataset limpio exportado: {clean_path}")
log(f"  Filas: {len(df_clean):,}  |  Columnas: {len(df_clean.columns)}")

# ── 9. Exportar log de limpieza ──────────────────────────────────────────────
log_path = os.path.join(OUTPUTS_REPORTS, "log_limpieza.txt")
with open(log_path, "w", encoding="utf-8") as f:
    f.write("\n".join(log_lines))
log(f"Log de limpieza exportado: {log_path}")

# ── 10. Resumen consola ──────────────────────────────────────────────────────
log("")
log("=" * 60)
log("RESUMEN FASE 2 — LIMPIEZA Y PIVOT")
log("=" * 60)
log(f"  Dataset raw               : {len(df_raw):,} filas")
log(f"  Dataset limpio (wide)     : {len(df_clean):,} filas")
log(f"  Columnas                  : {len(df_clean.columns)}")
log(f"  Entidades únicas (INST+PROG+AÑO): {df_clean.groupby(KEY3).ngroups:,}")
log(f"  Target PROMEDIO_GLOBAL    : 0 nulos [OK]")
log(f"  Target PROMEDIO_PRUEBA    : 0 nulos [OK]")
log(f"  Años incluidos            : {sorted(df_clean['AÑO'].unique().tolist())}")
log(f"  Nivel de agregación       : {AGREGACION_TARGET}")
log("")
log(f"Artefactos generados:")
log(f"  {clean_path}")
log(f"  {log_path}")
log(f"  {fig_path}")
log("")

print()
print('FASE 2 COMPLETADA -- Revisa los resultados anteriores y escribe "ok" para continuar con la Fase 3.')
