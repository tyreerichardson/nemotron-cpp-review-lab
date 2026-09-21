#!/usr/bin/env python3
"""Check whether an endpoint reproduces reviewed train or validation records."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).parent


def expected_pairs(review):
    return {(finding["category"], finding["location"]["start_line"]) for finding in review["findings"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--split", choices=("train", "validation"), required=True)
    parser.add_argument("--endpoint", default="http://127.0.0.1:8090/v1/chat/completions")
    parser.add_argument("--model", required=True)
    parser.add_argument("--timeout", type=float, default=180)
    parser.add_argument("--temperature", type=float, default=0, help="sampling temperature forwarded to cli.py")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error(f"refusing to overwrite existing report: {args.output}")
    source_path = ROOT / "data" / args.split / "records.jsonl"
    records = [json.loads(line) for line in source_path.read_text().splitlines() if line]
    cases = []
    with tempfile.TemporaryDirectory() as temp:
        tempdir = Path(temp)
        for record in records:
            filename = record["review"]["file"]
            source = tempdir / filename
            source.write_text(record["source"])
            command = [sys.executable, str(ROOT / "cli.py"), "--endpoint", args.endpoint, "--model", args.model, "--timeout", str(args.timeout), "--temperature", str(args.temperature), str(source)]
            result = subprocess.run(command, text=True, capture_output=True)
            expected = expected_pairs(record["review"])
            if result.returncode:
                cases.append({"id": record["id"], "status": "client_error", "expected": sorted(expected), "stderr": result.stderr.strip()})
                continue
            review = json.loads(result.stdout)
            predicted = expected_pairs(review)
            cases.append({"id": record["id"], "status": "ok", "expected": sorted(expected), "predicted": sorted(predicted), "true_positive": sorted(expected & predicted), "false_positive": sorted(predicted - expected), "false_negative": sorted(expected - predicted)})
    successful = [case for case in cases if case["status"] == "ok"]
    tp = sum(len(case["true_positive"]) for case in successful)
    fp = sum(len(case["false_positive"]) for case in successful)
    fn = sum(len(case["false_negative"]) for case in successful)
    report = {"split": args.split, "model": args.model, "temperature": args.temperature, "summary": {"cases": len(cases), "successful_cases": len(successful), "true_positive": tp, "false_positive": fp, "false_negative": fn, "precision": tp / (tp + fp) if tp + fp else None, "recall": tp / (tp + fn) if tp + fn else None}, "cases": cases}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report["summary"], indent=2))
    if len(successful) != len(cases):
        sys.exit(2)


if __name__ == "__main__":
    main()
