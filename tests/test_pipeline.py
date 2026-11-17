"""Tests for the data pipeline (src/panel.py, src/levers.py).

Run with: uv run python -m pytest -q tests/test_pipeline.py
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"

DISTRICTS = [
    "Mitte", "Friedrichshain-Kreuzberg", "Pankow", "Charlottenburg-Wilmersdorf",
    "Spandau", "Steglitz-Zehlendorf", "Tempelhof-Schöneberg", "Neukölln",
    "Treptow-Köpenick", "Marzahn-Hellersdorf", "Lichtenberg", "Reinickendorf",
]


@pytest.fixture(scope="module")
def panel() -> pd.DataFrame:
    import sys
    sys.path.insert(0, str(ROOT))
    from src.panel import build_panel
    return build_panel()


@pytest.fixture(scope="module")
def levers() -> dict:
    import sys
    sys.path.insert(0, str(ROOT))
    from src.levers import build
    return build()


def test_census_identity():
    assert 149403 + 25577 - 9562 == 165418


def test_levers_identity_matches_json(levers):
    ident = levers["roundA"]["identity"]
    assert ident["formula"] == "149403 + 25577 - 9562 = 165418"
    assert ident["dwellings"]["value"] == 165418


def test_levers_round1_taps(levers):
    taps = levers["roundA"]["taps"]
    assert taps["neu_gebaut"]["value"] == 149403
    assert taps["aus_leeren_wohnungen"]["value"] == 25577
    assert taps["ferienwohnungen_gewerbe_zweitwohnungen"]["value"] == -9562
    assert levers["roundA"]["arrivals"]["value"] == 304614


def test_levers_round2(levers):
    rb = levers["roundB"]
    assert rb["arrivals"]["value"] == 103598
    assert rb["stock_change"]["value"] == 50592
    assert rb["unterkuenfte_change"]["value"] == 27635
    assert rb["uebernommen"]["dwellings"]["value"] == 5400
    assert rb["uebernommen"]["persons"]["value"] == 0


def test_levers_bridge_sums_to_137000(levers):
    bridge = levers["dials"]["bridge"]
    total = (bridge["reserve_component"]["value"] + bridge["relief_component"]["value"]
             + bridge["replacement_component"]["value"])
    assert total == 137000
    assert bridge["total_at_senate_values"]["value"] == 137000


def test_levers_vergesellschaften_umfang(levers):
    verg = levers["partB"]["levers"]["vergesellschaften"]
    assert verg["umfang"]["value"]["value"] == 222
    assert verg["umfang"]["neue_wohnungen"]["value"] == 0
    assert verg["vacancy_card"]["private_company_pct"]["value"] == 2.07
    assert verg["vacancy_card"]["berlin_pct"]["value"] == 2.02


def test_levers_stock_and_need(levers):
    assert levers["partB"]["stock_squares"]["value"] == 2069
    assert levers["partB"]["senate_need"]["value"] == 211000


def test_levers_berlin_totals_match_consolidated_findings(levers):
    # docs/research/consolidated_findings.md §1
    assert levers["roundA"]["arrivals"]["value"] == 304614
    assert levers["roundB"]["arrivals"]["value"] == 103598
    # §2 Bauüberhang end-2025
    ueberhang = levers["partB"]["levers"]["ueberhang"]
    assert ueberhang["felder"]["value"] == 48.4
    assert ueberhang["unter_dach"]["value"] == 12.9
    assert ueberhang["rohbau"]["value"] == 12.3
    assert ueberhang["nicht_begonnen"]["value"] == 15.8
    # §3 expropriation scope
    assert levers["partB"]["levers"]["vergesellschaften"]["umfang"]["value"]["value"] == 222


def test_every_leaf_number_has_six_fields_and_valid_tag(levers):
    required = {"value", "unit", "ref_date", "spatial_unit", "source", "tag"}
    valid_tags = {"V", "S", "I"}
    errors = []

    def walk(node, path):
        if isinstance(node, dict):
            if required.issubset(node.keys()):
                if node["tag"] not in valid_tags:
                    errors.append(f"{path}: invalid tag {node['tag']!r}")
                return  # this dict IS a leaf number object; don't recurse further
            for k, v in node.items():
                walk(v, f"{path}.{k}")
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, f"{path}[{i}]")

    walk(levers, "levers")
    assert not errors, "\n".join(errors)


def test_panel_bezirk_count_and_years(panel):
    assert set(panel.bezirk) == set(DISTRICTS) | {"Berlin"}
    assert set(panel.year) == set(range(2011, 2026))
    assert len(panel) == 13 * 15


def test_panel_completions_bezirk_sums_equal_berlin(panel):
    for year in range(2012, 2026):
        yr = panel[panel.year == year]
        bezirk_sum = yr[yr.bezirk != "Berlin"]["completions"].sum()
        berlin_val = yr[yr.bezirk == "Berlin"]["completions"].iloc[0]
        assert bezirk_sum == pytest.approx(berlin_val, rel=1e-6), f"year {year}"


def test_panel_population_census_basis_bezirk_sums_equal_berlin_at_anchors(panel):
    for year in (2011, 2022, 2025):
        yr = panel[panel.year == year]
        bezirk_sum = yr[yr.bezirk != "Berlin"]["population_census_basis"].sum()
        berlin_val = yr[yr.bezirk == "Berlin"]["population_census_basis"].iloc[0]
        assert bezirk_sum == pytest.approx(berlin_val, rel=1e-6), f"year {year}"


def test_panel_estimated_years_flagged(panel):
    anchors = {2011, 2022, 2025}
    non_anchor = panel[~panel.year.isin(anchors)]
    assert (non_anchor["estimated"] == True).all()
    at_anchor = panel[panel.year.isin(anchors)]
    assert (at_anchor["estimated"] == False).all()


def test_panel_files_exist_on_disk():
    assert (PROCESSED / "berlin_panel.csv").exists()
    assert (PROCESSED / "levers.json").exists()
    df = pd.read_csv(PROCESSED / "berlin_panel.csv")
    assert "estimated" in df.columns
    data = json.loads((PROCESSED / "levers.json").read_text())
    assert "roundA" in data and "partB" in data
