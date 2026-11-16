# F3-D exogenous H2 matched-service model resilience LP screening

Original observed source year: 2022; physical storage interpretation: max_inventory.

Predeclared service levels **25, 27.5 and 30 tonnes/day** from the original nominal 50t/day H2 contract, each STRICTLY below the original source selected E-only maximal uniform service. Their hourly H2 targets are identical for E and E+S and each observed-wind-electricity multiplier 0.90, 0.95 and 1.00.

| Exogenous H2 t/day | Original wind POWER factor | E 20t relaxed LP | E+S 40t relaxed LP | Source matched service economics |
|---:|---:|---|---|---|
| 25.0 | 0.90 | SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED | SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED | NULL |
| 25.0 | 0.95 | SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED | SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED | NULL |
| 25.0 | 1.00 | SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED | SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED | NULL |
| 27.5 | 0.90 | SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED | SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED | NULL |
| 27.5 | 0.95 | SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED | SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED | NULL |
| 27.5 | 1.00 | SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED | SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED | NULL |
| 30.0 | 0.90 | SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED | SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED | NULL |
| 30.0 | 0.95 | SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED | SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED | NULL |
| 30.0 | 1.00 | SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED | SOURCE_LP_PRIMAL_FEASIBLE_INTEGER_UNDETERMINED | NULL |

Independent PtXLens reconstructs the original full hourly E/E+S constraints and tests *linear-programming relaxations only*; a feasible LP solution does NOT prove the original mixed-integer equipment-dispatch model can operate. A source LP status-2 infeasibility rules out the original integer model. A separate necessary storage-and-energy inequality can independently prove certain infeasible cases, but nonviolation proves nothing.

This is a preregistered throughput comparison designed to remove the E-only maximal-throughput selection artifact of the earlier 90%-wind resilience demonstration. Successful LP screening must be followed by both E and E+S ORIGINAL-MODEL integer feasibility replays and, if economic costs are compared, original annual MILP cost minimization under the identical exogenous product.

No site-measured wind, hydrogen contracts, modelled availability probabilities, native BAFU:2026 manufacturing LCIA, manufacturer CAPEX/OPEX, forward price forecasts, whole-plant viability or programme scientific v1.0 is established.
