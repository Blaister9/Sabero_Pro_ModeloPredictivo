"""
fase1_auditoria.py
Auditoría completa de datos Saber Pro 2024 (y todos los años disponibles).
Fase 1 del pipeline — Motor Predictivo Saber Pro.
Autor: Edwin Santiago Paz Bedoya — Código 1071010
"""

import os
import sys
import warnings
from datetime import datetime

import matplotlib
matplotlib.use("Agg")  # Sin GUI — compatible con entornos sin display
import matplotlib.pyplot as plt
import missingno as msno
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ── Rutas base ──────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
from src.ingestion import load_years, EXPECTED_COLUMNS

OUTPUTS_REPORTS = os.path.join(BASE_DIR, "outputs", "reports")
OUTPUTS_FIGURES = os.path.join(BASE_DIR, "outputs", "figures")
os.makedirs(OUTPUTS_REPORTS, exist_ok=True)
os.makedirs(OUTPUTS_FIGURES, exist_ok=True)


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


# ── 1. Carga del dataset ─────────────────────────────────────────────────────
log("=== FASE 1: AUDITORÍA DE DATOS ===")
log("Cargando archivos disponibles...")

YEARS_AVAILABLE = [2020, 2021, 2022, 2023, 2024]
df = load_years(YEARS_AVAILABLE, data_dir=os.path.join(BASE_DIR, "data", "raw"))

log(f"Dataset consolidado: {len(df):,} filas × {len(df.columns)} columnas")

# ── 2. Detección de columnas reales vs esperadas ─────────────────────────────
log("Validando schema...")

real_cols = list(df.columns)
missing_expected = [c for c in EXPECTED_COLUMNS if c not in real_cols]
extra_cols = [c for c in real_cols if c not in EXPECTED_COLUMNS and c != "AÑO"]

lines_schema = []
lines_schema.append("=" * 70)
lines_schema.append("VALIDACIÓN DE SCHEMA")
lines_schema.append("=" * 70)
lines_schema.append(f"Columnas en el archivo: {len(real_cols)}")
lines_schema.append(f"Columnas esperadas según spec: {len(EXPECTED_COLUMNS)}")
lines_schema.append("")
lines_schema.append("Columnas presentes en archivo:")
for c in sorted(real_cols):
    status = "✓" if c in EXPECTED_COLUMNS or c == "AÑO" else "⚠ EXTRA"
    lines_schema.append(f"  {status}  {c}")
lines_schema.append("")
if missing_expected:
    lines_schema.append("COLUMNAS ESPERADAS AUSENTES:")
    for c in missing_expected:
        lines_schema.append(f"  ✗  {c}")
else:
    lines_schema.append("Todas las columnas esperadas están presentes.")
lines_schema.append("")
if extra_cols:
    lines_schema.append("COLUMNAS ADICIONALES NO ESPERADAS:")
    for c in extra_cols:
        lines_schema.append(f"  +  {c}")

for l in lines_schema:
    print(l)

# ── 3. Reporte de auditoría completo ─────────────────────────────────────────
log("Generando reporte de auditoría...")

report_lines = []

