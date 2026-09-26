from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n < count:
        raise SystemExit(f'replace mismatch expected >= {count}, found {n}: {old[:180]!r}')
    s=s.replace(old,new,count)

def sub(pattern,repl,count=1,flags=0):
    global s
    s2,n=re.subn(pattern,repl,s,count=count,flags=flags)
    if n != count:
        raise SystemExit(f'regex mismatch expected {count}, found {n}: {pattern[:180]!r}')
    s=s2

# ------------------------------------------------------------
# v3.38 visible version + notes
# ------------------------------------------------------------
rep('BATTLE <b>v3.37</b>','BATTLE <b>v3.38</b>')
rep('📒 패치노트 · v3.37','📒 패치노트 · v3.38')
old='<div class="patch-body"><div class="patch-version"><h3>v3.37 · 화염을 가르는 소방대, 더 빨라진 해골 군단</h3>'
new='''<div class="patch-body"><div class="patch-version"><h3>v3.38 · 피의 저택, 좀비 반란의 밤</h3><ul><li>소방관: 소방차 호출 주기 15초 → 10초.</li><li>밸런스: 일반 독 지속시간 10초 → 3초. 맹독은 기존 규칙 유지.</li><li>버그 수정: 알라딘의 지니가 적을 벽에 몰아붙인 채 계속 압박하던 이동 AI를 개선. 벽 근처에서는 중앙 복귀와 측면 이동을 우선.</li><li>CHAPTER 3 추가: CHAPTER 2의 STAGE 1·2·3을 모두 클리어하면 흡혈귀의 저택에 입장 가능.</li><li>CHAPTER 3 STAGE 1: 🧛 흡혈귀 + 🧛‍♀️ 여자 뱀파이어가 🧟‍♂️ 좀비 5마리씩 5웨이브를 방어. 좀비 HP 75, 근접 50, 적중 시 독 70% / 맹독 30%.</li><li>CHAPTER 3 STAGE 2: HP 1500의 👑🧟‍♂️ 왕좀비 등장. 근접 피해 100, 3초마다 일반 좀비 1마리 소환.</li><li>CHAPTER 3 STAGE 3: 🧌 법사좀비 등장. HP 2000, 이동속도 30% 감소, 크기 1.5배. 2초마다 피해 85 유도탄을 발사하며 명중 시 HP 10의 미니좀비를 소환.</li><li>여자 뱀파이어: STAGE 1·2에서 HP 500으로 흡혈귀를 돕고, STAGE 3에는 등장하지 않음. 능력은 흡혈귀와 동일.</li><li>CHAPTER 3 STAGE 3 클리어 시 매번 10% 확률로 🧌 법사좀비 캐릭터 획득.</li></ul></div><div class="patch-version"><h3>v3.37 · 화염을 가르는 소방대, 더 빨라진 해골 군단</h3>'''
rep(old,new)

# ------------------------------------------------------------
# Balance: firefighter and poison
# ------------------------------------------------------------
rep("15초마다 HP 500의 🚒 소방차를 타고 10초 동안 물을 뿌려.","10초마다 HP 500의 🚒 소방차를 타고 10초 동안 물을 뿌려.")
rep("🚒 15초마다 탑승","🚒 10초마다 탑승")
rep("f.firetruckNext=this.time+15/f.scale","f.firetruckNext=this.time+10/f.scale",2)
rep("old.expires=this.time+10*f.scale","old.expires=this.time+3*f.scale")
rep("expires:this.time+10*f.scale","expires:this.time+3*f.scale")

# ------------------------------------------------------------
# Genie anti-wall / spacing AI
# ------------------------------------------------------------
old="if(g.stunUntil<=this.time){const target=this.nearest(g);if(target){const mv=this.aim(g,target);g.vx=mv.x;g.vy=mv.y;g.x+=mv.x*g.speed*dt;g.y+=mv.y*g.speed*dt;this.keepInside(g)}}"
new="if(g.stunUntil<=this.time){const target=this.nearest(g);if(target){const mv=this.aim(g,target),d=distance(g,target),edge=g.x<115||g.x>605||g.y<115||g.y>605;let x=mv.x,y=mv.y;if(edge){const cx=360-g.x,cy=360-g.y,cn=Math.hypot(cx,cy)||1;x=cx/cn-mv.y*.35;y=cy/cn+mv.x*.35}else if(d<150*g.scale){x=-mv.x-mv.y*.45;y=-mv.y+mv.x*.45}else if(d<270*g.scale){x=-mv.y;y=mv.x}const n=Math.hypot(x,y)||1;g.vx=x/n;g.vy=y/n;g.x+=g.vx*g.speed*dt;g.y+=g.vy*g.speed*dt;this.keepInside(g)}}"
rep(old,new)

