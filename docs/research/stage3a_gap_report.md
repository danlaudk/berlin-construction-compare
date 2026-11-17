# Stage 3a – Household-based housing gap per Bezirk (Berlin, 2011–2025)

Research date 2026-11-15. **VERIFIED** = number read in a primary source I opened. **INFERRED** = my arithmetic or an assumption. All arithmetic scripts and downloads are in this scratchpad (`z22.py`, `z11.py`, `cmp.py`, `gap.py`, `z11/`, `mz/`, `z22br.xlsx`, `step.pdf`, `ce_*.pdf`).

## 0. Bottom line

- **Census-consistent gap, Berlin, 9.5.2011 → 31.12.2025: about 32,000 dwellings** (definition ii). The sensitivity range on census-consistent bases is 16,000–44,000.
- **The register-based version (about 74,000) is not defensible.** It divides register growth, which overstates by about 78,000 people over this period versus the census-anchored series, by a survey household size.
- **The direct census comparison (households vs dwellings, 2011→2022) shows only +16,000.** But census households are *Wohnhaushalte*, built by assigning every person at an address to a dwelling. So they cannot show doubling-up; the shortage appears only as vacancy falling from 3.5% to 2.0%.
- **Household size is rising, not falling** (Mikrozensus 1.75 in 2011 to 1.88 in 2025). This is the hidden part of the shortage (later moving out, flat-sharing). It is exactly what StEP's "Entlastungsbedarf" tries to capture.
- **Against a 3% reserve, the 2025 shortfall is about 25,000** (2%: 5,000). In 2011 the same calculation gave a 12,000 surplus, so the swing is ≈37,000, consistent with definition ii.

---

## 1. Census-to-census per Bezirk (Task 1)

### Sources (VERIFIED)
- **Zensus 2011 (9.5.2011):** Amt für Statistik BB "Gemeindeblätter" per Bezirk, two PDFs each: `11xx_<Bezirk>_BEV.pdf` (population, households) and `11xx_<Bezirk>_GWZ.pdf` (buildings/dwellings, also households by size). Linked from statistik-berlin-brandenburg.de/bevoelkerung/zensus/zensus_2011/ergebnisse-berlin/ → statistischebibliothek.de (e.g. BBHeft_derivate_00004784/1111_Lichtenberg_GWZ.pdf). Berlin sheets `11_Berlin_Bev.pdf`, `11_Berlin_GWZ.pdf`. Used: BEV table 1 "Insgesamt"; GWZ table 2.1 "Wohnungen in Gebäuden mit Wohnraum" (Insgesamt, incl. Wohnheime) and "Leer stehend"; households by size from GWZ.
  - Berlin checks: population 3,292,365; dwellings 1,869,437; vacant 66,277 (Berlin GWZ table 2.2.1). The Bezirk sums reproduce these exactly.
- **Zensus 2022 (15.5.2022):** "Kleinräumige Daten Berlin – Zensus 2022, Ebene Bezirksregionen" (`Zensus_2022_BE_SKA_110000000000_Bezirksregionen.xlsx`, statistik-berlin-brandenburg.de/zensus22/lokale-daten-berlin/). Sheets 1.1 (population), 3.2 (households by size), 4.1 (dwellings by building type), 4.9 (use incl. "Leer stehend"), 4.14 (vacancy duration). The 143 Bezirksregionen are summed to Bezirke via the first two digits of BZR_ID.
  - Berlin "Insgesamt" rows: population 3,596,999; private households 1,960,342; dwellings 2,018,831 (incl. 25,025 in Wohnheimen); vacant 40,681; vacant 12+ months 11,764.
  - The Bezirksregion sums differ by ≤ 20 from these totals because of cell-key secrecy (SKA).

### Table 1 – Census 2011 vs Census 2022 (VERIFIED inputs; differences INFERRED)

"Other" = dwellings − vacant − households. It covers holiday flats, commercially used flats and dwellings with no generated household.

