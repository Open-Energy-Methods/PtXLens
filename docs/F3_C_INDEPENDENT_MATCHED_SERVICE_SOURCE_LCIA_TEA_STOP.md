# F3-C — Independent PtXLens verification of source-2023 equal-service physical-screen operational savings

**Status, 14 November 2026:** **Numerical source-comparable grid WHOLESALE settlement: VERIFIED.** **Native full-system life cycle E/E+S GWP and investment/discounted LCOH: NOT QUALIFIED.**

## Imported direct original-source 2023 evidence

[Original 2023 reconstructed PyNEXUS E+E/S source operations](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43580088115) were independently solved with Type I 200bar(a) gas-pressure and 20bar(a) delivery pressure constraints, RVO-based compression electricity and original frozen 2023 observed NL A44 price/ERA5-derived wind. Two separate E-pressure-feasible Stage A *incumbent* profiles, one for `max_inventory`, one for `usable_service`, define distinct common 8,760h hydrogen delivery sequences. The original full 18.25-million-kg industrial H₂ demand is **not** met.

The four source-derived [gross E](../data/results/F3_C_2023_source_pressure_matched_max_inventory_E.json), [gross E+S](../data/results/F3_C_2023_source_pressure_matched_max_inventory_E_plus_S.json), [usable E](../data/results/F3_C_2023_source_pressure_matched_usable_service_E.json), [usable E+S](../data/results/F3_C_2023_source_pressure_matched_usable_service_E_plus_S.json) results are each **byte-locked with different registered SHA256**, verified by [dedicated consumer bridge](../src/ptxlens/f3c_common_service_bridge.py) and [tamper tests](../tests/test_f3c_common_service_bridge.py). The consumer verifies original source hashes, fixed-common-hourly-target `float64` hash *matching between E and E+S*, source full-shortfall, 20–200bar(a) ideal EOS bounds, independently audited physical residuals, 2023 EUR wholesale model cost, solver dual/incumbent bounds, and a certified ≤1e-6 relative MIP gap in each of four cases. Original 2023 source event-hour trace is not an actual measured industrial plant or gas-supplier connection.

## Physical common-hourly service and bounded E/E+S wholesale costs

| Separate source bank semantics | Same delivered H₂ each hour — annual sum kg | E20t net wholesale € | E+S40t net wholesale € | E+S lower modelled wholesale settlement € | Deterministic source MILP bound interval |
|---|---:|---:|---:|---:|---:|
| Max/gross 20t vs40t inventory | 16,268,755.001 | 25,587,589.630 | 24,463,257.361 | **1,124,332.269** | [1,124,318.034; 1,124,348.115] |
| Usable 20t vs40t capacity | 16,331,558.946 | 25,880,392.499 | 24,776,928.770 | **1,103,463.729** | [1,103,461.954; 1,103,474.625] |

Gross E feasible Stage A physical additional modelled shortage relative to the original E 16,335,279.317kg reference: **66,524.317kg**; usable **3,720.371kg**, respectively. Thus original full 18.25-million-kg industrial demand remains unmet by **1,981,244.999kg** or **1,918,441.054kg** respectively. Those service regimes are separately frozen; do not compare between them as if the volume/functional unit were identical.

**Interpretation:** the larger modelled bank improves wholesale **time-shifting** under the source model even though annual ideal compressor electricity is higher. The net-wholesale reduction is NOT the cost of additional storage, net profit, whole-plant savings, LCOH or total cost of supplying 18.25mkg. The HiGHS deterministic cost bounds are numerical solver envelopes, **not confidence intervals or real-world uncertainty bars**.

The independent full result is [PtXLens F3-C operational source bridge](../data/results/F3_C_2023_source_real_gas_equal_H2_hour_E_vs_ES_Lens_operational_bridge.json) SHA `dddd07d5c0a3d4f276e80af44e28cf3cfdbc93421107fb5d9e39843a0d1d90e2`. Source-matched PtXLens bridge [CI fully passed](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43580637209). Model construction, original archive hashes, all physical equations and fuller scientific caveats are detailed in [PtXFlex F3-C methods](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F3_C_2023_PHYSICAL_COMMON_HOURLY_SERVICE_VERIFIED.md).

## Native BAFU L1/L2 and TEA L3 STOP

There is **no native manufacturing process for a verified incrementally installed 20t stationary Type I steel-storage + pressure station**, selected by a manufacturer for a real site, and no matching CAPEX, installation, compression equipment, cooling/hydraulics, maintenance or recurring costs. Even with a real native BAFU 2026 v1.1 background and registered scoped supplier impacts, their absence prevents a complete incremental-gross-GWP or LCOH result. The [native BAFU tank mass-unit audit](../data/results/BAFU2026_v1_storage_tank_source_unit_mismatch_audit.json) specifically forbids using a light vehicle composite H₂ tank per kg capacity as a stationary steel tank dry mass process.

**Priority physical handoff:** select a pressure-vessel architecture and calculate stationary vessel **empty steel mass** (real engineering geometry and allowable pressure design), welds/joints/nodes, supports/foundations, valves and safety, compressing/drying/cooling and H₂ quality station, construction, on-site installation, inspections and replacements, any connection/civil works, end-of-life treatment, uncertainty and geographic inventory. Independent reviewer to classify sources as actual vendor specifications, manufacturer engineering or documented design assumptions, not promise an installed physical system where none is proven.

Matched-service GWP functional unit must be defined at the exact product pressure/purity and `2023 modelled actual service schedule`, and any supply shortfall relative to full industrial contract must be explicitly declared. An optional backup import pathway remains **prospective 2026 counterfactual** and requires a real site and two distinct gas+network contracts.

**Release:** F3-C operational source import: **PASSED within narrow numerical scope**. F3 full physical manufacturer/reliability + L1/L2/L3/P0 and programme v1.0: **NOT PASSED**.
