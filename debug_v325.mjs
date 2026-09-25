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
if(!eye||eye.hp!==666) throw new Error('Devil Eye roster missing/HP wrong');

// Police barrage: exactly 5 seconds.
{
  const g=new Engine('police','boxer',()=>.5);const p=g.fighters[0];
  g.startPoliceBarrage(p);
  if(Math.abs((p.policeBarrageUntil-g.time)-5)>1e-9) throw new Error('Police barrage is not 5 seconds');
  console.log('POLICE_5S_OK');
}

// Devil Eye contact curse must affect status-immune Moai and tick for 10 every .3 seconds.
{
  const g=new Engine('devileye','moai',()=>.5);const d=g.fighters[0],m=g.fighters[1];
  d.x=m.x=360;d.y=m.y=360;g.collide(d,m);
  if(!m.curse) throw new Error('Moai did not receive curse on contact');
  const hp=m.health;
  for(let i=0;i<40;i++) g.step(1/120);
  if(m.health>hp-10+1e-9) throw new Error('Curse did not tick for 10 damage');
  console.log('CURSE_IMMUNITY_BYPASS_OK');

  // Run long enough to exercise cursed-target 4s summons, hand homing shots, 5s expiry, and own 13s summon.
  let firstHand=null;
  for(let i=0;i<1700&&g.result===null;i++){
    g.step(1/120);
    if(!firstHand) firstHand=g.fighters.find(f=>f.id==='cursedhand');
  }
  if(!firstHand) throw new Error('No cursed hand spawned');
  if(firstHand.expiresAt-firstHand.createdAt>5.000001) throw new Error('Hand lifetime marker invalid');
  if(d.nextCursedHand<=13) throw new Error('Devil Eye 13-second summon timer did not advance');
  if(errors.length) throw new Error('runtime errors: '+errors.join('\n'));
  console.log('CURSED_HAND_RUNTIME_OK');
}

// Boss Devil Eye's hand gets only x1.5 summon scaling.
{
  const g=new Engine('devileye','boxer',()=>.5,{mode:'boss',allies:['boxer','archer','knight','mage','vampire']});
  const owner=g.fighters[0],h=g.spawnCursedHand(owner,owner);
  if(!h) throw new Error('Boss cursed hand did not spawn');
  if(Math.abs(h.scale-1.5)>1e-9) throw new Error('Boss hand scale is not 1.5');
  if(Math.abs(h.hp-169.5)>1e-9) throw new Error('Boss hand HP is not 113 x 1.5');
  console.log('BOSS_HAND_1_5X_OK');
}

console.log('V325_RUNTIME_OK');
