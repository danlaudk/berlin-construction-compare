# Opus 3: hostile design review of the enteignen lever and the two-round game (2026-11-16)

Method note. All arithmetic below was re-derived locally (python). Primary PDFs were NOT re-fetched in this pass; "V" items rely on the stage/sonnet agents' verification and are marked "citation to print" with the document they named. Where my arithmetic disagrees with the design, that is flagged as a finding.

## Top findings (read these if nothing else)
1. **Unit mismatch in the Vergabe sub-lever (MUST).** +7.0–8.3k is *lettings per year*; −7.2k (empirica) is a *stock* of dwellings' floor space withdrawn. They cannot sit on one balance bar. Show them on different axes or drop the −7.2k from the lever.
2. **The +7.0–8.3k is gross, and its turnover input is too high (MUST).** Bernt & Holm assume 5% turnover. The LWU's own observed re-letting rate in 2024 is 12,398 / 374,472 = 3.3%. The *net* gain vs. today's private quota (Bündnis 30%) is what the lever changes: at 5% turnover +4,613 (63%) / +4,995 (75%); at 3.3% turnover ≈ +3,300 (75%). Show "netto ≈ 3,300–5,000 zusätzliche WBS-Vergaben pro Jahr", with 6,999 as the campaign's gross figure in a quote.
3. **"Where the newcomers live" is an accounting decomposition, not a tracking result (MUST).** New dwellings were occupied by everyone, including movers within Berlin. Round 1 must say "rechnerisch" and frame taps as "Die Stadt hat Platz geschaffen durch…", not "Die Neuen wohnen in…".
4. **"Enger gewohnt = 0" is not robust (MUST).** Census HH size 2011 depends on the unretrieved institutional population: 70k → 1.795; 90k → 1.784; 110k → 1.773 (2022: 1.789). ±0.01 ≈ ±20,000 people. Show "≈ 0 (± 20.000)" until Zensus 2011 persons-in-private-households is fetched (Gemeindeblatt BEV table; this is the fix).
5. **Compensation slider builds a false counterfactual (MUST change).** The sum is debt refinanced from rents, not a budget line that would otherwise build flats. Replace with the annual Land top-up (DIW Table 2: −325 m € to +1,142 m € per year) and, if any dwelling conversion is shown, convert only that annual budget burden, with all-in cost incl. land and Baunebenkosten, not KG 300–400.
6. **Risk band over-attributes (SHOULD).** DIW's 42–46% is "private Wohnungsunternehmen" (all companies), not the ≥3,000-flat owners in scope. Label it so, or find the in-scope share (Vonovia/DW Berlin completions, open item).
7. **Vacancy card applies a category rate to a different set (SHOULD).** 2.07% is for 389,015 dwellings of all private housing companies; the 222,000 in scope are a subset. "~4,600" is an inference; say "bei gleicher Quote etwa 4.600".

## 1. Campaigner (DW & Co. enteignen)
- **"222 recoloured, 0 added" is fair on supply, unfair as the only visible effect.** The campaign's goals are rent, allocation, displacement. The panel must give the rent channel its own field: ~16% rent relief, €936/household/yr (Bernt & Holm 2023), labelled campaign estimate. Without it the waffle grammar (which only knows dwellings) silently declares the lever useless.
- **Equal weight.** As designed, +7–8.3k and −7.2k look like a wash. That is wrong twice: unit mismatch (finding 1) and source asymmetry. Bernt & Holm is campaign-adjacent (RLS) but transparent arithmetic. Empirica/Simons is bank-commissioned and "ausdrücklich ohne Anspruch auf Kausalität". A non-causal estimate should not be a lever component. Show lock-in as a text risk with the literature line (Kholodilin 2024: 25 of 26 studies find lower mobility), which is causal-literature-backed and not bank-funded.
- **Compensation slider.** The campaign's position is refinancing from rents (Holm/Thonke/Arpagaus 2025). The slider implies "8–39 bn could have built 25–134k flats". Agree this is a false counterfactual (finding 5).
- **Vacancy and Entmietung.** Census vacancy *does* include Modernisierungs-/Bauleerstand (9,205 vacant for construction, Drs. 19/20607), so the campaign's "hidden modernisation vacancy" objection is answered by the data. But Entmietung, Umwandlung pressure, and modernisation rent increases displace occupied households and are not vacancy. The card must say what it does not measure.
- **Quotes that must appear:** campaign "nicht gegen Neubau"; campaign: relief from new build only above 10–20% vacancy (SECONDARY: verify before print); AöR concept "nach einer Konsolidierungsphase sind auch eigene Neubauprojekte … denkbar". **Opposing:** IMK PB 225 "Neubau in großem Stil ist hier der einzige Weg" (note: IMK is otherwise pro-feasibility, which makes it strong); DIW aktuell 126 "schafft keine zusätzliche Wohnung"; Sondervotum "nicht belegt und eher unplausibel".
- **Missed channels the campaign would raise:** (a) rent savings as housing-cost relief (€936/HH/yr); (b) stop of Umwandlung in Eigentum in 222k flats (data: Umwandlungen per year, Senate answers; not inventoried); (c) Wohnungstausch to counter lock-in (LWU Tauschbörse counts; not inventoried); (d) Abwendungsvereinbarungen as protection without transfer.

