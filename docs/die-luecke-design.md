# „Die Lücke" und „Was bringt wie viele Wohnungen?" — Datengrundlage, Narrative, Visualisierungsstrategie

Status: design document, no code. Written 2026-11-15 from four research stages (see `docs/research/`).
Verification tags follow the research reports: **VERIFIED** = read in a primary source; **SECONDARY** = press/secondary only; **INFERRED** = our arithmetic.

---

## 0. The one finding that changes everything

The pitch as drafted ("245,000 people arrived in five years, a decade of building added 126,373 dwellings, pick your district and watch the lines diverge") is true but fragile. Three things break it under hostile reading:

1. **The population series.** The Einwohnerregister (the series already in this repo) overstates Berlin's population by ~213,000 at end-2025 against the census-anchored Fortschreibung (3,913,644 vs 3,700,577, VERIFIED). Register growth 2011→2025 is +486,530; census-anchored growth (Zensus 9.5.2011 → A I 3 31.12.2025) is +408,212. The dwelling stock and the Mikrozensus households are both census-anchored, so mixing in the register inflates "missing dwellings" by ~40,000.
2. **The household-size divisor.** Berlin's Mikrozensus household size has **risen**, from 1.75 (2011) to 1.85 (2024) and 1.88 (2025, VERIFIED, within-segment rises despite breaks in 2016/2020/2022). Every 0.05 moves the Berlin gap by 5,000–6,000 dwellings.
3. **The result.** Depending on basis and divisor the same completions give a "gap" anywhere between ~9,000 and ~92,000. A critic picks the low number and the piece is dead.

The defensible version (stage 3a): **census-anchored growth ÷ 2024 Bezirk household size − completions 2012–2025 ≈ +32,000 dwellings for Berlin, range 16,000–44,000**, positive in 9 of 12 Bezirke. That is much smaller than the Senate's 137,000/138,000 "Entlastungsbedarf". The reason is in the ledger in §2.2: **all 408,000 newcomers found a home, and nearly nine in ten of them found it in a newly built dwelling.** The shortage is not "people without flats". It is a buffer that has been spent, a shelter population that has doubled, and the households that never formed or never came. That is where the Senate's 137,000 sits, and that is what the visualisation lets the reader go looking for. "Die Lücke" becomes **„Berlin hat Platz gemacht. Wo?"** (§3).

---

## 1. Datasets

### 1.1 Already in the repo (do not redo)
| Dataset | Source | Granularity | Years | Obs | Measures |
|---|---|---|---|---|---|
| Baufertigstellungen | Statistischer Bericht F II 2 (Statistische Bibliothek series BBSerie_mods_00000448), one XLS/XLSX per year | Bezirk | 2010–2025 | 12×16 | dwellings_total (incl. Baumaßnahmen an bestehenden Gebäuden), dwellings_new_residential, buildings, Wohnfläche m² |
| Einwohnerregister | A I 5 (BBSerie_mods_00000260), 31.12. issue per year | Bezirk | 2010–2025 | 12×16 | population at Hauptwohnsitz |

Correction to `data/processed/berlin_NOTES.md`: the 2025 F II 2 figure of 11,027 is a **full calendar year** (press release 59/2026, corrected 22.05.2026, VERIFIED), not partial. New-build dwellings fell to 9,524 (−35%), measures on existing buildings rose to 1,503 (more than doubled). Two totals exist: 11,027 (all buildings) vs 10,952 (residential buildings only, shown on the F II 2 web page). Fix one definition and keep it.

