# World Happiness 2015–2019: Drivers, Disparities, and Statistical Tests

[![Docker Support](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end data-science investigation of the **World Happiness Report (2015–2019)**. The project unifies five years of inconsistent CSV releases into a single tidy panel, enriches it with macroeconomic and geographic context from the **World Bank** and **REST Countries** APIs, and runs exploratory visualizations and formal hypothesis tests on the result.

---

## Research Overview

The World Happiness Report ranks countries by a composite "Cantril ladder" score and decomposes it into six explanatory factors (GDP per capita, social support, healthy life expectancy, freedom, generosity, perceived corruption). Between 2015 and 2019 the report's column names, units, and even country labels drifted year over year — so most of the work is upstream of the analysis.

**Research questions:**

### 1. How are happiness scores distributed globally and regionally?

Use the 2019 panel to characterize the global distribution of the ladder score and contrast regional means via boxplots and violin plots.

### 2. Which factors most strongly co-vary with happiness?

Compute pairwise correlations between the ladder score and its six explanatory factors, and visualize the strongest relationships with regression overlays.

### 3. How did country-level happiness evolve from 2015 to 2019?

Track per-country trajectories across the five releases after reconciling country-name changes (e.g. "Hong Kong" vs "Hong Kong S.A.R., China").

### 4. Are observed regional and economic gaps statistically significant?

Three pre-registered hypothesis tests:

- **H1** — Western Europe vs Sub-Saharan Africa: independent two-sample *t*-test on 2019 ladder scores.
- **H2** — GDP per capita predicts happiness: Pearson correlation with significance test.
- **H3** — World Bank income group is associated with happiness class: chi-squared test of independence.

---

## Data Sources

| Source                                                                        | Access            | Used for                                                              |
| ----------------------------------------------------------------------------- | ----------------- | --------------------------------------------------------------------- |
| [World Happiness Report 2015–2019](https://worldhappiness.report/)            | Local CSVs        | Primary panel: ladder score and six factor decompositions.            |
| [World Bank Open Data](https://data.worldbank.org/) (via `wbgapi`)            | REST API + cache  | GDP per capita PPP, unemployment rate, income group classification.   |
| [REST Countries](https://restcountries.com/)                                  | REST API + cache  | Region, subregion, common name, population (2019 snapshot).           |
| [`country_converter`](https://github.com/IndEcol/country_converter)           | Python package    | Normalize heterogeneous country labels to ISO-3166-1 alpha-3 codes.   |

Raw API responses are cached under `data/raw/` so the notebook is reproducible offline after the first run. The fully enriched dataset is materialized to `data/processed/happiness_enriched.csv`.

---

## Tech Stack

- **Language:** Python 3.11
- **Wrangling:** `pandas`, `numpy`, `country_converter`, `pycountry`
- **APIs:** `requests`, `wbgapi`
- **Statistics:** `scipy.stats` (*t*-test, Pearson, chi-squared)
- **Visualization:** `matplotlib`, `seaborn`
- **Environment:** Docker & JupyterLab

---

## Getting Started

### 1. Prerequisites

Ensure you have [Docker](https://docs.docker.com/get-docker/) installed on your host machine.

### 2. Build the Environment

Clone the repo and make the helper scripts executable:

```bash
git clone https://github.com/your-username/world-happiness-data-science.git
cd world-happiness-data-science

chmod +x .scripts/*.sh
```

Build the Docker image using the provided script:

```bash
./.scripts/build.sh
```

This builds the image tagged as `data-science`.

### 3. Run the Research Environment

Start the JupyterLab server with the local directory mounted:

```bash
./.scripts/run.sh
```

This will:

- Start a Docker container from the `data-science` image
- Mount your current directory to `/research` inside the container
- Expose JupyterLab on port **5555** (mapped from the container's 8888)

Navigate to `localhost:5555` in your browser and open `Main.ipynb`.

**Alternative — manual Docker command:**

```bash
docker run -p 5555:8888 -v $(pwd):/research data-science
```

### 4. First Run

The first execution of `Main.ipynb` will hit the World Bank and REST Countries APIs and write the responses to `data/raw/worldbank/` and `data/raw/restcountries/`. Subsequent runs read from cache and are fully offline.

---

## Project Structure

```text
.
├── .scripts/                            # Build and run automation scripts
│   ├── build.sh                         # Docker image build
│   └── run.sh                           # Container startup
├── data/
│   ├── raw/
│   │   ├── world-happines-2015-2019/    # Original yearly CSVs
│   │   ├── worldbank/                   # Cached World Bank API responses
│   │   └── restcountries/               # Cached REST Countries responses
│   └── processed/
│       └── happiness_enriched.csv       # Final tidy panel
├── notebooks/                           # Exploratory side notebooks
│   ├── explore_schema_drift.ipynb
│   ├── explore_worldbank_indicators.ipynb
│   └── explore_country_name_reconciliation.ipynb
├── src/                                 # Modular Python package
│   ├── data/                            # Pandas-only loaders & wrangling
│   │   ├── happiness.py                 # Unify 2015–2019 CSVs
│   │   ├── reconcile.py                 # Country name → ISO-3 normalization
│   │   ├── restcountries.py             # REST Countries client
│   │   ├── worldbank.py                 # World Bank indicator client
│   │   └── pipeline.py                  # End-to-end enrichment pipeline
│   └── charts/                          # Matplotlib/seaborn-only plots
│       ├── distributions.py             # Histograms, boxplots, violins
│       ├── relationships.py             # Scatter + regression, heatmaps
│       ├── geographic.py                # Country & region rankings
│       └── timeseries.py                # 2015–2019 trajectories
├── Main.ipynb                           # Primary research notebook
├── Dockerfile                           # Container definition
├── .gitignore                           # Git ignore rules
└── README.md                            # You are here
```

A strict separation is enforced between layers: modules under `src/data/` import only `pandas`/`numpy`/HTTP clients and never `matplotlib`; modules under `src/charts/` accept tidy DataFrames and return `matplotlib.figure.Figure` objects.

---

## Methodology

1. **Schema reconciliation.** Each yearly CSV uses different column names (`Happiness Score` vs `Score` vs `Ladder score`) and different factor labels. `src/data/happiness.py` maps each release to a canonical schema and emits a long-format DataFrame keyed on `(country, year)`.
2. **Country-name normalization.** `country_converter` resolves naming drift across years and across data sources (e.g. the happiness report uses "Taiwan Province of China"; the World Bank uses "Taiwan, China"). All joins use ISO-3 alpha codes as the canonical key.
3. **Enrichment.** The reconciled panel is left-joined against World Bank macro indicators and REST Countries geographic metadata. API responses are cached on disk to keep the notebook reproducible.
4. **Exploratory analysis.** Distributions, regional comparisons, correlation heatmaps, and 2015→2019 trajectories.
5. **Hypothesis testing.** Three pre-registered tests using `scipy.stats`:
   - Independent two-sample *t*-test (Welch) for the Western Europe vs Sub-Saharan Africa contrast.
   - Pearson correlation with two-sided *p*-value for GDP per capita vs ladder score.
   - Chi-squared test of independence for income group vs happiness tertile.
   For each test the notebook states the null hypothesis, alternative, significance level, test statistic, *p*-value, and a written decision.

---

## License

This project is licensed under the MIT License — see the `LICENSE` file for details.

**Author:** Alexander Avramov
