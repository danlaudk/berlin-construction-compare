# Opus prompts for the "Enteignen" lever and the two-round Part A game 
# (proposed, not yet dispatched)

Inputs available to all three: docs/die-luecke-design.md and docs/research/* (stage1–3b, sonnetA/B/C, stage4 brief).
Scratchpad for downloads: the session scratchpad directory. No writes into the repo.

## Sonnet 1 — Census vacancy by owner type, and the public cost per new flat

You are a data analyst with browser tools (Playwright MCP). No repo writes. Write the full report to 
<scratchpad>/opus1_owner_vacancy_cost.md plus a CSV of extracted figures; reply with the path and five lines. Tag 
VERIFIED / SECONDARY / INFERRED.

1. Open https://ergebnisse.zensus2022.de in the browser. Locate table 4000W-3006 "Wohnungen: Art der Wohnungsnutzung – Eigentumsform des Gebäudes" (and neighbouring 4000W tables) for Berlin (Land) and, if the regional selector offers Berlin's Bezirke or Stadtteile, per Bezirk. Extract dwellings and vacant dwellings per owner type (Privatpersonen, WEG, privatwirtschaftliche Wohnungsunternehmen, kommunale/öffentliche Unternehmen, Genossenschaften, other). Also the vacancy-duration and vacancy-reason tables crossed with owner type where the database allows. Save as CSV with the table code, region, date 15.05.2022. Do the same for Zensus 2011 (ergebnisse2011.zensus2022.de or the Zensus 2011 database) for Berlin.
2. Compute vacancy rate per owner type and compare: are privatwirtschaftliche Unternehmen above or below the Berlin average (1.97%)? Reconcile with the company disclosures already collected (Deutsche Wohnen 0.7%, BBU 1.6%).
3. Public construction cost per new dwelling in Berlin, verified: Senate Wohnungsbauförderungsbestimmungen (cost caps per m²), LWU annual results press releases 2022–2026 (investment per completed flat), Howoge/degewo/Gewobag annual reports (Baukosten per m² or per Wohnung), IBB Wohnungsmarktbericht construction cost tables, and Destatis Baukosten index for Berlin. Give €/m² and €/flat with date and definition (Kostengruppen 300–400 vs all-in incl. land).
4. Convert each compensation estimate (8, 10.1, 11, 13.5, 21, 29, 36, 39.5 bn €; sources in sonnetB and sonnetC) into new-dwelling equivalents at that cost, as a table, labelled INFERRED with the cost assumption shown.

## Sonnet 2 — Historical transfers 2011–2025 and the allocation baseline (REVISED after Sonnet C)

You are a data researcher. No repo writes. Use WebSearch/WebFetch, read-only shell (curl with a browser User-Agent, pdftotext) and the Playwright browser tools for sites that refuse scripts (bbu.de, leerstandsmelder.de). Write the full report to <scratchpad>/opus2_transfers_allocation.md; reply with the path and five lines. Tag VERIFIED / SECONDARY / INFERRED.

Already done, do NOT redo: Bernt & Holm 2023 (7,000/yr = 222,000 × 5% × 63%, "ohne Zuwachs durch Neubau"), the campaign's Gesetz/Begründung/Factsheet/AöR concept (75% quota), Holm et al. 2025, IMK 225, Rechnungshof 2024, Expertenkommission quotes, DIW aktuell 126 — all in docs/research/sonnetB and sonnetC. Build on them.

1. Per-year series 2011–2025 of existing flats that moved into public ownership: (a) LWU Ankauf per year from the Senate's LWU results press releases (berlin.de/rbmskzl, "Landeseigene Wohnungsunternehmen" 2015–2026) and the Wohnraumversorgung Berlin AöR annual reports; (b) the 2021 Vonovia/Deutsche Wohnen sale: 14,750 flats split by buyer (HOWOGE, berlinovo, degewo) and by seller, with the Senate press release; (c) Vorkaufsrecht: flats acquired and flats under Abwendungsvereinbarung per year from all nine Senate reports (Berichte über die Wahrnehmung von Vorkaufsrechten, 2017–2026); (d) Genossenschaft purchases funded by the Senate's Genossenschaftsförderung if reported. Deliver one table: year | flats bought by LWU | Vorkauf | Abwendung | total into public/non-profit hands | source. Then state the people newly housed by these transfers and justify the figure (expected: zero, the flats were occupied; cite the occupancy evidence).
2. The allocation baseline for the lever: from the Wohnraumversorgung Berlin AöR annual reports 2018–2025, extract per year the LWU lettings to WBS holders (Bernt & Holm's 9,349/yr average 2016–2021) and the LWU WBS quota actually achieved vs the 63% target; from the Kooperationsvereinbarung 2017/2021/2024 the quota rules. Also WBS holders registered per year (Drs. 19/12259 and later) so the 7,000 can be shown against demand. Note the 63% vs 75% quota discrepancy and compute the lever at both (6,999 vs ~8,325/yr, INFERRED).
3. BBU Jahresstatistik / Marktmonitor 2022–2024 by Unternehmensart (kommunal, genossenschaftlich, privat): Leerstand, Fluktuation, Neubau-Fertigstellungen, Modernisierungsleerstand. Use the browser if bbu.de returns 403. Extract the tables with dates.
4. Vonovia/Deutsche Wohnen Berlin: completions per year 2019–2025 and Aufstockung units from their annual reports and the deutsche-wohnen.com facts page (1,230 in 2024, 652 in 2025 already verified), plus any monitoring of the 2021 Zukunfts- und Sozialpakt 13,000-flat pledge (Schriftliche Anfragen on "Zukunfts- und Sozialpakt Wohnen Umsetzung").
5. Milieuschutz: number of Erhaltungsgebiete and flats covered, latest Senate figure, as context for the "Besitzer wechseln / schützen" lever group.
6. If time allows: leerstandsmelder.de Berlin via browser (entry count, last update); Berliner Mieterverein MieterMagazin articles with Leerstand/Entmietung counts at Deutsche Wohnen/Vonovia.

End with: a per-year transfer table; the allocation-lever card numbers at 63% and 75%; and the list of what stays unverified.

## Opus 3 — Design review of the expropriation lever and the two-round game

You are three hostile reviewers in turn (campaigner, official statistician, data-journalist fact-checker). Read docs/die-luecke-design.md, all files in docs/research/, and the outputs of Opus 1 and 2. No repo writes. Write the full report to <scratchpad>/opus3_design_review.md; reply with the path and five lines.

Campaigner: is "222 squares recoloured, 0 added" fair when the campaign's goal is rent and allocation, not supply? Is the allocation gain (7,000–8,300/yr to WBS households) given equal visual weight to the lock-in loss (7,200, bank-commissioned, non-causal)? Does the compensation-to-dwellings conversion smuggle in a false counterfactual (the Land would not otherwise spend 8–39 bn on building)? Use the campaign's Neubau position ("nicht gegen Neubau"; relief only above 10–20% vacancy) and IMK's "Neubau in großem Stil ist der einzige Weg" and say which the piece must quote.
Statistician: are the two rounds' taps additive and non-overlapping (new build, ex-vacant, other use, shelters, densification, transfers, Brandenburg)? Can round two (2022–2025) be revealed with census-grade confidence or must it be marked estimated? Is census household size "flat at 1.79" robust to the institutional-population assumption? Does the "transfers housed zero people" claim hold given the 450 commercial units and any vacant flats in the 14,750?
Fact-checker: re-derive 6,999, 7,200, 42–46%, the compensation table, 14,750, and the per-year transfer totals from the primary documents and state whether each survives a correction request; flag any card where date, definition or spatial unit would mislead.
Then propose: the exact German on-screen wording for the "Übernehmen / Vergesellschaften" tap in Part A and the lever panel in Part B (slider for compensation, sub-lever for allocation vs lock-in, toggle for build mandate with the commission's promise and dissent as text), the reveal numbers per tap for each round, and the dial-to-137,000 bridge text, every number tagged. Finish with a must/should/could list and a verdict on survivability.
