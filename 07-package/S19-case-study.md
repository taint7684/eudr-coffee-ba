# The EUDR problem in Vietnamese coffee is a data problem, not a forest problem

*A business analysis case study · Đắk Lắk, Vietnam · October 2026*

On 30 December 2026 the EU Deforestation Regulation (EUDR) starts to apply to large and medium operators. From that date, every bag of coffee entering the EU must come from land that was not deforested after 31 December 2020, must be legally produced, and must be covered by a due diligence statement listing the geolocation of **every** plot where the coffee was grown.

For Vietnam, this matters. The EU takes 44–48% of Vietnam's coffee export value. Most of that coffee is Robusta from the Central Highlands, grown on farms of one or two hectares and passed through traders and agents who mix beans from dozens of households.

I set out to answer one question as a business analyst would for a real client: **what does a mid-size Vietnamese coffee exporter need to build, and is it worth it?** I worked only with public sources and labelled synthetic data. The full repository contains every document, dataset and script.

## 1. Start from the law, not from a summary

Most EUDR content online is secondary commentary. I downloaded the official texts instead: the 2023 regulation, the December 2025 amendment that postponed and simplified it, and the 2025 country benchmarking act. I then extracted **40 obligations** into a requirements matrix.

One rule kept the matrix honest: the *verbatim* column is filled by a script that searches the official text for an anchor phrase, and the script stops if the phrase is missing or ambiguous. Nothing in that column is typed by hand.

Reading the primary text changed the project in three ways:

- **Vietnam is low-risk.** The Commission's benchmarking act lists Vietnam among low-risk countries. EU importers can therefore skip formal risk assessment and mitigation (Article 13). They still need the geolocation of every plot and "adequately conclusive and verifiable information" that the coffee is deforestation-free (Article 9).
- **The exporter is not the operator.** Under Article 7, the first company established in the EU that makes the product available on the EU market is the operator, and only an EU-established representative can file on the operator's behalf. My original idea of a system that "submits the DDS to the EU" was legally wrong. The system has to produce a **DDS data package** for the EU importer.
- **Agroforestry is not forest.** Article 2(6) excludes agricultural plantations, including crops grown under tree cover, from the definition of forest. This becomes critical once satellite data enters the picture.

The gap analysis scored 14 obligations as not met, 12 as partly met and 14 as needing interpretation. The five biggest gaps were: no plot coordinates; mixing across four or five supply-chain tiers; no verifiable deforestation-free evidence; land-use documents that are incomplete or not digitised; and no data channel to the EU importer.

## 2. Measure risk with public satellite data, then distrust it

Global Forest Watch publishes tree-cover loss per district, together with the dominant driver of loss. For Đắk Lắk (pre-2025 boundaries, 15 districts), the data show three things:

- **15,873 ha** of tree cover were lost in 2021–2025, **48% less** than in 2016–2020.
- **Five districts** account for **80%** of that loss.
- **55%** of the loss is attributed to agriculture and 44% to logging.

The eastern districts lose the most tree cover, but mostly through logging. In the core coffee district Cư M'gar, **99.9%** of the loss is classified as agricultural.

A naive reading would flag Cư M'gar as a deforestation hotspot. The better reading is that "tree cover loss" counts every tree taller than five metres, including shade trees and old coffee replanting on land farmed for decades. Under EUDR, that is not deforestation. I therefore labelled the district index a **screening indicator** and moved the real decision down to plot level.

At plot level the system overlays each plot on the EU's 2020 forest map (JRC GFC2020, 10 m) and on tree-cover loss after 2020. It then applies a six-rule decision table. When the data disagree, the plot goes to a **gray zone**: it cannot enter a DDS package until it is verified with historical imagery or a field visit. The data also proved sensitive to definitions. Moving the canopy threshold from GFW's default of 30% to EUDR's 10% raises measured loss by 16% overall and almost doubles it in the dry dipterocarp districts.

## 3. Design the system so the trace is checkable

The solution, ECTS, has five capability groups: plot registration, plot risk screening, purchase recording, DDS data package, and dashboard/audit. The design artefacts are:

- a BPMN to-be process and RACI;
- an ISO/IEC/IEEE 29148 SRS with 24 functional requirements, 28 business rules written in EARS ("WHEN …, THE SYSTEM SHALL …") and 12 NFRs;
- 31 user stories with 58 Gherkin acceptance criteria;
- 88 test cases built from decision tables, boundary values and equivalence classes;
- a clickable prototype running on 298 synthetic plots.

All requirements, stories, criteria and tests live in CSV files. A build script generates the traceability matrix and **fails if any unmet EUDR obligation does not reach a test case**. The same script fills the requirement tables in the SRS, so the document cannot drift from the data. The current result is 14 of 14 unmet obligations traced to tests, with zero errors.

## 4. The business case: data is the binding constraint

The value-at-risk analysis gave the project's main insight. The five high-risk districts hold 55.9% of Đắk Lắk's coffee area (2024 statistical yearbook), worth roughly USD 137–264 million a year in EU exports. Without plot coordinates, however, **no** due diligence statement can be filed. That blocks the whole Đắk Lắk share of EU exports, roughly **USD 245–472 million a year**, even when the land is clean. The MVP therefore prioritises collecting coordinates over sophisticated risk scoring.

For the fictitious exporter (30,000 t/year, 45% to the EU), I compared building in-house, renting SaaS and joining an industry consortium over three years:

- **Renting SaaS** has the best expected NPV (about USD 4.4 million) and is the only option that can go live in the roughly two months left before the deadline.
- **The consortium** wins the weighted decision matrix, especially from the farmers' perspective, because plots are registered once and shared across buyers.
- My recommendation is SaaS now, with a contractual data-export clause, then migration to a consortium.

A tornado chart showed that the three parameters that matter all sit on the **benefit** side: the price penalty avoided, the EU share and the volume. Software cost barely moves the result. The analysis also states when **not** to invest: if the price penalty avoided is below about 1.2–1.6%, or the EU share is below 3–5%, no option pays back.

## 5. What I would do differently

- **Talk to an importer first.** The weakest assumption in the model is the market price penalty. One conversation with an EU buyer would tighten the business case more than any model change.
- **Get the statistical yearbook early.** The official district coffee area changed the high-risk list: the district with the most tree-cover loss (M'Đrắk) has under 2,000 ha of coffee, while the coffee heartland moved to the top.
- **Run the plot-overlay analysis.** Overlaying Hansen loss on the EU's 2020 forest map would show what share of "loss" really sits in forest. It is scoped as an extension.

The broader lesson: in compliance projects, the regulation is the easy part to read and the hardest part to read *correctly*. Secondary summaries and first drafts consistently missed the amendment, the low-risk classification and the operator definition. Each of those changed the design.

*Repository: github.com/taint7684/eudr-coffee-ba · Dashboard and prototype via GitHub Pages.*
