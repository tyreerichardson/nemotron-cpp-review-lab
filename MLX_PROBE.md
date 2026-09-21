# MLX environment probe

This is a diagnostic for the Apple Silicon adaptation environment. Run it only after completing steps 1 and 5 in [SETUP.md](SETUP.md).

The measured environment used Python 3.12, MLX 0.32.2, MLX-LM 0.31.3, and MLX OptiQ 0.5.11. The older Python 3.9 environment was incompatible with the model configuration and is not part of the supported setup.

Run from a normal interactive Mac Terminal, not an execution environment without a Metal device:

```sh
cd /path/to/nemotron-cpp-review-lab
.venv-mlx312/bin/python - <<'PY'
import mlx.core as mx
print(mx.default_device())
print(mx.metal.get_active_memory())
PY
```

Then confirm the model's LoRA candidates before training:

```sh
.venv-mlx312/bin/python inspect_mlx_model.py
```

The measured V4, V7, and V8 runs completed this probe successfully. If it fails, stop before training and resolve the local MLX/Metal setup.
