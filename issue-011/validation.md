# Issue 011 proof record

Status: technical review complete; awaiting Mel’s complete listening review and explicit merge approval. The live page still serves the previously published edition.

- House Qwen Arizona render passed the canonical factory gates and an independent scan: zero gaps at −50 dB lasting 0.30 s; zero digital-black intervals longer than 0.28 s. Spectrograms for 0–20, 20–40 and 40 seconds through the end were generated in private QA.
- Delivered MP3: 24 kHz mono, 160 kb/s CBR with Xing. ffprobe duration is 63.656458 seconds; edition.json and the manifest match exactly. Both audio and public transcript hashes are bound in the manifest.
- Local Whisper recognized the full eight-theme sequence, opening sentence and complete closing. It placed approximately 140 ms of natural air after Matt. ASR homophones included “son’s identity” for Suns identity and “will mean” for remain; pronunciation and perceived pace remain part of Mel’s listening review. No words were added to the public transcript for those recognition variants.
- The public transcript spells Mat with one T. Only the private TTS input uses Matt. The final standalone line is exactly “Much love, my brother, dominate!”
- The original shared player is copied byte-for-byte to the neutral shared assets/audio-player path. Its custom element and behavior are preserved. The Issue 011 eyebrow is Audio and title is the edition title only; no duration_seconds tag attribute.
- Ballmer JSON-LD datePublished is 2026-09-14T05:37:28Z, or September 13 at 10:37 p.m. Arizona. Silver JSON-LD is 2026-09-16T03:12:28Z, or September 15 at 8:12 p.m. Arizona. Cards, ISO time labels, builder and Source Ledger use September 13 and 15; Suns September 16 items remain unchanged.
- Home returns to the edition hub by the existing navigation contract. The repository root opens Issue 005, not a series index.
- All other body prose and direct quotations match the published main version. Historical editions and their shared original player remain unchanged. Arizona v4 remains as backup.
- After listening approval, merge and verify the Pages build, live update stamp, complete playback and download, dates, 390px view and exact live MP3 bytes before declaring publication complete.
- No client message was sent; repository visibility is unchanged.
