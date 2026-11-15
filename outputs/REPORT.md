# From completions to residents: Berlin vs Copenhagen, 2010–2025

## Answer

Yes — at district level, new dwelling completions are a strong, statistically
significant predictor of subsequent population change in both cities, and the
cross-sectional (cumulative, 2010–2024) relationship is close to linear and
tight. But the implied **residents per new dwelling is systematically above
plausible household size** in both cities (roughly **2.0** pooled, vs. **~1.8**
average household size in Berlin and **~1.9-2.0** in Copenhagen) and is **not
stable** across specifications: it varies with whether you use same-year or
lagged completions, with the completions measure chosen, and — for Copenhagen
— with how the stock-based completions proxy is calibrated. The year-to-year
relationship is noisier and smaller than the cumulative one, which is the
more trustworthy estimate here. The gap above the household-size benchmark is
consistent with completions not being the only channel into a district's
population (in-migration into existing stock, household formation/shrinkage,
student/co-living units with unusually high occupancy) rather than with
vacancy, which would push the coefficient *below* household size, not above
it.

## Key coefficients ("residents per completed dwelling")

| Specification | City | Coefficient | 95% CI | N | R2 |
|---|---|---:|---|---:|---:|
| Same-year, district+year FE | Berlin | 0.81 | 0.12 - 1.50 | 180 | 0.65 |
| Lag-1 year, district+year FE | Berlin | 0.58 | -0.46 - 1.61 | 180 | 0.64 |
| Same-year, new-residential only | Berlin | 0.84 | 0.11 - 1.58 | 180 | 0.65 |
| Same-year, district+year FE | Copenhagen | 1.48 | 1.22 - 1.73 | 150 | 0.81 |
| Lag-1 year, district+year FE | Copenhagen | 1.29 | 0.98 - 1.61 | 150 | 0.76 |
| Cumulative 2010-2024, cross-section (12 districts) | Berlin | 2.02 | 1.35 - 2.70 | 12 | 0.82 |
| Cumulative 2010-2024, cross-section (10 districts) | Copenhagen | 2.11 | 2.01 - 2.20 | 10 | 0.997 |
| Pooled cumulative, city FE | Both | 2.04 | 1.98 - 2.10 | 22 | 0.93 |

Full tables: `regression_results.csv`, `robustness_results.csv`.

## How to read this

- **Annual panel regressions** (district + year fixed effects, clustered SEs
  by district) use only within-district, within-year deviations — i.e. they
  strip out city-wide shocks (Berlin's 2013 register/census correction,
  2015-16 migration wave, 2020-21 COVID, 2022 Ukraine arrivals) and
  cross-district level differences. These are noisier because annual
  completions and annual net migration don't line up tightly in any one year
  (construction lags, lease-up time, reporting timing). Still, Berlin's
  same-year coefficient (0.81) and Copenhagen's (1.48) are both positive and
  significant; lagging completions by one year weakens both, so most of the
  pop-change response shows up the same calendar year completions are
  recorded, not with a one-year delay.
- **The cumulative cross-section** (sum of 2010-2024 completions vs. sum of
  2010-2024 population change, one point per district — 12 Berlin Bezirke +
  10 Copenhagen bydele) averages out annual noise and reporting lags, and fits
  very tightly (R2 0.82 Berlin, 0.997 Copenhagen). This is the more reliable
  estimate of the long-run relationship: roughly 2.0 residents gained per
  completed dwelling in both cities over the period, pooling to 2.04 with a
  narrow CI. See `cumulative_scatter.png`.
- **Benchmark comparison**: average household size is ~1.8 persons/dwelling
  in Berlin and ~1.9-2.0 in Copenhagen. The cumulative coefficients (2.0-2.1)
  sit above both benchmarks — a new dwelling is associated with more
  population growth than one new household's worth. Below-benchmark would
  suggest vacancy or dwellings not translating into residents; above-benchmark
  (what we see) is more consistent with new building also triggering
  in-migration into the existing stock nearby (knock-on effects: amenities,
  jobs, induced moves) or occupancy patterns in new-build units (co-living,
  larger households, students) that exceed the city average. It could also
  partly reflect reverse causality / simultaneity — developers building
  where demand and in-migration are already concentrated — which this design
  cannot fully rule out without an instrument for completions.

## Shares check: does growth concentrate where building happens?

District shares of cumulative completions line up closely with district
shares of cumulative population growth in both cities
(`district_shares_cumulative.csv`): e.g. Berlin's Pankow has ~14% of
completions and ~13% of population growth; Mitte ~12% of completions vs ~14%
of growth; Copenhagen's Amager Vest ~27% of completions and ~25% of growth.
No district is a large outlier in either direction, reinforcing that
completions and population growth move together spatially, not just in
aggregate.

## Robustness

