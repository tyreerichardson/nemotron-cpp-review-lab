# Calibration-draft leakage audit — 2026-09-19

The following drafts were written after evaluating mounted V4. They must not reuse evaluation sources or mechanisms.

| Draft | Mechanism | Independence note |
| --- | --- | --- |
| `train-cal-001` | Zero accepted by a bit-test power-of-two predicate | Distinct logic condition; no bounds, lifetime, or division mechanism. |
| `train-cal-002` | Exact inventory equality rejected | Distinct business-rule comparison. |
| `train-cal-003` | Clean first-token extraction | Clean string control; distinct from bracket/parenthesis construction. |
| `train-cal-004` | Clean minimum-with-fallback scan | Clean vector control; distinct from max/swap controls. |
| `train-cal-005` | Regex compiled inside a loop | Distinct repeated setup cost; not append, copy, sort, or repeated lookup. |
| `train-cal-006` | Clean monotonic sequence predicate | Clean indexed-vector control with bounds protected by loop start. |
| `validation-cal-001` | Incorrect status result for a false condition | Distinct return-value logic. |
| `validation-cal-002` | Short-name suffix subtraction underflow | Distinct string-position precondition. |
| `validation-cal-003` | Clean parenthesis construction | Clean string control distinct from existing controls. |

This is an author-side audit, not approval. The owner must independently confirm technical correctness, category, location, and independence before promotion.
