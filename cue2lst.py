import sys
import re
from typing import Tuple, Optional
from copy import deepcopy


class Track:
    # TRACK 02 AUDIO
    #   TITLE "Margret Evening Fashion"
    #   PERFORMER "Le Hammond Inferno"
    #   INDEX 01 04:47:69

    def __init__(self, track_num: str = None, title: str = None, performer: str = None, index: str = None):
        self.track_num = int(track_num) if track_num else None
        self.title = title if title else None
        self.performer = performer if performer else None
        self.index = index if index else None

    def parseline(self, line):
        r_tmp = re.search(r'^\s{0,}TRACK\s{1,}(\d{1,})\s{1,}AUDIO$', line)
        if r_tmp:
            self.track_num = int(r_tmp.group(1))
            self.title = None
            self.performer = None
            self.index = None
        r_tmp = re.search(r'^\s{0,}TITLE\s{1,}\"(.*?)\"$', line)
        if r_tmp:
            self.title = r_tmp.group(1)
        r_tmp = re.search(r'^\s{0,}PERFORMER\s{1,}\"(.*?)\"$', line)
        if r_tmp:
            self.performer = r_tmp.group(1)
        r_tmp = re.search(r'^\s{0,}INDEX\s{1,}\d{1,}\s{1,}(.*?)$', line)
        if r_tmp:
            self.index = r_tmp.group(1)

    def track_complete(self):
        return self.track_num and self.title and self.performer and self.index

    def __str__(self):
        if self.performer and self.title and self.track_num and self.index:
            return "Track "+str(self.track_num)+": "+self.performer+"/"+self.title
        else:
            return "Incomplete track"


class Cuesheet:
    # PERFORMER "Ursula 1000"
    # TITLE "All Systems Are Go Go"
    # FILE "CDImage.wav" WAVE
    tracks = []

    def __init__(self, title: str = None, performer: str = None):
        self.title = title if title else None
        self.performer = performer if performer else None

    def parseline(self, line):
        r_tmp = re.search(r'^PERFORMER\s{1,}\"(.*?)\"$', line)
        if r_tmp:
            self.performer = r_tmp.group(1)
        r_tmp = re.search(r'^TITLE\s{1,}\"(.*?)\"$', line)
        if r_tmp:
            self.title = r_tmp.group(1)

    def add_track(self, track: Track):
        c_track = deepcopy(track)
        self.tracks.append(c_track)

    def len(self):
        return len(self.tracks)

    def header_complete(self):
        return self.title and self.performer

    def tracks_complete(self):
        return self.len() > 0

    def __str__(self):
        if self.performer and self.title:
            return "Cuesheet with "+str(self.len())+" track(s): "+self.performer+"/"+self.title
        else:
            return "Incomplete Cuesheet with "+str(self.len())+" track(s)"


def parse_cue_file(file_path: str) -> Tuple[Optional[Cuesheet], Optional[str]]:
    """
    Parse a CUE file and return performer, title, and list of tracks with optional lengths.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return None, "Error reading file: " + e

    sheet = Cuesheet()
    idx = 0

    for line in lines:
        sheet.parseline(line)
        if sheet.header_complete():
            break;
        idx += 1
    del lines[0:idx+1]

    if sheet.header_complete():
        track = Track()
        for line in lines:
            track.parseline(line)
            if track.track_complete():
                sheet.add_track(track)
            idx += 1

    if not sheet.performer or not sheet.title or not sheet.tracks:
        return None, "Error: Missing required metadata in CUE file."

    return sheet, None


def format_output(sheet: Cuesheet, output_format: str, include_length: bool) -> str:
    performer_title = sheet.performer + ": " + sheet.title

    if output_format == "md":
        output = "# " + performer_title + "\n\n"
        for track in sheet.tracks:
            track_line = str(int(track.track_num)) + ". " + track.title + " - " + track.performer
            if include_length:
                track_line += " (" + track.index + ")"
            output += track_line + "\n"
    elif output_format == "txt":
        output = performer_title + "\n\n"
        for track in sheet.tracks:
            track_line = str(track.track_num) + ". " + track.title + " - " + track.performer
            if include_length:
                track_line += " (" + track.index + ")"
            output += track_line + "\n"
    else:
        return "Unsupported output format."

    return output


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 cue2lst.py <cuefile> <output_format> [--verbose]")
        return

    cue_file = sys.argv[1]
    output_format = sys.argv[2].lower()
    include_length = False
    # Apparently, it is not possible to calculate track length for the last track!
    # include_length = "--length" in sys.argv[3:] if len(sys.argv) > 3 else False
    verbose = "--verbose" in sys.argv[3:] if len(sys.argv) > 3 else False

    if output_format not in ("md", "txt"):
        print("Output format must be 'md' or 'txt'.")
        return

    sheet, error = parse_cue_file(cue_file)
    if error:
        print(error)
        return

    output = format_output(sheet, output_format, include_length)
    output_file = os.path.splitext(cue_file)[0] + (".md" if output_format == "md" else ".txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)

    if verbose:
        print("Disc performer:", sheet.performer)
        print("Disc title:", sheet.title)
        print("Total tracks:", sheet.len())
        print(*sheet.tracks, sep='\n')
        print("-----------------------------------")
    print("Output written to:", output_file)


if __name__ == "__main__":
    import os
    main()