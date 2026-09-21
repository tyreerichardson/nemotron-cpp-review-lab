# Evaluation v3 leakage audit

These mechanisms were selected to differ from existing promoted, candidate, DPO, and locked evaluation records. This document is a review aid and does not establish independence by itself.

| Case | Category | Mechanism and separation |
| --- | --- | --- |
| `dangling_c_str` | memory_safety | Returns `c_str()` from a local string; distinct from temporary `string_view`, null dereference, and freed aliases. |
| `mismatched_delete` | memory_safety | Uses scalar `delete` on an array allocation; distinct from use-after-free and buffer overflow. |
| `free_stack_storage` | memory_safety | Calls `free` on automatic storage; distinct allocation/deallocation API misuse. |
| `double_delete` | memory_safety | Deletes the same allocation twice; distinct from later dereference of freed memory. |
| `integer_mean` | bug | Loses fractional results through integer division under a nonzero-count contract; distinct from divide-by-zero. |
| `month_index` | bug | Treats a one-based month as a zero-based array index; distinct from caller-supplied unchecked indexing. |
| `discount_rounding` | bug | Adds one to a two-digit year result; distinct from arithmetic overflow and boolean predicates. |
| `list_distance` | performance | Recomputes `std::distance` from list begin for each element; distinct from nested vector search and repeated sorting. |
| `flush_each_line` | performance | Flushes an output stream on each iteration; distinct from string front insertion and repeated regex construction. |
| `copy_map_per_query` | performance | Copies an unchanged map on every query; distinct from one-time vector copying. |
| `clean_optional` | clean | Checks an optional before dereference. |
| `clean_transform` | clean | Performs an in-place bounded vector transformation. |
