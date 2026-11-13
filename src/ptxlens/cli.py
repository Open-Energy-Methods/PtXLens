import argparse
import json
from pathlib import Path
from .core import assess, inventory

def main(argv=None):
    p = argparse.ArgumentParser(description="Hypothetical PtX screening")
    p.add_argument("command", choices=["assess", "inventory"])
    p.add_argument("input", type=Path)
    p.add_argument("--output", type=Path)
    args = p.parse_args(argv)
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = assess(payload) if args.command == "assess" else inventory(payload)
    output = json.dumps(result, sort_keys=True, indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")

if __name__ == "__main__":
    main()
