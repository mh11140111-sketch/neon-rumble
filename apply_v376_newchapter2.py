from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1 got {n}')
    s=s.replace(old,new,1)

# Patch notes (keep 3.76)
once(
'<summary>📒 패치노트 · v3.76</summary><div class="patch-body">',
'<summary>📒 패치노트 · v3.76</summary><div class="patch-body"><div class="patch-version"><h3>v3.76 · NEW-CHAPTER 2 · 편의성/밸런스</h3><ul><li>👨‍💻 기술전문가가 랜치를 회수할 때마다 HP 20 회복.</li><li>🗺️ 제작소 옆에 스테이지 바로가기 버튼 추가.</li><li>🥊 복싱장 · 🧪 실험실 · 🔥 지옥 클리어 후 전용 배경 상점 구매 가능.</li><li>💀 NEW-CHAPTER 2 「해골 강림」 추가. 주인공은 🤠 카우보이, 전장은 사막.</li></ul></div>',
'patch note')

# Technician heal on wrench pickup + text
once(
"f.techWrenches.splice(f.techWrenches.indexOf(w),1);f.techWrenchStock++;this.effect(f,'🔧 회수 '+f.techWrenchStock+'/3','heal');f.techCollectTarget=null",
"f.techWrenches.splice(f.techWrenches.indexOf(w),1);f.techWrenchStock++;const heal=Math.min(20*f.scale,f.hp-f.health);f.health+=heal;f.healed=(f.healed||0)+heal;this.effect(f,'🔧 회수 '+f.techWrenchStock+'/3'+(heal?' · HP +'+Math.round(heal):''),'heal');f.techCollectTarget=null",
'technician heal')
once(
"description:'로봇을 만든 기술전문가. 랜치 3개를 던지며 날아가는 랜치는 피해 70. 벽에 닿으면 박히고, 박힌 랜치에 닿은 적은 피해 80. 3개를 모두 사용하면 랜치 수집 AI로 바뀌어 직접 회수하고, 전부 회수하면 다시 일반 전투로 돌아온다.',detail:'HP 1000 · 🔧 3개 · 투척 70 / 1.3초 · 벽 고정 랜치 접촉 80 · 랜치 0개 시 회수 AI · 3개 회수 시 일반 AI 복귀 · NEW-CH1 STAGE 3 15% 획득'",
"description:'로봇을 만든 기술전문가. 랜치 3개를 던지며 날아가는 랜치는 피해 70. 벽에 닿으면 박히고, 박힌 랜치에 닿은 적은 피해 80. 랜치를 회수할 때마다 HP 20을 회복하며, 3개를 전부 회수하면 다시 일반 전투로 돌아온다.',detail:'HP 1000 · 🔧 3개 · 투척 70 / 1.3초 · 벽 고정 랜치 접촉 80 · 회수마다 HP +20 · 랜치 0개 시 회수 AI · 3개 회수 시 일반 AI 복귀 · NEW-CH1 STAGE 3 15% 획득'",
'technician text')

# Backgrounds 8/9/10
once(
" {id:'bg_forge',name:'대장간 배경',icon:'🔨',price:1000,type:'background',chapter:7,backgroundStyle:'forge',exclusiveFor:null,desc:'CHAPTER 7 스테이지 1·2·3 클리어 후 구매 가능'},",
" {id:'bg_forge',name:'대장간 배경',icon:'🔨',price:1000,type:'background',chapter:7,backgroundStyle:'forge',exclusiveFor:null,desc:'CHAPTER 7 스테이지 1·2·3 클리어 후 구매 가능'},\n {id:'bg_boxing',name:'복싱장 배경',icon:'🥊',price:1000,type:'background',chapter:8,backgroundStyle:'boxing',exclusiveFor:null,desc:'CHAPTER 8 복싱장 STAGE 1·2·3 클리어 후 구매 가능'},\n {id:'bg_lab',name:'실험실 배경',icon:'🧪',price:1000,type:'background',chapter:9,backgroundStyle:'lab',exclusiveFor:null,desc:'CHAPTER 9 실험실 탈출 STAGE 1·2·3 클리어 후 구매 가능'},\n {id:'bg_hell',name:'지옥 배경',icon:'🔥',price:1000,type:'background',chapter:10,backgroundStyle:'hell',exclusiveFor:null,desc:'CHAPTER 10 지옥 STAGE 1·2·3 클리어 후 구매 가능'},",
'background items')
once(
"return item.chapter===2?(desertStageMask&7)===7:item.chapter===3?(mansionStageMask&7)===7:item.chapter===4?(spaceStageMask&7)===7:item.chapter===5?(casinoStageMask&7)===7:item.chapter===7?(forgeStageMask&7)===7:false}",
"return item.chapter===2?(desertStageMask&7)===7:item.chapter===3?(mansionStageMask&7)===7:item.chapter===4?(spaceStageMask&7)===7:item.chapter===5?(casinoStageMask&7)===7:item.chapter===7?(forgeStageMask&7)===7:item.chapter===8?(boxingStageMask&7)===7:item.chapter===9?(labStageMask&7)===7:item.chapter===10?(hellStageMask&7)===7:false}",
'background unlock')
# refresh shop on completion
once("function markBoxingStage(n){const before=chapter9Unlocked();boxingStageMask|=(1<<(n-1));try{localStorage.setItem(BOXING_STAGE_KEY,String(boxingStageMask))}catch{}updateChapter9UI();updateLegacyStageCompletionUI();return !before&&chapter9Unlocked()}",
     "function markBoxingStage(n){const before=chapter9Unlocked();boxingStageMask|=(1<<(n-1));try{localStorage.setItem(BOXING_STAGE_KEY,String(boxingStageMask))}catch{}updateChapter9UI();updateLegacyStageCompletionUI();renderShop();return !before&&chapter9Unlocked()}",
     'boxing shop refresh')
