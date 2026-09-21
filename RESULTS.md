# Measured results

The primary metric matches a predicted finding to an adjudicated finding only when both category and start line match. Range-overlap recall is diagnostic: it credits a category match when the gold line lies inside the model's predicted range.

## eval_v2 development benchmark

`eval_v2` was used during calibration and is retained as a frozen development benchmark.

| Candidate | Precision | Recall | Range-overlap recall | True positives | False positives | False negatives |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Same-runtime OptiQ base | — | 0.000 | 0.000 | 0 | 0 | 10 |
| Mounted V4 | 0.417 | 0.500 | 0.600 | 5 | 7 | 5 |
| V4+V7 | 0.500 | 0.600 | 0.700 | 6 | 6 | 4 |
| V4+V7+V8 | 0.667 | 0.800 | 0.900 | 8 | 4 | 2 |

## eval_v3 generalization benchmark

`eval_v3` was authored, reviewed, locked with SHA-256 hashes, and first evaluated after V8 training.

| Candidate | Precision | Recall | Range-overlap recall | True positives | False positives | False negatives |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| V4+V7+V8 | 0.667 | 0.800 | 0.800 | 8 | 4 | 2 |

## Limits

- Each benchmark has 12 cases and ten labeled findings; these figures are engineering measurements, not production-quality estimates.
- Promoted adaptation data used single-owner review.
- The current candidate still returns false `bug` findings on clean controls.
- Models, adapter weights, raw response artifacts, and local environment directories are excluded from version control.
