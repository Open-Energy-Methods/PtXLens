# L3-D / L1-L2 — Native BAFU:2026 v1.1 stationary hydrogen storage inventory admission contract

**Status:** 15 November 2026 · **Scientific status:** NOT NATIVE-INVENTORY READY. The machine-readable stop gate in src/ptxlens/l3d_bafu_incremental_inventory_gate.py binds the existing original F2 19-category incremental Type I stationary hydrogen equipment source by Git blob **424a8f738cb9caa2d05c1ec5c22cbf6cdd601b82**. This source provides a literature *empty vessel hardware* mass, not complete steel manufacturing material quantities. There is **no measured, manufactured, installed stationary 20–200bar(a) BOM, native BAFU process linkage, or complete matched-service GWP result** in these sources.

## 1. Study objective and functional units

Compare incremental 20t source-model E and 40t source-model E+S physical Type I storage pressure bank (two distinct gross-inventory/usable-service semantics), **at identical hourly delivered hydrogen product in the same source year**. An expected functional unit is **1 kg of H2 delivered at the original source-model pressure/time/product quality**, backed by the appropriate full-year E and E+S service and quantity; this unit must be specified before any climate preference is computed.

The wind grid cell 52.5N, 3.5E is **not** a demonstrated installation site. Dutch A44 spot-electricity prices are **not** grid GWP characterization factors. Choose a physically verified site, the correct region and technical power supply, installed materials, service life and end-of-life before binding BAFU electricity and upstream manufacture background.

## 2. Actual source hardware register, without invented inventory data

Original F2 locked source artifact:
[data/results/F2_L1_2023_source_incremental_20t_to_40t_stationary_typeI_200bar_BOM_SCOPE_NOT_complete_native_LCI.json](../data/results/F2_L1_2023_source_incremental_20t_to_40t_stationary_typeI_200bar_BOM_SCOPE_NOT_complete_native_LCI.json).

The literature reference Type I vessel has **2,400kg EMPTY equipment mass** per hypothetical vessel, **1.8m³ internal volume**, with source pressure convention limitations. The gross-inventory model suggests 802 additional empty vessels (1,924,800kg empty equipment), usable-service model 902 (2,164,800kg empty equipment). These are **not** 1,924,800/2,164,800kg of cold-rolled, forged or virgin steel; material grade, alloy chemistry, shell/liner/closure parts, coatings, scrap/yield, work energy and complete installation are unverified.

| # | Required incremental manufactured process equipment scope | Current original-source quantity | Native BAFU:2026 v1.1 provider ID, unit, process and LCIA |
|---:|---|---|---|
| 01 | typeI_200bar_bare_reference_vessels | 802/902 published empty reference vessels; 1,924,800/2,164,800 kg of **equipment** | Unknown |
| 02 | steel_alloy_material_grade_and_inclusions | Unknown (must not set to zero) | Unknown |
| 03 | rack_frames_and_anchors | Unknown (must not set to zero) | Unknown |
| 04 | high_pressure_headers_and_interconnects | Unknown (must not set to zero) | Unknown |
| 05 | isolation_valves_and_actuators | Unknown (must not set to zero) | Unknown |
| 06 | non_return_valves_and_filters | Unknown (must not set to zero) | Unknown |
| 07 | pressure_relief_and_vent_stack | Unknown (must not set to zero) | Unknown |
| 08 | pressure_regulation_delivery_header | Unknown (must not set to zero) | Unknown |
| 09 | compressor_recips_and_seals | Unknown (must not set to zero) | Unknown |
| 10 | compressor_motor_drive_VFD | Unknown (must not set to zero) | Unknown |
| 11 | intercooler_aftercooler_heat_exchange | Unknown (must not set to zero) | Unknown |
| 12 | cooling_pumps_and_fans | Unknown (must not set to zero) | Unknown |
| 13 | gas_quality_dryer_and_sample_system | Unknown (must not set to zero) | Unknown |
| 14 | pressure_temperature_flow_metering | Unknown (must not set to zero) | Unknown |
| 15 | hydrogen_leak_detection_ESD_ATEX | Unknown (must not set to zero) | Unknown |
| 16 | civil_foundations_and_construction | Unknown (must not set to zero) | Unknown |
| 17 | inspections_fatigue_cycle_testing | Unknown (must not set to zero) | Unknown |
| 18 | installation_and_transport | Unknown (must not set to zero) | Unknown |
| 19 | decommission_and_EOL | Unknown (must not set to zero) | Unknown |

