# Cue2List
---

Converts Cuefile (`.cue`) to Markdown list (`.md`) or text list (`.txt`).

Usage: `python3 cue2lst.py <cuefile> <output_format> [--verbose]`

- **cuefile**: cuefile `.cue`,
- **output_format**: `md` or `txt`,
- **verbose**: switch, if used, tracklist will be displayed.

## Install

Pure Python 3 standard library — no third-party dependencies.

### Option A — install as a command with pipx

Installs into an isolated environment and puts a `cue2lst` command on your `$PATH`:

```bash
pipx install cue2list
cue2lst album.cue md
```

To install the latest development version straight from the repo instead:

```bash
pipx install git+https://codeberg.org/elkarrde/Cue2List
```

(Use `pip install ...` instead of `pipx` if you prefer installing into the current environment.)

### Option B — grab the single file (no install)

The whole tool is one self-contained script. Download it and run:

```bash
curl -O https://codeberg.org/elkarrde/Cue2List/raw/branch/master/cue2lst.py
python3 cue2lst.py album.cue md
```

Or drop it on your `$PATH` as a command (it has a shebang and is executable):

```bash
curl -o ~/.local/bin/cue2lst https://codeberg.org/elkarrde/Cue2List/raw/branch/master/cue2lst.py
chmod +x ~/.local/bin/cue2lst
cue2lst album.cue md
```

----

- Website: [iso3200.net/cue2list](https://iso3200.net/cue2list/)
- Main repo: [Codeberg](https://codeberg.org/elkarrde/Cue2List)
- Mirror: [GitHub](https://github.com/elkarrde/cue2list)
