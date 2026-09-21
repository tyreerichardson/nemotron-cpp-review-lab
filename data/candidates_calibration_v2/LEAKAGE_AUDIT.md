# Leakage audit — second calibration candidates

The locked suite must remain measurement-only. These drafts do not reuse its code, source text, or exact defect mechanisms.

| Candidate | Target | Distinction from locked and promoted data |
| --- | --- | --- |
| `train-cal2-001` | `bug` | Incorrect disjunctive interval test; distinct from arithmetic, suffix, status, and negative-remainder examples. |
| `train-cal2-002` | `bug` | Incorrect ceiling-division result for exact multiples; distinct from bounds, indexing, and overflow. |
| `train-cal2-003` | `bug` | Boolean sense is inverted while assembling a feature mask; distinct from existing comparison and status cases. |
| `train-cal2-004` | clean | A straightforward `std::accumulate` sum has no issue. |
| `train-cal2-005` | clean | A bounded `std::clamp` helper has no issue. |
| `validation-cal2-001` | `bug` | Minute conversion subtracts rather than adds a component; distinct from prior arithmetic and predicate examples. |
| `validation-cal2-002` | clean | A `std::find` membership helper has no issue. |
| `validation-cal2-003` | clean | A small string prefix builder reserves capacity and has no issue. |

No draft duplicates a locked label/source pair. This audit does not grant approval.
