# Candidate review packet — 2026-09-17

## Reviewer instructions

Review each record independently. A reviewer must not inspect base-model evaluation reports while deciding whether the target is correct.

For every candidate, confirm:

1. The C++ source is syntactically valid for C++17.
2. The stated issue exists under the documented assumptions, or the clean target is justified.
3. Category follows `data/LABELING_GUIDE.md`.
4. Location covers the responsible source line and is within the source.
5. Explanation and suggested fix are technically sound and preserve intended behavior.
6. Source is materially distinct from both held-out suites.

Record each reviewer’s name/date and approve or reject outcome in a future split manifest. Rejected records must be rewritten as new drafts; do not silently edit an approved record.

## AI technical pre-review

This is an automated/AI pre-review and does not count as a human approval.

| Candidate | Pre-review result |
| --- | --- |
| train-001 | Ready for independent review: fixed-buffer memcpy overflow at line 5. |
| train-002 | Ready: moved-from unique_ptr dereference at line 5. |
| train-003 | Ready: temporary-backed string_view at line 4. |
| train-004 | Ready with stated large-input assumption: signed multiplication overflow at line 2. |
| train-005 | Corrected before review: added empty check; repeated copy/sort is lines 6–7. |
| train-006 | Ready: repeated front insertion at line 5. |
| validation-001 | Corrected before review: function renamed is_odd so negative-odd behavior is a bug. |
| validation-002 | Ready: strcpy writes terminator past the three-byte buffer. |
| validation-003 | Ready: clean string-construction control. |
