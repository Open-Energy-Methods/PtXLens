# P0 private-source recovery and F3-D leap-year mathematical readiness — 2026-11-14

Programme: OEM-PTX-2026-01. This is a **limited technical handoff**, NOT programme-gate certification.

## 1. Original 2023 source artifact recovery

Three original source GitHub Actions ZIP artifacts were retrieved on 2026-11-14
from private upstream `abhijith-sivaprasadan/PyNEXUS` and inspected in the
current **temporary** computation workspace. Their whole-artifact SHA-256 matches
the frozen upstream REST artifact digests, and their ZIP member CRC checks pass.
These checks test the original GitHub Actions ZIP *wrappers*, not just derived
numerical result JSON.

| Original | Upstream artifact ID | Original ZIP SHA-256 | CRC | Members |
|---|---:|---|---|---:|
| E, 2023 | 12612294862 | `069455704573825f4e709e6705f5db43823722909cb93a37bd86b978636fb051` | PASS | 5 |
| E+S, 2023 | 12613045475 | `cd4101fe62c3f1b8aa2d7508d3651d2fee40d2bafe6d5b87e40d5f4d055070f9` | PASS | 5 |
| NL ENTSO-E A44 original XML, 2023 | 12610917985 | `bc1751b86a3fe712ac2713985c4e189c922a031bacb53a7bd8f422809ba24248` | PASS | 15 |

Three original ZIPs were packaged, unchanged as inner members, into a
**private user-download-only temporary handoff ZIP** with an offline verifier,
source provenance manifest and explicit storage limitations.

- Outer package SHA-256: `10321ce1ad34344bf0285718bd22c320fb1c2a0edb3f471622888f39f0b7da5b`
- Outer package bytes: `1628681`
- Offline verifier executed against the extracted staging directory: PASS all 3 original source ZIP SHA and CRC.
- **No raw provider XML, original wind/price hourly arrays, raw source ZIP bytes, user paths, or credentials are committed here.**
- No assertion that private user-controlled first/second copy exists or that a distinct physical storage device has been reviewed.

**P0 NOT PASSED:** current chat workspace and a downloadable archive are not
durable independent escrow. User must download privately, verify extracted
archives in a user-owned primary destination, create another copy on an
independently identifiable failure domain, perform an actual restoration,
record device/procedure/evidence privately, and obtain legal/provider permission
and independent scientific review. The existing
`scripts/verify_private_pynexus_recovery.py` in PtXFlex verifies necessary
hash/CRC/alias controls; it does not certify physical media or rights.

As of 2026-11-14 GitHub Actions lists all three as unexpired. Earliest
upstream original source expiry: **2026-12-24T19:24:29Z**. Do not rely on that
temporary retention.

## 2. 2024 calendar numerical compatibility — distinct from source admission

PtXFlex `solve_ideal_storage` now has opt-in
`source_calendar_year=2022 or 2024` with mandatory 8760/8784 source-hour
counts and an explicit *non-certified* input class. Frozen 2023 model calls
retain their previous 8760-hour maximum, default source-year semantics and
source-specific result labels. An alternative-year result cannot silently
reuse a 2023 cost-currency label, assert another observed history, or
declare external verification or v1.0 plant accuracy.

The synthetic-only 2024 test constructs the complete **8,784-hour**
full model matrix with a stub solver (it does not optimize genuine 2024
observations), and negative tests reject dropped leap hours and false
observed-year input classes.

PtXFlex verification run:
https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43614899584 (success).

**Still unavailable / blocked:** authenticated 2022/2024 NL A44 plus ERA5
100m provider pairs, original 2023 rederivation of provider arrays to frozen
float64 SHA, independent physical new-year H2 service construction,
E/E+S reoptimization and solver certification, 2024 calendar-modelled
economic comparisons and deflator normalization. Do not use the source-derived
2023 wind/price perturbations as 2022/2024 observations.

## 3. Release consequences

P0, F3, L1, L2 and L3 complete acceptance, full native BAFU stationary H2
storage manufacturing GWP, manufacturer-installed site CAPEX/OPEX, and
scientific v1.0 remain **NOT_PASSED**. Passing offline hashes, calendar
regression tests and CI proves only those narrowly named subgates.
