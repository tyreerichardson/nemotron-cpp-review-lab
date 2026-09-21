# Leakage audit — 2026-09-17

The initial drafts failed semantic independence. The table preserves that audit trail; all nine source records were rewritten on 2026-09-17 and require a fresh independent audit before promotion.

| Candidate | Original conflict with held-out suite | Resolution status |
| --- | --- | --- |
| `train-001` | Same inclusive vector-bound pattern as eval v1 | Rewritten: fixed-buffer memcpy overflow |
| `train-002` | Same null-dereference pattern as eval v2 | Rewritten: dereference after unique_ptr move |
| `train-003` | Same local-string `c_str()` lifetime pattern as eval v1 | Rewritten: string_view from temporary |
| `train-004` | Same divide-by-zero pattern as both suites | Rewritten: signed multiplication overflow |
| `train-005` | Same repeated string-append pattern as eval v2 | Rewritten: repeated copy and sort |
| `train-006` | Too close to the vector-copy performance case in eval v2 | Rewritten: repeated front insertion |
| `validation-001` | Same missing-return pattern as eval v2 | Rewritten: negative odd-value logic |
| `validation-002` | Same fixed-array bounds pattern as eval v2 | Rewritten: strcpy terminator overflow |
| `validation-003` | Too close to clean controls in existing suites | Rewritten: string construction clean control |

All nine candidates were rewritten on 2026-09-17 with materially different source mechanisms. They remain drafts pending an independent semantic re-audit and two human reviews. After the audit, rerun `review_candidates.py`, then perform the two human reviews.