once("function markLabStage(n){const before=chapter10Unlocked();labStageMask|=(1<<(n-1));try{localStorage.setItem(LAB_STAGE_KEY,String(labStageMask))}catch{}updateChapter9UI();updateChapter10UI();return !before&&chapter10Unlocked()}",
     "function markLabStage(n){const before=chapter10Unlocked();labStageMask|=(1<<(n-1));try{localStorage.setItem(LAB_STAGE_KEY,String(labStageMask))}catch{}updateChapter9UI();updateChapter10UI();renderShop();return !before&&chapter10Unlocked()}",
     'lab shop refresh')
once("function markHellStage(n){hellStageMask|=(1<<(n-1));try{localStorage.setItem(HELL_STAGE_KEY,String(hellStageMask))}catch{}updateChapter10UI();updateDevilTalkUI();updateNewChapter1UI();return (hellStageMask&7)===7}",
     "function markHellStage(n){hellStageMask|=(1<<(n-1));try{localStorage.setItem(HELL_STAGE_KEY,String(hellStageMask))}catch{}updateChapter10UI();updateDevilTalkUI();updateNewChapter1UI();renderShop();return (hellStageMask&7)===7}",
     'hell shop refresh')

# Wardrobe background visuals
once(
"}else if(st==='forge'){const fg=ctx.createLinearGradient(0,0,0,720);",
"}else if(st==='boxing'){const bg=ctx.createLinearGradient(0,0,0,720);bg.addColorStop(0,'#1b2430');bg.addColorStop(.55,'#10151c');bg.addColorStop(1,'#090c11');ctx.fillStyle=bg;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.55;ctx.strokeStyle='#eee';ctx.lineWidth=5;for(const y of [110,145,180]){ctx.beginPath();ctx.moveTo(55,y);ctx.lineTo(665,y);ctx.stroke()}ctx.globalAlpha=.35;ctx.font='42px sans-serif';ctx.fillText('🥊',90,610);ctx.fillText('🥊',620,610);ctx.globalAlpha=1}else if(st==='lab'){const lg=ctx.createLinearGradient(0,0,0,720);lg.addColorStop(0,'#102633');lg.addColorStop(.55,'#0b1a22');lg.addColorStop(1,'#071014');ctx.fillStyle=lg;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.38;ctx.font='44px sans-serif';ctx.fillText('🧪',90,150);ctx.fillText('🧬',620,170);ctx.fillText('🔬',110,610);ctx.globalAlpha=1}else if(st==='hell'){const hg=ctx.createLinearGradient(0,0,0,720);hg.addColorStop(0,'#300709');hg.addColorStop(.55,'#170508');hg.addColorStop(1,'#070305');ctx.fillStyle=hg;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.45;ctx.font='46px sans-serif';ctx.fillText('🔥',95,160);ctx.fillText('⛓️',610,170);ctx.fillText('🔥',620,610);ctx.globalAlpha=1}else if(st==='forge'){const fg=ctx.createLinearGradient(0,0,0,720);",
'background visuals')

