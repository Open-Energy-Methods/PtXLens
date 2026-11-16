# 2023 Dutch wind-to-hydrogen — life-cycle impact research note (v0.1)

**Research status: verified 2023-source electricity-supply GWP calculation plus published PEM stack material foreground. NOT a complete hydrogen cradle-to-gate LCA, NOT openLCA LCIA, and NOT an ISO 14044-compliant comparative assertion.**

Date: 13 November 2026. Model: original PyNEXUS, research freeze 26 October 2026. Recalculation code: [lca_screen.py](../src/ptxlens/lca_screen.py). [Continuous verification](https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43424086998).

## 1. Goal, scope and functional unit

Quantify **the electricity-supply life-cycle GWP component** associated with the actual 2023 Dutch wind+grid electricity inputs used by the *modelled* hydrogen E and E+S PyNEXUS dispatch cases. Functional unit: **1 kg of modelled H2 delivered against demand over 2023**, with no claim of chemically verified purity or delivery pressure.

- Real-source inputs: 8760 historical Netherlands ENTSO-E day-ahead electricity-price hours and ERA5-derived North Sea wind driving the original PyNEXUS optimization; two original Stage B CSV archives, SHA256 checked. Hydrogen, consumed power and storage throughput are **solver outputs**, not physical plant measurements.
- GWP factor approach: Dutch **2023 national location-based** production+upstream electricity factor with infrastructure; UNECE/EU28 reference offshore wind LCA intensity. Both are **annual/reference** factors, not hourly or marginal carbon signals. No time-dependent emissions claims.
- Allocation to electrolysis: grid electricity imports plus offshore wind produced but not curtailed or exported. Wind-supply lifecycle factor incorporates infrastructure. Grid infrastructure added once, not double counted separately. No credit for exported electricity, no certification or counterfactual consequential LCA.
- Included: electricity supply GWP only. **Excluded:** PEM manufacturing, equipment replacement, storage, water treatment, compression, pipeline, delivery-pressure processes and end-of-life. A material LCI is now available separately, but intentionally has no assigned production-process GWP before authentic background providers are linked.

## 2. Primary factors (explicit component separation)

| Input | Published factor (kg CO2e/kWh) | Source and boundary |
|---|---:|---|
| Dutch grid electricity generation | 0.290 | Dutch Rijkswaterstaat/Stichting Stimular 2023 |
| Dutch grid upstream fuel chain | 0.047 | Same 2023 source |
| Dutch grid power-plant infrastructure | 0.007 | Same 2023 source, add *once* to 0.337 |
| Offshore wind lifetime supply chain | 0.0142 | UNECE 2021 life-cycle electricity-generation assessment, offshore wind EU28 benchmark |

**Grid total used: 0.344 kg CO2e/kWh = 0.290 + 0.047 + 0.007.** This is *not* the CBS direct combustion-only 0.22 kg CO2/kWh indicator; the scopes and labels differ.

Sources (manual primary-source verification):
- https://co2emissiefactoren.nl/factoren/2023/11/52/elektriciteit-stroom-onbekend-gridmix/
- https://unece.org/sed/documents/2021/10/reports/life-cycle-assessment-electricity-generation-options
- https://wiki.unece.org/download/attachments/271089909/A-LCA-20-05e_infrastructure%20emissions_ICCT.pdf?api=v2

## 3. Original evidence and independently reproduced arithmetic

Original PyNEXUS source: https://github.com/abhijith-sivaprasadan/PyNEXUS/actions/runs/40229852457
2023 NL price provenance audited independently: https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43420276286 (all 8760 hours match, max absolute difference 0 EUR/MWh).
2023 hourly LCA input/GWP workflow: https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43424086998 .

For one modelled hour t:

    wind_to_electrolyser_MWh[t] = wind_available[t] - curtailment[t] - grid_exports[t]
    electrolysis_MWh[t] = wind_to_electrolyser_MWh[t] + grid_import_MWh[t]
    grid_generated_GWP_kg[t] = grid_import_MWh[t] × 1000 × 0.290
    grid_upstream_GWP_kg[t] = grid_import_MWh[t] × 1000 × 0.047
    grid_infrastructure_GWP_kg[t] = grid_import_MWh[t] × 1000 × 0.007
    wind_lifecycle_GWP_kg[t] = wind_to_electrolyser_MWh[t] × 1000 × 0.0142
    GWP_supply_per_kg_H2 = sum(hourly_supply_GWP_kg[t]) / sum(modelled_H2_delivered_kg[t])

The CI separately recomputes all source-hour input identities and validates aggregate values from every hourly CSV.

| 2023 model and electricity-supply GWP | E | E+S |
|---|---:|---:|
| Delivered modelled H2 (kg) | 16,335,279.3 | 16,679,072.1 |
| Grid consumption for electrolysis (MWh) | 300,591.3 | 302,644.2 |
| Wind consumed for electrolysis (MWh) | 474,370.1 | 488,880.9 |
| Grid generation (tonnes CO2e) | 87,171.46 | 87,766.81 |
| Grid upstream fuel (tonnes CO2e) | 14,127.79 | 14,224.28 |
| Grid infrastructure (tonnes CO2e) | 2,104.14 | 2,118.51 |
| Offshore wind full supply chain (tonnes CO2e) | 6,736.06 | 6,942.11 |
| **Total electricity-supply GWP (tonnes CO2e)** | **110,139.45** | **111,051.70** |
| **Electricity-supply GWP/kg modelled delivered H2** | **6.74243** | **6.65815** |