| Bezirk | Pop 2011 | HH 2011 | Dw 2011 | Vac 2011 | Vac% | Pop 2022 | HH 2022 | Dw 2022 | Vac 2022 | Vac% | ΔHH | ΔDw | ΔHH−ΔDw | Other 2011 | Other 2022 | HH size 2011* | HH size 2022* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Mitte | 316,507 | 180,168 | 188,050 | 7,440 | 4.0 | 357,319 | 205,001 | 211,686 | 4,741 | 2.2 | +24,833 | +23,636 | +1,197 | +442 | +1,944 | 1.79 | 1.70 |
| Friedrichshain-Kreuzberg | 251,226 | 141,233 | 145,673 | 4,339 | 3.0 | 264,032 | 153,283 | 157,558 | 3,180 | 2.0 | +12,050 | +11,885 | +165 | +101 | +1,095 | 1.79 | 1.68 |
| Pankow | 355,361 | 198,874 | 205,078 | 6,196 | 3.0 | 400,405 | 218,855 | 224,214 | 4,298 | 1.9 | +19,981 | +19,136 | +845 | +8 | +1,061 | 1.80 | 1.78 |
| Charlottenburg-Wilmersdorf | 290,741 | 172,630 | 181,166 | 5,985 | 3.3 | 317,006 | 187,482 | 194,165 | 4,820 | 2.5 | +14,852 | +12,999 | +1,853 | +2,551 | +1,863 | 1.70 | 1.64 |
| Spandau | 214,235 | 110,330 | 116,975 | 5,210 | 4.5 | 237,761 | 121,145 | 126,800 | 3,025 | 2.4 | +10,815 | +9,825 | +990 | +1,435 | +2,630 | 1.92 | 1.91 |
| Steglitz-Zehlendorf | 277,078 | 145,405 | 153,798 | 5,780 | 3.8 | 295,126 | 155,286 | 162,188 | 3,920 | 2.4 | +9,881 | +8,390 | +1,491 | +2,613 | +2,982 | 1.91 | 1.86 |
| Tempelhof-Schöneberg | 316,936 | 173,755 | 180,002 | 5,949 | 3.3 | 331,283 | 182,432 | 186,619 | 3,205 | 1.7 | +8,677 | +6,617 | +2,060 | +298 | +982 | 1.84 | 1.78 |
| Neukölln | 298,552 | 155,929 | 161,694 | 5,735 | 3.5 | 305,021 | 162,760 | 167,358 | 3,582 | 2.1 | +6,831 | +5,664 | +1,167 | +30 | +1,016 | 1.92 | 1.83 |
| Treptow-Köpenick | 237,881 | 128,011 | 131,501 | 3,586 | 2.7 | 275,543 | 148,051 | 151,361 | 2,530 | 1.7 | +20,040 | +19,860 | +180 | −96 | +780 | 1.86 | 1.82 |
| Marzahn-Hellersdorf | 243,893 | 126,114 | 131,654 | 5,440 | 4.1 | 270,007 | 138,233 | 140,977 | 2,040 | 1.4 | +12,119 | +9,323 | +2,796 | +100 | +704 | 1.93 | 1.90 |
| Lichtenberg | 252,197 | 140,302 | 144,971 | 4,694 | 3.2 | 290,539 | 159,148 | 163,237 | 2,636 | 1.6 | +18,846 | +18,266 | +580 | −25 | +1,453 | 1.79 | 1.77 |
| Reinickendorf | 237,758 | 122,185 | 128,875 | 5,923 | 4.6 | 252,937 | 128,678 | 132,677 | 2,723 | 2.1 | +6,493 | +3,802 | +2,691 | +767 | +1,276 | 1.93 | 1.91 |
| **Berlin (Σ)** | **3,292,365** | **1,794,936** | **1,869,437** | **66,277** | **3.5** | **3,596,979** | **1,960,354** | **2,018,840** | **40,700** | **2.0** | **+165,418** | **+149,403** | **+16,015** | **+8,224** | **+17,786** | 1.84 | 1.79 |

\*Persons in households estimated from the size classes, with "6 and more" set to 6.5 persons (INFERRED; the 2011 estimate slightly exceeds total population, so read these as ±0.02). Census household size falls because these are *dwelling* households (next point), not because people live more spaciously.

