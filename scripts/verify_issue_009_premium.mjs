/**
 * Issue 009 approved editorial lock, compatible with the authorized hash-route hub.
 * Run: node scripts/verify_issue_009_premium.mjs
 *
 * Captured BEFORE the FULL BELLS hub conversion from the current-global-standard
 * recut. UI wrappers, navigation and hero chrome may evolve; editorial paragraphs,
 * headlines, reporting labels and original source entries may not silently change.
 * Authorized calendar additions are checked separately; original prose stays locked.
 * Current transcript is the approved recut minus the spoken Rankin attribution.
 *
 * --inspect <HTML> prints diagnostic hashes only; it never refreshes expectations.
 * Requires Node and Python 3 standard library. No browser/network/package install.
 */
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
import {execFileSync} from 'node:child_process';

const hash = value => crypto.createHash('sha256').update(value).digest('hex');
export const fileHash = file => hash(fs.readFileSync(file));
const parser = String.raw`
import json, re, sys
from html.parser import HTMLParser

VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
IGNORED = set('head script style template noscript'.split())

class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = {'tag': '#document', 'attrs': {}, 'children': []}
        self.stack = [self.root]
    def handle_starttag(self, tag, attrs):
        node = {'tag': tag, 'attrs': dict(attrs), 'children': []}
        self.stack[-1]['children'].append(node)
        if tag not in VOID:
            self.stack.append(node)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i]['tag'] == tag:
                del self.stack[i:]
                return
    def handle_data(self, data):
        self.stack[-1]['children'].append(data)

def hidden(node):
    return node['tag'] in IGNORED or node['attrs'].get('aria-hidden', '').lower() == 'true'

def text(node, visible=True):
    if isinstance(node, str):
        return node
    if visible and hidden(node):
        return ''
    return ''.join(text(child, visible) for child in node['children'])

def clean(value):
    return re.sub(r'\s+', ' ', value).strip()

def walk(node, visible=False):
    if isinstance(node, str) or (visible and hidden(node)):
        return
    yield node
    for child in node['children']:
        yield from walk(child, visible)

doc = Document()
doc.feed(sys.stdin.read())
nodes = list(walk(doc.root))
body = next(n for n in nodes if n['tag'] == 'body')
visible = list(walk(body, True))
head = next(n for n in nodes if n['tag'] == 'head')
head_nodes = list(walk(head))
metadata = {
    'title': [clean(text(n, False)) for n in head_nodes if n['tag'] == 'title'],
    'meta': [n['attrs'] for n in head_nodes if n['tag'] == 'meta'],
    'canonical': [n['attrs'] for n in head_nodes if n['tag'] in ('link', 'base') and (n['tag'] == 'base' or n['attrs'].get('rel') == 'canonical')],
    'structured_data': [json.loads(text(n, False)) for n in head_nodes if n['tag'] == 'script' and n['attrs'].get('type') == 'application/ld+json'],
}
ledger = next(n for n in nodes if n['attrs'].get('id') == 'sources')
scans = [n for n in nodes if n['attrs'].get('data-weekly-service') in ('suns-pulse', 'league-scan')]
calendar = next(n for n in nodes if n['attrs'].get('id') == 'calendar')
data_strip = next(n for n in nodes if 'data-strip' in n['attrs'].get('class', '').split())
out = {
    'paragraphs': [clean(text(n)) for n in visible if n['tag'] == 'p'],
    'ledger_entries': [clean(text(n)) for n in walk(ledger, True) if n['tag'] == 'li'],
    'scans': {n['attrs']['data-weekly-service']: {'window': n['attrs'].get('data-reporting-window'), 'cards': len([a for a in walk(n, True) if a['tag'] == 'article'])} for n in scans},
    'ids': [n['attrs']['id'] for n in visible if 'id' in n['attrs']],
    'calendar_labels': [clean(text(n)) for n in walk(calendar, True) if n['tag'] == 'span'],
    'calendar_cells': [{'date': n['attrs']['data-calendar-date'], 'number': clean(text(next(a for a in walk(n, True) if 'calendar-number' in a['attrs'].get('class', '').split()))), 'events': [a['attrs'] for a in walk(n, True) if 'data-calendar-event' in a['attrs']]} for n in walk(calendar, True) if 'data-calendar-date' in n['attrs']],
    'calendar_weekdays': [n['attrs'].get('abbr') for n in walk(calendar, True) if n['tag'] == 'th' and n['attrs'].get('scope') == 'col'],
    'stat_values': [clean(text(n)) for n in walk(data_strip, True) if n['tag'] == 'span'],
    'visible_text': clean(text(body)),
    'headings': [[n['tag'], clean(text(n))] for n in visible if re.fullmatch(r'h[1-6]', n['tag'])],
    'anchor_hrefs': [n['attrs'].get('href') for n in visible if n['tag'] == 'a'],
    'reporting_labels': [[n['attrs'].get('datetime'), clean(text(n))] for n in visible if n['tag'] == 'time'],
    'section_labels': [clean(text(n)) for n in visible if set(n['attrs'].get('class', '').split()) & {'source-tag', 'label'}],
    'metadata': metadata,
    'player': [n['attrs'] for n in nodes if n['tag'] == 'mel-audio-player'],
    'sections': [[n['tag'], n['attrs'].get('id'), n['attrs'].get('data-weekly-service'), n['attrs'].get('data-reporting-window')] for n in visible if n['tag'] in ('section', 'aside')],
}
print(json.dumps(out, ensure_ascii=False, sort_keys=True, separators=(',', ':')))
`;

