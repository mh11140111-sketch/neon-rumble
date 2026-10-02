from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1, got {n}')
    s=s.replace(old,new,1)

# Patch notes, same v3.75
once(
'<summary>📒 패치노트 · v3.75</summary><div class="patch-body">',
'<summary>📒 패치노트 · v3.75</summary><div class="patch-body"><div class="patch-version"><h3>v3.75 · NEW-CHAPTER 1 · 편의성 개선</h3><ul><li>🎰 도박장 스테이지 스킵권의 독립 당첨 구간을 제거하고 꾸미기 당첨 시 함께 지급되도록 변경.</li><li>✅ CHAPTER 1~8의 각 STAGE에 클리어 표시 추가.</li><li>⚙️ 게임 시작 버튼 위치에 위·아래 동시 표시 옵션 추가. 기존 위/아래 옵션 유지.</li><li>🆕 CHAPTER 10 전체 클리어 후 NEW-CHAPTER 1 「빌런의 재등장」 해금.</li><li>🌳 STAGE 1 조종당한 나무, 🦹‍♂️ STAGE 2 강화 빌런, 👨‍💻 STAGE 3 기술전문가 추가.</li></ul></div>',
'patch note')

# Settings both option
once(
'<label class="setting-item">게임 시작 버튼 위치<select id="setting-start-position"><option value="top">위</option><option value="bottom">아래 · CHAPTER 1 위</option></select></label>',
'<label class="setting-item">게임 시작 버튼 위치<select id="setting-start-position"><option value="top">위</option><option value="bottom">아래 · CHAPTER 1 위</option><option value="both">위 · 아래 동시에</option></select></label>',
'setting both option')
once("if(!['top','bottom'].includes(settings.startPosition))settings.startPosition='top';",
     "if(!['top','bottom','both'].includes(settings.startPosition))settings.startPosition='top';",
     'settings validation')
once(
"function applyStartButtonPosition(){const b=$('start'),top=$('start-top-anchor'),stage=$('stage-entry');if(!b||!top||!stage)return;if(settings.startPosition==='bottom')stage.before(b);else top.after(b)}",
"""function applyStartButtonPosition(){const b=$('start'),top=$('start-top-anchor'),stage=$('stage-entry');if(!b||!top||!stage)return;let second=$('start-secondary');if(settings.startPosition==='both'){top.after(b);if(!second){second=document.createElement('button');second.id='start-secondary';second.type='button';second.className=b.className;second.onclick=()=>b.click();new MutationObserver(()=>syncSecondaryStartButton()).observe(b,{attributes:true,childList:true,subtree:true,characterData:true});}stage.before(second);syncSecondaryStartButton()}else{if(second)second.remove();if(settings.startPosition==='bottom')stage.before(b);else top.after(b)}}
function syncSecondaryStartButton(){const b=$('start'),s2=$('start-secondary');if(!b||!s2)return;s2.textContent=b.textContent;s2.disabled=b.disabled;s2.hidden=b.hidden}""",
'start both logic')
once("$('start').textContent=mode==='group'?'단체전 시작 · 3 vs 3 동시전투':mode==='relay'?'릴레이 전투 시작 · 팀당 3명':isBossMode()?'보스전 시작 · 1 vs 5':mode==='control'?'조정 모드 시작 · 왼쪽 직접 이동':'이 조합으로 전투 시작';updateStageUI();",
     "$('start').textContent=mode==='group'?'단체전 시작 · 3 vs 3 동시전투':mode==='relay'?'릴레이 전투 시작 · 팀당 3명':isBossMode()?'보스전 시작 · 1 vs 5':mode==='control'?'조정 모드 시작 · 왼쪽 직접 이동':'이 조합으로 전투 시작';syncSecondaryStartButton();updateStageUI();",
     'sync secondary')

# Casino: skip ticket only bundled with cosmetics, no independent chance
once(
"else if(r<.70){casinoShowReels('🎫');grantStageSkipTicket(1);text='🎫 스테이지 스킵권 획득! 현재 '+stageSkipTickets+'장 보유.'}else if(r<.85){casinoShowReels('🎟️');grantCoinBoostTicket(1);text='🎟️ 코인 2배 획득권 획득! 옷장에서 10분 동안 사용할 수 있어.'}else{casinoShowReels('❌');text='아쉽다! 이번에는 꽝이야.'}",
"else if(r<.55){casinoShowReels('🎟️');grantCoinBoostTicket(1);text='🎟️ 코인 2배 획득권 획득! 옷장에서 10분 동안 사용할 수 있어.'}else{casinoShowReels('❌');text='아쉽다! 이번에는 꽝이야.'}",
'remove independent skip')
once(
"if(dup){const won=grantCoins(150);text=item.icon+' '+item.name+' 중복! 대신 🪙 '+won+'코인 획득!'}else{ownedCosmetics.push(id);text=item.icon+' '+item.name+' 획득! 옷장에서 장착할 수 있어.'}",
"if(dup){const won=grantCoins(150);text=item.icon+' '+item.name+' 중복! 대신 🪙 '+won+'코인 획득!'}else{ownedCosmetics.push(id);text=item.icon+' '+item.name+' 획득! 옷장에서 장착할 수 있어.'}grantStageSkipTicket(1);text+=' · 🎫 스테이지 스킵권 1장도 함께 획득!'",
'cosmetic bundled skip')
s=s.replace("꾸미기 30%, 캐릭터 10%, 스테이지 스킵권 30%, 코인 2배 획득권 15%, 꽝 15%야.","꾸미기+스테이지 스킵권 30%, 캐릭터 10%, 코인 2배 획득권 15%, 꽝 45%야.")
s=s.replace("꾸미기 30% · 캐릭터 10% · 꽝 60%","꾸미기+스킵권 30% · 캐릭터 10% · 코인2배권 15% · 꽝 45%")

