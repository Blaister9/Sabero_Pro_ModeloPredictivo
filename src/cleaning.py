"""Pivot, cleaning, and filtering of the raw Saber Pro dataset.

This module implements Phase 2 of the Saber Pro predictive pipeline.  It
receives the multi-year concatenated long-format DataFrame produced by
``ingestion.load_years`` and performs two major transformations:

1. **Long-to-wide pivot** (``_pivot_long_to_wide``): The ICFES publishes
   results in a long format where each row corresponds to one
   ``MEDIDA_AGREGACION`` value for one entity at one aggregation level.
   The pivot reconstructs a single wide row per
   ``(AÑO, ID_INSTITUCION, ID_PROGRAMA_ACAD, NOMBRE_PRUEBA)`` entity by
   joining the three relevant measurement subsets — ``PUNTAJE_PRUEBA`` (base),
   ``PUNTAJE_GLOBAL`` (the prediction target), and
   ``NIVEL_DESEMPEÑO_PRUEBA`` (performance-level distribution).

2. **Cleaning rules C1-C5**: After the pivot, five deterministic rules remove
   or normalise records that would otherwise corrupt model training:
   C1 removes rows with zero or null evaluated students, C2 removes rows with
   null target values (targets are never imputed per design rule R2), C3
   documents secondary-metric nulls for later median imputation in
   ``features.py``, C4 drops exact duplicates, and C5 normalises column
   dtypes so all downstream code can rely on consistent numeric/string types.

The chosen aggregation level is ``PROGRAMA_ACÁDEMICO``, the most granular
level that includes both ``ID_INSTITUCION`` and ``ID_PROGRAMA_ACAD``,
enabling program-level predictions.  Rows at other aggregation levels (e.g.
``NACIONAL``, ``DEPARTAMENTAL``) are discarded during the pivot.

Usage example::

    from src.ingestion import load_years
    from src.cleaning import clean_dataset

    df_raw = load_years([2020, 2021, 2022, 2023, 2024], data_dir="data/raw/")
    df_clean, log_lines = clean_dataset(df_raw)

    print(df_clean.shape)
    with open("outputs/cleaning_log.txt", "w") as f:
        f.write("\\n".join(log_lines))

Warning:
    Target columns ``PROMEDIO_GLOBAL`` and ``PROMEDIO_PRUEBA`` are **never**
    imputed (Regla R2).  Any row with a null target is removed at rule C2.
    Imputing targets would introduce a systematic bias in the label distribution
    and violate the evaluation integrity of the temporal train/test split.
"""

import os
from datetime import datetime

import numpy as np
import pandas as pd


def _log(msg: str) -> None:
    """Print a timestamped log message to stdout.

    Args:
        msg: The message text to print.

    Example:
        >>> _log("Starting pivot")
        [09:15:42] Starting pivot
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


# Columnas clave para la identidad de la entidad (pivot key)
KEY3 = ["AÑO", "ID_INSTITUCION", "ID_PROGRAMA_ACAD"]          # entidad sin prueba
KEY4 = ["AÑO", "ID_INSTITUCION", "ID_PROGRAMA_ACAD", "NOMBRE_PRUEBA"]  # entidad + prueba
"""list[str]: Four-column composite key that uniquely identifies a
program-exam observation: year, institution, academic programme, and exam name.
Used as the deduplication and join key throughout the cleaning phase."""

# Nivel de agregación elegido para modelado
AGREGACION_TARGET = "PROGRAMA_ACÁDEMICO"
"""str: The aggregation level used for modelling.

Chosen because it is the most granular level that retains both
``ID_INSTITUCION`` and ``ID_PROGRAMA_ACAD``, enabling institution- and
program-level predictions.  All rows at other aggregation levels are discarded
during the pivot step.
"""

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
"""list[str]: Context columns retained from the ``PUNTAJE_PRUEBA`` subset.

