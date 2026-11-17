# Stage 1 – Dataset inventory for "Die Lücke" (Berlin)

Verified = I opened the file/table. Inferred = from search snippets or memory, not opened.
Scratch downloads (PDF/XLSX) sit next to this file.

## Two headline caveats

**Register population is on a different basis from stock and household data.**
- The repo's population series (A I 5 Einwohnerregister) is a raw count of registrations, never corrected by a census (the 1983 Constitutional Court ruling forbids feeding census findings back into the registers).
- The dwelling stock (F I 1) is anchored to census 2011, and since the 2023 issue to the 2022 building census. The Mikrozensus household figures are weighted to the census-anchored population (census 2022 basis from 2022).
- Gap at end-2025: register 3,913,644 vs census-anchored estimate (A I 3) 3,700,577, so the register is ~213,000 higher. The gap grows over time (stale registrations from people who left, students not deregistering at home, missed deaths, and the 2022 Ukraine influx: +75,329 in the register that year).
- Dividing register population growth by survey household size, or comparing it to census-anchored stock, mixes bases and inflates "missing dwellings".

**District household size: Mikrozensus vs register-based households.**
- The district-level household size comes from the **Mikrozensus, report A I 10 / A I 11 / A VI 2, 2024 (Erstergebnisse), Table 7.4 "Haushalte im Land Berlin 2024 nach Bezirken und Haushaltsgröße"** (verified).
  - Berlin: 1,971,000 households, 3,655,000 household members, 1.9 persons per household.
- The register-based household generation (A I 17, press release 186-2025, 19.12.2025, as of 31.12.2024) gives ~2.22 million households at 1.77 persons, with 3.92 million people in private households.
- The ~250,000 difference in households follows from the population each source starts from:
  - The register-based method splits the inflated register population (~3.92m) into households, and assigns many phantom or stale registrations as single-person households.
  - The Mikrozensus is a 1% sample weighted to the census-anchored population (~3.66m in households).
  - The generation algorithm also infers households from shared addresses and names, which splits flat-shares into several "households".
- Use one source consistently: either census-anchored population with Mikrozensus household size, or register population with register-based households. Do not mix them.

## Claim checks

| Claim | Verdict | Source and figures |
|---|---|---|
| ~245,000 extra residents in the five years to 2016 | Correct for end-2011 → end-2016 on either series | Register: 3,427,114 → 3,670,622 (+243,508). Census-anchored estimate, 2011 basis: 3,326,002 → 3,574,830 (+248,828). Both on the statistik-berlin-brandenburg.de page "Melderegister, Zensus, Fortschreibung" (19.12.2024). |
| A decade added only 126,373 dwellings, +6.8% | Correct for end-2011 → end-2021, census 2011 basis | Stock 1,871,782 → 1,998,155 (+6.75%). Both values in F I 1 j/21, 2nd corrected edition. Quoted in press release 142-2022. After rebasing to the 2022 census, end-2021 is 2,014,192, so the claim only holds on the old basis. |
| F II 2 2025, 11,027 dwellings | Full calendar year 2025 | Press release no. 59, corrected version 22.05.2026 (the original had errors in text and tables). 2,127 completions. New buildings 9,524 dwellings (2024: 14,632, a fall of about 35%). Work on existing buildings 1,503 dwellings, more than doubled. Lowest total of the decade. |

The F II 2 web page shows **10,952** for 2025. That is dwellings in residential buildings only. 11,027 also includes dwellings in non-residential buildings.

## 1. Dwelling stock – Statistischer Bericht F I 1 (verified)

- **Series:** Statistische Bibliothek **BBSerie_mods_00000694**. Issues 2007–2014 and 2016–2025; there is no 2015 issue.
  - Before 2007 the series was published as F II 4.
  - Current issues: statistik-berlin-brandenburg.de/f-i-1-j/ (2024 and 2025, PDF and XLSX). Older issues are PDF only.
- **District table (Table 2, 31.12.):**
  - Wohnungen insgesamt in residential and non-residential buildings, including Wohnheime.
  - Dwellings by number of rooms (1, 2, 3, 4, 5, 6, 7 or more).
  - Räume.
  - Wohnfläche in 100 m².
  - Dwellings and Wohnfläche in non-residential buildings.
- **Other tables:**
  - Table 4: Wohnfläche and rooms per dwelling by district.
  - Table 6: Wohngebäude by size (1, 2, 3+ dwellings) and district.
  - Since the 2023 issue, Tables 7–18 give Planungsraum detail (LOR 2021, 542 areas): dwellings by rooms, Räume, Wohnfläche, Wohngebäude. The 2025 XLSX has one sheet per district.
