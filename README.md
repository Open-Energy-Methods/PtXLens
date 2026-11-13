# PtXLens — source-verified Power-to-X economics and environmental assessment

## Latest scientific result — genuine native BAFU:2026 v1.1 30-bar PEM E/E+S GWP100

Using the **user-provided real BAFU v1.1 native openLCA database**, the actual GreenDelta openLCA 2.7 Java engine and UMFPACK sparse solver have now produced independently checked **IPCC 2021 / IPCC 2021 GWP 100** results from native, closed supplier process systems:

| Native BAFU v1.1, kgCO₂e/kg H₂ | GWP100 | Linked processes | Unlinked product/waste exchanges |
|---|---:|---:|---:|
| Original Swiss 30-bar PEM reference | **5.541965562** | 4,235 | 0 / 0 |
| **E**, original 2023 NL-model electricity reparameterization | **6.148174396** | 4,240 | 0 / 0 |
| **E+S**, original 2023 NL-model electricity reparameterization | **6.076552654** | 4,240 | 0 / 0 |

All native results agree with independent source-factor reconstructions using the uploaded **corrected BAFU v1** LCIA to within ~2.2×10⁻⁸ kgCO₂e/kg H₂. Original data: 2023 PyNEXUS real observed NL market and ERA5-derived wind inputs, with **modelled (not metered) hydrogen operation**. The raw licensed BAFU v1.1 database and v1 source files remain **outside GitHub**.

**Crucial scope restriction:** E+S has **20,000 kg additional configured hydrogen storage capacity** (40,000 vs E 20,000 kg), but a validated *physical* storage vessel, compressor, losses and extra infrastructure inventory is **not included**. The BAFU offshore-wind reference is an old 2MW "xx" process and E/E+S H₂ delivery differs. These are genuine native GWP100 results for **scoped BAFU-reference 30-bar PEM systems with source-grounded Dutch electricity/water substitutions**, not a completed matched-service industrial E vs E+S cradle-to-gate comparison. **Do not present E+S as environmentally superior from the intensity difference alone.**

