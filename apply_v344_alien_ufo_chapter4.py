from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n < count:
        raise SystemExit(f'replace mismatch expected >= {count}, found {n}: {old[:220]!r}')
    s=s.replace(old,new,count)

def sub(pattern,repl,count=1,flags=0):
    global s
    s2,n=re.subn(pattern,repl,s,count=count,flags=flags)
    if n!=count:
        raise SystemExit(f'regex mismatch expected {count}, found {n}: {pattern[:220]!r}')
    s=s2

# ---------------- visible release + patch notes ----------------
rep('BATTLE <b>v3.43</b>','BATTLE <b>v3.44</b>')
rep('<summary>📒 패치노트 · v3.43</summary><div class="patch-body">',
    '<summary>📒 패치노트 · v3.44</summary><div class="patch-body"><div class="patch-version"><h3>v3.44 · UFO 납치와 CHAPTER 4</h3><ul><li>👽 외계인: 10초마다 HP 300의 🛸 UFO에 탑승. UFO는 랜덤한 적 1명을 빨아들여 5초 동안 🐄 소로 만들며, 소 상태에서는 이동만 가능.</li><li>🛸 탑승 중 일반 공격은 외계인의 기존 무한 반사 레이저와 동일. UFO HP가 0이 되면 외계인으로 복귀하고 10초 뒤 다시 탑승.</li><li>CHAPTER 4 추가: CHAPTER 3의 STAGE 1·2·3을 모두 클리어하면 해금. 주인공은 👽 외계인.</li><li>STAGE 1·2: 👾 외계생물 3마리씩 5웨이브. HP 100, 2초마다 무한 반사 레이저, 피해는 50으로 고정. 웨이브 통과 시 외계인이 최대 HP의 30% 회복.</li><li>STAGE 3: 🛸👾 감염 UFO 등장. 10초마다 두꺼운 파멸의 레이저를 예고 후 발사하며 맵을 관통하고 피해 350. 클리어 시 5% 확률로 감염 UFO 획득.</li></ul></div>')

# ---------------- selection HTML: Chapter 4 ----------------
rep('<button id="boss-control-entry" class="stage-entry boss-control-entry" type="button" disabled>🔒 조정 보스전 · STAGE 2 클리어 시 해금</button><button id="chapter2-entry" class="stage-entry" type="button" disabled>🔒 CHAPTER 2 · 로봇 스테이지 1·2·3 클리어 필요</button><button id="chapter3-entry" class="stage-entry" type="button" disabled>🔒 CHAPTER 3 · CHAPTER 2 STAGE 1·2·3 클리어 필요</button>',
    '<button id="boss-control-entry" class="stage-entry boss-control-entry" type="button" disabled>🔒 조정 보스전 · STAGE 2 클리어 시 해금</button><button id="chapter2-entry" class="stage-entry" type="button" disabled>🔒 CHAPTER 2 · 로봇 스테이지 1·2·3 클리어 필요</button><button id="chapter3-entry" class="stage-entry" type="button" disabled>🔒 CHAPTER 3 · CHAPTER 2 STAGE 1·2·3 클리어 필요</button><button id="chapter4-entry" class="stage-entry" type="button" disabled>🔒 CHAPTER 4 · CHAPTER 3 STAGE 1·2·3 클리어 필요</button>')
rep('</div></div><p class="hint">일반 모드는 직접 조작 없는 자동 전투',
    '</div></div><div id="space-panel" class="stage-panel" hidden><p class="eyebrow">CHAPTER 4 · ALIEN INVASION</p><h2>👽 외계인의 역습</h2><p>외계 생물과 감염된 UFO가 전장을 침공했어. 외계인을 직접 조작해 침공을 막아.</p><div class="stage-grid"><button class="stage-card" id="space-1" type="button"><b>STAGE 1</b><span>👽 VS 👾👾👾</span><strong>첫 번째 침공</strong><small>HP 100 외계생물 3마리씩 총 5웨이브. 웨이브마다 최대 HP 30% 회복.</small></button><button class="stage-card" id="space-2" type="button"><b>STAGE 2</b><span>👽 VS 👾👾👾</span><strong>증식하는 외계생물</strong><small>외계생물 3마리씩 총 5웨이브. 레이저 피해는 50으로 고정.</small></button><button class="stage-card" id="space-3" type="button"><b>STAGE 3</b><span>👽 VS 🛸👾</span><strong>감염 UFO</strong><small>10초마다 예고 후 발사되는 두꺼운 파멸의 레이저를 피하고 감염 UFO를 격파.</small></button></div></div><p class="hint">일반 모드는 직접 조작 없는 자동 전투')

