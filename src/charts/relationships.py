"""Bivariate and multivariate relationship plots."""

from __future__ import annotations

from collections.abc import Sequence

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure


def _filter(df: pd.DataFrame, year: int | None) -> pd.DataFrame:
    return df if year is None else df[df["year"] == year]


def scatter_with_regression(
    df: pd.DataFrame,
    x: str,
    y: str,
    year: int | None = None,
    log_x: bool = False,
) -> Figure:
    """Scatter plot of ``y`` against ``x`` with an OLS regression line.

    Args:
        df: Long-format enriched happiness DataFrame.
        x: Name of the column to put on the x-axis.
        y: Name of the column to put on the y-axis.
        year: Optional year filter.
        log_x: When ``True``, render the x-axis on a log scale (useful
            for heavily skewed monetary indicators like GDP).

    Returns:
        The matplotlib ``Figure``.
    """
    data = _filter(df, year).dropna(subset=[x, y])
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.regplot(
        data=data,
        x=x,
        y=y,
        ax=ax,
        scatter_kws={"alpha": 0.55, "s": 28, "color": "steelblue"},
        line_kws={"color": "crimson"},
    )
    if log_x:
        ax.set_xscale("log")
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    title = f"{y} vs {x}"
    ax.set_title(f"{title} ({year})" if year else title)
    fig.tight_layout()
    return fig


def correlation_heatmap(
    df: pd.DataFrame,
    columns: Sequence[str] | None = None,
    year: int | None = None,
) -> Figure:
    """Heat map of the Pearson correlation matrix.

    Args:
        df: Long-format enriched happiness DataFrame.
        columns: Subset of columns to include. ``None`` uses every
            numeric column except ``year``.
        year: Optional year filter.

    Returns:
        The matplotlib ``Figure``.
    """
    data = _filter(df, year)
    if columns is None:
        numeric = data.select_dtypes(include="number").columns.tolist()
        columns = [c for c in numeric if c != "year"]
    corr = data[list(columns)].corr(method="pearson")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="vlag",
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        cbar_kws={"shrink": 0.8},
        ax=ax,
    )
    title = "Pearson correlation matrix"
    ax.set_title(f"{title} ({year})" if year else f"{title} (all years pooled)")
    fig.tight_layout()
    return fig