export const inspectHtml = html => JSON.parse(execFileSync('python3', ['-c', parser], {
  input: html, encoding: 'utf8', maxBuffer: 4 * 1024 * 1024,
}));

const EXPECTED = {
  "paragraphs": [
    "Phoenix’s development work now carries more immediate weight. Camp will begin to show how that preparation holds up when players are asked to contribute sooner.",
    "The Suns announced Mark Williams’s shoulder surgery September 11. No team return timetable has been established.",
    "Coverage of Khaman Maluach’s next step preceded the injury announcement by five days. His progress was already drawing interest.",
    "Sampled discussion shows enthusiasm for young players alongside concern about placing too much on them too soon.",
    "Clearer responsibilities and contributions that repeat would give Phoenix better evidence of its depth.",
    "Five days before Phoenix announced Mark Williams’s shoulder surgery, coverage was already focused on Khaman Maluach’s development.",
    "Williams’s absence puts that preparation to an earlier test. Young players may be asked to contribute sooner, giving Phoenix a clearer view of who is ready for more responsibility. Dependable contributions would give the team more options as the season begins.",
    "Aug. 31–Sept. 13Two weeks of Suns activity and league developments. Earlier reporting is labeled as background.",
    "Return timetable pendingThe Suns announced his shoulder surgery September 11. The team will establish a return timetable later.",
    "Earlier work, greater valueWilliams’s absence raises the value of preparing other players for larger roles.",
    "On September 6, Holden Sherman’s SB Nation analysis examined Maluach’s need to become a more meaningful contributor. On September 11, Phoenix announced that Williams had undergone surgery the previous day to repair a torn labrum in his left shoulder following an offseason workout. The team said a return timetable would be established later. Arizona’s Family/AP reported the announcement.",
    "The injury brought the need forward. Maluach was already part of the development discussion; camp will begin to show how much responsibility he and the other young players can carry.",
    "Maluach Summer League games",
    "Points per game",
    "Rebounds per game",
    "Summer League background",
    "Maluach recorded a double-double in each of those four Summer League games. In his July 27 analysis, Brandon Duenas made the case for a larger role. Maluach gave people a reason to be interested. Dependable regular-season play will have to develop against stronger competition, over more games.",
    "Arizona’s Family/AP also identified Oso Ighodaro as a possible replacement. Having several players preparing for more responsibility gives Phoenix options. As camp and preseason unfold, ownership will get a better sense of which contributions the team can count on.",
    "The public sees only part of that work. Young players may now be judged against an immediate need while they are still learning. Describing their progress in specific terms helps people understand how the development is going.",
    "Comments in the September 11 Suns injury thread welcomed the possibility of more time for Maluach and the younger players. Other comments questioned Williams’s durability and the prior investment in him.",
    "Replies emphasized Maluach’s limited NBA experience and warned against treating this as an immediate pass-or-fail test. Both reactions were present in the same conversation.",
    "Enthusiasm and impatience were present in the same discussion. At media day, concrete accounts of what a player has been working on would give that audience something to follow as games begin.",
    "Source: r/suns, September 11 injury discussion. A qualitative review of visible comments in one self-selected thread; directional and nonrepresentative.",
    "When a player can explain his responsibilities clearly, or a coach can describe a part of his preparation in detail, the progress is easier to understand. Games then give those accounts something to be measured against.",
    "Contributions that repeat would tell Phoenix more about which young players are becoming dependable and where development still needs time. That is useful knowledge to have as the season approaches.",
    "Kellan Olson placed Phoenix eighth in the West. He credited the bench and coaching while questioning how the starters fit. His assessment records one analyst’s view before the Williams announcement, with confidence already resting partly on the depth now facing an earlier test.",
    "The Suns shared footage of Dillon Brooks practicing kung fu in Wudang. The visit gives the team material built around a player’s personality and an international setting. Audience reach remains unverified. The response to those posts would help show whether they are drawing interest beyond the usual basketball audience.",
    "Suns On SI reported that the October 10 home game against San Antonio will air on ESPN2. A national audience gets an early look at Phoenix, while the group is still preparing. Who is available and how far that preparation has progressed will help explain the performance.",
    "A Spurs supporter opened an r/nba discussion by asking why other teams could not offer the same free local access as Phoenix. Replies praised antenna access, though some people were unsure where to watch. In this self-selected sample, goodwill and confusion sit together. Clear viewing information could help interested people become regular viewers.",
    "The September 22 open house includes a Brian Gregory–Jordan Ott Chalk Talk. Prospective members will hear directly from basketball leadership. Their questions afterward could reveal what they understand about the team and what they still want to know. Attendance and later ticket interest would help show whether that access brings people back.",
    "Reporting cutoff: September 13, 2026. The review covers August 31–September 13. Dates identify publication or announcement dates except the explicitly labeled event-listing check. The open house is included as forward context. Interpretation is AVC’s.",
    "The NBA fined the Clippers $30 million, took five first-round picks, and suspended Steve Ballmer for one year over salary-cap circumvention. The club disputed the findings. Losing the picks narrows future roster options. The suspension affects current leadership as well, leaving the organization to manage consequences on both timelines.",
    "Michael Grange reported that the Kawhi Leonard deal remained incomplete, with the Clippers needing replacement leadership to sign off. His sources remained confident it would proceed. Toronto is approaching camp with that approval still pending, a practical complication for its preparation.",
    "NBA TV announced its 60-game regular-season schedule, including Golden State at Phoenix on October 24. The league said the release completed the national television schedule. Phoenix now has the full package for assessing its exposure and telling fans where to watch.",
    "Sam Amico, citing ESPN’s Brian Windhorst, reported that Seattle and Las Vegas expansion would be discussed at the September 14–15 owners’ meetings. Whether a vote would occur remained uncertain. Entry terms and timing will determine much of what expansion means for existing teams; the public outcome may give Phoenix more detail on that process.",
    "At his introduction, Jonathan Kuminga described the relationships that helped bring him to Minnesota. AP reported repeated player outreach and an in-person visit by team representatives. Several people made the team’s interest tangible. That kind of contact gives a prospective player a chance to understand where he would fit.",
    "The next scheduled public opportunity to hear how the organization describes health, preparation, and responsibilities.",
    "The start of collective preparation. First preseason game: October 5 at Detroit.",
    "Public information reviewed September 13, 2026. Team announcements, reported developments, external analysis, and AVC interpretation are distinguished. Health updates follow the team’s statements. Social reaction reflects the self-selected discussions cited above. Older sources are used only for background or the forward calendar."
  ],
  "headings": [
    "The Next Step Starts Early",
    "The 20-second read.",
    "A changed plan can reveal the value of earlier work.",
    "Five days separated the prospect story and the immediate need.",
    "Summer progress is a starting point.",
    "The opportunity is welcome. The expectations need perspective.",
    "Some supporters want to see the young group.",
    "The same discussion pushed back on instant expectations.",
    "The strongest September evidence will be specific.",
    "Five signals across the organization.",
    "The bench and coaching drew early confidence.",
    "Brooks’s China visit gave the Suns a different setting.",
    "The home preseason opener has a national window.",
    "Easy viewing is earning attention beyond Phoenix.",
    "The member event connects access with understanding.",
    "Five developments with ownership implications.",
    "The Clippers’ penalties reach into future seasons.",
    "Toronto is preparing around an unfinished deal.",
    "The national television schedule is now complete.",
    "Expansion is approaching another decision point.",
    "Minnesota made its interest personal and specific.",
    "Media day first. Camp the next day.",
    "Suns media day",
    "Training camp opens",
    "Source Ledger"
  ],
  "reporting_labels": [
    [
      "2026-09-02",
      "External analysis · Sept. 2"
    ],
    [
      "2026-09-08",
      "Reported team activity · Sept. 8"
    ],
    [
      "2026-09-10",
      "Reported broadcast · Sept. 10"
    ],
    [
      "2026-09-13",
      "Directional reception · Sept. 13"
    ],
    [
      "2026-09-13",
      "Official listing checked · Sept. 13"
    ],
    [
      "2026-09-02",
      "Official · League office / West · Sept. 2"
    ],
    [
      "2026-09-11",
      "Reported / Pending · East · Sept. 11"
    ],
    [
      "2026-09-03",
      "Official · Media / Market · Sept. 3"
    ],
    [
      "2026-09-11",
      "Reported / Pending · Expansion · Sept. 11"
    ],
    [
      "2026-09-10",
      "Reported · West / Recruitment · Sept. 10"
    ]
  ],
  "external_hrefs": [
    "https://apnews.com/article/0dc5e1a0d34224d5c65dbc39a74076c5",
    "https://apnews.com/article/0dc5e1a0d34224d5c65dbc39a74076c5",
    "https://arizonasports.com/nba/phoenix-suns/western-conference-power-rankings-suns-play-in-top-6",
    "https://arizonasports.com/nba/phoenix-suns/western-conference-power-rankings-suns-play-in-top-6",
    "https://hoopswire.com/nba-owners-seattle-las-vegas-expansion/",
    "https://hoopswire.com/nba-owners-seattle-las-vegas-expansion/",
    "https://pr.nba.com/nba-tv-unveils-game-schedule-for-2026-27-regular-season/",
    "https://pr.nba.com/nba-tv-unveils-game-schedule-for-2026-27-regular-season/",
    "https://sports.yahoo.com/articles/jonathan-kuminga-picked-timberwolves-court-201601646.html",
    "https://sports.yahoo.com/articles/jonathan-kuminga-picked-timberwolves-court-201601646.html",
    "https://sports.yahoo.com/articles/suns-khaman-maluach-become-more-160000145.html",
    "https://sports.yahoo.com/articles/suns-khaman-maluach-become-more-160000145.html",
    "https://uk.sports.yahoo.com/news/phoenix-suns-begin-training-camp-151956018.html",
    "https://uk.sports.yahoo.com/news/phoenix-suns-begin-training-camp-151956018.html",
    "https://www.azfamily.com/2026/09/11/suns-center-mark-williams-undergoes-shoulder-surgery-could-miss-extended-time/",
    "https://www.azfamily.com/2026/09/11/suns-center-mark-williams-undergoes-shoulder-surgery-could-miss-extended-time/",
    "https://www.brightsideofthesun.com/suns-analysis/108140/khaman-maluach-summer-league-mark-williams-center-rotation-development",
    "https://www.brightsideofthesun.com/suns-analysis/108140/khaman-maluach-summer-league-mark-williams-center-rotation-development",
    "https://www.nba.com/news/nba-investigation-findings-la-clippers",
    "https://www.nba.com/news/nba-investigation-findings-la-clippers",
    "https://www.nba.com/suns/openhouse",
    "https://www.nba.com/suns/openhouse",
    "https://www.reddit.com/r/nba/comments/1wezbj4/are_the_suns_still_broadcasting_most_of_their/",
    "https://www.reddit.com/r/nba/comments/1wezbj4/are_the_suns_still_broadcasting_most_of_their/",
    "https://www.reddit.com/r/suns/comments/1wdkd76/shams_phoenix_suns_center_mark_williams_underwent/",
    "https://www.reddit.com/r/suns/comments/1wdkd76/shams_phoenix_suns_center_mark_williams_underwent/",
    "https://www.si.com/nba/suns/onsi/dillon-brooks-takes-phoenix-suns-offseason-training-new-level",
    "https://www.si.com/nba/suns/onsi/dillon-brooks-takes-phoenix-suns-offseason-training-new-level",
    "https://www.si.com/nba/suns/onsi/phoenix-suns-san-antonio-spurs-preseason-game-nationally-televised",
    "https://www.si.com/nba/suns/onsi/phoenix-suns-san-antonio-spurs-preseason-game-nationally-televised",
    "https://www.sportsnet.ca/nba/article/fortunes-depend-on-kawhi-leonard-as-raptors-prep-for-new-season/",
    "https://www.sportsnet.ca/nba/article/fortunes-depend-on-kawhi-leonard-as-raptors-prep-for-new-season/"
  ],
  "ledger_entries": [
    "Arizona’s Family/AP, Sept. 11: Williams surgery and the team’s timetable statement",
    "Holden Sherman / SB Nation via Yahoo, Sept. 6: the pre-injury development discussion",
    "Brandon Duenas / Bright Side, July 27: four-game Summer League performance; background only",
    "r/suns, Sept. 11: qualitative, nonrepresentative public reaction",
    "Kellan Olson / Arizona Sports, Sept. 2: pre-injury West assessment",
    "Suns On SI, Sept. 8: Brooks in Wudang; embedded Sept. 7–8 Suns posts",
    "Suns On SI, Sept. 10: October 10 ESPN2 broadcast",
    "AP, Sept. 2: Clippers penalties and the club’s dispute; official NBA findings",
    "Michael Grange / Sportsnet, Sept. 11: Leonard trade still pending",
    "NBA Communications, Sept. 3: completed NBA TV schedule",
    "Duane Rankin via HoopsHype/Yahoo, Aug. 4: media day, camp and preseason opener",
    "r/nba, Sept. 13: directional reception of Phoenix viewing access, not verified broadcast terms",
    "Suns open-house listing, checked Sept. 13: September 22 event and leadership Chalk Talk",
    "Sam Amico / Hoops Wire, Sept. 11, citing Brian Windhorst: expected expansion discussion, no guaranteed vote",
    "Dave Campbell / AP, Sept. 10: Kuminga’s introductory comments and Minnesota’s outreach"
  ]
};