## 2. Statistician (AfS)
- **Additivity.** ΔHH = ΔDw − ΔVac − ΔOther: 149,403 + 25,577 − 9,562 = 165,418. Exact. The taps are additive and non-overlapping *in dwellings*. Converting to people at one HH size makes "Enger gewohnt" the residual by construction; it is not a separate measurement.
- **Use official census totals.** 304,614 = 3,596,979 − 3,292,365, consistent with the official Zensus 2022 Berlin figure. The kleinräumig file gives 3,596,999 / 1,960,342 (cell-key noise). The design's 1,960,354 households and 2,018,840 dwellings must be checked against the Gemeinde-level Zensus 2022 tables, not summed Bezirksregionen. Same for F I 1 2,018,831 vs census 2,018,840 (different concept, Wohnheime).
- **Shelters in Round 1.** Unterkünfte statistic starts 31.01.2022, so Round 1 has no measured shelter flow. Shelters sit inside population but outside private households, i.e. inside the ~8,500 residual (with Wohnheime, care homes, prisons, noise). Show tap "In Unterkünften" for Round 1 as "nicht gemessen, im Rest von ≈ 8.500".
- **Household size flat.** See finding 4. Also cell-key noise is negligible at Berlin level (≤ tens), the institutional assumption dominates.
- **Round 2.** Can be shown only as an estimate. Problems: different instruments (A I 3 Fortschreibung, F I 1 Fortschreibung, Wohnungslosenstatistik); date mismatch (shelters 31.01.2022→31.01.2025, population 15.5.2022→31.12.2025); some accommodated homeless live in Trägerwohnungen inside the dwelling stock, so dwellings and shelters double-count; the sum over-explains by ≈14,600 (50,592×1.79 + 27,635 − 103,598). Label: "Schätzung, keine Volkszählung. Die Teile ergeben mehr als 100 %, weil die Quellen sich überschneiden." Do not reveal a vacancy tap in Round 2 (no measurement; empirica only market-active 0.3% throughout).
- **Transfers = 0 people.** Holds as "0 zusätzliche Menschen" (net). 14,750 × 0.7% ≈ 100 vacant flats; any refill is within normal turnover and not attributable. The 450 commercial units are not dwellings. Wording: "praktisch null".
- **2.07% vs 2.02%.** Difference is 0.05 pp ≈ 195 flats on 389,015: not meaningful given definitional sensitivity (vacancy reason coding, cell-key at Bezirk × owner type). Bezirk range 1.1–2.9% for private companies rests on small cells; show Berlin only, describe as "gleich hoch wie im Durchschnitt".
- **Construction cost.** KG 300–400 excludes land (KG 100), Erschließung (200), Außenanlagen (500), Baunebenkosten (700, ~15–20%). All-in for LWU new build should come from LWU Gesamtkosten (Senate answers / KoopV report / IBB Förderdaten). Until verified, no dwelling equivalent should be printed.

