"""The Pyramz icon set.

All artwork here is original, drawn on a 24x24 grid. Design rules:

* Content lives inside 2..22. Icons must stay legible at stroke 2 at 18-20px.
* The "pen lift" signature: one deliberate gap per icon (``ring``,
  ``open_rect``, ``swept_arrow``/``swept_head``, dot terminals).
* Boxes are inset, with soft corners (radius about 4); rings use radius 8.5
  with a 70-degree opening; diagonal icons are tilted off 45 degrees with
  ``rotate=``.
* Shapes marked ``tone`` are tinted in the duotone style; line-only icons have
  no tone layer.
* Draw round corners only: ``corners="sharp"`` is derived automatically.
"""

from __future__ import annotations

from ._shapes import (
    C,
    Dot,
    IconDef,
    P,
    R,
    gear_path,
    open_rect,
    rays_path,
    ring,
    star_path,
    swept_arrow,
    swept_head,
)

_ICONS: dict[str, IconDef] = {}
_ALIASES: dict[str, str] = {}


def _add(name, category, tags, *shapes):
    if name in _ICONS:
        raise ValueError(f"duplicate icon {name!r}")
    _ICONS[name] = IconDef(name, category, tuple(tags.split()), tuple(shapes))


# ---------------------------------------------------------------- interface
_add(
    "home",
    "interface",
    "house main start dashboard",
    P("M5.5 9.6V19a1.5 1.5 0 0 0 1.5 1.5h10a1.5 1.5 0 0 0 1.5-1.5V9.6"),
    P("M5.5 9.6 12 4.3l6.5 5.3V19a1.5 1.5 0 0 1-1.5 1.5H7A1.5 1.5 0 0 1 5.5 19Z", tone_only=True),
    P("M3 11.2 12 3.8l9 7.4"),
    P("M10 20.5v-4.5a2 2 0 0 1 4 0v4.5"),
)

_add(
    "search",
    "interface",
    "find magnifier lookup zoom",
    C(10.5, 10.5, 6.5, tone=True),
    P("M15.3 15.3 20.5 20.5"),
    P("M7.6 9.2a3.2 3.2 0 0 1 2.2-2"),
)

_add(
    "settings",
    "interface",
    "gear cog preferences options",
    P(gear_path(teeth=7, inner=7, outer=9.5, tooth=0.5), tone=True),
    *ring(12, 12, 2.9, gap=70),
)

_add(
    "sliders",
    "interface",
    "controls adjust filters mixer",
    P("M4 7h9M18 7h2M4 17h3M12 17h8"),
    C(15.5, 7, 2.5, tone=True),
    C(9.5, 17, 2.5, tone=True),
)

_add("menu", "interface", "hamburger navigation list lines", P("M8 7.5h12M4 12h16M8 16.5h12"))

_add(
    "more-horizontal",
    "interface",
    "dots ellipsis overflow options",
    Dot(6, 12, 1.3),
    Dot(12, 12, 1.3),
    *ring(18, 12, 1.6, gap=90),
)

_add(
    "more-vertical",
    "interface",
    "dots ellipsis overflow kebab",
    Dot(12, 6, 1.3),
    Dot(12, 12, 1.3),
    *ring(12, 18, 1.6, gap=90),
)

_add(
    "grid",
    "interface",
    "layout apps tiles dashboard",
    R(2.5, 2.5, 7, 7, 2.6, tone=True),
    *open_rect(14.5, 2.5, 7, 7, 2.6),
    R(2.5, 14.5, 7, 7, 2.6),
    R(14.5, 14.5, 7, 7, 2.6, tone=True),
)

_add(
    "list",
    "interface",
    "items rows bullets",
    *ring(5, 6.5, 1.3, gap=90),
    *ring(5, 12, 1.3, gap=90),
    *ring(5, 17.5, 1.3, gap=90),
    P("M10 6.5H20M10 12H17M10 17.5H14"),
)

_add(
    "filter",
    "interface",
    "funnel sort refine",
    P("M4.5 5h15a.6.6 0 0 1 .45 1L14 13v5.6l-4 1.9V13L4.05 6a.6.6 0 0 1 .45-1Z", tone=True),
)

_add(
    "plus",
    "interface",
    "add new create",
    P("M12 9v6M9 12h6"),
    Dot(12, 3.8, 1.45),
    Dot(12, 20.2, 1.45),
    Dot(3.8, 12, 1.45),
    Dot(20.2, 12, 1.45),
)

_add("minus", "interface", "remove subtract", P("M9 12h6"), Dot(3.8, 12, 1.45), Dot(20.2, 12, 1.45))

_add(
    "x",
    "interface",
    "close cancel dismiss times",
    P("M9.4 9.4l5.2 5.2M14.6 9.4l-5.2 5.2"),
    Dot(5.6, 5.6, 1.45),
    Dot(18.4, 18.4, 1.45),
    Dot(18.4, 5.6, 1.45),
    Dot(5.6, 18.4, 1.45),
)

_add("check", "interface", "done tick confirm ok", P("M4.5 13l3.2 3.2"), P("M10.8 16.4 20 6.2"))

