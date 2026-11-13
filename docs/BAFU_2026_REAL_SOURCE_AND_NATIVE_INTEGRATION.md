# BAFU:2026 v1 — real-source Dutch PtXLens integration and native openLCA gates

**Research state (13 November 2026):** Official Swiss FOEN BAFU:2026 v1 climate-impact catalogue and reproducible E/E+S electricity/material-component assessments have been executed. The original BAFU Nexus database has **not** been imported as a native product-system database. Full 2023 Netherlands cradle-to-gate H2 LCA is **not yet complete**.

## Primary sources and licensing

The 23 June 2026 BAFU:2026 v1 openLCA release includes original inventory EcoSpold1, reports, IPCC 2021/EF3.1 results and a ready-to-use zolca database: https://www.openlca.org/bafu2026-version-1-is-now-available-on-nexus/

The **Nexus zolca** is free but requires the person downloading to accept its separate Terms of Use. It cannot be acquired here by automatically accepting terms or bypassing login. Citation required: **Database of the Swiss Federal Administration, BAFU:2026, Federal Office for the Environment, 2026**. No original Nexus database should be committed or redistributed.

The Swiss federal government separately publishes **pre-calculated per-process LCIA impact factors** under OGD terms, "Open use. Must provide source", with a free GraphQL API at https://data.bafu.admin.ch/api and documentation at https://data.bafu.admin.ch/en/dataproduct-economy-consumption-lca . This API DOES NOT contain the raw provider-linked product inventory.

## Verified 2026 dataset acquisition

[Successful full 2026 official Swiss API ingestion](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43441882303): **11,947** unique original process UUIDs, all 16 nonoverlapping UUID partitions, exactly version BAFU:2026 v1, method IPCC 2021, category GWP 100, source geographic and functional units and source studies. Each original HTTP result hash and the full original catalogue CSV SHA256 are retained in CI artifacts; no generated/fictitious factor substituted.

Full source and candidate code: [bafu_candidates.py](../src/ptxlens/bafu_candidates.py).

## Real source supplier mapping — actual cases

| Literature PEM stack group or plant input | BAFU v1 source | Region | Unit | Status |
|---|---|---|---|---|
| Aluminium primary | Aluminium, primary, at plant | RER | kg | Comparable provisional source |
| Stainless steel 18/8 | Chromium steel 18/8, at plant | RER | kg | Comparable provisional source |
| Copper | Copper, at regional storage | RER | kg | Comparable provisional source |
| Platinum metal | Platinum, at regional storage | RER | kg | Comparable provisional source |
| Titanium metal | Titanium dioxide and other *non-metal* compounds only | — | — | **Unavailable as suitable metal producer** |
| Activated carbon production | Spent activated-carbon *disposal* only | — | — | **Unavailable as suitable virgin adsorbent producer** |
| Nafion sulfonyl fluoride precursor | Finished Nafion membrane production | RER | kg | **Different product, not interchangeable** |
| Iridium-bearing PGM concentrate | Iridium metal production | GLO | kg | **Different grade/product/mass basis** |
| Dutch high-voltage grid electricity | Electricity, high voltage, at grid | NL | MJ | Source for annual/reference scenario only |
| Offshore wind supply | xx Electricity, at wind power plant 2MW, offshore | OCE | MJ | **Legacy 2 MW model, not actual modern Dutch turbine** |
| Deionised water | Water, deionised, water balance MoeK 2013 | NL | kg | Supplier factor available; 9–10 L/kg H2 only literature assumption |
| Hydrogen process gate | Hydrogen production, gaseous, 30 bar, PEM electrolysis, grid | CH | kg | Published reference process, not Dutch 2023 original |
| Hydrogen storage equipment | High pressure hydrogen storage tank | GLO | kg tank | Needs actual physical vessel design and tank mass |
| Pipeline hydrogen delivery | PEM electrolysis from grid and distributed by pipeline | CH | kg H2 | Different boundary; not automatically combinable with electrolysis + compression |

The exact real process UUID, name, geography and units are verified by code in [bafu_real_screen.py](../src/ptxlens/bafu_real_screen.py), and published factors are read from the actual Swiss API catalogue, never written as assumed numeric constants.

## Source-based 2023 original E/E+S outputs (completed, **not full LCA**)

[Successful 8760-hour source-checked E/E+S numerical execution](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43443319012).

