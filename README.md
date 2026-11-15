# berlin-construction-compare

Compare construction statistics between Berlin and Denmark using open data APIs.

## Setup
    uv sync
    uv run jupyter lab          # notebooks live in notebooks/

## Data sources
- Statistics Denmark StatBank API (`https://api.statbank.dk/v1`) — helpers in `src/sources.py` (`dst_*`).
- Berlin Open Data CKAN (`https://datenregister.berlin.de`) — helpers in `src/sources.py` (`berlin_*`).
Raw downloads are cached in `data/raw/` (git-ignored).

## Exploration toolkit
pandas, polars, duckdb (query files with SQL), skimpy (`skim(df)` summary),
fg-data-profiling (`ProfileReport(df)` HTML report), missingno (missingness plots),
pyjanitor (`df.clean_names()`), great_tables, matplotlib / seaborn / plotly.
