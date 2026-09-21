# Reproducibility guide

## Scope

This project evaluates structured C++17 code-review responses. It never executes submitted C++ source. The repository includes scripts, schemas, and locked data definitions; it excludes model weights, trained adapters, raw requests/responses, and Python environments.

## Hardware split

- **Jetson Orin Nano:** CUDA llama.cpp inference for the NVIDIA Nemotron 3 Nano 4B GGUF `Q4_K_M` model. The stable constrained configuration uses eight GPU-offloaded layers, 512 context tokens, one parallel slot, and reasoning disabled.
- **Mac M4 Pro:** MLX/OptiQ 4-bit model adaptation and adapter serving. The measured environment used Python 3.12, MLX 0.32.2, MLX-LM 0.31.3, and MLX OptiQ 0.5.11.

## Python environments

The CLI and evaluators use only the Python standard library. For Mac adaptation, create a Python 3.12 environment and install:

```sh
python3.12 -m venv .venv-mlx312
.venv-mlx312/bin/pip install -r requirements-mlx.txt
```

Obtain the model under its own license and place it under `models/`; it is ignored by Git. Recreate adapter artifacts locally with the versioned training scripts. The current serving artifact is produced by composing V4, V7, and V8; adapter files are also ignored.

## Local validation

```sh
python3 validate_promoted_data.py
python3 validate_eval_candidates.py --suite data/eval_v3
python3 evaluate.py --help
python3 evaluate_supervised.py --help
```

The latter two commands validate local CLI setup without contacting a model server. C++ candidate syntax can be checked without execution:

```sh
for source in data/eval_v3/*.cpp; do
  c++ -std=c++17 -fsyntax-only "$source"
done
```

## Evaluation boundaries

`data/eval_v2/` is an exhausted development benchmark. `data/eval_v3/` is the fresh generalization benchmark. Both are locked and must not be used in training, DPO preference construction, or prompt tuning. Use a new versioned suite for future optimization.

See [RESULTS.md](RESULTS.md) for measured outcomes and [data/LABELING_GUIDE.md](data/LABELING_GUIDE.md) for category policy.