# Stage jump button beside craft
once(
"bar.appendChild(b);const p=document.createElement('div');",
"bar.appendChild(b);const jump=document.createElement('button');jump.id='stage-jump-btn';jump.type='button';jump.textContent='🗺️ 스테이지 바로가기';jump.onclick=()=>{for(const id of ['shop-panel','wardrobe-panel','casino-system-panel','craft-system-panel']){const x=$(id);if(x)x.hidden=true}const target=$('stage-entry')||$('chapter2-entry');if(target)target.scrollIntoView({behavior:'smooth',block:'start'})};bar.appendChild(jump);const p=document.createElement('div');",
'stage jump')

# New progress/unlock keys and state
once(
"NEW_CH1_STAGE_KEY='neonRumble.newChapter1Stages.v1',TECHNICIAN_UNLOCK_KEY='neonRumble.technicianUnlocked.v1',",
"NEW_CH1_STAGE_KEY='neonRumble.newChapter1Stages.v1',NEW_CH2_STAGE_KEY='neonRumble.newChapter2Stages.v1',TECHNICIAN_UNLOCK_KEY='neonRumble.technicianUnlocked.v1',SKELE44_UNLOCK_KEY='neonRumble.skele44Unlocked.v1',",
'newch2 keys')
once(
"hellStageMask=0,newChapter1StageMask=0,skeletonsUnlocked=false",
"hellStageMask=0,newChapter1StageMask=0,newChapter2StageMask=0,skeletonsUnlocked=false",
'newch2 mask var')
once("doctorUnlocked=false,hellDemonUnlocked=false,technicianUnlocked=false;",
     "doctorUnlocked=false,hellDemonUnlocked=false,technicianUnlocked=false,skele44Unlocked=false;",
     'skele44 var')
once(
"newChapter1StageMask=Number(localStorage.getItem(NEW_CH1_STAGE_KEY)||0)||0;technicianUnlocked=localStorage.getItem(TECHNICIAN_UNLOCK_KEY)==='1';",
"newChapter1StageMask=Number(localStorage.getItem(NEW_CH1_STAGE_KEY)||0)||0;newChapter2StageMask=Number(localStorage.getItem(NEW_CH2_STAGE_KEY)||0)||0;technicianUnlocked=localStorage.getItem(TECHNICIAN_UNLOCK_KEY)==='1';skele44Unlocked=localStorage.getItem(SKELE44_UNLOCK_KEY)==='1';",
'load newch2')
once("function newChapter1Unlocked(){return (hellStageMask&7)===7}",
     "function newChapter1Unlocked(){return (hellStageMask&7)===7}\nfunction newChapter2Unlocked(){return (newChapter1StageMask&7)===7}",
     'newch2 unlock')
once("(c?.unlock==='technician'&&!technicianUnlocked)}",
     "(c?.unlock==='technician'&&!technicianUnlocked)||(c?.unlock==='skele44'&&!skele44Unlocked)}",
     'skele44 lock')

