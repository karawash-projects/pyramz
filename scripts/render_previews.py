"""Render preview sheets of the whole set and a small-size check sheet.

    pip install -e ".[docs]"
    python scripts/render_previews.py            # writes build/preview-*.png
    python scripts/render_previews.py home bot   # + build/check.png for these icons

The check sheet shows each icon at stroke 2 at true 20px and 18px (and 4x
zoomed pixels) so you can judge legibility at real UI sizes.
"""

from __future__ import annotations

import io
import sys
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw

import pyramz

ROOT = Path(__file__).resolve().parent.parent
INK = "#1f2937"


def _png(name: str, size: int, **kw) -> Image.Image:
    svg = str(pyramz.icon(name, size=size, color=INK, **kw))
    return Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert("RGBA")


def sheet(style: str, out: Path, cols: int = 12, cell: int = 96) -> None:
    names = pyramz.names()
    rows = -(-len(names) // cols)
    img = Image.new("RGB", (cols * cell, rows * cell), "white")
    draw = ImageDraw.Draw(img)
    for i, n in enumerate(names):
        x, y = (i % cols) * cell, (i // cols) * cell
        ic = _png(n, 64, style=style, accent="#6366f1")
        img.paste(ic, (x + 16, y + 6), ic)
        draw.text((x + 4, y + 78), n[:15], fill="#666")
    img.save(out)
    print(f"wrote {out.relative_to(ROOT)}")


def check(names: list[str], out: Path) -> None:
    w = 110
    img = Image.new("RGB", (len(names) * w, 250), "white")
    draw = ImageDraw.Draw(img)
    for i, n in enumerate(names):
        x = i * w
        big = _png(n, 96, stroke_width=2)
        img.paste(big, (x + 7, 5), big)
        zoom = _png(n, 20, stroke_width=2).resize((80, 80), Image.NEAREST)
        img.paste(zoom, (x + 15, 108), zoom)
        for dx, s in ((30, 18), (60, 20)):
            ic = _png(n, s, stroke_width=2)
            img.paste(ic, (x + dx, 200), ic)
        draw.text((x + 4, 232), n[:17], fill="#555")
    out.parent.mkdir(exist_ok=True)
    img.save(out)
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    (ROOT / "build").mkdir(exist_ok=True)
    sheet("outline", ROOT / "build" / "preview-outline.png")
    sheet("duotone", ROOT / "build" / "preview-duotone.png")
    if len(sys.argv) > 1:
        check(sys.argv[1:], ROOT / "build" / "check.png")
