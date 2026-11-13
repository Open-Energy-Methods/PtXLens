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

**Registered source evidence imported on 14 November 2026.**
The real 2023 six-artifact source verification
[passed in PtXFlex](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43526250517).
The reconciled derived JSON was registered unchanged in
[`data/results/F3_2023_reconciled_research_evidence.json`](../data/results/F3_2023_reconciled_research_evidence.json)
with SHA-256 `5dead18cfa0c3fecf15562f423e01044bcc6ad4ba4f5212dfb44a010b0d1a0d3`.
The [independent PtXLens bridge](../src/ptxlens/f3_reconciled_source_bridge.py)
and source-locked regression tests now verify its physical/mathematical
shortage interpretation. This is an original-source-based numerical study,
not a measured plant or a native incremental-storage LCA.
Synthetic contract tests remain explicitly distinct from the real study.

**Next:** after PtXFlex reconciles its E+S feasible witness and completes
the source-run certificate, register the certified artifact SHA and workflow
ID, ingest it, then construct equipment-specific impact scenarios with
the original native BAFU 2026 v1.1 source. Do **not** assume that the
original BAFU vehicle-composite tank process is a suitable proxy for
manufacturing the published Type I steel storage bank.

[Coordinated PtXFlex checkpoint](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F3_2023_STAGE_A_CERTIFIED_SHORTFALL_BOUNDS.md).

## Source-verified Stage A correction — 14 November 2026

The 2023 source-locked Stage A certificate workflow
[passed all four jobs](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43524738270).
An independent pressure-screened 8,760-hour E+S fixed-service witness
[passed for both storage definitions](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43525385492).

- **20t E (maximum inventory):** proven additional modelled shortage
  between 65,860.378 and 66,524.317 kg H2; numerical optimum not fully closed.
- **20t E (usable capacity):** between 3,718.744 and 3,720.371 kg H2;
  positive minimum proven, numerical optimum not fully closed.
- **40t E+S (both definitions):** independent zero-additional-shortfall
  full-year dispatch proven feasible. The earlier 2,307.413 kg maximum-inventory
  Stage A result is a *suboptimal incumbent*, not unavoidable shortage.

**LCA decision remains BLOCKED:** these source-based screen systems do
not satisfy equivalent hourly hydrogen service. Both original industrial
full-demand service and source-vessel manufacturing, compressor/cooler,
native material process links, and harmonized complete TEA remain open.
The intake contract still requires a registered SHA-256 of the *derived*
upstream JSON file before accepting its contents as source evidence.
