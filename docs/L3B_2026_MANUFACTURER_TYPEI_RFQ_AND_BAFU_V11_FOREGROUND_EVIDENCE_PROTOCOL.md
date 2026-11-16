# L3-B — OEM stationary H₂ equipment RFQ, foreground inventory and native BAFU v1.1 evidence protocol

**Research programme:** OEM-PTX-2026-01  
**Status:** 2026-11-14; source-derived engineering request package, **not yet an OEM RFQ sent, received, verified, or a completed LCA**.  
**Owner:** PtXLens independent OEM cost/GWP qualification, with source quantities in PtXFlex.

## 1. Problem being priced / characterized

Reference model: E (20,000 kg modelled hydrogen storage) versus E+S (40,000 kg), 30 bar absolute PEM outlet, minimum 20 bar absolute delivery, 200 bar absolute vessel-bank *thermodynamic screening ceiling*, 313 K constant-temperature gas property screen, source charging upper bound 2,200 kg/h, 50 MW signed electrical interconnection, onshore/industrial site location and requirements **unspecified**.

There are **two separate design interpretations**, not one universal capacity: `max_inventory` (20t/40t is total bank-stored H₂, including residual heel) and `usable_service` (20t/40t is withdrawable H₂ above residual heel). The literature 200 bar **gauge** vessel rating and source 200 bar **absolute** screening are different reference conditions. The published Ademollo et al. DOI `10.1016/j.ijhydene.2025.152849` Table 2 is a harmonized 2024 EUR *literature* example: nominal 26 kg H₂ capacity per 1.8 m³ 200 bar(g) Type I reference vessel, **2,400 kg reference finished empty equipment mass**, and **222 EUR2024 per kg rated H₂ capacity**. It is *not* a manufacturer quote, a guaranteed usable gas density at 313 K, proof of a plant-safe PED design, or raw steel material mass.

The source-model study reports the **additional** 20t→40t bank reference of 802 literature vessels (max-inventory interpretation) or 902 literature vessels (usable-service interpretation). These counts are model sensitivities, **not recommended station hardware or vendor order quantities**. Vendor sizing must instead specify free gas volume, material, pressure, operating temperature, allowable duty cycles, design life, hydrogen compatibility, product pressure classification, inspectability and fatigue margins for a real service/design specification.

## 2. Technical datasheet / RFQ question set to manufacturer

Request a **dated, supplier-identified, revision-controlled and site-conditional** quotation, if available, separately covering each of the following:

- **Pressure storage:** design/maximum working pressure in explicit **bar(a) or bar(g)**, minimum operational delivery pressure, allowable pressure range, MAWP/test pressure, free internal volume, temperature range, design cycles, fatigue life, H₂ compatibility and purity/material requirements, installed clearances, PED evidence and any locally applicable conformity scheme; serial number is unnecessary at RFQ stage.
- **Manufactured vessel and material inventory:** actual empty manufactured vessel/module mass **by model**, separately from gas capacity; material grade, corrosion coating, material input masses by grade (virgin/recycled by documented supplier), plate/forging feedstock, fabrication/heat treatment, scrap/yield, welds, equipment energy inputs and manufacturing origin. **A 2,400 kg finished reference is not 2,400 kg of purchased virgin steel.**
- **Headers and auxiliaries:** rack/structural and anchor steel, valves, isolation/ESD, pressure relief and vent stack, non-return valves, purifiers/dryers, filters, delivery regulation, condition monitoring/flow-temperature-pressure metering, leak detection and area classification, electrical motors and VFD.
- **Compression/cooling:** 30 bar(a) inlet to the selected approved bank pressure, H₂ mass-flow and part-load operating window, number of stages, efficiency and parasitics with guaranteed electric inputs (not merely a theoretical upper-pressure enthalpy), intercooling and aftercooling energy, cooling water/pump/fan use, gas cleanliness/temperature control, annual inspections, equipment service life.
- **Civil and balance of plant:** foundations, pipe/cable and site construction, safety zoning, installation and commissioning, pressure-test/fatigue test plan, logistics/transport including site and supplier geography, annual maintenance/consumables/spares, end-of-life disposal/steel recovery.
- **Commercial scope:** quantities and units, itemized price **currency and quotation year**, ex-works versus installed pricing, taxes excluded/included, geography/currency/year assumptions, warranty, what is excluded, escalation, project schedule and quoted service frequency. Do not mix 2024 nominal literature EUR with 2023 project-value EUR without explicit deflator and missing-scope corrections.
- **Environmental evidence:** product-specific EPD/ISO 14040/14044 model or process inventory when genuinely provided; life-cycle boundary, source year and geography, material input exchanges, energy transport and scrap allocation assumptions, operational electricity separation, recycling/end-of-life scenario and verification status. Manufacturer-provided data are distinct from a native BAFU-linked LCIA calculation.

