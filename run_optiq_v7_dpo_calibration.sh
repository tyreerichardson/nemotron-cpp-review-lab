#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
MODEL="$ROOT/models/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit"
DATA="$ROOT/data/mlx_dpo_v4_calibration"
BASE_ADAPTER="$ROOT/adapters/nemotron-cpp-review-v4-base-order"
OUTPUT="$ROOT/adapters/nemotron-cpp-review-v7-dpo-calibration"

if [[ ! -f "$DATA/train.jsonl" || ! -f "$DATA/valid.jsonl" ]]; then
  echo "missing prepared DPO triples: $DATA" >&2
  exit 1
fi
if [[ -e "$OUTPUT" ]]; then
  echo "refusing to overwrite existing adapter output: $OUTPUT" >&2
  exit 1
fi

exec "$ROOT/.venv-mlx312/bin/optiq" lora train "$MODEL" \
  --data "$DATA" \
  --output "$OUTPUT" \
  --method dpo \
  --mount-adapter "$BASE_ADAPTER" \
  --preset small \
  --rank-scaling by_bits \
  --num-layers -1 \
  --num-epochs 3 \
  --batch-size 1 \
  --learning-rate 5e-5 \
  --max-seq-length 512 \
  --dpo-label-smoothing 0.2 \
  --steps-per-report 1 \
  --steps-per-eval 5 \
  --steps-per-save 5 \
  --early-stopping-patience 2
