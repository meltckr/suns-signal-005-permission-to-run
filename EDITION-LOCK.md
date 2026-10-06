# Suns Signal Edition Lock

**Product of record:** Issue 009, “The Next Step Starts Early”

**Approved release date:** September 14, 2026

**Canonical release commit:** `d1aadbced3cf72462eb9430d1159587e280d8a0a`

**Permanent public URL:** <https://meltckr.github.io/suns-signal-005-permission-to-run/issue-009/>

Issue 009 is the last shipped Suns Signal product standard. Every future issue must begin with its shell. Preserve the system. Refresh the edition.

This is a product lock, not a content lock. Future commissions replace the reporting, analysis, title, dates, hero treatment, lead-player photograph, OG card, audio, sources, and client note. They inherit the architecture and release gates below.

Use `/Users/meltucker/.codex/skills/suns-signal-weekly/SKILL.md` as the operating manual and `/Users/meltucker/.codex/skills/avc-audio-module/SKILL.md` as the audio implementation standard. This file remains the repository product lock. If instructions drift, reconcile them to the shipped Issue 009 shell and the approved audio standard before starting a new edition.

## Mandatory product inheritance

### Design and UX

- The command-deck hub is the first viewport on desktop and approximately 390-pixel mobile screens.
- Keep the premium Blender hero with in-room court depth. Extend the scene for the new edition; do not paste a stock or photoreal Suns practice-facility still behind it.
- Use the facility references in `voice/og-source/facility-ref/` only to study in-scene depth, scale, wood tone, ceiling height, glass, and light. Their status is **REFERENCE ONLY**.
- Keep the audio module on the hub. Seeking and the `−15` and `+15` controls must work.
- Player chrome uses the eyebrow `Listen` or `Audio`. The track title is the edition title. Never label the player with `Mel`, `Mel Tucker`, another personal name, or an engine/provider name.
- Keep five section tiles on the hub:
  1. Ownership / First read
  2. Suns Weekly Pulse
  3. Around The League
  4. Calendar Ahead
  5. Source Ledger
- A tile opens its section. Each section keeps the sticky `← Home` / Suns Signal control back to the hub.
- Preserve the hash routes `#hub`, `#ownership`, `#pulse`, `#league`, `#calendar`, and `#sources`. Deep links must open the requested section.
- Keep one edition lane beneath the masthead. Remove redundant `Suns Signal Weekly` kickers and any floating second Suns logo.
- Keep a decision strip with one to three short ownership signals. It is a scan layer, not a second article.
- Collapse dead space below the masthead. The first viewport must hold the tightened hero, decision strip, audio, and tiles 01–05.

The locked Issue 009 shell consists of `issue-009/index.html`, `styles.css`, `depth.css`, `premium.css`, `hub.css`, `calendar.css`, `hub.js`, `premium-motion.js`, and the responsive Blender hero assets. Do not redesign the hub for a routine new issue.

### OpenGraph and share presentation

- Use a 1200 × 630 share card with the visual hierarchy of a strong YouTube thumbnail: a short hook and a real photograph of this edition’s lead player.
- Follow the Issue 008/009 player-card pattern: full-bleed player photography, immediate contrast, mobile legibility, and no clutter.
- The card creates the hook; it does not repeat the page title verbatim without a reason.
- Spell `Mat` with one T on every card and in all metadata. Never use `Matt` for Mat Ishbia.
- Keep prior OG versions when a card is recut. Add a new version and update `og:image`, Twitter metadata, JSON-LD, and descriptive alt text together.

### Voice and copy

- Write as an experienced outside consultant helping Mat and ownership see the situation more clearly. Always `Mat`, never `Matt`.
- Use the Gladwell method, not a costume: one concrete detail, one turn between what something looked like and what it reveals, a plain-English name for the pattern, then stop.
- Apply the September 13 anti-hedge lock. Do not use the “this is X, not Y,” “what this is not saying,” or “what this does not mean” loop. State what the evidence means, may mean, or what to watch. Use soft language only when the evidence is soft.
- Preserve `Official`, `Reported`, and `directional` labels. Separate fact, interpretation, uncertainty, and next evidence.
- Apply the global `mel-tucker-voice`, `mel-executive-writing`, humanizer, humanizer-voice, unslop, and humanize-ai-writing standards to the page and transcript.
- Final Buzzer remains score-first and contains no audio, quotes, or sentiment. Do not import Final Buzzer constraints into the weekly product beyond that boundary.
- Cut fan, scout, and pundit posture. Cut canned phrases including `game changer`, `elite mentality`, and `must-win`.

### Audio

