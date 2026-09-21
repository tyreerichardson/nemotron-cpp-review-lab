# Second DPO calibration candidate drafts

These eight assistant-drafted records target the composed V4+V7 adapter's measured weaknesses: unsupported findings on clean controls and `memory_safety` labels for ordinary correctness defects. They are review-only and must not be promoted or converted into DPO pairs until the project owner approves them.

The sources are distinct from every promoted record and from locked `eval_v2` sources. See `LEAKAGE_AUDIT.md` for the mechanism-level comparison. Validate them with:

```sh
python3 review_candidates.py --candidates data/candidates_calibration_v2
```
