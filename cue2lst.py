#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import os
import sys
import re
from copy import copy
from typing import Tuple, Optional

__version__ = "1.0.1"


class Track:
    _RE_TRACK = re.compile(r'^\s*TRACK\s+(\d+)\s+AUDIO$')
    _RE_TITLE = re.compile(r'^\s*TITLE\s+"(.*?)"$')
    _RE_PERFORMER = re.compile(r'^\s*PERFORMER\s+"(.*?)"$')
    _RE_INDEX = re.compile(r'^\s*INDEX\s+\d+\s+(.+)$')

    def __init__(self, track_num: Optional[str] = None, title: Optional[str] = None,
                 performer: Optional[str] = None, index: Optional[str] = None):
        self.track_num = int(track_num) if track_num else None
        self.title = title
        self.performer = performer
        self.index = index

    def parseline(self, line):
        m = self._RE_TRACK.search(line)
        if m:
            self.track_num = int(m.group(1))
            self.title = None
            self.performer = None
            self.index = None
            return
        m = self._RE_TITLE.search(line)
        if m:
            self.title = m.group(1)
            return
        m = self._RE_PERFORMER.search(line)
        if m:
            self.performer = m.group(1)
            return
        m = self._RE_INDEX.search(line)
        if m:
            self.index = m.group(1)

    def track_complete(self):
        return bool(self.track_num and self.title and self.index)

    def __str__(self):
        if self.track_num and self.title and self.index:
            suffix = "/" + self.performer if self.performer else ""
            return "Track " + str(self.track_num) + ": " + self.title + suffix
        return "Incomplete track"


class Cuesheet:
    _RE_PERFORMER = re.compile(r'^PERFORMER\s+"(.*?)"$')
    _RE_TITLE = re.compile(r'^TITLE\s+"(.*?)"$')
    _RE_FILE = re.compile(r'^FILE\s+".*?"\s+\w+$')

    def __init__(self, title: Optional[str] = None, performer: Optional[str] = None):
        self.title = title
        self.performer = performer
        self.tracks = []
        self.incomplete_header = False

    def parseline(self, line):
        m = self._RE_PERFORMER.search(line)
        if m:
            self.performer = m.group(1)
            return
        m = self._RE_TITLE.search(line)
        if m:
            self.title = m.group(1)
            return
        if self._RE_FILE.search(line):
            self.incomplete_header = True

    def add_track(self, track: Track):
        self.tracks.append(copy(track))

    def header_complete(self):
        return self.incomplete_header or bool(self.title and self.performer)

    def tracks_complete(self):
        return len(self.tracks) > 0

    def __str__(self):
        n = len(self.tracks)
        label = "Cuesheet with " + str(n) + " track(s)"
        if not self.tracks_complete():
            return "Incomplete " + label
        if self.performer and self.title:
            return label + ": " + self.performer + "/" + self.title
        elif self.performer:
            return label + ": " + self.performer
        elif self.title:
            return label + ": " + self.title
        return label


def parse_cue_file(file_path: str) -> Tuple[Optional[Cuesheet], Optional[str]]:
    """Parse a CUE file and return a Cuesheet, or an error string on failure."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return None, "Error reading file: " + str(e)

    sheet = Cuesheet()

    for idx, line in enumerate(lines):
        sheet.parseline(line)
        if sheet.header_complete():
            lines = lines[idx + 1:]
            break
    else:
        lines = []

    if sheet.header_complete():
        track = Track()
        for line in lines:
            track.parseline(line)
            if track.track_complete():
                sheet.add_track(track)
                # Reset by replacing with a fresh instance so that extra lines
                # between INDEX and the next TRACK directive don't re-trigger
                # track_complete() and add a duplicate.
                track = Track()

    if not sheet.header_complete():
        return None, "Error: Missing header info."
    if not sheet.tracks_complete():
        return None, "Error: Missing track list."

    return sheet, None


def format_output(sheet: Cuesheet, output_format: str, include_length: bool) -> str:
    if sheet.performer and sheet.title:
        sheet_title = sheet.performer + ": " + sheet.title
    elif sheet.performer or sheet.title:
        sheet_title = sheet.performer or sheet.title
    else:
        sheet_title = "Tracklist"

    if output_format == "md":
        output = "# " + sheet_title + "\n\n"
        for track in sheet.tracks:
            performer = track.performer or sheet.performer
            track_line = str(track.track_num) + ". " + track.title + " - " + performer
            if include_length:
                track_line += " (" + track.index + ")"
            output += track_line + "\n"
    elif output_format == "txt":
        output = sheet_title + "\n\n"
        for track in sheet.tracks:
            performer = track.performer or sheet.performer
            track_line = str(track.track_num) + ". " + track.title + " - " + performer
            if include_length:
                track_line += " (" + track.index + ")"
            output += track_line + "\n"
    else:
        return "Unsupported output format."

    return output


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 cue2lst.py <cuefile> <output_format> [--verbose]")
        sys.exit(1)

    cue_file = sys.argv[1]
    output_format = sys.argv[2].lower()
    include_length = False
    # Track length for the last track cannot be calculated from a CUE file alone.
    # include_length = "--length" in sys.argv[3:] if len(sys.argv) > 3 else False
    verbose = "--verbose" in sys.argv[3:] if len(sys.argv) > 3 else False

    if output_format not in ("md", "txt"):
        print("Output format must be 'md' or 'txt'.")
        sys.exit(1)

    sheet, error = parse_cue_file(cue_file)
    if error:
        print(error)
        sys.exit(1)

    output = format_output(sheet, output_format, include_length)
    output_file = os.path.splitext(cue_file)[0] + (".md" if output_format == "md" else ".txt")
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
    except Exception as e:
        print("Error writing file: " + str(e))
        sys.exit(1)

    if verbose:
        print("Disc performer:", sheet.performer)
        print("Disc title:", sheet.title)
        print("Total tracks:", len(sheet.tracks))
        print(*sheet.tracks, sep='\n')
        print("-----------------------------------")
    print("Output written to:", output_file)


if __name__ == "__main__":
    main()
