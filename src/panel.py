"""Build the Bezirk x year panel for "Die Lücke" (data/processed/berlin_panel.csv).

Combines:
 - completions: data/processed/berlin_completions_wide.csv (existing, from src/berlin.py)
 - population_register: data/processed/berlin_population_by_district.csv (existing)
 - population_census_basis: census-anchored population, built per the handoff method
   (docs/handoff-build-oversight.md §4): Zensus 2011 and A I 3 2025 per-Bezirk anchors
   from src/data/hand_inputs.yaml, with 2012-2021 estimated by scaling the register by
   the Berlin-wide A I 3/register ratio and blending the Bezirk residual between the
   two census anchors (`estimated=True`).
 - stock / stock_basis: F I 1 series (Berlin-wide verified; per-Bezirk 2025 is an
   estimate carried in hand_inputs.yaml, `estimated=True`).
 - households, dwellings_zensus, vacancy_zensus, vacancy_rate: Zensus 2022 kleinräumig
   (Bezirksregionen -> Bezirk), Gemeinde-level official totals for the Berlin row.
 - hh_size: Mikrozensus Bezirk household size (A I 10 Tab. 7.4) and the Berlin series.

Run with: uv run python src/panel.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
HAND = ROOT / "src" / "data" / "hand_inputs.yaml"

DISTRICTS = [
    "Mitte", "Friedrichshain-Kreuzberg", "Pankow", "Charlottenburg-Wilmersdorf",
    "Spandau", "Steglitz-Zehlendorf", "Tempelhof-Schöneberg", "Neukölln",
    "Treptow-Köpenick", "Marzahn-Hellersdorf", "Lichtenberg", "Reinickendorf",
]
YEARS = list(range(2011, 2026))


def load_hand() -> dict:
    with open(HAND, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _nearest_mz_size(hand: dict, district: str | None, year: int) -> float:
    """Nearest available Mikrozensus household-size value <= year, falling back to
    the closest later year if none earlier exists. district=None -> Berlin series."""
    if district is None:
        series = hand["hh_size"]["berlin_by_year"]
        years = sorted(series)
        le = [y for y in years if y <= year]
        y = max(le) if le else min(years)
        return series[y]
    series = hand["hh_size"]["by_district_year"]
    years = sorted(int(y) for y in series)
    le = [y for y in years if y <= year]
    y = max(le) if le else min(years)
    return series[y][district]


def build_population_census_basis(register_long: pd.DataFrame, hand: dict) -> pd.DataFrame:
    """Census-anchored population per Bezirk x year, 2011-2025.

    Anchors: Zensus 2011 (9.5.2011, treated as the 2011 value) and A I 3 2025
    (31.12.2025). 2022 also has a direct anchor (Zensus 2022). For 2012-2021 and
    2023-2024, scale the register by the Berlin-wide ratio of the census-anchored
    series to the register for that year (register is available 2011-2025; the
    Berlin-wide A I 3 Fortschreibung end-2025/2022 gives the two solid later
    anchor ratios, interpolated for years without a direct Berlin-wide reading),
    then blend the Bezirk-specific residual (census/register at the two nearest
    anchors) linearly between anchors, per the handoff's §4 method.
    """
    census = hand["census"]["by_district"]
    census_berlin = hand["census"]["berlin"]
    pop25 = hand["pop_census_anchored_2025"]["by_district"]
    pop25_berlin = hand["pop_census_anchored_2025"]["berlin"]

    reg_wide = register_long.pivot(index="year", columns="district", values="population")

    anchors = {2011: {}, 2022: {}, 2025: {}}
    for d in DISTRICTS:
        anchors[2011][d] = census[d]["pop_2011"]
        anchors[2022][d] = census[d]["pop_2022"]
        anchors[2025][d] = pop25[d]
    anchors[2011]["Berlin"] = census_berlin["pop_2011"]
    anchors[2022]["Berlin"] = census_berlin["pop_2022"]
    anchors[2025]["Berlin"] = pop25_berlin

    rows = []
    for year in YEARS:
        for d in DISTRICTS:
            reg_val = reg_wide.loc[year, d] if year in reg_wide.index else None
            if year in (2011, 2022, 2025):
                rows.append({"bezirk": d, "year": year, "population_census_basis": anchors[year][d],
                             "population_register": reg_val, "estimated": False})
                continue
            # choose bracketing anchors
            lo, hi = (2011, 2022) if year < 2022 else (2022, 2025)
            if reg_val is None or reg_wide.loc[lo, d] is None or reg_wide.loc[hi, d] is None:
                rows.append({"bezirk": d, "year": year, "population_census_basis": None,
                             "population_register": reg_val, "estimated": True})
                continue
            ratio_lo = anchors[lo][d] / reg_wide.loc[lo, d]
            ratio_hi = anchors[hi][d] / reg_wide.loc[hi, d]
            frac = (year - lo) / (hi - lo)
            ratio = ratio_lo + frac * (ratio_hi - ratio_lo)
            est = reg_val * ratio
            rows.append({"bezirk": d, "year": year, "population_census_basis": est,
                         "population_register": reg_val, "estimated": True})
        # Berlin row
        reg_val = reg_wide.loc[year].sum() if year in reg_wide.index else None
        if year in (2011, 2022, 2025):
            rows.append({"bezirk": "Berlin", "year": year, "population_census_basis": anchors[year]["Berlin"],
                         "population_register": reg_val, "estimated": False})
        else:
            lo, hi = (2011, 2022) if year < 2022 else (2022, 2025)
            reg_lo = reg_wide.loc[lo].sum()
            reg_hi = reg_wide.loc[hi].sum()
            ratio_lo = anchors[lo]["Berlin"] / reg_lo
            ratio_hi = anchors[hi]["Berlin"] / reg_hi
            frac = (year - lo) / (hi - lo)
            ratio = ratio_lo + frac * (ratio_hi - ratio_lo)
            rows.append({"bezirk": "Berlin", "year": year, "population_census_basis": reg_val * ratio,
                         "population_register": reg_val, "estimated": True})
    return pd.DataFrame(rows)


def build_stock(hand: dict) -> pd.DataFrame:
    """Stock per Bezirk x year. Only Berlin-wide values are verified for most years;
    per-Bezirk values are only available for 2023 (example) and 2025 (estimate from
    stage3a Table 4b). We fill district x year stock by holding the district's 2025
    estimated share of the Berlin total constant back through time, scaled to each
    year's Berlin total -- flagged estimated for all years except where a direct
    reading exists (none at Bezirk level here, so all Bezirk-level stock is
    `stock_basis`-tagged as derived; Berlin rows carry the verified series)."""
    s = hand["stock"]
    berlin_by_year = s["berlin_by_year"]
    district_2025 = s["district_2025_estimate"]["values"]
    berlin_2025 = s["district_2025_estimate"]["berlin"]
    shares = {d: district_2025[d] / berlin_2025 for d in DISTRICTS}

    def basis_for(year: int) -> str:
        if year < 2021:
            return "census_2011"
        return "census_2022_gwz"

    rows = []
    for year in YEARS:
        # interpolate Berlin total for years not directly given
        known_years = sorted(berlin_by_year)
        if year in berlin_by_year:
            berlin_val = berlin_by_year[year]
        else:
            lo = max(y for y in known_years if y <= year)
            hi = min(y for y in known_years if y >= year)
            if lo == hi:
                berlin_val = berlin_by_year[lo]
            else:
                frac = (year - lo) / (hi - lo)
                berlin_val = berlin_by_year[lo] + frac * (berlin_by_year[hi] - berlin_by_year[lo])
        for d in DISTRICTS:
            rows.append({"bezirk": d, "year": year, "stock": berlin_val * shares[d],
                         "stock_basis": basis_for(year)})
        rows.append({"bezirk": "Berlin", "year": year, "stock": berlin_val, "stock_basis": basis_for(year)})
    return pd.DataFrame(rows)


def build_hh_zensus(hand: dict) -> pd.DataFrame:
    """Zensus 2022 households/dwellings/vacancy per Bezirk, held constant across
    years (it is a point-in-time census reading; see design: Zensus 2022 kleinraeumig
    for households/dwellings/vacancy, Gemeinde-level official totals for Berlin)."""
    census = hand["census"]["by_district"]
    census_berlin = hand["census"]["berlin"]
    rows = []
    for d in DISTRICTS:
        hh = census[d]["hh_2022"]
        dw = census[d]["dw_2022"]
        vac = census[d]["vac_2022"]
        rows.append({"bezirk": d, "households": hh, "dwellings_zensus": dw,
                      "vacancy_zensus": vac, "vacancy_rate": vac / dw})
    rows.append({"bezirk": "Berlin", "households": census_berlin["hh_2022"],
                 "dwellings_zensus": census_berlin["dw_2022"], "vacancy_zensus": census_berlin["vac_2022"],
                 "vacancy_rate": census_berlin["vac_2022"] / census_berlin["dw_2022"]})
    return pd.DataFrame(rows)


def build_panel() -> pd.DataFrame:
    hand = load_hand()
    completions_wide = pd.read_csv(PROCESSED / "berlin_completions_wide.csv", index_col=0)
    register_long = pd.read_csv(PROCESSED / "berlin_population_by_district.csv")

    comp_rows = []
    for year in completions_wide.index:
        if year not in YEARS:
            continue
        for d in DISTRICTS + ["Berlin"]:
            if d in completions_wide.columns:
                comp_rows.append({"bezirk": d, "year": int(year), "completions": completions_wide.loc[year, d]})
    comp_df = pd.DataFrame(comp_rows)

    pop_df = build_population_census_basis(register_long, hand)
    stock_df = build_stock(hand)
    hh_df = build_hh_zensus(hand)
    hh_size_df = pd.DataFrame(
        [{"bezirk": d, "year": y, "hh_size": _nearest_mz_size(hand, d, y)} for d in DISTRICTS for y in YEARS]
        + [{"bezirk": "Berlin", "year": y, "hh_size": _nearest_mz_size(hand, None, y)} for y in YEARS]
    )

    panel = comp_df.merge(pop_df, on=["bezirk", "year"], how="outer")
    panel = panel.merge(stock_df, on=["bezirk", "year"], how="left")
    panel = panel.merge(hh_size_df, on=["bezirk", "year"], how="left")
    panel = panel.merge(hh_df, on="bezirk", how="left")

    panel["completions"] = panel.get("completions")
    panel = panel.sort_values(["bezirk", "year"]).reset_index(drop=True)
    cols = ["bezirk", "year", "completions", "population_census_basis", "population_register",
            "estimated", "stock", "stock_basis", "households", "dwellings_zensus",
            "vacancy_zensus", "vacancy_rate", "hh_size"]
    panel = panel[cols]
    return panel


def main() -> None:
    panel = build_panel()
    out = PROCESSED / "berlin_panel.csv"
    panel.to_csv(out, index=False)
    print(f"wrote {out} ({len(panel)} rows)")
    berlin_2025 = panel[(panel.bezirk == "Berlin") & (panel.year == 2025)].iloc[0]
    print(berlin_2025)


if __name__ == "__main__":
    main()
