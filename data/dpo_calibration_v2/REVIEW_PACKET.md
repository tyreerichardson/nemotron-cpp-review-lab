# Second DPO calibration review packet

Review the chosen and rejected output for each row in `pairs.jsonl`. Confirm that the chosen response is correct and that the rejected response is plausible, schema-valid, and strictly worse for the identical source.

| Pair | Source behavior | Chosen | Rejected |
| --- | --- | --- | --- |
| `dpo2-001` | Interval predicate | `bug` at line 2 | Same finding mislabeled `memory_safety` |
| `dpo2-002` | Exact-multiple page count | `bug` at line 2 | Same finding mislabeled `memory_safety` |
| `dpo2-003` | Enable-bit operation | `bug` at line 4 | Same finding mislabeled `memory_safety` |
| `dpo2-004` | Clean accumulation | Empty findings | Fabricated `memory_safety` at line 4 |
| `dpo2-005` | Clean clamp | Empty findings | Fabricated `performance` at line 3 |
| `dpo2-006` | Elapsed-minute arithmetic | `bug` at line 2 | Same finding mislabeled `memory_safety` |
| `dpo2-007` | Clean membership lookup | Empty findings | Fabricated `memory_safety` at line 4 |
| `dpo2-008` | Clean label builder | Empty findings | Fabricated `performance` at line 5 |

The first five pairs are proposed DPO training rows and the final three are proposed validation rows. Approval authorizes conversion into a new DPO triple dataset; it does not authorize use of locked `data/eval_v2/` cases.
