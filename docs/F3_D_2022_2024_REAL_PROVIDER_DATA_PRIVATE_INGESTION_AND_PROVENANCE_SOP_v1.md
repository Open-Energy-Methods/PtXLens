# F3-D external historical-year source admission SOP — genuine 2022 and 2024 ENTSO-E / ERA5 pairs

**14 November 2026 · Programme OEM-PTX-2026-01 · Current status: 0 source-approved alternative observed historical years.** This procedure prepares verifiable acquisition and physics-continuity; **no 2022 or 2024 provider pair has been downloaded, source-hashed, admitted, or model-solved in the PtXFlex/PtXLens programme**. The 2023-derived 2023 perturbations must never be relabelled as observed years.

## Why the requested data are not yet available

The public [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/) day-ahead price document A44 for **Netherlands bidding zone NL** is accessible through a registered/authorized API credential for automated retrieval; source code already exists in the original [PyNEXUS `data/entsoe.py`](https://github.com/abhijith-sivaprasadan/PyNEXUS/blob/main/data/entsoe.py). Direct source access in this current repo execution does not provide a verified private provider API credential or a 2022/2024 raw provider document, so claiming a genuinely collected source year would fabricate evidence.

The original offshore resource series is **ERA5 at 52.5°N, 3.5°E**, requiring the [CDS dataset](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels) with 100m and 10m u/v wind components, the accepted provider licence and a user-authorized API credential. PyNEXUS's actual original [`data/era5.py`](https://github.com/abhijith-sivaprasadan/PyNEXUS/blob/main/data/era5.py) fetches **12 monthly raw NetCDF provider files** and enforces UTC coverage; source [`components/wind_turbine.py`](https://github.com/abhijith-sivaprasadan/PyNEXUS/blob/main/components/wind_turbine.py) models turbine availability. A national Dutch measured *total wind production* series is NOT the point-specific ERA5/turbine-resource profile and cannot replace it. The original PyNEXUS 2023 configuration [`configs/annual.yaml`](https://github.com/abhijith-sivaprasadan/PyNEXUS/blob/main/configs/annual.yaml) names the weather point “North Sea / Netherlands”, not an industrial storage site.

Existing authenticated original PyNEXUS 2023 archive artifacts are ephemeral, requiring lawful private independent recovery before **24 December 2026**; new provider data must **also** be privately source-archived with original licensing respected, not pushed as raw data or price tables to these public repositories.

## 1. Correct original physics/calibration to preserve

ERA5 four wind components `u10,v10,u100,v100` are hourly UTC reanalysis fields. PyNEXUS computes `v100 = sqrt(u100²+v100²)`, then shear-adjusts to **120m hub**: `vhub = v100*(120/100)^0.11` (offshore `alpha=0.11`). Its original 15MW×10 **cubic** farm power curve is zero below **3 m/s**, ramps cubically to rated speed **13 m/s**, caps above rated to cut-out **25 m/s**, shuts down above 25m/s, then applies **10% wake, 2% electrical and 5% unavailability**. Thus original static modelled maximum source wind power is `150*.9*.98*.95 = 125.685 MW`, **not 150MW available**.

In original 2023 source F3-D, the +10%/−10% *available wind electrical MW multipliers* do NOT recalculate this wind-speed curve and cannot be mistaken for authentic new ERA5 wind samples.

The 2023 source-archived original E/E+S output SHA provenance:
- Source E archive: `069455704573825f4e709e6705f5db43823722909cb93a37bd86b978636fb051`
- Source E+S archive: `cd4101fe62c3f1b8aa2d7508d3651d2fee40d2bafe6d5b87e40d5f4d055070f9`
- Original 2023 available-wind float64 little-endian SHA: `abbfea17224cd92f694ed26b7a179ef7e35fff5a5bb17c6ee060a674c1977717`
- Original 2023 NL day-ahead price float64 little-endian SHA: `e67f59598079303df0c51a553904d2352a939ed7439af73ccbfb3daab9d667b6`

**Mandatory normalization calibration:** before using any reconstructed 2022/2024 wind MW, independently reproduce the exact 2023 original 8,760h wind MW and price arrays with newly fetched original provider files, original source PyNEXUS model/transformation revision SHA, and compare their *float64 little-endian SHA* with the frozen source above. Otherwise a wind-height/units/timezone mismatch may look like genuine interannual variability.

## 2. Provider acquisition and private admissibility

1. **Original ENTSO-E:** use an authorized `ENTSOE_API_KEY` from the official provider account and source `data/entsoe.py` / documented 2023 primary [A44 workflow](https://github.com/abhijith-sivaprasadan/PyNEXUS/blob/main/.github/workflows/wp1-entsoe-raw-a44.yml). Request full original 2022 and 2024 Dutch A44 market price intervals with enough start/end days on the Europe/Amsterdam market clock to recover exact **UTC** year coverage. Preserve raw original XML and SHA; any native 15-min price blocks must be **duration-weighted** to hourly, never averaged over irregular or duplicated DST data. Retain **negative prices**, correct EUR/MWh units and bidding zone NL.
2. **Original ERA5:** use authorized `CDSAPI_KEY` for [ERA5 single levels](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels) and the source `data/era5.py` 12-month fetch method (which already contains exact 2023 source-precedent, non-silent missing-hour checks); obtain the grid cell returned for 52.5N 3.5E, exact hourly native UTC; retain original monthly NetCDF SHA, 100m/10m four components, expver and source request. Do not privately/source-store the API tokens inside actual raw data or public logs.
3. **Original turbine and site-free conversion:** apply the exact original PyNEXUS `components/wind_turbine.py` source model, store the generating code revision hash, no re-shearing a 120m hub value again, no wind-speed×0.9 substituted for available power×0.9, no clipping rates beyond original physical turbine curve.
4. **Full-year calendar integrity:** 2022 starts `2022-01-01T00:00:00Z`, ends `2022-12-31T23:00:00Z`, **8,760** hours. 2024 starts `2024-01-01T00:00:00Z`, ends `2024-12-31T23:00:00Z`, **8,784** hours including 29 February. The existing original 2023 `solve_ideal_storage` code checks `n<=8760`: it must be explicitly upgraded and retested for 8784, NOT quietly drop leap day or reinterpret 2024 as 2023. No hourly price forward-fill/interpolation or arbitrary duration correction without explicit provider gap decision.
5. **Rights and independent copy:** record every raw provider file SHA, supplier permission, original request and raw/normalized file timestamps in a user-controlled PRIVATE source manifest; preserve two recoverable independent copies with verified ZIP/NetCDF/CSV bytes and explicit legal/technical reviewer notes. Keep only source hashes and admissibility certificates in public PtXFlex/PtXLens.
6. **2023 external conversion cross-validation:** repeat original 2023 from privately preserved primary provider files to the archived exact original 2023 SHA values stated above; if not exact, investigate physical power-curve, 100m grid, time-of-day alignment, negative-price handling, data vintage/revision, provider corrections and turbine model version. Do not force a match via post-hoc scaling and call it original source.

## 3. Implemented private offline data admission

[`src/ptxflex/f3d_external_observed_year_private_intake.py`](../src/ptxflex/f3d_external_observed_year_private_intake.py) validates the **private local input documents**, their expected SHA-256, original provider/type/zone, separately authenticated original raw monthly price/wind files, 2022/2024 exact UTC calendar, negative market prices, time-independent original cubic turbine cap `125.685MW` and original source-2023 model-reproduction evidence. It writes only a **sanitized metadata/aggregate checksum certificate**—no raw source pricing/wind tables or private paths. This is an intake gate, not validation of an actual H₂ installation, and source reviewer signoff and physics reoptimization still follow.

The [public research admission ledger](../research/F3_D_ALTERNATIVE_OBSERVED_2022_2024_ENTSOE_ERA5_PRIVATE_SOURCE_ADMISSION_v1.json) has 2022/2024 original raw SHA **NULL**, normalized UTC data SHA **NULL**, provider-auth and source 2023 rederivation **NOT VERIFIED**, and zero eligible external observed year pairs. The registered [hermetic synthetic-only calendar/units/error tests](../tests/test_f3d_external_observed_year_private_intake.py) explicitly verify leap 8,784h, missing/duplicate UTC, DST-related UTC shifts, negative EUR/MWh prices and physical 125.685MW farm cap, with no synthetic sample labelled observed.

**Example after genuine private acquisition**, with a locally created and independently verified private manifest (not yet available):

```bash
python -m ptxflex.f3d_external_observed_year_private_intake \
  --private-manifest /PRIVATE/verified-observed-year-source-manifest.json \
  --private-source-root /PRIVATE/observed-historical-providers \
  --output outputs/F3D_private_2024_original_provider_hourly_provenance_only.json
```

The manifest schema is `ptxflex.f3d_external_private_provider_original_year_and_reconstructed_2023_sha.v1`. It must specify `year: 2022 or 2024`, genuine `price` and `wind` provider source with at least 12 original private raw documents and per-document SHA, original normalized private CSV `timestamp_utc,day_ahead_eur_mwh` and `timestamp_utc,wind_available_mw`, each CSV SHA, the original power-curve/reanalysis conversion, and a private **2023 source SHA reproduction attestation**. A false or missing raw SHA, placeholder source, missing leap hour, incomplete H₂/year/physics scope or non-verified price/ERA5 origin must not advance v1.0. An output for private data calendar eligibility **is not yet a successful full F3-D observed-year physical/economic validation**.

## 4. New-year optimization and scientific cross-year design

Once *genuine* source pairs are independently admitted, do not automatically reuse the 2023 Stage A E-physical shortage hour vector as a new-year guaranteed product contract. Specify and independently solve the H₂ deliverability question for each year: either a **predefined identical customer service profile** with explicit year/calendar normalization (and potential shortfall) or a source-year-specific constructively feasible E hourly profile derived *without using the E+S result* and applied identically to both E and E+S. Declare which question is answered. F3-D can then report **comparisons within each matched year/mode**, with consistent 2022/2024 inflation/currency normalization if interpreting monetary differences. Source 2022/2024 must be **solved**, not used as independent evidence for the original 2023 market-only DCF without new operations. Maintain the distinction between `max_inventory` and `usable_service`, identical hourly product delivery, original compressor/pressure limitations and full 2023 industrial service deficits.

Only then consider extended field wind, source abnormal periods and future grid price scenarios, true stationary manufacturer/CAPEX and native BAFU linked manufacturing inventories. The investor, industrial customer and GHG scope are unknown until appropriate external evidence is obtained.

**Status / stop:** **Observed-year 2022 = NO VERIFIED PAIR. 2024 = NO VERIFIED PAIR.** Method, source-specific physical pipeline and negative ingestion tests implemented. We cannot responsibly claim genuine external year reoptimization, full H₂ contract service, whole plant investment NPV, native full-plant LCIA or v1.0 scientific release from the 2023 source perturbations.
