import fs from 'fs';
import {JSDOM} from 'jsdom';
const html=fs.readFileSync('index.html','utf8');
const errors=[];let raf=[];
const dom=new JSDOM(html,{runScripts:'dangerously',resources:'usable',pretendToBeVisual:true,url:'https://neon-rumble.test/',beforeParse(window){
 window.scrollTo=()=>{};window.ResizeObserver=class{observe(){}disconnect(){}};window.AudioContext=class{};window.webkitAudioContext=window.AudioContext;
 window.requestAnimationFrame=(cb)=>{raf.push(cb);return raf.length};window.cancelAnimationFrame=()=>{};
 Object.defineProperty(window.HTMLCanvasElement.prototype,'getContext',{value(){const fn=()=>{};return new Proxy({canvas:this,measureText:()=>({width:10})},{get(t,p){if(p in t)return t[p];return fn},set(t,p,v){t[p]=v;return true}})}});
 window.addEventListener('error',e=>errors.push(String(e.error?.stack||e.message||e.error)));window.addEventListener('unhandledrejection',e=>errors.push(String(e.reason?.stack||e.reason)));
}});
await new Promise(r=>setTimeout(r,60));
if(errors.length) throw new Error('boot errors: '+errors.join('\n'));
const {Engine,ROSTER}=dom.window.DuelEngine||{};if(!Engine||!ROSTER)throw new Error('engine unavailable');
if(!ROSTER.find(x=>x.id==='snowman'))throw new Error('snowman missing');
if(!ROSTER.find(x=>x.id==='angryman'))throw new Error('angryman missing');

{
 const g=new Engine('devileye','boxer',()=>.5);const h=g.spawnCursedHand(g.fighters[0],g.fighters[0]);if(h.hp!==66)throw new Error('hand hp not 66');console.log('CURSED_HAND_HP_66_OK');
}
{
 const g=new Engine('knight','boxer',()=>.5);const k=g.fighters[0],e=g.fighters[1];g.time=k.knightGiantNext;g.knightGiantSlash(k,e);const s=g.shots.find(x=>x.kind==='giantslash');if(!s||s.damage!==150)throw new Error('knight giant slash wrong');console.log('KNIGHT_GIANT_SLASH_150_OK');
}
{
 const g=new Engine('snowman','phoenix',()=>.4);const s=g.fighters[0],e=g.fighters[1];g.snowmanShot(s,e);const shot=g.shots.find(x=>x.kind==='snow');if(!shot||shot.damage!==30||shot.stun!==1)throw new Error('snow shot/freeze wrong');
 e.burn={source:s.side,damage:10,interval:.5,next:.5,expires:1};g.time=.5;const before=e.health;g.tickBurn(e);if(before-e.health!==50)throw new Error('snowman burn x5 wrong');console.log('SNOWMAN_FREEZE_BURN_OK');
}
{
 const g=new Engine('angryman','boxer',()=>.5);const a=g.fighters[0];if(a.hp!==333||a.icon!=='😠')throw new Error('angry base wrong');a.health=0;if(!g.formEgg(a)||a.revivals!==1||a.icon!=='😡'||a.health!==333)throw new Error('angry revive 1 wrong');a.health=0;if(!g.formEgg(a)||a.revivals!==2||a.icon!=='🤬'||a.health!==333)throw new Error('angry revive 2 wrong');a.health=0;if(g.formEgg(a))throw new Error('angry revived more than twice');console.log('ANGRY_TWO_REVIVES_OK');
}
if(errors.length)throw new Error('runtime errors: '+errors.join('\n'));
console.log('V326_RUNTIME_OK');
