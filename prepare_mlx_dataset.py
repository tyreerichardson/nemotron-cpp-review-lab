#!/usr/bin/env python3
"""Create MLX-LM chat JSONL from the promoted review records."""
import argparse
import hashlib
import json
from pathlib import Path

from cli import PROMPT_VERSION, prompt_for

ROOT = Path(__file__).parent

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def user_prompt(record: dict) -> str:
    return prompt_for(record["review"]["file"], record["source"])


def rendered_review(review: dict, assistant_order: str) -> str:
    if assistant_order == "reviewed":
        value = review
    else:
        # Match the JSON member order emitted by the unadapted OptiQ server.
        # JSON object order is semantically irrelevant; this only tests whether
        # completion-prefix alignment improves learned structured output.
        value = {
            "schema_version": review["schema_version"],
            "file": review["file"],
            "findings": review["findings"],
            "assumptions": review["assumptions"],
            "summary": review["summary"],
        }
    return json.dumps(value, separators=(",", ":"))


def convert(path: Path, assistant_order: str) -> list[dict]:
    records = [json.loads(line) for line in path.read_text().splitlines() if line]
    return [
        {
            "messages": [
                {"role": "user", "content": user_prompt(record)},
                {
                    "role": "assistant",
                    "content": rendered_review(record["review"], assistant_order),
                },
            ]
        }
        for record in records
    ]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, separators=(",", ":")) + "\n" for row in rows))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "data" / "mlx_review_sft")
    parser.add_argument("--assistant-order", choices=("reviewed", "base"), default="reviewed")
    args = parser.parse_args()
    output = args.output.resolve()
    inputs = {
        "train": ROOT / "data" / "train" / "records.jsonl",
        "valid": ROOT / "data" / "validation" / "records.jsonl",
    }
    existing = [path for path in output.iterdir() if path.name != "README.md"] if output.exists() else []
    if existing:
        raise SystemExit(f"refusing to overwrite non-empty output directory: {output}")
    output.mkdir(parents=True, exist_ok=True)
    for split, source in inputs.items():
        write_jsonl(output / f"{split}.jsonl", convert(source, args.assistant_order))
    manifest = {
        "format": "mlx-lm chat dataset",
        "template_version": f"aligned-with-cli-{PROMPT_VERSION}",
        "assistant_json_member_order": args.assistant_order,
        "source_records": {str(path.relative_to(ROOT)): digest(path) for path in inputs.values()},
        "review_policy": "single_owner_review",
        "limitation": "Small owner-reviewed learning dataset; not production-quality evidence.",
    }
    (output / "dataset_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Wrote MLX chat dataset to {output}")


if __name__ == "__main__":
    main()
