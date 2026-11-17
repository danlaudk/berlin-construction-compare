# Handoff: oversee the build of „Berlin hat Platz gemacht. Wo?" (two-part interactive)

You are the build lead. You do not write most of the code yourself; you choose the stack, set up the project, split the work into subagent tasks, review every deliverable against the design, and run the tests. Your job ends when the page is published, verified against the number tables below, and documented. Work in /home/dl/repos/berlin-construction-compare.

## 1. Read these first, in this order
1. docs/die-luecke-design.md — the design. §6 overrides §3–§4 where they conflict. §6.1 is Part A (two-round game + dials + bridge), §6.2 is the expropriation lever, §4 is the visual grammar.
2. docs/research/consolidated_findings.md — every number with its tag (V verified / S secondary / I inferred) and source.
3. docs/research/opus3_design_review.md — the must/should/could list already folded into §6; its "Fact-checker" table gives the citation to print for each number.
4. docs/research/stage1_datasets_report.md §(c) — the minimal file set for the Bezirk × year panel; stage3a_gap_report.md — the per-Bezirk tables and the census-anchored population method.
5. data/processed/berlin_NOTES.md and src/berlin.py — what the repo already downloads and parses (F II 2 completions and A I 5 register population, 2010–2025, Bezirk level). Note the 2025 completions figure 11,027 is a full year; the NOTES file wrongly says partial. Fix that line.

The other research files in docs/research/ are detail; consult them when a number needs its primary source.

## 2. What exists
- Python project managed by uv (pyproject.toml: pandas, polars, duckdb, plotly, openpyxl, xlrd, httpx, statsmodels). Run things with `uv run python …`. No JS toolchain yet.
- src/berlin.py: downloads and parses the Statistische Bibliothek Excel reports; src/geo_prep.py and src/map_animation.py produce docs/index.html, a self-contained Plotly.js choropleth animation (Berlin vs Copenhagen, 2010–2025) with the Bezirk GeoJSON in data/geo/. Reuse the Bezirk geometry and the download helpers; do not break that page.
- data/processed/: berlin_completions_wide.csv (year × Bezirk, dwellings_total), berlin_population_by_district.csv (register), Copenhagen files (not needed here).
- docs/research/sonnet1_figures.csv: Zensus 2022 vacancy by owner type (table 4000W-3006).

## 3. What to build
A single static, self-contained web page (German UI, mobile-first, no server, no keys), published as an Artifact and also committed to docs/ so it can be served from the repo. Two parts, one visual grammar (design §4): solid square = new dwelling, recoloured = owner change, hatched = existing dwelling returned, dotted outline = permitted not built, thin outline = need; 1 square = 1,000 dwellings everywhere.

**Part A — two-round allocation game (design §6.1).**
- Round 1 „gezählt" (Zensus 9.5.2011 → 15.5.2022): 304,614 arrivals; taps: Neu gebaut, Aus leeren Wohnungen, Ferienwohnungen/Gewerbe/Zweitwohnungen, Enger gewohnt, In Unterkünften, Umgebaut/aufgestockt, Übernommen, Gar nicht gekommen. Reader allocates until spent, commits, ledger reveals the census identity (149,403 + 25,577 − 9,562 = 165,418 households) at 1.79 persons, labelled „rechnerisch". Reveal values and labels exactly as in §6.1's table.
- Round 2 „geschätzt" (15.5.2022 → 31.12.2025): 103,598 arrivals; stock +50,592; Unterkünfte +27,635 persons; Übernommen ≈5,400 flats, 0 people; print the 114 % overlap caveat verbatim.
- Bezirk picker (12 + Berlin) for the per-Bezirk two-line chart and vacancy small multiples (stage3a tables). Population basis toggle (Zensus-basiert default; Melderegister labelled alternative).
- Two dials after both rounds: Reserve 0–5 % (Senat 3 %) and Haushaltsgröße 1.70–2.00 (Senat 1.77). At the Senate's settings the bridge text (§6.1) shows 137,000 = 41,000 + 77,000 + 19,000; the dial value becomes Part B's outline.

**Part B — lever waffle (design §3 hand-off paragraph, §4, §6.2).**
- 2,069 squares of stock, the dial number as outline, the Senate's 211,000 as a fainter second outline.
- Lever cards, each with Felder / Tempo / Wer zahlt / Quelle: Neu bauen (11.0/yr 2025, 19/yr 2019; LWU 4.7/yr), Überhang fertigstellen (48.4 dotted; 12.9 unter Dach, 12.3 Rohbau, 15.8 nicht begonnen), Leerstand aktivieren (5.4 market-active; 11.8 ceiling), Ferienwohnungen (8.4 listings, 4.9 active; 8.3 already returned since 2014; ~0.5/yr), Zweckentfremdung gesamt (31.7 banked), Aufstocken/umnutzen (20–36 supermarket sites; ~30 offices, S), Sozialbindungen (−46 by 2034, recolour reverse), Unterkünfte (54k people as demand marker), and the Vergesellschaften panel.
- Vergesellschaften panel exactly per §6.2: five fields (Umfang 222 recolour; Vergabe as a net yearly flow 3,300–5,000 on its own axis with 6,999 as a quote and lock-in as text; Miete −16 % / 936 €; Kosten 8–36 bn € with the DIW annual budget figure −0.3 to +1.1 bn, no flats conversion; Bauen? text toggle with the three quotes) plus the vacancy card. Do not recolour Abwendungsvereinbarungen. Label the 42–46 % as „alle privaten Wohnungsunternehmen".
- Every number carries reference date and spatial unit in its tooltip and the citation from the fact-checker table.