### 1.2 To add for Part 1 ("Die Lücke")
| # | Dataset | Code / where | Granularity | Years | Format / friction | Obs | Variables, measures |
|---|---|---|---|---|---|---|---|
| A | Dwelling stock (Fortschreibung des Wohngebäude- und Wohnungsbestandes) | F I 1, BBSerie_mods_00000694; current issues statistik-berlin-brandenburg.de/f-i-1-j/ | Bezirk; Planungsraum (542 LOR) from 2023 issue | 2007–2014, 2016–2025 (no 2015 issue) | PDF; XLSX 2024+ | 12×19; 542×3 | Wohnungen insgesamt (incl. Wohnheime, incl. in Nichtwohngebäuden), by rooms 1…7+, Räume, Wohnfläche (100 m²). No Baujahr. Two rebasings: −31,449 at end-2011 (Zensus 2011), +16,037 at end-2021 (GWZ 2022). End-2025: 2,069,432 |
| B | Bauabgang | F II 2 Tables 19–23 | Bezirk (whole buildings only, Tab. 23) | annual | in A's files | 12×15 | dwellings demolished: 110–923/yr Berlin 2016–25 → footnote only |
| C | Bauüberhang | F II 2 Tables 16–17 | Bezirk × Bauzustand (unter Dach / Rohbau / nicht begonnen / erloschen), Bauherr, Genehmigungshalbjahr | annual 31.12. | same files; BF_BA_BU_Diagramm.xlsx on F II 2 page gives Berlin 2016–25 | 12×15×4 | end-2025: 48,394 total; 40,937 in new buildings: 12,901 unter Dach, 12,252 Rohbau, 15,784 not started; 3,055 lapsed |
| D | Baugenehmigungen | F II 1 j (annual XLSX/PDF, statistik-berlin-brandenburg.de/f-ii-1-j/), F II 1 m monthly PDFs | Bezirk (Tab. 6) | 2005– | one PDF/month; annual XLSX enough | 12×~20 | permitted dwellings incl. Baumaßnahmen. Berlin 2016–25: 21,107 / 21,562 / 21,029 / 19,752 / 18,077 / 17,005 / 15,186 / 14,398 / 9,772 (2024) / 13,754 (2025); 2024 and 2025 Bezirk tables extracted in stage 3b |
| E | Census-anchored population | A I 3 Bevölkerungsfortschreibung, BBSerie_mods_00000019; 2025 issue XLSX | Berlin 2011–2021 (2011 basis); **Bezirk only 2022–2025 (2022 basis)** | 2011–2025 | PDF/XLSX | 1×11 + 12×4 | Berlin: 3,326,002 (2011) … 3,677,472 (2021); 3,632,853 (2022) … 3,700,577 (2025). Bezirk 2012–2021 must be **estimated** (register × Berlin ratio, blended between census anchor points) |
| F | Zensus 2011 per Bezirk | AfS Gemeindeblätter, two PDFs per Bezirk (`11xx_<Bezirk>_BEV.pdf`, `_GWZ.pdf`) via statistischebibliothek.de | Bezirk | 9.5.2011 | 24 PDFs | 12 | population 3,292,365; private households 1,794,936; dwellings 1,869,437; vacant 66,277 (3.5%); households by size |
| G | Zensus 2022 kleinräumig | „Kleinräumige Daten Berlin – Zensus 2022", Ebene Bezirksregionen XLSX (statistik-berlin-brandenburg.de/zensus22/lokale-daten-berlin/), also Planungsraum and Block levels | 143 Bezirksregionen → sum to Bezirk; 542 PLR | 15.5.2022 | XLSX, 35 characteristics, cell-key noise ≤20 per Bezirk | 143×35 | pop 3,596,999; private households 1,960,342; dwellings 2,018,831; vacant 40,681 (1.97%), ≥12 months 11,764; vacancy reasons (Drs. 19/20607); ownership, rented share, heating |
| H | Mikrozensus households | A I 11 (to 2019, BBSerie_mods_00000011), joint A I 10/11/A VI 2 (2020+, BBSerie_mods_00000633); Tab. 7.4 Bezirke | Bezirk | 2011–2025 | PDF; breaks 2016 (new sample), 2020 (redesign), 2022 (census weighting) | 12×14 | households (1,000), persons, size. Berlin 1.754 (2011) → 1.789 (2019) → 1.80 (2021) → 1.85 (2024) → 1.88 (2025). Bezirk 2024: F-K 1.73 … Reinickendorf 2.01 |
| I | Register-based households | A I 17 (BBSerie_mods_00001585) | Planungsraum, Bezirk | 2022–2025 | PDF/XLSX | 542×4 | 2.22 m households, 1.77 persons (31.12.2024) — **different concept**, ~250k more households than Mikrozensus; use only as sensitivity |
| J | Register population, small-area | A I 16 (LOR Planungsräume), Open Data CSV „Einwohner in LOR-Planungsräumen am 31.12." (daten.berlin.de; 403 to scripts, download manually) | 542 PLR | 2007–2025 | CSV; LOR boundary break 2020→2021 | 542×19 | E_E, E_EM, E_EW, age bands — for a small-area map layer only |
| K | Untergebrachte Wohnungslose | AfS page „Untergebrachte Wohnungslose" (Stichtag 31.01.), Destatis Wohnungslosenstatistik | Bezirk (partial) | 2022–2025 | web table | 12×4 | 25,975 / 39,375 / 47,260 / 53,610; LAF capacity 45,276 places, 41,369 occupied 02.01.2025 (Drs. 19/21327) |
| L | **Net migration Berlin↔Brandenburg** | A III 1 Wanderungen / Open Data „Wanderungen nach Bezirken" — **not yet inventoried** | Bezirk × Ziel/Herkunft | annual | to confirm | 12×15 | needed for panel 4 („Gar nicht da": households that left for the Umland) |
| M | Vacancy benchmarks | CBRE-empirica Leerstandsindex Methode PDFs 2016/2023/2025 (empirica-institut.de); StEP Wohnen 2040 Bericht p. 76 | Berlin | 2010–2024 | PDF | 15 | market-active vacancy Berlin 2.6% (2010), 2.3 (2011), 1.1 (2016), 0.8 (2018–19), 0.3 (2022–24) = 5,400 flats; „3 % Fluktuationsreserve" is a convention („nach allgemeiner Auffassung", StEP 2040 p. 76; glossary 2–5%) |
| N | Demand targets | StEP Wohnen 2040 (Senat 2024) + Fortschrittsbericht 16.06.2026; Bevölkerungsprognose 2024–2040 (Prognoseräume); IW-Report 03.10.2024 | Berlin / Bezirk / Prognoseraum | 2022–2040 | PDF | small | 222,000 = 137,000 Entlastung (41k reserve + 77k relief + 19k replacement) + 85,000 demographic; update 211,000 = 138k + 73k; IW: need 31,300/yr 2021–25 vs 16,382 built |