Reported difference in intensities: -0.08428 kgCO2e/kg modelled H2 (E+S vs E). Total system electricity-supply GWP increases by ~912.25 t because E+S also delivers 343,792.77 kg more modelled H2. The comparison is **not** service-matched, not an LCA interpretation that E+S is environmentally superior.

Sensitivity: excluding the 7 g/kWh grid plant infrastructure component yields E = approximately 6.61362, E+S = approximately 6.53113 kgCO2e/kg modelled delivered H2. The preferred electricity-supply boundary includes the infrastructure to align more closely with the wind supply factor.

## 4. Published foreground PEM stack material inventory

Reference: Olga Kanz (2024), *Life Cycle Assessment of Photovoltaic Applications*, Eindhoven University of Technology, Appendix B, Table B:8, p.136:
https://pure.tue.nl/ws/portalfiles/portal/330479277/20240626_Kanz_hf.pdf

One nominal 1 MW PEM stack reference includes 528 kg titanium, 27 kg primary aluminium, 100 kg chromium-nickel steel, 4.5 kg copper, 16 kg Nafion/membrane precursor proxy, 9 kg activated carbon, 0.75 kg iridium-bearing platinum group metal concentrate and 0.075 kg platinum. **These are mass inputs**, not characterized emission coefficients or supplier-specific lifecycle impacts. The original study used GaBi/ecoinvent background records; those are not distributed here.

Reference data: [published stack inventory](../data/lci/pem_stack_kanz_2024_1mw.json).
A separate CI calculation, source-verified against the original PyNEXUS 8760-hour model, can allocate these inputs per hypothetical delivered hydrogen over 30 repeated operating years with a 40,000-hour replacement interval: https://github.com/Open-Energy-Methods/PtXLens/actions/runs/43425080024 . This allocation is a **declared scenario assumption**, not a measured 125 MW electrolysis plant composition, and is not yet added to the numeric supply-GWP above.

What the LCI still needs: compatible and legally usable linked providers for the eight materials plus physically specified electrolyser BoP, stack manufacturing energy, storage, 9–10 L water/kg H2 and water treatment, compression and delivery, disposal/recycling. The source paper's reference manufacturing inputs are predominantly from proprietary databases and cannot be silently reconstructed.

## 5. Real openLCA calculation acceptance gate

The existing [IPC interface](../src/ptxlens/olca_real.py) checks user-selected product-system and impact-method UUID/name and dispatch energy parameters. **No openLCA engine result is published or claimed** because a complete linked database, flow IDs/providers and a compatible GWP100 method have not yet been created.

For next validation:
1. Build a linked foreground product system for 1 kg delivered H2 at explicitly stated delivery gate, source-resolved electricity, 1MW-to-125MW stack material mapping, replacements, water, compressor, BoP and storage.
2. Import open LCI background providers and a named method into an actual local or headless openLCA database; run numerical provider/flow completeness and LCIA method check.
3. Run the same product system with E and E+S dispatch-reparameterizations. Collect native openLCA impact-category results, detailed contribution matrix and independently reproducible checks against the existing supply-GWP study.
4. Reconcile full product-system boundaries before making a comparative statement. Check 2023 Netherlands-specific dataset representativeness; USLCI is not a Dutch background by default.
5. Publish full source, version, impact-method, and dataset licences; do not upload restricted proprietary LCI.

**Until step 3 passes with genuine provider data, status is electricity-supply LCA-informed GWP screening plus a sourced PEM material LCI — not complete cradle-to-gate LCA.**

## 6. Scientific risks / limitations

- Comparing real market inputs with *simulated* electricity and H2 production does not validate operation against actual plant measurements.
- Published grid **annual mean**, not 8760 hourly marginal/consumption intensities. Price arbitrage effects on actual carbon cannot be inferred from this method.
- National grid electricity production mix vs imported electrical energy has possible methodological mismatch, as does EU28 offshore wind vs actual North Sea turbine vintage.
- Upstream GHG factors involve distinct production and infrastructure allocation methods. The combination is an explicitly declared reference boundary, not a complete product LCIA calculated from compatible elementary flow inventory.
- Functional unit delivery pressure (30bar modeled electrolysis output, 20bar pipeline minimum in PyNEXUS configuration) is not independently verified, and downstream use/conditioning is excluded.
- Asset lifetimes and storage size differ; no matched-service optimization or incremental footprint is established by simple reported intensity differences.
- No methane leakage, electrolyte/water disposal, material extraction supplier impacts beyond published reference inventory, refrigerants or system boundary harmonization yet.

Data licensing: source documents are cited; no original proprietary background inventories or copyrighted thesis PDF redistributed. Software is MIT; source data retain their own terms.
