# F3-D exogenous 30t/day source-year integer MILP and independent replay protocol

**Checkpoint:** 16 November 2026. The 2022 max_inventory exogenous LP screen completed: 25, 27.5 and 30 t/day each at 90%, 95% and 100% original modeled wind electric power, E20t and E+S40t (18 original-source annual LPs); all relaxed LPs were feasible. The LP results do NOT establish original integer dispatch feasibility. The previous 2022 original E-max ~30.481 t/day wind infeasibility threshold is mathematically boundary-conditioned because the hydrogen delivery target was selected by maximizing E itself.

## Prospective primary experiment

Fix an EXOGENOUS, analyst-selected hourly hydrogen target of 1,250kg/h (30,000kg/day, 10.95 million kg over 2022's 8,760 UTC hours). The same vector is imposed on both E (20t) and E+S (40t), and is never selected by a price or stressed-wind optimizer. Use the original 2022 NL ENTSO-E A44 price and 90% of the original Copernicus ERA5 ARCO PyNEXUS-derived model wind ELECTRICAL power (not 90% of meteorological wind speed). Preserve original registered hardware, grid cap, pressure-screened 200bar(a) Type I storage, compression duty, binary on/off, charge/discharge exclusivity, ramp, cyclic inventory and hourly H2 balance.

The original source data are verified against the four-case public Git blob ca07f5ef1e381fa157982bc5a68e46ce3022003a. The new PtXFlex source integer model additionally gates on the exact 2022/max_inventory original PtXLens independent exogenous H2 LP screen, its E and E+S accepted feasible statuses, selected hourly H2 SHA, wind/price original source SHA, and the original E-selected source-model reference. Source cost solver must reach accepted 1e-6 relative MILP gap. Timeouts, incomplete primal or missing solver bound are INCONCLUSIVE, not evidence of zero saving or impossible operation.

## Private-original and public-reviewed division

PtXFlex script: src/ptxflex/f3d_exogenous_h2_integer_dispatch.py. Run original 8,760-hour full integer cost optimization individually for E and E+S, store each accepted full hourly eight-variable solver witness solely under the user's PtX_PRIVATE_RESEARCH/results/exogenous_service_robustness directory, and reuse an existing source-matched private witness without overwriting.

PtXLens script: src/ptxlens/f3d_exogenous_h2_integer_independent_replay.py. Do not accept any public matched-service cost until BOTH full-year private original E/ES witnesses are present and source-registered. Independently replay all 8,760 hourly grid/PEM/H2 balances, storage/leakage, binary commitment, ramp, charge/discharge, curtailment, 313K CoolProp real H2 pressure at original screen bounds, signed annual wholesale price settlement, and solver-reported 1e-6 cost bound. Independently recomputed E minus E+S nominal 2022 EUR and normalized EUR/kg are reported only after BOTH pass. The HiGHS integer dual tree remains independently unverified; source-reported numerical cost bounds are not probabilistic uncertainty. No actual 50t/day contract delivery, vendor CAPEX/OPEX, native BAFU:2026 v1.1 LCIA, site performance or programme scientific v1.0 is established.

Public aggregate, if both pass: PtXLens/data/results/F3D_EXOGENOUS_2022_max_inventory_H30_W090_BOTH_INTEGER_INDEPENDENT_REPLAY_v1.json. Contains SCALAR annual cost, original source fingerprints, EOS, annual service and solver bound metadata only. NEVER stage private original provider arrays or original hourly solver/primal witnesses.

## Local Windows execution after pulling both feature branches

PowerShell:

    cd C:\Users\prasa\OEM_Research\PtXFlex
    git pull --ff-only
    cd ..\PtXLens
    git pull --ff-only
    .\scripts\F3D_Robustness_Local.ps1 -Phase Test

Computationally expensive original annual source cost optimizations (E then E+S, each independently saved and restartable):

    .\scripts\F3D_Robustness_Local.ps1 -Phase ExogenousH30SolvePair -Year 2022 -Mode max_inventory -DispatchTimeLimit 3600

Then source-independent physical/cost/EOS replay; no new integer solver work:

    .\scripts\F3D_Robustness_Local.ps1 -Phase ExogenousH30ReviewPair -Year 2022 -Mode max_inventory
    git status --short

If E original MILP fails or times out, no matched-service saving is publishable. If both pass, the result will be an observed-source-year model-only paired net electricity cost comparison for independently prescribed 30t/day at 90% modeled wind availability, not a site or future-market storage benefit prediction.

**Status:** method and tests committed; original E/ES integer source solves and new independent PtXLens replay NOT YET run locally; earlier exogenous LP screen passed, 64 previous regression tests passed.
