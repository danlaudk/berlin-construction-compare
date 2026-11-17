# Consolidated findings for the Berlin housing visualisation (as of 2026-11-16)

Input for the Opus design review. Sources: docs/research/stage1_datasets_report.md, stage2_levers_report.md, stage3a_gap_report.md, stage3b_verify_report.md, sonnetA_corporate_vacancy.md, sonnetB_enteignen_supply.md, sonnetC_campaign_docs.md, sonnet1_owner_vacancy_cost.md (+ sonnet1_figures.csv), sonnet2_transfers_allocation.md. Design: docs/die-luecke-design.md. Tags: V = VERIFIED in a primary source by an agent; S = SECONDARY; I = INFERRED (our arithmetic).

## 1. The population and dwelling ledger (Part A material)

| Item | Figure | Tag | Source |
|---|---|---|---|
| Register population growth end-2011→end-2025 | +486,530 | V | A I 5 (in repo) |
| Census-anchored growth 9.5.2011→31.12.2025 | +408,212 (3,292,365 → 3,700,577) | V | Zensus 2011 Gemeindeblätter; A I 3 2025 |
| Register overstatement at end-2025 | ~213,000 | V | AfS "Melderegister, Zensus, Fortschreibung" |
| Completions 2012–2025 (dwellings_total) | 188,428; 2025 = 11,027 full year (new-build 9,524, existing-building measures 1,503) | V | F II 2; PM 59/2026 |
| Stock F I 1 | 1,871,782 (end-2011, 2011 basis) → 2,069,432 (end-2025); rebasings −31,449 (2011), +16,037 (2021) | V | F I 1 |
| Census 2011→2022 Berlin | pop +304,614; private households +165,418 (1,794,936→1,960,354); dwellings +149,403 (1,869,437→2,018,840); vacant −25,577 (66,277→40,700, 3.5%→2.0%); other-use +9,562 | V inputs, I differences | Zensus 2011/2022 per Bezirk (table in stage3a §1) |
| Census household size | ≈1.79 in both 2011 and 2022 (flat) | I (from size classes) | stage3a |
| Mikrozensus household size Berlin | 1.754 (2011) → 1.789 (2019) → 1.85 (2024) → 1.88 (2025); breaks 2016/2020/2022; rose in 11 of 12 Bezirke 2014→2024 | V | A I 10/11 |
| 2022→2025 | pop +103,598; stock +50,592; accommodated homeless 25,975 (2022) → 53,610 (2025) | V | A I 3, F I 1, AfS Wohnungslose |
| Headline gap (def. ii) | ≈ +32,000 Berlin (range 16k–44k); per Bezirk: Mitte +3.8k, F-K −4.5k, Pankow +5.2k, C-W +7.1k, Spandau +6.0k, S-Z +1.0k, T-S +2.8k, Neukölln −1.7k, T-K −1.8k, M-H +3.5k, Lichtenberg +6.8k, Reinickendorf +2.7k | I | stage3a |
| Register version | +73,939 (not defensible as headline) | I | stage3a |
| 3% reserve shortfall 2025 | +25,217 (2011: −12,429 surplus) | I | stage3a |
| StEP Wohnen 2040 need | 222,000 = 137,000 Entlastung (41k reserve from 1.1%→3%; 77k relief: HH size 1.79→1.77 + halve suburbanisation; 19k replacement) + 85,000 demographic; 2026 update 211,000 = 138k + 73k; "3 %" is "nach allgemeiner Auffassung" (p. 76), glossary 2–5% | V | StEP 2040 pp. 75–77; PM 1682261 |
| Market-active vacancy (CBRE-empirica) | 2.6% (2010), 2.3% (2011, 39,000), 1.1% (2016), 0.8% (2018–19), 0.3% (2022–24, 5,400 flats) | V | empirica Methode PDFs 2016/2023/2025 |
| Census vacancy 2022 reasons | 24,879 available ≤3 months; 9,205 construction; 678 demolition; 1,464 sale; 767 own use; 3,686 other; ≥12 months 11,764 | V | Drs. 19/20607 |
| Bauüberhang end-2025 | 48,394 (12,901 unter Dach, 12,252 Rohbau, 15,784 not started); 3,055 lapsed | V | F II 2 Tab. 17 |
| Permits Berlin | 21,107 (2016) … 17,005 (2021), 15,186, 14,398, 9,772 (2024), 13,754 (2025) | V | F II 1 |
| Not yet inventoried | Net migration Berlin↔Brandenburg per Bezirk (A III 1 / Open Data Wanderungen) | – | – |

## 2. Lever figures (Part B material)

