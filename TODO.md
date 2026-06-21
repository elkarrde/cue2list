# TODO

Future ideas, no particular priority.

- **Add a `Makefile` to automate the PyPI release flow.** Wrap the manual steps
  (`rm -rf dist/` → `python -m build` → `twine check dist/*` → `twine upload dist/*`
  → `git tag` + `git push --tags`) behind targets like `build`, `check`, `publish`,
  `clean`, and `tag`. Single-source the version from `cue2lst.__version__`. Needs
  `twine >= 6.1` (older twine chokes on the Metadata-Version 2.4 that the MPL-2.0
  SPDX license expression produces).
