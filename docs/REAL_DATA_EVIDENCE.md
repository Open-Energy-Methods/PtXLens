# Real-source research evidence register — 13 November 2026

The invented 4-hour input is confined to unit testing. It is never called a research result.

## Original observed 2023 NL source from PyNEXUS

Frozen source: https://github.com/abhijith-sivaprasadan/PyNEXUS
Original 17-case run: https://github.com/abhijith-sivaprasadan/PyNEXUS/actions/runs/40229852457
Independent PtXLens source re-audit passed: https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43418772493

Two exact archived ZIPs are pinned by SHA256 inside src/ptxlens/observed.py: E artifact ID 12612294862 and E+S artifact ID 12613045475. The CI re-downloads the **original archives** via GitHub Actions API, byte-verifies both and their Stage B CSVs, verifies 8760 hourly rows per scenario, reconstructs electric and H2 balances and each price-times-net-grid-settlement objective. No edits to the original frozen PyNEXUS repo.

| 2023 observed-price model output | E | E+S |
|---|---:|---:|
| Delivered H2 (million kg) | 16.3353 | 16.6791 |
| Unserved demand (million kg) | 1.9147 | 1.5709 |
| Electrolyser input (MWh) | 774961 | 791525 |
| Wholesale electricity settlement (2023 EUR) | 25748968.93 | 27508060.36 |

E+S delivers 343792.77 kg more modeled H2 at 1759091.43 EUR greater net wholesale settlement. NOT matched service and NOT a full hydrogen cost/LCOH. The dispatch represents a computational model using verified real input weather/market prices, **not instrumented plant operation**.

Original GitHub Actions source artifacts expire on 24 December 2026. Preserve unaltered ZIPs and checksums outside ephemeral Actions storage.

## Independent API verification: actual NL 2023 hourly prices

Fraunhofer ISE Energy-Charts API: https://api.energy-charts.info/price?bzn=NL&start=2023-01-01T00%3A00Z&end=2024-01-01T00%3A00Z

Provider licence in downloaded source metadata: CC BY 4.0, Bundesnetzagentur/SMARD; attribution to Fraunhofer ISE Energy-Charts. Actual live GitHub Actions 8760-hour API execution: https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43417523516 .

Downloaded source has 8760 distinct UTC hours, finite EUR/MWh and source+CSV checksums. A separate full-length comparison against original PyNEXUS 2023 observed prices recorded **zero numeric mismatches**. Never describe a price feed as an emissions-factor feed.

## Real OpenPyTEA against published DOE capital assumptions

Primary source, DOE Program Record 24005, May 2024:
https://www.hydrogen.energy.gov/docs/hydrogenprogramlibraries/pdfs/24005-clean-hydrogen-production-cost-pem-electrolyzer.pdf

DOE gives installed PEM CAPEX 1500, 2000 or 2500 USD per kW in **2022 USD**, 30-year system lifetime and stack replacement after 40000 operating hours at 11% of CAPEX. The system reference consumption of approximately 57 kWh per kg differs materially from PyNEXUS's simplified model and must not be conflated.

OpenPyTEA 3.2.2 truly ran with source-pinned 2023 PyNEXUS modeled delivered H2 and operating hours, using 2000 USD2022 per kW and a separate analyst 8% real discount-rate sensitivity. It repeats observed-input 2023 modelled operation for 30 years as an explicit sensitivity, not a 30-year forecast. CAPEX year indexing is 1-based, initial and replacement spending independently cross-checked.

| Capital-only benchmark (2022 USD/kg delivered) | E | E+S |
|---|---:|---:|
| Actual OpenPyTEA run | 1.558145 | 1.526028 |
| Independent discounted-cash-flow cross-check | 1.558145 | 1.526028 |

Successful real external software CI: https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43418299360 .

**NOT LCOH**: wind and storage CAPEX, electricity, other plant OPEX, grid tariffs, compression, financing and many other items are omitted. Do not add this 2022 USD component to 2023 EUR electricity settlements without sourced FX/inflation conversions. No independently measured industrial performance is claimed.

## LCA remains uncalculated

Actual openLCA IPC interface exists, but no connected, physically complete foreground plus licensed background plus named compatible GWP100 characterization method has been provided; **there is no completed LCIA score**.

Free official public LCI access: https://www.lcacommons.gov/quick-start-guide
USLCI openLCA 2 data: https://www.lcacommons.gov/lca-collaboration/National_Renewable_Energy_Laboratory/USLCI_Database_Public
Federal LCA Commons API: https://www.lcacommons.gov/lca-commons-api-guide (free API key required; demo key available for exploration).
OpenLCA Nexus free/paid data and method: https://www.openlca.org/data/

The USLCI US-background is not a geographically representative Dutch electricity mix. Use it for a documented software exercise only, unless transparent regional data adjustments and uncertainties are justified. Do not count user-supplied factors as a completed provider-linked LCA.

See OPENLCA_EXECUTION.md for the actual process-gated methodology.