### 1.3 To add for Part 2 (levers)
| Lever | Dataset / primary source | Headline figures (reference date) | Granularity | Tag |
|---|---|---|---|---|
| Zweckentfremdung (misuse ban since 1.5.2014) | Drs. 19/24230 (13.11.2025); Bezirk × year table Drs. 19/21276 (28.01.2025); 19/24712 (21.01.2026) | 31,706 dwellings returned since 2014, of which 8,330 Ferienwohnungen (30.06.2025); Senate records no further split; Ferienwohnung returns ~500/yr since 2020; registration numbers issued 4,319 (30.09.2024) | Ferienwohnungen by Bezirk 2016–2024; total Berlin only | VERIFIED |
| Short-term rentals | Inside Airbnb Berlin snapshot 19.09.2026, listings.csv (~75 vars, `neighbourhood_group` = Bezirk) | 12,376 listings; 8,446 entire homes (6,532 with availability; 4,929 reviewed in last 12 months); Mitte 1,973, F-K 1,662, Pankow 1,432 … M-H 72 | Bezirk / Ortsteil / point | VERIFIED (own count) |
| Vacancy activation | Zensus 2022 (G) + CBRE-empirica (M) | 40,681 total vacant, 11,764 ≥12 months, 5,400 market-active | Bezirk (census) / Berlin | VERIFIED |
| Vergesellschaftung | Expertenkommission Abschlussbericht 27.06.2023; Rahmengesetz Drs. 19/2842 (CDU/SPD, 18.12.2025); Rechnungshof Bericht 20.02.2024 | ~222,000 flats at owners with ≥3,000 flats (Dec 2021) = 13.5% of rental stock; no € figure in the commission report; Rahmengesetz: Verkehrswert as starting point, no threshold, no AöR; Rechnungshof: compensation >11 bn € → AöR deficits; Sondervotum: construction boost „nicht belegt und eher unplausibel" | Berlin | VERIFIED |
| Public purchases / Vorkaufsrecht | Senate LWU results PM 1672180 (19.05.2026); Vorkaufsrecht reports 4 (2021) and 9 (31.03.2026) | LWU stock 374,472 (404,170 incl. Berlinovo); 2025: +4,692 Neubau, +4,609 Ankauf; 2022–25 completions 18,896; Vorkaufsrecht 4,121 flats (2020) → 72 (2025) after BVerwG 4 C 1.20, 9.11.2021 | Berlin | VERIFIED |
| Conversions / Aufstockung | F II 2 „Baumaßnahmen an bestehenden Gebäuden"; Deutschlandstudie 2019 (TU Darmstadt/Pestel); bulwiengesa for Berlin Hyp 04/2025 | 1,503 completions 2025 (permits 2,120); 20,000–36,000 units on ~330 single-storey supermarket sites (only Berlin number in the study); ~30,000 from ~2 m m² offices (theoretical) | Bezirk / Berlin | VERIFIED / SECONDARY (office) |
| Social bindings | IBB Wohnungsmarktbericht 2024 Tabellenband Tab. 10–12 | ~90,600 bound flats (2023); 46,408 bindings expire 2024–2034 | Berlin | VERIFIED |
| Mietendeckel | DIW Wochenbericht 8/2021; ifo Schnelldienst 3/2021 + PM 12.04.2022 | listings −50% (DIW), „up to 60%" (ifo 2022) | Berlin | VERIFIED |
| Deficit benchmarks | IW-Report 2024; Pestel Bau-Monitor 08/2026 | IW: 31,300/yr need vs 16,382 built; Pestel: ≥58,000 deficit | Berlin | VERIFIED / SECONDARY |

Still unverified (do not print without checking): Pestel 58,000 PDF; bulwiengesa primary PDF; LWU per-year series 2015–2024 and 2.1% vacancy; WBS holders; permits by Bezirk 2016–2023 and lapsed permits by year; Zweckentfremdung annual totals before 2025; Berlin Dachgeschoss potential study; Brandenburg migration dataset (L).

---

## 2. The numbers to build on

### 2.1 Headline gap per Bezirk (definition ii, stage 3a)
Census-anchored growth 9.5.2011→31.12.2025, ÷ 2024 Mikrozensus Bezirk household size, − completions 2012–2025 (dwellings_total).

| Bezirk | Δ pop (census-anch.) | Completions 2012–25 | Gap | Census vacancy 2011→2022 | HH size 2014→2024 |
|---|---|---|---|---|---|
| Mitte | +49,234 | 23,201 | **+3,800** | 4.0 → 2.2% | 1.71 → 1.82 |
| Friedrichshain-Kreuzberg | +16,032 | 13,831 | **−4,500** (kept pace) | 3.0 → 2.0% | 1.71 → 1.73 |
| Pankow | +55,772 | 24,737 | **+5,200** | 3.0 → 1.9% | 1.65 → 1.86 |
| Charlottenburg-Wilmersdorf | +32,971 | 11,639 | **+7,100** | 3.3 → 2.5% | 1.67 → 1.76 |
| Spandau | +33,887 | 11,307 | **+6,000** | 4.5 → 2.4% | 1.72 → 1.96 |
| Steglitz-Zehlendorf | +18,004 | 8,094 | **+1,000** | 3.8 → 2.4% | 1.81 → 1.97 |
| Tempelhof-Schöneberg | +22,106 | 9,063 | **+2,800** | 3.3 → 1.7% | 1.82 → 1.86 |
| Neukölln | +10,689 | 7,657 | **−1,700** (kept pace) | 3.5 → 2.1% | 1.87 → 1.79 |
| Treptow-Köpenick | +55,800 | 31,174 | **−1,800** (kept pace) | 2.7 → 1.7% | 1.76 → 1.90 |
| Marzahn-Hellersdorf | +41,329 | 17,872 | **+3,500** | 4.1 → 1.4% | 1.85 → 1.93 |
| Lichtenberg | +52,921 | 22,892 | **+6,800** | 3.2 → 1.6% | 1.69 → 1.79 |
| Reinickendorf | +19,467 | 6,961 | **+2,700** | 4.6 → 2.1% | 1.88 → 2.01 |
| **Berlin** | **+408,212** | **188,428** | **≈ +32,000** (16k–44k) | **3.5 → 2.0%** | **1.75 → 1.85** |

