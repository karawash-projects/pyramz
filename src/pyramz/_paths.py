"""Minimal SVG path parsing, used to derive the ``corners="sharp"`` variant.

Every icon is drawn once, with round corners. In sharp mode, each
quarter-circle corner (an elliptical-arc segment with equal radii of at most
``MAX_CORNER`` that turns exactly 90 degrees) is tightened to ``SHARP_RADIUS``
around the same corner point. Large arcs (rings, curves) are left untouched.
"""

from __future__ import annotations

import re
from functools import lru_cache

SHARP_RADIUS = 0.75
MAX_CORNER = 5.0
_EPS = 0.06

_TOKEN = re.compile(r"[MmLlHhVvCcSsQqTtAaZz]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")
_ARGS = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7, "Z": 0}


def _fmt(v: float) -> str:
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def _tokens(d: str) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(d):
        m = _TOKEN.match(d, i)
        if m is None:
            i += 1  # separators: spaces and commas
            continue
        out.append(m.group())
        i = m.end()
    return out


def to_absolute(d: str) -> list[tuple[str, list[float]]]:
    """Parse ``d`` into absolute segments: M L C Q A Z (H/V/S/T are expanded)."""
    toks = _tokens(d)
    segs: list[tuple[str, list[float]]] = []
    cx = cy = sx = sy = 0.0
    last_ctrl = None
    i, cmd = 0, None
    while i < len(toks):
        if toks[i].isalpha():
            cmd = toks[i]
            i += 1
            if cmd in "Zz":
                segs.append(("Z", []))
                cx, cy = sx, sy
                last_ctrl = None
                continue
        if cmd is None:
            raise ValueError(f"path data must start with a command: {d!r}")
        up = cmd.upper()
        n = _ARGS[up]
        vals = [float(t) for t in toks[i : i + n]]
        if len(vals) < n:
            raise ValueError(f"incomplete path data: {d!r}")
        i += n
        rel = cmd.islower()
        if up == "M":
            x, y = vals
            if rel:
                x, y = cx + x, cy + y
            segs.append(("M", [x, y]))
            cx, cy = sx, sy = x, y
            cmd = "l" if rel else "L"  # implicit lineto after moveto
            last_ctrl = None
        elif up in "LHV":
            if up == "L":
                x, y = vals
                if rel:
                    x, y = cx + x, cy + y
            elif up == "H":
                x, y = (cx + vals[0] if rel else vals[0]), cy
            else:
                x, y = cx, (cy + vals[0] if rel else vals[0])
            segs.append(("L", [x, y]))
            cx, cy = x, y
            last_ctrl = None
        elif up in "CS":
            if up == "C":
                x1, y1, x2, y2, x, y = vals
                if rel:
                    x1, y1, x2, y2, x, y = cx + x1, cy + y1, cx + x2, cy + y2, cx + x, cy + y
            else:
                x2, y2, x, y = vals
                if rel:
                    x2, y2, x, y = cx + x2, cy + y2, cx + x, cy + y
                x1, y1 = (2 * cx - last_ctrl[0], 2 * cy - last_ctrl[1]) if last_ctrl else (cx, cy)
            segs.append(("C", [x1, y1, x2, y2, x, y]))
            last_ctrl = (x2, y2)
            cx, cy = x, y
        elif up in "QT":
            if up == "Q":
                x1, y1, x, y = vals
                if rel:
                    x1, y1, x, y = cx + x1, cy + y1, cx + x, cy + y
            else:
                x, y = vals
                if rel:
                    x, y = cx + x, cy + y
                x1, y1 = (2 * cx - last_ctrl[0], 2 * cy - last_ctrl[1]) if last_ctrl else (cx, cy)
            segs.append(("Q", [x1, y1, x, y]))
            last_ctrl = (x1, y1)
            cx, cy = x, y
        else:  # A
            rx, ry, rot, large, sweep, x, y = vals
            if rel:
                x, y = cx + x, cy + y
            segs.append(("A", [rx, ry, rot, large, sweep, x, y]))
            cx, cy = x, y
            last_ctrl = None
    return segs


def to_string(segs: list[tuple[str, list[float]]]) -> str:
    return "".join(c + " ".join(_fmt(v) for v in vals) for c, vals in segs)


def _quarter_corner(p0, seg):
    """If ``seg`` (an absolute A from ``p0``) is a 90-degree corner arc,
    return (corner_point, sweep); otherwise None."""
    rx, ry, rot, large, sweep, x, y = seg
    if abs(rx - ry) > _EPS or rx > MAX_CORNER or rx <= SHARP_RADIUS or large or abs(rot) > _EPS:
        return None
    dx, dy = x - p0[0], y - p0[1]
    if abs(abs(dx) - rx) > _EPS or abs(abs(dy) - rx) > _EPS:
        return None
    for centre, corner in (((p0[0], y), (x, p0[1])), ((x, p0[1]), (p0[0], y))):
        a = (p0[0] - centre[0], p0[1] - centre[1])
        b = (x - centre[0], y - centre[1])
        cross = a[0] * b[1] - a[1] * b[0]
        if (cross > 0) == bool(sweep):
            return corner, sweep
    return None


@lru_cache(maxsize=4096)
def sharpen(d: str, radius: float = SHARP_RADIUS) -> str:
    """Return ``d`` with every small quarter-circle corner tightened to ``radius``."""
    segs = to_absolute(d)
    out: list[tuple[str, list[float]]] = []
    cur = (0.0, 0.0)
    start = cur
    changed = False
    for cmd, vals in segs:
        if cmd == "A":
            hit = _quarter_corner(cur, vals)
            if hit:
                (vx, vy), sweep = hit
                r = vals[0]
                k = radius / r
                ax, ay = vx + (cur[0] - vx) * k, vy + (cur[1] - vy) * k
                ex, ey = vals[5], vals[6]
                bx, by = vx + (ex - vx) * k, vy + (ey - vy) * k
                out += [("L", [ax, ay]), ("A", [radius, radius, 0, 0, sweep, bx, by]), ("L", [ex, ey])]
                cur = (ex, ey)
                changed = True
                continue
        out.append((cmd, vals))
        if cmd == "M":
            cur = start = (vals[0], vals[1])
        elif cmd == "Z":
            cur = start
        else:
            cur = (vals[-2], vals[-1])
    return to_string(out) if changed else d


def corner_arcs(d: str) -> int:
    """Number of corners ``sharpen`` would tighten (used in tests)."""
    segs = to_absolute(d)
    cur = (0.0, 0.0)
    start = cur
    n = 0
    for cmd, vals in segs:
        if cmd == "A" and _quarter_corner(cur, vals):
            n += 1
        if cmd == "M":
            cur = start = (vals[0], vals[1])
        elif cmd == "Z":
            cur = start
        else:
            cur = (vals[-2], vals[-1]) if vals else cur
    return n
