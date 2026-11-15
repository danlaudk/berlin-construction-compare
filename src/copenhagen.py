"""Download and parse Copenhagen Municipality (Københavns Kommune) statistics
for dwelling completions, buildings and population by bydel (district), plus a
cross-check against Statistics Denmark's national statbank.

Københavns Kommunes Statistikbank (https://kk.statistikbank.dk) runs on the
legacy "Statbank5" engine (NOT PxWeb / not the api.statbank.dk REST API used
by Statistics Denmark). It has no documented JSON API. The only way to pull
data programmatically is to drive its classic ASP selection-form workflow:

  1. GET  SelectVarVal/Define.asp?MainTable=<table>   -> HTML form with hidden
     V{i}/VS{i}/VP{i} fields (one per table variable) and <select> boxes
     listing each variable's valid option codes (var1, var2, ... varN).
  2. POST SelectVarVal/saveselections.asp with the chosen var{i} values
     (repeated for multi-select) -> redirects to the rendered table view.
  3. The table view embeds a small <FORM action="../selectout/ready.asp?...">
     with a `fileformatid` dropdown (6 = semicolon CSV). POST to it.
  4. That POST redirects to a temp .csv file under .../selectout/../temp/,
     which `requests` follows automatically (redirects are same-host).

The resulting CSV has no header row. Each row looks like:
    "<eliminated dim label>";...;"<row-axis label>";<v1>;<v2>;...;<vN>
Exactly one dimension ends up spread across columns (the one we queried with
several codes) and the *other* queried-with-several-codes dimension is spread
across rows, with its value as the LAST quoted field in the row (either
"Bydel - <name>" or a bare period like "2010"/"2010K4"). All other quoted
fields are "<label> i alt" placeholders for dimensions fixed at their TOT /
single value and are not needed. `_parse_kk_csv` below figures out which
arrangement applies by checking for the "Bydel - " marker, so one parser
handles all three tables used here (KKBOL1, KKBYG1, KKBEF1).

Run as a script to (re)build every file under data/raw/copenhagen/ and
data/processed/:

    uv run python src/copenhagen.py
"""
from __future__ import annotations

import csv
import io
import re
from pathlib import Path
from urllib.parse import urlencode

import pandas as pd
import requests

sys_path_root = Path(__file__).resolve().parent.parent
RAW = sys_path_root / "data" / "raw" / "copenhagen"
PROCESSED = sys_path_root / "data" / "processed"
RAW.mkdir(parents=True, exist_ok=True)
PROCESSED.mkdir(parents=True, exist_ok=True)

KK_BASE = "https://kk.statistikbank.dk/statbank5a"
UA = "berlin-construction-compare/0.1 (data analysis)"

# The 10 official Copenhagen bydele (+ the catch-all "unassigned" bucket),
# with their stable KK statbank area codes (var "omrkk" / "distrikt").
BYDELE: dict[str, str] = {
    "1001": "Indre By",
    "1002": "Østerbro",
    "1003": "Nørrebro",
    "1004": "Vesterbro/Kongens Enghave",
    "1005": "Valby",
    "1006": "Vanløse",
    "1007": "Brønshøj-Husum",
    "1008": "Bispebjerg",
    "1009": "Amager Øst",
    "1010": "Amager Vest",
}
BYDEL_UNKNOWN = {"1099": "Uden for inddeling"}  # excluded from the 10 bydele, kept separately
BYDEL_CODES = list(BYDELE.keys())


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": UA})
    return s


def _hidden(html: str, name: str) -> str:
    m = re.search(rf'NAME="{re.escape(name)}"[^>]*VALUE="([^"]*)"', html, re.IGNORECASE)
    return m.group(1) if m else ""


