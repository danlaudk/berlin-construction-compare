# Stage 4 brief — adversarial review (NOT RUN; saved for later)

Intended agent: Opus, general-purpose, WebSearch/WebFetch + read-only shell. No repo writes.
Inputs to read first (in docs/research/): stage1_datasets_report.md, stage2_levers_report.md,
stage3a_gap_report.md, stage3b_verify_report.md, and the design document
docs/die-luecke-design.md.

## Prompt

You are three hostile reviewers in turn. Attack the design and its numbers; do not rewrite them.
Write your full report to <path>/stage4_adversarial_review.md and reply with the path and five lines.

**Reviewer A — Deutsche Wohnen & Co. enteignen campaigner / Mietenbewegung.**
Find every place the visualisation could be called biased. In particular:
- Does showing expropriation as "222 squares recoloured, 0 added" misrepresent the campaign's aims
  (rent stabilisation, anti-displacement, not supply)? Quote the campaign's own stated goals.
- Is there any published evidence that socialised/public landlords build more per flat owned than
  private ones (LWU completions per 1,000 flats vs Vonovia Berlin completions per 1,000 flats)?
- Does the Rechnungshof "11 bn €" threshold deserve the prominence we give it, given the
  Expertenkommission majority view on below-market compensation?
- Is "Neubau" the right counterfactual when 2017–2022 completions of 15–19k/yr coincided with
  the steepest rent rises? Find the data a campaigner would use (Angebotsmieten vs completions).
- Are we hiding that most new-build is high-rent and that Sozialbindungen expire (−46k 2024–34)?

**Reviewer B — official statistician (Amt für Statistik Berlin-Brandenburg).**
- Is definition (ii) (census-anchored growth 9.5.2011→31.12.2025 ÷ MZ-2024 Bezirk household size
  − completions 2012–2025) methodologically clean? Check: May vs January timing (~2,900
  completions), institutional population (~90k not in private households), Bezirk-level
  census-anchored population for 2012–2021 does not exist and must be estimated, Mikrozensus
  breaks 2016/2020/2022, rounding of Bezirk household sizes to 0.01 from thousands-rounded tables.
- Is the claim "household size is rising because of shortage" defensible, or is it migration
  composition (families from Ukraine 2022, fewer students), ageing, or the 2020 redesign?
  Decompose if any source allows (MZ household size by nationality or age; A I 17 register
  households 2022–2025).
- Is it legitimate to compare census 2022 vacancy (2.0%), StEP's "1.1%", and empirica's 0.3%
  on one chart? Define each and say which can be shown together.
- Is the "Wohin sind 408.000 Menschen gezogen?" decomposition additive? Which components overlap
  (people in shelters are inside the census-anchored population; vacancy absorption is already in
  the stock numbers)? Propose a non-overlapping decomposition and the dataset for net migration
  Berlin↔Brandenburg per Bezirk (A III 1 Wanderungen, or the Open Data "Wanderungen nach
  Bezirken" CSV) with years, variables, format.
- Should the headline use completions (flow) or F I 1 stock change (which includes conversions and
  demolitions and the two rebasings)? Quantify the difference per Bezirk if possible.

**Reviewer C — data journalist fact-checker (Tagesspiegel/Correctiv style).**
- Re-derive the five numbers most likely to be quoted from the piece (32,000 gap; 408,000 growth;
  188,428 completions; 5,400 market-active vacancy; 222,000 expropriation scope) from their
  primary sources and state whether each would survive a correction request.
- Check the three numbers the design still marks as secondary (Pestel 58,000; bulwiengesa 30,000
  office conversions; LWU vacancy 2.1%) against primary PDFs.
- Flag any figure where the reference date, definition, or spatial unit on the card would be
  misleading to a lay Berliner (e.g. "Ferienwohnungen 8,446" = Airbnb entire-home listings on
  19.09.2026, not registered holiday flats).
- Identify the single most damaging "but what about…" rebuttal and the data that answers it.

Finish with a ranked list of required changes (must / should / could), each with the data source
that fixes it, and a one-paragraph verdict on whether the piece as designed would survive
publication.
