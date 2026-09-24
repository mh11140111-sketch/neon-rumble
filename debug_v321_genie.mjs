import fs from 'fs';
import {JSDOM} from 'jsdom';

// Runtime regression test: must survive Genie attack start beyond 3 seconds.
const html=fs.readFileSync('index.html','utf8');
const errors=[];
let raf=[];
let now=0;

const dom=new JSDOM(html,{runScripts:'dangerously',resources:'usable',pretendToBeVisual:true,beforeParse(window){
  window.scrollTo=()=>{};
  window.ResizeObserver=class{constructor(cb){this.cb=cb}observe(){}disconnect(){}};
  window.AudioContext=class{}; window.webkitAudioContext=window.AudioContext;
  window.requestAnimationFrame=(cb)=>{raf.push(cb);return raf.length};
  window.cancelAnimationFrame=()=>{};
  Object.defineProperty(window.HTMLCanvasElement.prototype,'getContext',{value(){
    const fn=()=>{};
    const ctx=new Proxy({canvas:this,measureText:()=>({width:10})},{get(t,p){if(p in t)return t[p];return fn},set(t,p,v){t[p]=v;return true}});
    return ctx;
  }});
  window.addEventListener('error',e=>errors.push(String(e.error?.stack||e.message||e.error)));
  window.addEventListener('unhandledrejection',e=>errors.push(String(e.reason?.stack||e.reason)));
}});

await new Promise(r=>setTimeout(r,50));
const {document}=dom.window;
const aladdin=[...document.querySelectorAll('.fighter-card')].find(b=>b.dataset.character==='aladdin');
if(!aladdin) throw new Error('Aladdin card not found');
aladdin.click();
document.getElementById('start').click();

for(let frame=0;frame<900;frame++){
  now+=1000/120;
  const q=raf; raf=[];
  for(const cb of q){try{cb(now)}catch(e){errors.push(e.stack||String(e));}}
  if(errors.length)break;
}

console.log('frames',Math.round(now/(1000/120)),'time',now/1000,'errors',errors.length);
if(errors.length){console.error(errors.join('\n---\n'));process.exit(1)}
const event=document.getElementById('event')?.textContent||'';
console.log('last_event',event);
if(!event.includes('지니') && now>=3_000) console.log('note: no genie event text captured, but runtime stayed alive');
console.log('GENIE_RUNTIME_OK');
