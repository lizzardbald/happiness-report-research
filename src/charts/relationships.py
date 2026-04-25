"""Bivariate and multivariate relationship plots."""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd
from matplotlib.figure import Figure


def scatter_with_regression(
    df: pd.DataFrame,
    x: str,
    y: str,
    year: int | None = None,
) -> Figure:
    """Scatter plot of ``y`` against ``x`` with an OLS regression line.

    Args:
        df: Long-format enriched happiness DataFrame.
        x: Name of the column to put on the x-axis.
        y: Name of the column to put on the y-axis.
        year: Optional year filter.

    Returns:
        The matplotlib ``Figure``.
    """
    pass


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
    pass
