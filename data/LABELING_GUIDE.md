# C++ review labeling guide v0.1

Use one principal category per issue:

| Category | Use for |
| --- | --- |
| `memory_safety` | Out-of-bounds access, null dereference, use-after-free, invalid dereference, dangling lifetime |
| `bug` | Incorrect behavior or undefined behavior outside the memory-safety category, including a division-by-zero precondition failure |
| `performance` | Unnecessary copying, avoidable repeated work, or algorithmic cost when the cost and trigger are explained |

Findings need a source line that performs or directly enables the issue. `start_line` and `end_line` are inclusive. Report no finding when the evidence is insufficient. For a clean example, use an empty `findings` array rather than a low-confidence warning.

Every suggested fix must preserve the stated intent where it is known. Do not include chain-of-thought or hidden reasoning in supervised targets.
