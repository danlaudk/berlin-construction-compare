"""Build docs/die-luecke.html: one self-contained page with CSS, JS and data inlined.

Usage: uv run python src/build_page.py [--out PATH]
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE = ROOT / "src" / "page"
PROC = ROOT / "data" / "processed"
OUT = ROOT / "docs" / "index.html"
SCRIPTS = ["app.js", "partA.js", "partB.js"]  # order matters: app.js defines window.DL
MAX_BYTES = 16 * 1024 * 1024


def _num(v: str):
    try:
        f = float(v)
        return int(f) if f.is_integer() and "." not in v else f
    except (TypeError, ValueError):
        return v if v != "" else None


def load_data() -> dict:
    data: dict = {"panel": [], "levers": {}, "warnings": []}
    panel = PROC / "berlin_panel.csv"
    if panel.exists():
        with panel.open(newline="", encoding="utf-8") as fh:
            data["panel"] = [{k: _num(v) for k, v in row.items()} for row in csv.DictReader(fh)]
    else:
        data["warnings"].append("berlin_panel.csv missing")
    levers = PROC / "levers.json"
    if levers.exists():
        data["levers"] = json.loads(levers.read_text(encoding="utf-8"))
    else:
        data["warnings"].append("levers.json missing")
    return data


def build(out: Path = OUT) -> Path:
    html = (PAGE / "template.html").read_text(encoding="utf-8")
    css = (PAGE / "style.css").read_text(encoding="utf-8")
    js = []
    for name in SCRIPTS:
        p = PAGE / name
        if not p.exists():
            p.write_text(f"// {name} stub\n", encoding="utf-8")
        js.append(f"/* ---- {name} ---- */\n" + p.read_text(encoding="utf-8"))
    data = load_data()
    for w in data["warnings"]:
        print(f"WARNING: {w}; building with empty placeholder", file=sys.stderr)
    # escape '</' so inlined JSON cannot close the script tag
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = (
        html.replace("/*__STYLE__*/", css)
        .replace("/*__DATA__*/", f"window.DATA = {payload};")
        .replace("/*__SCRIPTS__*/", "\n".join(js).replace("</script", "<\\/script"))
    )
    size = len(page.encode("utf-8"))
    if size > MAX_BYTES:
        raise SystemExit(f"page is {size} bytes, over the 16 MB limit")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out} ({size / 1024:.1f} KB)")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=OUT)
    build(ap.parse_args().out)
