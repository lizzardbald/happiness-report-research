"""End-to-end enrichment pipeline.

Glues the happiness, reconcile, World Bank, and REST Countries modules
together and writes a single tidy CSV at
``data/processed/happiness_enriched.csv`` for downstream consumption by
``Main.ipynb``.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from . import happiness, reconcile, restcountries, worldbank

PROCESSED_DIR = Path(__file__).resolve().parents[2] / "data" / "processed"
PROCESSED_FILE = PROCESSED_DIR / "happiness_enriched.csv"

# The temporal window covered by the WHR CSVs that ship with the project.
DEFAULT_YEARS = range(2015, 2020)


def build_dataset(use_cache: bool = True, write: bool = True) -> pd.DataFrame:
    """Assemble the enriched happiness dataset and persist it to disk.

    Steps:
        1. Load all five years of happiness data via
           :func:`src.data.happiness.load_all`.
        2. Attach ISO3 codes via :func:`src.data.reconcile.normalize_names`.
        3. Merge World Bank GDP/PPP, unemployment, and income-group fields.
        4. Merge REST Countries region, subregion, and population fields.
        5. Write the result to ``data/processed/happiness_enriched.csv``.

    Args:
        use_cache: When ``True`` (default), let the upstream fetchers
            reuse their on-disk caches instead of hitting the network.
        write: When ``True`` (default), persist the result to
            ``data/processed/happiness_enriched.csv``.

    Returns:
        The enriched long-format DataFrame, sorted by ``(year, country)``.
    """
    df = happiness.load_all()
    df = reconcile.normalize_names(df, col="country")

    wb_gdp = worldbank.fetch_gdp_per_capita_ppp(DEFAULT_YEARS, use_cache=use_cache)
    wb_unemp = worldbank.fetch_unemployment(DEFAULT_YEARS, use_cache=use_cache)
    wb_income = worldbank.fetch_income_groups(use_cache=use_cache)
    rc_meta = restcountries.fetch_country_metadata(use_cache=use_cache)

    df = (
        df.merge(wb_gdp, on=["country_iso3", "year"], how="left")
          .merge(wb_unemp, on=["country_iso3", "year"], how="left")
          .merge(wb_income, on="country_iso3", how="left")
          .merge(rc_meta, on="country_iso3", how="left")
    )

    df = df.sort_values(["year", "country"]).reset_index(drop=True)

    if write:
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        df.to_csv(PROCESSED_FILE, index=False)

    return df