## 3. Fact-checker
| Figure | My re-derivation | Survives correction request? | Citation to print |
|---|---|---|---|
| 6,999 | 222,000×5%×63% = 6,993 (6,999 implies slightly different inputs; print as source's number) | Yes as *quoted gross campaign figure*; No as "gain" | Bernt, M./Holm, A. (2023): Vergesellschaftung …, RLS Studien 1/2023 |
| 8,189–9,622 | LWU WBS lettings 2024 / 2021 | Yes; label year per value | Kooperationsvereinbarung „Leistbare Mieten…", Berichte 2021–2024 (SenSBW) |
| 7,200 | Stock, not flow | No as lever component; yes as quoted, contested estimate | empirica/Simons 2026 as quoted in DIW aktuell 126 (05.10.2026); cite DIW page |
| 42–46% | DIW, 2008–2025 / 2025 | Yes only if labelled "alle privaten Wohnungsunternehmen" | DIW aktuell 126 |
| 2.07 / 1.91 / 1.07% | 8,047/389,015 = 2.07; 7,270/381,075 = 1.91; 2,188/205,018 = 1.07 | Yes | Zensus 2022, Tabelle 4000W-3006, Berlin, Stichtag 15.5.2022 |
| 14,750 | deal size | Yes (+450 Gewerbe, €2.46 bn) | Senate/LWU PM Sept 2021, closing 2022 |
| 11,644 | LWU Ankauf 2022 | Yes, but do not add to 14,750; berlinovo (~4,000) is outside the KoopV LWU count | KoopV-Bericht 2022 |
| "~20,000+ 2019–2025" | 2021–25 sum = 20,070; 2019–20 not in it | Fix: say "rund 20.000 (2021–2025)" or add 2019–20 explicitly | as above + PM 1672180 |
| Compensation table | 8 bn ÷ 294–315k = 25.4–27.2k; 39.5 bn = 125–134k | Arithmetic yes, concept no (finding 5) | Rechnungshof Bericht 20.02.2024; Senat 2019; Holm/Thonke/Arpagaus 2025; IMK PB 225 |
| 304,614 / 149,403 | 3,596,979 − 3,292,365; 2,018,840 − 1,869,437 | Yes (check 2,018,840 against Gemeinde table) | Zensus 2011 & 2022, Ergebnisse Berlin |
| 137,000 = 41+77+19 | sums | Yes | StEP Wohnen 2040, S. 75–77 |

**Cards that mislead a lay Berliner:** vacancy card (category ≠ the 222k; 15.5.2022 date); Vorkaufsrecht numbers (Abwendungsvereinbarungen do NOT change owner: must not recolour); 42–46% (all companies); Airbnb 8,446 (listings, not flats, 2026); 7,200 (stock vs flow); "22 % of 2,069 squares" — 222 is 13.5% of *rental* stock but ~10.7% of all dwellings, say which; Round 2 dates.

## 4. Designer: on-screen German
**(a) Part A tap "Übernommen / angekauft".** Tap label: „Übernommen". Hint: „Wohnungen, die den Besitzer wechselten." Reveal: „Rund 20.000 Wohnungen kauften die landeseigenen Gesellschaften 2021–2025. Darin wohnten schon Menschen. Zusätzlich untergebracht: praktisch niemand. Die Felder färben sich um, keins kommt dazu."

**(b) Panel „Vergesellschaften".**
1. „222.000 Wohnungen großer Vermieter (ab 3.000 Wohnungen) gingen an eine Anstalt öffentlichen Rechts. Neue Wohnungen: 0." (Expertenkommission 2023)
2. „Vergabe: Pro Jahr würden rund 3.300–5.000 Wohnungen mehr an Haushalte mit WBS vermietet als heute. Gleiche Wohnungen, andere Mieter. Die Initiative rechnet mit 7.000 (brutto). Risiko: Wer günstig wohnt, zieht seltener um (25 von 26 Studien)."
3. „Kosten: Entschädigung 8–36 Mrd. € (Schätzungen 2019–2026), über Kredite und Mieten finanziert. Jährliche Belastung für den Landeshaushalt: −0,3 bis +1,1 Mrd. € (DIW)." No dotted squares.
4. Toggle „Bauen?": „Mehrheit der Kommission: ‚verspricht einen hohen Beitrag' zum Neubau, wenn gesetzlich vorgegeben. Minderheit: ‚nicht belegt und eher unplausibel'. Initiative: eigene Neubauprojekte ‚denkbar'. Keine Zahl."
5. Risk band: „Private Wohnungsunternehmen bauten 42–46 % der neuen Wohnungen. Welcher Teil davon auf die betroffenen Konzerne entfällt, ist nicht veröffentlicht." Plus field „Miete: −16 % für Neuvermietete, ca. 936 € pro Haushalt und Jahr (Schätzung der Initiative)."

**(c) Vacancy card.** „Stehen bei den Konzernen Wohnungen leer? Kaum mehr als anderswo: 2,1 % bei privaten Wohnungsunternehmen, 2,0 % in ganz Berlin (Zensus, 15.5.2022; Leerstand wegen Sanierung eingerechnet). Bei gleicher Quote wären das etwa 4.600 der 222.000. Nicht gemessen: Verdrängung aus bewohnten Wohnungen."

**(d) Reveals.**
Round 1 (Zensus 9.5.2011 → 15.5.2022, „gezählt"; people = dwellings × 1,79, „rechnerisch"):
Neu gebaut +149.403 Whg. ≈ 267.000 (88 %) | Aus leeren Wohnungen 25.577 ≈ 46.000 (15 %) | Ferienwohnungen/Gewerbe/Zweitwohnung: −9.562 ≈ −17.000 (−6 %) | Enger gewohnt ≈ 0 (± 20.000) | In Unterkünften: nicht gemessen, im Rest ≈ 8.500 (3 %) | Umgebaut/aufgestockt: in „Neu gebaut" enthalten | Übernommen: 0 | Gar nicht gekommen: nicht messbar.
Round 2 (15.5.2022 → 31.12.2025, „geschätzt"): Wohnungsbestand +50.592 ≈ 90.600 | Unterkünfte +27.635 Personen (31.1.2022→31.1.2025) | Summe ≈ 114 % der 103.598: „Die Quellen überschneiden sich." Übernommen ≈ 5.400 Whg., 0 Personen.

**(e) Bridge.** „Berlin hat Platz geschaffen, auch indem es Reserven aufgebraucht hat. Stellen Sie ein, wie viel Reserve und wie viel Platz pro Haushalt Berlin haben sollte. Mit den Werten des Senats (3 % Reserve, 1,77 Personen je Haushalt) ergibt sich der Entlastungsbedarf von 137.000 Wohnungen: 41.000 Reserve, 77.000 Entlastung, 19.000 Ersatz (StEP Wohnen 2040). Nicht enthalten: die Menschen in Unterkünften."

## 5. Change list
**Must**
- Separate flow vs stock in Vergabe; show net, not gross; use observed turnover. Fix: KoopV reports (re-letting ÷ stock).
- Remove compensation→dwellings squares. Fix: DIW aktuell 126 Tab. 2 annual burden.
- Relabel Round 1 as arithmetic decomposition; "Enger gewohnt ≈0 ±20k". Fix: Zensus 2011 Gemeindeblatt BEV (persons in private households).
- Round 1 shelter tap = not measured/residual. Round 2 labelled estimate, overlap explained, dates printed.
- Don't recolour Abwendungsvereinbarungen; fix "20,000+" period. Fix: Vorkaufsrecht-Bericht 9.
- Add rent-relief field and the required quotes from both sides.
- Use official Gemeinde-level census totals throughout.
**Should**
- Risk band labelled "alle privaten Unternehmen"; find in-scope share (Vonovia/DW Berlin completion reports).
- Vacancy card: "bei gleicher Quote", Berlin only, state Entmietung not measured.
- Lock-in as text with Kholodilin 2024, empirica only in footnote.
- Say 222 squares = 10.7% of all dwellings / 13.5% of rental stock.
**Could**
- Umwandlung and Wohnungstausch fields (Senate Umwandlungsstatistik; LWU Tauschbörse).
- All-in LWU cost per flat incl. land (Senate Drucksachen) for any cost-equivalence elsewhere.
- Brandenburg migration (dataset L) for "Gar nicht gekommen".

## 6. Verdict
As designed, the piece would not survive a hostile taz fact-check, and only narrowly a Tagesspiegel one. The census ledger itself is sound and exact, and the 137,000 bridge is clean. The enteignen panel, though, contains three errors a checker will find in an afternoon. It nets a per-year flow against a stock. It presents a gross, 5%-turnover campaign number as the gain while the LWU's own turnover is 3.3%. It converts debt-financed compensation into flats that would never otherwise be built. The campaign would rightly call the slider and the bank-funded lock-in figure biased, and the statistician would object to "zero enger gewohnt" and to people-tracking language. With the must-list applied, the panel becomes defensible: it shows honestly that expropriation adds no dwellings, changes allocation by a few thousand lettings a year and rents by a measurable amount, and costs a debated annual sum.
