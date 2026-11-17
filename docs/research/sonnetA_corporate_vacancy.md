# Corporate-landlord vacancy data for Berlin "Vergesellschaftung" lever

Research for: testing the claim that expropriating large landlords (≥3,000 flats, ~222,000 flats)
would release meaningful hidden housing capacity (vacancy, modernisation-holds, commercial misuse,
unbuilt potential), vs. treating Vergesellschaftung as a pure zero-net-new-dwellings ownership transfer.

Tags: VERIFIED (primary document opened and read) / SECONDARY (opened a secondary/press source) /
INFERRED (derived by me from other figures, not stated directly in a source).

---

## 1. Context / current status of Vergesellschaftung (background, SECONDARY)

- Berlin's 2021 referendum ("Deutsche Wohnen & Co. enteignen") passed with ~59% support, targeting
  landlords with >3,000 Berlin flats — ~220,000–222,000 flats (~12% of total stock, ~14.5% of rental
  stock). SECONDARY (nd-aktuell, Wikipedia DE/EN, Statista reference).
- On 12 March 2026 the Abgeordnetenhaus passed a "Vergesellschaftungsrahmengesetz" (framework law).
  It has no immediate operative effect — it only takes effect 24 months after promulgation, and is
  expected to face an abstract judicial-review challenge on constitutionality. SECONDARY
  (berliner-wirtschaft.de, smartlandlord.de, haufe.de, search-engine synthesis — I did not open the
  primary Abgeordnetenhaus plenary record, so treat the date/mechanics as SECONDARY, not VERIFIED).
- Coalition compromise reportedly raises the threshold from 3,000 to 10,000 flats per company, with
  a "Sockelbestand" of 10,000 flats exempted; ~160,000 flats would move to public ownership under
  this narrower version (5 large groups affected). SECONDARY (search synthesis of Sondierungspapier
  coverage) — not independently opened; flag as unconfirmed/contested, may be superseded.

---

## 2. Zensus (census) vacancy by owner type — the core ask, PARTIALLY UNRESOLVED

**I could not pull numeric Berlin figures for vacancy-by-owner-type directly** — the
ergebnisse.zensus2022.de database (table 4000W-3006, "Wohnungen: Art der Wohnungsnutzung —
Eigentumsform des Gebäudes") is a JavaScript single-page app; WebFetch only returns the page shell
("Zensusdatenbank: Ergebnisse des Zensus"), not the underlying data grid. A companion table exists
titled "Wohnungen: Grund des Wohnungsleerstands" (reason for vacancy) at the same site — also not
machine-readable via fetch. **This needs a manual browser session (the table lets you pick region =
Berlin and cross Eigentumsform × Nutzungsart) or a direct CSV/API pull — flagging as a gap for
someone with interactive browser access or Destatis GENESIS-API credentials.** INFERRED gap, not a
finding.

What IS confirmed from Destatis national press release (VERIFIED, opened primary page
destatis.de/.../PM_zenus2022_46.html):
- Nationwide 15 May 2022: ~1.9 million dwellings vacant, vacancy rate 4.3%.
- Nationwide: >50% of vacant dwellings vacant ≥1 year; ~38% available within 3 months.
- Berlin specifically: 29% of Berlin's vacant units were long-term vacant (≥12 months) vs 41% short
  term (<3 months) — i.e. Berlin's vacancy skews short-term/frictional relative to national average.
- Primary vacancy reason nationwide: "Bau-/Sanierungsarbeiten" (construction/renovation) = 24% of
  vacant-dwelling cases. This is the closest the primary press release gets to "modernisation
  vacancy," but it is not broken out by owner type and not Berlin-specific.
- The release does **not** break vacancy down by Eigentümertyp (owner type) at all — that cross-tab
  exists only in the underlying database table, not in the press summary.

From a Berlin parliamentary written answer (SECONDARY, not opened primary PDF, from search
synthesis): Berlin had 40,681 vacant flats at Zensus 2022 (vacancy rate 1.97%), of which 11,764 had
been vacant ≥12 months. This is **lower** than the Destatis press release's national framing would
suggest and is Berlin's own total, not owner-type split. SECONDARY — flag for someone to open
pardok.parlament-berlin.de/starweb/adis/citat/VT/19/SchrAnfr/S19-20607.pdf directly (I got a 403 on
one related BBU fetch; did not attempt this specific PDF via curl — worth a retry with a different
user agent/direct PDF download rather than WebFetch).

---

## 3. The empirica/IBB-commissioned study (VERIFIED — opened and parsed primary PDF)

Source: *Untersuchung zu den Auswirkungen einer Vergesellschaftung auf den Berliner Wohnungsmarkt*,
empirica ag (Prof. Dr. Harald Simons), commissioned by Berliner Sparkasse, Berliner Volksbank, DKB,
and Investitionsbank Berlin (IBB). Dated Berlin, June 2026. PDF opened and converted with pdftotext;
all figures below read directly from the extracted text.

**Note on provenance/bias**: commissioned by banks with a direct financial stake in the housing
market (mortgage/development lenders) — treat as an interested-party study, not neutral, even though
the figures themselves are traceable to named sources (empirica regio, Destatis, Bernt & Holm).

Key figures:
- Berlin-wide **vacancy rate fell from ~3.63% (2011) to ~1.59% (2024)** — Berlin now has the
  3rd-lowest vacancy rate of any German city/county (was ranked 112th in 2011). VERIFIED (Table 2,
  sourced to empirica regio / Destatis).
- Average living space per capita in Berlin: 39.9 m² (2024) vs 40.2 m² (2011), i.e. essentially flat
  while the German average rose from ~44.5 to 48.2 m². Used as a second scarcity indicator. VERIFIED.
- The Vergesellschaftung-relevant stock is ~240,000 flats in this study's framing (12% of total
  stock / 14.5% of rental stock) — slightly higher than the oft-cited ~222,000, likely reflecting a
  later/different cutoff. VERIFIED (as stated in source), reconciliation with the 222,000 figure not
  resolved — INFERRED these are different snapshots of the same underlying universe.
