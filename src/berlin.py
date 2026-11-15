"""Download and parse Berlin building-completions (F II 2) and population (A I 5) data.

Source: Amt für Statistik Berlin-Brandenburg, Statistische Bibliothek
(https://www.statistischebibliothek.de), series "Baufertigstellungen, Bauüberhang
und Bauabgang in Berlin" (F II 2) and Einwohnerregisterstatistik (A I 5) /
Berlin Open Data (daten.berlin.de).

Run as a script to (re)download everything and rebuild the processed CSVs:
    uv run python src/berlin.py
"""
from __future__ import annotations

import re
import time
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "berlin"
PROCESSED = ROOT / "data" / "processed"
RAW.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
HEADERS = {"User-Agent": UA}
LIB = "https://www.statistischebibliothek.de"

# --------------------------------------------------------------------------- districts
DISTRICTS = [
    "Mitte", "Friedrichshain-Kreuzberg", "Pankow", "Charlottenburg-Wilmersdorf",
    "Spandau", "Steglitz-Zehlendorf", "Tempelhof-Schöneberg", "Neukölln",
    "Treptow-Köpenick", "Marzahn-Hellersdorf", "Lichtenberg", "Reinickendorf",
]

# Issue (BBHeft_mods) ids for report years 2010-2025, scraped from the series page
# https://www.statistischebibliothek.de/mir/receive/BBSerie_mods_00000448
HEFT_IDS = {
    2025: "BBHeft_mods_00050158",
    2024: "BBHeft_mods_00049589",
    2023: "BBHeft_mods_00049037",
    2022: "BBHeft_mods_00046964",
    2021: "BBHeft_mods_00044533",
    2020: "BBHeft_mods_00042819",
    2019: "BBHeft_mods_00041829",
    2018: "BBHeft_mods_00037224",
    2017: "BBHeft_mods_00033801",
    2016: "BBHeft_mods_00028220",
    2015: "BBHeft_mods_00021634",
    2014: "BBHeft_mods_00014874",
    2013: "BBHeft_mods_00008343",
    2012: "BBHeft_mods_00004057",
    2011: "BBHeft_mods_00004053",
    2010: "BBHeft_mods_00021638",
}

# Population series: Statistischer Bericht A I 5 "Einwohnerregisterstatistik Berlin"
# (series BBSerie_mods_00000260). The ",02" issue of each report year is the
# 31 December snapshot used here (population as of year-end, matching the
# completions-during-year series above).
POP_HEFT_IDS = {
    2010: "BBHeft_mods_00001569",
    2011: "BBHeft_mods_00001577",
    2012: "BBHeft_mods_00001538",
    2013: "BBHeft_mods_00007522",
    2014: "BBHeft_mods_00012622",
    2015: "BBHeft_mods_00018984",
    2016: "BBHeft_mods_00027544",
    2017: "BBHeft_mods_00032403",
    2018: "BBHeft_mods_00036199",
    2019: "BBHeft_mods_00040823",
    2020: "BBHeft_mods_00042477",
    2021: "BBHeft_mods_00044336",
    2022: "BBHeft_mods_00046167",
    2023: "BBHeft_mods_00048831",
    2024: "BBHeft_mods_00049422",
    2025: "BBHeft_mods_00050002",
}


def _fetch_html(obj_id: str) -> str:
    url = f"{LIB}/mir/receive/{obj_id}"
    r = requests.get(url, headers=HEADERS, timeout=60, allow_redirects=True)
    r.raise_for_status()
    return r.text


def find_derivate_files(html: str) -> list[tuple[str, str]]:
    """Return list of (derivate_id, filename) pairs found in the page, in document order."""
    pairs = re.findall(r'data-mainDoc="([^"]*)" data-deriID="([^"]*)"', html)
    return [(deri_id, fname) for fname, deri_id in pairs]


