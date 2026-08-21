#!/usr/bin/env python3
"""Validate recurring Suns Signal weekly-service sections before publishing."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

SERVICES = ("suns-pulse", "league-scan")
WINDOW_RE = re.compile(r'data-reporting-window="\d{4}-\d{2}-\d{2}/\d{4}-\d{2}-\d{2}"')
AUDIO_SIGNOFF = "Much love, my brother, dominate!"


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def section_for(html: str, service: str) -> str:
    pattern = re.compile(
        rf'<section[^>]*data-weekly-service="{re.escape(service)}"[^>]*>.*?</section>',
        re.DOTALL,
    )
    match = pattern.search(html)
    if not match:
        fail(f"missing weekly service section: {service}")
    return match.group(0)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    target = Path(sys.argv[1] if len(sys.argv) > 1 else "issue-006/index.html")
    html = target.read_text(encoding="utf-8")

    for service in SERVICES:
        section = section_for(html, service)
        opening_tag = section.split(">", 1)[0] + ">"
        if not WINDOW_RE.search(opening_tag):
            fail(f"{service} is missing an ISO reporting window")
        article_count = len(re.findall(r"<article\b", section))
        if article_count < 3:
            fail(f"{service} needs at least 3 dated items; found {article_count}")
        time_count = len(re.findall(r"<time\s+datetime=", section))
        if time_count != article_count:
            fail(f"{service} needs one dated <time> label per item")
        if "Official" not in section and "Reported" not in section:
            fail(f"{service} is missing reporting-status labels")

    required_text = (
        "Suns Weekly Pulse",
        "Around The League",
        "Next Watch",
        "Source Ledger",
        "Reporting cutoff:",
    )
    for text in required_text:
        if text not in html:
            fail(f"missing required release text: {text}")

    player_match = re.search(r"<mel-audio-player\b[^>]*>", html, re.DOTALL)
    if player_match:
        player_tag = player_match.group(0)
        src_match = re.search(r'\bsrc="([^"]+)"', player_tag)
        transcript_match = re.search(r'\btranscript="([^"]+)"', player_tag)
        if not src_match or not transcript_match:
            fail("Mel audio player must link both an MP3 and a transcript")
        audio_path = target.parent / src_match.group(1)
        transcript_path = target.parent / transcript_match.group(1)
        metadata_path = audio_path.with_suffix(".metadata.json")

        if not transcript_path.is_file():
            fail(f"missing linked audio transcript: {transcript_path}")
        transcript = transcript_path.read_text(encoding="utf-8")
        final_line = next((line.strip() for line in reversed(transcript.splitlines()) if line.strip()), "")
        if final_line != AUDIO_SIGNOFF:
            fail(f'audio transcript must end exactly: "{AUDIO_SIGNOFF}"')

        if not audio_path.is_file():
            fail(f"missing linked audio file: {audio_path}")
        if not metadata_path.is_file():
            fail(f"missing version-matched audio metadata: {metadata_path}")

        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if metadata.get("required_closing") != AUDIO_SIGNOFF or metadata.get("closing_verified") is not True:
            fail("audio metadata does not verify the required closing")
        if metadata.get("transcript_sha256") != sha256_file(transcript_path):
            fail("audio metadata transcript hash does not match the linked transcript")
        if metadata.get("sha256") != sha256_file(audio_path):
            fail("audio metadata hash does not match the linked MP3")

    print(f"PASS: {target} contains both dated weekly-service sections, reporting labels, and the required audio closing.")


if __name__ == "__main__":
    main()
