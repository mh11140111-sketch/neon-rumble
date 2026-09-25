import fs from 'fs';
import {JSDOM} from 'jsdom';

const html=fs.readFileSync('index.html','utf8');
const errors=[];let raf=[];
const dom=new JSDOM(html,{runScripts:'dangerously',resources:'usable',pretendToBeVisual:true,url:'https://neon-rumble.test/',beforeParse(window){
  window.scrollTo=()=>{};
  window.ResizeObserver=class{observe(){}disconnect(){}};
  window.AudioContext=class{};window.webkitAudioContext=window.AudioContext;
  window.requestAnimationFrame=(cb)=>{raf.push(cb);return raf.length};
  window.cancelAnimationFrame=()=>{};
  Object.defineProperty(window.HTMLCanvasElement.prototype,'getContext',{value(){const fn=()=>{};return new Proxy({canvas:this,measureText:()=>({width:10})},{get(t,p){if(p in t)return t[p];return fn},set(t,p,v){t[p]=v;return true}})}});
  window.addEventListener('error',e=>errors.push(String(e.error?.stack||e.message||e.error)));
}});
await new Promise(r=>setTimeout(r,60));
if(errors.length) throw new Error(errors.join('\n'));
const {Engine}=dom.window.DuelEngine||{};
if(!Engine) throw new Error('DuelEngine unavailable');

// Normal Cursed Hand: projectile direct damage 25 + curse.
{
  const g=new Engine('devileye','boxer',()=>.5);const eye=g.fighters[0],enemy=g.fighters[1];
  const h=g.spawnCursedHand(eye,eye,true);
  if(Math.abs(h.damage-25)>1e-9) throw new Error('Normal Cursed Hand damage stat is not 25');
  const hp=enemy.health;
  g.attackProjectile(h,enemy,{curseOnly:true,damage:25,kind:'curseorb'});
  if(Math.abs((hp-enemy.health)-25)>1e-9) throw new Error('Normal Cursed Hand projectile did not deal 25');
  if(!enemy.curse) throw new Error('Cursed Hand projectile did not apply curse');
  console.log('CURSED_HAND_25_OK');
}

// Boss hand receives only x1.5 scaling: 37.5.
{
  const g=new Engine('devileye','boxer',()=>.5,{mode:'boss',allies:['boxer','archer','knight','mage','vampire']});
  const eye=g.fighters[0];const h=g.spawnCursedHand(eye,eye,true);
  if(Math.abs(h.damage-37.5)>1e-9) throw new Error('Boss Cursed Hand damage stat is not 37.5');
  console.log('BOSS_CURSED_HAND_37_5_OK');
}

// Devil Eye body contact damage stays 50.
{
  const g=new Engine('devileye','boxer',()=>.5);const eye=g.fighters[0],enemy=g.fighters[1];
  eye.x=enemy.x=360;eye.y=enemy.y=360;const hp=enemy.health;g.collide(eye,enemy);
  if(Math.abs((hp-enemy.health)-50)>1e-9) throw new Error('Devil Eye contact damage changed from 50');
  console.log('DEVIL_EYE_CONTACT_50_STILL_OK');
}
console.log('V325_CURSED_HAND_25_HOTFIX_OK');
