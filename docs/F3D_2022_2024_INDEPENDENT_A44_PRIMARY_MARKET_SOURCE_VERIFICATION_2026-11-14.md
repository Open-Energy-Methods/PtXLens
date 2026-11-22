# F3-D independent observed NL ENTSO-E market audit — 2022, 2023 and 2024

Date: 2026-11-14. Original 14-document A44 source ZIPs for **each** year acquired successfully by the [PtXFlex source workflow](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/43617006319), attempt 4. All original A44 provider XML files were independently SHA-256/length validated and re-parsed from raw data using a separate Python implementation of official A03 source-defined constant-price positions, including both PT60M and PT15M. Reconstructed quarter-hours were strictly grouped into each UTC hour and compared against the deposited normalized hourly price CSV: **zero price mismatches** in 2022 (8760), 2023 (8760), 2024 (8784). No interpolation or source gap filling was introduced.

| Year | Hourly NL mean EUR/MWh | Minimum | Maximum | Negative hourly prices | Original A44 XML count | Original-source UTC hours |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 2022 | 241.909755 | -222.36 | 871.00 | 86 | 14 | 8760 |
| 2023 | 95.817771 | -500.00 | 463.77 | 315 | 14 | 8760 |
| 2024 | 77.289214 | -200.00 | 872.96 | 458 | 14 | 8784 |

Original derived hourly price float64-le SHA256: 2022 `1a5490fd607d6c786878ca56b5d82ce8568f62b5277bc201206f1e6761b04f28`; 2023 `e67f59598079303df0c51a553904d2352a939ed7439af73ccbfb3daab9d667b6`; 2024 `834449561032a1c81f76950fd49b1b0276f6cd27b4a0e07e9188a09144574fce`. The 2023 SHA exactly reproduces the source-frozen PyNEXUS reference.

**Scope:** descriptive genuine NL market source years only. Neither ERA5 2022/2024 (still awaiting), nor matched hourly H2 delivery, comparable annual dispatch optimization, independent solver primal/dual certificates, CAPEX/OPEX manufacturer invoices, inflation-normalization or complete native BAFU environmental conclusions are implied. This file is not an investment recommendation or forecast.

The three provider-retrieved original source ZIPs are in a private user-owner Drive folder: https://drive.google.com/drive/folders/1DUUCaClrNXnNPrz6XWCGviHWup7NOOP_ (one storage location only; second independently restored backup not proved). Original hourly price data are intentionally excluded from GitHub.
