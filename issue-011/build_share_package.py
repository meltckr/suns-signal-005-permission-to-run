from pathlib import Path
from html import escape
from html.parser import HTMLParser
import json, hashlib, zipfile, struct

edition = Path(__file__).resolve().parent
root = edition.parent
html = (edition / 'index.html').read_text()
class Head(HTMLParser):
    def __init__(self):
        super().__init__(); self.meta = {}; self.canonical = ''; self.schema = ''; self.in_schema = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'meta' and ('name' in a or 'property' in a): self.meta[a.get('property', a.get('name'))] = a.get('content')
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical = a['href']
        if tag == 'script' and a.get('type') == 'application/ld+json': self.in_schema = True
    def handle_endtag(self, tag):
        if tag == 'script': self.in_schema = False
    def handle_data(self, data):
        if self.in_schema: self.schema += data
h = Head(); h.feed(html)
audio = json.loads((edition/'edition.json').read_text())
og = edition/'assets/og-suns-signal-011-the-standard-in-your-own-words-v3.png'
metadata = {'title': audio['title'], 'issue': '011', 'canonical_url': h.canonical, 'complete_view_url': h.canonical+'?review=all', 'description': h.meta['description'], 'social': {k:v for k,v in h.meta.items() if k.startswith(('og:', 'twitter:', 'article:'))}, 'structured_data': json.loads(h.schema), 'audio': audio, 'share_card_sha256': hashlib.sha256(og.read_bytes()).hexdigest()}
(edition/'release-metadata.json').write_text(json.dumps(metadata, indent=2, ensure_ascii=False)+'\n')
assert struct.unpack('>II', og.read_bytes()[16:24]) == (1200,630)
assert og.read_bytes()[25] == 2, 'OG must be RGB'
assert hashlib.sha256((edition/audio['audio']).read_bytes()).hexdigest() == audio['audio_sha256']
assert hashlib.sha256((edition/audio['transcript']).read_bytes()).hexdigest() == audio['transcript_sha256']
ship = edition/'ship'; ship.mkdir(exist_ok=True)
msg = (edition/'imessage.txt').read_text().strip()
start = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Suns Signal 011 | Complete Share Kit</title><style>body{{margin:0;background:#111722;color:#edf0f5;font:18px/1.6 system-ui,sans-serif}}main{{max-width:920px;margin:auto;padding:32px 24px}}a{{color:#f8b674}}img.card{{width:100%;height:auto}}.brand{{width:240px;max-width:80%}}pre{{white-space:pre-wrap;font:inherit;background:#1d2531;padding:20px;border-radius:12px}}h1{{font-size:clamp(30px,5vw,46px);line-height:1.15}}footer{{margin-top:40px;border-top:1px solid #59616c;padding-top:20px}}</style><main><img class="brand" src="assets/brand/logos/AVC-logo-horizontal-light.svg" alt="Accelerated Velocity Consulting"><p>SUNS SIGNAL · ISSUE 011 · SEPTEMBER 27, 2026</p><h1>The Standard in Your Own Words</h1><p><a href="{h.canonical}?review=all">Read your complete published edition</a></p><p><a href="issue-011/complete-edition.html">Open the included complete edition</a> · <a href="issue-011/audio/suns-signal-011-v2.mp3">Audio</a> · <a href="issue-011/content/audio-brief-transcript.txt">Transcript</a></p><img class="card" src="share-card.png" alt="Suns Signal 011 share card with your portrait and AVC branding"><p><a href="share-card.png" download>Download share card / OG image</a> · <a href="issue-011/release-metadata.json">Metadata</a> · <a href="issue-011/sources.md">Sources</a></p><h2>Ready-to-send iMessage</h2><pre>{escape(msg)}</pre><p><a href="issue-011/imessage.txt">Copy from the text file</a></p><footer><img class="brand" src="assets/brand/logos/AVC-logo-horizontal-light.svg" alt="Accelerated Velocity Consulting"></footer></main></html>'''
zip_path = ship/'suns-signal-011-your-words-review.zip'
included=[]
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('START-HERE.html', start)
    z.writestr('share-card.png', og.read_bytes())
    # Keep the full content visible when opened locally without a module server.
    offline = html.replace('<script type="module" src="hub.js?v=011-hub-v4"></script>', '').replace('<body ', '<body data-review="all" data-route="hub" ', 1)
    z.writestr('issue-011/complete-edition.html', offline)
    for p in sorted(edition.rglob('*')):
        if not p.is_file() or 'ship' in p.parts or p.suffix == '.py' or p.name == 'render-og.mjs' or 'arizona-v12-v4' in p.name or p.name in {'suns-signal-011.metadata.json', 'suns-signal-011.mp3'} or ('og-suns-signal-' in p.name and p.name != og.name): continue
        z.write(p, p.relative_to(root)); included.append(str(p.relative_to(root)))
    for sub in ['assets/audio-player', 'assets/brand/logos', 'assets/teams/suns']:
        for p in sorted((root/sub).rglob('*')):
            if p.is_file(): z.write(p, p.relative_to(root))
print(json.dumps({'zip':str(zip_path), 'size':zip_path.stat().st_size, 'audio_sha256':audio['audio_sha256'], 'og_rgb':True, 'files':len(included)}, indent=2))
