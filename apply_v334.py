from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n!=count:
        raise SystemExit(f'replace mismatch: expected {count}, found {n}: {old[:160]!r}')
    s=s.replace(old,new,count)

# Version and patch notes
rep('BATTLE <b>v3.33</b>','BATTLE <b>v3.34</b>')
rep('📒 패치노트 · v3.33','📒 패치노트 · v3.34')
rep('<div class="patch-body"><div class="patch-version"><h3>v3.33 · 쿨가이 & 밸런스</h3>', '<div class="patch-body"><div class="patch-version"><h3>v3.34 · 사막의 해골 & 밸런스</h3><ul><li>쿨가이: 샤우팅 피해 150 → 200.</li><li>스테이지 모드 CHAPTER 2 추가. 기존 로봇 스테이지 1·2·3을 모두 클리어하면 입장 가능.</li><li>CHAPTER 2: 카우보이가 주인공인 사막 전투. STAGE 1~2는 해골 3마리씩 총 5웨이브, STAGE 3은 해골 법사와 전투.</li><li>신규 적: 🔫 총잡이 해골, 🗡️ 칼잡이 해골, 🍺 취한 해골. 기본 HP 125.</li><li>해골 법사: 추적 마법탄을 사용하며 10초마다 해골 1마리를 소환.</li><li>CHAPTER 2 STAGE 3 클리어 시 해골 3종 해금. 일반 전투에서 해금 해골은 최대 3회 등장.</li></ul></div><div class="patch-version"><h3>v3.33 · 쿨가이 & 밸런스</h3>')

# Cool Guy damage 150 -> 200 (roster, skill, HUD)
rep("hp:1000,damage:150,speed:160,cooldown:8,description:'8초마다 가장 가까운 적 방향으로 자기 몸에서 시작하는 부채꼴 샤우팅 공격을 해. 범위 안 모든 적에게 피해 150을 주며 공격 순간 🗣️ 모습으로 변해.',detail:'HP 1000 · 부채꼴 샤우팅 150 · 공격 주기 8초", "hp:1000,damage:200,speed:160,cooldown:8,description:'8초마다 가장 가까운 적 방향으로 자기 몸에서 시작하는 부채꼴 샤우팅 공격을 해. 범위 안 모든 적에게 피해 200을 주며 공격 순간 🗣️ 모습으로 변해.',detail:'HP 1000 · 부채꼴 샤우팅 200 · 공격 주기 8초")
rep("this.attack(f,target,150*f.scale)","this.attack(f,target,200*f.scale)")
rep("+'초 · 부채꼴 150'","+'초 · 부채꼴 200'")

