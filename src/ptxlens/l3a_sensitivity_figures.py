"""Reproducible 2023-real EUR L3-A scientific scenario charts.

matplotlib Agg; 4 native vector-SVG figures + rendered PNG previews.
All plotted quantities come directly from SHA-verified PtXLens L3-A DCF.
These are CONDITIONAL break-even *thresholds*, NOT prices, calibrated
expected 2026+ savings, confidence intervals or full plant economics.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from .l3a_source_wholesale_dcf import make_all, constant_scenario,     pv_components, break_even_uniform_annual_opex, MODES

FIGURES=(
  "L3A_2023_conditional_CAPEX_ceiling_vs_discount_and_life",
  "L3A_2023_conditional_annual_OPEX_vs_installed_CAPEX_frontier",
  "L3A_2023_max_inventory_wholesale_persistence_and_OPEX_scenarios",
  "L3A_2023_usable_service_wholesale_persistence_and_OPEX_scenarios",
)


def generate(outdir):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError as e:
        raise RuntimeError("Install pinned optional plotting dependencies for L3-A: matplotlib and numpy") from e
    d=make_all()
    outdir=Path(outdir)
    outdir.mkdir(parents=True,exist_ok=True)
    colors={"max_inventory":"#155e75","usable_service":"#b45309"}
    names={"max_inventory":"Gross model inventory","usable_service":"Usable H2 storage"}
    plt.rcParams.update({
       "font.family":"DejaVu Sans","font.size":10.4,
       "axes.spines.top":False,"axes.spines.right":False,
       "axes.edgecolor":"#77818b","axes.labelcolor":"#26313a",
       "xtick.color":"#42505c","ytick.color":"#42505c",
       "grid.color":"#dae1e6","grid.alpha":.7,"grid.linewidth":.7,
       "svg.fonttype":"none","figure.facecolor":"white",
       "axes.facecolor":"white","savefig.facecolor":"white",
    })

    def plotbase(title,sub,*,h=5.2):
        fig,ax=plt.subplots(figsize=(10.6,h))
        fig.suptitle(title,fontsize=16,fontweight="bold",x=.09,y=.96,ha="left",color="#102d3e")
        ax.set_title(sub,loc="left",fontsize=10.2,pad=15,color="#495b65")
        ax.grid(True,zorder=0)
        ax.set_axisbelow(True)
        fig.subplots_adjust(top=.81,bottom=.21,left=.13,right=.96)
        return fig,ax

    def finish(fig,base,note):
        fig.text(.085,.055,note,fontsize=9.1,color="#52636e",ha="left",va="bottom")
        fig.text(.085,.032,"Source: 2023 original F3-C 8,760-hour equal-H2 operating model; SHA-locked PtXLens L3-A. Financial scenarios are illustrative.",fontsize=8.1,color="#7e8b94",ha="left")
        svg=outdir/(base+".svg")
        png=outdir/(base+".png")
        fig.savefig(svg,format="svg",metadata={"Title":base,"Creator":"PtXLens L3-A; source-verified 2023 F3-C, hypothetical DCF"})
        fig.savefig(png,format="png",dpi=175)
        plt.close(fig)
        ET.parse(svg)
        assert svg.stat().st_size>6000 and png.stat().st_size>10000
        return {
         "svg_path":str(svg),"png_path":str(png),
         "svg_sha256":hashlib.sha256(svg.read_bytes()).hexdigest(),
         "png_sha256":hashlib.sha256(png.read_bytes()).hexdigest(),
         "original_data_year":2023,"full_investment_prediction":False
        }

    figs={}
    fig,ax=plotbase("Maximum hypothetical all-in storage CAPEX","No extra operating/replacement costs, 2023 wholesale saving repeated identically each year")
    rates=np.linspace(0,.15,61)
    for mode in MODES:
        s=d["per_distinct_capacity_semantics"][mode]["source_2023_wholesale_annual_savings_eur"]
        for n,ls in ((10,":"),(20,"-"),(30,"--")):
            y=[pv_components(constant_scenario(s,years=n,r=float(r)))["max_initial_all_in_incremental_capex_at_zero_NPV_eur"]/1e6 for r in rates]
            ax.plot(rates*100,y,label=f"{names[mode]} · {n} y",linewidth=2.5 if n==20 else 1.7,
                    linestyle=ls,color=colors[mode],alpha=1. if n==20 else .73)
    ax.set_xlabel("Real discount rate (%)")
    ax.set_ylabel("Theoretical maximum installed CAPEX (million real 2023 EUR)")
    ax.set_xlim(0,15)
    ax.set_ylim(bottom=0)
    ax.legend(ncol=2,fontsize=9,loc="upper right",frameon=False)
    figs["discount_lifetime"]=finish(fig,FIGURES[0],"ZERO additional OPEX is an optimistic mathematical bound, not a real storage project or vendor CAPEX.")

    fig,ax=plotbase("Annual extra OPEX vs installed CAPEX — break-even","20-year term · 8% real discount · repeated 2023 wholesale difference · no replacements")
    capex=np.linspace(0,20e6,81)
    for mode in MODES:
        src=d["per_distinct_capacity_semantics"][mode]["source_2023_wholesale_annual_savings_eur"]
        benchmark=constant_scenario(src,years=20,r=.08)
        y=[break_even_uniform_annual_opex(benchmark,float(c))/1e6 for c in capex]
        ax.plot(capex/1e6,y,color=colors[mode],linewidth=2.8,label=names[mode])
        ceiling=pv_components(benchmark)["max_initial_all_in_incremental_capex_at_zero_NPV_eur"]
        ax.scatter([ceiling/1e6],[0],color=colors[mode],s=45,zorder=4)
    ax.axhline(0,color="#7c2828",linewidth=1.3,linestyle="--",label="No additional OPEX")
    ax.set_xlabel("Assumed incremental installed CAPEX (million real 2023 EUR)")
    ax.set_ylabel("Maximum extra OPEX at NPV=0 (million EUR/year)")
    ax.set_xlim(0,20)
    ax.legend(loc="upper right",frameon=False)
    figs["opex_capex"]=finish(fig,FIGURES[1],"Negative OPEX threshold: even zero extra OPEX cannot break even. These CAPEX inputs are not vendor prices.")

    for mode,base in zip(MODES,FIGURES[2:]):
        src=d["per_distinct_capacity_semantics"][mode]["source_2023_wholesale_annual_savings_eur"]
        fig,ax=plotbase(f"{names[mode]} — conditional price persistence frontier",
                        "20 years · 8% real discount · additional fixed OPEX scenarios · no replacement")
        factor=np.linspace(0,1.6,81)
        opexs=((0.,"#155e75","No extra OPEX (optimistic)"),
               (250000.,"#806c22","+250k EUR/year (hypothetical)"),
               (500000.,"#a74038","+500k EUR/year (hypothetical)"))
        for opex,color,label in opexs:
            y=[pv_components(constant_scenario(src,years=20,r=.08,
                repeat_factor=float(f),annual_opex_eur=opex))["max_initial_all_in_incremental_capex_at_zero_NPV_eur"]/1e6 for f in factor]
            ax.plot(factor,y,label=label,color=color,linewidth=2.5)
        ax.axhline(0,color="#77818b",linewidth=1,linestyle="--")
        ax.axvline(1,color="#77818b",linewidth=1,linestyle=":")
        ax.set_xlim(0,1.6)
        ax.set_xlabel("Hypothetical future annual wholesale benefit / original 2023 difference")
        ax.set_ylabel("Maximum incremental all-in CAPEX (million real 2023 EUR)")
        ax.legend(loc="upper left",frameon=False,fontsize=9.2)
        figs[mode]=finish(fig,base,"Different modes use DIFFERENT hourly H2 services. A multiplier is NOT a future electricity price forecast.")

    return {
       "schema_version":"ptxlens.l3a_source2023_foreground_economic_frontier_4_reproducible_figures.v1",
       "programme":"OEM-PTX-2026-01",
       "input_result_l3a_recomputed_from_frozen_source":True,
       "actual_h2_storage_capex_OPEX_and_LCOH_available":False,
       "charts":figs,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output-dir",required=True)
    a=p.parse_args()
    dest=Path(a.output_dir)
    manifest=generate(dest)
    p=dest/"L3A_figures_manifest.json"
    p.write_text(json.dumps(manifest,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print("L3-A: generated",len(manifest["charts"]),"reproducible source-locked scenario FIGURES as SVG+PNG.")
    print("These are hypothetical CAPEX/OPEX ceilings, not observed future 2023 vendor revenue/cost forecasts.")
if __name__=="__main__":main()
