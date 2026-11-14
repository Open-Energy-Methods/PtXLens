# PtXFlex × PtXLens — integrated scientific master plan v1.0

**Programme ID:** OEM-PTX-2026-01  
**Baseline status:** ADOPTED RESEARCH PLAN, **not a claim that v1.0 scientific results exist**  
**Plan version:** 1.0.0 · **Approved as proposed baseline:** 2026-11-13 · **Repositories:** [PtXFlex](https://github.com/Open-Energy-Methods/PtXFlex) and [PtXLens](https://github.com/Open-Energy-Methods/PtXLens)  
**Baseline evidence:** immutable 2023 PyNEXUS model/market/weather artifacts; BAFU:2026 v1.1 native inventory and the independently reproduced corrected v1 impacts; published process engineering and techno-economic data  
**Accountability:** data provenance, physics and optimization verification, product boundary, native LCA and uncertainty, cost methodology and critical interpretation

> **DO NOT CONFLATE:** a published input; observed 2023 market/weather; PyNEXUS-modelled H2 production; user-selected scenario assumptions; independent numerical verification; externally validated physical plant operation; and native BAFU LCIA are six different evidence types. Each output must identify which it uses. Original PyNEXUS remains frozen. No invented measurements, impact factors, vendor costs or industrial validation.

## 14 November 2026 methodological milestone (sub-gate, not revision of v1.0 criteria)

The original 2023 model E 20t pressure-screen failed the original E-delivered hourly H₂ target under two independent bank-inventory interpretations, so a full-service original-target E/E+S cost comparison is inadmissible. To advance **F3-C** without inventing 2023 H₂ purchases, a **source-archived feasible E Stage A** 8,760h shortage is subtracted hour-by-hour from original modelled E-delivered H₂. Both source E20t and E+S40t are independently re-optimized against the same **SHA-registered physically screened *reduced* 8,760h hydrogen service**, within each separate inventory semantics, with original market/wind, Type I 200bar(a), 20bar(a) end withdrawal, compressor power and source inventory. Source SHA, hourly physical residual, MIP gap and provider data legal separation are independent controls. See [ADR-013](DECISION_REGISTER_v1.0.md#adr-013--adopt-constructive-reduced-common-h₂-service-for-a-pressure-screened-2023-f3-c-operating-benchmark), [primary method/results](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F3_C_2023_PHYSICAL_COMMON_HOURLY_SERVICE_VERIFIED.md) and [independent PtXLens bridge](https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/docs/F3_C_INDEPENDENT_MATCHED_SERVICE_SOURCE_LCIA_TEA_STOP.md).

**Subgate F3-C PASSED numerically:** original 2023 source SHA and 8,760h real-gas-screened four MILPs all pass solver gap 1e-6 and independent energy/H₂/pressure/cost audit. Gross mode source exact common annual H₂ service 16,268,755.001kg; E+S modelled **€1,124,332.269** lower **net wholesale grid settlement** with deterministic optimizer bracket [€1,124,318.034; €1,124,348.115]. Usable bank interpretation independent target 16,331,558.946kg; E+S €1,103,463.729 lower modelled settlement with optimizer bracket [€1,103,461.954; €1,103,474.625]. **Do not compare the two modes with different hourly functional services or interpret solver gap bounds as equipment/price uncertainty.** This common service is one **feasible incumbent** and not mathematically proven globally largest; full original 18.25mkg contract remains unmet.

**Remaining programme critical path unchanged:**
- **P0**: private user-controlled lawful permanent source ZIP recovery plus independent second physical backup and source licence. Original GitHub Actions E/ES/A44 source artifacts verified live available on Nov 14 but first expire **24 Dec 2026 19:24:29 UTC**; not archived privately by the programme.
- **F2/L1**: actual buildable manufacturer source Type I bank incremental 20t storage plus associated compressor/cooling/valves/safety, pressure-relevant BOM and audited mass/cost, with relevant geographic inventory.
- **L2/L3**: source-native BAFU 2026 v1.1 life-cycle engineering and complete discounted EUR cash flows matched to the same H₂ pressure/purity/hourly service with uncertainty. 2023 8760h *wholesale* difference is not LCOH or environmental benefit.
- **Scientific review/release**: preserve all missing terms as null/NOT_PASSED, original source modelled H₂ is not metered, 2026 NL network is not a real 2023 supplier. F3 overall, L1, L2, L3, P0, hydrogen and methanol **v1.0 remain blocked** pending accepted evidence.

This record tracks a completed *substudy*, not a relaxation of the original acceptance gates or a new v1.0 product claim.

---

## 14 November 2026 — F2/L1 manufacturer-source mass and installed equipment foreground checkpoint (NOT full v1.0)

The F3-C original-source 8,760-hour pressure-screened equal-H₂-service operational benchmark now has a preliminary **component-by-component installed-capital/LCI engineering handoff**, not a native cradle-to-gate footprint. [ADR-014](DECISION_REGISTER_v1.0.md) explicitly distinguishes original modelled E20t/E+S40t gas stock, real 313K CoolProp pressure-hypothetical Type I storage, peer-reviewed **empty equipment mass** and actual, physically different OEM products.

At modelled **313K, 20→200bar(a)**, IJHE Table 2 Type I steel 1.8m³/2,400kg *reference* requires **+802 vessels /1,924.8t EMPTY equipment** between E20t and E+S40t for original **gross** capacity semantics, or **+902 vessels /2,164.8t** under the distinct **usable** capacity semantics. This is neither material-input tons of virgin steel nor a complete incremental storage station or approved certified design. The real heiserTEC **210bar 36×87L stationary PED COSMOS** module has public gas capacity and frames/manifold concept but **no vendor-published module empty mass**; its **12×50L 935kg mobile TPED** cannot be transferred. Separate [heiserTEC Type I H₂ 50L/330bar PED genuine catalogue per-cylinder empty mass 85.5kg](https://www.heisertec.com/products/type-1/) gives a distinct hypothetical operated-at-200bar(a)/313K reference **+28,878 cylinders /2,469.1t empty cylinder hardware** gross, or **+32,468 /2,776.0t** usable. These are not alternative error bounds for one design nor manufacturer approval to operate 330bar class cylinders on this stationary site. [NEN-EN17533:2025](https://www.nen.nl/en/nen-en-17533-2025-en-338598) is a valid published Dutch stationary cylinder/tube standard but **not for complete assembled manifolds/external piping**; all PED conformity documents, material chemistry, pressure cycling and site details remain unavailable.

The source-audited [19-category equipment requirements ledger](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F2_L1_STATIONARY_TYPEI_INCREMENTAL_EQUIPMENT_SOURCE_AUDIT_v1.md) has **one preliminary known empty reference vessel quantity and 18 completely unquantified physical/lifecycle categories** (compression motor/cooling, racks, valves/pipes, foundations, controls, O&M/EOL etc.) explicitly **null**, not zero. [PtXLens independent environmental provider compatibility stop](https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/docs/L1_STATIONARY_TYPEI_OEM_SOURCE_MANUFACTURING_GWP_GATE_v1.md) prohibits using the original BAFU 2026 *automotive composite H₂ tank per kg H₂ storage capacity* provider as a stationary Type I forged steel-vessel manufacturing process per kg equipment. [Manufacturer-source data requests](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F2_L1_STATIONARY_H2_VENDOR_RFI_AND_BOM_DATA_REQUIREMENTS_v1.md) are drafted but **not sent** and no actual industrial site, supplier contract, commissioned compressor or vendor price exists.

**F2/L1 narrow scope:** peer-reviewed & actual distinct OEM-catalogue source geometry/equipment dry mass calculations and an auditable full equipment-*categories* scope are **verified numerically**, with successful four dedicated original-source/independent PtXLens CI controls. **Remaining original acceptance:** manufacturer/CAD/CE/PED approved complete incremental hardware BOM, pressure and material-source certified plant, native compatible BAFU 2026 v1.1 inventory/GWP, real installed cost and whole-lifetime DCF, physical site, 2023 original H₂ full industrial contract and private P0 independent source archive. All complete F2/L1/L2/L3/P0 and hydrogen/methanol v1.0 gates **NOT PASSED**.

---

## 1. Research charter and preregistered hypotheses

### RQ-H2 — Marginal value of physical hydrogen storage

For 125 MW nominal PEM electrolysis, 2023 Netherlands ERA5-derived offshore wind and observed Dutch electricity prices, what are the **incremental operating cost, equivalent delivered-service emissions, unmet demand, compressor burden, equipment costs and life-cycle impacts** of nominal 20,000 vs 40,000 kg H2 storage? Are gains robust to storage pressure, vessel technology, usable pressure swing, charge/discharge limits, ageing, leakage and system lifetime?

- **H0-H2:** At matched service and common model/physical constraints, the added 20 t of storage does *not* robustly lower both lifecycle GWP and discounted cost; any benefit may depend on excluded infrastructure/energy or model assumptions.
- **H1-H2:** There exists a documented region of the jointly varied operating/technology parameters where increasing H2 storage improves a declared objective, conditional on verified matched service and full marginal equipment/energy burden.
- **Non-claim:** Original E/E+S 6.1481744 vs 6.0765527 kgCO2e/kg differences demonstrate only a scoped electricity/water substitution, not an environmental superiority result; the original two scenarios delivered unequal H2 and omitted incremental E+S storage construction and storage operation.

### RQ-MeOH — What operational flexibility is genuinely available to CO2-to-methanol?

For an explicitly documented 30-bar-H2-to-synthesis interface, source-based CO2 delivery and feed quality, reactor/separation/auxiliary technology and fixed **1 kg qualifying methanol product at the product gate**, how do minimum load, ramp, conversion/recycle, storage and CO2-supply boundaries affect dispatch, price exposure and GWP? What portion of results comes from 2023 observed weather/price, what portion from literature engineering, and what cannot be validated?

- **H0-MeOH:** Ideal stoichiometric fixed-yield assumptions inadequately reproduce a defensible methanol plant once actual auxiliary loads, recycle, CO2 access and operating limitations are included.
- **H1-MeOH:** A source-validated reduced-order process/dispatch formulation can reproduce independently published balances within predefined error tolerances and produce robust, reproducible 2023 scenarios, with sensitivity explicitly distinguishing unobserved CO2 schedule from observed power/weather.
- **Non-claim:** The existing four-hour synthetic MILP is code verification only. It is neither an observed 2023 e-methanol plant nor a validated methanol economics/LCA result.

### Study type and disclosure restrictions

Comparative, prospective **engineering research / scenario LCA and TEA**, not a measured plant study, comparative marketing claim or ISO certification. Follow goal/scope, inventory, impact, interpretation and reporting in [ISO 14040](https://www.iso.org/standard/37456.html) and [ISO 14044](https://www.iso.org/standard/38498.html). Carbon-footprint scope may use [ISO 14067](https://www.iso.org/standard/71206.html) terminology, but **no conformity claim without a documented conformity check and, where required, external critical review**.

## 2. Boundary and functional-unit lock (ADR-001; change-control required)

| Question | Declared reference/denominator | Boundary and time | Never infer |
|---|---|---|---|
| RQ-H2 operating comparison | Equal hourly **kg H2 at specified pressure/purity and delivery node**, same 8,760 timestamps and target service | From electricity and water source through PEM, storage, compression/conditioning to named plant delivery gate; 2023 operations plus a defined equipment economic/physical life | H2 capacity = tank equipment mass; modeled H2 = metered; mismatched annual H2 delivery implies matched service |
| H2 product climate impact | kg CO2e/**kg H2 satisfying matched functional unit** | Inventory extraction, manufacturing, installation, operating electricity/water, spares, replacements, storage/BoP/compression, and end-of-life at declared cut-off; no transport/end-use unless separately scoped | Native 0 unlinked providers proves absolute data completeness or ISO compliance |
| H2 TEA | Discounted cost / **kg service-compliant delivered H2** | Same installed asset boundary, lifetimes, source currency/price year; grid contracts/tariffs and curtailed wind opportunity cost explicit | DOE USD2022 CAPEX-only result is full EUR2023 LCOH |
| RQ-MeOH | **kg saleable methanol at explicit grade/pressure/temperature gate**, CO2 origin and temporal supply | Upstream H2 + captured/bought CO2 to synthesis/recycle/separations/auxiliaries/product gate; product EOL separately | kgCO2e/kg H2 = kgCO2e/kg MeOH; carbon uptake = permanent removal |
| Emissions accounting | Native openLCA named **IPCC 2021 GWP 100**; distinguish climate footprints from operational indicators | Baseline attributional BAFU v1.1, scenario/sensitivity electricity mix and counterfactual separately | Hourly price = hourly carbon factor; average grid footprint = marginal avoided emissions |

**Common 2023 service:** source PyNEXUS original target is 18,250,000 kg H2/year (50,000 kg/day) and original E/E+S each had delivery shortfalls. Treat this as the **candidate common demand**; verify hourly target definition from frozen Stage A/B before final preregistration. Reject a comparison that assumes both originally delivered 18.25 million kg. Baseline comparison must use the **same hourly delivery target, pressure, purity and reliability treatment**. If full service is infeasible under the original grid cap, explicitly report infeasibility or add an *identical, sourced* backstop supply option; never silently relax one case or invent replacement impacts.

**Study time** is a **one-year historical input experiment**. For multiyear TEA/LCA, state repeated-2023 representative-year assumptions, replacement timing and scenario uncertainty; never call repeated weather a 30-year observation.

## 3. Evidence register and data quality

Every nontrivial quantity must have:
\`input_id, source_title, authors/institution, publication_date, retrieval_utc, source_url_or_doi, original_locator(page/table/process UUID), source_SHA256/version, native_units, study_units, conversion_formula, geographic_scope, temporal_scope, technology_scope, source_license, evidence_class, uncertainty_distribution/bounds, transformation_script_version, reviewer, approval_state\`.

Evidence classes:
1. **O:** observed original provider data (ENTSO-E A44 price, ERA5 atmospheric source) with independent timestamp/coverage audit; ERA5-derived wind remains a *computed conversion* of observed/reanalysis weather.
2. **M:** original solved PyNEXUS hourly hydrogen dispatch with fixed original ZIP/Stage B SHA and independently verified balances.
3. **D:** original native BAFU:2026 v1.1 foreground/background LCI and named LCIA method; original v1 corrected workbook is a separate cross-check.
4. **L:** peer-reviewed literature, DOE H2A/DOE technical targets, Argonne HDSAM, physical vendor specification and test method; dates and edition pinned.
5. **A:** preregistered analyst assumption, bounded by physically plausible source references and never labeled as observation.
6. **T:** synthetic/fabricated inputs **only for unit/property tests**, never real-case optimization results.
7. **V:** independently measured experimental validation. **None currently available for full plant performance.**

No acceptance of orphan or undocumented values. Track missing source records as **BLOCKED**, not zero. BAFU restricted original inventories remain private; publish reproducibility scripts, process IDs, hashes and permitted derived summaries only. Freeze original PyNEXUS repository; new work records exact hashes and transformations.

## 4. System architecture, responsibilities and single-source ownership

\`\`\`text
Frozen PyNEXUS 2023: immutable source ZIPs (O weather/market, M H2 model)
                     |
                     v
PtXFlex: provenance, hourly physical power/H2/CO2/methanol model
   -> chosen design, full 8,760h dispatch, uncertainty, matched service
   -> versioned PtX exchange manifest (quantities, pressure, kg and energy)
                     |
                     v
PtXLens: source-verified equipment foreground/BOM, BAFU provider mapping,
   native IPCC2021 LCIA, harmonized TEA (source/price year), uncertainty
   -> versioned marginal manufacturing/operating costs and GWP impacts
                     |
                     v
PtXFlex: epsilon-constraint dispatch and design frontiers on approved factors
    -> final PtXLens consistent scenario re-evaluation, audit and report
\`\`\`

- **Authoritative thermo/dispatch equations:** PtXFlex. Hydrogen properties via version-pinned [CoolProp Hydrogen EOS](https://coolprop.org/fluid_properties/fluids/Hydrogen.html), using independently checked physical limits/reference points. Physical storage design equations, charge state and compressor duty belong here.
- **Authoritative physical equipment BOM:** versioned shared output generated by PtXFlex design module, verified with manufacturer/technical references, reviewed and consumed unaltered in PtXLens.
- **Authoritative environmental calculation and cost methodology:** PtXLens. BAFU 2026 v1.1 native openLCA on authorized local inventory; LCA contribution tree and independently reconciled source reference; OpenPyTEA/independent DCF with a common currency and price-year conversion ledger.
- **Authoritative cross-repo interface:** \`contracts/ptx-exchange-v1.schema.json\` **identical bytes in both repos**; canonical specimen and tests check full numeric and physical invariants. No implicit unit conversions or missing CO2/methanol fields accepted.
- **Source-only GPL/native solver and licensed databases:** build/tools separated from distributed original inventories.
- **Project integration:** use fixed commit hashes/artifact hashes for both repositories, not floating \`main\` branches in published results. Cross-repo CI may fetch *schemas and permitted derived inputs*, not private LCIs.

## 5. Model equations and required scientific verification

### Hydrogen and electricity

For hourly step \(\Delta t\), distinguish electricity generated, curtailed, imported, PEM DC input, BoP and compressor energy. The hourly electrical balance is \(W_\mathrm{used}+G_\mathrm{import}=E_\mathrm{PEM}+E_\mathrm{BoP}+E_\mathrm{comp}+E_\mathrm{synth}\), with explicit loss and metering location. Ensure no uncosted electricity.

Hydrogen stock balance with explicit reference at each timestamp:

\[
S_{t+1}=S_t+H_{2,\mathrm{produced},t}-H_{2,\mathrm{delivered},t}-H_{2,\mathrm{leaked},t}-H_{2,\mathrm{vented},t}-H_{2,\mathrm{rejected},t}.
\]

Every term has a validated source or must be explicitly marked scenario assumption. Treat true compressor losses and storage compression energy separately; avoid double counting the original 30-bar BAFU system's electricity.

Pressure/usable inventory \(m_\mathrm{usable}=V[\rho(P_\mathrm{max},T)-\rho(P_\mathrm{min},T)]\). Work from compressor thermodynamics (enthalpy rise and isentropic efficiency with inlet/outlet limits) or validated benchmark; prohibit a flat kWh/kg "realistic" coefficient with no physical or sourced pressure duty. Compare ideal-gas and real-gas density over specified range; verify conservation, positive temperatures/pressures, temperature limits and test model failure on impossible pressures.

**Original configured capacity vs physical capacity — original source audit completed:** the original archived PyNEXUS config and storage equations prove **20,000/40,000 kg are maximum inventory state bounds** with common initial/final minimum 10,000 kg, charge/discharge limits 2,200 kg/h, PEM outlet 30 bar and pipeline delivery minimum 20 bar. These are NOT already usable mass in a pressure-rated bank. The F2 source-based [working-pressure and published Type I-IV vessel audit](F2_PUBLISHED_STORAGE_PRESSURE_SWING_AUDIT.md) documents very different physical heel inventories and equipment masses. Demand pressure, tank pressure rating, source study bar basis and external pressure-vessel suitability must still be validated; do not conflate max gas stock, withdrawable gas and empty vessel kg.

### Methanol

Stoichiometry: \(\mathrm{CO_2+3H_2\to CH_3OH+H_2O}\) with full carbon, H and O atomic conservation; reactor conversion, recycle, purge, water handling, pressure/temperature, minimum load, start/shutdown, synthesis auxiliaries and CO2 purity *must be source-supported*. Keep original ideal 4h MILP for math tests only.

- CO2 scenarios: identified source geography and technology (e.g. biogenic or industrial point source) and declared capture/conditioning energy; no unverified 2023 hourly availability or blanket negative emissions credit.
- Methanol synthesis model **verification vs external published benchmark** for conversion, energy per kg MeOH and material/carbon flow; plant grade and saleable product gate declared.
- Without such source checks, a real 8,760h methanol result remains **exploratory**, and v1.0 may not describe methanol operations as validated.

### Optimization correctness and interpretation

For MILP, store SciPy/HiGHS version, incumbent objective, best bound, MIP relative/absolute gap, infeasibility status, wall time, deterministic settings and 8,760-hour coverage. Require explicit technical optimum vs feasibility; cap sweeps use the epsilon-constraint method, **same fixed delivered service**, and each Pareto point is independently audited, not just accepted from solver status.

Independent residual checks for every hour/annual ledger (dimensionalized tolerance, e.g. \(|r_t|\le 10^{-6}\times\max(1,\text{input magnitude in corresponding units})\) as preregistered initial numerical QA; tighter where exact mass arithmetic permits). Confirm bounds on pressure, min-load, recharge, terminal state, energy cost and emissions; analytical small cases and property-based perturbations must show rejection of infeasible data. Avoid proclaiming global optimum when solver time-limited/gap too large.

## 6. Work packages and release gates

**A gate is passed only with versioned artifact, independent test, source record, reviewer sign-off and no open critical defect.** No green badge alone confers scientific validity.

| WP | Owner | Deliverable | Required release evidence | Depends on |
|---|---|---|---|---|
| **P0** governance, immutable sources | Both | master plan, two native scientific audit baselines, evidence/gap registry, ADRs, cross-repo freeze ledger | every existing claim classified verified/incomplete/synthetic; original hashes and CI archived | — |
| **P1** contract and geometry of product gates | Both | pinned JSON schema, unit ontology, functional units, evidence metadata, scenario manifest | schema round-trip/negative tests and cross-repo byte identity; no undocumented physical defaults | P0 |
| **F1** original PyNEXUS replication | PtXFlex | E/E+S 8760h frozen source importer, independent hourly mass/price/energy reconstruction | all 17,520 source rows, source ZIP hashes, original annual and hourly conservation; separate original/non-original model | P1 |
| **F2** physically credible storage H2 EOS | PtXFlex | 30bar outlet to explicit min/max tank pressure, real-gas volume, storage state, compressor/cooling/vent model and 20/40t versions | two independent EOS reference points, unit/limit tests, physically sourced pressure vessel data, mass/energy residuals | F1 |
| **L1** shared BOM & source matching | PtXLens + PtXFlex | sourced vessel/valve/compressor, auxiliaries, replacements/EOL ledger for E and E+S | supplier UUID/functional unit, pressure/volume/material/vessel mass, country/year, no double counting, missing-material table | F2 |
| **F3** matched service and H2 dispatch | PtXFlex | identical demand/quality/reliability/terminal inventory, production/operating costs under source prices | independent 8760h audit; identical service vs explicit infeasibility or common source-backed backstop; solver gap and counterfactual | F2 |
| **L2** complete H2 native attributional LCIA | PtXLens | authorized BAFU v1.1 native product systems with E+S storage delta and matched service | 0 material unresolved providers; named IPCC2021 GWP100; contribution and source-factor reconstruction; characterization completeness review | L1,F3 |
| **L3** harmonized H2 TEA | PtXLens | original-year EUR cost model, physical sizing, annualized CAPEX, finance, replacement, energy tariffs and H2 denominator | H2A benchmark, original OpenPyTEA validation, independent DCF, cumulative project ledger + sensitivity | F3,L1 |
| **F4** physical e-methanol + CO2 source | PtXFlex | mass/energy/reactor/CO2 supply model, operating limits, independent literature process check | carbon/hydrogen/oxygen balances, source process specs and uncertainty; refuse fabricated CO2 telemetry | F2 |
| **L4** methanol gate LCA/TEA | PtXLens | 1kg MeOH gate, upstream H2 and CO2, explicit allocation/end-use, process-linked LCIA and LCOM | BAFU process reference + foreground differences; no CO2 double credit or H2-to-MeOH denominator error | F4,L2,L3 |
| **X1** coupled design/operating frontier | Both | approved equipment scenarios → matched dispatch → native environmental/cost re-evaluation; **H₂-only frontier first, methanol frontier conditional** | objective/best bound, independent audit, sampled frontier dominance, no circular cross-repo coefficient injection | **H₂:** L2,L3; **MeOH branch:** F4,L4 additional |
| **X2** robustness, external review and release | Both | sensitivity/uncertainty, independent source checks, traceable v1.0 results, reproducibility package | documented assumptions/limitations, adverse cases, source/licence audit, peer technical review, release signed by gates | X1 |

### v1.0 acceptance levels: separate what is *scientifically established*

- **Dependency rule:** A v1.0 **hydrogen** research release must not be blocked by unrelated, unavailable CO₂-to-methanol source data. X1's hydrogen cost–GWP frontier can pass after L2/L3; the separate full MeOH frontier additionally requires F4/L4. This does not waive any mandatory hydrogen physical-storage or LCA gates.

**Tier A — Native validated calculation / source-verified modeling:** all H2 P0–L3, matched-service F3, storage equipment L1/L2, material/pressure/electricity constraints and source cross-checks **mandatory for both repos to call the hydrogen comparison v1.0**. A native computational result is "executed and numerically verified"; do not claim plant validation without measurements.
- **Tier B — Scientifically supported e-methanol:** F4 and L4 pass if independently sourced reactor/CO2/auxiliaries data and proper product boundaries are obtained, then X1 includes MeOH Pareto results. If unable, v1.0 must **explicitly label methanol as an exploratory subsystem** and may only ship as **"Hydrogen core v1.0 / methanol experimental"**, never "full validated Power-to-methanol v1.0".
- **Tier C — Industrial/experimental validation:** real-time plant data for a specified operating plant are not available. Tier C is NOT a release-blocker for an appropriately labeled *prospective engineering research* v1.0, but must be flagged absent in report/abstract/portfolio.

## 7. Scientific test and uncertainty matrix

| Class | Required coverage | Fail behavior |
|---|---|---|
| Data provenance | immutable ZIP and Stage A/B SHA, time UTC 8,760 exactly, negative/time discontinuity checks, price cross-source | hard fail, no interpolation or synthetic fallback |
| EOS and pressure | reference density/enthalpy against CoolProp, pressure swing and 30bar tank outlet gate, compressor efficiency and limits | reject impossible/two-phase/out-of-range states |
| Hydrogen operating balances | hourly electricity, H2 mass, state, storage charge/discharge, pressure, terminal inventory, demand and flexibility | hard fail if residual/bounds breached |
| MILP verification | toy analytic cases, known infeasible/feasible, independently reconstructed primal, global gap and re-solve reproducibility | no "optimal" label without bound/gap |
| Methanol atom/energy | stoichiometry, CO2 availability, reactor conversion, H2 consumption, process heat/power | no greenhouse/product claims if violated |
| Background LCA | real provider links, allocation, GWP100 chosen, elementary flow characterization, BoP/storage avoided double count | reject unsupported footprint; no missing=0 |
| TEA | $2022 vs €2023 price basis, CAPEX/stacks, energy charges, discount/replacements, independent DCF | no full LCOH/LCOM if missing |
| Uncertainty | bounded source distributions, 1-way + interacting sensitivity, joint cost–GWP ranking under extremes; converged sample counts | never assert robust superiority from point estimates |
| Code/research quality | deterministic lockfiles, type/unit/shape validation, documented exception/failure states, CI on clean checkout, peer code review | block v1.0 tag |

Uncertainty plan: classify **aleatory** weather/market (only one historical year available, not a time-series probability distribution) vs **epistemic** plant/background/CO2 parameters; use physically coherent joint scenarios, maintain a base/pessimistic/optimistic ledger, check correlation and multiyear sensitivity with alternative sourced years only if available. Report sensitivity intervals and threshold where E+S ceases to be advantageous. Do not label bootstrap from a single 2023 year a validated 30-year climate risk forecast.

## 8. Integration contract and release traceability

**P1 implementation status:** initial identical schema + Python scientific validator now exist in both repos and reject unmatched/native LCA and capital-only-cost overclaims. It currently stores **source SHA, functional unit, rated storage capacity and source status, annual flow ledger, native impact status and finance claims**. The *target v1.0 contract* below additionally requires a content-addressed 8,760-hour flow artifact (rather than embedding arrays in every summary), equipment-list supplier UUIDs, physical pressure/quality certificates and full TEA/LCA contribution outputs. Those extensions remain P1 blockers; the current initial schema is not itself the complete v1 release interface.

Target shared exchange fields/semantics:
- \`schema_version\`, \`study_id\`, \`scenario_id\`, \`source_provenance\` (original ZIP sha256, solver commit, BAFU edition/method UUID);
- \`functional_unit\` (product, kg, pressure bar, purity fraction, location/gate, service profile SHA), \`hourly\` (UTC intervals, power sources, grid/curtailment/PEM/compressor, H2 production/delivery/store/leak, optional methanol and CO2 with explicitly named dimensions);
- \`equipment\` (kg hardware, original process provider UUID + reference unit, lifetime/replacement and manufacturing technology);
- \`impact\` (method and region, gross climate, embodied, operational, upstream, end-of-life, noncharacterized flow counts, native-run evidence);
- \`economics\` (country/currency/price year, capex/opex, VAT/tariffs treatment and DCF);
- \`evidence_status\` and \`limits\` with \`null\` for *unknown*, never 0.

**BAFU provider rule, newly audited from original v1 EcoSpold:** process UUID b4739ad2-aa38-368d-8ada-63f5417c8b55 (High pressure hydrogen storage tank) is a **vehicle/composite** tank reference with general comment describing inventory *per kg of hydrogen capacity*, despite an exported reference flow unit of kg. Its recipe uses 7.14kg carbon fibre and 3.06kg epoxy plus metal inputs per reference unit. It is **not a kg-empty-Type-I-steel source**. No existing nominal/mass-based BAFU tank multiplication is approved; source v1.1 must be independently verified and the physical technology matched before native storage impacts. PtXLens records this mismatch in its original-source audit. 

**Critical identity:** \`m_\mathrm{H2,delivered}\` refers to product flowing over the boundary at the same delivered service/pressure/purity. \`m_\mathrm{tank}\` refers to empty equipment mass; \`m_\mathrm{stored}\` to instantaneous physical H2; \`m_\mathrm{tank,nominal}\` to rated H2 capacity; no implicit exchange is permitted.

**Two comparison thresholds:** `matched_operational_service_verified` means both dispatch scenarios actually satisfy the same physical hourly product service (pressure, quality, demand profile and source series). `matched_service_comparison_eligible` is a *stronger* GWP/TEA claim that additionally requires full storage equipment/LCA cost scope and complete comparable financial/impact methods. Operational parity may be established first; no circular dependency on unavailable environmental inputs is allowed.

Cross-repo contract tests: byte-identical schema SHA, valid real-source-derived example passes, missing/unknown/null impact fails publication gate, changed functional-unit/service hash and source-market/wind/demand SHA fail cross-case comparison, source process UUID and units do not autocorrect. Version \`1.x\` additions must be backward-compatible; all breaking schema changes require version 2 + ADR + migration.

## 9. Technical governance and anti-scope-creep procedure

- **One authoritative plan** in each repo, same content and hash, and one [decision log](DECISION_REGISTER_v1.0.md) per repo; all code changes reference WP and gate. Existing issues kept; derive new tasks from WP dependencies, not whichever feature is most attractive.
- **Change request required** for altered functional unit, boundary, source year, database edition, storage pressure, default equipment technology, demand service, CO2 origin, discount rate, method/category or solver economics. Each request contains alternatives, source evaluation, consequences, changed tests and effect on previous results.
- **Implementation stages:** (1) P0/P1/F1, (2) F2/L1, (3) F3/L2/L3, (4) F4/L4, (5) X1/X2. **No new graphics/GUI/full website work until the science gates pass.**
- **Review process:** primary model author not sole verifier of equations, optional adversarial independent reasoning test, negative-case QA, review of numerical precision, assumptions, source licences and claims.
- **Releases:** \`v0.x\` working branches and reproducible runs, audited \`v1.0-rc1\` with pinned source/contract/CI and release report, independent review and issue closure before \`v1.0.0\`. Never tag a release based solely on green unit tests.

## 10. Predefined result package and expected publishable figures

Each v1.0 study exports:
1. Source/version/attribution and hourly time-alignment audit; equation, symbol and units dictionary.
2. Source benchmark comparison E/E+S, original (unmatched) vs optimized matched-service (clearly labeled).
3. Thermodynamic storage size/pressure/usable inventory, compressor power and residual profiles, vessel BOM + unit manufacturing sourcing.
4. Price-sorted wind/grid dispatch with actually constrained storage; negative/positive price effects distinguished from emissions.
5. Annual mass and energy Sankey ledger from genuine solved numbers, not decorative graphics.
6. Full native IPCC GWP100 product-system contribution bars (stack, grid, offshore wind, water, storage vessels, compressors and EOL), separately quantified missing/uncertain.
7. Harmonized cost breakdown (capex, power, compression, storage, replacement, non-power OPEX) and independently checked cash-flow table.
8. Matched-service cost–GWP epsilon frontier and feasibility/robustness envelope.
9. Methanol reaction carbon balance / CO2 source and product-grade analysis **only after F4/L4**; distinguish methanol-at-gate from any combusted/equivalent end use.
10. Scientific limitations, validation evidence, negative test cases, reproducible scripts, licensed-data acquisition instructions, contributor and reviewer credits.

## 11. Release stop conditions — never negotiate away for a date

- Original source ZIP/LCIA SHA mismatch; unproven input provenance, incompatible units or mixed BAFU editions.
- Missing physically necessary storage/CO2/BOP flow substituted as *zero impact*, or an LCI supplier mapped on name alone.
- Common H2 demand not satisfied/infeasibility hidden; E and E+S have unequal service in a claimed superiority comparison.
- Missing pressure, storage volume, compressor energy, equipment mass or inventory lifetime in a purported complete E+S footprint.
- MILP result missing objective/best bound/gap; no independent residual audit.
- Native LCA category mismatch, unlinked critical provider/flow, double counted pre-characterized BAFU factor.
- Currency/price-year mismatch or incomplete CAPEX/OPEX represented as complete LCOH.
- Methanol input chemistry/CO2 emissions unattributed or lab-quality measurements falsely claimed.
- Published comparative superiority/ISO certification without warranted review.

## 12. Decision hierarchy and source references

Primary model decisions are made in order: **product functional service → actual source data → physical conservation/technology → validated supplier inventory → cost/emissions accounting → optimization → uncertainty → comparative interpretation**. Later convenient solver behavior does **not** retroactively override an earlier boundary decision.

Initial external references to pin at WP execution:
- [ISO 14040:2006](https://www.iso.org/standard/37456.html), [ISO 14044:2006](https://www.iso.org/standard/38498.html), [ISO 14067:2018](https://www.iso.org/standard/71206.html).
- [CoolProp hydrogen reference EOS](https://coolprop.org/fluid_properties/fluids/Hydrogen.html) (install/pin actual version and check reference state; original source and EOS validity documented).
- [DOE PEM electrolysis technical targets](https://www.energy.gov/cmei/fuels/technical-targets-proton-exchange-membrane-electrolysis) — **targets, not our plant measurements**.
- [DOE H2A production methods](https://www.hydrogen.energy.gov/program-areas/systems-analysis/h2a-analysis/h2a-production) and [ANL HDSAM](https://hdsam.es.anl.gov/index.php?content=hdsam) — benchmark assumption framework; transfer to NL only with regional adjustment.
- [2026 stationary hydrogen vessel technology comparison](https://doi.org/10.1016/j.ijhydene.2025.152849) — *candidate* real vessel geometry and cost; verify exact pressure, temperature, mass and source conditions rather than assuming type I 200 bar default is optimal.
- [BAFU:2026 v1 Nexus reference](https://www.openlca.org/bafu2026-version-1-is-now-available-on-nexus/) and separate authorized v1.1 native source / corrected v1 original workbook; do not redistribute raw source.

**V1.0 means reproducible, source-reconciled, uncertainty-bounded *prospective modelling* of explicitly named boundaries; not industrial measurement or universally predictive PtX performance.**