# Technician roster
once(
"{id:'hell_demon',name:'악마',icon:'👿',tag:'악의 돌진 · 악의 소환 · 무적 · 지옥의 불',hp:1366,damage:13,speed:175,cooldown:0,unlock:'hellDemon',description:'샌드박스 악마. 악의 돌진 13~166 / 5초, 악마의 눈 소환 / 13초, 13초마다 1.3초 무적과 HP 136 회복. 2.5초마다 피해 66의 보라색 지옥의 불을 던진다.',detail:'HP 1366 · 악의 돌진 13~166 / 5초 · 🧿 HP 66 소환 / 13초 · 무적 1.3초 + HP 136 / 13초 · 🟣🔥 지옥의 불 66 / 2.5초 · 지옥의 화상 13 / 0.66초 · 사망 시 해제 · 특별 코드로 샌드박스 해금'},",
"{id:'hell_demon',name:'악마',icon:'👿',tag:'악의 돌진 · 악의 소환 · 무적 · 지옥의 불',hp:1366,damage:13,speed:175,cooldown:0,unlock:'hellDemon',description:'샌드박스 악마. 악의 돌진 13~166 / 5초, 악마의 눈 소환 / 13초, 13초마다 1.3초 무적과 HP 136 회복. 2.5초마다 피해 66의 보라색 지옥의 불을 던진다.',detail:'HP 1366 · 악의 돌진 13~166 / 5초 · 🧿 HP 66 소환 / 13초 · 무적 1.3초 + HP 136 / 13초 · 🟣🔥 지옥의 불 66 / 2.5초 · 지옥의 화상 13 / 0.66초 · 사망 시 해제 · 특별 코드로 샌드박스 해금'},\n{id:'technician',name:'기술전문가',icon:'👨‍💻',tag:'🔧 랜치 3개 · 벽 고정 · 회수 AI',hp:1000,damage:70,speed:155,cooldown:1.3,unlock:'technician',description:'로봇을 만든 기술전문가. 랜치 3개를 던지며 날아가는 랜치는 피해 70. 벽에 닿으면 박히고, 박힌 랜치에 닿은 적은 피해 80. 3개를 모두 사용하면 랜치 수집 AI로 바뀌어 직접 회수하고, 전부 회수하면 다시 일반 전투로 돌아온다.',detail:'HP 1000 · 🔧 3개 · 투척 70 / 1.3초 · 벽 고정 랜치 접촉 80 · 랜치 0개 시 회수 AI · 3개 회수 시 일반 AI 복귀 · NEW-CH1 STAGE 3 15% 획득'},",
'technician roster')

# Technician engine behavior
anchor="furballDeathHeal(dead,preHp){"
tech_code="""technicianSkill(f,e){
 if(!f||f.id!=='technician'||f.health<=0)return;
 if(!Array.isArray(f.techWrenches))f.techWrenches=[];
 if(!Number.isFinite(f.techWrenchStock))f.techWrenchStock=3;
 if(!Number.isFinite(f.techWrenchNext))f.techWrenchNext=this.time;
 for(const w of f.techWrenches){
  w.hitTargets=w.hitTargets||{};
  for(const x of this.enemies(f)){if(x.health<=0||w.hitTargets[x.side]||Math.hypot(x.x-w.x,x.y-w.y)>x.radius+16*f.scale)continue;const dealt=this.attack(f,x,80*f.scale);if(dealt>0)w.hitTargets[x.side]=true;if(this.result!==null)return}
 }
 if(f.techCollecting){
  if(f.techWrenches.length){const w=f.techWrenches.reduce((a,b)=>!a||Math.hypot(f.x-b.x,f.y-b.y)<Math.hypot(f.x-a.x,f.y-a.y)?b:a,null);f.techCollectTarget=w;const d=Math.hypot(f.x-w.x,f.y-w.y);if(d<=f.radius+19*f.scale){f.techWrenches.splice(f.techWrenches.indexOf(w),1);f.techWrenchStock++;this.effect(f,'🔧 회수 '+f.techWrenchStock+'/3','heal');f.techCollectTarget=null}}
  if(f.techWrenchStock>=3&&f.techWrenches.length===0){f.techWrenchStock=3;f.techCollecting=false;f.techCollectTarget=null;f.techWrenchNext=this.time+.35;this.effect(f,'🔧 랜치 전부 회수!','skill')}
  return
 }
 if(f.techWrenchStock>0&&e&&e.health>0&&this.time>=f.techWrenchNext-1e-9){
  const a=this.aim(f,e);this.shots.push({x:f.x+a.x*(f.radius+9),y:f.y+a.y*(f.radius+9),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'tech_wrench',icon:'🔧',radius:10*f.scale,speed:390*f.scale,damage:70*f.scale,life:5,bounces:0,techHits:{}});f.techWrenchStock--;f.techWrenchNext=this.time+1.3/f.scale;f.attack=.18/f.scale;this.effect(f,'🔧 투척 · 남은 '+f.techWrenchStock,'skill');if(f.techWrenchStock===0)f.techCollectPending=true
 }
 if(f.techCollectPending&&!this.shots.some(s=>s.owner===f.side&&s.kind==='tech_wrench')){f.techCollectPending=false;f.techCollecting=true;this.effect(f,'🔧 랜치 수집 모드','skill')}
}
"""
once(anchor,tech_code+anchor,'technician engine')

