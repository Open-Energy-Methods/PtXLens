# F3-D live ENTSO-E / ERA5 historical-year intake — 2026-11-14 status and independent Lens gate

Programme OEM-PTX-2026-01. The upstream [PtXFlex live source workflow](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43617006319) implements original raw Dutch A44 XML plus ERA5 four-component 100m wind retrieval for 2022, 2023 and leap-year 2024. The original 2023 Dutch price XML in the recovered source archive was independently expanded (source A03 semantics) to all 8,760 UTC hours and its resulting float64 SHA exactly reproduced the frozen price fingerprint `e67f59598079303df0c51a553904d2352a939ed7439af73ccbfb3daab9d667b6`.

**Actual GitHub Actions observation:** the live workflow's offline unit tests passed. All three ENTSO-E retrieval jobs and all three ERA5 retrieval jobs failed their *secret availability* preflight, before calling either provider. The organization-level `ENTSOE_API_KEY` and `ERA5_API_KEY` are therefore **not available to the PtXFlex private repository Actions context**, even though the user reports adding them as organization secrets. Fix organization secret selected-repository access and plan restrictions, or add both as **repository secrets** to PtXFlex. Never commit keys or print their values. Do not claim that an external source year has been fetched.

The source workflow includes original monthly provider SHA/byte manifests, 2023 frozen price and wind float64 reference calibration, strict 8,760/8,784 UTC coverage, original 100m-to-120m offshore shear, PyNEXUS cubic farm availability cap 125.685 MW, and a source-only pairing certificate. Each original provider ZIP/NetCDF and normalized source file is retained in **temporary private Actions artifacts for 7 days only**; this is *not* durable source escrow and not permission to publish provider data.

## Independent PtXLens release conditions

1. Require both source-year original price and wind SHA manifests, genuine local validated provider source files, calibrated 2023 re-derivation (both price and wind), negative-price preservation, original market timezone handling and explicit correct 2024 leap day.
2. Require independently selected source-year E-deliverable *hourly* hydrogen service, not a repackaged 2023 hourly E target, and the **identical hourly service** for E and E+S within each year/storage interpretation.
3. Require separate solver integer feasibility and independently audited primal/dual economic cost bounds for both cases. A feasible LP relaxation does not imply a feasible MILP. If any required service is not achieved, matched-service advantage is undefined, not zero.
4. Do not pool 2022/2023/2024 nominal electricity euros in present-value terms without explicit calendar-price-year normalization and independent finance assumptions.
5. Do not label partial original-2023 BAFU foreground inventory, unpublished provider data or literature-only pressure-vessel equipment costs as native whole-plant LCA, manufacturer quotations or commercial investment feasibility.
6. P0 currently has one **Google Drive escrow** folder containing three recovered original 2023 ZIPs with correct recorded byte sizes and owner-only permissions, but no proven second independent recovery/storage domain. The user-controlled Drive path is outside these repositories. P0 remains NOT_PASSED pending actual independent restore and legal review.

**Current external observed year count admitted to F3-D: zero.** This document is an independent intake decision record and does **not** change any numerical results or programme gate. Both repositories remain pre-v1.0.
