import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import build_page  # noqa: E402

ALLOWED = ("https://cdnjs.cloudflare.com/", "https://cdn.jsdelivr.net/npm/",
           "https://fonts.googleapis.com", "https://fonts.gstatic.com", "http://www.w3.org/")


def test_build(tmp_path):
    out = build_page.build(tmp_path / "page.html")
    text = out.read_text(encoding="utf-8")
    assert "window.DATA = {" in text
    assert out.stat().st_size < 16 * 1024 * 1024
    bad = [u for u in re.findall(r"https?://[^\s\"'<>)`]+", text) if not u.startswith(ALLOWED)]
    assert not bad, bad
    assert '<html lang="de">' in text
    assert "/*__" not in text