# Roster additions
once(
"{id:'technician',name:'기술전문가',icon:'👨‍💻',tag:'🔧 랜치 3개 · 벽 고정 · 회수 AI',hp:1000,damage:70,speed:155,cooldown:1.3,unlock:'technician',description:'로봇을 만든 기술전문가. 랜치 3개를 던지며 날아가는 랜치는 피해 70. 벽에 닿으면 박히고, 박힌 랜치에 닿은 적은 피해 80. 랜치를 회수할 때마다 HP 20을 회복하며, 3개를 전부 회수하면 다시 일반 전투로 돌아온다.',detail:'HP 1000 · 🔧 3개 · 투척 70 / 1.3초 · 벽 고정 랜치 접촉 80 · 회수마다 HP +20 · 랜치 0개 시 회수 AI · 3개 회수 시 일반 AI 복귀 · NEW-CH1 STAGE 3 15% 획득'},",
"{id:'technician',name:'기술전문가',icon:'👨‍💻',tag:'🔧 랜치 3개 · 벽 고정 · 회수 AI',hp:1000,damage:70,speed:155,cooldown:1.3,unlock:'technician',description:'로봇을 만든 기술전문가. 랜치 3개를 던지며 날아가는 랜치는 피해 70. 벽에 닿으면 박히고, 박힌 랜치에 닿은 적은 피해 80. 랜치를 회수할 때마다 HP 20을 회복하며, 3개를 전부 회수하면 다시 일반 전투로 돌아온다.',detail:'HP 1000 · 🔧 3개 · 투척 70 / 1.3초 · 벽 고정 랜치 접촉 80 · 회수마다 HP +20 · 랜치 0개 시 회수 AI · 3개 회수 시 일반 AI 복귀 · NEW-CH1 STAGE 3 15% 획득'},\n{id:'skeleton_king',name:'해골왕',icon:'👑💀',tag:'모든 해골 전투술',hp:1500,damage:70,speed:135,cooldown:1,stageOnly:true,description:'총잡이·칼잡이·취한 해골·해골 법사의 공격 방식을 모두 사용하는 해골왕.',detail:'HP 1500 · 🔫 총알 70 · 🗡️ 칼 70 · 🍺 맥주병 100 · 💀 마법탄 65 · 해골 소환'},\n{id:'skele44',name:'스켈-44',icon:'🧫☠️',tag:'감염 투사체 · 해골 변환',hp:1000,damage:50,speed:140,cooldown:1,unlock:'skele44',description:'1초마다 피해 50의 감염 투사체를 던진다. 적중 시 30% 확률로 랜덤 해골을 소환하고, 직접 처치한 적은 죽기 직전 체력의 2배 HP를 가진 랜덤 해골로 바꾼다.',detail:'HP 1000 · 🧫 투사체 50 / 1초 · 명중 시 해골 소환 30% · 처치 시 죽기 직전 HP×2 랜덤 해골 변환 · NEW-CH2 STAGE 3 10% 획득'},",
'roster new')

# Engine methods for skeleton king / Skele-44 before technician
anchor="technicianSkill(f,e){"
methods=r"""spawnSkele44Skeleton(owner,x,y,hpOverride=null){
 if(!owner||owner.health<=0)return null;const ids=['skeleton_gun','skeleton_sword','skeleton_drunk','skeleton_mage'],id=ids[Math.floor(this.random()*ids.length)],base=new Engine('boxer',id,this.random,{mode:'control'}).fighters[1],side=this.fighters.length;
 base.side=side;base.team=owner.team;base.summon=true;base.ownerSide=owner.side;base.noSkeletonRevive=true;base.revivals=0;base.boss=false;base.scale=1;base.bodyScale=1;base.radius=33;base.x=clamp(x+this.rand(-26,26),55,665);base.y=clamp(y+this.rand(-26,26),55,665);base.trail=[];base.deathOrder=null;
 if(hpOverride!=null){base.hp=Math.max(1,Math.round(hpOverride));base.health=base.hp}
 this.fighters.push(base);this.effect(owner,'🧫☠️ '+base.icon+' 소환!','skill');return base
}
skele44Skill(f,e){
 if(!f||f.id!=='skele44'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0||f.cd>1e-9)return;const a=this.aim(f,e);this.shots.push({x:f.x+a.x*(f.radius+8),y:f.y+a.y*(f.radius+8),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'skele44',icon:'🧫',radius:9*f.scale,speed:360*f.scale,damage:50*f.scale,life:4,bounces:0});f.cd=1/f.scale;f.attack=.18/f.scale;this.effect(f,'🧫☠️ 감염 투사체!','skill')
}
skeletonKingSkill(f,e){
 if(!f||f.id!=='skeleton_king'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0)return;
 if(!Number.isFinite(f.skGunNext)){f.skGunNext=this.time;f.skSwordNext=this.time;f.skBeerNext=this.time;f.skMagicNext=this.time;f.skSummonNext=this.time+10}
 const a=this.aim(f,e),ang=Math.atan2(a.y,a.x);
 if(this.time>=f.skGunNext-1e-9){this.shots.push({x:f.x+a.x*(f.radius+8),y:f.y+a.y*(f.radius+8),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'skeletonbullet',radius:5*f.scale,speed:440*f.scale,damage:70*f.scale,life:3,bounces:0});f.skGunNext=this.time+1.5/f.scale}
 if(this.time>=f.skSwordNext-1e-9&&distance(f,e)<=f.radius+e.radius+55*f.scale){this.attack(f,e,70*f.scale);f.skSwordNext=this.time+3/f.scale;this.effect(f,'🗡️ 70','skill')}
 if(this.time>=f.skBeerNext-1e-9){const aa=ang+this.rand(-.95,.95),vx=Math.cos(aa),vy=Math.sin(aa);this.shots.push({x:f.x+vx*(f.radius+22),y:f.y+vy*(f.radius+22),vx,vy,owner:f.side,team:f.team,target:e.side,kind:'beer',radius:9*f.scale,speed:285*f.scale,damage:100*f.scale,life:3,bounces:0});f.skBeerNext=this.time+1/f.scale}
 if(this.time>=f.skMagicNext-1e-9){this.shots.push({x:f.x+a.x*(f.radius+6),y:f.y+a.y*(f.radius+6),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'magic',radius:5*f.scale,speed:200*f.scale,damage:65*f.scale,life:5*f.scale,bounces:0});f.skMagicNext=this.time+1.45/f.scale}
 if(this.time>=f.skSummonNext-1e-9){f.skSummonNext=this.time+10/f.scale;this.spawnSkele44Skeleton(f,f.x,f.y);this.effect(f,'👑💀 해골 소환!','skill')}
}
"""
once(anchor,methods+anchor,'new engine methods')

