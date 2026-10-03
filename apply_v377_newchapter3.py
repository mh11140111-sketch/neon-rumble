from pathlib import Path
import re
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1 got {n}')
    s=s.replace(old,new,1)

# v3.77
once('BATTLE <b>v3.76</b>','BATTLE <b>v3.77</b>','version')
once('<summary>📒 패치노트 · v3.76</summary><div class="patch-body">',
     '<summary>📒 패치노트 · v3.77</summary><div class="patch-body"><div class="patch-version"><h3>v3.77 · NEW-CHAPTER 3 · 밸런스/버그 수정</h3><ul><li>👨‍💻 기술전문가 랜치 3개 → 5개.</li><li>💀💀💀 해골들 선택 시 일반/조정 전투 연결 오류 수정.</li><li>🏚️ NEW-CHAPTER 3 「몰락한 피의 저택」 추가 · 주인공 👻 유령 + AI 동료 🧛‍♀️ 여자 뱀파이어.</li><li>🎃 STAGE 3 신규 보스 호박왕 추가.</li></ul></div>',
     'patch notes')

# Technician 5 wrench balance
repls=[
("tag:'🔧 랜치 3개 · 벽 고정 · 회수 AI'","tag:'🔧 랜치 5개 · 벽 고정 · 회수 AI'"),
("랜치 3개를 던지며","랜치 5개를 던지며"),
("3개를 전부 회수하면","5개를 전부 회수하면"),
("HP 1000 · 🔧 3개 ·","HP 1000 · 🔧 5개 ·"),
("랜치 0개 시 회수 AI · 3개 회수 시","랜치 0개 시 회수 AI · 5개 회수 시"),
("if(!Number.isFinite(f.techWrenchStock))f.techWrenchStock=3;","if(!Number.isFinite(f.techWrenchStock))f.techWrenchStock=5;"),
("f.techWrenchStock+'/3'","f.techWrenchStock+'/5'"),
("if(f.techWrenchStock>=3&&f.techWrenches.length===0){f.techWrenchStock=3;","if(f.techWrenchStock>=5&&f.techWrenches.length===0){f.techWrenchStock=5;"),
("(f.techWrenchStock??3)+'/3","(f.techWrenchStock??5)+'/5"),
("t.techWrenchStock=3;t.techWrenchNext=0;","t.techWrenchStock=5;t.techWrenchNext=0;"),
("🔧 랜치 3개 · 비행 중 70","🔧 랜치 5개 · 비행 중 70"),
("🔧 랜치 3개 · 날아가는 랜치 70","🔧 랜치 5개 · 날아가는 랜치 70"),
("3개 소진 후 회수 AI","5개 소진 후 회수 AI")
]
for a,b in repls:
    if a not in s: raise SystemExit('technician anchor missing: '+a)
    s=s.replace(a,b)

# Skeleton bundle routing bug: count only primary fighters in 1v1/control verification.
old_verify="battleEngine.fighters.filter(f=>!f.summon).length===2"
new_verify="battleEngine.fighters.filter(f=>!f.summon&&!f.skeletonBundleMate).length===2"
if s.count(old_verify)!=2: raise SystemExit(f'skeleton bundle routing anchors: expected 2 got {s.count(old_verify)}')
s=s.replace(old_verify,new_verify)

# New storage keys/state based on current NC2 anchors.
once("NEW_CH2_STAGE_KEY='neonRumble.newChapter2Stages.v1',",
     "NEW_CH2_STAGE_KEY='neonRumble.newChapter2Stages.v1',NEW_CH3_STAGE_KEY='neonRumble.newChapter3Stages.v1',",
     'newch3 key')
once("newChapter2StageMask=0,",
     "newChapter2StageMask=0,newChapter3StageMask=0,",
     'newch3 state')
once("newChapter2StageMask=Number(localStorage.getItem(NEW_CH2_STAGE_KEY)||0)||0;",
     "newChapter2StageMask=Number(localStorage.getItem(NEW_CH2_STAGE_KEY)||0)||0;newChapter3StageMask=Number(localStorage.getItem(NEW_CH3_STAGE_KEY)||0)||0;",
     'newch3 load')