# Add skeleton roster entries after Cool Guy
needle="{id:'coolguy',name:'쿨가이',icon:'👤',tag:'부채꼴 샤우팅',hp:1000,damage:200,speed:160,cooldown:8,description:'8초마다 가장 가까운 적 방향으로 자기 몸에서 시작하는 부채꼴 샤우팅 공격을 해. 범위 안 모든 적에게 피해 200을 주며 공격 순간 🗣️ 모습으로 변해.',detail:'HP 1000 · 부채꼴 샤우팅 200 · 공격 주기 8초 · 범위 내 모든 적 타격 · 공격 중 🗣️ 변신 · 전용 웅장한 샤우팅 사운드'}"
insert=needle+",\n{id:'skeleton_gun',name:'총잡이 해골',icon:'💀',tag:'🔫 회전총 · 3회 등장',hp:125,damage:70,speed:155,cooldown:1,unlock:'skeleton',description:'몸 주위를 도는 총이 가장 가까운 적을 향해 1초마다 피해 70의 총알을 발사해. CHAPTER 2에서 해금하면 한 경기에서 최대 3번 등장해.',detail:'HP 125 · 🔫 회전총 · 총알 70 / 1초 · 해금 후 총 3회 등장'},\n{id:'skeleton_sword',name:'칼잡이 해골',icon:'💀',tag:'🗡️ 추적검 · 3회 등장',hp:125,damage:70,speed:175,cooldown:3,unlock:'skeleton',description:'칼이 항상 가장 가까운 적을 가리켜. 칼이 닿으면 피해 70을 주고 3초 동안 다시 공격할 수 없어. CHAPTER 2에서 해금하면 한 경기에서 최대 3번 등장해.',detail:'HP 125 · 🗡️ 피해 70 · 쿨타임 3초 · 해금 후 총 3회 등장'},\n{id:'skeleton_drunk',name:'취한 해골',icon:'💀',tag:'🍺 비틀비틀 조준 · 3회 등장',hp:125,damage:100,speed:145,cooldown:3,unlock:'skeleton',description:'맥주잔이 적을 노리지만 술에 취해 조준 오차가 커. 3초마다 빗나가기 쉬운 맥주 공격으로 피해 100을 노려. CHAPTER 2에서 해금하면 한 경기에서 최대 3번 등장해.',detail:'HP 125 · 🍺 피해 100 · 쿨타임 3초 · 낮은 명중률 · 해금 후 총 3회 등장'},\n{id:'skeleton_mage',name:'해골 법사',icon:'💀🧙',tag:'추적 마법 · 해골 소환',hp:1000,damage:65,speed:140,cooldown:1.45,stageOnly:true,description:'마법사처럼 추적 마법탄을 사용하고 10초마다 해골 1마리를 소환하는 CHAPTER 2 보스.',detail:'HP 1000 · 추적 마법탄 65 · 10초마다 해골 1마리 소환'}"
rep(needle,insert)

# Engine: keep desert wave battles from auto-ending between waves; hero death still loses.
rep("checkEnd(){if(this.resolvingBlast)return;if(this.mode==='relay')", "checkEnd(){if(this.resolvingBlast)return;if(this.desertWaveMode){const hero=this.fighters.find(f=>f.team===0&&!f.summon);if(!hero||hero.health<=0)this.result=1;return}if(this.mode==='relay')")

# Skeleton combat methods before angry man skill
marker="angryManSkill(f,e,dt){"
methods="""skeletonSkill(f,e){
 if(!['skeleton_gun','skeleton_sword','skeleton_drunk','skeleton_mage'].includes(f.id)||f.health<=0||f.stunUntil>this.time)return;
 const a=this.aim(f,e),ang=Math.atan2(a.y,a.x);
 if(f.id==='skeleton_gun'){
   f.skeletonGunAngle=(f.skeletonGunAngle||0)+.045*f.scale;f.skeletonAimAngle=ang;
   if(f.cd<=1e-9){const gx=f.x+Math.cos(f.skeletonGunAngle)*(f.radius+28*f.scale),gy=f.y+Math.sin(f.skeletonGunAngle)*(f.radius+28*f.scale);this.shots.push({x:gx,y:gy,vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'skeletonbullet',radius:5*f.scale,speed:440*f.scale,damage:70*f.scale,life:3,bounces:0});f.cd=1/f.scale;f.attack=.16/f.scale;this.effect(f,'🔫 70','skill')}
 }else if(f.id==='skeleton_sword'){
   f.skeletonAimAngle=ang;const reach=f.radius+50*f.scale;
   if(f.cd<=1e-9&&distance(f,e)<=reach+e.radius){this.attack(f,e,70*f.scale);f.cd=3/f.scale;this.effect(f,'🗡️ 70','skill')}
 }else if(f.id==='skeleton_drunk'){
   f.skeletonAimAngle=ang;
   if(f.cd<=1e-9){const miss=this.rand(-.95,.95),aa=ang+miss,vx=Math.cos(aa),vy=Math.sin(aa);this.shots.push({x:f.x+vx*(f.radius+22),y:f.y+vy*(f.radius+22),vx,vy,owner:f.side,team:f.team,target:e.side,kind:'beer',radius:9*f.scale,speed:285*f.scale,damage:100*f.scale,life:3,bounces:0});f.cd=3/f.scale;f.attack=.18/f.scale;this.effect(f,'🍺 비틀!','skill')}
 }else if(f.id==='skeleton_mage'&&f.cd<=1e-9){this.shots.push({x:f.x+a.x*(f.radius+6),y:f.y+a.y*(f.radius+6),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'magic',radius:5*f.scale,speed:200*f.scale,damage:65*f.scale,life:5*f.scale,bounces:0});f.cd=1.45/f.scale;f.attack=.18/f.scale;this.effect(f,'💀 마법탄!','skill')}
}
"""
rep(marker,methods+marker)

