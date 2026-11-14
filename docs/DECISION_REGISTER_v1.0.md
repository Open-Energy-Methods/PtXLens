# PtX Research Programme v1.0 — engineering decisions and change control

**Programme:** OEM-PTX-2026-01 · **Effective:** 2026-11-13  
**Canonical companion:** [PROGRAMME_MASTER_PLAN_v1.0.md](PROGRAMME_MASTER_PLAN_v1.0.md)  
**Decision requirement:** Every new numerical source/technology assumption and every goal/scope change gets an ADR entry *before* scientific results are issued. Existing actual source observations cannot be altered by an ADR.

## ADR-001 — Two different functional units and system boundaries

**Status:** ACCEPTED · **Decision:** hydrogen comparison reports *kg H₂ delivered at common named pressure, composition, time/demand/reliability gate*; methanol comparison reports *kg saleable methanol at defined product gate*. Use separate native LCAs and discounted cash-flow denominators.

**Why:** electricity-to-H₂ output and methanol-at-gate do not provide interchangeable service; raw impacts per kg cannot be compared directly. Alternative rejected: multiply H₂ impact by stoichiometric 0.1888 kg H₂/kg MeOH and call that full methanol LCA; that omits CO₂ sourcing, synthesis, losses and plant manufacture.

**Evidence / falsification:** [ISO 14040](https://www.iso.org/standard/37456.html), [ISO 14044](https://www.iso.org/standard/38498.html); unit tests must reject H2-to-MeOH functional unit substitution.

**Reopen if:** gate requirements or delivered pressure/purity documented differently from frozen source.

## ADR-002 — Preserve original PyNEXUS, do not reinterpret modeled H₂ as observation

**Status:** ACCEPTED · **Decision:** use the source-frozen October 2026 2023 E and E+S ZIPs with exact registered hashes, independent 8,760-hour checks and preserved UTC assumption. Market is observed from NL A44; wind availability is ERA5-derived, while H2 dispatch is a *numerical model*.

**Why:** Frozen upstream protects reproducibility and prevents retuning benchmark "evidence" to a new result. Rejected: change the original repository's storage model and replace its historical CI artifacts.

**Evidence:** [PtXLens frozen original source registry](https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/data/source_registry/pynexus_wp5_2023.json). Original source ZIPs expire 24 Dec 2026; a legitimate non-redistributing preservation record is required.

**Reopen if:** original provider XML contradicts source UTC alignment; document correction instead of altering original raw bytes.

## ADR-003 — Baseline shared 2023 service is 50,000 kg H₂/day *candidate*, not a presumed success

**Status:** CONDITIONALLY ACCEPTED, PENDING F1 verification · **Decision:** verify original hourly H₂ demand implied by annual 18.25 Mt input target (18,250 tonnes = 18,250,000 kg/yr). Fix one common hourly demand, delivery pressure/purity, reliability criterion, terminal storage condition and lifetime for E and E+S, before optimization.

**Why:** actual original 2023 modeled delivery differs: E ~16.335 Mt and E+S ~16.679 Mt. Comparing their per-kg footprint cannot establish matched-service superiority. Alternative "normalize every annual total by 18.25 Mt" rejected because it hides unmet physical demand.

**Reopen if:** frozen hourly demand differs from nominal 50,000 kg/day or product gate is unspecified. Require infeasibility reporting or identical sourced fallback instead of asymmetric relaxing constraints.

## ADR-004 — No fixed 200-bar storage design until duty is known

**Status:** OPEN FOR FINAL TECHNOLOGY CHOICE; ORIGINAL SOURCE STORAGE SEMANTICS VERIFIED · **Original source:** both SHA-verified PyNEXUS configurations and `optimization/dispatch.py` show 20/40t are the MAXIMUM MODELLED H₂ STOCK STATE, with common 10t initial/terminal and 30bar PEM / 20bar delivery; this is NOT usable pressurized gas. Published Table 2 vessel screening using CoolProp 8 finds very different working gas/heel and per-vessel equipment masses across Type I–IV. See [F2 source audit](F2_PUBLISHED_STORAGE_PRESSURE_SWING_AUDIT.md). **Next decisions:** confirm source vessel pressure basis, real usable inventory, temperature/pressure duty and actual installation before choosing Type I/II/III/IV.

**Previous unresolved study framing:** determine whether H₂ storage nominal 20/40t refers to usable or maximum contents; establish PEM outlet and product-delivery pressure, minimum working vessel pressure, temperature range, operating cycles and model duty first. Then compare candidate 30/200/350 bar, steel/composite, real-gas volume and BOM.

**Why:** available storage *mass* is not vessel material mass; vessel pressure affects compressor power, temperature limits, usable volume and equipment GWP/TEA. "200-bar steel baseline" is a candidate, not a chosen engineering result.

**Source methods:** [CoolProp Hydrogen EOS](https://coolprop.org/fluid_properties/fluids/Hydrogen.html), [2026 comparative stationary storage vessel table](https://doi.org/10.1016/j.ijhydene.2025.152849), [DOE/ANL HDSAM](https://hdsam.es.anl.gov/index.php?content=hdsam). Any chosen vessel type requires reference design specs, mass, unit and pressure rating.

**Reopen if:** physical pressure requirement or source vessel design differs materially.

## ADR-005 — One authoritative engineering mass/energy model

**Status:** ACCEPTED · **Decision:** PtXFlex owns H₂/pressure/energy/process operational equations and emits an evidence-bearing equipment BOM; PtXLens does not implement a second, conflicting physics calculator. PtXLens independently verifies the exported ledger and connects it to native BAFU processes.

**Why:** two independently evolving storage assumptions would compromise claimed environmental differences. Independent analytic/EOS reference checks remain desirable but use separate *verification calculations*, not diverging production models.

## ADR-006 — Primary GWP method is native BAFU v1.1 / IPCC 2021 GWP 100

**Status:** ACCEPTED FOR SCOPED REFERENCE; PENDING COMPLETE STORAGE LCIA · **Decision:** use the user's authorized BAFU:2026 v1.1 private inventory; actual native GreenDelta openLCA 2.7 engine with exact category. Its Swiss original 30bar reference and E/E+S scoped annual source-input calculations already executed and independently checked. Use original corrected BAFU v1 impact workbook only for *independent* cross-checks, never assume BAFU v1=v1.1.

**Why:** prior Federal Commons graph had many missing suppliers and a physically questionable reference; native BAFU v1.1 closes its reference process supplier graph. Rejected: add precharacterized per-material BAFU API values to a fully linked native inventory and double count manufacturing.

**BAFU actual supplier source warning:** original BAFU v1 process b4739ad2-aa38-368d-8ada-63f5417c8b55 `High pressure hydrogen storage tank` is a **road vehicle composite tank** source described *per kg hydrogen capacity* though its reference unit is simply `kg`. The recipe includes 7.14kg woven carbon fibre and 3.06kg epoxy per source unit plus metals, total 12.6kg materials. It is **NOT a source for kg empty steel tank manufacture**. Its native v1.1 equivalent is not yet independently inspected, so no source tank GWP is added. See [PtXLens original licensed source audit](https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/docs/L1_BAFU_STATIONARY_H2_TANK_PROVIDER_UNIT_AUDIT.md).

**Reference results, not matched-service conclusion:** 5.541965561665505 CH reference; 6.148174395784 E; 6.0765526538929 E+S kgCO₂e/kg modeled H₂. Added E+S 20t vessel, compression and operational losses not included. [Authoritative scientific report](https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/docs/BAFU_2026_V11_NATIVE_2023_DUTCH_E_ES_VERIFIED.md).

**Reopen if:** process provider IDs/elementary flow characterization fail completeness review, source method changed or physical storage inventory requires an alternative impact method.

## ADR-007 — Real-source quality over convenient model convergence

**Status:** ACCEPTED · **Decision:** no synthetic hourly carbon factors, invented CO₂ feed profiles, equipment masses or cost coefficients can enter real-case evidence or release results. Missing parameters remain \`null\` / BLOCKED with a source action. Tests may use clearly labeled synthetic fixtures and must *reject* physically invalid inputs.

**Why:** an optimizer will always return plausible numbers when supplied invented plausible coefficients; this is not scientific validation.

**Reopen if:** a genuine new source is obtained and its version, page/process UUID, geography, license and uncertainty recorded.

## ADR-008 — Same finance basis and no capital-only LCOH claim

**Status:** ACCEPTED; COMPLETENESS PENDING · **Decision:** PtXLens reports full H₂ discounted life cost only when CAPEX installed system (wind/PEM/store/BoP/compressor), replacement, OPEX, energy contract/tariff and discount/price-year/currency are recorded on one basis. The prior OpenPyTEA 2022-dollar capital-only result is *not* LCOH.

**Sources:** [DOE H2A production](https://www.hydrogen.energy.gov/program-areas/systems-analysis/h2a-analysis/h2a-production), independently executed OpenPyTEA and original project cost context.

**Reopen if:** region/finance/energy contract changes; record FX/inflation and VAT/contract boundaries.

## ADR-009 — Methanol results require CO₂ physical and carbon-accounting boundaries

**Status:** CONDITIONAL PENDING F4/L4 · **Decision:** distinct CO₂ source, purity, availability in time, capture/separation energy, allocation of upstream CO₂, reaction \`CO₂+3H₂→CH₃OH+H₂O\`, recycle/purge, synthesis auxiliaries and product grade are required before a real-data methanol v1.0 claim. Do not treat short-term CO₂ incorporation as permanent negative emissions. Report methanol EOL scenario separately.

**Why:** the existing 4h MILP verifies math only; no external chemistry/CO₂ validation exists.

**Reopen if:** verified continuous CO₂ contract/source data, published process benchmark or industrial measurement becomes available.

## ADR-010 — Uncertainty includes model-form and geographic sensitivity, not just statistical confidence

**Status:** ACCEPTED · **Decision:** label epistemic storage pressure, lifetime, vessel/cost/LCI, 2026 factor vs 2023 mix and CO₂ assumptions separately from historical year-to-year variability. With just 2023 observations, do **not** describe resampling as actual long-term observed risk. Use physically linked scenario ensembles and tipping-point analysis of incremental vessel/energy GWP.

**Why:** 2023 is one correlated weather/market trajectory; hourly points are not independent annual observations. A per-hour bootstrap can erase weather/dispatch correlation.

## ADR-011 — Strict claims and review gate

**Status:** ACCEPTED · **Decision:** a passing CI run proves code and contract tests, not industrial validation, complete attributional LCA, ISO conformity or publicly reviewed environmental superiority. All actual findings carry process scope, source version, uncertainty, limitations and missing-material table.

**Why:** [ISO 14044](https://www.iso.org/standard/38498.html) has explicit LCA reporting and review provisions. Public comparative assertions need appropriate review; prospective v1.0 is not an ISO-certified industrial comparison.

## ADR-012 — Two-repository version contract must be identical

**Status:** ACCEPTED; initial implementation under P1 · **Decision:** canonical \`contracts/ptx-exchange-v1.schema.json\` is mirrored byte-for-byte across PtXFlex/PtXLens, validated by a scientific cross-field gate. Publication rejects null relevant impacts, missing storage BOM, mismatched service profile/hash, methods/functional unit/year or unverified economic terms. Any breaking change increments major contract version and requires an ADR and migration tests.

**Scientific distinction:** The initial implemented schema is a source-verified **annual summary** and rejects false matched-service GWP; an hourly content-addressed flow ledger, full equipment BOM provider list and original pressure/quality evidence remain to be built before the P1 gate can pass. The distinct `matched_operational_service_verified` (physical dispatch comparability) and `matched_service_comparison_eligible` (complete economic/environmental comparability) statuses must not be collapsed. Original E and E+S source wind/price/demand SHA are pinned even though their actual H₂ delivery is unequal.

**Why:** source preservation and exchange semantics, not a shared website dashboard, are v1.0 integration prerequisites.

## ADR-013 — Adopt constructive *reduced* common H₂ service for a pressure-screened 2023 F3-C operating benchmark

**Status:** ACCEPTED AS A NARROW NUMERICAL METHOD (14 November 2026), full F3/L2/L3/P0 and coordinated v1.0 gates **NOT PASSED**. **Registration transparency:** the general requirement to re-optimize both source E/E+S on one physically achievable hourly service was selected in the programme conversation before execution; these detailed numerical inputs, outcome certificates and this ADR wording were recorded **after the source-replayed solver run**. This is not an independently prospective preregistration of the quantitative savings.

**Affected WPs:** F1/F2/F3, L1/L2/L3, P0 and exchange contract P1.

**Problem:** original 2023 E20t cannot reproduce the historic E-delivered hourly reference under Type I 200bar(a), 20bar(a) product withdrawal and source compressor work assumptions, whereas E+S40t has source model zero-additional-shortfall feasible witness. An economic comparison at that unattainable target is invalid. The original modelled 16.335279m kg E reference is already less than 18.25m kg original full demand.

**Decision:** for each capacity semantics separately (`max_inventory`, `usable_service`), create exact 8,760h `d_common,t = d_source,E,delivered,t - shortfall_source,E,StageA-feasible,t`. Obtain the raw 8,760h Stage A H₂ shortage from the original SHA-locked source-derived Stage A GitHub artifact (not merely invented source hours), compare it against source-hash-frozen published sparse positive-hour evidence, and re-optimize source physical E20t and E+S40t with their original matched wind/A44 prices and one fixed modelled H₂ service SHA. Original bank initial/terminal inventory, electrolysis limits/ramp, grid, charge/discharge exclusivity, screened Type I 200bar(a) real-gas EOS inventory and 20bar(a) outlet, source storage losses and reference RVO compressor power remain active. Independently audit 8,760h electricity/H₂/stock/terminal/pressure and net wholesale cost residuals; record separate source cases and original full industrial unmet H₂.

**Alternatives rejected and why:** (a) original ideal H₂-storage cost comparison falsely claims physical E feasibility; (b) annual delivered-H₂-only normalization ignores hourly service and source intertemporal constraints; (c) external hydrogen purchase at unspecified 2023 customer site invents supplier, pressure/purity/GWP/cost and backdates a prospective 2026 network; (d) comparing 20t E gross with 40t usable or claiming common service profiles across capacity interpretations conflates different service quantities; (e) treating Stage A source shortfall incumbent as globally minimum is not supported by its solver's MIP bound interval. The chosen target is **constructively feasible but not proven globally maximum-achievable**.

**Accepted F3-C source numerical evidence:** all four original-2023 8,760-hour MILPs pass independent physical residuals and ≤1e-6 relative MIP gap. Within gross stock interpretation the same-hour H₂ service is **16,268,755.001kg/year** and E+S has **EUR1,124,332.269** lower modelled 2023 *NET WHOLESALE electricity settlement* with deterministic HiGHS bound [**EUR1,124,318.034**, **EUR1,124,348.115**]. Within the separate usable-bank source interpretation the common service is **16,331,558.946kg/year**, with lower settlement **EUR1,103,463.729**, bound [**EUR1,103,461.954**, **EUR1,103,474.625**]. These are not GWP, LCOH, lifetime benefit, industrial plant performance or a full 18.25mkg/year service. Original raw weather and market source files remain privately acquired in CI, not published as this model's new source.

**Verification:** [PtXFlex original source Stage A + E/ES F3-C CI](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43580088115), [PtXLens source-hash independent intake CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43580637209), [F3-C complete auditable method](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F3_C_2023_PHYSICAL_COMMON_HOURLY_SERVICE_VERIFIED.md), derived pair certificate SHA-256 `dddd07d5c0a3d4f276e80af44e28cf3cfdbc93421107fb5d9e39843a0d1d90e2`.

**Remaining critical tests and science stop:** source-hourly service sensitivity to Stage A tie-breaking and full optimum, source hourly weather/market period and price volatility, uncertainty in vessel Type I geometry/EOS temperature and heel, pressure-dependent compressor part-load, station cooling/pipeline losses, 20t additional stationary steel equipment/cost/LCI, lifetime € discounting and native full BAFU:2026 v1.1 comparative LCIA; archival recovery of the original three source ZIPs. No complete L1/L2/L3 output or v1.0 release may be inferred from accepted **wholesale-only source-matched numerical** operations.

**Reopen if:** original 2023 source archive or hourly Stage A hash changes, any state audit/solver MIP bound fails, actual installed vessel technology differs, the research question changes to fulfilling **original full** 18.25mkg demand, or a vendor/source pressure, purity, technology and manufacturing inventory is proven and needs a changed functional unit.

## Decision request template

A new or changed decision must explicitly document:

1. **Problem / affected WP**, primary metric, responsible owner and currently locked assumptions.
2. **Alternatives** including retain current baseline, technical and environmental consequences.
3. **Sources** with exact locator, edition, process UUID and unit/geographic/time relevance; data class O/M/D/L/A/T/V.
4. **Chosen assumption** and uncertainty range, rejected assumptions and reasoning, foreseeable bias.
5. **Code and gate impact**, new residual/negative tests, effect on old results, whether previously claimed conclusions require withdrawal.
6. **Review record:** author, independent reviewer, date, decision status Accepted/Conditional/Open/Superseded and PR links.

**No model feature is implemented or reported as validated solely because it seems physically reasonable.**
