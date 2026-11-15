"""Prepare simplified district GeoJSON files for Berlin and Copenhagen.

Reads the raw downloads in data/geo/ (fetched once from open-data sources,
see docs/README.md for provenance) and writes small, simplified, re-keyed
GeoJSON files that carry a single `district` property matching the district
names used in data/processed/*_by_district.csv.

Run with: uv run python src/geo_prep.py
"""
from __future__ import annotations

import json
from pathlib import Path

from shapely.geometry import shape, mapping

GEO_DIR = Path(__file__).resolve().parent.parent / "data" / "geo"

# Berlin: raw file already uses `name` == CSV district name directly.
BERLIN_SRC = GEO_DIR / "berlin_raw.geojson"
BERLIN_OUT = GEO_DIR / "berlin_bezirke.geojson"

# Copenhagen: raw file uses `navn`, with one punctuation mismatch vs the CSV.
CPH_SRC = GEO_DIR / "cph_wfs.geojson"
CPH_OUT = GEO_DIR / "copenhagen_bydele.geojson"
CPH_NAME_MAP = {
    "Amager Vest": "Amager Vest",
    "Amager Øst": "Amager Øst",
    "Bispebjerg": "Bispebjerg",
    "Brønshøj-Husum": "Brønshøj-Husum",
    "Indre By": "Indre By",
    "Nørrebro": "Nørrebro",
    "Valby": "Valby",
    "Vanløse": "Vanløse",
    "Vesterbro-Kongens Enghave": "Vesterbro/Kongens Enghave",  # dash -> slash to match CSV
    "Østerbro": "Østerbro",
}

# Simplification tolerance in degrees (~tens of metres at these latitudes).
SIMPLIFY_TOLERANCE = 0.0003


def simplify_feature(feat: dict, name: str, tolerance: float) -> dict:
    geom = shape(feat["geometry"])
    simplified = geom.simplify(tolerance, preserve_topology=True)
    return {
        "type": "Feature",
        "properties": {"district": name},
        "geometry": mapping(simplified),
    }


def build_berlin() -> None:
    data = json.loads(BERLIN_SRC.read_text())
    features = []
    names = set()
    for feat in data["features"]:
        name = feat["properties"]["name"]
        names.add(name)
        features.append(simplify_feature(feat, name, SIMPLIFY_TOLERANCE))
    assert len(features) == 12, f"expected 12 Berlin Bezirke, got {len(features)}"
    out = {"type": "FeatureCollection", "features": features}
    BERLIN_OUT.write_text(json.dumps(out))
    print(f"Berlin: {len(features)} features -> {BERLIN_OUT} ({BERLIN_OUT.stat().st_size/1024:.1f} KB)")
    print("  names:", sorted(names))


def build_copenhagen() -> None:
    data = json.loads(CPH_SRC.read_text())
    features = []
    names = set()
    for feat in data["features"]:
        raw_name = feat["properties"]["navn"]
        name = CPH_NAME_MAP[raw_name]
        names.add(name)
        features.append(simplify_feature(feat, name, SIMPLIFY_TOLERANCE))
    assert len(features) == 10, f"expected 10 Copenhagen bydele, got {len(features)}"
    out = {"type": "FeatureCollection", "features": features}
    CPH_OUT.write_text(json.dumps(out))
    print(f"Copenhagen: {len(features)} features -> {CPH_OUT} ({CPH_OUT.stat().st_size/1024:.1f} KB)")
    print("  names:", sorted(names))


if __name__ == "__main__":
    build_berlin()
    build_copenhagen()