Dutch historical grid MWh + offshore-wind allocated MWh came from SHA-pinned original 2023 PyNEXUS archives. Applied BAFU 2026 IPCC 2021 published grid and legacy 2MW offshore-wind production reference factors, converted from kgCO2e/MJ into kgCO2e/kWh using 3.6 MJ/kWh:

| BAFU:2026 published-factor electricity-supply screening (kgCO2e/kg MODELLED delivered H2) | E | E+S |
|---|---:|---:|
| Electricity supply component | **5.522554** | **5.455317** |

Four source-matched material components of the published 1MW Kanz 2024 PEM stack, scaled to a hypothetical 125MW stack set and repeated 2023 production for 30 years with literature 40,000 operating-hour replacement:

| Four documented materials only (kgCO2e/kg MODELLED delivered H2) | E | E+S |
|---|---:|---:|
| Primary Al, chromium steel 18/8, copper, platinum | **0.002613** | **0.002559** |

The tiny four-material result **omits titanium**, the dominant stack mass, as well as Nafion precursor, activated carbon, iridium concentrate and all plant balance-of-plant, water, storage and compression manufacturing. Neither sum is a complete H2 climate footprint, and no missing flow is assumed to have zero impact. The wind provider is an older source labelled xx. The source H2 delivery differs between cases and is modelled, not measured plant output. The BAFU factors are published 2026 process references, **not actual 2023 hourly marginal GHG intensity**.

The original BAFU also includes independently characterized **30bar PEM hydrogen production and pipeline-delivery processes** useful as geographically and technologically labelled external benchmarks, NOT the calculated result of the Dutch E/E+S product system.

## Native database completion — one original external input is still required

To complete native openLCA, the person legally obtaining BAFU:2026 v1 must:

1. Visit https://nexus.openlca.org/database/BAFU, sign in if prompted, read/accept the applicable BAFU:2026 v1 terms and download the actual release. Extract the inner zolca from the outer ZIP containing reports and EcoSpold if provided.
2. Keep the original zolca in a private folder, **outside public GitHub** (the repository gitignore excludes zolca and original EcoSpold files).
3. Validate the source archive and compute SHA256 on Windows PowerShell, from the PtXLens repository:

   ~~~powershell
   python -m pip install -e .
   python -m ptxlens.bafu_zolca_local "C:\private\BAFU_2026_v1.zolca" --output "outputs\bafu_local\source_fingerprint.json"
   ~~~

4. With Java 25 and Maven available, run the actual openLCA 2.7.0 native Java importer against a **new, not-yet-existing** private Derby directory:

   ~~~powershell
   mvn -f native-openlca/pom.xml -Dexec.mainClass=org.openenergymethods.ptxlens.BafuZolcaAudit -Dexec.args="C:\private\BAFU_2026_v1.zolca C:\private\ptxlens_BAFU_new_db" compile exec:java
   ~~~

   This source audit checks actual BAFU process UUIDs, their reference product flows and units, the IPCC characterization method list, real 30bar PEM process inputs and missing links **after native openLCA product-system auto-linking**. It cannot claim native LCIA before executing the final model.

5. Select real physically compatible foreground supplier flow UUIDs (not just source process names); establish a pressure/purity/energy/water/BoP/stack/tank/transport boundary that matches the original PyNEXUS source.
6. Re-parameterize the real BAFU electrolyser reference product system separately for original E and E+S Dutch historical grid/wind fractions, H2 output and storage; document actual vessel/plant materials, 30year assumptions, stack replacement and missing data, with zero unresolved material provider burdens.
7. Run real native openLCA IPCC GWP100 on those **new linked product systems**, independently check the contribution matrix, mass/energy balance and GWP sensitivity, then run matched-service comparators before reporting complete cradle-to-gate H2 results.

**The native BAFU database was not provided or imported in this session.** The GraphQL source-factor analysis is real and complete as a *partial* scenario assessment; it is not substituted for a linked product-system LCIA.

## Research reporting rule

Keep the BAFU component sensitivities separate from the [Dutch 2023 published default electricity factor assessment](LCA_2023_METHODS_RESULTS.md), the [previous U.S. Commons Merged native-engine diagnostic](NATIVE_OPENLCA_DIAGNOSTIC_AND_FULL_LCA_GATES.md), and any future process-linked BAFU model. Do not mix methodology, geography, lifetime or functional units, or report any of these as metered plant operation or ISO 14044 certification.
