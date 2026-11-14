# F3-D / L3-B integrated scientific assessment — original 2023 hourly robustness, incremental storage economics, and LCA limits

**Programme:** OEM-PTX-2026-01 · **Research checkpoint:** 14 November 2026 · **Scope:** PtXFlex (source model and physical dispatch) + PtXLens (independent source verification, financial conditional frontiers, and BAFU admission).  
**Scientific state:** **F3-D original-2023 derived-input numerical experiments: 6/8 certified; 2/8 unresolved**. **L3-B peer-reviewed tank-only 2024-price estimate verified**. **Actual vendor installation, full manufacturer materials, alternative observed 2022/2024 joint weather-and-market histories, native matched-service full LCA, real project economics and v1.0: NOT VERIFIED.**

## Abstract

We ask whether the original PyNEXUS E+S hydrogen storage scenario (40 t nominal inventory) retains an operational wholesale grid-electricity cost advantage over the E scenario (20 t nominal inventory) when price chronology, price dispersion or wind availability are perturbed. The common *hour-by-hour* hydrogen product profile is fixed within each pressure-storage interpretation, and each of E and E+S is reoptimized for 8,760 hours with the same input arrays, physical pressure-screen assumptions and original plant constraints. The original 2023 historical operating cases are provenance-locked by original archived inputs and their SHA-256 evidence. Four derived perturbations are **counterfactuals, not another observed year**. Across two separately defined inventory conventions, six of the eight scenario pairs reached the source acceptance rule (both models independently passing the 1×10⁻⁶ relative HiGHS MIP gap and physical audits). In all six, the simulated E+S advantage remained positive, from approximately **€0.721m/year** to **€1.710m/year**. Both wind −10% runs yielded no accepted E or E+S incumbent; a comparative cost or infeasibility proof has **not** been issued.

A separate peer-reviewed Type I reference cost of **€222 per kg of nominal rated hydrogen capacity in 2024-harmonized euros** corresponds to **€5,772 per published 26 kg nominal vessel** and hence **€4.629m** or **€5.206m** for the source-screened incremental 802 or 902 literature vessels. This is **a tank-only paper estimate, not an OEM quote or installed capital**; the source cost basis (200 bar gauge; nominal) and the F2 screen (maximum 200 bar absolute; 313 K) also differ. These 2024 study euros cannot be subtracted unchanged from L3-A's hypothetical 2023-real-EUR capital ceiling. Native BAFU:2026 v1.1 30 bar PEM LCIA examples exist, but no scientifically compatible manufacturer inventory covers the complete incremental stationary Type I bank or equal-hour product service. The overall climate-economic preference remains unknown.

## 1. Research question, scenario boundaries and fixed functional unit

The original simulated H₂ industrial demand is **18,250,000 kg/year**, which neither constructed matched-service benchmark fully serves. The original historical E Stage B *modelled delivered* quantity is about 16,335,279 kg/year. F3-C builds a fixed feasible common-hour target by subtracting the extra physically screened E storage shortfall from that original delivered profile. The Stage A incumbent is explicitly **feasible, not proven to maximize delivery or minimize curtailment/shortfall globally**. For original gross inventory semantics, the same 8,760-hour target for E20t and E+S40t sums to **16,268,755.001 kg/year**; for the distinct usable/withdrawable semantics, its own common-hour target sums to **16,331,558.946 kg/year**. **The two semantics do not describe the same hourly functional unit; do not compare the two modes as if one beats the other in a service-equivalent contest.**

Within each mode, model assumptions include the original source PEM output, ramp, minimum load, grid exchange, pressure-screened source Type I 200 bar absolute gas bank at isothermal **313 K**, minimum product 20 bar absolute, and charge compressor energy approximation. E and E+S have the **same** derived weather, market prices, hydrogen delivery target and nonstorage source parameters, with only source nominal capacity 20t vs 40t differing. The source model remains simplified: dynamic H₂ compressor map, cooler operation, certified installation pressure, materials fatigue, industrial outlet contract and auxiliary electric loads are not fully validated.

The original wind sampling **52.5°N, 3.5°E is an offshore ERA5 resource-grid coordinate**, NOT a customer, pipeline connection, vessel installation or geographic LCA delivery site.

## 2. Provenance and reproducibility

Original archived PyNEXUS E SHA-256: `069455704573825f4e709e6705f5db43823722909cb93a37bd86b978636fb051`. Original E+S SHA-256: `cd4101fe62c3f1b8aa2d7508d3651d2fee40d2bafe6d5b87e40d5f4d055070f9`. The original 2023 hourly Dutch ENTSO-E A44 price and source ERA5-derived wind series match between the two source archives. F3-C Stage A source shortfall and per-mode common hourly H₂ SHA-256 are further locked: gross `8e0d55994c7fe5f1abd952771a1b169336893d12698147fb3a93cb61a4ee7a16`, usable `6a30baf00ddb065cd906dedd711db7cbf67504c50b4fda5809c5dfd29b23fa87`.

