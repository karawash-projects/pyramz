# Pyramz

[![PyPI](https://img.shields.io/pypi/v/pyramz)](https://pypi.org/project/pyramz/)
[![Python versions](https://img.shields.io/pypi/pyversions/pyramz)](https://pypi.org/project/pyramz/)
[![CI](https://github.com/karawash-projects/pyramz/actions/workflows/ci.yml/badge.svg)](https://github.com/karawash-projects/pyramz/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue)](https://github.com/karawash-projects/pyramz/blob/main/LICENSE)

Original SVG icons for Python, in outline and duotone styles with round or sharp corners.

Pyramz returns clean, accessible SVG markup for web pages, templates, notebooks and files. It has no dependencies and supports Python 3.9+. Browse every icon in the [gallery](https://karawash-projects.github.io/pyramz/).

## Installation

```bash
pip install pyramz
```

PNG export is optional: `pip install "pyramz[png]"`.

## Usage

```python
import pyramz

pyramz.icon("home")
pyramz.icon("bell", size=32, stroke_width=1.5)
pyramz.icon("heart", style="duotone", accent="#e11d48")
pyramz.icon("folder", corners="sharp")
pyramz.icon("search", title="Search")  # accessible label

pyramz.search("money")  # find icons by name or tag
pyramz.set_defaults(stroke_width=2)  # project-wide defaults
```

`pyramz.icon()` returns an `Icon` that behaves like a string of SVG markup. It renders directly in Jinja2 and Django templates (no `|safe` needed) and in Jupyter, and it can be saved with `.save("home.svg")`, `.to_data_uri()` or `.to_png("home.png")`.

### Options

| Option | Default | Description |
|---|---|---|
| `size` | `24` | Width and height: a number or a CSS length |
| `color` | `"currentColor"` | Stroke colour |
| `stroke_width` | `1.75` | Stroke width in grid units |
| `style` | `"outline"` | `"outline"` or `"duotone"` |
| `accent` | same as `color` | Duotone tint colour |
| `accent_opacity` | `0.22` | Duotone tint opacity |
| `corners` | `"round"` | `"round"` or `"sharp"` |
| `absolute_stroke` | `False` | Keep the stroke the same width in pixels at any size |
| `title` | `None` | Accessible label; leave it out for decorative icons |
| `class_` | `None` | Extra CSS classes |

Any other keyword becomes an SVG attribute, with underscores turned into dashes (`data_testid="x"` → `data-testid="x"`).

### More

- `pyramz.names()`, `pyramz.categories()` and `pyramz.info(name)` list and describe icons.
- `pyramz.icons.arrow_right()` gives attribute access with tab completion.
- `pyramz.sprite([...])` builds an SVG sprite sheet for `<use href="#pyramz-home"/>`.
- `pyramz.register(name, paths)` adds your own icons.

## Command line

```bash
pyramz list
pyramz search arrow
pyramz show heart --style duotone
pyramz export -o svg/ --size 32
pyramz gallery -o gallery.html
```

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](https://github.com/karawash-projects/pyramz/blob/main/CONTRIBUTING.md).

## License

Licensed under the [Apache License, Version 2.0](https://github.com/karawash-projects/pyramz/blob/main/LICENSE).
