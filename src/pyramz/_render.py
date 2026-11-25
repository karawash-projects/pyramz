from __future__ import annotations

import base64
import re
from html import escape
from itertools import count
from pathlib import Path
from typing import Literal

from ._paths import sharpen
from ._shapes import IconDef

Style = Literal["outline", "duotone"]
Corners = Literal["round", "sharp"]

_uid = count(1)
_ATTR_NAME = re.compile(r"^[A-Za-z_:][-A-Za-z0-9_:.]*$")


def _attrs(d: dict[str, object]) -> str:
    return "".join(f' {k}="{escape(str(v), quote=True)}"' for k, v in d.items() if v is not None)


class Icon:
    """A rendered icon. Behaves like a string of SVG markup.

    Works directly in Jinja2/Django/Markupsafe (``__html__``), Jupyter
    (``_repr_svg_``) and anywhere a ``str`` is accepted.
    """

    __slots__ = ("name", "svg")

    def __init__(self, name: str, svg: str):
        self.name = name
        self.svg = svg

    # string-like behaviour
    def __str__(self) -> str:
        return self.svg

    def __html__(self) -> str:
        return self.svg

    def _repr_svg_(self) -> str:
        return self.svg

    def __repr__(self) -> str:
        return f"<pyramz.Icon {self.name!r}>"

    def __eq__(self, other) -> bool:
        return str(self) == str(other)

    def __hash__(self) -> int:
        return hash(self.svg)

    def to_data_uri(self) -> str:
        """``data:image/svg+xml;base64,...`` for use in <img src> or CSS."""
        return "data:image/svg+xml;base64," + base64.b64encode(self.svg.encode()).decode()

    def save(self, path: str | Path) -> Path:
        p = Path(path)
        p.write_text(self.svg, encoding="utf-8")
        return p

    def to_png(self, path: str | Path | None = None, scale: float = 1.0) -> bytes:
        """Rasterise to PNG. Requires the optional ``cairosvg`` extra."""
        try:
            import cairosvg  # type: ignore
        except ImportError as e:  # pragma: no cover
            raise ImportError("PNG export needs: pip install pyramz[png]") from e
        data = cairosvg.svg2png(bytestring=self.svg.encode(), scale=scale)
        if path is not None:
            Path(path).write_bytes(data)
        return data


def render(
    definition: IconDef,
    *,
    size: int | float | str = 24,
    color: str = "currentColor",
    stroke_width: float = 1.75,
    style: Style = "outline",
    accent: str | None = None,
    accent_opacity: float = 0.22,
    corners: Corners = "round",
    absolute_stroke: bool = False,
    title: str | None = None,
    class_: str | None = None,
    **attrs: object,
) -> Icon:
    if style not in ("outline", "duotone"):
        raise ValueError(f"style must be 'outline' or 'duotone', got {style!r}")
    if corners not in ("round", "sharp"):
        raise ValueError(f"corners must be 'round' or 'sharp', got {corners!r}")

    opacity = f"{float(accent_opacity):g}"
    sw = float(stroke_width)
    if absolute_stroke:
        try:
            sw = sw * 24 / float(size)
        except (TypeError, ValueError):
            raise ValueError("absolute_stroke needs a numeric size") from None
    sw_s = f"{sw:.3f}".rstrip("0").rstrip(".")

    root: dict[str, object] = {
        "xmlns": "http://www.w3.org/2000/svg",
        "width": size,
        "height": size,
        "viewBox": "0 0 24 24",
        "fill": "none",
        "stroke": color,
        "stroke-width": sw_s,
        "stroke-linecap": "round" if corners == "round" else "square",
        "stroke-linejoin": "round" if corners == "round" else "miter",
        "class": " ".join(c for c in ("pyramz", f"pyramz-{definition.name}", class_) if c),
    }
    if corners == "sharp":
        root["stroke-miterlimit"] = 4  # acute joins (swept arrowheads) bevel instead of spiking
    for k, v in attrs.items():
        key = k.rstrip("_").replace("_", "-")
        if not _ATTR_NAME.match(key):
            raise ValueError(f"invalid SVG attribute name: {k!r}")
        root[key] = v

    body = []
    if title:
        tid = f"pyramz-t{next(_uid)}"
        root["role"] = "img"
        root["aria-labelledby"] = tid
        body.append(f'<title id="{tid}">{escape(title)}</title>')
    else:
        root["aria-hidden"] = "true"
        root.setdefault("focusable", "false")

    duo = style == "duotone"
    tint = accent or color
    tone_layer, line_layer = [], []
    for s in definition.shapes:
        a = s.attr_dict()
        if corners == "sharp":
            if s.tag == "rect" and "rx" in a:
                a["rx"] = str(min(float(a["rx"]), 0.75))
            elif s.tag == "path":
                a["d"] = sharpen(a["d"])
        if s.tone_only:
            if duo:
                tone_layer.append(f'<{s.tag}{_attrs(a)} fill="{escape(tint)}" fill-opacity="{opacity}" stroke="none"/>')
            continue
        if s.solid:
            line_layer.append(f'<{s.tag}{_attrs(a)} fill="{escape(color)}" stroke="none"/>')
            continue
        if duo and s.tone:
            tone_layer.append(f'<{s.tag}{_attrs(a)} fill="{escape(tint)}" fill-opacity="{opacity}" stroke="none"/>')
        line_layer.append(f"<{s.tag}{_attrs(a)}/>")

    body.extend(tone_layer)
    body.extend(line_layer)
    return Icon(definition.name, f"<svg{_attrs(root)}>{''.join(body)}</svg>")
