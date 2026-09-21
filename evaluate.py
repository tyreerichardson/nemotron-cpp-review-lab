#!/usr/bin/env python3
"""Run locked evaluation cases through cli.py and report category-and-line matches."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).parent
def pairs(suite):
    for source in sorted(suite.glob("*.cpp")):
        gold = source.with_suffix(".gold.json")
        if not gold.exists(): raise RuntimeError(f"missing gold label for {source.name}")
        yield source, json.loads(gold.read_text())

def evaluate_case(source, gold, endpoint, model, timeout):
    command = [sys.executable, str(ROOT / "cli.py"), "--endpoint", endpoint, "--model", model, "--timeout", str(timeout), str(source)]
    result = subprocess.run(command, text=True, capture_output=True)
    expected = {(x["category"], x["line"]) for x in gold["expected_findings"]}
    if result.returncode:
        return {"case_id": gold["case_id"], "source": source.name, "status": "client_error", "stderr": result.stderr.strip(), "expected": sorted(expected)}
    review = json.loads(result.stdout)
    predicted = {(x["category"], x["location"]["start_line"]) for x in review["findings"]}
    ranges = {(x["category"], x["location"]["start_line"], x["location"]["end_line"]) for x in review["findings"]}
    range_hits = {(category, line) for category, line in expected if any(kind == category and start <= line <= end for kind, start, end in ranges)}
    return {"case_id": gold["case_id"], "source": source.name, "status": "ok", "expected": sorted(expected), "predicted": sorted(predicted), "predicted_ranges": sorted(ranges), "true_positive": sorted(expected & predicted), "false_positive": sorted(predicted - expected), "false_negative": sorted(expected - predicted), "range_overlap_true_positive": sorted(range_hits), "range_overlap_false_negative": sorted(expected - range_hits)}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint", default="http://127.0.0.1:8080/v1/chat/completions")
    parser.add_argument("--model", default="nvidia/NVIDIA-Nemotron-3-Nano-4B-GGUF:Q4_K_M", help="model label sent to the endpoint and recorded in raw artifacts")
    parser.add_argument("--suite", type=Path, default=ROOT / "data" / "eval", help="locked suite directory")
    parser.add_argument("--timeout", type=float, default=90)
    parser.add_argument("--output", type=Path, required=True, help="JSON report path; use a new path for every run")
    args = parser.parse_args()
    if args.output.exists(): parser.error(f"refusing to overwrite existing report: {args.output}")
    if not args.suite.is_dir(): parser.error(f"suite is not a directory: {args.suite}")
    results = [evaluate_case(source, gold, args.endpoint, args.model, args.timeout) for source, gold in pairs(args.suite)]
    successful = [x for x in results if x["status"] == "ok"]
    tp = sum(len(x["true_positive"]) for x in successful)
    fp = sum(len(x["false_positive"]) for x in successful)
    fn = sum(len(x["false_negative"]) for x in successful)
    range_tp = sum(len(x["range_overlap_true_positive"]) for x in successful)
    range_fn = sum(len(x["range_overlap_false_negative"]) for x in successful)
    summary = {"cases": len(results), "successful_cases": len(successful), "true_positive": tp, "false_positive": fp, "false_negative": fn, "precision": tp / (tp + fp) if tp + fp else None, "recall": tp / (tp + fn) if tp + fn else None}
    summary["range_overlap_recall"] = range_tp / (range_tp + range_fn) if range_tp + range_fn else None
    report = {"protocol": "category_and_start_line_v1", "range_diagnostic": "category_and_gold_line_inside_predicted_range_v1", "suite": str(args.suite), "model": args.model, "prompt_version": "read from raw per-case artifacts", "summary": summary, "cases": results}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    if len(successful) != len(results): sys.exit(2)

if __name__ == "__main__": main()
