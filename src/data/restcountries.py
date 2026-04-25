"""REST Countries (restcountries.com) metadata enrichment.

Provides region/subregion/population context that is missing from the
World Happiness Report. Responses are cached as JSON under
``data/raw/restcountries/`` so re-runs work offline.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import requests

# Project-relative cache directory.
CACHE_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "restcountries"
CACHE_FILE = CACHE_DIR / "all_v3.1.json"

# v3.1 requires an explicit ``fields`` parameter; the unfiltered ``all``
# endpoint started returning 400 in mid-2024.
API_URL = "https://restcountries.com/v3.1/all"
FIELDS = ["name", "cca3", "region", "subregion", "population"]
REQUEST_TIMEOUT = 30  # seconds


def _download() -> list[dict]:
    """Hit the live REST Countries API and return the parsed payload."""
    response = requests.get(
        API_URL,
        params={"fields": ",".join(FIELDS)},
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def _load_cached() -> list[dict] | None:
    if not CACHE_FILE.exists():
        return None
    with CACHE_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def _write_cache(payload: list[dict]) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with CACHE_FILE.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


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
    payload: list[dict] | None = None
    if use_cache:
        payload = _load_cached()
    if payload is None:
        payload = _download()
        _write_cache(payload)

    rows = []
    for entry in payload:
        rows.append(
            {
                "country_iso3": entry.get("cca3"),
                "name_common": (entry.get("name") or {}).get("common"),
                "region": entry.get("region"),
                "subregion": entry.get("subregion"),
                "population": entry.get("population"),
            }
        )

    df = pd.DataFrame(rows)
    df = df.dropna(subset=["country_iso3"]).drop_duplicates(subset=["country_iso3"])
    return df.sort_values("country_iso3").reset_index(drop=True)
