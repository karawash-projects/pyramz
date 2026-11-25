import re
import xml.etree.ElementTree as ET

import pytest

import pyramz
from pyramz._registry import registry
from pyramz.cli import main

SVG = "{http://www.w3.org/2000/svg}"


@pytest.fixture(autouse=True)
def _reset():
    pyramz.reset_defaults()
    yield
    pyramz.reset_defaults()


@pytest.mark.parametrize("name", pyramz.names())
@pytest.mark.parametrize("style", ["outline", "duotone"])
@pytest.mark.parametrize("corners", ["round", "sharp"])
def test_every_icon_is_valid_svg(name, style, corners):
    root = ET.fromstring(str(pyramz.icon(name, style=style, corners=corners)))
    assert root.tag == SVG + "svg"
    assert root.get("viewBox") == "0 0 24 24"
    assert len(list(root)) >= 1


@pytest.mark.parametrize("name", pyramz.names())
def test_icons_stay_inside_grid(name):
    body = str(pyramz.icon(name)).split(">", 1)[1]
    body = re.sub(r'transform="[^"]*"', "", body)  # rotation angles are not coordinates
    nums = [float(n) for n in re.findall(r"-?\d*\.?\d+", body)]
    # absolute coordinates in our artwork never exceed the 24px canvas
    assert max(nums) <= 24 and min(nums) >= -24


@pytest.mark.parametrize("name", pyramz.names())
def test_every_icon_has_a_duotone_layer_or_is_line_only(name):
    d = registry()[name]
    toned = any(s.tone or s.tone_only for s in d.shapes)
    duo = str(pyramz.icon(name, style="duotone"))
    assert ("fill-opacity" in duo) == toned


def test_options_are_applied():
    s = str(pyramz.icon("home", size=40, color="#f00", stroke_width=2, class_="nav", data_testid="h"))
    assert 'width="40"' in s and 'stroke="#f00"' in s and 'stroke-width="2"' in s
    assert 'class="pyramz pyramz-home nav"' in s and 'data-testid="h"' in s


def test_duotone_accent():
    s = str(pyramz.icon("heart", style="duotone", accent="#e11d48", accent_opacity=0.3))
    assert 'fill="#e11d48"' in s and 'fill-opacity="0.3"' in s


def test_absolute_stroke():
    assert 'stroke-width="1"' in str(pyramz.icon("x", size=48, stroke_width=2, absolute_stroke=True))


def test_accessibility():
    plain = str(pyramz.icon("bell"))
    assert 'aria-hidden="true"' in plain
    titled = str(pyramz.icon("bell", title="Notifications"))
    assert 'role="img"' in titled and "<title" in titled and "aria-hidden" not in titled


def test_title_is_escaped():
    assert "&lt;script&gt;" in str(pyramz.icon("x", title="<script>"))


def test_unknown_icon_suggests():
    with pytest.raises(KeyError, match="home"):
        pyramz.icon("hom")


def test_name_normalisation_and_namespace():
    assert pyramz.icon("arrow_right") == pyramz.icon("Arrow Right") == pyramz.icons.arrow_right()
    assert "arrow_right" in dir(pyramz.icons)


def test_search_ranks_names_then_tags():
    assert pyramz.search("arrow")[0].startswith("arrow")
    assert "trash" in pyramz.search("delete")
    assert pyramz.search("") == []


def test_defaults():
    pyramz.set_defaults(stroke_width=1.25, style="duotone")
    s = str(pyramz.icon("star"))
    assert 'stroke-width="1.25"' in s and "fill-opacity" in s
    with pytest.raises(TypeError):
        pyramz.set_defaults(bogus=1)


def test_register_custom_icon():
    pyramz.register("custom-tri", ["M12 4 20 19H4Z"], tone=[0], tags=["triangle"])
    assert "custom-tri" in pyramz.names("custom")
    assert "fill-opacity" in str(pyramz.icon("custom-tri", style="duotone"))
    with pytest.raises(ValueError):
        pyramz.register("home", ["M0 0"])


def test_html_and_jupyter_protocols():
    ic = pyramz.icon("sun")
    assert ic.__html__() == ic._repr_svg_() == str(ic)
    assert ic.to_data_uri().startswith("data:image/svg+xml;base64,")


def test_sprite():
    s = pyramz.sprite(["home", "user"])
    ET.fromstring(s)
    assert 'id="pyramz-home"' in s and 'id="pyramz-user"' in s


def test_bad_options():
    with pytest.raises(ValueError):
        pyramz.icon("x", style="filled")
    with pytest.raises(ValueError):
        pyramz.icon("x", corners="soft")


def test_cli(tmp_path, capsys):
    assert main(["search", "money"]) == 0
    assert "wallet" in capsys.readouterr().out
    assert main(["export", "home", "mail", "-o", str(tmp_path)]) == 0
    assert (tmp_path / "home.svg").exists()
    assert main(["gallery", "-o", str(tmp_path / "g.html")]) == 0
    assert main(["show", "nope"]) == 2


