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
node scripts/verify_issue_009_depth.mjs
node scripts/verify_issue_009_premium.mjs
node scripts/verify_issue_009_hub.mjs
node scripts/verify_issue_009_calendar.mjs
git diff --check
```

## V8 pronunciation listening gate — complete

Mel listened to the final v8 release-chain audition on September 13 and approved the corrected Maluach pronunciation and delivery: “That sounds a lot better. Let’s go with that.” V8 remains the approved source for sentences 0–22 in v11.

## Release boundary

Mel initially held the recut for local review. On September 13 he explicitly authorized GitHub Pages publication to enable iPhone review. That authorization supersedes the historical local-only holds below. The drafted iMessage remains unsent. Verify live HTML, PNG, WebP and MP3 against the authorized build, including hashes, byte-range delivery and player source; merging alone does not establish a completed deployment.

## V11 declarative closing — approved release

- Sentences 0–22 are byte-identical to approved v8, including both Mel-approved Maluach sentences. Sentence 23 is the complete approved terminal take; 700ms of silence is added after its source ends. No word splice, speech fade, truncation or overlapping join is used.
- Source-line ASR recognizes `Much love, my brother. Dominate.` once. Final-ten-second ASR also ends with one complete `Dominate.` Full-file Whisper emitted repeated zero-duration or out-of-bounds tail segments for the emphatic isolated word; these are recorded as a recognition limitation. Decoded PCM is silent across the final 300ms.
- The source take has a 600ms lead-in pause, a 600ms final-word span, 1.261× phrase RMS and a 17.5% falling pitch contour. Mel approved the exact performance by listening and then said, “That’s much better. All right let’s publish it.”
- V11 duration: 103.423 seconds; 24kHz mono; 160kbps; −16.63 LUFS; −2.19 dBTP. MP3 SHA-256: `b053e7579853046d9f89b01a08a95c68d53f17a86fc4a321c210411791288d64`. Manifest SHA-256: `ca5bfee21e13218371a9b5555ef9715fe839d1f6af2b2384de99b30159aa61b1`.
- V7 and v9 were rejected full masters; v10 was a rejected question-cadence audition only. The player and versioned metadata now use v11. V1–v9 remain preserved. GitHub Pages publication is authorized; the client iMessage remains unsent.

## Approved writing recut — v3, September 13

- Applied the approved ownership note and audio opening, then recut page prose and narration for natural cadence and direct explanation. Retained uncertainty where supported, all ten dated reporting labels, source links, the source ledger, calendar and numerical facts. This was an editorial preservation pass, not a new reporting-window refresh.
- Removed the client-facing Next Watch section. Research prompts stay in private production notes outside this repository. Renamed the abstract rail labels to Reporting Period, Williams Update and Why It Matters, with direct explanations underneath.
- Preserved the locally approved Blender artwork, depth CSS and opaque high-contrast audio panel. Shared player code, original v1/v2 MP3s, OG artwork, metadata URLs and prior editions are unchanged.
- Rebuilt all 31 sentences in the approved Arizona v12 voice, retaining the pronunciation alias and exact closing. Each context cut occurs inside a measured quiet gap after the recognized final word. Minimum accepted quiet run: 141ms. Three initial unsafe gaps triggered rerenders; the gates were not relaxed. Two additional sentences were rerendered for wording checks. No speech fades or overlapping joins.
- V3: 341 words, 128.915 seconds (2:09), 24kHz mono, 160kbps, approximately 159 words/minute, −16.62 LUFS dual-mono, −2.16 dBTP. Player, transcript, manifest and README point to the new version; the positive iMessage draft is updated and unsent.
- Full-file ASR recognized the content sequence, numerical claims, dates and exact closing words. It hallucinated extra text within the last fraction-second of silence. Independent recognition of the final ten seconds ended correctly with the sign-off; the final 300ms measured effectively silent (peak 0.000000750). Proper-name spelling variants remain an ASR limitation. No perceptual listening approval is claimed.
- Browser checks: desktop 1280px and mobile 390×844 had no horizontal overflow or missing images. V3 loaded without autoplay; play/pause, 1.5×, return to 1×, seeking, backward skip and playback through the final 15 seconds passed without media error. Browser duration was approximately 129 seconds.

## Current-global-standard writing recut — historical v4 checkpoint

- Mel approved the revised ownership note and audio opening. Both are applied verbatim. The full page and transcript follow the current Mel voice, anti-hedge and humanizer standards: concrete evidence, plain explanations, varied sentence length and qualified interpretation where warranted.
- A separate editorial comparison against the published base found two final corrections: restore “with” in the Grange report to avoid adding a causal claim, and state the source scope positively. Both are applied. Existing reporting facts, quotations, dates, numerical claims, source entries, URLs and Official/Reported/directional labels are preserved. This pass does not refresh or newly verify the reporting window.
- A second read-only editorial check passed after those corrections. It confirmed both approved passages exactly, natural cadence, preserved factual qualifications and no remaining substantive editorial issue. Browser checks at 390×844 and 1280×800 confirmed the current copy, all ten scan cards, 15 source entries, loaded images and no horizontal overflow.
- The ownership idea remains that Williams’s surgery raises the value of earlier depth work. No rotation advice, medical prediction, invented scene or first-person claim was added. The client-facing Next Watch section remains removed; `Listen`, `Mat` and the exact standalone closing remain intact.
- The approved Option B hub and locked-photo OG v2 briefs were located in the canonical checkout’s `voice/` directory. Mel temporarily prioritized completing writing and narration before the UI rebuild. The subsequent FULL BELLS authorization superseded that pause. No publication is authorized.
- V4 narration: 309 words, 24 sentences, 106.624 seconds (1:47), 24kHz mono, 160kbps, −16.63 LUFS dual-mono and −2.17 dBTP. Seventeen source clips were newly rendered; seven exact transcript matches were reused. All 24 sentence endings passed measured quiet-gap checks; the minimum accepted run was 127.83ms. No speech fades or overlapping joins. Full-context ASR supports the wording, with recognition variants documented in the manifest. Independent recognition of the final ten seconds ends with the exact closing; the final 300ms is effectively silent. Perceptual listening approval remains pending.
- Player, transcript, versioned manifest and README are synchronized. Local HTTP returned the matching transcript hash and a 206 byte-range response for v4. Browser play/pause, 1.5×, return to 1×, seeking, both ±15-second buttons and playback through the final 15 seconds passed without media error. No autoplay occurred. The MP3 remains distinct from v1–v3; all prior versions are preserved.

## FULL BELLS — current local review

- Built the requested hash-routed command deck in the same issue and worktree. The original editorial material is now available through five section views. Home/Listen remain in the sticky header; Escape and legacy hash aliases return through the same router. The shared audio element stays mounted once. No shared player code or earlier issue changed.
- Desktop 1280×800 and mobile 390×844 both fit the hub, audio and five tiles within one viewport. Mobile document dimensions are 390×844; the final tile ends at y=778 and the audio at y=612. Desktop document dimensions are 1280×800; audio and tiles end at y=776. Images loaded. The mobile header overflow found on first proof was corrected by permitting the date to wrap. No content was hidden to mask overflow.
- All five desktop and mobile tiles opened the correct isolated view and Home restored the hub and originating tile focus. Section pages had no horizontal overflow. A fresh `#league` deep link, Escape return, Sources with 16 entries and sticky Listen-to-player focus passed. The actual router is also tested in a DOM fixture for every destination, legacy aliases, unknown fragments and inherited-property edge cases; the latter were found in code review and fixed with own-key lookup.
- OG v2: 1200×630 opaque RGB PNG, 697,788 bytes, SHA-256 `b5ffa0dc8cfb02b70b0a995a6950d4012cf0e200c4321597550a690fe3e77a34`. Locked smiling Maluach photo SHA-256 `88d88ac4f3fd11b99781b1ef94d66893b84c9c50375805e055a377be326e231e`. Full-size and thumbnail review passed; metadata/alt/JSON-LD updated. V1 remains unchanged.
- V5 narration changes only the training-camp attribution. 304 words, 103.839 seconds, −16.61 LUFS dual-mono, −2.17 dBTP. One sentence newly rendered, 23 raw clips reused byte-for-byte. All 24 quiet tails and the final ten seconds passed technical checks; no speech fades or overlapping joins. Human listening remains pending. Player/manifest/transcript/README are synchronized.
- Content preservation tests lock the approved paragraphs, headlines, statistics, calendar, source labels and original sources while accepting the authorized shell. Mutation controls reject changes to those facts, copy, sources, player identity and canonical URL. The source record now distinguishes the official NBA camp date from reported Suns media day. No new reporting-window refresh was performed.
- Mobile v5 controls passed play/pause, seek-to-start/end, exactly 15-second forward/backward jumps and speed selection. Playback continued while entering League with exactly one audio instance, and Listen returned to the player. Local MP3 hash matched the manifest, byte-range requests returned 206, and OG v2 returned 200 `image/png`. This is local verification, not a Pages release or perceptual listening approval.
- V5 browser playback reached the end without media error. At the review panel’s native 1154×1324 size, the hub also fit the viewport with audio and tiles ending at y=1300. The updated hub was opened in the existing review tab. The superseding v6 closing emphasis is documented below after its technical checks.

