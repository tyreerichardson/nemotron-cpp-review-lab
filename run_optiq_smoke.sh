#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
MODEL="$ROOT/models/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit"
DATA="$ROOT/data/mlx_review_sft"
OUTPUT="$ROOT/adapters/nemotron-cpp-review-smoke"

if [[ -e "$OUTPUT" ]]; then
  echo "refusing to overwrite existing adapter output: $OUTPUT" >&2
  exit 1
fi

exec "$ROOT/.venv-mlx312/bin/optiq" lora train "$MODEL" \
  --data "$DATA" \
  --output "$OUTPUT" \
  --method sft \
  --preset small \
  --rank-scaling by_bits \
  --target-modules q_proj,v_proj \
  --num-layers -1 \
  --iters 5 \
  --batch-size 1 \
  --learning-rate 2e-4 \
  --max-seq-length 512 \
  --mask-prompt \
  --val-batches -1 \
  --steps-per-report 1 \
  --steps-per-eval 5 \
  --steps-per-save 5
