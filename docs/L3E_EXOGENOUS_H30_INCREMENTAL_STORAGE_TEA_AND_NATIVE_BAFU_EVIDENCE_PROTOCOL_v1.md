# L3-E — Exogenous H₂ matched-service incremental storage economics and environmental-inventory evidence

**Protocol version:** 1.0 (research protocol, NOT project scientific v1.0). **Authoring checkpoint:** 16 November 2026. **Status:** implementation and hermetic regression tests committed, original public source numerical evidence independently accepted; new L3-E local computations and regression suite **NOT YET RUN**.

**Scope:** incremental hypothetical stationary Type I pressurised H₂ bank from E nominal 20 tonnes to E+S nominal 40 tonnes under `max_inventory` and original 20–200 bar(a) source-model pressure/duty. Identical exogenous H₂ delivered to both, fixed **30 tonnes/day** at every source-year UTC hour (2022: 10,950,000 kg, 8,760 h; 2024: 10,980,000 kg, 8,784 h), at 90% original source-year *modelled wind ELECTRICAL POWER*. The price and wind source years stay distinct.

## 1. Immutable basis of comparison, independently replayed

Published [original two-year E20t versus E+S40t full-year integer source record](../data/results/F3D_2022_2024_max_inventory_H30_W090_TWO_YEAR_MATCHED_SERVICE_ECONOMICS_v1.json), Git blob `c24b4cb0d6a409798c8a7e764965fffd51478a77`, is the **only** annual avoided power cost input. The individual original-source public E/ES 2022 and 2024 physical/energy/EOS replay JSON Git blobs are respectively `0ef8966342b516d94ee6b7ce6223cb8fe6a535b0` and `c702bf79f826fc28def0e60a5d2c0537241961ac`. These are held apart from the private provider hourly arrays and private complete 8-field original hourly MILP dispatch witnesses.

| Evidence from published original source-year model | 2022 | 2024 |
|---|---:|---:|
| Fixed H₂ delivery, t/day | 30 | 30 |
| Total delivered, kg | 10,950,000 | 10,980,000 |
| E20t modelled signed wholesale electricity cost, nominal original EUR | 32,160,567.931485903 | 2,544,581.872826561 |
| E+S40t modelled signed wholesale electricity cost, nominal original EUR | 28,878,954.877419014 | 612,906.0201971165 |
| **E−E+S annual modelled avoided wholesale cost, nominal source EUR** | **3,281,613.054066889** | **1,931,675.8526294443** |
| Independent hour-by-hour original H₂/electricity/EOS integer primal replay | PASS | PASS |
| Source HiGHS original solver-relative MIP gap | ≤1e−6 | ≤1e−6 |

These savings are **not** manufacturer revenue projections, renewable-energy/carbon credits, exogenous electricity forecasts or complete H₂ plant profits. The historic year-specific monetary unit is *not* silently made inflation-adjusted 2026 EUR, and the two historical years do not form a reliable stochastic distribution.

## 2. Conditional CAPEX/OPEX break-even equation

The new [L3-E source-hash-locked DCF model](../src/ptxlens/l3e_exogenous_incremental_dcf.py) returns a *conditional upper bound* on all-in incremental upfront installed CAPEX, not an investment recommendation. For an analyst-disclosed scenario with horizon `N`, annual net WHOLESALE electricity saving `S_year` from ONE original source year, hypothetical repeat fraction `k`, annual savings degradation `g`, constant additional annual OPEX `O`, real discount `r`, replacement payments `R_t`, salvage `V_N` and terminal decommission cost `D_N`:

\[
C_{\max} = \sum_{t=1}^{N} \frac{k S_{\mathrm{year}}(1-g)^{t-1}-O-R_t}{(1+r)^t} + \frac{V_N-D_N}{(1+r)^N}.
\]

- The additional all-in CAPEX `C` is paid at `t=0`; the scenario incremental NPV is `C_max − C`. A **negative** `C_max` means not even zero nonnegative incremental CAPEX is covered under the specified assumptions.
- Annual revenues/savings, OPEX and replacement costs are end-year cash flows; replacements at explicitly specified year ends, no hidden residual credit, no site tax/depreciation/financing or inflation forecast.
- The companion uniform annual incremental-OPEX break-even at a *hypothetical* initial CAPEX `C` is

\[
O_{\max}(C) =
\frac{\sum_{t=1}^{N}\frac{k S_{\mathrm{year}}(1-g)^{t-1}-R_t}{(1+r)^t}
+\frac{V_N-D_N}{(1+r)^N}-C}{
\sum_{t=1}^{N}(1+r)^{-t}}.
\]

- The original HiGHS source-only savings lower and upper values are propagated monotonically to cost frontiers **solely as numerical MIP optimization bounds**, not uncertainty or market-confidence intervals.
- Results are calculated **separately for 2022-like and 2024-like hypothetical constant purchasing-power yearly cashflows**; there is NO weighted average, invented recurrence probability, mixing of nominal EUR across years or assertion of sustained price conditions.

