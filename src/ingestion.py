"""Multi-year data loader for ICFES Saber Pro raw files.

This module is responsible for Phase 1 of the Saber Pro predictive pipeline:
loading and concatenating the annual raw data files published by the ICFES.
Each year's file is discovered via a configurable file-pattern and directory,
with automatic fallback to several common naming conventions. Both Excel (.xlsx)
and CSV (comma- or semicolon-delimited) formats are supported.

After loading, all column names are normalised (stripped, uppercased) and an
``AÑO`` column is appended so that downstream phases can perform temporal
operations without relying on the source file name.  An optional
``COLUMN_ALIASES`` dictionary allows ad-hoc renaming when a source file uses a
non-canonical column name without requiring changes to the rest of the pipeline.

The module performs a cross-year schema consistency check: any column added or
dropped between years is logged as a warning.  A final pass validates that every
column listed in ``EXPECTED_COLUMNS`` is present in the consolidated frame;
missing columns are reported so the caller can update ``COLUMN_ALIASES``
accordingly.

Usage example::

    from src.ingestion import load_years

    df_raw = load_years(
        years=[2020, 2021, 2022, 2023, 2024],
        data_dir="data/raw/",
        file_pattern="saber_pro_{year}.xlsx",
    )
    print(df_raw.shape)         # (N_rows, N_cols + 1)
    print(df_raw["AÑO"].value_counts().sort_index())

Warning:
    This module only loads and lightly normalises the raw data.  No filtering,
    pivot, or feature engineering is performed here.  Downstream cleaning
    (``cleaning.py``) must be run before the data is suitable for modelling.
    Passing the raw concatenated frame directly to a model will result in
    target leakage because the long-format rows contain the target variable
    mixed with auxiliary aggregation rows.
"""

import os
import pandas as pd
from datetime import datetime


def _log(msg: str) -> None:
    """Print a timestamped log message to stdout.

    Args:
        msg: The message text to print.

    Example:
        >>> _log("Loading year 2022")
        [14:03:27] Loading year 2022
    """
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


# Mapeo de nombres de columnas alternativos → nombre canónico esperado
# Se actualiza si el archivo real tiene nombres distintos al schema esperado.
COLUMN_ALIASES = {
    # Agregar aquí cualquier mapeo detectado durante la auditoría
    # "NOMBRE_REAL_EN_ARCHIVO": "NOMBRE_CANONICO",
}

EXPECTED_COLUMNS = [
    "EXAMEN", "AGREGACION", "MEDIDA_AGREGACION", "CANTIDADEVALUADOS",
    "ID_PAIS", "ID_REGION", "NOMBRE_REGION", "ID_DEPARTAMENTO", "NOMBRE_DEPARTAMENTO",
    "ID_MUNICIPIO", "NOMBRE_MUNICIPIO", "ID_INSTITUCION", "NOMBRE_INSTITUCION",
    "ID_SEDE", "NOMBRE_SEDE", "ID_GRUPOREFERENCIA", "NOMBRE_GRUPOREF",
    "ID_NBC", "NBC", "ID_PROGRAMA_ACAD", "NOMBRE_PROGRAMA_ACAD",
    "NOMBRE_PRUEBA", "CATEGORIAPRUEBA", "PROMEDIO_GLOBAL", "PROMEDIO_PRUEBA",
    "DESVIACION", "PROMEDIO_PERCENTIL", "NIVEL1", "NIVEL2", "NIVEL3", "NIVEL4", "NIVEL5",
    "AFIRMACION", "PORCENTAJERTAINCORRECTA",
]
"""list[str]: Canonical column names expected in every annual Saber Pro file.

Any column absent from the loaded frame is reported as a warning so the caller
can add an entry to ``COLUMN_ALIASES`` if the source file uses a different name.
"""


def _load_single_year(year: int, data_dir: str, file_pattern: str) -> pd.DataFrame:
    """Load a single year's Saber Pro file, auto-detecting format and delimiter.

    Tries the caller-supplied ``file_pattern`` first, then falls back to three
    common alternative naming conventions.  Supports ``.xlsx``, ``.xls``, and
    ``.csv`` files; CSV delimiter (comma vs. semicolon) is inferred from the
    first 4 KB of the file.

    Column names are normalised (stripped, uppercased) after loading so that
    downstream code can use consistent identifiers regardless of how the source
    file was formatted.  Any entry in ``COLUMN_ALIASES`` is applied before
    the ``AÑO`` column is appended.

    Args:
        year: The calendar year to load (e.g. ``2022``).
        data_dir: Directory that contains the raw annual files.
        file_pattern: Filename template with a ``{year}`` placeholder
            (e.g. ``"saber_pro_{year}.xlsx"``).

    Returns:
        A DataFrame with normalised column names and an additional ``AÑO``
        column set to ``year``.

    Raises:
        FileNotFoundError: If none of the candidate file paths exist on disk.
        ValueError: If the discovered file has an unsupported extension
            (i.e. neither ``.xlsx``/``.xls`` nor ``.csv``).

    Example:
        >>> df = _load_single_year(2022, "data/raw/", "saber_pro_{year}.xlsx")
        >>> df.shape
        (45000, 34)
        >>> df["AÑO"].unique()
        array([2022])
    """
    # Intentar primero el patrón indicado, luego alternativas
    candidates = [
        os.path.join(data_dir, file_pattern.format(year=year)),
        os.path.join(data_dir, f"saber_pro_{year}.csv"),
        os.path.join(data_dir, f"Saber_Pro_{year}.xlsx"),
        os.path.join(data_dir, f"SaberPro{year}.xlsx"),
    ]

    filepath = None
    for c in candidates:
        if os.path.exists(c):
            filepath = c
            break

    if filepath is None:
        raise FileNotFoundError(
            f"No se encontró archivo para el año {year}. "
            f"Buscado en: {candidates}"
        )

    ext = os.path.splitext(filepath)[1].lower()
    _log(f"Cargando año {year} desde: {filepath}")

    if ext in (".xlsx", ".xls"):
        df = pd.read_excel(filepath, engine="openpyxl")
    elif ext == ".csv":
        # Detectar separador automáticamente
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            sample = f.read(4096)
        sep = ";" if sample.count(";") > sample.count(",") else ","
        df = pd.read_csv(filepath, sep=sep, encoding="utf-8", low_memory=False)
    else:
        raise ValueError(f"Formato no soportado: {ext}")

    # Normalizar nombres de columnas: strip + upper
    df.columns = [c.strip().upper() for c in df.columns]

    # Aplicar aliases si los hay
    df = df.rename(columns=COLUMN_ALIASES)

    # Agregar columna AÑO
    df["AÑO"] = year

    _log(f"  >> {len(df):,} filas cargadas para {year}.")
    return df


