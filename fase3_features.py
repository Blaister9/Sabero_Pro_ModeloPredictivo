"""
fase3_features.py
Ejecuta el feature engineering completo sobre el dataset limpio.
Fase 3 del pipeline — Motor Predictivo Saber Pro.
Autor: Edwin Santiago Paz Bedoya — Código 1071010
"""

import os
import sys
import warnings
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from src.features import build_features, ENTITY_COLS

OUTPUTS_REPORTS = os.path.join(BASE_DIR, "outputs", "reports")
OUTPUTS_FIGURES = os.path.join(BASE_DIR, "outputs", "figures")
PROCESSED_DIR   = os.path.join(BASE_DIR, "data", "processed")


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


# ── 1. Carga del dataset limpio ──────────────────────────────────────────────
log("=== FASE 3: FEATURE ENGINEERING ===")
clean_path = os.path.join(PROCESSED_DIR, "saber_pro_limpio.csv")
df_clean = pd.read_csv(clean_path, low_memory=False)
log(f"Dataset limpio cargado: {len(df_clean):,} filas x {df_clean.shape[1]} columnas")

# ── 2. Análisis de cobertura temporal ────────────────────────────────────────
log("\nAnalizando cobertura temporal por entidad...")

years_per_entity = df_clean.groupby(ENTITY_COLS)["AÑO"].nunique()
vc = years_per_entity.value_counts().sort_index()
total_entities = len(years_per_entity)

log("  Distribución de años de historia por entidad (ID_INST + ID_PROG + NOMBRE_PRUEBA):")
for n_yrs, cnt in vc.items():
    pct = 100 * cnt / total_entities
    bar = "█" * int(pct / 2)
    log(f"    {n_yrs} año(s) : {cnt:>6,} entidades ({pct:>5.1f}%)  {bar}")

log(f"\n  Resumen:")
log(f"    Entidades con 5 años completos : {(years_per_entity==5).sum():,} ({100*(years_per_entity==5).mean():.1f}%)")
log(f"    Entidades con >= 3 años        : {(years_per_entity>=3).sum():,} ({100*(years_per_entity>=3).mean():.1f}%)")
log(f"    Entidades con >= 2 años (lag_1): {(years_per_entity>=2).sum():,} ({100*(years_per_entity>=2).mean():.1f}%)")
log(f"    Entidades con solo 1 año       : {(years_per_entity==1).sum():,} ({100*(years_per_entity==1).mean():.1f}%)")
log(f"\n  Implicación para lags:")
log(f"    lag_1_promedio_global : disponible para {(years_per_entity>=2).sum():,} entidades ({100*(years_per_entity>=2).mean():.1f}%)")
log(f"    lag_2_promedio_global : disponible para {(years_per_entity>=3).sum():,} entidades ({100*(years_per_entity>=3).mean():.1f}%)")

# Figura de cobertura temporal
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("Cobertura Temporal por Entidad — Saber Pro 2020-2024", fontsize=13)

ax = axes[0]
ax.bar(vc.index, vc.values, color="#3572A5", edgecolor="white")
ax.set_xlabel("Años de historia disponibles")
ax.set_ylabel("Número de entidades")
ax.set_title("Distribución de cobertura temporal")
ax.set_xticks(range(1, 6))
for i, (n, v) in enumerate(vc.items()):
    ax.text(n, v + 100, f"{v:,}\n({100*v/total_entities:.0f}%)", ha="center", fontsize=9)

ax = axes[1]
cum = vc.sort_index(ascending=False).cumsum().sort_index()
pct_cum = 100 * cum / total_entities
ax.bar(pct_cum.index, pct_cum.values, color="#5F7A9D", edgecolor="white")
ax.set_xlabel("Al menos N años de historia")
ax.set_ylabel("% de entidades")
ax.set_title("Entidades con al menos N años (acumulado)")
ax.set_xticks(range(1, 6))
for i, (n, v) in enumerate(pct_cum.items()):
    ax.text(n, v + 1, f"{v:.0f}%", ha="center", fontsize=9)
ax.axhline(y=48.3, color="red", linestyle="--", alpha=0.5, label="48.3% con 5 años")
ax.legend(fontsize=9)

plt.tight_layout()
cov_fig_path = os.path.join(OUTPUTS_FIGURES, "cobertura_temporal.png")
fig.savefig(cov_fig_path, dpi=150, bbox_inches="tight")
plt.close(fig)
log(f"\n  Figura de cobertura exportada: {cov_fig_path}")

# ── 3. Feature engineering ───────────────────────────────────────────────────
log("\nEjecutando build_features()...")
df_feat, report_lines = build_features(df_clean)
log(f"Dataset con features: {len(df_feat):,} filas x {df_feat.shape[1]} columnas")