**Execution:** GitHub Actions [PtXFlex complete eight-case 2023 source-reoptimization matrix](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43590739436) authenticated source ZIPs privately at runtime, checked artifact SHA, reproduced 8,760-hour per-case E and E+S physical models, independently audited hourly hydrogen, grid, ramp, pressure bounds and source optimum objective bounds, and emitted a separate research JSON for each experiment. [PtXLens independent eight-result audit](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43591690578) verifies all eight result file fingerprints, mode target SHA, source operating/financial boundary and uncertainty status; both repositories retain all eight outputs and a [source-verified combined certificate](https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/data/results/F3_D_2023_8_original_source_price_wind_counterfactuals_PtXLens_6_certified_2_unknown_not_forecast.json). In particular, original price/wind raw or rescaled hourly values are **not redistributed as public new observed source archives**.

[Four F3-D source experiments](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/research/F3_D_2023_SOURCE_DERIVED_PRICE_WIND_COUNTERFACTUAL_PROTOCOL_v1.json), all generated from **2023** only:

| Scenario ID | Exactly what changes | What it *does not* imply |
|---|---|---|
| `price_circular_168h` | Circularly roll the original 8,760-hour NL electricity price series by 168 hours, keeping the original 2023 price distribution and wind unchanged | Not observed 2024 prices, not actual supply evolution, not a causal estimate of a real calendar shift |
| `price_centered_spread_150` | New price = original 2023 median + 1.50×(original price−median), preserving median but increasing dispersion | Not calibrated forward volatility, does not describe a realized or probabilistic 2022/2024 market |
| `wind_090_multiplier` | Multiply original source-model hourly available **wind electrical output** by 0.90; preserve source 2023 prices | Not a −10% change in wind speed, not a new ERA5 reanalysis or turbine power-curve simulation |
| `wind_110_multiplier` | Multiply original source-model hourly available wind electrical output by 1.10; preserve 2023 prices | Not proof extra output obeys a real installed turbine's rated cap or a physically generated new wind speed history |

No statistical probability weights, sample-based confidence bands, real future electricity-price forecast or independent historical-year results are inferred from these stress factors.

## 3. Mathematical comparison, solver acceptance, missing-result policy

For each mode `m` and source-adjustment scenario `s`, let `hₜ,m` be that mode's original F3-C common hourly delivered hydrogen requirement. Each E and E+S independently minimizes the same 2023-basis net grid wholesale settlement `Cₘ,s = Σₜ priceₜ,s × signed_grid_importₜ,s`, subject to the original input and pressure-screen constraints and **delivered_H2ₜ = hₜ,m for every hour**.

A paired E+S wholesale saving can be published **only if both runs** have audited physically consistent primal solutions and accepted solver certification. Under minimization, with E cost (C_E), E+S cost (C_{ES}), per-run certified lower bounds (L_E) and (L_{ES}), the reported source numerical saving interval is:

```text
  S = C_E - C_ES
  [S_low, S_high] = [L_E - C_ES, C_E - L_ES].
```

The interval represents **solver numerical optimization gap only**. It is not a sensitivity/confidence interval for weather, electricity prices, real compressor losses or equipment costs. Missing incumbent or timeout/error **must not become zero cost, zero economic advantage or an unverified proof of mathematical infeasibility**. For any result lacking both accepted source cases, `S = null` and matched-service DCF must also be `null`.

## 4. F3-D quantitative results — 2023-original and derived-input counterfactual

**Units: million 2023-EUR modelled annual net wholesale grid cost advantage of E+S over E.** Same source-mode H₂ delivery in each row, independently reoptimized in both configurations.

| Source 2023 scenario | Gross inventory E−E+S | Usable inventory E−E+S | Both source models certified? |
|---|---:|---:|---|
| Original observed 2023 chronology, F3-C | **1.124332** | **1.103464** | Yes, original reference baseline |
| `price_circular_168h` | **0.726848** | **0.720619** | Yes / yes |
| `price_centered_spread_150` | **1.709870** | **1.681103** | Yes / yes |
| `wind_090_multiplier` | **NULL** | **NULL** | No accepted pair; model status unresolved |
| `wind_110_multiplier` | **1.028800** | **0.994498** | Yes / yes |

