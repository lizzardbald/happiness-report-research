"""Time-evolution plots across the 2015-2019 window."""

from __future__ import annotations

from collections.abc import Sequence

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure


def lineplot_score_over_years(
    df: pd.DataFrame,
    by: str = "region",
) -> Figure:
    """Line plot of the mean happiness score over time, grouped by ``by``.

    Args:
        df: Long-format enriched happiness DataFrame.
        by: Grouping column, typically ``"region"`` or ``"income_group"``.

    Returns:
        The matplotlib ``Figure``.
    """
    data = df.dropna(subset=[by])
    agg = (
        data.groupby([by, "year"], as_index=False)["score"]
            .mean()
            .sort_values(["year", by])
    )
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.lineplot(data=agg, x="year", y="score", hue=by, marker="o", ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("Mean happiness score")
    ax.set_title(f"Mean happiness score by {by}, 2015-2019")
    ax.legend(loc="best", fontsize=9)
    ax.set_xticks(sorted(agg["year"].unique()))
    fig.tight_layout()
    return fig


def multi_country_trend(
    df: pd.DataFrame,
    countries: Sequence[str],
) -> Figure:
    """Line plot of happiness scores for a hand-picked set of countries.

    Args:
        df: Long-format enriched happiness DataFrame.
        countries: ISO3 codes (or country names, matched case-insensitively)
            to plot.

    Returns:
        The matplotlib ``Figure``.
    """
    wanted = {str(c).strip().upper() for c in countries}
    mask = (
        df["country_iso3"].astype(str).str.upper().isin(wanted)
        | df["country"].astype(str).str.upper().isin(wanted)
    )
    data = df[mask].sort_values(["country", "year"])
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.lineplot(data=data, x="year", y="score", hue="country", marker="o", ax=ax)
    ax.set_xlabel("Year")
    ax.set_ylabel("Happiness score")
    ax.set_title("Happiness score over time, selected countries")
    ax.set_xticks(sorted(data["year"].unique()))
    fig.tight_layout()
    return fig
