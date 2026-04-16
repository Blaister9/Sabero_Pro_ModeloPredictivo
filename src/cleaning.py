"""
src/cleaning.py
Pivot, limpieza y filtrado del dataset Saber Pro.
Fase 2 del pipeline — Motor Predictivo Saber Pro.
Autor: Edwin Santiago Paz Bedoya — Código 1071010

Estrategia de pivot (validada en auditoría Fase 1):
  - Dataset en formato LONG: cada fila = una medida por entidad
  - NOMBRE_PRUEBA es nulo en PUNTAJE_GLOBAL → join sin esa columna
  - PERCENTIL_PRUEBA no existe al nivel PROGRAMA_ACÁDEMICO → excluido
  - NIVEL5 tiene 99.42% nulos → excluido
  - Nivel de agregación elegido: PROGRAMA_ACÁDEMICO (más granular con ID_PROGRAMA_ACAD)
"""

import os
from datetime import datetime

import numpy as np
import pandas as pd


def _log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


# Columnas clave para la identidad de la entidad (pivot key)
KEY3 = ["AÑO", "ID_INSTITUCION", "ID_PROGRAMA_ACAD"]          # entidad sin prueba
KEY4 = ["AÑO", "ID_INSTITUCION", "ID_PROGRAMA_ACAD", "NOMBRE_PRUEBA"]  # entidad + prueba

# Nivel de agregación elegido para modelado
AGREGACION_TARGET = "PROGRAMA_ACÁDEMICO"

# Columnas de contexto a conservar desde PUNTAJE_PRUEBA
CONTEXT_COLS = [
    "AÑO", "ID_PAIS", "ID_REGION", "NOMBRE_REGION",
    "ID_DEPARTAMENTO", "NOMBRE_DEPARTAMENTO",
    "ID_MUNICIPIO", "NOMBRE_MUNICIPIO",
    "ID_INSTITUCION", "NOMBRE_INSTITUCION",
    "ID_NBC", "NBC",
    "ID_PROGRAMA_ACAD", "NOMBRE_PROGRAMA_ACAD",
    "NOMBRE_PRUEBA", "CATEGORIAPRUEBA",
    "CANTIDADEVALUADOS", "PROMEDIO_PRUEBA", "DESVIACION",
]