**Reading.**
- Census households grew 165,000 and dwellings 149,000 (VERIFIED inputs). The 16,000 difference is almost entirely the **fall in vacancy (−25,600)**, partly offset by "other" non-household dwellings rising by 9,600.
- Vacancy fell in every Bezirk. The steepest fall was in Marzahn-Hellersdorf (4.1% → 1.4%), with Reinickendorf (4.6% → 2.1%) and Spandau (4.5% → 2.4%) next.
- **Why the census cannot show a bigger gap.** The 2011 BEV Gemeindeblatt states that the household generation "anschriftenweise Personen zu Haushalten zusammengefasst und den in der Gebäude- und Wohnungszählung erfassten Wohnungen zugeordnet … bildet daher die Wohnhaushalte an einer Anschrift ab" (VERIFIED, introduction of 1101_Mitte_BEV.pdf). So every occupied dwelling holds exactly one census household by construction. Adult children who cannot move out, or a couple who split but still share a flat, never appear as an extra household. Definition (iii) therefore measures only *vacancy absorption*, a lower bound.
- **Dwellings grew faster in the census than in completions.** Census Δdwellings 2011→2022 was +149,403, against completions May 2011–May 2022 of ≈138,000 (INFERRED, pro-rated). The F I 1 stock change 2011→2021 on the old basis was only +126,373. The difference (conversions, attic flats and Fortschreibung drift) is the +16,037 rebasing jump Stage 1 found.

### The 1,983,000 vs 1,960,342 conflict
- **1,960,342** is the Zensus 2022 count of *private households* (Wohnhaushalte at the main residence; persons in Gemeinschaftsunterkünfte excluded), from the SKA Berlin total row (VERIFIED). This is the census number.
- **1,943,000** is Mikrozensus 2022 in the revised edition `SB_A01-10-00_2022j01_BE-end-rev2022`, table 7.4 (VERIFIED). The Mikrozensus counts households at the main residence by the *Wirtschaftshaushalt* concept, which splits shared flats when budgets are separate.
- **1,983,000:** I did not find this in any primary source I opened. The search engine attributed it to IBB Wohnungsmarktbericht 2023 (not opened). Most likely it is the Mikrozensus 2022 *Erstergebnis* weighted to the old census-2011-basis population (3.76m, about 130,000 too high). That would shift households by about 70,000 at 1.85 persons, which fits (INFERRED).
- Recommendation: use the census 1,960,342 for stock comparisons and do not use 1,983,000.

---

## 2. Mikrozensus household series (Task 2)

### Berlin (VERIFIED)
- 2011–2019: A I 11 j/19, table 7.1/7.2 "Privathaushalte im Land Berlin 2011 bis 2019" (BBHeft_derivate_00023088). Footnote: 2011–12 re-weighted to the census-2011 Fortschreibung.
- 2021–2025: A I 10/A I 11/A VI 2 joint reports, table 7.4.
- Size is computed as persons ÷ households.

| Year | Households (1,000) | Persons in HH (1,000) | Persons/HH | Note |
|---|---|---|---|---|
| 2011 | 1,877.8 | 3,293.4 | 1.754 | re-weighted to census 2011 |
| 2012 | 1,910.2 | 3,346.5 | 1.752 | re-weighted |
| 2013 | 1,932.5 | 3,386.0 | 1.752 | |
| 2014 | 1,963.2 | 3,443.1 | 1.754 | |
| 2015 | 1,998.3 | 3,487.4 | 1.745 | |
| 2016 | 1,964.3 | 3,529.8 | 1.797 | new sample from 2016 (level shift in single-person HH) |
| 2017 | 2,002.9 | 3,591.4 | 1.793 | |
| 2018 | 2,026.3 | 3,622.7 | 1.788 | |
| 2019 | 2,033.7 | 3,638.1 | 1.789 | |
| 2020 | – | – | – | redesign year; Berlin issue not in the library (only a BB-korr file). **Break.** |
| 2021 | 1,945 | 3,509 | 1.80 | edition "end-rev2022" |
| 2022 | 1,943 | 3,567 | 1.84 | edition "end-rev2022" (census 2022 weighting) |
| 2023 | 1,961 | 3,633 | 1.85 | endgültig |
| 2024 | 1,971 | 3,655 | 1.85 | Erstergebnis |
| 2025 | 1,953 | 3,663 | 1.88 | Erstergebnis (SB_A01-10-00_2025j01_BE.pdf) |