_add(
    "check-circle",
    "interface",
    "done success verified met complete",
    *ring(12, 12, 8.5, gap=70, tone=True),
    P("M8.2 12.3l2.2 2.2", rotate=12),
    P("M12.8 13.8l3.3-3.9", rotate=12),
)

_add(
    "x-circle",
    "interface",
    "error close cancel",
    *ring(12, 12, 8.5, gap=70, tone=True),
    P("M9.3 9.3l5.4 5.4M14.7 9.3l-5.4 5.4", rotate=15),
)

_add(
    "info",
    "interface",
    "about help details",
    *ring(12, 12, 8.5, gap=70, tone=True),
    P("M12 11v5.2h1.4"),
    Dot(12, 7.9, 1.2),
)

_add(
    "alert-triangle",
    "interface",
    "warning caution danger",
    P("M12 3.8Q18.24 10.90 21 20Q12 21.20 3 20Q5.76 10.90 12 3.8Z", tone=True),
    P("M12 9.4v3.4"),
    Dot(12, 16.9, 1.15),
)

_add(
    "help-circle",
    "interface",
    "question support faq",
    *ring(12, 12, 8.5, gap=70, tone=True),
    P("M9.7 9.8a2.4 2.4 0 0 1 4.6.8c0 1.6-2.3 2.1-2.3 3.4"),
    Dot(12, 16.7, 1.15),
)

_add(
    "eye",
    "interface",
    "view visible show watch",
    P("M19.8 10.6C17.6 7.5 15 6.8 12 6.8S5.4 8.3 2.8 12c2.6 3.5 5.7 4.7 9.2 5.2s6.6-1.5 9.2-5.2", tone=True),
    *ring(12, 12, 3, gap=80),
    Dot(12, 12, 0.9),
)

_add(
    "eye-off",
    "interface",
    "hidden invisible hide",
    P(
        "M7.6 6.6A9.6 9.6 0 0 1 12 5.5c3.8 0 7.2 2.5 9.2 6.5a14 14 0 0 1-1.8 2.7M16.6 17.2a8.9 8.9 0 0 1-4.6 1.3C8.2 18.5 4.8 16 2.8 12a14 14 0 0 1 2-2.8"
    ),
    P("M12 3v18", rotate=-35),
    Dot(12, 12, 1.4),
)

_add(
    "lock",
    "interface",
    "secure private password closed",
    *open_rect(4, 10.5, 16, 10, 3.5, tone=True),
    P("M7.8 10.5V8a4.2 4.2 0 0 1 8.4 0v2.5"),
    Dot(12, 15.5, 1.3),
)

_add(
    "unlock",
    "interface",
    "open unsecure public",
    *open_rect(4, 10.5, 16, 10, 3.5, tone=True),
    P("M7.8 10.5V8a4.2 4.2 0 0 1 8.1-1.6"),
    Dot(12, 15.5, 1.3),
)

_add(
    "refresh",
    "interface",
    "reload sync rotate update",
    P("M19 10.2A7.3 7.3 0 0 0 6.1 7.6"),
    P(swept_head(5, 9.2, -0.55, 1, 0.55)),
    P("M5 13.8a7.3 7.3 0 0 0 12.9 2.6"),
    P(swept_head(19, 14.8, 0.55, -1, 0.55)),
)

_add(
    "loader",
    "interface",
    "spinner loading progress wait",
    C(12, 12, 8.5, tone_only=True),
    P("M12 3.5a8.5 8.5 0 1 1-8.5 8.5"),
)

_add(
    "log-out",
    "interface",
    "sign out exit leave",
    P("M10 20H7a2.5 2.5 0 0 1-2.5-2.5v-11A2.5 2.5 0 0 1 7 4h3"),
    P(swept_arrow(9.5, 12, 20.5, 12, size=0.75)),
)

_add(
    "log-in",
    "interface",
    "sign in enter",
    P("M14 4h3a2.5 2.5 0 0 1 2.5 2.5v11A2.5 2.5 0 0 1 17 20h-3"),
    P(swept_arrow(3.5, 12, 14.5, 12, size=0.75)),
)

_add(
    "external-link",
    "interface",
    "open new window outbound",
    P("M17.5 14v3.5a3.5 3.5 0 0 1-3.5 3.5H6.5A3.5 3.5 0 0 1 3 17.5V10.5A3.5 3.5 0 0 1 6.5 7h3.5"),
    P(swept_arrow(10.5, 13.5, 20.5, 3.5, size=0.75)),
)

_add(
    "toggle",
    "interface",
    "switch on off setting",
    P("M15 7.5H7.5a4.5 4.5 0 0 0 0 9h9a4.5 4.5 0 0 0 4.3-5.8", tone=True),
    C(16.5, 12, 2.2),
)

