#!/usr/bin/env python3
"""Verify the immutable Issue 009 source and the reusable factory contract."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LOCKED_HASHES = {
    "issue-009/index.html": "dee53c0830acce37d369aa65bb7988353bc09bd8c4eaa3b2a639fdc562a1f73c",
    "issue-009/styles.css": "b1d0cec118020e6d8e13c70b46212b70dab49fdb24dfde461238c3684d26cc79",
    "issue-009/depth.css": "8bce417cf545d0e2e44b88785ad19b338ace628badceb40fe2ced5449dc1aa7c",
    "issue-009/premium.css": "245b8a09ef3e37df2ce911c5cc180aff01647abdac675b3aa6cd0ea0103fdf4f",
    "issue-009/hub.css": "d5c861d4592f7843cea425c54ce7248cba89d26b7f8e0cbf6c24d11fc3d74046",
    "issue-009/calendar.css": "ff548c7f8802c9d6449b9198ed80048dfe5a0299b54050ea9695a24baa5f6e65",
    "issue-009/hub.js": "194b5dde9117ff3440a7e70d2cf0d4dddeb3322d3171d392ef38e11ab3c6327c",
    "issue-009/premium-motion.js": "98edeecb7226b49b27d8bceefbda9b01a5fd46982d1fdb2ccc96bb5cc09b7984",
    "issue-009/assets/signal-room-v4-desktop.webp": "5799537b4e799f3c158defcc15a5d77cca127e945cf3297287639f1a762d8f5b",
    "issue-009/assets/signal-room-v4-mobile.webp": "e74ced4f78a87606001b7189f1049e0cdf39109fd24a8d7652a00e4bae301946",
    "issue-009/assets/og-suns-signal-009-next-step-v2.png": "08d1b66543c37397b2012038c505d37a14098d41fe42a80199c67aeac67bd14a",
    "issue-009/audio/suns-signal-009-next-step-arizona-v12-v11.mp3": "b053e7579853046d9f89b01a08a95c68d53f17a86fc4a321c210411791288d64",
    "issue-009/audio/suns-signal-009-next-step-arizona-v12-v11.metadata.json": "ca5bfee21e13218371a9b5555ef9715fe839d1f6af2b2384de99b30159aa61b1",
    "issue-009/content/audio-brief-transcript.txt": "ce59afbf7018ea8c92964185920586946e428c43fc8febff049af224f947e5af",
}
REQUIRED_VOICE_FILES = (
    "voice/ISSUE-009-HUB-OPTION-B.md",
    "voice/OG-009-MALUACH-BRIEF.md",
    "voice/AVC-Gladwell-voice-pack.md",
    "voice/CODEX-GLADWELL-PROMPT.md",
    "voice/og-source/PRIMARY-maluach-summer-league.jpg",
    "voice/og-source/facility-ref/README-REFERENCE-ONLY.md",
)
ROUTES = ("hub", "ownership", "pulse", "league", "calendar", "sources")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()


def require_text(path: str, needles: tuple[str, ...]) -> str:
    target = ROOT / path
    if not target.is_file():
        fail(f"missing required file: {path}")
    text = target.read_text(encoding="utf-8")
    for needle in needles:
        if needle not in text:
            fail(f"{path} is missing required lock text: {needle}")
    return text


def verify_locked_release() -> None:
    for relative, expected in LOCKED_HASHES.items():
        path = ROOT / relative
        if not path.is_file():
            fail(f"Issue 009 product-of-record file is missing: {relative}")
        actual = digest(path)
        if actual != expected:
            fail(f"Issue 009 product-of-record drift: {relative} ({actual})")

    html = (ROOT / "issue-009/index.html").read_text(encoding="utf-8")
    for route in ROUTES:
        if f'href="#{route}"' not in html and route != "hub":
            fail(f"Issue 009 is missing hub tile route: #{route}")
    if 'id="hub"' not in html or html.count('href="#hub"') < 2:
        fail("Issue 009 hub/Home route is incomplete")
    if 'eyebrow="Listen"' not in html:
        fail("Issue 009 audio player must use the Listen eyebrow")
    if "Mel Tucker audio" in html or "Mel Tucker Audio" in html:
        fail("Issue 009 player exposes a prohibited personal-name label")

    player = require_text(
        "assets/mel-audio-player/mel-audio-player.js",
        (
            'aria-label="Go back 15 seconds"',
            'aria-label="Go forward 15 seconds"',
            "this.seekBy(-15)",
            "this.seekBy(15)",
            'this.seek.addEventListener("input"',
        ),
    )
    if "currentTime = Number(this.seek.value)" not in player:
        fail("shared audio player seek control is not wired to currentTime")


def verify_contract() -> None:
    require_text(
        "EDITION-LOCK.md",
        (
            "Issue 009 is the last shipped Suns Signal product standard",
            "Preserve the system. Refresh the edition.",
            "#hub`, `#ownership`, `#pulse`, `#league`, `#calendar`, and `#sources",
            "Studio Qwen3-TTS **AVC Arizona Voice v12**",
            "Much love, my brother, dominate!",
            "Do not push a live Pages release until Mel says yes",
            "./scripts/new_issue_from_009.sh <issue-number>",
        ),
    )
    require_text(
        "AGENTS.md",
        (
            "## Product of record",
            "Issue 009 is the shipped product standard",
            "Do not redesign or rebuild the hub",
            "## Required audio closing",
            "## Audio player label",
            "## Required client iMessage",
        ),
    )
    for relative in REQUIRED_VOICE_FILES:
        if not (ROOT / relative).is_file():
            fail(f"missing required product provenance: {relative}")
    facility_dir = ROOT / "voice/og-source/facility-ref"
    if not any(facility_dir.glob("*.jpg")):
        fail("facility-ref needs at least one reference-only image")


def verify_scaffold() -> None:
    with tempfile.TemporaryDirectory(prefix="suns-signal-factory-") as temp_dir:
        sandbox = Path(temp_dir)
        shutil.copy2(ROOT / "EDITION-LOCK.md", sandbox / "EDITION-LOCK.md")
        shutil.copytree(ROOT / "issue-009", sandbox / "issue-009")
        (sandbox / "scripts").mkdir()
        shutil.copy2(ROOT / "scripts/new_issue_from_009.sh", sandbox / "scripts/new_issue_from_009.sh")
        shutil.copy2(ROOT / "scripts/reset_issue_from_009.py", sandbox / "scripts/reset_issue_from_009.py")

        command = [str(sandbox / "scripts/new_issue_from_009.sh"), "998"]
        result = subprocess.run(command, cwd=sandbox, text=True, capture_output=True, check=False)
        if result.returncode != 0:
            fail(f"scaffold smoke test failed: {result.stderr.strip()}")
        target = sandbox / "issue-998"
        if not target.is_dir():
            fail("scaffold did not create the requested issue directory")

        for preserved in ("styles.css", "depth.css", "premium.css", "hub.css", "calendar.css", "premium-motion.js"):
            if digest(target / preserved) != digest(sandbox / "issue-009" / preserved):
                fail(f"scaffold changed locked shell file: {preserved}")
        for hero in ("signal-room-shell-desktop.webp", "signal-room-shell-mobile.webp"):
            if not (target / "assets" / hero).is_file():
                fail(f"scaffold did not preserve responsive Blender shell: {hero}")

        html = (target / "index.html").read_text(encoding="utf-8")
        hub_js = (target / "hub.js").read_text(encoding="utf-8")
        transcript = (target / "content/audio-brief-transcript.txt").read_text(encoding="utf-8")
        for route in ROUTES:
            if route == "hub":
                present = 'id="hub"' in html
            else:
                present = f'href="#{route}"' in html
            if not present:
                fail(f"scaffold lost route: #{route}")
        if 'eyebrow="Listen"' not in html or "data-issue-number=\"998\"" not in html:
            fail("scaffold lost the player label or new issue identity")
        if "Suns Signal 009" in hub_js or "The Next Step Starts Early" in hub_js:
            fail("scaffold retained the Issue 009 browser title")
        if "[[REPLACE:" not in html or not (target / "assets/OG-REQUIRED.txt").is_file():
            fail("scaffold does not expose required content and OG placeholders")
        if list((target / "audio").glob("*.mp3")) or list((target / "audio").glob("*.metadata.json")):
            fail("scaffold retained Issue 009 audio")
        if any("og-suns-signal-009" in p.name for p in (target / "assets").iterdir()):
            fail("scaffold retained Issue 009 OG art")
        final_line = next(line.strip() for line in reversed(transcript.splitlines()) if line.strip())
        if final_line != "Much love, my brother, dominate!":
            fail("scaffold transcript lost the exact closing line")

        release_gate = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_weekly_structure.py"), str(target / "index.html")],
            text=True,
            capture_output=True,
            check=False,
        )
        if release_gate.returncode == 0:
            fail("an unfinished scaffold incorrectly passes the weekly release validator")

        overwrite = subprocess.run(command, cwd=sandbox, text=True, capture_output=True, check=False)
        if overwrite.returncode == 0 or "refusing to overwrite" not in overwrite.stderr:
            fail("scaffold overwrite guard did not stop an existing target")


def main() -> None:
    verify_locked_release()
    verify_contract()
    verify_scaffold()
    print("PASS: Issue 009 is locked, provenance is present, and the new-issue scaffold preserves the shell while clearing edition content.")


if __name__ == "__main__":
    main()