# ------------------------------------------------------------
# Zombie roster entries + mage as unlockable character
# ------------------------------------------------------------
anchor="{id:'skeleton_mage',name:'해골 법사'"
zombies="""{id:'zombie',name:'좀비',icon:'🧟‍♂️',tag:'근접 · 독/맹독',hp:75,damage:50,speed:135,cooldown:1,stageOnly:true,description:'CHAPTER 3의 일반 좀비. 근접 피해 50을 주며 적중 시 70% 확률로 독, 30% 확률로 맹독을 건다.',detail:'HP 75 · 근접 50 / 1초 · 독 70% · 맹독 30%'},
{id:'king_zombie',name:'왕좀비',icon:'👑🧟‍♂️',tag:'왕좀비 · 3초 소환',hp:1500,damage:100,speed:120,cooldown:1,stageOnly:true,description:'CHAPTER 3 STAGE 2의 왕좀비. 근접 피해 100을 주며 3초마다 일반 좀비 1마리를 소환한다.',detail:'HP 1500 · 근접 100 / 1초 · 3초마다 일반 좀비 1마리 소환'},
{id:'zombie_mage',name:'법사좀비',icon:'🧌',tag:'유도탄 · 미니좀비 소환',hp:2000,damage:85,speed:105,cooldown:2,unlock:'zombieMage',description:'이동속도가 느리고 몸집이 큰 법사좀비. 2초마다 피해 85의 유도탄을 발사하며 적중 시 HP 10의 미니좀비를 소환한다.',detail:'HP 2000 · 이동속도 -30% · 크기 1.5배 · 유도탄 85 / 2초 · 명중 시 HP 10 미니좀비 · 미니좀비 피해 5~20'},
"""
rep(anchor,zombies+anchor)

# Mage zombie is intrinsically 1.5x body size; normal boss scaling still stacks.
rep("*(type.id==='moai'?1.5:1),team=this.mode", "*(type.id==='moai'?1.5:1)*(type.id==='zombie_mage'?1.5:1),team=this.mode")

# ------------------------------------------------------------
# Zombie engine skills / summons
# ------------------------------------------------------------
anchor="firefighterSkill(f,e){\n"
methods="""spawnZombieMinion(owner,id='zombie',near=null,mini=false){
 if(!owner)return null;
 const base=near||owner,tmp=new Engine('vampire',id,this.random,{mode:'control'}).fighters[1],a=this.rand(-Math.PI,Math.PI);
 tmp.side=this.fighters.length;tmp.team=owner.team;tmp.summon=true;tmp.ownerSide=owner.side;tmp.boss=false;tmp.scale=1;tmp.bodyScale=mini?.5:1;tmp.radius=33*tmp.bodyScale;
 tmp.x=clamp(base.x+this.rand(-55,55),55,665);tmp.y=clamp(base.y+this.rand(-55,55),55,665);tmp.vx=Math.cos(a);tmp.vy=Math.sin(a);tmp.trail=[];tmp.deathOrder=null;tmp.poison=null;tmp.toxin=null;tmp.burn=null;tmp.curse=null;tmp.stunUntil=0;tmp.capturedBy=null;tmp.captureTarget=null;
 if(mini){tmp.id='zombie_mini';tmp.name='미니좀비';tmp.icon='🧟';tmp.hp=10;tmp.health=10;tmp.damage=5;tmp.speed=130;tmp.cooldown=1;tmp.bodyScale=.5;tmp.radius=16.5}
 this.fighters.push(tmp);return tmp
}
zombieSkill(f,e){
 if(!['zombie','king_zombie','zombie_mini','zombie_mage'].includes(f.id)||f.health<=0||f.stunUntil>this.time)return;
 if(f.id==='zombie_mage'){
  if(f.cd<=1e-9&&e&&e.health>0){const a=this.aim(f,e);this.shots.push({x:f.x+a.x*(f.radius+8),y:f.y+a.y*(f.radius+8),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'zombiemagic',radius:8*f.scale,speed:215*f.scale,damage:85*f.scale,life:5*f.scale,bounces:0});f.cd=2/f.scale;f.attack=.2/f.scale;this.effect(f,'🧌 85 유도탄!','skill')}
  return
 }
 if(f.id==='king_zombie'){if(!Number.isFinite(f.zombieSummonNext))f.zombieSummonNext=this.time+3/f.scale;if(this.time>=f.zombieSummonNext-1e-9){f.zombieSummonNext=this.time+3/f.scale;const z=this.spawnZombieMinion(f,'zombie',f,false);if(z){this.effect(f,'🧟‍♂️ 좀비 소환!','skill');this.emit('👑🧟‍♂️ 왕좀비가 일반 좀비를 소환!')}}}
 if(!e||e.health<=0||f.cd>1e-9||distance(f,e)>f.radius+e.radius+35*f.scale)return;
 const dmg=f.id==='zombie_mini'?Math.floor(this.rand(5,21)):f.id==='king_zombie'?100:50,dealt=this.attack(f,e,dmg*f.scale);f.cd=1/f.scale;
 if(dealt>0&&f.id==='zombie'&&e.health>0){if(this.random()<.7)this.applyPoison(f,e);else this.applyToxin(f,e)}
}
"""
rep(anchor,methods+anchor)