Predeclared DCF grid: horizons **10/20/25 years**, real discount **3/8/12%**, annual repeat multipliers **0.50/0.75/1.00**, yearly saving fade **0/2%**, added incremental annual OPEX **€0/€250,000/€500,000 in that historic year's hypothetical purchasing-power units**. **324** paired per-year scenarios in total. Initial CAPEX **€10 million** appears only in the *inverse OPEX and illustrative NPV calculation*, never as verified installed manufacturer cost. Default grid assumes no replacements; explicit 20-year benchmark subtracts a **hypothetical €1 million replacement paid at END of year 10**, solely for sensitivity.

**Independent arithmetic illustration (no site or vendor estimate):** at 20y, 8% real rate, k=1, g=0, added annual OPEX €250,000, no replacements or terminal residual, annuity PV factor 9.818147407449:

| 20-year conditional CAPEX ceiling | 2022-like original EUR | 2024-like original EUR |
|---|---:|---:|
| No replacement payments | €29,764,823.85 | €16,510,941.41 |
| Additional hypothetical €1 million end-year-10 replacement | €29,301,630.36 | €16,047,747.92 |

**These thresholds are conditional mathematics, NOT evidence that a manufacturer can deliver the extra storage bank for less than the ceiling, or that the original source-market price regime repeats for 20 years.** Installed CAPEX, recurring BoP OPEX, realistic replacement/degradation, site contracting and real financing remain UNKNOWN.

## 3. Incremental 19-category physical equipment specification, quote intake

[Existing source-verified F2 Type I pressure-reference BOM](../data/results/F2_L1_2023_source_incremental_20t_to_40t_stationary_typeI_200bar_BOM_SCOPE_NOT_complete_native_LCI.json), source Git blob `424a8f738cb9caa2d05c1ec5c22cbf6cdd601b82`, contains **19 incremental physical scope categories**. [L3-E physical/BAFU foreground intake](../src/ptxlens/l3e_exogenous_incremental_hardware_lci.py) identifies *every* category and its missing quantities, manufacturer price and process-unit evidence. [PtXFlex matching manufacturer intake](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/src/ptxflex/f2l3e_exogenous_vendor_cost_intake.py) provides the separate original-source 19-line quote and data-sheet questionnaire.

The historical **2023 F2 technical reference** includes a nominal extra 20t storage capacity and the paper-based reference geometric vessel count **802 × 2,400 kg = 1,924,800 kg of EMPTY reference vessel equipment** under max_inventory. Actual installed equipment quantity, certified vessel layout, minimum/design pressure, alloy/part and BOM mass, raw material purchase mass, manufacturing scrap and coatings are **NOT** identified by that figure. The number **MUST NOT** be used as 1,924,800kg virgin steel or substituted for BAFU provider activity mass, and must not be treated as an OEM certified 2022/2024 site layout. The earlier F2 reference establishes only a modelled pressure-swing screen.

The remaining categories require original engineering/vendor evidence, including steel/alloy material grade, rack frames and anchors, high-pressure manifolds, isolation/check valves and filters, regulation/delivery piping, pressure relief and venting, compressor reciprocating heads/seals and driver, VFD/motor, intercoolers/aftercoolers and cooling pumps/fans, gas-quality/drying/sampling, instrumentation, leak detection/ESD/ATEX, civil foundations, in-service testing and inspections, transport/installation, disposal/reuse and end-of-life. Do NOT assume every category creates a new independently priced item: manufacturer quotes must segregate package price from bills of materials, avoid double-counting alloy material already contained in an OEM vessel quote, and separate initial CAPEX, recurrent OPEX, replacement CAPEX and terminal liabilities. An omitted item requires a signed engineering exclusion, **not automatic zero material/cost**.

Supplier evidence must include actual product scope/revision/pressure basis, documented bill of quantities, contract locality/date/quote terms, evidence hashes retained privately and corresponding source-specified materials/assembly methods. Populating a hypothetical questionnaire does NOT authenticate suppliers or qualify certified equipment. Until then every real installed all-in quote, actual annual incremental OPEX, replacement schedule and design qualification remains **NULL, not zero**.

## 4. Native BAFU 2026 v1.1 and matched-service environmental assessment

The [L3-E independently replayed annual operating electricity inventory](../src/ptxlens/l3e_exogenous_operational_energy_inventory.py) quantifies original signed grid import, export and compressor duty for each source year under the same 30t/day H₂ service:

| E+S minus E: annual energy change, MWh/year | 2022 | 2024 |
|---|---:|---:|
| Gross imports | −8,244.813 | −11,659.948 |
| Gross exports | −9,144.901 | −10,779.190 |
| **Signed net grid imports (import − export)** | **+900.088** | **−880.758** |
| Compressor electricity (already included within system electric load) | +432.641 | +576.552 |

A larger bank saves modelled wholesale electricity money in BOTH years, but **2022 net grid electricity increases** while **2024 net grid electricity decreases**. Compressor power is a component of original total electric balances and must **NOT** be added a second time to purchases. Therefore **electricity cost savings cannot establish positive greenhouse-gas savings or reduced energy use in every year**.

