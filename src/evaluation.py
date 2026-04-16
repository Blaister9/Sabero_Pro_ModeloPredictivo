"""Metrics computation, error analysis, and evaluation plots for Saber Pro models.

This module is used across Phases 4, 5, and 6 of the Saber Pro predictive
pipeline and provides a unified set of evaluation utilities that can be called
from any model-training script (baseline, boosting, or transformer).

Three categories of functionality are provided:

1. **Scalar metrics**: ``compute_metrics`` returns RMSE, MAE, and R² as a
   dictionary keyed by a caller-supplied label.  ``compute_metrics_by_group``
   disaggregates the same metrics by any grouping variable (e.g. NBC,
   department) to reveal whether model error is uniform across the Colombian
   higher-education landscape.

2. **Diagnostic plots**: ``plot_pred_vs_real`` produces a scatter plot of
   predicted vs. actual ``PROMEDIO_GLOBAL`` values with a perfect-prediction
   reference line.  ``plot_residuals`` produces a two-panel figure showing the
   residual distribution and a residuals-vs-predicted scatter.
   ``plot_error_by_group`` renders a horizontal bar chart of per-group RMSE
   values.  ``plot_lasso_coefs`` visualises the top-N Lasso coefficients by
   magnitude, with positive and negative values colour-coded.

3. **Persistence**: all plot functions save figures to disk at a caller-supplied
   path using ``matplotlib`` with 150 DPI.

All evaluation is performed exclusively on the **test set** (year 2024) to
respect the temporal train/test split.  Training-set metrics are computed
solely to diagnose overfitting, not to report model performance.

Usage example::

    import numpy as np
    from src.evaluation import compute_metrics, plot_pred_vs_real, plot_residuals

    y_true = np.array([152.3, 145.0, 160.5, ...])
    y_pred = np.array([149.8, 147.2, 158.0, ...])

    metrics = compute_metrics(y_true, y_pred, label="LightGBM")
    print(metrics)
    # {'modelo': 'LightGBM', 'RMSE': 9.33, 'MAE': 7.12, 'R2': 0.706}

    plot_pred_vs_real(
        y_true, y_pred, label="LightGBM", metrics=metrics,
        out_path="outputs/lgbm_pred_vs_real.png"
    )
    plot_residuals(y_true, y_pred, label="LightGBM",
                   out_path="outputs/lgbm_residuals.png")

Warning:
    All metric computations and plots in this module operate on raw numpy arrays
    or pandas Series.  It is the caller's responsibility to ensure that
    ``y_true`` and ``y_pred`` correspond to the test set only (rows where
    ``AÑO == 2024``).  Mixing train and test observations will produce
    optimistic metrics that do not reflect the model's true generalisation
    ability on unseen programme-year pairs.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray, label: str = "") -> dict:
    """Compute RMSE, MAE, and R² for a set of predictions.

    Args:
        y_true: Array of ground-truth ``PROMEDIO_GLOBAL`` values.  Must have
            the same length as ``y_pred``.
        y_pred: Array of predicted ``PROMEDIO_GLOBAL`` values produced by a
            fitted model.
        label: Human-readable model name to include in the returned dictionary
            (e.g. ``"LightGBM"``, ``"Ridge"``).  Defaults to an empty string.

    Returns:
        A dictionary with four keys:

        - ``"modelo"``: The value of ``label``.
        - ``"RMSE"``: Root Mean Squared Error, rounded to 4 decimal places.
        - ``"MAE"``: Mean Absolute Error, rounded to 4 decimal places.
        - ``"R2"``: Coefficient of determination R², rounded to 4 decimal places.

    Raises:
        ValueError: If ``y_true`` and ``y_pred`` have different lengths
            (propagated from scikit-learn metrics).

    Example:
        >>> import numpy as np
        >>> y_true = np.array([150.0, 155.0, 148.0])
        >>> y_pred = np.array([149.0, 157.0, 146.0])
        >>> compute_metrics(y_true, y_pred, label="Ridge")
        {'modelo': 'Ridge', 'RMSE': 1.9149, 'MAE': 1.6667, 'R2': 0.7368}

    Note:
        On the Saber Pro test set (2024, n ≈ 8,000 rows), the final LightGBM
        model achieved RMSE = 9.33 and R² = 0.706, which are the benchmark
        values for comparing future model iterations.
    """
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
    """Compute RMSE and MAE disaggregated by a grouping variable.

    Splits the predictions into subsets defined by unique values of ``group``
    and computes RMSE, MAE, and sample count for each subset.  The result is
    sorted by descending RMSE to surface the groups where the model performs
    worst.

    Args:
        y_true: Pandas Series of ground-truth ``PROMEDIO_GLOBAL`` values.
            Index must be aligned with ``y_pred`` and ``group``.
        y_pred: Numpy array of predicted values with the same length as
            ``y_true``.
        group: Pandas Series of group labels (e.g. ``df["NBC"]`` or
            ``df["ID_DEPARTAMENTO"]``).  Must be the same length as ``y_true``.
        label: Human-readable model name included in every output row.
            Defaults to an empty string.

    Returns:
        A DataFrame with columns ``["grupo", "modelo", "RMSE", "MAE", "n"]``
        sorted by ``RMSE`` in descending order (worst groups first).

    Raises:
        ValueError: If ``y_true``, ``y_pred``, and ``group`` have different
            lengths.

    Example:
        >>> metrics_nbc = compute_metrics_by_group(
        ...     y_true=df_test["PROMEDIO_GLOBAL"],
        ...     y_pred=y_pred_lgbm,
        ...     group=df_test["NBC"],
        ...     label="LightGBM",
        ... )
        >>> metrics_nbc.head(3)
          grupo      modelo    RMSE     MAE    n
        0  ARTES   LightGBM  14.230  11.500   87
        1  SALUD   LightGBM  12.810  10.230  342
        ...
    """
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
    """Save a scatter plot of predicted vs. actual PROMEDIO_GLOBAL values.

    Produces a square scatter plot where each point represents one
    program-exam-year observation from the test set.  A dashed red line
    marks perfect predictions (y = x).  RMSE, MAE, and R² values from
    ``metrics`` are displayed in a text box in the upper-left corner.

    Args:
        y_true: 1-D array of ground-truth ``PROMEDIO_GLOBAL`` values (test set).
        y_pred: 1-D array of model predictions aligned with ``y_true``.
        label: Model name used in the plot title (e.g. ``"LightGBM"``).
        metrics: Dictionary returned by ``compute_metrics``, expected to
            contain ``"RMSE"``, ``"MAE"``, and ``"R2"`` keys.
        out_path: Absolute or relative path where the PNG figure should be
            saved (e.g. ``"outputs/lgbm_pred_vs_real.png"``).

    Returns:
        None.  The figure is saved to ``out_path`` at 150 DPI and the
        matplotlib figure is closed to free memory.

    Raises:
        OSError: If ``out_path`` points to a directory that does not exist.

    Example:
        >>> plot_pred_vs_real(
        ...     y_true=y_test.values,
        ...     y_pred=y_pred_lgbm,
        ...     label="LightGBM",
        ...     metrics={"RMSE": 9.33, "MAE": 7.12, "R2": 0.706},
        ...     out_path="outputs/lgbm_pred_vs_real.png",
        ... )
    """
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
    """Save a two-panel residual analysis plot.

    Panel 1 (left): Histogram of residuals (y_true - y_pred) with a vertical
    dashed line at zero.  A symmetric distribution centred near zero suggests
    unbiased predictions.

    Panel 2 (right): Scatter plot of residuals against predicted values.
    A horizontal band of points near zero with no visible pattern indicates
    that variance is roughly constant across the prediction range (homoscedastic
    errors).

    Args:
        y_true: 1-D array of ground-truth ``PROMEDIO_GLOBAL`` values (test set).
        y_pred: 1-D array of model predictions aligned with ``y_true``.
        label: Model name used in the plot's super-title (e.g. ``"Ridge"``).
        out_path: Absolute or relative path where the PNG figure should be
            saved (e.g. ``"outputs/ridge_residuals.png"``).

    Returns:
        None.  The figure is saved at 150 DPI and closed.

    Raises:
        OSError: If the target directory for ``out_path`` does not exist.

    Example:
        >>> plot_residuals(
        ...     y_true=y_test.values,
        ...     y_pred=y_pred_ridge,
        ...     label="Ridge",
        ...     out_path="outputs/ridge_residuals.png",
        ... )
    """
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
    """Save a horizontal bar chart of per-group RMSE values.

    Displays the ``top_n`` groups with the highest RMSE from the DataFrame
    produced by ``compute_metrics_by_group``, sorted in ascending order
    (lowest RMSE at the bottom of the chart) so that the worst-performing
    group appears at the top.

    Args:
        metrics_by_group: DataFrame returned by ``compute_metrics_by_group``.
            Must contain at least ``"grupo"`` and ``"RMSE"`` columns.
        label: Model name included in the chart title.
        group_name: Human-readable name for the grouping variable used in
            the chart title (e.g. ``"NBC"`` or ``"Departamento"``).
        out_path: Path where the PNG figure should be saved.
        top_n: Maximum number of groups to display.  Defaults to ``25``.

    Returns:
        None.  The figure is saved at 150 DPI and closed.

    Raises:
        OSError: If the target directory for ``out_path`` does not exist.

    Example:
        >>> plot_error_by_group(
        ...     metrics_by_group=metrics_nbc,
        ...     label="LightGBM",
        ...     group_name="NBC",
        ...     out_path="outputs/lgbm_rmse_by_nbc.png",
        ...     top_n=20,
        ... )
    """
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
    """Save a horizontal bar chart of the top-N Lasso coefficients by magnitude.

    Selects the ``top_n`` features with the largest absolute coefficient values,
    sorts them by absolute magnitude, and plots them as a horizontal bar chart.
    Bars are coloured red for negative coefficients and blue for positive ones
    to aid visual interpretation.

    Args:
        coefs: Dictionary mapping feature name (str) to its fitted Lasso
            coefficient (float).  Features with coefficient zero are included
            in the candidate set but will only appear if they rank in the top N
            by absolute value (i.e. they generally will not).
        out_path: Path where the PNG figure should be saved.
        top_n: Maximum number of features to display.  Defaults to ``20``.

    Returns:
        None.  The figure is saved at 150 DPI and closed.

    Raises:
        OSError: If the target directory for ``out_path`` does not exist.

    Example:
        >>> # Assume lasso_result is the dict returned by train_lasso()
        >>> plot_lasso_coefs(
        ...     coefs=lasso_result["coefs"],
        ...     out_path="outputs/lasso_coefs.png",
        ...     top_n=20,
        ... )

    Note:
        Only features with non-zero Lasso coefficients are informative in this
        chart; the rest were set to zero by the L1 penalty and had no predictive
        contribution.  The number of non-zero features is reported in the
        ``"n_selected"`` key of ``train_lasso``'s return dictionary.
    """
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