# ---------------- roster additions ----------------
alien_line="{id:'alien',name:'외계인',icon:'👽',tag:'무한 반사 레이저',hp:1000,damage:50,speed:150,cooldown:2,description:'2초마다 레이저를 발사해. 레이저는 상대에게 닿을 때까지 벽을 횟수 제한 없이 계속 튕기며, 명중 피해는 50~70 중 무작위야.',detail:'HP 1000 · 👽 레이저 2초마다 발사 · 피해 50~70 랜덤 · 적중 전까지 벽 무한 반사'},"
new_roster=alien_line+"\n{id:'alien_creature',name:'외계생물',icon:'👾',tag:'고정 피해 반사 레이저',hp:100,damage:50,speed:145,cooldown:2,stageOnly:true,description:'CHAPTER 4의 외계생물. 2초마다 피해 50으로 고정된 무한 반사 레이저를 발사해.',detail:'HP 100 · 레이저 50 / 2초 · 적중 전까지 벽 무한 반사'},\n{id:'infected_ufo',name:'감염 UFO',icon:'🛸👾',tag:'파멸의 레이저',hp:1000,damage:350,speed:105,cooldown:10,unlock:'infectedUfo',description:'10초마다 아주 두꺼운 파멸의 레이저를 예고 후 발사해. 레이저는 맵 끝까지 관통하고 피해 350을 줘.',detail:'HP 1000 · 파멸의 레이저 350 / 10초 · 발사 전 1초 피격 예고 · 맵 관통'},"
rep(alien_line,new_roster)

# ---------------- progression / unlock state ----------------
rep("const ROBOT_STAGE_KEY='neonRumble.robotStages.v1',SKELETON_UNLOCK_KEY='neonRumble.skeletonBundleUnlocked.v2',SKELETON_MAGE_UNLOCK_KEY='neonRumble.skeletonMageUnlocked.v1',DESERT_STAGE_KEY='neonRumble.desertStages.v1',ZOMBIE_MAGE_UNLOCK_KEY='neonRumble.zombieMageUnlocked.v1',LEGACY_SKELETON_UNLOCK_KEY='neonRumble.skeletonUnlocked.v1';",
    "const ROBOT_STAGE_KEY='neonRumble.robotStages.v1',SKELETON_UNLOCK_KEY='neonRumble.skeletonBundleUnlocked.v2',SKELETON_MAGE_UNLOCK_KEY='neonRumble.skeletonMageUnlocked.v1',DESERT_STAGE_KEY='neonRumble.desertStages.v1',MANSION_STAGE_KEY='neonRumble.mansionStages.v1',ZOMBIE_MAGE_UNLOCK_KEY='neonRumble.zombieMageUnlocked.v1',INFECTED_UFO_UNLOCK_KEY='neonRumble.infectedUfoUnlocked.v1',LEGACY_SKELETON_UNLOCK_KEY='neonRumble.skeletonUnlocked.v1';")
rep("let robotStageMask=0,desertStageMask=0,skeletonsUnlocked=false,skeletonMageUnlocked=false,zombieMageUnlocked=false;try{localStorage.removeItem(LEGACY_SKELETON_UNLOCK_KEY);robotStageMask=Number(localStorage.getItem(ROBOT_STAGE_KEY)||0)||0;desertStageMask=Number(localStorage.getItem(DESERT_STAGE_KEY)||0)||0;skeletonsUnlocked=localStorage.getItem(SKELETON_UNLOCK_KEY)==='1';skeletonMageUnlocked=localStorage.getItem(SKELETON_MAGE_UNLOCK_KEY)==='1';zombieMageUnlocked=localStorage.getItem(ZOMBIE_MAGE_UNLOCK_KEY)==='1'}catch{}",
    "let robotStageMask=0,desertStageMask=0,mansionStageMask=0,skeletonsUnlocked=false,skeletonMageUnlocked=false,zombieMageUnlocked=false,infectedUfoUnlocked=false;try{localStorage.removeItem(LEGACY_SKELETON_UNLOCK_KEY);robotStageMask=Number(localStorage.getItem(ROBOT_STAGE_KEY)||0)||0;desertStageMask=Number(localStorage.getItem(DESERT_STAGE_KEY)||0)||0;mansionStageMask=Number(localStorage.getItem(MANSION_STAGE_KEY)||0)||0;skeletonsUnlocked=localStorage.getItem(SKELETON_UNLOCK_KEY)==='1';skeletonMageUnlocked=localStorage.getItem(SKELETON_MAGE_UNLOCK_KEY)==='1';zombieMageUnlocked=localStorage.getItem(ZOMBIE_MAGE_UNLOCK_KEY)==='1';infectedUfoUnlocked=localStorage.getItem(INFECTED_UFO_UNLOCK_KEY)==='1'}catch{}")
rep("function chapter3Unlocked(){return (desertStageMask&7)===7}\nfunction markDesertStage(n){",
    "function chapter3Unlocked(){return (desertStageMask&7)===7}\nfunction chapter4Unlocked(){return (mansionStageMask&7)===7}\nfunction markMansionStage(n){const before=chapter4Unlocked();mansionStageMask|=(1<<(n-1));try{localStorage.setItem(MANSION_STAGE_KEY,String(mansionStageMask))}catch{}updateChapter4UI();return !before&&chapter4Unlocked()}\nfunction markDesertStage(n){")