# Run zombie skills and keep them out of generic body melee.
rep("if(f.id==='firefighter')this.firefighterSkill(f,e);if(f.id.startsWith('skeleton_'))this.skeletonSkill(f,e);", "if(f.id==='firefighter')this.firefighterSkill(f,e);if(['zombie','king_zombie','zombie_mini','zombie_mage'].includes(f.id))this.zombieSkill(f,e);if(f.id.startsWith('skeleton_'))this.skeletonSkill(f,e);")
rep("'firefighter','skeleton_gun'", "'firefighter','zombie','king_zombie','zombie_mini','zombie_mage','skeleton_gun'")

# Zombie mage homing projectile and mini-zombie-on-hit.
rep("(s.kind==='magic'||s.kind==='curseorb')", "(s.kind==='magic'||s.kind==='curseorb'||s.kind==='zombiemagic')")
old="if(s.kind==='magic'){e.slow=Math.max(e.slow,1.2*f.scale);e.slowPower=Math.max(e.slowPower,f.magicSlowStrength)}}"
new="if(s.kind==='magic'){e.slow=Math.max(e.slow,1.2*f.scale);e.slowPower=Math.max(e.slowPower,f.magicSlowStrength)}if(s.kind==='zombiemagic'&&e.health>0){const z=this.spawnZombieMinion(f,'zombie',e,true);if(z){this.effect(z,'🧟 미니좀비!','skill');this.emit('🧌 유도탄 적중 · 미니좀비 소환!')}}}"
rep(old,new)

# Female vampire keeps her visual identity after bat form ends.
old="else if(!low&&f.vampireBat){f.vampireBat=false;f.icon='🧛';f.name='흡혈귀';f.speed/=2;this.effect(f,'흡혈귀 복귀','skill')}"
new="else if(!low&&f.vampireBat){f.vampireBat=false;f.icon=f.femaleVampire?'🧛‍♀️':'🧛';f.name=f.femaleVampire?'여자 뱀파이어':'흡혈귀';f.speed/=2;this.effect(f,'흡혈귀 복귀','skill')}"
rep(old,new)