def download_excel_for_year(year: int, obj_id: str, prefix: str, retries: int = 3) -> Path | None:
    """Find and download the .xlsx/.xls file for a given report-year issue. Returns local path or None."""
    existing = glob.glob(str(RAW / f"{prefix}_{year}.*"))
    if existing:
        return Path(existing[0])
    html = _fetch_html(obj_id)
    files = find_derivate_files(html)  # [(deriID, filename), ...]
    xls_candidates = [(d, f) for d, f in files if f.lower().endswith((".xlsx", ".xls"))]
    if not xls_candidates:
        print(f"  [{year}] no Excel derivate found")
        return None
    deri_id, fname = xls_candidates[0]
    ext = Path(fname).suffix
    url = f"{LIB}/mir/servlets/MCRFileNodeServlet/{deri_id}/{fname}"
    out = RAW / f"{prefix}_{year}{ext}"
    for attempt in range(retries):
        try:
            r = requests.get(url, headers=HEADERS, timeout=120)
            r.raise_for_status()
            out.write_bytes(r.content)
            print(f"  [{year}] downloaded {fname} -> {out.name} ({len(r.content)} bytes)")
            return out
        except requests.RequestException as e:
            print(f"  [{year}] attempt {attempt+1} failed: {e}")
            time.sleep(2)
    return None


def download_all_completions() -> dict[int, Path]:
    out = {}
    for year, obj_id in sorted(HEFT_IDS.items()):
        p = download_excel_for_year(year, obj_id, prefix="berlin_F2")
        if p:
            out[year] = p
        time.sleep(0.5)
    return out


def download_all_population() -> dict[int, Path]:
    out = {}
    for year, obj_id in sorted(POP_HEFT_IDS.items()):
        p = download_excel_for_year(year, obj_id, prefix="berlin_pop")
        if p:
            out[year] = p
        time.sleep(0.5)
    return out


# --------------------------------------------------------------------------- parsing
import glob
import re as _re
import unicodedata

TOTAL_TITLE_RE = _re.compile(
    r"Baufertigstellungen im Wohn- und Nichtwohnbau einschließlich Baumaßnahmen an\s*\n?\s*bestehenden Gebäuden (in Berlin )?\d{4} nach Bezirken"
)
NEW_RES_TITLE_RE = _re.compile(r"Baufertigstellungen neuer Wohngebäude (in Berlin )?\d{4} nach Bezirken")


def _norm(s) -> str:
    if not isinstance(s, str):
        return ""
    s = s.replace("\n", " ").replace("-", "")
    s = unicodedata.normalize("NFKC", s)
    return s.strip().lower()


def _find_block(df: pd.DataFrame, title_re: _re.Pattern) -> int | None:
    for i in range(len(df)):
        v = df.iat[i, 0]
        if isinstance(v, str) and title_re.search(v.replace("\n", " ")):
            return i
    return None


