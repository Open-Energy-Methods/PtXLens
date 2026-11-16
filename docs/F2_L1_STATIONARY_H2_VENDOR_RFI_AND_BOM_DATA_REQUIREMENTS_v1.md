# F2/L1-RFI-001 — Stationary compressed-H₂ vessel bank and balance-of-plant: non-binding technical data request

**Prepared 14 November 2026 · Status: DRAFT / NOT SENT · Programme OEM-PTX-2026-01**

This document is **a scientific vendor-data acquisition checklist, not an issued RFQ, procurement commitment, connection application, actual project, design approval or representation of an industrial client**. No hydrogen customer location exists in the original PyNEXUS project. Its 52.5°N, 3.5°E coordinates represent offshore ERA5 wind weather sampling, not an industrial tank site. Do not sign supplier agreements or make financial commitments on that premise.

## 1. Why an RFI is necessary

The source-constrained original 2023 model compares Type I nominal 20,000 kg (E) versus 40,000 kg (E+S) storage; both configurations have the same 10,000 kg modeled initial and terminal inventory, 30 bar assumed PEM outlet, 20 bar minimum hydrogen outlet and conceptual max charge/discharge of 2,200 kg/h each. The **F3-C pressure-screened reference** assumes 313 K, a 200 bar absolute storage maximum and a 20 bar absolute product withdrawal minimum. Those pressures are mathematical modeling assumptions; the original industrial vessel or actual hydrogen site is unspecified.

At the **gross** inventory interpretation, the published 1.8 m³ / 2,400 kg empty **200 bar Type I peer-reviewed reference** requires 803 E vessels, 1,605 E+S, 802 additional reference vessels or **1,924,800 kg additional empty vessel equipment**. For the separate **usable** capacity interpretation: 902 E, 1,804 E+S, 902 additional vessels or **2,164,800 kg empty equipment**. The vessel quantities use CoolProp 8.0.0 at 313 K; neither empty mass represents kilograms of virgin low-alloy steel nor a vendor-certified installed assembly.