# ---------------------------------------------------------------- arrows
_add("chevron-right", "arrows", "next forward caret", P(swept_head(15.5, 12, 1, 0, 1.1)))
_add("chevron-left", "arrows", "back previous caret", P(swept_head(8.5, 12, -1, 0, 1.1)))
_add("chevron-up", "arrows", "collapse caret", P(swept_head(12, 8.5, 0, -1, 1.1)))
_add("chevron-down", "arrows", "expand caret dropdown", P(swept_head(12, 15.5, 0, 1, 1.1)))
_add("arrow-right", "arrows", "next forward direction", P(swept_arrow(7.4, 12, 19.5, 12, size=1.15)), Dot(3.8, 12, 1.3))
_add(
    "arrow-left", "arrows", "back previous direction", P(swept_arrow(16.6, 12, 4.5, 12, size=1.15)), Dot(20.2, 12, 1.3)
)
_add("arrow-up", "arrows", "up direction north", P(swept_arrow(12, 16.6, 12, 4.5, size=1.15)), Dot(12, 20.2, 1.3))
_add("arrow-down", "arrows", "down direction south", P(swept_arrow(12, 7.4, 12, 19.5, size=1.15)), Dot(12, 3.8, 1.3))
_add(
    "arrow-up-right",
    "arrows",
    "diagonal trend growth",
    P(swept_arrow(6.92, 15.56, 17.73, 7.98, size=0.95)),
    Dot(4.14, 17.51, 1.3),
)
_add(
    "download",
    "arrows",
    "save get import",
    Dot(12, 3.6, 1.3),
    P(swept_arrow(12, 7.2, 12, 15.5, size=0.75)),
    P("M4 15.5v1.5a3.5 3.5 0 0 0 3.5 3.5h9a3.5 3.5 0 0 0 3.5-3.5v-1.5"),
)
_add(
    "upload",
    "arrows",
    "send export publish",
    P(swept_arrow(12, 13, 12, 3.8, size=0.75)),
    Dot(12, 16.6, 1.3),
    P("M4 15.5v1.5a3.5 3.5 0 0 0 3.5 3.5h9a3.5 3.5 0 0 0 3.5-3.5v-1.5"),
)
_add("expand", "arrows", "fullscreen maximize", P("M4.5 9V4.5H9M15 4.5h4.5V9M19.5 15v4.5H15M9 19.5H4.5V15"))

# ---------------------------------------------------------------- files
_add(
    "file",
    "files",
    "document page paper",
    P("M13.0 3.5H8.5A3 3 0 0 0 5.5 6.5V17.5A3 3 0 0 0 8.5 20.5H15.5A3 3 0 0 0 18.5 17.5V9.0Z", tone=True),
)

_add(
    "file-text",
    "files",
    "document notes article",
    P("M13.0 3.5H8.5A3 3 0 0 0 5.5 6.5V17.5A3 3 0 0 0 8.5 20.5H15.5A3 3 0 0 0 18.5 17.5V9.0Z", tone=True),
    P("M8.7 13h6.6M8.7 16.3h4"),
)

_add(
    "folder",
    "files",
    "directory collection",
    P("M3.5 7A1.5 1.5 0 0 1 5 5.5h4.2l2 2.3H19a1.5 1.5 0 0 1 1.5 1.5V17a2 2 0 0 1-2 2h-13a2 2 0 0 1-2-2Z", tone=True),
)

_add(
    "folder-open",
    "files",
    "directory browse",
    P("M3.5 17V7A1.5 1.5 0 0 1 5 5.5h4.2l2 2.3H17a1.5 1.5 0 0 1 1.5 1.5v1.2"),
    P(
        "M3.5 17 6 11.5a1.5 1.5 0 0 1 1.4-1H20a1 1 0 0 1 .9 1.4L18.6 17.8a2 2 0 0 1-1.8 1.2H5.5a2 2 0 0 1-2-2Z",
        tone=True,
    ),
)

_add(
    "image",
    "files",
    "picture photo gallery",
    *open_rect(3.5, 5, 17, 14.5, 4, tone=True),
    *ring(9, 10, 1.8, gap=80),
    P("M4.2 17.6 8.7 13.3l3.5 3.3 2.4-2.3 5.6 5.2"),
)

_add(
    "clipboard",
    "files",
    "copy paste board",
    P("M8.5 5.5H8A4 4 0 0 0 4 9.5v7.5a4 4 0 0 0 4 4h8a4 4 0 0 0 4-4V9.5a4 4 0 0 0-2.2-3.32"),
    R(8.5, 3.5, 7, 3.8, 1.9, tone=True),
    P("M7.5 13h9M7.5 16.5h4.5"),
)

_add(
    "copy",
    "files",
    "duplicate clone",
    *open_rect(9, 9, 11.5, 11.5, 3.5, tone=True),
    P("M6.2 15.5A2.7 2.7 0 0 1 3.5 12.8V6.2a2.7 2.7 0 0 1 2.7-2.7h6.6a2.7 2.7 0 0 1 2.7 2.7"),
)