# call skills + contact exclusions
once("if(f.id==='technician')this.technicianSkill(f,e);",
     "if(f.id==='technician')this.technicianSkill(f,e);if(f.id==='skele44')this.skele44Skill(f,e);if(f.id==='skeleton_king')this.skeletonKingSkill(f,e);",
     'new skill calls')
once("'doctor','technician','hell_clone','hell_demon'].includes(f.id)",
     "'doctor','technician','skele44','skeleton_king','hell_clone','hell_demon'].includes(f.id)",
     'contact exclusions')

# Skele44 hit summon + death conversion in attack()
once(
"this.formEgg(e);\n if(e.health===0){this.furballDeathHeal(e,preDeathHp);",
"this.formEgg(e);\n if(f.id==='skele44'&&n>0&&this.random()<.30&&e.health>0)this.spawnSkele44Skeleton(f,e.x,e.y);\n if(e.health===0){if(f.id==='skele44')this.spawnSkele44Skeleton(f,e.x,e.y,preDeathHp*2);this.furballDeathHeal(e,preDeathHp);",
'skele44 attack hooks')

# New chapter2 mode names and manual/draw
once("'lab','hell','newchapter'].includes(mode)",
     "'lab','hell','newchapter','newchapter2'].includes(mode)",
     'manual newch2')
once("mode==='newchapter'?'로봇 이동 · '+controlName():",
     "mode==='newchapter'?'로봇 이동 · '+controlName():mode==='newchapter2'?'카우보이 이동 · '+controlName():",
     'control label newch2')
once("else if(mode==='desert'){const dg=ctx.createLinearGradient",
     "else if(mode==='desert'||mode==='newchapter2'){const dg=ctx.createLinearGradient",
     'desert background newch2')

# UI special mode support
once("newChapterSelect=mode==='newchapter-select',special=",
     "newChapterSelect=mode==='newchapter-select',newChapter2Select=mode==='newchapter2-select',special=",
     'newch2 select var')
once("||hellSelect||newChapterSelect;",
     "||hellSelect||newChapterSelect||newChapter2Select;",
     'newch2 special')
once("if($('newchapter1-entry'))$('newchapter1-entry').hidden=special;",
     "if($('newchapter1-entry'))$('newchapter1-entry').hidden=special;if($('newchapter2-entry'))$('newchapter2-entry').hidden=special;",
     'hide newch2 entry')
once("if($('newchapter1-selection'))$('newchapter1-selection').hidden=!newChapterSelect;",
     "if($('newchapter1-selection'))$('newchapter1-selection').hidden=!newChapterSelect;if($('newchapter2-selection'))$('newchapter2-selection').hidden=!newChapter2Select;",
     'newch2 panel visibility')
once("updateChapter10UI();updateNewChapter1UI();updateLegacyStageCompletionUI()",
     "updateChapter10UI();updateNewChapter1UI();updateNewChapter2UI();updateLegacyStageCompletionUI()",
     'update newch2 UI')
once("'newchapter1-selection']",
     "'newchapter1-selection','newchapter2-selection']",
     'hide panels newch2')

# start/selection reset and rematch
old_reset="||mode==='newchapter'||mode==='newchapter-select'){engine=null;mode='duel'}"
new_reset="||mode==='newchapter'||mode==='newchapter-select'||mode==='newchapter2'||mode==='newchapter2-select'){engine=null;mode='duel'}"
if s.count(old_reset)!=2: raise SystemExit(f'start/selection reset newch2: expected 2 got {s.count(old_reset)}')
s=s.replace(old_reset,new_reset)
once("mode==='newchapter'?startNewChapter1Stage(newChapter1StageNo):start();",
     "mode==='newchapter'?startNewChapter1Stage(newChapter1StageNo):mode==='newchapter2'?startNewChapter2Stage(newChapter2StageNo):start();",
     'rematch newch2')