These columns form the base of the wide-format row before the global score
and performance-level columns are joined in.  Only columns actually present
in the DataFrame are selected to guard against minor schema differences
between years.
"""


def _pivot_long_to_wide(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Convert the long-format ICFES dataset to one wide row per entity.

    Implements a three-step join strategy validated against the audited schema:

    1. **Base** — ``PUNTAJE_PRUEBA`` at ``PROGRAMA_ACÁDEMICO`` level.
       One row per ``(AÑO, ID_INSTITUCION, ID_PROGRAMA_ACAD, NOMBRE_PRUEBA)``.
       Retains context columns (location, institution, evaluated count,
       exam score, and standard deviation).
    2. **Inner join** with ``PUNTAJE_GLOBAL`` at the same level.
       Appends ``PROMEDIO_GLOBAL`` (the prediction target).  Entities without
       a global score are discarded; this is intentional because a row without
       a target cannot be used for supervised learning.
    3. **Left join** with ``NIVEL_DESEMPEÑO_PRUEBA``.
       Appends ``NIVEL1`` through ``NIVEL4`` (performance-level percentages).
       ``NIVEL5`` is excluded because it has 99.42% nulls at this aggregation
       level.  ``PERCENTIL_PRUEBA`` does not exist at ``PROGRAMA_ACÁDEMICO``
       and is therefore omitted.

    Duplicate rows within each join key are resolved by keeping the first
    occurrence and logging a warning.

    Args:
        df_raw: The raw concatenated long-format DataFrame produced by
            ``ingestion.load_years``.  Must contain the columns ``MEDIDA_AGREGACION``,
            ``AGREGACION``, ``PROMEDIO_GLOBAL``, and all entries of ``CONTEXT_COLS``
            that are relevant to the current year's schema.

    Returns:
        A wide-format DataFrame with one row per
        ``(AÑO, ID_INSTITUCION, ID_PROGRAMA_ACAD, NOMBRE_PRUEBA)`` entity,
        including context columns from the base join, ``PROMEDIO_GLOBAL`` from
        the target join, and ``NIVEL1``-``NIVEL4`` from the performance join.

    Raises:
        KeyError: If the ``MEDIDA_AGREGACION`` or ``AGREGACION`` column is
            absent from ``df_raw`` (indicates incorrect input data).

    Example:
        >>> df_wide = _pivot_long_to_wide(df_raw)
        >>> df_wide.columns.tolist()
        ['AÑO', 'ID_PAIS', ..., 'PROMEDIO_GLOBAL', 'NIVEL1', 'NIVEL2', ...]
        >>> df_wide.duplicated(subset=KEY4).sum()
        0

    Note:
        Entities present in ``PUNTAJE_PRUEBA`` but absent from
        ``PUNTAJE_GLOBAL`` are silently dropped by the inner join.  This is
        by design: a program-exam-year with a sub-test score but no composite
        global score cannot serve as a training example.  The drop count is
        logged to aid in data quality audits.
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
    """Apply the long-to-wide pivot and cleaning rules C1-C5 to the raw dataset.

    This is the main entry point for Phase 2 of the pipeline.  It calls
    ``_pivot_long_to_wide`` first to convert the long-format input to a
    one-row-per-entity wide format, then sequentially applies five deterministic
    cleaning rules:

    - **C1**: Remove rows where ``CANTIDADEVALUADOS`` is zero or null.
      A program with no evaluated students cannot have a reliable mean score.
    - **C2**: Remove rows where ``PROMEDIO_GLOBAL`` or ``PROMEDIO_PRUEBA`` is
      null.  Targets are **never** imputed (Regla R2 of the pipeline design).
    - **C3**: Audit secondary metrics (``DESVIACION``, ``NIVEL1``-``NIVEL4``)
      for nulls without dropping rows.  These nulls are imputed later in
      ``features.build_features`` using grouped medians.
    - **C4**: Drop exact duplicate rows on the ``KEY4`` composite key.
    - **C5**: Normalise column dtypes — ``CANTIDADEVALUADOS`` to ``Int64``,
      numeric scores to ``float64``, ID columns to strings (for categorical
      use, not arithmetic), and text columns to stripped uppercased strings.

    A detailed cleaning log is accumulated and returned alongside the cleaned
    DataFrame so that callers can persist it to disk for audit purposes.

    Args:
        df_raw: Raw concatenated long-format DataFrame produced by
            ``ingestion.load_years``.  Must be the unmodified output of that
            function — in particular it must still contain the
            ``MEDIDA_AGREGACION`` and ``AGREGACION`` columns needed by the
            pivot step.

    Returns:
        A tuple ``(df_clean, log_lines)`` where:

        - ``df_clean`` is a wide-format DataFrame with one row per
          ``(AÑO, ID_INSTITUCION, ID_PROGRAMA_ACAD, NOMBRE_PRUEBA)`` entity,
          ready for feature engineering.
        - ``log_lines`` is a list of strings forming a human-readable cleaning
          report that documents how many rows each rule removed and why.

    Raises:
        KeyError: If ``MEDIDA_AGREGACION`` or ``AGREGACION`` is absent from
            ``df_raw``, indicating the wrong DataFrame was passed (e.g. one
            that was already pivoted).

    Example:
        >>> from src.ingestion import load_years
        >>> df_raw = load_years([2020, 2021, 2022, 2023, 2024], "data/raw/")
        >>> df_clean, log = clean_dataset(df_raw)
        >>> df_clean.shape
        (38500, 22)
        >>> print(log[0])
        ======================================================================
        >>> # Persist the cleaning log
        >>> with open("outputs/cleaning_log.txt", "w") as f:
        ...     f.write("\\n".join(log))

    Note:
        The temporal train/test split (train 2020-2023, test 2024) is NOT
        applied here.  It is the responsibility of the calling phase script
        (``fase4_baseline.py``, etc.) to split the cleaned DataFrame by year
        before fitting any model.  Applying the split before cleaning would
        cause the pivot and deduplication logic to behave differently on
        partial data, potentially introducing subtle inconsistencies.
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
