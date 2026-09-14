# Suns Signal dimensional artwork

Design preview for Issue 009. Preserve the publication, source links, five-card scans, voice and player. This is a presentation-layer enhancement requested by Mel, not an editorial revision or new publishing system.

## Source and rendering

`build_signal_depth.py` creates original procedural geometry and materials in Blender 4.5.3 LTS. It follows the existing AVC Briefing Room method: Cycles CPU, fixed seed, denoising, AgX, then optimized WebP delivery. No external models or textures. The sculpture is illustrative; it is not a real facility, trophy, or statistical chart.

```sh
blender --background --factory-startup --python scripts/blender/build_signal_depth.py -- --output /absolute/path/to/private-art-masters --samples 64
cwebp -q 88 -m 6 -metadata none /absolute/path/to/private-art-masters/signal-depth-v1.png -o issue-009/assets/signal-depth-v1.webp
```

Keep `.blend` and PNG masters in the configured private art-master directory outside the public deployment. Source script is portable; Blender executable must be resolved in the active environment. No installation or system security changes are required.

## Web integration

- `issue-009/depth.css` is an additive, edition-scoped layer. Remove its HTML link to restore the prior surface treatment.
- The previous SVG hero remains available. The new WebP is 1600 × 1100 and 43,106 bytes.
- Light-facing edges, layered shadows, copper highlights and a full-width final scan card add dimensionality without changing reading order.
- A four-second, one-time hero camera-style reveal and pointer-only card lift supply restrained motion. Reduced-motion preferences disable transforms, transitions and smooth scrolling. No WebGL, new dependencies or ongoing animation loops.
- Existing article text, audio MP3/transcript/player, source ledger, OG image and deployment workflow stay unchanged.
- Player theme correction: `--player-bg` must remain a six-digit opaque color. The shared component uses it as a gradient color stop and play-icon color; assigning a gradient invalidates both and exposes the beige page under white text. Use opaque dark control surfaces and verify primary, muted and accent text contrast. The depth validator rejects this regression.

## Preview gate

Verify desktop and phone layouts, preserved visible text and links, no overflow, successful image loading, working audio controls, and existing Issue 009 tests. The preview has not been committed or deployed. Obtain Mel's approval before replacing the live edition or updating its approved share card.

## V3 architectural room extension

`build_signal_room.py` reuses the scene-construction portion of `build_signal_premium.py`, checks its final render-loop contract, and adds the room before rendering new files. Keep both source scripts together. V1 and V2 assets remain available.

The steps, pebbled basketball, copper/bronze surfaces and sun arc are unchanged. The V3 setting adds a procedural smoked-maple court, subdued illustrative court markings, recessed navy wall panels and broad ambient light. It is an original fictional setting, not a photograph, composite, real venue or measured court diagram. No external textures or models are used.

```sh
blender --background --factory-startup --python scripts/blender/build_signal_room.py -- --output /absolute/path/to/private-art-masters --samples 96
cwebp -q 90 -m 6 -metadata none /absolute/path/to/private-art-masters/signal-room-v3-desktop.png -o issue-009/assets/signal-room-v3-desktop.webp
cwebp -q 90 -m 6 -metadata none /absolute/path/to/private-art-masters/signal-room-v3-mobile.png -o issue-009/assets/signal-room-v3-mobile.webp
```

Desktop is 1920 × 1200, with the sculpture on the right and darker space on the left for text. Mobile is a separate 900 × 1100 composition. Keep PNG and `.blend` masters in the private art-master directory above. Inspect both optimized images before integration; verify file sizes, preserved sculpture detail, legible overlaid copy, correct responsive image selection and reduced-motion behavior. Publication still requires Mel's approval.