Cross-checks: census households vs census dwellings 2011→2022 = +16,015 (lower bound: census households are dwelling-households and cannot show doubling-up, so the shortage appears only as vacancy −25,600); households vs F I 1 stock 2011→2025 = +21,441; shortfall against a 3% reserve in 2025 = +25,217 (2011 on the same rule: a 12,429 surplus). Register version = +73,939 — **do not use as headline**; show it only inside the "basis" toggle, labelled.

### 2.2 The ledger: where the 408,000 live, and where the Senate's 137,000 comes from

**Census to census, 9.5.2011 → 15.5.2022 (all inputs VERIFIED, stage 3a; arithmetic INFERRED).** Population +304,614. Private households +165,418. Dwellings +149,403. Vacant dwellings −25,577 (66,277 → 40,700). Dwellings in non-household use (holiday, commercial, second homes, unassigned) +9,562 (8,224 → 17,786). Identity: ΔHouseholds = ΔDwellings − ΔVacant − ΔOther = 149,403 + 25,577 − 9,562 = 165,418 ✓.

Census household size was **flat at ≈1.79 in both censuses** (persons in private households ÷ households; ~90,000 persons outside private households in 2022, 2011 share assumed equal). Converting at 1.79:

| Where the 304,614 newcomers of 2011–2022 live | Dwellings | People |
|---|---|---|
| In newly added dwellings | +149,403 | ≈ 267,000 (88%) |
| In dwellings that were vacant in 2011 | 25,577 | ≈ 46,000 (15%) |
| Displaced by dwellings leaving household use | −9,562 | ≈ −17,000 (−6%) |
| Residual: institutions, shelters, rounding | | ≈ 8,500 (3%) |

**2022 → 2025 (A I 3 and F I 1, VERIFIED).** Population +103,598; stock +50,592 (2,018,831 → 2,069,432) ≈ 90,600 people at 1.79; accommodated homeless +27,600 persons 2022→2025 (25,975 → 53,610), most of them outside private households. The three together over-explain the growth by ~15,000, i.e. within the error of the household-size assumption; no further vacancy draw-down is needed to close it, consistent with market-active vacancy being flat at 0.3% since 2022.

**Full period 2011 → 2025.** +408,212 people, +199,995 dwellings in the stock (completions 2012–25 were 188,428; the stock grew more because of conversions and the 2021 rebasing). That is **2.04 people per added dwelling** against a household size of 1.79. The excess (408,212 ÷ 1.79 = 228,000 needed vs 200,000 added ≈ 28,000) is the vacancy draw-down plus the shelter population. So the 408,000 *are* all housed. The "Lücke" is not a crowd without flats; it is three things that the census ledger makes visible:

1. **The buffer was spent.** Census vacancy 3.5% → 2.0%; market-active vacancy 2.3% (2011, 39,000 flats) → 0.3% (2024, 5,400 flats). Against a 3% reserve Berlin had a 12,000 surplus in 2011 and an 18,000 deficit in 2022 (25,000 in 2025).
2. **The shelter column grew.** 53,610 people in Unterkünfte on 31.01.2025, double 2022. They are inside the 408,000 but not inside any household statistic; at ~2 persons each they are 25,000–30,000 dwellings of demand that the ledger carries as "institutions".
3. **Who is not in the 408,000.** Households that did not form (adult children, separated couples, flat-shares) and households that went to Brandenburg instead. The census cannot see either; the Mikrozensus household-size rise (1.75 → 1.88) is suggestive but is a different household concept (Wirtschaftshaushalt) and is confounded by the 2016/2020/2022 breaks and by migration composition, so it must be shown as a hint, not a measurement. Net migration to the Berlin Umland is measurable (dataset L, still to inventory).

**Mapping onto StEP Wohnen 2040's 137,000 (p. 75–77, VERIFIED).**

