# Calibration candidate review log

This log records the project owner's review of assistant-drafted calibration candidates. Approval covers technical correctness and label/schema/location accuracy; it does not promote a draft into training data.

| Candidate | Reviewer | Date | Outcome | Notes |
| --- | --- | --- | --- | --- |
| `train-cal-001` | Project owner | 2026-09-19 | Approved | Zero must not be accepted as a power of two; `bug` at line 2 is appropriate. |
| `train-cal-002` | Project owner | 2026-09-19 | Approved | Exact inventory equality is a correctness case; `bug` at line 2 is appropriate. |
| `train-cal-003` | Project owner | 2026-09-19 | Approved | Clean target is appropriate. |
| `train-cal-004` | Project owner | 2026-09-19 | Approved | Clean target is appropriate. |
| `train-cal-005` | Project owner | 2026-09-19 | Approved | Repeated regex construction is a supported performance issue at line 7. |
| `train-cal-006` | Project owner | 2026-09-19 | Approved | Clean target is appropriate. |
| `validation-cal-001` | Project owner | 2026-09-19 | Approved | Under the stated HTTP-status assumption, `bug` at line 2 is appropriate. |
| `validation-cal-002` | Project owner | 2026-09-19 | Approved | Short-name suffix subtraction is a `bug` at line 3. |
| `validation-cal-003` | Project owner | 2026-09-19 | Approved | Clean target is appropriate. |
