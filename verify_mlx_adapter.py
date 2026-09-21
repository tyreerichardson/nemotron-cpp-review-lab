#!/usr/bin/env python3
"""Verify that the selected adapter loads and changes next-token logits."""
import argparse
import gc
from pathlib import Path

import mlx.core as mx
from mlx_lm import load

from cli import prompt_for

ROOT = Path(__file__).parent
MODEL = ROOT / "models" / "NVIDIA-Nemotron-3-Nano-4B-OptiQ-4bit"
SOURCE = ROOT / "data" / "train" / "records.jsonl"


def last_logits(adapter_path=None):
    model, tokenizer = load(str(MODEL), adapter_path=adapter_path)
    record = __import__("json").loads(SOURCE.read_text().splitlines()[0])
    tokens = tokenizer.encode(prompt_for(record["review"]["file"], record["source"]))
    logits = model(mx.array(tokens)[None])[:, -1, :]
    mx.eval(logits)
    lora_modules = [
        name for name, module in model.named_modules()
        if "lora" in type(module).__name__.lower()
    ]
    return logits, lora_modules


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--adapter",
        type=Path,
        default=ROOT / "adapters" / "nemotron-cpp-review-v1" / "best",
        help="adapter directory containing adapter_config.json and adapters.safetensors",
    )
    args = parser.parse_args()
    adapter = args.adapter.resolve()
    if not (adapter / "adapter_config.json").is_file() or not (adapter / "adapters.safetensors").is_file():
        parser.error(f"not an adapter directory: {adapter}")
    base_logits, _ = last_logits()
    gc.collect()
    mx.clear_cache()
    adapter_logits, lora_modules = last_logits(str(adapter))
    difference = mx.max(mx.abs(adapter_logits - base_logits)).item()
    print(f"adapter: {adapter}")
    print(f"adapter_lora_modules: {len(lora_modules)}")
    print(f"max_abs_logit_difference: {difference:.8f}")
    if not lora_modules:
        raise SystemExit("adapter did not create any LoRA modules")
    if difference == 0:
        raise SystemExit("adapter produced no logit change")


if __name__ == "__main__":
    main()
