import fs from 'fs';
import {JSDOM} from 'jsdom';

const html=fs.readFileSync('index.html','utf8');
const errors=[];
const dom=new JSDOM(html,{runScripts:'dangerously',resources:'usable',pretendToBeVisual:true,url:'https://neon-rumble.test/',beforeParse(window){
  window.scrollTo=()=>{};
  window.ResizeObserver=class{observe(){}disconnect(){}};
  window.AudioContext=class{}; window.webkitAudioContext=window.AudioContext;
  window.requestAnimationFrame=()=>1; window.cancelAnimationFrame=()=>{};
  Object.defineProperty(window.HTMLCanvasElement.prototype,'getContext',{value(){const fn=()=>{};return new Proxy({canvas:this,measureText:()=>({width:10})},{get(t,p){if(p in t)return t[p];return fn},set(t,p,v){t[p]=v;return true}})}});
  window.addEventListener('error',e=>errors.push(String(e.error?.stack||e.message||e.error)));
  window.addEventListener('unhandledrejection',e=>errors.push(String(e.reason?.stack||e.reason)));
}});
await new Promise(r=>setTimeout(r,60));
if(errors.length) throw new Error('boot errors: '+errors.join('\n'));
const {Engine}=dom.window.DuelEngine||{};
if(!Engine) throw new Error('DuelEngine unavailable');

const g=new Engine('devileye','boxer',()=>.5);
const eye=g.fighters[0],enemy=g.fighters[1];

// Curse-generated hand: still 5 seconds.
const temporary=g.spawnCursedHand(eye,enemy,false);
if(!temporary) throw new Error('temporary hand missing');
if(!Number.isFinite(temporary.expiresAt)||Math.abs((temporary.expiresAt-g.time)-5)>1e-9) throw new Error('curse-generated hand is not 5 seconds');
if(temporary.persistentHand) throw new Error('temporary hand marked persistent');
console.log('CURSE_HAND_5S_OK');

// Body-generated hand: permanent.
const permanent=g.spawnCursedHand(eye,eye,true);
if(!permanent) throw new Error('permanent hand missing');
if(permanent.expiresAt!==Infinity) throw new Error('body hand is not infinite');
if(!permanent.persistentHand) throw new Error('body hand persistent flag missing');
g.time=1000;
g.cursedHandSkill(permanent,1/120);
if(permanent.health<=0) throw new Error('permanent hand expired by time');
console.log('BODY_HAND_INFINITE_OK');

// Verify the actual 13-second Devil Eye skill uses the permanent path.
const g2=new Engine('devileye','boxer',()=>.5);
const eye2=g2.fighters[0];
g2.time=13; eye2.nextCursedHand=13;
const before=g2.fighters.length;
g2.devilEyeSkill(eye2);
const autoHand=g2.fighters.slice(before).find(f=>f.id==='cursedhand');
if(!autoHand||autoHand.expiresAt!==Infinity||!autoHand.persistentHand) throw new Error('13-second body summon is not permanent');
console.log('BODY_13S_SUMMON_INFINITE_OK');

console.log('V325_HAND_PERSIST_OK');
