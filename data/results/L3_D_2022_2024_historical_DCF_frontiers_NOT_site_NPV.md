# L3-D: 2022/2024 source-year conditional hydrogen storage DCF frontiers

Source: Git-blob pinned PtXFlex original four-case F3-D independently physical-replayed hourly matched H2 model; no original hourly data redistributed.

| Historical year | Capacity semantics | Annual modelled wholesale saving EUR | Modelled H2 t/day | 20y 8% zero-OPEX zero-replacement CAPEX ceiling EUR | 20y 8% 250k OPEX 1m EOY10 replacement CAPEX ceiling EUR |
|---|---|---:|---:|---:|---:|
| 2022 | max_inventory | 3,905,632.94 | 30.481 | 38,346,079.89 | 35,428,349.55 |
| 2022 | usable_service | 3,903,807.25 | 30.884 | 38,328,155.00 | 35,410,424.66 |
| 2024 | max_inventory | 2,247,126.18 | 30.748 | 22,062,616.05 | 19,144,885.71 |
| 2024 | usable_service | 2,206,233.52 | 31.006 | 21,661,125.92 | 18,743,395.58 |

## Mathematical definition

For each scenario separately: NPV = -I0 + sum over t=1..N of [S_original * k * (1-d)^(t-1) - O - R_t] / (1+r)^t + (salvage - decommission)/(1+r)^N. Capital ceiling is the discounted cashflow excluding I0. All payments occur at specified year ends. A negative capital or OPEX ceiling implies that no nonnegative expenditure breaks even.

S_original is a source-year observed-price/wind model DIFFERENCE, not a future market forecast. The 20-year 8% real rate, savings persistence, annual incremental OPEX, replacement costs and site economics are illustrative analyst assumptions ONLY. Each result has its own 2022 or 2024 nominal purchasing-power euro unit, without inflation harmonization. 2023 L3-A uses a different product H2 target and cannot be spliced into future years.

The accompanying JSON includes 324 sensitivity cells (4 scenarios x 3 lives x 3 rates x 3 persistence factors x 3 OPEX assumptions; one 1m EUR replacement at end year 10) and propagates source-solver economic bounds without calling them statistical confidence limits.

No independently reconstructed HiGHS dual, vendor installed CAPEX/OPEX or compressor BOM, production forecast, native BAFU whole-system LCIA, site permit or financial viability is demonstrated. Scientific v1.0 remains blocked.
