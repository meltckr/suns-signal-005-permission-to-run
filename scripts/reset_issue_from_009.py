#!/usr/bin/env python3
"""Clone the locked Issue 009 shell and reset every edition-specific field.

This helper is invoked by new_issue_from_009.sh. It intentionally produces an
incomplete draft whose placeholders and missing MP3/OG files block release.
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path


SIGNOFF = "Much love, my brother, dominate!"
PLACEHOLDER = "[[REPLACE: {label}]]"


def stop(message: str, code: int = 1) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def placeholder(label: str) -> str:
    return PLACEHOLDER.format(label=label)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def story_card(number: int, lane: str) -> str:
    return (
        f'          <article><span><time datetime="{placeholder("YYYY-MM-DD")}">'
        f'{placeholder("Official, Reported, analysis, or directional · date")}</time></span>'
        f'<h3>{placeholder(f"{lane} headline {number}")}</h3>'
        f'<p>{placeholder(f"{lane} evidence, meaning, and ownership relevance {number}")}</p>'
        f'<a href="{placeholder(f"primary source URL {number}")}">'
        f'{placeholder(f"source label {number}")} ↗</a></article>'
    )


def render_index(issue: str) -> str:
    title = placeholder("EDITION TITLE")
    description = placeholder("ONE-SENTENCE DESCRIPTION")
    iso_date = placeholder("YYYY-MM-DDTHH:MM:SS-04:00")
    public_date = placeholder("MONTH D, YYYY")
    reporting_range = placeholder("REPORTING WINDOW")
    reporting_iso = placeholder("YYYY-MM-DD/YYYY-MM-DD")
    origin = f"https://meltckr.github.io/suns-signal-005-permission-to-run/issue-{issue}/"
    og_name = placeholder("VERSIONED OG PNG FILENAME")
    audio_name = placeholder("VERSIONED ARIZONA V12 MP3 FILENAME")
    pulse_cards = "\n".join(story_card(i, "Suns Weekly Pulse") for i in range(1, 6))
    league_cards = "\n".join(story_card(i, "Around The League") for i in range(1, 6))

    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Suns Signal {issue} | {title}</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="noindex,nofollow,noarchive">
  <link rel="canonical" href="{origin}">
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="Suns Signal">
  <meta property="article:published_time" content="{iso_date}">
  <meta property="article:modified_time" content="{iso_date}">
  <meta property="og:title" content="Suns Signal {issue} | {title}">
  <meta property="og:description" content="{description}">
  <meta property="og:url" content="{origin}">
  <meta property="og:image" content="{origin}assets/{og_name}">
  <meta property="og:image:secure_url" content="{origin}assets/{og_name}">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{placeholder('OG ALT: hook, lead player, context, curated for Mat Ishbia')}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Suns Signal {issue} | {title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="{origin}assets/{og_name}">
  <meta name="twitter:image:alt" content="{placeholder('TWITTER IMAGE ALT')}">
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{title}","datePublished":"{iso_date}","author":{{"@type":"Organization","name":"Accelerated Velocity Consulting"}},"publisher":{{"@type":"Organization","name":"Accelerated Velocity Consulting"}},"image":["{origin}assets/{og_name}"],"mainEntityOfPage":"{origin}"}}</script>
  <link rel="stylesheet" href="../styles.css">
  <link rel="stylesheet" href="styles.css?v={issue}-v1">
  <link rel="stylesheet" href="depth.css?v={issue}-depth-v1">
  <link rel="stylesheet" href="premium.css?v={issue}-premium-v1">
  <link rel="stylesheet" href="hub.css?v={issue}-hub-v1">
  <link rel="stylesheet" href="calendar.css?v={issue}-calendar-v1">
  <script type="module" src="hub.js?v={issue}-hub-v1"></script>
  <script type="module" src="../assets/mel-audio-player/mel-audio-player.js"></script>
</head>
<body data-issue-number="{issue}" data-issue-title="{title}">
<header class="site-header">
  <a class="series-brand" href="#hub" aria-label="Suns Signal home"><img src="../assets/teams/suns/phoenix-suns-logo.png" alt="Phoenix Suns logo"><span><strong>Suns Signal</strong><em>Weekly | Issue {issue}</em></span></a>
  <div class="edition"><span class="avc-provenance">Prepared by <img src="../assets/brand/logos/AVC-logo-horizontal-light.svg" alt="Accelerated Velocity Consulting"></span><strong>{public_date}</strong></div>
  <nav class="section-toolbar" aria-label="Section navigation" hidden><span class="current-section">Ownership</span><a href="#hub" data-listen-link>Listen</a><a href="#hub" class="home-link">← Home</a></nav>
</header>
<main id="top">
  <section id="hub" class="hero issue-nine-hero command-deck" aria-label="Issue {issue} command deck">
    <picture class="hero-picture">
      <source media="(max-width:760px)" srcset="assets/signal-room-shell-mobile.webp" width="900" height="1100">
      <img class="hero-art" src="assets/signal-room-shell-desktop.webp" width="1920" height="1200" fetchpriority="high" alt="{placeholder('NEW EDITION HERO ALT; REPLACE OR EXTEND THE BLENDER SCENE')}">
    </picture>
    <div class="hero-overlay"></div>
    <div class="hub-layout">
      <div class="hub-intro">
        <p class="kicker">{placeholder('ONE EDITION LANE')}</p>
        <h1 tabindex="-1">{title}</h1>
        <p class="hub-byline">Curated for Mat Ishbia <span>· {reporting_range}</span></p>
      </div>
      <div class="decision-strip" aria-label="Ownership signals">
        <div><span>{placeholder('SIGNAL 1 LABEL')}</span><strong>{placeholder('SIGNAL 1 READ')}</strong></div>
        <div><span>{placeholder('SIGNAL 2 LABEL')}</span><strong>{placeholder('SIGNAL 2 READ')}</strong></div>
        <div><span>{placeholder('SIGNAL 3 LABEL OR REMOVE THIS ITEM')}</span><strong>{placeholder('SIGNAL 3 READ OR REMOVE THIS ITEM')}</strong></div>
      </div>
      <div class="signal-audio"><mel-audio-player src="audio/{audio_name}" title="{title}" eyebrow="Listen" transcript="content/audio-brief-transcript.txt" download></mel-audio-player></div>
      <nav class="hub-tiles" aria-label="Explore this edition">
        <a href="#ownership" data-hub-tile="ownership"><span class="tile-number">01</span><span><strong>Ownership</strong><small>First read &amp; the central idea</small></span><span class="tile-arrow" aria-hidden="true">↗</span></a>
        <a href="#pulse" data-hub-tile="pulse"><span class="tile-number">02</span><span><strong>Pulse</strong><small>Suns Weekly Pulse</small></span><span class="tile-arrow" aria-hidden="true">↗</span></a>
        <a href="#league" data-hub-tile="league"><span class="tile-number">03</span><span><strong>League</strong><small>Around The League</small></span><span class="tile-arrow" aria-hidden="true">↗</span></a>
        <a href="#calendar" data-hub-tile="calendar"><span class="tile-number">04</span><span><strong>Calendar</strong><small>Calendar Ahead</small></span><span class="tile-arrow" aria-hidden="true">↗</span></a>
        <a href="#sources" data-hub-tile="sources"><span class="tile-number">05</span><span><strong>Sources</strong><small>Source Ledger</small></span><span class="tile-arrow" aria-hidden="true">↗</span></a>
      </nav>
    </div>
  </section>

  <div id="ownership" class="section-view ownership-view" data-section-view="ownership">
    <p class="section-dek">{placeholder('OWNERSHIP SECTION DEK')}</p>
    <section class="top-brief" aria-label="Suns Signal first read">
      <div class="glance-panel"><span class="source-tag">At A Glance</span><h2>{placeholder('20-SECOND READ HEADLINE')}</h2><div class="glance-grid">
        <article><span>{placeholder('GLANCE LABEL 1')}</span><strong>{placeholder('GLANCE READ 1')}</strong><p>{placeholder('GLANCE SUPPORT 1')}</p></article>
        <article><span>{placeholder('GLANCE LABEL 2')}</span><strong>{placeholder('GLANCE READ 2')}</strong><p>{placeholder('GLANCE SUPPORT 2')}</p></article>
        <article><span>{placeholder('GLANCE LABEL 3')}</span><strong>{placeholder('GLANCE READ 3')}</strong><p>{placeholder('GLANCE SUPPORT 3')}</p></article>
        <article><span>The Next Evidence</span><strong>{placeholder('NEXT EVIDENCE READ')}</strong><p>{placeholder('WHAT OWNERSHIP SHOULD WATCH')}</p></article>
      </div></div>
      <div class="ownership-note"><span class="source-tag">Ownership Note</span><h2>{placeholder('OWNERSHIP NOTE HEADLINE')}</h2><p>{placeholder('CONCRETE OPENING FACT')}</p><p>{placeholder('PLAIN-ENGLISH PATTERN AND WHY IT MATTERS')}</p></div>
    </section>
    <section class="newsletter-body">
      <aside class="left-rail">
        <div class="rail-block"><span class="label">Reporting Period</span><p><strong>{reporting_range}</strong><br>{placeholder('REPORTING SCOPE AND BACKGROUND BOUNDARY')}</p></div>
        <div class="rail-block"><span class="label">Central Signal</span><p><strong>{placeholder('CENTRAL SIGNAL')}</strong><br>{placeholder('ONE-SENTENCE SUPPORT')}</p></div>
        <div class="rail-block"><span class="label">Why It Matters</span><p><strong>{placeholder('OWNERSHIP RELEVANCE')}</strong><br>{placeholder('EVIDENCE-SUPPORTED IMPLICATION')}</p></div>
        <div class="rail-block"><span class="label">Inside This Issue</span><p><a href="#pulse">Suns Weekly Pulse</a><br><a href="#league">Around The League</a><br><a href="#calendar">Calendar Ahead</a><br><a href="#sources">Source Ledger</a></p></div>
      </aside>
      <article class="story">
        <section><span class="source-tag">{placeholder('STORY SECTION LABEL 1')}</span><h2>{placeholder('STORY HEADLINE 1')}</h2><p>{placeholder('VERIFIED EVIDENCE AND SOURCE LINK')}</p><p>{placeholder('WHAT THE SEQUENCE REVEALS')}</p></section>
        <section class="data-strip" aria-label="Edition evidence"><div><span>{placeholder('STAT 1')}</span><p>{placeholder('STAT 1 LABEL')}</p></div><div><span>{placeholder('STAT 2')}</span><p>{placeholder('STAT 2 LABEL')}</p></div><div><span>{placeholder('STAT 3')}</span><p>{placeholder('STAT 3 LABEL')}</p></div><div><span>{placeholder('STAT 4')}</span><p>{placeholder('STAT 4 LABEL')}</p></div></section>
        <section><span class="source-tag">{placeholder('STORY SECTION LABEL 2')}</span><h2>{placeholder('STORY HEADLINE 2')}</h2><p>{placeholder('ANALYSIS PARAGRAPH 1')}</p><p>{placeholder('ANALYSIS PARAGRAPH 2')}</p></section>
        <section class="capture-section"><span class="source-tag">Directional Public Reaction</span><h2>{placeholder('DIRECTIONAL REACTION HEADLINE')}</h2><div class="capture-grid"><article><span class="source-tag">{placeholder('REACTION THEME 1')}</span><h3>{placeholder('REACTION READ 1')}</h3><p>{placeholder('SAMPLED EVIDENCE 1')}</p></article><article><span class="source-tag">{placeholder('REACTION THEME 2')}</span><h3>{placeholder('REACTION READ 2')}</h3><p>{placeholder('SAMPLED EVIDENCE 2')}</p></article></div><p>{placeholder('DIRECTIONAL INTERPRETATION')}</p><p class="count-note">{placeholder('PLATFORM, DATE, SAMPLE METHOD, AND NONREPRESENTATIVE LIMIT')}</p></section>
        <section><span class="source-tag">The Ownership Read</span><h2>{placeholder('FINAL OWNERSHIP HEADLINE')}</h2><p>{placeholder('WHAT IT MEANS')}</p><p>{placeholder('WHAT TO WATCH')}</p></section>
      </article>
    </section>
  </div>

  <div id="pulse" class="section-view story" data-section-view="pulse">
    <section id="suns-pulse" class="league-roundup suns-pulse" data-weekly-service="suns-pulse" data-reporting-window="{reporting_iso}">
      <div class="roundup-heading"><span class="source-tag">Suns Weekly Pulse</span><h2>{placeholder('FIVE SUNS SIGNALS HEADLINE')}</h2></div>
      <div class="roundup-grid">
{pulse_cards}
      </div>
      <p class="count-note"><strong>Reporting cutoff:</strong> {placeholder('CUTOFF DATE, WINDOW, AND LABELING NOTE')}</p>
    </section>
  </div>

  <div class="section-view story" data-section-view="league">
    <section id="league" class="league-roundup" data-weekly-service="league-scan" data-reporting-window="{reporting_iso}">
      <div class="roundup-heading"><span class="source-tag">Around The League</span><h2>{placeholder('FIVE LEAGUE DEVELOPMENTS HEADLINE')}</h2></div>
      <div class="roundup-grid">
{league_cards}
      </div>
    </section>
  </div>

  <div class="section-view story" data-section-view="calendar">
    <section id="calendar" class="scoreboard-section reception-ledger"><span class="source-tag">Calendar Ahead</span><h2>{placeholder('CALENDAR HEADLINE')}</h2>
      <figure class="calendar-board" aria-label="{placeholder('CALENDAR RANGE ALT')}">
        <div class="calendar-heading"><span>{placeholder('CALENDAR RANGE LABEL')}</span><strong>{placeholder('CALENDAR DATE RANGE')} <small>{placeholder('YEAR')}</small></strong></div>
        <div class="calendar-placeholder"><p>{placeholder('REBUILD THE VISIBLE TWO-OR-THREE-WEEK CALENDAR WITH VERIFIED SUNS AND LEAGUE DATES')}</p></div>
        <figcaption><div class="calendar-legend"><span class="suns-key">Suns</span><span class="league-key">League-wide</span></div><span>{placeholder('CALENDAR QUALIFIER IF NEEDED')}</span></figcaption>
      </figure>
      <div class="calendar-details"><div class="calendar-suns"><h3 class="calendar-lane">Phoenix</h3><div class="scoreboard-grid"><article><span>{placeholder('DATE')}</span><h3>{placeholder('SUNS DATE 1')}</h3><small class="calendar-status">{placeholder('Official or Reported')}</small><p>{placeholder('WHY THE DATE MATTERS')}</p></article><article><span>{placeholder('DATE')}</span><h3>{placeholder('SUNS DATE 2')}</h3><small class="calendar-status">{placeholder('Official or Reported')}</small><p>{placeholder('WHY THE DATE MATTERS')}</p></article></div></div><div class="calendar-league"><h3 class="calendar-lane">Around the NBA</h3><article><span class="calendar-date">{placeholder('DATE')}</span><h4>{placeholder('LEAGUE DATE')}</h4><small class="calendar-status">{placeholder('Official or Reported')}</small><p>{placeholder('WHY THE DATE MATTERS')}</p><a href="{placeholder('PRIMARY CALENDAR SOURCE URL')}">{placeholder('SOURCE')} ↗</a></article></div></div>
      <p class="count-note">Calendar sources: {placeholder('PRIMARY OFFICIAL AND REPORTED SOURCES WITH LABELS')}</p>
    </section>
  </div>

  <div class="section-view story" data-section-view="sources">
    <section id="sources" class="source-ledger"><h2>Source Ledger</h2><ol><li>{placeholder('SOURCE 1: outlet, date, claim, URL, and status')}</li><li>{placeholder('SOURCE 2')}</li><li>{placeholder('SOURCE 3')}</li></ol><p class="count-note">{placeholder('REVIEW DATE, SOURCE HIERARCHY, INTERPRETATION, HEALTH, SENTIMENT, AND BACKGROUND NOTE')}</p></section>
  </div>
</main>
<footer class="site-footer"><img src="../assets/brand/logos/AVC-icon-light.svg" alt="" aria-hidden="true"><div><strong>Prepared by Accelerated Velocity Consulting</strong><span>Sports strategy and sentiment intelligence.</span></div><a href="#hub">← Home</a></footer>
</body>
</html>'''


def render_hub_js(source: str) -> str:
    anchor = "let firstLoad = true;"
    if anchor not in source:
        stop("Issue 009 hub.js no longer matches the locked routing shell")
    source = source.replace(
        anchor,
        anchor
        + "\nconst issueTitle = document.body.dataset.issueTitle || 'Suns Signal';"
        + "\nconst issueNumber = document.body.dataset.issueNumber || '';",
        1,
    )
    source, count = re.subn(
        r"document\.title = atHome \? 'Suns Signal 009 \| The Next Step Starts Early' : `\$\{labels\[name\]\} \| Suns Signal 009`;",
        "document.title = atHome ? `Suns Signal ${issueNumber} | ${issueTitle}` : `${labels[name]} | Suns Signal ${issueNumber}`;",
        source,
        count=1,
    )
    if count != 1:
        stop("Could not reset the hard-coded Issue 009 browser title in hub.js")
    return source


def reset_assets(target: Path) -> None:
    assets = target / "assets"
    keep = {
        "signal-room-v4-desktop.webp": "signal-room-shell-desktop.webp",
        "signal-room-v4-mobile.webp": "signal-room-shell-mobile.webp",
    }
    for path in list(assets.iterdir()):
        if path.name not in keep:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
    for old_name, new_name in keep.items():
        old_path = assets / old_name
        if not old_path.is_file():
            stop(f"locked Blender shell asset is missing: {old_path}")
        old_path.rename(assets / new_name)
    write_text(
        assets / "OG-REQUIRED.txt",
        "Create a story-specific 1200x630 versioned PNG and update all page metadata before release.\n"
        "Use a real photograph of this edition's lead player. Preserve older versions when recutting.",
    )


def reset_audio(target: Path) -> None:
    audio = target / "audio"
    for path in list(audio.iterdir()):
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    write_text(
        audio / "README.md",
        "# Audio pending\n\n"
        "Generate this edition with the Studio Qwen3-TTS AVC Arizona Voice v12 recipe. "
        "Use a new versioned MP3 and matching metadata JSON. Update the player, transcript, README, and client note together. "
        "Listen to the final approximately ten seconds and confirm the complete spoken sign-off before release.",
    )
    write_text(
        target / "content" / "audio-brief-transcript.txt",
        f"{placeholder('WRITE THE COMPLETE VERIFIED AUDIO BRIEF')}\n\n{SIGNOFF}",
    )


def reset_notes(target: Path, issue: str) -> None:
    origin = f"https://meltckr.github.io/suns-signal-005-permission-to-run/issue-{issue}/"
    write_text(
        target / "README.md",
        f"# Suns Signal {issue} — scaffold\n\n"
        "Status: draft scaffold only. Content, facts, sources, hero, OG, audio, metadata, and client note are incomplete. "
        "Publishing is not authorized.\n\n"
        "This directory inherits the Issue 009 command-deck shell under `EDITION-LOCK.md`. Preserve the hub, routes, audio placement, "
        "responsive behavior, and permanent URL architecture. Refresh every edition-specific field.\n\n"
        "## Required before review\n\n"
        "- Replace every `[[REPLACE: ...]]` marker.\n"
        "- Verify current facts and label Official, Reported, analysis, and directional evidence.\n"
        "- Replace or extend the Blender hero and write accurate alt text.\n"
        "- Add a story-specific, real-player 1200x630 OG card and update all metadata.\n"
        "- Generate new versioned Arizona v12 audio and matching metadata.\n"
        "- Complete `sources.md`, `social-capture.md`, `validation.md`, and `imessage.txt`.\n"
        f"- Run `python3 scripts/validate_weekly_structure.py issue-{issue}/index.html`.\n"
        "- Complete desktop, approximately 390-pixel mobile, hash-route, Home, seek, and ±15 proof.\n"
        "- Obtain Mel's explicit approval before any Pages push.\n\n"
        f"Permanent URL after an approved release: {origin}",
    )
    write_text(
        target / "sources.md",
        "# Source plan and ledger\n\n"
        f"Reporting window: {placeholder('YYYY-MM-DD through YYYY-MM-DD')}\n\n"
        "Use primary and official sources first. Record the exact claim each source supports, publication or update date, "
        "Official/Reported/analysis/directional status, and whether it is current-window reporting or labeled background.\n\n"
        f"1. {placeholder('SOURCE URL — outlet — date — supported claim — status')}\n"
        f"2. {placeholder('SOURCE URL — outlet — date — supported claim — status')}\n"
        f"3. {placeholder('SOURCE URL — outlet — date — supported claim — status')}",
    )
    write_text(
        target / "social-capture.md",
        "# Directional sentiment capture\n\n"
        "Status: not yet collected.\n\n"
        f"- Platform and public URL: {placeholder('PLATFORM AND URL')}\n"
        f"- Capture time: {placeholder('TIMESTAMP AND TIME ZONE')}\n"
        f"- Visible sample reviewed: {placeholder('COUNT OR BOUNDED METHOD')}\n"
        f"- Recurring themes: {placeholder('THEMES WITH DISCONFIRMING EVIDENCE')}\n"
        "- Required label: qualitative, directional, self-selected, and nonrepresentative unless a stronger method is documented.",
    )
    write_text(
        target / "imessage.txt",
        f"{placeholder('DRAFT FOR MEL: POSITIVE, ACCURATE TWO-TO-FOUR SENTENCE CLIENT NOTE')}\n\n{origin}",
    )
    write_text(
        target / "validation.md",
        f"# Suns Signal {issue} validation\n\n"
        "Status: incomplete scaffold. No release approval.\n\n"
        "- [ ] All placeholders removed\n"
        "- [ ] Consequential facts verified and labels correct\n"
        "- [ ] Mat spelled with one T throughout\n"
        "- [ ] Issue 009 and earlier editions unchanged\n"
        "- [ ] Desktop hub fits the intended first viewport\n"
        "- [ ] Approximately 390-pixel mobile hub fits and remains legible\n"
        "- [ ] Tiles, Home, and all six hash routes work\n"
        "- [ ] Audio seek and ±15 work\n"
        "- [ ] Versioned MP3 and matching metadata verify\n"
        "- [ ] Full audio listened to; final sign-off complete and unclipped\n"
        "- [ ] Story-specific OG is 1200x630 and metadata/alt are synchronized\n"
        "- [ ] Weekly structure validator passes\n"
        "- [ ] Mel has explicitly approved a Pages release",
    )


def main() -> None:
    if len(sys.argv) != 3:
        stop("Usage: reset_issue_from_009.py <repo-root> <issue-number>", 64)
    root = Path(sys.argv[1]).resolve()
    raw = sys.argv[2]
    if not re.fullmatch(r"\d{1,3}", raw):
        stop("issue number must contain one to three digits", 64)
    issue = f"{int(raw):03d}"
    if issue == "009":
        stop("Issue 009 is the immutable product-of-record source")
    source = root / "issue-009"
    target = root / f"issue-{issue}"
    if not (root / "EDITION-LOCK.md").is_file() or not source.is_dir():
        stop("run this command from the canonical Suns Signal repository with Issue 009 present")
    if target.exists():
        stop(f"refusing to overwrite existing target: {target}")

    shutil.copytree(source, target)
    try:
        reset_assets(target)
        reset_audio(target)
        write_text(target / "index.html", render_index(issue))
        write_text(target / "hub.js", render_hub_js((source / "hub.js").read_text(encoding="utf-8")))
        reset_notes(target, issue)
    except Exception:
        shutil.rmtree(target)
        raise

    print(f"CREATED: {target}")
    print("STATUS: incomplete scaffold; publishing is not authorized")
    print(f"NEXT: replace every {placeholder('...')} marker and complete EDITION-LOCK.md release gates")


if __name__ == "__main__":
    main()
