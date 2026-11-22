# Research programme and boundaries

## Completed here (subject to CI)

- Versioned hourly scenario schema with source-kind requirement, exact 8760-hour annualization, consecutive UTC times, flow sign/finite checks and a guard against simultaneous grid purchase/sale.
- Formula-auditable component annualized cost (CAPEX + discounted replacements × CRF, fixed and variable OPEX, grid *net wholesale settlement*, separately declared wind value), divided by **delivered** hydrogen.
- Hypothetical source-supplied operational GWP factors + explicitly annualized embodied asset impacts; no exported electricity avoided-emission credits.
- Separate foreground electricity-inventory **staging export** for future openLCA, explicitly **not** an openLCA database or LCIA computation.
- Byte-hash and row-count inspection helper for read-only PyNEXUS run artifacts; no source-column translation yet.

## Not done

- No OpenPyTEA hydrogen case study has been executed in this repository; its generic equipment correlations are not electrolyser cost models. Need source-pinned electrolyser CAPEX and BoP boundary.
- No real openLCA product system, providers, LCIA characterization method, olca-ipc execution, or Brightway run. These require separately recorded data and end-to-end numerical evidence.
- No EXIOBASE dataset import or redistribution. EXIOBASE 3.8.x and 3.9+ have different licence conditions.
- No actual frozen PyNEXUS WP5 observed-price artifacts have been ingested, matched, unit reconciled or converted to the new schema. The historical annual demo is wind-observed plus *synthetic* pricing and is not a substitute.
- No full scoped TEA, LCA, industrial validation, hydrogen compression/purity assessment, tariff/tax system, or ISO 14044 conformance.

## Next gates

WP0: toolchain execution + exact software versions; openLCA foreground LCIA with named GWP100 method, literature cost factor ledger.
WP1: recover/hash-check frozen 2023 PyNEXUS WP5 Actions inputs, actual columns, original source timestamps.
WP2: full investment/operational boundary and life-cycle inventories with source references and double-counting ledger.
WP3: matched delivered-service E vs E+S analyses under observed-price and explicitly sourced hourly electricity emission factors.
WP4: emissions-constrained or epsilon-frontier optimization (not merely ex-post accounting), independent recheck.
WP5: reproducible evidence/report release if independently substantiated.

Frozen reference: https://github.com/abhijith-sivaprasadan/PyNEXUS ; 26 October 2026 freeze, baseline code commit e7eb6acd2ab4254947f999a10fd016ee1127abbb. Its WP5 economics has an illustrative cost-accounting framework, while its separately checked observed-price study is **wholesale settlement only**, not LCOH. This repository will not modify that freeze.

Evidence classes: [S] source confirmed, [R] repo verified, [E] executed, [P] proposed. All example inputs are **invented arithmetic fixtures**, not literature-sourced research claims. This is an AI-assisted research-software implementation requiring human scientific audit. Software may be MIT licensed; third-party dataset licences remain separate.
