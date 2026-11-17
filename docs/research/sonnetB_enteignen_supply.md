# Sonnet B — Supply-side channels claimed for Vergesellschaftung (expropriation of large Berlin landlords)

Tagging: **VERIFIED** = I opened/rendered the primary document myself (PDF text extraction or rendered page image) and quote from it directly. **SECONDARY** = drawn from a WebSearch/WebFetch summary of a primary source I did not open myself (summarizer model risk). **INFERRED** = my own calculation/extrapolation, not stated by any source.

Caveat on method: one WebFetch call on the DIW PDF initially failed to parse the binary and a parallel WebFetch summary of the same report returned numbers I could not corroborate in the raw text (garbled digit-encoding in `pdftotext` output made verification hard). I therefore re-fetched the PDF, rendered each page to PNG with `pdftoppm`, and read the pages as images directly — all DIW figures below are confirmed this way and are VERIFIED, not taken from the earlier fetch summary.

---

## 1. Campaign's own supply claims (Deutsche Wohnen & Co. enteignen / Gemeingut Wohnen AöR)

- **Scale of transfer**: ~3,000+ Berlin-flat threshold; draft law would transfer **"rund 220.000 Wohnungen"** to public ownership (dwenteignen.de, "Unser Gesetz" page). SECONDARY/VERIFIED-partial (I fetched the page directly via WebFetch; it returned this one figure but stated the page itself contains no Neubau/Aufstockung/Entmietung claims — those live in linked PDFs — "Fact Sheet, law draft, and justification" — which I did not open). **Flagged gap**: the detailed AöR construction-mandate language (if any) is in those linked PDFs, not retrieved.
- **New-construction framing in public debate**: the initiative's position, as reported, is that new construction only relieves the market empirically "ab einer Leerstandsquote von zehn bis 20 Prozent" (vacancy rate of 10–20%) — i.e. they argue Neubau is largely ineffective at Berlin's current (~1.6%, see §3) vacancy rate, and that they are "nicht gegen Neubau" but don't rely on it for their case. SECONDARY (WebSearch synthesis citing taz.de/verfassungsblog.de coverage of the campaign's law-draft press conference, Oct 2023–2024).
- **Cost/financing study used by the campaign**: Andrej Holm, Friederike Thonke, Gian Arpagaus (2025), commissioned by the DWE initiative — "Refinanzierungsoptionen in vergesellschafteten Wohnungsbeständen." Base-case compensation **10.1 billion EUR**, full range across variants **3.1–20.4 billion EUR**, for ~240,000 flats (bibliographic detail VERIFIED via DIW aktuell Nr. 126's own footnote 4, see §6 below — I did not open the Holm et al. study itself, so the range number is SECONDARY as cited by DIW).
  - A separate DWE "Faktencheck" page (dwenteignen.de) states compensation of **"8 bis 18 Milliarden Euro"**, i.e. **"40 bis 60 Prozent des herkömmlichen Verkehrswerts"**, with **"zwischen 3,1 und 25,6 Milliarden Euro aus den Mieteinnahmen refinanzierbar"** without permanent subsidy, under entry rents of €6.00–8.00/m² and varying management standards/timeframes/financing instruments. SECONDARY (WebFetch summary of dwenteignen.de Faktencheck page; I did not independently render this page). No supply/Neubau claim appears on this page per the fetch.
  - None of the campaign material I could retrieve quantifies a *dwelling-count* effect of socialization (new units built, commercial conversions, or densification numbers). The campaign's own documented numbers are entirely about compensation/refinancing, not supply. **This is a structural finding, not a retrieval failure**: on the material available to me, the proponents do not publish a quantified supply-increase claim — only a qualitative one (see §2) and a legal "Eignung" (suitability) argument.

## 2. Expertenkommission Vergesellschaftung — Abschlussbericht, 27.06.2023

Source: `abschlussbericht_vergesellschaftung-grosser-wohnungsunternehmen-230627.pdf`, berlin.de/kommission-vergesellschaftung. **VERIFIED** — downloaded the PDF and extracted full text with `pdftotext -layout`; all quotes below pulled from that text.

**Majority report, §162–165 (within the "Erforderlichkeit"/necessity test)**:
> "163 Eine verstärkte Neubautätigkeit stellt keine Alternative dar, um das Ziel der Verbesserung der dauerhaften Versorgung mit bezahlbaren Wohnungen zu erreichen. Es ist jedenfalls alles andere als gesichert, dass sich Neubau in signifikantem Ausmaß dämpfend auf die Entwicklung von Mietpreisen auswirkt. ... Mieteffekte durch Neubau setzen ein reales Überangebot voraus ... Insbesondere auf angespannten Mietmärkten bleiben die sogenannten Sickereffekte von Neubau weitgehend aus (BBSR, Umzugsmobilität ... BBSR-Online-Publikation Nr. 11/2020, insb. S. 109 ff.)."
> "164 ... Die Senatsverwaltung für Stadtentwicklung hat ... ein ermitteltes Neubaupotential von 200.000 Wohnungen bis 2030 angegeben. Indes ist nur ein Viertel der entsprechenden Bauflächen landeseigen ... Die Förderung wird ... indes nur zu 10 bis 20% von privaten Bauträgern in Anspruch genommen..."

So the **majority's own case for socialization explicitly downgrades new construction as a lever** — it argues Neubau (even the Senate's own 200,000-by-2030 potential) is unreliable as policy, which is used to justify socialization as the *necessary* (not merely sufficient) alternative. This is a rhetorical point **against** relying on Neubau generally, not a claim that socialization itself will add net new units in large numbers.

