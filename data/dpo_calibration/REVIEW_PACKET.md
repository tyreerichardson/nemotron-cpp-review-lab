# DPO calibration review packet

Review the eight proposed preference pairs below. For each, verify that the chosen response is correct and that the rejected response is plausible, schema-valid, and demonstrably worse for the same source. These are training preferences, not evaluation cases.

| Pair | Source | Chosen behavior | Rejected behavior |
| --- | --- | --- | --- |
| `dpo-001` | zero power-of-two predicate | `bug` at line 2 | same finding mislabeled `memory_safety` |
| `dpo-002` | exact inventory equality | `bug` at line 2 | same finding mislabeled `memory_safety` |
| `dpo-003` | clean first-token extraction | empty findings | fabricated `memory_safety` at line 3 |
| `dpo-004` | clean minimum scan | empty findings | fabricated `memory_safety` at line 4 |
| `dpo-005` | repeated regex construction | `performance` at line 7 | empty findings |
| `dpo-006` | wrong false-branch status | `bug` at line 2 | same finding mislabeled `memory_safety` |
| `dpo-007` | short-name suffix check | `bug` at line 3 | same finding mislabeled `memory_safety` |
| `dpo-008` | clean parenthesis construction | empty findings | fabricated `memory_safety` at line 3 |

Approval authorizes conversion into DPO triples. Rejected pairs must be rewritten as new drafts. Locked evaluation sources must never appear here.
