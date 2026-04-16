"""
src/models/baseline.py
Modelos lineales Ridge y Lasso con Pipeline que incluye target encoding
calculado solo sobre datos de train en cada fold de TimeSeriesSplit.
Fase 4 del pipeline — Motor Predictivo Saber Pro.
Autor: Edwin Santiago Paz Bedoya — Código 1071010
"""

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LassoCV, RidgeCV
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, TargetEncoder


# ── Definición de columnas por tipo ──────────────────────────────────────────

# Categóricas que van a TargetEncoder (calculado DENTRO del Pipeline → sin leakage)
CAT_TARGET_ENCODE_COLS = ["NBC", "NOMBRE_PRUEBA", "ID_DEPARTAMENTO"]

# Numéricas construidas en Fase 3 — solo features sin leakage temporal
# EXCLUIDAS explícitamente (concurrent con el target del mismo año):
#   PROMEDIO_PRUEBA  → mismo release ICFES que PROMEDIO_GLOBAL
#   DESVIACION       → de PUNTAJE_PRUEBA, mismo año
#   NIVEL1-4         → de NIVEL_DESEMPEÑO_PRUEBA, mismo año
#   prop_nivel*      → derivadas de NIVEL1-4 (concurrent_prop_* en CSV)
#   delta_1_global   → = PROMEDIO_GLOBAL - lag_1 (target leak directo, eliminado)
# CORREGIDAS (tendencia y volatilidad ahora usan solo historia t-1):
#   tendencia_global, tendencia_prueba → expanding lag, excluyen año t
#   desviacion_estandar_historica, coeficiente_variacion → idem
NUMERIC_FEATURE_COLS = [
    # Lags temporales (historia t-1, t-2 — sin leakage)
    "lag_1_promedio_global", "lag_2_promedio_global",
    "lag_1_promedio_prueba",  "lag_2_promedio_prueba",
    # Tendencia (expanding lag: slope calculado con historia hasta t-1)
    "tendencia_global", "tendencia_prueba",
    # Volatilidad (expanding lag: std/CV calculados con historia hasta t-1)
    "desviacion_estandar_historica", "coeficiente_variacion",
    # Contexto (tamaño de cohorte, disponible antes de resultados)
    "log_cantidadevaluados",
    # Tendencia temporal global del sistema educativo
    "AÑO",
]

TARGET_COL = "PROMEDIO_GLOBAL"


def get_feature_columns(df: pd.DataFrame) -> tuple[list, list, list]:
    """
    Retorna (numeric_cols, cat_cols, ohe_cols) disponibles en df.
    """
    num_cols = [c for c in NUMERIC_FEATURE_COLS if c in df.columns]
    cat_cols = [c for c in CAT_TARGET_ENCODE_COLS if c in df.columns]
    # Columnas OHE ya creadas en Fase 3 (cat_prueba_*)
    ohe_cols = [c for c in df.columns if c.startswith("cat_prueba_")]
    return num_cols, cat_cols, ohe_cols


def build_preprocessor(num_cols: list, cat_cols: list, ohe_cols: list) -> ColumnTransformer:
    """
    ColumnTransformer con:
    - Numéricas: SimpleImputer(mediana) + StandardScaler
    - Categóricas (te): TargetEncoder (smoothing='auto', cv=5) — SIN leakage
    - OHE (binarias): pass-through (ya son 0/1)
    """
    transformers = []

    if num_cols:
        numeric_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler",  StandardScaler()),
        ])
        transformers.append(("num", numeric_pipe, num_cols))

    if cat_cols:
        # TargetEncoder de sklearn 1.3+: calcula el encoding DENTRO del fit
        # sobre los datos de train que recibe → sin leakage cuando se usa
        # dentro de un Pipeline con TimeSeriesSplit.
        te_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="constant", fill_value="DESCONOCIDO")),
            ("encoder", TargetEncoder(smooth="auto", cv=2, random_state=42)),
        ])
        transformers.append(("cat", te_pipe, cat_cols))

    if ohe_cols:
        transformers.append(("ohe", "passthrough", ohe_cols))

    return ColumnTransformer(transformers=transformers, remainder="drop")


def train_ridge(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test:  pd.DataFrame,
    y_test:  pd.Series,
    tscv:    TimeSeriesSplit,
) -> dict:
    """
    Entrena Ridge con RidgeCV usando TimeSeriesSplit dentro del train.
    Retorna el pipeline entrenado y métricas básicas de evaluación.
    """
    num_cols, cat_cols, ohe_cols = get_feature_columns(X_train)
    preprocessor = build_preprocessor(num_cols, cat_cols, ohe_cols)

    alphas = np.logspace(-3, 5, 60)
    ridge = RidgeCV(alphas=alphas, cv=tscv, scoring="neg_mean_squared_error")

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model",        ridge),
    ])
    pipeline.fit(X_train, y_train)

    y_pred_train = pipeline.predict(X_train)
    y_pred_test  = pipeline.predict(X_test)

    return {
        "pipeline":      pipeline,
        "alpha":         pipeline.named_steps["model"].alpha_,
        "num_features":  len(num_cols) + len(cat_cols) + len(ohe_cols),
        "feature_names": num_cols + cat_cols + ohe_cols,
        "y_pred_train":  y_pred_train,
        "y_pred_test":   y_pred_test,
    }


def train_lasso(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test:  pd.DataFrame,
    y_test:  pd.Series,
    tscv:    TimeSeriesSplit,
) -> dict:
    """
    Entrena Lasso con LassoCV usando TimeSeriesSplit dentro del train.
    Retorna pipeline + lista de features seleccionadas (coef != 0).
    """
    num_cols, cat_cols, ohe_cols = get_feature_columns(X_train)
    preprocessor = build_preprocessor(num_cols, cat_cols, ohe_cols)

    lasso = LassoCV(
        n_alphas=100,
        cv=tscv,
        max_iter=10_000,
        random_state=42,
        n_jobs=-1,
    )

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model",        lasso),
    ])
    pipeline.fit(X_train, y_train)

    coefs = pipeline.named_steps["model"].coef_
    all_names = num_cols + cat_cols + ohe_cols
    selected = [n for n, c in zip(all_names, coefs) if abs(c) > 1e-10]

    y_pred_train = pipeline.predict(X_train)
    y_pred_test  = pipeline.predict(X_test)

    return {
        "pipeline":          pipeline,
        "alpha":             pipeline.named_steps["model"].alpha_,
        "coefs":             dict(zip(all_names, coefs)),
        "selected_features": selected,
        "n_selected":        len(selected),
        "n_total":           len(all_names),
        "feature_names":     all_names,
        "y_pred_train":      y_pred_train,
        "y_pred_test":       y_pred_test,
    }