# Invoke skeleton combat
rep("if(f.id==='chef')this.chefSkill(f);if(f.id==='coolguy')this.coolGuySkill(f,e);", "if(f.id==='chef')this.chefSkill(f);if(f.id==='coolguy')this.coolGuySkill(f,e);if(f.id.startsWith('skeleton_'))this.skeletonSkill(f,e);")

# Sword skeleton actively closes distance
rep("if(['knight','vampire','smith'].includes(f.id)){", "if(['knight','vampire','smith','skeleton_sword'].includes(f.id)){")

# Exclude all skeletons from generic body melee
rep("'cowboy','chef','coolguy'].includes(f.id)","'cowboy','chef','coolguy','skeleton_gun','skeleton_sword','skeleton_drunk','skeleton_mage'].includes(f.id)")

# Standard unlocked skeletons respawn up to total 3 appearances. Stage enemies opt out.
form_marker="formEgg(f){\n if(f.id==='angryman'"
skeleton_revive="""formEgg(f){
 if(['skeleton_gun','skeleton_sword','skeleton_drunk'].includes(f.id)&&!f.noSkeletonRevive&&f.health<=0&&(f.revivals||0)<2){f.revivals=(f.revivals||0)+1;f.health=f.hp;f.cd=.4/f.scale;f.poison=null;f.toxin=null;f.burn=null;f.curse=null;f.stunUntil=0;f.slow=0;f.slowPower=0;f.rootSlow=0;f.rootSlowPower=0;f.trail=[];this.shots=this.shots.filter(s=>s.owner!==f.side);this.effect(f,'💀 재등장 '+(f.revivals+1)+'/3','skill');this.emit(f.name+' 재등장! '+(f.revivals+1)+'/3');return true}
 if(f.id==='angryman'"""
rep(form_marker,skeleton_revive)

# Render skeleton weapons before fighter body
render_marker="if(f.id==='chef'&&f.health>0){const pp=engine.chefPanTip(f)"
skeleton_render="""if(f.id==='skeleton_gun'&&f.health>0){const ga=f.skeletonGunAngle||0,gr=f.radius+28*f.scale,gx=f.x+Math.cos(ga)*gr,gy=f.y+Math.sin(ga)*gr;ctx.save();ctx.font=(28*f.scale)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🔫',gx,gy);ctx.restore();}if(f.id==='skeleton_sword'&&f.health>0){const se=engine.nearest(f),sa=se?Math.atan2(se.y-f.y,se.x-f.x):(f.skeletonAimAngle||0),sr=f.radius+44*f.scale,sx=f.x+Math.cos(sa)*sr,sy=f.y+Math.sin(sa)*sr;ctx.save();ctx.translate(sx,sy);ctx.rotate(sa);ctx.font=(30*f.scale)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🗡️',0,0);ctx.restore();}if(f.id==='skeleton_drunk'&&f.health>0){const da=f.skeletonAimAngle||0,dr=f.radius+38*f.scale,dx=f.x+Math.cos(da)*dr,dy=f.y+Math.sin(da)*dr;ctx.save();ctx.font=(28*f.scale)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🍺',dx,dy);ctx.restore();}"""
rep(render_marker,skeleton_render+render_marker)

