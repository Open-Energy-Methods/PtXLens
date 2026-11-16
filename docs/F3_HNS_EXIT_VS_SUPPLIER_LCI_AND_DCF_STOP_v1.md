# F3 — 2026 Hynetwork customer exit vs H₂ molecule supplier: L1/L2/L3 admissibility audit

**Date:** 14 November 2026 · **Status:** **NOT qualified for full 2023 E/E+S H₂ service LCIA or whole-plant EUR DCF**.

## 1. Correct physical boundary

The original 8,760h [PyNEXUS annual configuration](https://github.com/abhijith-sivaprasadan/PyNEXUS/blob/main/configs/annual.yaml) has a 52.5°N/3.5°E **North Sea ERA5 wind sampling location**, **not an actual industrial H₂ customer connection**. No real hydrocarbon process, PEM skid, delivery plant coordinates or commercial counterparty is specified. This means the infrastructure can be evaluated only as a **prospective 2026 technical counterfactual** replaying 2023 weather/prices, not observed 2023 hydrogen import or a site-calibrated plant.

Hynetwork (HNS) physically transports hydrogen but explicitly **does not produce/procure it or guarantee security of supply** in [Exit Connection Conditions v2.0, clause 2.1.2](https://www.hynetwork.nl/sites/hynetwork/files/2026-07/general-terms-and-conditions-connection-exit.pdf) (p.4). Its [**Exit Annex 12**, p.3](https://www.hynetwork.nl/sites/hynetwork/files/2026-07/general-terms-and-conditions-connection-exit-annex-12-pressure-specification.pdf) provides either network-pressure open-pipe delivery or **a contractually defined reduced fixed exit pressure in the customer's Contract Data Sheet**. The 30–50 bar(g) *system* is not a guaranteed minimum bar(a) at PtXFlex's 20bar(a) header. [Exit Annex 3](https://www.hynetwork.nl/sites/hynetwork/files/2026-07/general-terms-and-conditions-connection-exit-annex-3-quality-and-temperature-specifications.pdf) does not certify any unspecified industrial end-use gas quality.

**Two independent legal/physical gates** must be satisfied: **(A)** actual customer network connection + exit CDS + hydraulic pressure/capacity, and **(B)** separately procured H₂ molecules and nominated shipping/production + end-use assay. An operator transport connection is **not** a fuel sales agreement. Customer CDS and producer contracts are both missing.

## 2. Hynetwork's capacity unit / source-derived result

[Hynetwork 2026 Connection Study Agreement Annex A](https://www.hynetwork.nl/media/t4xd5jjx/connection-study-agreement-template-v0126-with-1-signature-field.pdf) records HHV **12.74 MJ/Nm³** and density **0.090 kg/Nm³**:

`HHV = (12.74 / 0.09 / 3.6) = 39.3209876543 kWh/kg H₂`.

In the original 2023 model, two separate Type I 20t E storage semantics produce source-verified extra-H₂ shortage patterns; full hourly series and source fingerprints reside in [PtXLens source register](../research/f3_h2_exit_and_supplier_source_evidence_v1.json), [gross](../data/results/F3_2023_original_E_sparse_H2_backup_need_max_inventory.json), [usable](../data/results/F3_2023_original_E_sparse_H2_backup_need_usable_service.json).

| One feasible source E configuration | Historical *modelled additional* top-up kg/year | Max 2023 source need kg/h | HNS CSA HHV-based incremental equivalent | **Actual required *full* HNS customer exit booked capacity** |
|---|---:|---:|---:|---|
| 20t E gross | 66,524.317 | 1,029.028 | **40,462.393 kWh/h** (~40.46 MW HHV) | **Unknown** (site/main H₂ + backup allocation unresolved) |
| 20t E usable | 3,720.371 | 183.609 | **7,219.688 kWh/h** (~7.22 MW HHV) | **Unknown** |

**Never conflate** (a) 2023 original H₂ delivered reference 16.335279 million kg/year with original full 18.25 million kg demand, (b) 2023 modelled wind-resource location with a hydrogen customer site, (c) 2026 HNS system pressure with signed CDS exit pressure, (d) **incremental H₂ backstop HHV** with total customer exit booked flow, (e) one optimised *feasible but nonoptimal* E shortage trace with globally minimal equipment rating, or (f) an economically/physically viable supplier with an illustrative perfectly-available source.

## 3. Source-verified downstream gate

[PtXFlex original-source 8,760h hourly H₂ supplier-control workflow](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43577251078) verifies actual source 2023 pressure-model E extra shortage and tests mathematical-only 8,760h supplier/transport/station flow, product header pressure, quality and outages. It generates [two-contract source boundary JSON](../data/results/F3_2023_shortage_2026_HNS_exit_and_supplier_boundary_control.json) with SHA-256 `e918364ad469dd29791d8c9a01f1dc5f9a37435f8247c65a87ba6c388f1e2d25`, byte-identical in PtXFlex and PtXLens. PtXLens [strict HNS/supplier evidence intake](../src/ptxlens/f3_hns_exit_supplier_bridge.py) checks original 2023/2026 timing, model demand, HHV conversion and whether passing synthetic math was improperly promoted to physical/financial certification.

**For every alternative, including hypothetical perfect supply, actual site, supply agreement, legal shipping nominations, customer outlet CDS, gas quality, P&ID, equipment BOM, native provider-linked cradle-to-gate LCI, real source emissions, capital and operating cost, lifetime DCF and critical review are unverified.** Thus: full E/E+S BAFU v1.1 LCIA **null**, full cost EUR DCF **null**, no comparative environmental/cost advantage can be claimed.

For future external enquiry/contract, gather two independent legal offers with actual site date and historical/prospective status, outlet hydraulic/quality and peak flow, manufacturer source process inventory and cost. See [PtXFlex full physical evidence and procurement method](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F3_HNS_EXIT_AND_SUPPLIER_SEPARATE_CONTRACTS_v1.md).

**Decision: L1/L2/L3, F3 and v1.0 gates NOT PASSED; publication may report the modelled shortage and methodological limitations only.**
