"""Load and unify the World Happiness Report CSVs for 2015-2019.

The five yearly CSVs ship with slightly different column names and column
counts. This module hides that drift behind two functions that always
return tidy frames with the canonical schema documented below.

Canonical long schema returned by :func:`load_all`:

    country, year, score, gdp, social_support, life_expectancy,
    freedom, generosity, corruption
"""

from __future__ import annotations

import pandas as pd


def load_year(year: int) -> pd.DataFrame:
    """Load a single year's happiness CSV and return the canonical schema.

    Args:
        year: Report year between 2015 and 2019 inclusive.

    Returns:
        DataFrame with columns
        ``[country, year, score, gdp, social_support, life_expectancy,
        freedom, generosity, corruption]``.
    """
    pass


def load_all() -> pd.DataFrame:
    """Concatenate all available years into a single long DataFrame.

    Returns:
        Long-format DataFrame, one row per (country, year), using the
        canonical schema described in the module docstring.
    """
    pass