once("if(f.id==='doctor')this.doctorSkill(f);if(f.id==='hell_clone'||f.id==='hell_demon')this.demonSkill(f,e,dt);",
     "if(f.id==='doctor')this.doctorSkill(f);if(f.id==='technician')this.technicianSkill(f,e);if(f.id==='hell_clone'||f.id==='hell_demon')this.demonSkill(f,e,dt);",
     'technician call')

# Technician collection movement override
once(
"if(manual&&!heroAuto){f.vx=Number(this.controlX)||0;f.vy=Number(this.controlY)||0;f.turn=1}else if(f.id==='snail'&&!heroAuto&&f.dash<=0){",
"if(manual&&!heroAuto){f.vx=Number(this.controlX)||0;f.vy=Number(this.controlY)||0;f.turn=1}else if(f.id==='technician'&&f.techCollecting&&f.techCollectTarget){const d=Math.hypot(f.techCollectTarget.x-f.x,f.techCollectTarget.y-f.y)||1;f.vx=(f.techCollectTarget.x-f.x)/d;f.vy=(f.techCollectTarget.y-f.y)/d;f.turn=.2}else if(f.id==='snail'&&!heroAuto&&f.dash<=0){",
'technician collect movement')

# Exclude technician from generic contact attack
once("'furball','scientist','doctor','hell_clone','hell_demon'].includes(f.id)",
     "'furball','scientist','doctor','technician','hell_clone','hell_demon'].includes(f.id)",
     'technician generic contact exclusion')

# Custom wrench projectile: flying hit then sticks to wall
once(
"if(s.kind==='wave'){for(const e of this.enemies(f)){",
"""if(s.kind==='tech_wrench'){
   s.techHits=s.techHits||{};
   for(const x of this.enemies(f)){if(x.health<=0||s.techHits[x.side]||distance(s,x)>=x.radius+s.radius)continue;const dealt=this.attack(f,x,70*f.scale);if(dealt>0)s.techHits[x.side]=true;if(this.result!==null)break}
   if(s.x<=22+s.radius||s.x>=698-s.radius||s.y<=22+s.radius||s.y>=698-s.radius){s.x=clamp(s.x,22+s.radius,698-s.radius);s.y=clamp(s.y,22+s.radius,698-s.radius);f.techWrenches=f.techWrenches||[];f.techWrenches.push({x:s.x,y:s.y,hitTargets:{}});s.life=0;this.effect(f,'🔧 벽에 박힘','skill')}continue
  }
  if(s.kind==='wave'){for(const e of this.enemies(f)){""",
'wrench projectile')

# Render flying + stuck wrench
once("else if(s.kind==='beer'){",
     "else if(s.kind==='tech_wrench'){ctx.rotate(-Math.atan2(s.vy,s.vx)+engine.time*12);ctx.font=(30*s.radius/10)+'px \"Apple Color Emoji\",\"Segoe UI Emoji\",sans-serif';ctx.fillText('🔧',0,0)}else if(s.kind==='beer'){",
     'wrench projectile render')
once("for(const f of engine.fighters){if(f.captureTarget===null||f.health<=0)continue;",
     "for(const f of engine.fighters){if(f.id!=='technician'||!Array.isArray(f.techWrenches))continue;for(const w of f.techWrenches){ctx.save();ctx.translate(w.x,w.y);ctx.rotate(-.65);ctx.font=(30*f.scale)+'px \"Apple Color Emoji\",\"Segoe UI Emoji\",sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('🔧',0,0);ctx.restore()}}\nfor(const f of engine.fighters){if(f.captureTarget===null||f.health<=0)continue;",
     'stuck wrench render')

# Tree aura item and custom renderer
once(
"{id:'aura_rainbow',name:'무지개 아우라',icon:'🌈',price:130,type:'aura',auraStyle:'rainbow',exclusiveFor:null,desc:'무지개빛 에너지가 계속 색을 바꾸며 회전하는 아우라'}",
"{id:'aura_rainbow',name:'무지개 아우라',icon:'🌈',price:130,type:'aura',auraStyle:'rainbow',exclusiveFor:null,desc:'무지개빛 에너지가 계속 색을 바꾸며 회전하는 아우라'},\n {id:'aura_tree',name:'나무 아우라',icon:'🌿',price:0,type:'aura',auraStyle:'tree',exclusiveFor:null,stageRewardOnly:true,desc:'NEW-CHAPTER 1 STAGE 1에서 획득 가능한 나뭇잎 아우라'}",
'tree aura item')
once("if(item.casinoOnly||item.codeOnly)continue;",
     "if(item.casinoOnly||item.codeOnly||item.stageRewardOnly)continue;",
     'tree aura shop hidden')
