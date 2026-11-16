"""F3-D robust source-2023 observed-market counterfactual data figures.

True original 2023 E/ES F3C cost and all eight source-verified F3D 8760h
same-hour H2 MILP outcomes. The 2 cases under wind 0.90 HAVE NO
CERTIFIED RESULT; they must show as missing/unknown, NEVER bar zero.

The 20y/8% capital frontier is a HYPOTHETICAL annual repetition of the
transformed source-2023 wholesale saving with ZERO extra OPEX and equipment
cost: no vendor installed CAPEX, not an observed future forward curve.
"""
from __future__ import annotations
import argparse
import json
import hashlib
from pathlib import Path
import xml.etree.ElementTree as ET

from .f3d_independent_2023_stress_finance_bridge import synthesize_independent_comparison

SCHEMA="ptxlens.f3d_original_2023_price_wind_source_eight_stress_timing_candles_vector_figures.v1"
FIGURES={
  "wholesale":"F3D_2023_original_source_8760h_EplusS_wholesale_advantage_and_unknown.svg",
  "capital":"F3D_2023_conditional_20y8pct_repeat_wholesale_capex_ceiling_not_vendor.svg"
}
KEYS=("baseline","price_circular_168h","price_centered_spread_150","wind_090_multiplier","wind_110_multiplier")
LABELS=("Original\n2023","Price shift\n+168 h","Price spread\n×1.5","Wind energy\n×0.90","Wind energy\n×1.10")
MODES=("max_inventory","usable_service")
COLORS={"max_inventory":"#1e5b78","usable_service":"#b5682b"}


