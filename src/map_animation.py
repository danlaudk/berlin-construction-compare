"""Build an animated, side-by-side choropleth comparing Berlin and Copenhagen.

Metric: dwellings completed per 1,000 residents, by district, 2010-2025.
Output: docs/index.html (self-contained; GitHub Pages serves docs/).

Run with: uv run python src/map_animation.py
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "processed"
GEO = ROOT / "data" / "geo"
OUT_HTML = ROOT / "docs" / "index.html"

YEARS = list(range(2010, 2026))

# Sequential blue ramp, light->dark, from the dataviz skill's reference palette.
BLUE_RAMP = [
    "#fcfcfb",  # near-zero recedes to the chart surface
    "#cde2fb",
    "#9ec5f4",
    "#6da7ec",
    "#3987e5",
    "#1c5cab",
    "#104281",
    "#0d366b",
]
COLORSCALE = [[i / (len(BLUE_RAMP) - 1), c] for i, c in enumerate(BLUE_RAMP)]

INK = "#0b0b0b"
SECONDARY_INK = "#52514e"
SURFACE = "#fcfcfb"


def load_berlin() -> pd.DataFrame:
    comp = pd.read_csv(DATA / "berlin_completions_by_district.csv")
    comp = comp[comp["measure"] == "dwellings_total"][["year", "district", "value"]]
    comp = comp.rename(columns={"value": "dwellings"})
    pop = pd.read_csv(DATA / "berlin_population_by_district.csv")[["year", "district", "population"]]
    df = comp.merge(pop, on=["year", "district"], how="inner")
    df["city"] = "Berlin"
    return df


def load_copenhagen() -> pd.DataFrame:
    comp = pd.read_csv(DATA / "copenhagen_completions_by_district.csv")
    measure = [m for m in comp["measure"].unique() if m.startswith("dwellings_by_commissioning_year")][0]
    comp = comp[comp["measure"] == measure][["year", "district", "value"]]
    comp = comp.rename(columns={"value": "dwellings"})
    pop = pd.read_csv(DATA / "copenhagen_population_by_district.csv")[["year", "district", "population"]]
    df = comp.merge(pop, on=["year", "district"], how="inner")
    df["city"] = "Copenhagen"
    return df


def build_panel() -> pd.DataFrame:
    df = pd.concat([load_berlin(), load_copenhagen()], ignore_index=True)
    df = df[df["year"].isin(YEARS)].copy()
    df["per_1000"] = df["dwellings"] / df["population"] * 1000
    return df


def city_totals(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby(["city", "year"], as_index=False).agg(
        dwellings=("dwellings", "sum"), population=("population", "sum")
    )
    g["per_1000"] = g["dwellings"] / g["population"] * 1000
    return g


def load_geo(path: Path) -> tuple[dict, list[str]]:
    gj = json.loads(path.read_text())
    names = [f["properties"]["district"] for f in gj["features"]]
    return gj, names


def make_frame_traces(
    df_year: pd.DataFrame,
    names: list[str],
    geojson: dict,
    cmax: float,
    geo_key: str,
    showscale: bool,
) -> go.Choroplethmap:
    d = df_year.set_index("district").reindex(names)
    z = d["per_1000"].clip(upper=cmax).fillna(0).tolist()
    # Keep customdata as a plain list of per-row lists (mixed str/float) rather
    # than np.stack, which would force a common dtype and silently turn the
    # numeric columns into strings -- breaking the hovertemplate's :,.0f /
    # :.2f number formatting.
    dwellings_col = d["dwellings"].fillna(0).tolist()
    population_col = d["population"].fillna(0).tolist()
    rate_col = d["per_1000"].fillna(0).tolist()
    customdata = [
        [name, dw, pop, rate]
        for name, dw, pop, rate in zip(names, dwellings_col, population_col, rate_col)
    ]
    return go.Choroplethmap(
        geojson=geojson,
        locations=names,
        z=z,
        zmin=0,
        zmax=cmax,
        colorscale=COLORSCALE,
        featureidkey="properties.district",
        customdata=customdata,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Dwellings completed: %{customdata[1]:,.0f}<br>"
            "Population: %{customdata[2]:,.0f}<br>"
            "Per 1,000 residents: %{customdata[3]:.2f}"
            "<extra></extra>"
        ),
        marker_line_width=0.6,
        marker_line_color="rgba(11,11,11,0.35)",
        subplot=geo_key,
        showscale=showscale,
        colorbar=dict(
            title=dict(text="Dwellings<br>per 1,000<br>residents", font=dict(size=11, color=SECONDARY_INK)),
            tickfont=dict(size=10, color=SECONDARY_INK),
            len=0.75,
            x=1.02,
        ) if showscale else None,
    )


def main() -> None:
    df = build_panel()
    totals = city_totals(df)

    berlin_geo, berlin_names = load_geo(GEO / "berlin_bezirke.geojson")
    cph_geo, cph_names = load_geo(GEO / "copenhagen_bydele.geojson")

    cmax = float(np.percentile(df["per_1000"], 98))
    cmax = round(cmax, 1)

    year0 = YEARS[0]
    b0 = df[(df["city"] == "Berlin") & (df["year"] == year0)]
    c0 = df[(df["city"] == "Copenhagen") & (df["year"] == year0)]

    trace_b = make_frame_traces(b0, berlin_names, berlin_geo, cmax, "map", showscale=False)
    trace_c = make_frame_traces(c0, cph_names, cph_geo, cmax, "map2", showscale=True)

    fig = go.Figure(data=[trace_b, trace_c])

    def totals_annotation_text(city: str, year: int) -> str:
        row = totals[(totals["city"] == city) & (totals["year"] == year)]
        if row.empty:
            return f"<b>{city}</b> {year}: no data"
        r = row.iloc[0]
        return (
            f"<b>{city}</b> {year}: {r['dwellings']:,.0f} dwellings "
            f"· {r['per_1000']:.2f} / 1,000"
        )

    def annotations_for_year(year: int):
        # One combined city-name + total annotation per panel (avoids a second
        # row of text competing with the two-line title for vertical space).
        return [
            dict(
                text=totals_annotation_text("Berlin", year),
                xref="paper", yref="paper", x=0.0, y=1.045,
                xanchor="left", showarrow=False,
                font=dict(size=13, color=INK),
            ),
            dict(
                text=totals_annotation_text("Copenhagen", year),
                xref="paper", yref="paper", x=1.0, y=1.045,
                xanchor="right", showarrow=False,
                font=dict(size=13, color=INK),
            ),
        ]

    frames = []
    for year in YEARS:
        by = df[(df["city"] == "Berlin") & (df["year"] == year)]
        cy = df[(df["city"] == "Copenhagen") & (df["year"] == year)]
        tb = make_frame_traces(by, berlin_names, berlin_geo, cmax, "map", showscale=False)
        tc = make_frame_traces(cy, cph_names, cph_geo, cmax, "map2", showscale=True)
        frames.append(
            go.Frame(
                data=[tb, tc],
                name=str(year),
                layout=go.Layout(annotations=annotations_for_year(year)),
            )
        )
    fig.frames = frames
    fig.layout.annotations = annotations_for_year(year0)

    # Berlin centroid approx 52.52N 13.40E; Copenhagen approx 55.68N 12.57E
    fig.update_layout(
        map=dict(
            style="carto-positron",
            center=dict(lat=52.50, lon=13.40),
            zoom=8.85,
            domain=dict(x=[0.0, 0.48], y=[0.0, 1.0]),
        ),
        map2=dict(
            style="carto-positron",
            center=dict(lat=55.685, lon=12.56),
            zoom=10.3,
            domain=dict(x=[0.52, 1.0], y=[0.0, 1.0]),
        ),
        margin=dict(l=10, r=10, t=110, b=10),
        height=680,
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        font=dict(family="system-ui, -apple-system, 'Segoe UI', sans-serif", color=INK),
        title=dict(
            text=(
                "Dwellings completed per 1,000 residents by district, 2010–2025<br>"
                "<sup>Berlin: Fertigstellungen (AfS Berlin-Brandenburg F II 2). "
                "Copenhagen: KKBOL1 stock-by-commissioning-year (Københavns Kommune), "
                "a completions proxy. 2025 provisional.</sup>"
            ),
            x=0.5, xanchor="center",
            font=dict(size=17),
        ),
        annotations=annotations_for_year(year0),
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                x=0.0, y=-0.02, xanchor="left", yanchor="top",
                buttons=[
                    dict(
                        label="Play",
                        method="animate",
                        args=[None, dict(frame=dict(duration=900, redraw=True), fromcurrent=True, transition=dict(duration=300))],
                    ),
                    dict(
                        label="Pause",
                        method="animate",
                        args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate", transition=dict(duration=0))],
                    ),
                ],
            )
        ],
        sliders=[
            dict(
                active=0,
                x=0.08, len=0.84, y=-0.02, xanchor="left", yanchor="top",
                currentvalue=dict(prefix="Year: ", font=dict(size=13, color=INK)),
                pad=dict(t=30),
                steps=[
                    dict(
                        label=str(year),
                        method="animate",
                        args=[[str(year)], dict(mode="immediate", frame=dict(duration=300, redraw=True), transition=dict(duration=300))],
                    )
                    for year in YEARS
                ],
            )
        ],
    )

    OUT_HTML.parent.mkdir(parents=True, exist_ok=True)
    fig.write_html(
        str(OUT_HTML),
        include_plotlyjs="cdn",
        full_html=True,
        auto_play=False,
        config={"responsive": True, "displaylogo": False},
    )
    inject_wrapper(OUT_HTML)
    print(f"Wrote {OUT_HTML} ({OUT_HTML.stat().st_size/1024:.1f} KB)")


def inject_wrapper(path: Path) -> None:
    html = path.read_text()
    header = """
