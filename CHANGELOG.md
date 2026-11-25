# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses [Semantic Versioning](https://semver.org/). Before 1.0, minor versions may rename or redraw icons; such changes are always listed here.

## [Unreleased]

## [0.4.0] - 2026-11-25

First public release.

### Added
- Original icons on a 24×24 grid, in outline and duotone styles with round or sharp corners.
- `pyramz.icon()` with size, colour, stroke width, accent colour and opacity, absolute stroke, accessible titles, CSS classes and custom SVG attributes.
- `Icon` objects that render in Jinja2, Django and Jupyter, and save as SVG, data URIs or PNG (`pyramz[png]`).
- `names()`, `categories()`, `search()`, `info()`, `aliases()`, `set_defaults()`, `reset_defaults()`, `sprite()`, `register()` and attribute access via `pyramz.icons`.
- The `pyramz` command-line tool: `list`, `search`, `show`, `export`, `sprite` and `gallery`.

[Unreleased]: https://github.com/karawash-projects/pyramz/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/karawash-projects/pyramz/releases/tag/v0.4.0
