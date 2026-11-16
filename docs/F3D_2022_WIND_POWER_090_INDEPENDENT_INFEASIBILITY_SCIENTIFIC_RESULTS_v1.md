# F3-D 2022 fixed-service −10% wind electric power: independently established source-model infeasibility

**Status:** technical results from the locally executed independent PtXLens source replay, 16 November 2026. Numerical source original archived privately under PtX_PRIVATE_RESEARCH. No native manufacturer quote, BAFU process emissions or real industrial performance claim.

## Research question

Holding identical source-year 2022 original model H2 delivery at approximately **30.481 t/day** (price-blind uniform maximum service) and source NL ENTSO-E A44 hourly prices, can an E-only 20t nominal hydrogen storage bank or E+S 40t bank continue satisfying **all 8,760 hourly hydrogen targets** if source-PyNEXUS modelled available wind **electrical power** is multiplied by 0.9?

**No equivalence to reducing wind speed by 10% is claimed.** This intervention is a deterministic stress on modeled available electrical power, not a physical ERA5 alternative year.

## Primary observed model results and independent verification

| 2022 max-inventory source model | 90% of original modeled wind electric power |
|---|---|
| E, 20t nominal bank | Original source zero-objective LP relaxation HiGHS status 2 (infeasible); **independent LP matrix reconstruction also HiGHS-infeasible** |
| E+S, 40t nominal bank | Original full-year MILP solved; independent full-hourly primal mass/electricity/real-gas pressure/EOS replay passed, plus independent reconstructed constraint-matrix E+S verification passed |
| E+S original source-market annual signed grid settlement | **€31,128,728.45**, nominal 2022 source EUR, not total production cost |
| E−E+S matched-service operating-cost saving | **NULL** (E cannot meet the same H2 product in this source model) |
| Independent native HiGHS Farkas ray | **NOT obtained** |
| Real site infeasibility or supplier hardware performance | **NOT certified** |

### Direct mathematical H2 energy-storage contradiction

The external original source physical model has hydrogen yield \(y\) kg/MWh and hourly PEM power \(P_t\) MW. With a signed grid exchange bounded above by \(G_{\max}\), wind electricity availability \(W_t\), and nonnegative curtailment and electrical H2 compression power, its balance implies:

\[
P_t \le \min\left(P_{\mathrm{rated,max}},\, 0.9\,W_t+G_{\max}\right).
\]

With storage inventory \(S_t\) restricted to \([S_{\min}, S_{\max}]\) and nonnegative storage leakage, summing delivered hydrogen over any **contiguous** interval \([a,b)\) gives the necessary inequality:

\[
\sum_{t=a}^{b-1} H_{t,\mathrm{delivered}}
\;\le\;
y\,\sum_{t=a}^{b-1}\min(P_{\mathrm{rated,max}},\,0.9W_t+G_{\max})
\;+\;(S_{\max}-S_{\min}).
\]

The right-hand side is deliberately permissive: it ignores physical ramping, charge rates and compression electricity and assumes the maximum conceivable use of stored H2. If this upper bound is still too small, no valid original-source model E dispatch exists. This conclusion needs no branch-and-bound or dual solver result.

Independent computation with the original **SHA-registered** 2022 source model identifies:

| Quantity | Independent source-model result |
|---|---:|
| Interval start (UTC, inclusive) | 2022-04-30 18:00 |
| Interval end (UTC, exclusive) | 2022-05-06 05:00 |
| Duration | **131 hours** |
| Maximum continuous demand minus best-case instantaneous H2 production | **18,669.0071 kg H2** |
| Maximum allowable bank inventory swing under 200-bar(a) reference Type I pressure model | **17,786.0367 kg H2** |
| **Minimum physically unavoidable hydrogen delivery deficit within the permissive interval inequality** | **882.9705 kg H2** |

Source original UTC hour indices are **2874 to 3005 (exclusive)**. This is **not** the total annual model hydrogen shortage or expected unserved industrial production. It is a *single 131h contradiction* that establishes infeasibility of the original fixed H2 service, irrespective of price and binary commitment choices.

The cut and E+S witness are checked by a fully distinct PtXLens constraint implementation. The LP feasibility recheck uses the **same** SciPy/HiGHS solver family, so it is independent model-equation reconstruction, **not** a fully independent numerical solver or a Farkas ray. The analytical contiguous deficit inequality is a stronger proof because it does not require trusting a solver's status.

## Source-year scientific interpretation

At the original full 2022 wind input, E **does** have a published, independently physically replayed full-year integer-feasible dispatch serving the same price-independent hourly H2. Under the exactly 10%-reduced original wind electric power, this is **impossible for E** but **feasible for E+S**. For this source-model and selected hydrogen functional unit, the larger bank therefore adds a **hydrogen service feasibility / resilience margin** in addition to the original electricity dispatch cost advantage. The benefit is a feasibility difference, **not** an economic saving that can be valued by subtracting costs when the reference is infeasible.

This single historical model stress is NOT an empirical availability rate, probability of outage, proof of site reliability, vendor pressure-vessel sizing compliance or project economics.

## Prespecified follow-on: necessary-condition wind-factor threshold

New implementation [f3d_analytic_wind_feasibility_threshold.py](../src/ptxlens/f3d_analytic_wind_feasibility_threshold.py) quantifies the wind electric availability multiplier where the *analytical necessary interval deficit* stops demonstrating infeasibility. It applies O(N) maximum contiguous shortage scans and source-locked bisection between 0.9 (infeasible) and 1.0 (full-wind original feasible).

**The analytical-cut boundary is a LOWER bound on the actual original E-model feasible wind multiplier, not an estimate of its exact value.** If the cut does not violate above that point, the full MILP may STILL be infeasible because of hour-by-hour ramp, inventory, storage charge/discharge exclusivity, startup, leakage, compression or physical constraints. A new full-year original E MILP feasibility search at a tighter selected factor would be necessary to narrow the true feasible threshold. Do not call this 10% the project's reliability margin.

The new threshold script and its additional hermetic tests are committed, **not yet executed on the original private 2022 sources**.

## Reproduce locally without new MILPs

\`\`\`powershell
cd C:\Users\prasa\OEM_Research\PtXLens
git pull --ff-only

.\scripts\F3D_Robustness_Local.ps1 -Phase Test

.\scripts\F3D_Robustness_Local.ps1 \`
  -Phase AnalyticWindBound \`
  -Year 2022 \`
  -Mode max_inventory \`
  -Variant wind_power_090
\`\`\`

The original independent LP feasibility source check is already passed; the new calculation reads that immutable JSON, validates original private source hashes and hourly H2 target, reproduces the verified 131h witness, and publishes ONLY a scalar bound and text explanation, never provider hourly data or private primal dispatch.

**Research status:** independent source-model E infeasibility **PASS** and E+S feasibility **PASS** under the 10% electric-wind availability shortfall. Exact wind-factor threshold, independent full MIP search-tree dual, real-world emissions, manufacturer-verified capital cost and whole-project scientific v1.0 **remain outstanding**.
