"""Distribution plots for the happiness score."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure


def _filter(df: pd.DataFrame, year: int | None) -> pd.DataFrame:
    return df if year is None else df[df["year"] == year]


def histogram_score(df: pd.DataFrame, year: int | None = None) -> Figure:
    """Plot the distribution of happiness scores.

    Args:
        df: Long-format enriched happiness DataFrame.
        year: Optional year filter. ``None`` plots all years pooled.

    Returns:
        The matplotlib ``Figure``.
    """
    data = _filter(df, year)
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(data["score"], bins=20, kde=True, ax=ax, color="steelblue")
    ax.set_xlabel("Happiness score")
    ax.set_ylabel("Number of countries")
    title = "Distribution of happiness scores"
    ax.set_title(f"{title} ({year})" if year else f"{title} (all years pooled)")
    fig.tight_layout()
    return fig


def boxplot_by_region(df: pd.DataFrame, year: int | None = None) -> Figure:
    """Box plot of happiness score grouped by world region.

    Args:
        df: Long-format enriched happiness DataFrame.
        year: Optional year filter.

    Returns:
        The matplotlib ``Figure``.
    """
    data = _filter(df, year).dropna(subset=["region"])
    order = (
        data.groupby("region")["score"].median().sort_values(ascending=False).index.tolist()
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.boxplot(data=data, x="region", y="score", order=order, ax=ax)
    ax.set_xlabel("Region")
    ax.set_ylabel("Happiness score")
    title = "Happiness score by region"
    ax.set_title(f"{title} ({year})" if year else f"{title} (all years pooled)")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    return fig


def violin_score_by_region(df: pd.DataFrame, year: int | None = None) -> Figure:
    """Violin plot of happiness score by world region.

    Args:
        df: Long-format enriched happiness DataFrame.
        year: Optional year filter.

    Returns:
        The matplotlib ``Figure``.
    """
    data = _filter(df, year).dropna(subset=["region"])
    order = (
        data.groupby("region")["score"].median().sort_values(ascending=False).index.tolist()
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.violinplot(data=data, x="region", y="score", order=order, inner="quartile", ax=ax)
    ax.set_xlabel("Region")
    ax.set_ylabel("Happiness score")
    title = "Happiness score density by region"
    ax.set_title(f"{title} ({year})" if year else f"{title} (all years pooled)")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    return fig
