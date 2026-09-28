from pathlib import Path
from lxml import html, etree
from html import escape
import json

HERE=Path(__file__).parent
TITLE='The Standard in His Own Words'
DESCRIPTION='Mat Ishbia’s public remarks reveal a consistent view of care, culture, roles and accountability, with a current Suns and league briefing.'
URL='https://meltckr.github.io/suns-signal-005-permission-to-run/issue-011/'
DATE='2026-09-27T00:00:00-07:00'
MODIFIED='2026-09-27T18:23:57-07:00'
STAMP='Updated Sep. 27, 2026 · 6:23 PM Arizona'
OG='og-suns-signal-011-the-standard-in-his-own-words-v2.png'
AUDIO='suns-signal-011.mp3'
ROOT=html.fromstring((HERE/'index.html').read_text())
def one(xpath):
 found=ROOT.xpath(xpath)
 assert len(found)==1,(xpath,len(found))
 return found[0]
def set_text(xpath,text): one(xpath).text=text
def set_attr(xpath,key,value):one(xpath).set(key,value)
def replace_children(xpath,markup):
 el=one(xpath)
 for child in list(el):el.remove(child)
 el.text=None
 for child in html.fragments_fromstring(markup):
  if isinstance(child,str): el.text=(el.text or '')+child
  else:el.append(child)
def replace(xpath,markup):
 el=one(xpath);el.getparent().replace(el,html.fragment_fromstring(markup))
def tag_link(label,url):return f'<a href="{escape(url,quote=True)}">{escape(label)}</a>'

# Metadata and first viewport remain in the approved Issue 009 shell.
set_attr('//link[@rel="stylesheet" and (starts-with(@href,"../styles.css") or starts-with(@href,"base.css"))]','href','base.css?v=011-base-v1')
set_attr('//link[@rel="stylesheet" and starts-with(@href,"hub.css")]','href','hub.css?v=011-hub-v3')
set_attr('//script[starts-with(@src,"hub.js")]','src','hub.js?v=011-hub-v2')
set_text('//head/title','Suns Signal 011 | '+TITLE)
set_attr('//meta[@name="robots"]','content','index,follow,max-image-preview:large')
for prop in ('description','twitter:description'):
 set_attr(f'//meta[@name="{prop}"]','content',DESCRIPTION)
for prop in ('og:description',):set_attr(f'//meta[@property="{prop}"]','content',DESCRIPTION)
for prop in ('og:title','twitter:title'):
 sel=f'//meta[@property="{prop}"]' if prop.startswith('og:') else f'//meta[@name="{prop}"]'
 set_attr(sel,'content','Suns Signal 011 | '+TITLE)
set_attr('//meta[@property="article:published_time"]','content',DATE)
set_attr('//meta[@property="article:modified_time"]','content',MODIFIED)
for prop in ('og:image','og:image:secure_url'):set_attr(f'//meta[@property="{prop}"]','content',URL+'assets/'+OG)
set_attr('//meta[@name="twitter:image"]','content',URL+'assets/'+OG)
alt='Suns Signal Issue 011 share card, The Standard in His Own Words, with Mat Ishbia portrait and AVC branding.'
set_attr('//meta[@property="og:image:alt"]','content',alt)
set_attr('//meta[@name="twitter:image:alt"]','content',alt)
set_text('//script[@type="application/ld+json"]',json.dumps({'@context':'https://schema.org','@type':'Article','headline':TITLE,'datePublished':DATE,'dateModified':MODIFIED,'author':{'@type':'Organization','name':'Accelerated Velocity Consulting'},'publisher':{'@type':'Organization','name':'Accelerated Velocity Consulting'},'image':[URL+'assets/'+OG],'mainEntityOfPage':URL}))
set_attr('//body','data-issue-title',TITLE)
set_attr('//script[contains(@src,"audio-player.js")]','src','../assets/audio-player/audio-player.js')
set_text('//header//div[@class="edition"]/strong','September 27, 2026')
set_text('//footer/div/span','Sports strategy and sentiment intelligence. · '+STAMP)
set_attr('//section[@id="hub"]//source[@media="(max-width:760px)"]','srcset','assets/signal-philosophy-011-mobile.webp')
set_attr('//section[@id="hub"]//img[@class="hero-art"]','src','assets/signal-philosophy-011-desktop.webp')
set_attr('//section[@id="hub"]//img[@class="hero-art"]','alt','Original 3D Suns court room with basketball, rising platforms, bronze arc, and three etched quote panels on the far wall.')
set_text('//section[@id="hub"]//p[@class="kicker"]','The Ishbia Philosophy')
set_text('//section[@id="hub"]//h1',TITLE)
set_text('//section[@id="hub"]//p[@class="hub-byline"]/span','· September 14–27, 2026')
for div,label,read in zip(one('//section[@id="hub"]//div[@class="decision-strip"]').xpath('./div'),
 ('Public record','Leadership pattern','Next public test'),
 ('Care and daily standards','Roles and accountability','Media day · Sept. 28')):
 div.xpath('./span')[0].text=label;div.xpath('./strong')[0].text=read