**Majority report, §198 (within the proportionality/"Angemessenheit" section, listing goals Vergesellschaftung is said to serve)**:
> "198 In Bezug auf die Ziele der energetischen Gebäudesanierungen, des Neubaus durch Aufstockung und Nachverdichtung sowie einer diskriminierungsfreien und bedarfsgerechten Wohnungsvergabe ... verspricht die Vergesellschaftung einen hohen Beitrag zu leisten. ... Zu den gesetzlich vorgegebenen Kernaufgaben können auch ... eine effiziente und bedarfsgerechte Instandhaltung, Instandsetzung und Modernisierung der Bestände, als auch Vornahme von Neubau und Ankauf [gehören]."

This is the majority's **sole textual basis for a supply claim**: a promise ("verspricht ... einen hohen Beitrag zu leisten") that the AöR *could* be legally obligated to pursue Aufstockung/Nachverdichtung/Neubau/Ankauf as "Kernaufgaben" — but **no number is given anywhere in the majority report** for how many dwellings this would add. It is a legal-design possibility, not a quantified forecast.

**Sondervotum (dissenting opinion of 2–3 commission members), on exactly this point — directly rebuts the majority**:
> "Dass die Vergesellschaftung der großen Wohnungsunternehmen über Aufstockung und Nachverdichtung im vergesellschafteten Bereich zu einem signifikanten Anstieg des Wohnungsneubaus in Berlin insgesamt führen wird, ist nicht belegt und eher unplausibel. Vielmehr spricht einiges dafür, dass eine Vergesellschaftung großen Stils im verbleibenden privaten Wohnungsmarkt zu einer Bauzurückhaltung führen wird."
> (and, a few paragraphs earlier): "Insbesondere dürften große private Wohnungsunternehmen durch die Vergesellschaftung von einer Bautätigkeit in Berlin eher abgehalten werden." ... "Nachverdichtungen, Aufstockungen ... bedürfen jedenfalls auch in sozialisierten Wohneinheiten einer Steuerung durch die öffentliche Hand. Nur bei hinreichend konkretisierten und dauerhaft gesicherten Maßgaben ... dürfte die Eignung der Vergesellschaftung für das Erreichen der avisierten Gemeinwohlziele zu bejahen sein."

This is the single most important primary-source finding for the lever's supply component: **even the commission's own dissent, written by legal/constitutional experts (not economists), treats the "socialization increases supply via Aufstockung/Nachverdichtung" claim as an unverified assertion that would require a legally binding, concretely specified construction mandate in the law itself (not present in the draft they reviewed) to be credible — and considers a chilling effect on private building more plausible.**

