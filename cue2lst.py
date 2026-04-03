import sys
import re
from typing import List, Dict, Tuple, Optional


def parse_cue_file(file_path: str) -> Tuple[Optional[Dict[str, str]], Optional[List[Dict[str, str]]], Optional[str]]:
    """
    Parse a CUE file and return performer, title, and list of tracks with optional lengths.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        return None, None, "Error reading file: " + e

    performer = None
    title = None
    tracks = []

    idx = 0
    list_started = False

    for line in lines:
        line = line.strip()
        if line.startswith("PERFORMER"):
            if not list_started:
                performer = re.search(r'\"(.*?)\"', line).group(1)
        elif line.startswith("TITLE"):
            if not list_started:
                title = re.search(r'\"(.*?)\"', line).group(1)
        elif line.startswith("TRACK"):
            tracks.append({"number": line.split()[1], "title": None, "performer": None, "length": None})
            list_started = True
        elif line.startswith("INDEX 01") and tracks:
            last_track = tracks[-1]
            last_track["length"] = line.split()[2]
        idx += 1

    # Fill in track details
    for line in lines:
        line = line.strip()
        if line.startswith("TITLE") and not line.startswith("PERFORMER"):
            for track in tracks:
                if track["title"] is None:
                    track["title"] = re.search(r'\"(.*?)\"', line).group(1)
                    break
        elif line.startswith("PERFORMER"):
            for track in tracks:
                if track["performer"] is None and track["title"] is None:
                    track["performer"] = re.search(r'\"(.*?)\"', line).group(1)
                    break
                elif track["performer"] is None and track["title"] is not None:
                    track["performer"] = re.search(r'\"(.*?)\"', line).group(1)
                    break

    if not performer or not title or not tracks:
        return None, None, "Error: Missing required metadata in CUE file."

    return {"performer": performer, "title": title}, tracks, None


def to_title_case(s: str) -> str:
    return ' '.join(word.capitalize() for word in s.split())


def format_output(performer: str, title: str, tracks: List[Dict[str, str]], output_format: str, include_length: bool) -> str:
    print("Got:", performer, title, len(tracks), output_format)
    performer_title = to_title_case(performer) + ": " + to_title_case(title)

    if output_format == "md":
        output = "# " + performer_title + "\n\n"
        for track in tracks:
            track_line = str(int(track['number'])) + ". " + to_title_case(track['title']) + " - " + to_title_case(track['performer'])
            if include_length and track["length"]:
                track_line += " (" + track['length'] + ")"
            output += track_line + "\n"
    elif output_format == "txt":
        output = performer_title + "\n\n"
        for track in tracks:
            track_line = track['number'] + ". " + to_title_case(track['title']) + " - " + to_title_case(track['performer'])
            if include_length and track["length"]:
                track_line += " (" + track['length'] + ")"
            output += track_line + "\n"
    else:
        return "Unsupported output format."

    return output


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 cue2lst.py <cuefile> <output_format> [--length]")
        return

    cue_file = sys.argv[1]
    output_format = sys.argv[2].lower()
    include_length = "--length" in sys.argv[3:] if len(sys.argv) > 3 else False

    if output_format not in ("md", "txt"):
        print("Output format must be 'md' or 'txt'.")
        return

    metadata, tracks, error = parse_cue_file(cue_file)
    if error:
        print(error)
        return

    output = format_output(metadata["performer"], metadata["title"], tracks, output_format, include_length)

    output_file = os.path.splitext(cue_file)[0] + (".md" if output_format == "md" else ".txt")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output)

    print("Output written to: ", output_file)


if __name__ == "__main__":
    import os
    main()