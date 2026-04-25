"""REST Countries (restcountries.com) metadata enrichment.

Provides region/subregion/population context that is missing from the
World Happiness Report. Responses are cached as JSON under
``data/raw/restcountries/`` so re-runs work offline.
"""

from __future__ import annotations

import pandas as pd


def fetch_country_metadata(use_cache: bool = True) -> pd.DataFrame:
    """Return one row per country with region, subregion, and population.

    Args:
        use_cache: When ``True`` (default), reuse a cached JSON snapshot
            on disk if available; otherwise hit the live API and refresh
            the cache.

    Returns:
        DataFrame with columns
        ``[country_iso3, name_common, region, subregion, population]``.
    """
    pass