## 3. Comparative build rates — LWU vs. private vs. cooperatives

- **DIW aktuell Nr. 126 (5 Oct 2026)** [see §6 for full citation] publishes a chart "Wohnungsunternehmen stellen gut 40 Prozent der neuen Wohnungen in Berlin fertig" (completions by Bauherren type, 2008–2025, source: Amt für Statistik Berlin-Brandenburg). **VERIFIED** (read directly off the rendered chart image, page 2/5 of the PDF):
  - Private/corporate "Wohnungsunternehmen" share of all Berlin completions: ~42% on average 2008–2025, **46% in 2025 specifically**.
  - "Öffentliche Bauherren" (public builders, i.e. LWU + AöR-type) share rose from ~0% (2008–2012) to a peak around 33% (~2021) then fell back to ~26% by 2025 — i.e. public building increased sharply after ~2016 but never caught up to and recently fell further behind the corporate/private share.
  - Absolute completions: Berlin-wide total peaked near 19,000/year around 2019, falling to **11,027 in 2025** (DIW text, p.1 — "so wenige wie zuletzt 2015").
  - 2024 building permits: **9,921 Wohnungen genehmigt**, a ~38% YoY drop, first time under 10,000 since 2012 (BBU Marktmonitor 2024, SECONDARY via WebSearch summary of bbu.de press materials).
- I did **not** obtain the disaggregated BBU Marktmonitor table split by Unternehmensart (LWU vs. Genossenschaften vs. private vs. Vonovia/Deutsche Wohnen specifically) — the WebSearch only surfaced top-line BBU 2024 figures (Leerstandsquote 1.6%, ~12,400 vacant units; Fluktuation 4.6% in 2024 vs >9% in 2008). That disaggregation (task item 3a–3d) needs a direct pull of the BBU Marktmonitor/Jahresstatistik PDF or Pressemappe, which I did not fetch in full; flagging as **not completed** rather than guessing.
- **Vonovia/Deutsche Wohnen Berlin-specific completions**: not retrieved from their annual reports directly. SECONDARY only via the 2021 "Zukunfts- und Sozialpakt Wohnen": Vonovia CEO Rolf Buch committed proceeds from selling ~14,754 Berlin flats (for ~€2.46bn, split Howoge >8,000 / Berlinovo >4,000 / Degewo ~2,500) toward **13,000 new Berlin apartments**, alongside a rent-increase cap to 2026 (WebSearch synthesis of taz.de, vonovia.com press release, tagesspiegel.de, Oct 2021). I could not verify from a primary source whether the 13,000-unit Neubau commitment was actually delivered — this is a pledge, not a completions figure, and should be tagged **INFERRED-RISK**: treat as aspirational unless a delivery audit is found.

## 4. Densification potential on Großsiedlungen (corporate large estates)

- A 2024 industry study (Syte/Probis/Pricehubble/Liwood, AI-based roof-extension mapping) found Berlin-wide **Aufstockung (rooftop extension) potential of up to ~8,000 dwellings**, largest in Neukölln (up to 1,167), Tempelhof-Schöneberg (up to 906), Pankow (up to 834). SECONDARY (WebSearch synthesis of Tagesspiegel/entwicklungsstadt.de/build-ing.de coverage).
- A separate Bulwiengesa/Berlin Hyp study on 1950s/60s Großsiedlungen estimated a **theoretical densification potential of 625,000 dwellings nationally** (not Berlin-specific; applies across German growth regions) — SECONDARY, and importantly this is national not Berlin-only, so cannot be allocated to the Vergesellschaftung lever without further disaggregation I did not find.
- I found **no Berlin-specific, estate-by-estate (Gropiusstadt / Märkisches Viertel / Hellersdorf) Nachverdichtung study with owner-attributed dwelling counts** (i.e. tagged to Vonovia/DW vs. LWU ownership). This item is **not completed** — the searches surfaced only the roof-extension and the national Bulwiengesa studies, neither owner-attributed nor estate-specific as requested. Flagging as a gap rather than guessing at numbers.

## 5. Rent/turnover channel — does lower rent reduce mobility and thus "lock up" flats?

