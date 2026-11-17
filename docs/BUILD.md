# Build: „Berlin hat Platz gemacht. Wo?" (docs/die-luecke.html)

## Stack

Vanilla JavaScript (ES2020, no modules, no bundler) plus **D3 7.9.0** loaded from
`https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js`. Fonts from Google Fonts
(Fraunces, IBM Plex Sans, IBM Plex Mono) with system fallbacks. Everything else,
CSS, page JS and data, is inlined by a Python build step into one HTML file.

### Why D3 and not the alternatives

- **Plotly** (used by docs/index.html) is good for standard charts but cannot draw
  the custom grammar: a 2,069-cell waffle with hatched, recoloured and dotted
  cells, outline contours, and animated lever pulls. It also adds ~3.5 MB.
- **Observable Plot** handles lines well but the waffle, the two-sided ledger and
  the lever animation would still need raw D3, so we would ship both.
- **Svelte/React** need a bundler or a compile step and add a toolchain for a
  single page with a few hundred lines of UI code.
- D3 alone gives scales, axes, transitions and data joins for every form in the
  design (waffle, ledger, line chart, small multiples, map) at ~280 KB.

## Constraints

- Static, single self-contained HTML, no runtime fetches, no server.
- External scripts only from cdnjs.cloudflare.com or cdn.jsdelivr.net/npm.
- Phone-first, 16 px side gutter, no horizontal page scroll.
- Colour tokens on `:root`, dark values under `@media (prefers-color-scheme: dark)`
  guarded by `:root:not([data-theme="light"])` and again under `:root[data-theme="dark"]`.
- Page size at most 16 MB (the builder refuses to write a larger file).

## File layout

| Path | Role |
|---|---|
| `src/page/template.html` | Shell: head, SVG pattern defs, header, sticky legend, `#part-a`, `#part-b`, tooltip host. Placeholders `/*__STYLE__*/`, `/*__DATA__*/`, `/*__SCRIPTS__*/`. |
| `src/page/style.css` | Tokens (both themes), layout, mark-kind classes `.m-stock/.m-built/.m-owner/.m-freed/.m-permit/.m-need`. |
| `src/page/app.js` | Shared helpers on `window.DL` (see below), theme toggle. |
| `src/page/partA.js` | Teil 1, Wohnungsbilanz. Renders into `#part-a-root`. |
| `src/page/partB.js` | Teil 2, Hebel and waffle. Renders into `#part-b-root`. |
| `src/build_page.py` | Inlines the above plus `data/processed/berlin_panel.csv` (as `DATA.panel`, list of row objects) and `data/processed/levers.json` (as `DATA.levers`). |
| `docs/die-luecke.html` | Build output, committed. |
| `tests/test_build_page.py` | Build smoke test. |

## Helper API (`window.DL`)

```js
DL.fmt(n, digits?)                       // "1.000", "1,8"; null -> "–"
DL.tagBadge(tag)                         // "V" | "S" | "I" -> HTML badge string
DL.tooltip(el, info | (event) => info)   // info: {value, unit, ref_date, spatial_unit, source, tag, label?}
DL.waffle(container, {squares:[{n, kind, info?}], outlines:[{n, label, strength:"strong"|"weak"}],
          perSquare=1000, cols=10, size?}) // -> {svg, cells, update(squares)}
DL.lineChart(container, series, {height=220, fillGap:[keyA,keyB], gapLabel, okLabel, ...})
          // series: [{key, label, color, values:[{x, y, info?}]}]
DL.smallMultiples(container, [{id, title, series}], opts)
DL.KINDS  // ["stock","built","owner","freed","permit"]
```

Colours are referenced as CSS variables (`var(--k-built)` etc.), so charts follow the theme
without redraw. Palette slots 1 to 3 of the dataviz reference palette (blue, orange, aqua) carry
the three filled kinds; they pass the all-pairs colour-vision checks in both themes. Hatching and
dotted/thin outlines carry the other kinds, so no kind relies on colour alone.

## Regenerate and test

```sh
uv run python src/build_page.py                       # writes docs/die-luecke.html
uv run python -m pytest -q                             # pipeline + build + number-audit tests
uv run python tests/browser_test.py                    # Playwright end-to-end check (needs a server; see below)
```

`tests/browser_test.py` expects `docs/die-luecke.html` served at
`http://localhost:8765/die-luecke.html` (e.g. `python -m http.server 8765 --directory docs`
in another shell). It drives both rounds of Part A, both dials, the Part B waffle and the
Vergesellschaften panel with Playwright (`uv add --dev playwright` +
`uv run playwright install chromium` once), and asserts: formatted reveal numbers, the
114 % overlap caveat verbatim, the 137.000 = 41.000+77.000+19.000 bridge, that moving a
dial changes Part B's outline, that the Vergabe axis never feeds `#pb-total`, that S/I
numbers carry a tag badge, no horizontal scroll at 375 px, a working dark-mode toggle,
zero console errors (favicon excluded) and no network calls outside the allowed CDN
hosts. `tests/test_numbers.py` recomputes every printed figure from
`data/processed/levers.json`, the rendered page's inlined `window.DATA`, and
`docs/research/consolidated_findings.md` / `sonnet1_figures.csv`; see
`docs/research/verification_report.md` for the full number-by-number audit and the gate
checklist (handoff §7).

The builder warns and inlines empty placeholders when the processed data files are missing.

## Known gaps

- No map yet (design §4 "Part 1 maps"); geometry would need inlining as TopoJSON.
- No table view for screen readers yet.
- The Part B waffle's column count is responsive
  (`cols = max(20, floor(containerWidth / 9))`, redrawn on a debounced resize) rather
  than the design's literal "10 per row", to avoid an excessive vertical scroll on a
  phone (the fixed 10-column layout gave ~207 rows for the 2,069-square stock). At
  375 px this yields 38 columns and ~7 px cells, slightly under the ~8–9 px a
  back-of-envelope target would suggest, because the 16 px page gutters and the 2 px
  inter-cell gap eat more of the available width than a naive estimate assumes.
- Part 1's three caveats render as the last section of Part A (after the Bezirk chart
  and the two dials), not immediately under the Round 1/2 charts; see
  `docs/research/verification_report.md` §3 (Gate 2) for the reasoning.

Published Artifact: https://claude.ai/artifact/Qb9iUm75xzrZoPU1JWWrC7
