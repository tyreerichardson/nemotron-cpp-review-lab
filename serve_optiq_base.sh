#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
exec "$ROOT/.venv-mlx312/bin/optiq" serve \
  --model "$ROOT/models/NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit" \
  --host 127.0.0.1 --port 8090 \
  --max-concurrent 1 --max-context 512 \
  --no-auth --max-tokens 256 --temp 0
