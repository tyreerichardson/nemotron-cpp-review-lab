#!/usr/bin/env python3
"""Create reviewed DPO triples for V4 calibration; refuses to overwrite output."""
import argparse
import json
from pathlib import Path

from cli import prompt_for

ROOT = Path(__file__).parent
TRAIN_IDS = ("train-cal-001", "train-cal-002", "train-cal-003", "train-cal-004", "train-cal-005")
VALID_IDS = ("validation-cal-001", "validation-cal-002", "validation-cal-003")
FAKE_CLEAN_LINES = {"train-cal-003": 3, "train-cal-004": 4, "validation-cal-003": 3}


def base_order(review: dict) -> str:
    return json.dumps({
        "schema_version": review["schema_version"],
        "file": review["file"],
        "findings": review["findings"],
        "assumptions": review["assumptions"],
        "summary": review["summary"],
    }, separators=(",", ":"))


def rejected(record: dict) -> str:
    review = record["review"]
    if review["findings"] and review["findings"][0]["category"] == "performance":
        value = {**review, "summary": "No supported issues identified.", "assumptions": [], "findings": []}
        return base_order(value)
    if review["findings"]:
        finding = {**review["findings"][0], "category": "memory_safety"}
        value = {**review, "summary": "A memory-safety issue was identified.", "findings": [finding]}
        return base_order(value)
    line = FAKE_CLEAN_LINES[record["id"]]
    value = {**review, "summary": "A memory-safety issue was identified.", "findings": [{
        "category": "memory_safety", "severity": "medium",
        "location": {"start_line": line, "end_line": line},
        "title": "Unsupported memory-safety finding",
        "explanation": "This is deliberately the rejected alternative for a clean control.",
        "suggested_fix": "No change is required.",
    }]}
    return base_order(value)


def read_records() -> dict[str, dict]:
    records = {}
    for split in ("train", "validation"):
        for line in (ROOT / "data" / split / "records.jsonl").read_text().splitlines():
            if line:
                record = json.loads(line)
                records[record["id"]] = record
    return records


def triples(ids: tuple[str, ...], records: dict[str, dict]) -> list[dict]:
    output = []
    for record_id in ids:
        record = records[record_id]
        output.append({
            "id": record_id,
            "prompt": [{"role": "user", "content": prompt_for(record["review"]["file"], record["source"])}],
            "chosen": base_order(record["review"]),
            "rejected": rejected(record),
        })
    return output


def write(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, separators=(",", ":")) + "\n" for row in rows))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "mlx_dpo_v4_calibration")
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        raise SystemExit(f"refusing to overwrite non-empty output directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    records = read_records()
    write(output / "train.jsonl", triples(TRAIN_IDS, records))
    write(output / "valid.jsonl", triples(VALID_IDS, records))
    (output / "manifest.json").write_text(json.dumps({
        "format": "optiq dpo triples",
        "base_adapter": "adapters/nemotron-cpp-review-v4-base-order",
        "train_ids": TRAIN_IDS,
        "valid_ids": VALID_IDS,
        "review_policy": "single_owner_review",
        "status": "owner-approved DPO calibration pairs",
    }, indent=2) + "\n")
    print(f"Wrote DPO triples to {output}")


if __name__ == "__main__":
    main()