- Use the Studio Qwen3-TTS **AVC Arizona Voice v12** recipe for Suns Signal narration: model `mlx-community/Qwen3-TTS-12Hz-1.7B-Base-8bit`, rendered through `/Users/meltucker/avc-tools/avc-audio-render.sh`, with the approved declarative reference pair `/Users/meltucker/avc-tools/breeze-proof/mel-az-2026-decl-18s.wav` and `/Users/meltucker/avc-tools/breeze-proof/mel-az-2026-decl-18s.txt`. Do not use the full 66-second source, the 10-second kittens clip, a greeting/consent clip, or the default punch clip. ElevenLabs, Chatterbox, Breeze, Gemini stock voices, and other substitutes remain off for new renders unless Mel explicitly names one for that edition.
- Keep visible Suns copy spelled `Mat`. A temporary private TTS input may spell the name `Matt` when that pronunciation is required; never carry that spelling into page copy, transcript display, metadata, OG, or the iMessage.
- End every transcript and delivered audio file with this exact standalone final line:

  `Much love, my brother, dominate!`

- After any transcript edit, create a new versioned MP3 filename. Synchronize the transcript, player `src`, matching metadata manifest, README, and client note.
- Run:

  ```bash
  python3 scripts/validate_weekly_structure.py issue-<n>/index.html
  ```

- A release remains incomplete until the final approximately ten seconds have been checked for the complete spoken sign-off. A file that exists is not proof that the close is audible and unclipped.

### Release and client handoff

- The supported destination is the public GitHub Pages path backed by the canonical repository: `https://meltckr.github.io/suns-signal-005-permission-to-run/issue-<n>/`.
- Do not use ChatGPT Sites, `visbrk`, Netlify, Vercel, or a new repository for a normal edition.
- Preserve every permanent prior-edition URL.
- Prepare `issue-<n>/imessage.txt` for Mel to review and send. Never send it automatically.
- The iMessage should lead with an evidence-supported positive takeaway, explain the central ownership pattern, identify the timely Suns updates, mention directional sentiment when present, include the Around The League scan and audio brief when present, and use the clean permanent URL.
- Do not push a live Pages release until Mel says yes and the chief-of-staff proof is complete: final copy, `Mat` with one T, prior-edition isolation, story-specific OG, MP3 hole scan, full audio listen, and mobile/desktop product proof.
- Committing a production issue, merging a Pages branch, or otherwise changing the live site requires explicit approval. A lock or draft PR does not authorize a live release.

## Scope fence

Do not turn this factory into:

- a multi-edition always-on platform;
- a generative-AI ask-to-visualization product;
- an Omniverse or pixel-stream experience;
- a new bot; or
- a new repository.

## Starting a future edition

Run the scaffold from the repository root:

```bash
./scripts/new_issue_from_009.sh <issue-number>
```

Use digits only; the script zero-pads the directory name. It refuses to overwrite an existing issue and refuses to modify Issue 009. It performs these bounded actions:

1. Copies `issue-009/` to the new permanent issue directory.
2. Preserves the hub, route logic, responsive CSS, premium/depth layers, calendar shell, shared audio component, and responsive Blender room base.
3. Replaces the Issue 009 story, weekly scans, calendar entries, sources, dates, title, metadata, decision strip, audio path, transcript, OG references, README, validation record, and iMessage with explicit placeholders.
4. Removes Issue 009 audio, OG cards, lead-player photography, and other edition-specific artwork from the new directory.
5. Leaves the new issue visibly and technically incomplete until fresh reporting, imagery, audio, and verification are supplied.

The scaffold intentionally does not create a topic or claim that the new issue is release-ready. Fill every `[[REPLACE: ...]]` marker, generate a new story-specific hero and OG card, generate versioned Arizona v12 audio, then run the weekly validator and the release proof.

### Factory regression check

Before using or changing the factory, run:

```bash
python3 scripts/verify_factory_lock_009.py
```

This check protects the Issue 009 product-of-record files, required routes, player label, audio controls, voice provenance, and factory instructions. If it fails, stop and reconcile the drift before scaffolding a new issue.

## Provenance retained in the repository

- `voice/ISSUE-009-HUB-OPTION-B.md` records the approved command-deck decision.
- `voice/OG-009-MALUACH-BRIEF.md` records the Issue 009 share-card direction.
- `voice/AVC-Gladwell-voice-pack.md` and `voice/CODEX-GLADWELL-PROMPT.md` preserve the method calibration; they are posture references, never a source of reusable facts or copied prose.
- `voice/og-source/PRIMARY-maluach-summer-league.jpg` preserves the approved Issue 009 OG source photograph.
- `voice/og-source/facility-ref/` contains reference-only room-depth material. The Blender scene must be rebuilt in-scene; the facility photographs must not be pasted into the hero.
- `voice/CODEX-LOCK-FACTORY-FROM-009-PASTE.txt` preserves the original Issue 009 factory-lock commission.
- `voice/CODEX-UPDATE-SUNS-SIGNAL-WEEKLY-SKILL-PASTE.txt` preserves the commission that aligned the installed skill and Arizona v12 audio standard with this lock.

These files explain how the standard was reached. They do not authorize reusing Issue 009 facts, title, player, dates, or conclusions in a later edition.