# Render beer / skeleton bullet projectiles distinctly
rep("if(s.kind==='bomb'){ctx.rotate(-Math.atan2(s.vy,s.vx));", "if(s.kind==='beer'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(27*s.radius/9)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🍺',0,0)}else if(s.kind==='skeletonbullet'){circle(0,0,7,'#ffd36b');circle(0,0,3,'#fff')}else if(s.kind==='bomb'){ctx.rotate(-Math.atan2(s.vy,s.vx));")

# Frontend state: robot chapter progress and skeleton unlock.
rep("const CONTROL_BOSS_KEY='neonRumble.controlBossUnlocked.v1';", "const CONTROL_BOSS_KEY='neonRumble.controlBossUnlocked.v1';\nconst ROBOT_STAGE_KEY='neonRumble.robotStages.v1',SKELETON_UNLOCK_KEY='neonRumble.skeletonUnlocked.v1';\nlet robotStageMask=0,skeletonsUnlocked=false;try{robotStageMask=Number(localStorage.getItem(ROBOT_STAGE_KEY)||0)||0;skeletonsUnlocked=localStorage.getItem(SKELETON_UNLOCK_KEY)==='1'}catch{}\nfunction chapter2Unlocked(){return (robotStageMask&7)===7}\nfunction markRobotStage(n){const before=chapter2Unlocked();robotStageMask|=(1<<(n-1));try{localStorage.setItem(ROBOT_STAGE_KEY,String(robotStageMask))}catch{}updateChapter2UI();return !before&&chapter2Unlocked()}\nfunction unlockSkeletons(){if(skeletonsUnlocked)return false;skeletonsUnlocked=true;try{localStorage.setItem(SKELETON_UNLOCK_KEY,'1')}catch{}for(const b of $('roster').children){const c=ROSTER.find(v=>v.id===b.dataset.character);if(c?.unlock==='skeleton')b.hidden=false}return true}\nfunction updateChapter2UI(){const b=$('chapter2-entry');if(!b)return;const ok=chapter2Unlocked();b.disabled=!ok;b.textContent=ok?'🏜️ CHAPTER 2 · 카우보이와 해골':'🔒 CHAPTER 2 · 로봇 스테이지 1·2·3 클리어 필요'}")

# Manual control includes desert battle.
rep("function isManualMode(){return ['control','stage','boss-control'].includes(mode)}", "function isManualMode(){return ['control','stage','boss-control','desert'].includes(mode)}")

# Add Chapter 2 entry button and panel.
rep("<button id=\"boss-control-entry\" class=\"stage-entry boss-control-entry\" type=\"button\" disabled>🔒 조정 보스전 · STAGE 2 클리어 시 해금</button>", "<button id=\"boss-control-entry\" class=\"stage-entry boss-control-entry\" type=\"button\" disabled>🔒 조정 보스전 · STAGE 2 클리어 시 해금</button><button id=\"chapter2-entry\" class=\"stage-entry\" type=\"button\" disabled>🔒 CHAPTER 2 · 로봇 스테이지 1·2·3 클리어 필요</button>")
rep("<p class=\"hint\">일반 모드는 직접 조작 없는 자동 전투", "<div id=\"desert-panel\" class=\"stage-panel\" hidden><p class=\"eyebrow\">CHAPTER 2 · DESERT</p><h2>🤠 카우보이와 해골 바이러스</h2><p>평범한 서부 사람들이 미지의 바이러스로 💀 해골이 됐어. 카우보이를 직접 조작해 사막을 돌파해.</p><div class=\"stage-grid\"><button class=\"stage-card\" id=\"desert-1\" type=\"button\"><b>STAGE 1</b><span>🤠 VS 💀💀💀</span><strong>사막의 첫 습격</strong><small>해골 3마리씩 총 5웨이브를 격파.</small></button><button class=\"stage-card\" id=\"desert-2\" type=\"button\"><b>STAGE 2</b><span>🤠 VS 💀💀💀</span><strong>바이러스 마을</strong><small>총잡이·칼잡이·취한 해골이 섞인 5웨이브.</small></button><button class=\"stage-card\" id=\"desert-3\" type=\"button\"><b>STAGE 3</b><span>🤠 VS 💀🧙</span><strong>해골 법사</strong><small>추적 마법탄과 10초마다 소환되는 해골을 돌파.</small></button></div></div><p class=\"hint\">일반 모드는 직접 조작 없는 자동 전투")

