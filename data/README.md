# RSPCA Animal Welfare – data folder (FIT3179 DV2)

All CSVs are tidy (one row per observation) so they drop straight into Vega-Lite `"data": {"url": "data/<file>.csv"}`.
Numbers were transcribed from the published reports and checked against each report's own totals.

## Sources
| Code | Source | Used for |
|---|---|---|
| A | RSPCA Australia, *National Statistics 2024-2025* – https://rspca.sfo2.cdn.digitaloceanspaces.com/public/Uploads/annual-statistics/RSPCA-Australia-Annual-Statistics-2024-2025.pdf | all `rspca_*` files |
| B | ABS, *Population up 1.5% in June 2025* (18 Dec 2025) – https://www.abs.gov.au/media-centre/media-releases/population-15-june-2025 | `abs_*`, per-capita columns in `derived_*` |
| C | RSPCA WA, *RSPCA WA reveals state's animal cruelty hotspots* (2023-24) – https://www.rspcawa.org.au/news/rspca-wa-reveals-states-animal-cruelty-hotspots | `rspcawa_cruelty_reports_*`, `rspcawa_offences_*` |
| D | RSPCA WA, *2024-25 Impact Statement* – https://www.rspcawa.org.au/wp-content/uploads/2026/07/2024-25-Impact-Statement.pdf | other `rspcawa_*` files |

## Files
| File | Grain | Key fields | Good for |
|---|---|---|---|
| `rspca_state_species_outcomes_2024_25.csv` | state × species × outcome (320 rows) | `state`, `species`, `outcome`, `outcome_group`, `outcome_order`, `count` | normalised stacked bars, mosaic, small-multiple maps by species |
| `rspca_state_species_received_2023_2025.csv` | year × state × species | `received` | slope/dumbbell 2023-24 → 2024-25, tile-grid cartogram |
| `rspca_national_trend_5yr.csv` (+ `_long`) | year × species group (2020-21 → 2024-25) | live vs euthanased, `pct_euthanased` | streamgraph, heatmap, trend |
| `rspca_euthanasia_reasons_2024_25.csv` | state × dog/cat × reason | `reason`, `count` | heatmap, diverging/butterfly chart |
| `rspca_inspectorate_by_state_2024_25.csv` (+ `_long`) | state (no NT) | complaints, prosecutions, charges, inspections | funnel, choropleth |
| `rspca_national_complaints_prosecutions_6yr.csv` | year (2019-20 → 2024-25) | complaints, prosecutions, per-1000 rate | dual trend / connected scatter |
| `abs_state_population_2024_2025.csv` | state | `pop_jun2024`, `pop_jun2025`, `centroid_lat/lon` | normalising, symbol placement |
| `derived_state_rates_2024_25.csv` | state | per-10k rates, live-release %, prosecutions per 1,000 complaints | **choropleth** (join on `state_name`) |
| `rspcawa_cruelty_reports_top_lga_2023_24.csv` | top-10 metro + top-12 regional WA councils | `reports`, `pct_change_vs_2022_23`, `approx_lat/lon` | **proportional symbol map** of WA |
| `rspcawa_offences_reported_2022_2024.csv` | offence × year | `reports` | slope chart / dumbbell |
| `rspcawa_inspectorate_funnel_2024_25.csv` | measure | calls → investigated → prosecuted | funnel |
| `rspcawa_care_and_adoptions_by_type_2024_25.csv` | animal type | `cared_for`, `adopted` | waffle / pictogram |
| `rspcawa_animals_in_prosecutions_2024_25.csv` | animal type | `animals` | waffle / isotype |

## Definitions (put these on the web page in plain English)
- **Received** – every animal in an RSPCA facility during the financial year (1 July – 30 June).
- **Reclaimed / Returned** – back to the owner. **Rehomed** – adopted. **Released** – wildlife let back into the wild.
- **Transferred** – sent to another shelter, pound or rescue group. **Other** – includes died in care.
- **Live release % (derived)** = (reclaimed + returned + rehomed) ÷ (received − still in care), dogs + cats only.
- **Per 10k** = count ÷ June 2025 population × 10,000.

## Caveats – read before charting
1. **Pounds aren't counted the same way.** RSPCA ACT, NT and TAS exclude council pound animals; the other states include them. This inflates/deflates state comparisons.
2. **NSW shelter numbers are tiny** (465 animals) compared with its population – NSW reporting to RSPCA Australia is clearly partial. Don't let NSW look like "the kindest state" on a received-per-capita map; grey it out or annotate it.
3. **No NT cruelty data** – RSPCA NT can't enforce animal welfare law (the NT Government does). Show NT as "no data", not zero.
4. **QLD finalised just 3 prosecutions** from 13,874 complaints – real figure as published, but worth a footnote rather than a headline until you've checked why.
5. **"Other animals" rows don't add up in the source**: the outcome rows sum to 6,221 but the published total is 6,267 (−46 nationally; state differences range −73 to +24). Use `rspca_state_species_received_*` for totals and treat the "Other animals" outcome split as approximate.
6. **Wildlife is almost entirely QLD** (26,564 of 27,794) – log scale or separate wildlife from pets.
7. `centroid_lat/lon` and WA `approx_lat/lon` are approximate centre points I added for symbol placement – nudge them to fit your TopoJSON.
8. WA council data covers only the top 22 councils, so use symbols, not a choropleth (a choropleth would show most of WA as blank).
