# L3-D — historical observed-price/wind matched-H2 storage DCF: complete method and conditional source-year investment ceilings

**Programme:** OEM-PTX-2026-01 · **Checkpoint:** 15 November 2026 · **Tool:** src/ptxlens/l3d_historical_source_dcf.py · **Primary source:** Open-Energy-Methods/PtXFlex research/F3D_ARCO_2022_2024_PUBLIC_VERIFIED_AGGREGATES_v1.json, Git blob `ca07f5ef1e381fa157982bc5a68e46ce3022003a`, source-data publication commit `bdf82be`. **Nature of the result:** CONDITIONAL source-year purchasing-power theoretical DCF, not manufacturer/installation procurement and not a real project investment decision.

## 1. Incremental economic boundary

This module compares only **E+S source-model storage dispatch versus E source-model dispatch under identical hourly H2 supply** within each original 2022/2024 source year and each separately defined pressure-storage capacity interpretation. It uses the 2022/2024 NL ENTSO-E A44 nominal hourly market prices and offshore Copernicus ERA5 ARCO weather-derived source model results **already physically audited at 8,760h / 8,784h**, including pressure/EOS and electricity compressor duty.

There are **four separate annual historical model results**, not a future 2022–2024–2025 operating trajectory, and no probability weights for the historical years. The selected annual H2 product is not the nominal industrial 50t/day contract: it is approximately **30–31t/day**. One cannot mix a gross 2022 saving with a usable 2024 saving as if they have the same annual H2 output, electricity price year, equipment pressure rating, or storage semantics.

The four potential operating benefits are the original *net wholesale grid electricity expense differences* (E minus E+S), not physical storage revenues, whole-factory margins, net hydrogen LCOH savings or future power-price forecasts. The original model's source-evidenced E+S 2024 net grid cost can be **negative**, because modelled electricity export credit exceeds cost; that is not independently verified market revenue.

## 2. Money bases, cash flow timing and formula

For a given historical source year y and capacity definition m, let S(y,m) be the observed-calendar **modelled annual** wholesale electricity cost advantage. Define an entirely hypothetical same-source-year purchasing-power economic environment, and let the annual persistence factor k >= 0, annual performance/benefit decay d in [0,1], extra annual fixed OPEX O >= 0, all-in initial installed storage CAPEX I0 >= 0, replacement expenditure R(t) >= 0 at explicitly specified year-end t, terminal salvage V and decommission D. For N years at real discount rate r >= 0:

    Incremental NPV = -I0
                    + sum(t=1..N) [S(y,m)*k*(1-d)^(t-1) - O - R(t)]/(1+r)^t
                    + (V-D)/(1+r)^N.

The reported zero-NPV threshold **maximum initial additional all-in storage CAPEX** is exactly the discounted sum excluding the -I0 expenditure. The *constant annual extra OPEX break-even threshold at a chosen initial CAPEX* is the remaining present-value headroom divided by the discount annuity factor. Negative ceilings are reported as negative, not clipped or misrepresented as an achievable break-even at zero cost.

No tax, financing debt, accelerated depreciation, contractor margins, site-specific availability, hydrogen sales premium, new contract price, steam heat revenue, infrastructure tariff, site plant license, CPI deflator or cross-year EUR equivalence has been inferred. These are original 2022- or 2024-source-year purchasing-power **scenario units**, not harmonized 2026 real euros. All money assumptions and cashflows must be consistently converted to a common base year **before** real procurement or prospective project finance comparison.

## 3. Original evidence + illustrative central capital-budget ceilings

The following 20-year/8% real-rate sensitivity columns are derived *arithmetically from the published four source-year savings and an exact discount annuity*; they are NOT measured capital costs or estimates from manufacturers. Case A assumes **zero additional annual storage OPEX/replacement**, an optimistic theoretical maximum. Case B assumes **analyst-only EUR250,000 annual incremental OPEX and a EUR1,000,000 extra end-year-10 replacement** (also optimistic because it excludes other BoP unknowns).

| Historical nominal EUR year | Original storage capacity semantics | Source operating saving EUR/year | Modelled matched H2 t/day | Case A theoretical extra CAPEX ceiling EUR | Case B theoretical extra CAPEX ceiling EUR |
|---|---|---:|---:|---:|---:|
| 2022 | max_inventory | 3905632.94 | 30.481 | 38346079.89 | 35428349.55 |
| 2022 | usable_service | 3903807.25 | 30.884 | 38328155.00 | 35410424.66 |
| 2024 | max_inventory | 2247126.18 | 30.748 | 22062616.05 | 19144885.71 |
| 2024 | usable_service | 2206233.52 | 31.006 | 21661125.92 | 18743395.58 |