APP_ICONS = [
    "layout-dashboard",
    "bot",
    "clipboard-check",
    "file-search",
    "library",
    "git-compare-arrows",
    "activity",
    "shield-check",
    "file-text",
    "plug",
    "users",
    "play",
    "file-down",
    "badge-info",
    "circle-check",
    "calendar-clock",
]


@pytest.mark.parametrize("name", APP_ICONS)
def test_alias_names_resolve(name):
    s = str(pyramz.icon(name, size=20, stroke_width=2))
    root = ET.fromstring(s)
    assert root.get("stroke-width") == "2" and root.get("stroke-linecap") == "round"
    assert root.get("stroke-linejoin") == "round" and root.get("fill") == "none"


def test_aliases_point_at_real_icons():
    for alias, target in pyramz.aliases().items():
        assert pyramz.icon(alias) == pyramz.icon(target)
        assert alias not in pyramz.names()
    assert pyramz.search("circle-check")[0] == "check-circle"


def test_markup_injection_is_escaped():
    evil = '"><script>alert(1)</script>'
    for svg in (
        str(pyramz.icon("home", color=evil, style="duotone", accent=evil, class_=evil, title=evil)),
        pyramz.sprite(["home"], color=evil),
    ):
        assert "<script>" not in svg
        ET.fromstring(svg)
    with pytest.raises(ValueError):
        pyramz.icon("home", **{'x" onload="alert(1)': 1})
    with pytest.raises(ValueError):
        pyramz.icon("home", style="duotone", accent_opacity='1" onload="x')


def test_fuzzy_search_is_only_a_fallback():
    assert pyramz.search("audit") == ["clipboard-check", "shield-check"]
    assert "settings" in pyramz.search("setings")  # typo still finds it


@pytest.mark.parametrize("name", pyramz.names())
def test_rendered_ink_stays_on_canvas(name):
    """Render at 96px (4px per grid unit) at stroke 2 and check that nothing,
    including rotated parts, spills outside the 0.5..23.5 grid area."""
    import io

    try:
        import cairosvg
        from PIL import Image as pil
    except (ImportError, OSError):  # cairosvg needs the Cairo C library
        pytest.skip("cairosvg/Cairo not available")

    svg = str(pyramz.icon(name, size=96, stroke_width=2, color="#000"))
    img = pil.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert("RGBA")
    alpha = img.getchannel("A")
    left, top, right, bottom = alpha.point(lambda a: 255 if a > 64 else 0).getbbox()
    assert left >= 2 and top >= 2 and right <= 94 and bottom <= 94, (name, (left, top, right, bottom))


# --- sharp corners -----------------------------------------------------------
from pyramz._paths import corner_arcs, sharpen, to_absolute  # noqa: E402


def test_path_parser_handles_relative_and_compact_syntax():
    segs = to_absolute("M1 2h3v4l-1-1a2 2 0 0 0 2 2c1 0 1 1 2 2s1 1 2 0Z")
    assert [c for c, _ in segs] == ["M", "L", "L", "L", "A", "C", "C", "Z"]
    assert segs[1][1] == [4, 2] and segs[2][1] == [4, 6] and segs[3][1] == [3, 5]
    assert segs[4][1][-2:] == [5, 7]
    assert to_absolute("M.5.5l.5-.5")[1][1] == [1, 0]


def test_sharpen_tightens_quarter_corners_only():
    box = "M8 3H5.5A2.5 2.5 0 0 0 3 5.5V18"
    assert corner_arcs(box) == 1
    sharp = sharpen(box)
    assert "A0.75 0.75 0 0 0 3 3.75" in sharp and sharp.startswith("M8 3L5.5 3L3.75 3")
    assert sharpen(sharp) == sharp  # idempotent
    ring_arc = "M19.55 7.1A9 9 0 1 1 15.52 3.72"  # a large arc, not a corner
    assert sharpen(ring_arc) == ring_arc


@pytest.mark.parametrize("name", pyramz.names())
def test_sharp_mode_is_valid_and_keeps_corners_tight(name):
    root = ET.fromstring(str(pyramz.icon(name, corners="sharp")))
    assert root.get("stroke-miterlimit") == "4"
    for el in root.iter():
        if el.tag == SVG + "path":
            assert corner_arcs(el.get("d")) == 0, name  # no round box corners left
        if el.tag == SVG + "rect" and el.get("rx"):
            assert float(el.get("rx")) <= 0.75


@pytest.mark.skipif(__import__("sys").platform == "win32", reason="uses a POSIX shell pipe")
def test_cli_survives_closed_pipe():
    import subprocess
    import sys as _sys

    proc = subprocess.run(
        f'"{_sys.executable}" -c "from pyramz.cli import entry; entry()" list | head -n 1',
        shell=True,
        capture_output=True,
        text=True,
    )
    assert "BrokenPipeError" not in proc.stderr