## V6 — closing emphasis

- Regenerated only the closing sentence in the approved Arizona v12 voice. The other 23 source clips are byte-identical to v5, and the full transcript is unchanged. The selected take extends “dominate” to approximately 407ms versus 278ms in v5, with approximately 148ms preceding pause. These are recognition-based timing estimates, not perceptual approval. An alternate take failed exact-word recognition and was rejected.
- Delivered duration: 103.914 seconds. Loudness: −16.59 LUFS dual-mono; true peak: −2.20 dBTP. All 24 sentence tails pass the existing checks. Full-file and final-ten-second recognition preserve the exact closing. No speech fades or overlapping joins. Mel’s listening review remains pending.
- MP3 SHA-256: `abef267c012bc66985b86a6c910aa3f8567bb98bf531534612a3b49569a9bc3b`. Manifest SHA-256: `90e39f231967e2a674a67a843e5f8ce39f154d1bb0b6ecb50295a09582133d60`. Unchanged transcript SHA-256: `ce59afbf7018ea8c92964185920586946e428c43fc8febff049af224f947e5af`.
- Player, README, manifest and artifact checks now reference v6. V1–v5 remain preserved. No publication is authorized.
- All five local verification commands passed after v6 synchronization, along with the router syntax check and `git diff --check`. The freshly loaded review hub used v6 with no autoplay. Seek-to-end, backward 15 seconds and playback through the closing completed with `ended: true`, no media error and one player instance. The local server returned HTTP 206 for a v6 byte-range request. These checks establish technical delivery, not perceptual listening approval.