# Stage selector can show either Chapter 1 or Chapter 2 panel.
rep("function updateStageUI(){const on=mode==='stage';document.querySelector('.section-title').hidden=on;", "function updateStageUI(){const on=mode==='stage',desertSelect=mode==='desert-select',special=on||desertSelect;document.querySelector('.section-title').hidden=special;")
rep("document.querySelector('.versus').hidden=on;$('start').hidden=on;document.querySelector('.pick-heading').hidden=on;$('character-search').hidden=on;$('roster').hidden=on;document.querySelector('.match-info').hidden=on;$('stage-entry').hidden=on;$('boss-control-entry').hidden=on;$('stage-panel').hidden=!on;if(on){", "document.querySelector('.versus').hidden=special;$('start').hidden=special;document.querySelector('.pick-heading').hidden=special;$('character-search').hidden=special;$('roster').hidden=special;document.querySelector('.match-info').hidden=special;$('stage-entry').hidden=special;$('boss-control-entry').hidden=special;$('chapter2-entry').hidden=special;$('stage-panel').hidden=!on;$('desert-panel').hidden=!desertSelect;if(special){")
rep("updateControlBossUnlockUI()}","updateControlBossUnlockUI();updateChapter2UI()}",1)

# updateSelection must not flash normal picker while either stage selector is open.
rep("const stageWas=mode==='stage';if(!stageWas){", "const stageWas=mode==='stage'||mode==='desert-select';if(!stageWas){")
rep("$('boss-control-entry').hidden=false}","$('boss-control-entry').hidden=false;$('chapter2-entry').hidden=false}")

# Roster cards: stage-only mage is hidden; skeletons hidden until unlocked.
rep("ROSTER.forEach(c=>{const b=document.createElement('button');", "ROSTER.forEach(c=>{const b=document.createElement('button');")
rep("b.dataset.character=c.id;b.setAttribute('aria-label'", "b.dataset.character=c.id;b.hidden=!!c.stageOnly||(c.unlock==='skeleton'&&!skeletonsUnlocked);b.setAttribute('aria-label'")

# Random only picks currently playable fighters.
rep("$('random').onclick=()=>{const rand=()=>ROSTER[Math.floor(Math.random()*ROSTER.length)].id;", "$('random').onclick=()=>{const playable=ROSTER.filter(c=>!c.stageOnly&&(!c.unlock||skeletonsUnlocked)),rand=()=>playable[Math.floor(Math.random()*playable.length)].id;")

# Chapter 2 navigation and stage start state.
rep("$('boss-control-entry').onclick=()=>{if(!controlBossUnlocked)return;mode='boss-control';bossSlot=-1;side=0;updateSelection();window.scrollTo({top:0,behavior:'auto'})};", "$('boss-control-entry').onclick=()=>{if(!controlBossUnlocked)return;mode='boss-control';bossSlot=-1;side=0;updateSelection();window.scrollTo({top:0,behavior:'auto'})};\n$('chapter2-entry').onclick=()=>{if(!chapter2Unlocked())return;mode='desert-select';updateSelection();window.scrollTo({top:0,behavior:'auto'})};")
rep("$('stage-1').onclick=()=>startStage(1);$('stage-2').onclick=()=>startStage(2);$('stage-3').onclick=()=>startStage(3);", "$('stage-1').onclick=()=>startStage(1);$('stage-2').onclick=()=>startStage(2);$('stage-3').onclick=()=>startStage(3);$('desert-1').onclick=()=>startDesertStage(1);$('desert-2').onclick=()=>startDesertStage(2);$('desert-3').onclick=()=>startDesertStage(3);")

