# Recreate the README demo

The README animation is a visual recreation of the successful September 21, 2026 review of `samples/out_of_bounds.cpp`. It shows the real finding as a short excerpt. It is not a screen recording or a fresh model result.

To **use** a visual version of the reviewer, start the model endpoint, run `python3 visual_app.py` from the repository root, and open `http://127.0.0.1:8765`. You can edit C++ and request a fresh, validated review. The rest of this page explains how to regenerate the fixed README animation.

From the repository root on macOS, regenerate both files:

```sh
python3.12 -m venv .venv-demo
.venv-demo/bin/python -m pip install 'Pillow==12.3.0'
.venv-demo/bin/python docs/render_demo.py
open docs/demo.gif
```

The script uses the checked-in C++ sample and the recorded finding embedded in `render_demo.py`. It checks that the sample's faulty line still matches before rendering. The outputs are `docs/demo.gif` (the README preview) and `docs/demo.avi` (the 10-second Motion JPEG video). On macOS it uses Monaco and Arial; fallback fonts on other systems can change the appearance.

To inspect the actual tool behavior, start the local model endpoint as described in [SETUP.md](../SETUP.md), then run:

```sh
python3 cli.py --no-save samples/out_of_bounds.cpp
```

The model's wording may differ from the recorded example. If you want a real screen recording, capture that Terminal run with macOS Screenshot (`Shift-Command-5`) and trim the recording. Check the recording for local paths or other private details before sharing it.
