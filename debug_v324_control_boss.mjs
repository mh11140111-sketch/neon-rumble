import fs from 'fs';
import {JSDOM} from 'jsdom';

const html=fs.readFileSync('index.html','utf8');

async function boot({unlocked=false}={}){
  const errors=[]; let raf=[];
  const dom=new JSDOM(html,{runScripts:'dangerously',resources:'usable',pretendToBeVisual:true,url:'https://neon-rumble.vercel.app/',beforeParse(window){
    if(unlocked) window.localStorage.setItem('neonRumble.controlBossUnlocked.v1','1');
    window.scrollTo=()=>{};
    window.ResizeObserver=class{observe(){}disconnect(){}};
    window.AudioContext=class{}; window.webkitAudioContext=window.AudioContext;
    window.requestAnimationFrame=(cb)=>{raf.push(cb);return raf.length};
    window.cancelAnimationFrame=()=>{};
    Object.defineProperty(window.HTMLCanvasElement.prototype,'getContext',{value(){
      const fn=()=>{};
      return new Proxy({canvas:this,measureText:()=>({width:10})},{get(t,p){if(p in t)return t[p];return fn},set(t,p,v){t[p]=v;return true}});
    }});
    window.addEventListener('error',e=>errors.push(String(e.error?.stack||e.message||e.error)));
    window.addEventListener('unhandledrejection',e=>errors.push(String(e.reason?.stack||e.reason)));
  }});
  await new Promise(r=>setTimeout(r,40));
  return {dom,errors,getRaf:()=>raf,setRaf:v=>{raf=v}};
}

{
  const {dom,errors}=await boot();
  const d=dom.window.document,b=d.getElementById('boss-control-entry');
  if(!b) throw new Error('boss-control-entry missing');
  if(!b.disabled) throw new Error('controlled boss must be locked before stage 2 clear');
  if(!b.textContent.includes('STAGE 2')) throw new Error('locked label missing stage 2 requirement');
  if(errors.length) throw new Error(errors.join('\n'));
  console.log('CONTROL_BOSS_LOCKED_STATE_OK');
}

{
  const {dom,errors,getRaf,setRaf}=await boot({unlocked:true});
  const d=dom.window.document,b=d.getElementById('boss-control-entry');
  if(b.disabled) throw new Error('persisted controlled boss unlock was not restored');
  if(!b.textContent.includes('조정 보스전')) throw new Error('unlocked label missing');
  b.click();
  const start=d.getElementById('start');
  if(start.hidden) throw new Error('boss-control selection UI start button hidden');
  const bossRules=d.getElementById('boss-rules');
  if(bossRules.hidden) throw new Error('boss rules should be visible in controlled boss selection');
  start.click();
  if(d.getElementById('battle').hidden) throw new Error('controlled boss battle did not start');
  if(d.getElementById('control-stick').hidden) throw new Error('controlled boss stick hidden');
  if(d.getElementById('battle-mode').textContent!=='CONTROL BOSS') throw new Error('controlled boss battle label missing');
  let now=0;
  for(let frame=0;frame<480;frame++){
    now+=1000/120; const q=getRaf(); setRaf([]);
    for(const cb of q){try{cb(now)}catch(e){errors.push(e.stack||String(e));}}
    if(errors.length) break;
  }
  if(errors.length) throw new Error('controlled boss runtime error: '+errors.join('\n'));
  console.log('CONTROL_BOSS_PERSIST_AND_RUNTIME_OK');
}

console.log('V324_CONTROL_BOSS_OK');