## Visual Calendar — local review

- Added the requested three-week visual within the existing Calendar route. September 14–October 4 has 21 consecutive Monday-first cells and seven event markers: the two-day owners’ meeting, two events on September 22, media day, camp opening and NBA preseason opening. An October 5 next-up item retains its Reported label. Copper and teal distinguish Suns and league events; status is explicit in the details and accessible labels.
- Reopened NBA key dates and the Suns open-house listing. A separate date/source review confirmed weekday alignment and the source classifications. ESPN’s original Windhorst report was accessible and added to the visible source ledger, which now has 17 entries. The original 16 entries and all existing editorial paragraphs remain intact. No vote is promised, and no team-reporting date is used to upgrade Suns media day to Official.
- Independent review found two presentation issues before handoff: mobile event badges needed a naming-supported accessibility role, and early-camp/preseason abbreviations needed more precise wording. Corrected both. The browser accessibility tree now exposes each complete event name and status on mobile. The calendar remains a static semantic table; no third-party calendar, account write or new JavaScript was added.
- Desktop 1154px and mobile 390×844 visual checks passed with no horizontal overflow. The calendar grid is fully visible in the mobile first screen. Calendar-to-Pulse and sticky Home navigation passed; the returned mobile hub still measures 390×844 with v6 audio unchanged. The updated Calendar was opened for review.
- The new `verify_issue_009_calendar.mjs` checks date continuity, Monday-first columns, event/date/status mappings, full accessible labels and responsive/print styles, then applies the existing editorial/audio preservation lock. It and all five existing issue/structure/depth/premium/hub commands passed, as did `git diff --check`. No commit, push, publication or message was made.

## Tightened hub and Blender room — local review

