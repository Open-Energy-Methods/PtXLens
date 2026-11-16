# L1 — physically referenced stationary H₂ storage manufacturing source intake, not yet admissible native BAFU LCIA

**14 November 2026 · OEM-PTX-2026-01 · Source-backed component-foreground preparation: TESTED. Complete native L1/L2/L3 scientific release: NOT PASSED.**

## A. Correct original 2023 physical and functional boundary

[PtXFlex F2 engineering source audit](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F2_L1_STATIONARY_TYPEI_INCREMENTAL_EQUIPMENT_SOURCE_AUDIT_v1.md) defines original PyNEXUS E20t vs E+S40t source, at 313K, research 20–200bar(a) Type I gas-pressure screen. The source 2023 model has **two distinct inventory semantics**: `max_inventory` means original upper bank *gross* H₂ mass, and `usable_service` means hypothetical actually withdrawable H₂ from 200bar(a) to 20bar(a). A bank's physical gas heel is a *stock of hydrogen*, not the quantity of steel required to manufacture it.

The downstream LCA/TEA functional unit must retain exact **F3-C modelled original-E-physically-feasible reduced 8,760-hour H₂ service**, and not the original full industrial 18.25mkg/year demand. [Four-case original-source F3-C 8760h certificate](../data/results/F3_C_2023_source_real_gas_equal_H2_hour_E_vs_ES_Lens_operational_bridge.json) proves net **2023 wholesale-only** EUR savings 1.12433m (gross) or 1.10346m (usable) with solver bounds, but no installed capital or lifecycle GWP.

## B. Two independent sourced pressure-vessel candidates — NOT interchangeable

