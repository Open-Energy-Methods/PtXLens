# F3-D — first independently replayed exogenous-service matched-architecture electricity comparison

**Evidence date:** 16 November 2026. **Scope:** 2022 original NL ENTSO-E A44 price and ERA5 ARCO/PyNEXUS model available wind ELECTRIC power; stationary 20–200-bar(a) Type I 20t E and 40t E+S nominal H₂ banks; source-model **max_inventory** capacity interpretation. The outcome is a frozen-model engineering result, **not** an observed operating plant or investment decision.

## Claim and original research design

The independent product is an *analyst-prespecified*, hourly constant **30 t/day hydrogen demand**, equal to **1,250 kg/h** for every one of **8,760 hours**, or **10,950,000 kg/year**. It is **strictly lower** than the source-only E maximum constant-delivery selection (approximately 30.48065 t/day), which had made prior near-100%-wind E feasibility stress partly boundary-conditioned by construction. The same exact hourly H₂ schedule is imposed on both architectures; no service selection or re-optimization is performed after viewing the wind scenario.

The controlled intervention multiplies the original source-model **wind electrical power availability** by **0.90** at each hour; it is **not** a 10% reduction in wind speed, a separately observed weather year or a probabilistically characterized wind forecast. Original hourly 2022 nominal market prices are unchanged for both architectures; market settlement is a signed grid import/export wholesale-energy proxy and excludes network charges, balancing, fixed tariffs, actual contract permissions, financing, capex and many balance-of-plant operating expenses.

The original independent LP-screen result for 2022/max_inventory found **both E and E+S LP-feasible at all nine prespecified 25/27.5/30 t/day × 90/95/100% scenarios**, 18 physically matched relaxed LPs. Relaxed LP feasibility by itself cannot certify integer source-model unit commitment or feasible source model storage direction.

## Original source full-year mixed-integer result

Both original annual source-model MILPs at this fixed externally specified H₂ product, the same hourly 90%-wind-electric power and 2022 historical prices **completed locally** and were saved in PRIVATE H30_W090 E and E+S records. The source PtXFlex solver acceptance requires an original HiGHS/SciPy reported relative integer cost optimality gap no greater than **1e−6**, plus complete 8,760-hour source-model integer primal witness; this solver-reported cost bound is *not* externally reconstructed branch-and-bound evidence.

Subsequently, the separately implemented PtXLens independent original-model replay passed locally for **both cases**, checking source hash identity, hour-by-hour PEM electricity, hourly H₂ conservation, signed grid settlement, ramp/binary commitments and charge/discharge directions, original bank inventory/heel/leakage and terminal state, compressor electricity and real-gas 313 K CoolProp 20–200-bar(a) screen. **88 automated hermetic regression tests passed** at the checkpoint before the new public-release audit was added.

| 2022/max_inventory scenario (90% modeled source wind POWER) | E 20t nominal H₂ bank | E+S 40t nominal H₂ bank |
|---|---:|---:|
| Prespecified hydrogen product | 30 t/day | 30 t/day |
| Delivered model H₂ | 10,950,000 kg/year | 10,950,000 kg/year |
| Annual modelled signed wholesale grid settlement cost, nominal 2022 EUR | **€32,160,567.931485903** | **€28,878,954.877419014** |
| Electricity cost per unit delivered H₂, nominal 2022 EUR/kg | €2.9370382/kg | €2.6373475/kg |
| Original integer feasibility and full hourly physical/EOS replay | Passed | Passed |
| Source HiGHS reported 1e-6 relative integer cost gap gate | Passed | Passed |
| Independently recreated integer dual search-tree certificate | No | No |

**Paired E minus E+S modelled annual electricity cost advantage = €3,281,613.054066889 (nominal 2022 EUR/year), or €0.2996906898691223/kg identical delivered H₂, about 10.20384% of E source-model wholesale energy cost.**

The source's own solver-reported individual cost lower bounds, together with both independently reverified primal costs, can define a source-reported MIP savings interval; its precise numerical endpoints are in the local sanitized independent replay JSON. Do **not** invent them here or claim their source integer dual proofs were independently reproduced.

## Relation to earlier F3-D 2022 results

The previously audited 2022 original-price, **100% original wind** E-max selected service was about 30.481t/day and yielded a nominal modelled E−E+S wholesale saving of about €3.906m/year. That earlier comparison had a **different model-selected hourly H₂ target** AND a different wind-power input; it must **not** be used as a paired counterfactual for this 30t/day/90%-wind experiment or as evidence that the difference in savings was caused solely by wind. The original 30.481t/day/90%-wind E case was correctly infeasible for its internally maximized H₂ requirement, but the 30t/day/90%-wind E and E+S cases are both **integer-feasible and independently replayed**. This is not a contradiction; it illustrates the need for an independently specified service functional unit.

