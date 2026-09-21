# Public file scope

This file defines the intended initial Git commit.

## Included

- Application code, schemas, samples, evaluators, and validation scripts.
- Versioned training, merge, and serving scripts that document adapter lineage.
- Reviewed source/review records, candidate review packets, and DPO preference-pair definitions.
- Locked `eval`, `eval_v2`, and `eval_v3` source/label suites, including the eval-v3 hash manifest.
- Reproducibility, results, environment-pin, and publishing documentation.

Candidate and DPO directories are intentionally included. They are compact textual provenance for reviewed calibration decisions; they contain no model weights, server responses, credentials, or personal network configuration.

## Excluded

- Python environments, model files, adapter files, Hugging Face caches, and generated MLX datasets.
- Raw request/response artifacts under `runs/`.
- `.env` files, macOS metadata, bytecode caches, and downloaded GGUF or SafeTensors files.

## Verified before initial commit

- The non-ignored candidate set is approximately 780 KiB.
- Searches found no private filesystem paths, LAN addresses, credential-like strings, model weights, adapter weights, or raw response artifacts.
- Loopback endpoints such as `127.0.0.1` remain because they are required local defaults; the README uses host placeholders for SSH forwarding.
