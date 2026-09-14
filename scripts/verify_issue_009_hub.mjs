// Exercise the actual router in a small DOM fixture; visual proof remains separate.
import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const handlers = {};
const elements = new Map();
const make = (name, dataset={}) => ({
  name, dataset, hidden:false, attrs:{}, listeners:{},
  addEventListener(event, fn) { this.listeners[event]=fn; },
  hasAttribute(key) { return Object.hasOwn(this.attrs,key); },
  focus() { elements.set('focused',this.name); },
  scrollIntoView() {},
  querySelector(selector) { return elements.get(`${name}:${selector}`); },
});
const views=['ownership','pulse','league','calendar','sources'].map(name=>make(name,{sectionView:name}));
views.forEach(view=>elements.set(`${view.name}:h2`,make(`${view.name}-heading`)));
const tiles=views.map(view=>make(`${view.name}-tile`));
const hub=make('hub');
elements.set('hub:h1',make('hub-heading'));
const player=make('player');
player.shadowRoot={querySelector:()=>make('play-button')};
elements.set('hub:mel-audio-player',player);
const toolbar=make('toolbar'),footer=make('footer'),label=make('label'),listen=make('listen');
const document={body:{dataset:{}},title:'',querySelector(selector) { return {'#hub':hub,'.section-toolbar':toolbar,'.site-footer':footer,'.current-section':label,'[data-listen-link]':listen}[selector]; },querySelectorAll(selector) { return {'[data-section-view]':views,'[data-hub-tile]':tiles}[selector]; },addEventListener(event,fn) {handlers[event]=fn;} };
const location={hash:''};
const context={document,location,history:{replaceState(_a,_b,hash){location.hash=hash;}},window:{addEventListener(event,fn){handlers[event]=fn;},scrollTo(){}},requestAnimationFrame:fn=>fn()};
vm.runInNewContext(fs.readFileSync('issue-009/hub.js','utf8'),context);
const check=name=>{
  assert.equal(document.body.dataset.route,name);
  assert.equal(hub.hidden,name!=='hub');
  assert.deepEqual(views.filter(v=>!v.hidden).map(v=>v.dataset.sectionView),name==='hub'?[]:[name]);
  assert.equal(toolbar.hidden,name==='hub');
};
check('hub');
for(const name of ['ownership','pulse','league','calendar','sources']) {
  location.hash='#'+name;handlers.hashchange();check(name);
  assert.equal(elements.get('focused'),name+'-heading');
  location.hash='#hub';handlers.hashchange();check('hub');
}
for(const [hash,expected] of [['#suns-pulse','pulse'],['#top','hub'],['#unknown','hub'],['#constructor','hub'],['#__proto__','hub'],['#LEAGUE','league']]) {
  location.hash=hash;handlers.hashchange();check(expected);
  assert.equal(location.hash,'#'+expected);
}
let prevented=false;
handlers.keydown({key:'Escape',target:{closest:()=>null},preventDefault(){prevented=true;}});
assert(prevented);assert.equal(location.hash,'hub');
location.hash='#hub';handlers.hashchange();check('hub');
tiles[1].listeners.click();location.hash='#pulse';handlers.hashchange();
location.hash='#hub';handlers.hashchange();assert.equal(elements.get('focused'),'pulse-tile');
listen.listeners.click();handlers.hashchange();assert.equal(elements.get('focused'),'play-button');
const html=fs.readFileSync('issue-009/index.html','utf8');
assert.equal((html.match(/<mel-audio-player\b/g)||[]).length,1);
assert.equal((html.match(/data-hub-tile=/g)||[]).length,5);
assert(!/\.remove\(|\.replaceWith\(|innerHTML\s*=/.test(fs.readFileSync('issue-009/hub.js','utf8')),'Keep the audio element mounted while routing');
console.log('PASS: actual hub router, five isolated views, legacy/deep/unknown hashes, Home, Escape, focus return, Listen focus and one persistent player.');
