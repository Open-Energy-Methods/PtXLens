# L1/L2/L3 — physical H₂ backup source admissibility and native LCIA/DCF evidence contract (v0.1)

**Programme:** OEM-PTX-2026-01 · **Date:** 2026-11-14 · **Status:** BLOCKED for comparative full-plant GWP or LCOH.

PtXFlex's original 2023 8,760-hour wind/market and PyNEXUS E-delivered H₂ data are used as the historical operating experiment. A 2026 network or supplier option is a **prospective scenario** only, not proof of physical 2023 delivery. The source-registered physical route design is in [PtXFlex F3-DESIGN-001](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F3_PROSPECTIVE_H2_BACKUP_SYSTEM_DESIGN_BASIS_v1.md).

## H₂ replacement scope

The actual source-verified additional H₂ top-up envelopes for two distinct 20t E storage interpretations are:

| 20t E model semantics | Source-derived feasible dispatch top-up kg/year | Peak kg/h | Largest 24h kg | Historical service |
|---|---:|---:|---:|---|
| Original gross maximum stock | 66,524.317 | 1,029.028 | 2,509.516 | Only original E-delivered 16.335m kg, not full 18.25m kg |
| Physically usable above EOS heel | 3,720.371 | 183.609 | 324.546 | Same E-delivered 2023 target |

These are **not** zero-emission external H₂, source purchase contracts, actual backup peak duties or a full matching of the original industrial 50t/day target. The 40t E+S source model can meet the E-delivered hourly reference under both screening interpretations, but that does not prove either system's full lifecycle costs or impacts.

## Source provider and quality requirements

The **2026 Hynetwork Transport Annex 7** (source register [`research/f3_backup_physical_source_register_v1.json`](../research/f3_backup_physical_source_register_v1.json)) gives 30–50 bar(g) for **transport-network entry** conditions. It does **not** guarantee an offtake exit point at 30 bar(g), so the original model's 20 bar(a) product node cannot be declared physically supplied. The 2026 **Annex 2** similarly does not establish the customer's hydrogen end-use impurity requirements. A real customer contract, network connection and source supply route are still unknown. [ISO 14687:2025](https://www.iso.org/standard/82660.html) is application-specific; do not assign a generic "pipeline purity" to unspecified industrial product feedstock.

### Full non-optional system inventory before native openLCA

For any actual candidate connection and source, request:
- **External fuel supply cradle-to-delivery:** documented production method and upstream feedstocks, gas compression and electricity, purification, drying, metering, valves, transfer losses, source-country grid/electricity mix, transport and distribution network allocation; separate attributional average and marginal/counterfactual climate frameworks.
- **Customer interface equipment BOM:** code-compliant pressure regulation train, isolation, check, relief and vent, gas detector, sampler/analyzer, meters, certified supports/pipe and auxiliaries, installation, maintenance, replacement cycles and end-of-life. For a trailer-based option include trailer ownership/allocation, fuel, trips, loading/unloading, onsite pressure buffer and loss-to-minimum-pressure. **Published 900kg US composite-trailer nominal capacity is not a Dutch delivered or usable payload.**
- **Native BAFU provider mapping:** source BAFU:2026 v1.1 process UUIDs and verified source-unit compatibility, geographical and temporal scope, product and functional unit, uncertainty distributions; explicit rejected/alternative provider decisions. Do not misuse the existing composite vehicle-tank dataset for Type I stationary steel vessel manufacturing, or silently treat missing flows as zero.
- **TEA:** source price/currency base year, tariff/connection capacity charge, H₂ purchase, gas transport, regulator and buffer installed capital, operations, pressure loss, auxiliaries, delivery failure cost, replacement and discounted cash flow; no original wholesale electricity settlement reclassification as total LCOH.

## Two separate acceptance gates

**Source physical gate:** confirm a real site-specific infrastructure connection and delivery supplier, commissioning/availability year, gas quality, guaranteed exit pressure and certified peak flow (at least the particular source-incumbent top-up as a starting design requirement), time-matched deliverability, detailed piping/component compliance and independent review. If physically matched backup is used, ensure no double-counting of upstream electricity or external H₂ and no unlocked artificial supply.

**Full LCA/TEA gate:** after physical service gate and product interface pass, execute actual native BAFU v1.1 cradle-to-gate inventories and lifetime EUR DCF for **equal hourly certified hydrogen service**, including backup and all incremental equipment. Distinguish the historical 2023 operating inputs from prospective 2026 network technology, and report temporal uncertainty. Signed supplier evidence and owner/critical reviewer approvals are required before removing the current comparative block.

Existing 6.1481744 (E) and 6.0765527 (E+S) kgCO2e/kg H₂ native BAFU results remain *scoped original source electricity/water replacements* and cannot be used as comparative full-system superiority. A validated BAFU supplier network does not demonstrate that omitted manufacturing and backup operations were counted.

**Release:** L1/L2/L3, F3 and the combined hydrogen v1.0 gate remain NOT PASSED; draft PR not merged.
