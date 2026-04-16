"""
src/inference.py
Módulo de inferencia para el Motor Predictivo Saber Pro.
Fase 7 del pipeline — Edwin Santiago Paz Bedoya (1071010)

Funciones principales:
    load_model(model_path)          → carga el pipeline LightGBM serializado
    predict_institution(...)        → predicciones por institución/programa
    predict_batch(df, model)        → predicciones en lote sobre un DataFrame
    build_inference_row(...)        → construye una fila de features para un
                                      programa+prueba+año nuevos

Reglas de confianza:
    BAJA_CONFIANZA_MUESTRA_PEQUEÑA = True  cuando CANTIDADEVALUADOS < 5
    BAJA_CONFIANZA_SIN_HISTORIAL   = True  cuando no hay lag_1 disponible
    BAJA_CONFIANZA_EXTRAPOLACION   = True  cuando AÑO > max(año visto en train)

El resultado de predict_institution() es siempre un dict estructurado con
la predicción, los flags de confianza y metadatos explicativos.
"""

from __future__ import annotations

import os
import warnings
from datetime import datetime
from typing import Any, Optional

import joblib
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# ── Constantes ────────────────────────────────────────────────────────────────

UMBRAL_MUESTRA_PEQUENA = 5      # CANTIDADEVALUADOS < 5 → baja confianza
MAX_AÑO_TRAIN          = 2023   # Último año del conjunto de entrenamiento

# Columnas que el pipeline LightGBM espera como entrada
NUMERIC_COLS = [
    "lag_1_promedio_global", "lag_2_promedio_global",
    "lag_1_promedio_prueba",  "lag_2_promedio_prueba",
    "tendencia_global",       "tendencia_prueba",
    "desviacion_estandar_historica", "coeficiente_variacion",
    "log_cantidadevaluados",  "AÑO",
]
CAT_COLS = ["NBC", "NOMBRE_PRUEBA", "ID_DEPARTAMENTO"]
OHE_COLS = ["cat_prueba_1", "cat_prueba_34"]

ALL_FEATURE_COLS = NUMERIC_COLS + CAT_COLS + OHE_COLS

# Mapeo de CATEGORIAPRUEBA a columnas OHE (derivado de Fase 3)
# cat_prueba_1 = CATEGORIAPRUEBA == 1, cat_prueba_34 = CATEGORIAPRUEBA in {3,4}
CATEGORIA_TO_OHE = {
    1:  {"cat_prueba_1": 1, "cat_prueba_34": 0},
    2:  {"cat_prueba_1": 0, "cat_prueba_34": 0},
    3:  {"cat_prueba_1": 0, "cat_prueba_34": 1},
    4:  {"cat_prueba_1": 0, "cat_prueba_34": 1},
}


# ── Carga del modelo ──────────────────────────────────────────────────────────

