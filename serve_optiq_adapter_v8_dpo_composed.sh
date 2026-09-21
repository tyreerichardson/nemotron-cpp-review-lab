#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
ADAPTER="$ROOT/adapters/nemotron-cpp-review-v8-dpo-composed"

if [[ ! -f "$ADAPTER/adapters.safetensors" ]]; then
  echo "missing composed V4+V7+V8 adapter; run ./merge_optiq_v7_v8_dpo.sh first" >&2
  exit 1
fi

exec "$ROOT/.venv-mlx312/bin/optiq" serve \
  --model "$ROOT/models/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit" \
  --adapter "$ADAPTER" \
  --host 127.0.0.1 --port 8090 \
  --max-concurrent 1 --max-context 512 \
  --no-auth --max-tokens 256 --temp 0