once("function newChapter2Unlocked(){return (newChapter1StageMask&7)===7}",
     "function newChapter2Unlocked(){return (newChapter1StageMask&7)===7}\nfunction newChapter3Unlocked(){return (newChapter2StageMask&7)===7}",
     'newch3 unlock')

# Add Pumpkin King roster after Skele-44.
skele_anchor="{id:'skele44',name:'스켈-44',icon:'🧫☠️',tag:'감염 투사체 · 해골 변환',hp:1000,damage:50,speed:140,cooldown:1,unlock:'skele44',description:'1초마다 피해 50의 감염 투사체를 던진다. 적중 시 30% 확률로 총잡이·칼잡이·취한 해골 중 하나를 소환하고, 직접 처치한 적도 죽기 직전 체력의 2배 HP를 가진 세 종류 해골 중 하나로 바꾼다.',detail:'HP 1000 · 🧫 투사체 50 / 1초 · 명중 시 30%로 🔫/🗡️/🍺 해골 소환 · 처치 시 죽기 직전 HP×2로 🔫/🗡️/🍺 해골 변환 · 법사해골 소환 없음 · NEW-CH2 STAGE 3 10% 획득'},"
pumpkin=skele_anchor+"\n{id:'pumpkin_king',name:'호박왕',icon:'🎃',tag:'불타는 영역 · 감속 · 사망 폭발',hp:1800,damage:10,speed:90,cooldown:.5,stageOnly:true,description:'느리게 움직이지만 상대를 불타는 영역 안에 넣도록 추적한다. 주변 불타는 영역은 항상 유지되며 안에 있는 적에게 0.5초마다 피해 10, 감속, 화상을 건다. 사망하면 넓은 범위로 피해 200 폭발을 일으킨다.',detail:'HP 1800 · 이동속도 90 · 🔥 상시 반경 105 · 범위 내 0.5초마다 10 + 감속 35% + 화상 · 사망 폭발 200 · 폭발 반경 260'},"
once(skele_anchor,pumpkin,'pumpkin roster')

# Pumpkin mechanics inside Engine before technicianSkill.
anchor="technicianSkill(f,e){"
pumpkin_methods=r"""pumpkinKingAura(f){
 if(!f||f.id!=='pumpkin_king'||f.health<=0)return;
 if(!Number.isFinite(f.pumpkinAuraNext))f.pumpkinAuraNext=this.time;
 const radius=105*f.scale;
 for(const e of this.enemies(f)){
  if(e.health<=0||distance(f,e)>radius+e.radius)continue;
  e.slow=Math.max(e.slow||0,.12);e.slowPower=Math.max(e.slowPower||0,.35);
  if(this.time>=f.pumpkinAuraNext-1e-9){
   const dealt=this.attack(f,e,10*f.scale);
   if(dealt>0&&e.health>0)this.applyBurn(f,e);
  }
 }
 if(this.time>=f.pumpkinAuraNext-1e-9)f.pumpkinAuraNext=this.time+.5/f.scale
}
pumpkinKingExplosion(f){
 if(!f||f.id!=='pumpkin_king'||f.pumpkinExploded)return;f.pumpkinExploded=true;
 const radius=260*f.scale;
 for(const e of this.fighters){
  if(e.team===f.team||e.health<=0||distance(f,e)>radius+e.radius)continue;
  const n=Math.min(e.health,Math.round(200*f.scale*(1-(e.armor||0))));e.health-=n;e.flash=.2;this.effect(e,'🎃💥 −'+n,'doom');if(this.formEgg(e))continue;if(e.health<=0)e.trail=[]
 }
 this.effects.push({x:f.x,y:f.y,text:'🎃💥 200!',kind:'blast',side:f.side,team:f.team,life:1});this.emit('🎃 호박왕 사망 폭발! 넓은 범위 피해 200')
}
"""
once(anchor,pumpkin_methods+anchor,'pumpkin methods')