def load_model(model_path: str) -> Any:
    """
    Carga el pipeline LightGBM serializado con joblib.

    Args:
        model_path: Ruta al archivo .pkl (ej. 'outputs/lgbm_model.pkl')

    Returns:
        Pipeline de sklearn entrenado.

    Raises:
        FileNotFoundError si el archivo no existe.
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Modelo no encontrado en: {model_path}\n"
            "Ejecuta primero: python3 fase5_boosting.py"
        )
    pipeline = joblib.load(model_path)
    return pipeline


# ── Construcción de fila de features ─────────────────────────────────────────

def build_inference_row(
    año:                         int,
    nbc:                         str,
    nombre_prueba:               str,
    id_departamento:             Any,
    cantidadevaluados:           int,
    categoriaprueba:             int                 = 2,
    lag_1_promedio_global:       Optional[float]     = None,
    lag_2_promedio_global:       Optional[float]     = None,
    lag_1_promedio_prueba:       Optional[float]     = None,
    lag_2_promedio_prueba:       Optional[float]     = None,
    tendencia_global:            Optional[float]     = None,
    tendencia_prueba:            Optional[float]     = None,
    desviacion_estandar_historica: Optional[float]  = None,
    coeficiente_variacion:       Optional[float]     = None,
) -> pd.DataFrame:
    """
    Construye una fila de features lista para pasar al pipeline LightGBM.
    Todos los valores None se dejan como NaN → el Imputer del Pipeline
    los imputará con la mediana del conjunto de entrenamiento.

    Args:
        año                 : Año de la predicción (ej. 2025)
        nbc                 : Núcleo Básico del Conocimiento (ej. 'EDUCACIÓN')
        nombre_prueba       : Nombre de la prueba Saber Pro (ej. 'INGLÉS')
        id_departamento     : ID del departamento (int o str)
        cantidadevaluados   : Número de estudiantes que presentarán el examen
        categoriaprueba     : Categoría de la prueba (1=genérica, 2=específica,
                              3=genérica con módulo, 4=específica con módulo)
        lag_1_promedio_global : PROMEDIO_GLOBAL del año anterior (t-1)
        lag_2_promedio_global : PROMEDIO_GLOBAL de hace 2 años (t-2)
        lag_1_promedio_prueba : PROMEDIO_PRUEBA del año anterior (t-1)
        lag_2_promedio_prueba : PROMEDIO_PRUEBA de hace 2 años (t-2)
        tendencia_global    : Pendiente OLS del PROMEDIO_GLOBAL histórico
        tendencia_prueba    : Pendiente OLS del PROMEDIO_PRUEBA histórico
        desviacion_estandar_historica : Std del PROMEDIO_GLOBAL histórico
        coeficiente_variacion : CV del PROMEDIO_GLOBAL histórico

    Returns:
        DataFrame de 1 fila con todas las columnas que espera el pipeline.
    """
    ohe = CATEGORIA_TO_OHE.get(categoriaprueba, {"cat_prueba_1": 0, "cat_prueba_34": 0})

    row = {
        # Numéricas
        "lag_1_promedio_global":        lag_1_promedio_global,
        "lag_2_promedio_global":        lag_2_promedio_global,
        "lag_1_promedio_prueba":         lag_1_promedio_prueba,
        "lag_2_promedio_prueba":         lag_2_promedio_prueba,
        "tendencia_global":              tendencia_global,
        "tendencia_prueba":              tendencia_prueba,
        "desviacion_estandar_historica": desviacion_estandar_historica,
        "coeficiente_variacion":         coeficiente_variacion,
        "log_cantidadevaluados":         np.log1p(cantidadevaluados),
        "AÑO":                           float(año),
        # Categóricas
        "NBC":                           str(nbc),
        "NOMBRE_PRUEBA":                 str(nombre_prueba),
        "ID_DEPARTAMENTO":               id_departamento,
        # OHE
        "cat_prueba_1":                  float(ohe["cat_prueba_1"]),
        "cat_prueba_34":                 float(ohe["cat_prueba_34"]),
    }

    return pd.DataFrame([row])


# ── Evaluación de flags de confianza ─────────────────────────────────────────

def _evaluate_confidence_flags(
    cantidadevaluados: int,
    lag_1_global:      Optional[float],
    año:               int,
) -> dict:
    """
    Evalúa los flags de confianza de la predicción.

    Returns dict con:
        baja_confianza_muestra_pequeña : bool
        baja_confianza_sin_historial   : bool
        baja_confianza_extrapolacion   : bool
        confianza_global               : str  ('ALTA', 'MEDIA', 'BAJA')
        advertencias                   : list[str]
    """
    flags = {
        "baja_confianza_muestra_pequeña": False,
        "baja_confianza_sin_historial":   False,
        "baja_confianza_extrapolacion":   False,
    }
    advertencias = []

    # Flag 1: Muestra pequeña — recomendado en analisis_outliers.txt
    if cantidadevaluados < UMBRAL_MUESTRA_PEQUENA:
        flags["baja_confianza_muestra_pequeña"] = True
        advertencias.append(
            f"CANTIDADEVALUADOS={cantidadevaluados} < {UMBRAL_MUESTRA_PEQUENA}. "
            f"Con muy pocos estudiantes evaluados el promedio del programa es "
            f"altamente sensible a valores individuales atípicos. "
            f"Revisar el outlier documentado en analisis_outliers.txt."
        )

    # Flag 2: Sin historial — no hay lag_1 disponible
    if lag_1_global is None or (isinstance(lag_1_global, float) and np.isnan(lag_1_global)):
        flags["baja_confianza_sin_historial"] = True
        advertencias.append(
            "lag_1_promedio_global no disponible. El modelo usará la mediana "
            "imputada del conjunto de entrenamiento. La predicción es menos "
            "precisa para programas sin historia previa."
        )

    # Flag 3: Extrapolación temporal — predicción fuera del rango de entrenamiento
    if año > MAX_AÑO_TRAIN:
        flags["baja_confianza_extrapolacion"] = True
        años_extra = año - MAX_AÑO_TRAIN
        advertencias.append(
            f"AÑO={año} está {años_extra} año(s) más allá del último año de "
            f"entrenamiento ({MAX_AÑO_TRAIN}). La precisión puede degradarse "
            f"si el sistema educativo cambia significativamente."
        )

    # Confianza global
    n_flags = sum(flags.values())
    if n_flags == 0:
        nivel = "ALTA"
    elif n_flags == 1 and not flags["baja_confianza_muestra_pequeña"]:
        nivel = "MEDIA"
    else:
        nivel = "BAJA"

    return {**flags, "confianza_global": nivel, "advertencias": advertencias}


# ── Función principal de predicción ──────────────────────────────────────────

def predict_institution(
    model:              Any,
    año:                int,
    nbc:                str,
    nombre_prueba:      str,
    id_departamento:    Any,
    cantidadevaluados:  int,
    categoriaprueba:    int              = 2,
    lag_1_promedio_global:       Optional[float] = None,
    lag_2_promedio_global:       Optional[float] = None,
    lag_1_promedio_prueba:       Optional[float] = None,
    lag_2_promedio_prueba:       Optional[float] = None,
    tendencia_global:            Optional[float] = None,
    tendencia_prueba:            Optional[float] = None,
    desviacion_estandar_historica: Optional[float] = None,
    coeficiente_variacion:       Optional[float] = None,
    nombre_institucion: Optional[str]    = None,
    nombre_programa:    Optional[str]    = None,
) -> dict:
    """
    Genera una predicción de PROMEDIO_GLOBAL para un programa-prueba-año,
    con flags de confianza y metadatos de diagnóstico.

    Args:
        model             : Pipeline LightGBM cargado con load_model()
        año               : Año para el que se predice (ej. 2025)
        nbc               : Núcleo Básico del Conocimiento
        nombre_prueba     : Nombre de la prueba Saber Pro
        id_departamento   : ID del departamento
        cantidadevaluados : Número estimado de estudiantes a evaluar
        categoriaprueba   : Categoría de prueba (1-4)
        lag_1_promedio_global  : PROMEDIO_GLOBAL año anterior (None si no hay)
        lag_2_promedio_global  : PROMEDIO_GLOBAL hace 2 años (None si no hay)
        lag_1_promedio_prueba  : PROMEDIO_PRUEBA año anterior (None si no hay)
        lag_2_promedio_prueba  : PROMEDIO_PRUEBA hace 2 años (None si no hay)
        tendencia_global       : Pendiente OLS del PROMEDIO_GLOBAL histórico
        tendencia_prueba       : Pendiente OLS del PROMEDIO_PRUEBA histórico
        desviacion_estandar_historica : Std del PROMEDIO_GLOBAL histórico
        coeficiente_variacion  : CV del PROMEDIO_GLOBAL histórico
        nombre_institucion     : Nombre descriptivo de la institución (metadato)
        nombre_programa        : Nombre descriptivo del programa (metadato)

    Returns:
        dict con los siguientes campos:
            prediccion_promedio_global : float   (valor predicho)
            año                        : int
            nbc                        : str
            nombre_prueba              : str
            id_departamento            : Any
            cantidadevaluados          : int
            nombre_institucion         : str | None
            nombre_programa            : str | None
            # Flags de confianza
            baja_confianza_muestra_pequeña : bool  ← True si CANTIDADEVALUADOS < 5
            baja_confianza_sin_historial   : bool
            baja_confianza_extrapolacion   : bool
            confianza_global               : str   ('ALTA', 'MEDIA', 'BAJA')
            advertencias                   : list[str]
            # Features usadas (para auditoría)
            features_usadas            : dict
            timestamp                  : str
    """
    # 1. Construir fila de features
    X = build_inference_row(
        año=año,
        nbc=nbc,
        nombre_prueba=nombre_prueba,
        id_departamento=id_departamento,
        cantidadevaluados=cantidadevaluados,
        categoriaprueba=categoriaprueba,
        lag_1_promedio_global=lag_1_promedio_global,
        lag_2_promedio_global=lag_2_promedio_global,
        lag_1_promedio_prueba=lag_1_promedio_prueba,
        lag_2_promedio_prueba=lag_2_promedio_prueba,
        tendencia_global=tendencia_global,
        tendencia_prueba=tendencia_prueba,
        desviacion_estandar_historica=desviacion_estandar_historica,
        coeficiente_variacion=coeficiente_variacion,
    )

    # 2. Predicción
    pred = float(model.predict(X)[0])

    # 3. Flags de confianza
    confidence = _evaluate_confidence_flags(
        cantidadevaluados=cantidadevaluados,
        lag_1_global=lag_1_promedio_global,
        año=año,
    )

    # 4. Features usadas (para auditoría / explicabilidad)
    features_dict = X.iloc[0].to_dict()

    return {
        "prediccion_promedio_global":    pred,
        "año":                           año,
        "nbc":                           nbc,
        "nombre_prueba":                 nombre_prueba,
        "id_departamento":               id_departamento,
        "cantidadevaluados":             cantidadevaluados,
        "nombre_institucion":            nombre_institucion,
        "nombre_programa":               nombre_programa,
        # Flags
        "baja_confianza_muestra_pequeña": confidence["baja_confianza_muestra_pequeña"],
        "baja_confianza_sin_historial":   confidence["baja_confianza_sin_historial"],
        "baja_confianza_extrapolacion":   confidence["baja_confianza_extrapolacion"],
        "confianza_global":               confidence["confianza_global"],
        "advertencias":                   confidence["advertencias"],
        # Auditoría
        "features_usadas":               features_dict,
        "timestamp":                     datetime.now().isoformat(),
    }


# ── Predicción en lote ────────────────────────────────────────────────────────

def predict_batch(
    df:    pd.DataFrame,
    model: Any,
) -> pd.DataFrame:
    """
    Predicciones en lote sobre un DataFrame con las columnas del pipeline.

    El DataFrame debe contener al mínimo:
        - Todas las columnas de ALL_FEATURE_COLS (NaN permitido en lags/tendencias)
        - CANTIDADEVALUADOS (para evaluar los flags de confianza)
        - AÑO

    Columnas opcionales que se incluirán en el resultado si están presentes:
        ID_INSTITUCION, ID_PROGRAMA_ACAD, NOMBRE_INSTITUCION,
        NOMBRE_PROGRAMA_ACAD, NBC, NOMBRE_PRUEBA, AÑO

    Returns:
        DataFrame con las columnas originales más:
            prediccion_promedio_global
            baja_confianza_muestra_pequeña
            baja_confianza_sin_historial
            baja_confianza_extrapolacion
            confianza_global
    """
    df = df.copy()

    # Asegurar columnas OHE si no están (ej. input limpio sin OHE pre-calculado)
    if "cat_prueba_1" not in df.columns:
        df["cat_prueba_1"] = 0.0
    if "cat_prueba_34" not in df.columns:
        df["cat_prueba_34"] = 0.0

    # Predicciones
    X = df[ALL_FEATURE_COLS]
    preds = model.predict(X)
    df["prediccion_promedio_global"] = preds

    # Flags de confianza vectorizados
    cant = df["CANTIDADEVALUADOS"] if "CANTIDADEVALUADOS" in df.columns else pd.Series(
        [UMBRAL_MUESTRA_PEQUENA] * len(df), index=df.index
    )
    lag1 = df.get("lag_1_promedio_global", pd.Series([np.nan] * len(df), index=df.index))
    año_col = df["AÑO"] if "AÑO" in df.columns else pd.Series([MAX_AÑO_TRAIN] * len(df))

    df["baja_confianza_muestra_pequeña"] = cant < UMBRAL_MUESTRA_PEQUENA
    df["baja_confianza_sin_historial"]   = lag1.isna()
    df["baja_confianza_extrapolacion"]   = año_col > MAX_AÑO_TRAIN

    # Nivel de confianza global
    n_flags = (
        df["baja_confianza_muestra_pequeña"].astype(int)
        + df["baja_confianza_sin_historial"].astype(int)
        + df["baja_confianza_extrapolacion"].astype(int)
    )
    df["confianza_global"] = np.where(
        n_flags == 0, "ALTA",
        np.where(
            (n_flags == 1) & (~df["baja_confianza_muestra_pequeña"]),
            "MEDIA",
            "BAJA"
        )
    )

    return df


# ── Helpers de formato ────────────────────────────────────────────────────────

def format_prediction_report(result: dict) -> str:
    """
    Formatea el resultado de predict_institution() como texto legible.
    """
    flag_si_no = lambda b: "SÍ ⚠" if b else "no"

    lines = [
        "=" * 60,
        "PREDICCIÓN MOTOR SABER PRO",
        "=" * 60,
    ]
    if result.get("nombre_institucion"):
        lines.append(f"Institución  : {result['nombre_institucion']}")
    if result.get("nombre_programa"):
        lines.append(f"Programa     : {result['nombre_programa']}")
    lines += [
        f"NBC          : {result['nbc']}",
        f"Prueba       : {result['nombre_prueba']}",
        f"Año          : {result['año']}",
        f"N evaluados  : {result['cantidadevaluados']}",
        "",
        f"PROMEDIO_GLOBAL predicho : {result['prediccion_promedio_global']:.2f}",
        f"Confianza global         : {result['confianza_global']}",
        "",
        "Flags de confianza:",
        f"  Muestra pequeña (N<{UMBRAL_MUESTRA_PEQUENA}): "
            f"{flag_si_no(result['baja_confianza_muestra_pequeña'])}",
        f"  Sin historial previo:   "
            f"{flag_si_no(result['baja_confianza_sin_historial'])}",
        f"  Extrapolación temporal: "
            f"{flag_si_no(result['baja_confianza_extrapolacion'])}",
    ]
    if result["advertencias"]:
        lines.append("")
        lines.append("Advertencias:")
        for i, adv in enumerate(result["advertencias"], 1):
            # Wrap a 56 chars
            words = adv.split()
            line, wrapped = [], []
            for w in words:
                if sum(len(x) + 1 for x in line) + len(w) > 54:
                    wrapped.append("  " + " ".join(line))
                    line = [w]
                else:
                    line.append(w)
            if line:
                wrapped.append("  " + " ".join(line))
            lines.append(f"  [{i}] {wrapped[0].strip()}")
            for l in wrapped[1:]:
                lines.append(f"      {l.strip()}")

    lines += ["", f"Timestamp: {result['timestamp']}", "=" * 60]
    return "\n".join(lines)
