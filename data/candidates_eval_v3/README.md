# Candidate evaluation suite v3

This is a review-only candidate for the next locked generalization suite. It is separate from every existing train, validation, DPO, `eval`, and `eval_v2` source. Do not run it as an outcome benchmark, train on it, or edit its labels after approval.

The proposed suite has 12 cases: four memory-safety issues, three correctness bugs, three performance issues, and two clean controls. Run `python3 validate_eval_candidates.py --suite data/candidates_eval_v3` before review, then approve sources, labels, and the leakage audit together before copying the files into a new locked `data/eval_v3/` directory.
