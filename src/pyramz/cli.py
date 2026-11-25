"""Command line interface: ``pyramz list | search | show | export | sprite | gallery``."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pyramz
from pyramz.gallery import build_gallery


def _render_opts(a) -> dict:
    o = {"size": a.size, "color": a.color, "stroke_width": a.stroke_width, "style": a.style, "corners": a.corners}
    if a.accent:
        o["accent"] = a.accent
    return o


def _add_style_args(p):
    p.add_argument("--size", type=int, default=24)
    p.add_argument("--color", default="currentColor")
    p.add_argument("--stroke-width", type=float, default=1.75)
    p.add_argument("--style", choices=["outline", "duotone"], default="outline")
    p.add_argument("--accent", default=None, help="duotone tint colour")
    p.add_argument("--corners", choices=["round", "sharp"], default="round")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="pyramz", description="Pyramz icon toolkit")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("list", help="list icon names")
    p.add_argument("--category")

    p = sub.add_parser("search", help="search icons by name or tag")
    p.add_argument("query")

    p = sub.add_parser("show", help="print an icon's SVG to stdout")
    p.add_argument("name")
    _add_style_args(p)

    p = sub.add_parser("export", help="write icons as .svg (or .png) files")
    p.add_argument("names", nargs="*", help="icon names (default: all)")
    p.add_argument("-o", "--out", default="pyramz-svg")
    p.add_argument("--png", action="store_true", help="also write PNGs (needs cairosvg)")
    _add_style_args(p)

    p = sub.add_parser("sprite", help="write an SVG sprite sheet")
    p.add_argument("-o", "--out", default="pyramz-sprite.svg")
    p.add_argument("names", nargs="*")

    p = sub.add_parser("gallery", help="write an interactive HTML gallery")
    p.add_argument("-o", "--out", default="pyramz-gallery.html")

    a = ap.parse_args(argv)

    if a.cmd == "list":
        cats = [a.category] if a.category else pyramz.categories()
        for c in cats:
            print(f"# {c}")
            for n in pyramz.names(c):
                print(f"  {n}")
    elif a.cmd == "search":
        hits = pyramz.search(a.query)
        print("\n".join(hits) if hits else "no matches")
        return 0 if hits else 1
    elif a.cmd == "show":
        try:
            print(pyramz.icon(a.name, **_render_opts(a)))
        except KeyError as e:
            print(e.args[0], file=sys.stderr)
            return 2
    elif a.cmd == "export":
        out = Path(a.out)
        out.mkdir(parents=True, exist_ok=True)
        targets = a.names or pyramz.names()
        for n in targets:
            ic = pyramz.icon(n, **_render_opts(a))
            ic.save(out / f"{n}.svg")
            if a.png:
                ic.to_png(out / f"{n}.png")
        print(f"wrote {len(targets)} icon(s) to {out}/")
    elif a.cmd == "sprite":
        Path(a.out).write_text(pyramz.sprite(a.names or None), encoding="utf-8")
        print(f"wrote {a.out}")
    elif a.cmd == "gallery":
        Path(a.out).write_text(build_gallery(), encoding="utf-8")
        print(f"wrote {a.out}")
    return 0


def entry() -> None:
    """Console-script entry point. Exits quietly when output is piped into a
    command that stops reading early (e.g. ``pyramz list | head``)."""
    import os

    try:
        code = main()
        sys.stdout.flush()
    except BrokenPipeError:
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        code = 0
    raise SystemExit(code)


if __name__ == "__main__":  # pragma: no cover
    entry()