rep("(c?.unlock==='zombieMage'&&!zombieMageUnlocked)||(c?.unlock==='moneyManShop'&&!moneyManOwned())",
    "(c?.unlock==='zombieMage'&&!zombieMageUnlocked)||(c?.unlock==='infectedUfo'&&!infectedUfoUnlocked)||(c?.unlock==='moneyManShop'&&!moneyManOwned())")
rep("function tryUnlockZombieMage(){if(zombieMageUnlocked)return 'already';if(Math.random()>=.1)return 'miss';zombieMageUnlocked=true;try{localStorage.setItem(ZOMBIE_MAGE_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return 'won'}",
    "function tryUnlockZombieMage(){if(zombieMageUnlocked)return 'already';if(Math.random()>=.1)return 'miss';zombieMageUnlocked=true;try{localStorage.setItem(ZOMBIE_MAGE_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return 'won'}\nfunction tryUnlockInfectedUfo(){if(infectedUfoUnlocked)return 'already';if(Math.random()>=.05)return 'miss';infectedUfoUnlocked=true;try{localStorage.setItem(INFECTED_UFO_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return 'won'}")

# ---------------- Alien UFO shield damage ----------------
needle="if(this.result!==null||f.health<=0||e.health<=0||(!friendly&&f.team===e.team)||this.isStudying(e)||(e.id==='ghost'&&e.ghostPhaseUntil>this.time))return 0;\n dmg=Math.max(0,dmg-10*(f.moneyHappiness||0));"
replacement="if(this.result!==null||f.health<=0||e.health<=0||(!friendly&&f.team===e.team)||this.isStudying(e)||(e.id==='ghost'&&e.ghostPhaseUntil>this.time))return 0;\n if(e.id==='alien'&&e.ufoMounted&&e.ufoHp>0){const n=Math.min(e.ufoHp,Math.max(0,Math.round(dmg)));e.ufoHp-=n;f.damageDealt+=n;f.hits++;e.flash=.15;this.effect(e,'🛸 −'+n,'hit');if(e.ufoHp<=0){e.ufoMounted=false;e.ufoHp=0;e.icon='👽';e.ufoNext=this.time+10;this.effect(e,'🛸 UFO 파괴!','skill');this.emit('🛸 UFO가 파괴되어 외계인이 탈출!')}return n}\n dmg=Math.max(0,dmg-10*(f.moneyHappiness||0));"
rep(needle,replacement)

# ---------------- alien skills, UFO mount, cow status, Chapter4 enemies ----------------
old_alien="alienSkill(f,e){if(f.id!=='alien'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0||f.cd>1e-9)return;const a=this.aim(f,e),dmg=50+Math.floor(this.random()*21);this.shots.push({x:f.x+a.x*(f.radius+8),y:f.y+a.y*(f.radius+8),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'alienlaser',radius:7*f.scale,speed:430*f.scale,damage:dmg*f.scale,life:Infinity,bounces:0});f.cd=2/f.scale;f.attack=.18/f.scale;this.effect(f,'👽 레이저 '+dmg+'!','skill')}"
new_alien="""updateAlienUfo(f){if(f.id!=='alien'||f.health<=0)return;if(!Number.isFinite(f.ufoNext))f.ufoNext=this.time+10;if(!f.ufoMounted&&this.time>=f.ufoNext-1e-9){f.ufoMounted=true;f.ufoHp=300;f.icon='🛸';const es=this.enemies(f);if(es.length){const e=es[Math.floor(this.random()*es.length)];e.cowUntil=this.time+5;this.shots=this.shots.filter(s=>s.owner!==e.side);e.x=clamp(f.x+this.rand(-35,35),55,665);e.y=clamp(f.y+65,55,665);e.stunUntil=0;this.effect(e,'🐄 5초 변신!','skill');this.emit('🛸 UFO가 '+e.name+'을 빨아들여 5초 동안 🐄 소로 만들었어!')}this.effect(f,'🛸 UFO 탑승 · HP 300','skill')}}
cowMove(f,dt){f.attack=0;f.cd=Math.max(0,(f.cd||0)-dt);f.turn=(f.turn||0)-dt;const manual=(this.mode==='control'||this.manualTeam0)&&f.team===0&&!f.summon;if(manual){f.vx=Number(this.controlX)||0;f.vy=Number(this.controlY)||0}else if(f.turn<=0)this.turn(f);const n=Math.hypot(f.vx,f.vy)||1;if(!manual){f.vx/=n;f.vy/=n}f.x+=f.vx*f.speed*dt;f.y+=f.vy*f.speed*dt;const {low,high}=this.bounds(f);if(f.x<low||f.x>high){f.x=clamp(f.x,low,high);f.vx*=-1}if(f.y<low||f.y>high){f.y=clamp(f.y,low,high);f.vy*=-1}}
alienSkill(f,e){if(f.id!=='alien'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0||f.cd>1e-9)return;const a=this.aim(f,e),dmg=50+Math.floor(this.random()*21);this.shots.push({x:f.x+a.x*(f.radius+8),y:f.y+a.y*(f.radius+8),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'alienlaser',radius:7*f.scale,speed:430*f.scale,damage:dmg*f.scale,life:Infinity,bounces:0});f.cd=2/f.scale;f.attack=.18/f.scale;this.effect(f,'👽 레이저 '+dmg+'!','skill')}
alienCreatureSkill(f,e){if(f.id!=='alien_creature'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0||f.cd>1e-9)return;const a=this.aim(f,e);this.shots.push({x:f.x+a.x*(f.radius+8),y:f.y+a.y*(f.radius+8),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'alienlaser',radius:7*f.scale,speed:410*f.scale,damage:50*f.scale,life:Infinity,bounces:0});f.cd=2/f.scale;f.attack=.18/f.scale;this.effect(f,'👾 레이저 50!','skill')}
infectedUfoSkill(f,e){if(f.id!=='infected_ufo'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0)return;if(!Number.isFinite(f.doomNext))f.doomNext=this.time+10;if(!f.doomFireAt&&this.time>=f.doomNext-1-1e-9){const a=this.aim(f,e);f.doomAngle=Math.atan2(a.y,a.x);f.doomFireAt=f.doomNext;this.effect(f,'⚠️ 파멸의 레이저 예고!','doom');this.emit('⚠️ 감염 UFO의 파멸의 레이저! 붉은 피격 범위에서 벗어나!')}if(f.doomFireAt&&this.time>=f.doomFireAt-1e-9){const ang=f.doomAngle||0,dx=Math.cos(ang),dy=Math.sin(ang),width=55*f.scale;this.resolvingBlast=true;for(const t of this.enemies(f)){const rx=t.x-f.x,ry=t.y-f.y,along=rx*dx+ry*dy,perp=Math.abs(rx*dy-ry*dx);if(along>=-t.radius&&perp<=width+t.radius)this.attack(f,t,350*f.scale)}this.resolvingBlast=false;this.effects.push({x:f.x,y:f.y,text:'',kind:'doomlaser',side:f.side,team:f.team,life:.55,angle:ang});this.checkEnd();f.doomFireAt=0;f.doomNext=this.time+10;this.emit('🛸👾 파멸의 레이저 발사! 피해 350')}}"""
rep(old_alien,new_alien)