The new findings establish one repeatable **model-conditional** economic operating-cost comparison at a fixed independent service, not the storage marginal cost curve or an industrial investment decision. The manufacturer cost, real BoP, full pressure vessel manufacturing material, land, grid agreement, electrolyser capital, electricity purchase contracts and site-level reliability remain open.

## Independence and limitations

- **Independent source-year provider/time/data admission:** source 2022 NL A44 market, ERA5 ARCO/PyNEXUS wind and original E-selected H₂ model four-case public evidence immutable Git blob *ca07f5ef1e381fa157982bc5a68e46ce3022003a*, corresponding private 8,760-hour provider data and full-hourly model witnesses. Neither proprietary/restricted provider vector nor original private full-hour witness is for public redistributions.
- **Independent *equations* and physical replay:** PtXLens independently implements hourly H₂ mass/electricity/compression/inventory/binary constraints, 313K CoolProp H₂ EOS and wholesale cost arithmetic rather than trusting producer summary claims. It did **not** independently rerun the exact original integer branch-and-bound proof tree, or establish physical OEM pressure vessel certification.
- **Artificial price/wind experiment:** 90%-original modeled wind electricity represents one controlled perturbation, not observed 2022 alternate weather; no statistical distribution, forecast accuracy or meteorological site co-location evidence.
- **Economic conclusion:** annual 2022 wholesale-energy *cost difference only*; source 2022 EUR has not been inflation-adjusted. It cannot be multiplied by 20 years to assert real site NPV without independent forward electricity-price/wind scenarios, vendor-installed capital, OPEX, replacements, maintenance and revenue/discount assumptions.
- **Environmental conclusion:** no native BAFU:2026 v1.1 process-matched manufacturing, fixed equipment BOM, compressor/cooling BoP, emission-inventory or full net LCIA attributable to this particular 30t/day operating case has been demonstrated.

## Evidence and exact publication gate

The completed independent reviewer locally wrote:
\`data/results/F3D_EXOGENOUS_2022_max_inventory_H30_W090_BOTH_INTEGER_INDEPENDENT_REPLAY_v1.json\`.
The preceding exact H₂/wind/LP screen:
\`data/results/F3D_2022_max_inventory_EXOGENOUS_H2_SOURCE_LP_FEASIBILITY_SCREEN_v1.json\`.

**These outputs remain UNTRACKED locally in the user's working tree at the recorded checkpoint**; GitHub currently contains the source and this methodology, **not yet the new nine actual measured/replayed result files**. Do not misrepresent the result as an externally accessible public archived numerical dataset until the separate source-admission and manual publication occurs.

The source-locked [additional nine-file publication gate](../src/ptxlens/f3d_2022_public_evidence_admission.py) accepts only exactly named scalar outputs, checks the exogenous LP-screen byte SHA is retained by the independently reviewed integer result, recomputes annual E−E+S source-model economics/per-kg and source solver bound arithmetic, rejects scientific scope inflation and large hourly private arrays or source witness fields, and never stages or pushes files itself. Newly added gate and negative tests are **not yet run locally**.

Windows sequence after pulling PtXLens branch:

    .\scripts\F3D_Robustness_Local.ps1 -Phase Test
    .\scripts\F3D_Robustness_Local.ps1 -Phase AuditPublic2022 -Year 2022 -Mode max_inventory

Then manually inspect nine files, staged diff/check and published commit. Private original E/E+S H30 W090 annual full-hourly witnesses must remain exclusively under PtX_PRIVATE_RESEARCH.

## Next research iteration

Repeat the **same externally prescribed 30t/day** service and 90%-original **2024** modeled wind electric power, with actual source 2024 NL A44 prices and 8,784 UTC hours. First independently screen **all 18** 2024 exogenous LP cells, then choose identical H30 W090 original E/E+S MILPs only if both LPs are source-feasible. Independently replay both full-year integer states and never compare nominal 2022 and nominal 2024 EUR without appropriate contextual qualification. This additional source year is a robustness replication, not a statistically justified weather-risk distribution.

**Scientific release status: local source-model exogenous operating-value result independently replayed; complete vendor-installed TEA, native BAFU matched-service LCA and programme scientific v1.0 NOT CERTIFIED.**
