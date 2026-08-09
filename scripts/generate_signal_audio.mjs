#!/usr/bin/env node
import { mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";

const DEFAULT_VOICE_ID = "Ib97zM6uFBc71OWgj75I";
const MODEL_ID = "eleven_multilingual_v2";
const VOICE_SETTINGS = Object.freeze({
  stability: 0.50,
  similarity_boost: 0.78,
  style: 0.06,
  use_speaker_boost: true,
  speed: 0.96
});

function usage() {
  console.log("Usage: node generate_signal_audio.mjs --input transcript.txt --output brief.mp3 --title \"Ownership Audio Brief\"");
}

function parseArgs(argv) {
  const args = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === "--help" || token === "-h") return { help: true };
    if (!token.startsWith("--") || !argv[index + 1]) throw new Error(`Invalid argument: ${token}`);
    args[token.slice(2)] = argv[index + 1];
    index += 1;
  }
  return args;
}

const args = parseArgs(process.argv.slice(2));
if (args.help) {
  usage();
  process.exit(0);
}

if (!args.input || !args.output || !args.title) {
  usage();
  throw new Error("--input, --output, and --title are required.");
}

const inputPath = resolve(args.input);
const outputPath = resolve(args.output);
const narration = (await readFile(inputPath, "utf8")).trim();
if (!narration) throw new Error("Narration text is empty.");

const wordCount = narration.split(/\s+/).filter(Boolean).length;
if (wordCount < 300 || wordCount > 420) {
  throw new Error(`Narration must be 300-420 words for this feature brief; found ${wordCount}.`);
}

const denseSentences = narration
  .split(/(?<=[.!?])\s+/)
  .map(sentence => ({ sentence, words: sentence.split(/\s+/).filter(Boolean).length }))
  .filter(item => item.words > 42);
if (denseSentences.length) {
  throw new Error(`Rewrite for the ear: ${denseSentences.length} sentence(s) exceed 42 words.`);
}

const apiKey = process.env.ELEVENLABS_API_KEY;
if (!apiKey) throw new Error("ELEVENLABS_API_KEY is required to generate narration.");

const workDir = await mkdtemp(join(tmpdir(), "suns-signal-elevenlabs-"));
try {
  await mkdir(dirname(outputPath), { recursive: true });
  const voiceId = process.env.ELEVENLABS_VOICE_ID ?? DEFAULT_VOICE_ID;
  const response = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voiceId}?output_format=mp3_44100_128`, {
    method: "POST",
    headers: { "xi-api-key": apiKey, "Content-Type": "application/json" },
    body: JSON.stringify({
      text: narration,
      model_id: MODEL_ID,
      language_code: "en",
      voice_settings: VOICE_SETTINGS
    })
  });
  if (!response.ok) throw new Error(`ElevenLabs generation failed with status ${response.status}.`);

  const rawPath = join(workDir, "raw.mp3");
  await writeFile(rawPath, Buffer.from(await response.arrayBuffer()));
  const ffmpeg = spawnSync("ffmpeg", [
    "-hide_banner", "-loglevel", "error", "-y", "-i", rawPath,
    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ac", "1",
    "-codec:a", "libmp3lame", "-b:a", "96k",
    "-metadata", `title=${args.title}`,
    "-metadata", "artist=Accelerated Velocity Consulting",
    outputPath
  ], { encoding: "utf8" });
  if (ffmpeg.error) throw ffmpeg.error;
  if (ffmpeg.status !== 0) throw new Error(`Audio finishing failed: ${ffmpeg.stderr}`);

  const probe = spawnSync("ffprobe", [
    "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", outputPath
  ], { encoding: "utf8" });
  if (probe.error) throw probe.error;
  if (probe.status !== 0) throw new Error(`Audio duration check failed: ${probe.stderr}`);

  const durationSeconds = Number.parseFloat(probe.stdout.trim());
  if (!Number.isFinite(durationSeconds) || durationSeconds < 140 || durationSeconds > 220) {
    throw new Error(`Audio duration must be 140-220 seconds; found ${probe.stdout.trim()}.`);
  }

  const audioBytes = await readFile(outputPath);
  const metadataPath = outputPath.replace(/\.mp3$/i, ".metadata.json");
  await writeFile(metadataPath, `${JSON.stringify({
    generated_at: new Date().toISOString(),
    title: args.title,
    voice_id: voiceId,
    model_id: MODEL_ID,
    voice_settings: VOICE_SETTINGS,
    duration_seconds: Number(durationSeconds.toFixed(3)),
    word_count: wordCount,
    sha256: createHash("sha256").update(audioBytes).digest("hex")
  }, null, 2)}\n`);
  console.log(`Generated ${outputPath}`);
  console.log(`Generated ${metadataPath}`);
} finally {
  await rm(workDir, { recursive: true, force: true });
}
