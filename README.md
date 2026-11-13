# PtXLens

**Status: executable, evidence-gated arithmetic baseline — not yet an independently sourced TEA/LCA.**

PtXLens is a research companion to [PyNEXUS](https://github.com/abhijith-sivaprasadan/PyNEXUS). It provides a versioned hourly dispatch contract, an auditable annualized cost calculation, illustrative GWP100 component accounting, a *staging* inventory for later openLCA modelling, and a read-only source hash gate.

~~~bash
python -m pip install -e ".[dev]"
python -m pytest -q
ptxlens assess examples/illustrative.json
ptxlens inventory examples/illustrative.json
~~~

**All bundled numerical inputs are invented arithmetic test fixtures**, including the hypothetical four-hour cycle repeated 2,190 times to reach 8,760 hours. These results are NOT observed Dutch 2023 dispatch, sourced electrolyser LCOH, or a valid life-cycle impact assessment.

The staging inventory is **not** a native openLCA database or an executed LCIA. OpenPyTEA, openLCA/olca-ipc, Brightway25, and exact-version EXIOBASE integration are subsequent validation gates, not claimed achievements. No restricted databases are bundled.

The [research plan and boundaries](docs/RESEARCH_PLAN.md) explain asset inclusion, replacement discounting, wind opportunity costs, delivered-H2 normalization, export emissions and the separation between frozen PyNEXUS market settlement and complete TEA.

Related repository: [PtXFlex](https://github.com/Open-Energy-Methods/PtXFlex), a separate experimental renewable-hydrogen-to-methanol MILP research model. **No production integration has been demonstrated** between them yet.

This is independently developed, AI-assisted research software requiring scientific review before making research claims.
