# Owner-type vacancy, construction cost, and compensation-to-dwelling conversion (Berlin)

Companion CSV: `sonnet1_figures.csv` (same directory). Raw Zensus downloads: `playwright-dl/4000W-3006_de_flat.csv`, `playwright-dl/4000W-0018_de_flat.csv`, `playwright-dl/4000W-0001_de_flat.csv`, and a cleaned per-Bezirk extract `berlin_4000W-3006_by_bezirk_owner_usage.csv`.

Tags: **VERIFIED** = I opened/downloaded the primary source myself this session. **SECONDARY** = relayed from another agent's report or a WebSearch AI summary I did not independently re-render against the primary document. **INFERRED** = my own calculation/assumption. **UNVERIFIED-this-session** = a figure the task brief asked me to use but I could not locate it verbatim in the time available.

---

## 1. Owner-type vacancy, Zensus 2022, Berlin

**Source, VERIFIED:** I opened `ergebnisse.zensus2022.de`, located table **4000W-3006** ("Wohnungen: Art der Wohnungsnutzung – Eigentumsform des Gebäudes/Räume – Wohnungen im Gebäude"), switched the regional dimension to "Bezirke (Hamburg und Berlin)" and downloaded the full CSV. I then also downloaded the purpose-built official indicator table **4000W-0018** ("Wohnungskennzahlen: Leerstandsquote nach Eigentumsform des Gebäudes"), which gives Destatis's own computed vacancy-rate percentage per owner type per Bezirk — a direct cross-check on my own ratio calculation from 3006's raw counts. Reference date for both: **15.05.2022**.

### 1a. Berlin-wide vacancy rate by owner type (dwelling-weighted, my calculation from 4000W-3006 raw counts, all 12 Bezirke summed)

| Owner type (Eigentumsform des Gebäudes) | Dwellings | Vacant | Vacancy rate |
|---|---:|---:|---:|
| **Insgesamt (all Berlin)** | 2,018,830 | 40,687 | **2.02%** |
| Bund oder Land | 40,748 | 1,942 | 4.77% |
| Anderes privatwirtschaftliches Unternehmen | 89,837 | 3,074 | 3.42% |
| Organisation ohne Erwerbszweck (Kirche etc.) | 22,164 | 539 | 2.43% |
| **Privatwirtschaftliches Wohnungsunternehmen** | 389,015 | 8,047 | **2.07%** |
| Gemeinschaft von Wohnungseigentümer/-innen | 372,040 | 7,370 | 1.98% |
| **Privatperson/-en** | 518,950 | 10,236 | **1.97%** |
| Kommune/kommunales Wohnungsunternehmen | 381,075 | 7,270 | 1.91% |
| Wohnungsgenossenschaft | 205,018 | 2,188 | 1.07% |

All VERIFIED (own aggregation of primary-source dwelling counts).

### 1b. Official Destatis "Leerstandsquote" kennzahl, per Bezirk (4000W-0018), for the owner types most relevant to the team's question

| Owner type | Lowest Bezirk | Highest Bezirk | Range (12 Bezirke) |
|---|---:|---:|---|
| Privatwirtschaftliches Wohnungsunternehmen | 1.1% (Marzahn-Hellersdorf) | 2.9% (Charlottenburg-Wilmersdorf) | 1.1–2.9% |
| Kommune/kommunales Wohnungsunternehmen | 1.1% | 3.6% (Steglitz-Zehlendorf) | 1.1–3.6% |
| Wohnungsgenossenschaft | 0.6% (Charlottenburg-Wilmersdorf) | 1.9% (Neukölln) | 0.6–1.9% |
| Privatperson/-en | 1.3% | 2.5% | 1.3–2.5% |
| Insgesamt (all owner types) | 1.4% (Marzahn-Hellersdorf) | 2.4% (Charlottenburg-Wilmersdorf, Steglitz-Zehlendorf) | 1.4–2.4% |

Full 108-row breakdown (12 Bezirke × 9 owner categories) is in `playwright-dl/4000W-0018_de_flat.csv`. These per-Bezirk official rates are consistent with my own 3006-derived dwelling-weighted averages in §1a (e.g. a simple 12-Bezirk average of "Insgesamt" column ≈ 1.9–2.0%, matching the 2.02% weighted figure).

### 1c. Vacancy-duration and vacancy-reason crossed with owner type — table codes located but not downloaded (time-boxed)

