# BAFU:2026 v1.1 — native Dutch 2023 E / E+S hydrogen GWP100

**Executed and source-verified: 13 November 2026.** This is a native GreenDelta openLCA process-linked result for **electricity- and water-reparameterized 30-bar PEM reference systems**. It is **NOT** a complete, service-matched environmental assessment of E vs E+S once their different hydrogen storage infrastructure, compression, losses and transport are considered.

## Verified original source data

- **Original native model:** user-authorized BAFU:2026 **v1.1** \`.zolca\`, exact uploaded source SHA256 \`e63b7e7ef5cde04bfe1176a783a55b5f72e2b73f42c36632b6150af39d348c4c\` (135,424,513 bytes). The raw model is never uploaded to GitHub or redistributed.
- **Independent source reference:** BAFU:2026 **v1** EcoSpold inputs ZIP, SHA256 \`ebaab56717a6227b5eb271fcb4c86fb9db206115eb937fb0ec0b10d7accf26c7\`; corrected v1 LCIA workbook ZIP, SHA256 \`a692f72705baac82fc59e85e00389302446ac2d5e921ab9df86fce7441a49e01\`. These **are not presumed identical** to v1.1, but provide an independently audited reference.
- **Actual 2023 operation *model* inputs:** original [PyNEXUS frozen observed-price archives](../data/source_registry/pynexus_wp5_2023.json): E SHA256 \`069455704573825f4e709e6705f5db43823722909cb93a37bd86b978636fb051\`; E+S SHA256 \`cd4101fe62c3f1b8aa2d7508d3651d2fee40d2bafe6d5b87e40d5f4d055070f9\`. 8,760 modeled operating hours driven by 2023 observed Netherlands electricity market and ERA5-derived wind, **not plant telemetry**. Model-delivered H₂ differs between cases.
- Method: **IPCC 2021**, exact native impact category **\`IPCC 2021 GWP 100\`**. Do not accidentally choose \`AGWP 100\`, \`GWP 20\`, an alternate biogenic variant or weighted single-score.
- Engine: actual **GreenDelta openLCA-core 2.7.0 Java/Derby**, **GreenDelta optional UMFPACK sparse solver** (GPL; keep separate from MPL software and comply with upstream terms).

### Native source checks and independent reconstruction

For the original **Swiss** 30-bar PEM process UUID \`99a1af16-58cd-3f11-a877-c43d3c8e5d78\`:

| Check | Verified result |
|---|---:|
| Processes in source BAFU v1.1 | 11,947 |
| Available LCIA methods | 46 |
| Native linked original Swiss product-system processes | 4,235 |
| Native supplier links | 52,066 |
| Unlinked product inputs / waste outputs | **0 / 0** |
| Native BAFU **v1.1** IPCC 2021 GWP100 | **5.541965561665505 kgCO₂e/kgH₂** |
| Corrected published BAFU **v1** reference GWP100 | **5.541965540130873 kgCO₂e/kgH₂** |
| Difference between the two releases | **0.000000021535 kgCO₂e/kgH₂** |

The BAFU v1 source *six original direct inputs* (54 kWh CH LV electricity, 14 kg deionized water, stack and balance-of-plant manufacture and their end of life) independently reconstruct the v1 corrected total within **2.4 × 10⁻¹⁰ kgCO₂e/kgH₂**, using an explicit 3.6 MJ/kWh conversion. This is a **reference numerical cross-check**, not proof that every source version and inventory exchange is identical.

The original v1 EcoSpold provider graph independently reaches 4,219 upstream processes with 52,010 matched product input links, **zero unmatched and zero ambiguous**. The separate v1.1 native product-system linking is verified independently above.

## Reparameterized native 2023 Netherlands E/E+S results

The native program builds separately named, **new process copies in a local scratch database**, preserving the original uploaded BAFU source. It replaces the original CH 54 kWh/kgH₂ low-voltage grid supply with **original-model** grid and offshore-wind use per modeled delivered H₂, and replaces the original CH water provider with an actual NL deionized-water provider at the original 14 kg water/kg H₂. It **retains** the original BAFU 30-bar PEM reference electrolysis stack, balance of plant, end-of-life and other upstream materials.

Authentic 2023 E and E+S source energy consumption is time-integrated from hourly PyNEXUS records and aggregated per model-delivered kg H₂ (not arbitrary fixture demand).

| Source and native GWP100 indicator | E | E+S |
|---|---:|---:|
| Model-delivered H₂ during 2023 (kg) | 16,335,279.3174 | 16,679,072.0879 |
| NL grid input per model-delivered H₂ (kWh/kg) | 18.401354 | 18.145143 |
| Offshore wind input per model-delivered H₂ (kWh/kg) | 29.039608 | 29.311038 |
| Original-model configured H₂ storage **capacity** (kg) | 20,000 | 40,000 |
| Native linked processes | 4,240 | 4,240 |
| Native supplier links | 52,123 | 52,123 |
| Missing product inputs / waste outputs | **0 / 0** | **0 / 0** |
| **Native BAFU v1.1 IPCC 2021 GWP100 (kgCO₂e/kg model-delivered H₂)** | **6.148174395784** | **6.076552653893** |
| Independent BAFU corrected v1-factor reconstruction (kgCO₂e/kgH₂) | 6.148174403272 | 6.076552667834 |
| Absolute native-vs-independent difference (kgCO₂e/kgH₂) | **7.49 × 10⁻⁹** | **1.39 × 10⁻⁸** |

**E+S minus E** on this *restricted shared-foreground boundary*: \`-0.071621741891\` kgCO₂e/kg model-delivered H₂. This is a **diagnostic variation attributable to the modeled electricity allocation under common 30-bar reference inputs**, not evidence E+S has lower overall cradle-to-gate impact.

Both independent scenarios calculated successfully with real native openLCA matrix solutions and exact GWP100 impact-category selection; all linked product/waste checks passed before accepting a result.

### Scientific scope, unresolved additions and limitations

1. **E+S has 20,000 kg *additional configured hydrogen storage capacity***, but the original dispatch model does not provide the actual storage vessel weight, vessel design, operating pressure, composite/steel grade, construction power, compressor equipment, or storage losses as a buildable plant inventory. The BAFU original 30-bar PEM reference manufacturing is the same in E and E+S; **additional E+S tank/plant manufacture is NOT included** in either new scenario. Storage *capacity* cannot be interpreted as storage-equipment mass.
2. **The E and E+S functional service differs**: additional modeled H₂ delivered in E+S ~343,793 kg over 2023. Comparative superiority at a *matched* hydrogen demand/purity/pressure/output service has not been established.
3. The BAFU offshore-wind supplier is a **legacy \`xx Electricity, at wind power plant 2MW, offshore\` reference**, not modern actual Dutch offshore fleet output; its location/source vintage and capacity scaling need uncertainty evaluation.
4. The **BAFU:2026 v1.1** LCIA geography and life-cycle assumptions cannot automatically represent original Dutch 2023 electricity suppliers; NL low-voltage electricity references and NL deionized water are from the real BAFU database, but factors are published-background values rather than time-matched marginal electricity carbon.
5. The original BAFU 30-bar H₂ gate does not validate downstream transport, site operating performance, or end-use H₂ pressure/purity; no proprietary plant data were measured.
6. The user's separate \`bioenergiedat_18.zolca\` was **not mixed into the hydrogen product system**; no invented biogenic credits assigned.
7. Native **supplier closure** does not by itself prove scientific completeness, technology representativeness, ISO 14044 conformity, elementary flow characterization completeness or absence of uncertainty. It is a strong necessary verification rather than a sufficient certification.

**Publication status:** Fully executed and independently checked native GWP100 for a **scoped BAFU-reference reparameterization**; **not** a complete industrial Dutch E/E+S hydrogen energy/storage-system life-cycle comparison. Keep the PR draft pending storage/pressure/matched-service and geography sensitivity.

## Reproducing without exposing original licensed data

- Keep authorized BAFU v1.1 original zolca file **outside GitHub** (see [gitignore](../.gitignore)).
- Verify its SHA256 against the source above.
- Source-only PyNEXUS dataset and scenario input construction: [bafu_native_scenario_config.py](../src/ptxlens/bafu_native_scenario_config.py).
- Native source import/link audit: [BafuZolcaAudit.java](../native-openlca/src/main/java/org/openenergymethods/ptxlens/BafuZolcaAudit.java).
- Native reference GWP100: [NativeBafuCalculation.java](../native-openlca/src/main/java/org/openenergymethods/ptxlens/NativeBafuCalculation.java).
- E and E+S cloned reference foreground and native sparse GWP100: [NativeBafuDutchScenario.java](../native-openlca/src/main/java/org/openenergymethods/ptxlens/NativeBafuDutchScenario.java).
- Independent original BAFU v1 corrected reference reconstruction against six direct source exchanges: [bafu_uploaded_reconcile.py](../src/ptxlens/bafu_uploaded_reconcile.py). This needs Python \`lxml\` (install \`pip install -e ".[lca]"\`).
- Use a scratch **copy** of restored private database for E and E+S; ensure the original raw source remains unchanged; private source files, native Derby directories and provider matrix must not appear in public CI artifacts. Use the optional separately GPL-licensed GreenDelta UMFPACK native solver for the ~4.2k process matrix (the pure Java dense LU fallback is impractical).

Full BAFU background citation: *Database of the Swiss Federal Administration, BAFU:2026, Federal Office for the Environment, 2026*. Original user-provided v1 EcoSpold and corrected LCIA are distinct from the v1.1 native database. Original PyNEXUS historical 2023 model source: [PyNEXUS](https://github.com/abhijith-sivaprasadan/PyNEXUS).