There are two breaks. In 2016 a new sample was drawn. In 2020 the Mikrozensus was integrated with EU-SILC and LFS, and from 2022 it is weighted to census 2022. Within each segment the size **rises** (2011–15 flat at 1.75; 2016–19 at 1.79; 2021–25 from 1.80 to 1.88). StEP Wohnen 2040 reads the same rise (1.75 in 2013 to 1.79 in 2019) as a shortage symptom (section 6 below). **There is no evidence of falling household size creating extra demand. The opposite is true: households are being suppressed.**

### Per Bezirk (VERIFIED)
- 2011 and 2014: A I 11 table 6.2 (2011 on the *old* pre-census weighting, Berlin 1,995.4k; Bezirk shares usable, levels not).
- 2024 and 2025: table 7.4. The 2024 and 2025 sizes are members ÷ households from the 1,000-rounded table.

| Bezirk | 2011 (old weights) | 2014 | 2019 | 2024 | 2025 |
|---|---|---|---|---|---|
| Mitte | 1.65 | 1.71 | 1.7 | 1.82 | 1.88 |
| Friedrichshain-Kreuzberg | 1.64 | 1.71 | 1.7 | 1.73 | 1.74 |
| Pankow | 1.64 | 1.65 | 1.8 | 1.86 | 1.77 |
| Charlottenburg-Wilmersdorf | 1.64 | 1.67 | 1.7 | 1.76 | 1.77 |
| Spandau | 1.79 | 1.72 | 1.9 | 1.96 | 1.98 |
| Steglitz-Zehlendorf | 1.84 | 1.81 | 1.9 | 1.97 | 1.96 |
| Tempelhof-Schöneberg | 1.76 | 1.82 | 1.8 | 1.86 | 1.89 |
| Neukölln | 1.80 | 1.87 | 1.8 | 1.79 | 1.83 |
| Treptow-Köpenick | 1.75 | 1.76 | 1.8 | 1.90 | 1.93 |
| Marzahn-Hellersdorf | 1.86 | 1.85 | 1.9 | 1.93 | 1.98 |
| Lichtenberg | 1.73 | 1.69 | 1.7 | 1.79 | 1.88 |
| Reinickendorf | 1.91 | 1.88 | 2.0 | 2.01 | 1.98 |
| Berlin | 1.74 | 1.75 | 1.8 | 1.85 | 1.88 |

Household size rose 2014→2024 in 11 of 12 Bezirke. Neukölln is roughly flat. District values carry sampling error (household counts are ~120–230 thousand, with cells in brackets for small groups), so read single-year changes of ±0.05 as noise.

---

## 3. Census-anchored population per Bezirk (Task 3)

- **A I 3 issues on the census-2011 basis contain no Bezirk tables.** I checked the 2021 issue (`SB_A01-03-00_2021j01_BE.pdf`): Table 1 covers Berlin only, 2018–2021, ending at 3,677,472. The 2022 old-basis issue has no Bezirk tables either. VERIFIED.
- **The 2025 issue has Bezirk tables on the census-2022 basis** (Table 1/2, with Bezirk pages for 2022–2025). End-2025 values (VERIFIED):

| Mitte | F-Kreuzberg | Pankow | Charl.-Wilm. | Spandau | Steglitz-Z. | Tempelhof-S. | Neukölln | Treptow-K. | Marzahn-H. | Lichtenberg | Reinickendorf | Berlin |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 365,741 | 267,258 | 411,133 | 323,712 | 248,122 | 295,082 | 339,042 | 309,241 | 293,681 | 285,222 | 305,118 | 257,225 | 3,700,577 |

