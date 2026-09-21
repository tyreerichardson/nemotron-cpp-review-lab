# Second DPO calibration review packet

Review every draft for C++17 correctness, target behavior, category, source location, and suggested fix. Then verify the leakage audit's claimed separation from locked and promoted examples.

| Draft | Intended review |
| --- | --- |
| `train-cal2-001` | `bug` at line 2: interval predicate must use `&&`. |
| `train-cal2-002` | `bug` at line 2: exact multiples should not create an extra page. |
| `train-cal2-003` | `bug` at line 4: enabling should clear the disabled bit. |
| `train-cal2-004` | clean, empty findings. |
| `train-cal2-005` | clean, empty findings. |
| `validation-cal2-001` | `bug` at line 2: minute component is subtracted rather than added. |
| `validation-cal2-002` | clean, empty findings. |
| `validation-cal2-003` | clean, empty findings. |

Approval authorizes a separate DPO-pair draft only. It does not authorize modification of locked evaluation data.
