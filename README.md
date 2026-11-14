# PtXLens — source-verified Power-to-X economics and environmental assessment

## 14 November 2026 — F3-D/L3-B integrated original 2023 source robustness, lower-wind LP proof and external observed-year input gate

[The new complete integrated F3-D / L3-B methods report](docs/F3_D_L3_B_INTEGRATED_SOURCE_ROBUSTNESS_ECONOMIC_AND_BAFU_METHODS_v1.md), [ADR-016 and *subsequent* ADR-016A](docs/DECISION_REGISTER_v1.0.md), [research gates](research/gates-v1.0.json), and both repositories' shared [2022/2024 observed source acquisition SOP](docs/F3_D_2022_2024_REAL_PROVIDER_DATA_PRIVATE_INGESTION_AND_PROVENANCE_SOP_v1.md) document all current evidence and limitations.

**F3-D:** Original PyNEXUS 2023 source-E and E+S 8,760-hour pressure-screened/identical hourly H₂ product for each DIFFERENT gross/usable inventory mode, reoptimized independently under source original 2023 Dutch wholesale/ERA5-derived wind chronology plus deliberately controlled *2023-only* input variations. Six altered-input source pairings certified to HiGHS 1×10⁻⁶ MIP gap: original 2023 price circular shifted by 168h (E+S net wholesale difference €0.726848m gross / €0.720619m usable), 1.5× source price dispersion (€1.709870m / €1.681103m), and source wind *available MW* ×1.1 (€1.028800m / €0.994498m). The original 2023 source reference is €1.124332m / €1.103464m. These are NOT alternate observed weather years or future market forecasts; do not compare gross and usable across different H₂ product functional units. Original 18.25mkg H₂ customer demand remains unmet.

**Critical follow-on −10% wind model feasibility proof:** The original E and E+S full-hour MIPs under 0.9× available wind returned no accepted primal; new source ZIP/StageA SHA-locked, original 8,760-hour identical physical/pressure/H₂ constraint **LP relaxation**, zero cost objective and only binary integrality removed, returns **HiGHS status=2 infeasible for E and E+S in BOTH modes**. Since this LP feasible set contains the integer dispatch feasible set, **the original fixed source-model H₂ target is mathematically infeasible under that altered source wind** (numerical solver tolerances). It is **not proof of real plant or alternative contract infeasibility** and the savings and DCF remain **NULL**. [PtXFlex actual original-source four-solve CI](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43603396526), [PtXLens independent source fingerprint/proof check CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43603733878).

**L3-B paper manufacturer-cost *reference* only:** Peer-reviewed 2024-harmonized IJHE Type I **200bar gauge**/1.8m³ nominal vessel source €222/kg rated **H₂ capacity** ×26kg H₂ = €5,772 per paper 2,400kg EMPTY vessel; 802/902 additional original research vessels imply **€4.629144m / €5.206344m 2024 EUR tank-only**. Not vendor contracted installed CAPEX, not source study 200bar(a) real installed pressure rating, not comparable directly with L3-A 2023-real-EUR capital ceilings without a price-year conversion; 18 other BoP categories and compatible BAFU:2026 native steel manufacture remain **UNKNOWN**, not zero. [Original source L3-B scientific CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43591024424).

**Independent source-year extension:** Source [private 2022/2024 input ledger](research/F3_D_ALTERNATIVE_OBSERVED_2022_2024_ENTSOE_ERA5_PRIVATE_SOURCE_ADMISSION_v1.json) has **ZERO** accepted raw A44 NL plus offshore ERA5 (52.5N,3.5E) historical pairs. Original PyNEXUS 100m u/v wind-to-120m hub, cubic 15MW×10 turbine model (max available source 125.685MW), provider authorization/licensing, private raw SHA/copy and original 2023 source reproduction must be validated. 2022 UTC=8760h, **2024 UTC=8784h** and original 2023 F3-MILP solver cannot yet accept the leap year. [Synthetic-only negative source intake/UTC/leap CI passed](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43604474724); this **does not mean** observed new-year datasets have been obtained. P0 original 2023 independent private escrow still not completed, source GitHub Actions expires **24 Dec 2026**.

**Strict status:** F3-D original source partial physics/model and LLP proof VERIFIED; genuinely observed-year/whole-plant F3 **NOT PASSED**. L3-B bare-vessel source-only cost VERIFIED; full vendor CAPEX/DCF, L1/L2 BAFU GWP, P0 and hydrogen/methanol v1.0 **NOT PASSED**. Both pull requests remain **DRAFT**.