- Before: the native 1154×1324 review placed the title block at y=445, below a 72px masthead. The first grid row expanded to 801px and centered the intro. After: the title block starts at y=88 (16px gap), with a bounded hero row. The 390×844 phone view has a 14px gap. No fixed-height clipping or hidden navigation was used.
- Extended the same procedural Blender sculpture through `build_signal_room.py`, keeping the v2 construction and materials. Added court flooring/paint, architectural wall depth and ambient light; no photograph, external model, texture or real-facility claim. Desktop and mobile compositions were separately exported and visually inspected by the renderer, root and an independent reviewer. Private PNG/.blend masters stay outside the release.
- Desktop WebP: 1920×1200, 120,144 bytes, SHA-256 `c783933aa109c58390821af6ecc56506ad2d429b49dac3bd656034f2670c3020`. Mobile: 900×1100, 56,692 bytes, SHA-256 `8abbb1a536ed424d1ee9e64ec5e40e98c4b799c979bfb87abdfe59a21cc26d71`. Both are under the 150KB per-image budget. Responsive `picture` paths and illustration alt text match v3. V2 and the smiling-Maluach OG v2 remain unchanged.
- Final in-app browser proof: 1280×800 document equals viewport, hero gap16px, audio and tiles end at y=779.719. Phone390×844 document equals viewport, hero gap14px, audio ends at y=562.656 and tiles at y=728.656. All five numbered tiles are visible. Both correct responsive images load, and the new room setting is visible above the controls. Native1154×1324 also passes top alignment and fit.
- All six local verification commands pass after integration, along with `git diff --check`. The depth check now requires the v3 responsive pair, preserves old-asset budgets and rejects reintroducing centered title alignment. Editorial paragraphs, sources, calendar, v6 narration/transcript, shared player and OG v2 remain protected by existing locks. Mel later approved removing the two optional hero hotspots; the five numbered section tiles are the hub’s sole section-entry controls. No commit, push, Pages publication or message was made.
- On the final v3 hub, desktop forward/back controls moved from0 to15 and back to0; seeking and playback through the final15seconds reached `ended:true` with no media error. Phone forward/back, seek-to-end/start and play/pause were exercised; the player was left paused at0. Calendar tile and sticky Home returned through the existing hash router with focus restored to Calendar and one player instance. Browser viewport overrides were reset before handoff.

## V7 — Maluach pronunciation repair

- V7 attempted to follow the written `kah-mahn mahl-oo-ahch` guide literally. Its hyphens and capitalized `OO` forced the surname into slow, separate acoustic chunks. That contradicted Maluach’s own connected delivery, heard as `kah-MAHN mahl-WAHCH`. Mel rejected v7 after listening. V7’s metadata also overstated the player recording’s role: the NBA clip was comparison evidence, not an acoustic synthesis reference.
- Regenerated complete sentences 0 and 5 in AVC Arizona Voice v12. The other 22 raw source clips are byte-identical to v6. Each replacement was cut only after the final word inside a measured quiet gap: 192.5ms for sentence 0 and 200.08ms for sentence 5. Every one of the 24 sentence tails retains at least 100ms of verified quiet room; the minimum is 127.83ms. No token splice, speech fade or overlapping join was used.
- V7 duration: 104.574 seconds; 24kHz mono; 160kbps; −16.74 LUFS; −2.19 dBTP. MP3 SHA-256: `da80296540508cb7e471f395ae5d88ba46c8cca654ab7645f1f462a6a2bc336d`. Manifest SHA-256: `3e110e3a37ad999f8a5f594f3a0a63a714a592375019a9ff2236b9360f4bc30e`. Transcript SHA-256 remains `ce59afbf7018ea8c92964185920586946e428c43fc8febff049af224f947e5af`.
- Full-file recognition preserved the content sequence and required closing, and the last 300ms was effectively silent. Those technical results did not establish natural pronunciation; Mel’s listening review identified the failure.
- The actual local player loaded v7 without autoplay, exposed one audio instance and reported no media error. The ±15-second controls and position slider worked; playback crossed both corrected sentences and reached the complete ending with `ended: true`. A direct v7 byte-range request returned HTTP 206.
- V7 remains preserved as rejected history. The player and current checks must not return to it.

## V8 — connected Maluach pronunciation approved by Mel

- Research hierarchy: Maluach’s player-recorded NBA clip is the listening authority; the official NBA guide and Suns game notes print `kah-mahn mahl-oo-ahch`; his natural connected delivery compresses `oo-ah` into the glide heard as `kah-MAHN mahl-WAHCH`. The synthesis used the approved private Mel reference only. The NBA clip was not fed into the voice model.
- Regenerated complete sentences 0 and 5 with the connected production input `Kahman Malwatch` / `Malwatch`. The selected full-name span is 0.80 seconds; the surname-only span is 0.60 seconds. Sentence 5 preserves “points and nearly thirteen rebounds.” The other 22 raw clips remain byte-identical to v6, including the approved emphatic closing.
- V8 duration: 102.919 seconds; 24kHz mono; 160kbps; −16.59 LUFS; −2.19 dBTP. MP3 SHA-256: `4d30a8f64dbc60f750dc372dfe4dc6881b3e93265540e48176db0880cca23229`. Manifest SHA-256 after recording Mel’s approval: `6c05b20bc20ab38624a7bd768f5f4b8e4386447f12881391aa36a3f2eccffb0f`. Transcript SHA-256 remains `ce59afbf7018ea8c92964185920586946e428c43fc8febff049af224f947e5af`.
- The replacement sentences end inside measured quiet gaps of 173.96ms and 218.25ms; the minimum verified quiet run across all 24 sources is 117.83ms. No token splice, speech fade or overlapping join was used. Independent final-ten-second recognition ends with the required close, and the final 300ms is effectively silent.
- Mel approved the 10.582-second release-chain audition on September 13: “That sounds a lot better. Let’s go with that.” V8 is the approved local player source. No commit, push, GitHub Pages deployment or client message has been authorized.

