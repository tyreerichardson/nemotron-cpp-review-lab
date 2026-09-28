# Setup and first run

Follow these steps in order. The first path runs the review application; the later adaptation path reproduces the measured V4+V7+V8 workflow on Apple Silicon.

## 1. Clone and validate local files

```sh
git clone <your-repository-url> nemotron-cpp-review-lab
cd nemotron-cpp-review-lab
python3 validate_promoted_data.py
python3 validate_eval_candidates.py --suite data/eval_v3
```

The CLI and evaluation tools use only Python's standard library. These checks do not contact a model server or run submitted C++.

## 2. Start a local OpenAI-compatible inference endpoint

The measured Jetson setup used CUDA llama.cpp with NVIDIA Nemotron 3 Nano 4B GGUF `Q4_K_M`, eight GPU-offloaded layers, a 512-token context, one parallel slot, and reasoning disabled:

```sh
llama-server -m /path/to/model.gguf -ngl 8 -c 512 --parallel 1 \
  --reasoning off --host 127.0.0.1 --port 8080
```

If the server runs on another machine, forward its loopback port:

```sh
ssh -N -L 8080:127.0.0.1:8080 <jetson-user>@<jetson-host>
```

Keep the server or tunnel terminal open.

## 3. Run a structured review

In a second terminal from the repository root:

```sh
python3 cli.py samples/out_of_bounds.cpp
cat samples/clean.cpp | python3 cli.py -
```

The CLI validates JSON shape, filename, and source-line ranges. It saves raw server envelopes under `runs/`; those files are ignored by Git. Use `--no-save` to suppress that artifact.

### Use the visual reviewer

With the model server and tunnel still running, start the local web interface from the repository root:

```sh
python3 visual_app.py
```

Open `http://127.0.0.1:8765` in your browser. Edit the sample, click **Review code**, and inspect the validated finding and full JSON. The interface uses the same prompt and validation as `cli.py`; it does not run the C++ source or save raw responses. It binds only to `127.0.0.1`. Stop it with `Ctrl-C`.

If the model server uses another local port, configure it when starting the interface:

```sh
python3 visual_app.py --endpoint http://127.0.0.1:8090/v1/chat/completions
```

## 4. Run an evaluation

Use a fresh output path every time. Do not rerun `eval_v2` or `eval_v3` to guide tuning: both are frozen historical measurements.

```sh
python3 evaluate.py \
  --suite data/eval_v3 \
  --endpoint http://127.0.0.1:8080/v1/chat/completions \
  --output runs/eval-local-YYYYMMDD.json
```

## 5. Reproduce the measured adaptation lineage

This path requires Apple Silicon, Python 3.12, the MLX dependencies in `requirements-mlx.txt`, and the separately licensed OptiQ model under `models/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit/`.

```sh
python3.12 -m venv .venv-mlx312
.venv-mlx312/bin/pip install -r requirements-mlx.txt
.venv-mlx312/bin/python inspect_mlx_model.py
```

Then create the trainer inputs and adapters in lineage order:

```sh
python3 prepare_mlx_dataset.py --assistant-order base --output data/mlx_review_sft_v3_base_order
./run_optiq_base_order_v4.sh
python3 prepare_dpo_calibration.py
./run_optiq_v7_dpo_calibration.sh
./merge_optiq_v4_v7_dpo.sh
python3 prepare_dpo_calibration_v2.py
./run_optiq_v8_dpo_calibration.sh
./merge_optiq_v7_v8_dpo.sh
./serve_optiq_adapter_v8_dpo_composed.sh
```

Every trainer and merge script refuses to overwrite an existing artifact. Confirm that each DPO startup reports stacked reference layers before treating its metrics as meaningful.

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for exact measured versions and [RESULTS.md](RESULTS.md) for the evaluation record.