const ORIGIN = 'https://meltckr.github.io/suns-signal-005-permission-to-run/issue-009/';
const CALENDAR_SOURCE = 'https://www.nba.com/news/key-dates';
const OG_IMAGE = ORIGIN + 'assets/og-suns-signal-009-next-step-v2.png';
const CURRENT_AUDIO = 'audio/suns-signal-009-next-step-arizona-v12-v11.mp3';
const TRANSCRIPT_SHA = 'ce59afbf7018ea8c92964185920586946e428c43fc8febff049af224f947e5af';
const METADATA_SHA = 'ab29ad9de70ad43aaa2cbd7aa73d881e487299355b8ddde59cd1a2447be4f551';
const CALENDAR_NOTE = 'Calendar sources: NBA key dates — official September 29 camp opening; Duane Rankin, August 4, via HoopsHype/Yahoo — Suns media day and preseason opener. Earlier reporting included as forward calendar context.';
const CALENDAR_ENTRY = 'NBA official 2026–27 key dates: September 29 training-camp opening; checked September 13';
const OWNERS_SOURCE = 'https://www.espn.com/nba/story/_/id/49894591/nba-intel-board-governors-next-steps-clippers-las-vegas-seattle-europe-expansion';
const OWNERS_ENTRY = 'Brian Windhorst / ESPN, Sept. 11: September 14–15 owners’ meetings and expected expansion discussion';
const HISTORICAL_ASSETS = {
  'assets/mel-audio-player/mel-audio-player.js': '14644aeeab42d18917aa155c5511ba4ec7db56bafc039c748cda14ca15fa86ac',
  'assets/mel-audio-player/player-utils.mjs': 'fbf4d7ddfdcb301341564811dc1ad16847b03e7374e2de52389b2b181e01666e',
  'issue-009/assets/og-suns-signal-009-next-step-v1.png': 'd710dffed05f35298d10dc90ea24c60b0a1695ceda3ccef810d87d3efe84392a',
  'issue-009/audio/suns-signal-009-next-step-arizona-v12-v1.mp3': 'a44a66ea7502a377f4db51bb3bed35db893aa289f5e0a57953432b714a9b9d3a',
  'issue-009/audio/suns-signal-009-next-step-arizona-v12-v2.mp3': '63651e20b053621c2055cd57e0b2d5184089ac9f6b2bb61c6b8a6b2ebf59612e',
  'issue-009/audio/suns-signal-009-next-step-arizona-v12-v3.mp3': '1d58ea08495ed7a081ab4b9812bd893035485a72379d4fa402b6155bcb2d589e',
  'issue-009/audio/suns-signal-009-next-step-arizona-v12-v4.mp3': '1b8f6b4d817291336c0953a3626521dd7bd2ffd323eb89f37b2efde082a2fde7',
  'issue-009/audio/suns-signal-009-next-step-arizona-v12-v5.mp3': '866f390eb4dcd0ff449c4f69236a13cdab983673d2b88a68413399f8b7e4c860',
  'issue-009/audio/suns-signal-009-next-step-arizona-v12-v5.metadata.json': '011533a96a75998be193a3025d10af07a3bf1fd1b9bb48a43571929bc6294270',
  'issue-009/audio/suns-signal-009-next-step-arizona-v12-v6.mp3': 'abef267c012bc66985b86a6c910aa3f8567bb98bf531534612a3b49569a9bc3b',
  'issue-009/audio/suns-signal-009-next-step-arizona-v12-v6.metadata.json': '90e39f231967e2a674a67a843e5f8ce39f154d1bb0b6ecb50295a09582133d60',
  'issue-009/audio/suns-signal-009-next-step-arizona-v12-v7.mp3': 'da80296540508cb7e471f395ae5d88ba46c8cca654ab7645f1f462a6a2bc336d',
  'issue-009/audio/suns-signal-009-next-step-arizona-v12-v7.metadata.json': '3e110e3a37ad999f8a5f594f3a0a63a714a592375019a9ff2236b9360f4bc30e',
  'issue-009/audio/suns-signal-009-next-step-arizona-v12-v8.mp3': '4d30a8f64dbc60f750dc372dfe4dc6881b3e93265540e48176db0880cca23229',
  'issue-009/audio/suns-signal-009-next-step-arizona-v12-v8.metadata.json': '6c05b20bc20ab38624a7bd768f5f4b8e4386447f12881391aa36a3f2eccffb0f',
  'issue-009/audio/suns-signal-009-next-step-arizona-v12-v9.mp3': 'c7a2086dc04809906d22bcb6b30e142cb534a79515af5dde1c0b8ffd8072be44',
  'issue-009/audio/suns-signal-009-next-step-arizona-v12-v9.metadata.json': 'dbaeb1c9361be345d3e2e90a6172988662bd8ef4a688efa52f4c800b9b801d0a',
};
const APPROVED_CURRENT_ASSETS = {
  'issue-009/audio/suns-signal-009-next-step-arizona-v12-v11.mp3': 'b053e7579853046d9f89b01a08a95c68d53f17a86fc4a321c210411791288d64',
  'issue-009/audio/suns-signal-009-next-step-arizona-v12-v11.metadata.json': 'ca5bfee21e13218371a9b5555ef9715fe839d1f6af2b2384de99b30159aa61b1',
  'issue-009/assets/og-suns-signal-009-next-step-v2.png': 'b5ffa0dc8cfb02b70b0a995a6950d4012cf0e200c4321597550a690fe3e77a34',
  'issue-009/assets/maluach-summer-league-primary.jpg': '88d88ac4f3fd11b99781b1ef94d66893b84c9c50375805e055a377be326e231e',
};

