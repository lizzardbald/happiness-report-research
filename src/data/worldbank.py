"""World Bank indicator enrichment via the ``wbgapi`` client.

Indicators of interest:

    NY.GDP.PCAP.PP.CD  - GDP per capita, PPP (current international $)
    SL.UEM.TOTL.ZS     - Unemployment, total (% of total labor force)

Income-group classification is fetched from ``wbgapi.economy.list``.
All downloads are cached as CSVs under ``data/raw/worldbank/``.
"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

import pandas as pd
import wbgapi as wb

CACHE_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "worldbank"

# World Bank reports income level as a 3-letter code; map to the
# human-readable categories used in the analysis.
_INCOME_CODE_TO_NAME: dict[str, str] = {
    "HIC": "High income",
    "UMC": "Upper middle income",
    "LMC": "Lower middle income",
    "LIC": "Low income",
}


def _cache_path(filename: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / filename


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
    years = sorted(set(int(y) for y in years))
    span = f"{years[0]}-{years[-1]}"
    cache = _cache_path(f"{code}_{span}.csv")

    if use_cache and cache.exists():
        return pd.read_csv(cache)

    wide = wb.data.DataFrame(code, time=years)
    # ``wide`` has economy IDs as the index and ``YRxxxx`` columns.
    wide = wide.reset_index().rename(columns={"economy": "country_iso3"})
    long = wide.melt(
        id_vars="country_iso3",
        var_name="year",
        value_name="value",
    )
    long["year"] = long["year"].str.removeprefix("YR").astype(int)
    long = long.dropna(subset=["country_iso3"]).reset_index(drop=True)
    long.to_csv(cache, index=False)
    return long


def fetch_gdp_per_capita_ppp(
    years: Iterable[int], use_cache: bool = True
) -> pd.DataFrame:
    """GDP per capita, PPP (current international $)."""
    df = fetch_indicator("NY.GDP.PCAP.PP.CD", years, use_cache=use_cache)
    return df.rename(columns={"value": "gdp_ppp"})


def fetch_unemployment(
    years: Iterable[int], use_cache: bool = True
) -> pd.DataFrame:
    """Unemployment, total (% of total labor force, ILO modelled estimate)."""
    df = fetch_indicator("SL.UEM.TOTL.ZS", years, use_cache=use_cache)
    return df.rename(columns={"value": "unemployment"})


def fetch_income_groups(use_cache: bool = True) -> pd.DataFrame:
    """Return World Bank income-group classification per economy.

    Args:
        use_cache: When ``True`` (default), reuse the cached CSV on disk
            if present.

    Returns:
        DataFrame with columns ``[country_iso3, income_group]`` where
        ``income_group`` is one of ``{"Low income", "Lower middle income",
        "Upper middle income", "High income"}``. Regional aggregates are
        filtered out.
    """
    cache = _cache_path("income_groups.csv")
    if use_cache and cache.exists():
        return pd.read_csv(cache)

    rows = []
    for econ in wb.economy.list():
        if econ.get("aggregate"):
            continue
        code = econ.get("incomeLevel")
        rows.append(
            {
                "country_iso3": econ["id"],
                "income_group": _INCOME_CODE_TO_NAME.get(code),
            }
        )
    df = pd.DataFrame(rows).dropna(subset=["country_iso3"])
    df = df.dropna(subset=["income_group"]).reset_index(drop=True)
    df.to_csv(cache, index=False)
    return df