# Loop includes later stage updaters
once("updateForgeStage();updateBoxingStage();hud()}",
     "updateForgeStage();updateBoxingStage();updateLabStage();updateHellStage();updateNewChapter1Stage();updateNewChapter2Stage();hud()}",
     'loop newch2')

# Result handling newch2
once(
"else if(mode==='newchapter'){$('winner-icon').textContent='🤖';$('winner').textContent='NEW-CHAPTER 1 · STAGE '+newChapter1StageNo+' 실패';$('summary').textContent=t+'초 · 로봇이 쓰러졌어. 다시 도전해 봐.'}else{",
"else if(mode==='newchapter'){$('winner-icon').textContent='🤖';$('winner').textContent='NEW-CHAPTER 1 · STAGE '+newChapter1StageNo+' 실패';$('summary').textContent=t+'초 · 로봇이 쓰러졌어. 다시 도전해 봐.'}else if(mode==='newchapter2'&&engine.result===0){const coinReward=awardStageCoins(newChapter2StageNo),skRoll=newChapter2StageNo===3?tryUnlockSkele44():null;markNewChapter2Stage(newChapter2StageNo);$('winner-icon').textContent='💀';$('winner').textContent='NEW-CHAPTER 2 · STAGE '+newChapter2StageNo+' 클리어!';$('summary').textContent=t+'초 · 해골 강림 돌파 · 🪙 '+coinReward+'코인 획득!'+(skRoll==='won'?' · 🎁 10% 보상 성공! 🧫☠️ 스켈-44 획득!':skRoll==='miss'?' · 🎲 스켈-44 획득 실패 (10%)':'')}else if(mode==='newchapter2'){$('winner-icon').textContent='🤠';$('winner').textContent='NEW-CHAPTER 2 · STAGE '+newChapter2StageNo+' 실패';$('summary').textContent=t+'초 · 카우보이가 쓰러졌어. 다시 해골 강림에 도전해 봐.'}else{",
'result newch2')