# Cow only moves; add skills for new enemies.
rep("for(const f of this.fighters){if(f.health<=0)continue;const e=this.nearest(f);if(e)this.stepFighter(f,e,dt)}",
    "for(const f of this.fighters){if(f.health<=0)continue;if((f.cowUntil||0)>this.time){this.cowMove(f,dt);continue}const e=this.nearest(f);if(e)this.stepFighter(f,e,dt)}")
rep("if(f.id==='coolguy')this.coolGuySkill(f,e);if(f.id==='firefighter')this.firefighterSkill(f,e);if(f.id==='moneyman')this.moneyManSkill(f,e);if(f.id==='alien')this.alienSkill(f,e);if(['zombie'",
    "if(f.id==='coolguy')this.coolGuySkill(f,e);if(f.id==='firefighter')this.firefighterSkill(f,e);if(f.id==='moneyman')this.moneyManSkill(f,e);if(f.id==='alien'){this.updateAlienUfo(f);this.alienSkill(f,e)}if(f.id==='alien_creature')this.alienCreatureSkill(f,e);if(f.id==='infected_ufo')this.infectedUfoSkill(f,e);if(['zombie'")
rep("'chef','coolguy','firefighter','moneyman','alien','zombie'",
    "'chef','coolguy','firefighter','moneyman','alien','alien_creature','infected_ufo','zombie'")
# Stop cow form from performing collision attacks/specials.
rep("for(const f of order){const e=f===a?b:a;if(f.id==='spider'",
    "for(const f of order){const e=f===a?b:a;if((f.cowUntil||0)>this.time)continue;if(f.id==='spider'")
rep("if(a.team!==b.team&&(a.id==='ghost'||b.id==='ghost')){for(const g of [a,b])if(g.id==='ghost'&&g.health>0){",
    "if(a.team!==b.team&&(a.id==='ghost'||b.id==='ghost')){for(const g of [a,b])if(g.id==='ghost'&&g.health>0&&(g.cowUntil||0)<=this.time){")

# ---------------- Chapter 4 UI / mode plumbing ----------------
rep("function isManualMode(){return ['control','stage','boss-control','desert','mansion'].includes(mode)}",
    "function isManualMode(){return ['control','stage','boss-control','desert','mansion','space'].includes(mode)}")
rep("function updateChapter3UI(){const b=$('chapter3-entry');if(!b)return;const ok=chapter3Unlocked();b.disabled=!ok;b.textContent=ok?'🏰 CHAPTER 3 · 피의 저택과 좀비 반란':'🔒 CHAPTER 3 · CHAPTER 2 STAGE 1·2·3 클리어 필요'}",
    "function updateChapter3UI(){const b=$('chapter3-entry');if(!b)return;const ok=chapter3Unlocked();b.disabled=!ok;b.textContent=ok?'🏰 CHAPTER 3 · 피의 저택과 좀비 반란':'🔒 CHAPTER 3 · CHAPTER 2 STAGE 1·2·3 클리어 필요'}\nfunction updateChapter4UI(){const b=$('chapter4-entry');if(!b)return;const ok=chapter4Unlocked();b.disabled=!ok;b.textContent=ok?'🪐 CHAPTER 4 · 외계인의 역습':'🔒 CHAPTER 4 · CHAPTER 3 STAGE 1·2·3 클리어 필요'}")