report_lines.append("=" * 70)
report_lines.append("REPORTE DE AUDITORÍA — DATOS SABER PRO")
report_lines.append(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
report_lines.append(f"Años cargados: {YEARS_AVAILABLE}")
report_lines.append("=" * 70)
report_lines.append("")

# 3.1 Dimensiones generales
report_lines.append("── DIMENSIONES GENERALES ──")
report_lines.append(f"Filas totales        : {len(df):,}")
report_lines.append(f"Columnas totales     : {len(df.columns)}")
report_lines.append("")

# 3.2 Distribución por año
if "AÑO" in df.columns:
    report_lines.append("── DISTRIBUCIÓN POR AÑO ──")
    yr_counts = df["AÑO"].value_counts().sort_index()
    for yr, cnt in yr_counts.items():
        report_lines.append(f"  {yr}: {cnt:,} filas")
    report_lines.append("")

# 3.3 Tipos de dato
report_lines.append("── TIPOS DE DATO POR COLUMNA ──")
for col in df.columns:
    report_lines.append(f"  {col:<40} {str(df[col].dtype)}")
report_lines.append("")

# 3.4 Nulidad por columna
report_lines.append("── NULIDAD POR COLUMNA ──")
report_lines.append(f"  {'Columna':<40} {'Nulos':>8} {'%':>8}")
report_lines.append("  " + "-" * 60)
null_stats = {}
for col in df.columns:
    n_null = int(df[col].isnull().sum())
    pct = 100.0 * n_null / len(df) if len(df) > 0 else 0.0
    null_stats[col] = (n_null, pct)
    report_lines.append(f"  {col:<40} {n_null:>8,} {pct:>7.2f}%")
report_lines.append("")

# 3.5 Distribución de CANTIDADEVALUADOS
if "CANTIDADEVALUADOS" in df.columns:
    report_lines.append("── DISTRIBUCIÓN DE CANTIDADEVALUADOS ──")
    ce = pd.to_numeric(df["CANTIDADEVALUADOS"], errors="coerce")
    report_lines.append(f"  Mínimo       : {ce.min()}")
    report_lines.append(f"  P25          : {ce.quantile(0.25)}")
    report_lines.append(f"  Mediana (P50): {ce.median()}")
    report_lines.append(f"  P75          : {ce.quantile(0.75)}")
    report_lines.append(f"  P99          : {ce.quantile(0.99)}")
    report_lines.append(f"  Máximo       : {ce.max()}")
    report_lines.append(f"  Filas con CE == 0 : {(ce == 0).sum():,}")
    report_lines.append(f"  Filas con CE nulo : {ce.isnull().sum():,}")
    report_lines.append("")

# 3.6 Filas con CE > 0 pero PROMEDIO_GLOBAL nulo
if "CANTIDADEVALUADOS" in df.columns and "PROMEDIO_GLOBAL" in df.columns:
    ce2 = pd.to_numeric(df["CANTIDADEVALUADOS"], errors="coerce")
    pg = pd.to_numeric(df["PROMEDIO_GLOBAL"], errors="coerce")
    mask = (ce2 > 0) & pg.isnull()
    report_lines.append("── INCONSISTENCIAS TARGET ──")
    report_lines.append(
        f"  CE > 0 pero PROMEDIO_GLOBAL nulo  : {mask.sum():,} filas"
    )
    if "PROMEDIO_PRUEBA" in df.columns:
        pp = pd.to_numeric(df["PROMEDIO_PRUEBA"], errors="coerce")
        mask2 = (ce2 > 0) & pp.isnull()
        report_lines.append(
            f"  CE > 0 pero PROMEDIO_PRUEBA nulo  : {mask2.sum():,} filas"
        )
    report_lines.append("")

# 3.7 Valores únicos de AGREGACION y MEDIDA_AGREGACION
for col in ["AGREGACION", "MEDIDA_AGREGACION"]:
    if col in df.columns:
        report_lines.append(f"── VALORES ÚNICOS DE {col} ──")
        uniques = df[col].dropna().unique()
        for u in sorted(uniques, key=str):
            cnt = int((df[col] == u).sum())
            report_lines.append(f"  {str(u):<40} {cnt:,}")
        report_lines.append("")

# 3.8 Valores únicos de NOMBRE_PRUEBA
if "NOMBRE_PRUEBA" in df.columns:
    report_lines.append("── VALORES ÚNICOS DE NOMBRE_PRUEBA ──")
    pruebas = df["NOMBRE_PRUEBA"].dropna().unique()
    report_lines.append(f"  Total pruebas distintas: {len(pruebas)}")
    for p in sorted(pruebas, key=str):
        report_lines.append(f"  • {p}")
    report_lines.append("")

# 3.9 Schema final (matching)
report_lines.extend(lines_schema)

# Exportar reporte
report_path = os.path.join(OUTPUTS_REPORTS, "auditoria_2024.txt")
with open(report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))
log(f"Reporte exportado: {report_path}")