def generate(outdir):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as e:
        raise RuntimeError("Pinned Matplotlib 3.11.2 and NumPy 2.5.4 required for original-source figures") from e
    d=synthesize_independent_comparison()
    assert d["certified_matched_source_year_scenarios_count"]==6
    outdir=Path(outdir)
    outdir.mkdir(parents=True,exist_ok=True)
    plt.rcParams.update({
        "font.family":"DejaVu Sans","font.size":10.1,
        "axes.spines.right":False,"axes.spines.top":False,
        "axes.edgecolor":"#74808a","axes.labelcolor":"#203a46",
        "xtick.color":"#324855","ytick.color":"#324855",
        "svg.fonttype":"none","svg.hashsalt":"OEM-PTX-2026-F3D-2023-original-source",
        "figure.facecolor":"white","axes.facecolor":"white","savefig.facecolor":"white",
        "grid.color":"#e0e5e9","grid.linewidth":0.8
    })
    row={(r["source_capacity_semantics"],r["source_2023_counterfactual_stress_id"]):r for r in d["rows"]}
    results={}
    for kind,name in FIGURES.items():
        fig,ax=plt.subplots(figsize=(12.2,6.6))
        fig.suptitle(
          "Source-2023 PtX E+S operating advantage — full-year F3-D controls"
          if kind=="wholesale" else
          "Conditional capital ceiling — hypothetically replaying one-year source difference",
          fontweight="bold",fontsize=16,x=.065,y=.96,ha="left",color="#112e40"
        )
        ax.set_title(
          "Same 8,760-hour modelled H₂ service within each mode; original 2023 and four source-derived changes"
          if kind=="wholesale" else
          "20 years · 8% real · assume transformed 2023 annual saving repeats · zero EXTRA station OPEX/repairs (optimistic)",
          fontsize=10.5,loc="left",color="#52616d",pad=18
        )
        xx=np.arange(len(KEYS),dtype=float)
        barwidth=.34
        for offset,mode in ((-.18,"max_inventory"),(.18,"usable_service")):
            values=[]
            for id in KEYS:
                if id=="baseline":
                    first=next(r for r in d["rows"] if r["source_capacity_semantics"]==mode)
                    if kind=="wholesale": val=first["original_2023_F3C_reference_wholesale_EplusS_saving_eur"]/1e6
                    else:
                        from .l3a_source_wholesale_dcf import constant_scenario,pv_components
                        s=constant_scenario(first["original_2023_F3C_reference_wholesale_EplusS_saving_eur"],years=20,r=.08)
                        val=pv_components(s)["max_initial_all_in_incremental_capex_at_zero_NPV_eur"]/1e6
                else:
                    item=row[(mode,id)]
                    cost=item["source_2023_counterfactual_wholesale_EplusS_saving_eur"]
                    if cost is None:val=None
                    else:
                        val=(cost if kind=="wholesale" else
                             item["conditional_20y_8pct_no_extra_cost_C0_max_eur_2023_basis"])/1e6
                values.append(val)
            for i,value in enumerate(values):
                if value is None:continue
                rect=ax.bar(i+offset,value,width=barwidth,color=COLORS[mode],
                            label=("20t gross max inventory" if mode=="max_inventory" else "20t usable withdrawal") if i==0 else "_nolegend_",
                            zorder=3)
                ax.text(i+offset,value+.02 if kind=="wholesale" else value+.17,
                        f"{value:.2f}",ha="center",va="bottom",fontsize=9.1,
                        color=COLORS[mode],fontweight="medium")
        ax.set_xticks(xx,LABELS)
        ax.set_ylabel("Modelled source-2023 wholesale saving (million EUR)" if kind=="wholesale"
                      else "Maximum ALL-IN t=0 CAPEX (million real 2023 EUR), mathematical scenario only")
        ax.set_ylim(0,2.04 if kind=="wholesale" else 19.4)
        ax.grid(axis="y",alpha=.7,zorder=0)
        # Unknown is NOT plotted as 0 EUR, and it is NOT called provably infeasible.
        ypos=0.5 if kind=="wholesale" else 4.
        ax.text(3,ypos,"No certified\nE/ES solve\n— NOT zero",
                ha="center",va="center",color="#794034",fontsize=10.3,fontweight="bold",
                bbox={"boxstyle":"round,pad=.3","facecolor":"#f6f0ec","edgecolor":"#d2afa1"})
        ax.legend(loc="upper right",frameon=False)
        fig.subplots_adjust(left=.1,right=.955,top=.79,bottom=.24)
        fig.text(.065,.09,"Observed input year: 2023 only. Altered prices/wind are controlled counterfactuals, NOT additional observed years or forecasts.",
                fontsize=9.2,color="#526773")
        fig.text(.065,.065,"+10% wind is scaled modelled source available power, NOT a physical ERA5/turbine reanalysis; no real site, OEM quote or native full BAFU GWP.",
                fontsize=9.0,color="#526773")
        fig.text(.065,.04,"Source: PyNEXUS 2023 ERA5-derived resource and NL A44 price, matched physical F3-C H2; PtXFlex F3-D SHA and PtXLens verification.",
                fontsize=8.4,color="#82909a")
        path=outdir/name
        fig.savefig(path,format="svg",metadata={"Title":name,"Creator":"PtXLens F3D source-2023 counterfactuals","Date":"2026-11-14"})
        png=path.with_suffix(".png")
        fig.savefig(png,format="png",dpi=175)
        plt.close(fig)
        ET.parse(path)
        assert path.stat().st_size>7000 and png.stat().st_size>8000
        results[kind]={
            "svg_filename":name,
            "svg_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
            "png_filename":png.name,
            "png_sha256":hashlib.sha256(png.read_bytes()).hexdigest(),
            "source_2023_observed_alternative_new_year":False,
            "unknown_wind_minus10pct_not_assumed_zero":True
        }
    return {
      "schema_version":SCHEMA,"programme":"OEM-PTX-2026-01",
      "source_observed_year":2023,
      "price_and_wind_changes_actual_new_weather_year":False,
      "source_altered_2023_data_only":True,
      "six_certified_cases_and_two_no_accepted_incumbent":True,
      "source_F3D_2023_PtXLens_reconciled_SCIENCE_RESULT_SHA256":"26b5abce70e0dc5f2274528c75ac4ef80f9b42d796e61f9b3365d83e9d05095b",
      "full_vendor_20t_station_storage_CAPEX":None,
      "native_stationary_typeI_2026_BAFU_GWP":None,
      "actual_20y_project_NPV_or_LCOH":None,
      "figures":results
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output-dir",required=True)
    args=p.parse_args()
    dest=Path(args.output_dir)
    obj=generate(dest)
    fp=dest/"F3D_2023_counterfactual_sensitivity_figure_manifest.json"
    if fp.exists():raise FileExistsError("do not overwrite original figure checksum manifest")
    fp.write_text(json.dumps(obj,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    for key,r in obj["figures"].items():
        print("F3D_FIG_"+key+"_SHA256="+r["svg_sha256"])
        print("F3D_FIG_"+key+"_FILE="+r["svg_filename"])
    print("Only 2023 original source; -10% wind two missing bar results intentionally NOT ZERO.")
if __name__=="__main__":main()
