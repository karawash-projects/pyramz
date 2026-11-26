"""Pyramz: original, duotone-ready SVG icons for Python.

>>> import pyramz
>>> svg = pyramz.icon("home", size=32, style="duotone", accent="#6366f1")
>>> str(svg)[:4]
'<svg'
>>> pyramz.icons.search(size=20)        # attribute-style access
<pyramz.Icon 'search'>
"""

from __future__ import annotations

import difflib
from collections.abc import Iterable
from html import escape

from ._registry import aliases as _aliases
from ._registry import registry as _registry
from ._render import Icon
from ._render import render as _render
from ._shapes import IconDef, P

__all__ = [
    "Icon",
    "icon",
    "names",
    "search",
    "categories",
    "info",
    "icons",
    "aliases",
    "sprite",
    "set_defaults",
    "reset_defaults",
    "register",
    "__version__",
]
__version__ = "0.5.0"

_FACTORY_DEFAULTS: dict[str, object] = {
    "size": 24,
    "color": "currentColor",
    "stroke_width": 1.75,
    "style": "outline",
    "corners": "round",
}
_defaults: dict[str, object] = dict(_FACTORY_DEFAULTS)


def _normalise(name: str) -> str:
    return name.strip().lower().replace("_", "-").replace(" ", "-")


def _get(name: str) -> IconDef:
    key = _normalise(name)
    key = _aliases().get(key, key)
    reg = _registry()
    if key not in reg:
        close = difflib.get_close_matches(key, [*reg.keys(), *_aliases()], n=3, cutoff=0.55)
        hint = f" Did you mean: {', '.join(close)}?" if close else ""
        raise KeyError(f"Unknown icon {name!r}.{hint}")
    return reg[key]


def icon(name: str, **options) -> Icon:
    """Render an icon by name.

    Options: size, color, stroke_width, style ("outline" | "duotone"),
    accent, accent_opacity, corners ("round" | "sharp"), absolute_stroke,
    title (adds an accessible <title>), class_, plus any extra SVG
    attribute (underscores become dashes, e.g. ``data_testid="x"``).
    """
    merged = {**_defaults, **options}
    return _render(_get(name), **merged)


def names(category: str | None = None) -> list[str]:
    reg = _registry()
    return sorted(n for n, d in reg.items() if category is None or d.category == category)


def aliases() -> dict[str, str]:
    """Alternative names mapped to Pyramz icon names."""
    return dict(_aliases())


def categories() -> list[str]:
    return sorted({d.category for d in _registry().values()})


def info(name: str) -> dict[str, object]:
    d = _get(name)
    return {"name": d.name, "category": d.category, "tags": list(d.tags)}


def search(query: str, limit: int = 20) -> list[str]:
    """Rank icons by name, tag and category match (with fuzzy fallback)."""
    q = _normalise(query)
    if not q:
        return []
    scored = []
    target = _aliases().get(q)
    for d in _registry().values():
        if d.name == target:
            scored.append((-90, d.name))
            continue
        score = 0
        if d.name == q:
            score = 100
        elif d.name.startswith(q):
            score = 80
        elif q in d.name:
            score = 60
        elif q in d.tags:
            score = 50
        elif any(t.startswith(q) for t in d.tags):
            score = 35
        elif q == d.category:
            score = 20
        else:
            words = (d.name, *d.tags)
            if difflib.get_close_matches(q, words, n=1, cutoff=0.8):
                score = 10
        if score:
            scored.append((-score, d.name))
    # fuzzy (typo) matches are only a fallback when nothing matched directly
    if any(-s > 10 for s, _ in scored):
        scored = [(s, n) for s, n in scored if -s > 10]
    return [n for _, n in sorted(scored)[:limit]]


def set_defaults(**options) -> None:
    """Set project-wide defaults, e.g. ``set_defaults(stroke_width=1.5)``."""
    unknown = set(options) - {
        "size",
        "color",
        "stroke_width",
        "style",
        "accent",
        "accent_opacity",
        "corners",
        "absolute_stroke",
        "class_",
    }
    if unknown:
        raise TypeError(f"Unknown default(s): {', '.join(sorted(unknown))}")
    _defaults.update(options)


def reset_defaults() -> None:
    _defaults.clear()
    _defaults.update(_FACTORY_DEFAULTS)


def register(
    name: str, paths: Iterable[str], *, category: str = "custom", tags: Iterable[str] = (), tone: Iterable[int] = ()
) -> None:
    """Add your own icon to the set at runtime.

    ``paths`` are SVG path ``d`` strings on a 24x24 grid; ``tone`` lists the
    indexes of paths that should be tinted in the duotone style.
    """
    key = _normalise(name)
    reg = _registry()
    if key in reg or key in _aliases():
        raise ValueError(f"Icon {key!r} already exists")
    tone_idx = set(tone)
    shapes = tuple(P(d, tone=i in tone_idx) for i, d in enumerate(paths))
    if not shapes:
        raise ValueError("register() needs at least one path")
    reg[key] = IconDef(key, category, tuple(tags), shapes)


def sprite(icon_names: Iterable[str] | None = None, *, prefix: str = "pyramz-", **options) -> str:
    """Build an SVG sprite sheet of <symbol>s for ``<use href="#pyramz-home"/>``.

    Embed it once per page; each use costs a few bytes instead of a full SVG.
    """
    options.pop("size", None)
    out = ['<svg xmlns="http://www.w3.org/2000/svg" style="display:none">']
    for n in icon_names or names():
        svg = str(icon(n, **options))
        inner = svg[svg.index(">") + 1 : -len("</svg>")]
        opts = {**_defaults, **options}
        round_ = opts["corners"] == "round"
        join = 'stroke-linejoin="round"' if round_ else 'stroke-linejoin="miter" stroke-miterlimit="4"'
        cap = "round" if round_ else "square"
        out.append(
            f'<symbol id="{escape(prefix + _normalise(n))}" viewBox="0 0 24 24" fill="none" '
            f'stroke="{escape(str(opts["color"]))}" stroke-width="{float(opts["stroke_width"]):g}" '
            f'stroke-linecap="{cap}" {join}>{inner}</symbol>'
        )
    out.append("</svg>")
    return "".join(out)


class _Namespace:
    """``pyramz.icons.arrow_right(size=20)``: attribute-style access with
    tab completion in IPython."""

    def __getattr__(self, attr: str):
        if attr.startswith("__"):
            raise AttributeError(attr)
        definition = _get(attr)

        def _make(**options) -> Icon:
            return icon(definition.name, **options)

        _make.__name__ = attr
        _make.__doc__ = f"Render the '{definition.name}' icon."
        return _make

    def __dir__(self):
        return [n.replace("-", "_") for n in names()]


icons = _Namespace()
