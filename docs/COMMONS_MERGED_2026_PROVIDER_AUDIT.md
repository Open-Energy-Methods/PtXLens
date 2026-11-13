# Commons Merged (2026) — actual PEM-H₂ LCA database and provider-coverage audit

**Audit date:** 2026-11-13  
**Status:** original background database acquired and indexed; IPCC climate method present; **full provider-linked product system NOT achieved**. No native openLCA LCIA calculation is claimed.

## 1. Real database acquisition (passed)

Primary database: [Federal LCA Commons — Commons Merged](https://www.lcacommons.gov/new-commons-merged-repositories-combining-existing-databases). Exact source downloaded from the public openLCA Collaboration Server API, **without fabricating or embedding any library**:

- Prepare: \`https://lcacommons.gov/lca-collaboration/ws/public/download/json/prepare/Federal_LCA_Commons/commons_merged\`
- Download: \`https://lcacommons.gov/lca-collaboration/ws/public/download/json/{opaque-download-token}\`
- OpenLCA 2 JSON-LD ZIP size: **51,012,635 bytes**.
- Immutable source ZIP SHA256: \`1ded185617d4de67f8ed6933c473a68d65c232dd738779179e8559a31dfd056d\`
- ZIP members: 10,573, including duplicate archive index entries. When keyed by JSON-LD \`@id\`: 2,516 processes, 6,883 flows, 3 LCIA methods, 30 LCIA categories.
- Full original download and integrity verification, CI: https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43431179377
- Current provider/method graph CI: https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43432287400

All calculations and export routines re-download and verify the full SHA256. We intentionally do **not** publish the raw ZIP in GitHub because it aggregates third-party source datasets with individual terms. The provenance and coverage CSVs are published as GitHub Actions artifacts.

## 2. Real 1 kg PEM reference unit process (passed source inspection, blocked upstream)

Original USLCI record: [Hydrogen; proton exchange membrane water electrolysis; at plant](https://lcacommons.gov/lca-collaboration/National_Renewable_Energy_Laboratory/USLCI_Database_Public/dataset/PROCESS/f00a298a-295f-4fbc-b463-45f8e96f018b?commitId=978870b1695caa9519f55aa5904dfd348a823623).

UUID: \`f00a298a-295f-4fbc-b463-45f8e96f018b\`. Source process data SHA256: \`67a6bd9afffb76c5e51a8ded69cc1de0ddbddf104ed69e4f75ec89f7f86d79d3\`. It represents a **US-background hydrogen process with 2017 representative inputs**, adapted from the Bareiß et al. PEM process, not a measured Netherlands 2023 electrolyser. Anode drying/purification not included.

| Source input per kg dry hydrogen | Amount | Actual provider status |
|---|---:|---|
| Electricity AC, 120 V | 198 MJ (55 kWh) | Existing supplier UUID referenced, original output flow matched |
| PEM stack, 1 MW | 8.97 × 10^-7 units | Existing stack manufacturing supplier referenced and source flow matched |
| Electrolysis plant construction | 3.18 × 10^-7 units | Existing plant construction supplier referenced and source flow matched |
| Deionized water | 9 kg | **NO supplier**, NO identical-flow output process in downloaded Commons Merged |

This already represents a useful native foreground *reference inventory*, but **not a connected cradle-to-gate product system**. Its equipment inventories must not be double counted with the separate Kanz (2024) material input model. A future scenario must replace/sensitize electricity use with original PyNEXUS E/E+S delivered-H₂-normalized energy, with explicit geographic substitutions and quality/pressure boundary.

## 3. Actual supplier graph (hard research blocker)

The code traverses defaultProvider UUIDs from the actual 1 kg PEM process and checks that each provider process exists and actually produces the required **exact flow UUID**. After allowing valid coproduct supplier outputs, the verified output is:

| Graph inspection | Count |
|---|---:|
| Unique reachable upstream processes | 1,005 |
| Technosphere input exchanges examined | 3,511 |
| Exchanges without explicit default provider | **695** |
| Missing exchanges with **no** same-flow output supplier in archive | **683** |
| Missing exchanges with **one** same-flow supplier candidate | **6** |
| Missing exchanges with **multiple** same-flow supplier candidates | **6** |

These counts are input **exchanges**, not 695 different materials or 695 necessarily significant environmental contributors. However, incomplete chains can silently omit real burdens. Twelve exchange-level candidates are potentially repairable from providers with matching flow UUIDs; **none has passed process/year/region/units/LCIA review**. The other 683 unresolved exchanges currently lack same-flow suppliers in the downloaded archive, so automatic default-provider selection cannot fix them merely by changing a preference.

Five near-source critical missing exchanges, from actual JSON-LD source IDs:

| Actual missing supply | Flow UUID | Limitation |
|---|---|---|
| Deionized process water | \`82f8b155-a9c4-3e4b-ac66-1e33af2f8f54\` | No same-flow producer |
| Tetrafluoroethylene | \`b544e484-ebb7-32bf-a241-385457452aa8\` | Missing PEM stack precursor source |
| Activated carbon | \`889db3d1-a55e-3c24-984e-ee23c829f41a\` | No identical source output; similar US carbon process may be a proxy with different flow identity |
| Electronic component, unspecified | \`d1940a7c-9f2e-3eef-84f7-9ef2d4442d29\` | Construction/BOP background not connected |
| Silica gel | \`5c53eb4a-3f9f-4a70-8225-f174953c2911\` | Construction/plant process missing |

**No automated graph completion has occurred.** The [full unresolved exchange CSV](https://github.com/Open-Energy-Methods/PtXLens/actions/workflows/commons-public.yml) produced by the on-demand workflow and its unique flow summary preserve every gap by original consumer UUID, input flow UUID, possible supplier IDs and explicit \`verified_linked=False\`. Never fill these with guessed substitutes or zero GWP.

## 4. Impact-method verification (available, not yet executed)

Actual merged database contains an \`IPCC\` LCIA method with UUID \`00feb6d9-9282-3bcf-9d18-7b040f516935\`. The \`AR6-100\` category has UUID \`a6206006-65bc-395c-8dc9-f12262f45a04\`; all **134** included characterization-factor flow references exist in the original archive's flow list. Also includes AR5-100 (117 matching factors), AR6-20, AR6-500 and biogenic accounting variants.

This is strong evidence the database contains a usable **LCIA method vocabulary**. It is **not** proof every relevant upstream emission can be characterized, not proof of provider closure, and not a native openLCA calculation. No GWP100 footprint should be reported from this source until the actual product-system model, links and impact coverage pass.

## 5. Separate API material discovery (candidates, not links)

A separate live USDA FLCAC API, using searches in Commons Merged, checked titanium, aluminium, steel, copper, Nafion, activated carbon, iridium, platinum, deionized-water/treatment, compression and offshore wind. The result CSV intentionally marks **0 verified provider links** because the API returns text search records, not validated product-flow providers.

Promising **candidate only:** US stainless steel 304 and activated carbon production; neither automatically maps to the original 1 MW PEM source flow and both require geographic/process review. Titanium dioxide and aluminium sulphate are **not** titanium/aluminium metal inventory replacements. Precious-metal and Nafion results are incomplete. A final search hit was rate-limited with HTTP 429, not an indication that no source process exists.

API https://www.lcacommons.gov/lca-commons-api-guide requires a **personal free api.data.gov key** for larger searches. DEMO_KEY is restricted to occasional manual exploratory testing. The repository's key-based workflows now require a user's \`LCA_COMMONS_API_KEY\` secret and run manually only; the authentic full-ZIP public download needs no API key.

## 6. Prioritized, source-checked repair decisions

The following are *research work requirements*, not new provider-mapping assertions:

1. **Mandatory foreground baseline repair:** find actual compatible upstream supply of deionized water, tetrafluoroethylene (or technology-justified Nafion supply), activated carbon, plant electronics and silica. Record source/process UUID, reference product flow UUID, units, location, year, allocator, licence and quality. For an absent identical flow, any replacement requires a **new documented bridge/foreground process** and stoichiometric/mass reconciliation. Never force a different flow UUID simply because the name sounds similar.
2. Resolve the twelve potentially same-flow linked candidates by inspection of their actual producer processes (6 single-source + 6 multi-source **exchanges**, not unique flow counts); only accept scientifically justified process and method.
3. Rank remaining unresolved exchanges by model contribution potential and upstream dependency; classify top material supply-chain cuts vs low-relevance/infrastructural artifacts. No silent impact=0 for missing provider.
4. **Native openLCA execution gate:** install/import exactly this ZIP into openLCA 2 with IPCC/AR6-100, build a process-linked 1 kg H₂ product system; validate database, providers and flow coverage before running any production GWP. Run actual IPC, record native impact result and contribution analysis, *then* sensitivity and comparison with existing 2023 Dutch electricity supply screen.
5. **Dutch geographical/physical scope:** Dutch 2023 grid/offshore wind supply and 125 MW simplified PyNEXUS PEM model differ from US 2017 process. Treat US result only as an explicitly labeled geography/technology sensitivity, do not call it the observed Dutch plant's real life-cycle inventory. E/E+S deliver different service and need matched-service sensitivity for comparative claims.

## 7. Acceptance gates and repo evidence

- [x] G1 Exact Commons Merged source acquired by public API and SHA pinned
- [x] G2 Actual 1 kg source process UUID and 2017 US inventory identified
- [x] G3 Actual supplier UUID graph and missing exchanges quantified
- [x] G4 IPCC/AR6-100 method UUID and matched 134 factor-flow references identified
- [ ] G5 Complete appropriate upstream supplier/bridge graph, separately justified geography and product gate
- [ ] G6 Execute an actual **native openLCA provider-linked** LCIA and compare to independent checks
- [ ] G7 Peer-review-readiness: uncertainties, process completeness, allocation, data licence and interpretation

### Code and artifacts

- [Source downloader](../src/ptxlens/commons_public.py)
- [Actual provider/LCIA method graph](../src/ptxlens/commons_jsonld_audit.py)
- [Full missing-links matrix and grouped flow CSV](../src/ptxlens/commons_gaps.py)
- [Live material search and coverage](../src/ptxlens/provider_coverage.py)
- [Original USLCI reference model](../data/lci/uslci_pem_reference_2017.json)
- [Existing PyNEXUS electricity-supply GWP screen](LCA_2023_METHODS_RESULTS.md)
- [Existing native IPC integration and controls](OPENLCA_EXECUTION.md)

Research code is AI-assisted and requires scientific review. No confidential industrial or proprietary database products are published.
