#!/usr/bin/env python3
"""Validate recurring Suns Signal weekly-service sections before publishing."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SERVICES = ("suns-pulse", "league-scan")
WINDOW_RE = re.compile(r'data-reporting-window="\d{4}-\d{2}-\d{2}/\d{4}-\d{2}-\d{2}"')


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

    print(f"PASS: {target} contains both dated weekly-service sections and reporting labels.")


if __name__ == "__main__":
    main()
