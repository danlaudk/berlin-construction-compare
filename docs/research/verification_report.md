# Verification report: „Berlin hat Platz gemacht. Wo?" (docs/die-luecke.html)

Run 2026-11-17. Scope: recompute every printed number from `data/processed/levers.json`
and the research docs, diff against the rendered `docs/die-luecke.html`, check every
S/I-tagged leaf is visibly marked, drive the page end-to-end with Playwright, and check
the five handoff gates (`docs/handoff-build-oversight.md` §7).

Tests added: `tests/test_numbers.py` (37 cases), `tests/browser_test.py` (Playwright,
19 checks). Both pass; `uv run python -m pytest -q` (15 existing + 37 new = 52 cases)
is green.

## 1. Number audit

| Item | Page value | Source value | Tag | Citation | Status |
|---|---|---|---|---|---|
| Identity 149.403+25.577−9.562=165.418 | 149.403+25.577−9.562=165.418 (formatted after fix, see §3) | consolidated_findings.md §2.2 | V | Zensus 2011/2022 | match |
| Round 1 arrivals 304.614 | 304614 | consolidated_findings.md §1, §2.2 | V | Zensus 2011→2022 | match |
| Round 2 arrivals 103.598 | 103598 | consolidated_findings.md §2.2 | V | A I 3 | match |
| Round 2 stock Δ 50.592 | 50592 | consolidated_findings.md §2.2 | V | F I 1 | match |
| Round 2 Unterkünfte Δ 27.635 | 27635 | design §6.1 | V | AfS Wohnungslosenstatistik | match |
| Round 2 Übernommen 5.400 Whg. | 5400 | design §6.1 | V | sonnet2_transfers_allocation.md | match |
| Round 2 overlap 114 % | 114 | design §6.1 (die Teile ergeben mehr als 100%) | I | arithmetic | match |
| HH size 1,79 | 1.79 | consolidated_findings.md §2.2 | I | Zensus household size | match |
| Bridge 41.000+77.000+19.000=137.000 | 41000+77000+19000=137000 | StEP Wohnen 2040 pp. 75–77 | V | consolidated_findings.md §1 | match |
| Senate update 211.000 | 211000 | consolidated_findings.md §1 | S | Fortschrittsbericht PM 1682261 | match |
| Stock squares 2.069 | 2069 (x1000) | consolidated_findings.md §1 (2,069,432) | V | F I 1 | match |
| Neu bauen 2025 11,0/Jahr; 2019 19,0/Jahr; LWU 4,7/Jahr | 11.0 / 19.0 / 4.7 | consolidated_findings.md §2 | V | F II 2; KoopV | match |
| Überhang 48,4 (12,9/12,3/15,8) | 48.4 / 12.9 / 12.3 / 15.8 | consolidated_findings.md §1 (48,394: 12,901/12,252/15,784) | V | F II 2 Tab. 17 | match (rounded ×1000 consistently) |
| Leerstand 5,4 / 11,8 | 5.4 / 11.8 | consolidated_findings.md §2 (~5,400; 11,764) | V | CBRE-empirica; Zensus 2022 | match |
| Ferienwohnungen 8,4 / 4,9 / 8,3 / 0,5 | 8.4 / 4.9 / 8.3 / 0.5 | consolidated_findings.md §2 | V | Inside Airbnb; Drs. 19/24230 | match |
| Zweckentfremdung gesamt 31,7 | 31.7 | consolidated_findings.md §2 (31,706) | V | Drs. 19/24230 | match |
| Aufstocken 20–36 / 30 | [20,36] / 30 | consolidated_findings.md §2 | S | Deutschlandstudie 2019; bulwiengesa | match |
| Sozialbindungen −46 | -46 | consolidated_findings.md §2 (46,408 expire) | V | IBB WMB 2024 | match |
| Unterkünfte 54 | 54 | consolidated_findings.md §1 (53,610) | V | AfS Wohnungslose | match (rounded) |
| Vergesellschaften Umfang 222, 0 neu | 222 / 0 | consolidated_findings.md §3.1 | V | Expertenkommission 27.06.2023 | match |
| Vergabe 3.300–5.000 netto, 6.999 brutto | 3300/5000/6999 | opus3_design_review.md finding 2 | I/I/S | Bernt/Holm 2023; KoopV | match |
| Miete −16 % / 936 € | -16 / 936 | consolidated_findings.md §3.4 | S | Bernt/Holm 2023 | match |
| Kosten 8–36 Mrd €; DIW −0,3…+1,1 | 8/36/-0.3/1.1 | consolidated_findings.md §3.6 | V | Rechnungshof 2024; DIW aktuell 126 | match |
| Risiko-Band 42–46 % | [42,46] | consolidated_findings.md §3.4 | V | DIW aktuell 126 | match |
| Vacancy card 2,07 % / 2,02 % / ~4.600 | 2.07 / 2.02 / 4600 | consolidated_findings.md §3.2; sonnet1_figures.csv | V/V/I | Zensus 2022 Tab. 4000W-3006 | match |
| Owner-type vacancy 2,07/2,02/1,91/1,07 | 2.07/2.02/1.91/1.07 | sonnet1_figures.csv | V | Zensus 2022 | match |