The price-phase experiment lowers the reported source-2023 E+S operating advantage by around **35%** in both modes, while increasing source price spread to 1.5× increases the benefit around **52%**. Increasing *modelled available wind electricity* by 10% slightly decreases E+S's advantage, showing that the gross benefit is not simply monotonic in available renewable power. This is a finding *within the source model and counterfactual perturbations*; it does not imply that additional storage will be economically viable in other weather regimes or a different real plant.

**Two missing wind −10% pairs:** stored result files record `NO_ACCEPTED_INCUMBENT_OR_FAILED_UNKNOWN` for both E and E+S, with no accepted solution, economic objective or optimality bounds. They do **not** preserve the original numerical solver status/message necessary to distinguish LP infeasibility, MILP infeasibility, presolve failure, time exhaustion or numerical difficulty. An independently audited LP-relaxation feasibility test and/or explicit source solver status capture is required; the result **must remain unknown until established**.

## 5. Link to L3-A: what discounted cash-flow results do and do not mean

[PtXLens L3-A](https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/docs/L3_A_2023_MATCHED_SERVICE_WHOLESALE_DCF_BREAKEVEN_METHODS_RESULTS_v1.md) considers the purely **conditional** capital break-even frontier

```text
 ΔNPV = −C0 + ∑(t=1..N){[k_t×S_source2023 − incremental_OPEX_t − replacement_t]/(1+r)^t}
                    + [salvage_N − decommission_N]/(1+r)^N .
```

It uses a single mode's source-verified operating saving, stated hypothetical repetition factor `k_t`, constant real 2023 EUR and a **real** discount rate. Applying this mathematical threshold calculation to F3-D certified source-derived operating savings is permitted as a **scenario illustration** only; it is not reoptimizing physical operations on any future weather or price. Under an illustrative 20-year life, 8% real rate, `k=1` (hypothetically repeat the transformed 2023 modelled saving annually) and **zero extra OPEX, installed maintenance, replacements or decommission costs**, the original source 2023 gross/usable ceilings are €11.039m/€10.834m. The shifted-price condition produces €7.137m/€7.075m, enhanced-price-spread €16.785m/€16.505m, and +10% wind €10.101m/€9.764m. There is **no value** for −10% wind.

Zero incremental operating cost is only an **optimistic mathematical upper envelope**, NOT evidence that real extra vessels, compressors, foundations, annual inspections, support systems and safety equipment will cost nothing. No source input supports a commercial project NPV or levelized H₂ production cost.

## 6. L3-B: peer-reviewed Type I tank-only cost and source-unit firewall

