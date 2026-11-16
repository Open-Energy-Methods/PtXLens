# F3-D — 2022 fixed-service wind resilience: independent source-LP feasibility boundary protocol

**Status: method committed; new 8-factor LP experiment not run locally.**
Scope is Open-Energy-Methods PtXLens/PtXFlex, 2022 NL A44 price/Copernicus ERA5 ARCO single-location model, `max_inventory` stationary Type I screened 20t E and 40t E+S H₂ configurations.

**Post-experiment status clarification, 16 November 2026:** the eight additional independently reconstructed original LP feasibility evaluations have now been completed locally with **48 regression tests passed**. They tightened the E relaxed-LP infeasible lower limit to wind electric-power multiplier **0.999933047961622**, while the original integer-feasible E source reference remains at **1.0**. All eight intermediate tested factors were LP-infeasible; there was **no independently identified new interior feasible LP point**. The original integer threshold is still UNKNOWN in **(0.999933047961622, 1.0]**. The following prespecified method remains useful as the accepted protocol; its original 'not run' header refers to the status before the local experiment. The target was E-selected near maximal service, so this is a **boundary-conditioned stress**, not a site-level reliability result. See [exogenous matched-service correction and follow-on](F3D_MAXIMAL_H2_SERVICE_SELECTION_BIAS_AND_EXOGENOUS_ROBUSTNESS_PROTOCOL_v1.md).

## Established independently before this experiment

- Original E reference at **100% source-year wind electric POWER**: independently verified full-year original E integer primal feasible, meeting the immutable hourly price-neutral hydrogen functional unit.
- At **90% source-model wind electric POWER**, E LP relaxation rebuilt independently and HiGHS-infeasible; E+S full-year integer witness feasible, independently replayed for physics and 200bar pressure.
- A **131h low-wind interval**, 2022-04-30 18:00Z–2022-05-06 05:00Z, creates **18,669.0071kg H₂** net deficit even with generously idealized maximum PEM production, versus **17,786.0367kg** of bank inventory swing. The **882.9705kg** excess is a direct analytic source-model infeasibility proof for E at k=0.90.
- O(N) interval bound bisection establishes that the necessary energy-inventory inequality still rejects factors up to **k=0.9828602781752124**, and stops rejecting at **k=0.9828602781984954**. That sharp numerical boundary is specific to the *generous energy-inventory inequality*, NOT the true E LP or integer model feasibility cutoff.

The reduced-wind E−E+S annual electricity-saving contrast is **NULL** because original E cannot supply the unchanged hourly product. E+S solved net wholesale source-market cost €31.128728m nominal 2022 EUR is not enough to compute a valid matched-service saving.

## New independent linear-programming experiment

The new [source-locked LP feasibility bracket runner](../src/ptxlens/f3d_independent_wind_lp_bracket.py) uses the original annual hourly H₂ target and historical wind and price SHA verified by prior scientific evidence. Source-model variables and constraints are independently reconstructed *from scratch* using PtXLens, not a second call to the PtXFlex source MILP builder. Only unit commitment and charge/discharge direction are relaxed to continuous [0,1], preserving all other E source-model bounds, grid/wind curtailment, PEM min-load and ramps, pressure-screened 200bar storage, losses, compression-electricity duty, H₂ delivery and initial/terminal stock.

With E known infeasible at k=0.90, the generous analytical cut supplies an even stronger initial infeasible lower bound k≈0.9828602782. With the original E full-year MILP independently verified feasible at k=1.0, the physical model's **true original integer transition** is bounded to (0.982860278..., 1.0] (under source power curtailment monotonicity).

The solver then tests **eight midpoint wind factors** in (analytic lower, 1.0] by solving an independently built, **zero-objective full-year relaxed LP**. Each trial result is one of:

| Check | Consequence |
|---|---|
| HiGHS LP status 2 | Independently rebuilt source **LP** infeasible at k; therefore original E **MILP** also infeasible at k |
| HiGHS LP status 0 *with independent primal-residual check* | Source **LP** feasible at k; original E integer MILP may still be infeasible |
| Timeout / numerical issue / inconclusive / primal residual fails | **Stop; no new claimed bracket or published result** |

Because modelled additional wind can be freely curtailed (incrementing curtailment by the available-power change), the reconstructed source feasibility set is monotonic nondecreasing with k, conditional on the frozen source equations. A dichotomy on the LP feasible/infeasible status is therefore valid.

The strongest new LP-infeasible factor is a lower bound for the original E MILP threshold. The LP-feasible factor is **not** an upper bound for that MILP threshold. The only independently reviewed *integer feasible* upper factor remains **1.0**. Do not collapse the actual source E integer feasibility interval to the LP bracket.

The independent equations still use the same SciPy/HiGHS optimization backend as the source. This is **not** an independent solver implementation, a verified Farkas infeasibility ray, a full integer search-tree proof, or a measured industrial-plant wind availability criterion.

## Public evidence contract

- Read immutable original public provider-year four-case PtXFlex aggregate Git blob `ca07f5ef1e381fa157982bc5a68e46ce3022003a`.
- Read original private 2022 A44/ERA5 hourly arrays solely for source hashes and model reconstruction. **Do not publish these arrays**.
- Read independently PtXLens-reviewed original E LP KKT report, E20t infeasibility/E+S40t feasibility report at 90% wind, and analytic threshold source report, each retaining original provider/H₂ SHA and nested independent receipt hashes.
- Write **two scalar-only, immutable public files**: `F3D_WIND_090_2022_max_inventory_INDEPENDENT_E_LP_FEASIBILITY_BRACKET_v1.{json,md}`. Contain tested wind-power factors, statuses, at most numerical LP constraint residuals, original source hashes, original proof gates, and **NULL** operating saving at 90%. They contain **no private hourly H₂/wind/market/dispatch arrays**.
- If the original source is changed, or any previously independent-reviewed physics/LP receipt is missing, refuse a result.

## Windows run

First publish *only after inspecting* the four previously generated untracked public-only 90%-wind files. For the new scientific LP run, leave them locally present until the independently source-matched bracket has been generated and reviewed.

```powershell
cd C:\Users\prasa\OEM_Research\PtXLens
git pull --ff-only

# Regression checks; no original source-year MILPs.
.\scripts\F3D_Robustness_Local.ps1 -Phase Test

# 8 independent full-year E LP feasibility checks (not MILPs).
.\scripts\F3D_Robustness_Local.ps1 `
  -Phase IndependentWindLPBracket `
  -Year 2022 `
  -Mode max_inventory `
  -Variant wind_power_090
```

The check may require more computation than the O(N) analytical proof but does not rerun a full-year mixed-integer production optimization. Do not bypass scientific checks by loosening LP feasibility tolerances.

## Next release-gated questions

1. **E original MILP true wind-factor threshold**: Needs original-source E MILP feasibility checks between proven LP infeasibility below and known integer-feasible k=1; independently review any integer witness before claiming an upper wind factor other than 1.
2. **Uncertainty/reliability**: A single source-year controlled fractional-wind experiment does not define a reliability quantile, climate scenario probability or actual hydrogen offtake.
3. **Project economics/LCIA**: Vendor-verified 200bar stationary Type I bank installed CAPEX/OPEX and an actual native BAFU:2026 v1.1 source-linked BOM/impact run are missing; v1.0 cannot be declared.
