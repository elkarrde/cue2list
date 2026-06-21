# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - unreleased

### Changed
- Install instructions now use `pipx install cue2list` from PyPI as the primary
  method, with the `git+` repo URL kept as a "latest from source" alternative.

## [1.0.0] - 2026-06-21

First public release, [published to PyPI](https://pypi.org/project/cue2list/).

### Added
- CLI to parse CD Audio CUE sheets (`.cue`) into a Markdown or plain-text tracklist.
- Packaging metadata (`pyproject.toml`) with the `cue2lst` console-script entry point.
- Single-source version via `cue2lst.__version__`.
- `curl` single-file and `pipx`/`pip` installation paths.
- MPL-2.0 license.

[1.0.1]: https://codeberg.org/elkarrde/Cue2List/compare/v1.0.0...HEAD
[1.0.0]: https://codeberg.org/elkarrde/Cue2List/releases/tag/v1.0.0
