# Future

Longer-horizon ideas, not yet scheduled.

## Structured data output formats (JSON / YAML / CSV)

The current formats (`md`, `txt`) are **presentation** formats — flattened,
human-readable, and they deliberately discard data (per-track INDEX timestamps,
FILE directives, etc.). A structured format would instead let other programs
consume the parsed CUE, preserving the fields the human formats throw away. This
turns cue2list into a CUE-to-structured-data converter, which is a genuinely
different (and more valuable) use case than another presentation skin.

Ranked plan:

1. **JSON** — highest value, lowest cost. Zero dependencies (stdlib `json`), the
   universal target for piping into other tools/scripts. Add this first.
2. **YAML** — worthwhile only if humans are expected to hand-edit the output
   (YAML's main edge over JSON). Pulls in `PyYAML` as a runtime dependency, which
   is a real tradeoff for a currently dependency-free tool on PyPI. For pure
   machine consumption, JSON already covers it.
3. **CSV** — niche but trivial (stdlib `csv`); handy for spreadsheets. Add if
   asked.

Skip: XML (verbose, no audience), TOML (awkward for lists of tracks).

**Structural prerequisite:** `format_output()` currently uses an `if/elif` chain
with the track-formatting loop duplicated between `md` and `txt`. Before adding
more branches, refactor to a dispatch table
(`{"md": _format_md, "json": _format_json, ...}`) plus a shared "flatten sheet to
tracks" step. The structured formats need the full track data (index, file), so
they should serialize the `Cuesheet`/`Track` objects directly rather than reuse
the presentation loop.

Recommended first step: add **JSON only** (no new deps) together with the
dispatch-table refactor.
