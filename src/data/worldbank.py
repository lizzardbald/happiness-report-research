"""World Bank indicator enrichment via the ``wbgapi`` client.

Indicators of interest:

    NY.GDP.PCAP.PP.CD  - GDP per capita, PPP (current international $)
    SL.UEM.TOTL.ZS     - Unemployment, total (% of total labor force)

Income-group classification is fetched from ``wbgapi.economy.list``.
All downloads are cached as CSVs under ``data/raw/worldbank/``.
"""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd


def fetch_indicator(
    code: str,
    years: Iterable[int],
    use_cache: bool = True,
) -> pd.DataFrame:
    """Download a single World Bank indicator for the requested years.

    Args:
        code: World Bank indicator code, e.g. ``"NY.GDP.PCAP.PP.CD"``.
        years: Years to retrieve.
        use_cache: When ``True`` (default), reuse the per-indicator CSV
            cache on disk if present.

    Returns:
        Long-format DataFrame with columns
        ``[country_iso3, year, value]``.
    """
    pass


def fetch_gdp_per_capita_ppp(
    years: Iterable[int], use_cache: bool = True
) -> pd.DataFrame:
    """Convenience wrapper around :func:`fetch_indicator` for GDP/PPP."""
    pass


def fetch_unemployment(
    years: Iterable[int], use_cache: bool = True
) -> pd.DataFrame:
    """Convenience wrapper around :func:`fetch_indicator` for unemployment."""
    pass


def fetch_income_groups(use_cache: bool = True) -> pd.DataFrame:
    """Return World Bank income-group classification per economy.

    Args:
        use_cache: When ``True`` (default), reuse the cached CSV on disk
            if present.

    Returns:
        DataFrame with columns ``[country_iso3, income_group]`` where
        ``income_group`` is one of ``{"Low income", "Lower middle income",
        "Upper middle income", "High income"}``.
    """
    pass
