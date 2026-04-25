"""End-to-end enrichment pipeline.

Glues the happiness, reconcile, World Bank, and REST Countries modules
together and writes a single tidy CSV at
``data/processed/happiness_enriched.csv`` for downstream consumption by
``Main.ipynb``.
"""

from __future__ import annotations

import pandas as pd


def build_dataset(use_cache: bool = True) -> pd.DataFrame:
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

    Returns:
        The enriched long-format DataFrame.
    """
    pass