old_ui="function updateStageUI(){const on=mode==='stage',desertSelect=mode==='desert-select',mansionSelect=mode==='mansion-select',special=on||desertSelect||mansionSelect;document.querySelector('.section-title').hidden=special;document.querySelector('.versus').hidden=special;$('start').hidden=special;document.querySelector('.pick-heading').hidden=special;$('character-search').hidden=special;$('roster').hidden=special;document.querySelector('.match-info').hidden=special;$('stage-entry').hidden=special;$('boss-control-entry').hidden=special;$('chapter2-entry').hidden=special;$('chapter3-entry').hidden=special;$('stage-panel').hidden=!on;$('desert-panel').hidden=!desertSelect;$('mansion-panel').hidden=!mansionSelect;if(special){"
new_ui="function updateStageUI(){const on=mode==='stage',desertSelect=mode==='desert-select',mansionSelect=mode==='mansion-select',spaceSelect=mode==='space-select',special=on||desertSelect||mansionSelect||spaceSelect;document.querySelector('.section-title').hidden=special;document.querySelector('.versus').hidden=special;$('start').hidden=special;document.querySelector('.pick-heading').hidden=special;$('character-search').hidden=special;$('roster').hidden=special;document.querySelector('.match-info').hidden=special;$('stage-entry').hidden=special;$('boss-control-entry').hidden=special;$('chapter2-entry').hidden=special;$('chapter3-entry').hidden=special;$('chapter4-entry').hidden=special;$('stage-panel').hidden=!on;$('desert-panel').hidden=!desertSelect;$('mansion-panel').hidden=!mansionSelect;$('space-panel').hidden=!spaceSelect;if(special){"
rep(old_ui,new_ui)
rep("updateControlBossUnlockUI();updateChapter2UI();updateChapter3UI()}","updateControlBossUnlockUI();updateChapter2UI();updateChapter3UI();updateChapter4UI()}",1)
rep("const stageWas=mode==='stage'||mode==='desert-select'||mode==='mansion-select';if(!stageWas)",
    "const stageWas=mode==='stage'||mode==='desert-select'||mode==='mansion-select'||mode==='space-select';if(!stageWas)")
rep("$('chapter2-entry').hidden=false;$('chapter3-entry').hidden=false}","$('chapter2-entry').hidden=false;$('chapter3-entry').hidden=false;$('chapter4-entry').hidden=false}")

# Handlers + stage buttons.
rep("$('chapter3-entry').onclick=()=>{if(!chapter3Unlocked())return;if(mode==='desert'||mode==='desert-select')resetDesertTransient();mode='mansion-select';updateSelection();window.scrollTo({top:0,behavior:'auto'})};",
    "$('chapter3-entry').onclick=()=>{if(!chapter3Unlocked())return;if(mode==='desert'||mode==='desert-select')resetDesertTransient();if(mode==='space'||mode==='space-select')resetSpaceTransient();mode='mansion-select';updateSelection();window.scrollTo({top:0,behavior:'auto'})};\n$('chapter4-entry').onclick=()=>{if(!chapter4Unlocked())return;if(mode==='mansion'||mode==='mansion-select')resetMansionTransient();mode='space-select';updateSelection();window.scrollTo({top:0,behavior:'auto'})};")
rep("$('mansion-1').onclick=()=>startMansionStage(1);$('mansion-2').onclick=()=>startMansionStage(2);$('mansion-3').onclick=()=>startMansionStage(3);",
    "$('mansion-1').onclick=()=>startMansionStage(1);$('mansion-2').onclick=()=>startMansionStage(2);$('mansion-3').onclick=()=>startMansionStage(3);$('space-1').onclick=()=>startSpaceStage(1);$('space-2').onclick=()=>startSpaceStage(2);$('space-3').onclick=()=>startSpaceStage(3);")

