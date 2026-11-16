# F3-D: analytically certified low-wind model infeasibility and necessary-condition wind-factor boundary

Observed source year 2022, max_inventory. Wind availability is modelled ELECTRIC POWER, not wind speed. Original fixed hourly hydrogen service is unchanged.

At 0.90 times original source wind-power availability, the original 20t E case is independently rebuilt LP-infeasible and 40t E+S has an independently feasible full-year integer primal witness. From 2022-04-30T18:00:00Z to 2022-05-06T05:00:00Z (end excluded; 131 hours), the direct generous upper bound of source H2 production plus possible discharge requires 18,669.007 kg net storage, exceeding possible inventory swing 17,786.037 kg by 882.970 kg. This contradiction uses no optimization solver and is independent of integer commitment assumptions.

A bisection of this **necessary inequality only** brackets its nonviolation transition in wind-power multiplier **(0.9828602782, 0.9828602782]**, precision 2.33e-11. Every factor at or below the tested violating lower bound still violates the necessary condition. The no-violation upper bound is **not** an accepted feasible annual dispatch, and the exact E MILP feasibility threshold remains UNKNOWN within the interval from this analytical cut to the separately validated original factor 1.0. Original full-wind source E is feasible, not a site-service guarantee.

The E-versus-E+S cost saving at 0.9 remains **NULL**, not zero. No original provider hourly arrays, private dispatch or native BAFU inventories were redistributed; complete manufacturer/system engineering, site performance, financial viability, dual/Farkas certificates and programme scientific v1.0 remain UNVERIFIED.
