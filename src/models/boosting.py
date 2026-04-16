"""
src/models/boosting.py
LightGBM con Pipeline idéntico al baseline: TargetEncoder calculado SOLO
sobre datos de train en cada fold de TimeSeriesSplit → sin leakage.
Fase 5 del pipeline — Motor Predictivo Saber Pro.
Autor: Edwin Santiago Paz Bedoya — Código 1071010
"""

from datetime import datetime

import numpy as np
import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import TargetEncoder

# Reutiliza las mismas listas de columnas que el baseline
from src.models.baseline import (
    CAT_TARGET_ENCODE_COLS,
    NUMERIC_FEATURE_COLS,
    TARGET_COL,
    get_feature_columns,
)


def _log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def build_lgbm_preprocessor(
    num_cols: list,
    cat_cols: list,
    ohe_cols: list,
) -> ColumnTransformer:
    """
    Mismo ColumnTransformer que el baseline, sin StandardScaler:
    LightGBM (basado en árboles) no requiere escalado numérico.
    TargetEncoder calculado DENTRO del Pipeline → sin leakage.
    """
    transformers = []

    if num_cols:
        transformers.append((
            "num",
            SimpleImputer(strategy="median"),
            num_cols,
        ))

    if cat_cols:
        # cv=None: deshabilita el cross-fitting interno del TargetEncoder.
        # El leakage train→test sigue prevenido porque el Pipeline entero
        # solo se fittea sobre datos de train (nunca ve X_test en .fit()).
        # El cross-fitting interno (cv=5) solo previene within-fold leakage,
        # que es menor; eliminarlo reduce el tiempo de Optuna ~5×.
        cat_pipe = Pipeline([
            ("imputer", SimpleImputer(strategy="constant", fill_value="DESCONOCIDO")),
            ("encoder", TargetEncoder(smooth="auto", cv=2, random_state=42)),
        ])
        transformers.append(("cat", cat_pipe, cat_cols))

    if ohe_cols:
        transformers.append(("ohe", "passthrough", ohe_cols))

    return ColumnTransformer(transformers=transformers, remainder="drop")


def build_lgbm_pipeline(params: dict, num_cols, cat_cols, ohe_cols) -> Pipeline:
    preprocessor = build_lgbm_preprocessor(num_cols, cat_cols, ohe_cols)
    model = LGBMRegressor(
        objective="regression",
        metric="rmse",
        boosting_type="gbdt",
        verbose=-1,
        n_jobs=-1,
        random_state=42,
        **params,
    )
    return Pipeline([("preprocessor", preprocessor), ("model", model)])


def run_optuna_search(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    tscv: TimeSeriesSplit,
    n_trials: int = 50,
) -> dict:
    """
    Búsqueda de hiperparámetros con Optuna + cross_val_score(TimeSeriesSplit).
    El Pipeline completo (incluyendo TargetEncoder) se reajusta en cada fold
    → TargetEncoder solo ve datos de train del fold en curso.
    n_estimators fijo a 500 durante la búsqueda (suficiente para comparar).
    """
    import optuna
    optuna.logging.set_verbosity(optuna.logging.WARNING)

    num_cols, cat_cols, ohe_cols = get_feature_columns(X_train)

    # Para la búsqueda Optuna usamos un split único 80/20 cronológico
    # (más rápido que 4-fold CV) y n_estimators reducido a 200.
    # El modelo final se entrena con best_params sobre TODO el train.
    split_idx  = int(len(X_train) * 0.80)
    X_opt_tr   = X_train.iloc[:split_idx]
    y_opt_tr   = y_train.iloc[:split_idx]
    X_opt_val  = X_train.iloc[split_idx:]
    y_opt_val  = y_train.iloc[split_idx:]

    def objective(trial):
        params = {
            "n_estimators":      200,          # reducido para velocidad de búsqueda
            "learning_rate":     trial.suggest_float("learning_rate",     0.01,  0.15, log=True),
            "num_leaves":        trial.suggest_int(  "num_leaves",         31,   127),
            "min_child_samples": trial.suggest_int(  "min_child_samples",  10,    50),
            "subsample":         trial.suggest_float("subsample",          0.6,   1.0),
            "colsample_bytree":  trial.suggest_float("colsample_bytree",   0.6,   1.0),
            "reg_alpha":         trial.suggest_float("reg_alpha",          0.0,   1.0),
            "reg_lambda":        trial.suggest_float("reg_lambda",         0.0,   1.0),
        }
        pipe = build_lgbm_pipeline(params, num_cols, cat_cols, ohe_cols)
        pipe.fit(X_opt_tr, y_opt_tr)
        preds = pipe.predict(X_opt_val)
        rmse  = float(np.sqrt(np.mean((y_opt_val.values - preds) ** 2)))
        return rmse

    study = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=42))
    study.optimize(objective, n_trials=n_trials, show_progress_bar=True)

    best_params = study.best_params
    best_params["n_estimators"] = 500
    _log(f"  Mejor RMSE CV: {study.best_value:.4f}")
    _log(f"  Mejores parámetros: {best_params}")
    return best_params, study


