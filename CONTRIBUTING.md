# Contributing to Pyramz

Thanks for helping. Icon requests, new icons, bug fixes and documentation improvements are all welcome.

## Development setup

```bash
git clone https://github.com/karawash-projects/pyramz.git
cd pyramz
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev,docs]"
pytest
ruff check . && ruff format --check .
```

The `docs` extra installs `cairosvg` and Pillow. These let the test suite render every icon and let you generate preview sheets.

## Adding an icon

Icons live in `src/pyramz/_registry.py` as `_add(name, category, tags, *shapes)` calls. They use these helpers from `src/pyramz/_shapes.py`:

| Helper | Draws |
|---|---|
| `P(d)` | a path (`d` uses 24×24 grid coordinates) |
| `C(cx, cy, r)` | a circle |
| `R(x, y, w, h, rx)` | a rounded rectangle |
| `Dot(cx, cy, r)` | a small filled dot |
| `ring(cx, cy, r)` | a circle with the signature opening |
| `open_rect(x, y, w, h, rx)` | a rounded box with its top-right corner open |
| `swept_arrow(...)`, `swept_head(...)` | arrows and chevrons in the house style |

These options control how a shape renders:

- `tone=True` tints a shape in the duotone style.
- `tone_only=True` makes a backdrop that is filled in duotone but never stroked.
- `rotate=` (in degrees) on `P()` or `R()` tilts a shape.

Draw corners round only, because `corners="sharp"` is derived automatically from the path data.

### Design checklist

- [ ] **Original work.** The artwork must be your own, drawn from the idea rather than copied or traced.
- [ ] **Grid.** 24×24, with content inside the 2–22 area. Tilted parts must stay on the canvas; `pytest -k rendered_ink` checks this.
- [ ] **Pen lift.** Give the icon its one deliberate gap: an open ring, an open box corner, a swept arrowhead or dot terminals.
- [ ] **House geometry.** Inset boxes have soft corners (radius about 4). Rings use radius 8.5 with a 70° opening. Diagonal shapes are tilted 10–30° rather than set at 45°.
- [ ] **Spacing.** Leave at least 3 grid units between parallel strokes so the icon stays clean at stroke 2 and 18px.
- [ ] **Duotone.** If the icon has an enclosed area, mark one meaningful region as `tone`.
- [ ] **Sizes.** Run `python scripts/render_previews.py <your-icon> <a-neighbour>` and check `build/check.png` at 20px and 18px.
- [ ] **Naming.** Use lowercase, hyphenated, noun-first names (`file-search`, `calendar-clock`) and add descriptive `tags` for search.

The tests check that every icon is valid SVG in every style and corner mode, and that sharp mode leaves no rounded box corners.

## Pull requests

- Keep each pull request focused, for example one icon family or one fix.
- For icon changes, attach the `build/check.png` screenshot.
- Add a line under **Unreleased** in `CHANGELOG.md`.
- By contributing, you agree that your contribution is licensed under the project's [Apache License 2.0](LICENSE), and you confirm that you have the right to license it.

## Code of conduct

This project follows the [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before taking part.