- **No chaining is needed for the 2011→2025 comparison.** Both endpoints are census-anchored: the census of 9.5.2011 per Bezirk (Gemeindeblätter) and the A I 3 end-2025 figure built on census 2022. Census-anchored growth is +408,212 (Berlin), against register growth (end-2011→end-2025) of +486,530, so the register overstates growth by ≈78,000.
- **For intermediate years 2012–2021, scale per year.** Use the register per Bezirk multiplied by the Berlin-wide ratio (A I 3 Berlin ÷ register Berlin) for that year. Then linearly blend the residual Bezirk-specific error between the two census points. That residual is the census Bezirk value ÷ register Bezirk value at 2011 and at 2022. This is INFERRED and still needs to be built; label it "geschätzt".

---

## 4. Gap definitions compared (Task 4)

### Inputs
- **Completions:** repo `berlin_completions_wide.csv`, 2012–2025 summed. The Bezirk sum equals the Berlin column, 188,428.
- **MZ 2024 household size:** Section 2.
- **Stock 2025:** F I 1 2025 XLSX Tab. 2 (VERIFIED).
- **Households 2025:** census-2022 households × (A I 3 pop 2025 ÷ census pop 2022) per Bezirk. This holds census household size constant (INFERRED).

### Definitions
Positive = shortfall.
- **(i)** (register Δ end-2011→end-2025) ÷ MZ-2024 size − completions 2012–25.
- **(ii)** (census-anchored Δ 9.5.2011→31.12.2025) ÷ MZ-2024 size − completions 2012–25.
- **(iii)** census ΔHH − census ΔDw, 2011→2022 (no size assumption).
- **(iv)** (est. HH 2025 − census HH 2011) − (F I 1 stock 2025 − census Dw 2011).

### Table 4a

| Bezirk | Register Δpop | Census-anch. Δpop | MZ24 size | Completions 2012–25 | (i) register | (ii) census-anch. | (iii) census 2011–22 | (iv) HH vs stock 2011–25 |
|---|---|---|---|---|---|---|---|---|
| Mitte | 64,727 | 49,234 | 1.82 | 23,201 | +12,346 | +3,837 | +1,197 | +2,074 |
| Friedrichshain-Kreuzberg | 27,428 | 16,032 | 1.73 | 13,831 | +2,048 | −4,549 | +165 | −162 |
| Pankow | 63,879 | 55,772 | 1.86 | 24,737 | +9,563 | +5,210 | +845 | +1,076 |
| Charlottenburg-Wilmersdorf | 28,714 | 32,971 | 1.76 | 11,639 | +4,706 | +7,129 | +1,853 | +2,022 |
| Spandau | 40,621 | 33,887 | 1.96 | 11,307 | +9,425 | +5,988 | +990 | +1,978 |
| Steglitz-Zehlendorf | 15,646 | 18,004 | 1.97 | 8,094 | −165 | +1,030 | +1,491 | +489 |
| Tempelhof-Schöneberg | 29,474 | 22,106 | 1.86 | 9,063 | +6,808 | +2,840 | +2,060 | +3,315 |
| Neukölln | 18,378 | 10,689 | 1.79 | 7,657 | +2,632 | −1,673 | +1,167 | +987 |
| Treptow-Köpenick | 61,199 | 55,800 | 1.90 | 31,174 | +1,036 | −1,806 | +180 | −631 |
| Marzahn-Hellersdorf | 47,455 | 41,329 | 1.93 | 17,872 | +6,721 | +3,547 | +2,796 | +5,117 |
| Lichtenberg | 61,981 | 52,921 | 1.79 | 22,892 | +11,826 | +6,751 | +580 | +1,748 |
| Reinickendorf | 27,028 | 19,467 | 2.01 | 6,961 | +6,501 | +2,735 | +2,691 | +3,428 |
| **Berlin** | **486,530** | **408,212** | **1.85** | **188,428** | **+73,939** | **+31,705** | **+16,015** | **+21,441** |

**Sign pattern.**
- **(i)** is positive in 11 Bezirke. Steglitz-Zehlendorf is about zero.
- **(ii)** is positive in 9 Bezirke and negative in Friedrichshain-Kreuzberg, Neukölln and Treptow-Köpenick, where building kept pace with census-anchored growth. Inner-city outflow to the outer districts is part of the story.
- **(iii)** is positive in all 12, but small: 165 in F-Kreuzberg up to 2,800 in Marzahn-Hellersdorf.
- **(iv)** is positive in 10 Bezirke. F-Kreuzberg and Treptow-Köpenick are negative.