Exactly **19 foreground classes × 2 capacity interpretations = 38 unresolved BAFU provider mapping records**. The source F2 literature mass validates only the first line's **empty equipment reference**, and the other 18 system classes have no source-manufacturer quantities. Their contributions are **UNKNOWN**, NOT zero. The machine-readable readiness output explicitly retains null native process IDs, null manufacturing material inventories, null impact values, null vendor price evidence and a false v1.0 flag.

## 3. Native dataset matching/admission requirements

The original local BAFU:2026 v1.1 openLCA database is not included in the public repository. Native LCI work must be executed against a **legitimately obtained, actual original database**, and a source receipt should record at least the database file SHA256, BAFU edition (including v1.1), import/openLCA software versions, native process UUIDs, reference product/flow UUID and quantitative reference unit, provider-to-consumer product system link, geography/technology/vintage, process exchange conversion factor with explicit dimensional and sign checks, system-boundary and allocation assumptions.

For every physical manufacturer line, obtain equipment source-mass and material chemistry/fabrication through OEM drawings/BOM and mass-balance receipts. Separate primary metal, secondary metal/recycled content, alloying, forging/forming, heat treatment, machining/yield/scrap, corrosion protection, NDT/testing, transport/installation, use-period maintenance/replacement, energy use and end of life where relevant. Do not assume shell mass equals net purchased metal or treat every process as kg of steel production.

The known BAFU:2026 example of a high-pressure vehicle composite storage item (functional reference per **kg H2 stored**) cannot be repurposed as a stationary **steel** Type I vessel per **kg empty hardware** without demonstrating physically equivalent manufacturing/system boundaries and units. In particular, a composite automotive tank process is **not** an admissible shortcut for a stationary assembled steel bank.

A source-compatible environmental comparison needs the *actual* native openLCA product system and a named BAFU-supported LCIA method. Compute:
- equipment total `sum_i quantity_i * native cradle-to-gate impact_i` plus transportation, on-site construction and end-of-life where studied, while handling recycling allocation consistently;
- source-year electricity and other operating flows multiplied by regionally and temporally appropriate, **independently sourced** inventory factors (not hourly price in EUR/MWh);
- incremental system difference E+S minus E, **divided by same independently delivered H2 service** in kg, with uncertainty terms for missing material/process/geography and a life/replacement sensitivity.

If any essential manufactured equipment quantity/provider conversion or native LCIA run is missing, the total GWP must remain **NULL**, not a precise-but-incomplete numerical result.

## 4. Hard scientific verification and executable stop gate

Code: src/ptxlens/l3d_bafu_incremental_inventory_gate.py. Run:

    python -m ptxlens.l3d_bafu_incremental_inventory_gate --output data/results/L3_D_BAFU2026_native_incremental_stationary_TypeI_MAPPING_BLOCKED_v1.json

This source-locked generator ensures original 19-category BOM completeness in each semantics; the original reference count and empty equipment masses; no false material or vendor quotation assumptions; no substitution of BAFU native process IDs; and no implicit zeroing of 18 missing BoP categories. The final native-BAFU admission function always **fails closed**: it will not certify a hand-written collection of UUID strings as an actual validated openLCA database calculation.

To progress beyond this ledger requires a separate *real native-database import and process/provider/reference product UUID replay*, then an independently verified LCIA result against the exact licensed input source. Actual complete native process inventory and validation of all 38 source-F2 scope lines are not established.

## 5. Reproducibility and release constraints

- Preserve source equipment Git blob and original published F3-D source-year aggregate SHA; model H2 service within year/mode is the functional denominator, not the original full 50t/day contract.
- Treat 2023 Type I tank-only literature cash cost (2024 EUR) and 2022/2024 operational cost differences as **financial**, not material emission data. L3-D source-year hypothetical CAPEX ceilings are not vendor BOM proofs.
- Do not commit BAFU .zolca, .spold, proprietary process inventories, private original ENTSO-E/ERA5 hourly files or source hourly solver primal without separate distribution authorization.
- The missing native LCIA cannot be assigned a value from the published four-case **energy and money aggregates alone**.

**Conclusion:** A physically sourced incremental hardware scope and fail-closed native BAFU 2026 admission methodology are now available. Actual complete BAFU provider-linked LCA and whole-system/whole-plant CO2e remain NOT VERIFIED; neither PtXFlex nor PtXLens has met the scientific v1.0 gate.