| Lever | Adds / frees / transfers | Figure | Tag | Source |
|---|---|---|---|---|
| New build | adds | 11,027/yr (2025); 15–19k/yr 2017–2022; LWU 4,692 (2025), 4,599 (2023), 3,276 (2024) | V | F II 2; KoopV report 2024; PM 1672180 |
| Overhang | adds (if finished) | 48,394 permitted, 15,784 not started | V | F II 2 |
| Market-active vacancy | frees | ~5,400 | V | CBRE-empirica |
| Long-term vacant | frees (ceiling) | 11,764 | V | Zensus 2022 |
| Zweckentfremdung enforcement | frees (already banked) | 31,706 returned since 2014, of which 8,330 Ferienwohnungen (30.06.2025); holiday-flat returns ~500/yr since 2020; registration numbers 4,319 (09/2024) | V | Drs. 19/24230; 19/21276 |
| Airbnb entire homes | frees (ceiling) | 8,446 listings (19.09.2026), 4,929 reviewed in last 12 months; Bezirk counts | V | Inside Airbnb |
| Supermarket-site redevelopment | adds | 20,000–36,000 (330 sites) | V | Deutschlandstudie 2019 |
| Office conversion | adds (theoretical) | ~30,000 | S | bulwiengesa/Berlin Hyp 2025 |
| Rooftop extension (AI study) | adds (theoretical) | up to ~8,000 | S | Syte et al. 2024 |
| Social bindings | protects, no supply | ~90,600 (2023); 46,408 expire 2024–34 | V | IBB WMB 2024 |
| Milieuschutz | protects | 82 areas, 664,504 flats, 1,198,619 residents (31.12.2024) | V | Drs. 19/25318 |
| Mietendeckel | none/negative | listings −50% (DIW), "up to 60%" (ifo 2022) | V | DIW WB 8/2021 |
| Demand benchmarks | – | IW: need 31,300/yr 2021–25 vs 16,382 built; Pestel ≥58,000 deficit (S) | V/S | IW-Report 2024 |

## 3. The expropriation ("Vergesellschaftung") lever: everything quantified

### 3.1 Scope and legal state
- ~222,000 flats at owners with ≥3,000 Berlin flats (Dec 2021), 13.5% of rental stock (V, Expertenkommission 27.06.2023). Campaign Begründung: 243,000–250,000 gross, minus ~30,000 Selbstbehalt = 213,000–220,000 (V). Senate/Rechnungshof use 240,000.
- Rahmengesetz: Drs. 19/2842 (CDU/SPD, 18.12.2025), passed 12.03.2026 (S), in force 24 months after promulgation; Verkehrswert as starting point, no threshold, no AöR; an Anwendungsgesetz is still required (V). Referendum 26.09.2021: 1,035,950 yes = 57.6% of valid votes (V).

### 3.2 Vacancy in the corporate stock (the "they sit on empty flats" claim)
- Zensus 2022, Berlin, by owner type (V, table 4000W-3006): all 2.02%; privatwirtschaftliches Wohnungsunternehmen 389,015 dwellings, 8,047 vacant = 2.07%; kommunal 381,075 / 7,270 = 1.91%; Genossenschaft 205,018 / 2,188 = 1.07%; Privatpersonen 1.97%; WEG 1.98%; Bund/Land 4.77% (small); andere Unternehmen 3.42%. Per Bezirk, private companies range 1.1% (M-H) to 2.9% (C-W).
- Company disclosures: Deutsche Wohnen Berlin 0.7% (V, company page); Vonovia group 1.9% (V, no Berlin split); BBU members 1.6%, ~12,400 flats, mainly refurbishment vacancy (S).
- Reading: at 2.07% on ~222,000 flats, the corporate stock holds ~4,600 vacant dwellings, most of them frictional; no owner type except Bund/Land is materially above average. No source (campaign, commission, Mieterverein) publishes a Berlin "speculative vacancy" count for the corporates.

### 3.3 Supply claims by proponents
- Campaign law text, Factsheet: no supply provisions (V). Begründung: Nachverdichtung/Aufstockung "zusätzlicher bezahlbarer Wohnraum" qualitatively, no number (V). AöR concept: "nach einer Konsolidierungsphase sind auch eigene Neubauprojekte … denkbar"; 75% of re-lettings to WBS holders (V). Campaign position: "nicht gegen Neubau"; relief from new build only above 10–20% vacancy (S).
- Expertenkommission majority §198: Vergesellschaftung "verspricht einen hohen Beitrag" to Neubau via Aufstockung/Nachverdichtung if mandated; no number. Sondervotum: "nicht belegt und eher unplausibel"; expects Bauzurückhaltung (V).
- IMK Policy Brief 225 (2026, pro-compensation-feasibility): "Vergesellschaftung … ist keine Lösung für den Mangel an Wohnraum … Neubau in großem Stil ist hier der einzige Weg" (V).
- DIW aktuell 126 (05.10.2026): "schafft keine zusätzliche Wohnung"; private Wohnungsunternehmen built 42% of completions 2008–2025, 46% in 2025; AöR would be ~3× the largest LWU (V).

