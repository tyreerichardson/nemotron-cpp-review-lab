# Calibration candidate drafts

These drafts address the mounted V4 adapter's held-out error profile: it overuses `memory_safety` for non-memory correctness defects and finds issues in clean controls. They are deliberately separate from promoted records and from every locked evaluation case.

All records are assistant-drafted and require the project owner's technical and label/schema/location review before any promotion. Do not copy a locked evaluation source, label, or mechanism into this directory.

Validate structure with:

```sh
python3 review_candidates.py --candidates data/candidates_calibration
```

Then compile extracted sources as C++17 and complete a fresh leakage review before approval.
