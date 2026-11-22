# F3-D: second historical source-year replication — exogenous H₂ service, cost and physical audit

**Research checkpoint: 16 November 2026** · Original historical years: **2022 and 2024 only** · Storage interpretation: **max_inventory** · Study: E20t versus E+S40t stationary hydrogen-bank configurations.

## 1. Methodological contribution

Previous F3-D comparisons used a price-neutral **E-selected maximum** uniform hydrogen demand; the original E architecture was consequently almost at its own feasibility boundary. A source-verified reduced-wind E infeasibility finding is valid for that internally selected demand, but is not evidence of industrial reliability at ordinary offtake.

This replication instead fixes the *same hypothetical, independently selected* H₂ contract at **30,000 kg/day = 1,250 kg/h**, before looking at the operating costs. Both original E20t and E+S40t use precisely this H₂ vector within each year. The reference is independent of both architectures' wind-stressed feasible maxima and of wholesale prices. The 2024 product comprises **8,784 UTC hours / 10.98 million kg H₂**; 2022 has **8,760 UTC hours / 10.95 million kg H₂**. They have identical *daily* service but different calendar lengths.

The registered intervention is **0.90 × original year-specific modelled AVAILABLE WIND ELECTRICAL POWER at each original UTC hour**, not a 10% reduction in wind speed or an independently observed alternative weather year. Original independent **2022 and 2024 NL ENTSO-E A44 price series** and **year-specific ERA5 ARCO/PyNEXUS generated wind power** are not mixed across years, not inflation adjusted, and are not published as original hourly provider arrays.

The source-model physical interpretations are held fixed across the year comparison: E20t/E+S40t, original 50MW signed grid power limit, original PEM load/ramp/commitment and curtailment constraints, compressed H₂ original 20–200bar(a) Type I reference inventory capacity semantics, CoolProp real-gas 313 K screening, compressor electricity and inventory/leakage/terminal constraints. Original four-case public source year Git blob: `ca07f5ef1e381fa157982bc5a68e46ce3022003a`.

## 2. Actual independently replayed results

Source-model annual cost figures were produced on the user's private Windows source-year data and are **not public on GitHub for 2024 at the start of this checkpoint**. Both full-year original-source HiGHS mixed-integer cost optimization cases locally completed and independently replayed by PtXLens at exact matched service and pressure/EOS. 2024 original LP screen also passed for all **3 prescribed H₂ services × 3 wind multipliers × 2 architectures = 18 full-year LP cases**. This LP result by itself is NOT integer feasibility; the separately completed full 2024 E+S integer physical replay is the necessary second admission.

