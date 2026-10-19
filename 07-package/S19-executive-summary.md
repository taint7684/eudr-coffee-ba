# Executive Summary — EUDR-Ready Coffee Traceability (Đắk Lắk, Vietnam)

*Independent BA portfolio project · October 2026 · Not legal advice · Synthetic data is labelled*

## Problem

From **30 December 2026**, coffee placed on the EU market must be deforestation-free after 31 December 2020, legally produced, and covered by a due diligence statement (DDS) with the **geolocation of every plot** (Regulation (EU) 2023/1115 as amended by 2025/2650). The EU buys **44–48% of Vietnam's coffee export value** (UN Comtrade 2021–2023). Most of it comes from 0.5–2 ha smallholdings, through traders and agents who mix beans. A 2025 survey found only about **1 in 10 smallholders keep plot-level data**.

## Approach

Business analysis for a fictitious mid-size exporter in Đắk Lắk (30,000 t/year):

1. **Regulation → requirements.** 40 obligations extracted verbatim from the official texts by script, then gap-scored: 14 ⛔ not met, 12 ⚠️ partial, 14 ✏️ needs interpretation.
2. **Public satellite data.** District risk screening for 15 districts, built from Global Forest Watch tree-cover loss and driver data.
3. **Self-critique of the data.** Canopy-threshold sensitivity, tree cover loss vs. EU forest definition, and a "gray zone" rule set for uncertain plots.
4. **Solution design.** BPMN, ISO/IEC/IEEE 29148 SRS with 24 FR, 28 EARS business rules and 12 NFR; 31 user stories and 58 acceptance criteria; 88 test cases; a machine-checked RTM; a clickable prototype.
5. **Business case.** Three options, Monte Carlo, tornado chart and break-even analysis.

## Key findings

| # | Finding | Evidence |
|---|---|---|
| 1 | **The binding constraint is missing data, not deforestation.** Without plot coordinates no DDS can be filed, which puts **~USD 245–472 m/year** of Đắk Lắk coffee exports to the EU at risk. Only USD 49–236 m sits in high-risk districts. | S9 §3 |
| 2 | **Vietnam is classified low-risk** (Implementing Regulation 2025/1093). EU importers can use simplified due diligence, but still need every plot's geolocation and verifiable deforestation-free evidence (Art. 9, 13). The Vietnamese exporter is **not** the EUDR "operator", so the system produces a DDS *data package* for the EU importer rather than filing the DDS. | S7; DEC-03, DEC-04 |
| 3 | **Tree cover loss ≠ deforestation.** Đắk Lắk lost 15,873 ha of tree cover in 2021–2025 (−48% vs. 2016–2020). **5 of 15 districts account for 80%** of it. 55% is attributed to agriculture and 44% to logging. In core coffee districts almost 100% is agricultural, which is likely shade-tree or replanting cycles that EUDR excludes from "forest" (Art. 2(6)). | S9; S10 |

## Recommendation

**Rent a SaaS traceability platform (Option B) for the MVP and Release 2, with a contractual data-export clause, then migrate to an industry consortium (Option C) in 2027–28.**

- B has the highest expected NPV (USD 4.4 m over 3 years) and is the only option that can go live before the 2026/27 harvest.
- C ranks first on the weighted decision matrix from both the exporter's and the farmers' perspectives.
- **Do not invest** if the price penalty avoided is below about 1.2–1.6%, the EU share is below about 3–5%, or volume is below about 800–2,100 t/year.

## Roadmap

| Phase | Window | Scope | Gate |
|---|---|---|---|
| MVP | Nov 2026 – Jan 2027 | Register plots (high-risk districts first), automated plot screening, gray-zone verification | ≥ 60% plots geolocated before 30 Dec 2026 |
| R2 | Jan – Jun 2027 | Plot-linked purchases, EU stream segregation, DDS data package, reference tracking | 100% EU shipments with DDS reference before arrival |
| R3 | 2027 – 2028 | Consortium, automatic re-screening, dashboard, importer API | Next EU country benchmarking review |

## Limitations

- No access to company data and no field interviews; firm-level figures are documented assumptions.
- District coffee area is still pending the provincial statistical yearbook.
- The Hansen vs. JRC GFC2020 overlay script is ready but has not yet been run.
- The largest uncertainty in the business case is the market price penalty (ASM-25).