_add(
    "trash",
    "files",
    "delete remove bin garbage",
    P("M6.2 7.5 7.1 19a1.5 1.5 0 0 0 1.5 1.4h6.8a1.5 1.5 0 0 0 1.5-1.4l.9-11.5", tone=True),
    P("M4 7.5h16"),
    P("M9.5 7.5V5a1.5 1.5 0 0 1 1.5-1.5h2A1.5 1.5 0 0 1 14.5 5v2.5"),
    P("M10 11.5v5M14 11.5v5"),
)

_add(
    "edit",
    "files",
    "pencil write compose modify",
    P("M15 4.6a2 2 0 0 1 2.8 0l1.6 1.6a2 2 0 0 1 0 2.8L10 18.4", rotate=15),
    P("M13.6 6 5.6 14 5 18.9 9.9 18.3", rotate=15),
    P("M15 4.6a2 2 0 0 1 2.8 0l1.6 1.6a2 2 0 0 1 0 2.8L9.9 18.3 5 18.9l.6-4.9Z", tone_only=True, rotate=15),
    P("M13.2 6.4l4.4 4.4", rotate=15),
)

_add(
    "save",
    "files",
    "disk floppy store",
    P("M4.5 6.5A2 2 0 0 1 6.5 4.5h9.2l3.8 3.8v9.2a2 2 0 0 1-2 2h-11a2 2 0 0 1-2-2Z", tone=True),
    P("M8 4.5v3.5h6.5V4.5"),
    R(7.5, 13, 9, 6.5, 1),
)

_add(
    "archive",
    "files",
    "box storage package",
    R(2.5, 3, 19, 3.8, 1.9),
    *open_rect(4, 9.5, 16, 11, 3.5, tone=True),
    P("M9.6 13.2h4.8"),
)

# ---------------------------------------------------------------- communication
_add(
    "mail",
    "communication",
    "email envelope message inbox",
    *open_rect(3.5, 5.5, 17, 13, 4, tone=True),
    P("M5.6 8.7c2.6 2.2 4.5 3.4 6.4 3.4s3.8-1.2 6.4-3.4"),
)

_add(
    "message",
    "communication",
    "chat bubble comment talk",
    P(
        "M4.5 6.5A2.5 2.5 0 0 1 7 4h10a2.5 2.5 0 0 1 2.5 2.5v7A2.5 2.5 0 0 1 17 16h-5L7.5 19.8V16H7a2.5 2.5 0 0 1-2.5-2.5Z",
        tone=True,
    ),
    P("M8.5 8.8h7M8.5 11.8h4"),
)

_add(
    "bell",
    "communication",
    "notification alert alarm",
    P(
        "M15.6 5.3A6 6 0 0 1 18 10.2v5.3l1.6 2.2H4.4L6 15.5v-5.3a6 6 0 0 1 7.7-5.8",
        tone=True,
        rotate=15,
        about=(12, 10),
    ),
    Dot(9.3, 20, 1.4),
)

_add(
    "send",
    "communication",
    "paper plane submit share",
    P("M20.5 3.5 3.5 10.5l7 3 3 7Z", tone=True, rotate=15),
    P("M20.5 3.5 10.5 13.5", rotate=15),
)

_add("phone", "communication", "smartphone mobile device", R(6.5, 2.5, 11, 19, 4, tone=True), P("M10.5 18h3"))

_add(
    "share",
    "communication",
    "network connect distribute",
    *ring(19.97, 9.10, 2.2, gap=80, tone=True),
    Dot(6.56, 9.46, 2.2),
    *ring(14.90, 19.97, 2.2, gap=80, tone=True),
    P("M9.96 9.37L16.57 9.19M8.68 12.13L12.79 17.31"),
)

_add(
    "link",
    "communication",
    "url chain hyperlink attach",
    P("M10.2 13.8a4 4 0 0 0 5.6 0l2.9-2.9a4 4 0 0 0-5.6-5.7l-1.2 1.2"),
    P("M13.8 10.2a4 4 0 0 0-5.6 0l-2.9 2.9a4 4 0 0 0 5.6 5.7l1.2-1.2"),
)

_add(
    "at-sign",
    "communication",
    "mention email handle",
    P("M15 8.8v4.6a2.3 2.3 0 0 0 4.6 0V9a5 5 0 0 0-5-5H9a5 5 0 0 0-5 5v6a5 5 0 0 0 5 5h5.5"),
    *ring(12, 12, 2.8, gap=70, tone=True),
)

# ---------------------------------------------------------------- people
_add(
    "user",
    "people",
    "person profile account avatar",
    C(12, 8, 3.8, tone=True),
    P("M4.5 20.5c.9-4 3.8-6.5 7.5-6.5s6.6 2.5 7.5 6.5"),
)

_add(
    "users",
    "people",
    "group team people members",
    C(9, 8.5, 3.3, tone=True),
    P("M2.8 19.5c.8-3.4 3.2-5.5 6.2-5.5s5.4 2.1 6.2 5.5"),
    P("M15 5.4a3.3 3.3 0 0 1 0 6.2"),
    P("M17.4 14.4c1.9.7 3.2 2.5 3.8 5.1"),
)

