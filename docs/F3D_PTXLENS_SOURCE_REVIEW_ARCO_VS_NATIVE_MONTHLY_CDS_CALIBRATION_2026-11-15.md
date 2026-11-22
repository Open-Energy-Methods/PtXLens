# F3-D local source review: ARCO ERA5 alternative is not original monthly CDS

Date 15 November 2026. The live PtXFlex January 2023 ARCO geo-chunked point pilot **actually matched 744 source-original PyNEXUS CDS wind-power hours at 1W resolution** with 0 MW maximum recorded discrepancy and 7.2-second remote data read. The full 8,760-hour 2023 calibration and 2022/2024 yearly alternate ERA5 source reads are **new unexecuted stages**. They are not source-verified results until local user execution.

The linked [PtXFlex calibrated fast ARCO path](https://github.com/Open-Energy-Methods/PtXFlex/blob/feat/milp-methanol-baseline/docs/F3D_ARCO_FULL_2023_8760H_SOURCE_EQUIVALENCE_AND_LOCAL_2022_2024_RETRIEVAL_2026-11-15.md) is designed to bypass long-monthly CDS processing queues without changing the model's point 52.5N 3.5E, physical wind conversion or original 2023 source reference. It uses complete original 2023 CDS twelve-month SHA verification; 2023 8,760-hour ARCO direct point data; every hour's 1W wind equivalence; four original U/V components at 10m and 100m; and explicit source generation provenance.

For each 2022 and leap 2024 calendar, the independent PtXFlex source gate must verify actual private ARCO point extraction NetCDF files, 8,760/8,784-hour UTC continuity, per-component native SHA/dtype, recomputed wind MW and complete 2023 source calibration certificate before it can pass the source data to any economic comparison. The ORIGINAL NetCDF monthly provider workflow remains separate. No ARCO data may be presented as original CDS monthly NetCDF bytes.

PtXLens's F3-D annual source reviewer now explicitly refuses a source-year/model metadata report where:

- Repackaged ARCO is falsely tagged as ORIGINAL_MONTHLY_CDS_ERA5_NETCDF;
- It claims the full 2023 original hourly calibration without the corresponding source-gate classification;
- The two capacity-interpretation cases for one year use different wind-source representations, even if annual price/wind hashes were otherwise supplied.

The independent hourly private witness replay remains unchanged and must still recompute hydrogen mass storage, compressor/PEM/electricity balance, same-hour E/E+S H2 delivery, signed grid settlement and 313 K/20–200bar hydrogen CoolProp EOS using the real private source-year arrays. This does not constitute an independent external plant measurement, investment-capital quote, native BAFU whole-plant GWP/LCIA or verified investment NPV. The strict model 2022/2024 solver/validation/witness stage remains NOT PASSED until the user's actual local full-year provider sources and MIP witnesses are available.

The local implementation and negative tests are versioned; the GitHub organization has exhausted its included Actions minutes so new code tests cannot presently be certified from hosted CI. The source Windows PowerShell script runs all tests, full-year ARCO source calibration, alternative annual data acquisition, four cost-optimal MILPs and PtXLens independent review locally.
