#!/usr/bin/env python3
"""Create owner-approved DPO triples for the V4+V7 calibration continuation."""
import argparse
import json
from pathlib import Path

from cli import prompt_for

ROOT = Path(__file__).parent
PAIRS = ROOT / "data" / "dpo_calibration_v2" / "pairs.jsonl"


def base_order(review: dict) -> str:
    return json.dumps({
        "schema_version": review["schema_version"],
        "file": review["file"],
        "findings": review["findings"],
        "assumptions": review["assumptions"],
        "summary": review["summary"],
    }, separators=(",", ":"))


def load_pairs() -> list[dict]:
    rows = [json.loads(line) for line in PAIRS.read_text().splitlines() if line]
    if len(rows) != 8:
        raise ValueError(f"expected 8 approved pairs, found {len(rows)}")
    ids = {row["id"] for row in rows}
    if len(ids) != len(rows):
        raise ValueError("duplicate DPO pair id")
    if sum(row["split"] == "train" for row in rows) != 5:
        raise ValueError("expected five train pairs")
    if sum(row["split"] == "validation" for row in rows) != 3:
        raise ValueError("expected three validation pairs")
    return rows


def triple(row: dict) -> dict:
    chosen, rejected = row["chosen"], row["rejected"]
    if chosen == rejected:
        raise ValueError(f"{row['id']}: chosen and rejected are identical")
    return {
        "id": row["id"],
        "prompt": [{"role": "user", "content": prompt_for(chosen["file"], row["source"])}],
        "chosen": base_order(chosen),
        "rejected": base_order(rejected),
    }


def write(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, separators=(",", ":")) + "\n" for row in rows))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "mlx_dpo_v4_v7_calibration_v2")
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        raise SystemExit(f"refusing to overwrite non-empty output directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    rows = load_pairs()
    write(output / "train.jsonl", [triple(row) for row in rows if row["split"] == "train"])
    write(output / "valid.jsonl", [triple(row) for row in rows if row["split"] == "validation"])
    (output / "manifest.json").write_text(json.dumps({
        "format": "optiq dpo triples",
        "base_adapter": "adapters/nemotron-cpp-review-v7-dpo-composed",
        "train_ids": [row["id"] for row in rows if row["split"] == "train"],
        "valid_ids": [row["id"] for row in rows if row["split"] == "validation"],
        "review_policy": "single_owner_review",
        "status": "owner-approved second DPO calibration pairs",
    }, indent=2) + "\n")
    print(f"Wrote DPO triples to {output}")


if __name__ == "__main__":
    main()