- **Not available:** a breakdown by construction year.
- **Rebasing (verified):**
  - Pre-2011 basis (GWZ 1987 West / GWZ 1995 East): end-2011 stock 1,903,231. On the census 2011 basis: 1,871,782. Jump of **−31,449**.
    - The definition of rooms also changed: kitchens are counted from then on, and 1-room dwellings went from 26,188 to 73,189.
  - End-2021: 1,998,155 on the census 2011 basis vs 2,014,192 on the 2022 GWZ basis. Jump of **+16,037**.
    - Since 2023 the reports only show the series "since 2021" on the new basis.
  - Stock end-2025: **2,069,432** (+10,766 on 2024). +55,240 for 2021–2025.
- **Example district values, 31.12.2023:** Pankow 226,992; Mitte 213,666; Reinickendorf 133,303.
- **Stock change vs completions:** 2025 completions 11,027 minus 110 dwellings demolished = 10,917, against a stock change of 10,766. The residual (~150) is conversions, homes and similar.
- **Observations:** 12 districts × ~19 years, or 542 Planungsräume × 3 years (2023–2025).

## 2. Bauabgang – F II 2 (verified)

- **Tables (2025 XLSX):**
  - Table 19: Abgang im Wohnbau including parts of buildings, by building type, owner and building age. No district.
  - Table 20: whole residential buildings.
  - Table 23: whole buildings by cause **and district** (buildings, dwellings, floor area).
- **Berlin, dwellings in residential buildings:**

| Year | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|
| Dwellings | 175 | 130 | 593 | 572 | 338 | 532 | 923 | 322 | 167 | 110 |

- In 2025, 83 of the 106 dwellings lost with whole buildings were demolished to build new housing. Removals are 1–5% of completions, so they can be ignored or shown as a footnote.

## 3. Bauüberhang – F II 2, Tables 16–18 (verified)

- **Table 16:** residential buildings. **Table 17:** dwellings. **Table 18:** non-residential.
- **Columns:**
  - Bauüberhang insgesamt (including work on existing buildings).
  - Dwellings in new buildings: total; unter Dach; noch nicht unter Dach; noch nicht begonnen; erloschene Genehmigungen.
- **Row blocks:**
  - Building type (1, 2, 3+ dwellings, Wohnheime).
  - Bauherr (public, companies including housing companies, private households and others).
  - Genehmigungszeitraum (half-years of the last two years, previous year, "2022 und früher"). In Table 16 only.
  - District.
- **2025, dwellings:** 48,394 total. New buildings: 40,937, of which 12,901 unter Dach, 12,252 noch nicht unter Dach, 15,784 noch nicht begonnen. Erloschen: 3,055.
- **2025 by district:**

| District | Total | Not started |
|---|---|---|
| Treptow-Köpenick | 6,546 | 1,626 |
| Lichtenberg | 6,190 | 1,284 |
| Spandau | 5,113 | 1,238 |
| Marzahn-Hellersdorf | 4,623 | 1,860 |
| Mitte | 4,529 | 1,304 |
| Charlottenburg-Wilmersdorf | 4,345 | 1,757 |
| Pankow | 3,444 | 1,683 |
| Neukölln | 3,123 | 898 |
| Reinickendorf | 2,938 | 1,838 |
| Tempelhof-Schöneberg | 2,608 | 963 |
| Friedrichshain-Kreuzberg | 2,483 | 455 |
| Steglitz-Zehlendorf | 2,452 | 878 |

- **Berlin totals, dwellings in residential buildings:**

| Year | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|
| Dwellings | 50,825 | 58,460 | 63,403 | 65,047 | 65,661 | 65,270 | 61,534 | 58,029 | 49,554 | 48,394 |

  Source: BF_BA_BU_Diagramm.xlsx on the F II 2 page, which also gives completions and demolitions 2016–2025.
- **Observations:** 12 × ~15 years × 4 stages.

## 4. Baugenehmigungen – F II 1

- **Monthly report** "F II 1 – m", file names SB_F02-01-00_YYYYmMM_BE.pdf (verified to exist, e.g. 2025m08). Older issues back to at least 2005 as SB_F2-1_mMM-YY_BE.pdf.
- **Annual report** "F II 1 – j" on statistik-berlin-brandenburg.de/f-ii-1-j/, PDF and XLSX.
- **Inferred:** district tables (permits for new residential buildings, dwellings, floor area, costs by district).
- **Series ID:** not resolved. A combined permits and completions series from 1992 is BBSerie_mods_00001217.
- **Access:** one PDF per month. The annual XLSX is sufficient for a yearly panel.