[Full reproducible source and native calculation methodology](docs/BAFU_2026_V11_NATIVE_2023_DUTCH_E_ES_VERIFIED.md) · [Remaining equipment/service gates](https://github.com/Open-Energy-Methods/PtXLens/issues/2)



## BAFU:2026 — Swiss official full GWP100 process catalogue and Dutch original E/E+S work

The **official Swiss Federal Office for the Environment (BAFU:2026 v1) public API** has been queried live for all **11,947 real process-reference IPCC 2021 GWP100 results** over 16 complete UUID partitions. Records include exact source UUIDs, names, country, units, edition and source provenance. [Successful full source ingest](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43441882303).

Using frozen original 8,760-hour PyNEXUS E and E+S dispatch ZIPs, we executed a second independent **BAFU-published-factor electricity-supply component sensitivity**, with source-verified NL high-voltage grid and legacy offshore-wind factors: **5.522554 (E)** and **5.455317 (E+S)** kgCO2e/kg modelled delivered H2. Four of the eight published PEM stack material categories also have source-matched mass-based BAFU reference factors, resulting in strictly **partial material components** only (0.002613 and 0.002559 kgCO2e/kg model H2). Titanium metal production, virgin activated carbon, Nafion precursor, and iridium-bearing concentrate **do not have technology-equivalent verified suppliers**; they were never given zero GWP. [Successful original data CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43443319012).

**These are NOT complete H2 cradle-to-gate LCA results.** The official API exposes pre-calculated BAFU process impact factors, not the native process supplier graph. **Historical preliminary stage:** the BAFU:2026 original native v1.1 zolca was subsequently supplied with user authorization and executed locally; see the latest section above. The local source-archive verifier and the real openLCA 2.7 native BAFU import, supplier graph checks and numerical calculations have since all executed successfully on the authorized v1.1 copy. [Exact source, 30bar PEM benchmark references, methods, limitations and local execution](docs/BAFU_2026_REAL_SOURCE_AND_NATIVE_INTEGRATION.md).



## Native openLCA 2.7.0 engine actually executed

GreenDelta's genuine openLCA **2.7.0** native Java engine has imported the unmodified SHA-verified Federal Commons Merged (2026) ZIP, constructed the real USLCI reference PEM product system (2,516 source processes, 3,077 linked supply exchanges) and run its native IPCC AR6-100 LCIA calculation. [Successful Java kernel run](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43435190584).

**This is an executed diagnostic, NOT a complete or valid Dutch cradle-to-gate footprint**: native auto-linking still leaves **681 nonzero product inputs unlinked**, and the original 2017 U.S. process has a source oxygen-output mass-balance discrepancy (12 kg O2 plus 1 kg H2 out versus 9 kg water in). Its diagnostic 77.616 kg CO2e/kg reference H2 is **not** an approved research finding. An additional real-data Hybrid (USEEIO v2) import reduces original source default-provider gaps only from 695 to 672 and introduces monetary IO assumptions.

Read [complete native execution, IPCC method and supplier-validation evidence](docs/NATIVE_OPENLCA_DIAGNOSTIC_AND_FULL_LCA_GATES.md). No fake GWP coefficients or generic missing-provider=zero treatment are accepted as a completed PtXLens study.


## Commons Merged real-background audit — November 2026

The **authentic Federal LCA Commons Merged 2026 openLCA JSON-LD archive** (51,012,635 bytes, SHA256 `1ded185617d4de67f8ed6933c473a68d65c232dd738779179e8559a31dfd056d`) is now reproducibly downloadable without an API key. The actual 1 kg PEM-hydrogen USLCI unit process and IPCC **AR6-100 method with 134 matching characterization-flow references** were identified. The exact supplier graph still has **695 unresolved upstream input exchanges (683 without any same-flow output supplier; 12 with candidate suppliers requiring review)**, including deionized water and PEM-stack precursor flows. **This earlier Commons-only LCA had unresolved links**; subsequently the legitimate BAFU v1.1 native model was obtained and executed with zero unlinked product/waste exchanges (see current BAFU section).

Read [the actual background database / missing-provider research audit](docs/COMMONS_MERGED_2026_PROVIDER_AUDIT.md). [Source acquisition and provider graph CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43432287400).


**Research status (13 Nov 2026): real-source native BAFU v1.1 provider-linked reference and scoped Dutch E/E+S IPCC GWP100 calculations completed, original model provenance audited; full matched-service E/E+S storage-equipment cradle-to-gate comparison and complete LCOH not yet completed.** The original source PyNEXUS model is unchanged.

## Executed work, not mock data

| Gate | Status | Evidence |
|---|---|---|
| Dutch 2023 A44 wholesale price, 8760 real UTC hours | **Passed** | [live Fraunhofer/SMARD API CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43417523516) |
| Frozen PyNEXUS 2023 E and E+S archives, 17520 Stage B hours | **Passed** | [original ZIP re-download, hashes and numerical audit](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43418772493) |
| OpenPyTEA 3.2.2 + DOE 2024-source 2022-USD electrolyser installed CAPEX | **Passed: capital only** | [real OpenPyTEA execution + independently reconstructed cashflows](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43418299360) |
| 2023 Dutch energy-supply GWP (historical dispatch, sourced lifecycle factors) | **Passed — electricity supply only** | [real-data LCA results & methods](docs/LCA_2023_METHODS_RESULTS.md), [17,520-hour CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43424086998) |
| Published PEM 1MW stack materials foreground + declared model allocation | **Passed — LCI only** | [1MW stack 2024 thesis source](data/lci/pem_stack_kanz_2024_1mw.json), [CI](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43425080024) |
| Native openLCA provider-linked BAFU v1.1 reference, E and E+S 30bar PEM GWP100 | **Passed — scoped native LCA** | [actual calculations and limitations](docs/BAFU_2026_V11_NATIVE_2023_DUTCH_E_ES_VERIFIED.md); complete additional storage/compression and matched-service comparison still pending |
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

**Native openLCA LCIA is now executed:** the authorized BAFU v1.1 process database and exact `IPCC 2021 GWP 100` method produced the reference and E/E+S scoped numerical results above, with zero unlinked product/waste exchanges. [Older IPC procedure](docs/OPENLCA_EXECUTION.md) remains available; native Java execution was used here to solve the large matrix with the real UMFPACK sparse solver. Full plant-specific storage/compression and matched-service physical boundaries remain unresolved.

## Scope and safety

- External history: actual 2023 ERA5-derived wind and NL ENTSO-E/SMARD electricity prices; simulated hydrogen dispatch and delivery, not actual equipment telemetry.
- Published DOE CAPEX benchmarks: **2022 USD**. Dutch settlement: **2023 EUR**. Do not sum or compare without sourced FX/price-year harmonization.
- Users can execute the original four-hour invented fixture under examples/ to test arithmetic only. It is **not a scientific research dataset**, and tests must never be presented as findings.
- No restricted LCI/economic database included; exact EXIOBASE 3.8 versus 3.9+ licence differs. OpenLCA process providers and database licences require separate review.
- No full LCA, industrial validation, ISO 14044 conformity, industrially validated investment decision, or commercial process simulator use claimed.
- AI-assisted implementation with independent numerical checks and necessary scientific review.

Related: [PtXFlex](https://github.com/Open-Energy-Methods/PtXFlex), an independently gated e-methanol MILP with separate original historical-market/wind input ingestion.
