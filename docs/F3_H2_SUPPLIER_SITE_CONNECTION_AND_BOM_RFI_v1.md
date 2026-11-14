# F3-RFI-001 — Physical H₂ delivery and station equipment evidence request

**Programme:** OEM-PTX-2026-01 · **Status:** Technical due-diligence specification, **NOT sent to supplier or Hynetwork**, no plant site verified.  
**Date:** 2026-11-14 · **Purpose:** obtain the *minimum auditable vendor/TSO evidence* that would allow a prospective H₂ supply source to be integrated into a same-service 8,760-hour dispatch, native BAFU v1.1 LCIA, and EUR DCF.

## 1. Reference service to state accurately

The original 2023 Dutch electricity/weather PyNEXUS run is a **modelled study**: original full demand **18,250,000 kg H₂/year**, original E *delivered* profile **16,335,279.317 kg/year**. Pressure-screened Type I storage uses the source-model **20 bar(a) minimum delivery node**.

Against the original E-*delivered* hourly profile (not 50,000 kg/day full contractual demand), independent source-based optimization proves an E 20t gross-stock extra shortage lower bound **65,860.378 kg**; one feasible E schedule has **66,524.317 kg/year**, **1,029.028 kg/h** maximum hourly replacement, **2,509.516 kg** largest rolling 24h, over **176 hours** in **92 episodes** (longest 8h). The different physical interpretation, 20t *usable above heel*, has 3,718.744–3,720.371 kg annual shortage; a feasible schedule needs at most **183.609 kg/h**, 324.546 kg/24h, over 91 hours in 87 episodes (longest 2h). Both hourly schedules are in [original-source-derived 8,760h sparse files](../data/results/).

**All of these are modelled top-up requirements for specific feasible incumbents, not certified capacity ratings, actual purchased hydrogen, 2023 storage plant measurements or a statement of year-round source reliability.** A future system should be designed using time-indexed source/plant simulations and appropriate margins—not uncritically to just one maximum number.

## 2. Minimum submission from a proposed H₂ supplier / Hynetwork connection developer

| Requirement | Evidence requested | Signoff gate |
|---|---|---|
| Geographic scope | **Actual industrial site coordinates**, customer delivery point, commissioning date and 2023 vs prospective 2026+ service date | Verify physical connection is real/contractable |
| Source and ownership | Identified hydrogen-producing supplier(s), origin and production technology, balancing party, contracts and upstream capacity | No anonymous “green pipeline H₂” |
| Hourly supply | Firm 8,760h nominal and firm capacity as **kg H₂/h**, seasonal/maintenance outages, notification/startup lag, nominating rules and time zone | Source H₂ shortfall profile can be matched each hour |
| Pressure | **Guaranteed MINIMUM bar(a) at the customer product node after regulation and piping losses**, maximum allowable pressure, temperature envelope, hydraulic pressure drop at worst-hour flow | 20 bar(a) target met with a verified model |
| Gas quality | Customer-specific H₂ content, max H₂O/O₂/N₂/Ar/CO/CO₂/hydrocarbon/sulfur/other contaminants and product application, sampling/measurement method, quality excursion remedy | End use rather than an assumed ISO class |
| Contract | Exit/entry fees, minimum take, take-or-pay, imbalance, demand/peak tariff, availability, force majeure, guaranteed hourly rights | Reliable and monetizable service |
| Station mechanical | P&ID, hydraulic and valve/relief sizing, pipe material/embrittlement fatigue assessment, check valves, ESD, vent/purge, regulation, flow meters and analyzers, redundancy, gas detection | Vendor/qualified independent engineering approval |
| Compliance | PED/CE/ATEX and relevant Dutch local regulatory basis, local permits, safety and HAZOP files | Engineering and permitting acceptance |
| Equipment BOM | Fabrication materials in kg by grade, component manufacturing/installation quantities, motor/regulator/control/valves/meter/cooling energy, equipment replacement and end of life | Native BAFU v1.1 compatible LCI mapping |
| Physical losses | Purge/vent, leakage, transport, drying, booster compression and pressure drop, gas heel/transfer | Mass/energy closure and LCA |
| Cost | Delivered H₂ EUR/unit, capacity reservation, connection CAPEX and permitting, stations & installation, OPEX, electricity, tariff, replacement, cost year/FX | Source-supported 2023/forward EUR DCF with sensitivity |
| Environmental data | Upstream lifecycle H₂ source, production electricity/water/feedstock, transport and conditioning inventory, source-geography and time basis, EOL/replacement, uncertainty and allocation | Real native BAFU supplier links and IPCC 2021 GWP100 |

**Do not imply that supplier delivery is certain if a contact, quote, pipe map or generic Hynetwork PDF is the only evidence.** These are screening documents only. Hynetwork's [2026 Transport Annex 7](https://www.hynetwork.nl/sites/hynetwork/files/2026-07/general-terms-and-conditions-transport-annex-7-pressure-specification.pdf) describes **network-entry pressure 30–50 bar(g)**, **not customer-exit 30 bar(g)**; Annex 2 delegates quality/temperature specifications to the competent authority. Obtain the actual **connection exit technical annex** and end-user quality requirements before rating the 20 bar(a) interface. Use [Hynetwork customer connection process](https://www.hynetwork.nl/en/contracts).

## 3. Alternative trucked-gas procurement evidence

For an actual Dutch qualified tube-trailer system require: supplier and site location, permitted route/parking and available deliveries, certified usable mass **at customer minimum 20 bar(a)** (not nominal onboard mass), trailer rating and residual pressure, transfer compressor/booster, receiving/flow capacity, on-site buffer vessel, unloading duration and personnel, backup stock and refill calendar, trailer manufacturing and fleet allocation, truck fuel and emissions, losses, insurance/safety and end-of-life. For comparison only, [US DOE](https://www.energy.gov/cmei/fuels/hydrogen-tube-trailers) lists 560–900 kg composite **nominal payload**; the 20t gross-incumbent 66.5t annual need corresponds to at least 74 *900kg nominal payload equivalents*, **not actual physically available Dutch trips**. At 1,029 kg/h worst-hour, one hypothetical 900kg fully available truck cargo alone is insufficient for an entire such hour without a buffer or another supply route.

## 4. Evidence processing and study release gates

Accept data only when source locator, document date/version, native units, pressure basis, geographic/temporal relevance, confidentiality/reuse license, equipment material specification, independent evidence checker and uncertainty have all been recorded. Historical model weather and prices **remain 2023**, while 2026 network infrastructure or merchant H₂ is a **prospective counterfactual**, not observed historic service.

Before a comparison: solve an updated *joint* physical H₂ optimization for both E and E+S including backup production, pressure/cooling and all equipment; independently verify full 8,760h H₂/energy conservation and same purity/pressure/product gate; then run native actual BAFU-v1.1 manufacturing/operating inventory and full EUR lifecycle DCF. Until these are possible, data remain `null`, matched-system superiority claims `false` and v1.0 gates **NOT PASSED**.

**Prepared by programme for potential sourcing; no external party has been contacted and no cost/purity/operability quotation has been received.**
