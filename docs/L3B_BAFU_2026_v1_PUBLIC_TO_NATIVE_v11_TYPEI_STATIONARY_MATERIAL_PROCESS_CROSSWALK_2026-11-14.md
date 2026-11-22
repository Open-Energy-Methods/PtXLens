# L3-B — Original BAFU:2026 v1 public process metadata → v1.1 native material/service crosswalk

**Programme:** OEM-PTX-2026-01. **Date:** 14 November 2026.  
**Current scientific gate:** SOURCE CANDIDATES VERIFIABLE; **native v1.1 foreground flow assignment NOT PASSED;** 19 stationary equipment classes still lack OEM-verified feedstock/manufacturing inventories. No whole-plant GWP100, manufacturer-quoted installed CAPEX or LCOH is established.

## Evidence hierarchy and actual execution

**A. Authentic public Swiss FOEN/Bundesamt für Umwelt OGD data.** The source is the official `https://data.bafu.admin.ch/api` with *BAFU:2026 v1*, `IPCC 2021 / GWP 100`, exactly **11,947** distinct process UUIDs in 16 full hexadecimal partitions. The independently recalculated original published-process CSV SHA256 is **`7a6dc0f2cf43527b1c329dfa0383679abef68e5129859898abc5d11309e08265`**. This is anchored to [real source workflow 43644651127](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43644651127), which independently checked 16 curated source process UUID/name/geography/unit identities against **all 11,947 actual public rows**. This public v1 source contains **pre-characterized per-process LCIA results**, not a native `.zolca` process material/input bill. It cannot be used in lieu of actual technosphere reference flows or linked product-system calculations. The public OGD and the separate Nexus model have different source/licensing representations.

**B. Original native BAFU v1.1 source.** Previously sourced uploaded original native `.zolca` is registered at SHA256 **`e63b7e7ef5cde04bfe1176a783a55b5f72e2b73f42c36632b6150af39d348c4c`**, **135,424,513 bytes**. Its prior native Dutch 30bar PEM *reference* calculation exists, but this *new Type I* native material-process crosswalk has **not been run on that v1.1 source** in the current runtime. No later native process identity, quantitative-reference flow UUID, unit, input exchanges, supplier links or installation process can be reported as newly verified until actual original source replay succeeds. The new [Java 25, GreenDelta openLCA-core 2.7 executor](../native-openlca/src/main/java/org/openenergymethods/ptxlens/BafuNativeV11Crosswalk.java) compiles and will verify the exact original archived SHA before restoring the authorized database into a new **private** Derby folder, then write the process quantitative-reference flow UUID, unit and `PRODUCT_FLOW` vs `WASTE_FLOW` distinction for a bounded candidate list. This is *not* a GWP computation.

**C. Approved foreground supplier mapping.** To approve even one physical input requires actual manufacturer grade-specific raw input quantities, related manufacturing operations/waste/yields, a native v1.1 matching reference flow (same functional and dimensional meaning), geography and lifecycle boundary, mutually exclusive direct and upstream burdens, complete versioning, and independent signoff. Neither source A nor source B alone establishes C.

## First source-verified public BAFU v1 identity shortlist

Process names, UUIDs, reference units and locations below are verified against the exact original public v1 metadata file. They are **not v1.1 native approved manufacturing providers**. The full 16-row, machine-readable source register is [the audited shortlist](../research/L3B_BAFU2026v1_SOURCE_VERIFIED_PUBLIC_PROCESS_SHORTLIST_NOT_NATIVE_v11_2026-11-14.json).

| Foreground role only | Actual public BAFU v1 process | Region, reference unit | Candidate ID (abbreviated) | Compatibility risk |
|---|---|---|---|---|
| Raw alloy steel | Steel, low-alloyed, at plant | RER, **kg** | `b9430f24…` | Source actual vessel steel grade unknown |
| Stainless steel alternative | Chromium steel 18/8, at plant | RER, **kg** | `fc9385f8…` | 18/8 is not automatically OEM-approved Type I shell |
| Recycled-content alternative | Chromium steel 18/8, secondary production (100% Rec.) | CH, **kg** | `84a22beb…` | Secondary raw-steel system, not an avoided EOL credit |
| Metalworking service | Chromium steel product manufacturing, average metal working | RER, **kg** | `2346a410…` | Per processed kg service; not extra equipment mass |
| Rolling service | Sheet rolling, chromium steel | RER, **kg** | `8f574699…` | Not an extra kg input of steel |
| Equipment pipe *example* | Pipe, stainless steel | CH, **kg** | `a578893c…` | No proof of H₂, pressure rating or PED design suitability |
| Construction | Concrete, normal, at plant | CH, **m³** | `9dc7ef6a…` | Actual installed foundation volume and NL site source missing |
| Freight | Transport, freight, lorry, 16t–32t, fleet average | RER, **t·km** | `85b3a5a6…` | Actual supplier/site journey and transported tonnes unknown |
| Process heat | Heat, natural gas, at industrial furnace 1MW | CH, **MJ** | `2fcda415…` | A candidate, not measured OEM fabrication energy |
| Electricity | Electricity, high voltage, at grid | NL, **MJ** | `437a439d…` | 1 kWh = 3.6 MJ; avoid confusion with dispatch electricity |
| Other hardware inputs | Aluminium, primary, at plant / Copper, at regional storage | RER, **kg** | `5cac9857…` / `3972eb0c…` | Only if actual OEM auxiliary BOM includes these grades |
| **Excluded** | High pressure hydrogen storage tank | GLO, **kg label** | `b4739ad2…` | Original v1 EcoSpold **vehicle composite** H₂ storage, documented per kg H₂ basis, not per kg finished stationary Type I steel equipment |

