"""Geographic / categorical bar charts (regions, top-N countries)."""

from __future__ import annotations

import pandas as pd
from matplotlib.figure import Figure


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
    pass


def bar_mean_by_region(df: pd.DataFrame, year: int | None = None) -> Figure:
    """Bar chart of the mean happiness score per world region.

    Args:
        df: Long-format enriched happiness DataFrame.
        year: Optional year filter.

    Returns:
        The matplotlib ``Figure``.
    """
    pass