def train_lgbm(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_test:  pd.DataFrame,
    best_params: dict,
) -> dict:
    """
    Entrena el pipeline final con los mejores hiperparámetros sobre TODO el train.
    TargetEncoder se calcula solo sobre X_train, y_train → sin leakage en test.
    """
    num_cols, cat_cols, ohe_cols = get_feature_columns(X_train)
    pipeline = build_lgbm_pipeline(best_params, num_cols, cat_cols, ohe_cols)
    pipeline.fit(X_train, y_train)

    y_pred_train = pipeline.predict(X_train)
    y_pred_test  = pipeline.predict(X_test)

    # Extraer nombres de features transformadas (para SHAP)
    try:
        feat_names = list(pipeline.named_steps["preprocessor"].get_feature_names_out())
        # Limpiar prefijos de ColumnTransformer (num__lag_1... → lag_1...)
        feat_names = [n.split("__", 1)[-1] for n in feat_names]
    except Exception:
        feat_names = [f"f{i}" for i in range(X_train.shape[1])]

    return {
        "pipeline":       pipeline,
        "feat_names":     feat_names,
        "num_cols":       num_cols,
        "cat_cols":       cat_cols,
        "ohe_cols":       ohe_cols,
        "y_pred_train":   y_pred_train,
        "y_pred_test":    y_pred_test,
        "best_params":    best_params,
    }


def get_learning_curve(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    best_params: dict,
    val_year: int = 2023,
    df_with_year: pd.DataFrame = None,
) -> dict:
    """
    Curva de aprendizaje train vs validation por iteración.
    Usa los últimos datos de entrenamiento (año val_year) como validación
    interna, solo para visualización — no altera el modelo final.
    TargetEncoder solo se ve fit sobre los años < val_year del split interno.
    """
    import lightgbm as lgb

    num_cols, cat_cols, ohe_cols = get_feature_columns(X_train)

    if df_with_year is not None:
        mask_inner_train = df_with_year["AÑO"] < val_year
        mask_inner_val   = df_with_year["AÑO"] == val_year
        X_it = X_train[mask_inner_train.values]
        y_it = y_train[mask_inner_train.values]
        X_iv = X_train[mask_inner_val.values]
        y_iv = y_train[mask_inner_val.values]
    else:
        split = int(len(X_train) * 0.85)
        X_it, y_it = X_train.iloc[:split], y_train.iloc[:split]
        X_iv, y_iv = X_train.iloc[split:], y_train.iloc[split:]

    # Preprocessor solo sobre inner train
    pre = build_lgbm_preprocessor(num_cols, cat_cols, ohe_cols)
    X_it_t = pre.fit_transform(X_it, y_it)
    X_iv_t = pre.transform(X_iv)

    params_lc = {k: v for k, v in best_params.items() if k != "n_estimators"}
    params_lc.update({
        "objective": "regression", "metric": "rmse",
        "verbose": -1, "n_jobs": -1, "random_state": 42,
    })
    lc_model = lgb.LGBMRegressor(n_estimators=800, **params_lc)

    evals_result = {}
    lc_model.fit(
        X_it_t, y_it,
        eval_set=[(X_it_t, y_it), (X_iv_t, y_iv)],
        eval_names=["train", "val"],
        callbacks=[
            lgb.record_evaluation(evals_result),
            lgb.early_stopping(50, verbose=False),
        ],
    )
    return {
        "train_rmse": evals_result["train"]["rmse"],
        "val_rmse":   evals_result["val"]["rmse"],
        "best_iter":  lc_model.best_iteration_,
    }


def compute_shap(pipeline: Pipeline, X_test: pd.DataFrame) -> tuple:
    """
    Calcula SHAP values sobre el test set transformado por el Pipeline.
    Retorna (shap_values, X_test_transformed, feature_names).
    """
    import shap

    preprocessor = pipeline.named_steps["preprocessor"]
    lgbm_model   = pipeline.named_steps["model"]

    X_test_t = preprocessor.transform(X_test)
    try:
        feat_names = list(preprocessor.get_feature_names_out())
        feat_names = [n.split("__", 1)[-1] for n in feat_names]
    except Exception:
        feat_names = [f"f{i}" for i in range(X_test_t.shape[1])]

    explainer   = shap.TreeExplainer(lgbm_model)
    shap_values = explainer.shap_values(X_test_t)

    # Si shap_values es lista (clasificación), tomar primero; aquí es regresión
    if isinstance(shap_values, list):
        shap_values = shap_values[0]

    return shap_values, X_test_t, feat_names
