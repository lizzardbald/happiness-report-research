"""Country-name reconciliation utilities.

The happiness, World Bank, and REST Countries datasets disagree on
country spellings (e.g. "United States" vs "United States of America",
"Congo (Kinshasa)" vs "Democratic Republic of the Congo"). All joins in
this project happen on ISO 3166-1 alpha-3 codes produced here via
``country_converter``.
"""

from __future__ import annotations

import pandas as pd


def to_iso3(name: str) -> str | None:
    """Convert a free-form country name to its ISO 3166-1 alpha-3 code.

    Args:
        name: Country name as it appears in source data.

    Returns:
        Three-letter ISO code, or ``None`` if no confident match exists.
    """
    pass


def normalize_names(df: pd.DataFrame, col: str = "country") -> pd.DataFrame:
    """Add an ``country_iso3`` column derived from ``df[col]``.

    Args:
        df: Input frame containing a country-name column.
        col: Name of the column holding country names.

    Returns:
        Copy of ``df`` with an additional ``country_iso3`` column. Rows
        whose names cannot be resolved are kept with ``NaN`` so callers
        can decide whether to drop or impute them.
    """
    pass
