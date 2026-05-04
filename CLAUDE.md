# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

`cue2list` is a single-file Python 3 CLI tool (`cue2lst.py`) that parses CD Audio CUE sheet files (`.cue`) and outputs a formatted tracklist as Markdown or plain text.

## Running

```bash
python3 cue2lst.py <cuefile> <output_format> [--verbose]
# output_format: md or txt
# --verbose: prints disc performer, title, track count, and all tracks to stdout
```

Output is written to a file with the same base name as the input but with the new extension (e.g. `beck.cue` → `beck.md`).

Example CUE files are in `examples/`.

## Architecture

All logic lives in `cue2lst.py`. The flow is:

1. `parse_cue_file()` — reads the `.cue` file line-by-line. It first feeds lines into a `Cuesheet` until `header_complete()` is true (either PERFORMER+TITLE found, or a FILE directive is seen), then feeds remaining lines into a `Track` instance, flushing completed tracks into the sheet via `add_track()`.
2. `format_output()` — renders the `Cuesheet` (and its `Track` list) into a string. Per-track PERFORMER falls back to disc-level PERFORMER when absent.
3. `main()` — CLI argument parsing, writes the output file. Note: `import os` is deferred to inside `main()`.

**Known design quirk**: `Cuesheet.tracks = []` is declared at class level, which means all instances share the list unless a fresh list is assigned per instance. This works in practice because only one `Cuesheet` is created per run.

**Track length**: `include_length` (which would append the INDEX timestamp to each track line) is intentionally disabled — the last track's length cannot be calculated from a CUE file alone since no end-time is present.

## CUE format handled

```
PERFORMER "Artist"
TITLE "Album"
FILE "CDImage.wav" WAVE
  TRACK 01 AUDIO
    TITLE "Song"
    PERFORMER "Artist"       ← optional per-track override
    INDEX 01 00:00:00
```

Only `AUDIO` track types are parsed. The INDEX timestamp format is `MM:SS:FF` (frames).