once(
"function drawEquippedAura(f,item){if(!item||!item.auraStyle||f.health<=0)return;const t=engine?engine.time:0,r=f.radius*(1.72+.08*Math.sin(t*5+f.side));ctx.save();ctx.translate(f.x,f.y);ctx.globalCompositeOperation='lighter';if(item.auraStyle==='space'){",
"""function drawEquippedAura(f,item){if(!item||!item.auraStyle||f.health<=0)return;const t=engine?engine.time:0,r=f.radius*(1.72+.08*Math.sin(t*5+f.side));ctx.save();ctx.translate(f.x,f.y);ctx.globalCompositeOperation='lighter';if(item.auraStyle==='tree'){ctx.shadowColor='#78d96a';ctx.shadowBlur=20;for(let i=0;i<10;i++){const a=t*.55+i*Math.PI*2/10,rr=r*(.72+.18*((i%3)/2));ctx.globalAlpha=.38+.18*Math.sin(t*3+i);ctx.font=(18+4*(i%2))*f.scale+'px \"Apple Color Emoji\",\"Segoe UI Emoji\",sans-serif';ctx.fillText(i%2?'🍃':'🌿',Math.cos(a)*rr,Math.sin(a)*rr)}ctx.globalAlpha=.45;ctx.strokeStyle='#7bd36b';ctx.lineWidth=5*f.scale;ctx.beginPath();ctx.arc(0,0,r*.92,0,Math.PI*2);ctx.stroke()}else if(item.auraStyle==='space'){""",
'tree aura renderer')
once(
"if(!f.summon){const aura=currentAura(f.team);if(aura&&(!aura.exclusiveFor||aura.exclusiveFor===f.id))drawEquippedAura(f,aura)}circle(f.x,f.y,r,f.flash>0?'#ffffff':c);",
"if(f.stageTreeAura)drawEquippedAura(f,{auraStyle:'tree'});if(!f.summon&&!f.stageTreeAura){const aura=currentAura(f.team);if(aura&&(!aura.exclusiveFor||aura.exclusiveFor===f.id))drawEquippedAura(f,aura)}circle(f.x,f.y,r,f.flash>0?'#ffffff':c);",
'stage tree aura no overlap')

# New persistence / unlocks
once(
"HELL_STAGE_KEY='neonRumble.hellStages.v1',HELL_DEMON_UNLOCK_KEY='neonRumble.hellDemonUnlocked.v1',",
"HELL_STAGE_KEY='neonRumble.hellStages.v1',NEW_CH1_STAGE_KEY='neonRumble.newChapter1Stages.v1',TECHNICIAN_UNLOCK_KEY='neonRumble.technicianUnlocked.v1',HELL_DEMON_UNLOCK_KEY='neonRumble.hellDemonUnlocked.v1',",
'new keys')
once(
"let robotStageMask=0,desertStageMask=0,mansionStageMask=0,spaceStageMask=0,casinoStageMask=0,oceanStageMask=0,forgeStageMask=0,boxingStageMask=0,labStageMask=0,hellStageMask=0,skeletonsUnlocked=false",
"let robotStageMask=0,desertStageMask=0,mansionStageMask=0,spaceStageMask=0,casinoStageMask=0,oceanStageMask=0,forgeStageMask=0,boxingStageMask=0,labStageMask=0,hellStageMask=0,newChapter1StageMask=0,skeletonsUnlocked=false",
'new stage mask')
once("doctorUnlocked=false,hellDemonUnlocked=false;",
     "doctorUnlocked=false,hellDemonUnlocked=false,technicianUnlocked=false;",
     'tech state')
once(
"hellStageMask=Number(localStorage.getItem(HELL_STAGE_KEY)||0)||0;psychicUnlocked=",
"hellStageMask=Number(localStorage.getItem(HELL_STAGE_KEY)||0)||0;newChapter1StageMask=Number(localStorage.getItem(NEW_CH1_STAGE_KEY)||0)||0;technicianUnlocked=localStorage.getItem(TECHNICIAN_UNLOCK_KEY)==='1';psychicUnlocked=",
'load new progress')
once("function chapter10Unlocked(){return (labStageMask&7)===7}",
     "function chapter10Unlocked(){return (labStageMask&7)===7}\nfunction newChapter1Unlocked(){return (hellStageMask&7)===7}",
     'new unlock')
once("function markHellStage(n){hellStageMask|=(1<<(n-1));try{localStorage.setItem(HELL_STAGE_KEY,String(hellStageMask))}catch{}updateChapter10UI();updateDevilTalkUI();return (hellStageMask&7)===7}",
     "function markHellStage(n){hellStageMask|=(1<<(n-1));try{localStorage.setItem(HELL_STAGE_KEY,String(hellStageMask))}catch{}updateChapter10UI();updateDevilTalkUI();updateNewChapter1UI();return (hellStageMask&7)===7}",
     'mark hell new update')
once("(c?.unlock==='hellDemon'&&!hellDemonUnlocked)}",
     "(c?.unlock==='hellDemon'&&!hellDemonUnlocked)||(c?.unlock==='technician'&&!technicianUnlocked)}",
     'technician lock')

