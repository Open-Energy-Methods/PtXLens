# L3-G — Paired PtXFlex/PtXLens source-scoped scientific release qualification

Research protocol revision: 18 November 2026. This is a **scientific claim audit**, not physical procurement approval, industrial validation, native BAFU LCIA, verified installed NPV or unconditional v1.0.

## 1. Exact analysis boundary

Compare original E20t and E+S40t equipment concepts under the **same exogenously prescribed 1,250 kg H2/h (30 t/day)** for each individual source year, with original 90% wind ELECTRICAL POWER and original `max_inventory` storage semantics. 2022 and 2024 remain separate historical modelled scenarios: 365 and 366 days, respectively, giving 10,950,000 kg and 10,980,000 kg delivered H2. The 2022/2024 energy-price advantages are not probabilities, forecasts or merchant revenue contracts.

Original F2 stationary Type I source: an extra **20,000 kg MAX gas inventory** is **not** the original reference **17,784.924849614785 kg pressure-swing usable quantity**. Preserve the distinction even when a hypothetical EOS calculation rounds an original 1.8 m3 paper-vessel count. The original 802 empty reference vessel positions and 1,924,800 kg empty paper equipment are NOT a supplier-qualified bank, virgin steel input or manufactured foreground flow.

## 2. Technical qualification of the research evidence

The L3-F auditor first *regenerates byte-for-byte* eight public-safe artifacts. A distinct L3-G validator then independently checks the paired JSON semantics, including:

- four files per repository and original F2 source Git-blob concordance;
- fixed maximum-inventory semantics and two distinct H2 capacity quantities;
- 2022 and 2024 annual matched-service masses, separate accounting years;
- exactly 19 aligned original F2 equipment/physical/cost/native mapping line IDs, plus 13 site engineering domains;
- hypothetical temperature endpoints and absolute pressure not misrepresented as vendor PED MAWP;
- NULL/false actual installed CAPEX, OEM pressure certification, actual site NPV, native BAFU LCIA, lifecycle GHG, and full v1.0 release.

The code rejects any missing, modified, non-LF or source-incompatible L3-F report **before** it issues a manifest. L3-G verifies the science *claims* and the file fingerprints, not external manufacturer authenticity, original raw source datasets or native openLCA product-system outputs.

## 3. Claim-to-evidence ledger

Allowed but scoped:
- R01: source-model fixed H2 delivery in matched E/E+S yearly runs;
- R02: original F2 gross versus pressure-swing usable reference capacities;
- R03: three hypothetical real-gas thermal endpoint sizing screens;
- R04: independent separate-year wholesale savings plus explicitly conditional DCF ceilings;
- R05: signed modeled grid-import inventory, *not* an emissions comparison;
- R06: 19 original BOM category coverage across physical, finance and future LCI requirements.

Blocked:
- B01: actual OEM pressure bank and site/PED/HAZOP conformity;
- B02: actual signed all-in installed costs, contract rates and project NPV;
- B03: real material foreground and native BAFU:2026 v1.1 provider-linked production/replacement/EOL LCIA;
- B04: lifecycle environmental superiority;
- B05: comprehensive scientific v1.0 and validated real operation.

Every ledger row points to actual relative source-audited JSON paths and never includes private file paths. The manifest carries hashes for the **eight already-scope-verified public records only**. This is not evidence of the content of private original datasets.

## 4. Local Windows reproduction and immutable release review

Use the original paired PtXFlex Python venv containing scientific dependencies, and pull the **reviewed** L3-G change on each branch before running:

    cd C:\Users\prasa\OEM_Research\PtXLens
    .\scripts\F3D_Robustness_Local.ps1 -Phase Test
    .\scripts\F3D_Robustness_Local.ps1 -Phase L3FAuditPublic -Mode max_inventory
    .\scripts\F3D_Robustness_Local.ps1 -Phase L3GPrepare -Mode max_inventory
    .\scripts\F3D_Robustness_Local.ps1 -Phase L3GAuditPublic -Mode max_inventory

L3GPrepare creates exactly **two more** LF-stable, immutable, public-safe output files under PtXLens/data/results (JSON and Markdown). L3GAuditPublic requires them to exist and be exact. It rechecks all eight L3-F sources and does not publish or download private data.

Output names:
- `L3G_PTXFLEX_PTXLENS_CROSS_REPO_CLAIM_EVIDENCE_GATE_NOT_SCIENTIFIC_V1_v1.json`
- `L3G_PTXFLEX_PTXLENS_SCIENTIFIC_RELEASE_READINESS_NOT_V1_v1.md`

**Manual release safety:** First review all 10 filenames and diffs, including possible credentials or local paths. Stage only known generated paths with `git add -- <exact paths>`, then `git diff --cached --check`, `git diff --cached --stat`, `git diff --cached` before committing. Do not use `git add .`; no original hourly MILP witnesses, private provider-price datasets, supplier original documents, proprietary native database content or personal filesystem paths should enter public GitHub.

## 5. What would unblock the full scientific v1.0?

For a model-limited reproducibility release, retain provenance, independent fixed-service LP/MILP audit, solver bounds, uncertainty limits and per-year assumptions. For an **unqualified** physical/economic/LCA v1.0, additionally require a reviewed site layout and pressure design, validated dynamic H2 storage charging/withdrawal, site-correlated compressor and thermal duty, authenticated OEM installed BOM/BoP quotation and maintenance schedule, comparably valued grid contracts, independently run native BAFU provider-linked foreground product systems with correct manufactured input masses, and matched-hour operational LCIA with explicit electricity accounting. An independent research audit cannot certify legal PED conformity.

Current decision: **L3-G source-scoped research release audit can pass; B01-B05 remain BLOCKED.** Do not label the two repositories comprehensive scientific v1.0 on that basis.
