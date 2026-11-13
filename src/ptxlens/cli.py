"""Fail-closed research CLI; no placeholder output on missing real sources."""
import argparse
import json
from pathlib import Path
from .core import assess, inventory


def _write(obj, output):
    content = json.dumps(obj,indent=2,sort_keys=True,allow_nan=False) + "\n"
    if output is None:
        print(content,end="")
    else:
        path = Path(output)
        if path.exists():
            raise FileExistsError(f"existing results may not be overwritten: {path}")
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(content,encoding="utf-8")


def main(argv=None):
    parser = argparse.ArgumentParser(description="PtXLens reproducible cost, provenance and LCA workflows")
    commands = parser.add_subparsers(dest="command",required=True)
    for name in ("assess","inventory","pynexus-audit"):
        sub = commands.add_parser(name)
        sub.add_argument("source",type=Path)
        sub.add_argument("--output",type=Path)
    comp=commands.add_parser("pynexus-compare")
    comp.add_argument("e_zip",type=Path)
    comp.add_argument("es_zip",type=Path)
    comp.add_argument("--output",type=Path)
    doe=commands.add_parser("doe-capital")
    doe.add_argument("source",type=Path,help="original pinned observed-price WP5 ZIP")
    doe.add_argument("--installed-cost-usd2022-kw",type=int,choices=(1500,2000,2500),required=True)
    doe.add_argument("--real-discount-rate",type=float,required=True,help="explicit analyst sensitivity, not DOE-specified")
    doe.add_argument("--output",type=Path)
    api=commands.add_parser("fetch-nl-prices")
    api.add_argument("--year",type=int,required=True)
    api.add_argument("--csv",type=Path,required=True)
    api.add_argument("--manifest",type=Path,required=True)
    olca=commands.add_parser("openlca-run")
    olca.add_argument("source",type=Path,help="original pinned 2023 observed-price archive")
    olca.add_argument("--config",type=Path,required=True,help="actual connected openLCA model IDs and LCI database")
    olca.add_argument("--output",type=Path,required=True)
    args=parser.parse_args(argv)
    if args.command in ("assess","inventory"):
        payload=json.loads(args.source.read_text(encoding="utf-8"))
        _write(assess(payload) if args.command=="assess" else inventory(payload),args.output)
    elif args.command=="pynexus-audit":
        from .observed import load_archive
        _write(load_archive(args.source),args.output)
    elif args.command=="pynexus-compare":
        from .observed import compare_archives
        _write(compare_archives(args.e_zip,args.es_zip),args.output)
    elif args.command=="doe-capital":
        from .observed import load_archive
        from .doe import assess_doe_capital_component
        _write(assess_doe_capital_component(
            load_archive(args.source),
            installed_cost_usd2022_kw=args.installed_cost_usd2022_kw,
            real_discount_rate=args.real_discount_rate),args.output)
    elif args.command=="fetch-nl-prices":
        from .energy_charts import fetch_prices,write_prices
        report=write_prices(fetch_prices(args.year),args.csv,args.manifest)
        print(json.dumps(report,indent=2,sort_keys=True))
    elif args.command=="openlca-run":
        from .olca_real import run_from_files
        report=run_from_files(args.source,args.config,args.output)
        print(json.dumps({"status":report["execution_status"],"result_file":str(args.output)},indent=2))


if __name__=="__main__":
    main()