## 5. Population

**(a) Einwohnerregister**
- **A I 5** (BBSerie_mods_00000260), half-yearly 2007/02–2026/01.
  - The current issue (2025 h2, verified) has district tables (Table 3, since 2014), Ortsteile (Tables 11–13) and postcodes (Table 14).
  - It no longer has Planungsraum tables.
- **A I 16** "Einwohnerregisterstatistik … Bestand – LOR-Planungsräume" (verified title of 2024 h2), half-yearly. This is the Planungsraum source.
- **Open data** "Einwohnerinnen und Einwohner in Berlin in LOR-Planungsräumen am 31.12.YYYY" (CSV, CC-BY).
  - Exists through 31.12.2025, published 02.04.2026.
  - daten.berlin.de returned 403 to me, so columns are **not verified**.
  - Inferred schema: ZEIT, BEZ, PGR, BZR, PLR, STADTRAUM, E_E, E_EM, E_EW, then age-band columns.
  - There is a LOR boundary break between 2020 (LOR 2006/2019) and 2021+ (LOR 2021).

**(b) Bevölkerungsfortschreibung – A I 3 (verified for 2025)**
- **Table 1** by district on the census 2022 basis, 2022–2025: start-of-year stock, births, deaths, moves in and out across the district boundary, end-of-year stock. Tables 2–3 add citizenship and sex.
- **Berlin end-of-year, census 2022 basis:**

| Year | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Population | 3,632,853 | 3,662,381 | 3,685,265 | 3,700,577 |

- **Old basis:** Berlin on the census 2011 basis 2011–2021: 3,326,002 … 3,677,472. End-2022 on the old basis: 3,755,251.
  - **District values on the 2011 basis: not confirmed.** This needs checking in older A I 3 issues.
- **Census corrections:**
  - Census 2011 (9.5.2011): 3,292,365, which is **−179,391 (−5.2%)** against the previous estimate. zensus2011.de press release 152.
  - Census 2022 (15.5.2022): **3,596,999**, which is **−128,651** against the previous estimate of 3,725,650 (release 25.06.2024). The office's later table lists 3,598,006, apparently a revised value.

**Recommendation:** use the census-anchored estimates (A I 3) for the headline. They are on the same basis as F I 1 stock and Mikrozensus households. Keep the register as a sensitivity layer. See the caveat at the top.

## 6. Household size

- **Mikrozensus A I 10 / A I 11 / A VI 2** (joint annual report).
  - 2024 Table 4.1: Berlin 1,971k households, 1.9 persons.
  - 2024 Table 7.4: district households and household size (verified):

| District | Persons per household |
|---|---|
| Mitte | 1.8 |
| Friedrichshain-Kreuzberg | 1.7 |
| Pankow | 1.9 |
| Charlottenburg-Wilmersdorf | 1.8 |
| Spandau | 2.0 |
| Steglitz-Zehlendorf | 2.0 |
| Tempelhof-Schöneberg | 1.9 |
| Neukölln | 1.8 |
| Treptow-Köpenick | 1.9 |
| Marzahn-Hellersdorf | 1.9 |
| Lichtenberg | 1.8 |
| Reinickendorf | 2.0 |

  - District household counts are in thousands, from 123 (Spandau) to 218 (Pankow).
  - Values are rounded to one decimal; compute members ÷ households from the table for more precision.
  - Berlin 2011–2023: **not extracted**. Inferred ~1.8–1.9 per year from the same table in earlier issues.
  - Breaks: Mikrozensus redesign in 2020; census 2022 weighting from 2022.
- **A I 17 "Haushalte" from household generation** (BBSerie_mods_00001585, 2022–2025): register-based, at Planungsraum and district level.
  - 31.12.2024: ~2.22m households, 1.77 persons, 56.5% single-person (Friedrichshain-Kreuzberg 63.0%, Marzahn-Hellersdorf 48.4%).
  - A Planungsraum XLSX is linked from press release 186-2025.
- **Census 2011 and census 2022:** household counts available (2022 via "Lokale Daten Berlin" at Bezirksregion and Planungsraum level). Values not extracted.
- **IBB Wohnungsmarktbericht table volume:** district household size (inferred to be register-based).

