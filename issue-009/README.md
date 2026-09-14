# Suns Signal Weekly 009 — The Next Step Starts Early

Reporting window: August 31–September 13, 2026 (14 inclusive calendar days).

Canonical intended URL: https://meltckr.github.io/suns-signal-005-permission-to-run/issue-009/

## Publication authorization — September 13, 2026

Mel explicitly authorized publishing the updated edition to the existing GitHub Pages site so it can be reviewed on iPhone. This supersedes the earlier local-only publication holds recorded below. The release includes the tightened command-deck hub, v3 Blender room artwork, visual Suns/NBA calendar, locked smiling-Maluach OG v2 and Arizona v12 narration v6. The positive iMessage remains a draft; no client message is authorized. Technical audio checks passed; Mel’s perceptual listening review remains separate.

Base: published Issue 007, canonical series repository. Shared stylesheet, logos, player, editorial modules, metadata conventions and permanent issue URLs are preserved. Unfinished Issue 008 is untouched. No new host or product architecture.

Audio: approved AVC Arizona Voice v12, using the Standard 004 clean-opening-and-endings production method, exact Suns closing and `Listen` eyebrow. Voice reference files and raw renders stay private. See version-matched audio metadata for actual verification status. Technical QA is distinct from perceptual listening approval.

Share card: deterministic SVG source and 1200×630 PNG, unique Issue 009 filename. Public facts only; no confidential information or private voice reference assets.

September 13 review revision: five sourced cards in each weekly scan; v2 audio replaces v1 in the player without deleting the original. Version 2 uses a pronunciation alias for Khaman Maluach and regenerates 13 sentences, removing temporary spoken context only inside measured quiet pauses. The written audio brief stays unchanged and is a summary, not a reading of every scan card. See `validation.md` for the technical results and remaining listening approval.

Run `python3 scripts/validate_weekly_structure.py issue-009/index.html` from the repository root. Do not treat a pass as fact verification or perceptual listening approval. See `sources.md` and `validation.md` for those separate gates.

`imessage.txt` is drafted for Mel to send. Do not send automatically.

## Approved writing recut — local review, not published

Mel approved the sample ownership note and audio opening. The page and transcript now use that voice throughout: concrete evidence, plain-English implications, and uncertainty only where the evidence warrants it. The internal Next Watch section is removed; its research prompts are kept outside this release repository in private production notes.

Current audio: `audio/suns-signal-009-next-step-arizona-v12-v6.mp3`, with matching `.metadata.json`, linked by the unchanged `Listen` player. The current recut has 24 sentences and 304 words and runs 103.914 seconds (approximately 1:44; the shared player floors its display to 1:43). V1–v5 remain preserved. V6 changes only the closing delivery, giving “dominate” more emphasis and duration with a brief preceding pause; all other source clips and the transcript are unchanged. The transcript retains the exact standalone closing, `Much love, my brother, dominate!` Technical checks passed; Mel’s listening approval remains pending. The iMessage draft describes this recut and the new hub and retains the permanent production URL; it is unsent.

The approved Blender depth treatment and high-contrast audio surface remain intact. Reporting dates and labels, source links, source ledger, permanent URLs, shared player code, OG artwork and prior editions are preserved. The structural validator permits the requested section removal and rejects its internal editorial heading. The issue and depth checks now validate the approved recut rather than requiring unchanged prose or v2's fixed count of repaired sentences.

Review locally at `http://127.0.0.1:4200/issue-009/` on this Mac. This local preview is not a public phone-sharing link. Do not commit, push, or publish Pages until Mel explicitly approves publication. Audio listening approval remains separate from technical verification; see `validation.md`.

## Writing-first checkpoint

The page and transcript now follow the current global Mel voice, anti-hedge and four humanizer standards. The approved ownership note and audio opening are locked by assertions in `scripts/verify_issue_009.mjs`. A final independent editorial comparison passed after removing a defensive source disclaimer and restoring the original qualification in the Grange report. No new reporting or factual refresh was part of this recut.

## FULL BELLS product — local review

Mel’s latest lock supersedes the temporary design pause. Option B is implemented in `index.html`, `hub.css` and `hub.js`. The canonical briefs remain in the canonical checkout’s local, unpublished `voice/` directory. The first screen combines the responsive Blender hero, one mounted standard audio player, the Williams/Maluach/next-evidence strip and five section tiles. Duplicate hero branding is removed; the edition lane is The Camp Preview.

Routes: `#hub`, `#ownership`, `#pulse`, `#league`, `#calendar`, `#sources`. `#top` and `#suns-pulse` remain compatible aliases. Sections are separate views; sticky Home, Listen and Escape return to the hub. Native hash history and direct links use the same route handler. Audio stays mounted and can continue during section navigation. Focus moves into a newly opened section and returns to its hub tile. With JavaScript unavailable, the document remains readable and anchors work; print CSS reveals every section. Smaller viewports or enlarged text may scroll rather than clip content.

OG v2 is `assets/og-suns-signal-009-next-step-v2.svg` and `.png`, a 1200×630 photo-led card using `assets/maluach-summer-league-primary.jpg`, copied byte-for-byte from the locked smiling Maluach source. V1 stays intact. Absolute OG, Twitter, image-alt and JSON-LD fields point to v2. No private voice references or raw audio renders are included.

The v5 audio edit removed only the spoken Rankin credit from the camp sentence; v6 subsequently adjusted the closing emphasis. The NBA official calendar supports the September 29 camp opening; media day retains its reported provenance in the source ledger. The approved ownership note/opening, all 39 existing editorial paragraphs, all 25 original headings, statistics, ten scan labels and original source entries remain protected by the hub-compatible tests. See `validation.md` for completed interaction checks and remaining human listening approval.

## Visual calendar

The Calendar view includes a Monday-first, three-week table for September 14–October 4, 2026. Copper marks Suns events; teal marks league events. The details retain Official/Reported labels, the source links and the original media-day/camp descriptions. The October 5 Detroit opener remains a reported next-up item. This is a selected edition calendar, not an exhaustive schedule or live calendar feed.

Calendar markup lives in `index.html`; scoped responsive/print styles live in `calendar.css`. No new JavaScript, navigation route, audio edit, third-party widget or calendar-account integration is involved. Run `node scripts/verify_issue_009_calendar.mjs` after calendar edits. Refresh the range, weekday alignment, source status and event details together in later editions.

## Tightened hub and Blender room — local review

The hero starts directly beneath the masthead: 16px to the edition lane on desktop and 14px on mobile. The former viewport-expanded, vertically centered title row caused the empty top band. `hub.css` now top-aligns the title and bounds the desktop hero row; mobile starts at the top and displays tile numbers 01–05. The five hash-routed sections, decision strip, standard player, approved writing and Calendar view remain unchanged.

Current hero assets are `assets/signal-room-v3-desktop.webp` (1920×1200) and `assets/signal-room-v3-mobile.webp` (900×1100). The existing Blender sculpture is extended with procedural court flooring, recessed walls and soft room lighting. Both crops place the sculpture high/right, with a shaded left reading area. No facility photograph or stock composite was introduced. V1/v2 assets and the locked smiling-Maluach OG v2 are preserved. The repeatable Blender source is `scripts/blender/build_signal_room.py`; private masters remain outside the release.

The two optional hero hotspots remain under the earlier keep instruction; their proposed removal is awaiting Mel’s response. Pages publication is authorized as recorded above.
