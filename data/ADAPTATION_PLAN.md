# Adapter experiment decision — 2026-09-17

> **Current status — 2026-09-20:** The preflight and adaptation gates below are complete. The current measured candidate is composed V4+V7+V8, with 0.667 strict precision and 0.800 strict recall on both `eval_v2` and fresh locked `eval_v3`. Both suites are frozen; historical steps remain below for reproducibility while the active work shifts to project hardening.

## Decision

Keep the Jetson Orin Nano for GGUF inference. Do not attempt this model's LoRA or full SFT on its 8 GB shared memory.

The supported NVIDIA Megatron-Bridge LoRA reference for Nemotron 3 Nano is verified on eight H100 GPUs, not Jetson hardware. It uses BF16 model weights and a 2,048-token sequence length. The Jetson only runs a Q4 GGUF with a 512-token context and partial GPU offload, so inference success does not establish BF16 training feasibility.

Use the Mac M4 Pro as the first adapter-training probe, with the MLX-compatible 4-bit model path. The MLX model card states that custom NemotronH files are included and describes sensitivity-aware LoRA fine-tuning through `mlx-optiq`. This is a compatibility decision only: no package installation, model download, or training has run.

## Gate before training

1. Preserve the locked `data/eval/` and `data/eval_v2/` suites.
2. Run `python3 prepare_mlx_dataset.py` to convert only the promoted train and validation records into MLX-LM's `messages` chat format.
3. On the Mac, run `inspect_mlx_model.py` in the isolated environment to confirm model loading, chat-template availability, and valid LoRA module names for the pinned revision.
4. Run a five-step LoRA smoke experiment with short sequences, batch size one, and saved configuration/logs.
5. If it succeeds, train a small adapter and compare it with the base model on the unchanged locked v2 suite.

The generated dataset lives in `data/mlx_review_sft/` and includes hashes of both input record files. It is trainer input, not a new source of labels.

## Evidence

- NVIDIA's [PEFT documentation](https://docs.nvidia.com/nemotron/nightly/train-models/reference/peft/index.html) describes LoRA adapter artifacts.
- NVIDIA's [Nemotron 3 Nano Megatron-Bridge page](https://docs.nvidia.com/nemo/megatron-bridge/nightly/models/nemotron/nemotron3-nano-4b.html) lists its verified LoRA configuration as eight H100 GPUs.
- The [MLX OptiQ model card](https://huggingface.co/mlx-community/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit) documents custom NemotronH loading and LoRA fine-tuning support.

## Dataset limitation

The nine promoted records were reviewed only by the project owner. Their manifests preserve this `single_owner_review` policy. Treat any measured adapter improvement as a learning result from a very small, single-reviewer dataset, not general evidence of production quality.

## Current preflight status

`mlx-lm[train]` is installed in `.venv-mlx312` with Python 3.12, MLX 0.32.2, and MLX-LM 0.31.3; the earlier Python 3.9 environment is incompatible with the model configuration. The MLX chat dataset was generated and validated as six train rows and three validation rows. The pinned 4-bit model is downloaded locally. The Codex shell cannot initialize a Metal device, so the model-load gate must run in a normal interactive Mac Terminal. See `MLX_PROBE.md`. No LoRA run has occurred.

## Smoke configuration

Use `./run_optiq_smoke.sh` from a normal Mac Terminal. It uses OptiQ's Nemotron-compatible LoRA trainer, trains only attention-layer `q_proj` and `v_proj` suffixes, does not adapt MoE experts, and runs five steps at rank 8, batch size one, and 512 tokens. It saves to `adapters/nemotron-cpp-review-smoke/` and refuses to overwrite an existing output. This is a compatibility and artifact-save test, not a quality experiment.

The smoke adapter had no held-out detections, matching the same-runtime base model. Before the first meaningful experiment, regenerate the `data/mlx_review_sft_v2/` view. It uses the production `cli.prompt_for` user prompt exactly, instead of the original training-only wording. Then run `./run_optiq_experiment_v1.sh`: three epochs over the six approved training examples, rank 8 attention-only LoRA, batch size one, learning rate `1e-4`, validation every three steps, and early stopping after two non-improvements. This is still a small learning experiment; the validation split has only three records.

The v1 run completed all 18 planned steps. Its best validation loss was `1.0592` at step 15; its final step-18 validation loss was `1.0960`. Evaluate `adapters/nemotron-cpp-review-v1/best/` through `./serve_optiq_adapter_v1.sh`, then run the unchanged v2 suite with model label `NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit-v1-best-lora` and a fresh report name. Do not use the final step-18 adapter for the comparison because the validation split selected the step-15 checkpoint.

The selected v1 adapter also scored zero detections on the held-out suite. Its raw summaries often recognize a defect but leave `findings` empty. Before changing the dataset or training recipe, run `evaluate_supervised.py` against the training and validation records while the v1 adapter server is running. This distinguishes a failure to learn the supervised format from a held-out generalization failure.

The direct adapter probe found 92 loaded LoRA modules and a maximum next-token logit change of `2.375`, confirming that v1 loads and affects the model even though it does not alter greedy structured output. The next isolated experiment is `./run_optiq_broad_smoke.sh`: five prompt-aligned SFT steps with OptiQ's default model-aware trainable projections, no explicit target suffix restriction, and MoE experts still disabled. It establishes the memory footprint and saves a distinct adapter before any longer broad-target run.

The broad smoke adapted 50 targets with 7.655M trainable parameters (0.193%) at 5.386 GB peak memory. Its five-step validation loss reached `1.2004`, compared with `1.8455` initially. Start `./serve_optiq_adapter_v2_broad_smoke.sh`, then run `evaluate_supervised.py --split train` with model label `NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit-v2-broad-smoke`. Use that reproduction check, not held-out results, to decide whether a longer broad-target experiment is warranted.

## Smoke adapter evaluation

Evaluate the base and smoke adapter separately through OptiQ's loopback-only OpenAI-compatible server. Run `./serve_optiq_base.sh` in one normal Mac Terminal, then run:

```sh
python3 evaluate.py \
  --endpoint http://127.0.0.1:8090/v1/chat/completions \
  --model NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit-base \
  --suite data/eval_v2 \
  --timeout 180 \
  --output runs/eval-v2-optiq-base-normalized-20260918.json
```

Stop the base server, start `./serve_optiq_adapter.sh`, then use the same command with model label `NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit-smoke-lora` and output `runs/eval-v2-optiq-smoke-lora-normalized-20260918.json`. The CLI removes only a known trailing MLX `<|im_end|>` terminator before parsing; raw responses remain saved unchanged. These two reports compare the same model family, runtime, prompt, and held-out suite. The adapter had only five steps, so this is a pipeline check rather than an adaptation-quality claim.