No mismatches were found between `levers.json` / the rendered page and
`consolidated_findings.md` or `sonnet1_figures.csv`. The pipeline (`src/levers.py`)
was already internally consistent with the design and the research docs before this
pass; `tests/test_numbers.py` now pins all of the above so a future edit cannot drift
silently.

## 2. Fixes made in this pass

All fixes are in `src/page/*.js` / `src/page/style.css` / `src/page/template.html`
(never in generated `docs/die-luecke.html` directly; regenerated with
`uv run python src/build_page.py`).

1. **Round 1 identity line was unformatted.** `src/page/partA.js::identityHtml` printed
   the raw `"149403 + 25577 - 9562 = 165418"` string from `levers.json` verbatim. Fixed
   to run each number through `DL.fmt` and render the minus sign as "−", giving
   „149.403 + 25.577 − 9.562 = 165.418 Haushalte × 1,79 ≈ 296.098 Menschen (rechnerisch)".
   Verified live via Playwright (`tests/browser_test.py`, "Round 1 #r1-ledger shows
   formatted identity numbers").
2. **Vergabe axis max was unrounded and the 6.999 label could overflow.**
   `src/page/partB.js::renderVergabeAxis` used `max(campaign, hi) * 1.1` directly as the
   axis domain top (≈ 7.699), so the printed max label was an ugly number, not the
   "0 … 8.000" the handoff specifies. Fixed to round the axis max up to the nearest
   1.000 (→ 8.000) and to switch the „Initiative: 6.999" label's text-anchor to the
   chart's right edge when it would otherwise overflow past the axis.
3. **Waffle used a fixed 10 columns regardless of viewport**, giving ~207 rows and a
   ~1.9k px (not 7.000 px as the brief estimated, but still clearly excessive) vertical
   scroll on a phone for the 2.069-square stock. Fixed: `partB.js` now computes
   `cols = max(20, floor(containerWidth / 9))` and redraws (new layout, not just an
   update) on a debounced `resize` listener. At 375 px viewport this now gives **38
   columns**, ~7 px cells (target in the brief was ~40 cols / 8–9 px; see "Known gaps"
   in `docs/BUILD.md` for the reason — the container's 16 px gutters plus the 2 px cell
   gap eat into the available width more than the brief's back-of-envelope estimate).
   `DL.waffle` itself was already generic in `o.cols`, so the outline contour draws
   correctly at any column count; this needed no change there.
4. **Sozialbindungen used the `owner` kind with an ad-hoc `reverse: true` flag**, so it
   was visually identical (solid orange) to the Vergesellschaften recolour, even though
   the design calls for a distinct "recolour reverse" look. Added a new `reverse` kind
   to `DL.KINDS` (`src/page/app.js`), a `.m-reverse` CSS class and a `pat-cross` SVG
   pattern (orange cross-hatch, dashed outline — visually distinct from both the solid
   `.m-owner` orange and the green-hatched `.m-freed`), wired `sozialbindungenSquares()`
   in `partB.js` to the new kind, and added it to the legend in `template.html`
   ("Bindung läuft aus") since there was room.

## 3. Gate check (handoff §7)

| Gate | Result | Notes |
|---|---|---|
| 1. All V-tagged numbers match consolidated_findings.md to the unit | **pass** | See §1 table; `tests/test_numbers.py` pins 37 of these as regression tests. |
| 2. Three Part 1 caveats and Round 1/2 labels visible without scrolling past the chart | **pass, with a caveat** | Round 1 (#round1) and Round 2 (#round2) headings render at the top of Part A (confirmed via Playwright bounding-box check). The three caveats (#part-a-caveats) render as the *last* section of Part A, after the Bezirk chart and the two dials, but still fully inside Part 1 and well before Part 2 (#part-b) begins — i.e. not "at the page bottom" of the whole document, but also not adjacent to the Round 1/2 charts. This matches design §4 ("three caveats printed under Part 1") literally. If the gate is read to require the caveats directly under the Round charts rather than under all of Part 1, that would be a larger layout change outside this pass's scope; flagging it rather than silently reinterpreting the design doc. |
| 3. Vergesellschaftung panel shows both sides' quotes, no compensation-to-flats squares | **pass** | `quotes_both_sides` (5 quotes, both pro and contra) render in `#pb-verg`; `V.kosten.no_dwelling_conversion` is `true` and the Kosten field only ever shows the DIW annual-budget range (slider, €/yr), never a squares/outline count. Confirmed the Vergabe axis numbers (3.300/5.000/6.999) never appear in `#pb-total` after pulling the lever (`tests/browser_test.py`). |
| 4. Secondary items (Pestel 58.000, bulwiengesa 30.000, campaign 10–20 % vacancy, Vonovia halt) marked S or omitted | **pass** | All four are present in `levers.json.partB.secondary_items`, all tagged `S`, and `partB.js::renderSecondary` only renders items whose tag is `S` or `I`, with `DL.tagBadge` on each. |
| 5. Phone width works; dark mode works; page ≤ 16 MB; no external data calls at runtime | **pass** | 375 px: no horizontal scroll (`scrollWidth === clientWidth`). Dark mode toggle flips `document.documentElement.dataset.theme` and the computed body background. Page size 147.2 KB (`uv run python src/build_page.py` output), far under 16 MB. Network requests during the full interaction script were limited to `cdnjs.cloudflare.com` (D3) — Google Fonts requests happen via `<link>` in `<head>`/CSS `@font-face`, also allowed; zero other hosts seen. |

## 4. Still unverified / out of scope for this pass

- Gate 2's literal placement question above (caveats vs. Round charts proximity).
- The deeper content/sourcing questions already flagged as open in
  `docs/die-luecke-design.md` §5 and §6.4 (dataset L Brandenburg migration, Zensus 2011
  institutional population, Umwandlungen/Wohnungstausch counts, BBU by
  Unternehmensart, all-in LWU cost incl. land) are unchanged by this verification pass;
  they were already out of scope per the handoff (§8 "do not block the build").
- No map yet (noted pre-existing in `docs/BUILD.md` "Known gaps"), unaffected by this
  pass.
- Waffle cell size at 375 px (~7 px) is slightly below the brief's ~8–9 px estimate;
  see fix 3 above and `docs/BUILD.md` "Known gaps" for the reason.

## 5. Final test output

```
$ uv run python src/build_page.py
wrote docs/die-luecke.html (147.2 KB)

$ uv run python -m pytest -q
52 passed

$ uv run python tests/browser_test.py
... (19 checks) ...
All browser checks passed.
```