# ------------------------------------------------------------
# Chapter 3 selection UI
# ------------------------------------------------------------
old='<button id="boss-control-entry" class="stage-entry boss-control-entry" type="button" disabled>🔒 조정 보스전 · STAGE 2 클리어 시 해금</button><button id="chapter2-entry" class="stage-entry" type="button" disabled>🔒 CHAPTER 2 · 로봇 스테이지 1·2·3 클리어 필요</button>'
new=old+'<button id="chapter3-entry" class="stage-entry" type="button" disabled>🔒 CHAPTER 3 · CHAPTER 2 STAGE 1·2·3 클리어 필요</button>'
rep(old,new)
old='<div id="desert-panel" class="stage-panel" hidden><p class="eyebrow">CHAPTER 2 · DESERT</p><h2>🤠 카우보이와 해골 바이러스</h2><p>평범한 서부 사람들이 미지의 바이러스로 💀 해골이 됐어. 카우보이를 직접 조작해 사막을 돌파해.</p><div class="stage-grid"><button class="stage-card" id="desert-1" type="button"><b>STAGE 1</b><span>🤠 VS 💀💀💀</span><strong>사막의 첫 습격</strong><small>해골 3마리씩 총 5웨이브를 격파.</small></button><button class="stage-card" id="desert-2" type="button"><b>STAGE 2</b><span>🤠 VS 💀💀💀</span><strong>바이러스 마을</strong><small>총잡이·칼잡이·취한 해골이 섞인 5웨이브.</small></button><button class="stage-card" id="desert-3" type="button"><b>STAGE 3</b><span>🤠 VS 💀🧙</span><strong>해골 법사</strong><small>추적 마법탄과 10초마다 소환되는 해골을 돌파.</small></button></div></div>'
new=old+'''<div id="mansion-panel" class="stage-panel" hidden><p class="eyebrow">CHAPTER 3 · BLOOD MANSION</p><h2>🧛 피의 저택과 좀비 반란</h2><p>흡혈귀가 사는 저택을 차지하려는 좀비 군단이 침략했어. 흡혈귀를 직접 조작해 저택을 지켜.</p><div class="stage-grid"><button class="stage-card" id="mansion-1" type="button"><b>STAGE 1</b><span>🧛🧛‍♀️ VS 🧟‍♂️×5</span><strong>반란의 첫 밤</strong><small>좀비 5마리씩 총 5웨이브. 여자 뱀파이어가 함께 싸워.</small></button><button class="stage-card" id="mansion-2" type="button"><b>STAGE 2</b><span>🧛🧛‍♀️ VS 👑🧟‍♂️</span><strong>왕좀비의 포위</strong><small>HP 1500 왕좀비가 3초마다 일반 좀비를 소환해.</small></button><button class="stage-card" id="mansion-3" type="button"><b>STAGE 3</b><span>🧛 VS 🧌</span><strong>법사좀비의 저주</strong><small>HP 2000 법사좀비의 유도탄과 미니좀비 소환을 돌파.</small></button></div></div>'''
rep(old,new)

# ------------------------------------------------------------
# Chapter 3 progress + rare unlock persistence
# ------------------------------------------------------------
old="const ROBOT_STAGE_KEY='neonRumble.robotStages.v1',SKELETON_UNLOCK_KEY='neonRumble.skeletonBundleUnlocked.v2',SKELETON_MAGE_UNLOCK_KEY='neonRumble.skeletonMageUnlocked.v1',LEGACY_SKELETON_UNLOCK_KEY='neonRumble.skeletonUnlocked.v1';\nlet robotStageMask=0,skeletonsUnlocked=false,skeletonMageUnlocked=false;try{localStorage.removeItem(LEGACY_SKELETON_UNLOCK_KEY);robotStageMask=Number(localStorage.getItem(ROBOT_STAGE_KEY)||0)||0;skeletonsUnlocked=localStorage.getItem(SKELETON_UNLOCK_KEY)==='1';skeletonMageUnlocked=localStorage.getItem(SKELETON_MAGE_UNLOCK_KEY)==='1'}catch{}"
new="const ROBOT_STAGE_KEY='neonRumble.robotStages.v1',SKELETON_UNLOCK_KEY='neonRumble.skeletonBundleUnlocked.v2',SKELETON_MAGE_UNLOCK_KEY='neonRumble.skeletonMageUnlocked.v1',DESERT_STAGE_KEY='neonRumble.desertStages.v1',ZOMBIE_MAGE_UNLOCK_KEY='neonRumble.zombieMageUnlocked.v1',LEGACY_SKELETON_UNLOCK_KEY='neonRumble.skeletonUnlocked.v1';\nlet robotStageMask=0,desertStageMask=0,skeletonsUnlocked=false,skeletonMageUnlocked=false,zombieMageUnlocked=false;try{localStorage.removeItem(LEGACY_SKELETON_UNLOCK_KEY);robotStageMask=Number(localStorage.getItem(ROBOT_STAGE_KEY)||0)||0;desertStageMask=Number(localStorage.getItem(DESERT_STAGE_KEY)||0)||0;skeletonsUnlocked=localStorage.getItem(SKELETON_UNLOCK_KEY)==='1';skeletonMageUnlocked=localStorage.getItem(SKELETON_MAGE_UNLOCK_KEY)==='1';zombieMageUnlocked=localStorage.getItem(ZOMBIE_MAGE_UNLOCK_KEY)==='1'}catch{}"
rep(old,new)
rep("function chapter2Unlocked(){return (robotStageMask&7)===7}","function chapter2Unlocked(){return (robotStageMask&7)===7}\nfunction chapter3Unlocked(){return (desertStageMask&7)===7}\nfunction markDesertStage(n){const before=chapter3Unlocked();desertStageMask|=(1<<(n-1));try{localStorage.setItem(DESERT_STAGE_KEY,String(desertStageMask))}catch{}updateChapter3UI();return !before&&chapter3Unlocked()}")
rep("function characterLocked(c){return !!c?.stageOnly||(c?.unlock==='skeleton'&&!skeletonsUnlocked)||(c?.unlock==='skeletonMage'&&!skeletonMageUnlocked)}", "function characterLocked(c){return !!c?.stageOnly||(c?.unlock==='skeleton'&&!skeletonsUnlocked)||(c?.unlock==='skeletonMage'&&!skeletonMageUnlocked)||(c?.unlock==='zombieMage'&&!zombieMageUnlocked)}")
rep("function updateChapter2UI(){const b=$('chapter2-entry');if(!b)return;const ok=chapter2Unlocked();b.disabled=!ok;b.textContent=ok?'🏜️ CHAPTER 2 · 카우보이와 해골':'🔒 CHAPTER 2 · 로봇 스테이지 1·2·3 클리어 필요'}", "function tryUnlockZombieMage(){if(zombieMageUnlocked)return 'already';if(Math.random()>=.1)return 'miss';zombieMageUnlocked=true;try{localStorage.setItem(ZOMBIE_MAGE_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return 'won'}\nfunction updateChapter2UI(){const b=$('chapter2-entry');if(!b)return;const ok=chapter2Unlocked();b.disabled=!ok;b.textContent=ok?'🏜️ CHAPTER 2 · 카우보이와 해골':'🔒 CHAPTER 2 · 로봇 스테이지 1·2·3 클리어 필요'}\nfunction updateChapter3UI(){const b=$('chapter3-entry');if(!b)return;const ok=chapter3Unlocked();b.disabled=!ok;b.textContent=ok?'🏰 CHAPTER 3 · 피의 저택과 좀비 반란':'🔒 CHAPTER 3 · CHAPTER 2 STAGE 1·2·3 클리어 필요'}")