_add(
    "user-plus",
    "people",
    "add member invite",
    C(10, 8, 3.8, tone=True),
    P("M2.5 20.5c.9-4 3.8-6.5 7.5-6.5 2.1 0 3.9.8 5.3 2.2"),
    P("M19 13.5v6M16 16.5h6"),
)

_add(
    "heart",
    "people",
    "love like favorite health",
    P("M12 20s-8-4.7-8-10.4A4.4 4.4 0 0 1 12 7.2a4.4 4.4 0 0 1 8 2.4C20 15.3 12 20 12 20Z", tone=True),
    P("M7.1 8.6a2 2 0 0 1 1.6-.9"),
)

_add("star", "people", "favorite rating bookmark", P(star_path(), tone=True))

_add(
    "thumbs-up",
    "people",
    "like approve vote",
    P("M8 10.5 11.4 4a2 2 0 0 1 2.6 2.3l-.6 3.2h4.9a2 2 0 0 1 2 2.4l-1.2 6.4a2 2 0 0 1-2 1.7H8Z", tone=True),
    R(3.5, 10.5, 4.5, 9.5, 1.5),
)

_add(
    "smile",
    "people",
    "emoji happy face",
    *ring(12, 12, 8.5, gap=70, tone=True),
    P("M8.6 14a4 4 0 0 0 6.8 0"),
    Dot(9.2, 9.8, 1.15),
    Dot(14.8, 9.8, 1.15),
)

# ---------------------------------------------------------------- commerce
_add(
    "cart",
    "commerce",
    "shopping basket buy checkout",
    P("M2.5 4h2.2l2.2 11a1.5 1.5 0 0 0 1.5 1.2h8.9a1.5 1.5 0 0 0 1.5-1.1L20.5 8H5.6"),
    P("M5.6 8h14.9l-1.7 7.1a1.5 1.5 0 0 1-1.5 1.1H8.4a1.5 1.5 0 0 1-1.5-1.2Z", tone_only=True),
    C(9, 20, 1.3),
    C(17, 20, 1.3),
)

_add(
    "bag",
    "commerce",
    "shopping purchase store",
    P("M17.3 8h2.2l.9 10.6a2.2 2.2 0 0 1-2.2 2.4H5a2.2 2.2 0 0 1-2.2-2.4L3.7 8H15", tone=True),
    P("M9 11.5V7.2a3 3 0 0 1 6 0v4.3"),
)

_add(
    "tag",
    "commerce",
    "label price category",
    P(
        "M3.5 8.8a3 3 0 0 1 3-3h8.1a2 2 0 0 1 1.5.7l4.4 4.8a1.2 1.2 0 0 1 0 1.6l-4.4 4.8a2 2 0 0 1-1.5.7H6.5a3 3 0 0 1-3-3Z",
        tone=True,
    ),
    *ring(15.2, 12, 1.6, gap=90),
)

_add(
    "credit-card",
    "commerce",
    "payment billing card",
    *open_rect(3.5, 5.5, 17, 13, 4, tone=True),
    P("M3.5 10.2h17M7.2 14.8h3.3"),
)

_add(
    "wallet",
    "commerce",
    "money funds balance",
    *open_rect(3.5, 6, 17, 13.5, 4, tone=True),
    P("M3.5 9.6c0-2 1.3-3.4 3.3-4.1L13.8 3.6a1.6 1.6 0 0 1 2 1.5V6"),
    P("M20.5 11h-3a2 2 0 0 0 0 4h3"),
    Dot(17.6, 13, 1),
)

_add(
    "gift",
    "commerce",
    "present reward bonus",
    *open_rect(4, 9.5, 16, 11, 3.5, tone=True),
    P("M12 9.5v11M3.5 9.5h17"),
    *ring(9.3, 6.6, 2.1, gap=90, at=60),
    *ring(14.7, 6.6, 2.1, gap=90, at=120),
)

# ---------------------------------------------------------------- media
_add(
    "play",
    "media",
    "start video audio resume",
    P("M9 6.4 18.4 11.3a.8.8 0 0 1 0 1.4L9 17.6a.8.8 0 0 1-1.2-.7V10", tone=True),
)

_add("pause", "media", "stop hold audio video", R(6.5, 6, 3, 12, 1.5, tone=True), R(14.5, 6, 3, 12, 1.5, tone=True))

_add(
    "camera",
    "media",
    "photo picture capture",
    P(
        "M15.8 6.5h1.7a3 3 0 0 1 3 3v7a3 3 0 0 1-3 3h-11a3 3 0 0 1-3-3v-7a3 3 0 0 1 3-3h1.8l1.5-2h4.4l1.1 1.5",
        tone=True,
    ),
    *ring(12, 13, 3.3, gap=60),
    Dot(17.2, 9.8, 1),
)

_add(
    "music",
    "media",
    "audio song note sound",
    P("M9 17.5V5.8l11-2.3v11.7"),
    C(6.5, 17.5, 2.5, tone=True),
    C(17.5, 15.2, 2.5, tone=True),
    P("M9 9.3l11-2.3"),
)

