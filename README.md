# PtXLens — source-verified Power-to-X economics and environmental assessment

## 14 November 2026 — F3 source-verified hourly H₂ and prospective backup-LCIA admissibility

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
