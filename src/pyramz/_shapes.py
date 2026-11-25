"""Low-level shape primitives and geometry helpers used to define icons.

Every icon is drawn on a 24x24 grid with a 2px safe margin. Shapes are
stored as lightweight tuples so the registry stays fast to import.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Shape:
    """A single SVG element inside an icon.

    tone:   in the ``duotone`` style this shape is also filled with the
            accent colour (at reduced opacity). Ignored in ``outline``.
    solid:  the shape is always filled with the stroke colour (dots, pips).
    tone_only: drawn only in ``duotone`` as a filled backdrop, never stroked.
    """

    tag: str
    attrs: tuple[tuple[str, str], ...]
    tone: bool = False
    solid: bool = False
    tone_only: bool = False

    def attr_dict(self) -> dict[str, str]:
        return dict(self.attrs)


def _fmt(v: float) -> str:
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def _a(**kw) -> tuple[tuple[str, str], ...]:
    return tuple((k.replace("_", "-"), _fmt(v) if isinstance(v, (int, float)) else v) for k, v in kw.items())


def _rot(rotate: float, about: tuple[float, float]) -> dict:
    return {"transform": f"rotate({_fmt(rotate)} {_fmt(about[0])} {_fmt(about[1])})"} if rotate else {}


def P(d: str, tone: bool = False, tone_only: bool = False, rotate: float = 0, about=(12, 12)) -> Shape:
    """Path. ``rotate`` (degrees, clockwise) tilts it about ``about``."""
    return Shape("path", _a(d=d, **_rot(rotate, about)), tone=tone, tone_only=tone_only)


def C(cx: float, cy: float, r: float, tone: bool = False, tone_only: bool = False) -> Shape:
    return Shape("circle", _a(cx=cx, cy=cy, r=r), tone=tone, tone_only=tone_only)


def R(
    x: float,
    y: float,
    w: float,
    h: float,
    rx: float = 0,
    tone: bool = False,
    tone_only: bool = False,
    rotate: float = 0,
    about=(12, 12),
) -> Shape:
    return Shape("rect", _a(x=x, y=y, width=w, height=h, rx=rx, **_rot(rotate, about)), tone=tone, tone_only=tone_only)


def Dot(cx: float, cy: float, r: float = 1.1) -> Shape:
    return Shape("circle", _a(cx=cx, cy=cy, r=r), solid=True)


# --------------------------------------------------------------------------
# Procedural geometry (used for gears, rays, stars, ...)
# --------------------------------------------------------------------------


def polygon_path(points) -> str:
    head, *rest = points
    d = f"M{_fmt(head[0])} {_fmt(head[1])}"
    for x, y in rest:
        d += f"L{_fmt(x)} {_fmt(y)}"
    return d + "Z"


def star_path(cx=12.0, cy=12.4, outer=9.0, inner=4.1, points=5) -> str:
    pts = []
    for i in range(points * 2):
        r = outer if i % 2 == 0 else inner
        ang = -math.pi / 2 + i * math.pi / points
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return polygon_path(pts)


def gear_path(cx=12.0, cy=12.0, outer=9.0, inner=6.9, teeth=8, tooth=0.42) -> str:
    """Gear outline with trapezoid teeth. ``tooth`` is the fraction of each
    sector occupied by the tooth tip."""
    pts = []
    step = 2 * math.pi / teeth
    for i in range(teeth):
        a = -math.pi / 2 + i * step
        tip = step * tooth / 2
        base = step * (tooth / 2 + 0.14)
        for ang, r in ((a - base, inner), (a - tip, outer), (a + tip, outer), (a + base, inner)):
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return polygon_path(pts)


def rays_path(cx=12.0, cy=12.0, r1=6.6, r2=9.2, count=8, offset=0.0) -> str:
    d = ""
    for i in range(count):
        ang = offset + i * 2 * math.pi / count
        x1, y1 = cx + r1 * math.cos(ang), cy + r1 * math.sin(ang)
        x2, y2 = cx + r2 * math.cos(ang), cy + r2 * math.sin(ang)
        d += f"M{_fmt(x1)} {_fmt(y1)}L{_fmt(x2)} {_fmt(y2)}"
    return d


@dataclass(frozen=True)
class IconDef:
    name: str
    category: str
    tags: tuple[str, ...]
    shapes: tuple[Shape, ...] = field(default_factory=tuple)


def seal_path(cx=12.0, cy=12.0, inner=7.7, outer=10.4, lobes=8) -> str:
    """Scalloped badge/seal outline made of quadratic lobes."""
    step = 2 * math.pi / lobes

    def pt(r, a):
        return cx + r * math.cos(a), cy + r * math.sin(a)

    a0 = -math.pi / 2 - step / 2
    x, y = pt(inner, a0)
    d = f"M{_fmt(x)} {_fmt(y)}"
    for i in range(lobes):
        a = a0 + i * step
        qx, qy = pt(outer, a + step / 2)
        ex, ey = pt(inner, a + step)
        d += f"Q{_fmt(qx)} {_fmt(qy)} {_fmt(ex)} {_fmt(ey)}"
    return d + "Z"


# --------------------------------------------------------------------------
# Signature: the "pen lift". Each icon carries one deliberate gap, as if the
# pen left the paper: open rings, open corners, detached arms and heads.
# --------------------------------------------------------------------------


def ring(cx: float, cy: float, r: float, gap: float = 50, at: float = -50, tone: bool = False) -> tuple[Shape, ...]:
    """Circle with a gap of ``gap`` degrees centred at angle ``at``
    (degrees, 0 = 3 o'clock, -90 = 12 o'clock). Tone fills the full disc."""
    a1 = math.radians(at + gap / 2)
    a2 = math.radians(at - gap / 2)
    x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
    x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
    d = f"M{_fmt(x1)} {_fmt(y1)}A{_fmt(r)} {_fmt(r)} 0 1 1 {_fmt(x2)} {_fmt(y2)}"
    shapes: tuple[Shape, ...] = (P(d),)
    if tone:
        shapes = (C(cx, cy, r, tone_only=True), *shapes)
    return shapes


def open_rect(x: float, y: float, w: float, h: float, rx: float, tone: bool = False) -> tuple[Shape, ...]:
    """Rounded rectangle whose top-right corner is lifted (left open)."""
    r = _fmt(rx)
    d = (
        f"M{_fmt(x + w - rx - 0.6)} {_fmt(y)}H{_fmt(x + rx)}"
        f"A{r} {r} 0 0 0 {_fmt(x)} {_fmt(y + rx)}V{_fmt(y + h - rx)}"
        f"A{r} {r} 0 0 0 {_fmt(x + rx)} {_fmt(y + h)}H{_fmt(x + w - rx)}"
        f"A{r} {r} 0 0 0 {_fmt(x + w)} {_fmt(y + h - rx)}V{_fmt(y + rx + 0.6)}"
    )
    shapes: tuple[Shape, ...] = (P(d),)
    if tone:
        shapes = (R(x, y, w, h, rx, tone_only=True), *shapes)
    return shapes


def swept_head(tx: float, ty: float, dx: float, dy: float, size: float = 1.0) -> str:
    """Pyramz arrowhead: two arms that sweep into the tip (concave curves),
    pointing along (dx, dy) with the tip at (tx, ty)."""
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    nx, ny = -uy, ux

    def p(a: float, b: float) -> str:
        a, b = a * size, b * size
        return f"{_fmt(tx + a * ux + b * nx)} {_fmt(ty + a * uy + b * ny)}"

    return f"M{p(-7, -6)}C{p(-5.4, -2.7)} {p(-3, -0.7)} {p(0, 0)}C{p(-3, 0.7)} {p(-5.4, 2.7)} {p(-7, 6)}"


def swept_arrow(x1: float, y1: float, x2: float, y2: float, size: float = 1.0, lift: float = 2.0) -> str:
    """Shaft from (x1, y1) towards (x2, y2), stopping ``lift`` short of the
    swept head's tip: the pen lift."""
    n = math.hypot(x2 - x1, y2 - y1)
    ex, ey = x2 - (x2 - x1) / n * lift * size, y2 - (y2 - y1) / n * lift * size
    return f"M{_fmt(x1)} {_fmt(y1)}L{_fmt(ex)} {_fmt(ey)}" + swept_head(x2, y2, x2 - x1, y2 - y1, size)