player=one('//mel-audio-player');player.set('src','audio/'+AUDIO);player.set('title',TITLE);player.set('eyebrow','Audio');player.attrib.pop('duration_seconds',None)
set_text('//nav[@class="hub-tiles"]/a[@href="#pulse"]//small','Three Suns signals')
set_text('//nav[@class="hub-tiles"]/a[@href="#league"]//small','Five league developments')
set_text('//nav[@class="hub-tiles"]/a[@href="#calendar"]//small','Media day through preseason')

# First read: editorial synthesis stays visibly distinct from direct quotations.
set_text('//div[@id="ownership"]/p[@class="section-dek"]','Across interviews spanning UWM, Michigan State and Phoenix, Mat returns to a few practical ideas: care for people, live the culture, know your role and own the work. Selected quotations below show the pattern in his own words.')
set_text('//div[@class="glance-panel"]/h2','Four ideas that recur.')
glance=[
 ('Care','People are the starting point.','His 2025 Fortune interview describes care as a leadership obligation.'),
 ('Culture','The leader has to live it.','The 2020 Forbes interview makes behavior the test of stated expectations.'),
 ('Role','Contribution has a shape.','The third-string point guard story explains why he returns to roles and teammates.'),
 ('Next evidence','Listen for examples at media day.','Public remarks on September 28 can show how the Suns describe these standards now.'),
]
for card,(label,read,support) in zip(one('//div[@class="glance-grid"]').xpath('./article'),glance):
 card.xpath('./span')[0].text=label;card.xpath('./strong')[0].text=read;card.xpath('./p')[0].text=support
set_text('//div[@class="ownership-note"]/h2','His clearest ideas describe behavior.')
set_text('//div[@class="ownership-note"]/p[1]','In a 2019 Forbes interview, Ishbia used his place on Michigan State’s bench to explain role clarity: he wanted to be the best third-string point guard in the country.')
set_text('//div[@class="ownership-note"]/p[2]','That detail makes the broader language more concrete. Care means developing people. Culture asks the leader to live the standard. Accountability begins with the part each person can own. The Suns remarks bring those ideas into an organization still working to make its identity visible.')
rail=one('//aside[@class="left-rail"]').xpath('./div[@class="rail-block"]')
replace_children('//aside[@class="left-rail"]/div[1]/p','<strong>September 14–27, 2026</strong><br>Current weekly scan; historical interviews are labeled as background.')
replace_children('//aside[@class="left-rail"]/div[2]/p','<strong>Behavior makes a standard visible.</strong><br>The quote categories show the same idea across different settings and years.')
replace_children('//aside[@class="left-rail"]/div[3]/p','<strong>A clearer public reference.</strong><br>Dated Suns positions stay attached to their original context.')

