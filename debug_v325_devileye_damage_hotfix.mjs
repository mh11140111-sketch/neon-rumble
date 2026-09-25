import fs from 'fs';
import {JSDOM} from 'jsdom';

const html=fs.readFileSync('index.html','utf8');
const errors=[]; let raf=[];
const dom=new JSDOM(html,{runScripts:'dangerously',resources:'usable',pretendToBeVisual:true,url:'https://neon-rumble.test/',beforeParse(window){
  window.scrollTo=()=>{};
  window.ResizeObserver=class{observe(){}disconnect(){}};
  window.AudioContext=class{}; window.webkitAudioContext=window.AudioContext;
  window.requestAnimationFrame=(cb)=>{raf.push(cb);return raf.length};
  window.cancelAnimationFrame=()=>{};
  Object.defineProperty(window.HTMLCanvasElement.prototype,'getContext',{value(){const fn=()=>{};return new Proxy({canvas:this,measureText:()=>({width:10})},{get(t,p){if(p in t)return t[p];return fn},set(t,p,v){t[p]=v;return true}})}});
  window.addEventListener('error',e=>errors.push(String(e.error?.stack||e.message||e.error)));
  window.addEventListener('unhandledrejection',e=>errors.push(String(e.reason?.stack||e.reason)));
}});
await new Promise(r=>setTimeout(r,60));
if(errors.length) throw new Error('boot errors: '+errors.join('\n'));
const {Engine,ROSTER}=dom.window.DuelEngine||{};
if(!Engine||!ROSTER) throw new Error('DuelEngine unavailable');
const eye=ROSTER.find(c=>c.id==='devileye');
if(!eye||eye.damage!==50) throw new Error('Devil Eye roster damage is not 50');

// Contact: first curse contact deals direct 50 before curse DOT.
{
  const g=new Engine('devileye','boxer',()=>.5); const d=g.fighters[0], e=g.fighters[1];
  d.x=e.x=360; d.y=e.y=360; const hp=e.health;
  g.collide(d,e);
  if(!e.curse) throw new Error('Devil Eye contact did not curse');
  if(Math.abs(e.health-(hp-50))>1e-9) throw new Error(`Devil Eye direct contact damage wrong: ${hp-e.health}`);
  console.log('DEVIL_EYE_CONTACT_50_OK');
}

// Hand projectile: normal hand deals 50 direct + curse.
{
  const g=new Engine('devileye','boxer',()=>.5); const owner=g.fighters[0], e=g.fighters[1];
  const h=g.spawnCursedHand(owner,owner,true); const hp=e.health;
  g.attackProjectile(h,e,{curseOnly:true,damage:50});
  if(Math.abs(e.health-(hp-50))>1e-9) throw new Error(`Cursed Hand direct damage wrong: ${hp-e.health}`);
  if(!e.curse) throw new Error('Cursed Hand projectile did not curse');
  console.log('CURSED_HAND_PROJECTILE_50_OK');
}

// Boss hand remains x1.5 scaling: 50 -> 75.
{
  const g=new Engine('devileye','boxer',()=>.5,{mode:'boss',allies:['boxer','archer','knight','mage','vampire']});
  const owner=g.fighters[0], h=g.spawnCursedHand(owner,owner,true);
  if(Math.abs(h.damage-75)>1e-9) throw new Error('Boss cursed hand damage is not 75');
  console.log('BOSS_CURSED_HAND_75_OK');
}

if(errors.length) throw new Error('runtime errors: '+errors.join('\n'));
console.log('V325_DEVILEYE_DAMAGE_HOTFIX_OK');
