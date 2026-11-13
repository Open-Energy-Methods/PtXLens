# PtXLens — source-verified Power-to-X economics and environmental assessment
## Commons Merged real-background audit — November 2026

The **authentic Federal LCA Commons Merged 2026 openLCA JSON-LD archive** (51,012,635 bytes, SHA256 `1ded185617d4de67f8ed6933c473a68d65c232dd738779179e8559a31dfd056d`) is now reproducibly downloadable without an API key. The actual 1 kg PEM-hydrogen USLCI unit process and IPCC **AR6-100 method with 134 matching characterization-flow references** were identified. The exact supplier graph still has **695 unresolved upstream input exchanges (683 without any same-flow output supplier; 12 with candidate suppliers requiring review)**, including deionized water and PEM-stack precursor flows. **Native openLCA cradle-to-gate LCIA remains blocked; no full GWP value is claimed.**

Read [the actual background database / missing-provider research audit](docs/COMMONS_MERGED_2026_PROVIDER_AUDIT.md). [Source acquisition and provider graph CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43432287400).


**Research status (13 Nov 2026): real-data provenance, genuine OpenPyTEA capital calculation, and a reproducible, published-factor electricity-supply life-cycle GWP screening completed; full LCOH and provider-linked process-based cradle-to-gate LCA not yet completed.** The original source PyNEXUS model is unchanged.

## Executed work, not mock data

| Gate | Status | Evidence |
|---|---|---|
| Dutch 2023 A44 wholesale price, 8760 real UTC hours | **Passed** | [live Fraunhofer/SMARD API CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43417523516) |
| Frozen PyNEXUS 2023 E and E+S archives, 17520 Stage B hours | **Passed** | [original ZIP re-download, hashes and numerical audit](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43418772493) |
| OpenPyTEA 3.2.2 + DOE 2024-source 2022-USD electrolyser installed CAPEX | **Passed: capital only** | [real OpenPyTEA execution + independently reconstructed cashflows](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43418299360) |
| 2023 Dutch energy-supply GWP (historical dispatch, sourced lifecycle factors) | **Passed — electricity supply only** | [real-data LCA results & methods](docs/LCA_2023_METHODS_RESULTS.md), [17,520-hour CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43424086998) |
| Published PEM 1MW stack materials foreground + declared model allocation | **Passed — LCI only** | [1MW stack 2024 thesis source](data/lci/pem_stack_kanz_2024_1mw.json), [CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43425080024) |
| openLCA 2 connected process database, real linked providers and LCIA GWP100 | **Blocked** | [exact execution and database requirements](docs/OPENLCA_EXECUTION.md) |
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

For a *genuine* openLCA LCIA, first import a real background process inventory and GWP100 method and build a connected, audited hydrogen foreground. Then run the actual [IPC procedure](docs/OPENLCA_EXECUTION.md) using an openLCA desktop database. There is no fake numerical footprint fallback.

## Scope and safety

- External history: actual 2023 ERA5-derived wind and NL ENTSO-E/SMARD electricity prices; simulated hydrogen dispatch and delivery, not actual equipment telemetry.
- Published DOE CAPEX benchmarks: **2022 USD**. Dutch settlement: **2023 EUR**. Do not sum or compare without sourced FX/price-year harmonization.
- Users can execute the original four-hour invented fixture under examples/ to test arithmetic only. It is **not a scientific research dataset**, and tests must never be presented as findings.
- No restricted LCI/economic database included; exact EXIOBASE 3.8 versus 3.9+ licence differs. OpenLCA process providers and database licences require separate review.
- No full LCA, industrial validation, ISO 14044 conformity, industrially validated investment decision, or commercial process simulator use claimed.
- AI-assisted implementation with independent numerical checks and necessary scientific review.

Related: [PtXFlex](https://github.com/Open-Energy-Methods/PtXFlex), an independently gated e-methanol MILP with separate original historical-market/wind input ingestion.
