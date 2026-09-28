#!/usr/bin/env python3
"""Recreate the README demo from its public sample and recorded finding."""

import argparse
from io import BytesIO
from pathlib import Path
import struct

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "samples/out_of_bounds.cpp"
TITLE = "Out-of-bounds array access in loop"
CATEGORY = "memory_safety"
SEVERITY = "high"
LINE = 4
FIX = "change i <= values.size() to i < values.size()"
SIZE = (1280, 720)
GIF_SIZE = (960, 540)
COLORS = {
    "background": "#0b1220",
    "panel": "#111c2d",
    "border": "#25344c",
    "white": "#ecf3fc",
    "muted": "#9eb0c8",
    "teal": "#55e1c4",
    "amber": "#ffd078",
    "red": "#ff8c92",
}


def load_fonts():
    mono = "/System/Library/Fonts/Monaco.ttf"
    sans = "/System/Library/Fonts/Supplemental/Arial.ttf"
    try:
        return (
            ImageFont.truetype(mono, 21),
            ImageFont.truetype(mono, 18),
            ImageFont.truetype(sans, 38),
            ImageFont.truetype(sans, 25),
        )
    except OSError:
        return (
            ImageFont.truetype("DejaVuSansMono.ttf", 21),
            ImageFont.truetype("DejaVuSansMono.ttf", 18),
            ImageFont.truetype("DejaVuSans.ttf", 38),
            ImageFont.truetype("DejaVuSans.ttf", 25),
        )


def render_stage(stage, source_lines, fonts):
    mono, tiny, title, heading = fonts
    c = COLORS
    image = Image.new("RGB", SIZE, c["background"])
    draw = ImageDraw.Draw(image)

    def label(position, value, font=mono, color=None):
        draw.text(position, value, font=font, fill=color or c["white"])

    def panel(coords):
        draw.rounded_rectangle(coords, radius=18, fill=c["panel"], outline=c["border"], width=2)

    label((58, 35), "NEMOTRON  /  C++ REVIEW LAB", heading, c["teal"])
    label((58, 78), "A local, structured C++17 review", title)
    label((58, 131), "Recorded example from a validated run · 2026-09-21", tiny, c["muted"])

    panel((58, 184, 1222, 407))
    label((84, 205), "samples/out_of_bounds.cpp", mono, c["amber"])
    for number, code in enumerate(source_lines, 1):
        if number == LINE:
            draw.rounded_rectangle((78, 305, 1202, 334), radius=7, fill="#3d2634")
        label((89, 236 + (number - 1) * 24), f"{number:>2}  {code}", mono,
              c["red"] if number == LINE else c["white"])

    panel((58, 425, 1222, 650))
    label((83, 441), "Terminal · result excerpt", heading, c["muted"])
    if stage >= 1:
        label((84, 480), "$ python3 cli.py samples/out_of_bounds.cpp", mono, c["teal"])
    if stage == 1:
        label((84, 525), "Review request sent to local model endpoint...", mono, c["muted"])
    if stage >= 2:
        label((84, 525), f"Summary: {TITLE}")
    if stage >= 3:
        label((84, 558), f"Finding: {CATEGORY} · {SEVERITY} · line {LINE}", mono, c["amber"])
    if stage >= 4:
        label((84, 591), f"Suggested fix: {FIX}", mono, c["teal"])
    if stage >= 5:
        draw.rounded_rectangle((892, 667, 1222, 701), radius=12, fill="#1c493f")
        label((918, 674), "Validated finding", tiny, c["teal"])
    label((58, 670), "Source is reviewed, never executed  •  Full output: CLI JSON", tiny, c["muted"])
    return image


def chunk(tag, payload):
    return tag + struct.pack("<I", len(payload)) + payload + (b"\0" if len(payload) & 1 else b"")


def listing(tag, payload):
    return chunk(b"LIST", tag + payload)


def write_avi(path, frames):
    fps = 10
    repeats = [15, 15, 13, 14, 18, 25]
    width, height = GIF_SIZE
    encoded = []
    for frame, repeat in zip(frames, repeats):
        buffer = BytesIO()
        frame.resize(GIF_SIZE, Image.Resampling.LANCZOS).save(
            buffer, format="JPEG", quality=84, subsampling=0
        )
        encoded.extend([buffer.getvalue()] * repeat)
    frame_count = len(encoded)
    max_size = max(map(len, encoded))
    avih = struct.pack("<IIIIIIIIII4I", 1_000_000 // fps, max_size * fps, 0, 0x10,
                       frame_count, 0, 1, max_size, width, height, 0, 0, 0, 0)
    strh = struct.pack("<4s4sIHHIIIIIIIIhhhh", b"vids", b"MJPG", 0, 0, 0, 0,
                       1, fps, 0, frame_count, max_size, 0xFFFFFFFF, 0,
                       0, 0, width, height)
    strf = struct.pack("<IiiHH4sIiiII", 40, width, height, 1, 24, b"MJPG",
                       width * height * 3, 0, 0, 0, 0)
    hdrl = listing(b"hdrl", chunk(b"avih", avih) + listing(b"strl", chunk(b"strh", strh) + chunk(b"strf", strf)))
    movi = bytearray()
    index = bytearray()
    for jpeg in encoded:
        offset = 4 + len(movi)
        movi.extend(chunk(b"00dc", jpeg))
        index.extend(struct.pack("<4sIII", b"00dc", 0x10, offset, len(jpeg)))
    body = hdrl + listing(b"movi", movi) + chunk(b"idx1", index)
    path.write_bytes(b"RIFF" + struct.pack("<I", len(body) + 4) + b"AVI " + body)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "docs")
    args = parser.parse_args()
    source_lines = SOURCE.read_text().splitlines()
    if len(source_lines) != 7 or "i <= values.size()" not in source_lines[LINE - 1]:
        parser.error("the public sample changed; review the recorded finding before rendering")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    frames = [render_stage(stage, source_lines, load_fonts()) for stage in range(6)]
    gif_frames = [frame.resize(GIF_SIZE, Image.Resampling.LANCZOS) for frame in frames]
    gif_path = args.output_dir / "demo.gif"
    gif_frames[0].save(gif_path, save_all=True, append_images=gif_frames[1:],
                       duration=[1500, 1500, 1300, 1400, 1800, 2500], loop=0, optimize=True)
    avi_path = args.output_dir / "demo.avi"
    write_avi(avi_path, frames)
    print(f"Created {gif_path} and {avi_path}")


if __name__ == "__main__":
    main()
