import fs from 'fs';
import {JSDOM} from 'jsdom';

const html=fs.readFileSync('index.html','utf8');

async function bootAndRun(stageId){
  const errors=[]; let raf=[]; let now=0;
  const dom=new JSDOM(html,{runScripts:'dangerously',resources:'usable',pretendToBeVisual:true,beforeParse(window){
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
  const d=dom.window.document;
  const entry=d.getElementById('stage-entry'); if(!entry) throw new Error('stage-entry missing');
  entry.click();
  if(d.getElementById('stage-panel').hidden) throw new Error('stage panel did not open');
  const b=d.getElementById('stage-'+stageId); if(!b) throw new Error('stage button missing '+stageId);
  b.click();
  if(d.getElementById('battle').hidden) throw new Error('battle did not start for stage '+stageId);
  if(d.getElementById('control-stick').hidden) throw new Error('control stick hidden for stage '+stageId);
  for(let frame=0;frame<480;frame++){
    now+=1000/120; const q=raf; raf=[];
    for(const cb of q){try{cb(now)}catch(e){errors.push(e.stack||String(e));}}
    if(errors.length) break;
  }
  if(errors.length) throw new Error('stage '+stageId+' runtime error: '+errors.join('\n'));
  console.log('STAGE_'+stageId+'_OK', 'time', (now/1000).toFixed(2));
}

for(const n of [1,2,3]) await bootAndRun(n);
console.log('V324_STAGE_RUNTIME_OK');
