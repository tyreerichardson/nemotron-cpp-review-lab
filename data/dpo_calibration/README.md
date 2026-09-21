# V4 DPO calibration drafts

This directory is for a small preference-calibration delta mounted on the measured V4 SFT adapter. It contains no locked evaluation source or label.

Each pair shares one production review prompt. `chosen` is the owner-approved response. `rejected` is a plausible but incorrect schema-valid response that reflects an observed failure mode: wrong `memory_safety` taxonomy, an unsupported finding on clean code, or empty findings for a supported performance issue.

Do not train until the owner approves every pair. The eventual DPO run must mount `adapters/nemotron-cpp-review-v4-base-order` as the frozen SFT reference and save a distinct delta adapter.
