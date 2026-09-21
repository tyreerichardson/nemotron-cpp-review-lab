# Validation data

Use this split only to choose prompt wording, response limits, LoRA hyperparameters, and stopping points. It must remain independent of both training and the locked evaluation suites.

It contains three owner-reviewed examples in `records.jsonl`. `manifest.json` records their immutable candidate provenance. Because there is only one reviewer, its `single_owner_review` policy is a stated dataset limitation. Never choose settings from `data/eval/` or `data/eval_v2/` results.