<style>
  body { margin: 0; background: #f9f9f7; font-family: system-ui, -apple-system, 'Segoe UI', sans-serif; color: #0b0b0b; }
  .viz-wrap { max-width: 1200px; margin: 0 auto; padding: 16px 16px 8px; }
  .viz-footer { max-width: 1200px; margin: 0 auto; padding: 0 16px 32px; color: #52514e; font-size: 13px; line-height: 1.5; }
  .viz-footer a { color: #184f95; }
  @media (max-width: 760px) { .viz-wrap, .viz-footer { padding-left: 8px; padding-right: 8px; } }
</style>
<div class="viz-wrap">
"""
    footer = """
</div>
<div class="viz-footer">
  <p><strong>Reading this map:</strong> colour encodes dwellings completed per 1,000 residents in each
  district for the selected year, on one fixed scale shared across both cities and all years (0 to the
  98th percentile of all district-year values; higher values are clipped to the top of the scale so a
  few outlier districts/years don't wash out the rest). Hover any district for the district name, year,
  raw number of dwellings completed, population, and the per-1,000 rate. The text above each map shows
  that city's total for the selected year.</p>
  <p><strong>Caveat:</strong> Berlin's figures are completions (Fertigstellungen) from Statistik
  Berlin-Brandenburg's F2 series. Copenhagen's KKBOL1 series is dwelling stock grouped by commissioning
  year, which is a proxy for completions rather than an identical measure, and may be revised in later
  releases. 2025 is provisional for both cities. See
  <a href="README.md">README.md</a> in this folder for data sources, processing notes and licences, and
  the repository's <code>outputs/REPORT.md</code> for the full completions-vs-population analysis.</p>
</div>
"""
    html = html.replace("<body>", "<body>" + header, 1)
    html = html.replace("</body>", footer + "</body>", 1)
    path.write_text(html)


if __name__ == "__main__":
    main()
