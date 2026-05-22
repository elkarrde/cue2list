---
title: "Cue2List"
date: 2024-01-01
description: "Convert CD Audio CUE sheet files into Markdown or plain text tracklists."
tags: ["python", "cli", "music", "tools"]
---

A small Python 3 CLI that parses CD Audio CUE sheet files (`.cue`) and outputs a formatted tracklist as Markdown or plain text.

## Usage

```bash
python3 cue2lst.py <cuefile> <output_format> [--verbose]
```

| Argument | Description |
|---|---|
| `cuefile` | Path to the `.cue` file |
| `output_format` | `md` for Markdown, `txt` for plain text |
| `--verbose` | Print disc info and full tracklist to stdout |

Output is written as a new file with the same base name as the input — for example, `beck.cue` becomes `beck.md`.

## Example

Given a CUE file like:

```
PERFORMER "Beck"
TITLE "Odelay"
FILE "CDImage.wav" WAVE
  TRACK 01 AUDIO
    TITLE "Loser"
    INDEX 01 00:00:00
  TRACK 02 AUDIO
    TITLE "Fuckin' With My Head"
    INDEX 01 03:54:53
```

Running:

```bash
python3 cue2lst.py odelay.cue md
```

Produces `odelay.md`:

```markdown
# Beck: Odelay

1. Loser - Beck
2. Fuckin' With My Head - Beck
```

## CUE format supported

The parser handles standard CD Audio CUE sheets with `PERFORMER`, `TITLE`, and `FILE` header fields, and per-track `TITLE`, `PERFORMER`, and `INDEX` directives. Only `AUDIO` track types are parsed. Per-track `PERFORMER` overrides the disc-level one when present.

## Installation

No dependencies beyond the Python 3 standard library. Clone the repository and run directly:

```bash
git clone https://codeberg.org/elkarrde/Cue2List
cd Cue2List
python3 cue2lst.py examples/beck.cue md
```

## Source

- Main repo: [Codeberg](https://codeberg.org/elkarrde/Cue2List)
- Mirror: [GitHub](https://github.com/elkarrde/cue2list)