| Quantity | Peer-reviewed *reference* steel Type I 200bar | Actual manufacturer heiserTEC *different* PED Type I 330bar 50L H₂ cylinder |
|---|---|---|
| Source | [Ademollo et al., IJHE 2026 Table 2](https://doi.org/10.1016/j.ijhydene.2025.152849) | [heiserTEC Type I product range, Hydrogen 50L / PED / EN1964-1 /330bar](https://www.heisertec.com/products/type-1/) |
| Published EMPTY equipment per pressure vessel | **2,400kg** per **1.8m³** paper reference vessel | **85.5kg** per **0.05m³** actual OEM-cylinder reference |
| Candidate source pressure rating | 200bar; **assumed absolute for screening** | 330bar *manufacturer product class*, not the simulated 200bar operating pressure |
| Gross `max_inventory`: incremental E→E+S vessel count | **802** | **28,878** (hypothetical use at 200bar(a), 313K) |
| Gross `max_inventory`: incremental EMPTY equipment mass | **1,924,800kg** | **2,469,069kg** |
| `usable_service`: incremental vessel count | **902** | **32,468** (hypothetical use at 200bar(a), 313K) |
| `usable_service`: incremental EMPTY equipment mass | **2,164,800kg** | **2,776,014kg** |
| Manufacturer component steel chemistry, forgings and weld inventory | Unknown | Unknown |
| Actual PED/EN17533 site conformity or module approval | Not demonstrated | Not demonstrated |
| Installed manifold/frames/coolers/compression, pressure reducers, inspection, price | **Unknown** | **Unknown** |
| Per-product matched BAFU v1.1 background manufacturing provider and complete LCIA | **NULL** | **NULL** |

The alternative OEM 330bar H₂ cylinder and IJHE 200bar large steel tube are **different capacities, wall thickness and pressure classes**. Their reference masses do **NOT** define an uncertainty distribution for a single installation. The OEM cylinder's **85.5kg** is sourced and hydrogen-compatible according to its public technical table but its **site-approved service and material certification** are absent. Calculating 200bar(a) actual gas content is *an operating counterfactual*, not manufacturer certification. The separate heiserTEC [**COSMOS Stationary (PED)** 210bar class 36×87L/49kg gross-H₂ module](https://www.heisertec.com/products/bundles/) has **no public stationary module empty mass**; do not transfer the empty mass of the 935kg **Mobile TPED 12×50L** product or the 330bar 50L PED cylinder to it.

Original [PtXFlex native-backed numerical Type I F2 results](../data/results/F2_L1_2023_source_incremental_20t_to_40t_stationary_typeI_200bar_BOM_SCOPE_NOT_complete_native_LCI.json) SHA **`1315d1181b9d1eab6d3368425c9571dbe295c3360935d2972403bf3c60e2dc47`**; [PtXLens imported source-hash physical equipment ledger](../data/results/F2_L1_2023_stationary_TypeI_Lens_manufacturing_foreground_REQUIREMENTS_NOT_native_LCA.json) SHA **`95e8ec08d85a02deabb6bb22757889c57dd96d3e4c11aa7c741e03fc5bbd4eac`**; [OEM independent manufacturer result](../data/results/F2_L1_OEM_heisertec_PED_330bar_50L_85_5kg_source_200bar_313K_NOT_certified_BOM.json) SHA **`9db1885bd42cc91049c4d2e7170aaf74782bf0d791ed88b877795e84fa4a8a57`**; [PtXLens OEM separate hardware comparison](../data/results/F2_L1_real_OEM_330bar_50L_PED_source_vs_IJHE_200bar_manufacturing_stop.json) SHA **`055f1971a1d239de54f925051b51afd046744b87f270efadcacb59c6f5a6d9b0`**.

## C. LCI unit matching, supplier processes and the 18 unresolved categories

**Functional unit mismatch must remain a hard block:** The original BAFU 2026 v1 source [vehicle composite “High pressure hydrogen storage tank” source-unit correction](../data/results/BAFU2026_v1_storage_tank_source_unit_mismatch_audit.json) proves UUID **`b4739ad2-aa38-368d-8ada-63f5417c8b55`** describes a **road-vehicle composite tank per kg H₂ storage capacity**, despite its output `kg` unit. It is **not** `kg virgin steel`, `kg empty Type I station vessel` or a 2026 native stationary-steel product system. It must not be substituted for **any** of these reference masses.

For a valid future manufacturer-foreground inventory we still require **all** of the following quantified and manufacturer-audited as either new incremental system burden, existing reused equipment or explicitly excluded with physical reason:

- Vessel material: actual alloy steel chemistry/grade, forging/heat treatment/machining, batch mass, scrap yield/steel recycled fraction, coatings, nozzles and head closure weight; separate equipment dry mass from gas mass, purchased raw steel, scrap and hot-work process.
- Racks & foundations: exact frame steel, anchors, concrete, foundation/civil/earthworks, lifts, and site layout/access/venting.
- H₂ piping and safety: manifold/header/fittings/gas valves, regulator, filters, check valves, pressure relief/TPRD, vent stack, hydrogen sensors and ATEX equipment.
- Compressing/cooling: OEM 30→200bar specific charge-flow vs discharge map, seals, motor drive, cooler/aftercooler heat load, cooling water fans/pumps and auxiliary electricity, life/cycle maintenance.
- Quality and metering: H₂ purity/water/oxygen specification, flow/pressure/temperature instruments, calibration, leak testing, process control & safety interlocks.
- Lifecycle: initial and replacement manufacturing, annual inspections, repairs, commissioning/transport, end-of-life / salvage and site-specific pressure-vessel safety approval.

This is an **18-unquantified-class + 1 quantified reference-only vessel equipment** engineering requirements register, **not a complete material/process-level LCI**. Current PtXFlex [source-registered 19 BOM categories](../data/results/F2_L1_2023_source_incremental_20t_to_40t_stationary_typeI_200bar_BOM_SCOPE_NOT_complete_native_LCI.json) set **NULL** for unknown quantity, source material and euros; no source item is implicitly zero. The existing original 2023 F3-C optimized **peak charge ~552.43kg/h**, **peak discharge ~2,083.33kg/h** and nominal maximum **2,200kg/h** are *model operating duty inputs*, not a commissioned OEM compressor. [Burckhardt industrial hydrogen compressor catalogue 2026, p2](https://www.burckhardtcompression.com/fileadmin/uploads/burckhardt/documents/applications/compression-solutions-hydrogen-mobility-energy-burckhardt-compression-en.pdf) confirms availability of an oil-free family with discharge up to ~200bar, **not equipment mass, CAPEX or specific site suitability**.

The final full result needs **matching actual BAFU v1.1 flow UUIDs and supplier process geography/units** for appropriate low-alloy/stainless steel, forging, fabrication, electricity, industrial equipment and waste/recycling. If no compatible process exists, source-registered proxy construction plus defensible documented uncertainty is required; **no invented dataset**, no unsourced GWP factor.

## D. Standards and legal interpretation

- [NEN-EN 17533:2025](https://www.nen.nl/en/nen-en-17533-2025-en-338598) is an **active Dutch stationary gas H₂ pressure-vessel standard**, with individual cylinder/tube design/manufacture/test scope (up to 10,000L and 1100bar); it **does not extend to manifolded assemblies or external pipelines**.
- [PED 2014/68/EU](https://single-market-economy.ec.europa.eu/sectors/pressure-equipment-and-gas-appliances/pressure-equipment-sector/pressure-equipment-directive_en) covers stationary pressure equipment >0.5bar and pressure assemblies; site project conformity not verified.
- [EIGA DOC247/24 §§7.3.1 and 7.4.3](https://www.eiga.eu/uploads/documents/DOC247.pdf) establishes representative bundle frames, periodic inspection, H₂ embrittlement/fatigue, safe relief/discharge, and pressure-control station component scope. This is not a vendor bill of materials.

**No full proprietary standard text has been obtained or reproduced.** An ISO draft's earlier status does not negate the valid published NEN-EN 17533:2025 source. Actual conformity requires a selected pressure-vessel assembly and an appropriately qualified engineering review.

## E. Methodology and audit outputs

The [PtXLens L1 physical component-gate source](../src/ptxlens/f2_l1_stationary_bom_bridge.py) and [adversarial unit/source tests](../tests/test_f2_l1_stationary_bom_bridge.py) independently reject any changed PtXFlex original engineering output SHA, false virgin steel mass, 935kg mobile→stationary product mapping, missing required physical equipment rows, fabricated GWP, or discrepant original F3-C H₂ service/pressure-corrected gas heel. [Dedicated source-bridge CI passed](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43583583937).

The [independent OEM product bridge](../src/ptxlens/f2_l1_oem_PED_cylinder_bridge.py) and [negative controls](../tests/test_f2_l1_oem_PED_cylinder_bridge.py) reject 330bar/200bar and different geometry substitution, invalid equipment masses, falsified CE/PED pressure service, or fabricated full Native GWP/DCF. [Dedicated OEM bridge CI passed](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43584237526).

**Stop / release decision:** narrow source-backed physical *reference equipment mass* F2/L1 subgate **VERIFIED**; **manufacturer-conformed 2023 stationary bank, source manufacturing route & mass breakdown, 18 BoP classes, native full BAFU LCI/LCIA, EUR discounted LCOH and full physical original contract not verified**. All overall F2/L1/L2/L3/P0 and hydrogen/methanol v1.0 gates **NOT PASSED**.