story=one('//div[@id="ownership"]//article[@class="story"]')
for child in list(story):story.remove(child)
source_forbes19='https://www.forbes.com/sites/robdube/2019/05/27/what-playing-for-a-national-championship-winning-basketball-team-taught-this-ceo-about-leadership/'
source_forbes20='https://www.forbes.com/sites/robdube/2020/07/13/business-basketball-and-building-a-winning-work-culture/'
source_fortune='https://fortune.com/2025/05/07/leadership-next-mat-ishbia-united-wholesale-mortgage/'
source_sporting='https://www.sportingnews.com/us/ncaa-basketball/news/mat-ishbia-michigan-state-tom-izzo-billionaire-mortgage/cazxqc2p1fgo1j36vs08gwgn3'
source_arizona='https://arizonasports.com/nba/phoenix-suns/culture-defined'
source_cronkite='https://cronkitenews.azpbs.org/2025/09/24/matt-ishbia-phoenix-suns-culture-driven-team/'
source_impact='https://msualumnipodcasts.transistor.fm/episodes/mat-ishbia-wants-to-impact-as-many-lives-as-possible-in-a-positive-way'
opening=f'''<section><span class="source-tag">The revealing detail</span><h2>The third-string point guard explains the larger idea.</h2><p>Ishbia described a demanding role at Michigan State in a {tag_link('2019 Forbes interview',source_forbes19)}. He could contribute without being a star, and he judged that contribution against the role he had. The example has survived because it gives ordinary work a clear standard.</p><p>His public remarks return to the same test in business and in Phoenix: what a person does each day, how leaders behave and what the group can depend on. That is the throughline of this issue.</p></section>'''
map_items=[
 ('Care','“The most important thing as a leader is a four-letter word called care.”','Fortune, May 7, 2025',source_fortune,'Develop people and attend to the details that affect them.'),
 ('Culture','“You have got to figure out what it is, design it, and live by it.”','Forbes, July 13, 2020',source_forbes20,'A stated culture gains credibility through the leader’s conduct.'),
 ('Role','“I had to be the best third-string point guard in the country.”','Forbes, May 27, 2019',source_forbes19,'The standard is specific to the contribution a person can make.'),
 ('Preparation','“If you start to outsource the little things”','Sporting News, 2021',source_sporting,'Staying close to the work protects execution. The excerpt is part of a longer sentence.'),
 ('Accountability','“I can take the criticism for not defining (that culture) well enough”','Arizona Sports, Aug. 21, 2025',source_arizona,'He places the early Suns culture definition on his own leadership.'),
 ('Improvement','“about 20 more mountains”','Sporting News, 2021',source_sporting,'Progress creates another level of work in his telling.'),
 ('Suns identity','“Do the right things every day, hold each other accountable”','Cronkite News, Sept. 24, 2025',source_cronkite,'Daily conduct is the public standard he described for Phoenix.'),
 ('Impact','“People will remember how you impacted them.”','MSU Today podcast, Nov. 2023',source_impact,'He measures success partly by what people carry away from the relationship.'),
]
quote_cards=[]
for label,quote,attribution,url,meaning in map_items:
 quote_cards.append(f'<article><span class="source-tag">{escape(label)}</span><blockquote>{escape(quote)}</blockquote><p>{escape(meaning)}</p><a href="{escape(url,quote=True)}">{escape(attribution)} ↗</a></article>')
quote_section='<section class="capture-section quote-map"><span class="source-tag">The public record</span><h2>The ideas in his own words.</h2><p>Eight short excerpts from public interviews and remarks. Each one shows a different part of the philosophy, with its original source linked below.</p><div class="capture-grid">'+''.join(quote_cards)+'</div></section>'
closing=f'''<section><span class="source-tag">The Suns application</span><h2>Identity becomes a shared description of the work.</h2><p>The historical Suns remarks bring the broader philosophy into ownership. Ishbia publicly acknowledged that defining culture at the start was his responsibility, and later described daily accountability as part of Phoenix basketball. Those remarks establish his stated standard; this season’s public examples will show how the organization describes it now. {tag_link('Arizona Sports, 2025',source_arizona)} · {tag_link('Cronkite News, 2025',source_cronkite)}</p></section><section><span class="source-tag">The ownership read</span><h2>Listen for the behaviors beneath the language.</h2><p>Media day provides the next public account of the team’s identity. Clear examples of development, responsibility and shared expectations will give the words something observable to stand on.</p></section>'''
for fragment in (opening,quote_section,closing):
 for element in html.fragments_fromstring(fragment):story.append(element)

