"""Thin clients for the two open data sources used in this project.

- Statistics Denmark (DST) StatBank API: https://api.statbank.dk/v1
- Berlin Open Data (CKAN):              https://datenregister.berlin.de/api/3
"""
from __future__ import annotations

import io
from pathlib import Path

import pandas as pd
import requests
from ckanapi import RemoteCKAN

RAW = Path(__file__).resolve().parent.parent / "data" / "raw"
DST = "https://api.statbank.dk/v1"
BERLIN_CKAN = "https://datenregister.berlin.de"
UA = "berlin-construction-compare/0.1 (data analysis)"


# ---------------------------------------------------------------- Statistics Denmark
def dst_subjects(subjects: list[str] | None = None, lang: str = "en") -> pd.DataFrame:
    """List subject tree nodes. Pass ids to drill down (e.g. ["3463"] for Construction, ["20214"] for Construction activity)."""
    body = {"lang": lang, "format": "JSON", "includeTables": True}
    if subjects:
        body["subjects"] = subjects
    r = requests.post(f"{DST}/subjects", json=body, timeout=60)
    r.raise_for_status()
    return pd.json_normalize(r.json(), record_path=None)


def dst_tables(subjects: list[str] | None = None, lang: str = "en") -> pd.DataFrame:
    """List available tables, optionally restricted to subject ids."""
    body = {"lang": lang, "format": "JSON"}
    if subjects:
        body["subjects"] = subjects
    r = requests.post(f"{DST}/tables", json=body, timeout=60)
    r.raise_for_status()
    return pd.DataFrame(r.json())


def dst_tableinfo(table: str, lang: str = "en") -> dict:
    """Metadata for one table: variables and their allowed values."""
    r = requests.post(f"{DST}/tableinfo", json={"table": table, "lang": lang, "format": "JSON"}, timeout=60)
    r.raise_for_status()
    return r.json()


def dst_data(table: str, variables: dict[str, list[str]] | None = None, lang: str = "en",
             cache: bool = True) -> pd.DataFrame:
    """Download a table as a tidy DataFrame. variables={"OMRÅDE": ["*"], "Tid": ["*"]} etc.
    Omitted variables are eliminated (summed) by the API if possible."""
    out = RAW / f"dst_{table}.csv"
    if cache and out.exists():
        return pd.read_csv(out, sep=";")
    body = {"table": table, "lang": lang, "format": "CSV", "valuePresentation": "CodeAndValue"}
    if variables:
        body["variables"] = [{"code": k, "values": v} for k, v in variables.items()]
    r = requests.post(f"{DST}/data", json=body, timeout=300)
    r.raise_for_status()
    out.write_text(r.text, encoding="utf-8")
    return pd.read_csv(io.StringIO(r.text), sep=";")


# ---------------------------------------------------------------- Berlin Open Data
def berlin_ckan() -> RemoteCKAN:
    return RemoteCKAN(BERLIN_CKAN, user_agent=UA)


def berlin_search(query: str, rows: int = 50) -> pd.DataFrame:
    """Search datasets; one row per dataset with its resource formats and URLs."""
    res = berlin_ckan().action.package_search(q=query, rows=rows)
    records = []
    for p in res["results"]:
        for rsrc in p.get("resources", []):
            records.append({
                "dataset": p["name"], "title": p.get("title"),
                "org": (p.get("organization") or {}).get("title"),
                "format": rsrc.get("format"), "resource_name": rsrc.get("name"),
                "url": rsrc.get("url"), "modified": p.get("metadata_modified"),
            })
    return pd.DataFrame(records)


def berlin_download(url: str, name: str | None = None, cache: bool = True) -> Path:
    """Fetch a resource URL into data/raw and return the local path."""
    name = name or url.rsplit("/", 1)[-1]
    out = RAW / f"berlin_{name}"
    if cache and out.exists():
        return out
    r = requests.get(url, headers={"User-Agent": UA}, timeout=300)
    r.raise_for_status()
    out.write_bytes(r.content)
    return out