---

## 14 November 2026 — L3-A scientifically source-registered conditional H₂ storage CAPEX/OPEX DCF frontiers

A complete **narrow mathematical economic study**, NOT a whole-plant TEA, has now been implemented. Original source-2023 [F3-C verified E20t vs E+S40t 8,760-hour E/E+S hydrogen SAME-SERVICE operating model](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F3_C_2023_PHYSICAL_COMMON_HOURLY_SERVICE_VERIFIED.md) and 313K Type I F2 empty vessel equipment [source](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F2_L1_STATIONARY_TYPEI_INCREMENTAL_EQUIPMENT_SOURCE_AUDIT_v1.md) are exact-SHA verified by the original [PtXFlex L3-A 2023 wholesale-only handoff](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/L3_A_2023_ORIGINAL_E_ES_FINANCIAL_HANDOFF_AND_SCOPE_STOP_v1.md). PtXLens [fully implemented incremental **real 2023 EUR** source-wholesale-only DCF](https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/src/ptxlens/l3a_source_wholesale_dcf.py) calculates zero-NPV maximum **hypothetical initial all-in incremental CAPEX**, annual extra OPEX break-even, EOY replacement/salvage and future source-benefit persistence scenarios; [full methods, source tests, results and FOUR reproducible scientific SVG sensitivity figures](https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/docs/L3_A_2023_MATCHED_SERVICE_WHOLESALE_DCF_BREAKEVEN_METHODS_RESULTS_v1.md).

Original model's **2023 net WHOLSALE GRID cost difference** E−E+S: **€1,124,332.269/year** for gross H₂ inventory (16,268,755.001kg annual modelled common-hourly H₂), **€1,103,463.729/year** for *different* usable-service interpretation (16,331,558.946kg). Both still fail original 18.25mkg complete industrial demand. At a wholly **illustrative** future 20-year horizon, 8% REAL rate, multiplier 1 on 2023 annual source saving repeated (NOT a future market price forecast), and **optimistically ZERO extra station OPEX or replacement**, the upper mathematical *all-in extra initial installed CAPEX ceiling* is **€11.03886m** gross or **€10.83397m** usable. In a separately *invented as a stated stress parameter*, not vendor-sourced, **€250k annual extra OPEX + €1m end-year-10 replacement** scenario the corresponding ceilings are **€8.12113m** gross or **€7.91624m** usable. [Exact source-registered full annual cashflow grid](https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/data/results/L3_A_2023_matched_hour_source_only_wholesale_savings_DCF_CAPEX_OPEX_frontiers_NOT_full_LCOH.json) and [compact cross-repo result SHA](https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/data/results/L3_A_2023_same_service_2023_wholesale_DCF_break_even_summary_NOT_final_project.json) are committed identically to both repositories. [L3-A plot and DCF original-source CI passed](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43588108224); [PtXFlex original 2023 H₂/equipment/wholesale handoff CI passed](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43587841285). The four vector SVGs are **bitwise deterministic** with pinned Matplotlib/Numpy and graph SHA regression.

**Strict limitations:** these are only *conditional theoretical budget ceilings*, **NOT actual manufacturer installed bank/storage costs or financial viability**. There are no actual vendor prices, BoP/compressor/cooling costs, verified operating life/failure/replacement schedules, site, real future hourly price/wind reoptimization, tax/financing/depreciation/insurance, full original industrial H₂ contract, or native full BAFU manufacturing GWP. Nor can the *different* gross and usable hourly services be cross-compared as one functional unit. Original market conditions are **not a 2026–2050 price forecast**. **L3-A numerical subgate PASSED, full L3/F2/L1/L2/P0/hydrogen/methanol scientific v1.0 NOT PASSED.** [ADR-015 and master plan](docs/DECISION_REGISTER_v1.0.md) updated, PR remains DRAFT.

---

## 14 November 2026 — F2/L1 stationary Type I 20t→40t equipment mass and LCI source audit (PRELIMINARY SUBGATE ONLY)

