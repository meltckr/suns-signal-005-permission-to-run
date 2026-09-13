# Issue 009 — review and release record

## Verified locally on September 13, 2026

- Base: canonical main, Issue 007. Prior editions, shared CSS and player unchanged; unfinished Issue 008 untouched.
- Editorial pass: removed old edition facts; restrained interpretation; no first-person claims, medical estimate, personnel prescription or broad fan sentiment claim. Calendar uses Sept. 28 / Sept. 29. Preseason broadcast corrected to Oct. 10 / ESPN2.
- Browser: 390×844 and 1280×800; no horizontal overflow; all page images loaded. A 32px top inset prevents hero text crowding. Same approved components and layout.
- Player: no autoplay; 1×, 1.5× and 2× verified; forward and backward skips, slider-to-end and playback through the end verified without media error. Local preview uses byte-range serving; the default Python server could not accurately test seeking and was not treated as a pass.
- Audio: approved Arizona v12 reference route and model, 35 sentence renders, protected sentence tails and natural pauses, 24kHz mono / 160kbps MP3. Duration 142.03 seconds (2:22); approximately 169 words/minute; delivered loudness −16.61 LUFS dual-mono, true peak −2.10 dBTP. No reference recordings or raw renders included in release.
- Automated transcription: complete sequence and exact closing words recognized. Names produced spelling variants; minor wording variants remain for listening review. Source sentences with short tails were checked against full-file recognition; recognition does not prove consonant naturalness.
- Share card: visually inspected; 1200×630 RGB PNG, versioned filename, central safe margins, correct issue/date/calendar and absolute OG/Twitter URLs.

## Required local commands

```sh
python3 scripts/validate_weekly_structure.py issue-009/index.html
node scripts/verify_issue_009.mjs
git diff --check
```

## Remaining listening gate

No perceptual listening review was available. Mel's listening approval, especially the opening, Khaman Maluach and Duane Rankin, and the closing, remains pending. Technical transcription, loudness and browser playback checks must not be described as human listening approval.

## Release boundary

Deliver as a public review edition on the existing GitHub Pages product, not as a sent client communication. Do not send the drafted iMessage. Verify live HTML, PNG and MP3; compare audio and image hashes, byte-range delivery and player source after publishing. The final clean link and review link are the same permanent issue URL, with review status disclosed to Mel.
