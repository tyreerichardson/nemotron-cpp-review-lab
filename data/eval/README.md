# Locked evaluation set

This initial set is a small, human-authored baseline smoke benchmark. It is not training data and must not be included in prompt development, LoRA examples, or synthetic-data generation.

Each `*.cpp` case has a matching `*.gold.json` file. Gold labels specify the issue category and the source line that must be identified for an exact match. The evaluator reports category-and-line matching only; it does not judge explanation quality or fix correctness. A result is not a claim of comprehensive code-review accuracy.

Do not alter existing case source or labels after seeing baseline results. Add a new versioned evaluation set when the rubric changes.
