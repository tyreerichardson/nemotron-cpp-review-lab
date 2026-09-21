# Data layout and boundaries

| Directory | Purpose | Status |
| --- | --- | --- |
| `train/` | Owner-reviewed supervised source/review records. | 12 records; used in adaptation. |
| `validation/` | Independent records for training and calibration decisions. | 6 records; used in adaptation. |
| `eval/` | Initial five-case protocol check. | Locked historical baseline. |
| `eval_v2/` | Twelve-case development benchmark. | Locked and exhausted for tuning. |
| `eval_v3/` | Twelve-case generalization benchmark. | Locked and first-run measured. |
| `candidates*/` | Review and leakage-audit provenance for promoted records. | Historical, text-only evidence. |
| `dpo_calibration*/` | Approved preference-pair provenance. | Historical, text-only evidence. |

Never copy `eval`, `eval_v2`, or `eval_v3` sources or gold labels into training, validation, candidate, or DPO data. New optimization requires a new versioned evaluation suite.

The `mlx_review*` and `mlx_dpo*` directories are generated trainer-specific views. They are excluded from Git and can be recreated with the preparation scripts.
