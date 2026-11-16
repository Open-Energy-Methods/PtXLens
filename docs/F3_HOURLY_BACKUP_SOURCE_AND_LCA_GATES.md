# PtXLens L1/L2 — 2023 source-based E hourly backup-load intake

**Programme:** OEM-PTX-2026-01 · **Checkpoint:** 14 November 2026.
**Evidence:** [PtXFlex F3 Stage B original-source workflow](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43527327817); mathematical hourly delivery-node top-up only, **no physically sourced backup supply**.

Two independently hash-pinned original 2023 E source-derived result files:
- [Gross maximum-inventory 20t E](../data/results/F3_2023_original_E_source_hypothetical_backup_max_inventory.json), SHA-256 `c65fda894ef4b30e09339ad88a3972625af78c17802fd0cb9a2fc25d3205882f`.
- [Physically usable 20t E](../data/results/F3_2023_original_E_source_hypothetical_backup_usable_service.json), SHA-256 `d893c6388f14d276b2ef5d4bff4b6c8057dd252067f307f83b9baafcfa1e5308`.

The backup envelope references the **same original E-delivered hourly target** of 16,335,279.317 kg H2, NOT the larger original 18,250,000 kg demand. Real-gas pressure-screened E Stage A produces minimum additional shortage bounds of 65,860.378–66,524.317 kg (gross max interpretation), or 3,718.744–3,720.371 kg (usable interpretation); 40t E+S has a separate independently validated zero-shortage witness in both.

## Hourly design-requirement envelopes — not approved hardware ratings

| E source mode | Feasible Stage A schedule top-up (kg/year) | Peak kg/h | Max rolling 24h kg | Hours with top-up | Contiguous events |
|---|---:|---:|---:|---:|---:|
| 20t gross inventory | 66,524.317 | 1,029.028 | 2,509.516 | 176 | 92 |
| 20t usable inventory | 3,720.371 | 183.609 | 324.546 | 91 | 87 |

These constitute **mathematical top-up for specific feasible (not global optimal) dispatch schedules**. A real supplier has not been selected, so minimum pressure/purity and transport, reserve/ramp/reliability, marginal environmental inventory and economics are all unknown. Do not treat missing quantities as zero, design source hardware from one raw peak without engineering reserves, or extrapolate these values to the original full 50t/day contract.

The [PtXLens source-verified gate](../src/ptxlens/f3_backup_service_gate.py) checks the two derived evidence SHA hashes, both original model hashes, F3 reconciled certificate interval closure and the explicit missing-source flags; it refuses full comparative LCA and TEA.

## Release decision

**L1:** Requires physically specified and documented backup manufacturing/transport/cooling and pressure regulation plus Type I steel-vessel/BoP compatible LCI provider(s).
**L2:** Requires native BAFU 2026 v1.1 calculation for the full matched service including actual backup supply and all omitted component life cycles, and published uncertainty/critical interpretation.
**L3:** Requires sourced backup electricity/H2 supply cost and installed capital, consistent economic lifetime and EUR reference price-year, tariff/replacement/OPEX and proper independently checked discounted cash flows.
**F4/L4:** Separate methanol chemistry, CO2 provenance, system allocation and product-gate release.

No full plant kgCO2e/kg or full EUR/kg H2 is currently derivable. This is **not a green light to merge/tag scientific v1.0**.
