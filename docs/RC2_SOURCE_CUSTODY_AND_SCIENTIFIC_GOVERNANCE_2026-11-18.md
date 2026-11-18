# RC2-A/B — Original-source custody and scientific governance reconciliation

**As-of 18 November 2026 UTC.** Shared programme OEM-PTX-2026-01. This is a scoped source-provenance and release-governance audit, not full P0 or scientific v1.0 approval.

## 1. Source custody: verified primary bytes, independent backup pending

The GitHub Actions API recheck confirms the following artifacts were unexpired on the check date. Their API SHA-256 digests matched the original freeze registry. All three already-stored private owner copies were retrieved into temporary analysis, their full ZIP bytes were hashed, and every archive CRC was checked with Python ZipFile.testzip. No raw provider XML, private file ID, path, token, or private archive contents enter Git.

| Original frozen artifact | ID | Verified ZIP bytes | Expiry UTC |
|---|---:|---:|---|
| E original 2023 | 12612294862 | 767808 | 2026-12-24 20:18:09 |
| E+S original 2023 | 12613045475 | 775930 | 2026-12-24 20:21:57 |
| Original A44 provider XML | 12610917985 | 79058 | 2026-12-24 19:24:29 |

Exact digests, source IDs, source-year receipt fingerprints and verification boundaries are in the shared [RC2 receipt](../research/RC2_SOURCE_PROVENANCE_AND_YEAR_EVIDENCE_2026-11-18.json).

**P0 NOT PASSED.** The observed existing private copies match the original archives; a temporary retrieval is not a second permanent physical backup. Independent storage-device custody, recovery, provider licensing and permitted distribution, and external scientific review have not been independently verified.

## 2. Offline preservation and recovery on the owner's computer

Use the previously verified files in the existing private owner folder. Download the three individual original ZIPs as-is (not a nested folder archive) into a private primary directory outside every Git checkout.

From PtXFlex with the existing Python environment, use the new no-network adoption mode:

    python scripts/preserve_pynexus_evidence.py --destination "<private-primary>" --adopt-verified-local

This validates each expected SHA/ZIP CRC and creates the original private provenance manifest without a token. If the primary ZIPs are already present, do not redownload or change them.

Choose a physically separate backup drive and a **new**, non-nested recovery directory outside all Git trees. Substitute the actual private directories:

    python scripts/verify_private_pynexus_recovery.py --primary "<private-primary>" --secondary "<private-secondary-drive>" --copy-secondary --strict-different-device --restore-into "<new-private-restore-directory>"

The verifier rejects altered, aliased, or missing files, backs up the original provenance manifest, and recreates all three originals plus that manifest **solely from the secondary**. It does not read the primary during the restoration operation. It reports separate filesystem IDs only as necessary evidence, not as proof of separate physical devices. If no second physical drive is available, do not present two directories/partitions as an independently verified backup. Document storage separation, custody, licensed access and a successful independent restoration outside Git.

No GitHub token or provider data belongs in a public report. Do not paste original archive bytes, private file locators, or the raw provenance manifest into GitHub.

## 3. Reconcile prior source-year evidence, not broad claims

The shared machine-readable gate register now records the following **scoped numerical admissions**. The old November 14 narratives are retained as historical context, not current truth.

- Two original source-year hash/calendar admissions: 2022 (8760 UTC hours) and 2024 (8784 UTC hours), observed Dutch A44 day-ahead price plus modelled wind derived from the equivalent-year ERA5 ARCO point extraction. The source represents reanalysis, not measured wind-farm power. The prior original 2023 CDS-to-ARCO 8760h 1W calibration receipt passed; upstream PyNEXUS original 2023 remains unchanged.
- Four separate E-selected price-neutral uniform-service year/mode pairs: 2022/2024 times max_inventory/usable_service. Do not merge these two different capacity semantics or use their optimized service selections as external contract assumptions.
- A **different** two-case study fixes 30 t/day and 90% of each source year's modelled wind electrical power, max_inventory only. Prior independent hourly physical/EOS/market primal replays support modeled nominal E-minus-E+S wholesale settlement savings of EUR 3,281,613.054 (2022) and EUR 1,931,675.853 (2024), with 10,950,000 and 10,980,000 kg respectively. The original HiGHS integer lower bounds are source reported, not independently reconstructed branch-and-bound certificates. Two years do not establish a distribution, expected value, forecast or market contract.
- The 8784-hour F3-D implementation compatibility statement is limited to admitted source-year experiments. It does not assert a modified upstream 2023 PyNEXUS solver, a complete 50t/day original contract, physically validated site, qualified OEM/PED, actual installed costs, native matched-storage BAFU LCIA, independent peer review or scientific v1.0.

No fresh readback of the private 2022/2024 source vectors is asserted by RC2. The existing public F3-D source audits and hashes already bind the prior private-source independent replay receipts.

## 4. Repeat the source-only public audit

Both repositories preserve all 12 original science gate decisions, dependencies, review requirements and acceptance evidence. All remain NOT_PASSED. The new PtXLens paired runner checks the shared receipt, original source registry and Git blob hashes, reconstructs prior F3-D admissions from published evidence, and runs RC1 (including exact L3-F/G publication checks).

From PtXLens with its paired PtXFlex environment:

    python -m ptxlens.rc2_provenance_governance --lens-root . --flex-root ../PtXFlex

Expected: RC2_SOURCE_RECEIPT_AND_GOVERNANCE_AUDIT_PASS_P0_AND_SCIENTIFIC_V1_BLOCKED.

This validates public receipts, not a second private archive readback, external legal licensing decision or validated plant design. Do not set any full acceptance flag to passed merely because CI is green.