| Senate component (forward, 2022–2040) | Dwellings | What the backward ledger shows for 2011–2025 |
|---|---|---|
| Restore a 3% Fluktuationsreserve from 1.1% | 41,000 | reserve drawn down by 25,600 (census) / 33,600 market-active (2011→2024); shortfall to 3% in 2025 ≈ 25,000 |
| „Linderung der Anspannung": household size back from 1.79 to 1.77, halve the rise in suburbanisation | 77,000 | not measurable in the census; Mikrozensus hint + Brandenburg migration (dataset L). Pricing the whole MZ rise 1.754→1.854 the same way would be ~112,000 (upper bound, INFERRED) |
| Replacement of demolitions/conversions | 19,000 | Bauabgang 110–923 dwellings/yr; dwellings leaving household use +9,562 in 2011–22 |
| (not in the Senate's method) | 0 | 53,610 people in shelters ≈ 25,000–30,000 dwellings |
| Demographic growth 2022–2040 | 85,000 (73,000 in the 2026 update) | the 2022–25 growth of 103,598 people already used 51,000 dwellings |

Reading: our 32,000 and the Senate's 137,000 are not rival estimates of one quantity. The 32,000 says how far building fell behind arrivals at today's household size. The 137,000 says what it would take to refill the buffer, let suppressed households form, and keep people from leaving. The ledger connects them, and the reader can set the two normative dials (reserve %, household size) and watch the need move between them.

---

## 3. One narrative: „Berlin hat Platz gemacht. Wo?"

**The premise the reader is handed.** Since 2011 Berlin has taken in 408,000 people, a city the size of Bochum. Nobody is sleeping in the Tiergarten in those numbers. So the city made room for them. The piece does not open with a shortage; it opens with a puzzle: *where did the room come from?* The reader's job is to find it, and every place they look turns out to be a place the city borrowed from. The piece never states a total shortfall. It lets the reader decide how much of what was borrowed should be paid back, and then shows what that costs in dwellings.

**The object the reader explores: the Wohnungsbilanz.** One ledger, people on the left, dwellings on the right, a year scrubber 2011→2025 and a Bezirk picker. The right side is a stack: occupied dwellings, vacant dwellings (the buffer), dwellings in other use. The left side is a stack: people in private households, people in Unterkünfte. Dragging the scrubber makes both sides grow. The reader sees, in the chosen Bezirk, the buffer thinning as the stack rises, the Unterkünfte band appearing after 2015 and doubling after 2022, and the two census years (2011, 2022) marked as the points where the ledger is exact rather than estimated. The census identity (ΔHouseholds = ΔDwellings − ΔVacant − ΔOther) is what keeps it honest, and it is printed under the chart.

**The four places to look (each is one tap on the ledger, each opens one panel, each links to one lever card).**

1. *Neu gebaut.* Tap the growth of the occupied stack. Panel: 200,000 dwellings added since 2011 housed about 88% of the newcomers; the two-line chart (arrivals at the Bezirk's household size vs completions) is here, with the honest sign per Bezirk: nine fell behind, three kept pace (Friedrichshain-Kreuzberg, Neukölln, Treptow-Köpenick). Permits-to-completions funnel and the 48,394 permitted-but-unbuilt sit in the same panel. Links to the construction levers.
2. *Aus dem Puffer.* Tap the shrinking vacancy band. Panel: 25,600 formerly vacant dwellings now occupied; vacancy by Bezirk 2011 vs 2022, every district down, Marzahn-Hellersdorf 4.1% → 1.4%; what the remaining 40,681 consist of (24,879 turnover, 9,205 under construction, 11,764 a year or more); the market-active line from 2.3% to 0.3%. Links to the vacancy and holiday-flat levers, which is where the reader who came to say "40,000 flats are empty" ends up, holding 5,400.
3. *In Unterkünften.* Tap the band on the people side. Panel: 25,975 → 53,610 people in accommodation 2022→2025, per Bezirk; LAF places 45,276. These people are counted as Berliners but not as households, so no household statistic ever shows them as demand. Links to no lever: this is the panel that explains why the Senate's own method undercounts.
4. *Gar nicht da.* Tap the empty space above the people stack. Panel: households that did not form and households that went to Brandenburg. The Mikrozensus household-size strip per Bezirk (up in 11 of 12 since 2014) is shown as a hint with its concept caveat, net migration to the Umland per year as the measurement (dataset L). This is the panel with the least certainty, and it says so. Links to the Senate's 77,000.

**The dial that replaces a conclusion.** Under the ledger sit two dials, both pre-set to the Senate's values and both movable: *Reserve* (0–5%, Senate 3%, glossary 2–5%) and *Haushaltsgröße* (1.70–2.00, Senate target 1.77, census 1.79, Mikrozensus 2025 1.88). Moving them changes one number: the dwellings Berlin would need to put back what it borrowed. At the Senate's settings that number reproduces the Senate's 137,000 components side by side with the ledger's backward measurements (the table in §2.2 is the on-screen explainer). At 2% reserve and today's household size it is a few thousand. The reader finds out that the "size of the shortage" is a choice about how much slack a city should have, and that at *any* setting above zero the answer is dwellings that do not yet exist.

**Hand-off to the lever grid (Part 2).** The number on the dial becomes the outline on the waffle (1 square = 1,000 dwellings), with the 2,069 squares of existing stock behind it. The lever cards are the same four places in reverse: *Neu bauen* (11/yr now, 19/yr in 2019; 48 permitted; LWU 4.7/yr; supermarket sites 20–36; offices ~30, all hatched-fill "also construction"), *Puffer zurückholen* (market-active 5.4; long-term vacant 11.8; Airbnb entire homes 8.4; Zweckentfremdung already returned 31.7 since 2014, ~0.5/yr for holiday flats now), *Besitzer wechseln* (Vergesellschaftung 222 recolour; LWU Ankauf 4.6/yr recolour; Vorkaufsrecht 0.07 in 2025; Sozialbindungen −46 by 2034 recolour in reverse), and the demand-side marker for the 54,000 in Unterkünfte. Cards are ordered by how often the lever is proposed, construction last. Levers stay pulled and add up; the total sits against the dial's outline. Only solid squares move the outline. The reader is not told that; the grid shows it, and the reader can still set the dial to zero and walk away unconvinced, which is the point: the piece argues by letting them try.

**Why this is one narrative and not six.** Every screen answers the same question in the same ledger: where did the room come from, and what would it take to give it back. The district chart, the vacancy map, the household-size strip, the shelter counts and the lever grid are all taps on that ledger, not chapters. The reader can stop after one tap and still have the shape of the argument; the reader who goes through all four and the dial ends up having built the Senate's 137,000 themselves, or a number of their own, with the sources attached.

---

## 4. Visualisation strategy

**Grammar (one legend for the whole piece).** Solid square = a dwelling that did not exist before. Recoloured square = the same dwelling with a new owner. Hatched square = an existing dwelling returned to the market. Dotted outline = permitted but not built. Thin outline = need. One square = 1,000 dwellings everywhere, including the Part 1 lines (annotate the 2019 peak as "19 Felder"). This single mapping is what lets Part 1 and Part 2 be read together.

**Part 1 form.** The Wohnungsbilanz of §3: a two-sided stacked ledger (people left, dwellings right) with a year scrubber 2011→2025 and a Bezirk picker (12 + Berlin). Dwelling side stacks occupied / vacant / other use; people side stacks private households / Unterkünfte. Census years 2011 and 2022 are drawn as solid ticks (exact), the years between and after as estimated (hatched edge), with the basis toggle (Zensus-basiert default; Melderegister as a labelled alternative, which makes the honesty visible instead of hiding it). The four tappable regions open the four panels; panel 1 holds the per-Bezirk two-line cumulative chart with the area filled when "need" exceeds "built" and labelled "Bau hat Schritt gehalten" when it does not. The two dials (reserve 0–5%, household size 1.70–2.00) sit under the ledger and drive the single need number that becomes the Part 2 outline. Per-Bezirk data exist for vacancy, stock, completions, permits, shelters and census households; Mikrozensus household size per Bezirk is noisy, so show the Berlin value with the Bezirk as a dot and ±0.05 as noise.

**Part 1 maps.** One map, three states: census vacancy 2011, 2022, change; a Planungsraum layer (542 LOR) for 2022 vacancy and stock is available and makes the piece feel local. Do not map the gap at LOR level: the population basis there is register only.

**Part 2 form.** A waffle of 1,000-dwelling squares, 10 per row, rendered as the Berlin stock would look at 1 square = 1,000 (2,069 squares) with the need outlines drawn on top, so the reader sees how small 32 or even 211 squares are against the stock and how large 222 recoloured squares are. Lever cards along the side, each with four fixed fields: Felder (adds / recolours / frees), Tempo (observed per year), Wer zahlt, Quelle (document + date). Pulling a lever animates its squares; levers are additive and stay pulled so the reader builds their own package and the total is shown against the two outlines. Default order on the cards: the ones most asked about first (Leerstand, Ferienwohnungen, Enteignen), construction last, so the reader discovers the conclusion rather than being told.

**Tone rules.** Expropriation card text is purely descriptive: scope, legal status (Rahmengesetz 19/2842, Anwendungsgesetz pending), what it changes (owner, rent policy) and what it does not change (number of dwellings); let the recolour do the arguing. Every number carries its reference date and spatial unit in the tooltip (e.g. "Airbnb entire-home listings, 19.09.2026 — not registered Ferienwohnungen"). Negative district gaps are labelled "Bau hat Schritt gehalten", never hidden.

**Three caveats printed under Part 1.** (1) Population is census-corrected (Zensus 2011, Fortschreibung on the 2022 basis), not the Melderegister, which shows ~78,000 more growth since 2011. (2) Household size is a dial, not a fact: the census shows ≈1.79 in both 2011 and 2022, the Mikrozensus (a different household concept, with breaks in 2016/2020/2022) shows a rise from 1.75 to 1.88; each 0.05 ≈ 5–6k dwellings. The ledger does not claim that Berliners live more densely; it shows what the need would be if they could live as they did before. (3) The need number is not a measurement; it is what it would take to restore the reserve and the household formation the dials are set to. The Senate's 137,000/138,000 is one setting of those dials (3% reserve, 1.77 persons, half the suburbanisation).

---

## 5. Data decisions taken and still open

Taken:
- Population basis: census-anchored (Zensus 2011 Bezirk anchors + A I 3 2022-basis Bezirk values for 2022–25; estimate 2012–21 per Bezirk by scaling the register with the Berlin-wide ratio and blending the Bezirk residual between the two census anchors; label "geschätzt").
- Completions flow (dwellings_total), not stock change, for the lines; stock (F I 1) only for the waffle base and the reserve calculation. Demolitions as a footnote (110–923/yr).
- Household size: Mikrozensus Tab. 7.4 Bezirk values; register-based A I 17 only as sensitivity.
- 2025 completions = 11,027 (all buildings), consistent with the series in the repo.

Open:
- Dataset L (Berlin↔Brandenburg migration by Bezirk) must be inventoried before panel 4 („Gar nicht da") has a measured component.
- Zensus 2011 persons in private households for Berlin and per Bezirk (Gemeindeblatt BEV tables) to replace the "same institutional share" assumption in the §2.2 ledger; and Zensus 2011/2022 Unterkünfte/Sonderbereiche counts per Bezirk for the people-side stack.
- The ledger for 2012–2021 and 2023–2025 per Bezirk is estimated (register scaled to the census-anchored Berlin total; vacancy interpolated between census points and the empirica series); the design marks those years as estimated and must keep doing so.
- Whether the Mikrozensus household-size rise is shortage or composition (Ukraine families 2022, ageing, concept) is unresolved; panel 4 shows it as a hint and quotes the Senate's reading rather than asserting our own. The earlier claim that Berlin housed newcomers by "packing more people per flat" is withdrawn: the census shows a flat 1.79.
- The adversarial review (brief saved at `docs/research/stage4_adversarial_review_brief.md`) has not been run.
- Secondary figures listed in §1.3 remain to be verified before publication.

---

## 6. Revision 2026-11-16: the two-round game, and „Vergesellschaften" as a lever

Sources for this section: docs/research/consolidated_findings.md (summary of all nine research passes) and docs/research/opus3_design_review.md (hostile review). Where this section conflicts with §3–§4 above, this section wins.

### 6.1 Part A becomes a two-round allocation game

**Round 1, „gezählt": Zensus 9.5.2011 → Zensus 15.5.2022.** The reader is handed 304,614 arrivals and a row of taps; each tap takes people until the count is spent. On commit the ledger reveals the census identity (ΔHH = ΔDw − ΔVacant − ΔOther = 149,403 + 25,577 − 9,562 = 165,418, exact), converted to people at the census household size of 1.79 and labelled „rechnerisch": the decomposition says how the city created room, not where any individual newcomer lives. Frame the taps as „Die Stadt hat Platz geschaffen durch …".

| Tap (German label) | Reveal, Round 1 | Tag |
|---|---|---|
| Neu gebaut | +149,403 Whg. ≈ 267,000 Menschen (88 %) | V inputs, I conversion |
| Aus leeren Wohnungen | 25,577 Whg. ≈ 46,000 (15 %); vacancy 3.5 % → 2.0 % | V / I |
| Ferienwohnungen, Gewerbe, Zweitwohnungen | −9,562 Whg. ≈ −17,000 (−6 %) | V / I |
| Enger gewohnt | ≈ 0 (± 20,000): census household size flat at ≈1.79, but the 2011 value moves between 1.773 and 1.795 with the unretrieved institutional population | I |
| In Unterkünften | nicht gemessen (statistic starts 31.01.2022); inside the residual ≈ 8,500 (3 %) with Wohnheime, care homes, noise | – |
| Umgebaut, aufgestockt | in „Neu gebaut" enthalten (F II 2 counts Baumaßnahmen an bestehenden Gebäuden) | V |
| Übernommen | 0 Menschen; Felder färben sich um | V/S |
| Gar nicht gekommen | nicht messbar in der Bilanz (Brandenburg migration, dataset L, is the only measurable piece) | – |

Use the official Gemeinde-level census totals (3,596,979 / 1,960,342 / 2,018,840), not the summed Bezirksregionen, which carry cell-key noise.

**Round 2, „geschätzt": 15.5.2022 → 31.12.2025.** 103,598 arrivals (A I 3). Reveal: stock +50,592 Whg. ≈ 90,600 people (F I 1); Unterkünfte +27,635 persons (31.01.2022 → 31.01.2025, different dates); Übernommen ≈ 5,400 Whg. (2023–2025 LWU purchases), 0 people. The parts sum to ≈114 % of the arrivals: print „Schätzung, keine Volkszählung. Die Teile ergeben mehr als 100 %, weil die Quellen sich überschneiden" (some accommodated homeless live in Trägerwohnungen inside the stock). No vacancy tap in Round 2 (no measurement; market-active stays 0.3 %).

**Bridge to 137,000.** On-screen text (from the review, to be used as is): „Berlin hat Platz geschaffen, auch indem es Reserven aufgebraucht hat. Stellen Sie ein, wie viel Reserve und wie viel Platz pro Haushalt Berlin haben sollte. Mit den Werten des Senats (3 % Reserve, 1,77 Personen je Haushalt) ergibt sich der Entlastungsbedarf von 137.000 Wohnungen: 41.000 Reserve, 77.000 Entlastung, 19.000 Ersatz (StEP Wohnen 2040). Nicht enthalten: die Menschen in Unterkünften." The two dials then carry the reader's own number into Part B as the outline.

### 6.2 The „Vergesellschaften" lever, in both parts

**What the data established (all in consolidated_findings.md §3).** No hidden pool: Zensus 2022 vacancy by owner type is 2.07 % for private housing companies against 2.02 % for Berlin, 1.91 % public, 1.07 % cooperatives; the 0.05-point difference is ≈195 flats and not meaningful. No proponent publishes a dwelling-count gain; the commission majority promises a contribution „wenn gesetzlich vorgegeben", its dissent calls it „nicht belegt und eher unplausibel", IMK (pro-feasibility on compensation) says „Neubau in großem Stil ist hier der einzige Weg". The one quantified channel is allocation: the public companies re-let 12,398–15,385 flats a year (2024–2021) and give 62–66 % to WBS holders; the campaign's 6,999/yr is 222,000 × 5 % × 63 %, gross. Transfers that already happened (≈20,000 flats 2021–2025, the 2021 sale at ≈99 % occupancy) housed nobody additional.

**Part A tap „Übernommen".** Hint: „Wohnungen, die den Besitzer wechselten." Reveal: „Rund 20.000 Wohnungen kauften die landeseigenen Gesellschaften 2021–2025. Darin wohnten schon Menschen. Zusätzlich untergebracht: praktisch niemand. Die Felder färben sich um, keins kommt dazu." Do not recolour Abwendungsvereinbarungen (no change of owner); berlinovo's ≈4,000 sit outside the KoopV LWU count, so 11,644 (2022 LWU purchases) and 14,750 (the deal) must not be added.

**Part B panel „Vergesellschaften", five fields and one card.**
1. Umfang: „222.000 Wohnungen großer Vermieter (ab 3.000 Wohnungen) gingen an eine Anstalt öffentlichen Rechts. Neue Wohnungen: 0." 222 squares recolour; say 10.7 % of all dwellings, 13.5 % of rental stock. (Expertenkommission 27.06.2023)
2. Vergabe, shown as a yearly flow on its own axis, net not gross: „Pro Jahr würden rund 3.300–5.000 Wohnungen mehr an Haushalte mit WBS vermietet als heute. Gleiche Wohnungen, andere Mieter. Die Initiative rechnet mit 7.000 (brutto). Risiko: Wer günstig wohnt, zieht seltener um (25 von 26 Studien)." Net = quota uplift over the private Bündnis's 30 % at observed turnover 3.3 % (12,398 ÷ 374,472) to 5 %. Lock-in appears as text with Kholodilin 2024; the empirica 7,200 figure (a stock, bank-commissioned, „ohne Anspruch auf Kausalität") goes to a footnote, never onto the bar.
3. Miete: „−16 % für Neuvermietete, ca. 936 € pro Haushalt und Jahr (Schätzung der Initiative, Bernt/Holm 2023)." This is the campaign's actual goal and must be visible even though the waffle cannot show it.
4. Kosten: „Entschädigung 8–36 Mrd. € (Schätzungen 2019–2026), über Kredite und Mieten finanziert. Jährliche Belastung für den Landeshaushalt: −0,3 bis +1,1 Mrd. € (DIW, je nach Entschädigung und Miete)." No compensation-to-dwellings squares: the sum is debt refinanced from rents, not a budget line that would otherwise build, and the only cost per flat we have (KG 300–400) excludes land. The slider stays, but it moves the annual budget figure from DIW Table 2, not an outline of flats.
5. Bauen? toggle, text only: „Mehrheit der Kommission: ‚verspricht einen hohen Beitrag' zum Neubau, wenn gesetzlich vorgegeben. Minderheit: ‚nicht belegt und eher unplausibel'. Initiative: eigene Neubauprojekte ‚denkbar'. Keine Zahl." Plus the risk line: „Private Wohnungsunternehmen bauten 42–46 % der neuen Wohnungen (DIW). Welcher Teil davon auf die betroffenen Konzerne entfällt, ist nicht veröffentlicht."

Vacancy card: „Stehen bei den Konzernen Wohnungen leer? Kaum mehr als anderswo: 2,1 % bei privaten Wohnungsunternehmen, 2,0 % in ganz Berlin (Zensus, 15.5.2022; Leerstand wegen Sanierung eingerechnet). Bei gleicher Quote wären das etwa 4.600 der 222.000. Nicht gemessen: Verdrängung aus bewohnten Wohnungen." Berlin level only; the Bezirk range (1.1–2.9 %) rests on small cells.

Quotes that must appear on the panel, both sides: campaign „nicht gegen Neubau" and the AöR „Neubauprojekte … denkbar"; IMK „Neubau in großem Stil ist hier der einzige Weg"; DIW „schafft keine zusätzliche Wohnung"; the commission's dissent. The campaign's „relief only above 10–20 % vacancy" line is SECONDARY and must be verified before print.

### 6.3 Changes to earlier sections
- §2.2 and §3: Round 1 is an arithmetic decomposition („rechnerisch"), not a tracking of newcomers; „Enger gewohnt" reads ≈ 0 ± 20,000 until Zensus 2011 persons in private households are fetched (Gemeindeblatt BEV).
- §4 Part 2 tone rule for expropriation is replaced by §6.2: descriptive, but with the rent field and both sides' quotes.
- §1.3 lever table: add the owner-type vacancy row (Zensus 2022 table 4000W-3006), the allocation baseline (KoopV reports 2021–2024), the transfer series (sonnet2), and Milieuschutz (82 areas, 664,504 flats, Drs. 19/25318).

### 6.4 Open items added by the review
- Zensus 2011 persons in private households (fixes the ± 20,000). Zensus 2011 vacancy by owner type.
- In-scope share of completions (Vonovia/DW Berlin completions per year) to replace „alle privaten Unternehmen".
- All-in LWU cost per flat incl. land, for any cost comparison elsewhere.
- Umwandlungen per year and LWU Wohnungstausch counts (campaign channels not yet quantified).
- BBU by Unternehmensart; 13,000-flat pledge audit; Brandenburg migration (dataset L).
- The stage 4 whole-design adversarial brief remains unrun; §6 covers only the lever and the game.