# Call aura and make movement deliberately chase enemies into aura.
once("if(f.id==='skeleton_king')this.skeletonKingSkill(f,e);",
     "if(f.id==='skeleton_king')this.skeletonKingSkill(f,e);if(f.id==='pumpkin_king')this.pumpkinKingAura(f);",
     'pumpkin skill call')
once("}else if(f.id==='snail'&&!heroAuto&&f.dash<=0){",
     "}else if(f.id==='pumpkin_king'&&!heroAuto&&f.dash<=0){const a=this.aim(f,e);f.vx=a.x;f.vy=a.y;f.turn=.15}else if(f.id==='snail'&&!heroAuto&&f.dash<=0){",
     'pumpkin chase AI')
once("'skele44','skeleton_king','hell_clone'",
     "'skele44','skeleton_king','pumpkin_king','hell_clone'",
     'pumpkin contact exclusion')

# Trigger death explosion before normal checkEnd.
once("if(e.health===0){if(f.id==='skele44')this.spawnSkele44Skeleton(f,e.x,e.y,preDeathHp*2);this.furballDeathHeal(e,preDeathHp);",
     "if(e.health===0){if(e.id==='pumpkin_king')this.pumpkinKingExplosion(e);if(f.id==='skele44')this.spawnSkele44Skeleton(f,e.x,e.y,preDeathHp*2);this.furballDeathHeal(e,preDeathHp);",
     'pumpkin death explosion')

# Manual-control and mansion-style background for NC3.
once("'lab','hell','newchapter','newchapter2'].includes(mode)",
     "'lab','hell','newchapter','newchapter2','newchapter3'].includes(mode)",
     'manual newch3')
once("mode==='newchapter2'?'카우보이 이동 · '+controlName():",
     "mode==='newchapter2'?'카우보이 이동 · '+controlName():mode==='newchapter3'?'유령 이동 · '+controlName():",
     'control label newch3')
# Reuse mansion background draw.
if "mode==='mansion'" not in s: raise SystemExit('mansion background mode missing')
s=s.replace("mode==='mansion'", "mode==='mansion'||mode==='newchapter3'", 1)