**Important non-interchangeable products:**
- [IJHE, DOI 10.1016/j.ijhydene.2025.152849, Table 2](https://doi.org/10.1016/j.ijhydene.2025.152849): research reference Type I 1.8m³ / 2,400kg empty 200bar vessel; exact alloy and actual manufacturer unknown
- [heiserTEC COSMOS **Stationary (PED)**](https://www.heisertec.com/products/bundles/): commercial 210bar class 36×87L = 3.132m³ module, nominal manufacturer **49 kg gross H₂** at vendor conditions; stationary empty assembled module mass **not published**
- [heiserTEC **distinct 50L Type I Hydrogen PED EN1964-1 cylinder**](https://www.heisertec.com/products/type-1/): 330bar catalogue pressure class, 472bar test pressure, **85.5kg EMPTY per cylinder**; not the 36×87L stationary module nor identical pressure duty or the 1.8m³ research vessel
- **heiserTEC COSMOS Mobile TPED 12×50L, 200bar, empty 935kg ±6%**: **not a stationary PED bundle**, no transfer of this mobile assembled mass into any stationary bill of materials

The independent manufacturer 50L 330bar PED cylinder only produces an **alternative hypothetical EOS-at-200bar(a)/313K** mass sensitivity: 28,878 additional individual cylinders / 2,469,069 kg empty equipment for gross inventory, or 32,468 additional / 2,776,014 kg for usable. It is not an approved 200bar(a) derating, and cannot supply a stationary bank without approved connections, racks, cycling assessment and pressure installation review.

## 2. Proposed engineering information request — actual hydrogen pressure vessel OEM

**Suggested recipients:** engineering/technical sales of qualified PED stationary Type I hydrogen pressure-vessel/module suppliers (e.g., heiserTEC for its identified products). No company has been contacted. Do not claim an existing site, actual order quantity or corporate affiliation.

**Subject:** Technical-source enquiry only: stationary hydrogen PED Type I cylinder bank mass/BOM and 20–200bar screening — independent scientific research

> Dear Technical Engineering Team,
>
> I am conducting independent research into the engineering and life-cycle requirements of stationary compressed gaseous hydrogen storage. This is a *hypothetical source-based* research comparison, **not** an offer or request to purchase, a specified site or a formally funded project.
>
> I have reviewed your published Type I hydrogen cylinder/module information. My research separately considers a 20,000kg gross storage case versus 40,000kg gross, and a different withdrawable-mass interpretation. The current **screening-only** conditions are 200bar absolute assumed maximum storage pressure, 20bar absolute minimum hydrogen product withdrawal and isothermal 313 K. A conceptual original model permits charging/discharging up to 2,200kg/h, although its optimized 2023 F3-C dispatch reached only about 552kg/h maximum charging and 2,083kg/h maximum discharging. The actual location, customer purity specification, plant available utilities and operating cycle spectrum remain undefined.
>
> Could you provide **publicly shareable** technical datasheets, relevant standards/conformity statements and the correct procedure for a future customer with a genuine location to request a stationary PED hydrogen-bank engineering quotation? Specifically, please clarify:
>
> **Cylinder/module construction:** model-specific **gross working pressure with its gauge/absolute basis**, permitted operating temperature and cyclic pressure range, water volume, delivered/buffer usable H₂ at specified reference conditions, empty per-cylinder and **assembled stationary PED module/bundle** mass separately, frame and manifold included/excluded material masses, steel grades, forgings/liner and closures, alloy/heat treatment, coatings, manufacturer test/quality certification, lifetime and inspections, document revision date.
>
> **Installation:** suitable manifolds/headers/valves/check/relief/TPRD and safe vent, pressure regulator and minimum customer header pressure after real flow-dependent losses, isolation concept, PE/PED assembly CE/DoC and applicable standards, NEN-EN 17533:2025 component relevance, site code interface and qualified pressure/fatigue, hydrogen compatibility, cycling and embrittlement design.
>
> **Engineering/operations:** limits on aggregate storage racks, space and support loading, stand-off/clearance and access, safety/fire zoning, optimized independent (not 2,200kg/h presumed) charge/discharge capacity, inlet/outlet mass-flow and temperature range, temperature rise and heat rejection, linepack and buffer, redundancy, leakage, gas purity/assay and permitted hydrogen grade.
>
> **Life-cycle/manufacturing (if releasable):** dry equipment per-product material mass breakdown by steel grade, process route (forging/rolling, heat treatment, machining, welded parts), electricity/fuel, scrap recycling, factory geography, expected inspection/refurbishment and component replacement, equipment service lifetime, documented environmental product declarations or manufacturer-supplied cradle-to-gate impact inventories and limitations.
>
> **Commercial information:** whether a meaningful quote is possible **only after** a legal site/customer/capacity specification, and what site-dependent categories would need identification (connection, frame/civil/pipe, training, commissioning, warranty, maintenance, spares, transport, decommissioning). Please do not interpret the research masses or annual savings as an actual purchase request.
>
> Thank you for any appropriate publicly available technical material or procedural clarification.
>
> Regards,
> Independent PtX engineering research
> [Researcher must add accurate contact details and affiliations before sending]

**No message has been sent.** Before any external contact, check source licensing, privacy, actual legal capacity to represent any industrial entity, and whether only public product documents are needed.

## 3. Separate information request — industrial compressor and thermal/cooling supplier

**Relevant technical source:** [Burckhardt Compression public hydrogen compressor family brochure, 2026](https://www.burckhardtcompression.com/fileadmin/uploads/burckhardt/documents/applications/compression-solutions-hydrogen-mobility-energy-burckhardt-compression-en.pdf). This establishes available compressor architectures to ~200bar, *not* a project-specific 30→200bar/2,200kg/h machine, motor mass or price.

Ask for publicly releaseable engineering parameters without implying a site/order:

- Exact **H₂ mass-flow and pressure-envelope feasibility** for 30bar(a) assumed electrolyser source to a 200bar(a) store, including 20bar(a) product header discharge and known pressure drops, actual inlet/outlet temperatures and stage pressures
- Compressor selection map at varying bank pressure (not always 200bar endpoint), isentropic/volumetric and motor/VFD efficiency vs load, start/stop and off-design/minimum load, throughput and number of installed parallel/redundant trains
- Manifold and station pipe/valves/relief/instrumentation, lubricants and cross-contamination, leak rates, compressor seals/overhauls, cycles, associated process heat exchangers and **intercooler/aftercooler cooling energy and equipment weight**
- Dry compressor skid, motor, MCC/VFD, cooling and foundations **split component masses and material grades**, manufacturing energy, transport/assembly, O&M, maintenance, lifetime, quoted EUR cost basis and allowed data publication/licensing
- Real pressure loss and temperature-dependent usable gas stock at modeled peak **2,200kg/h permitted charge** and **2,083kg/h reference discharge**, with the **~552kg/h optimized 2023 maximum charge** marked as historical model output (not necessarily the design-rating target)
- Explicitly distinguish requirements of **gross stored mass 20/40t** from *usable* H₂ capacity, and qualification of time-dependent 2023 weather/market replay (not observed mechanical plant data)

No compressor manufacturer quote, signed P&ID, guarantee of dynamic pressure-safety compliance, full materials life cycle or price currently exists.

## 4. Manufacturing LCI and economic intake record — mandatory source fields

For each future actual supplier/manufacturer datum, record **provider name, exact product and revision, public/private rights, publication date, model/assembly diagram, EU PED and standards, source pressure gauge/absolute, test/working pressure, operating T, applicable H₂ composition, quantity unit, manufacturing geography/year, engineering source class, raw file SHA, reviewer, uncertainty and whether a site-specific guarantee exists**.

Make these source-data classes distinct:
1. **Confirmed** — actual OEM-manufactured and published part mass, material grade and fabrication or an approved quoted installed BOM for a specified site
2. **Research reference** — literature empty equipment mass and EOS pressure/volume from a paper at documented assumptions
3. **Derived** — counts and tank-heel mass from CoolProp with explicit temperature/pressure, or source-2023 modelled charge duty
4. **Engineering-assumed** — hypothetical pressure derating or an unapproved alternate module arrangement
5. **Not sourced** — use `null`, **never zero**, for factory steel input mass, module rack/manifold dry mass, compression and cooler dry mass, native provider-linked CO₂e, purchase price, service life/maintenance, site/pressure/purity, discounted cash flow or whole-system emissions

Original [BAFU 2026 v1 audited process UUID `b4739ad2-aa38-368d-8ada-63f5417c8b55`](https://github.com/Open-Energy-Methods/PtXLens/blob/feat/wp0-screening-core/data/results/BAFU2026_v1_storage_tank_source_unit_mismatch_audit.json) is an **automotive composite hydrogen tank** described per kg *hydrogen capacity*, not per kg *empty stationary Type I steel equipment*. **Never** multiply that provider by the 1.9248kt / 2.1648kt literature Type I empty equipment mass, by the 2.4691kt / 2.7760kt alternative OEM per-cylinder empty equipment, or by kilograms of stored H₂.

A native BAFU v1.1 foreground can be completed **only after** appropriate compatible steel, processing and physical equipment provider UUIDs, mass/process conversions, EOL and recycled scrap, and source manufacturing mass breakouts are independently matched, with original licensed BAFU inventory retained outside public repositories.

## 5. Release checklist

- [x] Physical source reference and *actual* separately identified OEM product masses/volumes/pressure classes surveyed; NEN-EN 17533:2025 and EU PED scopes recorded
- [x] CoolProp source 313K/20–200bar(a) shell-only count and gross/usable heel computed; 2023 physically screened F3-C source MIP duty linked and SHA verified
- [x] Nineteen categories of potential incremental equipment and lifecycle foreground identified (one shell equipment reference mass, 18 not quantified)
- [x] Vendor/outreach request *prepared only* (no messages sent)
- [ ] OEM revised datasheets and pressure-class/absolute/bar(g) conversion approved; complete stationary module **empty dry equipment and steel material BOM**
- [ ] Stationary rack/module, certified assembly/P&ID, safety standards and 2,200kg/h maximum design operating coverage verified at an *actual site*
- [ ] Manufacturer compressor, motor, cooling and BoP model/cost/mass/energy and maintenance/replacement uncertainty independently sourced and allocated to *incremental* plant
- [ ] Compatible native BAFU 2026 v1.1 foreground providers linked; complete with no unknown product mass or invalid vehicle-tank proxy
- [ ] Same-hour service functional unit, geographic/year mismatch, GWP uncertainty and whole lifetime discounted cost independent review and approval
- [ ] Original E/E+S/A44 source ZIPs preserved on user-owned private media, tested on physically independent backup well before 24 December 2026

**No correspondence, site connection study, supplier quote, financial agreement or industrial validation has been initiated. F2 and L1 full gates, L2/L3, P0 and hydrogen/methanol v1.0 remain NOT PASSED.**
