#!/usr/bin/env python3
"""Validate draft candidate records; this does not approve or promote them."""
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).parent
CANDIDATES = ROOT / "data" / "candidates"

def load_cli():
    spec = importlib.util.spec_from_file_location("review_cli", ROOT / "cli.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--candidates",
        type=Path,
        default=CANDIDATES,
        help="candidate root containing train/ and validation/ JSON records",
    )
    args = parser.parse_args()
    cli = load_cli()
    records = sorted(args.candidates.resolve().glob("*/*.json"))
    if not records: raise SystemExit("no candidate records found")
    errors = []
    ids = set()
    for path in records:
        try:
            record = json.loads(path.read_text())
            if record.get("status") != "draft": raise ValueError("status must be draft")
            if record.get("split_candidate") not in {"train", "validation"}: raise ValueError("invalid split candidate")
            if record["id"] in ids: raise ValueError("duplicate id")
            ids.add(record["id"])
            source = record["source"]
            if not isinstance(source, str) or not source.strip(): raise ValueError("missing source")
            cli.validate(record["review"], record["review"]["file"], len(source.splitlines()))
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{path.name}: {exc}")
    if errors: raise SystemExit("\n".join(errors))
    print(f"Validated {len(records)} draft candidates in {args.candidates.resolve()}.")

if __name__ == "__main__": main()