# New Chapter 3 implementation before devil talk lines.
newch3=r"""
let newChapter3StageNo=1,newChapter3Wave=0;
function markNewChapter3Stage(n){newChapter3StageMask|=(1<<(n-1));try{localStorage.setItem(NEW_CH3_STAGE_KEY,String(newChapter3StageMask))}catch{}updateNewChapter3UI();return (newChapter3StageMask&7)===7}
function updateNewChapter3UI(){const b=$('newchapter3-entry');if(!b)return;const ok=newChapter3Unlocked(),d1=!!(newChapter3StageMask&1),d2=!!(newChapter3StageMask&2),d3=!!(newChapter3StageMask&4),count=(d1?1:0)+(d2?1:0)+(d3?1:0);b.disabled=!ok;b.textContent=ok?'🏚️ NEW-CHAPTER 3 · 몰락한 피의 저택'+(count?' · '+count+'/3':''):'🔒 NEW-CHAPTER 3 · NEW-CHAPTER 2 STAGE 1·2·3 클리어 필요';const prog=$('newchapter3-progress');if(prog)prog.textContent='진행도 '+count+' / 3'+(d3?' · ✅ COMPLETE':'');const data=[['newchapter3-1','newchapter3-status-1',d1,true],['newchapter3-2','newchapter3-status-2',d2,d1],['newchapter3-3','newchapter3-status-3',d3,d1&&d2]];for(const [id,sid,done,open] of data){const x=$(id),st=$(sid);if(!x)continue;x.disabled=!ok||!open;if(st)st.textContent=done?'✅ 클리어':open?'도전 가능':'🔒 이전 STAGE 클리어 필요'}}
function setupNewChapter3UI(){if($('newchapter3-entry')){updateNewChapter3UI();return}const after=$('newchapter2-entry'),sel=$('selection');if(!after||!sel)return;const b=document.createElement('button');b.id='newchapter3-entry';b.type='button';b.className=after.className;after.insertAdjacentElement('afterend',b);const p=document.createElement('section');p.id='newchapter3-selection';p.className='chapter-stage-panel';p.hidden=true;p.innerHTML='<div class="section-title"><div><p class="eyebrow">NEW-CHAPTER 3</p><h2>🏚️ 몰락한 피의 저택</h2></div><span id="newchapter3-progress" class="card-tag">진행도 0 / 3</span></div><p class="match-info">주인공 👻 유령을 직접 조작해. 모든 스테이지에서 🧛‍♀️ 여자 뱀파이어가 AI 동료로 함께 싸우며 직접 조작할 수 없어.</p><div class="roster newchapter3-grid"><button id="newchapter3-1" class="fighter-card" type="button"><span class="card-top"><span class="card-icon">🧟‍♂️</span><span><strong class="card-name">STAGE 1 · 다시 깨어난 좀비들</strong><small id="newchapter3-status-1" class="card-tag">도전 가능</small></span></span><span class="card-desc">CHAPTER 3처럼 좀비 5마리씩 5웨이브 · 👻 유령 + 🧛‍♀️ 여자 뱀파이어</span></button><button id="newchapter3-2" class="fighter-card" type="button"><span class="card-top"><span class="card-icon">🧌</span><span><strong class="card-name">STAGE 2 · 법사좀비</strong><small id="newchapter3-status-2" class="card-tag">🔒 이전 STAGE 클리어 필요</small></span></span><span class="card-desc">CHAPTER 3 STAGE 3과 같은 법사좀비 상태 · 기존 유령 조력자는 없음 · 주인공 유령 + 여자 뱀파이어</span></button><button id="newchapter3-3" class="fighter-card" type="button"><span class="card-top"><span class="card-icon">🎃</span><span><strong class="card-name">STAGE 3 · 호박왕</strong><small id="newchapter3-status-3" class="card-tag">🔒 이전 STAGE 클리어 필요</small></span></span><span class="card-desc">HP 1800 · 🔥 상시 불타는 영역 · 0.5초마다 10 + 감속 + 화상 · 느린 추적 AI · 사망 시 넓은 범위 폭발 200</span></button></div><div class="controls"><button id="newchapter3-back" type="button">← 챕터 목록으로</button></div>';sel.appendChild(p);const style=document.createElement('style');style.id='newchapter3-ui';style.textContent='#newchapter3-selection{margin:18px 0 24px;padding:18px;background:linear-gradient(180deg,#261018,#10090d);border:1px solid #6f3346;border-radius:14px}#newchapter3-selection .newchapter3-grid{margin-top:14px}#newchapter3-selection .fighter-card{width:100%;min-height:150px}#newchapter3-selection .fighter-card:disabled{opacity:.48;filter:saturate(.45)}@media(max-width:560px){#newchapter3-selection{padding:14px 10px}#newchapter3-selection .newchapter3-grid{grid-template-columns:1fr}#newchapter3-selection .fighter-card{min-height:0}}';document.head.appendChild(style);b.onclick=()=>{if(!newChapter3Unlocked())return;hideStageSelectionPanels();p.hidden=false;p.scrollIntoView({behavior:'smooth',block:'start'})};$('newchapter3-back').onclick=()=>{p.hidden=true;mode='duel';updateSelection();window.scrollTo({top:0,behavior:'smooth'})};$('newchapter3-1').onclick=()=>startNewChapter3Stage(1);$('newchapter3-2').onclick=()=>{if(newChapter3StageMask&1)startNewChapter3Stage(2)};$('newchapter3-3').onclick=()=>{if((newChapter3StageMask&3)===3)startNewChapter3Stage(3)};updateNewChapter3UI()}
function spawnNewChapter3FemaleVampire(){const base=new Engine('vampire','zombie',Math.random,{mode:'control'}).fighters[0];base.side=engine.fighters.length;base.team=0;base.summon=true;base.ownerSide=0;base.femaleVampire=true;base.icon='🧛‍♀️';base.name='여자 뱀파이어';base.hp=1000;base.health=1000;base.x=190;base.y=520;base.vx=0;base.vy=-1;base.trail=[];base.deathOrder=null;engine.fighters.push(base);return base}
function spawnNewChapter3ZombieWave(){newChapter3Wave++;const spots=[[500,120],[610,235],[625,410],[535,570],[440,360]];for(const [x,y] of spots){const z=new Engine('ghost','zombie',Math.random,{mode:'control'}).fighters[1];z.side=engine.fighters.length;z.team=1;z.summon=true;z.ownerSide=1;z.x=x;z.y=y;z.trail=[];z.deathOrder=null;engine.fighters.push(z)}$('event').textContent='🏚️ WAVE '+newChapter3Wave+' / 5 · 좀비 5마리 출현!'}
function startNewChapter3Stage(n){newChapter3StageNo=n;newChapter3Wave=0;mode='newchapter3';if(n===1){engine=new Engine('ghost','zombie',Math.random,{mode:'control'});engine.fighters[1].health=0;engine.desertWaveMode=true;spawnNewChapter3FemaleVampire();spawnNewChapter3ZombieWave()}else if(n===2){engine=new Engine('ghost','zombie_mage',Math.random,{mode:'control'});const m=engine.fighters[1];m.hp=2000;m.health=2000;m.bodyScale=1.5;m.radius=49.5;m.speed=105;m.zombieMageDamage=85;engine.desertWaveMode=false;spawnNewChapter3FemaleVampire()}else{engine=new Engine('ghost','pumpkin_king',Math.random,{mode:'control'});const b=engine.fighters[1];b.hp=1800;b.health=1800;b.speed=90;b.pumpkinAuraNext=0;b.pumpkinExploded=false;engine.desertWaveMode=false;spawnNewChapter3FemaleVampire()}engine.newChapter3Mode=true;engine.mansionMode=true;paused=false;acc=0;last=performance.now();lastHits=0;lastMessage='';hideStageSelectionPanels();if($('newchapter3-selection'))$('newchapter3-selection').hidden=true;$('selection').hidden=true;$('battle').hidden=false;$('result').hidden=true;$('pause-label').hidden=true;$('pause').disabled=false;$('pause').textContent='일시정지';resetStick();refreshControlUI();$('squad-hud').hidden=true;$('relay-hud').hidden=true;$('score-label0').textContent='👻 유령 + 🧛‍♀️ 여자 뱀파이어';$('score-label1').textContent=n===1?'🧟‍♂️ 좀비 웨이브':n===2?'🧌 법사좀비':'🎃 호박왕';$('battle-mode').textContent='NEW-CH3 '+n;$('battle-info').textContent=n===1?'NEW-CHAPTER 3 STAGE 1 · 좀비 5마리씩 총 5웨이브 · 주인공 유령 직접 조작 · 여자 뱀파이어 AI 동료.':n===2?'NEW-CHAPTER 3 STAGE 2 · CHAPTER 3 STAGE 3과 같은 법사좀비 HP 2000 · 유도탄 85/2초 · 명중 시 미니좀비 · 기존 유령 조력자는 없음 · 여자 뱀파이어 AI 동료.':'NEW-CHAPTER 3 STAGE 3 · 호박왕 HP 1800 · 반경 105 불타는 영역 상시 유지 · 범위 내 0.5초마다 10 + 감속 35% + 화상 · 상대를 영역에 넣는 추적 AI · 사망 시 반경 260 폭발 피해 200.';fit();hud();draw();window.scrollTo({top:0,behavior:'auto'});playSfx('start')}
function updateNewChapter3Stage(){if(mode!=='newchapter3'||!engine||engine.result!==null)return;const hero=engine.fighters.find(f=>f.id==='ghost'&&f.team===0&&!f.summon);if(!hero||hero.health<=0){engine.result=1;return}if(newChapter3StageNo===1){const alive=engine.fighters.some(f=>f.team===1&&f.health>0);if(!alive){if(newChapter3Wave>=5){engine.result=0;engine.desertWaveMode=false}else spawnNewChapter3ZombieWave()}}else{const boss=engine.fighters.find(f=>f.team===1&&!f.summon);if(!boss||boss.health<=0)engine.result=0}}
"""
once("const DEVIL_TALK_LINES=[",newch3+"\nconst DEVIL_TALK_LINES=[",'insert newch3')