### 3.4 The allocation channel (the one quantified availability effect)
- Bernt & Holm 2023 (RLS Studie 1/2023, V): 222,000 × 5% turnover × 63% WBS quota = 6,999 lettings/yr to WBS holders, "ohne Zuwachs durch Neubau"; vs 30% quota pledged by the private Bündnis = 2,386 → +4,613/yr; rent relief ~16%, €936/household/yr.
- Observed LWU baseline (V, KoopV reports): re-lettings 15,385 (2021), 14,740 (2022), 13,471 (2023), 12,398 (2024); to WBS holders 9,622 / 9,348 / 8,472 / 8,189; quota achieved 62.5% / 63.4% / 62.9% / 66.1% vs 63% target. Re-letting pool shrinking ~8%/yr ("konstant rückläufig").
- At 75% (campaign AöR quota) the same arithmetic gives ~8,300/yr (I). WBS holders with valid certificate ~51,000 (2023–24, S); applications 55–75k/yr (S, inconsistent).
- Counter-channel (empirica/Simons 2026, bank-commissioned, "grob und ausdrücklich ohne Anspruch auf Kausalität", V via DIW quote): turnover −13%, space per head +3% ≈ 7,200 dwellings' floor space withdrawn from circulation. Rent-control literature: 25 of 26 studies find lower mobility (Kholodilin 2024).

### 3.5 Transfers that already happened (Part A "übernommen" tap)
- LWU purchases of existing flats: 2021 3,067; 2022 11,644 (the Vonovia/DW sale: 14,750 flats + 450 commercial, €2.46 bn, HOWOGE ~8,300–8,671, berlinovo ~4,000, degewo ~2,400); 2023 512; 2024 238; 2025 4,609 (V). 2016–2019 cumulative ~19,435, 2019 ~12,000 incl. 5,964 ADO→Gewobag (S).
- Vorkaufsrecht + Abwendung: 1,851 (2019), 4,121 (2020), 2,350 (2021), 45 (2022), 54 (2023), 72 (2025) after BVerwG 4 C 1.20 of 09.11.2021 (V/S).
- People newly housed by transfers: zero; sold portfolio ~99% occupied; Vorkaufsrecht applies only to tenanted buildings (V/S).
- LWU stock 374,472 / 404,170 incl. Berlinovo (31.12.2025); 2022–25 LWU completions 18,896 (V).

### 3.6 Money
- Compensation estimates: Senate 2019–20 €29–36 bn (up to 39.5); Rechnungshof 2024 scenarios 8 / 11 / 29 / 36 bn, only the two low ones without permanent subsidy, annual subsidy ~€700m+ in the high cases; Holm/Thonke/Arpagaus 2025 base 10.1 bn, realistic 10–17, max ~21 (25.6 with cheaper finance); IMK 2026 13.5 bn for 210,000 flats; DIW Table 2: annual Land top-up from −€325m to +€1,142m depending on compensation and rent (V).
- Public build cost: WFB 2023 cap ~4,200–4,500 €/m² (KG 300–400, excl. land) (S) → 294k–315k €/flat at 70 m² (I). Dwelling-equivalents (I): 8 bn ≈ 25–27k; 10.1 ≈ 32–34k; 13.5 ≈ 43–46k; 21 ≈ 67–71k; 29 ≈ 92–99k; 36 ≈ 114–122k; 39.5 ≈ 125–134k. No all-in cost incl. land verified.
- Chilling-effect evidence: Vonovia CEO reportedly halting new Berlin projects after current ones (Nov 2026, S); 13,000-flat pledge of 2021 has no delivery audit found.

## 4. Proposed mechanism for the lever (to be reviewed)
- Part A, tap "Übernommen / angekauft": reader can allocate people to it; reveal: ~20,000+ flats changed to public hands 2019–2025 (table 3.5), people newly housed = 0; squares recolour, none fill.
- Part B lever panel "Vergesellschaften": (1) 222 squares recolour; (2) sub-lever "Vergabe": +7.0–8.3 thousand lettings/yr to WBS households (same flats, different tenants) against −7.2 thousand lock-in (empirica, contested) and the already-shrinking re-letting pool; (3) slider "Entschädigung" 8–39.5 bn € showing dwelling-equivalents as dotted squares; (4) toggle "Baupflicht der AöR": commission promise vs dissent as text, no squares; (5) risk band: 42–46% of completions by private companies (direction only).
- Vacancy card for the corporates: 2.07% vs 2.02% city; ~4,600 vacant of 222,000; no hidden pool.

## 5. Open items
- Zensus 2011 vacancy by owner type (not retrieved); vacancy-duration × owner type (table codes located, not downloaded).
- BBU by Unternehmensart (bbu.de 403); Vonovia/DW Berlin completions per year; 13,000-pledge audit; leerstandsmelder.de; Mieterverein vacancy counts.
- All-in construction cost incl. land; Pestel 58,000 primary; bulwiengesa primary; LWU 2015–2020 Ankauf by year.
- Brandenburg migration dataset; institutional-population share 2011 for the census household size; round-two (2022–25) ledger is estimate-grade.
- Adversarial review of the whole design (stage 4 brief) still not run.