**Berlin sensitivity of (ii) and (i) to household size (INFERRED):**

| Size used | (ii) census-anchored | (i) register |
|---|---|---|
| 1.754 (MZ 2011) | +44,300 | +89,000 |
| 1.80 | +38,400 | +81,900 |
| 1.85 (MZ 2024) | +32,200 | +74,600 |
| 1.876 (MZ 2025) | +29,200 | +70,900 |

The (ii) Berlin figure at 1.85 is 32,227 with Berlin-wide size, or 31,705 with Bezirk-specific size. Small mismatches: the census start date is May 2011, while completions start January 2012, which drops ~2,900 completions from mid-2011. The population growth also includes people in institutions (about 90,000 persons are not in private households in 2022). This barely matters because the gap uses growth, not levels, unless the institutional share changed.

### Table 4b – Reserve version
Dwellings needed = HH × (1 + r) + "other" (census 2022 non-household dwellings), compared with stock. Positive = shortfall. INFERRED.

| Bezirk | Est. HH 2025 | Stock 2025 | Implied vacancy 2025 | Rate | Shortfall @2% | Shortfall @3% | Same @3% in 2011 |
|---|---|---|---|---|---|---|---|
| Mitte | 209,833 | 215,641 | 3,864 | 1.8% | +333 | +2,431 | −2,035 |
| Friedrichshain-Kreuzberg | 155,156 | 159,758 | 3,507 | 2.2% | −404 | +1,148 | −102 |
| Pankow | 224,719 | 229,847 | 4,067 | 1.8% | +427 | +2,674 | −230 |
| Charlottenburg-Wilmersdorf | 191,448 | 197,962 | 4,651 | 2.3% | −822 | +1,092 | −806 |
| Spandau | 126,424 | 131,091 | 2,037 | 1.6% | +492 | +1,756 | −1,900 |
| Steglitz-Zehlendorf | 155,263 | 163,167 | 4,922 | 3.0% | −1,817 | −264 | −1,418 |
| Tempelhof-Schöneberg | 186,705 | 189,637 | 1,950 | 1.0% | +1,784 | +3,651 | −736 |
| Neukölln | 165,012 | 169,790 | 3,762 | 2.2% | −462 | +1,188 | −1,057 |
| Treptow-Köpenick | 157,797 | 161,918 | 3,341 | 2.1% | −185 | +1,393 | +254 |
| Marzahn-Hellersdorf | 146,022 | 146,445 | −281 | −0.2% | +3,202 | +4,662 | −1,657 |
| Lichtenberg | 167,134 | 170,055 | 1,468 | 0.9% | +1,875 | +3,546 | −485 |
| Reinickendorf | 130,859 | 134,121 | 1,986 | 1.5% | +632 | +1,940 | −2,257 |
| **Berlin** | **2,016,372** | **2,069,432** | **35,274** | **1.7%** | **+5,053** | **+25,217** | **−12,429** |

- The implied 2025 vacancy is a residual and only as good as the constant-household-size assumption. Marzahn-Hellersdorf's negative value shows the error band, about ±3,000 per Bezirk.
- This version mixes the census (2022 level) with F I 1 (Fortschreibung). F I 1 end-2022 Berlin is 2,028,467, against census 15.5.2022 at 2,018,831. Some ~5,000 of the difference is the 7½ months of completions; the rest is definitional. Expect ±5,000 for Berlin.

---

## 5. Vacancy-reserve benchmark (Task 5)

### "3% Fluktuationsreserve" (VERIFIED quotes, StEP Wohnen 2040 report, step-wohnen_bericht.pdf)
- **Page 76:** "Damit in einem angespannten Wohnungsmarkt wieder Umzugsketten in Gang kommen, ist nach allgemeiner Auffassung eine Fluktuationsreserve von rund drei Prozent des Wohnungsbestands erforderlich, die Wohnungssuchenden zur Verfügung steht. In Berlin müsste dazu der aktuelle Leerstand von 1,1 Prozent durch etwa 41.000 neu zu bauende Wohnungen auf diese Dreiprozentmarke angehoben werden."
- **Glossary:** "Für einen funktionierenden Wohnungsmarkt wird eine Fluktuationsreserve zwischen zwei und fünf Prozent der Wohnungen als notwendig erachtet."
- **The Senate document itself cites no primary BBSR/GdW source** ("nach allgemeiner Auffassung"). I did not find a BBSR or GdW document that fixes 3%, so it remains a convention, not a sourced standard. Cite it as "StEP Wohnen 2040 (Senat Berlin 2024), S. 76".