## 7. Census 2022 building and dwelling census (GWZ); census 2011 GWZ

- **Berlin, 15.05.2022:** 40,681 vacant dwellings (1.97%). 11,764 vacant 12 months or longer. Source: Drucksache 19/20607, answer of 30.10.2024.
- **Vacancy reasons:**

| Reason | All vacant | Vacant 12+ months |
|---|---|---|
| Available within 3 months | 24,879 | 4,014 |
| Construction work | 9,205 | 4,839 |
| Demolition | 678 | 456 |
| Sale | 1,464 | 456 |
| Own use | 767 | 414 |
| Other | 3,686 | 1,584 |

- **Spatial detail:** statistics office "Lokale Daten Berlin" offers 35 characteristics (population, households, families, buildings and dwellings: number of dwellings, ownership, rented share, heating, vacancy) for 182 Bezirksregionen, 542 Planungsräume and blocks, as Excel. These can be summed to districts.
- **Zensus database** (ergebnisse.zensus2022.de, GENESIS-style tables such as "Wohnungen: Grund des Wohnungsleerstands"): JavaScript only, not opened. Whether Berlin districts are a regional level there is **unverified**.
  - Vacancy rates reported for old districts: Weißensee 2.7%; Steglitz, Wedding, Kreuzberg and Neukölln 2.3%; Köpenick 0.9%.
- **Construction year by district:** not confirmed.
- **Census 2011 GWZ:** equivalent variables in the Zensus 2011 database (vacancy, ownership, construction year). Not checked.

## 8. Demand and plans

- **StEP Wohnen 2040** (Senate decision 03.09.2024, PDF report and brochure).
  - 222,000 dwellings needed 2022–2040: 137,000 existing deficit plus 85,000 from demographic growth.
  - Phasing: 100,000 by end-2026, 50,000 more by 2031, 72,000 by 2040. Land reserve for a further 50,000.
  - Focus districts: Pankow, Lichtenberg, Marzahn-Hellersdorf, Treptow-Köpenick.
  - The 137,000 deficit is the best official benchmark against which to check the "Lücke" estimate.
- **Bevölkerungsprognose für Berlin und die Bezirke 2024–2040** (SenStadt, decided 2025; Drucksache 19/2765, 11.11.2025).
  - Base: register 31.12.2023. Berlin reaches 4.006m in 2040 (+109,000).
  - 58 Prognoseräume plus districts. Treptow-Köpenick +9.6%; 4 districts shrink slightly.
  - PDF report plus overview tables; whether those are XLSX is unconfirmed.
- **IBB Wohnungsmarktbericht 2025:** PDF, summary, XLSX Tabellenband, district factsheets.
  - District indicators: population, households, household size, completions, rents, forecast to 2040.
  - No district vacancy or demand series seen.
- **Senate target of 20,000 per year:** not separately verified. The coalition target is consistent with the StEP phasing (100,000 in 2022–2026).

## (a) Summary table

| Dataset | Code / ID | Lowest granularity | Years | Format | Rows (approx.) |
|---|---|---|---|---|---|
| Completions (in repo) | F II 2, BBSerie 00000448 | District | 1990–2025 | PDF; XLSX recent | 12×16 |
| Stock | F I 1, BBSerie 00000694 | Planungsraum (from 2023); district | 2007–2025, no 2015 | PDF; XLSX 2024+ | 12×19; 542×3 |
| Demolitions | F II 2, Tables 19–23 | District (whole buildings) | annual | PDF/XLSX | 12×15 |
| Bauüberhang | F II 2, Tables 16–17 | District × stage | annual, 31.12 | PDF/XLSX | 12×15×4 |
| Building permits | F II 1 m / j | District (inferred) | monthly | PDF; XLSX annual | 12×180 |
| Register population (in repo) | A I 5, BBSerie 00000260; A I 16 | Planungsraum | half-yearly 2007–2026 | PDF; CSV open data | 542×15 |
| Census-anchored population | A I 3 | District (2022 basis) | 2022–2025 (new basis) | PDF/XLSX | 12×4 |
| Mikrozensus households | A I 10/11 | District | annual | PDF/XLSX | 12×14 |
| Register households | A I 17, BBSerie 00001585 | Planungsraum | 2022–2025 | PDF/XLSX | 542×4 |
| Census 2022 GWZ | Zensus DB; Lokale Daten | Block | 2022 | XLSX | 542×35 |
| StEP 2040 / Prognose / IBB | — | Prognoseraum / district | 2024–2040 | PDF/XLSX | small |

