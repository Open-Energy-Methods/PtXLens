"""Live, source-only BAFU:2026 IPCC-2021 GWP100 process candidate register.

The Swiss FOEN OGD GraphQL service exposes BAFU per-process ALREADY
CALCULATED impact scores. These are **not** elementary flow inventories or
evidence of a linked hydrogen product system. Candidate hits must be reviewed
for geography, technology, reference product and unit; never fill a missing
provider's impact from an unrelated name.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time

from .bafu_ogd import ENDPOINT, EXPECTED_VERSION, QUERY_NAMED, request, save_json

FILTER_TYPE="EconomyConsumption_Lca_LciaResults_Filter"
METHOD="IPCC 2021"
CATEGORY="GWP 100"
TERMS=[
    ("metals.titanium","%titanium%"),
    ("metals.aluminium","%aluminium%"),
    ("metals.stainless_steel","%stainless%steel%"),
    ("metals.copper","%copper%"),
    ("membrane.nafion","%nafion%"),
    ("membrane.tetrafluoroethylene","%tetrafluoroethylene%"),
    ("membrane.ptfe","%polytetrafluoroethylene%"),
    ("carbon.activated","%activated%carbon%"),
    ("metals.iridium","%iridium%"),
    ("metals.platinum","%platinum%"),
    ("water.deionised","%deionis%"),
    ("water.deionized","%deioniz%"),
    ("water.purification","%water%purif%"),
    ("electricity.offshore_wind","%electricity%wind%offshore%"),
    ("electricity.grid","%electricity%medium%voltage%"),
    ("gas.hydrogen_compression","%hydrogen%compress%"),
    ("storage.hydrogen","%hydrogen%stor%"),
    ("equipment.electrolyzer","%electrolys%"),
    ("equipment.electrolyser","%electrolyz%"),
    ("plant.electronics","%electronics%"),
    ("plant.silica","%silica%gel%"),
]
FIELD_NAMES=[
    "version","uuid","processName","location","referenceUnit","impactMethod",
    "impactCategory","impactCategoryUnit","value","isSingleScore","category",
    "lastDatasetUpdateYear","sourceStudy","sourceStudyAuthor"
]
GRAPHQL="""query BafuCandidates($where: EconomyConsumption_Lca_LciaResults_Filter, $limit:Int) {
  economy_consumption {
    lca {
      lcia_results(where:$where,limit:$limit) {
        version uuid processName location referenceUnit impactMethod
        impactCategory impactCategoryUnit value isSingleScore category
        lastDatasetUpdateYear sourceStudy sourceStudyAuthor
      }
    }
  }
}"""


def probe_filter():
    r=request(QUERY_NAMED,{"name":FILTER_TYPE})
    t=r["data"].get("__type")
    if not isinstance(t,dict) or t.get("kind")!="INPUT_OBJECT":
        # Most GraphQL gateways have introspection introspecting inputFields; if not, fail.
        raise ValueError("actual BAFU impact results where-filter type not present")
    return t


def discover_candidates(*, terms=TERMS, delay=.30, max_hits=300):
    # This request is only an API availability test; provider matching itself
    # is done from actual source rows and never automatically approved.
    results=[]
    for category,pattern in terms:
        where={"version":{"_eq":EXPECTED_VERSION},
               "impactMethod":{"_eq":METHOD},
               "impactCategory":{"_eq":CATEGORY},
               "processName":{"_ilike":pattern}}
        resp=request(GRAPHQL,variables={"where":where,"limit":max_hits})
        try:
            rows=resp["data"]["economy_consumption"]["lca"]["lcia_results"]
        except (KeyError,TypeError) as exc:
            raise ValueError(f"source BAFU LCIA response did not contain results for {category}") from exc
        if not isinstance(rows,list):
            raise ValueError("expected genuine source row list")
        if len(rows)>=max_hits:
            raise ValueError(f"{category} hit cap {max_hits}; needs narrowed source query")
        cleaned=[]
        for rec in rows:
            if not isinstance(rec,dict):raise ValueError("non-object BAFU source process")
            if rec.get("version")!=EXPECTED_VERSION or rec.get("impactMethod")!=METHOD or rec.get("impactCategory")!=CATEGORY:
                raise ValueError("mixed version/method/category; reject impact results")
            if rec.get("isSingleScore") is True:
                raise ValueError("GWP 100 returned as unexpected single score")
            if not (isinstance(rec.get("value"),(float,int)) and
                    isinstance(rec.get("uuid"),str) and
                    len(rec["uuid"])>=20 and
                    isinstance(rec.get("processName"),str) and rec["processName"]):
                raise ValueError("invalid BAFU source impact/process metadata")
            cleaned.append({
               **rec,
               "target_material_or_process_category":category,
               "manually_verified_provider_link":False,
               "foreground_linked_in_openlca":False,
               "process_name_is_not_product_flow":True,
               "geography_and_conversion_review_required":True
            })
        results.append({"term_key":category,"source_query_pattern":pattern,
                        "rows":cleaned,"candidate_count":len(cleaned),
                        "raw_response_sha256":resp["raw_sha256"]})
        time.sleep(delay)
    return {
       "schema_version":"ptxlens.bafu2026_actual_precharacterized_process_candidates.v0.1",
       "queried_at_utc":datetime.now(timezone.utc).isoformat(),
       "source_endpoint":ENDPOINT,
       "source_documentation":"https://data.bafu.admin.ch/en/dataproduct-economy-consumption-lca",
       "source_citation":"Database of the Swiss Federal Administration, BAFU:2026, Federal Office for the Environment, 2026",
       "source_license":"Swiss FOEN OGD: Open use. Must provide source. Separate Nexus LCI database use terms apply to full zolca download.",
       "database_version":EXPECTED_VERSION,"method":METHOD,"category":CATEGORY,
       "is_actual_openlca_foreground_calculation":False,
       "is_2023_netherlands_validated_lca":False,
       "source_rows":results,
       "available_candidate_process_records":sum(x["candidate_count"] for x in results),
       "verified_foreground_provider_links":0,
       "warnings":[
           "Per-process LCIA values already include BAFU supplier chain according to publisher; do not combine with a linked process provider or count twice.",
           "BAFU process reference unit and location may not match the actual source-input flow for a PEM stack.",
           "BAFU source factor is not an hourly Dutch grid carbon emission factor and must not be treated as such.",
           "No zero emission impact is imputed for absent process query results.",
           "Material mass LCI and product gate, BoP, storage, compression, service-matched comparisons still need validation.",
       ]
    }


def main(argv=None):
    import argparse
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    p.add_argument("--max-hits",type=int,default=300)
    p.add_argument("--scope",choices=["pilot","all"],default="pilot")
    args=p.parse_args(argv)
    if not 1<=args.max_hits<=2000:raise ValueError("max hits range 1-2000")
    terms=TERMS if args.scope=="all" else TERMS[:4]+TERMS[9:12]
    out=discover_candidates(terms=terms,max_hits=args.max_hits)
    save_json(out,args.output)
    for result in out["source_rows"]:
        print(json.dumps({"term":result["term_key"],"count":result["candidate_count"],
                          "sample":[{"id":r["uuid"],"name":r["processName"],
                                     "location":r["location"],"unit":r["referenceUnit"],
                                     "GWP_kgco2e_per_reference_unit":r["value"]}
                                    for r in result["rows"][:4]]},ensure_ascii=False))


if __name__=="__main__":
    main()