| Check | City | Coefficient | 95% CI |
|---|---|---:|---|
| Drop 2013 (census adj.) & 2025 (provisional) | Berlin | 0.67 | -0.03 - 1.37 |
| Drop 2025 (provisional) | Copenhagen | 1.52 | 1.25 - 1.79 |
| Use `dwellings_new_residential` instead of total, drop 2013/2025 | Berlin | 0.71 | -0.02 - 1.44 |
| Scale Copenhagen's KKBOL1 by the year-specific BYGV22/KKBOL1 ratio, drop 2025 | Copenhagen | 1.88 | 1.53 - 2.22 |

Dropping the Berlin 2013 census-correction year and both cities' 2025
provisional year weakens the same-year Berlin coefficient (0.81 to 0.67,
losing significance) — a reminder that part of the headline same-year
estimate is leveraged by a one-off register adjustment, not genuine
completions-driven growth. Swapping to `dwellings_new_residential` barely
moves Berlin's estimate, so the broader "total" measure (which includes
conversions/extensions) isn't driving the result. For Copenhagen, calibrating
KKBOL1 down to the true BYGV22 completions flow (KKBOL1 overstates true
completions by ~10-50% in most years per `copenhagen_NOTES.md`) raises the
implied residents-per-dwelling to 1.88, since the same population change is
now attributed to fewer "true" completions.

## Caveats — what this data can and cannot say

1. **Copenhagen's district-level completions are not a true flow.** KKBOL1 is
   dwelling stock as of the 2026 reference date, broken out by the year a unit
   was first occupied — any unit since demolished, merged, or reclassified
   never appears. It is a lower-bound/proxy for completions, consistently
   ~5-55% above the genuine municipality-wide completions flow (DST BYGV22,
   no bydel breakdown exists). The scaled-ratio robustness check is the best
   available correction, but it's a municipality-wide average ratio applied
   uniformly across districts, which may not hold district-by-district.
2. **Berlin's population series has a known register/census break.** The
   2011 census found the register-based count overstated; Berlin's official
   series was revised down around 2013, which shows up as an anomalous
   population swing in 2013 independent of any construction activity. All
   results are reported both with and without that year.
3. **2025 is provisional in both datasets** (Berlin's F II 2 2025 report and
   Copenhagen's KKBOL1 2026-reference update both flagged as partial/latest-
   available rather than final) — excluded in robustness checks.
4. **Population change is overwhelmingly a migration phenomenon, not a
   housing-supply phenomenon**, especially at annual frequency: net migration,
   birth/death balance, and household formation/dissolution in the existing
   stock move population independent of new construction. The fixed-effects
   design only identifies the part of the relationship that varies within a
   district over time net of city-wide shocks — it is not a structural causal
   estimate of "how many people would NOT have come had this dwelling not been
   built."
5. **Reverse causality / simultaneity**: developers build more where
   population and demand are already growing (and where land/zoning allow
   it), which biases the coefficient upward (completions "chasing" growth)
   relative to a pure supply effect. This analysis cannot separate that from
   a genuine supply effect without an instrument (e.g., zoning changes,
   permitting lags) for completions.
6. **Household-size benchmark is a single national-ish average**; new-build
   household size (more smaller/larger units, student housing, co-living) can
   differ systematically from the existing-stock average used as the
   benchmark, so deviations from it are not proof of vacancy or overcrowding.

## Output files

- `panel.csv` — full year x district x city panel (completions, population,
  pop_change, completions per 1,000, lagged completions).
- `skim_summary.txt` — skimpy descriptive summary of the panel.
- `city_year_totals.csv` — city-year totals of completions/population/pop change.
- `district_shares_cumulative.csv` — district shares of cumulative completions vs. population growth, 2010-2024.
- `regression_results.csv`, `robustness_results.csv` — all fixed-effects and robustness regression coefficients, CIs, N, R2.
- `copenhagen_calibration_ratio.csv` — year-by-year BYGV22/KKBOL1 scaling ratio used in the Copenhagen robustness check.
- `small_multiples_berlin.png`, `small_multiples_copenhagen.png` — per-district completions (bars) vs. population change (line), 2010-2025.
- `cumulative_scatter.png` — cumulative 2010-2024 completions vs. population change by district, fitted line vs. household-size benchmark line, both cities.
- `completions_per_1000_timeseries.png` — city-level completions per 1,000 residents, Berlin vs. Copenhagen, 2010-2025.

## Note on intercepts (added after review)
The cumulative cross-section fits have very different intercepts, which matters for interpretation:
- Berlin: intercept 11,095 residents per district, slope 2.02. That is 3.9% of the average 2010 district population growing with zero completions.
- Copenhagen: intercept 1,397 residents per district, slope 2.11. That is 2.6% of the average 2010 district population growing with zero completions.

Berlin districts gained roughly 11,000 residents each over 2010-2024 independent of building, so roughly a quarter of Berlin's total growth (about 133,000 of some 520,000) was absorbed by the existing stock (smaller households filling up, register effects, in-migration into vacancies). The slope of about 2 applies only to the increment above that. Copenhagen's intercept is near zero: district growth there tracks new dwellings almost one-to-one, which is also why its R-squared is so high. Part of that tightness is mechanical, since KKBOL1 counts dwellings that exist today by commissioning year, and dwellings that exist today are by construction occupied.