# Current service lanes use exactly sourced, non-feature developments.
pulse=[
 ('2026-09-16','Announced · Sept. 16','More local games remain within reach.','Arizona’s Family will carry 71 regular-season games on 3TV and Arizona’s Family Sports. Rex Chapman is set to call more than 20 road games. Familiar voices and broad availability make the fan-access promise tangible.','https://arizonasports.com/nba/phoenix-suns/rex-chapman-expanded-tv-role-calling-suns-games','Arizona Sports'),
 ('2026-09-16','Reported · Sept. 16','Depth was added before camp.','Arizona Sports reported Phoenix signed Duop Reath after Mark Williams’s shoulder surgery. The move adds a depth option. His role and Williams’s return timeline remain team questions.','https://arizonasports.com/nba/phoenix-suns/phoenix-suns-sign-duop-reath-for-depth-after-mark-williams-injury','Arizona Sports'),
 ('2026-09-22','NBA preview · Sept. 22','Last season sets the baseline.','The NBA’s season preview records Phoenix at 45–37 in 2025–26 and ninth in defensive ranking. Repeating the habits behind that improvement is a useful early-season question.','https://www.nba.com/news/2026-27-season-preview-phx','NBA.com'),
]
league=[
 ('2026-09-13','Official statement · Sept. 13','The Clippers case reached the owner’s desk.','Steve Ballmer accepted responsibility for the organization’s compliance failures and said the fine had been paid. The episode shows how league enforcement reaches ownership.','https://www.nba.com/news/statement-from-clippers-governor-steve-ballmer','NBA.com'),
 ('2026-09-15','League report · Sept. 15','Expansion remains an open decision.','Adam Silver said the league aims to reach a decision by year-end. Market and arena questions remain in front of the Board. No franchise award has been announced.','https://www.nba.com/news/adam-silver-board-of-governors-september-2026','NBA.com'),
 ('2026-09-15','League report · Sept. 15','Europe still depends on negotiation.','Silver described ongoing talks around the intended 2027 European league. Existing basketball institutions remain part of the conversation, with structure unresolved.','https://www.nba.com/news/adam-silver-board-of-governors-september-2026','NBA.com'),
 ('2026-09-15','League report · Sept. 15','Board leadership changes during a busy period.','Micky Arison now chairs the Board of Governors. The transition comes as the league weighs expansion and international plans.','https://www.nba.com/news/adam-silver-board-of-governors-september-2026','NBA.com'),
 ('2026-09-27','City status · reviewed Sept. 27','Portland’s arena plan still needs an agreement.','The city describes a proposed financing arrangement tied to a new 20-year lease, with a December 2026 deadline in the state framework. Civic approval and an executable lease remain the watch points.','https://www.portland.gov/venues/moda-center/moda-project-overview/moda-whats-next-get-facts','City of Portland'),
]
def render_cards(cards):
 return ''.join(f'<article><span><time datetime="{d}">{escape(status)}</time></span><h3>{escape(head)}</h3><p>{escape(body)}</p><a href="{escape(url,quote=True)}">{escape(label)} ↗</a></article>' for d,status,head,body,url,label in cards)
for section_id,cards,heading in [('suns-pulse',pulse,'Three signals outside the feature.'),('league',league,'Five ownership developments.')]:
 sec=one(f'//section[@id="{section_id}"]');sec.set('data-reporting-window','2026-09-14/2026-09-27')
 sec.xpath('./div[@class="roundup-heading"]/h2')[0].text=heading
 replace_children(f'//section[@id="{section_id}"]/div[@class="roundup-grid"]',render_cards(cards))
replace_children('//section[@id="suns-pulse"]/p[@class="count-note"]','<strong>Reporting cutoff:</strong> September 27, 2026. The preview supplies prior-season context; current items are September 16–22.')