| Verified source-model operating result | 2022 (published) | 2024 (private/local, publication pending) |
|---|---:|---:|
| Original calendar hours | 8,760 | 8,784 |
| H₂ delivery (t/day) | 30 | 30 |
| H₂ delivery (kg/year) | 10,950,000 | 10,980,000 |
| Wind power multiplier (relative to each year's original source) | 0.90 | 0.90 |
| Original E20t net signed wholesale electricity cost (nominal year EUR) | €32,160,567.931485903 | €2,544,581.872826561 |
| Original E+S40t net signed wholesale electricity cost (nominal year EUR) | €28,878,954.877419014 | €612,906.0201971165 |
| **E−E+S operating electricity saving (nominal year EUR)** | **€3,281,613.054066889** | **€1,931,675.8526294443** |
| **Source wholesale saving per kg delivered H₂ (nominal year EUR/kg)** | **0.2996906898691223** | **0.17592676253455777** |
| Source wholesale electricity cost reduction relative to E | 10.2038% | 75.9133% |
| Independent complete hourly binary/H₂/electricity/CoolProp real-gas 20–200bar(a) replay | PASS | PASS |
| Source original reported ≤1e-6 HiGHS integer optimization gap | PASS | PASS |
| Independently reconstructed HiGHS full branch-and-bound dual search certificate | NO | NO |

The **nominal source-year difference** in normalized saving (2024 minus 2022) is `−0.12376392733456451 EUR/kg`, or approximately **−41.30%** relative to 2022. This does not establish negative storage benefit in 2024; both year-specific savings remain positive. It also does **not** prove a statistically expected long-run saving, 41.30% degradation or explain causality: price levels, price spread chronology, wind production, grid purchases and intertemporal operation differ between the years; 2022 and 2024 cannot alone identify which driver caused the change.

Caution: **2024's 75.91% relative reduction** is referenced to a much smaller original E wholesale net settlement cost than 2022's cost, and is not a percentage of all H₂ production costs or a financial rate of return. Both signed import/export electricity settlement amounts may be strongly affected by the historical power-price regime.

## 3. Scientific independence and source admissions

- All 2022 nine evidence files have already been checked under the independent source-hash/provenance/publication `AuditPublic2022` and pushed as PtXLens commit `936177a`. Local verification on 16 November 2026 repeated **94 passed, 1 Windows-optional symlink test skipped**.
- Original 2024 E and E+S original-source full-year integer MILP witnesses were privately stored and individually replayed by PtXLens: original source hourly H₂/service SHA, grid electricity balance and signed market settlement, 313 K CoolProp hydrogen EOS 20–200bar absolute, original binary/ramp/bank capacity semantics, and original solver-reported 1e-6 integer cost-gap acceptance.
- The new public-safe [2024 source and cross-year admission tool](../src/ptxlens/f3d_2024_crossyear_publication.py) requires the **original immutable source Git blob**, all NINE previously public 2022 evidence files passing the original 2022 audit, the **THREE** untracked 2024 source/LP/integer evidence files, the 2024 H₂ product SHA for 8,784 hours and exact source 2024 provider-year price/wind/selected E-max SHA. It verifies E/ES original integer solver reported cost lower bound arithmetic, both physical/EOS service indicators, non-inflated source-year cost units and source hash chains. No original provider/witness hourly arrays are read or redistributed.
- The tool produces an immutable source-locked two-year aggregate **only after admission**: `F3D_2022_2024_max_inventory_H30_W090_TWO_YEAR_MATCHED_SERVICE_ECONOMICS_v1.{json,md}`. A newly derived report is NOT to be confused with an independent physical/optimization replay of its inputs: those replays were performed earlier.

## 4. Release gates

Run the new source-locked pre-publication audit and two-year scalar comparison locally after pulling the branch, without repeating source MILPs:

~~~powershell
cd C:\Users\prasa\OEM_Research\PtXLens
git pull --ff-only

.\scripts\F3D_Robustness_Local.ps1 -Phase Test

.\scripts\F3D_Robustness_Local.ps1 -Phase AuditAndCompare2024 -Year 2024 -Mode max_inventory
git status --short
~~~

**Expected staging candidates only if all checks pass:** three original 2024 source evidence files (the original exogenous LP JSON, exogenous LP Markdown and independently replayed E+S integer-source JSON) plus two new cross-year aggregate files (JSON and Markdown). Review `git diff --cached --check`, full staged diff and file hashes before manual git commit/push. Keep all `PtX_PRIVATE_RESEARCH` source original hourly H₂/market/wind and full 8-variable integer solver witness JSON off GitHub. Do not publish any raw original ENTSO-E/ERA5 arrays. The source 2022/2024 source registration documentation is unaffected.

## 5. v1.0 scientific and practical limits

This is an engineering model comparing *two selected original historical calendar years* under a deterministic 10%-wind-electric-power intervention and source modelled service. It is **not** a wind/price probability distribution, reliability/availability statistics, observed commercial plant data, manufacturer's 20–200-bar pressure-vessel validation, or a full bank-of-plant installed-cost package.

Unclosed barriers to real investment and environmental assessment include the confirmed H₂ offtake/quality service, site grid rights/fees and resale tariffs, compressor/motor/meter/ventilation/cooling/pressure vessel BoP, OEM and manufacturer independent cost/weight/maintenance/pressure certifications, stack replacements and degradation, complete source-linked native BAFU:2026 v1.1 matched-service process inventory/emissions and a coherent project-specific NPV/discount/currency/horizon definition. Therefore **neither full project economic viability nor environmental superiority nor scientific v1.0 can be claimed** from these two source years.

**Code status:** cross-year audit implementation and negative tests committed, local execution on 2024 evidence PENDING.
