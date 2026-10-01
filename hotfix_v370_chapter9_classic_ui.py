from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')

old_re=r"function updateChapter9UI\(\)\{.*?\}\nfunction setupChapter9UI\(\)\{.*?\}\nfunction spawnLabScientist"
m=re.search(old_re,s,re.S)
if not m:
    raise SystemExit('chapter9 UI block not found')
new=r'''function updateChapter9UI(){
 const b=$('chapter9-entry');if(!b)return;
 const ok=chapter9Unlocked(),d1=!!(labStageMask&1),d2=!!(labStageMask&2),d3=!!(labStageMask&4),count=(d1?1:0)+(d2?1:0)+(d3?1:0);
 b.disabled=!ok;b.textContent=ok?'🧪 CHAPTER 9 · 실험실 탈출'+(count?' · '+count+'/3':''):'🔒 CHAPTER 9 · CHAPTER 8 STAGE 1·2·3 클리어 필요';
 const prog=$('lab-progress');if(prog)prog.textContent='진행도 '+count+' / 3'+(d3?' · ✅ CHAPTER 9 COMPLETE':'');
 const data=[['lab-1','lab-status-1',d1,true,'STAGE 1 · 🧑‍🔬 과학자 5웨이브'],['lab-2','lab-status-2',d2,d1,'STAGE 2 · 🧑‍🔬 과학자 5웨이브'],['lab-3','lab-status-3',d3,d1&&d2,'STAGE 3 · 👨‍⚕️ 의사']];
 for(const [id,sid,done,open,label] of data){const x=$(id),st=$(sid);if(!x)continue;x.disabled=!ok||!open;x.setAttribute('aria-disabled',String(x.disabled));if(st)st.textContent=done?'✅ 클리어':open?'도전 가능':'🔒 이전 STAGE 클리어 필요';const name=x.querySelector('.card-name');if(name)name.textContent=label}
}
function setupChapter9UI(){
 if($('chapter9-entry')){updateChapter9UI();return}
 const after=$('chapter8-entry'),sel=$('selection');if(!after||!sel)return;
 const b=document.createElement('button');b.id='chapter9-entry';b.type='button';b.className=after.className;after.insertAdjacentElement('afterend',b);
 const p=document.createElement('section');p.id='lab-selection';p.className='chapter-stage-panel';p.hidden=true;
 p.innerHTML='<div class="section-title"><div><p class="eyebrow">CHAPTER 9</p><h2>🧪 실험실 탈출</h2></div><span id="lab-progress" class="card-tag">진행도 0 / 3</span></div><p class="match-info">주인공 🫈 털복숭이로 실험실을 탈출해. STAGE를 순서대로 클리어하면 다음 STAGE가 열려.</p><div class="roster lab-stage-grid"><button id="lab-1" class="fighter-card" type="button"><span class="card-top"><span class="card-icon">🧑‍🔬</span><span><strong class="card-name">STAGE 1 · 🧑‍🔬 과학자 5웨이브</strong><small id="lab-status-1" class="card-tag">도전 가능</small></span></span><span class="card-desc">과학자 3명씩 5웨이브 · 독 투사체 30 · 웨이브 클리어 시 HP 30% 회복</span></button><button id="lab-2" class="fighter-card" type="button"><span class="card-top"><span class="card-icon">🧪</span><span><strong class="card-name">STAGE 2 · 🧑‍🔬 과학자 5웨이브</strong><small id="lab-status-2" class="card-tag">🔒 이전 STAGE 클리어 필요</small></span></span><span class="card-desc">과학자 3명씩 5웨이브 · 독 투사체 30 · 웨이브 클리어 시 HP 30% 회복</span></button><button id="lab-3" class="fighter-card" type="button"><span class="card-top"><span class="card-icon">👨‍⚕️</span><span><strong class="card-name">STAGE 3 · 👨‍⚕️ 의사</strong><small id="lab-status-3" class="card-tag">🔒 이전 STAGE 클리어 필요</small></span></span><span class="card-desc">💉 적 80+독 · 아군 +50+약물치료 · 클리어 시 의사 10% 획득</span></button></div><div class="controls"><button id="lab-back" type="button">← 챕터 목록으로</button></div>';
 sel.appendChild(p);
 const style=document.createElement('style');style.id='chapter9-classic-ui';style.textContent='#lab-selection{margin:18px 0 24px;padding:18px;background:#101b2b;border:1px solid #35465f;border-radius:14px}#lab-selection .section-title h2{margin:4px 0 0}#lab-selection .lab-stage-grid{margin-top:14px}#lab-selection .fighter-card{width:100%;min-height:150px}#lab-selection .fighter-card:disabled{opacity:.48;filter:saturate(.45)}#lab-selection .card-top>span:last-child{display:flex;flex-direction:column;gap:4px;min-width:0}#lab-progress{white-space:nowrap}@media(max-width:560px){#lab-selection{padding:14px 10px}#lab-selection .lab-stage-grid{grid-template-columns:1fr}#lab-selection .fighter-card{min-height:0}}';document.head.appendChild(style);
 b.onclick=()=>{if(!chapter9Unlocked())return;mode='lab-select';hideStageSelectionPanels();p.hidden=false;updateChapter9UI();p.scrollIntoView({behavior:'smooth',block:'start'})};
 $('lab-back').onclick=()=>{p.hidden=true;mode='duel';window.scrollTo({top:0,behavior:'smooth'})};
 $('lab-1').onclick=()=>startLabStage(1);$('lab-2').onclick=()=>{if(labStageMask&1)startLabStage(2)};$('lab-3').onclick=()=>{if((labStageMask&3)===3)startLabStage(3)};
 updateChapter9UI()
}
function spawnLabScientist'''
s=s[:m.start()]+new+s[m.end():]

old="function markLabStage(n){labStageMask|=(1<<(n-1));try{localStorage.setItem(LAB_STAGE_KEY,String(labStageMask))}catch{}return (labStageMask&7)===7}"
new2="function markLabStage(n){labStageMask|=(1<<(n-1));try{localStorage.setItem(LAB_STAGE_KEY,String(labStageMask))}catch{}updateChapter9UI();return (labStageMask&7)===7}"
if old not in s: raise SystemExit('markLabStage anchor not found')
s=s.replace(old,new2,1)

# Keep v3.70; this is a UI/convenience hotfix only.
p.write_text(s,encoding='utf-8')
print('v3.70 chapter9 classic UI hotfix applied')