# New Chapter 2 implementation before devil lines
newch2=r"""
let newChapter2StageNo=1,newChapter2Wave=0;
function markNewChapter2Stage(n){newChapter2StageMask|=(1<<(n-1));try{localStorage.setItem(NEW_CH2_STAGE_KEY,String(newChapter2StageMask))}catch{}updateNewChapter2UI();return (newChapter2StageMask&7)===7}
function tryUnlockSkele44(){if(skele44Unlocked)return 'already';if(Math.random()>=.10)return 'miss';skele44Unlocked=true;try{localStorage.setItem(SKELE44_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return 'won'}
function updateNewChapter2UI(){const b=$('newchapter2-entry');if(!b)return;const ok=newChapter2Unlocked(),d1=!!(newChapter2StageMask&1),d2=!!(newChapter2StageMask&2),d3=!!(newChapter2StageMask&4),count=(d1?1:0)+(d2?1:0)+(d3?1:0);b.disabled=!ok;b.textContent=ok?'💀 NEW-CHAPTER 2 · 해골 강림'+(count?' · '+count+'/3':''):'🔒 NEW-CHAPTER 2 · NEW-CHAPTER 1 STAGE 1·2·3 클리어 필요';const prog=$('newchapter2-progress');if(prog)prog.textContent='진행도 '+count+' / 3'+(d3?' · ✅ COMPLETE':'');const data=[['newchapter2-1','newchapter2-status-1',d1,true],['newchapter2-2','newchapter2-status-2',d2,d1],['newchapter2-3','newchapter2-status-3',d3,d1&&d2]];for(const [id,sid,done,open] of data){const x=$(id),st=$(sid);if(!x)continue;x.disabled=!ok||!open;if(st)st.textContent=done?'✅ 클리어':open?'도전 가능':'🔒 이전 STAGE 클리어 필요'}}
function setupNewChapter2UI(){if($('newchapter2-entry')){updateNewChapter2UI();return}const after=$('newchapter1-entry'),sel=$('selection');if(!after||!sel)return;const b=document.createElement('button');b.id='newchapter2-entry';b.type='button';b.className=after.className;after.insertAdjacentElement('afterend',b);const p=document.createElement('section');p.id='newchapter2-selection';p.className='chapter-stage-panel';p.hidden=true;p.innerHTML='<div class="section-title"><div><p class="eyebrow">NEW-CHAPTER 2</p><h2>💀 해골 강림</h2></div><span id="newchapter2-progress" class="card-tag">진행도 0 / 3</span></div><p class="match-info">주인공 🤠 카우보이 · 배경은 사막. 다시 밀려온 해골 군단의 근원을 추적해.</p><div class="roster newchapter2-grid"><button id="newchapter2-1" class="fighter-card" type="button"><span class="card-top"><span class="card-icon">💀</span><span><strong class="card-name">STAGE 1 · 해골 10웨이브</strong><small id="newchapter2-status-1" class="card-tag">도전 가능</small></span></span><span class="card-desc">총잡이·칼잡이·취한 해골 랜덤 3명씩 10웨이브 · 웨이브 클리어마다 HP 30% 회복</span></button><button id="newchapter2-2" class="fighter-card" type="button"><span class="card-top"><span class="card-icon">👑💀</span><span><strong class="card-name">STAGE 2 · 해골왕</strong><small id="newchapter2-status-2" class="card-tag">🔒 이전 STAGE 클리어 필요</small></span></span><span class="card-desc">HP 1500 · 총잡이/칼잡이/취한 해골/해골 법사의 모든 공격 방식 사용</span></button><button id="newchapter2-3" class="fighter-card" type="button"><span class="card-top"><span class="card-icon">🧫☠️</span><span><strong class="card-name">STAGE 3 · 스켈-44</strong><small id="newchapter2-status-3" class="card-tag">🔒 이전 STAGE 클리어 필요</small></span></span><span class="card-desc">🧫 50 / 1초 · 적중 시 30% 랜덤 해골 소환 · 처치한 적을 죽기 직전 HP×2 랜덤 해골로 변환 · 클리어 시 10% 획득</span></button></div><div class="controls"><button id="newchapter2-back" type="button">← 챕터 목록으로</button></div>';sel.appendChild(p);const style=document.createElement('style');style.id='newchapter2-ui';style.textContent='#newchapter2-selection{margin:18px 0 24px;padding:18px;background:linear-gradient(180deg,#2d2113,#17110b);border:1px solid #7d633d;border-radius:14px}#newchapter2-selection .newchapter2-grid{margin-top:14px}#newchapter2-selection .fighter-card{width:100%;min-height:150px}#newchapter2-selection .fighter-card:disabled{opacity:.48;filter:saturate(.45)}@media(max-width:560px){#newchapter2-selection{padding:14px 10px}#newchapter2-selection .newchapter2-grid{grid-template-columns:1fr}#newchapter2-selection .fighter-card{min-height:0}}';document.head.appendChild(style);b.onclick=()=>{if(!newChapter2Unlocked())return;mode='newchapter2-select';updateSelection();updateNewChapter2UI();p.scrollIntoView({behavior:'smooth',block:'start'})};$('newchapter2-back').onclick=()=>{mode='duel';updateSelection();window.scrollTo({top:0,behavior:'smooth'})};$('newchapter2-1').onclick=()=>startNewChapter2Stage(1);$('newchapter2-2').onclick=()=>{if(newChapter2StageMask&1)startNewChapter2Stage(2)};$('newchapter2-3').onclick=()=>{if((newChapter2StageMask&3)===3)startNewChapter2Stage(3)};updateNewChapter2UI()}
function spawnNewChapter2Wave(){newChapter2Wave++;const ids=['skeleton_gun','skeleton_sword','skeleton_drunk'],spots=[[535,180],[610,360],[535,540]];for(let i=0;i<3;i++){const id=ids[Math.floor(Math.random()*ids.length)],tmp=new Engine('cowboy',id,Math.random,{mode:'control'}).fighters[1];tmp.side=engine.fighters.length;tmp.team=1;tmp.summon=true;tmp.ownerSide=1;tmp.noSkeletonRevive=true;tmp.revivals=0;tmp.x=spots[i][0];tmp.y=spots[i][1];tmp.trail=[];tmp.deathOrder=null;engine.fighters.push(tmp)}$('event').textContent='💀 WAVE '+newChapter2Wave+' / 10 · 해골 3명 출현!'}
function startNewChapter2Stage(n){newChapter2StageNo=n;newChapter2Wave=0;mode='newchapter2';if(n===1){engine=new Engine('cowboy','skeleton_gun',Math.random,{mode:'control'});engine.fighters[1].health=0;engine.desertWaveMode=true;spawnNewChapter2Wave()}else if(n===2){engine=new Engine('cowboy','skeleton_king',Math.random,{mode:'control'});const b=engine.fighters[1];b.hp=1500;b.health=1500;engine.desertWaveMode=false}else{engine=new Engine('cowboy','skele44',Math.random,{mode:'control'});engine.desertWaveMode=false}engine.newChapter2Mode=true;paused=false;acc=0;last=performance.now();lastHits=0;lastMessage='';hideStageSelectionPanels();$('selection').hidden=true;$('battle').hidden=false;$('result').hidden=true;$('pause-label').hidden=true;$('pause').disabled=false;$('pause').textContent='일시정지';resetStick();refreshControlUI();$('squad-hud').hidden=true;$('relay-hud').hidden=true;$('score-label0').textContent='🤠 카우보이';$('score-label1').textContent=n===1?'💀 해골 10웨이브':n===2?'👑💀 해골왕':'🧫☠️ 스켈-44';$('battle-mode').textContent='NEW-CH2 '+n;$('battle-info').textContent=n===1?'NEW-CHAPTER 2 STAGE 1 · 해골 3명씩 10웨이브 · 웨이브 클리어마다 카우보이 최대 HP 30% 회복.':n===2?'NEW-CHAPTER 2 STAGE 2 · 해골왕 HP 1500 · 모든 해골 공격 방식 사용.':'NEW-CHAPTER 2 STAGE 3 · 스켈-44 HP 1000 · 투사체 50/1초 · 적중 시 30% 랜덤 해골 소환 · 직접 처치한 적을 죽기 직전 HP×2 해골로 변환 · 클리어 시 10% 획득.';fit();hud();draw();window.scrollTo({top:0,behavior:'auto'});playSfx('start')}
function updateNewChapter2Stage(){if(mode!=='newchapter2'||!engine||engine.result!==null)return;const hero=engine.fighters.find(f=>f.id==='cowboy'&&f.team===0&&!f.summon);if(!hero||hero.health<=0){engine.result=1;return}if(newChapter2StageNo===1){const alive=engine.fighters.some(f=>f.team===1&&f.health>0);if(!alive){const before=hero.health;hero.health=Math.min(hero.hp,hero.health+hero.hp*.30);const heal=Math.max(0,Math.round(hero.health-before));if(heal){hero.healed=(hero.healed||0)+heal;engine.effect(hero,'💀 WAVE CLEAR +'+heal+' (30%)','heal')}if(newChapter2Wave>=10){engine.result=0;engine.desertWaveMode=false}else spawnNewChapter2Wave()}}else{const boss=engine.fighters.find(f=>f.team===1&&!f.summon);if(!boss||boss.health<=0)engine.result=0}}
"""
once("const DEVIL_TALK_LINES=[",newch2+"\nconst DEVIL_TALK_LINES=[",'newch2 functions')