### CBRE-empirica Leerstandsindex, marktaktiver Leerstand Berlin (VERIFIED)
Source: empirica methodology/result PDFs, editions 2016, 2023 and 2025, Bundesländer tables. The measure counts only dwellings in multi-family buildings.

| Year | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Rate | 2.6% | 2.3% | 2.0% | 1.8% | 1.5% | 1.2% | 1.1% | n/a | 0.8% | 0.8% | 0.9% | 0.8% | 0.3% | 0.3% | 0.3% |
| Units | 44,500 | 39,000 | 33,800 | 29,500 | 25,300 | 19,800 | 17,900 | n/a | 13,200 | 13,400 | 15,500 | 14,400 | 5,900 | 6,100 | 5,400 |

- Sources by year: 2010–16 from the 2016 edition; 2018–22 from the 2023 edition; 2020–24 from the 2025 edition. Overlapping years agree.
- 2017 is not in the editions I opened. Earlier search snippets claiming "0.9%/0.8% in 2012/13" were wrong.
- The 2025 edition notes that market-active vacancy "kann insbesondere auch kleiner sein als eine angenommene Fluktuationsrate, weil er nur unvermietete Wohnungen berücksichtigt".

**Comparison of vacancy measures, 2022:** census 2.0% (all vacancy), StEP "1.1%" (source not named), CBRE-empirica 0.3% (market-active). Any reserve target must name which vacancy measure it targets.

---

## 6. StEP Wohnen 2040 sanity check (Task 6)

### What the 137,000 contains
StEP Wohnen 2040 report, ch. 6.4, pp. 75–77 (VERIFIED). The "Entlastungsbedarf" for 2022–2040 has three parts:
1. **Building up a 3% Fluktuationsreserve from 1.1% vacancy: ≈41,000 dwellings.**
2. **Easing tension symptoms: ≈77,000.** The targets are to bring average household size back to 1.77, halfway between the 2013 value of 1.75 and the 2019 value of 1.79, and to halve the rise in suburbanisation since 2013.
3. **Replacement of demolitions/conversions: 1,000 per year (0.05% of stock), = 19,000 over 2022–2040.**

- 41 + 77 + 19 = 137 thousand.
- **There is no separate component for homeless people or refugees.** Wohnungslose and Geflüchtete do not appear in the bedarf method.
- The demographic demand (85,000) comes from the register-based population forecast (register 2021), translated with age-specific headship rates from the Mikrozensus plus sub-letting and second-home rates.

**Update.** The Fortschrittsbericht of 16.06.2026 (Senate press release 1682261, VERIFIED) gives 2026–2040 demand of 211,000. That is 138,000 Entlastungsbedarf plus 73,000 demographic, with ~60,000 dwellings built 2022–2025. The report itself was not opened, so its components are unverified.

### Comparison
- StEP's 137,000 is a **forward target**, not a measured backlog. About 96,000 of it (the reserve to 3% plus the household-size and suburbanisation relief) is a *normative* choice.
- Our census-consistent backward gap (ii) of ≈32,000 measures how far building fell behind population growth at today's crowded household size. Our 3%-reserve stock shortfall for 2025 is ≈25,000, close to StEP's ≈41,000 reserve component (StEP starts from 1.1% vacancy, we from ≈1.7–2.0%).
- **The difference to 137,000 is mostly the 77,000 "Linderung der Anspannung"**, which treats rising household size and outmigration to Brandenburg as suppressed demand.
- If we priced the 2011→2025 rise in MZ household size (1.754 → 1.854) the same way, the extra dwellings would be 3.66m/1.754 − 3.66m/1.854 ≈ 112,000 (INFERRED, mixed-break series). This is an upper bound on suppressed household formation, and it shows where StEP's 77,000 comes from.

