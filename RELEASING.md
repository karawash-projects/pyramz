# Releasing

## One-time setup

The repository is [karawash-projects/pyramz](https://github.com/karawash-projects/pyramz).

1. **GitHub Pages:** in Settings → Pages, set Source to **GitHub Actions**. The gallery deploys on every push to `main` that touches the package.
2. **Private vulnerability reporting:** in Settings → Security, turn on **Private vulnerability reporting**.
3. **Environment:** in Settings → Environments, create one named `pypi`. Optionally require your approval before each publish.
4. **PyPI Trusted Publishing** (no API tokens needed). Sign in to PyPI and go to **Your account → Publishing → Add a new pending publisher**, then enter:
   - PyPI project name: `pyramz`
   - Owner: `karawash-projects`
   - Repository: `pyramz`
   - Workflow name: `release.yml`
   - Environment: `pypi`

## Each release

1. Make sure CI on `main` is green.
2. Bump `__version__` in `src/pyramz/__init__.py`. It's the only place the version lives.
3. Move the **Unreleased** entries in `CHANGELOG.md` under a new version heading, and update the compare links.
4. Commit, push, then create a GitHub Release with the tag `vX.Y.Z` (for example `v0.4.0`, the first public release). Paste the changelog section into the release notes.
5. The **Release** workflow builds the package, checks that the tag matches `__version__`, and publishes to PyPI.

To try the process first, run `python -m build && twine check dist/*` locally. You can also upload to [TestPyPI](https://test.pypi.org) with `twine upload -r testpypi dist/*`.