# When CH1 is marked, update CH2
once("function markNewChapter1Stage(n){newChapter1StageMask|=(1<<(n-1));try{localStorage.setItem(NEW_CH1_STAGE_KEY,String(newChapter1StageMask))}catch{}updateNewChapter1UI();return (newChapter1StageMask&7)===7}",
     "function markNewChapter1Stage(n){newChapter1StageMask|=(1<<(n-1));try{localStorage.setItem(NEW_CH1_STAGE_KEY,String(newChapter1StageMask))}catch{}updateNewChapter1UI();updateNewChapter2UI();return (newChapter1StageMask&7)===7}",
     'newch1 updates newch2')

# Setup ordering + devil placement after newch2
once("const after=$('newchapter1-entry')||$('chapter10-entry');if(!after)return;const b=document.createElement('button');",
     "const after=$('newchapter2-entry')||$('newchapter1-entry')||$('chapter10-entry');if(!after)return;const b=document.createElement('button');",
     'devil after newch2')
once("setupChapter9UI();setupChapter10UI();setupNewChapter1UI();setupDevilTalkUI();updateLegacyStageCompletionUI();",
     "setupChapter9UI();setupChapter10UI();setupNewChapter1UI();setupNewChapter2UI();setupDevilTalkUI();updateLegacyStageCompletionUI();",
     'setup newch2')

p.write_text(s,encoding='utf-8')
print('v3.76 new chapter2 patch applied')
