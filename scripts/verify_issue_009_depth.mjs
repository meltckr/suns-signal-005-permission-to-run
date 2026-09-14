/**
 * Issue 009 presentation safeguards after the authorized FULL BELLS hub upgrade.
 * Content/source locks live in verify_issue_009_premium.mjs. This check deliberately
 * permits the approved hub wrappers and navigation instead of freezing HTML tags.
 * CSS contrast checks are conservative static checks; browser QA remains required.
 */
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {verifyIssue009} from './verify_issue_009_premium.mjs';

const current = fs.readFileSync('issue-009/index.html', 'utf8');
verifyIssue009(current);
const stylesheets = [...current.matchAll(/<link\b[^>]*rel="stylesheet"[^>]*href="([^"]+)"[^>]*>/g)]
  .map(m => path.resolve('issue-009', m[1].split('?')[0]));
const css = stylesheets.map(file => fs.readFileSync(file, 'utf8')).join('\n');
assert(/prefers-reduced-motion\s*:\s*reduce/.test(css), 'Reduced-motion styling is required');
assert(/\(hover\s*:\s*hover\)\s*and\s*\(pointer\s*:\s*fine\)/.test(css), 'Decorative hover movement must be limited to fine hover pointers');
assert(/:focus-visible/.test(css), 'Keyboard focus must remain visible');

const token = name => {
  const values = [...css.matchAll(new RegExp('--' + name + ':\\s*([^;]+);', 'g'))].map(m => m[1].trim());
  assert(values.length, `Missing audio theme token --${name}`);
  const value = values.at(-1);
  assert(/^#[0-9a-f]{6}$/i.test(value), `--${name} must resolve to an opaque six-digit color; got ${value}`);
  return value;
};
const bg = token('player-bg');
const surface = token('player-surface');
const soft = token('player-accent-soft');
const foregrounds = ['player-text', 'player-muted', 'player-accent'].map(token);
const luminance = hex => {
  const c = hex.match(/[0-9a-f]{2}/gi).map(x => parseInt(x, 16) / 255).map(x => x <= .04045 ? x / 12.92 : ((x + .055) / 1.055) ** 2.4);
  return c[0] * .2126 + c[1] * .7152 + c[2] * .0722;
};
const contrast = (a, b) => {
  const x = luminance(a), y = luminance(b);
  return (Math.max(x, y) + .05) / (Math.min(x, y) + .05);
};
// Include both gradient endpoints, control surfaces and the warm radial-overlay
// endpoint from the preserved shared player, instead of just one background.
const backgrounds = [bg, '#172033', '#342a36', surface, soft];
for (const fg of foregrounds) for (const background of backgrounds) {
  const ratio = contrast(fg, background);
  assert(ratio >= 4.5, `${fg} on ${background}: ${ratio.toFixed(2)}:1 is below 4.5:1`);
}
for (const name of ['signal-depth-v1.webp', 'signal-premium-v2-desktop.webp', 'signal-premium-v2-mobile.webp', 'signal-room-v3-desktop.webp', 'signal-room-v3-mobile.webp', 'signal-room-v4-desktop.webp', 'signal-room-v4-mobile.webp']) {
  assert(fs.statSync('issue-009/assets/' + name).size < 150000, `${name} exceeds the static hero asset budget`);
}
assert(/<picture\b/.test(current), 'Keep responsive Blender art direction');
assert(/<source\b[^>]*media="[^"]*max-width[^"]*"[^>]*srcset="[^"]*signal-room-v4-mobile\.webp/.test(current), 'Mobile must receive its own Blender room composition');
assert(/src="assets\/signal-room-v4-desktop\.webp"/.test(current), 'Desktop Blender room composition missing');
assert(/fetchpriority="high"/.test(current), 'The first-viewport hero should load with high priority');
assert(/alt="Original 3D illustration:/.test(current), 'Keep the illustration clearly identified in alternative text');
const hubCss = fs.readFileSync('issue-009/hub.css', 'utf8');
assert(/\.hub-intro\s*\{[^}]*align-self:start/.test(hubCss), 'Hero title must stay top-aligned below the masthead');
assert(!/\.hub-intro\s*\{[^}]*align-self:center/.test(hubCss), 'Viewport-height centering recreates the empty top band');
assert(/grid-template-rows:clamp\(180px,calc\(100svh - 505px\),300px\) auto auto/.test(hubCss), 'Keep the desktop hero row bounded; verify any new layout in the browser');
console.log('PASS: editorial lock, opaque audio contrast, keyboard/reduced-motion safeguards, top-aligned hub and lightweight responsive Blender room artwork.');