# Manual control includes mansion.
rep("return ['control','stage','boss-control','desert'].includes(mode)","return ['control','stage','boss-control','desert','mansion'].includes(mode)")
rep("controlLabel.textContent=mode==='boss-control'?'보스 이동 · '+controlName():mode==='stage'?'로봇 이동 · '+controlName():'왼쪽 캐릭터 이동 · '+controlName()", "controlLabel.textContent=mode==='boss-control'?'보스 이동 · '+controlName():mode==='stage'?'로봇 이동 · '+controlName():mode==='mansion'?'흡혈귀 이동 · '+controlName():'왼쪽 캐릭터 이동 · '+controlName()")

# Stage-selection UI supports mansion selector.
sub(r"function updateStageUI\(\)\{.*?updateChapter2UI\(\)\}", """function updateStageUI(){const on=mode==='stage',desertSelect=mode==='desert-select',mansionSelect=mode==='mansion-select',special=on||desertSelect||mansionSelect;document.querySelector('.section-title').hidden=special;document.querySelector('.versus').hidden=special;$('start').hidden=special;document.querySelector('.pick-heading').hidden=special;$('character-search').hidden=special;$('roster').hidden=special;document.querySelector('.match-info').hidden=special;$('stage-entry').hidden=special;$('boss-control-entry').hidden=special;$('chapter2-entry').hidden=special;$('chapter3-entry').hidden=special;$('stage-panel').hidden=!on;$('desert-panel').hidden=!desertSelect;$('mansion-panel').hidden=!mansionSelect;if(special){$('relay-rules').hidden=true;$('relay-picker').hidden=true;$('squad-picker').hidden=true;$('boss-rules').hidden=true}$('mode-duel').setAttribute('aria-pressed',String(mode==='duel'));$('mode-boss').setAttribute('aria-pressed',String(isBossMode()));$('mode-relay').setAttribute('aria-pressed',String(mode==='relay'));$('mode-group').setAttribute('aria-pressed',String(mode==='group'));$('mode-control').setAttribute('aria-pressed',String(mode==='control'));updateControlBossUnlockUI();updateChapter2UI();updateChapter3UI()}""",flags=re.S)
rep("const stageWas=mode==='stage'||mode==='desert-select';", "const stageWas=mode==='stage'||mode==='desert-select'||mode==='mansion-select';")
rep("$('chapter2-entry').hidden=false}","$('chapter2-entry').hidden=false;$('chapter3-entry').hidden=false}")

