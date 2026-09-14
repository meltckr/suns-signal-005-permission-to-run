/** Verify the selected three-week calendar without network or browser dependencies. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {inspectHtml, verifyIssue009} from './verify_issue_009_premium.mjs';

const html = fs.readFileSync('issue-009/index.html', 'utf8');
verifyIssue009(html); // Keep the original editorial, audio and asset locks.
const page = inspectHtml(html);
assert.deepEqual(page.calendar_weekdays, ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']);
assert.equal(page.calendar_cells.length, 21, 'Three complete weeks are required');
const expectedEvents = {
  '2026-09-14': [['owners','Reported']],
  '2026-09-15': [['owners','Reported']],
  '2026-09-22': [['openhouse','Official'],['early-camp','Official']],
  '2026-09-28': [['media-day','Reported']],
  '2026-09-29': [['camp','Official']],
  '2026-10-03': [['preseason','Official']],
};
for (const [index, cell] of page.calendar_cells.entries()) {
  const expectedDate = new Date(Date.UTC(2026, 8, 14 + index));
  const iso = expectedDate.toISOString().slice(0, 10);
  assert.equal(cell.date, iso, 'Calendar date order/alignment changed');
  assert.equal(expectedDate.getUTCDay(), (index + 1) % 7, 'Incorrect weekday column');
  assert.equal(cell.number, iso === '2026-10-01' ? '1 Oct' : String(expectedDate.getUTCDate()), 'Visible day does not match date');
  assert.deepEqual(cell.events.map(e => [e['data-calendar-event'],e['data-status']]), expectedEvents[iso] || [], `Event/date/status mismatch on ${iso}`);
  for (const event of cell.events) {
    assert.equal(event.role, 'img', 'Event badge needs a naming-supported role');
    assert(event['aria-label']?.length > 15 && event['aria-label'].includes(event['data-status'].toLowerCase()), 'Abbreviated event needs an accessible full label and source status');
  }
}
for (const label of ['Three weeks ahead','Official','Reported','For teams playing outside North America.','Whether a vote will occur remains uncertain.','Reported · Suns preseason opener']) assert(page.visible_text.includes(label), `Missing calendar qualification: ${label}`);
assert(html.includes('<caption class="calendar-sr-only">'), 'Calendar needs a table caption');
assert(html.includes('href="calendar.css?v=009-calendar-v1"'), 'Calendar stylesheet is not loaded');
assert(!/NBA tips off|Overseas camp|aria-current="date"/.test(html), 'Avoid ambiguous preseason/camp labels or live-today labels in an archived edition');
const css = fs.readFileSync('issue-009/calendar.css', 'utf8');
assert(css.includes('@media(max-width:760px)') && css.includes('@media print'), 'Responsive and print styles required');
console.log('PASS: 21 consecutive dates, Monday-first columns, seven correctly dated event markers, source statuses, accessible labels and unchanged editorial/audio assets.');