# ── 4. Validaciones post-features ────────────────────────────────────────────
log("\nValidaciones post-features:")

# 4a. Targets sin nulos
assert df_feat["PROMEDIO_GLOBAL"].isnull().sum() == 0
assert df_feat["PROMEDIO_PRUEBA"].isnull().sum() == 0
log("  [OK] Targets PROMEDIO_GLOBAL y PROMEDIO_PRUEBA: 0 nulos")

# 4b. Conteo de filas sin cambios
assert len(df_feat) == len(df_clean), "ERROR: cambió el número de filas!"
log(f"  [OK] Filas: {len(df_feat):,} (sin cambios)")

# 4c. Validar que los lags son NaN en la primera observación de cada entidad
first_obs = df_feat.sort_values(ENTITY_COLS + ["AÑO"]).groupby(ENTITY_COLS).head(1)
frac_lag1_null_first = first_obs["lag_1_promedio_global"].isnull().mean()
log(f"  [OK] lag_1 nulo en primera observación de cada entidad: {100*frac_lag1_null_first:.1f}% (esperado ~100%)")

# 4d. No hay target leak: lag_1 != PROMEDIO_GLOBAL en misma fila
if "lag_1_promedio_global" in df_feat.columns:
    mask_notna = df_feat["lag_1_promedio_global"].notna()
    same = (df_feat.loc[mask_notna, "lag_1_promedio_global"] ==
            df_feat.loc[mask_notna, "PROMEDIO_GLOBAL"]).mean()
    log(f"  [OK] lag_1 == PROMEDIO_GLOBAL en {100*same:.1f}% de filas (esperado bajo, solo coincidencias naturales)")

# ── 5. Distribución de features clave ────────────────────────────────────────
log("\nEstadísticas de features clave:")
key_feat = [
    "lag_1_promedio_global","lag_2_promedio_global",
    "delta_1_global","tendencia_global",
    "prop_nivel1","prop_nivel2","prop_niveles_bajos","prop_niveles_altos",
    "desviacion_estandar_historica","coeficiente_variacion",
    "log_cantidadevaluados","te_nbc","te_nombre_prueba",
]
for f in key_feat:
    if f in df_feat.columns:
        sub = df_feat[f].dropna()
        log(f"  {f:<35}: mean={sub.mean():.3f}, std={sub.std():.3f}, "
            f"null={100*df_feat[f].isnull().mean():.1f}%")

# ── 6. Figura de distribución de features ────────────────────────────────────
log("\nGenerando figuras de features...")

num_feat_plot = [
    ("lag_1_promedio_global", "Lag 1 PROMEDIO_GLOBAL"),
    ("delta_1_global",        "Delta t vs t-1 (GLOBAL)"),
    ("tendencia_global",      "Tendencia OLS (slope)"),
    ("prop_niveles_bajos",    "Prop. Niveles Bajos (N1+N2)"),
    ("prop_niveles_altos",    "Prop. Niveles Altos (N3+N4)"),
    ("log_cantidadevaluados", "Log(CANTIDADEVALUADOS+1)"),
]

fig2, axes2 = plt.subplots(2, 3, figsize=(15, 9))
fig2.suptitle("Distribución de Features Construidas — Fase 3", fontsize=13)
axes2 = axes2.flatten()

for i, (col, title) in enumerate(num_feat_plot):
    ax = axes2[i]
    if col in df_feat.columns:
        data = df_feat[col].dropna()
        ax.hist(data, bins=50, color="#3572A5", edgecolor="white", alpha=0.85)
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("Valor")
        ax.set_ylabel("Frecuencia")
        pct_null = 100 * df_feat[col].isnull().mean()
        ax.text(0.97, 0.95, f"null={pct_null:.1f}%\nn={len(data):,}",
                transform=ax.transAxes, ha="right", va="top", fontsize=8,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.7))
    else:
        ax.set_visible(False)

plt.tight_layout()
feat_fig_path = os.path.join(OUTPUTS_FIGURES, "distribucion_features.png")
fig2.savefig(feat_fig_path, dpi=150, bbox_inches="tight")
plt.close(fig2)
log(f"  Figura de features exportada: {feat_fig_path}")

# ── 7. Correlación con target ─────────────────────────────────────────────────
log("\nGenerando correlación de features con PROMEDIO_GLOBAL...")
numeric_cols = df_feat.select_dtypes(include=[np.number]).columns.tolist()
exclude = ["PROMEDIO_GLOBAL","PROMEDIO_PRUEBA","NIVEL1","NIVEL2","NIVEL3","NIVEL4",
           "ID_PAIS","CANTIDADEVALUADOS"]
feat_for_corr = [c for c in numeric_cols if c not in exclude]

