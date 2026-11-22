# F3-D: independently replayed exogenous 30t/day H2 source-year economics — 2022 and 2024

Both 2022 and 2024 original E20t and E+S40t full-year integer-model
dispatches independently passed original-hour physical, pressure/EOS
and signed 2022/2024 wholesale electricity settlement replay.
Every scenario holds 30 tonnes/day H2 constant, and
the intervention is 90% of source-year modelled wind ELECTRIC POWER.
No source 2023 data, weather uncertainty distribution or forward forecast is included.

| Metric | 2022 (8,760 h) | 2024 (8,784 h) |
|---|---:|---:|
| Delivered H2 (kg) | 10,950,000 | 10,980,000 |
| E20t nominal source-year wholesale electricity cost (EUR) | 32,160,567.93 | 2,544,581.87 |
| E+S40t nominal source-year wholesale electricity cost (EUR) | 28,878,954.88 | 612,906.02 |
| E−E+S annual nominal source-year saving (EUR) | **3,281,613.05** | **1,931,675.85** |
| E−E+S nominal saving per kg delivered H2 (EUR/kg) | 0.29969069 | 0.17592676 |
| E+S reduction versus E wholesale cost | 10.204% | 75.913% |

Difference in nominal source-year normalized savings (2024 minus 2022): **-0.12376393 EUR/kg**, or **-41.30%** relative to 2022. It is not inflation-adjusted and is not a weather-risk confidence interval or expected annual savings estimate.

The only optimization lower bounds here are original-source HiGHS reported integer cost bounds, with individual full-year MILP gaps <=1e-6. Their source-reported annual savings intervals are in the validated JSON, and are numerical bounds, NOT uncertainty bands. PtXLens independently recomputes all hourly state constraints and market-cost arithmetic but not the original full mixed-integer solver tree.

This does not establish matched-site vendor CAPEX/OPEX, actual grid export rights or power contracts, stack degradation, measured real plant performance, a statistically representative distribution of wind/price regimes, native BAFU:2026 v1.1 process-linked BOM or complete environmental LCA, additional storage investment viability or programme scientific v1.0.