I located and confirmed these exist in the Zensus 2022 database (titles read directly from the statistic's table-of-contents page, VERIFIED they exist, NOT downloaded this session):
- **4000W-0018 / -0026**: Leerstandsquote / Marktaktive Leerstandsquote nach Eigentumsform des Gebäudes (0018 downloaded, see above; 0026 is the "market-active" variant, not pulled)
- **4000W-3030**: Dauer des Wohnungsleerstands × Eigentumsform des Gebäudes × Fläche/Gebäudetyp
- **4000W-3031**: Dauer × Grund des Wohnungsleerstands × Baujahr/Eigentumsform/Gebäudetyp
- **4000W-3033**: Grund des Wohnungsleerstands × Eigentumsform des Gebäudes × Baujahr/Gebäudetyp
- **4000W-5020 / -5021**: Dauer × Grund × Eigentumsform × Fläche × Gebäudetyp (most granular)

**Recommendation if this is needed next:** 4000W-3033 (reason × owner type) is the single highest-value next pull — it would let you test whether "Bund oder Land"'s outlier 4.8% average (driven by huge per-Bezirk swings, e.g. 16.3% for "Organisation ohne Erwerbszweck" in Marzahn-Hellersdorf, likely a small-N artifact) is structural (renovation/demolition pending) vs. speculative withholding, same mechanics as the download flow used above (navigate to `/table/4000W-3033/table-toolbar`, switch region to "Bezirke (Hamburg und Berlin)", Download → CSV (Flat)).

### 1d. Zensus 2011 comparison — did not come through at Bezirk granularity

Table **4000W-0001** ("Leerstandsquote und Eigentumsquote") offers a Stichtag selector showing both 09.05.2011 and 15.05.2022 available. I selected both and applied the Bezirke filter, but the resulting CSV download contained **only the 2022 rows** (38 rows = 19 regions × 2 variables, all dated 2022-05-15) — the 2011 selection did not propagate into the per-Bezirk cross-tab, most likely because Zensus 2011 (register-based method) does not publish this indicator at Bezirk granularity the same way 2022's full-collection census does. I did not find a working path to Berlin-Bezirk-level 2011 vacancy in the time available — flagging this as a **gap**, not a negative result for owner-type 2011 comparison specifically (2011 almost certainly has no owner-type breakdown at all, since that detail requires the 2022 full enumeration).

---

## 2. Reconciliation with company disclosures

The team's brief cites: **Deutsche Wohnen 0.7%**, **BBU members 1.6%** (both self-reported, SECONDARY — provided in the task, not independently re-verified against a Deutsche Wohnen/BBU primary filing this session).

**Finding:** Berlin's sector-wide Zensus 2022 vacancy rate for **privatwirtschaftliches Wohnungsunternehmen is 2.07%** — **above**, not below, the Berlin-wide average of 2.02%, and nearly **3× Deutsche Wohnen's self-reported 0.7%**. The **kommunale Wohnungsunternehmen** sector-wide rate (1.91%) is closer to, but still above, the BBU-member figure (1.6%).

This is not a contradiction once the denominators are understood:
- "Privatwirtschaftliches Wohnungsunternehmen" in the census is the **entire private commercial landlord sector** (large REITs like Deutsche Wohnen/Vonovia down to small professional landlords with a handful of buildings), while Deutsche Wohnen's disclosed 0.7% is **one large, actively-managed, listed portfolio**. A well-capitalized REIT minimizing vacancy for yield can easily sit far below the sector mean while smaller/distressed private landlords (captured separately in "Anderes privatwirtschaftliches Unternehmen," at **3.42%**, the highest rate of any category after Bund/Land) pull the sector average up.
- Similarly, BBU's 1.6% almost certainly reflects **BBU's own membership roster** (large professional landlords, many of them the same municipal/cooperative companies already counted in "Kommune" and "Wohnungsgenossenschaft"), not the full census universe of every entity coded under those owner types.
- **Wohnungsgenossenschaft is the only category meaningfully below the Berlin average** (1.07% vs 2.02%), consistent with cooperatives' structural incentive (member-occupancy, no speculative holding) rather than any reporting artifact.

**Caveat on "Bund oder Land" (4.77%) and "Organisation ohne Erwerbszweck" (2.43%):** both are small-N categories (40,748 and 22,164 dwellings citywide respectively) and the per-Bezirk range is extreme (e.g. Bund/Land ranges 1.1%–11.0% across Bezirke; Org. ohne Erwerbszweck hits 16.3% in Marzahn-Hellersdorf). These are likely driven by a handful of large vacant/under-renovation federal or church-owned buildings, not a systematic pattern — treat citywide averages for these two categories with caution.

---

## 3. Public construction cost per new dwelling in Berlin

**I was not able to verify a clean, single "all-in €/flat including land" figure from a primary LWU annual report within the time budget.** What I did verify or find:

### 3a. WFB 2023 (Wohnungsbauförderungsbestimmungen) cost parameters — SECONDARY (WebSearch summaries of the WFB 2023 text; I did not re-render the Amtsblatt PDF directly to confirm exact wording/paragraph)
- Construction-cost ceiling (**Baukosten**, i.e. building construction only — this is **Kostengruppen 300–400 in the DIN 276 sense, excluding land/Grundstück**, which is funded separately under WFB): **~4,200–4,500 €/m² Wohnfläche**, varying by financing model and whether 20% equity is used to avoid external debt.
- Non-repayable construction-cost subsidy (verlorener Baukostenzuschuss), Fördermodell 1 only: up to **1,800 €/m²** of funded floor area.
- Interest-free public construction loan: up to **3,500 €/m²** (Fördermodell 1) or **5,300 €/m²** (Fördermodell 2) of funded floor area.
- Capped entry rents under WFB 2023 (not a cost figure, but context): €7.00/€9.50/€11.50 per m² across the three funding models.

### 3b. LWU (6 Landeseigene Wohnungsunternehmen) completions — VERIFIED, read directly from the Senate's "Bericht zur Kooperationsvereinbarung ... 2024" PDF (`inberlinwohnen.de/.../Jahresbericht_2023_KoopV_Bericht.pdf`, extracted via `pdftotext`)
- **Neubau-Fertigstellungen (new-build completions): 4,599 Wohnungen in 2023; 3,276 in 2024** (a real decline, which the report attributes to "anhaltend schwierige allgemeine Rahmenbedingungen für den Wohnungsbau" — persistently difficult general conditions for housing construction).
- Share of that new-build floor area let under rent/occupancy restrictions: 38.7% (2023) → 43.9% (2024).
- Senate expects >5,000 completions in 2025, sustained into 2026 (forward-looking statement in the report, not yet realized).
- I could **not** locate a clean "total Neubau-Investition in € / Fertigstellungen" division inside this specific report — it reports financial KPIs (EBITDA/m², book value/m² at €1,200.44/m² in 2024, Bestandsinvestition of €32.13/m² in 2024) for the **existing portfolio**, not a per-new-unit construction-cost breakout.
- A separate press/Senate-report figure, **SECONDARY** (WebSearch summary, not independently opened): the 7 Landeseigene companies' **total investment (new-build + stock) was >€1.7bn in 2023**, with a planned **>€2.0bn for 2024**; one cited 2023 split was **~€988m for new construction**. I flag this €988m/new-build figure as unverified this session — if the team wants a defensible €/flat from LWU internal figures, €988m ÷ 8,332 completions (a *different*, longer cumulative window than the 4,599 annual figure above — see caveat) would give a crude ≈€119,000/flat, but the mismatched denominators make this unreliable; I'd recommend pulling the individual HOWOGE/degewo/Gewobag 2024 Geschäftsberichte directly for a clean per-project cost rather than back-solving from aggregate press figures.

### 3c. Independent benchmark — SECONDARY (WebSearch AI-summary of market commentary citing Destatis Baupreisindex; not independently re-rendered against the Destatis table itself)
- Residential construction prices in major German cities, Q4 2024: **~4,473 €/m²** (not Berlin-specific).
- Destatis Baupreisindex Wohngebäude, conventional construction method (2021=100): **130.8** in Q4 2024, up from 126.9 a year earlier (index only, not a €/m² figure).
- IBB Wohnungsmarktbericht 2024: I downloaded and `pdftotext`-extracted both the main report and its Tabellenband; **neither contains a "Baukosten" table** — the report covers rents, land prices (Bauland, EUR/m²/mtl.), and purchase prices, not construction cost. An earlier AI-generated WebSearch summary claiming "1,985 €/m² (−9.4%)" and "2,192 €/m² (+16.8%)" construction-cost figures from this report **could not be confirmed in the actual document text** and should be treated as unreliable/possibly a misattribution (likely conflated with the land-price table, "Tab. 2: Entwicklung des Preisniveaus für Bauland") — **do not cite that 1,985/2,192 pair.**

### 3d. Summary cost range used for §4 below
Taking the WFB cost-cap range (4,200–4,500 €/m², Kostengruppen 300–400 only, **excluding land**) and the 70 m²/Wohnung convention already used elsewhere in this project (bulwiengesa/Berlin Hyp office-conversion study, per `stage3b_verify_report.md`):

| Scenario | €/m² | €/flat (×70m²) |
|---|---:|---:|
| Low (WFB cap, debt-free variant) | 4,200 | **294,000** |
| High (WFB cap, standard variant / city-benchmark) | 4,500 | **315,000** |

**This excludes land acquisition, Baunebenkosten beyond KG400, and Außenanlagen** — an all-in figure including land would be materially higher in central Berlin and I do not have a verified figure for that; flagging as a gap rather than guessing.

---

## 4. Compensation estimates converted to new-dwelling equivalents (INFERRED)

Using the two construction-only cost scenarios from §3d. **All rows below are INFERRED — a mechanical division, not a claim that compensation funds would or could actually be redirected to construction.**

| Compensation estimate | Source (per sonnetB/sonnetC reports) | Equivalent new dwellings @ 294,000 €/flat | Equivalent new dwellings @ 315,000 €/flat |
|---:|---|---:|---:|
| €8 bn | Rechnungshof Berlin 2024, low scenario | 27,211 | 25,397 |
| €10.1 bn | Holm/Thonke/Arpagaus 2025 (`dwe_refinanz_holm_thonke_arpagaus.txt`, already in scratchpad) — their base-case refinanceable-via-rents scenario: "eine Entschädigungssumme von 10,1 Mrd. € aus den Mieteinnahmen refinanziert werden" (VERIFIED — I grepped and read the exact sentence in the already-downloaded source) | 34,354 | 32,063 |
| €11 bn | Rechnungshof Berlin 2024 | 37,415 | 34,921 |
| €13.5 bn | IMK Policy Brief 225, Ertragswert-based, explicitly against 210,000 Wohnungen | 45,918 | 42,857 |
| €21 bn | Holm/Thonke/Arpagaus 2025, same source — their stated **maximum** of the modeled range: "ein[em] Maximalbetrag von etwa 21 Mrd. Euro" (VERIFIED — exact sentence read in the already-downloaded source); note the same source gives an even higher 25 Mrd. € under 1pp-cheaper financing, and a "realistic" range of 10–17 Mrd. € | 71,429 | 66,667 |
| €29 bn | Rechnungshof Berlin 2024 / Senat 2019-2020 Verkehrswert scenario | 98,639 | 92,063 |
| €36 bn | Rechnungshof Berlin 2024 / Senat 2019-2020 Verkehrswert scenario | 122,449 | 114,286 |
| €39.5 bn | Senat 2020 update, Verkehrswert | 134,354 | 125,397 |

**Context for scale:** the Senate's own 2040 need estimate is **211,000 additional dwellings** citywide (per `stage3b_verify_report.md`, VERIFIED there), and actual 2025 completions were only 11,027 citywide (all developers, not just LWU). Even the largest compensation figure (€39.5bn) converts to roughly 125,000–134,000 dwellings at pure construction cost — **well above what Berlin has built in any recent multi-year span**, but also a reminder that this is an apples-to-oranges comparison: compensation (if paid) would go to expropriated owners, not into a construction budget, and the IMK source explicitly frames its own €13.5bn figure as a *transfer*, not a supply mechanism.

€10.1bn and €21bn were not in sonnetB/sonnetC's grep hits, but both turned up directly in `dwe_refinanz_holm_thonke_arpagaus.txt` (already in the scratchpad from an earlier agent) — they are the Holm/Thonke/Arpagaus 2025 study's base-case refinanceable sum (10.1bn) and stated maximum of their modeled range (21bn), distinct from the Rechnungshof/Senat Verkehrswert scenarios and the IMK Ertragswert figure.

---

## Files delivered
- `/tmp/.../scratchpad/sonnet1_owner_vacancy_cost.md` — this report
- `/tmp/.../scratchpad/sonnet1_figures.csv` — flat CSV of every extracted figure with VERIFIED/SECONDARY/INFERRED tags
- `/tmp/.../scratchpad/berlin_4000W-3006_by_bezirk_owner_usage.csv` — cleaned Berlin-only extract (540 rows: 12 Bezirke × 5 usage types × 9 owner types) from the raw Zensus download
- `/tmp/.../scratchpad/playwright-dl/4000W-3006_de_flat.csv` — full raw Zensus download (Hamburg + Berlin Bezirke, all dimensions)
- `/tmp/.../scratchpad/playwright-dl/4000W-0018_de_flat.csv` — official Leerstandsquote-by-owner-type indicator, raw download
- `/tmp/.../scratchpad/playwright-dl/4000W-0001_de_flat.csv` — Leerstandsquote/Eigentumsquote, 2022 only (2011 did not propagate — see §1d)
- `/tmp/.../scratchpad/pdfs/koopv_bericht2024.txt` — full text extract of the Senate's 2024 KoopV report (LWU completions, financial KPIs)
- `/tmp/.../scratchpad/pdfs/ibb_tabellenband_2024.txt` — full text extract of IBB Wohnungsmarktbericht 2024 Tabellenband (confirms no Baukosten table present)