def _extract_block(df: pd.DataFrame, title_row: int) -> dict[str, float] | None:
    """Given the row index of a block's title, find the Bezirk header, the 12
    district rows, the Berlin total row, and the dwellings/buildings/floor-area
    columns. Returns a dict of measure -> Berlin-total-row value plus a
    'by_district' dict, or None if the shape doesn't match."""
    n = len(df)
    # find header row ("Bezirk" in col 0)
    header_row = None
    for i in range(title_row + 1, min(title_row + 8, n)):
        if _norm(df.iat[i, 0]) == "bezirk":
            header_row = i
            break
    if header_row is None:
        return None
    # find first district row
    first_district_row = None
    for i in range(header_row + 1, min(header_row + 12, n)):
        if _norm(df.iat[i, 0]) == _norm(DISTRICTS[0]):
            first_district_row = i
            break
    if first_district_row is None:
        return None
    berlin_row = first_district_row + len(DISTRICTS)
    if _norm(df.iat[berlin_row, 0]) != "berlin":
        return None

    ncols = df.shape[1]
    combined_headers = []
    for c in range(ncols):
        text = "".join(_norm(df.iat[r, c]) for r in range(header_row + 1, first_district_row))
        combined_headers.append(text.replace(" ", ""))

    gebaude_col = next((c for c in range(1, ncols) if "gebäude" in combined_headers[c]), None)
    wohnungen_col = next(
        (c for c in range(1, ncols) if "wohnungen" in combined_headers[c] and "insgesamt" in combined_headers[c]),
        None,
    )
    wohnflaeche_col = next((c for c in range(1, ncols) if "wohnfläche" in combined_headers[c]), None)

    by_district = {}
    for off, district in enumerate(DISTRICTS):
        row = first_district_row + off
        rec = {}
        if gebaude_col is not None:
            rec["buildings"] = df.iat[row, gebaude_col]
        if wohnungen_col is not None:
            rec["dwellings"] = df.iat[row, wohnungen_col]
        if wohnflaeche_col is not None:
            rec["floor_area"] = df.iat[row, wohnflaeche_col]
        by_district[district] = rec

    berlin_total = {}
    if gebaude_col is not None:
        berlin_total["buildings"] = df.iat[berlin_row, gebaude_col]
    if wohnungen_col is not None:
        berlin_total["dwellings"] = df.iat[berlin_row, wohnungen_col]
    if wohnflaeche_col is not None:
        berlin_total["floor_area"] = df.iat[berlin_row, wohnflaeche_col]

    return {"by_district": by_district, "berlin_total": berlin_total}


def parse_year(path: Path, year: int) -> list[dict]:
    """Parse one workbook into tidy long records: year, district, measure, value, source_file."""
    xl = pd.ExcelFile(path)
    records = []
    found_total = found_new = False
    for sheet in xl.sheet_names:
        df = xl.parse(sheet, header=None)
        if not found_total:
            t = _find_block(df, TOTAL_TITLE_RE)
            if t is not None:
                block = _extract_block(df, t)
                if block:
                    found_total = True
                    for d, rec in block["by_district"].items():
                        if "dwellings" in rec:
                            records.append({"year": year, "district": d, "measure": "dwellings_total",
                                             "value": rec["dwellings"], "source_file": path.name})
                        if "buildings" in rec:
                            records.append({"year": year, "district": d, "measure": "buildings_total",
                                             "value": rec["buildings"], "source_file": path.name})
                        if "floor_area" in rec:
                            records.append({"year": year, "district": d, "measure": "floor_area_total_m2",
                                             "value": rec["floor_area"] * 100 if pd.notna(rec["floor_area"]) else rec["floor_area"],
                                             "source_file": path.name})
        if not found_new:
            t = _find_block(df, NEW_RES_TITLE_RE)
            if t is not None:
                block = _extract_block(df, t)
                if block:
                    found_new = True
                    for d, rec in block["by_district"].items():
                        if "dwellings" in rec:
                            records.append({"year": year, "district": d, "measure": "dwellings_new_residential",
                                             "value": rec["dwellings"], "source_file": path.name})
                        if "buildings" in rec:
                            records.append({"year": year, "district": d, "measure": "buildings_new_residential",
                                             "value": rec["buildings"], "source_file": path.name})
                        if "floor_area" in rec:
                            records.append({"year": year, "district": d, "measure": "floor_area_new_residential_m2",
                                             "value": rec["floor_area"] * 100 if pd.notna(rec["floor_area"]) else rec["floor_area"],
                                             "source_file": path.name})
        if found_total and found_new:
            break
    if not found_total:
        print(f"  [{year}] WARNING: 'total completions by Bezirk' block not found")
    if not found_new:
        print(f"  [{year}] WARNING: 'new residential by Bezirk' block not found")
    return records