# Legacy completion UI
legacy="""function updateLegacyStageCompletionUI(){
 const groups=[['stage-',robotStageMask],['desert-',desertStageMask],['mansion-',mansionStageMask],['space-',spaceStageMask],['casino-',casinoStageMask],['ocean-',oceanStageMask],['forge-',forgeStageMask],['boxing-',boxingStageMask]];
 for(const [prefix,mask] of groups)for(let n=1;n<=3;n++){const card=$(prefix+n);if(!card)continue;let mark=card.querySelector('.legacy-stage-complete');if(mask&(1<<(n-1))){if(!mark){mark=document.createElement('small');mark.className='legacy-stage-complete card-tag';card.appendChild(mark)}mark.textContent='✅ 클리어'}else if(mark)mark.remove()}
}
"""
once("function updateChapter2UI(){",legacy+"function updateChapter2UI(){",'legacy completion function')
for old,new,label in [
("function markSpaceStage(n){const before=chapter5Unlocked();spaceStageMask|=(1<<(n-1));try{localStorage.setItem(SPACE_STAGE_KEY,String(spaceStageMask))}catch{}updateChapter5UI();",
 "function markSpaceStage(n){const before=chapter5Unlocked();spaceStageMask|=(1<<(n-1));try{localStorage.setItem(SPACE_STAGE_KEY,String(spaceStageMask))}catch{}updateChapter5UI();updateLegacyStageCompletionUI();",'mark space complete'),
("function markCasinoStage(n){const before=chapter6Unlocked();casinoStageMask|=(1<<(n-1));try{localStorage.setItem(CASINO_STAGE_KEY,String(casinoStageMask))}catch{}updateChapter6UI();renderShop();",
 "function markCasinoStage(n){const before=chapter6Unlocked();casinoStageMask|=(1<<(n-1));try{localStorage.setItem(CASINO_STAGE_KEY,String(casinoStageMask))}catch{}updateChapter6UI();updateLegacyStageCompletionUI();renderShop();",'mark casino complete'),
("function markOceanStage(n){const before=chapter7Unlocked();oceanStageMask|=(1<<(n-1));try{localStorage.setItem(OCEAN_STAGE_KEY,String(oceanStageMask))}catch{}updateChapter7UI();",
 "function markOceanStage(n){const before=chapter7Unlocked();oceanStageMask|=(1<<(n-1));try{localStorage.setItem(OCEAN_STAGE_KEY,String(oceanStageMask))}catch{}updateChapter7UI();updateLegacyStageCompletionUI();",'mark ocean complete'),
("function markForgeStage(n){const before=chapter8Unlocked();forgeStageMask|=(1<<(n-1));try{localStorage.setItem(FORGE_STAGE_KEY,String(forgeStageMask))}catch{}updateChapter8UI();renderShop();",
 "function markForgeStage(n){const before=chapter8Unlocked();forgeStageMask|=(1<<(n-1));try{localStorage.setItem(FORGE_STAGE_KEY,String(forgeStageMask))}catch{}updateChapter8UI();updateLegacyStageCompletionUI();renderShop();",'mark forge complete'),
("function markBoxingStage(n){const before=chapter9Unlocked();boxingStageMask|=(1<<(n-1));try{localStorage.setItem(BOXING_STAGE_KEY,String(boxingStageMask))}catch{}updateChapter9UI();",
 "function markBoxingStage(n){const before=chapter9Unlocked();boxingStageMask|=(1<<(n-1));try{localStorage.setItem(BOXING_STAGE_KEY,String(boxingStageMask))}catch{}updateChapter9UI();updateLegacyStageCompletionUI();",'mark boxing complete'),
("function markMansionStage(n){const before=chapter4Unlocked();mansionStageMask|=(1<<(n-1));try{localStorage.setItem(MANSION_STAGE_KEY,String(mansionStageMask))}catch{}updateChapter4UI();",
 "function markMansionStage(n){const before=chapter4Unlocked();mansionStageMask|=(1<<(n-1));try{localStorage.setItem(MANSION_STAGE_KEY,String(mansionStageMask))}catch{}updateChapter4UI();updateLegacyStageCompletionUI();",'mark mansion complete'),
("function markDesertStage(n){const before=chapter3Unlocked();desertStageMask|=(1<<(n-1));try{localStorage.setItem(DESERT_STAGE_KEY,String(desertStageMask))}catch{}updateChapter3UI();",
 "function markDesertStage(n){const before=chapter3Unlocked();desertStageMask|=(1<<(n-1));try{localStorage.setItem(DESERT_STAGE_KEY,String(desertStageMask))}catch{}updateChapter3UI();updateLegacyStageCompletionUI();",'mark desert complete'),
("function markRobotStage(n){const before=chapter2Unlocked();robotStageMask|=(1<<(n-1));try{localStorage.setItem(ROBOT_STAGE_KEY,String(robotStageMask))}catch{}updateChapter2UI();",
 "function markRobotStage(n){const before=chapter2Unlocked();robotStageMask|=(1<<(n-1));try{localStorage.setItem(ROBOT_STAGE_KEY,String(robotStageMask))}catch{}updateChapter2UI();updateLegacyStageCompletionUI();",'mark robot complete')]:
    once(old,new,label)

