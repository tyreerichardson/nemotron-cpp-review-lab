# Supervised training data

This directory contains six approved owner-reviewed examples. Do not copy `data/eval/` or `data/eval_v2/` here, and do not generate training examples from their source or gold labels.

Each future JSONL record must contain:

```json
{"id":"train-0001","source":"...","review":{"schema_version":"0.1","file":"example.cpp","summary":"...","assumptions":[],"findings":[]},"provenance":"human-authored","reviewer":"pending"}
```

Records are in `records.jsonl`; `manifest.json` links each frozen record to the SHA-256 of its reviewed candidate source. The project has one reviewer, so this dataset uses the explicit `single_owner_review` policy rather than claiming independent review. Treat that as a limitation when interpreting any adaptation result. Never train on an unresolved category-policy disagreement.