_add(
    "volume",
    "media",
    "sound speaker audio loud",
    P("M4 9.5A1 1 0 0 1 5 8.5h3l4.4-3.6a.6.6 0 0 1 1 .5v13.2a.6.6 0 0 1-1 .5L8 15.5H5a1 1 0 0 1-1-1Z", tone=True),
    P("M16.5 9a4.2 4.2 0 0 1 0 6M19 6.5a8 8 0 0 1 0 11"),
)

_add(
    "mic",
    "media",
    "microphone record voice",
    *open_rect(8.5, 3, 7, 11.5, 3.5, tone=True),
    P("M5 11a7 7 0 0 0 14 0M12 18v3"),
)

_add(
    "video", "media", "camera film record", *open_rect(2.5, 6.5, 12.5, 11, 2.5, tone=True), P("M17.5 12 21.5 8.2v7.6Z")
)

# ---------------------------------------------------------------- weather & nature
_add(
    "sun",
    "nature",
    "light day bright weather",
    *ring(12, 12, 4.6, gap=60, tone=True),
    P(rays_path(r1=7.6, r2=9, count=8, offset=0.3927)),
)

_add(
    "moon", "nature", "night dark mode sleep", P("M19.8 14.6A8.2 8.2 0 1 1 9.4 4.2a6.6 6.6 0 0 0 10.4 10.4Z", tone=True)
)

_add(
    "cloud",
    "nature",
    "weather sky storage",
    P("M7 19a4.5 4.5 0 0 1-.7-8.95A6 6 0 0 1 17.8 9.2 4.9 4.9 0 0 1 17 19Z", tone=True),
)

_add(
    "zap",
    "nature",
    "lightning bolt power energy flash",
    P("M14.2 2.8 6.3 12.6h11.4L9.8 21.2"),
    P("M14.2 2.8 6.3 12.6h11.4L9.8 21.2Z", tone_only=True),
)

_add(
    "leaf",
    "nature",
    "eco plant green nature",
    P("M5 19C4 11 9 4.5 19.5 4.5 19.5 15 13 20 5 19Z", tone=True),
    P("M5 19c3-4.5 6-7.5 10-10"),
)

_add(
    "droplet",
    "nature",
    "water liquid rain humidity",
    P("M12 3.5s6.5 6.6 6.5 11a6.5 6.5 0 0 1-13 0c0-4.4 6.5-11 6.5-11Z", tone=True, rotate=15, about=(12, 14)),
    P("M9 15a3 3 0 0 0 2.2 2.8", rotate=15, about=(12, 14)),
)

_add(
    "flame",
    "nature",
    "fire hot trending",
    P(
        "M12 21a6.5 6.5 0 0 1-6.5-6.5c0-3.4 2.4-5.4 3.6-8 .8 1.7 1.5 2.6 2.6 3.2.2-3 1.7-5.6 3.8-7 0 3.7 3 5.6 3 10.3A6.5 6.5 0 0 1 12 21Z",
        tone=True,
    ),
    P("M10 17.5a2.3 2.3 0 0 0 4-1.8c0-1.4-1.1-2.2-2-3.5-.9 1.3-2 2-2 3.5"),
)

_add(
    "sparkles",
    "nature",
    "ai magic new shine sparkle",
    P("M10 3.5c.6 3.6 2.4 5.4 6 6-3.6.6-5.4 2.4-6 6-.6-3.6-2.4-5.4-6-6 3.6-.6 5.4-2.4 6-6Z", tone=True),
    P("M17.5 14c.3 1.8 1.2 2.7 3 3-1.8.3-2.7 1.2-3 3-.3-1.8-1.2-2.7-3-3 1.8-.3 2.7-1.2 3-3Z", tone=True),
)

# ---------------------------------------------------------------- places & time
_add(
    "map-pin",
    "places",
    "location marker place address",
    P("M12 21s6.5-5.7 6.5-11a6.5 6.5 0 0 0-13 0c0 5.3 6.5 11 6.5 11Z", tone=True),
    C(12, 10, 2.5),
)

_add(
    "globe",
    "places",
    "world earth internet language",
    *ring(12, 12, 8.5, gap=70, tone=True),
    P("M3.5 12h17M12 3.5c2.3 2.4 3.4 5.2 3.4 8.5s-1.1 6.1-3.4 8.5c-2.3-2.4-3.4-5.2-3.4-8.5S9.7 5.9 12 3.5Z"),
)

_add(
    "compass",
    "places",
    "navigate explore direction",
    *ring(12, 12, 8.5, gap=70),
    P("M15.3 8.7 13.3 13.3 8.7 15.3 10.7 10.7Z", tone=True),
    Dot(12, 12, 0.9),
)

_add(
    "calendar",
    "places",
    "date schedule event month",
    *open_rect(3.5, 5, 17, 15.5, 4, tone=True),
    P("M3.5 10.2h17M8.5 3.2v3.6M14.3 3.2v3.6"),
    Dot(8.2, 14, 1.05),
    Dot(12, 14, 1.05),
    Dot(15.8, 14, 1.05),
    Dot(8.2, 17.3, 1.05),
    Dot(12, 17.3, 1.05),
)