# ---------------- Chapter 4 stage implementation ----------------
insert_before="function start(){if(mode==='desert'||mode==='desert-select'){resetDesertTransient();mode='duel'}"
space_code="""let spaceStageNo=1,spaceWave=0;
function resetSpaceTransient(){spaceStageNo=1;spaceWave=0;if(engine)engine.desertWaveMode=false}
function makeSpaceEnemy(x,y){const tmp=new Engine('alien','alien_creature',Math.random,{mode:'control'}).fighters[1];tmp.side=engine.fighters.length;tmp.team=1;tmp.summon=true;tmp.ownerSide=1;tmp.x=x;tmp.y=y;tmp.hp=100;tmp.health=100;tmp.damage=50;tmp.cooldown=2;tmp.cd=0;tmp.trail=[];tmp.deathOrder=null;engine.fighters.push(tmp);return tmp}
function spawnSpaceWave(){spaceWave++;const spots=[[535,180],[610,360],[535,540]];for(const [x,y] of spots)makeSpaceEnemy(x,y);$('event').textContent='🪐 WAVE '+spaceWave+' / 5 · 👾 외계생물 3마리 출현!'}
function startSpaceStage(n){spaceStageNo=n;mode='space';spaceWave=0;if(n===3){engine=new Engine('alien','infected_ufo',Math.random,{mode:'control'});const boss=engine.fighters[1];boss.hp=1000;boss.health=1000;boss.doomNext=10}else{engine=new Engine('alien','alien_creature',Math.random,{mode:'control'});engine.fighters[1].health=0;spawnSpaceWave()}engine.desertWaveMode=true;paused=false;acc=0;last=performance.now();lastHits=0;lastMessage='';$('selection').hidden=true;$('battle').hidden=false;$('result').hidden=true;$('pause-label').hidden=true;$('pause').disabled=false;$('pause').textContent='일시정지';resetStick();refreshControlUI();$('squad-hud').hidden=true;$('relay-hud').hidden=true;$('score-label0').textContent='👽 외계인';$('score-label1').textContent=n===3?'🛸👾 감염 UFO':'👾 외계생물 웨이브';$('battle-mode').textContent='CHAPTER 4 · '+n;$('battle-info').textContent=n===3?'CHAPTER 4 STAGE 3 · 감염 UFO가 10초마다 1초 피격 예고 후 두꺼운 파멸의 레이저를 발사. 피해 350 · 맵 관통.':'CHAPTER 4 STAGE '+n+' · 👾 외계생물 3마리씩 총 5웨이브 · HP 100 · 반사 레이저 피해 50 고정 · 웨이브마다 외계인 최대 HP 30% 회복.';fit();hud();draw();window.scrollTo({top:0,behavior:'auto'});playSfx('start')}
function updateSpaceStage(){if(mode!=='space'||!engine||engine.result!==null)return;const hero=engine.fighters.find(f=>f.team===0&&!f.summon);if(!hero||hero.health<=0){engine.result=1;return}if(spaceStageNo<3){const alive=engine.fighters.some(f=>f.team===1&&f.health>0);if(!alive){const before=hero.health,heal=hero.hp*.3;hero.health=Math.min(hero.hp,hero.health+heal);const actual=Math.max(0,Math.round(hero.health-before));if(actual>0){hero.healed=(hero.healed||0)+actual;engine.effect(hero,'🪐 WAVE CLEAR +'+actual,'heal')}if(spaceWave>=5)engine.result=0;else spawnSpaceWave()}}else{const boss=engine.fighters.find(f=>f.id==='infected_ufo'&&f.team===1);if(!boss||boss.health<=0)engine.result=0}}
"""
rep(insert_before,space_code+insert_before)

# Start/selection/rematch reset plumbing.
rep("function start(){if(mode==='desert'||mode==='desert-select'){resetDesertTransient();mode='duel'}if(mode==='mansion'||mode==='mansion-select'){resetMansionTransient();mode='duel'}",
    "function start(){if(mode==='desert'||mode==='desert-select'){resetDesertTransient();mode='duel'}if(mode==='mansion'||mode==='mansion-select'){resetMansionTransient();mode='duel'}if(mode==='space'||mode==='space-select'){resetSpaceTransient();mode='duel'}")
rep("function selection(){if(mode==='desert'||mode==='desert-select'){resetDesertTransient();mode='duel'}if(mode==='mansion'||mode==='mansion-select'){resetMansionTransient();mode='duel'}",
    "function selection(){if(mode==='desert'||mode==='desert-select'){resetDesertTransient();mode='duel'}if(mode==='mansion'||mode==='mansion-select'){resetMansionTransient();mode='duel'}if(mode==='space'||mode==='space-select'){resetSpaceTransient();mode='duel'}")
rep("$('rematch').onclick=()=>mode==='stage'?startStage(stageNo):mode==='desert'?startDesertStage(desertStageNo):mode==='mansion'?startMansionStage(mansionStageNo):start();",
    "$('rematch').onclick=()=>mode==='stage'?startStage(stageNo):mode==='desert'?startDesertStage(desertStageNo):mode==='mansion'?startMansionStage(mansionStageNo):mode==='space'?startSpaceStage(spaceStageNo):start();")