A scientifically valid LCA additionally requires:
- **Functional unit:** delivered **1kg H₂** with identical hourly physical product availability and same original energy-system boundary per architecture and historical year, not nominal H₂ tank capacity. If allocating the new storage manufacturing over an equipment lifetime, the lifetime delivered H₂ and repeated annual scenarios must be explicitly specified and must not borrow false future prices.
- **Foreground material and manufacturing:** actual vessel+BoP manufactured kg by graded material, procurement/scrap yields, weld/forming/heat-treatment, test/rework, manufacturer geography, shipping, maintenance, replacements and end-of-life. Original F2 empty equipment kg is **not sufficient** for any of these input exchanges.
- **Native BAFU:2026 v1.1 provider evidence:** exact authenticated original `.zolca` identity, native process/activity UUID, product and reference flow UUID, valid reference unit (e.g., manufacturing mass when applicable), geographically/technologically defensible provider link and exchange quantity. Do not borrow a vehicle-composite pressure vessel process or a BAFU:2026 v1 alias as v1.1 evidence.
- **Operational electricity/emissions:** time-matched hourly grid import/export and justified original specific provider/marginal impact factors, export displacement/credit methods and sensitivity to consequential vs attributional modelling. Annual MWh and € cannot be multiplied by an invented static kgCO₂e/MWh factor and called a source-verified LCIA.
- **Quantification gate:** genuine original native openLCA product system construction, cut-off/uncertainty, method/version and independently reproduced LCIA, covering manufacture, replacement, maintenance/transport/EOL and the same service. An independently filled YAML/JSON foreground form is only an intake, NOT native provider calculations.

The existing [L3-D native BAFU original-source evidence gate](../src/ptxlens/l3d_bafu_incremental_inventory_gate.py) intentionally remains blocked on original process/provider/manufacturer evidence. L3-E's new ledger preserves that separation. No real manufacturing GWP, total incremental environmental cost, external plant electricity emissions or measured site carbon intensity is currently computed. No claim that E+S is greener or viable at actual costs is permitted.

## 5. Reproducibility, regression and release

**Two repositories required:** PtXLens branch `feat/wp0-screening-core` and PtXFlex branch `feat/milp-methanol-baseline`, as previously, with PtXFlex virtualenv Python and existing original public F2/cross-year result files.

~~~powershell
cd C:\Users\prasa\OEM_Research\PtXFlex
git pull --ff-only
cd ..\PtXLens
git pull --ff-only

.\scripts\F3D_Robustness_Local.ps1 -Phase Test

# Generates only public-safe research scenarios, reference inventory, and
# blank OEM evidence questionnaire; NO private annual MILP solver work.
.\scripts\F3D_Robustness_Local.ps1 -Phase L3EPrepare -Mode max_inventory

# Rebuild all 7 public research candidates against original immutable sources,
# byte-for-byte; does not stage or publish files.
.\scripts\F3D_Robustness_Local.ps1 -Phase L3EAuditPublic -Mode max_inventory

git status --short
~~~

Outputs: PtXLens `data/results/L3E_2022_2024_H30_W090_EXOGENOUS_INCREMENTAL_DCF_FRONTIERS_NOT_VENDOR_NPV_v1.{json,md}`, `L3E_H30_W090_INCREMENTAL_STATIONARY_20t_to_40t_HARDWARE_AND_BAFU_FOREGROUND_NOT_LCIA_v1.{json,md}`, `L3E_H30_W090_2022_2024_SOURCE_ANNUAL_GRID_AND_COMPRESSOR_INVENTORY_NOT_LCIA_v1.{json,md}`. PtXFlex produces `data/results/F2L3E_H30_INCREMENTAL_20t_40t_TYPEI_OEM_BOM_COST_EVIDENCE_INTAKE_NOT_QUOTES_v1.json`. **Seven public-safe new outputs** are expected after passing local tests; do not use `git add .`, publish source private provider arrays, full-year source solver witness data, manufacturer quote files or signed confidential datasheets. Run the source-rebuilding [seven-output fail-closed scientific-publication audit](../src/ptxlens/l3e_publication_admission.py) and its [negative regression tests](../tests/test_l3e_publication_admission.py); review reported per-file SHA/contents and scope before manually staging exact files.

The original 2022+2024 source results and earlier 115-pass/one-skip base regression do not change. **L3-E modules, newly added tests and seven prospective outputs are NOT YET executed on local Windows**; do not mark them scientifically verified until the full source-hash and negative tests pass.

Remaining gates: authentic full manufacturer pressure-certified quote/composition/BoP evidence, source geography/maintenance profiles, native BAFU 2026 v1.1 independently reprocessed product systems, site hourly GHG/contract power settlement, externally defensible electricity/wind forecast sensitivities and project real installed-cost financial comparison. Full programme scientific v1.0 remains NOT PASSED.
