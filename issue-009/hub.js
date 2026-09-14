// Issue-scoped navigation shell. The shared audio element stays mounted once.
const hub = document.querySelector('#hub');
const views = [...document.querySelectorAll('[data-section-view]')];
const toolbar = document.querySelector('.section-toolbar');
const footer = document.querySelector('.site-footer');
const labels = {hub:'Home', ownership:'Ownership', pulse:'Suns Weekly Pulse', league:'Around The League', calendar:'Calendar Ahead', sources:'Source Ledger'};
const aliases = {top:'hub', 'suns-pulse':'pulse'};
let lastTile = null;
let focusAudio = false;
let firstLoad = true;

document.querySelectorAll('[data-hub-tile]').forEach(tile => tile.addEventListener('click', () => { lastTile = tile; }));
document.querySelector('[data-listen-link]').addEventListener('click', () => { focusAudio = true; });

function route() {
  const requested = location.hash.slice(1).toLowerCase();
  const name = Object.hasOwn(aliases, requested) ? aliases[requested] : (Object.hasOwn(labels, requested) ? requested : 'hub');
  if (location.hash !== `#${name}`) history.replaceState(null, '', `#${name}`);
  const atHome = name === 'hub';
  hub.hidden = !atHome;
  views.forEach(view => { view.hidden = view.dataset.sectionView !== name; });
  toolbar.hidden = atHome;
  footer.hidden = atHome;
  document.body.dataset.route = name;
  document.querySelector('.current-section').textContent = labels[name];
  document.title = atHome ? 'Suns Signal 009 | The Next Step Starts Early' : `${labels[name]} | Suns Signal 009`;
  const target = atHome ? (lastTile || hub.querySelector('h1')) : views.find(view => view.dataset.sectionView === name).querySelector('h2');
  if (target && !target.hasAttribute('tabindex')) target.tabIndex = -1;
  // Native fragment scrolling can run before panels are shown; settle it here.
  requestAnimationFrame(() => {
    window.scrollTo({top:0, behavior:'instant'});
    if (!firstLoad) target?.focus({preventScroll:true});
    if (focusAudio) {
      const player = hub.querySelector('mel-audio-player');
      player.scrollIntoView({block:'center', behavior:'instant'});
      player.shadowRoot?.querySelector('.play')?.focus({preventScroll:true});
      focusAudio = false;
    }
    firstLoad = false;
  });
}
window.addEventListener('hashchange', route);
document.addEventListener('keydown', event => {
  if (event.key !== 'Escape' || document.body.dataset.route === 'hub') return;
  if (event.target.closest('input,textarea,select,[contenteditable="true"]')) return;
  event.preventDefault();
  location.hash = 'hub';
});
route();
