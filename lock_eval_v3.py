#!/usr/bin/env python3
"""Lock approved evaluation-v3 candidate files into a fresh immutable suite."""
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).parent
SOURCE = ROOT / "data" / "candidates_eval_v3"
TARGET = ROOT / "data" / "eval_v3"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    if TARGET.exists():
        raise SystemExit(f"refusing to overwrite existing locked suite: {TARGET}")
    sources = sorted(SOURCE.glob("*.cpp"))
    if len(sources) != 12:
        raise SystemExit(f"expected 12 candidate sources, found {len(sources)}")
    TARGET.mkdir(parents=True)
    manifest = []
    for source in sources:
        gold = source.with_suffix(".gold.json")
        if not gold.exists():
            raise SystemExit(f"missing gold label: {gold.name}")
        for path in (source, gold):
            shutil.copy2(path, TARGET / path.name)
        manifest.append({
            "source": source.name,
            "gold": gold.name,
            "source_sha256": digest(source),
            "gold_sha256": digest(gold),
        })
    (TARGET / "README.md").write_text(
        "# Locked evaluation suite v3\n\n"
        "This suite was locked on 2026-09-20 after project-owner approval. "
        "It is a generalization benchmark for the V4+V7+V8 candidate and later work. "
        "Do not edit sources or gold labels after observing any model result; create a later version instead.\n"
    )
    (TARGET / "ADJUDICATION.md").write_text(
        "# Evaluation v3 adjudication\n\n"
        "The project owner approved all 12 candidate sources, labels, and the leakage audit on 2026-09-20. "
        "The frozen manifest records exact source and gold-label hashes.\n"
    )
    (TARGET / "manifest.json").write_text(json.dumps({
        "suite": "eval_v3",
        "status": "locked",
        "approved_by": "Project owner",
        "approved_date": "2026-09-20",
        "cases": manifest,
    }, indent=2) + "\n")
    print(f"Locked {len(sources)} evaluation cases in {TARGET}")


if __name__ == "__main__":
    main()