- **Bernt & Holm (2023) estimate, cited here**: if the ~240,000 vergesellschaftete flats were let at
  the 63% WBS-household allocation quota used by the landeseigene (public) companies, and if annual
  tenant turnover ("Fluktuation") stayed constant at 5%/year, this would produce **~7,000 additional
  new lettings per year to WBS-eligible (income-capped) households**. This is the single most
  concrete "additional capacity released" number found. SECONDARY-sourced-via-VERIFIED (i.e., I
  verified empirica's citation of Bernt & Holm, but did not independently open the Bernt & Holm 2023
  original).
- empirica's **counter-argument**, which materially changes the "net new housing" math: lower rents
  in the expropriated stock would depress turnover. Empirica estimates turnover ("Fluktuation") in
  the expropriated portfolio would fall by **~13%**, and per-capita floor-space consumption would
  rise by **~3%** in that stock — equivalent to taking **~7,200 dwellings' worth of floor space**
  (3% × 240,000) **out of effective circulation**. VERIFIED (own calculation stated explicitly in the
  study, §3.1/Zusammenfassung).
- Net reading from empirica/IW: the ~7,000/year WBS-reallocation gain from Bernt & Holm is likely
  **largely or fully offset** by the ~7,200-dwelling-equivalent reduction in effective supply from
  lower turnover and higher per-capita space use — i.e., this study argues the exercise is close to
  a wash or net negative for total units reaching the market, even before counting rent increases in
  the non-expropriated segment (cites Kholodilin 2024 meta-study: rent control raises prices in the
  uncontrolled segment in 14 of 17 studies reviewed; Mense et al. 2023 found Mietpreisbremse raised
  free-market rents 2.2–2.5%). VERIFIED as stated conclusions of this report; note these are
  modelled/extrapolated effects, not observed outcomes (Vergesellschaftung hasn't happened yet).
- Market-power finding: large landlords have workable market concentration in only 5 of Berlin's 190
  postal-code areas (Charlottenburg-Nord/Siemensstadt, Spandau/Falkenhagener Feld,
  Wedding/Rehberge). VERIFIED.
- Spatial-equity finding: Deutsche Wohnen/Vonovia holdings skew toward peripheral, already
  disadvantaged areas, not central/high-rent areas — the study argues Vergesellschaftung would do
  little to fight gentrification pressure in sought-after inner districts. VERIFIED.

**This study contains no owner-type vacancy breakdown and does NOT claim large landlords sit on
disproportionate vacancy** — its whole argument is that Berlin vacancy is now very low across the
board (1.59%) and that the "lever" being tested should really be framed around turnover/allocation,
not standing empty flats.

---

## 4. IW Köln-commissioned companion study (VERIFIED — opened and parsed primary PDF)

Source: *Auswirkungen der Vergesellschaftung privater Wohnungsunternehmen in Berlin* — Gutachten,
Institut der deutschen Wirtschaft (IW) Köln, authors Dr. Philipp Deschermeier & Prof. Dr. Michael
Voigtländer, same four bank/IBB commissioners, dated Köln, 23.06.2026 (Stand April 2026).

- This report's framing is macro/fiscal (social targeting of the measure, investment effects on the
  affected portfolios, historical analogues, consequences for Berlin as a business location) rather
  than a vacancy/unit-count study. A single textual mention of "Leerstand" occurs in the context of
  comparing Berlin's tight market to other capitals with oversupply/vacancy (i.e., Berlin lacks that
  oversupply) — no Berlin-specific vacancy statistic by owner type is given. VERIFIED (I opened and
  grepped the full extracted text; "Leerstand" appears once, in prose, not in a data table).