---

## 7. Recommendation for "Die Lücke"

### Headline gap: definition (ii)
"Census-anchored population growth 9.5.2011–31.12.2025, converted to households at the 2024 Mikrozensus household size of each Bezirk, minus dwellings completed 2012–2025."

| Bezirk | Headline gap (dwellings) |
|---|---|
| Mitte | +3,800 |
| Friedrichshain-Kreuzberg | −4,500 |
| Pankow | +5,200 |
| Charlottenburg-Wilmersdorf | +7,100 |
| Spandau | +6,000 |
| Steglitz-Zehlendorf | +1,000 |
| Tempelhof-Schöneberg | +2,800 |
| Neukölln | −1,700 |
| Treptow-Köpenick | −1,800 |
| Marzahn-Hellersdorf | +3,500 |
| Lichtenberg | +6,800 |
| Reinickendorf | +2,700 |
| **Berlin** | **≈ +32,000** |

Round to hundreds and show negative values as "building kept pace".

### Sensitivity range for Berlin
- **Floor: +16,000.** Census-to-census households vs dwellings 2011–2022 is a lower bound because census households cannot show doubling-up.
- **Cross-checks: +21,000 to +25,000.** Households vs stock to 2025 gives +21,000; the shortfall against a 3% reserve in 2025 gives +25,000.
- **Ceiling: +44,000.** This is (ii) at the 2011 household size of 1.754.
- **Do not show** the register version (+74,000) or the StEP 137,000 as the same measure. If shown, label StEP as "Senate target incl. reserve and relief".

### Three caveats to print next to the chart
1. **Population basis.** Figures use the census-corrected population (Zensus 2011 and the 2022-based Fortschreibung), not the resident register. The register shows about 78,000 more growth since 2011 because of stale registrations.
2. **Household size is an assumption, and it has been rising.** Each 0.05 change in persons per household moves the Berlin gap by about 5,000–6,000 dwellings. Berlin's average rose from 1.75 (2011) to 1.85 (2024), partly *because* of the shortage (people moving out later, more sharing). The chart therefore understates suppressed demand.
3. **"Gap" here is not "need".** It is the shortfall of building relative to population growth since 2011, which shows up as vacancy falling from 3.5% (2011) to 2.0% (census 2022) and market-active vacancy falling to 0.3%. The Senate's 137,000/138,000 figure is a forward target that adds a 3% reserve, relief for crowding and suburbanisation, and replacement building.

### Sources
- Zensus 2011 Gemeindeblätter: https://www.statistik-berlin-brandenburg.de/bevoelkerung/zensus/zensus_2011/ergebnisse-berlin/
- Zensus 2022 Lokale Daten: https://www.statistik-berlin-brandenburg.de/zensus22/lokale-daten-berlin/
- A I 3 series: https://www.statistischebibliothek.de/mir/receive/BBSerie_mods_00000019 ; 2025: statistik-berlin-brandenburg.de/a-i-3-j
- A I 11 (Berlin, to 2019): https://www.statistischebibliothek.de/mir/receive/BBSerie_mods_00000011 ; joint A I 10/11 2020+: BBSerie_mods_00000633 ; 2025: https://download.statistik-berlin-brandenburg.de/f2b39c025be9204d/300071e01377/SB_A01-10-00_2025j01_BE.pdf
- F I 1 2025 XLSX (Stage 1); F I 1 j/21 PDF
- StEP Wohnen 2040 Bericht: https://www.berlin.de/sen/stadtentwicklung/_assets/planung/stadtentwicklungplaene/step-wohnen_bericht.pdf ; Fortschrittsbericht PM: https://www.berlin.de/rbmskzl/aktuelles/pressemitteilungen/2026/pressemitteilung.1682261.php
- CBRE-empirica: https://www.empirica-institut.de/assets/content/typo3/Redaktion/Publikationen_Referenzen/PDFs/CBRE-empirica-Leerstandsindex-Methode-2016-v.pdf ; …-2023.pdf ; …-2025.pdf