cal=one('//section[@id="calendar"]')
cal.xpath('./h2')[0].text='Media day opens the next three weeks.'
fig=cal.xpath('./figure')[0];fig.set('aria-label','Selected Suns and NBA dates, September 28 through October 18, 2026')
fig.xpath('./div[@class="calendar-heading"]/span')[0].text='Three weeks ahead'
fig.xpath('./div[@class="calendar-heading"]/strong')[0].text='September 28 – October 18, ';fig.xpath('./div[@class="calendar-heading"]/strong/small')[0].text='2026'
events={
 '2026-09-28':('suns','Media day'),
 '2026-09-29':('league','Camps open'),
 '2026-10-03':('league','NBA preseason'),
 '2026-10-05':('suns','at Detroit'),
 '2026-10-07':('suns','at Chicago'),
 '2026-10-10':('suns','vs San Antonio'),
 '2026-10-14':('suns','at San Antonio'),
 '2026-10-16':('suns','vs Utah'),
}
from datetime import date,timedelta
start=date(2026,9,28)
rows=[]
for w in range(3):
 cells=[]
 for offset in range(7):
  day=start+timedelta(days=w*7+offset); iso=day.isoformat(); item=events.get(iso)
  css='has-'+item[0] if item else ''
  label=(f'<span class="calendar-event {item[0]}-event" role="img" aria-label="{escape(item[1])}"><span class="event-full">{escape(item[1])}</span><span class="event-short" aria-hidden="true">{escape(item[1])}</span></span>' if item else '')
  cells.append(f'<td data-calendar-date="{iso}" class="{css}"><span class="calendar-number">{day.day}</span>{label}</td>')
 rows.append('<tr>'+''.join(cells)+'</tr>')
table='<table class="calendar-table"><caption class="calendar-sr-only">Selected Suns and NBA dates, September 28 through October 18, 2026.</caption><thead><tr>'+''.join(f'<th scope="col">{d}</th>' for d in ('Mon','Tue','Wed','Thu','Fri','Sat','Sun'))+'</tr></thead><tbody>'+''.join(rows)+'</tbody></table>'
replace('//figure[@class="calendar-board"]/*[self::div[@class="calendar-placeholder"] or self::table[@class="calendar-table"]]',html.tostring(html.fragment_fromstring(table),encoding='unicode'))
fig.xpath('./figcaption/span')[0].text='Schedule is current as of September 27.'
replace_children('//section[@id="calendar"]/div[@class="calendar-details"]','''<div class="calendar-suns"><h3 class="calendar-lane">Phoenix</h3><div class="scoreboard-grid"><article><span>MONDAY · SEPTEMBER 28</span><h3>Suns media day</h3><small class="calendar-status">Scheduled · NBA</small><p>10 a.m. Arizona. Listen for current descriptions of identity, preparation and shared responsibility.</p></article><article><span>MONDAY · OCTOBER 5</span><h3>Preseason at Detroit</h3><small class="calendar-status">Scheduled</small><p>The first listed Suns preseason game begins the on-court evidence window.</p></article><article><span>OCTOBER 7, 10, 14 AND 16</span><h3>Four more preseason dates</h3><small class="calendar-status">Scheduled</small><p>At Chicago; home and away against San Antonio; home against Utah.</p></article></div></div><div class="calendar-league"><h3 class="calendar-lane">Around the NBA</h3><article><span class="calendar-date">TUESDAY · SEPTEMBER 29</span><h4>Training camps open</h4><small class="calendar-status">Scheduled · NBA</small><p>The league’s collective preparation period begins.</p><a href="https://www.nba.com/news/key-dates">NBA key dates ↗</a></article><article><span class="calendar-date">SATURDAY · OCTOBER 3</span><h4>Preseason begins</h4><small class="calendar-status">Scheduled · NBA</small><p>First league preseason games.</p><a href="https://www.nba.com/news/key-dates">NBA key dates ↗</a></article></div>''')
replace_children('//section[@id="calendar"]/p[@class="count-note"]','Calendar sources: <a href="https://www.nba.com/news/nba-media-days-schedule-for-all-30-teams">NBA media-day schedule</a>, <a href="https://www.nba.com/news/key-dates">NBA key dates</a>, <a href="https://arizonasports.com/nba/phoenix-suns/suns-reveal-2026-preseason-schedule">Phoenix preseason announcement</a> and <a href="https://www.nba.com/team/1610612756/schedule">current NBA team schedule</a>. Game times should be checked against the current NBA schedule.')