The native **BAFU:2026 v1.1** counterpart of each identity and its actual quantitative reference flow must be checked independently. A matching UUID string alone does **not** establish equivalence between v1 and v1.1. See [prior source unit error audit](L1_BAFU_STATIONARY_H2_TANK_PROVIDER_UNIT_AUDIT.md).

## Scope and controls

The [19-equipment-class source ledger](../src/ptxlens/l3b_stationary_manufacturer_bafu_foreground_intake.py) remains mandatory for both separately considered bank interpretations. Source-literature reference increments are **802** bare 200bar(g) 1.8m³ vessels (gross-maximum semantics) and **902** (usable-service semantics). The published reference 2,400kg **finished empty equipment** mass is neither installed OEM-approved mass nor 2,400kg purchased virgin steel. Do not extrapolate a single per-kg BAFU factor to 1,924.8t or 2,164.8t of complete finished reference vessel equipment.

The physical storage mathematical screen uses **200bar absolute**, whereas the published source rating is **200bar gauge**. Region-specific, code-compliant actual manufacturer design must reconcile these rather than assuming equivalence.

Foreground input classes must be represented according to their own reference flows: kg metal feedstock; kg metal *working service* (not additional steel mass); m³ concrete (not tonnes unless density is sourced); t·km freight (not vehicle km or tonnes); MJ electricity/heat (not kWh without the 3.6 conversion); **`PRODUCT_FLOW`** versus **`WASTE_FLOW`** end-of-life; and grade/recycling fraction as mutually exclusive steel-feedstock scenarios. Electricity from the economic dispatch solver must be separated from electricity consumed during equipment manufacture; no double counting in BAFU system models. Supplier links cannot be accepted just because a process includes `steel` in its name.

### Native-compatible incremental LCA only after data exists

For documented system life and functional unit, the incremental impact is calculated from **actual** linked foreground and operation (E+S minus E, same delivered H₂), e.g.:

```text
Delta GWP = native GWP(ES equipment+compression+site transport+maintenance+EOL
                       at identical H2 service)
          - native GWP(E equipment+compression+site transport+maintenance+EOL
                       at identical H2 service)
```

Each manufacturing supplier must be linked exactly once through either the native full supplier technosphere or its original direct-input recipe. Precharacterized v1 per-process GWP100 factors should **not** be multiplied into an already linked v1.1 native calculation. Unknown material quantities, quality processes, compressor and construction equipment, scrubber/cooling and end-of-life flows remain **unresolved non-zero**, not 0kg CO₂e.

## Reproducible source and native replay

Public official-v1 catalogue, strict full-source verification, native-execution input UUID list and both capacity interpretation candidate results have already been generated by [GitHub Actions](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43644651127). The artifact is `BAFU-2026-v1-source-OGD-real-process-19-BOM-crosswalk-NOT-native-v11`.

With original authorized `BAFU:2026 v1.1 .zolca` private outside GitHub, a new scratch DB destination, and the artifact's public candidate UUID list:

```bash
mvn --batch-mode -ntp -f native-openlca/pom.xml \
  -Dexec.mainClass=org.openenergymethods.ptxlens.BafuNativeV11Crosswalk \
  -Dexec.args="/PRIVATE/BAFU-2026_v1.1_original.zolca /PRIVATE/New_BAFU_2026_v11_db /PRIVATE/L3B_v1_original_candidate_process_UUIDs_for_private_native_replay.txt /PRIVATE/BAFU2026_v11_original_refs.tsv" \
  compile exec:java

python -m ptxlens.l3b_bafu_original_native_v11_reconcile \
  --public-v1-crosswalk /PRIVATE/L3B_gross_BAFU_v1_candidates_NOT_v11_native.json \
  --original-BAFU-v11-zolca /PRIVATE/BAFU-2026_v1.1_original.zolca \
  --private-native-reference-tsv /PRIVATE/BAFU2026_v11_original_refs.tsv \
  --output /PRIVATE/L3B_gross_actual_native_v11_identity_ONLY.json
```

Repeat the source v1 versus native v1.1 role-check for the usable-service interpretation (the BAFU process identities may be shared across hardware interpretations; the **OEM quantities must not**). The [original native review parser](../src/ptxlens/l3b_bafu_original_native_v11_reconcile.py) rejects missing/changed original bytes, missing/duplicate native source rows, incorrect reference-flow types and unit divergence; the [manufacturer evidence intake](../src/ptxlens/l3b_stationary_manufacturer_bafu_foreground_intake.py) rejects self-asserted provider IDs without a source-attested original-native quantitative reference certificate.

### Decision gate 2026-11-14

- Public BAFU:2026 **v1**: full 11,947-source process catalogue **RETRIEVED / VERIFIED**; 16 exact shortlist identities **VERIFIED**, 19 equipment categories mapped to *potential sources* with all approved links zero.
- Native original licensed BAFU:2026 **v1.1**: source SHA and previous reference-calculation provenance registered; **new Type I process/flow identity crosswalk NOT EXECUTED** (original licensed source file not available in this working runtime).
- Manufacturer stationary Type I full material/BoP BOM and installed quote: **NOT OBTAINED**.
- Native incremental station GWP100 and whole-investment LCOH: **NOT CALCULATED**.
- Programme scientific release: **pre-v1.0 / NOT PASSED**.

Sources: [BAFU official OGD data product](https://data.bafu.admin.ch/en/dataproduct-economy-consumption-lca), [official GraphQL reference](https://data.bafu.admin.ch/en/), [GreenDelta BAFU2026 Nexus release](https://www.openlca.org/bafu2026-version-1-is-now-available-on-nexus/) (reference original inventory terms; do not redistribute source model). Preserve citation: **Database of the Swiss Federal Administration, BAFU:2026, Federal Office for the Environment, 2026.**
