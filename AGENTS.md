# Suns Signal Weekly Project Instructions

Preserve the established Suns Signal Weekly architecture, permanent issue URLs, prior editions, metadata system, standard Mel audio module, and GitHub Pages release workflow.

## Required audio closing

Every narrated Suns Signal Weekly transcript and delivered audio file must end with the exact words:

`Much love, my brother, dominate!`

Place that sentence on the final standalone nonempty transcript line. Do not paraphrase it and do not place spoken words after it. After any transcript edit, regenerate the audio under a new versioned filename, keep the transcript, player source, metadata manifest, README, and client note synchronized, then run:

```bash
python3 scripts/validate_weekly_structure.py issue-<n>/index.html
```

The release is not complete until the final ten seconds have been checked for the full spoken sign-off.

## Audio player label

Use `eyebrow="Listen"` as the visible label for narrated Suns Signal players. Do not use `Mel Tucker audio` as visible interface copy.

## Required client iMessage

Every published Suns Signal issue must include a ready-to-send `issue-<n>/imessage.txt`. Lead with an evidence-supported, positive and encouraging takeaway before describing uncertainty or risk. Briefly explain what the edition contains, including the central ownership pattern, timely Suns updates, directional sentiment when present, the Around The League scan, and the audio brief when present. Include the clean permanent public URL.

Keep the note warm, concise, supportive without becoming sycophantic, and accurate about `Official`, `Reported`, analysis, and directional sentiment. Avoid first-person framing unless Mel explicitly requests it. Draft the message for Mel to send; never send it automatically.
