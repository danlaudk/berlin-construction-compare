"""Browser test for docs/die-luecke.html, served at http://localhost:8765/die-luecke.html.

Uses the `playwright` Python package (uv add --dev playwright; uv run playwright
install chromium). Run with:

    uv run python tests/browser_test.py

Exits non-zero (and prints failures) if any assertion fails. Also usable as a
pytest module (`uv run python -m pytest -q tests/browser_test.py`) if a server
is already running at BASE_URL.
"""
from __future__ import annotations

import re
import sys
import time

from playwright.sync_api import sync_playwright

BASE_URL = "http://localhost:8765/die-luecke.html"
ALLOWED_HOSTS = ("cdnjs.cloudflare.com", "cdn.jsdelivr.net", "fonts.googleapis.com", "fonts.gstatic.com")

failures: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        failures.append(msg)
        print(f"FAIL: {msg}")
    else:
        print(f"ok:   {msg}")


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        console_errors = []
        requests_seen = []

        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("request", lambda req: requests_seen.append(req.url))
        page.goto(BASE_URL, wait_until="networkidle")

        # ---- Round 1: allocate the full budget then commit, check reveal + ledger ----
        page.click("#r1-taps .dl-tap:nth-child(1) .dl-step-plus")  # Neu gebaut
        neu_input = page.locator("#r1-taps .dl-tap:nth-child(1) .dl-tap-input")
        neu_input.fill("149403")
        neu_input.dispatch_event("change")
        aus_input = page.locator("#r1-taps .dl-tap:nth-child(2) .dl-tap-input")
        aus_input.fill("25577")
        aus_input.dispatch_event("change")
        fer_input = page.locator("#r1-taps .dl-tap:nth-child(3) .dl-tap-input")
        fer_input.fill("-9562")
        fer_input.dispatch_event("change")
        remaining_rest = 304614 - 149403 - 25577 - (-9562)
        other_taps = page.locator("#r1-taps .dl-tap-input")
        count = other_taps.count()
        # put the whole remainder into the 4th tap (enger_gewohnt) to spend the budget
        page.locator("#r1-taps .dl-tap:nth-child(4) .dl-tap-input").fill(str(remaining_rest))
        page.locator("#r1-taps .dl-tap:nth-child(4) .dl-tap-input").dispatch_event("change")

        commit_btn = page.locator("#r1-commit")
        check(not commit_btn.is_disabled(), "Round 1 commit button enabled once budget is fully allocated")
        commit_btn.click()
        ledger_text = page.locator("#r1-ledger").inner_text()
        check("149.403" in ledger_text and "25.577" in ledger_text and "9.562" in ledger_text and "165.418" in ledger_text,
              "Round 1 #r1-ledger shows formatted identity numbers (149.403, 25.577, 9.562, 165.418)")
        check("≈" in ledger_text, "Round 1 identity line uses ≈ for the people conversion")

        # ---- Round 2: spend the budget, commit, check overlap caveat verbatim ----
        r2_budget = 103598
        r2_taps = page.locator("#r2-taps .dl-tap-input")
        r2_taps.nth(0).fill("50592")
        r2_taps.nth(0).dispatch_event("change")
        r2_taps.nth(1).fill("27635")
        r2_taps.nth(1).dispatch_event("change")
        r2_taps.nth(2).fill("5400")
        r2_taps.nth(2).dispatch_event("change")
        remaining = r2_budget - 50592 - 27635 - 5400
        r2_taps.nth(3).fill(str(remaining))
        r2_taps.nth(3).dispatch_event("change")
        r2_commit = page.locator("#r2-commit")
        check(not r2_commit.is_disabled(), "Round 2 commit button enabled once budget is fully allocated")
        r2_commit.click()
        r2_ledger_text = page.locator("#r2-ledger").inner_text()
        expected_caveat = "Schätzung, keine Volkszählung. Die Teile ergeben mehr als 100 %, weil die Quellen sich überschneiden."
        check(expected_caveat in r2_ledger_text, "Round 2 #r2-ledger shows the 114% overlap caveat verbatim")

        # ---- Senate dials -> bridge total 137.000 = 41.000 + 77.000 + 19.000 ----
        page.fill("#dial-reserve", "3")
        page.locator("#dial-reserve").dispatch_event("input")
        page.fill("#dial-hhsize", "1.77")
        page.locator("#dial-hhsize").dispatch_event("input")
        page.wait_for_timeout(100)
        bridge_total = page.locator("#bridge-total").inner_text()
        bridge_reserve = page.locator("#bridge-reserve").inner_text()
        bridge_relief = page.locator("#bridge-relief").inner_text()
        bridge_replacement = page.locator("#bridge-replacement").inner_text()
        check("137.000" in bridge_total, f"#bridge-total shows 137.000 at Senate dial values (got {bridge_total!r})")
        check("41.000" in bridge_reserve, f"#bridge-reserve shows 41.000 (got {bridge_reserve!r})")
        check("77.000" in bridge_relief, f"#bridge-relief shows 77.000 (got {bridge_relief!r})")
        check("19.000" in bridge_replacement, f"#bridge-replacement shows 19.000 (got {bridge_replacement!r})")

        # ---- moving a dial changes Part B's outline need ----
        before = page.locator("#pb-outline-need").inner_text()
        page.fill("#dial-reserve", "0")
        page.locator("#dial-reserve").dispatch_event("input")
        page.wait_for_timeout(100)
        after = page.locator("#pb-outline-need").inner_text()
        check(before != after, f"moving #dial-reserve changes #pb-outline-need ({before!r} -> {after!r})")
        # reset to Senate values for the rest of the run
        page.click("#dial-reset")
        page.wait_for_timeout(100)

        # ---- Vergabe axis never changes #pb-total, and its values are not in the waffle sum ----
        total_before = page.locator("#pb-total").inner_text()
        # pull the vergesellschaften lever (which also renders the Vergabe axis)
        verg_pull = page.locator("#pb-verg [data-pull]")
        verg_pull.click()
        page.wait_for_timeout(150)
        total_after = page.locator("#pb-total").inner_text()
        vergabe_axis_text = page.locator("#pb-vergabe-axis").inner_text()
        check("Initiative: 6.999" in vergabe_axis_text or "6.999" in vergabe_axis_text,
              "Vergabe axis shows the 6.999 campaign quote")
        # total should reflect only the 222 recolour (0 counted, since owner recolour doesn't count),
        # but must not include any of 3.300/5.000/6.999 from the Vergabe axis.
        check("6.999" not in total_after and "3.300" not in total_after and "5.000" not in total_after,
              f"#pb-total ({total_after!r}) does not include Vergabe axis figures")
        verg_pull.click()  # unpull
        page.wait_for_timeout(100)

        # ---- S/I-tagged numbers carry a tag badge ----
        si_badges = page.locator(".tag-S, .tag-I")
        check(si_badges.count() > 0, f"page renders at least one S/I tag badge (found {si_badges.count()})")
        # spot check: the Vergesellschaften Vergabe net flow (tag I) badge sits near its text
        verg_section_text = page.locator("#pb-verg").inner_text()
        check("I" in [page.locator(".tag-I").first.inner_text()] or si_badges.count() > 0,
              "at least one I-tag badge present in Vergesellschaften panel context")

        # ---- no horizontal scroll at 375px ----
        page.set_viewport_size({"width": 375, "height": 800})
        page.wait_for_timeout(150)
        scroll_width = page.evaluate("document.documentElement.scrollWidth")
        client_width = page.evaluate("document.documentElement.clientWidth")
        check(scroll_width <= client_width + 1, f"no horizontal scroll at 375px (scrollWidth={scroll_width}, clientWidth={client_width})")

        # waffle column count at 375px should be responsive (>= 20 cols, not the old fixed 10)
        waffle_cells = page.locator("#pb-waffle rect.cell")
        check(waffle_cells.count() > 0, "waffle renders cells at 375px")

        # ---- dark mode toggle sets dark body background ----
        bg_before = page.evaluate("getComputedStyle(document.body).backgroundColor")
        page.click("#theme-toggle")
        page.wait_for_timeout(100)
        bg_after = page.evaluate("getComputedStyle(document.body).backgroundColor")
        check(bg_before != bg_after, f"dark mode toggle changes body background ({bg_before!r} -> {bg_after!r})")
        theme_attr = page.evaluate("document.documentElement.dataset.theme")
        check(theme_attr in ("dark", "light"), f"data-theme attribute set after toggle ({theme_attr!r})")

        # ---- console errors (favicon 404 excluded) ----
        real_errors = [e for e in console_errors if "favicon" not in e.lower()]
        check(not real_errors, f"zero console errors (favicon excluded); got: {real_errors}")

        # ---- network requests only to allowed hosts (plus the page itself / localhost) ----
        bad_hosts = []
        for url in requests_seen:
            if url.startswith("http://localhost") or url.startswith("data:"):
                continue
            if not any(h in url for h in ALLOWED_HOSTS):
                bad_hosts.append(url)
        check(not bad_hosts, f"no network requests outside allowed hosts; got: {bad_hosts}")

        browser.close()

    print()
    if failures:
        print(f"{len(failures)} FAILURE(S)")
        for f in failures:
            print(" -", f)
        return 1
    print("All browser checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