# Regular mode switches clear both chapter transient states.
rep("function switchRegularMode(next){if(mode==='desert'||mode==='desert-select')resetDesertTransient();engine=null;mode=next;updateSelection()}", "function switchRegularMode(next){if(mode==='desert'||mode==='desert-select')resetDesertTransient();if(mode==='mansion'||mode==='mansion-select')resetMansionTransient();engine=null;mode=next;updateSelection()}")
rep("$('chapter2-entry').onclick=()=>{if(!chapter2Unlocked())return;mode='desert-select';updateSelection();window.scrollTo({top:0,behavior:'auto'})};", "$('chapter2-entry').onclick=()=>{if(!chapter2Unlocked())return;if(mode==='mansion'||mode==='mansion-select')resetMansionTransient();mode='desert-select';updateSelection();window.scrollTo({top:0,behavior:'auto'})};\n$('chapter3-entry').onclick=()=>{if(!chapter3Unlocked())return;if(mode==='desert'||mode==='desert-select')resetDesertTransient();mode='mansion-select';updateSelection();window.scrollTo({top:0,behavior:'auto'})};")
rep("$('desert-3').onclick=()=>startDesertStage(3);", "$('desert-3').onclick=()=>startDesertStage(3);$('mansion-1').onclick=()=>startMansionStage(1);$('mansion-2').onclick=()=>startMansionStage(2);$('mansion-3').onclick=()=>startMansionStage(3);")

# ------------------------------------------------------------
# CHAPTER 3 runtime controller
# ------------------------------------------------------------
anchor="function start(){if(mode==='desert'||mode==='desert-select'){resetDesertTransient();mode='duel'}"
mansion="""let mansionStageNo=1,mansionWave=0;
function resetMansionTransient(){mansionStageNo=1;mansionWave=0;if(engine)engine.desertWaveMode=false}
function makeMansionEnemy(id,x,y){const tmp=new Engine('vampire',id,Math.random,{mode:'control'}).fighters[1];tmp.side=engine.fighters.length;tmp.team=1;tmp.x=x;tmp.y=y;tmp.summon=true;tmp.ownerSide=1;tmp.trail=[];tmp.poison=null;tmp.toxin=null;tmp.burn=null;tmp.curse=null;tmp.deathOrder=null;engine.fighters.push(tmp);return tmp}
function spawnFemaleVampire(){const hero=engine.fighters.find(f=>f.team===0&&!f.summon),v={...hero};v.side=engine.fighters.length;v.team=0;v.summon=true;v.ownerSide=hero.side;v.femaleVampire=true;v.icon='🧛‍♀️';v.name='여자 뱀파이어';v.hp=500;v.health=500;v.boss=false;v.scale=1;v.bodyScale=1;v.radius=33;v.x=150;v.y=500;v.vx=0;v.vy=-1;v.poison=null;v.toxin=null;v.burn=null;v.curse=null;v.trail=[];v.deathOrder=null;v.vampireBat=false;engine.fighters.push(v);return v}
function spawnMansionWave(){mansionWave++;const spots=[[500,120],[610,235],[625,410],[535,570],[440,360]];for(const [x,y] of spots)makeMansionEnemy('zombie',x,y);$('event').textContent='🏰 WAVE '+mansionWave+' / 5 · 좀비 5마리 침입!'}
function startMansionStage(n){mansionStageNo=n;mode='mansion';mansionWave=0;if(n===1){engine=new Engine('vampire','zombie',Math.random,{mode:'control'});engine.fighters[1].health=0;spawnFemaleVampire();spawnMansionWave()}else if(n===2){engine=new Engine('vampire','king_zombie',Math.random,{mode:'control'});spawnFemaleVampire()}else{engine=new Engine('vampire','zombie_mage',Math.random,{mode:'control'});const m=engine.fighters[1];m.hp=2000;m.health=2000;m.bodyScale=1.5;m.radius=49.5;m.speed=105}engine.desertWaveMode=true;paused=false;acc=0;last=performance.now();lastHits=0;lastMessage='';$('selection').hidden=true;$('battle').hidden=false;$('result').hidden=true;$('pause-label').hidden=true;$('pause').disabled=false;$('pause').textContent='일시정지';resetStick();refreshControlUI();$('squad-hud').hidden=true;$('relay-hud').hidden=true;$('score-label0').textContent=n<3?'🧛 흡혈귀 + 🧛‍♀️':'🧛 흡혈귀';$('score-label1').textContent=n===1?'🧟‍♂️ 좀비 웨이브':n===2?'👑🧟‍♂️ 왕좀비':'🧌 법사좀비';$('battle-mode').textContent='MANSION '+n;$('battle-info').textContent=n===1?'CHAPTER 3 STAGE 1 · 좀비 5마리씩 총 5웨이브. 여자 뱀파이어 HP 500 지원.':n===2?'CHAPTER 3 STAGE 2 · 왕좀비 HP 1500 · 3초마다 좀비 소환 · 여자 뱀파이어 지원.':'CHAPTER 3 STAGE 3 · 법사좀비 HP 2000 · 2초마다 유도탄 85 · 명중 시 미니좀비 소환.';fit();hud();draw();window.scrollTo({top:0,behavior:'auto'});playSfx('start')}
function updateMansionStage(){if(mode!=='mansion'||!engine||engine.result!==null)return;const hero=engine.fighters.find(f=>f.team===0&&!f.summon);if(!hero||hero.health<=0){engine.result=1;return}if(mansionStageNo===1){const alive=engine.fighters.some(f=>f.team===1&&f.health>0);if(!alive){if(mansionWave>=5)engine.result=0;else spawnMansionWave()}}else if(mansionStageNo===2){const king=engine.fighters.find(f=>f.id==='king_zombie'&&f.team===1&&!f.summon);if(!king||king.health<=0)engine.result=0}else{const mage=engine.fighters.find(f=>f.id==='zombie_mage'&&f.team===1&&!f.summon);if(!mage||mage.health<=0)engine.result=0}}
"""
rep(anchor,mansion+"function start(){if(mode==='desert'||mode==='desert-select'){resetDesertTransient();mode='duel'}if(mode==='mansion'||mode==='mansion-select'){resetMansionTransient();mode='duel'}")

