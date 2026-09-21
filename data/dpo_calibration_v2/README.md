# Second DPO calibration pair drafts

These eight pairs derive only from owner-approved records in `data/candidates_calibration_v2/`. They target the composed V4+V7 adapter's clean-control hallucinations and incorrect `memory_safety` taxonomy for ordinary correctness defects.

Each row in `pairs.jsonl` contains the source, approved `chosen` review, and a schema-valid `rejected` review. This directory is a review artifact. Do not train or generate DPO triples until the owner approves every pair in `REVIEW_PACKET.md`.
