# PtXLens — source-verified Power-to-X economics and environmental assessment

**Research status (13 Nov 2026): real-data provenance and a genuine OpenPyTEA cost-component calculation completed; full LCOH and process-based LCA not yet completed.** The original source PyNEXUS model is unchanged.

## Executed work, not mock data

| Gate | Status | Evidence |
|---|---|---|
| Dutch 2023 A44 wholesale price, 8760 real UTC hours | **Passed** | [live Fraunhofer/SMARD API CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43417523516) |
| Frozen PyNEXUS 2023 E and E+S archives, 17520 Stage B hours | **Passed** | [original ZIP re-download, hashes and numerical audit](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43418772493) |
| OpenPyTEA 3.2.2 + DOE 2024-source 2022-USD electrolyser installed CAPEX | **Passed: capital only** | [real OpenPyTEA execution + independently reconstructed cashflows](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43418299360) |
| openLCA 2 connected process database, real linked providers and LCIA GWP100 | **Blocked** | [exact execution and database requirements](docs/OPENLCA_EXECUTION.md) |
| Complete, comparable and source-normalized hydrogen LCOH | **Blocked** | wind, storage, grid tariffs, complete OPEX, currency-year and project-service boundary |
| Full life-cycle-emissions-constrained MILP / Pareto front | **Not yet demonstrated** | Future verified frontier work |

Actual OpenPyTEA 2022-USD **electrolyser capital-only** results in the published $2000/kW installed cost case and a separate *analyst* 8% rate are **$1.55815/kg** (E) and **$1.52603/kg** (E+S). The scenarios have *different* delivered H2. These costs **exclude** electricity, storage and other plant components; they are **not LCOH**. DOE system electricity consumption and the simplified PyNEXUS electrolyser performance are distinct technology assumptions.

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
