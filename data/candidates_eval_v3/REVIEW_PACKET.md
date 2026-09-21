# Evaluation v3 review packet

Review every source and gold label before locking. Confirm the primary category and source line, the stated assumptions, and separation from all prior data in `LEAKAGE_AUDIT.md`.

| Case | Expected label |
| --- | --- |
| `dangling_c_str.cpp` | memory_safety, line 4 |
| `mismatched_delete.cpp` | memory_safety, line 4 |
| `free_stack_storage.cpp` | memory_safety, line 4 |
| `double_delete.cpp` | memory_safety, line 4 |
| `integer_mean.cpp` | bug, line 2 |
| `month_index.cpp` | bug, line 4 |
| `discount_rounding.cpp` | bug, line 2: adds one to the two-digit year result |
| `list_distance.cpp` | performance, line 7 |
| `flush_each_line.cpp` | performance, line 6 |
| `copy_map_per_query.cpp` | performance, line 7 |
| `clean_optional.cpp` | no finding |
| `clean_transform.cpp` | no finding |

Approval locks this candidate into a separate `eval_v3` suite. After locking, do not modify its source or gold labels in response to a model result.
