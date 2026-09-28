# Nemotron C++ Review Lab

A local, structured C++17 review application and adaptation experiment. It sends source to a local chat-completions endpoint, validates the returned JSON locally, and measures model behavior against locked source-level benchmarks. Submitted C++ is never executed.

## Demo

![Animated example of a C++ source review and its validated finding](docs/demo.gif)

This animation recreates a saved, schema-validated review from September 21, 2026; it shows an excerpt of the real result rather than a live screen recording. [Recreate the animation and export a video](docs/DEMO.md).

**Use the visual reviewer:** with your model endpoint running, start `python3 visual_app.py` and open [http://127.0.0.1:8765](http://127.0.0.1:8765). The page lets you edit C++ code and see the live, schema-validated result in a layout based on the demo. See [SETUP.md](SETUP.md#use-the-visual-reviewer) for endpoint options.

## Current result

The V4+V7+V8 adapter composition measured the same strict result on the development and fresh generalization benchmarks:

| Benchmark | Cases | Precision | Recall | Range-overlap recall |
| --- | ---: | ---: | ---: | ---: |
| `eval_v2` development | 12 | 0.667 | 0.800 | 0.900 |
| `eval_v3` generalization | 12 | 0.667 | 0.800 | 0.800 |

Each suite has ten labeled findings and two clean controls. The current model still produces false `bug` findings on clean controls, so these are small engineering measurements rather than production-quality estimates. See [RESULTS.md](RESULTS.md) for the full comparison and limits.

## Read this in order

1. [SETUP.md](SETUP.md) — ordered local setup, review, evaluation, and adaptation reproduction.
2. [REPRODUCIBILITY.md](REPRODUCIBILITY.md) — environment pins, validation commands, and evaluation boundaries.
3. [RESULTS.md](RESULTS.md) — measured benchmark results.
4. [data/README.md](data/README.md) — data-split and provenance policy.

## Repository boundaries

Source, schemas, reviewed data, experiment scripts, and documentation are tracked. The repository excludes model weights, adapters, virtual environments, generated datasets, raw request/response logs, local configuration, and generated video. See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the setup and evaluation boundaries.

## Status

Phases 0–4 are complete. The repository includes the local visual reviewer, the measured V4+V7+V8 result, and the reproduction guide. Both `eval_v2` and `eval_v3` are frozen; new tuning needs a separately versioned benchmark.
