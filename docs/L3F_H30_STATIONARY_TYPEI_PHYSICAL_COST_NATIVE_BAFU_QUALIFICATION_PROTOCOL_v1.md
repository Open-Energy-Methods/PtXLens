# L3-F: exogenous H30 Type I stationary H2 storage physical, installed-cost and BAFU readiness protocol

Scientific checkpoint: 17 November 2026. Scope: independently replayed original 2022 and 2024 source-year E20t versus E+S40t, 30t/day fixed hydrogen service, 90% each year's original modelled wind ELECTRIC POWER and max_inventory storage semantics. This is research screening, NOT pressure equipment approval, site qualification, authenticated manufacturer quote, native LCIA, or investment viability.

## 1. Preserve the original physically distinct hydrogen capacities

The published source 2023 F2 incremental storage reference has **20,000kg extra MAXIMUM H2 inventory** and **17,784.924849614785kg extra pressure-swing usable H2** at 313K, maximum 200 bar ABSOLUTE and withdrawal heel 20 bar ABSOLUTE. These are different physical quantities. Original 802 paper-reference cylinders with 1.8m3 INTERNAL free volume and 2400kg EMPTY equipment mass each imply 1,924,800kg EMPTY PAPER equipment reference, not installed OEM design, virgin-steel input, or actual manufacturer cost.

PtXFlex L3-F reuses the real-gas CoolProp F2 solver to independently size two constraints. Gross capacity requires hot-fill density times free volume to exceed 20,000kg; conservative working service requires (hot-fill density minus cold-heel density) times free volume to exceed 17,784.924849614785kg. The sizing volume is the greater required value. For paper-vessel reference free volume v = 1.8m3, the mathematical discrete count is ceil(required free volume / v), followed by an independent forward EOS replay of BOTH constraints and a one-fewer-vessel minimality test.

Predeclared hypothetical endpoints: cold/hot 313/313K, 303/323K, 293/333K; maximum 200bar(a), heel 20bar(a). These are analyst temperature assumptions, NOT measured plant temperatures, fatigue life, dynamic withdrawal, compressor map, certified design pressure or a guaranteed 30t/day station. Source-year 2023 dispatch peaks are not automatically 2022/2024 compressor or process-plant design duties.

Published source and thermal modules:
- https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/data/results/F2_L1_2023_source_incremental_20t_to_40t_stationary_typeI_200bar_BOM_SCOPE_NOT_complete_native_LCI.json
- https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/src/ptxflex/f2l3f_stationary_thermal_qualification.py

## 2. Legal/engineering manufacturer acceptance — all currently open

The original model uses ABSOLUTE pressure. Do NOT equate it to vendor MAWP/test pressure given on a gauge basis or claim that 200bar(a) is a PED-certified manufacturer rating.

The European Commission explains that the Pressure Equipment Directive 2014/68/EU applies to design, manufacture and conformity assessment of stationary pressure equipment above its 0.5bar maximum allowable pressure threshold:
https://single-market-economy.ec.europa.eu/sectors/pressure-equipment-and-gas-appliances/pressure-equipment-sector/pressure-equipment-directive_en

Applicable hydrogen-system guidance includes EIGA DOC 15/21 Gaseous Hydrogen Installations and EIGA DOC 247/24 Hydrogen Overview, Distribution, Storage, Applications:
https://www.eiga.eu/uploads/documents/DOC015.pdf
https://www.eiga.eu/uploads/documents/DOC247.pdf

L3-F PtXFlex specifies 13 original engineering documentary domains and all 19 F2 equipment categories, requiring independent proof of: certified pressure/temperature basis, H2 compatible materials and fatigue, actual 2022/2024 maximum charge/discharge rates, real compressor/motor map, gas-quality and flow headers, relief/ESD/detection/ATEX/vent dispersion, piping loss and containment, cooling, P&ID, site spacing/foundations, installation, inspection/replacements, supplier technical bid and native manufacturing inventories. All real source evidence remains unverified, with no document-hash or self-attested boolean allowed to stand in for engineering certification.
https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/src/ptxflex/f2l3f_stationary_site_evidence_gate.py

## 3. Vendor all-in CAPEX/OPEX against independent, conditional source-year economics

The PtXLens L3-F cost bridge links exactly 19 original F2 vessel/balance-of-plant/inspection/end-of-life cost roles to the published 2022 and 2024 H30/W090 independently replayed wholesale electricity savings. The 2022 and 2024 historic nominal EUR are separate accounting years, not a probability-weighted market forecast. All quote lines, actual installed quantities and payment rights remain NULL, never fake zeros.

