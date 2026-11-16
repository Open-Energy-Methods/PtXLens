# F3-D — 2022 source-year 10% less wind POWER: fixed-H₂ feasibility is a different scientific outcome

**Date:** 16 November 2026 · **Year:** 2022 (8,760 UTC hours) · **Storage semantics:** `max_inventory` · **Intervention:** multiply source-PyNEXUS modelled available wind **electric power** at each hour by **0.90**, while retaining the original 2022 ENTSO-E NL A44 hourly electricity price sequence, original plant parameters and **exact unchanged source-selected hourly H₂ delivery target**. No actual wind speed, source metered farm, real installation or future weather is claimed.

## Completed first local observations (not yet independent infeasibility reproof)

The original source-model E (20t nominal storage) under reduced wind returned **HiGHS LP-relaxation status 2 (infeasible)** with zero cost objective. This relaxation removes unit-commitment and charge/discharge integrality but keeps the original electricity/H₂/inventory/pressure/compression equations and calendar. If that necessary-condition LP is genuinely infeasible, the original more constrained E MILP is also infeasible for this specific 2022-model hourly H₂ product.

The original source-model E+S (40t nominal storage) solved its integer optimization to the original acceptance requirement (`mip_relative_gap <= 10^-6`) and reported **€31,128,728.45** nominal 2022 EUR net wholesale power cost. The independent PtXLens private full-hourly reviewer completed and saved `data/results/F3D_CF_2022_max_inventory_wind_power_090_INDEPENDENT_PUBLIC_REPLAY.json`, replaying both source conditions including the E+S feasible dispatch. This number is **not** profit, not an economic E−E+S saving, not a project OPEX quote and not a result for the original higher-wind service.

**The matched-service saving is NULL**: there is no feasible E source-cost value to subtract from E+S's €31.13m. Assigning a zero E cost or comparing E+S reduced-wind cost with the original-wind E cost would be a false economic comparison. The independent PtXLens review did **not** reconstruct an E infeasibility dual/Farkas certificate; the original source's LP status alone is not a separate external proof.

## Independently rebuilt mathematical cross-check (new code; local run pending)

[Independent original LP source-model reconstruction and analytical power/storage deficit check](../src/ptxlens/f3d_wind_reduction_independent_feasibility.py) uses only independently reviewed private provider-year inputs and existing original-source hourly H₂ SHA. It constructs **the E source model LP constraints independently** from PtXFlex: source H₂ product equality, 0–50 MW signed grid limit, wind curtailment, rated/minimum PEM output, ramps, original leakage, same initial/terminal inventory, screened 20–200-bar(a) H₂ bank and source compression power. It reruns a zero-cost E LP using SciPy/HiGHS and separately checks the previously independent-replayed E+S integer dispatch against the reconstructed E+S constraint matrix, including integrality.

This is an **independent equation implementation with the same HiGHS solver backend**, not a separate commercial LP solver, nor a Farkas infeasibility ray. The new report cannot be considered passed until the source year data and E/E+S witness checks have run locally. It never writes original hourly vectors to the public result.

## Stronger no-LP-solver necessary-condition experiment

For an arbitrary contiguous hourly interval `[a,b]`, original source H₂ and inventory conservation with nonnegative H₂ inventory losses give:

    sum_H2_required_kg <= source_H2_yield_kg_MWh * sum_PEM_electricity_MWh
                          + (bank_max_inventory_kg - bank_min_inventory_kg).

Electric power balance, nonnegative curtailment and nonnegative source compression electricity imply at each hour:

    PEM_power_MW <= min(PEM_rated_max_MW, available_wind_power_MW + grid_import_limit_MW).

Combine:

    sum_a_to_b H2_required <=
       H2_yield * sum_a_to_b min(PEM_rated_max, wind_available + grid_max)
       + (bank_max - bank_min).

If **any** interval violates this *generous* upper bound, E is impossible even with arbitrary idealized rates, no ramping and favorable omitted compression/loss terms. Such a deficit is a direct elementary proof of **source-model infeasibility**, not just a solver status. A nonviolating interval does **not** establish feasibility: minimum-load, losses, start/end constraints, charge/discharge rates and ramping can still obstruct the original LP/MILP.

The implementation computes the greatest contiguous sum of `source_hourly_H2_required - source_H2_yield * min(max_PEM_power, wind+grid_import_limit)` with an O(N) algorithm; it releases *only* its maximum deficit, bank headroom, a possible violating interval's hour indices and a boolean. A positive violation after safety margin is sufficient; otherwise the direct cut is inconclusive and only the separately reconstituted LP result applies.

## Research implication and follow-up

This suggests a **feasibility resilience benefit** from 40t versus 20t within this frozen model: retaining the original price-independent fixed 2022 H₂ service under 90% of its modelled wind electric power. A formal and independent pass of the reconstructed LP is required before upgrading the infeasible-reference claim.

For any continuous wind availability multiplier `k`, source-model dispatch feasibility is nondecreasing with `k` *as long as the extra available wind can be freely curtailed and the original constraints are unchanged*: increase curtailment by the increase in available wind. Thus the observed E infeasibility at 0.90 and original E feasibility at 1.00 can define a **conditional threshold bracket (0.90,1.00]**, subject to independent feasibility verification and numerical tolerance. This is not an empirical reliability statistic and no safety case or plant availability percentage follows.

### Windows local validation

```powershell
cd C:\Users\prasa\OEM_Research\PtXLens
git pull --ff-only

.\scripts\F3D_Robustness_Local.ps1 -Phase Test

.\scripts\F3D_Robustness_Local.ps1 `
  -Phase IndependentWindFeasibility `
  -Year 2022 `
  -Mode max_inventory `
  -Variant wind_power_090
```

Expected output is a sanitized independent-constraints feasibility report `data/results/F3D_WIND_090_2022_max_inventory_INDEPENDENT_SOURCE_LP_FEASIBILITY_v1.json`. The scientific claim is **still blocked** until the actual local run completes. A native Farkas certificate is **not** exported by the current tooling; equipment/industrial site measurements, manufacturer CAPEX and BAFU:2026 native LCIA remain unverified.

**Strict release status:** source-year +10%-wind robustness experiment not run; -10% wind E model original LP status infeasible/E+S feasible, physically replayed; E infeasibility independently reconstructed and simple energy interval cut still PENDING; economic savings NULL; no investment or native BAFU or programme scientific v1.0 release.
