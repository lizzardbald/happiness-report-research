"""Distribution plots for the happiness score."""

from __future__ import annotations

import pandas as pd
from matplotlib.figure import Figure


def histogram_score(df: pd.DataFrame, year: int | None = None) -> Figure:
    """Plot the distribution of happiness scores.

    Args:
        df: Long-format enriched happiness DataFrame.
        year: Optional year filter. ``None`` plots all years pooled.

    Returns:
        The matplotlib ``Figure``.
    """
    pass


def boxplot_by_region(df: pd.DataFrame, year: int | None = None) -> Figure:
    """Box plot of happiness score grouped by world region.

    Args:
        df: Long-format enriched happiness DataFrame.
        year: Optional year filter.

    Returns:
        The matplotlib ``Figure``.
    """
    pass


def violin_score_by_region(df: pd.DataFrame, year: int | None = None) -> Figure:
    """Violin plot of happiness score by world region.

    Args:
        df: Long-format enriched happiness DataFrame.
        year: Optional year filter.

    Returns:
        The matplotlib ``Figure``.
    """
    pass