# ---------------- result / unlock Chapter 4 ----------------
old_mansion="else if(mode==='mansion'&&engine.result===0){const coinReward=awardStageCoins(mansionStageNo),zRoll=mansionStageNo===3?tryUnlockZombieMage():null;$('winner-icon').textContent='🏰';$('winner').textContent='CHAPTER 3 · STAGE '+mansionStageNo+' 클리어!';$('summary').textContent=t+'초 · 피의 저택 방어 성공 · 🪙 '+coinReward+'코인 획득!'+(zRoll==='won'?' · 🎁 10% 보상 성공! 🧌 법사좀비 획득!':zRoll==='miss'?' · 🎲 법사좀비 획득 실패 (10%)':'')}else if(mode==='mansion'){$('winner-icon').textContent='🧟‍♂️';$('winner').textContent='CHAPTER 3 · STAGE '+mansionStageNo+' 실패';$('summary').textContent=t+'초 · 흡혈귀가 쓰러졌어. 저택을 다시 지켜 봐.'}else{"
new_mansion="else if(mode==='mansion'&&engine.result===0){const coinReward=awardStageCoins(mansionStageNo),zRoll=mansionStageNo===3?tryUnlockZombieMage():null,chapter4Now=markMansionStage(mansionStageNo);$('winner-icon').textContent='🏰';$('winner').textContent='CHAPTER 3 · STAGE '+mansionStageNo+' 클리어!';$('summary').textContent=t+'초 · 피의 저택 방어 성공 · 🪙 '+coinReward+'코인 획득!'+(zRoll==='won'?' · 🎁 10% 보상 성공! 🧌 법사좀비 획득!':zRoll==='miss'?' · 🎲 법사좀비 획득 실패 (10%)':'')+(chapter4Now?' · 🪐 CHAPTER 4 해금!':'')}else if(mode==='mansion'){$('winner-icon').textContent='🧟‍♂️';$('winner').textContent='CHAPTER 3 · STAGE '+mansionStageNo+' 실패';$('summary').textContent=t+'초 · 흡혈귀가 쓰러졌어. 저택을 다시 지켜 봐.'}else if(mode==='space'&&engine.result===0){const coinReward=awardStageCoins(spaceStageNo),ufoRoll=spaceStageNo===3?tryUnlockInfectedUfo():null;$('winner-icon').textContent='🪐';$('winner').textContent='CHAPTER 4 · STAGE '+spaceStageNo+' 클리어!';$('summary').textContent=t+'초 · 외계 침공 저지 성공 · 🪙 '+coinReward+'코인 획득!'+(ufoRoll==='won'?' · 🎁 5% 보상 성공! 🛸👾 감염 UFO 획득!':ufoRoll==='miss'?' · 🎲 감염 UFO 획득 실패 (5%)':'')}else if(mode==='space'){$('winner-icon').textContent='👾';$('winner').textContent='CHAPTER 4 · STAGE '+spaceStageNo+' 실패';$('summary').textContent=t+'초 · 외계인이 쓰러졌어. 다시 침공을 막아 봐.'}else{"
rep(old_mansion,new_mansion)

# ---------------- HUD ----------------
rep("function ability(f){if(f.id==='alien')return '👽 레이저 2초 · 벽 무한 반사 · 피해 50~70';",
    "function ability(f){if(f.id==='alien')return (f.ufoMounted?'🛸 UFO '+Math.ceil(f.ufoHp)+' / 300 HP':'🛸 UFO까지 '+Math.max(0,(f.ufoNext||10)-engine.time).toFixed(1)+'초')+' · 👽 레이저 2초 · 피해 50~70';if(f.id==='alien_creature')return '👾 반사 레이저 2초 · 피해 50 고정';if(f.id==='infected_ufo')return '🛸👾 파멸 레이저 '+Math.max(0,(f.doomNext||10)-engine.time).toFixed(1)+'초 · 피해 350';")
rep("+(f.moneyHappiness?' · 💰 행복 '+f.moneyHappiness+'중첩':'');$('bar'+team)",
    "+(f.moneyHappiness?' · 💰 행복 '+f.moneyHappiness+'중첩':'')+((f.cowUntil||0)>engine.time?' · 🐄 소 '+(f.cowUntil-engine.time).toFixed(1)+'초 · 이동만 가능':'');$('bar'+team)")

# ---------------- Chapter 4 visuals ----------------
old_bg="}else if(mode==='mansion'){const mg=ctx.createLinearGradient(0,0,0,720);mg.addColorStop(0,'#241327');mg.addColorStop(.55,'#130d1b');mg.addColorStop(1,'#090811');ctx.fillStyle=mg;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.16;ctx.fillStyle='#b8264c';ctx.beginPath();ctx.arc(585,105,58,0,Math.PI*2);ctx.fill();ctx.globalAlpha=.28;ctx.font='46px sans-serif';ctx.fillText('🕯️',92,170);ctx.fillText('🕸️',625,160);ctx.fillText('🪦',625,595);ctx.globalAlpha=1}else{ctx.fillStyle='#101c2d';ctx.fillRect(0,0,720,720)}"
new_bg="}else if(mode==='mansion'){const mg=ctx.createLinearGradient(0,0,0,720);mg.addColorStop(0,'#241327');mg.addColorStop(.55,'#130d1b');mg.addColorStop(1,'#090811');ctx.fillStyle=mg;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.16;ctx.fillStyle='#b8264c';ctx.beginPath();ctx.arc(585,105,58,0,Math.PI*2);ctx.fill();ctx.globalAlpha=.28;ctx.font='46px sans-serif';ctx.fillText('🕯️',92,170);ctx.fillText('🕸️',625,160);ctx.fillText('🪦',625,595);ctx.globalAlpha=1}else if(mode==='space'){const sg=ctx.createLinearGradient(0,0,0,720);sg.addColorStop(0,'#07162c');sg.addColorStop(.55,'#0b1532');sg.addColorStop(1,'#160d2d');ctx.fillStyle=sg;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.55;ctx.font='24px sans-serif';ctx.fillText('✦',95,125);ctx.fillText('✧',610,165);ctx.fillText('✦',565,585);ctx.fillText('✧',145,610);ctx.globalAlpha=1}else{ctx.fillStyle='#101c2d';ctx.fillRect(0,0,720,720)}"
rep(old_bg,new_bg)
rep("ctx.strokeStyle=mode==='desert'?'#b87a3c':mode==='mansion'?'#54243f':'#1c2d42';",
    "ctx.strokeStyle=mode==='desert'?'#b87a3c':mode==='mansion'?'#54243f':mode==='space'?'#315a86':'#1c2d42';")
