# RC1 — PtXFlex + PtXLens scientific and software release-candidate audit

**Audit date:** 18 November 2026. **Scope:** research feature heads PtXFlex at commit `eb9e6ff` and PtXLens at `f42de87`, before RC1 review changes. **Programme:** OEM-PTX-2026-01. **Decision:** structural/source-scoped reproducibility can be validated, but **unqualified scientific v1.0 is NOT ADMISSIBLE**. This is a testable audit protocol and bounded finding register, **not** an external peer-review certificate or plant validation.

## 1. Repository-wide baseline inventory and source boundaries

GitHub tree audit of the two published research heads (no truncation):
- **PtXFlex:** 287 Git tree entries; 25 workflows, 76 paths under tests, 38 published result files and 62 source paths. Original research feature PR [#1](https://github.com/Open-Energy-Methods/PtXFlex/pull/1) targets `main`, has 458 commits and 274 changed paths, and was a draft with GitHub `mergeable_state=dirty` at audit.
- **PtXLens:** 327 Git tree entries; 29 workflows, 55 test paths, 68 published result files and 69 source paths. Original research feature PR [#1](https://github.com/Open-Energy-Methods/PtXLens/pull/1) targets `main`, has 482 commits and 301 changed paths, and was a draft with GitHub `mergeable_state=dirty`.
- Both are MIT-licensed with public scientific source/report files. Absence of suspicious archive **filenames** in the enumerated Git trees is not a historical secret scan, source-licence clearance or assurance about the content of every file.
- `contracts/ptx-exchange-v1.schema.json`, `research/gates-v1.0.json`, `docs/PROGRAMME_MASTER_PLAN_v1.0.md` and `docs/DECISION_REGISTER_v1.0.md` have identical Git blobs between the two repositories at the audited commits. RC1 enforces byte identity.

The feature PRs to `main` must **not** be merged blindly. They need a conflict-aware rebase/merge integration plan, review of the huge accumulated changes, clean test runs on the *actual proposed merge commits*, and a deliberate supported software version.

## 2. Scientific audit and conflicting evidence levels

**What is reproducible:** narrowed, source-registered historical model simulations and original F2 reference screening, including an original fixed 30 t/day H2 matched-service 2022/2024 research counterfactual at 90% each modelled year's wind electric power, separate-year model wholesale cash savings, a 20,000 kg gross MAX inventory vs distinct 17,784.924849614785 kg original reference pressure-swing withdrawal, three hypothetical CoolProp temperature endpoint screens, and conditional discounted-CAPEX ceilings. The L3-F eight-output audit and L3-G two-report claim ledger have passed on Windows and in GitHub Actions.

**What is NOT reproducibly established as a real project:** actual hydrogen-station PED engineering/certification, site transient/piping/hazards and compression duty, manufacturer-signed procurement and 19-line installed costs, owner electricity tariff/market contract economics and investable project NPV, full material processing/replacements/EOL native BAFU:2026 v1.1 *matched-service* product-system LCIA, real experimental plant accuracy, or industrial environmental superiority. Paper-empty vessel equipment mass **must never become virgin steel input**. Price historical years are neither forecasts nor samples from a probability distribution; 2022 E+S net grid electricity imports increase while 2024 decrease under the reported accounting. Electricity-price advantage cannot prove CO2 advantage.

**All 12 top-level programme packages** P0, P1, F1, F2, L1, F3, L2, L3, F4, L4, X1, X2 are `NOT_PASSED` in both identical `gates-v1.0.json` files, despite valid narrower sub-gates. Flags `hydrogen_core_v1_allowed=false` and `full_methanol_v1_allowed=false` are correct and remain unchanged by RC1.

**Unresolved source consistency review:** the shared programme gates document still contains historical text claiming **zero authenticated 2022/2024 source pairs** and an unsupported 8784-hour year model, whereas newer published F3-D/L3-E/L3-F narrow H30 counterfactual evidence and independent annual 2022/2024 replay exist. Reconcile exact *which* source year/variant and original input-witness pair was authenticated, which solver handles leap-year, and what remains only a conditional source-linked audit. Do not replace the gate history with an unreviewed blanket assertion of "all years validated." Check newer reports and original private SHA receipts before changing status.

## 3. Ranked release blockers and remediations

| ID | Priority | Verified observation / risk | Required closure |
|---|---|---|---|
| RC1-C01 | Critical | Original 2023 PyNEXUS E, E+S and A44 source ZIPs are documented to expire **24 Dec 2026** (earliest historical documented 19:24:29 UTC); off-Git user-controlled verified private two-copy escrow has not been independently evidenced | Lawful immediate private source preservation, cryptographic SHA/ZIP integrity and independent restoration test, custody/licence record; do NOT put proprietary/raw files on public GitHub |
| RC1-C02 | Critical | Both main PR #1 are draft and GitHub reports merge conflicts; 274/301 changed paths | Isolate merge blockers, reconcile to main with reviewable PRs, test actual merge SHA; do not force merge, rebase away history or auto-release |
| RC1-C03 | Critical | 12/12 programme science gates still NOT_PASSED and external engineering/LCIA/financial data absent | Preserve structural green vs science red separation; decide whether a narrower research-software pre-v1 release is appropriate |
| RC1-H01 | High | Independent original 2022/2024 H30 publication is newer than some P0/F3-D programme status narratives | Source-receipt-led scientific gate reconciliation, documenting per input, year, leap and functional service scope before updating source statuses |
| RC1-H02 | High | PtXLens L3-G JSON/MD outputs initially lacked explicit LF attributes; Windows reported CRLF conversion warning | **Addressed in RC1 change:** add `data/results/L3G_*.json/md text eol=lf` and regression enforce it |
| RC1-H03 | High | PtXLens paired CI still used older fixed PtXFlex commit `15fb0b2`, not the newly published L3-F report evidence `eb9e6ff` | **Addressed in RC1 change:** pin the public paired source checkout at `eb9e6ff3f82edf13ed6be118dea0a29b6765b836` and run paired RC1 evidence check |
| RC1-H04 | High | `pyproject.toml` declares both packages **0.1.0**; NumPy/SciPy/pytest depend on compatible *ranges*, not a fully preserved tested environment/lock | Capture Python version, solver/HiGHS/CoolProp and dependency hashes; repeat bounded clean-env numerical regressions, then publish a licensed reproducible environment manifest |
| RC1-M01 | Medium | 54 workflows across both projects; representative original-provider workflows use authenticated private artifacts, secret-backed manual downloads and version-tag third-party Actions | Complete per-workflow permission, trigger, secret, archive retention/licence and action SHA review. RC1 adds `contents: read` to main core CI; it does **not** claim all 54 audited |
| RC1-M02 | Medium | Numerous older README / research milestone paragraphs have historical statuses (previously unrun, untracked, or blocked) | Create an as-of-SHA evidence index; historical log entries must remain dated, and the latest release status must not be ambiguous |
| RC1-M03 | Medium | Existing `main` does not yet have the research work from feature PRs | Do not publish a formal v1 tag from `main` or compare user-visible published package version with feature-only research status |

## 4. RC1 implemented checks and evidence integrity

`src/ptxlens/rc1_release_audit.py` is a **fail-closed structural auditor**. It:
1. Requires both local repository checkouts, their tracked Git filenames, approved LF settings, and exact 4 shared governance files by SHA;
2. Validates 12-gate dependencies as a DAG, requires reviewed acceptance evidence before accepting any gate marked PASSED, and rejects release flags inconsistent with the top-level gates;
3. Re-runs the source-exact L3-G/L3-F paired reconstruction and checks published 8+2 report bytes, SHA fingerprints and narrow credential/local-path signatures;
4. Rejects tracked raw provider/archive/private-key filename classes and prevents future accidental mismatch of CI-pinned evidence and scientific-release status;
5. Produces only `RC1_STRUCTURAL_SOURCE_EVIDENCE_PASS_FULL_SCIENTIFIC_V1_BLOCKED`. `--require-full-v1` deliberately fails. No private data, new annual source MILP, native BAFU, manufacturer station, independent licence authenticity or actual project NPV is processed.

To run from a PtXLens working copy with PtXFlex as a sibling:

    python -m ptxlens.rc1_release_audit --lens-root . --flex-root ../PtXFlex

Use the same Python environment that runs the paired L3-G audit and includes CoolProp 8.0.0. The independent CI gate installs a SHA-pinned PtXFlex checkout. Local Windows `-Phase Test`, `L3FAuditPublic` and `L3GAuditPublic` must still pass. Inspect any optional locally generated report before committing. RC1 does not modify either main PR or produce a release tag.

## 5. Release definitions and acceptance decisions

**Supported today:** a properly caveated source-model research evidence snapshot, labelled as experimental/numerical research **not** industrial validated. This may be archived as an internal **RC1** on research feature branches after CI and reviewer approval.

**Blocked:** an unqualified hydrogen/methanol scientific v1.0, industry-qualified plant, complete native BAFU-v1.1 H2 storage system environmental result, or full project return estimate. None can be claimed by passing source-only CI.

**Next priorities in dependency order:** private user-controlled source escrow before original archive expiry; reconcile new F3D year-specific evidence into the science-gate register; resolve two huge main-branch conflicts using reviewable integration; freeze and reproduce the dependency environment; complete scoped source/provider/physical validation and external review. Site/OEM and native BAFU requirements remain longer-term scientific dependencies, not placeholders to fill with invented numbers.

**Audit limitations:** scoped code/filename review and repeated CI do not constitute a comprehensive security scan of historical Git commits, an external scientific replication from independent raw datasets, scientific peer review, or native LCIA. The RC1 code cannot certify or waive those requirements.