// v2 is the approved image replacement. Every other metadata field stays locked.
export function metadataHash(metadata) {
  const normalized = structuredClone(metadata);
  // The approved v2 package adds this accessibility field; validate it separately.
  normalized.meta = normalized.meta.filter(m => m.name !== 'twitter:image:alt');
  for (const m of normalized.meta) {
    if (['og:image', 'og:image:secure_url', 'og:image:alt', 'twitter:image'].includes(m.property || m.name)) m.content = 'APPROVED_OG_V2';
  }
  for (const item of normalized.structured_data) item.image = ['APPROVED_OG_V2'];
  return hash(JSON.stringify(normalized));
}

function includesAll(actual, expected, label) {
  const pool = [...actual];
  for (const value of expected) {
    const index = pool.indexOf(value);
    assert(index >= 0, `${label} changed or disappeared: ${value.slice(0, 150)}`);
    pool.splice(index, 1);
  }
}

export function verifyIssue009(html = fs.readFileSync('issue-009/index.html', 'utf8')) {
  const p = inspectHtml(html);
  includesAll(p.paragraphs, EXPECTED.paragraphs, 'Approved editorial paragraph');
  includesAll(p.headings.map(h => h[1]), EXPECTED.headings, 'Approved headline');
  assert.deepEqual(p.reporting_labels, EXPECTED.reporting_labels, 'Official/Reported/directional labels or reporting dates changed');
  assert.deepEqual(p.anchor_hrefs.filter(h => /^https?:/.test(h) && ![CALENDAR_SOURCE, OWNERS_SOURCE].includes(h)).sort(), EXPECTED.external_hrefs, 'Existing source links changed or an unapproved source was added');
  // Two sourced calendar additions are authorized. Original source wording stays.
  assert.equal(p.ledger_entries.length, EXPECTED.ledger_entries.length + 2, 'The 15 original sources plus NBA and ESPN calendar entries are required');
  includesAll(p.ledger_entries, EXPECTED.ledger_entries, 'Source ledger entry');
  assert(p.ledger_entries.includes(CALENDAR_ENTRY), 'Approved NBA calendar source wording changed');
  assert(p.ledger_entries.includes(OWNERS_ENTRY), 'The owners’ meeting date needs its named reporting source');
  assert.equal(p.anchor_hrefs.filter(h => h === OWNERS_SOURCE).length, 2, 'ESPN must be linked in Calendar and the source ledger');
  assert(p.anchor_hrefs.filter(h => h === CALENDAR_SOURCE).length >= 2, 'Official NBA calendar must be cited in Calendar Ahead and the source ledger');
  const calendarNote = p.paragraphs.find(t => t.startsWith('Calendar sources:'));
  assert.equal(calendarNote, CALENDAR_NOTE, 'Calendar note must preserve the official-camp versus reported-media-day distinction');
  includesAll(p.calendar_labels, ['MONDAY · SEPTEMBER 28', 'TUESDAY · SEPTEMBER 29'], 'Calendar day/date');
  assert.deepEqual(p.stat_values, ['4', '19.5', '12.8', 'July'], 'Summer League evidence values changed');
  assert(!/Next Watch|What would sharpen the next edition|\bMatt\b/.test(p.visible_text), 'Internal checklist or incorrect Mat spelling returned');
  for (const [service, scan] of Object.entries(p.scans)) {
    assert.equal(scan.cards, 5, `${service}: five sourced cards required`);
    assert.equal(scan.window, '2026-08-31/2026-09-13', `${service}: reporting window changed`);
  }
  assert.equal(Object.keys(p.scans).length, 2, 'Both Suns Pulse and Around The League scans are required');
  for (const route of ['hub', 'ownership', 'pulse', 'league', 'calendar', 'sources']) assert(p.ids.includes(route), `Missing authorized route #${route}`);
  assert.equal(metadataHash(p.metadata), METADATA_SHA, 'Non-image metadata or canonical URL changed');
  assert(!/\bMatt\b/.test(JSON.stringify(p.metadata)), 'Incorrect Mat spelling in metadata');
  const meta = Object.fromEntries(p.metadata.meta.map(m => [m.property || m.name, m.content]));
  assert.equal(meta['og:url'], ORIGIN);
  for (const key of ['og:image', 'og:image:secure_url', 'twitter:image']) assert.equal(meta[key], OG_IMAGE, `${key}: wrong v2 image URL`);
  assert.equal(meta['og:image:width'], '1200');
  assert.equal(meta['og:image:height'], '630');
  assert.equal(meta['og:image:type'], 'image/png');
  assert(/Maluach/i.test(meta['og:image:alt']), 'OG v2 alt must describe the approved Maluach subject');
  assert(/Maluach/i.test(meta['twitter:image:alt']), 'Twitter image alt must describe the approved Maluach subject');
  assert.equal(meta['twitter:card'], 'summary_large_image');
  for (const item of p.metadata.structured_data) assert.deepEqual(item.image, [OG_IMAGE], 'JSON-LD must use OG v2');
  const png = fs.readFileSync('issue-009/assets/og-suns-signal-009-next-step-v2.png');
  assert.equal(png.readUInt32BE(16), 1200);
  assert.equal(png.readUInt32BE(20), 630);
  assert.equal(p.player.length, 1, 'Preserve one standard audio module');
  assert.deepEqual(p.player[0], {
    download: null,
    eyebrow: 'Listen',
    src: CURRENT_AUDIO,
    title: 'The Next Step Starts Early',
    transcript: 'content/audio-brief-transcript.txt',
  }, 'Audio identity or controls contract changed');
  for (const [file, expected] of Object.entries(HISTORICAL_ASSETS)) assert.equal(fileHash(file), expected, `Historical asset/shared player changed: ${file}`);
  for (const [file, expected] of Object.entries(APPROVED_CURRENT_ASSETS)) assert.equal(fileHash(file), expected, `Approved current artifact changed: ${file}`);
  assert.equal(fileHash('issue-009/content/audio-brief-transcript.txt'), TRANSCRIPT_SHA, 'Approved transcript changed beyond removal of the spoken Rankin attribution');
  const transcript = fs.readFileSync('issue-009/content/audio-brief-transcript.txt', 'utf8').trim();
  assert.equal(transcript.split(/\r?\n/).filter(line => line.trim()).at(-1), 'Much love, my brother, dominate!');
  const audioPath = path.join('issue-009', CURRENT_AUDIO);
  const manifest = JSON.parse(fs.readFileSync(audioPath.replace(/\.mp3$/, '.metadata.json'), 'utf8'));
  assert.equal(manifest.sha256, fileHash(audioPath), 'Player audio differs from its manifest');
  assert.equal(manifest.transcript_sha256, TRANSCRIPT_SHA, 'Audio manifest uses an old transcript');
  assert.equal(manifest.voice, 'AVC Arizona Voice v12');
  assert.equal(manifest.closing_verified, true);
  assert.equal(manifest.candidate_version, 11);
  assert.equal(manifest.status, 'mel_listening_approved_publication_authorized');
  assert.equal(manifest.release_eligible, true);
  assert.equal(manifest.publication_authorized, true);
  assert.deepEqual(manifest.user_rejected_versions, [7, 9, 10]);
  assert.deepEqual(manifest.changed_sentences, [23]);
  assert.equal(manifest.source_audio_version, 8);
  assert.equal(manifest.reused_raw_clips_verified_byte_identical, 23);
  assert.equal(manifest.candidate_selection?.reference_mode, 'approved_private_mel_energetic_icl');
  assert.equal(manifest.pronunciation_authority?.research_interpretation_for_natural_connected_delivery, 'kah-MAHN mahl-WAHCH');
  assert.equal(manifest.pronunciation_authority?.used_as_acoustic_synthesis_reference, false);
  assert.equal(manifest.technical_verification?.perceptual_listening_review_completed, true);
  assert.equal(manifest.technical_verification?.approved_v8_maluach_raw_clips_preserved, true);
  assert.equal(manifest.technical_verification?.whole_terminal_take_retained, true);
  assert.equal(manifest.technical_verification?.final_ten_asr_dominate_count, 1);
  return p;
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  if (process.argv[2] === '--inspect') {
    assert(process.argv[3], '--inspect requires an HTML path');
    const p = inspectHtml(fs.readFileSync(process.argv[3], 'utf8'));
    console.log(JSON.stringify({metadata_hash: metadataHash(p.metadata), paragraphs: p.paragraphs.length, headlines: p.headings.length, sources: p.ledger_entries.length, routes: p.ids, player: p.player}, null, 2));
  } else {
    assert.equal(process.argv.length, 2, 'Only verification or --inspect <HTML> is supported');
    verifyIssue009();
    console.log('PASS: approved editorial copy, source entries/links, reporting labels, 5+5 scans, hub routes, canonical metadata, Mel-approved v11 transcript/audio, Listen, exact close, OG v2 and immutable historical assets.');
    console.log('Scope: content/asset preservation. Browser navigation, mobile layout, audio interaction and perceptual listening are separate checks.');
  }
}