_add("clock", "places", "time watch hour schedule", *ring(12, 12, 8.5, gap=70, tone=True), P("M12 7.6v4.4h3.4"))

_add(
    "bookmark",
    "places",
    "save mark read later",
    P("M14.4 3.5H10A3.5 3.5 0 0 0 6.5 7V20.5L12 16.5l5.5 4V7.6", tone=True),
)

_add(
    "flag",
    "places",
    "report milestone goal",
    P("M5.5 21V3.5"),
    P("M5.5 4.5h12.3a.6.6 0 0 1 .5.95L15.6 9l2.7 3.55a.6.6 0 0 1-.5.95H5.5", tone=True, rotate=10, about=(5.5, 4.5)),
)

# ---------------------------------------------------------------- dev & data
_add(
    "code",
    "dev",
    "brackets develop programming html",
    P(swept_head(3.8, 12, -1, 0, 0.75)),
    P(swept_head(20.2, 12, 1, 0, 0.75)),
    P("M13.2 6.5 10.8 17.5"),
)

_add(
    "terminal",
    "dev",
    "console shell command prompt",
    *open_rect(3.5, 5.5, 17, 13, 4, tone=True),
    P("M7.5 9.8l2.6 2.4-2.6 2.4M12.5 15h4"),
)

_add(
    "database",
    "dev",
    "storage sql data server",
    *open_rect(4, 3.5, 16, 5, 2.5, tone=True),
    R(4, 10.5, 16, 5, 2.5),
    R(4, 17.5, 16, 3.5, 1.75),
)

_add(
    "server",
    "dev",
    "hosting rack backend",
    *open_rect(3.5, 3.5, 17, 7.5, 3, tone=True),
    R(3.5, 13, 17, 7.5, 3),
    P("M7 7.25h5M7 16.75h5"),
    Dot(16.5, 7.25, 1.1),
    Dot(16.5, 16.75, 1.1),
)

_add(
    "cpu",
    "dev",
    "chip processor hardware",
    *open_rect(5.5, 5.5, 13, 13, 4, tone=True),
    *ring(12, 12, 2.5, gap=70),
    P("M9.5 2.9v2.6M14.5 2.9v2.6M9.5 18.5v2.6M14.5 18.5v2.6M2.9 9.5h2.6M2.9 14.5h2.6M18.5 9.5h2.6M18.5 14.5h2.6"),
)

_add(
    "git-branch",
    "dev",
    "version control merge fork",
    C(6.5, 5.5, 2.3),
    C(6.5, 18.5, 2.3),
    C(17.5, 7.5, 2.3, tone=True),
    P("M6.5 7.8v8.4"),
    P("M17.5 9.8c0 4-4 4.2-8 5.6"),
)

_add(
    "wifi",
    "dev",
    "wireless internet signal network",
    P("M4.6 9.4a10.6 10.6 0 0 1 14.8 0M7.4 12.6a6.5 6.5 0 0 1 9.2 0"),
    Dot(12, 16.8, 1.5),
)

_add(
    "battery",
    "dev",
    "power charge energy level",
    *open_rect(2.5, 7, 16, 10, 3.5, tone=True),
    P("M6.3 10.2v3.6M9.5 10.2v3.6M12.7 10.2v3.6M21.3 10.7v2.6"),
)

_add(
    "bar-chart",
    "dev",
    "analytics stats graph metrics",
    R(4, 12, 4, 8, 1.2, tone=True),
    R(10, 4, 4, 16, 1.2),
    R(16, 8.5, 4, 11.5, 1.2, tone=True),
)

_add(
    "trending-up",
    "dev",
    "growth increase chart rise",
    P("M3 17.5l5.5-5.5 4 4 5.3-5.3"),
    P(swept_head(20, 7.5, 1, -1, 0.7)),
)

_add(
    "shield",
    "dev",
    "security protection safe privacy",
    P("M15.6 4.5 19 5.8v5.7c0 4.4-2.9 7.6-7 9.2-4.1-1.6-7-4.8-7-9.2V5.8L12 3.2l1.4.5", tone=True),
)

_add(
    "shield-check",
    "dev",
    "security verified audit trail evidence compliance protected",
    P("M15.6 4.5 19 5.8v5.7c0 4.4-2.9 7.6-7 9.2-4.1-1.6-7-4.8-7-9.2V5.8L12 3.2l1.4.5", tone=True),
    P("M8.8 11.8l1.8 1.8", rotate=-12),
    P("M12.5 13.3l3-3.4", rotate=-12),
)

_add(
    "key",
    "dev",
    "password access auth credential",
    C(8, 15, 4.5, tone=True),
    P("M11.2 11.8 19.5 3.5M16.5 6.5l2.5 2.5M14 9l2 2"),
)


# ---------------------------------------------------------------- app & governance
_add(
    "dashboard",
    "interface",
    "overview gauge meter speed summary metrics",
    *ring(12, 13.2, 8.5, gap=100, at=90, tone=True),
    P("M12 13.2l3.4-3.9"),
    Dot(12, 13.2, 1.5),
)

