# PtXLens L1/L2 — admissibility of F3 pressure-adequacy evidence

**Programme:** OEM-PTX-2026-01 · **Date:** 2026-11-14 · **Status:** research gate OPEN.

The existing BAFU 2026 v1.1 native E/E+S scenarios and their source-derived
GWP figures are **scope-limited**: they omit physical incremental storage and
cannot establish environmental superiority. The full-year pressure-screened
hydrogen cases may also be unable to deliver the same hourly service.

PtXFlex has executed genuine 8,760-hour minimum-shortage MILPs; some returned
feasible but **nonoptimal** operating schedules. A positive achieved shortage
is then only an *upper bound* on minimum shortage. An optimality dual bound
(or the trivial nonnegative slack bound) provides a *lower bound*. The existing
40t maximum-inventory E+S positive-shortfall Stage A incumbent must not
supersede its earlier independently solved zero-shortfall fixed-service case.

## Data contract and rejection criteria

- Source: `ptxflex.f3_stage_a_adequacy_certificates.v1` JSON, generated from
  original E and E+S model ZIPs and EOS pressure-audited Stage A dispatch.
- Importer: [F3 pressure adequacy intake](../src/ptxlens/f3_adequacy_intake.py).
  Requires source original hashes, the exact 16,335,279.317 kg historical
  E-delivered target, original 18,250,000 kg demand, internally consistent
  shortage intervals, original full-demand reconciliation, executable MILP
  evidence classification and an **independently registered SHA-256 of the
  upstream derived JSON file**.
- Any unproven positive incumbent is recorded as `BOUNDED_INCUMBENT_MINIMUM_UNPROVEN`.
  Uncertified cases carry *no* invented shortage bound.
- Cost, full-plant GWP, native additional tank manufacturing and new
  compressor/cooler impacts are not populated from Stage A output.
- Even two zero-shortfall modelled cases are not enough for a full LCA
  comparison: same pressure/purity, actual additional equipment mass
  allocation, process-compatible native manufacturing suppliers, cooling,
  OPEX, replacements and full native IPCC GWP 100 impacts are still absent.

## Remaining evidence

No official new PtXFlex shortage certificate has yet been imported or
registered as independently approved evidence in this repository.
Synthetic contract tests are unit tests, not real 2023 scenario outputs.

**Next:** after PtXFlex reconciles its E+S feasible witness and completes
the source-run certificate, register the certified artifact SHA and workflow
ID, ingest it, then construct equipment-specific impact scenarios with
the original native BAFU 2026 v1.1 source. Do **not** assume that the
original BAFU vehicle-composite tank process is a suitable proxy for
manufacturing the published Type I steel storage bank.

[Coordinated PtXFlex checkpoint](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F3_2023_STAGE_A_CERTIFIED_SHORTFALL_BOUNDS.md).
