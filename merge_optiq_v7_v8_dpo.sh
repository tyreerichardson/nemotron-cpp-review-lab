#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
V7_COMPOSED="$ROOT/adapters/nemotron-cpp-review-v7-dpo-composed"
V8="$ROOT/adapters/nemotron-cpp-review-v8-dpo-calibration-v2"
OUTPUT="$ROOT/adapters/nemotron-cpp-review-v8-dpo-composed"

if [[ ! -f "$V7_COMPOSED/adapters.safetensors" || ! -f "$V8/adapters.safetensors" ]]; then
  echo "missing V4+V7 composition or V8 delta weights" >&2
  exit 1
fi
if [[ -e "$OUTPUT" ]]; then
  echo "refusing to overwrite existing composed adapter: $OUTPUT" >&2
  exit 1
fi

exec "$ROOT/.venv-mlx312/bin/optiq" lora merge \
  "$V7_COMPOSED" "$V8" \
  --output "$OUTPUT"
