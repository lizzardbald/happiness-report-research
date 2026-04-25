"""Chart layer: matplotlib/seaborn plotting helpers.

Every public function in this package takes a ``pandas.DataFrame`` (and
optionally styling kwargs) and returns a ``matplotlib.figure.Figure``.
Modules here must not perform any data acquisition or transformation
beyond what is necessary to render the requested chart.
"""