The peer-reviewed [Ademollo et al., *International Journal of Hydrogen Energy* (2026), DOI 10.1016/j.ijhydene.2025.152849](https://doi.org/10.1016/j.ijhydene.2025.152849) reference specifies Type I all-steel 1.8 m³/2,400 kg **empty equipment**/26 kg **nominal stored H₂** vessel class at **200 bar gauge nominal** and a **2024-harmonized study estimate of €222 per kg nominal rated H₂ capacity**. Per-paper reference tank-only cost is therefore (26×222 = €5,772) in 2024 euros. This cost is neither a supplier-issued price nor a verified construction cost.

| Original F2 source storage capacity interpretation | Incremental 1.8m³ literature vessels | Added **empty equipment**, NOT virgin-steel material | 2024 *literature tank-only* cost |
|---|---:|---:|---:|
| Gross original 20t→40t nominal upper inventory | 802 | 1,924,800 kg | **€4,629,144** |
| Distinct usable-withdrawable original 20t→40t interpretation | 902 | 2,164,800 kg | **€5,206,344** |

**Three independent mismatches prevent drawing a payback inference:**

1. The **paper's 200 bar gauge nominal rating** differs from the research's hypothetical **200 bar absolute maximum** at 313 K. Neither manufacturer pressure plate nor true usable capacity/temperature/cycling is site certified.
2. Literature tank-only cost is harmonized to **2024 EUR**, whereas L3-A is a hypothetical **real 2023 EUR** DCF. No documented 2024→2023 equipment-cost deflator/source correction is available; do **not** directly subtract paper euros from the scenario capital ceilings.
3. The literature estimate is only the **bare nominal vessel cost category**, while real incremental all-in installed costs still require actual frames, supports, foundations, manifolds, valves, vent/relief, hydrogen compressor, heat rejection/cooling, instrumentation, site civil/electrical, safety conformity, maintenance and end of life. The original source did not define a physical H₂ delivery station. A different heiserTEC 330 bar 50 L PED OEM cylinder has a separately sourced empty individual-cylinder mass, **not** a quoted 200 bar 1.8m³ vessel or a signed bank module price.

The validated independent paper-source and BAFU boundary result is available in [PtXLens L3-B source JSON](https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/data/results/L3_B_2024_IJHE_nominal_200bar_gauge_TypeI_storage_tank_only_cost_NOT_supplier_quote_BAFU_stationary_NO_LCI.json) and the [paper-source/BAFU validation workflow](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43591024424).

## 7. L1/L2: BAFU 2026 native inventory sources and the missing complete physical manufacturing foreground

There is a native BAFU:2026 v1.1 IPCC 2021 GWP 100 execution tied to the source-2023 original Dutch E and E+S **30-bar PEM** H₂ reference, with original **non-matched** H₂ service quantities: E 16,335,279 kg and E+S 16,679,072 kg. The corresponding previously scoped reference is about **6.1482 and 6.0766 kgCO₂e/kg** respectively, but neither is the F3-C/F3-D equal-hourly storage system and neither includes the newly defined 20t incremental stationary steel Type I vessels, site compression, BoP or complete real manufacturing/EOL. It would be a scientific error to use their direct difference as a physically equivalent full-system climate benefit.

**BAFU original schema unit mismatch:** the identified version-1 high-pressure hydrogen storage tank native process UUID `b4739ad2-aa38-368d-8ada-63f5417c8b55` represents a **road-vehicle composite vessel expressed per kg H₂ STORAGE CAPACITY**, *not* per kg of 200-bar stationary Type I empty steel pressure equipment or per kg of raw low-alloy forged steel. Multiplying this provider by 1.9248 kt or 2.1648 kt paper *empty equipment* would violate the functional unit and technology identity. Its validity and transfer to v1.1 are also not established.

A full **19-category physical/installation/lifecycle source bill of materials** is a *requirements checklist*, of which only the large steel-vessel **paper reference empty weight** is quantified and **18 other quantity/material/process categories are not**. The material/compressor/foundation provider UUIDs and actual audited manufacturing routes/steel chemistry remain unknown; such missing entries are `null`, never implicitly zero or invented factors. Required future mapping is: actual OEM model and material mass → appropriate LCI steel/process provider exact UUID + functional unit + geography/year → manufacturing operations and losses → station BoP and operations → replacement/EOL → full matched-hour delivered H₂ functional unit → full impact and independent uncertainty.

**Native BAFU original database checksum:** `e63b7e7ef5cde04bfe1176a783a55b5f72e2b73f42c36632b6150af39d348c4c`. The existing v1.1 source calculations are real **for their limited 30-bar PEM scope**, but cannot be extended to a physical full-storage LCIA without actual compatible providers and manufacturer inventory. The RFI [technical vendor/manufacturing data request](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F2_L1_STATIONARY_H2_VENDOR_RFI_AND_BOM_DATA_REQUIREMENTS_v1.md) is drafted **but not sent**; no actual customer location, quote or OEM duty acceptance has been identified.

## 8. Independently observed 2022 and 2024 sources — acquisition and admissibility

**Current acquisition status: none verified as input to the same model.** Do not claim observed multi-year robustness from the four 2023 perturbations. A genuine observed-year pair requires *both* independently collected exact-hour Dutch A44 day-ahead market values **and** wind meteorology for the identical offshore **52.5°N, 3.5°E** source grid location, with the original 2023 PyNEXUS turbine/plant conversion assumptions and an explicitly chosen H₂ contract/service target. A nationwide Netherlands observed wind generation dataset is **not** an adequate substitute for the source offshore *turbine-resource weather point*, and using 2023 wind with 2024 prices is an intentional **cross-year synthetic mix**, not a naturally occurring observed 2024 pair.

- Electricity provider: [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/) day-ahead market A44 and Dutch bidding-zone code; API access may require registered authorization/token, with provider terms governing redistribution. A published API token belongs in a private secret store, never a GitHub repository, workflow log or committed JSON.
- Meteorology provider: [Copernicus Climate Data Store ERA5 hourly time-series single levels](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-timeseries), point 52.5°N/3.5°E. Its official [product user guide](https://confluence.ecmwf.int/pages/viewpage.action?pageId=638829720) documents hourly UTC and 0.25° atmospheric grid snapping. CDS access and dataset terms must be checked. Wind **velocity** cannot simply be treated as available **MW**; reproduce the original turbine speed-height/density/capacity curve and cap, and compare 2023 reconstructed energy hour-by-hour with the frozen original 2023 values before trusting a new-year array.
- **Calendar and interconnection:** 2022 has 8,760 UTC hours; **2024 is leap year with 8,784 UTC hours**. Do not silently delete 29 February or duplicate hours to force 8,760. Keep the full 8,784-hour model if supported or preregister explicit leap-day normalization and functional-unit accounting with its sensitivity; note change to source original 8,760-hour model solver. ENTSO-E timestamps and changes in Dutch 60/15-minute market intervals must be duration-weighted and reconciled to UTC before annual averaging; negative prices must be retained, not clipped. Hourly ERA5 uses hour-start timestamps. All missing hours, duplicate timestamps, timezone offsets, coordinate snapping, turbine caps and original H₂ assumptions require an explicit data-quality audit.
- **Provenance gate:** a *new observed-year model* may be tagged verified only when raw provider records are lawfully escrowed in private user-controlled storage and their bytes SHA-256 recorded; normalized hourly arrays are hashed; the source PyNEXUS conversion is reproducible; the same-hour service/delivery and physical input capacity are properly reconciled; and model cost/mass-balance tests and solver certificates pass for both E and E+S. No new historical-year dataset has met these conditions yet.

The legacy [Open Power System Data historical time-series package](https://data.open-power-system-data.org/time_series/latest/) terminates in 2020; it cannot supply a valid **2022 or 2024** replacement pair. Hence no claims about the true multi-year E+S advantage beyond the controlled 2023 perturbations.

## 9. Reproducible artifacts and quality assurance

- [PtXFlex original SHA-checked eight-case solver and 2023 price/wind transform](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/src/ptxflex/f3d_2023_source_hourly_counterfactuals.py) and [source-preserving transform/anti-fabrication tests](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/tests/test_f3d_2023_source_hourly_counterfactuals.py).
- [PtXLens independent eight-case 2023 source integrity and conditional DCF bridge](https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/src/ptxlens/f3d_independent_2023_stress_finance_bridge.py) and [negative science tests](https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/tests/test_f3d_independent_2023_stress_finance_bridge.py).
- [F3-D PtXLens two reproducible vector figures and generation workflow](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43591938694), with the −10% wind results **visibly marked NOT CERTIFIED rather than plotted as zero**.
- [L3-B paper-source €/unit and native BAFU v1.1 scope checker](https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/src/ptxlens/l3b_published_tank_cost_and_bafu_provider_gate.py), [negative controls](https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/tests/test_l3b_published_tank_cost_and_bafu_provider_gate.py).
- [L3-A same-hour 2023 source discount thresholds and source-admissibility discussion](https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/docs/L3_A_2023_MATCHED_SERVICE_WHOLESALE_DCF_BREAKEVEN_METHODS_RESULTS_v1.md).

**Recommended review order:** raw original source artifact hashes → per-mode common H₂ hourly hashes → original model source constraints → four transformations and exact source-only timestamps → E and E+S primal/dual/physical constraints → six source cost intervals plus two unknowns → separate tank-only year/unit/pressure interpretation → missing LCI and financial source quantities → full system adjudication.

## 10. Scientific decision and remaining gates

| Package | Strict present conclusion | What is required to pass its full gate |
|---|---|---|
| F3-C | Pressure-screened original 2023 equal-hour service within two distinct modes **source verified** | Constructibility, full industrial service/actual H₂ supply, independent review |
| **F3-D** | **Six certified 2023-derived counterfactual comparisons, two unresolved** | Resolve wind −10% mathematically/with diagnostics, acquire *genuine independent observed* price+ERA5 wind years, repeated time-aligned 8,760/8,784-hour physical optimization and sensitivity |
| **L3-A** | Source-2023 conditional capital/OPEX threshold math and figures **verified** | Actual installed manufacturer costs, complete O&M, future price and economic site, financing and whole-plant service |
| **L3-B** | 2024 peer-reviewed Type I reference **tank-only cost** **verified** | OEM full installed quote, currency/year reconciliation, system BoP, service-pressure certification, full DCF |
| **L1/L2** | Native v1.1 30 bar source-PEM scope verified; full physical storage manufacturing unknown | Real Type I supplier BOM/material mapping, exact native compatible manufacturing providers, complete equal-service functional unit and lifetime LCA |
| **P0** | Original 2023 artifacts live and hashed in actions; private escrow not independently recovered | Two independent lawful private copies, SHA/CRC restored outside GitHub Actions; originals currently expire **24 December 2026** |
| **Hydrogen/methanol v1.0** | **NOT PASSED** | All project release gates and independent scientific review |

**Overall:** scientifically auditable **limited 2023 counterfactual robustness** with verified source engineering and controlled missing evidence. **No claim of installed storage competitiveness, actual new historical-year robustness, full cradle-to-grave emissions comparison or v1.0 release is currently defensible.**