## Authorized public release — September 13

- Mel approved publication after confirming that the local preview could not open on his iPhone. Use the permanent `meltckr.github.io` issue URL, never a repository, pull request or localhost link for review.
- GitHub Pages is public, HTTPS enforced, serving `main` at repository root through its existing Pages build and deployment workflow. The release worktree matched current production commit `c0b2d19ca5b1ee5f80b63e47f2582ceacf49cace` after a fresh fetch. Recent Pages deployments succeeded. No hosting or workflow change is needed.
- All six local validation commands passed again immediately before release. Internal `voice/` briefs, private references, raw renders and art masters are excluded. Release source and verification scripts are included with the finished public assets. Mel subsequently approved removing the two redundant hero shortcuts; the five numbered section tiles remain.
- Publication approval is for the edition and public review link. No client message is sent, and technical audio verification is not described as Mel’s listening approval.
- A bounded pre-publication source refresh found no material contradiction or changed load-bearing fact. Official/named reporting supported the injury, calendar, disciplinary, pending-transaction and television claims. Original or syndicated reporting covered access-limited pages. The earlier qualitative sentiment sample is preserved; this pass did not reconstruct every nested social reply or claim a refreshed survey. See `sources.md` for limitations.

## Combined V4 room and V8 audio — local proof

- Rebuilt the same procedural scene through `scripts/blender/build_signal_room_v4.py`. The V4 camera is low perspective; the scene adds converging floor cues, a ceiling and beams, warm coves, a distant glazed office band, warm/cool side light and a bounded low-density atmosphere. The steps, basketball and copper ring remain the focal objects.
- The private facility stills supplied only general spatial reference. Blender does not load them, and no photograph, player, logo, external texture or real-facility plate appears in the deliverables.
- Desktop WebP: 1920×1200, 77,482 bytes, SHA-256 `5799537b4e799f3c158defcc15a5d77cca127e945cf3297287639f1a762d8f5b`. Mobile WebP: 900×1100, 42,258 bytes, SHA-256 `e74ced4f78a87606001b7189f1049e0cdf39109fd24a8d7652a00e4bae301946`. Both are sRGB and below the existing 150 KB budget; raw PNG and `.blend` masters remain private.
- Final full-quality masters and optimized WebPs were inspected at native dimensions. The desktop composition preserves a dark left reading area and places the metaphor on the right. The mobile composition retains the complete ring, ball and steps while adding foreground floor distance and far-wall depth.
- The combined `index.html` uses both V4 responsive hero sources and the approved v8 audio file. V1–V3 art and v1–v7 audio remain present. Hub CSS/JavaScript, section tiles, decision strip, page copy, transcript and OG v2 are preserved.
- Browser proof and all six existing validation commands plus `git diff --check` must pass again on the combined build before handoff. It remains local and unpublished until Mel separately approves GitHub Pages.

## V9 — emphatic closing candidate rejected by Mel

- Regenerated sentence 23 as one complete line in AVC Arizona Voice v12. Sentences 0–22 are byte-identical to approved v8, including the two Mel-approved Maluach sentences. No word-level splice, speech fade or overlapping join was used.
- The selected take uses a 560ms pause before `Dominate!`; the source word spans 600ms and measures 1.11× the RMS of the preceding phrase before mastering. The complete line was cut inside 180ms of measured quiet audio after the final word and before the guard phrase.
- V9 duration: 103.189 seconds; 24kHz mono; 160kbps; −16.64 LUFS; −2.19 dBTP. MP3 SHA-256: `c7a2086dc04809906d22bcb6b30e142cb534a79515af5dde1c0b8ffd8072be44`. Metadata SHA-256 after recording Mel’s rejection: `dbaeb1c9361be345d3e2e90a6172988662bd8ef4a688efa52f4c800b9b801d0a`.
- Source-line and final-ten-second ASR each recognize the complete closing once. Full-file Whisper emitted repeated low-confidence micro-segments for the strongly isolated final word; that limitation is recorded in the metadata rather than presented as spoken repetition. The final 300ms PCM peak is effectively zero.
- Mel rejected v9 after listening because the pause created separation without enough conviction or enthusiasm in the final word. The player stays on approved v8. No commit, push, Pages publication or client message is authorized by this audio request.
