# RC2-C — reproducible numerical and native runtime environments

**Status:** source-scoped research software qualification; never full scientific v1.0, industrial validation, or a fresh private annual optimization/LCIA.

## Paired Python profile and tested platforms

The reference dependency versions are taken from the successful 18 November 2026 RC2-B CI package install logs. The Python 3.11 patch releases differ: Linux Ubuntu 24.04 x86-64 3.11.18; Windows Server 2022 x64 3.11.9. These are explicit distinct profiles; ABI compatibility or numerical acceptance is not a claim that their interpreters, BLAS builds, CPU architectures or OS distributions are byte-identical. Both profiles use NumPy 2.4.6, SciPy 1.17.1, CoolProp 8.0.0, pandas 2.3.3, xarray 2026.9.0, pytest 9.2.0 and the reviewed direct/transitive set. Bootstrap/build packages and threadpoolctl/colorama are explicitly pinned additions. The Python versions are the observed qualified profile, not a general recommendation that all users remain on those patches indefinitely.

The canonical locks are maintained in [PtXFlex environment](https://github.com/Open-Energy-Methods/PtXFlex/tree/feat/rc2c-locked-environment/environment). Both platform lock files contain 25 pinned distributions and one SHA-256 per actual chosen wheel. Each was generated from the corresponding runner's PyPI binary wheel download, inspected top-level wheel metadata, and recorded in a separate wheel filename/hash manifest. Source: [candidate CI run 44418233340](https://github.com/Open-Energy-Methods/PtXFlex/actions/runs/44418233340). New candidate generation must not silently replace a reviewed lock. PyPI upstream publisher authenticity/availability and interpreter/OS binary supply-chain assurance remain separate; this is not a full vulnerability assessment.

## Reproduce locally

Use a fresh venv, not the existing source-research venv. From the PtXFlex checkout:

    py -3.11 -m venv .rc2c-venv
    .\.rc2c-venv\Scripts\python.exe -c "import sys; print(sys.version)"
    .\.rc2c-venv\Scripts\python.exe scripts/rc2c_environment_lock.py install --lens-root ../PtXLens
    .\.rc2c-venv\Scripts\python.exe scripts/rc2c_environment_lock.py verify
    .\.rc2c-venv\Scripts\python.exe scripts/rc2c_numerical_reproducibility.py --lens-root ../PtXLens

Use the exact interpreter patch announced by the installer. Substitute a CPython 3.11.9 executable explicitly if Windows's py launcher selects another patch. On Linux use CPython 3.11.18 and .rc2c-venv/bin/python. Set OPENBLAS_NUM_THREADS=1, OMP_NUM_THREADS=1, MKL_NUM_THREADS=1 and NUMEXPR_NUM_THREADS=1 before Python starts to match the runner profile.

The install downloads only binary wheels, enforces committed wheel SHA256, independently hashes downloaded files, installs offline from verified wheels without dependency resolution, builds editable project installs without network/build isolation and checks the exact distribution set and pip dependency graph. This does not automatically establish an immutable Python interpreter or OS image. The user's own existing .venv and private research source files are never replaced. The software version remains 0.1.0, not a scientific 1.0 release. Optional private source acquisition clients and BAFU-specific dependencies outside this declared profile need separately scoped locks.

## Scientific numerical acceptance

- Analytic dense/sparse linear system and residuals; analytic LP relaxation and independent exhaustive enumeration of a unique integer optimum, known infeasible MILP.
- Real-gas 313K 20–200bar(a) published 802-position *difference of independently rounded banks* (1443.6 m3, 17,784.924849614785 kg usable, 19,996.131073709454 kg gross), not an exact stand-alone 20,000 kg bank. The separate L3-F threshold screen requires 803 reference positions for both constraints; 802 and 803 are not actual OEM selections. No tolerance expansion to mask this physical distinction.
- Original simplified four-hour methanol example: independent stoichiometry, electricity and emissions-cap cost lower bounds, independent model mass/energy constraint replay; no claim to real methanol process validation.
- Paired PtXLens illustrative annualization, discounted annuity, electricity/embodied GWP accounting and source-receipt RC2/RC1 public reconstruction. Private full-year optimization inputs are not accessed.
- Fingerprint captures exact observed Python, package versions, platform, BLAS/LAPACK, loaded thread pools, CoolProp revision, SciPy-bundled HiGHS when its installed interface exposes a version (otherwise explicitly unknown), wheel-lock hash, and checked-out repository revisions, with no user paths or tokens.

## Native openLCA inventory (separate from Python)

PtXLens native POM declares Java compiler release 25 and actual openLCA-core 2.7.0. The no-database native CI job observed Temurin Java 25.0.5, Maven 3.10.0, and 32 classpath runtime JARs; exact JAR filename/byte-size/SHA256 and declared POM are recorded in PtXLens environment/rc2c-native-linux-inventory.json. Run Maven's pinned dependency plugin to obtain a runtime classpath, then the RC2-C native inventory script to compare against that baseline. An optional privately stored original BAFU:2026 v1.1 .zolca may be hashed locally against the frozen registered source, never uploaded. This inventory is not a complete Maven build-plugin/transitive/JDK/UMFPACK lock, native database import, native LCIA, or manufacturer site evidence. The existing more limited native 2023 result remains separate from the missing full incremental matched-service storage LCA.

## Release policy

Do not label a profile qualified until both its clean locked install and complete relevant numerical regression workflow pass. This is separate from the existing public receipt and source escrow gates. All 12 full programme acceptance gates remain NOT_PASSED. No actual OEM/PED, installed economics, industrial performance or complete scientific v1.0 release is authorized. Main integration remains a separate milestone.