- Net contribution to this question: **confirms there is no vacancy-release argument to extract from
  this document** — it's a different kind of brief (investment/compensation/fiscal), not a dwelling
  count study. Treat as a negative result (searched, found nothing usable), not a wasted citation —
  rules this out as a data source for the lever's numerator.

---

## 5. Corporate landlord vacancy rates — company-level figures

| Company | Berlin units | Vacancy rate | Date | Tag | Source |
|---|---|---|---|---|---|
| Vonovia + Deutsche Wohnen (combined) | ~140,000 | — | end 2025 | SECONDARY | search synthesis (multiple outlets) |
| Vonovia (standalone, Berlin-specific) | 138,372 | 0.8%–1.1% (sources disagree: one says 0.8%, another Q1 2023 says 1.1%) | Mar 2025 / Q1 2023 | SECONDARY | search synthesis; not independently opened a Vonovia Berlin-only disclosure |
| Vonovia (Group-wide, all of Germany, NOT Berlin-specific) | n/a | 1.9% EPRA vacancy (2023 and 2024 both reported ~1.9%) | 31 Dec 2024 | VERIFIED | report.vonovia.com/2024/q4/de/epra-leerstandsquote (opened primary page; it explicitly does NOT disclose a regional/Berlin breakdown in this section) |
| Deutsche Wohnen (Berlin-specific) | ~100,000 (~6% of Berlin's ~1.7m stock) | **0.7%** | current (2026 facts page) | VERIFIED | deutsche-wohnen.com/fakten-positionen/deutsche-wohnen-in-zahlen (opened primary page) |
| Deutsche Wohnen Berlin new-build completions | 1,230 units (2024); 652 units (2025) | — | 2024/2025 | VERIFIED | same page |
| Deutsche Wohnen Berlin 2026 capex plan | €539m (maintenance, modernisation, new-build, climate) | — | 2026 | VERIFIED | same page |
| BBU member companies (mostly cooperatives + municipal landlords, Berlin) | ~786,000 units managed (own + 3rd-party) | **1.6%** (~12,400 vacant flats), unchanged 2023→2024 | 31 Dec 2024 | SECONDARY (search-engine summary of bbu.de page; direct fetch of the page returned HTTP 403, so I did not open the primary page myself — downgrade from the VERIFIED I'd otherwise claim) | bbu.de/beitraege/bbu-jahresstatistik-2024-berlin... |
| BBU members — stated main driver of short-term vacancy | "Bestandsertüchtigung" (refurbishment/modernisation) by far the most-cited reason; vacancy due to letting difficulty ("Vermietungsschwierigkeiten") plays almost no role | 2023/2024 | SECONDARY | same (403 on direct fetch) |
| BBU members — modernisation status of stock | ~471,000 of ~746,000+ units fully modernised (63%) | end 2023 | SECONDARY | same |

**Reading**: the two numbers that matter most for the "lever" — Deutsche Wohnen Berlin at 0.7% and
BBU (largely public/co-op) members at 1.6% — point the *opposite* direction from the "corporate
landlords hoard vacant flats" narrative: the big private corporate landlord's disclosed vacancy is
*lower* than the municipal/cooperative sector's, not higher. This matches empirica's citywide 1.59%
figure. I found no company-level or owner-type figure anywhere in this research run showing
corporate landlords with materially elevated vacancy versus public/cooperative landlords in Berlin
specifically. If such a figure exists (e.g., a much higher "spekulativer Leerstand" claim from the
campaign side), I did not locate a primary, dated, Berlin-specific number for it in this session —
see §6.

---

## 6. Campaign-side ("Deutsche Wohnen & Co. enteignen") claims — NOT YET VERIFIED, scope gap

I confirmed the campaign's headline scope claim (>3,000-flat threshold, ~220,000 flats, 2021
referendum passed 59%, 2026 framework law) via search synthesis only (nd-aktuell, taz, Wikipedia,
vorwaerts.de) — I did not open dwenteignen.de/unser-gesetz itself, nor the Berliner Mieterverein's
"Leerstandsmelder" site, nor any campaign document making a specific vacancy/withheld-capacity
numeric claim. **This is the single biggest gap in my pass**: I did not find or verify a campaign-side
quantitative vacancy claim (count or rate) for the corporate portfolios to set against the
Deutsche Wohnen 0.7% / BBU 1.6% figures above. Recommend a follow-up pass specifically on
dwenteignen.de, berliner-mieterverein.de, and leerstandsmelder.de (if that domain still exists for
Berlin) before finalizing the "lever."

I also did not reach, in this pass: Adler Group/ADO Berlin, Heimstaden Berlin, Covivio Berlin, Grand
City Properties Berlin, or Akelius Berlin (pre-2021 sale) company-specific figures; Zweckentfremdung
(commercial-misuse) case counts against large companies; or the LWU (6 state-owned companies)
vacancy/modernisation-vacancy/commercial-unit breakdown from their own annual reports. Flagging all
of these as **not researched in this pass**, not as "zero data exists" — a second pass should target
them directly given remaining budget.

---

## 7. Zukunfts- und Sozialpakt Wohnen (2021) — delivery tracking

- Vonovia/Deutsche Wohnen (pre-merger-closing) offered the Senate a pact in connection with their
  2021 merger: commitment to build **13,000 new flats in Berlin** (one-third publicly subsidised),
  cap rent increases at 1%/year for 3 years then inflation-only for 2 more years, and sell part of
  the offered portfolio to public landlords. SECONDARY (search synthesis of multiple outlets:
  vorwaerts.de reporting style sources, berlin.de press release, wiwo.de, boersen-zeitung.de).
- Actual sale executed: **14,750 residential + 450 commercial units**, for **€2.46–2.5 billion**,
  split HOWOGE ~8,300, berlinovo ~4,000–4,065, degewo ~2,400. Of the 14,750, ~10,000 came from
  Deutsche Wohnen and ~4,250–4,750 from Vonovia (sources vary slightly on the split). SECONDARY
  (berlin.de Senate press release found via search, not independently opened with full text).
- I did **not** find and verify a Senate/Vonovia monitoring report tracking whether the 13,000
  new-build commitment has actually been delivered by 2026. This is a gap — worth checking Vonovia's
  own Berlin press releases and any Senate Kleine/Große Anfrage on "Zukunfts- und Sozialpakt
  Umsetzungsstand."

---

## 8. Honest reading for the "lever" — how many dwellings could plausibly be released?

Putting the verified pieces together:

1. **Citywide vacancy is now very low (~1.6%, Berlin among the 3 tightest markets in Germany)** and
   has fallen sharply since 2011 (~3.6%) — there is little slack sitting idle in *any* ownership
   category, corporate or public. This directly undercuts a framing of "222,000 flats sitting empty
   or withheld" — the overwhelming majority of that stock is occupied and let.
2. **Disclosed corporate vacancy (Deutsche Wohnen 0.7%) is not higher than the public/cooperative
   sector (BBU ~1.6%)** in the figures found — if anything it's lower, likely reflecting large
   corporate landlords' commercial incentive to keep units let versus smaller/cooperative landlords'
   mix of older, harder-to-let stock. I found no Berlin-specific, dated figure showing corporate
   landlords holding disproportionate "spekulativer Leerstand" or commercial-misuse units at scale —
   that claim remains unverified in this pass, not disproven, since I didn't reach the campaign's own
   sources (§6).
3. The one concrete, sourced "additional supply" number is Bernt & Holm's **~7,000 additional
   WBS-household lettings per year**, achieved not by releasing vacant units but by re-targeting who
   gets units as normal ~5%/year turnover churns through the expropriated stock — this is a
   reallocation effect, not new supply.
4. That gain is directly offset, in empirica's modelling, by an estimated **~13% fall in turnover**
   and **~3% rise in per-capita space use** in the expropriated stock once rents drop, which empirica
   quantifies as equivalent to **~7,200 dwellings' worth of floor space** removed from effective
   circulation per year — a number of the same order of magnitude as the gain, making the net new
   "effective supply" close to zero or even negative, by this one (bank-commissioned, non-neutral)
   study's own logic.
5. **At most, under the most favourable assumptions found in this research** (constant turnover,
   full WBS-quota reallocation, ignoring empirica's offsetting turnover-reduction effect), the
   defensible number for the lever is **on the order of ~7,000 flats/year reallocated to
   lower-income households** — not vacant stock newly brought onto the market, and not a one-time
   stock of hidden capacity. I found no credible, dated, Berlin-specific source in this pass
   supporting a materially larger number (e.g., tens of thousands of flats "hoarded").
6. If the visualisation wants a single caveat-laden number for the lever, I'd suggest something like:
   **"~7,000 flats/year could be reallocated to income-capped households under the public-sector
   letting quota — not new vacant capacity; one study estimates this is largely offset by reduced
   turnover once rents drop."** This should be flagged in the UI as modelled/contested, sourced to
   Bernt & Holm (2023) as cited by empirica (2026), not as an observed fact.

---

## Summary (5 lines, as requested)

1. Berlin's vacancy rate is now ~1.6% citywide (down from ~3.6% in 2011) — there is very little
   idle housing stock in any ownership category to "release." (VERIFIED, empirica/IBB study)
2. Deutsche Wohnen's disclosed Berlin vacancy is 0.7%; the largely public/cooperative BBU membership
   reports ~1.6% — no evidence found that corporate landlords hoard more vacancy than public ones.
3. The only concrete "additional capacity" figure in the literature is Bernt & Holm's ~7,000
   additional lettings/year to WBS households via reallocated turnover, not released vacant stock.
4. A bank-commissioned empirica study argues this gain is largely offset by an estimated ~13% drop
   in turnover and ~3% rise in per-capita space use once rents fall (≈7,200 dwelling-equivalents/yr).
5. Campaign-side ("Deutsche Wohnen & Co. enteignen") quantitative vacancy/withheld-capacity claims,
   LWU company-level data, and several named corporates (Adler, Heimstaden, Covivio, GCP, Akelius)
   were not reached in this pass — flag as open gaps for a follow-up research round.

Full file: /tmp/claude-1000/-home-dl-repos-berlin-construction-compare/01d35b68-ec32-4268-84d6-e6ede065e1b1/scratchpad/sonnetA_corporate_vacancy.md
Downloaded primary PDFs (for reuse/re-verification) also in this scratchpad: ibb_woma.pdf / ibb_woma.txt
(empirica study) and iwkoeln.pdf / iwkoeln.txt (IW Köln study).