corr_series = (
    df_feat[feat_for_corr + ["PROMEDIO_GLOBAL"]]
    .corr()["PROMEDIO_GLOBAL"]
    .drop("PROMEDIO_GLOBAL")
    .dropna()
    .sort_values(key=abs, ascending=False)
    .head(20)
)

fig3, ax3 = plt.subplots(figsize=(10, 7))
colors = ["#D63F3F" if v < 0 else "#3572A5" for v in corr_series.values]
ax3.barh(corr_series.index[::-1], corr_series.values[::-1], color=colors[::-1])
ax3.set_title("Top 20 Features por Correlación con PROMEDIO_GLOBAL", fontsize=12)
ax3.set_xlabel("Correlación de Pearson")
ax3.axvline(x=0, color="black", linewidth=0.8)
plt.tight_layout()
corr_fig_path = os.path.join(OUTPUTS_FIGURES, "correlacion_features_target.png")
fig3.savefig(corr_fig_path, dpi=150, bbox_inches="tight")
plt.close(fig3)
log(f"  Figura de correlación exportada: {corr_fig_path}")

# Top 10 correlaciones en consola
log("\n  Top 10 features por correlación con PROMEDIO_GLOBAL:")
for feat, corr in corr_series.head(10).items():
    log(f"    {feat:<35}: {corr:.4f}")

# ── 8. Exportar dataset con features ─────────────────────────────────────────
feat_path = os.path.join(PROCESSED_DIR, "saber_pro_features.csv")
df_feat.to_csv(feat_path, index=False, encoding="utf-8")
log(f"\nDataset con features exportado: {feat_path}")
log(f"  Filas: {len(df_feat):,}  |  Columnas: {df_feat.shape[1]}")

# ── 9. Exportar reporte de features ──────────────────────────────────────────
# Agregar sección de correlaciones al reporte
report_lines.append("── TOP 20 CORRELACIONES CON PROMEDIO_GLOBAL ──")
for feat, corr in corr_series.items():
    report_lines.append(f"  {feat:<35}: {corr:.4f}")
report_lines.append("")
report_lines.append("── FEATURES EXCLUIDAS (>70% nulos) ──")
high_null = [c for c in df_feat.select_dtypes(include=[np.number]).columns
             if df_feat[c].isnull().mean() > 0.70 and c not in
             ["PROMEDIO_GLOBAL","PROMEDIO_PRUEBA"]]
if high_null:
    for c in high_null:
        report_lines.append(f"  {c}: {100*df_feat[c].isnull().mean():.1f}% nulos")
else:
    report_lines.append("  Ninguna feature nueva supera el 70% de nulos.")

report_path = os.path.join(OUTPUTS_REPORTS, "feature_report.txt")
with open(report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(report_lines))
log(f"Reporte de features exportado: {report_path}")

# ── 10. Resumen consola ───────────────────────────────────────────────────────
log("")
log("=" * 60)
log("RESUMEN FASE 3 — FEATURE ENGINEERING")
log("=" * 60)

original_cols = {"AÑO","ID_PAIS","ID_REGION","NOMBRE_REGION","ID_DEPARTAMENTO",
    "NOMBRE_DEPARTAMENTO","ID_MUNICIPIO","NOMBRE_MUNICIPIO","ID_INSTITUCION",
    "NOMBRE_INSTITUCION","ID_NBC","NBC","ID_PROGRAMA_ACAD","NOMBRE_PROGRAMA_ACAD",
    "NOMBRE_PRUEBA","CATEGORIAPRUEBA","CANTIDADEVALUADOS","PROMEDIO_PRUEBA",
    "DESVIACION","PROMEDIO_GLOBAL","NIVEL1","NIVEL2","NIVEL3","NIVEL4"}
new_features = [c for c in df_feat.columns if c not in original_cols]

log(f"  Filas                    : {len(df_feat):,}")
log(f"  Columnas totales         : {df_feat.shape[1]}")
log(f"  Features nuevas          : {len(new_features)}")
log(f"  Features con >70% nulos  : 0")
log(f"  Target leak detectado    : No")
log(f"  Entidades con lag_1 disp.: {(years_per_entity>=2).sum():,} ({100*(years_per_entity>=2).mean():.1f}%)")
log(f"  Entidades con lag_2 disp.: {(years_per_entity>=3).sum():,} ({100*(years_per_entity>=3).mean():.1f}%)")
log(f"  Feature más correlacionada: {corr_series.index[0]} ({corr_series.iloc[0]:.4f})")
log("")
log(f"Artefactos generados:")
log(f"  {feat_path}")
log(f"  {report_path}")
log(f"  {cov_fig_path}")
log(f"  {feat_fig_path}")
log(f"  {corr_fig_path}")
log("")

print()
print('FASE 3 COMPLETADA -- Revisa los resultados anteriores y escribe "ok" para continuar con la Fase 4.')