rep("ctx.fillText(mode==='desert'?'DESERT · STAGE '+desertStageNo:mode==='mansion'?'BLOOD MANSION · STAGE '+mansionStageNo:mode==='stage'?'STAGE '+stageNo:",
    "ctx.fillText(mode==='desert'?'DESERT · STAGE '+desertStageNo:mode==='mansion'?'BLOOD MANSION · STAGE '+mansionStageNo:mode==='space'?'ALIEN INVASION · STAGE '+spaceStageNo:mode==='stage'?'STAGE '+stageNo:")
# Cow icon overrides normal character icon.
rep("}else if(f.id==='coolguy'&&f.coolGuyShoutUntil>engine.time){ctx.fillText('🗣️',f.x,f.y+1)}else{ctx.fillText(f.icon,f.x,f.y+1)}",
    "}else if((f.cowUntil||0)>engine.time){ctx.fillText('🐄',f.x,f.y+1)}else if(f.id==='coolguy'&&f.coolGuyShoutUntil>engine.time){ctx.fillText('🗣️',f.x,f.y+1)}else{ctx.fillText(f.icon,f.x,f.y+1)}")
# UFO shield ring.
rep("if(f.id==='robot'&&f.health>0&&f.robotLaserStart>=0",
    "if(f.id==='alien'&&f.ufoMounted&&f.health>0){ctx.save();ctx.globalAlpha=.75;ctx.strokeStyle='#7ef6ff';ctx.lineWidth=5;ctx.shadowColor='#7ef6ff';ctx.shadowBlur=16;ctx.beginPath();ctx.arc(f.x,f.y,r+13,0,Math.PI*2);ctx.stroke();ctx.restore();ctx.globalAlpha=f.id==='invisible'?.38:1;}if(f.id==='infected_ufo'&&f.doomFireAt&&engine.time<f.doomFireAt){const da=f.doomAngle||0;ctx.save();ctx.globalAlpha=.22+.12*Math.sin(engine.time*18);ctx.strokeStyle='#ff234f';ctx.lineWidth=110*f.scale;ctx.beginPath();ctx.moveTo(f.x,f.y);ctx.lineTo(f.x+Math.cos(da)*1200,f.y+Math.sin(da)*1200);ctx.stroke();ctx.globalAlpha=.9;ctx.strokeStyle='#ffb0bc';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(f.x,f.y);ctx.lineTo(f.x+Math.cos(da)*1200,f.y+Math.sin(da)*1200);ctx.stroke();ctx.restore();}if(f.id==='robot'&&f.health>0&&f.robotLaserStart>=0")
# Doom laser effect renderer.
rep("for(const v of engine.effects){if(v.kind==='shockwave'){",
    "for(const v of engine.effects){if(v.kind==='doomlaser'){ctx.save();ctx.globalAlpha=Math.min(1,v.life*2);ctx.strokeStyle='#ff1744';ctx.shadowColor='#ff1744';ctx.shadowBlur=35;ctx.lineWidth=110;ctx.beginPath();ctx.moveTo(v.x,v.y);ctx.lineTo(v.x+Math.cos(v.angle||0)*1400,v.y+Math.sin(v.angle||0)*1400);ctx.stroke();ctx.strokeStyle='#fff';ctx.lineWidth=28;ctx.beginPath();ctx.moveTo(v.x,v.y);ctx.lineTo(v.x+Math.cos(v.angle||0)*1400,v.y+Math.sin(v.angle||0)*1400);ctx.stroke();ctx.restore()}if(v.kind==='shockwave'){")

# Loop + initial chapter4 UI update.
rep("updateDesertStage();updateMansionStage();hud()","updateDesertStage();updateMansionStage();updateSpaceStage();hud()")
rep("applySettingsUI();updateControlBossUnlockUI();updateChapter2UI();updateChapter3UI();updateCoinUI();",
    "applySettingsUI();updateControlBossUnlockUI();updateChapter2UI();updateChapter3UI();updateChapter4UI();updateCoinUI();")

p.write_text(s,encoding='utf-8')
print('v3.44 Alien UFO + Chapter 4 patch applied')
