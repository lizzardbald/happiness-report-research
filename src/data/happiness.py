"""Load and unify the World Happiness Report CSVs for 2015-2019.

The five yearly CSVs ship with slightly different column names and column
counts. This module hides that drift behind two functions that always
return tidy frames with the canonical schema documented below.

Canonical long schema returned by :func:`load_all`:

    country, year, score, gdp, social_support, life_expectancy,
    freedom, generosity, corruption
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

RAW_DIR = Path(__file__).resolve().parents[2] / "data" / "raw" / "world-happines-2015-2019"

CANONICAL_COLUMNS = [
    "country",
    "year",
    "score",
    "gdp",
    "social_support",
    "life_expectancy",
    "freedom",
    "generosity",
    "corruption",
]

# Per-year mapping from raw column names to the canonical schema.
# 2015-2017 use "Family" as the social-support proxy; the WHR team relabelled
# the same metric to "Social support" starting with the 2018 edition.
_YEAR_COLUMN_MAP: dict[int, dict[str, str]] = {
    2015: {
        "Country": "country",
        "Happiness Score": "score",
        "Economy (GDP per Capita)": "gdp",
        "Family": "social_support",
        "Health (Life Expectancy)": "life_expectancy",
        "Freedom": "freedom",
        "Generosity": "generosity",
        "Trust (Government Corruption)": "corruption",
    },
    2016: {
        "Country": "country",
        "Happiness Score": "score",
        "Economy (GDP per Capita)": "gdp",
        "Family": "social_support",
        "Health (Life Expectancy)": "life_expectancy",
        "Freedom": "freedom",
        "Generosity": "generosity",
        "Trust (Government Corruption)": "corruption",
    },
    2017: {
        "Country": "country",
        "Happiness.Score": "score",
        "Economy..GDP.per.Capita.": "gdp",
        "Family": "social_support",
        "Health..Life.Expectancy.": "life_expectancy",
        "Freedom": "freedom",
        "Generosity": "generosity",
        "Trust..Government.Corruption.": "corruption",
    },
    2018: {
        "Country or region": "country",
        "Score": "score",
        "GDP per capita": "gdp",
        "Social support": "social_support",
        "Healthy life expectancy": "life_expectancy",
        "Freedom to make life choices": "freedom",
        "Generosity": "generosity",
        "Perceptions of corruption": "corruption",
    },
    2019: {
        "Country or region": "country",
        "Score": "score",
        "GDP per capita": "gdp",
        "Social support": "social_support",
        "Healthy life expectancy": "life_expectancy",
        "Freedom to make life choices": "freedom",
        "Generosity": "generosity",
        "Perceptions of corruption": "corruption",
    },
}


def load_year(year: int) -> pd.DataFrame:
    """Load a single year's happiness CSV and return the canonical schema.

    Args:
        year: Report year between 2015 and 2019 inclusive.

    Returns:
        DataFrame with columns
        ``[country, year, score, gdp, social_support, life_expectancy,
        freedom, generosity, corruption]``.

    Raises:
        ValueError: If ``year`` is outside the supported range.
        FileNotFoundError: If the expected raw CSV is missing.
    """
    if year not in _YEAR_COLUMN_MAP:
        raise ValueError(f"Unsupported year {year!r}; expected 2015-2019.")

    csv_path = RAW_DIR / f"{year}.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Missing raw CSV: {csv_path}")

    raw = pd.read_csv(csv_path)
    rename_map = _YEAR_COLUMN_MAP[year]

    # The corruption column is the only one that may be NaN in the source
    # (e.g. United Arab Emirates 2018 has it blank). Coerce numerics so any
    # stray strings become NaN rather than raising downstream.
    df = raw[list(rename_map)].rename(columns=rename_map).copy()
    df["year"] = year
    for col in ("score", "gdp", "social_support", "life_expectancy",
                "freedom", "generosity", "corruption"):
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["country"] = df["country"].astype(str).str.strip()

    return df[CANONICAL_COLUMNS]


def load_all() -> pd.DataFrame:
    """Concatenate all available years into a single long DataFrame.

    Returns:
        Long-format DataFrame, one row per (country, year), using the
        canonical schema described in the module docstring. Sorted by
        ``(year, country)`` for stable iteration.
    """
    frames = [load_year(y) for y in sorted(_YEAR_COLUMN_MAP)]
    out = pd.concat(frames, ignore_index=True)
    return out.sort_values(["year", "country"]).reset_index(drop=True)
