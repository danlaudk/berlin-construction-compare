# Pages in this folder

- `index.html`: **Die Bilanz**, a static long-form graphic on how Berlin housed
  408,000 new residents between 2011 and 2025, the size and composition of the
  housing gap, and what each policy lever can contribute. It is a single
  self-contained file (only Google Fonts load from outside) with no build step;
  edit it directly. Number sourcing: `docs/research/consolidated_findings.md`.
- `karte.html`: the Berlin vs Copenhagen animated district map, described below.

## Berlin vs Copenhagen: animated district map

`karte.html` is a self-contained static page (Plotly.js loaded from a CDN) showing
two choropleth maps side by side: Berlin's 12 Bezirke and Copenhagen's 10 bydele,
animated year by year from 2010 to 2025. Colour encodes dwellings completed per
1,000 residents that year, on one fixed scale shared across both cities and all
years (0 to the 98th percentile of all district-year values; higher values are
clipped). A slider and play/pause buttons drive both maps together. Hovering a
district shows its name, the year, dwellings completed, population and the
per-1,000 rate.

### Regenerating the map

```
uv run python src/geo_prep.py      # only needed if data/geo/*_raw*.geojson changes
uv run python src/map_animation.py # writes docs/karte.html
```

`map_animation.py` reads:

- `data/processed/berlin_completions_by_district.csv` (measure `dwellings_total`)
- `data/processed/berlin_population_by_district.csv`
- `data/processed/copenhagen_completions_by_district.csv` (measure starting
  `dwellings_by_commissioning_year`, from KK statbank table KKBOL1)
- `data/processed/copenhagen_population_by_district.csv`
- `data/geo/berlin_bezirke.geojson`, `data/geo/copenhagen_bydele.geojson`

### Metric caveat

Berlin's numbers are true completions (Fertigstellungen) from Statistik
Berlin-Brandenburg's F II 2 series. Copenhagen's KKBOL1 table is dwelling stock
grouped by commissioning year, a proxy for completions rather than an identical
measure. 2025 figures are provisional for both cities. See `outputs/REPORT.md`
and `data/processed/{berlin,copenhagen}_NOTES.md`.

### Map data: sources and licences

**Berlin Bezirke** (12 features): `data/geo/berlin_raw.geojson`, from a public
mirror of Berlin FIS-Broker administrative boundaries
(`https://raw.githubusercontent.com/funkeinteraktiv/Berlin-Geodaten/master/berlin_bezirke.geojson`),
licence "Datenlizenz Deutschland, Namensnennung".

**Copenhagen bydele** (10 features): `data/geo/cph_wfs.geojson`, from Københavns
Kommune's public WFS
(`https://wfs-kbhkort.kk.dk/k101/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=k101:bydel&outputFormat=json&srsName=EPSG:4326`),
free reuse with attribution. One name is remapped in
`src/geo_prep.py::CPH_NAME_MAP`: `Vesterbro-Kongens Enghave` becomes
`Vesterbro/Kongens Enghave`.

`src/geo_prep.py` simplifies both files (Shapely, tolerance 0.0003 degrees,
topology preserved) and writes `data/geo/berlin_bezirke.geojson` and
`data/geo/copenhagen_bydele.geojson`, each with a single `district` property
matching the CSV names.

## Publishing on GitHub Pages

In the repository's **Settings → Pages**, set the source to "Deploy from a
branch", choose the branch and the **`/docs`** folder. Pages then serves
`index.html` at `https://<user>.github.io/<repo>/` and the map at
`…/karte.html`. `.nojekyll` keeps Pages from running Jekyll over the folder.