# Desert stage helpers inserted before normal start().
start_marker="function start(){engine=mode==='group'?"
desert_code="""let desertStageNo=1,desertWave=0,desertNextMageSummon=10;
function makeDesertEnemy(id,x,y){const tmp=new Engine('cowboy',id,Math.random,{mode:'control'}).fighters[1];tmp.side=engine.fighters.length;tmp.team=1;tmp.x=x;tmp.y=y;tmp.noSkeletonRevive=true;tmp.revivals=0;tmp.trail=[];return tmp}
function spawnDesertSkeleton(id,x,y){const f=makeDesertEnemy(id,x,y);engine.fighters.push(f);return f}
function spawnDesertWave(){desertWave++;const ids=['skeleton_gun','skeleton_sword','skeleton_drunk'],spots=[[535,180],[610,360],[535,540]];for(let i=0;i<3;i++)spawnDesertSkeleton(ids[Math.floor(Math.random()*ids.length)],spots[i][0],spots[i][1]);$('event').textContent='🏜️ WAVE '+desertWave+' / 5 · 해골 3마리 출현!'}
function startDesertStage(n){desertStageNo=n;mode='desert';desertWave=0;desertNextMageSummon=10;if(n===3){engine=new Engine('cowboy','skeleton_mage',Math.random,{mode:'control'});engine.fighters[1].noSkeletonRevive=true}else{engine=new Engine('cowboy','skeleton_gun',Math.random,{mode:'control'});engine.fighters[1].health=0;engine.fighters[1].noSkeletonRevive=true}engine.desertWaveMode=true;if(n<3)spawnDesertWave();paused=false;acc=0;last=performance.now();lastHits=0;lastMessage='';$('selection').hidden=true;$('battle').hidden=false;$('result').hidden=true;$('pause-label').hidden=true;$('pause').disabled=false;$('pause').textContent='일시정지';resetStick();refreshControlUI();$('squad-hud').hidden=true;$('relay-hud').hidden=true;$('score-label0').textContent='🤠 카우보이';$('score-label1').textContent=n===3?'💀🧙 해골 법사':'💀 해골 웨이브';$('battle-mode').textContent='DESERT '+n;$('battle-info').textContent=n===3?'CHAPTER 2 STAGE 3 · 해골 법사는 10초마다 해골 1마리를 소환해.':'CHAPTER 2 STAGE '+n+' · 해골 3마리씩 총 5웨이브.';fit();hud();draw();window.scrollTo({top:0,behavior:'auto'});playSfx('start')}
function updateDesertStage(){if(mode!=='desert'||!engine||engine.result!==null)return;const hero=engine.fighters.find(f=>f.team===0&&!f.summon);if(!hero||hero.health<=0){engine.result=1;return}if(desertStageNo<3){const alive=engine.fighters.some(f=>f.team===1&&f.health>0);if(!alive){if(desertWave>=5)engine.result=0;else spawnDesertWave()}}else{const mage=engine.fighters.find(f=>f.id==='skeleton_mage'&&f.team===1);if(!mage||mage.health<=0){engine.result=0;return}if(engine.time>=desertNextMageSummon-1e-9){desertNextMageSummon+=10;const ids=['skeleton_gun','skeleton_sword','skeleton_drunk'],id=ids[Math.floor(Math.random()*ids.length)],a=Math.random()*Math.PI*2;spawnDesertSkeleton(id,Math.max(70,Math.min(650,mage.x+Math.cos(a)*95)),Math.max(70,Math.min(650,mage.y+Math.sin(a)*95)));$('event').textContent='💀🧙 해골 법사가 해골 1마리를 소환!'}}}
"""
rep(start_marker,desert_code+start_marker)

