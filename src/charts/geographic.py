"""Geographic / categorical bar charts (regions, top-N countries)."""

from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure


def _filter(df: pd.DataFrame, year: int | None) -> pd.DataFrame:
    if year is None:
        year = int(df["year"].max())
    return df[df["year"] == year], year


def bar_top_n_countries(
    df: pd.DataFrame,
    n: int = 10,
    year: int | None = None,
    ascending: bool = False,
) -> Figure:
    """Horizontal bar chart of the top (or bottom) ``n`` countries by score.

    Args:
        df: Long-format enriched happiness DataFrame.
        n: Number of countries to show.
        year: Optional year filter; defaults to the latest year present.
        ascending: When ``True``, show the lowest-scoring countries instead.

    Returns:
        The matplotlib ``Figure``.
    """
    data, used_year = _filter(df, year)
    ranked = data.sort_values("score", ascending=ascending).head(n)
    # Plot from highest at the top.
    ranked = ranked.iloc[::-1] if not ascending else ranked

    fig, ax = plt.subplots(figsize=(8, 0.45 * n + 1.5))
    sns.barplot(
        data=ranked,
        x="score",
        y="country",
        ax=ax,
        color="steelblue",
    )
    ax.set_xlabel("Happiness score")
    ax.set_ylabel("")
    direction = "Bottom" if ascending else "Top"
    ax.set_title(f"{direction} {n} countries by happiness ({used_year})")
    fig.tight_layout()
    return fig


def bar_mean_by_region(df: pd.DataFrame, year: int | None = None) -> Figure:
    """Bar chart of the mean happiness score per world region.

    Args:
        df: Long-format enriched happiness DataFrame.
        year: Optional year filter; defaults to the latest year present.

    Returns:
        The matplotlib ``Figure``.
    """
    data, used_year = _filter(df, year)
    agg = (
        data.dropna(subset=["region"])
            .groupby("region", as_index=False)["score"]
            .mean()
            .sort_values("score", ascending=False)
    )
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=agg, x="region", y="score", ax=ax, color="steelblue")
    ax.set_xlabel("Region")
    ax.set_ylabel("Mean happiness score")
    ax.set_title(f"Mean happiness score by region ({used_year})")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    return fig