def kk_download_csv(session: requests.Session, table: str, var_selections: dict[int, list[str]],
                     cache: bool = True) -> str:
    """Run the Statbank5 select -> show table -> export-CSV flow for `table`.

    var_selections maps 1-based variable index -> list of option codes to
    select for that variable (e.g. {1: ["1001", "1002"], 6: ["2025"]}).
    Variables not mentioned default to their total ("TOT").
    Returns the raw semicolon-CSV text (also cached to data/raw/copenhagen/).
    """
    cache_path = RAW / f"kk_{table}.csv"
    if cache and cache_path.exists():
        return cache_path.read_text(encoding="latin-1")

    r = session.get(
        f"{KK_BASE}/SelectVarVal/Define.asp",
        params={"MainTable": table, "PLanguage": "0", "PXSId": "0", "wsid": "cflist"},
        timeout=30,
    )
    r.raise_for_status()
    html = r.content.decode("latin-1")

    antvar = int(_hidden(html, "antvar"))
    subject_code = _hidden(html, "SubjectCode")
    tidrubr = _hidden(html, "tidrubr")
    contents = _hidden(html, "Contents") or "Indhold"
    ff = _hidden(html, "FF") or "20"
    tfrequency = _hidden(html, "tfrequency") or "1"

    data = {
        "TS": f"ShowTable&OldTab=SELECT&SubjectCode={subject_code}&AntVar={antvar}"
              f"&Contents={contents}&tidrubr={tidrubr}",
        "PLanguage": "0", "FF": ff, "OldTab": "SELECT", "SavePXSId": "0",
        "tidrubr": tidrubr, "MainTable": table, "SubTable": "S0",
        "SelCont": "Indhold", "Contents": contents, "antvar": str(antvar),
        "action": "urval", "guest": "-1", "GuestFileSize": "100000", "MaxFileSize": "100000",
        "SubjectCode": subject_code, "boksnr": "", "tfrequency": tfrequency, "Forward": "Forward",
    }
    post_items = list(data.items())
    for i in range(1, antvar + 1):
        post_items.append((f"V{i}", _hidden(html, f"V{i}")))
        post_items.append((f"VS{i}", _hidden(html, f"VS{i}")))
        post_items.append((f"VP{i}", _hidden(html, f"VP{i}")))
    for i in range(1, antvar + 1):
        for v in var_selections.get(i, ["TOT"]):
            post_items.append((f"var{i}", v))

    # The site is ISO-8859-1 and some hidden field *values* (variable codes
    # like "OPFØRELSESÅR") contain accented characters. requests defaults to
    # UTF-8 when urlencoding a plain dict/list body, which corrupts those
    # bytes for this ISO-8859-1 server -> encode the body ourselves.
    body = urlencode(post_items, encoding="latin-1")
    r = session.post(
        f"{KK_BASE}/SelectVarVal/saveselections.asp", data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"}, timeout=30,
    )
    r.raise_for_status()
    view_html = r.content.decode("latin-1")

    m = re.search(r'<FORM ACTION="(\.\./selectout/ready\.asp\?[^"]+)"', view_html)
    if not m:
        raise RuntimeError(f"{table}: could not find the ready.asp export form in the table view")
    ready_action = m.group(1).replace("&amp;", "&")
    main_table_m = re.search(r'NAME="MainTable" value="([^"]+)"', view_html, re.IGNORECASE)
    main_table = main_table_m.group(1) if main_table_m else table

    r = session.post(
        requests.compat.urljoin(r.url, ready_action),
        data={"fileformatid": "6", "Potsize": "160", "MainTable": main_table},  # 6 = semicolon CSV
        timeout=30,
    )
    r.raise_for_status()
    text = r.content.decode("latin-1")
    cache_path.write_text(text, encoding="latin-1")
    return text


_NUMERIC_RE = re.compile(r"^-?\d+(\.\d+)?$")
_MISSING = {"..", ".", "-", ""}


def _parse_kk_csv(text: str, row_codes_in_order: list[str], row_code_to_label: dict[str, str] | None,
                   col_values_in_order: list[str]) -> list[dict]:
    """Parse one Statbank5 semicolon-CSV export into long records.

    One of the two axes we queried with multiple codes ends up as columns (in
    exactly the order we requested them: `col_values_in_order`); the other
    ends up as the row's trailing quoted label, either "Bydel - <name>" (then
    look up the district code by name) or a bare value matched positionally
    against `row_codes_in_order` (same order we requested -> row i gets
    row_codes_in_order[i]). Returns a list of
    {"row": <code or label>, "col": <value>, "value": <float|None>} dicts.
    """
    # The number of trailing data columns is known up front (it's exactly the
    # axis we queried with several codes) -- splitting on that count avoids
    # ambiguity from label fields that happen to look numeric themselves
    # (e.g. a bare year like "2010" used as the row label).
    n_cols = len(col_values_in_order)
    reader = csv.reader(io.StringIO(text), delimiter=";")
    label_to_code = {v: k for k, v in (row_code_to_label or {}).items()}
    out = []
    row_i = 0
    for row in reader:
        row = [f.strip() for f in row]
        if not row or all(f == "" for f in row):
            continue
        if len(row) < n_cols + 1:
            continue
        labels, values = row[:-n_cols], row[-n_cols:]
        if not labels or not values:
            continue
        row_label = labels[-1]
        bydel_m = re.match(r"Bydel - (.+)", row_label)
        if bydel_m:
            row_key = label_to_code.get(bydel_m.group(1), bydel_m.group(1))
        elif row_code_to_label is None:
            # row axis is the "other" dimension (e.g. a year); use the raw label
            row_key = row_label
        else:
            # positional fallback: row i corresponds to row_codes_in_order[i]
            row_key = row_codes_in_order[row_i] if row_i < len(row_codes_in_order) else row_label
        for col_val, raw in zip(col_values_in_order, values):
            num = None if raw in _MISSING else float(raw)
            out.append({"row": row_key, "col": col_val, "value": num})
        row_i += 1
    return out