## (b) Open questions that change the design most

1. **Population basis.** Register (smooth, ~213,000 too high by 2025) vs census-anchored (consistent, but breaks in 2011/2022, and district values on the 2011 basis are unconfirmed). If district estimates on the old basis are missing, scale the register by the Berlin-wide ratio of estimate to register for each year.
2. **Flow or stock.** Completions are continuous. Stock change carries the −31,449 jump (2011) and the +16,037 jump (2021), which must be chained or flagged.
3. **Household size source and dynamics.** Mikrozensus 1.9 vs register-based 1.77. That changes "missing dwellings" by about 7% (≈9,000 dwellings per 240,000 residents). Also choose between a fixed baseline (e.g. 2011) and a size that varies by year and district. Falling household size itself creates demand.
4. **Completion definition.** All dwellings (11,027) vs new residential buildings (9,431 in 2025). Conversions doubled in 2025, so the choice matters most in recent years.

## (c) Recommended minimal file set for a district × year panel 2011–2025

1. **Completions:** already in the repo (dwellings_total).
2. **Stock:** F I 1 PDFs 2011–2014 and 2016–2021 (census 2011 basis), plus the **SB_F01-01-00_2025j01_BE.xlsx** (2021–2025, GWZ 2022 basis). Use stock change 2014→2016 for the missing 2015 issue, or interpolate. Add a `basis` column.
3. **Bauüberhang and demolitions:** **SB_F02-02-00_2025j01_BE.xlsx** and the 2024 XLSX, plus older F II 2 PDFs (already downloaded for completions): Table 17 district rows and Table 23.
4. **Population:** **A I 3 2025 XLSX** (districts 2022–2025, census 2022 basis). For 2011–2021, older A I 3 issues if they have district tables; otherwise register × Berlin estimate/register ratio. Keep register values as an alternative column.
5. **Household size:** Mikrozensus A I 10 issues 2011–2024, district table (7.4 in 2024). Minimal fallback: 2024 district values held constant, with A I 17 register-based households as a sensitivity check.

## Sources
- https://www.statistik-berlin-brandenburg.de/f-ii-2-j/ (and BF_BA_BU_Diagramm.xlsx, SB_F02-02-00_2025j01_BE.xlsx)
- https://www.statistik-berlin-brandenburg.de/f-i-1-j/ (SB_F01-01-00_2025j01_BE.xlsx); https://www.statistischebibliothek.de/mir/receive/BBSerie_mods_00000694
- https://www.statistik-berlin-brandenburg.de/presse/2026/59-baufertigstellungen-2025-berlin/
- https://www.statistik-berlin-brandenburg.de/142-2022/
- https://www.statistik-berlin-brandenburg.de/news/2024/zensus-melderegister/
- https://download.statistik-berlin-brandenburg.de/81bee49d8f2e3592/357676576a09/SB_A01-03_00_2025j01_BE.pdf
- https://download.statistik-berlin-brandenburg.de/b50a3a074782ec0e/e0095590e436/SB_A01-05-00_2025h02_BE.pdf
- https://download.statistik-berlin-brandenburg.de/9673209d56d43e64/bd35b2b2f78d/SB_A01-16-00_2024h02_BE.pdf
- https://download.statistik-berlin-brandenburg.de/e5a88f61949ce1dc/6541131bf63f/SB_A01-10-00_2024j01_BE.pdf
- https://www.statistik-berlin-brandenburg.de/186-2025/
- https://www.zensus2011.de/SharedDocs/Pressemitteilungen/DE/2013_Archiv/BE_BB/PM152_Veroeffentlichung_erster_Ergebnisse_des_Zensus_2011_fuer_das_Land_Berlin.html
- https://pardok.parlament-berlin.de/starweb/adis/citat/VT/19/SchrAnfr/S19-20607.pdf
- https://www.statistik-berlin-brandenburg.de/zensus22/lokale-daten-berlin/
- https://www.berlin.de/rbmskzl/aktuelles/pressemitteilungen/2024/pressemitteilung.1481557.php
- https://www.berlin.de/sen/stadt/_assets/stadtdaten/stadtwissen/bevoelkerungsprognose-2024-2040/bericht_bevoelkerungsprognose-fuer-berlin-und-die-bezirke-2024-2040.pdf
- https://www.ibb.de/de/ueber-uns/publikationen/wohnungsmarktbericht/2025.html