# Rematch handles desert chapter.
rep("$('start').onclick=start;$('rematch').onclick=()=>mode==='stage'?startStage(stageNo):start();", "$('start').onclick=start;$('rematch').onclick=()=>mode==='stage'?startStage(stageNo):mode==='desert'?startDesertStage(desertStageNo):start();")

# Chapter 1 completion tracks all 3 stages; Chapter 2 stage 3 unlocks skeletons.
rep("if(mode==='stage'){const unlockedNow=stageNo===2?unlockControlBoss():false;$('winner-icon').textContent='🏁';$('winner').textContent='STAGE '+stageNo+' 클리어!';$('summary').textContent=t+'초 · 로봇 생존 · 다음 스테이지도 테스트해 봐.'+(unlockedNow?' · 🎮 조정 보스전 해금!':'')}else{", "if(mode==='stage'){const unlockedNow=stageNo===2?unlockControlBoss():false,chapterNow=markRobotStage(stageNo);$('winner-icon').textContent='🏁';$('winner').textContent='STAGE '+stageNo+' 클리어!';$('summary').textContent=t+'초 · 로봇 생존 · 다음 스테이지도 테스트해 봐.'+(unlockedNow?' · 🎮 조정 보스전 해금!':'')+(chapterNow?' · 🏜️ CHAPTER 2 해금!':'')}else if(mode==='desert'){const skNow=desertStageNo===3?unlockSkeletons():false;$('winner-icon').textContent='🏜️';$('winner').textContent='CHAPTER 2 · STAGE '+desertStageNo+' 클리어!';$('summary').textContent=t+'초 · 사막 돌파 성공'+(skNow?' · 💀 해골 3종 캐릭터 해금!':'')}else{")

# Desert background and label.
rep("function draw(){if(!engine)return;ctx.clearRect(0,0,720,720);ctx.fillStyle='#101c2d';ctx.fillRect(0,0,720,720);ctx.lineWidth=1;ctx.strokeStyle='#1c2d42';", "function draw(){if(!engine)return;ctx.clearRect(0,0,720,720);if(mode==='desert'){const dg=ctx.createLinearGradient(0,0,0,720);dg.addColorStop(0,'#e8b85f');dg.addColorStop(.55,'#cf9447');dg.addColorStop(1,'#b97838');ctx.fillStyle=dg;ctx.fillRect(0,0,720,720);ctx.globalAlpha=.22;ctx.fillStyle='#fff0b3';ctx.beginPath();ctx.arc(585,115,62,0,Math.PI*2);ctx.fill();ctx.globalAlpha=.35;ctx.font='42px sans-serif';ctx.fillText('🌵',90,180);ctx.fillText('🌵',640,590);ctx.globalAlpha=1}else{ctx.fillStyle='#101c2d';ctx.fillRect(0,0,720,720)}ctx.lineWidth=1;ctx.strokeStyle=mode==='desert'?'#b87a3c':'#1c2d42';")
rep("ctx.fillText(mode==='stage'?'STAGE '+stageNo:mode==='group'?", "ctx.fillText(mode==='desert'?'DESERT · STAGE '+desertStageNo:mode==='stage'?'STAGE '+stageNo:mode==='group'?")

# Update desert progression once per rendered frame after simulation ticks.
rep("while(acc>=1/120&&engine.result===null){engine.step(1/120);acc-=1/120}hud()", "while(acc>=1/120&&engine.result===null){engine.step(1/120);acc-=1/120}updateDesertStage();hud()")

# Initialize chapter 2 button too.
rep("applySettingsUI();updateControlBossUnlockUI();updateSelection();", "applySettingsUI();updateControlBossUnlockUI();updateChapter2UI();updateSelection();")

p.write_text(s,encoding='utf-8')
print('v3.34 patch applied')
