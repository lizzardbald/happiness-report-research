"""Data layer: acquisition, normalization, and enrichment.

Modules in this package are strictly pandas-only and must not import any
plotting library. They take raw inputs (CSV files, HTTP responses, API
clients) and return tidy ``pandas.DataFrame`` objects.
"""