# Selection/rematch understand mansion.
rep("function selection(){if(mode==='desert'||mode==='desert-select'){resetDesertTransient();mode='duel'}", "function selection(){if(mode==='desert'||mode==='desert-select'){resetDesertTransient();mode='duel'}if(mode==='mansion'||mode==='mansion-select'){resetMansionTransient();mode='duel'}")
rep("mode==='desert'?startDesertStage(desertStageNo):start()", "mode==='desert'?startDesertStage(desertStageNo):mode==='mansion'?startMansionStage(mansionStageNo):start()")

# Record all Chapter 2 clears, and Chapter 3 results / 10% unlock.
old="else if(mode==='desert'&&engine.result===0){const skNow=desertStageNo===3?unlockSkeletons():false,mageRoll=desertStageNo===3?tryUnlockSkeletonMage():null;$('winner-icon').textContent='🏜️';$('winner').textContent='CHAPTER 2 · STAGE '+desertStageNo+' 클리어!';$('summary').textContent=t+'초 · 사막 돌파 성공'+(skNow?' · 💀 해골들 캐릭터 해금!':'')+(mageRoll==='won'?' · 🎁 10% 보상 성공! 💀🧙 해골 법사 획득!':mageRoll==='miss'?' · 🎲 해골 법사 획득 실패 (10%)':'')}else if(mode==='desert'){$('winner-icon').textContent='💀';$('winner').textContent='CHAPTER 2 · STAGE '+desertStageNo+' 실패';$('summary').textContent=t+'초 · 카우보이가 쓰러졌어. 다시 도전해 봐.'}"
new="else if(mode==='desert'&&engine.result===0){const chapter3Now=markDesertStage(desertStageNo),skNow=desertStageNo===3?unlockSkeletons():false,mageRoll=desertStageNo===3?tryUnlockSkeletonMage():null;$('winner-icon').textContent='🏜️';$('winner').textContent='CHAPTER 2 · STAGE '+desertStageNo+' 클리어!';$('summary').textContent=t+'초 · 사막 돌파 성공'+(skNow?' · 💀 해골들 캐릭터 해금!':'')+(mageRoll==='won'?' · 🎁 10% 보상 성공! 💀🧙 해골 법사 획득!':mageRoll==='miss'?' · 🎲 해골 법사 획득 실패 (10%)':'')+(chapter3Now?' · 🏰 CHAPTER 3 해금!':'')}else if(mode==='desert'){$('winner-icon').textContent='💀';$('winner').textContent='CHAPTER 2 · STAGE '+desertStageNo+' 실패';$('summary').textContent=t+'초 · 카우보이가 쓰러졌어. 다시 도전해 봐.'}else if(mode==='mansion'&&engine.result===0){const zRoll=mansionStageNo===3?tryUnlockZombieMage():null;$('winner-icon').textContent='🏰';$('winner').textContent='CHAPTER 3 · STAGE '+mansionStageNo+' 클리어!';$('summary').textContent=t+'초 · 피의 저택 방어 성공'+(zRoll==='won'?' · 🎁 10% 보상 성공! 🧌 법사좀비 획득!':zRoll==='miss'?' · 🎲 법사좀비 획득 실패 (10%)':'')}else if(mode==='mansion'){$('winner-icon').textContent='🧟‍♂️';$('winner').textContent='CHAPTER 3 · STAGE '+mansionStageNo+' 실패';$('summary').textContent=t+'초 · 흡혈귀가 쓰러졌어. 저택을 다시 지켜 봐.'}"
rep(old,new)

