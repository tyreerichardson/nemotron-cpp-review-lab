#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
MODEL="$ROOT/models/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit"
DATA="$ROOT/data/mlx_review_sft_v3_base_order"
OUTPUT="$ROOT/adapters/nemotron-cpp-review-v4-base-order"

if [[ ! -f "$DATA/dataset_manifest.json" ]]; then
  echo "missing prepared base-order dataset: $DATA" >&2
  exit 1
fi
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
  --num-layers -1 \
  --num-epochs 8 \
  --batch-size 1 \
  --learning-rate 1e-4 \
  --max-seq-length 512 \
  --mask-prompt \
  --val-batches -1 \
  --steps-per-report 1 \
  --steps-per-eval 6 \
  --steps-per-save 6 \
  --early-stopping-patience 4