## 4. Data pipeline before any UI
Extend src/ (new module, e.g. src/panel.py) to produce one tidy file data/processed/berlin_panel.csv (Bezirk × year 2011–2025) and one data/processed/levers.json, both consumed by the page. Required inputs and where they come from (stage1 §(c), stage3a §3–4):
- Completions: existing CSV.
- Census-anchored population: Zensus 2011 Gemeindeblätter per Bezirk (BEV PDFs), A I 3 2025 XLSX for 2022–2025 per Bezirk; 2012–2021 per Bezirk estimated by scaling the register with the Berlin-wide A I 3 ÷ register ratio and blending the Bezirk residual between the two census anchors; flag `estimated=True`.
- Stock: F I 1 2025 XLSX (2021–2025) plus older PDFs; carry a `basis` column for the two rebasings.
- Zensus 2022 kleinräumig XLSX (Bezirksregionen → Bezirk) for households, dwellings, vacancy, duration; but use Gemeinde-level official totals for Berlin.
- Mikrozensus Bezirk household size 2024 (A I 10 Tab. 7.4) and the Berlin series.
- Bauüberhang, permits, Zweckentfremdung Bezirk tables, Inside Airbnb Bezirk counts, Unterkünfte per Bezirk, Zensus vacancy by owner type: numbers are already extracted in docs/research; load them from a hand-maintained YAML/JSON with source and tag fields rather than re-scraping, unless a download is one call away.
Every number in levers.json must carry `value, unit, ref_date, spatial_unit, source, tag`. The page must render tags (S and I visibly marked) so nothing secondary is printed as fact.

## 5. Library choice (decide in your first hour, document in docs/BUILD.md)
Constraints: static single file or a small folder; works on a phone with a 16 px gutter; no build server at runtime; CDN scripts only from cdnjs.cloudflare.com or cdn.jsdelivr.net/npm; dark mode via CSS tokens. Candidates: D3 (full control of the waffle, ledger and taps; preferred), Plotly.js (already used in docs/index.html, fast for the line/small-multiple charts, weak for custom waffle/tap interactions), Observable Plot (quick charts, limited interaction), Svelte or vanilla + D3 with a Vite build emitted to docs/. Choose one and state why; a mixed approach (D3 for Part A ledger, taps and the Part B waffle; Plotly or Plot for the per-Bezirk charts) is acceptable if the page still ships as one HTML. Load the `dataviz` and `artifact-design` skills before any chart code; follow the colour-blind-safe palette rules and the one-legend grammar.

## 6. How to run the work
- Spawn subagents for: (a) the data pipeline (one agent, Python, tests included), (b) Part A UI, (c) Part B UI, (d) a verification agent that recomputes every printed number from data/processed and docs/research and diffs against the page. Run (a) first; (b) and (c) in parallel after (a) lands; (d) last. Give each agent the exact sections of the design to implement and the number tables it must match.
- Review each deliverable yourself before the next stage: open the page in the Playwright browser, tap through both rounds, move both dials, pull every lever, resize to 375 px, toggle dark mode, screenshot each state into the scratchpad.
- Tests: Python unit tests for the pipeline (identity 149,403 + 25,577 − 9,562 = 165,418; Berlin totals match consolidated_findings.md; per-Bezirk sums equal Berlin; estimated years flagged), and a browser test script that asserts the reveal numbers, the 137,000 bridge at the Senate dials, that the Vergabe field never sums with the waffle squares, and that no S/I-tagged number appears without its marker.
- Commit in small steps on a branch; do not touch docs/index.html's behaviour. Run `uv run python -m pytest` before each commit.

## 7. Gates before publishing
1. All V-tagged numbers on screen match consolidated_findings.md to the unit.
2. The three Part 1 caveats (design §4) and the Round 1/Round 2 labels are visible without scrolling past the chart.
3. The Vergesellschaften panel shows both sides' quotes and no compensation-to-flats squares.
4. Secondary items still unverified (Pestel 58,000; bulwiengesa 30,000; campaign "10–20 % vacancy" line; Vonovia halt) are either marked S on screen or omitted.
5. Phone width works; dark mode works; page ≤ 16 MB; no external data calls at runtime.
Then publish as an Artifact, commit the page to docs/, update docs/README.md, and write docs/BUILD.md (stack, how to regenerate data and page, test commands, known gaps).

## 8. Known open data items (do not block the build; mark on screen)
Zensus 2011 persons in private households per Bezirk (tightens „Enger gewohnt ± 20,000"); in-scope completions share of the affected companies; all-in public cost per flat incl. land; Umwandlungen per year and LWU Wohnungstausch counts; BBU by Unternehmensart; Brandenburg net migration per Bezirk (A III 1) for „Gar nicht gekommen"; the whole-design adversarial review in docs/research/stage4_adversarial_review_brief.md has not been run.
