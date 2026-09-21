#!/usr/bin/env python3
"""Load the pinned MLX model and list possible LoRA module paths."""
from pathlib import Path

from mlx_lm import load

ROOT = Path(__file__).parent
MODEL = ROOT / "models" / "NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit"


def main() -> None:
    # MLX-LM 0.29.1 loads custom modeling files from this local model directory
    # without a trust_remote_code keyword.
    model, tokenizer = load(str(MODEL))
    names = [name for name, _ in model.named_modules()]
    candidates = [
        name for name in names
        if any(token in name.lower() for token in ("q_proj", "v_proj", "out_proj", "in_proj"))
    ]
    print(f"model: {MODEL}")
    print(f"chat_template: {'present' if tokenizer.chat_template else 'missing'}")
    print("candidate LoRA modules:")
    for name in candidates:
        print(name)


if __name__ == "__main__":
    main()
