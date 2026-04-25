"""Country-name reconciliation utilities.

The happiness, World Bank, and REST Countries datasets disagree on
country spellings (e.g. "United States" vs "United States of America",
"Congo (Kinshasa)" vs "Democratic Republic of the Congo"). All joins in
this project happen on ISO 3166-1 alpha-3 codes produced here via
``country_converter``.

A small ``OVERRIDES`` dictionary is provided as an escape hatch for any
future name that ``country_converter`` does not resolve out of the box.
At time of writing all 170 unique names in the WHR 2015-2019 corpus
resolve without overrides.
"""

from __future__ import annotations

import warnings
from typing import Optional

import country_converter as coco
import pandas as pd

# Pre-instantiate the converter once - it loads a sizeable lookup table
# the first time it is constructed.
_CC = coco.CountryConverter()

# Manual escape hatch: name (as it appears in source data) -> ISO3.
# Empty by default; populate as new mismatches surface.
OVERRIDES: dict[str, str] = {}


def to_iso3(name: str) -> Optional[str]:
    """Convert a free-form country name to its ISO 3166-1 alpha-3 code.

    Args:
        name: Country name as it appears in source data.

    Returns:
        Three-letter ISO code, or ``None`` if no confident match exists.
    """
    if name is None:
        return None
    cleaned = str(name).strip()
    if not cleaned:
        return None
    if cleaned in OVERRIDES:
        return OVERRIDES[cleaned]
    with warnings.catch_warnings():
        # country_converter prints a warning for every unmatched name;
        # we surface those as None instead.
        warnings.simplefilter("ignore")
        result = _CC.convert(names=cleaned, to="ISO3", not_found=None)
    return result if isinstance(result, str) else None


def normalize_names(df: pd.DataFrame, col: str = "country") -> pd.DataFrame:
    """Add a ``country_iso3`` column derived from ``df[col]``.

    Args:
        df: Input frame containing a country-name column.
        col: Name of the column holding country names.

    Returns:
        Copy of ``df`` with an additional ``country_iso3`` column. Rows
        whose names cannot be resolved are kept with ``NaN`` so callers
        can decide whether to drop or impute them.
    """
    if col not in df.columns:
        raise KeyError(f"Column {col!r} not found in DataFrame.")

    out = df.copy()
    unique_names = out[col].dropna().astype(str).str.strip().unique().tolist()

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        resolved = _CC.convert(names=unique_names, to="ISO3", not_found=None)

    if isinstance(resolved, str):
        # ``convert`` returns a bare string when given a single name.
        resolved = [resolved]

    mapping = {
        name: (OVERRIDES.get(name) or (code if isinstance(code, str) else None))
        for name, code in zip(unique_names, resolved)
    }
    out["country_iso3"] = out[col].astype(str).str.strip().map(mapping)
    return out