# --------------------------------------------------------------------------- KKBOL1 (dwellings)
def fetch_completions_kkbol1(session: requests.Session, reference_year: str = "2026") -> pd.DataFrame:
    """KKBOL1: dwellings by distrikt x ejerforhold x ibrugtagningsaar x ... x tid.

    This is a STOCK table (dwellings standing at `reference_year`), broken down
    by the year they were taken into use (ibrugtagningsaar). The count with
    ibrugtagningsaar = Y is the surviving stock built in Y as of
    `reference_year` -- a proxy for completions in year Y, not a true flow
    (demolished dwellings from year Y are not counted). Single years are only
    available in the table from 2010.
    """
    year_codes = {str(y): f"{13 + (y - 2010):02d}" for y in range(2010, 2026)}  # 2010->13 ... 2025->28
    text = kk_download_csv(session, "KKBOL1", {
        1: BYDEL_CODES, 2: ["TOT"], 3: list(year_codes.values()), 4: ["TOT"], 5: ["TOT"],
        6: [reference_year],
    })
    recs = _parse_kk_csv(text, row_codes_in_order=list(year_codes.keys()), row_code_to_label=None,
                          col_values_in_order=BYDEL_CODES)
    df = pd.DataFrame(recs).rename(columns={"row": "year", "col": "district_code"})
    df["year"] = df["year"].astype(int)
    df["district"] = df["district_code"].map(BYDELE)
    df["measure"] = "dwellings_by_commissioning_year (stock, ref. " + reference_year + ")"
    df["source_table"] = "KK statbank KKBOL1"
    return df[["year", "district", "measure", "value", "source_table"]]


# --------------------------------------------------------------------------- KKBYG1 (buildings)
def fetch_buildings_kkbyg1(session: requests.Session, reference_year: str = "2025") -> pd.DataFrame:
    """KKBYG1: buildings & building floor area by distrikt x opfoerelsesaar x ... x enhed x tid.

    Same stock-by-construction-year caveat as KKBOL1. enhed=01 is number of
    buildings, enhed=02 is residential floor area (boligareal, m2). Table only
    has single years through 2024 (reference max 2025).
    """
    year_codes = {str(y): f"{13 + (y - 2010):02d}" for y in range(2010, 2025)}  # 2010->13 ... 2024->27
    frames = []
    for enhed_code, measure in [("01", "buildings_by_construction_year (stock)"),
                                 ("02", "residential_floor_area_m2_by_construction_year (stock)")]:
        text = kk_download_csv(session, "KKBYG1", {
            1: BYDEL_CODES, 2: ["TOT"], 3: list(year_codes.values()), 4: ["TOT"], 5: ["TOT"],
            6: [enhed_code], 7: [reference_year],
        }, cache=False)
        # cache separately per enhed since the generic cache key is table-only
        (RAW / f"kk_KKBYG1_enhed{enhed_code}.csv").write_text(text, encoding="latin-1")
        recs = _parse_kk_csv(text, row_codes_in_order=list(year_codes.keys()), row_code_to_label=None,
                              col_values_in_order=BYDEL_CODES)
        df = pd.DataFrame(recs).rename(columns={"row": "year", "col": "district_code"})
        df["year"] = df["year"].astype(int)
        df["district"] = df["district_code"].map(BYDELE)
        df["measure"] = measure + f", ref. {reference_year}"
        df["source_table"] = "KK statbank KKBYG1"
        frames.append(df[["year", "district", "measure", "value", "source_table"]])
    return pd.concat(frames, ignore_index=True)