def load_years(
    years: list,
    data_dir: str = "data/raw/",
    file_pattern: str = "saber_pro_{year}.xlsx",
) -> pd.DataFrame:
    """Load and concatenate Saber Pro files for multiple years into one DataFrame.

    Iterates over ``years`` in ascending order, loading each annual file via
    ``_load_single_year``.  After loading each year, the column set is compared
    against the first year's schema; any additions or omissions are logged as
    warnings.  ``pandas.concat`` with ``sort=False`` is used so that column
    order follows the first file.

    After concatenation the function checks that every column in
    ``EXPECTED_COLUMNS`` is present.  Missing columns are logged so the caller
    can add the appropriate entries to ``COLUMN_ALIASES``.

    The returned DataFrame is in the original ICFES **long format**: each row
    represents a single measurement (``MEDIDA_AGREGACION``) for a single
    entity at a single aggregation level (``AGREGACION``).  The pivot to
    wide format is performed later by ``cleaning.clean_dataset``.

    Args:
        years: List of integer years to load, e.g. ``[2020, 2021, 2022, 2023, 2024]``.
            Years are sorted internally so order in the list does not matter.
        data_dir: Path to the directory containing the raw annual files.
            Defaults to ``"data/raw/"``.
        file_pattern: Filename template with a ``{year}`` placeholder.
            Defaults to ``"saber_pro_{year}.xlsx"``.

    Returns:
        A concatenated DataFrame with one row per measurement record across all
        requested years, including a new ``AÑO`` column identifying the source
        year.  Column order follows the first loaded year's schema; columns
        present only in later years are appended at the right.

    Raises:
        FileNotFoundError: Propagated from ``_load_single_year`` if any
            requested year's file cannot be found on disk.
        ValueError: Propagated from ``_load_single_year`` if a discovered file
            has an unsupported extension.

    Example:
        >>> df = load_years(
        ...     years=[2020, 2021, 2022, 2023, 2024],
        ...     data_dir="data/raw/",
        ...     file_pattern="saber_pro_{year}.xlsx",
        ... )
        >>> df["AÑO"].value_counts().sort_index()
        2020    45231
        2021    46102
        ...
        >>> "PROMEDIO_GLOBAL" in df.columns
        True

    Note:
        This function loads the raw long-format data.  Do NOT use the returned
        DataFrame directly for modelling.  Always pass it through
        ``cleaning.clean_dataset`` and ``features.build_features`` first to
        perform the long-to-wide pivot, apply cleaning rules C1-C5, and
        engineer lag/trend features without temporal leakage.
    """
    _log(f"Iniciando carga multianual: {years}")
    frames = []
    schema_ref = None
    schema_warnings = []

    for year in sorted(years):
        df_year = _load_single_year(year, data_dir, file_pattern)
        current_cols = set(df_year.columns)

        if schema_ref is None:
            schema_ref = current_cols
        else:
            # Validar consistencia de schema entre años
            diff_added = current_cols - schema_ref
            diff_missing = schema_ref - current_cols
            if diff_added or diff_missing:
                msg = (
                    f"ADVERTENCIA schema año {year}: "
                    f"columnas nuevas={diff_added}, "
                    f"columnas faltantes={diff_missing}"
                )
                _log(msg)
                schema_warnings.append(msg)

        frames.append(df_year)

    df_all = pd.concat(frames, ignore_index=True, sort=False)

    if schema_warnings:
        _log(f"Se encontraron {len(schema_warnings)} diferencias de schema entre años.")

    # Validar columnas esperadas
    missing_expected = [c for c in EXPECTED_COLUMNS if c not in df_all.columns]
    if missing_expected:
        _log(
            f"ADVERTENCIA: columnas esperadas no encontradas en el dataset: "
            f"{missing_expected}"
        )
        _log("  → Verificar COLUMN_ALIASES en ingestion.py si los nombres difieren.")

    _log(f"Carga completada: {len(df_all):,} filas totales, {len(df_all.columns)} columnas.")
    return df_all
