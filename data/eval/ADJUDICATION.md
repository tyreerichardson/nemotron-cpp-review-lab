# Baseline adjudication record

This record preserves the first locked baseline without changing its labels after results were observed.

## eval-004: divide by zero

The original gold label is `bug` at line 2. The model reported `memory_safety` at the same line. Integer division by zero is undefined behavior, but this project needs a stable category policy before a future evaluation-set version can relabel it. Keep the v1 label unchanged; decide the policy before creating v2.

## eval-003: unnecessary copy

The original gold label is `performance` at line 5. The model returned no finding. This is a real baseline miss under the v1 rubric, not a reason to alter the source or label.

## eval-002: dangling pointer

The initial client response was not valid JSON. The diagnostic rerun saved the raw envelope: a 154-token prompt and 358 generated tokens filled the server's 512-token context, leaving the JSON unclosed. This is a context/output-budget failure, not evidence that the model failed to identify the issue. Prompt version 0.2 reduced the truncation for this case but another response still exceeded its cap. Prompt version `0.3-bounded` adds schema-enforced one-finding/one-assumption limits and uses a 256-token cap. Preserve v1 and v2 reports; treat the next run as a separate baseline series.
