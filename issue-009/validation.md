# Issue 009 — review and release record

## Verified locally on September 13, 2026

- Base: canonical main, Issue 007. Prior editions, shared CSS and player unchanged; unfinished Issue 008 untouched.
- Editorial pass: removed old edition facts; restrained interpretation; no first-person claims, medical estimate, personnel prescription or broad fan sentiment claim. Calendar uses Sept. 28 / Sept. 29. Preseason broadcast corrected to Oct. 10 / ESPN2.
- Browser: 390×844 and 1280×800; no horizontal overflow; all page images loaded. A 32px top inset prevents hero text crowding. Same approved components and layout.
- Player: no autoplay; 1×, 1.5× and 2× verified; forward and backward skips, slider-to-end and playback through the end verified without media error. Local preview uses byte-range serving; the default Python server could not accurately test seeking and was not treated as a pass.
- Audio: approved Arizona v12 reference route and model, 35 sentence renders, protected sentence tails and natural pauses, 24kHz mono / 160kbps MP3. Duration 142.03 seconds (2:22); approximately 169 words/minute; delivered loudness −16.61 LUFS dual-mono, true peak −2.10 dBTP. No reference recordings or raw renders included in release.
- Automated transcription: complete sequence and exact closing words recognized. Names produced spelling variants; minor wording variants remain for listening review. Source sentences with short tails were checked against full-file recognition; recognition does not prove consonant naturalness.
- Share card: visually inspected; 1200×630 RGB PNG, versioned filename, central safe margins, correct issue/date/calendar and absolute OG/Twitter URLs.

## September 13 review corrections — v2

- Supersedes v1's tail-protection assurance: adding silence after a short source clip did not establish that the spoken word itself was complete. Mel reported clipped endings and incorrect Maluach pronunciation.
- Regenerated 13 source sentences, including both name mentions, with additional spoken context. Removed that context only inside measured quiet gaps of 132–537ms after recognized final words. Rejected and regenerated one replacement without a safe gap. Retained the other 22 original source WAVs in full; no trimming or fading of their speech, no overlapping joins. Added 180ms quiet buffer per sentence.
- Spoken name alias: Kah-mahn Mah-loo-watch; visible transcript unchanged. The delivered surname now transcribes with a watch ending. Full-file ASR preserves the content sequence and closing but has name/contraction variants and an apparent extra “Next” near “context”; exact diction still needs Mel's listening review. Do not treat transcription as a perceptual pass.
- Versioned v2 MP3: 149.954 seconds, 24kHz mono, 160kbps, −16.55 LUFS dual-mono, −2.12 dBTP. Original v1 preserved. Full spoken closing recognized. Local player checked through its last 15 seconds to completion without a media error.
- Five sourced cards in Suns Weekly Pulse and five in Around The League. Current event listing is distinguished from a newly dated announcement; new social observations remain self-selected and nonrepresentative. Added source-ledger and iMessage details; audio stays a concise summary rather than reading all ten cards.
- 390×844 and 1280×800 checks: no horizontal overflow; ten cards present. Existing styles, shared audio player, main feature, transcript and OG image unchanged.
- Issue validator now resolves the player’s actual audio source and checks five cards per scan, pronunciation alias and measured quiet-gap records. Required closing gate initially failed before completion verification and was retained, not bypassed.

## Required local commands (current)

```sh
python3 scripts/validate_weekly_structure.py issue-009/index.html
node scripts/verify_issue_009.mjs
git diff --check
```

## Remaining listening gate

No perceptual listening review was available. Mel's listening approval, especially the opening, Khaman Maluach and Duane Rankin, and the closing, remains pending. Technical transcription, loudness and browser playback checks must not be described as human listening approval.

## Release boundary

Deliver as a public review edition on the existing GitHub Pages product, not as a sent client communication. Do not send the drafted iMessage. Verify live HTML, PNG and MP3; compare audio and image hashes, byte-range delivery and player source after publishing. The final clean link and review link are the same permanent issue URL, with review status disclosed to Mel.
