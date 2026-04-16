"""
src/evaluation.py
Métricas, análisis de error y gráficos de evaluación de modelos.
Fase 4+ del pipeline — Motor Predictivo Saber Pro.
Autor: Edwin Santiago Paz Bedoya — Código 1071010
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, label: str = "") -> dict:
    """Calcula RMSE, MAE y R² para un conjunto de predicciones."""
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae  = mean_absolute_error(y_true, y_pred)
    r2   = r2_score(y_true, y_pred)
    return {"modelo": label, "RMSE": round(rmse, 4), "MAE": round(mae, 4), "R2": round(r2, 4)}


def compute_metrics_by_group(
    y_true: pd.Series,
    y_pred: np.ndarray,
    group: pd.Series,
    label: str = "",
) -> pd.DataFrame:
    """RMSE y MAE desagregados por grupo (NBC, departamento, etc.)."""
    df = pd.DataFrame({"y_true": y_true.values, "y_pred": y_pred, "group": group.values})
    rows = []
    for grp, sub in df.groupby("group"):
        rows.append({
            "grupo": grp,
            "modelo": label,
            "RMSE": round(np.sqrt(mean_squared_error(sub["y_true"], sub["y_pred"])), 4),
            "MAE":  round(mean_absolute_error(sub["y_true"], sub["y_pred"]), 4),
            "n":    len(sub),
        })
    return pd.DataFrame(rows).sort_values("RMSE", ascending=False)


def plot_pred_vs_real(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    label: str,
    metrics: dict,
    out_path: str,
) -> None:
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(y_true, y_pred, alpha=0.25, s=8, color="#3572A5")
    lims = [min(y_true.min(), y_pred.min()) - 2, max(y_true.max(), y_pred.max()) + 2]
    ax.plot(lims, lims, "r--", linewidth=1.2, label="Predicción perfecta")
    ax.set_xlabel("PROMEDIO_GLOBAL real")
    ax.set_ylabel("PROMEDIO_GLOBAL predicho")
    ax.set_title(f"{label} — Predicho vs. Real (test)")
    ax.text(
        0.05, 0.95,
        f"RMSE={metrics['RMSE']:.3f}\nMAE={metrics['MAE']:.3f}\nR²={metrics['R2']:.3f}",
        transform=ax.transAxes, va="top", fontsize=10,
        bbox=dict(boxstyle="round,pad=0.4", fc="white", alpha=0.8),
    )
    ax.legend(fontsize=9)
    plt.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_residuals(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    label: str,
    out_path: str,
) -> None:
    residuals = y_true - y_pred
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle(f"{label} — Análisis de Residuos (test)", fontsize=12)

    axes[0].hist(residuals, bins=60, color="#3572A5", edgecolor="white", alpha=0.85)
    axes[0].axvline(0, color="red", linestyle="--")
    axes[0].set_title("Distribución de residuos")
    axes[0].set_xlabel("Error (real - predicho)")
    axes[0].set_ylabel("Frecuencia")

    axes[1].scatter(y_pred, residuals, alpha=0.2, s=8, color="#3572A5")
    axes[1].axhline(0, color="red", linestyle="--")
    axes[1].set_title("Residuos vs. predicho")
    axes[1].set_xlabel("Valor predicho")
    axes[1].set_ylabel("Residuo")

    plt.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_error_by_group(
    metrics_by_group: pd.DataFrame,
    label: str,
    group_name: str,
    out_path: str,
    top_n: int = 25,
) -> None:
    df = metrics_by_group.head(top_n).sort_values("RMSE")
    fig, ax = plt.subplots(figsize=(10, max(5, len(df) * 0.35)))
    ax.barh(df["grupo"].astype(str), df["RMSE"], color="#3572A5")
    ax.set_title(f"{label} — RMSE por {group_name} (top {top_n})")
    ax.set_xlabel("RMSE")
    plt.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_lasso_coefs(
    coefs: dict,
    out_path: str,
    top_n: int = 20,
) -> None:
    df = (
        pd.Series(coefs)
        .abs()
        .sort_values(ascending=False)
        .head(top_n)
        .sort_values()
    )
    fig, ax = plt.subplots(figsize=(9, max(5, len(df) * 0.4)))
    colors = ["#D63F3F" if coefs[n] < 0 else "#3572A5" for n in df.index]
    ax.barh(df.index, df.values, color=colors)
    ax.set_title(f"Lasso — Top {top_n} features por |coeficiente|")
    ax.set_xlabel("|Coeficiente|")
    plt.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