New original 2023 F3-C SHA-linked [physically screened 313K Type I incremental station equipment scope](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F2_L1_STATIONARY_TYPEI_INCREMENTAL_EQUIPMENT_SOURCE_AUDIT_v1.md): peer-reviewed IJHE 200bar 1.8m³/2,400kg **EMPTY EQUIPMENT** reference at 20bar(a) withdrawal requires **803 E /1605 E+S** gross inventory or **902 E /1804 E+S** usable, hence **802/902 additional vessels** of **1,924,800kg /2,164,800kg EMPTY reference vessel equipment** at 313K. Not tonnes of virgin steel or complete installed station weight. [F2 dedicated CI successful](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43583202468) and [PtXLens SHA-linked independent equipment/LCI source gate](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43583583937) both passed. The 19-category ledger identifies **18 unquantified equipment scope classes** (rack, manifold, gas quality, pressure relief, compressor, cooling, instruments, foundations, inspection, EOL etc.) as NULL, not zero.

**Real manufacturers separately audited:** heiserTEC COSMOS **Stationary PED** nominal 210bar 36×87L 49kg gas/module, but **stationary module EMPTY mass unknown**; 935kg empty COSMOS **Mobile TPED** does not transfer to stationary. Independently, [heiserTEC Type I H₂ PED 50L 330bar catalogue](https://www.heisertec.com/products/type-1/) provides **85.5kg empty per cylinder**; 200bar(a)/313K *hypothetical gas fill screen* would require extra **28,878/32,468 individual cylinders** or **2,469,069kg/2,776,014kg empty cylinder hardware** (gross/usable). This is a **different 330bar-rated cylinder geometry**, not a vendor-certified substitute for the IJHE 200bar 1.8m³ vessel or the 210bar stationary bundle; no pressure/tank fatigue or frame/installed mass approval. [OEM source CI successful](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43583991352), [PtXLens independent OEM CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43584237526).

[NEN-EN 17533:2025](https://www.nen.nl/en/nen-en-17533-2025-en-338598) is a *published* Dutch stationary compressed hydrogen cylinder/tube standard, **not** a certification for complete manifolded assemblies/external pipes. EIGA 247/24, EU PED and industrial H₂ compressor family source scopes recorded. [OEM + standards research registers](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/research/F2_L1_STATIONARY_TYPEI_OEM_AND_STANDARDS_SOURCE_REGISTER_v1.json), [manufacturer's independently weighted cylinder register](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/research/F2_L1_INDEPENDENT_OEM_PED_50L_330BAR_H2_CYLINDER_AND_EN17533_SOURCE_v1.json), and [technical OEM RFI prepared but NOT SENT](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F2_L1_STATIONARY_H2_VENDOR_RFI_AND_BOM_DATA_REQUIREMENTS_v1.md).

**Strict limits:** source vessel *empty equipment* is NOT native material input; original BAFU 2026 vehicle composite hydrogen tank provider per kg **stored hydrogen capacity** incompatible with stationary steel mass. Actual station site, bank/P&ID, steel grade/forging, installed rack/manifold/compression/cooler, capital/maintenance, native provider-linked BAFU full LCIA and discounted whole-system cost all missing. The existing 2023 F3-C €1.10–1.12m lower modelled *net wholesale settlement* is **NOT a net project benefit or LCOH**. Private recovered P0 archives absent. **F2 and L1 total gates and full v1.0 remain NOT PASSED.**

---

## 14 November 2026 — F3-C independently verified exact-hour source-2023 physically screened E/E+S operations

The [PtXFlex original-source 8,760h physically screened common-service F3-C](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F3_C_2023_PHYSICAL_COMMON_HOURLY_SERVICE_VERIFIED.md) is now **successfully numerically solved** in all four 20t E / 40t E+S MILPs. The hourly H₂ target is built from the 2023 E historical **modelled delivered reference minus a particular feasible E source-pressure Stage A shortfall**, not from the original full industrial contract and not a globally proven maximum-service schedule. Each pair uses identical original 2023 E/ES wind/NL A44 market input, fully source-locked original E/ES archive hashes, and a SHA-locked **same 8,760-hour** H₂ delivery profile within the independent gross/usable inventory interpretation, using source-model Type I 200bar(a), 20bar(a) minimum and compressor electrical assumptions. [Our independent LCI/TEA intake gate](src/ptxlens/f3c_common_service_bridge.py), [SHA-frozen paired data](data/results/F3_C_2023_source_real_gas_equal_H2_hour_E_vs_ES_Lens_operational_bridge.json), [methodological scientific report](docs/F3_C_INDEPENDENT_MATCHED_SERVICE_SOURCE_LCIA_TEA_STOP.md) and [successful original-source consumer CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43580637209) establish:

**Gross 20t/40t:** 16,268,755.001 kg/year *identical hourly H₂*; E+S **€1,124,332.269 lower modelled 2023 NET WHOLESALE electricity settlement**, guaranteed within the reported HiGHS cost bound interval €1,124,318.034–€1,124,348.115. **Usable 20t/40t:** 16,331,558.946 kg/year same-hour service; **€1,103,463.729 lower settlement** (interval €1,103,461.954–€1,103,474.625). **These are different service quantities, not cost-comparable across modes.** Original full-demand shortfall persists at 1,981,244.999 or 1,918,441.054 kg/year respectively.

This benchmark is **not** an assertion that additional 20t steel vessel hardware pays back, is lower in cradle-to-gate CO₂e, is cheaper on total lifetime costs, or satisfies the original 18.25mkg demand. The source 200bar storage/compressor is a **screened engineering model**, not a buildable authenticated supplier BOM/validated site. Stationary steel vessel manufacturing, compression/cooling station/BoP, operations, replacements, installed CAPEX, native complete BAFU v1.1 LCI, full discounted cost/financing and independent review are outstanding. **F3-C operational maths subgate verified; P0/F3 full and L1/L2/L3 and hydrogen/methanol v1.0 release NOT PASSED.**

---

## 14 November 2026 — F3 source-verified hourly H₂ and prospective backup-LCIA admissibility

**Further official-source H₂ contract correction (14 Nov):** [PyNEXUS original annual YAML](https://github.com/abhijith-sivaprasadan/PyNEXUS/blob/main/configs/annual.yaml) confirms 52.5°N,3.5°E is offshore ERA5 **wind data location, not an industrial hydrogen delivery site**. [Hynetwork Exit Terms 2026 clause 2.1.2](https://www.hynetwork.nl/sites/hynetwork/files/2026-07/general-terms-and-conditions-connection-exit.pdf) expressly exclude merchant supply of gas; signed **exit/transport CDS** and separately purchased **H₂ molecules/shipper nominations** are distinct. [Exit Annex 12](https://www.hynetwork.nl/sites/hynetwork/files/2026-07/general-terms-and-conditions-connection-exit-annex-12-pressure-specification.pdf) permits an individually specified reduced fixed customer pressure. [Source-verified 8,760-hour capacity/pressure/quality/availability boundary tests](data/results/F3_2023_shortage_2026_HNS_exit_and_supplier_boundary_control.json) and [strict PtXLens bridge](src/ptxlens/f3_hns_exit_supplier_bridge.py) confirm **no actual 2023 source or 2026 customer site exists for this study**, even when **synthetic perfect supply** mathematically fills the deficit. HNS CSA reference 39.321kWh/kg HHV gives modelled *incremental* peaks **40.46 or 7.22MW HHV**, not a total booked connection. [Full LCIA and DCF stop](docs/F3_HNS_EXIT_VS_SUPPLIER_LCI_AND_DCF_STOP_v1.md), [source register](research/f3_h2_exit_and_supplier_source_evidence_v1.json), [two distinct nonbinding enquiries drafted, unsent](docs/F3_TWO_CONTRACT_INFORMATIONAL_OUTREACH_DRAFT_v1.md). **No native whole-plant GWP/LCOH result.**

**P0 checked on 14 Nov:** [live GitHub original artifact metadata](research/P0_2023_PyNEXUS_original_actions_artifacts_live_status_2026-11-14.json) verifies historical E, E+S and A44 ZIPs currently **available**; earliest expiry **24 December 2026 19:24:29 UTC** (A44). This is not escrow; no verified private long-term archival recovery and licence clearance. **P0 and both coordinated v1 release gates still NOT PASSED.**

**Reconciled physical source result:** original historical E 2023 *modelled* H₂ delivery was 16,335,279.317 kg/year, below the original 18,250,000 kg demand. After Type I 200bar source physics, the 20t E configuration has **proven positive minimum additional shortage** of 65,860.378–66,524.317 kg (gross stock) or 3,718.744–3,720.371 kg (usable stock), while E+S 40t has **verified zero additional shortage** under both capacity interpretations ([upstream six-artifact verification](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43526250517)). Therefore **E/E+S physically screened hourly service is unmatched**; even valid scoped native BAFU E/E+S results cannot be misrepresented as full comparative plant GWP or LCOH.

**Source-derived hours, not invented supply:** verified [gross 176-hour nonzero H₂ top-up source profile](data/results/F3_2023_original_E_sparse_H2_backup_need_max_inventory.json) and [usable 91-hour profile](data/results/F3_2023_original_E_sparse_H2_backup_need_usable_service.json) are archived in both repos with identical hash fingerprints. See [cross-repo prospective physical backup source register](research/f3_backup_physical_source_register_v1.json), [source-based route comparison](data/results/F3_2023_2026_prospective_h2_delivery_architecture.json), [physical supply release blocker code](src/ptxlens/f3_physical_supply_gate.py) and [LCA/TEA methodological requirements](docs/F3_EXTERNAL_H2_SERVICE_LCIA_TEA_ADMISSIBILITY.md). A 2026 Dutch pipeline operator network entry pressure range is **not** an actual site exit-pressure contract or historical 2023 supply. An original 2023 source + future 2026 supply is a prospective model, not observed plant operation.

**Outstanding L1/L2/L3 and P0 gates:** actual NL site and H₂ supplier contract, delivered pressure/quality, firm hourly flows and backup operation, source-matched Type I steel/pressure station manufacturing, compressor/cooling, direct native BAFU v1.1 storage+backup LCIA, full lifetime EUR DCF, and verified long-term original-source private escrow. [Supplier/connection/BOM evidence request](docs/F3_H2_SUPPLIER_SITE_CONNECTION_AND_BOM_RFI_v1.md) is prepared but **not sent**. Costs and GWP for unsupported components remain **null, not zero**; neither H₂ core v1.0 nor methanol v1.0 is releasable, PR is DRAFT ([research gates](research/gates-v1.0.json)).

---

**Physical feasibility gate for native storage LCA:** [actual 2023 PtXFlex 200bar Type I EOS/energy screened study](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43514524449) found original E 20t physically screened source-case infeasibility for the same hourly H₂ service, while E+S 40t passes the chosen source screening. PtXLens now holds a [source-SHA-verified pressure evidence bridge](data/results/F3_2023_original_pressure_screen_PtXLens_L1_source_bridge.json) with [scientific unit/claim validation](src/ptxlens/l1_pressure_source_bridge.py) rejecting invented E costs, H₂-to-empty-vessel mass substitution and unsourced native GWP. Neither a whole-plant E-vs-E+S comparison nor v1.0 release is yet eligible.

### 13 November 2026: original BAFU storage-supplier functional-unit correction

**A major LCA mismatch was found in the genuine BAFU:2026 v1 source XML.** The process \`High pressure hydrogen storage tank\` (UUID \`b4739ad2-aa38-368d-8ada-63f5417c8b55\`) is a **vehicle composite tank** described per **kg hydrogen capacity**, with >10 kg raw composite/metal inputs per reference unit despite the exported generic unit \`kg\`. It is **not** a valid per-kg empty Type I stationary steel-vessel manufacturing provider. [Source-unit and technology audit](docs/L1_BAFU_STATIONARY_H2_TANK_PROVIDER_UNIT_AUDIT.md) · [derived source evidence](data/results/BAFU2026_v1_storage_tank_source_unit_mismatch_audit.json). The native BAFU v1.1 equivalent must still be verified; no new tank impact has been silently assigned or added as zero.

**Upstream matched-service operations:** PtXFlex independently solved 2023 **8,760-hour identical hourly E-delivered hydrogen** scenarios, with ideal storage wholesale cost €25.7489m (E) vs €24.6070m (E+S), but **the physically additional 20t storage construction, compressor/cooling, and full original daily demand are not included**. [F3 verified ideal pilot report](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F3_2023_MATCHED_H2_IDEAL_PILOT_VERIFIED.md). This does **not** update or supersede the two earlier incomplete native BAFU scores.



## Coordinated scientific v1.0 — adopted research programme

**Start here:** [shared v1.0 master plan](docs/PROGRAMME_MASTER_PLAN_v1.0.md) · [scientific decisions and change control](docs/DECISION_REGISTER_v1.0.md) · [12-WP release evidence status](research/gates-v1.0.json) · [versioned shared exchange schema](contracts/ptx-exchange-v1.schema.json) (byte-identical with PtXFlex).

**Existing native source evidence preserved:** [real BAFU:2026 v1.1 E/E+S native LCIA](docs/BAFU_2026_V11_NATIVE_2023_DUTCH_E_ES_VERIFIED.md) with original 2023 PyNEXUS modelled H₂ and native 30bar PEM reference. E=**6.148174395784**, E+S=**6.0765526538929** kg CO₂e/kg modelled delivered H₂ under a **scoped reference** that omits additional E+S storage equipment/compression and uses different delivered service. **Not** a complete matched-service comparison. [PtXFlex F1 audited source](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43497912940) and [F2 preliminary CoolProp physics](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43498612013) will provide the pressure/working-inventory evidence.

**Release gate:** the actual 20t→40t equipment inventory, storage pressure/usable mass and operational loss/compression must be sourced before we re-run BAFU whole-plant GWP. Full H₂ discounted cost needs complete EU plant CAPEX/OPEX and matched delivery; capital-only OpenPyTEA is not LCOH. Methanol must pass a separate CO₂/product-gate method. [Storage-LCA task](https://github.com/Open-Energy-Methods/PtXLens/issues/6) · [methanol product LCA task](https://github.com/Open-Energy-Methods/PtXLens/issues/7).



## Latest scientific result — genuine native BAFU:2026 v1.1 30-bar PEM E/E+S GWP100

Using the **user-provided real BAFU v1.1 native openLCA database**, the actual GreenDelta openLCA 2.7 Java engine and UMFPACK sparse solver have now produced independently checked **IPCC 2021 / IPCC 2021 GWP 100** results from native, closed supplier process systems:

| Native BAFU v1.1, kgCO₂e/kg H₂ | GWP100 | Linked processes | Unlinked product/waste exchanges |
|---|---:|---:|---:|
| Original Swiss 30-bar PEM reference | **5.541965562** | 4,235 | 0 / 0 |
| **E**, original 2023 NL-model electricity reparameterization | **6.148174396** | 4,240 | 0 / 0 |
| **E+S**, original 2023 NL-model electricity reparameterization | **6.076552654** | 4,240 | 0 / 0 |

All native results agree with independent source-factor reconstructions using the uploaded **corrected BAFU v1** LCIA to within ~2.2×10⁻⁸ kgCO₂e/kg H₂. Original data: 2023 PyNEXUS real observed NL market and ERA5-derived wind inputs, with **modelled (not metered) hydrogen operation**. The raw licensed BAFU v1.1 database and v1 source files remain **outside GitHub**.

**Crucial scope restriction:** E+S has **20,000 kg additional configured hydrogen storage capacity** (40,000 vs E 20,000 kg), but a validated *physical* storage vessel, compressor, losses and extra infrastructure inventory is **not included**. The BAFU offshore-wind reference is an old 2MW "xx" process and E/E+S H₂ delivery differs. These are genuine native GWP100 results for **scoped BAFU-reference 30-bar PEM systems with source-grounded Dutch electricity/water substitutions**, not a completed matched-service industrial E vs E+S cradle-to-gate comparison. **Do not present E+S as environmentally superior from the intensity difference alone.**

[Full reproducible source and native calculation methodology](docs/BAFU_2026_V11_NATIVE_2023_DUTCH_E_ES_VERIFIED.md) · [Remaining equipment/service gates](https://github.com/Open-Energy-Methods/PtXLens/issues/2)



## BAFU:2026 — Swiss official full GWP100 process catalogue and Dutch original E/E+S work

The **official Swiss Federal Office for the Environment (BAFU:2026 v1) public API** has been queried live for all **11,947 real process-reference IPCC 2021 GWP100 results** over 16 complete UUID partitions. Records include exact source UUIDs, names, country, units, edition and source provenance. [Successful full source ingest](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43441882303).

Using frozen original 8,760-hour PyNEXUS E and E+S dispatch ZIPs, we executed a second independent **BAFU-published-factor electricity-supply component sensitivity**, with source-verified NL high-voltage grid and legacy offshore-wind factors: **5.522554 (E)** and **5.455317 (E+S)** kgCO2e/kg modelled delivered H2. Four of the eight published PEM stack material categories also have source-matched mass-based BAFU reference factors, resulting in strictly **partial material components** only (0.002613 and 0.002559 kgCO2e/kg model H2). Titanium metal production, virgin activated carbon, Nafion precursor, and iridium-bearing concentrate **do not have technology-equivalent verified suppliers**; they were never given zero GWP. [Successful original data CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43443319012).

**These are NOT complete H2 cradle-to-gate LCA results.** The official API exposes pre-calculated BAFU process impact factors, not the native process supplier graph. **Historical preliminary stage:** the BAFU:2026 original native v1.1 zolca was subsequently supplied with user authorization and executed locally; see the latest section above. The local source-archive verifier and the real openLCA 2.7 native BAFU import, supplier graph checks and numerical calculations have since all executed successfully on the authorized v1.1 copy. [Exact source, 30bar PEM benchmark references, methods, limitations and local execution](docs/BAFU_2026_REAL_SOURCE_AND_NATIVE_INTEGRATION.md).



## Native openLCA 2.7.0 engine actually executed

GreenDelta's genuine openLCA **2.7.0** native Java engine has imported the unmodified SHA-verified Federal Commons Merged (2026) ZIP, constructed the real USLCI reference PEM product system (2,516 source processes, 3,077 linked supply exchanges) and run its native IPCC AR6-100 LCIA calculation. [Successful Java kernel run](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43435190584).

**This is an executed diagnostic, NOT a complete or valid Dutch cradle-to-gate footprint**: native auto-linking still leaves **681 nonzero product inputs unlinked**, and the original 2017 U.S. process has a source oxygen-output mass-balance discrepancy (12 kg O2 plus 1 kg H2 out versus 9 kg water in). Its diagnostic 77.616 kg CO2e/kg reference H2 is **not** an approved research finding. An additional real-data Hybrid (USEEIO v2) import reduces original source default-provider gaps only from 695 to 672 and introduces monetary IO assumptions.

Read [complete native execution, IPCC method and supplier-validation evidence](docs/NATIVE_OPENLCA_DIAGNOSTIC_AND_FULL_LCA_GATES.md). No fake GWP coefficients or generic missing-provider=zero treatment are accepted as a completed PtXLens study.


## Commons Merged real-background audit — November 2026

The **authentic Federal LCA Commons Merged 2026 openLCA JSON-LD archive** (51,012,635 bytes, SHA256 `1ded185617d4de67f8ed6933c473a68d65c232dd738779179e8559a31dfd056d`) is now reproducibly downloadable without an API key. The actual 1 kg PEM-hydrogen USLCI unit process and IPCC **AR6-100 method with 134 matching characterization-flow references** were identified. The exact supplier graph still has **695 unresolved upstream input exchanges (683 without any same-flow output supplier; 12 with candidate suppliers requiring review)**, including deionized water and PEM-stack precursor flows. **This earlier Commons-only LCA had unresolved links**; subsequently the legitimate BAFU v1.1 native model was obtained and executed with zero unlinked product/waste exchanges (see current BAFU section).

Read [the actual background database / missing-provider research audit](docs/COMMONS_MERGED_2026_PROVIDER_AUDIT.md). [Source acquisition and provider graph CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43432287400).


**Research status (13 Nov 2026): real-source native BAFU v1.1 provider-linked reference and scoped Dutch E/E+S IPCC GWP100 calculations completed, original model provenance audited; full matched-service E/E+S storage-equipment cradle-to-gate comparison and complete LCOH not yet completed.** The original source PyNEXUS model is unchanged.

## Executed work, not mock data

| Gate | Status | Evidence |
|---|---|---|
| Dutch 2023 A44 wholesale price, 8760 real UTC hours | **Passed** | [live Fraunhofer/SMARD API CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43417523516) |
| Frozen PyNEXUS 2023 E and E+S archives, 17520 Stage B hours | **Passed** | [original ZIP re-download, hashes and numerical audit](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43418772493) |
| OpenPyTEA 3.2.2 + DOE 2024-source 2022-USD electrolyser installed CAPEX | **Passed: capital only** | [real OpenPyTEA execution + independently reconstructed cashflows](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43418299360) |
| 2023 Dutch energy-supply GWP (historical dispatch, sourced lifecycle factors) | **Passed — electricity supply only** | [real-data LCA results & methods](docs/LCA_2023_METHODS_RESULTS.md), [17,520-hour CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43424086998) |
| Published PEM 1MW stack materials foreground + declared model allocation | **Passed — LCI only** | [1MW stack 2024 thesis source](data/lci/pem_stack_kanz_2024_1mw.json), [CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43425080024) |
| Native openLCA provider-linked BAFU v1.1 reference, E and E+S 30bar PEM GWP100 | **Passed — scoped native LCA** | [actual calculations and limitations](docs/BAFU_2026_V11_NATIVE_2023_DUTCH_E_ES_VERIFIED.md); complete additional storage/compression and matched-service comparison still pending |
| Complete, comparable and source-normalized hydrogen LCOH | **Blocked** | wind, storage, grid tariffs, complete OPEX, currency-year and project-service boundary |
| Full life-cycle-emissions-constrained MILP / Pareto front | **Not yet demonstrated** | Future verified frontier work |

Actual OpenPyTEA 2022-USD **electrolyser capital-only** results in the published $2000/kW installed cost case and a separate *analyst* 8% rate are **$1.55815/kg** (E) and **$1.52603/kg** (E+S). The scenarios have *different* delivered H2. These costs **exclude** electricity, storage and other plant components; they are **not LCOH**. DOE system electricity consumption and the simplified PyNEXUS electrolyser performance are distinct technology assumptions.

The 2023 source-based electricity-supply GWP is **6.74243** (E) and **6.65815** (E+S) kgCO2e/kg *modelled* delivered H2, based on official Dutch 2023 grid and UNECE offshore-wind reference factors; it is **not** a complete H2 product LCA or native openLCA calculation. [Exact methodology, scope, source citations, hourly audit and omissions](docs/LCA_2023_METHODS_RESULTS.md).

Read [real-source detailed evidence and acceptance gates](docs/REAL_DATA_EVIDENCE.md).

## Reproduce using original, external data

~~~bash
python -m pip install -e ".[dev]"
python -m pytest -q

# Fetch actual 2023 Dutch observed price via licensed live API
ptxlens fetch-nl-prices --year 2023 \
  --csv outputs/nl_2023_prices.csv --manifest outputs/nl_2023_manifest.json

# Download original E and E+S ZIPs from their registered source GitHub Actions
ptxlens pynexus-compare /path/to/original_E.zip /path/to/original_ES.zip \
  --output outputs/2023_observed_comparison.json

# Published DOE-case capital-only accounting, never a full LCOH
ptxlens doe-capital /path/to/original_E.zip \
  --installed-cost-usd2022-kw 2000 --real-discount-rate 0.08
~~~

The GitHub Actions workflows perform these real-source retrievals automatically and preserve reproducibility artifacts. No GitHub token is committed. Historical data licences and source attribution remain in force.

OpenPyTEA executes in separate CI against the SHA-pinned original-source **derived register**. The executable source is [src/ptxlens/openpytea_doe.py](src/ptxlens/openpytea_doe.py), with matching independently audited present-value cashflows; [original source register](data/source_registry/pynexus_wp5_2023.json).

**Native openLCA LCIA is now executed:** the authorized BAFU v1.1 process database and exact `IPCC 2021 GWP 100` method produced the reference and E/E+S scoped numerical results above, with zero unlinked product/waste exchanges. [Older IPC procedure](docs/OPENLCA_EXECUTION.md) remains available; native Java execution was used here to solve the large matrix with the real UMFPACK sparse solver. Full plant-specific storage/compression and matched-service physical boundaries remain unresolved.

## Scope and safety

- External history: actual 2023 ERA5-derived wind and NL ENTSO-E/SMARD electricity prices; simulated hydrogen dispatch and delivery, not actual equipment telemetry.
- Published DOE CAPEX benchmarks: **2022 USD**. Dutch settlement: **2023 EUR**. Do not sum or compare without sourced FX/price-year harmonization.
- Users can execute the original four-hour invented fixture under examples/ to test arithmetic only. It is **not a scientific research dataset**, and tests must never be presented as findings.
- No restricted LCI/economic database included; exact EXIOBASE 3.8 versus 3.9+ licence differs. OpenLCA process providers and database licences require separate review.
- No full LCA, industrial validation, ISO 14044 conformity, industrially validated investment decision, or commercial process simulator use claimed.
- AI-assisted implementation with independent numerical checks and necessary scientific review.

Related: [PtXFlex](https://github.com/Open-Energy-Methods/PtXFlex), an independently gated e-methanol MILP with separate original historical-market/wind input ingestion.
