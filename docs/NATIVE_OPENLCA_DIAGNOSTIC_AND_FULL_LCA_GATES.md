# Native openLCA 2.7.0 execution, source completeness and next closure gates

**13 November 2026. Status: actual native openLCA engine calculation executed, but the reference source is not a complete scientifically valid Dutch 2023 PEM hydrogen life-cycle inventory. No full cradle-to-gate result is approved.**

## Executed unmodified original source in actual openLCA

- Engine: GreenDelta openLCA **2.7.0**, real Java \`org.openlca:olca-core:2.7.0\`, fetched from Maven Central (MPL 2.0). This is **not** a homemade emissions multiplication, a mock, or merely the olca-ipc Python client; it uses the actual openLCA JSON-LD importer, Derby database, provider linker, matrix calculator and IPCC characterization method.
- Source: Federal LCA Commons 2026 Commons Merged archive, 51,012,635 bytes, SHA256 \`1ded185617d4de67f8ed6933c473a68d65c232dd738779179e8559a31dfd056d\`; source archive re-downloaded and byte verified. Not repackaged or re-distributed.
- Source process: USLCI \`f00a298a-295f-4fbc-b463-45f8e96f018b\`, \`Hydrogen; proton exchange membrane water electrolysis; at plant\`, from the original USA/2017 representative reference (process technology adapted from Bareiß et al.), NOT an industrial 2023 Netherlands plant.
- Method: \`IPCC\`, category \`AR6-100\`, method UUID \`00feb6d9-9282-3bcf-9d18-7b040f516935\`; category UUID \`a6206006-65bc-395c-8dc9-f12262f45a04\`. All 134 factor references resolve to elementary flows of process-only Commons Merged.
- [Native engine GitHub run](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43435190584): genuine successful Java compilation/import and matrix calculation.
- Native imported processes: **2,516**. Native product system contains **3,077 supply process links** and **1,058 processes** (different from the upstream JSON-LD default-provider graph because the native system builder can find extra suppliers).
- Native **diagnostic** IPCC AR6-100: **77.6161461819 kg CO2e per 1 kg source-reference H2**. This is a partial, *source-incomplete* model output. **DO NOT cite it as a measured, complete, Dutch, product-level or comparative LCA footprint.** Any apparently meaningful raw result is invalid for a complete-coverage claim until the provider graph is repaired and characterized flows are validated.

## Automatic linking still does not close the source

The original SHA-pinned source graph recorded **695 unlinked upstream exchanges across 265 distinct input-flow UUIDs**, with **683** exchanges lacking any same-flow output producer in the process-only archive.

A second actual native-engine run using the same original archive [verified automatic source linking](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43435753386): **681 unlinked, nonzero product-input exchanges remain after native product-system construction**. This is not simply a missing CSV header or a generic software setup problem. The mathematical solve can produce a diagnostic score with some suppliers missing, but cannot infer their omitted production impacts.

Examples of source-inventory blockers: deionized process water, tetrafluoroethylene membrane precursor, activated carbon, electronic components, silica gel; the full source-UUID audit includes raw consumption-process context and counts. None can be assigned zero GWP merely because a supplier was not available.

## Published foreground stoichiometry mismatch

The actual reference process contains **9 kg deionized water input, 1 kg H2 output and 12 kg oxygen output** per reference kg hydrogen. Independent ideal electrolysis chemistry, \`2 H2O -> 2 H2 + O2\`, implies ~**7.936 kg O2** and **8.936 kg reacted H2O** per kg H2 (using H 1.008, O 15.999). The source oxygen output therefore exceeds the basic reaction mass balance by ~**4.064 kg oxygen** (and total outputs exceed water input by 4 kg). The source is NOT silently corrected; the difference must be explained by verified source documentation / an additional oxygen source or an original dataset correction. This is a second, independent reason to withhold complete-LCA claims. [Live actual-process source audit](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43430644840); [science QA code](../src/ptxlens/lca_source_quality.py).

## Also examined: Commons Merged Hybrid (USEEIO v2)

- Public archived source acquired separately and SHA pinned to \`68112d3b17eb12f552f597b06d79627d6f1413c68a641c3268d384788853e6e6\`, size 78,748,123 bytes, 13,136 original entries.
- Original 2026 hybrid source contains ~2,931 unique process UUIDs, ~9,005 unique flow UUIDs, and a native IPCC AR6-100 category with **137** flow-mapped factors.
- [Executed source/provider audit](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43436516195): **672** missing default-provider exchanges (660 without any same-flow supplier; 12 with same-flow candidate matches). This is **23 fewer** than the base 695 in a different reachable graph; 672 is *still* far from complete. It is not evidence that USEEIO entirely solves the manufacturing supply chain, nor does USEEIO automatically represent the Netherlands.
- USEEIO bridges represent **US monetary input-output sector data** and process models together. Never describe their effects as process-only cradle-to-gate LCA or count them twice with the original equipment materials.

## What it takes to complete a legitimate Netherlands cradle-to-gate model

1. **Select and version a complete background**. Candidate priority: [Swiss Federal BAFU:2026 v1](https://www.openlca.org/bafu2026-version-1-is-now-available-on-nexus/) — free, approximately 12,000 unit-process inventories, but its terms require acceptance and citation; the user must obtain it from Nexus under the applicable terms. A departmentally licensed ecoinvent database is another option. No licence conditions are bypassed or automatically accepted. Generic US hybrid is not a geographic substitute.
2. **Verify provider links** for every material, deionized water, chemical precursor, BoP and manufacturing input; actual process/flow UUID and appropriate exchange units, provider geography, source age, allocation method, licence and source are required. Explicit mass/process bridge models can be constructed from published source facts but not by inventing impacts. Prioritize the first-order water/stack/BOP gaps, then the whole extended graph.
3. **Fix or justify the published oxygen mass imbalance** from primary documentation. Do not silently swap 12 kg for 8 kg just to make a numerical result more attractive.
4. **Define the functional unit physically**: delivered H2 pressure, purity, compression/water conditioning and location. The actual PyNEXUS source models simulated H2 from real weather/market inputs and does not validate a commissioned electrolyser.
5. **Derive versioned E/E+S source inputs** from the frozen original PyNEXUS archives and preserve hourly grid/wind allocation. Do not reuse U.S. 2017 grid electricity as the Netherlands 2023 grid.
6. **Build 1 kg linked foreground** and run real native openLCA against named, compatible IPCC GWP100. Export native result and contribution analysis; add an independently reconstructed material/mass ledger and verified 0 unresolved material supplier impacts. A run of the solver alone is insufficient.
7. **Compare carefully**: E and E+S deliver different H2 quantities; use matching system boundaries and matched service for a comparative assertion. Preserve unadjusted inputs, outputs and uncertainties.

## How to reproduce the native diagnostic

~~~bash
# Requires Java 25 / Maven / Python 3.12 and network access to public FLCAC
python -m pip install -e .
python -m ptxlens.commons_public \
  --repository commons_merged \
  --archive /tmp/commons_original.zip \
  --manifest /tmp/source_manifest.json

mvn --batch-mode -ntp -f native-openlca/pom.xml \
  -Dexec.mainClass=org.openenergymethods.ptxlens.DiagnosticNativeCalculation \
  -Dexec.args="/tmp/commons_original.zip /tmp/native_db_please_create_new" \
  compile exec:java
~~~

This is an **original-source diagnostic**, NOT an author-approved full hydrogen footprint. GitHub CI retains the numerical log, source provenance, post-link QA and an explicitly incomplete claims manifest. Core unit tests, API contract checks and ZIP source fingerprints are separate.

Software: MIT (original PtXLens code), native engine MPL-2.0 with upstream dependencies. Published LCI database, process sources and imported BAFU/economic data retain their own use and distribution terms.
