# F3-D locally executed independent review: original-source custody and release gates

**Date:** 15 November 2026. **Status:** method implemented, local reproduction awaiting genuine 2022/2024 ERA5 source. Open-Energy-Methods has exhausted its 2,000 Github-hosted Actions minutes for the current November cycle; this does **not** block git operations or running the research locally.

## Primary local research runner

Use the source-locked Windows PowerShell runner in [PtXFlex](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/scripts/F3D_Local_Research.ps1), with its [complete source/reproduction runbook](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F3D_LOCAL_WINDOWS_POWERSHELL_EXECUTION_2026-11-15.md).

The PtXFlex script locally retrieves and preserves the original source data, proves 2023 PyNEXUS wind equivalence to a **1 W** quantized power fingerprint without new API calls, collects REAL (not synthesized) ERA5 2022/2024 month-by-month with private CDS token, runs the year-specific price-blind E(20t) maximum feasible uniform original H₂ service selector, and then separately solves E and E+S(40t) against the exact same hourly service under both gross and usable storage interpretations. It saves full individual cost MILP primal witnesses in **private** local storage, not GitHub artifacts.

## Independent reviewer machine environment

The Python 3.12 PtXFlex virtual environment is used for **both** editable repositories and installs `CoolProp==8.0.0`. The local command `-Phase Review` invokes:

```text
python -m ptxlens.f3d_external_year_private_witness_replay  [private, per-year per-mode source and witness paths]
python -m ptxlens.f3d_external_year_independent_review     [four aggregate-only annual reports]
```

For each 2022/2024 year × gross/usable model capacity interpretation, PtXLens must independently check:

- Exact original 8,760/8,784-hour UTC chronology, original monthly NetCDF and A44 full-year source hashes, original PyNEXUS 2023 price and wind calibration.
- Strict float64 or documented 1 W original-2023 reference fingerprints without making unsupported claims of identical underlying original NetCDF bytes.
- The source-selected H₂ target digest, uniform source customer delivery shape, arithmetic of 50t/day original contractual target versus selected feasible fraction, E/E+S identical hourly target and annual delivered H₂.
- Hourly E/ES MILP witness independently recomputed H₂ production/charge/discharge, gas inventory stand loss, compressor charging power, wind curtailment, electric grid imports/exports, PEM min/max/ramp, plant bounds and binary commitment; original 20/200bar absolute EOS bank inventory at fixed 313 K with independent CoolProp hydrogen density.
- Recalculated signed market grid settlement cost, same-year E vs ES cost-saving direction, both HiGHS reported primal and dual bounds and no pooling of unadjusted 2022 nominal EUR with 2024 EUR.
- No supplier-proven installed high-pressure Type I station BOM, no direct site commercial tariff or measured H₂ demand, no native whole-facility BAFU inventory/GWP or LCOH/NPV claim.

A valid PtXLens result is **not** an independent re-solution of the underlying year MILP, not validation against industrial plant measurements and not a site-specific design.

**Crucial rule:** The command reports must remain NOT PASSED if 2022 or 2024 real original ERA5 monthly source files are incomplete, 2023 source calibration fails, either E or E+S annual MILP fails integer feasibility/bound proof, or a physical first-principles replay does not close.

## Research archival and budget control

Source netCDF/XML and physical hourly primal traces stay outside either private research Git worktree in `$HOME\PtX_PRIVATE_RESEARCH` by default. The [GitHub Actions reset budget](https://github.com/organizations/Open-Energy-Methods/settings/billing/budgets) does not itself provide a backup or source licence right. The original 2023 PyNEXUS / 2022–24 ENTSO-E short-lived artifacts should be copied locally before expiry and restored from at least two **physically independent** private storage domains. Avoid pushing raw data; only non-sensitive aggregate method/QA reports with explicit licences and provider caveats may be eligible for version control.

In this repository the ordinary CI is now filtered to scientific source/tests/examples/model change paths rather than all documentation commits; manual triggers remain available. Hosted Actions are not used for multi-hour CDS queued-retrieval jobs.

## Parallel L3-B work

The native BAFU v1.1 original process-reference verifier remains available under `native-openlca`; it requires the original licensed `.zolca` source, a new private scratch openLCA Derby directory and explicit candidate UUIDs. Public v1 candidate process names are **not** native v1.1 supplier identities; supplier raw steel masses, fabrication and BoP BOMs cannot be assumed to equal a literature finished-vessel weight.

**Current scientific v1.0:** NOT PASSED.