sources=[
 ('Forbes · Rob Dube · May 27, 2019',source_forbes19,'role and third-string point guard quotation','Reported background'),
 ('Forbes · Rob Dube · July 13, 2020',source_forbes20,'culture quotation','Reported background'),
 ('Sporting News · Mike DeCourcy · 2021',source_sporting,'execution and continuous-improvement fragments','Original interview background'),
 ('Fortune · Leadership Next · May 7, 2025',source_fortune,'care quotation','Original interview background'),
 ('Arizona Sports · Burns & Gambo · Aug. 21, 2025',source_arizona,'culture-accountability excerpt','Original interview background'),
 ('Cronkite News · Sept. 24, 2025',source_cronkite,'Suns daily-standard excerpt','Reported background'),
 ('MSU Today podcast · Nov. 2023',source_impact,'impact excerpt','Original audio background'),
 ('Arizona Sports · Sept. 16, 2026','https://arizonasports.com/nba/phoenix-suns/rex-chapman-expanded-tv-role-calling-suns-games','Suns local broadcast plan','Reported current'),
 ('Arizona Sports · Sept. 16, 2026','https://arizonasports.com/nba/phoenix-suns/phoenix-suns-sign-duop-reath-for-depth-after-mark-williams-injury','reported Reath depth signing','Reported current'),
 ('NBA.com · Sept. 22, 2026','https://www.nba.com/news/2026-27-season-preview-phx','prior-season Phoenix baseline','League preview'),
 ('NBA.com · Sept. 13, 2026','https://www.nba.com/news/statement-from-clippers-governor-steve-ballmer','Ballmer response','Official statement'),
 ('NBA.com · Sept. 15, 2026','https://www.nba.com/news/adam-silver-board-of-governors-september-2026','expansion, Europe and board leadership','League report'),
 ('City of Portland · reviewed Sept. 27, 2026','https://www.portland.gov/venues/moda-center/moda-project-overview/moda-whats-next-get-facts','proposed Moda Center financing and lease deadline','Official ongoing'),
 ('NBA · reviewed Sept. 27, 2026','https://www.nba.com/news/nba-media-days-schedule-for-all-30-teams','Suns media day','Official schedule'),
 ('NBA · reviewed Sept. 27, 2026','https://www.nba.com/news/key-dates','camp and preseason start','Official schedule'),
 ('Arizona Sports · July 2026','https://arizonasports.com/nba/phoenix-suns/suns-reveal-2026-preseason-schedule','five Suns preseason dates','Reported schedule'),
 ('NBA team schedule · reviewed Sept. 27, 2026','https://www.nba.com/team/1610612756/schedule','Oct. 10 timing discrepancy','Official schedule'),
]
ledger=''.join(f'<li><a href="{escape(url,quote=True)}">{escape(label)}</a> · {escape(status)} · {escape(claim)}.</li>' for label,url,claim,status in sources)
replace_children('//section[@id="sources"]/ol',ledger)
set_text('//section[@id="sources"]/p[@class="count-note"]','Reviewed September 27, 2026. The philosophy read is AVC analysis based on linked public remarks. No public-reaction sample was used in this edition.')

out='<!doctype html>\n'+html.tostring(ROOT,encoding='unicode',method='html')+'\n'
import re
left=set(re.findall(r'\[\[REPLACE:[^\]]+\]\]',out))
print('remaining',left)
assert not left
assert not re.search(r'\bMatt\b', ''.join(t for t in ROOT.xpath('//text()[not(ancestor::script)]')))
(HERE/'index.html').write_text(out)
print('Built',HERE/'index.html','with',len(pulse),'Suns items,',len(league),'league items and',len(map_items),'feature excerpts')