The bridge provides separately labelled analyst sensitivity cases for 20y, 8% real discount, 250k EUR/year additional OPEX, 1m EUR end-year-10 replacement, and 50/75/100% hypothetical repetition of EACH year's historic modelled electricity saving. Upfront incremental all-in storage CAPEX must include real vessel purchases, pressure-rated structures, compression, cooling, gas piping, safety/controls, civil, transport and installation; recurring inspection/maintenance is OPEX; replacements have dated CAPEX; terminal dismantling and EOL are separate. Material specification must not double-count vessel package costs.

Actual site NPV will require independently authenticated original vendor source bytes and contractual quote scope, pressure/hydrogen design compatibility, project price year and real-currency conversion, financing/tax assumptions, actual grid sale/purchase tariffs and qualified operating schedule. A successful JSON questionnaire or positive conditional CAPEX ceiling is NOT an investment approval.
https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/src/ptxlens/l3f_h30_cost_qualification_bridge.py

## 4. Original BAFU 2026 v1.1 LCA research gate

BAFU source data: https://www.openlca.org/bafu2026-version-1-is-now-available-on-nexus/ and https://api.data-platform.cloud.bafu.admin.ch/en/dataproduct-economy-consumption-lca

The new PtXLens L3-F source-locked contract requires genuine original BAFU:2026 v1.1 native openLCA process and provider UUIDs, reference product/flow, actual compatible exchange unit, manufacturer manufacturing-material input mass and fabrication yield, waste, transports, replacement, BoP and EOL, geographical appropriateness, LCIA method and independently replayed native product system. None are verified in public.

In particular, 802 times 2400kg of EMPTY paper-equipment mass must NEVER be substituted as virgin steel input or a BAFU steel-manufacturing reference exchange. The functional unit remains identical hourly delivered H2, 30t/day. Annual grid electricity differences also cannot become carbon differences without time-matched emission factors and justified export-credit accounting. The 2022 source E+S net grid import is +900.088MWh while 2024 is -880.758MWh compared with E, despite positive monetary benefits in both years. Compressor electricity is part of the physical system electrical balance and must not be counted twice.

An optional local original .zolca byte SHA256 and ZIP-container fingerprint feature can run privately with the actual file path and never uploads the database. This alone does NOT prove the original native database version, process/provider links, LCIA or manufacturer compatible quantities. Native BAFU GWP and environmental superiority remain NULL.
https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/src/ptxlens/l3f_bafu_native_mapping_contract.py

## 5. Eight-file immutable research publication workflow

Research branches: PtXFlex feat/milp-methanol-baseline and PtXLens feat/wp0-screening-core. Existing PtXFlex Windows Python virtualenv and CoolProp are required.

Run in PowerShell, in this order:

    cd C:\Users\prasa\OEM_Research\PtXFlex
    git pull --ff-only
    cd ..\PtXLens
    git pull --ff-only
    .\scripts\F3D_Robustness_Local.ps1 -Phase Test
    .\scripts\F3D_Robustness_Local.ps1 -Phase L3FPrepare -Mode max_inventory
    .\scripts\F3D_Robustness_Local.ps1 -Phase L3FAuditPublic -Mode max_inventory
    git status --short
    cd ..\PtXFlex
    git status --short

Four PtXFlex outputs: two source-locked paper thermal EOS sizing files, two PED/OEM/site-qualification requirement files. Four PtXLens outputs: two economic evidence-to-DCF crossover files, and two original native BAFU manufacturing/provider readiness files. All are JSON+Markdown pairs under each repo's data/results folder, generated with immutable fail-closed semantics.

The separate L3-F eight-file auditor regenerates each file byte-for-byte from already published source-year and F2 evidence, validates source scope and refuses private original hourly witness, supplier data or confidential BAFU database bytes. Only after an 8/8 audit and full staged diff review should the user selectively manually stage/commit/push exact new public reports. Never use git add . for these scientific experiments. No original provider-year full-year MILP rerun is needed.

At this checkpoint code and negative regression tests are committed but fresh L3-F local Windows testing and report generation are pending. The earlier published 171-pass/one-skipped L3-E and original independent 2022/2024 H30 replays remain unchanged. Whole-project certified hardware design, actual project profitability, independently rerun native BAFU LCIA and scientific programme v1.0 remain NOT PASSED.