# Mode integration
once("['control','stage','boss-control','desert','mansion','space','casino','ocean','forge','boxing','lab','hell'].includes(mode)",
     "['control','stage','boss-control','desert','mansion','space','casino','ocean','forge','boxing','lab','hell','newchapter'].includes(mode)",
     'manual new mode')
once("mode==='hell'?'히어로 이동 · '+controlName():'왼쪽 캐릭터 이동 · '+controlName()",
     "mode==='hell'?'히어로 이동 · '+controlName():mode==='newchapter'?'로봇 이동 · '+controlName():'왼쪽 캐릭터 이동 · '+controlName()",
     'new control label')

# updateStageUI integration
once(
"hellSelect=mode==='hell-select',special=on||desertSelect||mansionSelect||spaceSelect||casinoSelect||oceanSelect||forgeSelect||boxingSelect||labSelect||hellSelect;",
"hellSelect=mode==='hell-select',newChapterSelect=mode==='newchapter-select',special=on||desertSelect||mansionSelect||spaceSelect||casinoSelect||oceanSelect||forgeSelect||boxingSelect||labSelect||hellSelect||newChapterSelect;",
'new select special')
once("if($('chapter10-entry'))$('chapter10-entry').hidden=special;",
     "if($('chapter10-entry'))$('chapter10-entry').hidden=special;if($('newchapter1-entry'))$('newchapter1-entry').hidden=special;",
     'hide new entry')
once("if($('hell-selection'))$('hell-selection').hidden=!hellSelect;",
     "if($('hell-selection'))$('hell-selection').hidden=!hellSelect;if($('newchapter1-selection'))$('newchapter1-selection').hidden=!newChapterSelect;",
     'new panel visibility')
once("updateChapter9UI();updateChapter10UI()}",
     "updateChapter9UI();updateChapter10UI();updateNewChapter1UI();updateLegacyStageCompletionUI()}",
     'update stage calls')
once("['stage-panel','desert-panel','mansion-panel','space-panel','casino-panel','ocean-panel','forge-panel','boxing-panel','lab-selection','hell-selection']",
     "['stage-panel','desert-panel','mansion-panel','space-panel','casino-panel','ocean-panel','forge-panel','boxing-panel','lab-selection','hell-selection','newchapter1-selection']",
     'hide new panel')

# Update loop/hud
once("if(mode==='lab')updateLabStage();if(mode==='hell')updateHellStage();",
     "if(mode==='lab')updateLabStage();if(mode==='hell')updateHellStage();if(mode==='newchapter')updateNewChapter1Stage();",
     'new mode stage update')

# Result branch new mode before generic
once(
"else if(mode==='hell'){$('winner-icon').textContent='👿';$('winner').textContent='CHAPTER 10 · STAGE '+hellStageNo+' 실패';$('summary').textContent=t+'초 · 히어로가 쓰러졌어. 다시 지옥에 도전해 봐.'}else{",
"""else if(mode==='hell'){$('winner-icon').textContent='👿';$('winner').textContent='CHAPTER 10 · STAGE '+hellStageNo+' 실패';$('summary').textContent=t+'초 · 히어로가 쓰러졌어. 다시 지옥에 도전해 봐.'}else if(mode==='newchapter'&&engine.result===0){const coinReward=awardStageCoins(newChapter1StageNo),auraRoll=newChapter1StageNo===1?tryUnlockTreeAura():null,techRoll=newChapter1StageNo===3?tryUnlockTechnician():null;markNewChapter1Stage(newChapter1StageNo);$('winner-icon').textContent='🆕';$('winner').textContent='NEW-CHAPTER 1 · STAGE '+newChapter1StageNo+' 클리어!';$('summary').textContent=t+'초 · 빌런의 재등장 돌파 · 🪙 '+coinReward+'코인 획득!'+(auraRoll==='won'?' · 🎁 30% 보상 성공! 🌿 나무 아우라 획득!':auraRoll==='miss'?' · 🎲 나무 아우라 획득 실패 (30%)':'')+(techRoll==='won'?' · 🎁 15% 보상 성공! 👨‍💻 기술전문가 획득!':techRoll==='miss'?' · 🎲 기술전문가 획득 실패 (15%)':'')}else if(mode==='newchapter'){$('winner-icon').textContent='🤖';$('winner').textContent='NEW-CHAPTER 1 · STAGE '+newChapter1StageNo+' 실패';$('summary').textContent=t+'초 · 로봇이 쓰러졌어. 다시 도전해 봐.'}else{""",
'new result')

# Rematch
once("mode==='hell'?startHellStage(hellStageNo):start();",
     "mode==='hell'?startHellStage(hellStageNo):mode==='newchapter'?startNewChapter1Stage(newChapter1StageNo):start();",
     'new rematch')
# start and selection reset
once("if(mode==='lab'||mode==='lab-select'||mode==='hell'||mode==='hell-select'){engine=null;mode='duel'}engine=mode===",
     "if(mode==='lab'||mode==='lab-select'||mode==='hell'||mode==='hell-select'||mode==='newchapter'||mode==='newchapter-select'){engine=null;mode='duel'}engine=mode=",
     'start reset new')