Do not request confidential company information to be committed to public Git history. Keep all OEM original PDFs/CSVs/quotations and provider terms in private research storage, with non-sensitive SHA-256 references in reproducibility records.

## 3. Mandatory foreground equipment scope (19 line identifiers)

The evidence intake uses exactly the existing source-registered F2 scope, from `f2_l1_stationary_bom_bridge.py`:

`typeI_200bar_bare_reference_vessels`; `steel_alloy_material_grade_and_inclusions`; `rack_frames_and_anchors`; `high_pressure_headers_and_interconnects`; `isolation_valves_and_actuators`; `non_return_valves_and_filters`; `pressure_relief_and_vent_stack`; `pressure_regulation_delivery_header`; `compressor_recips_and_seals`; `compressor_motor_drive_VFD`; `intercooler_aftercooler_heat_exchange`; `cooling_pumps_and_fans`; `gas_quality_dryer_and_sample_system`; `pressure_temperature_flow_metering`; `hydrogen_leak_detection_ESD_ATEX`; `civil_foundations_and_construction`; `inspections_fatigue_cycle_testing`; `installation_and_transport`; `decommission_and_EOL`.

Every scope class must be explicitly quantified with original evidence or remain unresolved. Double-counting of a quoted complete equipment package and its individual subcomponents must be prevented by itemized source boundaries; do not assume any missing BoP has zero capital cost or zero environmental inventory.

## 4. Native BAFU:2026 v1.1 technical admission

1. Preserve original `.zolca` database and documented BAFU v1.1 source SHA/version. Reconfirm installed openLCA calculation method: `IPCC 2021 GWP 100`, functional unit and origin-dependent boundaries.
2. Identify process flow/product UUIDs **actually present in the loaded v1.1 database**, the process exchange reference flow unit and geography. **Never infer kg of fabricated vessel from a product described as kg of H₂ capacity**. The BAFU v1 *vehicle composite H₂ tank* process UUID `b4739ad2-aa38-368d-8ada-63f5417c8b55` is not a stationary Type I alloy steel vessel manufacturing inventory.
3. Link manufacturer-verified raw input material flows by alloy grade, recycled content and reported fabrication inputs to suitable BAFU material, metal forming, energy, infrastructure, transport, cooling and end-of-life processes. Require unit conversions, separate primary/recycled feedstocks, source geography and no double counting.
4. Compute the **incremental** E+S minus E inventory on the **same year-specific hourly delivered H₂ service** (not original 2023 E versus E+S scenarios with different delivered quantities). Distinguish foreground equipment manufacturing, operation/compression electricity, maintenance and EOL; report per installation and per **actually modelled delivered kg H₂** only with declared life, replacement and allocation boundary.
5. Verify the created native BAFU calculation **runs**, native input JSON and export are reconciled with independently audited physical BOM quantities, and the resulting LCIA category units match the method's output. Independently validate mass and carbon closure, release an uncertainty table, preserve database/legal rights and cite original supplier evidence.

**Current boundary:** existing BAFU v1.1 30 bar PEM native reference output is not whole-plant Type I storage GWP. No new stationary manufacturer-verified alloy/material process map or incremental type-I/BOP life-cycle cost and inventory has been validated.

## 5. Reproducible machine-readable input and validation

Under a controlled working copy with original public F2 source evidence unchanged:

```bash
python -m ptxlens.l3b_stationary_manufacturer_bafu_foreground_intake \
  --make-blank-mode max_inventory \
  --output /PRIVATE/RFQ_Gross_Incremental_TypeI_200bar_2026.json

python -m ptxlens.l3b_stationary_manufacturer_bafu_foreground_intake \
  --make-blank-mode usable_service \
  --output /PRIVATE/RFQ_Usable_Incremental_TypeI_200bar_2026.json
```

The 19 source-anchored rows are intentionally blank and do not claim received offers. After private source documents and true manufacturer data are available:

```bash
python -m ptxlens.l3b_stationary_manufacturer_bafu_foreground_intake \
  --audit-private-manifest /PRIVATE/RFQ_Usable_Incremental_TypeI_200bar_2026.json \
  --private-evidence-root /PRIVATE/source-documents \
  --output /PRIVATE/L3B_Usable_Supplier_Source_Readiness_Review.json
```

A SHA-verified *local source document* confirms only a preserved piece of evidence, not the authenticity of a supplier claim. Independent engineering sign-off, genuine BAFU process inspection, native calculation, field compatibility and supplier review remain mandatory. Audit results deliberately return `full_L3_B_economic_and_environmental_release_ALLOWED: false` until all such conditions are separately established.

**Research gate remains NOT PASSED.** The exercise is an evidence-based manufacturer and inventory acquisition route, not an extrapolated capital-price or CO₂-equivalent estimate.
