#!/usr/bin/env python3
"""Validate promoted supervised records and their candidate provenance."""
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).parent


def load_cli():
    spec = importlib.util.spec_from_file_location("review_cli", ROOT / "cli.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    cli = load_cli()
    errors, all_ids = [], set()
    count = 0
    for split in ("train", "validation"):
        directory = ROOT / "data" / split
        manifest = json.loads((directory / "manifest.json").read_text())
        records = [json.loads(line) for line in (directory / "records.jsonl").read_text().splitlines() if line]
        by_id = {record["id"]: record for record in records}
        if len(by_id) != len(records):
            errors.append(f"{split}: duplicate record IDs")
        for entry in manifest["records"]:
            record = by_id.get(entry["id"])
            if not record:
                errors.append(f"{split}: missing {entry['id']}")
                continue
            candidate = ROOT / entry["candidate"]
            digest = hashlib.sha256(candidate.read_bytes()).hexdigest()
            if digest != entry["candidate_sha256"]:
                errors.append(f"{entry['id']}: candidate hash changed")
            try:
                cli.validate(record["review"], record["review"]["file"], len(record["source"].splitlines()))
            except (KeyError, TypeError, ValueError) as exc:
                errors.append(f"{entry['id']}: {exc}")
            if record.get("review_policy") != "single_owner_review":
                errors.append(f"{entry['id']}: missing owner-review policy")
            if record["id"] in all_ids:
                errors.append(f"duplicate ID across splits: {record['id']}")
            all_ids.add(record["id"])
            count += 1
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated {count} promoted records with candidate provenance.")


if __name__ == "__main__":
    main()
