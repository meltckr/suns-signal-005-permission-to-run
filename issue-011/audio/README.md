# Issue 011 voice brief

The player now uses `suns-signal-011-elevenlabs-mel-az-feb2026.mp3` (78.95 seconds). It summarizes the philosophy feature and the issue's current Suns, league, and calendar material. The text remains `../content/audio-brief-transcript.txt`; the ElevenLabs same-basename metadata JSON records the new MP3 and existing transcript hashes.

The supplied ElevenLabs MP3 was kept intact. Local Whisper large-v3-turbo recognized the complete script and closing through 78.64 seconds; the file ends at 78.95 seconds. Its extra words with timestamps beyond the file duration were a recognition error. The 390px browser view stayed within the viewport, and playback plus both ±15 controls worked with byte-range serving. A full human listening pass remains required before release.

The former Arizona v4 MP3 and its metadata remain in this folder as a backup, unlinked from the player. V1–V3 and their render/ASR records remain in the separate local `production/issue-011/audio/` folder.