These are four **independent source-year thought experiments**: a CAPEX ceiling in 2022-source-year EUR must not be directly compared with a tank-only 2024 reference price without a properly documented inflation basis; the original source-model H2 output is different, and the 2023 historical L3-A model has its own distinct much larger original source H2 target. Therefore these do **not** constitute a 3-year statistical envelope nor three successive positive annual investment flows.

The gross 20t→40t incremental empty reference pressure-vessel hardware is **802 additional published 2400kg EMPTY vessels = 1,924,800kg empty equipment**; the usable convention has **902 = 2,164,800kg empty equipment**. Prior peer-reviewed Type I nominal 200-bar gauge cost reference €222/kg *rated nominal gas capacity* was harmonized to **2024 EUR**, giving **€4.629144m / €5.206344m tank-only**. Those numbers are neither site-representative 200-bar(a) hardware quotations nor all-in installed prices; they omit major 18 non-vessel hardware/BoP categories and compatible native BAFU manufacturing LCI, and cannot be used to assert investment viability from the columns above.

## 4. Reproducibility, controlled sensitivity and independent numerical uncertainty

Input is a **hard-pinned original Git blob** of the four-case audited source results. The loader fails closed on changed source bytes, missing original 2023 ARCO/CDS reproduction, wrong leap-year length, changing price/wind provider SHA across semantics within one year, different H2 mass for E and E+S, missing independent physical replay, malformed savings arithmetic or solver reported 1e-6 cost gap/bounds. No original licensed hourly source data are imported or republished by L3-D.

The implementation propagates source HiGHS-reported annual cost-bound endpoints into a DCF NPV interval by exact monotone cashflow arithmetic. This is a **conditional MILP cost optimization numerical interval**, not a future-power-price distribution or a confidence interval. PtXLens replayed the primal hourly solution; the independent dual construction remains **NOT VERIFIED**.

A deterministic *324-scenario screening matrix* is defined: all four real source-year/mode annual benefits separately crossed with 10/20/30-year horizons, 3%/8%/12% real discount, 0.5x/1.0x/1.5x assumed persistence and EUR0/250k/500k additional annual OPEX, while holding a **hypothetical** EUR1m replacement at year 10 and otherwise zero salvage/decommission. This is a structured sensitivity **grid of analyst-selected assumptions**, NOT a statistical forecast, published procurement budget, or proof of source-market robustness.

To reproduce locally with both sibling repositories checked out:

    cd C:\Users\prasa\OEM_Research\PtXLens
    ..\PtXFlex\.venv\Scripts\python.exe -m pytest -q tests/test_l3d_historical_source_dcf.py
    ..\PtXFlex\.venv\Scripts\python.exe -m ptxlens.l3d_historical_source_dcf --source ..\PtXFlex\research\F3D_ARCO_2022_2024_PUBLIC_VERIFIED_AGGREGATES_v1.json --output-dir data\results

The run writes the full 324-cell machine-readable cashflow sensitivity JSON and a repeatable Markdown report **only after** actual source evidence passes every gate. Do not claim a local run/CI is complete until these tests and generated original-source response files are verified on the Windows machine.

## 5. Remaining release blockers

1. **Real manufacturer procurement:** pressure-rated, temperature/site-certified 20→200bar system BOM and compressor+cold-side duty, actual vessel materials/manufacturing, frames, valves, cooler, control/PED and current vendor budget/quotation with delivery, installation, maintenance, inspection and availability. The OEM enquiry is drafted but not sent.
2. **Verified prospective site/service economics:** actual connection and energy tariffs, market participation/export credits, full hourly hydrogen product contract rather than 30–31t/day modeled reference, H2 losses, forward scenario and financing/tax basis in harmonized price-year EUR.
3. **Independent dual optimality and physical validation:** independent solver reconstruction or primal/dual source proof, real equipment data, time-matched site observations and engineering verification of pressure/compressor model.
4. **Native BAFU:2026 v1.1 inventory:** fixed complete foreground system quantities, manufacturer material breakdown and fabrication yields, 19 native producer/bank equipment categories including 18 unmeasured BoP classes, provider UUID and reference product links, local manufacturing electricity/transport and end of life, matched-service functional unit, independently validated LCIA and GWP.

**Scientific release status:** historical operating numerical subgate PASSED; hypothetical financial methodology implemented but requires local tests; actual CAPEX/OPEX viability, site, full hydrogen contract, native BAFU whole-system LCA and programme v1.0 are **NOT VERIFIED**.
