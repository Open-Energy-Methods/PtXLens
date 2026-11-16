# F3-D research correction: E-maximal selected hydrogen service and exogenous-service robustness

**Scientific methodological correction, 16 November 2026.** F3-D original source-year price/wind numerical evidence is retained unchanged; this note corrects the *interpretation* of the already verified 2022 low-wind stress. No primary source files or private hourly vectors have been modified.

## 1. The issue: maximum-service reference conditions on an E feasibility boundary

The original source-verified 2022/2024 study does NOT use an externally fixed 30t/day client demand. The code explicitly solves a *price-neutral E-only maximum uniform hydrogen delivery* reference under original hourly wind and equipment constraints:

    maximize alpha in [0,1] subject to E delivers alpha * 50,000 kg/day / 24 at EVERY hour.

For 2022 max_inventory, the published selected alpha is approximately 0.6096129731, i.e. 30.480648653 t/day at the original observed wind-power availability. The original selection is based on a source HiGHS original-integer service-optimization certificate, with the 2022 gross-selector proof method recorded as legacy (the reviewer did not independently reconstruct the original selector's integer dual). The original 2022 and 2024 E/ES source-year annual cost solutions WERE physically replayed independently.

The 2022 E LP source model was independently found infeasible when original wind available **electric POWER** was reduced by 10%, with a strict analytic 131h storage-energy contradiction of 882.9705kg H₂; its 8-case independent LP wind-factor bracket tightened the proven infeasible factor to **0.999933047961622**. E at 1.0 remains original-source integer feasible. Thus the true original E MILP wind-factor transition is known only to lie in approximately **(99.993304796%,100%]** under the original source model.

**This mathematically demonstrates a source-model operational failure at original maximal demand under reduced supply. It is NOT evidence that a normal contracted H₂ demand 1% or 10% below this threshold would also be infeasible, nor a probabilistic reliability estimate, nor an industrial availability margin.** Choosing maximum feasible E throughput at k=1 makes E close to a physical-model feasibility boundary *by construction*. This confounding must accompany every publication claiming that the larger 40t bank is more resilient than the smaller bank.

A separate important interpretation point: the larger E+S bank has an independently replayed feasible solution at k=.9 for the **original near-boundary E target**. That is a legitimate model-specific feasibility contrast, but extrapolating it to arbitrary exogenous customer contracts would be scientifically unsupported.

## 2. Prespecified independent product demands

The remedy is to freeze hydrogen delivery independently of maximizing E throughput or solving any stressed-wind scenario. The new experiment selects exactly:

| Contract-screen name | Hourly H₂ target (kg/h) | Daily H₂ delivered (tonnes/day) | Fraction of initial nominal 50t/day service |
|---|---:|---:|---:|
| H25 | 1,041.666666667 | 25.0 | 50% |
| H27.5 | 1,145.833333333 | 27.5 | 55% |
| H30 | 1,250.000000000 | 30.0 | 60% |

These are **hypothetical research throughput assumptions**, NOT a vendor/client-verified offtake agreement. They are below the original source-registered E-selected constant annual throughput in each 2022 and 2024 storage interpretation (minimum about 30.481t/day). The same exact hourly `float64` H₂ target vector is passed without alteration to both original E and E+S and to every controlled wind scenario *within* each source-year/capacity-semantics pair.

All candidate services are assessed at three explicitly predeclared electric-wind-availability multipliers:

- 0.90: 10% less source-model available wind ELECTRIC power; not meteorological wind speed.
- 0.95: 5% less source-model available wind ELECTRIC power.
- 1.00: original source model 2022/2024 wind, unchanged.

All simulations reuse original year-specific NL A44 wholesale electricity prices, original engineering parameter sets and original Type I source pressure/compressor duty. The registered provider-array and original maximal E-selected hourly H₂ SHA256 values are checked before any new data are admitted. The 2022/2024 nominal source years and gross/usable physical capacity interpretations remain scientifically separate.

## 3. Conservative first-stage LP model screening

[Independent PtXLens fixed-exogenous-service screening implementation](../src/ptxlens/f3d_exogenous_service_lp_screen.py) assembles an E and E+S **linear-programming relaxation** directly from the frozen original source hardware/energy equations:

- Original 8-field hourly electric/H₂ dispatch variables, grid power limits, PEM minimum/rated load, ramps, constrained curtailment, hydrogen inventory/leak, compressor electric duty, initial/end inventory, pressure-screened Type I tank semantics.
- The exogenous H₂ target is never price-optimized, maximized against E, or selected after seeing the stressed-wind results.
- HiGHS solver status 2 establishes original-source E/ES LP infeasibility; therefore the corresponding integer MILP is also infeasible. A separate generous storage/inventory necessary condition may prove failure without an LP solver.
- HiGHS LP status 0 is acceptable only after independent sparse original model equality, inequality and bound residual tests. **LP feasibility is not integer feasibility** because PEM commitment and charge/discharge direction are relaxed.
- Solver timeout, numerical failures, inconsistent source price/wind/H₂ hashes or missing independent source-year reference **abort** rather than write a misleading result.

The study defines **3 H₂ service levels × 3 wind factors × 2 architectures = 18 independent full-year LP feasibility solves** per historical year/capacity interpretation, producing 9 matched-service comparison rows. Outputs are only model-conditional original LP statuses, source hashes, hypothetical scalar service levels, solver-status metadata and numerical residuals. No raw price/wind data, original 8,760/8,784-hour target vectors or private MILP witnesses are exported.

An original price/wind provider-year LCA, real plant dynamics, geographical hardware location, updated manufacturer quotations, local electricity emissions factors and native BAFU 2026 v1.1 manufacturing process inventories do NOT follow from these LP screens.

## 4. Scientific decision tree before any new economic claim

**If E and E+S are both LP-infeasible:** the selected original source H₂ service cannot be met by either full integer model. No same-product cost saving is definable.

**If E is LP-infeasible and E+S is LP-feasible:** E is genuinely mathematically excluded under this original source model, but E+S remains *integer-feasibility unproven*. Do not claim a storage resilience difference until E+S original integer feasibility is independently verified for the same exogenous H₂ contract and year.

**If both E and E+S are LP-feasible:** neither integer feasibility nor net power settlement savings have been established. Select a *predeclared physically comparable* scenario, then run original E and E+S full-year source MILPs with the fixed exogenous H₂ contract and verify all 8760/8784 hourly primal and pressure/EOS states independently. Only then does `E cost - E+S cost` become a valid matched-service economic outcome.

**If E is LP-feasible and E+S LP-infeasible:** do not assert the source's presumed nested feasible sets without confirming the physical equipment model. Record the exceptional result and inspect original capacity/heel/pressure conventions before proceeding.

The published original 20-year hypothetical DCF remains only a response to the earlier source-year maximal-E-service comparisons. It must not silently substitute these new exogenous-service tests into its annual cashflow or redefine 2022/2024 source EUR as normalized future revenue.

## 5. Reproducibility and release gate

**New implementation has been committed but HAS NOT been executed against original private annual inputs.** Its synthetic regression tests have also not yet been run locally. Exact run:

```powershell
cd C:\Users\prasa\OEM_Research\PtXLens
git pull --ff-only
.\scripts\F3D_Robustness_Local.ps1 -Phase Test

.\scripts\F3D_Robustness_Local.ps1 `
  -Phase ExogenousServiceLPScreen `
  -Year 2022 `
  -Mode max_inventory
```

The generated public-safe outputs are `data/results/F3D_2022_max_inventory_EXOGENOUS_H2_SOURCE_LP_FEASIBILITY_SCREEN_v1.json` and `.md`; inspect their source SHA and absence of hourly data before publication. The *already generated six* 2022 fixed-maximal-service wind evidence files remain untracked local assets until reviewed/published. Do not accidentally commit private provider price, wind source arrays, or original 8-field hourly primal witnesses.

**Scientific v1.0 remains blocked**: no vendor-installed CAPEX/OPEX, real H₂ offtake, actual site wind/compressor performance, independently verified integer tree/dual/Farkas ray, completed native BAFU:2026 v1.1 matched-service LCA or whole-project economics are established by this exogenous LP study.