**VERIFIED**, from DIW aktuell Nr. 126 (p. 5 of 7, rendered page read directly), citing a commissioned empirica study:
> "Eine Studie von empirica schätzt grob und ausdrücklich ohne Anspruch auf Kausalität, dass die Fluktuation in den Beständen um rund 13 Prozent sinken und der Wohnflächenverbrauch pro Kopf um rund drei Prozent steigen würde. Das entspräche der Fläche von rund 7.200 Wohnungen, die dem Markt entzogen werden."

Full citation (from DIW's own footnote 13, VERIFIED on p.6 image): **Harald Simons (2026), "Untersuchung zu den Auswirkungen einer Vergesellschaftung auf den Berliner Wohnungsmarkt," Gutachten der empirica AG im Auftrag von Berliner Sparkasse, Berliner Volksbank, DKB und IBB, Berlin.** Note the commissioning banks are private-sector institutions with an interest in the outcome — this is a bank-commissioned study citing an explicitly non-causal, "rough" estimate; DIW nonetheless adopts it as its central turnover-channel number.

DIW's broader framing (p.6, VERIFIED): rent-control literature review finds "In 25 von 26 Studien zeigt sich eine geringere Umzugsmobilität, und 14 von 17 Studien belegen steigende Mieten im nicht regulierten Segment," citing Kholodilin (2024, J. Housing Economics) and Mense/Michelsen/Kholodilin (2023, J. Urban Economics) — i.e. the "lock-in reduces effective availability" mechanism is treated by DIW as well-established in the wider rent-control literature, with the Berlin-specific 7,200-unit figure being the one Simons/empirica estimate layered on top.

I found **no published Vonovia- or Deutsche Wohnen-specific Fluktuationsrate for their Berlin portfolios** (task item 5's second half) — only the aggregate BBU-member Fluktuation of 4.6% (2024) vs >9% (2008), which blends all member types. Not completed as a company-level breakdown.

## 6. Finance channel — opportunity cost of public money

**VERIFIED**, DIW Berlin, Dany-Knedlik/Kholodilin/Kritikos/Kriwoluzky, **"Vergesellschaftung der Wohnungsunternehmen in Berlin belastet den Haushalt und schafft keine zusätzliche Wohnung,"** *DIW aktuell* Nr. 126, **5 October 2026**. ISSN 2567-3971, CC BY 4.0. I confirmed this is genuinely dated and genuinely exists (not a hallucination) by downloading the PDF and rendering all 7 pages as images and reading them directly — the document discusses the aftermath of a real (to-this-session) Oct 2026 Berlin state election won by Die Linke, and cites a "Rahmengesetz ... vom 18. März 2026 (GVBl. 2026, 138)" that is now apparently in force (takes effect 2028 per its own text).

Key quantified content (Table 1, compensation estimates across studies — VERIFIED, read off the rendered table image):

| Study | Dwellings | Method | Compensation (€bn) |
|---|---|---|---|
| Senat (2019/2020) | 226,000–240,000 | Verkehrswert (market value) | 29–36 (2020 update: up to 39.5) |
| Rechnungshof Berlin (2024) | 240,000 | Scenarios, budget consequences | 8 / 11 / 29 / 36 |
| Holm et al. for Initiative DWE (2025) | 240,000 | Refinanzierbarkeit aus Mieten | 10.1 (realistic range 10–17) |
| IMK / Hans-Böckler-Stiftung, Dullien et al. (2026) | 210,000 | Ertragswert, 4% real, 40 yrs + Boden | 13.5 |

DIW's own Table 2 (fiscal subsidy scenarios, VERIFIED off rendered image) — annual Land Berlin top-up required, by compensation level and target rent, for 240,000 units at avg. 61 m²:

| Compensation | Rent €6/m² (annual, €m) | Rent €7/m² | Rent €8/m² |
|---|---|---|---|
| €8bn | +26 | −149 | −325 |
| €13.5bn | +318 | +143 | −33 |
| €21bn | +717 | +541 | +366 |
| €29bn | +1,142 | +966 | +791 |

(Negative = AöR runs a surplus; positive = Land Berlin must subsidize annually, in perpetuity, not a one-time cost.)

DIW's framing of the opportunity cost / "no additional dwelling" argument (direct quotes, VERIFIED):
> "Die Vergesellschaftung schafft keinen zusätzlichen Wohnraum und würde Investoren verschrecken. Damit wirkt sie sowohl auf das Angebot als auch auf die Nachfrage in die falsche Richtung: Das Angebot dürfte weiter schrumpfen, die Nachfrage wegen der günstigeren Mieten aber steigen."
> "Jede Zuzahlung an die AöR vergrößert diese Lücke und konkurriert unmittelbar mit anderen Ausgaben des Landes, etwa für Kitaplätze oder Schulsanierungen. Eine zusätzliche Wohnung entsteht dadurch nicht."
> "Wohnungsunternehmen haben zwischen 2008 und 2025 im Schnitt 42 Prozent der neuen Wohnungen fertiggestellt, 2025 sogar 46 Prozent. Diese Lücke müssten landeseigene Unternehmen und die Anstalt schließen. Gerade ihnen dürften aber die Kapazitäten fehlen, denn mit bis zu 240.000 Wohnungen wäre die AöR fast dreimal so groß wie die größte landeseigene Gesellschaft."
> "Berlin hat ein Mengenproblem. Der Stadt fehlen über 100.000 Wohnungen ... Die Vergesellschaftung ändert an dieser Zahl nichts..."

Context numbers also VERIFIED from the same report: Berlin 2026 budget deficit ~€4.6bn; 2028/2029 structural gaps €5.0bn/€5.4bn even after maximum borrowing; credit-financing ratio 8.8% vs permitted 6.7% ceiling (Stabilitätsbericht 2025, Senat von Berlin, Drucksache 19/2711, 15 Oct 2025); Senate's 2040 new-build need estimate **211,000 dwellings, of which 138,000 needed just to relieve the tight market** (≈14,000/year), against actual 2025 completions of only 11,027.

Institute der deutschen Wirtschaft / IW Köln (Deschermeier & Voigtländer 2026), commissioned by Berliner Sparkasse/Berliner Volksbank/DKB/IBB — "hält [eine Entschädigung] unter 15 Milliarden Euro für sehr wahrscheinlich," i.e. argues courts would likely require compensation well above the campaign's own 8–18bn range, with consequent bank-security/refinancing risk to the sector generally — SECONDARY relative to me (cited via DIW's footnote, not opened directly, but DIW's citation is itself VERIFIED).

**Rechnungshof von Berlin (2024), "Bericht nach § 88 Abs. 2 LHO zu den Auswirkungen einer Vergesellschaftung großer Wohnungsunternehmen auf den Landeshaushalt"** — I did not independently retrieve/open this report; its headline figures (8/11/29/36bn scenarios, "nur die beiden niedrigen ohne dauerhafte Zuschüsse finanzierbar") are VERIFIED only via DIW's citation of it (DIW footnote 6, Table 1), which I consider reliable since DIW is itself a verified primary source quoting it precisely, but I have not independently confirmed the Rechnungshof text itself. Tag: **SECONDARY** (one level removed).

## 7. Academic/think-tank evaluations — summary of who says what

| Source | Position on supply effect | Status |
|---|---|---|
| DIW Berlin (Dany-Knedlik/Kholodilin/Kritikos/Kriwoluzky), Oct 2026 | Explicitly: "schafft keine zusätzliche Wohnung"; predicts Neubau *decline* because corporate builders (42–46% of completions) would be deterred/removed from the market | VERIFIED |
| Expertenkommission majority, Jun 2023 | No quantified claim; qualitative "verspricht hohen Beitrag" to Neubau via Aufstockung/Nachverdichtung IF legally mandated in detail | VERIFIED |
| Expertenkommission Sondervotum (dissent), Jun 2023 | Explicitly: "nicht belegt und eher unplausibel" that socialization raises Berlin-wide Neubau; expects Bauzurückhaltung in remaining private market instead | VERIFIED |
| empirica (Simons 2026, bank-commissioned) | No net supply effect claimed; ~13% fall in Fluktuation ≈ 7,200 dwellings' worth of floor space "removed" from effective circulation | VERIFIED (via DIW citation + quote) |
| IW Köln (Deschermeier/Voigtländer 2026, bank-commissioned) | Compensation risk >15bn likely; implies financing/collateral stress rather than a supply claim | SECONDARY |
| IMK/Hans-Böckler-Stiftung (Dullien et al. 2026) | Focused on compensation financeability (13.5bn, "finanzierbar"), not on construction/supply | SECONDARY (title only; did not open) |
| Holm/Thonke/Arpagaus for DWE (2025) | Focused on refinanceability (10.1bn base case), not on construction/supply | SECONDARY (via DIW citation) |

**No academic or think-tank source I could access — including the pro-Vergesellschaftung commission majority and the campaign's own commissioned studies — publishes a quantified dwelling-count increase attributable to socialization.** The only concrete, numeric *supply-side* claims in the entire corpus run in the opposite direction (DIW's 42–46% corporate-completions share at risk; empirica's ~7,200-unit turnover-equivalent loss).

---

## (a) Table of every quantified supply channel

| Channel | Dwellings claimed | By whom | Source | Date | Tag | Depends on ownership change? |
|---|---|---|---|---|---|---|
| Direct transfer (stock moved to AöR) | ~220,000–240,000 | Expertenkommission / DWE / Senate (common figure) | Multiple, converging | 2019–2026 | VERIFIED | No — pure transfer, zero net units, this is the "zero" already modeled |
| Legal mandate for Aufstockung/Nachverdichtung/Neubau "Kernaufgabe" | Not quantified ("hohen Beitrag") | Expertenkommission majority | Abschlussbericht §198 | 27.06.2023 | VERIFIED | Yes, but only if written into law; no number given |
| Rebuttal: no Berlin-wide Neubau increase from Aufstockung/Nachverdichtung | 0 (explicitly "nicht belegt") | Expertenkommission Sondervotum | Abschlussbericht, Sondervotum | 27.06.2023 | VERIFIED | N/A — denies the mechanism |
| Senate's own 2030 Neubaupotential (cited by majority as insufficient reason to reject socialization) | 200,000 by 2030 | Senatsverwaltung für Stadtentwicklung | cited in Abschlussbericht §164 | (hearing 09.06.2022) | VERIFIED (citation within VERIFIED doc) | No — this is the general Neubau alternative, not AöR-specific |
| Senate's 2040 need estimate | 211,000 total / 138,000 to relieve tight market (~14,000/yr) | Senat | cited in DIW aktuell 126 | 2026 | VERIFIED | No |
| Actual 2025 Berlin completions | 11,027 | Amt für Statistik Berlin-Brandenburg | DIW aktuell 126 | 2026 | VERIFIED | No |
| Corporate ("Wohnungsunternehmen") share of completions at risk under socialization | 42% avg 2008–2025, 46% in 2025 | DIW (Amt für Statistik data) | DIW aktuell 126 | 2026 | VERIFIED | Yes — DIW's central mechanism: removing/deterring this share *reduces* supply |
| Turnover/"lock-in" loss (availability, not stock) | ~13% Fluktuation drop ≈ 7,200 units' worth of floor space | empirica (Simons), bank-commissioned | cited in DIW aktuell 126 | 2026 | VERIFIED (via DIW's direct quote) | Yes — but reduces availability, doesn't create or destroy dwellings |
| Vonovia 2021 pact Neubau pledge | 13,000 new Berlin units (pledged, delivery not verified) | Vonovia CEO Rolf Buch | Vonovia press release / taz.de | Oct 2021 | SECONDARY, pledge only | No — this predates and is unrelated to the socialization lever; it's a private-sector commitment made partly *to avert* broader expropriation pressure |
| Roof-extension (Aufstockung) technical potential, city-wide | up to ~8,000 | Syte/Probis/Pricehubble/Liwood industry study | Tagesspiegel et al. | 2024 | SECONDARY | No — not owner-attributed; applies regardless of who owns the buildings |
| National Großsiedlungen densification potential | 625,000 (nationwide, not Berlin) | Bulwiengesa/Berlin Hyp | immobilienmanager.de | 2024 | SECONDARY | No — national, not owner-attributed |
| Compensation→opportunity-cost (no dwelling-equivalent given) | €21–36bn one-off + €366m–1.14bn/yr forever | DIW / Rechnungshof / Senate | DIW aktuell 126, Table 2 | 2026 | VERIFIED | Indirect — money diverted from "Kitaplätze, Schulsanierungen," not explicitly converted to a foregone-dwellings figure by any source I found |

## (b) Strongest data-backed version of the "expropriation increases supply" case

It is thin. The only textually explicit, even qualitative, supply-increase claim from a pro-Vergesellschaftung source is the Expertenkommission majority's §198: Vergesellschaftung "verspricht einen hohen Beitrag zu leisten" to Neubau via Aufstockung and Nachverdichtung, *if* the enabling law locks the AöR into binding, durable construction/investment obligations as a statutory "Kernaufgabe." This is a legal-design argument ("if structured correctly, the new public owner can be compelled to build, unlike a private landlord who can simply choose not to") rather than an empirical one — no dwelling count, no timeline, no cost estimate accompanies it anywhere in the 230+-page report. The campaign's own draft law and cost studies do not fill this gap with numbers either; their quantified work is entirely about compensation and refinancing, not output.

A fair secondary case: removing profit-maximization incentives *could* in principle increase willingness to hold rents low and avoid "Entmietung"/luxury modernization displacement — but no source quantifies this as a *dwelling-count* effect (it is a quality/tenure-security claim, not a supply claim), and it's exactly what the lever currently models as the "transfer" (zero net units) component.

## (c) Strongest data-backed rebuttal

DIW aktuell Nr. 126 (Oct 2026) is the only source that puts numbers on both sides of the ledger simultaneously, and its central empirical point is structural, not just a cost argument: Berlin's private/corporate landlords (the very class targeted by the ≥3,000-unit threshold) built **42–46% of all new Berlin housing 2008–2025**, while the public sector's completions capacity, even after a decade of catch-up investment, has never exceeded ~33% of the total and the AöR created by socialization "wäre fast dreimal so groß wie die größte landeseigene Gesellschaft" — i.e. capacity-constrained from day one. Layered onto this is the empirica/Simons turnover estimate (~7,200-unit-equivalent reduction in effective availability from lower Fluktuation) and the Expertenkommission's own Sondervotum calling the Neubau-via-socialization mechanism "nicht belegt und eher unplausibel," predicting Bauzurückhaltung (building restraint) in the remaining private market instead. Together these give a coherent, number-backed case that the lever's *dwelling count* effect is not merely zero but plausibly negative if the ≥42% private completions share contracts while the AöR cannot absorb the gap — though no source quantifies that negative number precisely (DIW stops at "dürfte... sinken," a direction, not a figure).

## (d) What remains unverified / not retrieved

- BBU Marktmonitor/Jahresstatistik disaggregated table (Neubau and Leerstand by Unternehmensart: LWU vs. Genossenschaften vs. private vs. BBU-members overall) — only top-line 2024 figures found, not the full table.
- Vonovia/Deutsche Wohnen Berlin-specific annual completions and Aufstockung units from their own annual reports — not retrieved; only the 2021 pact pledge (13,000 units), with no delivery audit found.
- Company-level (Vonovia/DW) Fluktuationsrate for Berlin — not found; only BBU-aggregate (4.6% in 2024).
- Estate-specific, owner-attributed Nachverdichtung potential for Gropiusstadt/Märkisches Viertel/Hellersdorf — not found; only city-wide (roof-extension) and national (Bulwiengesa) studies, neither owner-attributed.
- Rechnungshof Berlin (2024) report itself — only read via DIW's citation, not opened directly.
- The DWE draft law's and "Fact Sheet"/Begründung PDFs (linked from dwenteignen.de/unser-gesetz) — not opened; these are the most likely place a campaign-side Neubau/Aufstockung/Entmietung quantification would live, if one exists, and I could not confirm or rule it out.
- IMK Policy Brief Nr. 225 (Dullien et al. 2026) and Holm et al. (2025) themselves — only read via DIW's citations/footnotes, not opened directly.
