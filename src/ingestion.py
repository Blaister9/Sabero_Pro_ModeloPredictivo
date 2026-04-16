"""
src/ingestion.py
Carga y concatenación multianual de archivos Saber Pro del ICFES.
Autor: Edwin Santiago Paz Bedoya — Código 1071010
"""

import os
import pandas as pd
from datetime import datetime


def _log(msg: str) -> None:
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


def _load_single_year(year: int, data_dir: str, file_pattern: str) -> pd.DataFrame:
    """Carga un único año. Detecta .xlsx o .csv automáticamente."""
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
    """
    Carga y concatena archivos Saber Pro de múltiples años.

    Parameters
    ----------
    years : list[int]
        Lista de años a cargar, e.g. [2020, 2021, 2022, 2023, 2024].
    data_dir : str
        Directorio donde están los archivos crudos.
    file_pattern : str
        Patrón de nombre de archivo con placeholder {year}.

    Returns
    -------
    pd.DataFrame
        DataFrame consolidado con columna AÑO.
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