# ------------------------------------------------------------
# Mansion draw + loop update + initial UI
# ------------------------------------------------------------
old="if(mode==='desert'){const dg=ctx.createLinearGradient(0,0,0,720);dg.addColorStop(0,'#e8b85f');dg.addColorStop(.55,'#cf9447');dg.addColorStop(1,'#b97838');ctx.fillStyle=dg;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.22;ctx.fillStyle='#fff0b3';ctx.beginPath();ctx.arc(585,115,62,0,Math.PI*2);ctx.fill();ctx.globalAlpha=.35;ctx.font='42px sans-serif';ctx.fillText('🌵',90,180);ctx.fillText('🌵',640,590);ctx.globalAlpha=1}else{ctx.fillStyle='#101c2d';ctx.fillRect(0,0,720,720)}"
new="if(mode==='desert'){const dg=ctx.createLinearGradient(0,0,0,720);dg.addColorStop(0,'#e8b85f');dg.addColorStop(.55,'#cf9447');dg.addColorStop(1,'#b97838');ctx.fillStyle=dg;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.22;ctx.fillStyle='#fff0b3';ctx.beginPath();ctx.arc(585,115,62,0,Math.PI*2);ctx.fill();ctx.globalAlpha=.35;ctx.font='42px sans-serif';ctx.fillText('🌵',90,180);ctx.fillText('🌵',640,590);ctx.globalAlpha=1}else if(mode==='mansion'){const mg=ctx.createLinearGradient(0,0,0,720);mg.addColorStop(0,'#241327');mg.addColorStop(.55,'#130d1b');mg.addColorStop(1,'#090811');ctx.fillStyle=mg;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.16;ctx.fillStyle='#b8264c';ctx.beginPath();ctx.arc(585,105,58,0,Math.PI*2);ctx.fill();ctx.globalAlpha=.28;ctx.font='46px sans-serif';ctx.fillText('🕯️',92,170);ctx.fillText('🕸️',625,160);ctx.fillText('🪦',625,595);ctx.globalAlpha=1}else{ctx.fillStyle='#101c2d';ctx.fillRect(0,0,720,720)}"
rep(old,new)
rep("ctx.strokeStyle=mode==='desert'?'#b87a3c':'#1c2d42'", "ctx.strokeStyle=mode==='desert'?'#b87a3c':mode==='mansion'?'#54243f':'#1c2d42'")
rep("ctx.fillText(mode==='desert'?'DESERT · STAGE '+desertStageNo:mode==='stage'?", "ctx.fillText(mode==='desert'?'DESERT · STAGE '+desertStageNo:mode==='mansion'?'BLOOD MANSION · STAGE '+mansionStageNo:mode==='stage'?")
rep("updateDesertStage();hud()", "updateDesertStage();updateMansionStage();hud()")
rep("applySettingsUI();updateControlBossUnlockUI();updateChapter2UI();updateSelection();", "applySettingsUI();updateControlBossUnlockUI();updateChapter2UI();updateChapter3UI();updateSelection();")

# Water/magic projectile visuals: zombie magic gets a distinct orb.
rep("else if(s.kind==='curseorb'){", "else if(s.kind==='zombiemagic'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(27*s.radius/8)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🟣',0,0)}else if(s.kind==='curseorb'){")

p.write_text(s,encoding='utf-8')
print('v3.38 Chapter 3 patch applied')
