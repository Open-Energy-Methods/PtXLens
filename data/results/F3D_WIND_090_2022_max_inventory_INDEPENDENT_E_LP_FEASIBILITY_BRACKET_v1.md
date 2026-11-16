# F3-D independent relaxed-LP E model wind-electric-power feasibility bracket

Historical source: 2022, max_inventory; original annual fixed-price-blind hourly H2 service.

Independent reconstructed LP E infeasible at **99.99330%** of original modeled wind ELECTRIC POWER, LP feasible at **100.00000%**. The LP bracket has width 0.00670 percentage points. This is a relaxed-LP feasibility bracket, NOT the original integer MILP feasibility transition.

A source-model E MILP feasible dispatch has been independently replayed at the original **100%** source wind. At 90%, E is independently LP-infeasible and its largest-contiguous H2-energy deficit violates the bank swing by 882.97 kg; E+S has an independently checked feasible MILP dispatch. For each wind-factor intermediate LP status, this report contains only status, factors and (when available) scalar primal constraint residuals. **No integer feasible witness has been shown at the upper LP threshold.** A separate E MILP feasibility search and external optimality proof are required to locate it.

All calculations are conditional on one historical 2022 model and its selected H2 service, not a weather-reliability confidence interval, a 2026 price forecast, a real installation safety case, full annual H2 contract, matched-service cash saving at k=0.9 (NULL), verified OEM costs, native BAFU LCIA, or scientific v1.0.