def build_completions_dataset() -> pd.DataFrame:
    all_records = []
    for year in sorted(HEFT_IDS):
        matches = glob.glob(str(RAW / f"berlin_F2_{year}.*"))
        if not matches:
            print(f"  [{year}] no raw file found, skipping")
            continue
        path = Path(matches[0])
        recs = parse_year(path, year)
        all_records.extend(recs)
        berlin_total = sum(r["value"] for r in recs if r["measure"] == "dwellings_total")
        print(f"  [{year}] {path.name}: Berlin total dwellings_total = {berlin_total:,.0f}")
    long_df = pd.DataFrame(all_records)
    long_df.to_csv(PROCESSED / "berlin_completions_by_district.csv", index=False)

    wide = (
        long_df[long_df.measure == "dwellings_total"]
        .pivot(index="year", columns="district", values="value")
        .reindex(columns=DISTRICTS)
    )
    wide["Berlin"] = wide.sum(axis=1)
    wide.to_csv(PROCESSED / "berlin_completions_wide.csv")
    return long_df


# --------------------------------------------------------------------------- population
POP_TITLE_RE = _re.compile(
    r"Einwohner(innen und Einwohner|\s+am Ort der Hauptwohnung) in Berlin seit \d{4} nach Bezirken"
)


def _match_stichtag(cell, year: int) -> bool:
    try:
        ts = pd.to_datetime(cell)
    except (ValueError, TypeError):
        return False
    return ts.year == year and ts.month == 12 and ts.day == 31


def parse_population_year(path: Path, year: int) -> list[dict]:
    """Parse one A I 5 workbook: find the 'Einwohner ... seit YYYY nach Bezirken'
    time-series table, take its 'insgesamt' (or only) sub-block, and pull out the
    row for 31 December of the report year."""
    xl = pd.ExcelFile(path)
    for sheet in xl.sheet_names:
        df = xl.parse(sheet, header=None)
        title_row = _find_block(df, POP_TITLE_RE)
        if title_row is None:
            continue
        # header row with "Stichtag" / "Berlin" / district names
        header_row = None
        for i in range(title_row + 1, min(title_row + 6, len(df))):
            if _norm(df.iat[i, 0]) == "stichtag":
                header_row = i
                break
        if header_row is None:
            continue
        # prefer the "insgesamt" sub-block if the table is split by nationality;
        # otherwise fall back to the single "anzahl" block.
        insgesamt_row = None
        anzahl_row = None
        for i in range(header_row + 1, min(header_row + 60, len(df))):
            v = _norm(df.iat[i, 1])
            if v == "insgesamt" and insgesamt_row is None:
                insgesamt_row = i
            elif v == "anzahl" and anzahl_row is None:
                anzahl_row = i
            # stop scanning once we hit the next numbered table title
            v0 = df.iat[i, 0]
            if isinstance(v0, str) and _re.match(r"^\d+\s+\S", v0) and i > header_row + 3:
                break
        block_start = insgesamt_row if insgesamt_row is not None else anzahl_row
        if block_start is None:
            continue
        for i in range(block_start + 1, min(block_start + 40, len(df))):
            if _match_stichtag(df.iat[i, 0], year):
                records = []
                for off, district in enumerate(DISTRICTS):
                    col = 2 + off
                    records.append({
                        "year": year, "district": district, "population": df.iat[i, col],
                        "source": path.name,
                    })
                return records
    print(f"  [{year}] WARNING: population-by-Bezirk table/row not found")
    return []


def build_population_dataset() -> pd.DataFrame:
    all_records = []
    for year in sorted(POP_HEFT_IDS):
        matches = glob.glob(str(RAW / f"berlin_pop_{year}.*"))
        if not matches:
            print(f"  [{year}] no raw file found, skipping")
            continue
        path = Path(matches[0])
        recs = parse_population_year(path, year)
        all_records.extend(recs)
        total = sum(r["population"] for r in recs)
        print(f"  [{year}] {path.name}: Berlin total population = {total:,.0f}")
    df = pd.DataFrame(all_records)
    df.to_csv(PROCESSED / "berlin_population_by_district.csv", index=False)
    return df


if __name__ == "__main__":
    print("Downloading completions workbooks...")
    download_all_completions()
    print("Parsing completions by district...")
    build_completions_dataset()
    print("Downloading population workbooks...")
    download_all_population()
    print("Parsing population by district...")
    build_population_dataset()
