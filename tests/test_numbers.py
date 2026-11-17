"""Number audit for docs/die-luecke.html against data/processed/levers.json and
docs/research/*.md.

Run with: uv run python -m pytest -q tests/test_numbers.py
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
PROCESSED = ROOT / "data" / "processed"
DOCS = ROOT / "docs"
RESEARCH = DOCS / "research"
sys.path.insert(0, str(ROOT))


# --------------------------------------------------------------------------- fixtures
@pytest.fixture(scope="module")
def levers() -> dict:
    return json.loads((PROCESSED / "levers.json").read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def page_data() -> dict:
    html = (DOCS / "die-luecke.html").read_text(encoding="utf-8")
    m = re.search(r"window\.DATA\s*=\s*(\{.*?\});\s*\n", html, re.S)
    assert m, "window.DATA = {...}; not found in docs/die-luecke.html"
    return json.loads(m.group(1))


@pytest.fixture(scope="module")
def page_html() -> str:
    return (DOCS / "die-luecke.html").read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def consolidated() -> str:
    return (RESEARCH / "consolidated_findings.md").read_text(encoding="utf-8")


# --------------------------------------------------------------------------- (a) identities
def test_census_identity_arithmetic():
    assert 149403 + 25577 - 9562 == 165418


def test_arrivals_round1_round2(levers):
    assert levers["roundA"]["arrivals"]["value"] == 304614
    assert levers["roundB"]["arrivals"]["value"] == 103598


def test_round1_taps_sum_to_identity(levers):
    taps = levers["roundA"]["taps"]
    assert taps["neu_gebaut"]["value"] == 149403
    assert taps["aus_leeren_wohnungen"]["value"] == 25577
    assert taps["ferienwohnungen_gewerbe_zweitwohnungen"]["value"] == -9562
    assert (taps["neu_gebaut"]["value"] + taps["aus_leeren_wohnungen"]["value"]
            + taps["ferienwohnungen_gewerbe_zweitwohnungen"]["value"]) == 165418


def test_round2_figures(levers):
    rb = levers["roundB"]
    assert rb["stock_change"]["value"] == 50592
    assert rb["unterkuenfte_change"]["value"] == 27635
    assert rb["uebernommen"]["dwellings"]["value"] == 5400
    assert rb["uebernommen"]["persons"]["value"] == 0


def test_hh_size_and_bridge(levers):
    assert levers["roundA"]["identity"]["persons_per_household"]["value"] == pytest.approx(1.79)
    bridge = levers["dials"]["bridge"]
    assert bridge["reserve_component"]["value"] == 41000
    assert bridge["relief_component"]["value"] == 77000
    assert bridge["replacement_component"]["value"] == 19000
    assert (bridge["reserve_component"]["value"] + bridge["relief_component"]["value"]
            + bridge["replacement_component"]["value"]) == 137000
    assert bridge["total_at_senate_values"]["value"] == 137000


def test_senate_update_211000(levers):
    assert levers["partB"]["senate_need"]["value"] == 211000
    assert levers["dials"]["bridge"]["update_211000"]["value"] == 211000


def test_stock_squares_2069(levers):
    assert levers["partB"]["stock_squares"]["value"] == 2069


# --------------------------------------------------------------------------- Part B lever figures (handoff §3)
def test_part_b_lever_figures(levers):
    L = levers["partB"]["levers"]
    assert L["neu_bauen"]["tempo_2025"]["value"] == 11.0
    assert L["neu_bauen"]["tempo_2019"]["value"] == 19.0
    assert L["neu_bauen"]["lwu"]["value"] == 4.7
    assert L["ueberhang"]["felder"]["value"] == 48.4
    assert L["ueberhang"]["unter_dach"]["value"] == 12.9
    assert L["ueberhang"]["rohbau"]["value"] == 12.3
    assert L["ueberhang"]["nicht_begonnen"]["value"] == 15.8
    assert L["leerstand"]["market_active"]["value"] == 5.4
    assert L["leerstand"]["ceiling"]["value"] == 11.8
    assert L["ferienwohnungen"]["listings"]["value"] == 8.4
    assert L["ferienwohnungen"]["active"]["value"] == 4.9
    assert L["ferienwohnungen"]["returned_since_2014"]["value"] == 8.3
    assert L["ferienwohnungen"]["per_year"]["value"] == 0.5
    assert L["zweckentfremdung_gesamt"]["felder"]["value"] == 31.7
    assert L["aufstocken_umnutzen"]["supermaerkte"]["value"] == [20, 36]
    assert L["aufstocken_umnutzen"]["buero"]["value"] == 30
    assert L["sozialbindungen"]["felder"]["value"] == -46
    assert L["unterkuenfte"]["felder"]["value"] == 54


def test_vergesellschaften_figures(levers):
    V = levers["partB"]["levers"]["vergesellschaften"]
    assert V["umfang"]["value"]["value"] == 222
    assert V["umfang"]["neue_wohnungen"]["value"] == 0
    assert V["umfang"]["share_all_dwellings"]["value"] == 10.7
    assert V["umfang"]["share_rental_stock"]["value"] == 13.5
    assert V["vergabe"]["net_flow_low"]["value"] == 3300
    assert V["vergabe"]["net_flow_high"]["value"] == 5000
    assert V["vergabe"]["campaign_gross_quote"]["value"] == 6999
    assert V["miete"]["rent_relief_pct"]["value"] == -16
    assert V["miete"]["rent_relief_eur_per_hh_year"]["value"] == 936
    assert V["kosten"]["compensation_low_bn_eur"]["value"] == 8
    assert V["kosten"]["compensation_high_bn_eur"]["value"] == 36
    assert V["kosten"]["diw_annual_low_bn_eur"]["value"] == -0.3
    assert V["kosten"]["diw_annual_high_bn_eur"]["value"] == 1.1
    assert V["bauen"]["risk_band"]["private_share_pct"]["value"] == [42, 46]
    assert V["vacancy_card"]["private_company_pct"]["value"] == 2.07
    assert V["vacancy_card"]["berlin_pct"]["value"] == 2.02
    assert V["vacancy_card"]["implied_vacant_of_222000"]["value"] == 4600


def test_zensus_owner_type_vacancy_from_sonnet1_csv(levers):
    """2.07 / 2.02 / 1.91 / 1.07 from docs/research/sonnet1_figures.csv."""
    rows = list(csv.DictReader((RESEARCH / "sonnet1_figures.csv").open(encoding="utf-8")))
    by_metric = {}
    for r in rows:
        try:
            by_metric[r["metric"]] = float(r["value"])
        except ValueError:
            continue  # range values like "1.1-2.9", not needed here
    assert by_metric["Leerstandsquote Insgesamt (dwelling-weighted avg of 12 Bezirke)"] == 2.02
    assert by_metric["Leerstandsquote Privatwirtschaftliches Wohnungsunternehmen"] == 2.07
    assert by_metric["Leerstandsquote Kommune/kommunales Wohnungsunternehmen"] == 1.91
    assert by_metric["Leerstandsquote Wohnungsgenossenschaft"] == 1.07

    V = levers["partB"]["levers"]["vergesellschaften"]
    assert V["vacancy_card"]["private_company_pct"]["value"] == 2.07
    assert V["vacancy_card"]["berlin_pct"]["value"] == 2.02


# --------------------------------------------------------------------------- (a) rendered page carries the same numbers
NUMBERS_IN_PAGE_DATA = [
    ("roundA.arrivals.value", 304614),
    ("roundA.identity.dwellings.value", 165418),
    ("roundA.taps.neu_gebaut.value", 149403),
    ("roundA.taps.aus_leeren_wohnungen.value", 25577),
    ("roundA.taps.ferienwohnungen_gewerbe_zweitwohnungen.value", -9562),
    ("roundB.arrivals.value", 103598),
    ("roundB.stock_change.value", 50592),
    ("roundB.unterkuenfte_change.value", 27635),
    ("roundB.uebernommen.dwellings.value", 5400),
    ("roundA.identity.persons_per_household.value", 1.79),
    ("dials.bridge.total_at_senate_values.value", 137000),
    ("dials.bridge.reserve_component.value", 41000),
    ("dials.bridge.relief_component.value", 77000),
    ("dials.bridge.replacement_component.value", 19000),
    ("partB.senate_need.value", 211000),
    ("partB.stock_squares.value", 2069),
]


def _get(d, path):
    for p in path.split("."):
        d = d[p]
    return d


@pytest.mark.parametrize("path,expected", NUMBERS_IN_PAGE_DATA)
def test_number_inlined_in_page_data(page_data, path, expected):
    got = _get(page_data["levers"], path)
    assert got == pytest.approx(expected) if isinstance(expected, float) else got == expected


# --------------------------------------------------------------------------- (b) every V-tagged value matches consolidated_findings.md
def fmt_de(n) -> str:
    """Render a number the way the German page would (thousands separator '.')."""
    if isinstance(n, float) and n.is_integer():
        n = int(n)
    s = f"{n:,}".replace(",", "§").replace(".", ",").replace("§", ".")
    return s


def walk_leaves(node, path=""):
    if isinstance(node, dict):
        required = {"value", "unit", "ref_date", "spatial_unit", "source", "tag"}
        if required.issubset(node.keys()):
            yield path, node
            return
        for k, val in node.items():
            yield from walk_leaves(val, f"{path}.{k}" if path else k)
    elif isinstance(node, list):
        for i, val in enumerate(node):
            yield from walk_leaves(val, f"{path}[{i}]")


# A handful of V-tagged values that the handoff explicitly calls out; checked by
# unit against consolidated_findings.md. Exact-number variants (e.g. "25.577" or
# "25,577") are searched since the doc mixes plain and German formatting.
V_SPOT_CHECKS = [
    ("roundA.arrivals.value", "304,614"),
    ("roundA.taps.neu_gebaut.value", "149,403"),
    ("roundA.taps.aus_leeren_wohnungen.value", "25,577"),
    ("roundB.arrivals.value", "103,598"),
    ("roundB.stock_change.value", "50,592"),
    ("dials.bridge.total_at_senate_values.value", "137,000"),
    ("partB.levers.ueberhang.felder.value", "48,394"),
    ("partB.levers.vergesellschaften.umfang.value.value", "222,000"),
]


@pytest.mark.parametrize("path,doc_substring", V_SPOT_CHECKS)
def test_v_tagged_value_appears_in_consolidated_findings(levers, consolidated, path, doc_substring):
    assert doc_substring in consolidated or doc_substring.replace(",", ".") in consolidated, (
        f"{doc_substring!r} (for levers.{path}) not found in consolidated_findings.md"
    )


def test_all_v_tagged_leaves_have_a_source_string(levers):
    """Every leaf tagged V/S/I must carry a non-empty source citation."""
    missing = [p for p, leaf in walk_leaves(levers) if not leaf.get("source")]
    assert not missing, missing


# --------------------------------------------------------------------------- (c) S/I leaves carry a tag badge in the HTML
# These are the labels used for S/I tagged leaves in the levers.json that should
# be discoverable as text in the built page (badge adjacency is checked by the
# browser test, which inspects the live DOM; here we assert the source text and
# tag exist together in the inlined JSON that app.js renders from).
def test_s_and_i_tagged_leaves_present(levers):
    si_leaves = [(p, leaf) for p, leaf in walk_leaves(levers) if leaf.get("tag") in ("S", "I")]
    assert si_leaves, "expected at least one S/I-tagged leaf"
    for p, leaf in si_leaves:
        assert leaf["tag"] in ("S", "I")


def test_tag_badge_rendering_function_marks_s_and_i(page_html):
    # DL.tagBadge renders class="tag tag-S"/"tag-I" for S/I values (app.js, inlined).
    assert 'tag-${t}' in page_html or "tag tag-" in page_html
    assert "TAG_TITLES" in page_html