once("if(mode==='lab'||mode==='lab-select'||mode==='hell'||mode==='hell-select'){engine=null;mode='duel'}engine=null;paused=false;",
     "if(mode==='lab'||mode==='lab-select'||mode==='hell'||mode==='hell-select'||mode==='newchapter'||mode==='newchapter-select'){engine=null;mode='duel'}engine=null;paused=false;",
     'selection reset new')

# New chapter functions inserted before devil talk lines
newchapter=r"""
let newChapter1StageNo=1;
function markNewChapter1Stage(n){newChapter1StageMask|=(1<<(n-1));try{localStorage.setItem(NEW_CH1_STAGE_KEY,String(newChapter1StageMask))}catch{}updateNewChapter1UI();return (newChapter1StageMask&7)===7}
function tryUnlockTreeAura(){if(ownedCosmetics.includes('aura_tree'))return 'already';if(Math.random()>=.30)return 'miss';ownedCosmetics.push('aura_tree');saveEconomy();renderWardrobe();return 'won'}
function tryUnlockTechnician(){if(technicianUnlocked)return 'already';if(Math.random()>=.15)return 'miss';technicianUnlocked=true;try{localStorage.setItem(TECHNICIAN_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return 'won'}
function updateNewChapter1UI(){const b=$('newchapter1-entry');if(!b)return;const ok=newChapter1Unlocked(),d1=!!(newChapter1StageMask&1),d2=!!(newChapter1StageMask&2),d3=!!(newChapter1StageMask&4),count=(d1?1:0)+(d2?1:0)+(d3?1:0);b.disabled=!ok;b.textContent=ok?'🆕 NEW-CHAPTER 1 · 빌런의 재등장'+(count?' · '+count+'/3':''):'🔒 NEW-CHAPTER 1 · CHAPTER 10 STAGE 1·2·3 클리어 필요';const prog=$('newchapter1-progress');if(prog)prog.textContent='진행도 '+count+' / 3'+(d3?' · ✅ COMPLETE':'');const data=[['newchapter1-1','newchapter1-status-1',d1,true],['newchapter1-2','newchapter1-status-2',d2,d1],['newchapter1-3','newchapter1-status-3',d3,d1&&d2]];for(const [id,sid,done,open] of data){const x=$(id),st=$(sid);if(!x)continue;x.disabled=!ok||!open;if(st)st.textContent=done?'✅ 클리어':open?'도전 가능':'🔒 이전 STAGE 클리어 필요'}}
function setupNewChapter1UI(){if($('newchapter1-entry')){updateNewChapter1UI();return}const after=$('chapter10-entry'),sel=$('selection');if(!after||!sel)return;const b=document.createElement('button');b.id='newchapter1-entry';b.type='button';b.className=after.className;after.insertAdjacentElement('afterend',b);const p=document.createElement('section');p.id='newchapter1-selection';p.className='chapter-stage-panel';p.hidden=true;p.innerHTML='<div class="section-title"><div><p class="eyebrow">NEW-CHAPTER 1</p><h2>🤖 빌런의 재등장</h2></div><span id="newchapter1-progress" class="card-tag">진행도 0 / 3</span></div><p class="match-info">CHAPTER 10 이후의 새로운 이야기. 주인공 🤖 로봇이 다시 나타난 빌런의 흔적을 추적해.</p><div class="roster newchapter1-grid"><button id="newchapter1-1" class="fighter-card" type="button"><span class="card-top"><span class="card-icon">🌳</span><span><strong class="card-name">STAGE 1 · 조종당한 나무</strong><small id="newchapter1-status-1" class="card-tag">도전 가능</small></span></span><span class="card-desc">빌런에게 조종당한 나무 · 🌿 나무 아우라 상시 · 클리어 시 30%로 나무 아우라 획득</span></button><button id="newchapter1-2" class="fighter-card" type="button"><span class="card-top"><span class="card-icon">🦹‍♂️</span><span><strong class="card-name">STAGE 2 · 강화 빌런</strong><small id="newchapter1-status-2" class="card-tag">🔒 이전 STAGE 클리어 필요</small></span></span><span class="card-desc">빌런의 체력·공격력·공격속도 모두 1.5배</span></button><button id="newchapter1-3" class="fighter-card" type="button"><span class="card-top"><span class="card-icon">👨‍💻</span><span><strong class="card-name">STAGE 3 · 기술전문가</strong><small id="newchapter1-status-3" class="card-tag">🔒 이전 STAGE 클리어 필요</small></span></span><span class="card-desc">🔧 랜치 3개 · 비행 중 70 · 벽에 박힌 랜치 80 · 전부 사용하면 회수 AI · 클리어 시 15% 획득</span></button></div><div class="controls"><button id="newchapter1-back" type="button">← 챕터 목록으로</button></div>';sel.appendChild(p);const style=document.createElement('style');style.id='newchapter1-ui';style.textContent='#newchapter1-selection{margin:18px 0 24px;padding:18px;background:linear-gradient(180deg,#121a25,#17101c);border:1px solid #68465c;border-radius:14px}#newchapter1-selection .newchapter1-grid{margin-top:14px}#newchapter1-selection .fighter-card{width:100%;min-height:150px}#newchapter1-selection .fighter-card:disabled{opacity:.48;filter:saturate(.45)}.legacy-stage-complete{color:#b8f279!important;font-weight:800;margin-top:3px}@media(max-width:560px){#newchapter1-selection{padding:14px 10px}#newchapter1-selection .newchapter1-grid{grid-template-columns:1fr}#newchapter1-selection .fighter-card{min-height:0}}';document.head.appendChild(style);b.onclick=()=>{if(!newChapter1Unlocked())return;mode='newchapter-select';updateSelection();updateNewChapter1UI();p.scrollIntoView({behavior:'smooth',block:'start'})};$('newchapter1-back').onclick=()=>{mode='duel';updateSelection();window.scrollTo({top:0,behavior:'smooth'})};$('newchapter1-1').onclick=()=>startNewChapter1Stage(1);$('newchapter1-2').onclick=()=>{if(newChapter1StageMask&1)startNewChapter1Stage(2)};$('newchapter1-3').onclick=()=>{if((newChapter1StageMask&3)===3)startNewChapter1Stage(3)};updateNewChapter1UI()}
function startNewChapter1Stage(n){newChapter1StageNo=n;mode='newchapter';if(n===1){engine=new Engine('robot','tree',Math.random,{mode:'control'});const e=engine.fighters[1];e.stageTreeAura=true}else if(n===2){engine=new Engine('robot','villain',Math.random,{mode:'control'});const v=engine.fighters[1];v.hp*=1.5;v.health=v.hp;v.damage*=1.5;v.stagePower=1.5;v.cooldown=2;v.cd=0}else{engine=new Engine('robot','technician',Math.random,{mode:'control'});const t=engine.fighters[1];t.techWrenchStock=3;t.techWrenchNext=0;t.techWrenches=[];t.techCollecting=false;t.techCollectPending=false}engine.newChapter1Mode=true;paused=false;acc=0;last=performance.now();lastHits=0;lastMessage='';hideStageSelectionPanels();$('selection').hidden=true;$('battle').hidden=false;$('result').hidden=true;$('pause-label').hidden=true;$('pause').disabled=false;$('pause').textContent='일시정지';resetStick();refreshControlUI();$('squad-hud').hidden=true;$('relay-hud').hidden=true;$('score-label0').textContent='🤖 로봇';$('score-label1').textContent=n===1?'🌳 조종당한 나무':n===2?'🦹‍♂️ 강화 빌런':'👨‍💻 기술전문가';$('battle-mode').textContent='NEW-CH1 '+n;$('battle-info').textContent=n===1?'NEW-CHAPTER 1 STAGE 1 · 나무는 🌿 전용 나무 아우라를 사용하며 다른 옷장 아우라와 겹치지 않아. 클리어 시 30%로 나무 아우라 획득.':n===2?'NEW-CHAPTER 1 STAGE 2 · 빌런 체력·공격력·공격속도 1.5배.':'NEW-CHAPTER 1 STAGE 3 · 기술전문가 HP 1000 · 🔧 랜치 3개 · 날아가는 랜치 70 · 벽에 박힌 랜치 접촉 80 · 3개 소진 후 회수 AI · 클리어 시 15% 획득.';fit();hud();draw();window.scrollTo({top:0,behavior:'auto'});playSfx('start')}
function updateNewChapter1Stage(){if(mode!=='newchapter'||!engine||engine.result!==null)return;const hero=engine.fighters.find(f=>f.id==='robot'&&f.team===0&&!f.summon);if(!hero||hero.health<=0){engine.result=1;return}const enemy=engine.fighters.find(f=>f.team===1&&!f.summon);if(!enemy||enemy.health<=0)engine.result=0}
"""
once("const DEVIL_TALK_LINES=[",newchapter+"\nconst DEVIL_TALK_LINES=[",'new chapter code')
once("setupChapter9UI();setupChapter10UI();setupDevilTalkUI();",
     "setupChapter9UI();setupChapter10UI();setupNewChapter1UI();setupDevilTalkUI();updateLegacyStageCompletionUI();",
     'setup new chapter')

# Preserve new chapter entry ordering when devil button is inserted by placing talk after new chapter entry if available
once("const after=$('chapter10-entry');if(!after)return;const b=document.createElement('button');",
     "const after=$('newchapter1-entry')||$('chapter10-entry');if(!after)return;const b=document.createElement('button');",
     'devil talk placement')

# Main mode clean-up should also understand newchapter-select in switch regular
once("function switchRegularMode(next){if(mode==='desert'||mode==='desert-select')",
     "function switchRegularMode(next){if(mode==='newchapter'||mode==='newchapter-select'){engine=null}if(mode==='desert'||mode==='desert-select')",
     'switch new mode')

# Ability HUD
once("function ability(f){if(f.id==='hell_demon'||f.id==='hell_clone')",
     "function ability(f){if(f.id==='technician')return '👨‍💻 🔧 '+(f.techWrenchStock??3)+'/3 · '+(f.techCollecting?'랜치 회수 중':'투척/전투');if(f.id==='hell_demon'||f.id==='hell_clone')",
     'tech ability')

p.write_text(s,encoding='utf-8')
print('v3.75 new chapter convenience patch applied')
