# Pages in this folder

- `die-luecke.html` — „Berlin hat Platz gemacht. Wo?", a two-part interactive on
  Berlin's housing gap and the levers proposed to close it. See `docs/BUILD.md` for the
  stack (vanilla JS + D3, no bundler), how to regenerate
  (`uv run python src/build_page.py`) and how to run the tests
  (`uv run python -m pytest -q` for the pipeline/build/number-audit tests,
  `uv run python tests/browser_test.py` for the Playwright end-to-end check). Data
  pipeline: `uv run python src/panel.py && uv run python src/levers.py` writes
  `data/processed/berlin_panel.csv` and `data/processed/levers.json`, which
  `src/build_page.py` inlines into the page along with `src/page/*`. Design doc:
  `docs/die-luecke-design.md`; number sourcing: `docs/research/consolidated_findings.md`
  and `docs/research/verification_report.md`.
- `index.html` — the Berlin vs Copenhagen animated district map, described below.

## Berlin vs Copenhagen: animated district map

`index.html` in this folder is a self-contained static page (Plotly.js loaded
from a CDN; no server, no API keys, no build step) showing two choropleth
maps side by side -- Berlin's 12 Bezirke and Copenhagen's 10 bydele -- animated
year by year from 2010 to 2025. Colour encodes dwellings completed per 1,000
residents that year, on one fixed scale shared across both cities and all
years (0 to the 98th percentile of all district-year values; higher values
are clipped to the top of the scale). A slider and play/pause buttons drive
both maps together. Hovering a district shows its name, the year, the raw
number of dwellings completed, the population, and the per-1,000 rate. A
permanent annotation above each map gives that city's total for the selected
year.

## Regenerating the page

```
uv run python src/geo_prep.py      # only needed if data/geo/*_raw*.geojson changes
uv run python src/map_animation.py # writes docs/index.html
```

`map_animation.py` reads:

- `data/processed/berlin_completions_by_district.csv` (measure `dwellings_total`)
- `data/processed/berlin_population_by_district.csv`
- `data/processed/copenhagen_completions_by_district.csv` (measure starting
  `dwellings_by_commissioning_year`, from KK statbank table KKBOL1)
- `data/processed/copenhagen_population_by_district.csv`
- `data/geo/berlin_bezirke.geojson`, `data/geo/copenhagen_bydele.geojson`
  (produced by `src/geo_prep.py`, see below)

## Metric caveat

Berlin's numbers are true completions (Fertigstellungen) from Statistik
Berlin-Brandenburg's F2 report series. Copenhagen's KKBOL1 table is dwelling
*stock* grouped by commissioning year, as recorded at the most recent
reference date -- a proxy for completions, not an identical measure (it can
differ from true completions where dwellings built in a given year have since
been demolished or merged/split before the reference date). 2025 figures are
provisional for both cities. See `outputs/REPORT.md` and
`data/processed/{berlin,copenhagen}_NOTES.md` for full detail.

## Map data: sources and licences

Both GeoJSON files were downloaded once and committed to `data/geo/`; they are
small, simplified boundary files, not full-resolution cadastral data.

**Berlin Bezirke** (12 features): `data/geo/berlin_raw.geojson`, downloaded
from a public mirror of Berlin's open administrative-boundary data:

```
https://raw.githubusercontent.com/funkeinteraktiv/Berlin-Geodaten/master/berlin_bezirke.geojson
```

Original source: Berlin FIS-Broker / Land Berlin open data (Bezirksgrenzen),
licence CC-BY or "Datenlizenz Deutschland -- Namensnennung" as published by
the Berlin FIS-Broker WFS service. Feature property `name` already matches
the district names used in the CSV data, so no renaming was needed.

**Copenhagen bydele** (10 features): `data/geo/cph_wfs.geojson`, fetched from
Københavns Kommune's public WFS endpoint:

```
https://wfs-kbhkort.kk.dk/k101/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=k101:bydel&outputFormat=json&srsName=EPSG:4326
```

Licence: Københavns Kommune open data (kk.dk / opendata.dk), free reuse with
attribution. Feature property `navn` needed one name-mapping fix to match the
CSV spelling (`src/geo_prep.py::CPH_NAME_MAP`):

| Raw WFS `navn`               | CSV / processed `district`      |
|-------------------------------|----------------------------------|
| `Vesterbro-Kongens Enghave`   | `Vesterbro/Kongens Enghave`      |
| (all other 9 names)           | unchanged                        |

`src/geo_prep.py` reads these two raw files, simplifies each polygon with
Shapely's Douglas-Peucker simplify (tolerance 0.0003 degrees, topology
preserved), and writes the slimmed-down files actually used by the map:

- `data/geo/berlin_bezirke.geojson` (~40 KB, 12 features)
- `data/geo/copenhagen_bydele.geojson` (~23 KB, 10 features)

each carrying a single `district` property that matches the CSV district
names exactly (used as `featureidkey="properties.district"` in the Plotly
trace).

## Publishing on GitHub Pages

1. Push this repository to GitHub.
2. In the repo, go to **Settings -> Pages**.
3. Under **Build and deployment**, set **Source** to "Deploy from a branch".
4. Choose the branch (e.g. `main`) and folder **`/docs`**, then **Save**.
5. GitHub Pages will serve `docs/index.html` at
   `https://<user>.github.io/<repo>/` within a few minutes.

No further configuration is needed -- the page has no server-side code and
loads Plotly.js from `cdn.plot.ly`, so it works as a plain static file.