# Update NC2 completion to unlock NC3 UI.
once("function markNewChapter2Stage(n){newChapter2StageMask|=(1<<(n-1));try{localStorage.setItem(NEW_CH2_STAGE_KEY,String(newChapter2StageMask))}catch{}updateNewChapter2UI();return (newChapter2StageMask&7)===7}",
     "function markNewChapter2Stage(n){newChapter2StageMask|=(1<<(n-1));try{localStorage.setItem(NEW_CH2_STAGE_KEY,String(newChapter2StageMask))}catch{}updateNewChapter2UI();updateNewChapter3UI();return (newChapter2StageMask&7)===7}",
     'nc2 updates nc3')

# HUD stage updater and results.
once("updateNewChapter2Stage();hud()}",
     "updateNewChapter2Stage();updateNewChapter3Stage();hud()}",
     'loop newch3')

res_anchor="else if(mode==='newchapter2'){$('winner-icon').textContent='🤠';$('winner').textContent='NEW-CHAPTER 2 · STAGE '+newChapter2StageNo+' 실패';$('summary').textContent=t+'초 · 카우보이가 쓰러졌어. 다시 해골 강림에 도전해 봐.'}else{"
res_new="else if(mode==='newchapter2'){$('winner-icon').textContent='🤠';$('winner').textContent='NEW-CHAPTER 2 · STAGE '+newChapter2StageNo+' 실패';$('summary').textContent=t+'초 · 카우보이가 쓰러졌어. 다시 해골 강림에 도전해 봐.'}else if(mode==='newchapter3'&&engine.result===0){const coinReward=awardStageCoins(newChapter3StageNo);markNewChapter3Stage(newChapter3StageNo);$('winner-icon').textContent='🏚️';$('winner').textContent='NEW-CHAPTER 3 · STAGE '+newChapter3StageNo+' 클리어!';$('summary').textContent=t+'초 · 몰락한 피의 저택 돌파 · 🪙 '+coinReward+'코인 획득!'}else if(mode==='newchapter3'){$('winner-icon').textContent='👻';$('winner').textContent='NEW-CHAPTER 3 · STAGE '+newChapter3StageNo+' 실패';$('summary').textContent=t+'초 · 유령이 쓰러졌어. 피의 저택에 다시 도전해 봐.'}else{"
once(res_anchor,res_new,'result newch3')

# Rematch branch.
once("mode==='newchapter2'?startNewChapter2Stage(newChapter2StageNo):start();",
     "mode==='newchapter2'?startNewChapter2Stage(newChapter2StageNo):mode==='newchapter3'?startNewChapter3Stage(newChapter3StageNo):start();",
     'rematch newch3')

# Devil talk button should be after newest chapter.
once("const after=$('newchapter2-entry')||$('newchapter1-entry')||$('chapter10-entry');",
     "const after=$('newchapter3-entry')||$('newchapter2-entry')||$('newchapter1-entry')||$('chapter10-entry');",
     'devil position newch3')

# Setup
once("setupChapter9UI();setupChapter10UI();setupNewChapter1UI();setupNewChapter2UI();setupDevilTalkUI();updateLegacyStageCompletionUI();",
     "setupChapter9UI();setupChapter10UI();setupNewChapter1UI();setupNewChapter2UI();setupNewChapter3UI();setupDevilTalkUI();updateLegacyStageCompletionUI();",
     'setup newch3')

p.write_text(s,encoding='utf-8')
print('v3.77 patch applied')
