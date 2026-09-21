# Calibration candidate review packet

These nine assistant-drafted records target the mounted V4 error profile: `bug` cases being emitted as `memory_safety`, and unsupported findings on clean code.

Review each record without modifying it. Confirm:

1. C++17 syntax and stated assumptions.
2. The finding exists, or the clean response is warranted.
3. `bug` is used only for non-memory incorrect behavior or undefined behavior.
4. The listed line directly performs or enables the finding.
5. The fix preserves the stated behavior.
6. The source and mechanism are separate from `data/eval/`, `data/eval_v2/`, promoted records, and earlier candidate drafts.

Record an owner approval or rejection in a new review log. Rejected drafts must be replaced, not silently edited after approval. Structural validation does not grant approval.
