# L1 — BAFU high-pressure tank reference-basis and technology audit

**Programme:** OEM-PTX-2026-01 · WP L1/L2 · 13 Nov 2026  
**Evidence:** actual user-authorized BAFU:2026 **v1 original EcoSpold** source archive, SHA-256 ebaab56717a6227b5eb271fcb4c86fb9db206115eb937fb0ec0b10d7accf26c7, examined directly from source XML \`process_b4739ad2-aa38-368d-8ada-63f5417c8b55.xml\`. Original EcoSpold is NOT redistributed. Its native **BAFU v1.1** counterpart has **not yet been rechecked** for this process's reference basis and providers.

## Finding: unit named kg is not enough to establish kg *empty vessel*

The BAFU source product named **High pressure hydrogen storage tank**, process UUID **b4739ad2-aa38-368d-8ada-63f5417c8b55**, has exported reference unit **kg** and is categorized under **road / Vehicle components / Energy storage / Hydrogen tank**. Crucially, the original source general-comment describes the tank inventory **per 1 kg hydrogen** and refers to Boureima et al. 2011, Das 2011 and Wulf et al., *Journal of Cleaner Production* 199 (2018), 431–443, with an assumed **20-year lifetime**. That wording is not one kilogram of empty hardware.

### Actual source technosphere recipe (per ambiguously labelled reference unit)

| Technosphere material | Original input, kg |
|---|---:|
| Steel, low alloyed | 0.90 |
| Chromium steel 18/8 | 0.90 |
| Woven carbon fibre | **7.14** |
| Aluminium alloy AlMg3 | 0.60 |
| Epoxy resin | **3.06** |
| **Total named materials** | **12.60 kg** |

The process separately accounts for sheet-rolling *services* and freight transport. Sheet-rolling exchanges are **not additional physical equipment material**, and counting them as physical kg would double-count.

Since material inputs sum to 12.60 kg for an output labelled 1 kg and the source explicitly describes a **per-kg-H₂ capacity** model, the process cannot honestly be used as a **per-kg-empty-stationary-steel-vessel** factor. A pressure/capacity reference unit is not interchangeable with equipment mass. The technology includes composite vehicle-tank materials; it is not identical to the published stationary **Type I steel** reference vessel in the PtXFlex F2 bank.

**Blocking rule:** do NOT multiply the BAFU tank process's published kgCO₂e/unit by the source-based **empty Type I steel-vessel mass**, or by the original PyNEXUS 20/40t stored H₂ without first resolving the actual product reference functionality. Do NOT set an unknown tank manufacturing impact to zero.

## Connection to actually source-grounded 2023 storage study

The frozen original E and E+S PyNEXUS configs specify **20,000 and 40,000 kg maximum modelled storage inventory**, common 10,000 kg initial/terminal, 30-bar PEM outlet, 20-bar minimum pipeline pressure, 2,200 kg/h source charge/discharge limits and a modelled 0.0001/h standing-loss parameter. Those do not define a physically installed compressor, vessel code, working hydrogen inventory or empty tank mass.

PtXFlex [F2 physical volume and published vessel source audit](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F2_PUBLISHED_STORAGE_PRESSURE_SWING_AUDIT.md) compares actual Type I/II/III/IV source vessel dimensions and mass from [2026 stationary storage study Table 2](https://doi.org/10.1016/j.ijhydene.2025.152849), with real-gas H₂ density from CoolProp 8.0.0 and hypothetical pressure bounds. **Reference-vessel masses are real literature parameters**, but not yet a complete physical plant BOM or source-verified manufactured-system LCI.

The F3 original-2023 historical comparison first fixes *the same hourly delivered hydrogen profile*. This can precede equipment LCA; cost/GWP/complete physical comparisons must wait until working gas capacity, hardware and energy are valid.

## Native PtXLens v1.0 source-provider completion procedure

1. **Read the authorized v1.1 native BAFU tank process** ID/reference product, actual output reference flow, functional unit, inputs, impact-method categories, geography, application technology and system lifetime. Use a private original DB, without publishing licensed inventories. Do not silently assume equality with the inspected v1 original.
2. **Select an engineering-matched actual vessel technology**. Only after F2 proves actual bank pressure, usable/heel inventory and representative wall/liner/composite BOM, determine if a valid native BAFU supplier matches its intended product. The published vehicle composite tank is not a generic stationary steel supplier.
3. **Construct a stationary Type I foreground material inventory if selected** using externally sourced manufacturer wall thickness, materials, valves, supports, pressure rating and installed mass, and appropriate BAFU metal-processing supplier flows. Process BOM and replacements must be independently checked. The original literature empty reference-vessel mass alone is not enough to assign steel/composite *fractions* or fabrication processes without review.
4. **Account for physical storage throughput**, compressors, pressure drops, heat/cooling, motor/auxiliary load, replacement lifetime and end-of-life. Avoid double-counting original 30bar BAFU PEM BoP, its stack replacements or BAFU tank materials.
5. **Re-execute native BAFU v1.1 IPCC 2021 GWP100** for physically comparable 20/40t operating configurations and same hydrogen service, reporting all flow/provider and elementary-characterization quality gates.

### Automated source-identity safeguards

- [BAFU tank original-v1 restricted-source audit module](../src/ptxlens/bafu_tank_process_audit.py) checks the exact authorized original ZIP SHA, tank UUID/name/reference unit, source comment and all named original source input quantities. It emits only source-safe derived metadata.
- [Derived original process-unit mismatch result](../data/results/BAFU2026_v1_storage_tank_source_unit_mismatch_audit.json) records exact verified material inputs and prohibited mappings, with no raw XML.
- [Negative regression tests](../tests/test_bafu_tank_process_audit.py) reject tampering and incorrect unit/technology claims; real restricted ZIP replay can be run on a private machine with the BAFU_ORIGINAL_PRIVATE_V1_ZIP environment variable.

**No native tank-manufacturing GWP added yet.** The previously executed native E/E+S reference scores of 6.1481744 and 6.0765527 kgCO₂e/kg modelled H₂ remain explicitly **scoped, incomplete and not same-service environmental comparisons**. This audit is a necessary prevention of a major apparent methodological error—not a complete L1/L2 pass.
