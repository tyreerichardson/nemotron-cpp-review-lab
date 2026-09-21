#!/usr/bin/env python3
"""Validate a draft evaluation suite without running model inference."""
import argparse
import json
from pathlib import Path

VALID_CATEGORIES = {"memory_safety", "bug", "performance"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--suite", type=Path, required=True)
    args = parser.parse_args()
    suite = args.suite.resolve()
    sources = sorted(suite.glob("*.cpp"))
    if len(sources) != 12:
        raise SystemExit(f"expected 12 C++ sources, found {len(sources)}")
    ids = set()
    errors = []
    counts = {category: 0 for category in VALID_CATEGORIES}
    clean = 0
    for source in sources:
        gold_path = source.with_suffix(".gold.json")
        try:
            gold = json.loads(gold_path.read_text())
            case_id = gold["case_id"]
            if case_id in ids:
                raise ValueError("duplicate case id")
            ids.add(case_id)
            lines = len(source.read_text().splitlines())
            findings = gold["expected_findings"]
            if not findings:
                clean += 1
            for finding in findings:
                if finding["category"] not in VALID_CATEGORIES:
                    raise ValueError("invalid category")
                if not isinstance(finding["line"], int) or not 1 <= finding["line"] <= lines:
                    raise ValueError("gold line outside source")
                counts[finding["category"]] += 1
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"{source.name}: {exc}")
    if errors:
        raise SystemExit("\n".join(errors))
    if counts != {"memory_safety": 4, "bug": 3, "performance": 3} or clean != 2:
        raise SystemExit(f"unexpected distribution: {counts}, clean={clean}")
    print(f"Validated {len(sources)} draft evaluation cases in {suite}.")


if __name__ == "__main__":
    main()
