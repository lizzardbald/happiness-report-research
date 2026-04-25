"""Time-evolution plots across the 2015-2019 window."""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd
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
    pass


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
    pass