# ── 4. Figura de nulidad ─────────────────────────────────────────────────────
log("Generando heatmap de nulidad...")

# Seleccionar muestra si el dataset es muy grande (>100k filas ralentiza msno)
df_sample = df.sample(min(50_000, len(df)), random_state=42) if len(df) > 50_000 else df

fig, ax = plt.subplots(figsize=(16, 8))
msno.matrix(df_sample, ax=ax, sparkline=False, fontsize=8, color=(0.25, 0.45, 0.65))
ax.set_title(
    f"Patrón de nulidad — Saber Pro {YEARS_AVAILABLE}\n"
    f"(muestra de {len(df_sample):,} filas)",
    fontsize=13,
    pad=12,
)
plt.tight_layout()
fig_path = os.path.join(OUTPUTS_FIGURES, "nulidad_2024.png")
fig.savefig(fig_path, dpi=150, bbox_inches="tight")
plt.close(fig)
log(f"Heatmap exportado: {fig_path}")

# Figura adicional: barplot de % nulidad por columna
cols_with_nulls = {c: v[1] for c, v in null_stats.items() if v[1] > 0}
if cols_with_nulls:
    fig2, ax2 = plt.subplots(figsize=(10, max(4, len(cols_with_nulls) * 0.4)))
    cols_sorted = sorted(cols_with_nulls, key=lambda c: cols_with_nulls[c], reverse=True)
    pcts = [cols_with_nulls[c] for c in cols_sorted]
    bars = ax2.barh(cols_sorted, pcts, color="#3572A5")
    ax2.set_xlabel("% de valores nulos")
    ax2.set_title("Porcentaje de nulos por columna — Saber Pro")
    ax2.axvline(x=70, color="red", linestyle="--", alpha=0.6, label="Umbral 70%")
    ax2.legend(fontsize=9)
    for bar, pct in zip(bars, pcts):
        ax2.text(
            pct + 0.3, bar.get_y() + bar.get_height() / 2,
            f"{pct:.1f}%", va="center", fontsize=8
        )
    plt.tight_layout()
    fig2_path = os.path.join(OUTPUTS_FIGURES, "nulidad_barplot_2024.png")
    fig2.savefig(fig2_path, dpi=150, bbox_inches="tight")
    plt.close(fig2)
    log(f"Barplot de nulidad exportado: {fig2_path}")

# ── 5. Resumen consola ───────────────────────────────────────────────────────
log("")
log("=" * 60)
log("RESUMEN DE AUDITORÍA — FASE 1")
log("=" * 60)
log(f"  Filas totales          : {len(df):,}")
log(f"  Columnas               : {len(df.columns)}")
if "AÑO" in df.columns:
    log(f"  Años cargados          : {sorted(df['AÑO'].unique().tolist())}")
log(f"  Columnas esperadas ausentes: {missing_expected if missing_expected else 'Ninguna'}")
log(f"  Columnas extra no esperadas: {extra_cols if extra_cols else 'Ninguna'}")

high_null = [c for c, (n, p) in null_stats.items() if p > 70]
log(f"  Columnas con >70% nulos: {high_null if high_null else 'Ninguna'}")

if "CANTIDADEVALUADOS" in df.columns:
    ce_num = pd.to_numeric(df["CANTIDADEVALUADOS"], errors="coerce")
    log(f"  Filas con CE == 0      : {(ce_num == 0).sum():,}")
log("")
log(f"Reporte guardado en   : {report_path}")
log(f"Figuras guardadas en  : {OUTPUTS_FIGURES}")
log("")

print()
print("✅ FASE 1 COMPLETADA — Revisa los resultados anteriores y escribe \"ok\" para continuar con la Fase 2.")