def _pivot_long_to_wide(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte el dataset long-format a wide-format con una fila por entidad.

    Estrategia de join (validada en auditoría):
      1. Base: PUNTAJE_PRUEBA @ PROGRAMA_ACÁDEMICO
             → una fila por (AÑO, ID_INST, ID_PROG, NOMBRE_PRUEBA)
             → columnas: PROMEDIO_PRUEBA, DESVIACION, contexto
      2. Inner join PUNTAJE_GLOBAL @ PROGRAMA_ACÁDEMICO
             → agrega PROMEDIO_GLOBAL (TARGET)
             → descarta entidades sin global score
      3. Left join NIVEL_DESEMPEÑO_PRUEBA @ PROGRAMA_ACÁDEMICO
             → agrega NIVEL1, NIVEL2, NIVEL3, NIVEL4
             → NIVEL5 excluido (99.42% nulos)
      4. PERCENTIL_PRUEBA: no existe al nivel PROGRAMA_ACÁDEMICO → omitido

    Returns: DataFrame wide con PROMEDIO_GLOBAL como target.
    """
    _log("Iniciando pivot long → wide...")

    # ── Subset 1: PUNTAJE_PRUEBA (base) ────────────────────────────────────
    pp = df_raw[
        (df_raw["MEDIDA_AGREGACION"] == "PUNTAJE_PRUEBA") &
        (df_raw["AGREGACION"] == AGREGACION_TARGET)
    ].copy()

    # Solo conservar columnas de contexto que existan
    ctx = [c for c in CONTEXT_COLS if c in pp.columns]
    base = pp[ctx].copy()
    _log(f"  PUNTAJE_PRUEBA @ {AGREGACION_TARGET}: {len(base):,} filas")

    # ── Subset 2: PUNTAJE_GLOBAL (target) ──────────────────────────────────
    pg = df_raw[
        (df_raw["MEDIDA_AGREGACION"] == "PUNTAJE_GLOBAL") &
        (df_raw["AGREGACION"] == AGREGACION_TARGET)
    ].copy()

    # Validar clave sin duplicados
    dup_pg = pg.duplicated(subset=KEY3).sum()
    if dup_pg > 0:
        _log(f"  ADVERTENCIA: {dup_pg} duplicados en clave KEY3 de PUNTAJE_GLOBAL — conservando primero.")
        pg = pg.drop_duplicates(subset=KEY3, keep="first")

    pg_slim = pg[KEY3 + ["PROMEDIO_GLOBAL"]].copy()
    _log(f"  PUNTAJE_GLOBAL @ {AGREGACION_TARGET}: {len(pg_slim):,} filas (entidades únicas)")

    # INNER JOIN: solo entidades que tienen target
    before = len(base)
    base = base.merge(pg_slim, on=KEY3, how="inner")
    dropped_notarget = before - len(base)
    _log(f"  Post inner-join con GLOBAL: {len(base):,} filas "
         f"({dropped_notarget:,} descartadas sin target)")

    # ── Subset 3: NIVEL_DESEMPEÑO_PRUEBA ───────────────────────────────────
    niv = df_raw[
        (df_raw["MEDIDA_AGREGACION"] == "NIVEL_DESEMPEÑO_PRUEBA") &
        (df_raw["AGREGACION"] == AGREGACION_TARGET)
    ].copy()

    nivel_cols = [c for c in ["NIVEL1", "NIVEL2", "NIVEL3", "NIVEL4"] if c in niv.columns]
    dup_niv = niv.duplicated(subset=KEY4).sum()
    if dup_niv > 0:
        _log(f"  ADVERTENCIA: {dup_niv} duplicados en clave KEY4 de NIVEL — conservando primero.")
        niv = niv.drop_duplicates(subset=KEY4, keep="first")

    niv_slim = niv[KEY4 + nivel_cols].copy()
    base = base.merge(niv_slim, on=KEY4, how="left")
    pct_niv = 100 * base["NIVEL1"].isnull().mean() if "NIVEL1" in base.columns else 100
    _log(f"  Post left-join NIVEL1-4: {len(base):,} filas | NIVEL1 nulos: {pct_niv:.1f}%")

    _log(f"  Pivot completado: {len(base):,} filas × {len(base.columns)} columnas")
    return base


def clean_dataset(df_raw: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """
    Aplica el pivot y las reglas de limpieza C1–C5.

    Parameters
    ----------
    df_raw : pd.DataFrame
        Dataset consolidado cargado con load_years() (formato long).

    Returns
    -------
    df_clean : pd.DataFrame
        Dataset limpio en formato wide, listo para feature engineering.
    log_lines : list[str]
        Líneas del log de limpieza para exportar.
    """
    log_lines = []
    log_lines.append("=" * 70)
    log_lines.append("LOG DE LIMPIEZA — SABER PRO")
    log_lines.append(f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_lines.append("=" * 70)
    log_lines.append("")

    # ── PIVOT ───────────────────────────────────────────────────────────────
    _log("Ejecutando pivot...")
    df = _pivot_long_to_wide(df_raw)
    n_original = len(df)
    log_lines.append(f"Filas post-pivot (pre-limpieza): {n_original:,}")
    log_lines.append(f"Nivel de agregación elegido    : {AGREGACION_TARGET}")
    log_lines.append(f"Justificación                  : Es el nivel más granular que contiene")
    log_lines.append(f"                                 ID_INSTITUCION e ID_PROGRAMA_ACAD,")
    log_lines.append(f"                                 permitiendo modelar a nivel programa.")
    log_lines.append("")

    # ── REGLA C1: Eliminar filas sin evaluados ──────────────────────────────
    _log("C1: Filtrando filas sin evaluados...")
    if "CANTIDADEVALUADOS" in df.columns:
        ce = pd.to_numeric(df["CANTIDADEVALUADOS"], errors="coerce")
        mask_c1 = (ce == 0) | ce.isnull()
        n_c1 = int(mask_c1.sum())
        df = df[~mask_c1].copy()
    else:
        n_c1 = 0
    pct_c1 = 100 * n_c1 / n_original if n_original > 0 else 0
    log_lines.append(f"C1 — Eliminadas sin evaluados (CE=0 o nulo): {n_c1:,} ({pct_c1:.2f}%)")
    _log(f"  C1: {n_c1:,} filas eliminadas")

    # ── REGLA C2: Eliminar filas sin target (NUNCA imputar) ─────────────────
    _log("C2: Filtrando filas sin target (PROMEDIO_GLOBAL / PROMEDIO_PRUEBA nulos)...")
    n_after_c1 = len(df)

    # 2a: PROMEDIO_GLOBAL nulo
    if "PROMEDIO_GLOBAL" in df.columns:
        mask_pg = pd.to_numeric(df["PROMEDIO_GLOBAL"], errors="coerce").isnull()
        n_pg = int(mask_pg.sum())
        df = df[~mask_pg].copy()
    else:
        n_pg = 0

    # 2b: PROMEDIO_PRUEBA nulo (segunda target)
    if "PROMEDIO_PRUEBA" in df.columns:
        mask_pp = pd.to_numeric(df["PROMEDIO_PRUEBA"], errors="coerce").isnull()
        n_pp = int(mask_pp.sum())
        df = df[~mask_pp].copy()
    else:
        n_pp = 0

    n_c2 = n_pg + n_pp
    pct_c2 = 100 * n_c2 / n_original if n_original > 0 else 0
    log_lines.append(f"C2 — Eliminadas por PROMEDIO_GLOBAL nulo : {n_pg:,}")
    log_lines.append(f"C2 — Eliminadas por PROMEDIO_PRUEBA nulo : {n_pp:,}")
    log_lines.append(f"C2 — Total eliminadas (targets nulos)    : {n_c2:,} ({pct_c2:.2f}%)")
    log_lines.append(f"     NOTA: targets NUNCA imputados (Regla R2)")
    _log(f"  C2: {n_c2:,} filas eliminadas (PROMEDIO_GLOBAL={n_pg}, PROMEDIO_PRUEBA={n_pp})")

    # ── REGLA C3: Métricas secundarias nulas → conservar fila, documentar ───
    _log("C3: Auditando métricas secundarias nulas...")
    secondary_cols = ["DESVIACION", "NIVEL1", "NIVEL2", "NIVEL3", "NIVEL4"]
    secondary_present = [c for c in secondary_cols if c in df.columns]
    log_lines.append("")
    log_lines.append("C3 — Métricas secundarias (filas conservadas, columnas con nulos):")
    for col in secondary_present:
        n_null = int(pd.to_numeric(df[col], errors="coerce").isnull().sum())
        pct = 100 * n_null / len(df) if len(df) > 0 else 0
        log_lines.append(f"  {col:<25}: {n_null:,} nulos ({pct:.1f}%) — fila conservada")
    log_lines.append("  Estrategia: imputación por mediana de grupo (NBC + NOMBRE_PRUEBA) en Fase 3")

    # ── REGLA C4: Eliminar duplicados exactos ───────────────────────────────
    _log("C4: Eliminando duplicados exactos...")
    dup_key = [c for c in KEY4 + ["AGREGACION"] if c in df.columns]
    n_before_c4 = len(df)
    df = df.drop_duplicates(subset=dup_key, keep="first").copy()
    n_c4 = n_before_c4 - len(df)
    pct_c4 = 100 * n_c4 / n_original if n_original > 0 else 0
    log_lines.append("")
    log_lines.append(f"C4 — Eliminados duplicados exactos: {n_c4:,} ({pct_c4:.2f}%)")
    log_lines.append(f"     Clave de unicidad: {dup_key}")
    _log(f"  C4: {n_c4:,} duplicados eliminados")

    # ── REGLA C5: Normalizar tipos ──────────────────────────────────────────
    _log("C5: Normalizando tipos de dato...")

    # Numéricos
    for col in ["CANTIDADEVALUADOS"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    for col in ["PROMEDIO_GLOBAL", "PROMEDIO_PRUEBA", "DESVIACION",
                "NIVEL1", "NIVEL2", "NIVEL3", "NIVEL4"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("float64")

    # IDs como string (para uso categórico, no aritmético)
    for col in ["ID_PAIS", "ID_REGION", "ID_DEPARTAMENTO", "ID_MUNICIPIO",
                "ID_INSTITUCION", "ID_SEDE", "ID_GRUPOREFERENCIA",
                "ID_NBC", "ID_PROGRAMA_ACAD", "CATEGORIAPRUEBA"]:
        if col in df.columns:
            df[col] = df[col].apply(
                lambda x: str(int(x)) if pd.notna(x) and x == x else None
            )

    # Texto: strip + upper
    text_cols = [c for c in df.columns if df[c].dtype == object]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip().str.upper()
        df[col] = df[col].replace({"NAN": None, "NONE": None, "": None})

    # AÑO como int
    if "AÑO" in df.columns:
        df["AÑO"] = df["AÑO"].astype(int)

    log_lines.append("")
    log_lines.append("C5 — Normalización de tipos:")
    log_lines.append("  CANTIDADEVALUADOS      → Int64")
    log_lines.append("  PROMEDIO_GLOBAL/PRUEBA → float64")
    log_lines.append("  NIVEL1-4, DESVIACION   → float64")
    log_lines.append("  IDs numéricos          → str (uso categórico)")
    log_lines.append("  Columnas de texto      → strip + upper")

    # ── RESUMEN FINAL ────────────────────────────────────────────────────────
    n_final = len(df)
    pct_retained = 100 * n_final / n_original if n_original > 0 else 0
    log_lines.append("")
    log_lines.append("=" * 70)
    log_lines.append("RESUMEN DE LIMPIEZA")
    log_lines.append("=" * 70)
    log_lines.append(f"Filas post-pivot (pre-limpieza) : {n_original:,}")
    log_lines.append(f"Eliminadas C1 (sin evaluados)   : {n_c1:,} ({pct_c1:.2f}%)")
    log_lines.append(f"Eliminadas C2 (target nulos)    : {n_c2:,} ({pct_c2:.2f}%)")
    log_lines.append(f"Eliminadas C4 (duplicados)      : {n_c4:,} ({pct_c4:.2f}%)")
    log_lines.append(f"Filas finales                   : {n_final:,} ({pct_retained:.1f}% del post-pivot)")
    log_lines.append("")
    log_lines.append(f"Columnas del dataset limpio     : {len(df.columns)}")
    log_lines.append(f"Columnas: {list(df.columns)}")

    _log(f"Limpieza completa: {n_original:,} → {n_final:,} filas ({pct_retained:.1f}% retenido)")
    return df, log_lines