_add(
    "bot",
    "dev",
    "ai robot assistant agent model automation",
    R(4.5, 8, 15, 12, 3.5, tone=True),
    P("M12 8V5.6"),
    Dot(12, 4, 1.5),
    P("M2.5 12.5v3.5M21.5 12.5v3.5"),
    Dot(9.3, 13, 1.35),
    Dot(14.7, 13, 1.35),
    P("M10.2 16.6a2.6 2.6 0 0 0 3.6 0"),
)

_add(
    "clipboard-check",
    "files",
    "assessment checklist task done audit review",
    P("M8.5 5.5H8A4 4 0 0 0 4 9.5v7.5a4 4 0 0 0 4 4h8a4 4 0 0 0 4-4V9.5a4 4 0 0 0-2.2-3.32"),
    R(8.5, 3.5, 7, 3.8, 1.9, tone=True),
    P("M8.3 14.3l1.9 1.9", rotate=10),
    P("M12.1 15.8l3.2-3.8", rotate=10),
)

_add(
    "file-search",
    "files",
    "findings review inspect find document lookup",
    P("M13.0 3.5H8.5A3 3 0 0 0 5.5 6.5V17.5A3 3 0 0 0 8.5 20.5H15.5A3 3 0 0 0 18.5 17.5V9.0Z", tone_only=True),
    P("M10 20.5H8.5A3 3 0 0 1 5.5 17.5V6.5A3 3 0 0 1 8.5 3.5H13L18.5 9v1.5"),
    *ring(15, 15.2, 2.9, gap=70),
    P("M17.2 17.5l2.8 2.8"),
)

_add(
    "library",
    "files",
    "books requirements reference shelf catalog standards",
    R(3.5, 4, 4.5, 16.5, 1.6, tone=True),
    R(10.5, 7, 4.5, 13.5, 1.6),
    P("M16.6 20.2 19 7.6l2.6.5-2.4 12.6Z", tone=True),
)

_add(
    "compare-arrows",
    "arrows",
    "change impact diff git swap exchange versions",
    *ring(5.5, 7.5, 2.2, gap=80, tone=True),
    *ring(18.5, 16.5, 2.2, gap=80, tone=True),
    P(swept_arrow(9, 7.5, 19.5, 7.5, size=0.55)),
    P(swept_arrow(15, 16.5, 4.5, 16.5, size=0.55)),
)

_add(
    "activity",
    "dev",
    "pulse monitoring heartbeat health signal metrics live",
    P("M2.5 12.5H6l2.2-4 3 10.5 3.3-15 2.6 8.5h4.4"),
)

_add(
    "plug",
    "dev",
    "integrations connect power plugin socket",
    P("M9.5 3.5v4M14.5 3.5v4"),
    R(6, 7.5, 12, 6.5, 2.5, tone=True),
    P("M9.5 14v1a2.5 2.5 0 0 0 5 0v-1"),
    P("M12 17.5V19a2 2 0 0 0 2 2h4.5"),
)

_add(
    "file-down",
    "files",
    "export download document pack save",
    P("M13.0 3.5H8.5A3 3 0 0 0 5.5 6.5V17.5A3 3 0 0 0 8.5 20.5H15.5A3 3 0 0 0 18.5 17.5V9.0Z", tone=True),
    P(swept_arrow(12, 10, 12, 17.2, size=0.5)),
)

_add(
    "badge-info",
    "interface",
    "notice information banner seal sample alert",
    R(4.25, 4.25, 15.5, 15.5, 3.8, tone=True, rotate=15),
    P("M12 11.2v4.6h1.2"),
    Dot(12, 8.4, 1.15),
)

_add(
    "calendar-clock",
    "places",
    "schedule reassessment due deadline recurring time",
    P("M20.5 10.2V9a4 4 0 0 0-4-4H7.5a4 4 0 0 0-4 4v7.5a4 4 0 0 0 4 4h3"),
    P("M3.5 10.2h7.5M8.5 3.2v3.6M14.3 3.2v3.6"),
    *ring(16.5, 16.5, 4.3, gap=70, tone=True),
    P("M16.5 14.6v2l1.4 1"),
)


def _alias(alias, target):
    assert target in _ICONS and alias not in _ICONS
    _ALIASES[alias] = target


# Alternative names, so common spellings resolve to Pyramz icons.
_alias("layout-dashboard", "grid")
_alias("gauge", "dashboard")
_alias("git-compare-arrows", "compare-arrows")
_alias("circle-check", "check-circle")
_alias("circle-x", "x-circle")
_alias("circle-help", "help-circle")
_alias("triangle-alert", "alert-triangle")
_alias("ellipsis", "more-horizontal")
_alias("ellipsis-vertical", "more-vertical")
_alias("shopping-cart", "cart")
_alias("pencil", "edit")
_alias("trash-2", "trash")
_alias("message-square", "message")
_alias("smartphone", "phone")


def aliases() -> dict[str, str]:
    return _ALIASES


def registry() -> dict[str, IconDef]:
    return _ICONS
