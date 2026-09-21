#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
V4="$ROOT/adapters/nemotron-cpp-review-v4-base-order"
V7="$ROOT/adapters/nemotron-cpp-review-v7-dpo-calibration"
OUTPUT="$ROOT/adapters/nemotron-cpp-review-v7-dpo-composed"

if [[ ! -f "$V4/adapters.safetensors" || ! -f "$V7/adapters.safetensors" ]]; then
  echo "missing V4 or V7 adapter weights" >&2
  exit 1
fi
if [[ -e "$OUTPUT" ]]; then
  echo "refusing to overwrite existing composed adapter: $OUTPUT" >&2
  exit 1
fi

exec "$ROOT/.venv-mlx312/bin/optiq" lora merge \
  "$V4" "$V7" \
  --output "$OUTPUT"