# --------------------------------------------------------------------------- KKBEF1 (population)
def fetch_population_kkbef1(session: requests.Session, years: range = range(2010, 2026),
                             quarter: str = "K4") -> pd.DataFrame:
    """KKBEF1: population by distrikt x koen x alder x civilstand x tid (quarterly)."""
    quarters = [f"{y}{quarter}" for y in years]
    text = kk_download_csv(session, "KKBEF1", {
        1: BYDEL_CODES, 2: ["TOT"], 3: ["TOT"], 4: ["TOT"], 5: quarters,
    })
    recs = _parse_kk_csv(text, row_codes_in_order=BYDEL_CODES, row_code_to_label=BYDELE,
                          col_values_in_order=quarters)
    df = pd.DataFrame(recs).rename(columns={"row": "district_code", "col": "period"})
    df["year"] = df["period"].str.slice(0, 4).astype(int)
    df["district"] = df["district_code"].map(BYDELE)
    df["source"] = f"KK statbank KKBEF1 ({quarter})"
    return df[["year", "district", "value", "source"]].rename(columns={"value": "population"})


# --------------------------------------------------------------------------- DST cross-check
def fetch_dst_bygv22_completions(years: range = range(2010, 2026)) -> pd.DataFrame:
    """Statistics Denmark BYGV22: new dwellings completed, by municipality.

    Copenhagen = municipality code 101. TAL=46 selects the "dwellings
    (number)" unit, BYGGESAG=1 restricts to new buildings (excludes
    extensions/conversions, which can also add dwellings), and ANVENDELSE is
    summed over the residential use codes 110-190.
    """
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from sources import dst_data  # local import to avoid a hard dependency at module load time

    quarters = [f"{y}K{q}" for y in years for q in range(1, 5)]
    residential_uses = ["110", "120", "130", "140", "150", "160", "190"]
    out_path = RAW / "dst_BYGV22.csv"
    df = dst_data("BYGV22", {
        "OMRÅDE": ["101"], "TAL": ["46"], "BYGGESAG": ["1"],
        "ANVENDELSE": residential_uses, "Tid": quarters,
    }, cache=False)
    df.to_csv(out_path, index=False, sep=";")
    val_col = df.columns[-1]
    df["year"] = df["TID"].astype(str).str.slice(0, 4).astype(int)
    yearly = df.groupby("year")[val_col].sum().reset_index().rename(columns={val_col: "dwellings_completed"})
    yearly["source_table"] = "DST BYGV22 (municipality 101, new buildings, residential uses)"
    return yearly


def main() -> None:
    session = _session()

    print("Fetching KKBOL1 (dwellings stock by commissioning year) ...")
    completions = fetch_completions_kkbol1(session)

    print("Fetching KKBYG1 (buildings & floor area by construction year) ...")
    buildings = fetch_buildings_kkbyg1(session)

    all_completions = pd.concat([completions, buildings], ignore_index=True)
    all_completions.to_csv(PROCESSED / "copenhagen_completions_by_district.csv", index=False)

    wide = (completions[completions["measure"].str.startswith("dwellings")]
            .pivot_table(index="year", columns="district", values="value", aggfunc="sum")
            .reindex(columns=list(BYDELE.values())))
    wide.to_csv(PROCESSED / "copenhagen_completions_wide.csv")

    print("Fetching KKBEF1 (population by district) ...")
    population = fetch_population_kkbef1(session)
    population.to_csv(PROCESSED / "copenhagen_population_by_district.csv", index=False)

    print("Fetching DST BYGV22 (municipality-level cross-check) ...")
    try:
        dst_check = fetch_dst_bygv22_completions()
        dst_check.to_csv(PROCESSED / "copenhagen_dst_bygv22_crosscheck.csv", index=False)
    except Exception as exc:  # pragma: no cover
        print(f"  DST cross-check failed: {exc}")
        dst_check = None

    print("\n--- Dwelling 'completions' (KKBOL1 stock-by-year) totals per year ---")
    totals = (completions[completions["measure"].str.startswith("dwellings")]
              .groupby("year")["value"].sum())
    print(totals.to_string())

    if dst_check is not None:
        print("\n--- DST BYGV22 Copenhagen municipality totals per year ---")
        print(dst_check.set_index("year")["dwellings_completed"].to_string())

    print("\nWrote:")
    for p in [
        PROCESSED / "copenhagen_completions_by_district.csv",
        PROCESSED / "copenhagen_completions_wide.csv",
        PROCESSED / "copenhagen_population_by_district.csv",
        PROCESSED / "copenhagen_dst_bygv22_crosscheck.csv",
    ]:
        if p.exists():
            print(f"  {p}")


if __name__ == "__main__":
    main()
