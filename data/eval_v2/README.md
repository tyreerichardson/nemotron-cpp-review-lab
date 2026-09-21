# Locked evaluation suite v2

Twelve new human-authored C++17 cases for a larger held-out baseline. This suite is separate from `data/eval/` and from all future training/validation data. It contains four memory-safety issues, three bugs, three performance issues, and two clean controls.

Gold labels use a category and a primary source line. The evaluator reports strict category/start-line precision and recall. It also reports a diagnostic category/range-overlap recall when a predicted line range includes the gold line; this diagnostic does not replace the strict score.

Do not edit source or gold labels after observing a run. Record taxonomy changes in an adjudication note and create a later suite version instead.
