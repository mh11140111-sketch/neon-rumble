from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

def atleast(old,new,label,min_count=1):
    global s
    n=s.count(old)
    if n<min_count:
        raise SystemExit(f'{label}: expected >= {min_count}, got {n}')
    s=s.replace(old,new)

# Version + patch notes
once('<span class="badge">BATTLE <b>v3.65</b></span>','<span class="badge">BATTLE <b>v3.66</b></span>','version')
once('<details class="patch-notes"><summary>📒 패치노트 · v3.65</summary><div class="patch-body">', '<details class="patch-notes"><summary>📒 패치노트 · v3.66</summary><div class="patch-body"><div class="patch-version"><h3>v3.66 · 소방차 호스 수정 · CHAPTER 8 복싱장</h3><ul><li>👨‍🚒 소방차 탑승 중 호스 물공격이 정상적으로 적을 추적해 발사되도록 수정.</li><li>🥊 CHAPTER 8 · 복싱장 추가. CHAPTER 7 STAGE 1·2·3 클리어 시 해금, 주인공은 복서.</li><li>STAGE 1: 🫡 사부. 복서와 비슷한 돌진/근접 전투를 하지만 어퍼컷은 사용하지 않음.</li><li>STAGE 2: ⚒️ 라이벌 대장장이와 대결.</li><li>STAGE 3: 🧘‍♂️ 초능력자. 염력탄 20/2초+넉백, 5초마다 벽 밀치기 50+1초 기절, 적 투사체를 주위 궤도로 끌어당기는 패시브 사용.</li><li>🧘‍♂️ 초능력자가 붙잡아 회전시키는 적 투사체가 원래 상대에게 닿으면 그 투사체 피해를 주며, 궤도 투사체가 벽에 닿으면 초능력자가 즉시 승리.</li><li>CHAPTER 8 STAGE 3 클리어 시 매번 10% 확률로 🧘‍♂️ 초능력자 획득.</li></ul></div>', 'patch notes')

# UI: chapter 8 entry + panel
once('<button id="chapter7-entry" class="stage-entry" type="button" disabled>🔒 CHAPTER 7 · CHAPTER 6 STAGE 1·2·3 클리어 필요</button>', '<button id="chapter7-entry" class="stage-entry" type="button" disabled>🔒 CHAPTER 7 · CHAPTER 6 STAGE 1·2·3 클리어 필요</button><button id="chapter8-entry" class="stage-entry" type="button" disabled>🔒 CHAPTER 8 · CHAPTER 7 STAGE 1·2·3 클리어 필요</button>', 'chapter8 entry')
boxing_panel='''<div id="boxing-panel" class="stage-panel" hidden><h2>🥊 CHAPTER 8 · 복싱장</h2><p>주인공은 🥊 복서. 자신의 사부와 라이벌을 넘어 진정한 힘을 망가뜨린 초능력자에게 도전해.</p><div class="stage-grid"><button id="boxing-1" type="button"><strong>STAGE 1</strong><span>🥊 VS 🫡</span><small>복서와 비슷한 사부. 돌진은 사용하지만 어퍼컷은 사용하지 않아.</small></button><button id="boxing-2" type="button"><strong>STAGE 2</strong><span>🥊 VS ⚒️</span><small>오랜 라이벌 대장장이와 정면 승부.</small></button><button id="boxing-3" type="button"><strong>STAGE 3</strong><span>🥊 VS 🧘‍♂️</span><small>염력탄·벽 밀치기·투사체 궤도 조작을 사용하는 초능력자. 클리어 시 10% 획득.</small></button></div></div>'''
once('<div id="forge-panel" class="stage-panel" hidden><h2>🔨 CHAPTER 7 · 대장간</h2><p>주인공은 ⚒️ 대장장이. 장비를 약탈하러 온 👹 도깨비 군단을 막아내.</p><div class="stage-grid"><button id="forge-1" type="button"><strong>STAGE 1</strong><span>⚒️ VS 👹👹👹</span><small>HP 300 도깨비 3마리씩 3웨이브 · 방망이 80 / 3초 · 웨이브마다 HP 30% 회복</small></button><button id="forge-2" type="button"><strong>STAGE 2</strong><span>⚒️ VS 👹👹👹</span><small>STAGE 1과 동일한 도깨비 군단 3마리씩 3웨이브</small></button><button id="forge-3" type="button"><strong>STAGE 3</strong><span>⚒️ VS 👑👹</span><small>왕도깨비 HP 1800 · 방망이 140 / 1.5초 · 클리어 시 기본 50 + 추가 100코인</small></button></div></div>', '<div id="forge-panel" class="stage-panel" hidden><h2>🔨 CHAPTER 7 · 대장간</h2><p>주인공은 ⚒️ 대장장이. 장비를 약탈하러 온 👹 도깨비 군단을 막아내.</p><div class="stage-grid"><button id="forge-1" type="button"><strong>STAGE 1</strong><span>⚒️ VS 👹👹👹</span><small>HP 300 도깨비 3마리씩 3웨이브 · 방망이 80 / 3초 · 웨이브마다 HP 30% 회복</small></button><button id="forge-2" type="button"><strong>STAGE 2</strong><span>⚒️ VS 👹👹👹</span><small>STAGE 1과 동일한 도깨비 군단 3마리씩 3웨이브</small></button><button id="forge-3" type="button"><strong>STAGE 3</strong><span>⚒️ VS 👑👹</span><small>왕도깨비 HP 1800 · 방망이 140 / 1.5초 · 클리어 시 기본 50 + 추가 100코인</small></button></div></div>'+boxing_panel, 'boxing panel')

# Roster: master stage-only + psychic unlockable
roster_add="""{id:'boxing_master',name:'사부',icon:'🫡',tag:'복서식 돌진 · 어퍼컷 없음',hp:1000,damage:65,speed:195,cooldown:.42,stageOnly:true,description:'복서와 거의 같은 근접 전투와 돌진을 사용하지만 어퍼컷은 사용할 수 없어.',detail:'HP 1000 · 접촉 65 · 돌진 130 / 2.8초 · 어퍼컷 없음'},
{id:'psychic',name:'초능력자',icon:'🧘‍♂️',tag:'염력탄 · 벽 밀치기 · 투사체 궤도',hp:1000,damage:20,speed:150,cooldown:2,unlock:'psychic',description:'2초마다 염력 마법탄으로 피해 20과 넉백. 5초마다 상대를 벽으로 날려 피해 50과 1초 기절. 가까운 적 투사체를 자기 주위 궤도로 끌어당겨 되돌려 이용한다.',detail:'HP 1000 · 염력탄 20 / 2초 + 넉백 · 벽 밀치기 50 / 5초 + 기절 1초 · 적 투사체 궤도 포획 · 궤도탄 벽 접촉 시 즉시 승리 · CH8 STAGE 3 10% 획득'},
"""
once("{id:'skeleton_mage',name:'해골 법사',icon:'💀🧙',tag:'추적 마법 · 10초 해골 소환',hp:700,damage:65,speed:140,cooldown:1.45,unlock:'skeletonMage',description:'추적 마법탄을 발사하고 10초마다 총잡이·칼잡이·취한 해골 중 1마리를 소환해. CHAPTER 2 STAGE 3 클리어 시 10% 확률로 획득할 수 있어.',detail:'HP 700 · 추적 마법탄 65 / 1.45초 · 10초마다 해골 1마리 소환 · CHAPTER 2 STAGE 3 클리어 보상 10%'}\n];", "{id:'skeleton_mage',name:'해골 법사',icon:'💀🧙',tag:'추적 마법 · 10초 해골 소환',hp:700,damage:65,speed:140,cooldown:1.45,unlock:'skeletonMage',description:'추적 마법탄을 발사하고 10초마다 총잡이·칼잡이·취한 해골 중 1마리를 소환해. CHAPTER 2 STAGE 3 클리어 시 10% 확률로 획득할 수 있어.',detail:'HP 700 · 추적 마법탄 65 / 1.45초 · 10초마다 해골 1마리 소환 · CHAPTER 2 STAGE 3 클리어 보상 10%'}\n,"+roster_add+"];", 'roster add')

# Fighter state for psychic
once("boxerUpperNext:type.id==='boxer'?10/scale:9999,airborneUntil", "boxerUpperNext:type.id==='boxer'?10/scale:9999,psychicPushNext:type.id==='psychic'?5/scale:9999,psychicOrbitAngle:0,airborneUntil", 'psychic state')

# Firefighter mounted hose target fix + dedicated visual kind
once("if(!e||e.health<=0)return;const a=this.aim(f,e);this.shots.push({x:f.x+a.x*(f.radius+10),y:f.y+a.y*(f.radius+10),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'water',radius:7*f.scale,speed:430*f.scale,damage:10*f.scale,life:3,bounces:0});f.attack=.1/f.scale;return", "const target=this.nearest(f);if(!target||target.health<=0)return;const a=this.aim(f,target);this.shots.push({x:f.x+a.x*(f.radius+10),y:f.y+a.y*(f.radius+10),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:target.side,kind:'firetruck_water',radius:7*f.scale,speed:430*f.scale,damage:10*f.scale,life:3,bounces:0});f.attack=.1/f.scale;this.effect(f,'🚒💧 호스!','skill');return", 'firefighter hose')
once("else if(s.kind==='water'){", "else if(s.kind==='water'||s.kind==='firetruck_water'){", 'firetruck render')

# Psychic combat methods inserted before smith skill
anchor="smithWeaponSkill(f,e){\n"
psychic_code="""psychicSkill(f,e){
 if(!f||f.id!=='psychic'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0)return;
 if(!Number.isFinite(f.psychicPushNext))f.psychicPushNext=this.time+5/f.scale;
 if(this.time>=f.psychicPushNext-1e-9){
  f.psychicPushNext=this.time+5/f.scale;const dealt=this.attack(f,e,50*f.scale);
  if(dealt>0&&e.health>0){const b=this.bounds(e),dl=Math.abs(e.x-b.low),dr=Math.abs(b.high-e.x),dt=Math.abs(e.y-b.low),db=Math.abs(b.high-e.y),m=Math.min(dl,dr,dt,db);if(m===dl)e.x=b.low;else if(m===dr)e.x=b.high;else if(m===dt)e.y=b.low;else e.y=b.high;e.stunUntil=Math.max(e.stunUntil,this.time+1*f.scale);this.effect(e,'🧘‍♂️ 벽 밀치기 50 · 기절!','skill');this.emit('🧘‍♂️ 초능력자가 상대를 벽으로 날렸다!')}
 }
 if(f.cd<=1e-9&&e.health>0){const a=this.aim(f,e);this.shots.push({x:f.x+a.x*(f.radius+8),y:f.y+a.y*(f.radius+8),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'psychic_bolt',icon:'🟣',radius:9*f.scale,speed:330*f.scale,damage:20*f.scale,life:4/f.scale,bounces:0,knockback:75*f.scale});f.cd=2/f.scale;f.attack=.18/f.scale;this.effect(f,'🟣 염력탄!','skill')}
}
psychicCaptureShots(){
 const psychics=this.fighters.filter(f=>f.id==='psychic'&&f.health>0&&f.stunUntil<=this.time);
 if(!psychics.length)return;
 for(const s of this.shots){if(!s||s.life<=0||s.psychicOrbitBy!=null)continue;const owner=this.fighters[s.owner];if(!owner||owner.health<=0)continue;const p=psychics.find(x=>x.team!==s.team&&distance(x,s)<=210*x.scale);if(!p)continue;if(['dragon_rain','dragon_lightning'].includes(s.kind)||(s.kind==='sun_orb'&&s.stopped))continue;s.psychicOrbitBy=p.side;s.psychicOriginalOwner=s.owner;s.psychicOriginalTeam=s.team;s.psychicOrbitAngle=Math.atan2(s.y-p.y,s.x-p.x);s.psychicOrbitRadius=Math.max(p.radius+42,Math.min(150,distance(p,s)));s.life=Math.max(s.life,8/p.scale);this.effect(p,'🌀 투사체 포획!','skill')}
}
updatePsychicOrbitShot(s,dt){
 const p=this.fighters[s.psychicOrbitBy];if(!p||p.health<=0){s.life=0;return true}const r=s.psychicOrbitRadius||p.radius+60;s.psychicOrbitAngle=(s.psychicOrbitAngle||0)+dt*3.6*p.scale;s.x=p.x+Math.cos(s.psychicOrbitAngle)*r;s.y=p.y+Math.sin(s.psychicOrbitAngle)*r;s.vx=-Math.sin(s.psychicOrbitAngle);s.vy=Math.cos(s.psychicOrbitAngle);
 if(s.x<=22+(s.radius||5)||s.x>=698-(s.radius||5)||s.y<=22+(s.radius||5)||s.y>=698-(s.radius||5)){s.life=0;this.result=p.team;this.effect(p,'🧘‍♂️ 투사체가 벽에 닿았다 · 승리!','doom');this.emit('🧘‍♂️ 궤도 투사체가 벽에 닿아 초능력자 승리!');return true}
 const victims=this.fighters.filter(v=>v.health>0&&v.team===s.psychicOriginalTeam&&v!==p);for(const v of victims){if(distance(s,v)>=v.radius+(s.radius||5))continue;const dmg=Math.max(0,Number(s.damage)||0);if(dmg>0)this.attack(p,v,dmg,false,true);s.life=0;this.effect(v,'🌀 되돌아온 투사체 −'+Math.round(dmg),'skill');return true}return true
}
"""
once(anchor,psychic_code+anchor,'psychic methods')

# Call psychic skill
once("if(f.id==='merman')this.mermanSkill(f,e);if(f.id==='dragon')", "if(f.id==='merman')this.mermanSkill(f,e);if(f.id==='psychic')this.psychicSkill(f,e);if(f.id==='dragon')", 'psychic skill call')

# Master dash same as boxer, no uppercut
once("if(f.id==='boxer'&&f.skill<=0){", "if((f.id==='boxer'||f.id==='boxing_master')&&f.skill<=0){", 'master dash trigger')
once("const dash=f.id==='boxer'&&f.dash>0&&!f.dashHit;", "const dash=(f.id==='boxer'||f.id==='boxing_master')&&f.dash>0&&!f.dashHit;", 'master dash damage')
# Psychic excluded from generic contact melee; boxing master intentionally not excluded
once("'goblin','goblin_king'].includes(f.id)", "'goblin','goblin_king','psychic'].includes(f.id)", 'psychic contact exclusion')

# Psychic projectile capture + orbit update in shot loop
once(" for(const s of this.shots){\n  s.life-=dt;const f=this.fighters[s.owner];", " this.psychicCaptureShots();\n for(const s of this.shots){\n  s.life-=dt;if(s.psychicOrbitBy!=null){this.updatePsychicOrbitShot(s,dt);if(this.result!==null)break;continue}const f=this.fighters[s.owner];", 'psychic orbit loop')

# Psychic bolt knockback in projectile hit effects
once("if(s.kind==='giantslash'&&typeof triggerGiantSlashShake==='function')triggerGiantSlashShake();", "if(s.kind==='psychic_bolt'&&e.health>0){e.x+=s.vx*(s.knockback||75);e.y+=s.vy*(s.knockback||75);this.keepInside(e);e.vx=s.vx;e.vy=s.vy;this.effect(e,'🟣 넉백!','skill')}if(s.kind==='giantslash'&&typeof triggerGiantSlashShake==='function')triggerGiantSlashShake();", 'psychic bolt knockback')
# Render psychic bolt
once("else if(s.kind==='zombiemagic'){", "else if(s.kind==='psychic_bolt'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(28*s.radius/9)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🟣',0,0)}else if(s.kind==='zombiemagic'){", 'psychic bolt render')

# Storage + unlock state
once("FORGE_STAGE_KEY='neonRumble.forgeStages.v1',SHARK_UNLOCK_KEY", "FORGE_STAGE_KEY='neonRumble.forgeStages.v1',BOXING_STAGE_KEY='neonRumble.boxingStages.v1',PSYCHIC_UNLOCK_KEY='neonRumble.psychicUnlocked.v1',SHARK_UNLOCK_KEY", 'boxing keys')
once("forgeStageMask=0,skeletonsUnlocked=false", "forgeStageMask=0,boxingStageMask=0,skeletonsUnlocked=false", 'boxing mask var')
once("mermanUnlocked=false;try{", "mermanUnlocked=false,psychicUnlocked=false;try{", 'psychic var')
once("forgeStageMask=Number(localStorage.getItem(FORGE_STAGE_KEY)||0)||0;sharkUnlocked=", "forgeStageMask=Number(localStorage.getItem(FORGE_STAGE_KEY)||0)||0;boxingStageMask=Number(localStorage.getItem(BOXING_STAGE_KEY)||0)||0;psychicUnlocked=localStorage.getItem(PSYCHIC_UNLOCK_KEY)==='1';sharkUnlocked=", 'load boxing')
once("function chapter7Unlocked(){return (oceanStageMask&7)===7}\n", "function chapter7Unlocked(){return (oceanStageMask&7)===7}\nfunction chapter8Unlocked(){return (forgeStageMask&7)===7}\n", 'chapter8 unlocked')
# markForge now transitions to ch8 and mark boxing
once("function markForgeStage(n){forgeStageMask|=(1<<(n-1));try{localStorage.setItem(FORGE_STAGE_KEY,String(forgeStageMask))}catch{}renderShop();return (forgeStageMask&7)===7}", "function markForgeStage(n){const before=chapter8Unlocked();forgeStageMask|=(1<<(n-1));try{localStorage.setItem(FORGE_STAGE_KEY,String(forgeStageMask))}catch{}updateChapter8UI();renderShop();return !before&&chapter8Unlocked()}\nfunction markBoxingStage(n){boxingStageMask|=(1<<(n-1));try{localStorage.setItem(BOXING_STAGE_KEY,String(boxingStageMask))}catch{}return (boxingStageMask&7)===7}", 'mark boxing')
once("(c?.unlock==='merman'&&!mermanUnlocked)}", "(c?.unlock==='merman'&&!mermanUnlocked)||(c?.unlock==='psychic'&&!psychicUnlocked)}", 'psychic lock')
once("function tryUnlockMerman(){if(mermanUnlocked)return 'already';if(Math.random()>=.10)return 'miss';mermanUnlocked=true;try{localStorage.setItem(MERMAN_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return 'won'}", "function tryUnlockMerman(){if(mermanUnlocked)return 'already';if(Math.random()>=.10)return 'miss';mermanUnlocked=true;try{localStorage.setItem(MERMAN_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return 'won'}\nfunction tryUnlockPsychic(){if(psychicUnlocked)return 'already';if(Math.random()>=.10)return 'miss';psychicUnlocked=true;try{localStorage.setItem(PSYCHIC_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return 'won'}", 'psychic unlock fn')

# Chapter 8 UI updater
once("function updateChapter7UI(){const b=$('chapter7-entry');if(!b)return;const ok=chapter7Unlocked();b.disabled=!ok;b.textContent=ok?'🔨 CHAPTER 7 · 대장간':'🔒 CHAPTER 7 · CHAPTER 6 STAGE 1·2·3 클리어 필요'}", "function updateChapter7UI(){const b=$('chapter7-entry');if(!b)return;const ok=chapter7Unlocked();b.disabled=!ok;b.textContent=ok?'🔨 CHAPTER 7 · 대장간':'🔒 CHAPTER 7 · CHAPTER 6 STAGE 1·2·3 클리어 필요'}\nfunction updateChapter8UI(){const b=$('chapter8-entry');if(!b)return;const ok=chapter8Unlocked();b.disabled=!ok;b.textContent=ok?'🥊 CHAPTER 8 · 복싱장':'🔒 CHAPTER 8 · CHAPTER 7 STAGE 1·2·3 클리어 필요'}", 'chapter8 ui')

# Manual mode / stage UI / hide panels
once("['control','stage','boss-control','desert','mansion','space','casino','ocean','forge'].includes(mode)", "['control','stage','boss-control','desert','mansion','space','casino','ocean','forge','boxing'].includes(mode)", 'manual boxing')
once("forgeSelect=mode==='forge-select',special=", "forgeSelect=mode==='forge-select',boxingSelect=mode==='boxing-select',special=", 'boxing select var')
once("on||desertSelect||mansionSelect||spaceSelect||casinoSelect||oceanSelect||forgeSelect;", "on||desertSelect||mansionSelect||spaceSelect||casinoSelect||oceanSelect||forgeSelect||boxingSelect;", 'boxing special')
once("$('chapter7-entry').hidden=special;", "$('chapter7-entry').hidden=special;$('chapter8-entry').hidden=special;", 'hide ch8 button')
once("$('forge-panel').hidden=!forgeSelect;", "$('forge-panel').hidden=!forgeSelect;$('boxing-panel').hidden=!boxingSelect;", 'show boxing panel')
once("updateChapter6UI();updateChapter7UI()}", "updateChapter6UI();updateChapter7UI();updateChapter8UI()}", 'update ch8 ui')
once("['stage-panel','desert-panel','mansion-panel','space-panel','casino-panel','ocean-panel','forge-panel']", "['stage-panel','desert-panel','mansion-panel','space-panel','casino-panel','ocean-panel','forge-panel','boxing-panel']", 'hide boxing panel')
once("mode==='forge-select';if(!stageWas)", "mode==='forge-select'||mode==='boxing-select';if(!stageWas)", 'boxing stageWas')
once("$('chapter7-entry').hidden=false}", "$('chapter7-entry').hidden=false;$('chapter8-entry').hidden=false}", 'restore ch8 button')

# chapter8 click and stage click handlers
once("$('chapter7-entry').onclick=()=>{if(!chapter7Unlocked())return;if(mode==='ocean'||mode==='ocean-select')resetOceanTransient();mode='forge-select';updateSelection();window.scrollTo({top:0,behavior:'auto'})};", "$('chapter7-entry').onclick=()=>{if(!chapter7Unlocked())return;if(mode==='ocean'||mode==='ocean-select')resetOceanTransient();mode='forge-select';updateSelection();window.scrollTo({top:0,behavior:'auto'})};$('chapter8-entry').onclick=()=>{if(!chapter8Unlocked())return;if(mode==='forge'||mode==='forge-select')resetForgeTransient();mode='boxing-select';updateSelection();window.scrollTo({top:0,behavior:'auto'})};", 'chapter8 click')
once("$('forge-1').onclick=()=>startForgeStage(1);$('forge-2').onclick=()=>startForgeStage(2);$('forge-3').onclick=()=>startForgeStage(3);", "$('forge-1').onclick=()=>startForgeStage(1);$('forge-2').onclick=()=>startForgeStage(2);$('forge-3').onclick=()=>startForgeStage(3);$('boxing-1').onclick=()=>startBoxingStage(1);$('boxing-2').onclick=()=>startBoxingStage(2);$('boxing-3').onclick=()=>startBoxingStage(3);", 'boxing stage clicks')

# Boxing stage functions before start()
boxing_funcs="""let boxingStageNo=1;
function resetBoxingTransient(){boxingStageNo=1;if(engine){engine.boxingMode=false;engine.desertWaveMode=false}}
function startBoxingStage(n){boxingStageNo=n;mode='boxing';if(n===1){engine=new Engine('boxer','boxing_master',Math.random,{mode:'control'})}else if(n===2){engine=new Engine('boxer','smith',Math.random,{mode:'control'})}else{engine=new Engine('boxer','psychic',Math.random,{mode:'control'});const boss=engine.fighters[1];boss.hp=1000;boss.health=1000;boss.psychicPushNext=5}engine.boxingMode=true;engine.desertWaveMode=true;paused=false;acc=0;last=performance.now();lastHits=0;lastMessage='';hideStageSelectionPanels();$('selection').hidden=true;$('battle').hidden=false;$('result').hidden=true;$('pause-label').hidden=true;$('pause').disabled=false;$('pause').textContent='일시정지';resetStick();refreshControlUI();$('squad-hud').hidden=true;$('relay-hud').hidden=true;$('score-label0').textContent='🥊 복서';$('score-label1').textContent=n===1?'🫡 사부':n===2?'⚒️ 라이벌 대장장이':'🧘‍♂️ 초능력자';$('battle-mode').textContent='BOXING '+n;$('battle-info').textContent=n===1?'CHAPTER 8 STAGE 1 · 사부 HP 1000 · 복서와 같은 돌진/근접 전투 · 어퍼컷 없음.':n===2?'CHAPTER 8 STAGE 2 · 라이벌 대장장이와 결투. 강화와 제작무기를 모두 사용.':'CHAPTER 8 STAGE 3 · 초능력자 HP 1000 · 염력탄 20/2초+넉백 · 5초마다 벽 밀치기 50+기절 1초 · 적 투사체를 궤도로 포획 · 궤도탄 벽 접촉 시 초능력자 즉시 승리 · 클리어 시 10% 획득.';fit();hud();draw();window.scrollTo({top:0,behavior:'auto'});playSfx('start')}
function updateBoxingStage(){if(mode!=='boxing'||!engine||engine.result!==null)return;const hero=engine.fighters.find(f=>f.team===0&&!f.summon);if(!hero||hero.health<=0){engine.result=1;return}const enemy=engine.fighters.find(f=>f.team===1&&!f.summon);if(!enemy||enemy.health<=0)engine.result=0}

"""
once("\n\nfunction start(){", "\n\n"+boxing_funcs+"function start(){", 'boxing functions')

# reset boxing when switching/start/selection
once("if(mode==='ocean'||mode==='ocean-select')resetOceanTransient();engine=null;mode=next", "if(mode==='ocean'||mode==='ocean-select')resetOceanTransient();if(mode==='boxing'||mode==='boxing-select')resetBoxingTransient();engine=null;mode=next", 'switch reset boxing')
once("if(mode==='forge'||mode==='forge-select'){resetForgeTransient();mode='duel'}engine=", "if(mode==='forge'||mode==='forge-select'){resetForgeTransient();mode='duel'}if(mode==='boxing'||mode==='boxing-select'){resetBoxingTransient();mode='duel'}engine=", 'start reset boxing')
once("if(mode==='forge'||mode==='forge-select'){resetForgeTransient();mode='duel'}engine=null;", "if(mode==='forge'||mode==='forge-select'){resetForgeTransient();mode='duel'}if(mode==='boxing'||mode==='boxing-select'){resetBoxingTransient();mode='duel'}engine=null;", 'selection reset boxing')
# rematch
once("mode==='forge'?startForgeStage(forgeStageNo):start();", "mode==='forge'?startForgeStage(forgeStageNo):mode==='boxing'?startBoxingStage(boxingStageNo):start();", 'boxing rematch')

# control label boxer in boxing
once("mode==='forge'?'대장장이 이동 · '+controlName():'왼쪽 캐릭터 이동", "mode==='forge'?'대장장이 이동 · '+controlName():mode==='boxing'?'복서 이동 · '+controlName():'왼쪽 캐릭터 이동", 'boxing control label')

# Draw boxing background + labels
once("!['stage','desert','mansion','space','casino','ocean','forge'].includes(mode)", "!['stage','desert','mansion','space','casino','ocean','forge','boxing'].includes(mode)", 'wardrobe bg boxing exclude')
once("}else if(mode==='forge'){const fg=", "}else if(mode==='boxing'){const bg=ctx.createLinearGradient(0,0,0,720);bg.addColorStop(0,'#1b2430');bg.addColorStop(.55,'#10151c');bg.addColorStop(1,'#090c11');ctx.fillStyle=bg;ctx.fillRect(0,0,720,720);ctx.save();ctx.globalAlpha=.68;ctx.strokeStyle='#e7e7e7';ctx.lineWidth=5;for(const y of [105,135,165]){ctx.beginPath();ctx.moveTo(55,y);ctx.lineTo(665,y);ctx.stroke();ctx.beginPath();ctx.moveTo(55,720-y);ctx.lineTo(665,720-y);ctx.stroke()}ctx.strokeStyle='#d94c4c';ctx.lineWidth=8;ctx.strokeRect(48,48,624,624);ctx.font='44px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🥊',92,105);ctx.fillText('🥊',628,615);ctx.restore()}else if(mode==='forge'){const fg=", 'boxing background')
once("mode==='forge'?'#8a4b2a':'#1c2d42'", "mode==='forge'?'#8a4b2a':mode==='boxing'?'#7f3940':'#1c2d42'", 'boxing grid color')
once("mode==='forge'?'FORGE · STAGE '+forgeStageNo:mode==='stage'", "mode==='forge'?'FORGE · STAGE '+forgeStageNo:mode==='boxing'?'BOXING GYM · STAGE '+boxingStageNo:mode==='stage'", 'boxing arena label')

# Result handling: CH7 unlock CH8 + boxing results
once("markForgeStage(forgeStageNo);tryUnlockDetective();$('winner-icon').textContent='🔨';$('winner').textContent='CHAPTER 7 · STAGE '+forgeStageNo+' 클리어!';$('summary').textContent=t+'초 · 대장간 방어 성공 · 🪙 '+baseReward+'코인 획득!'+(bonus?' · 👑 왕도깨비 추가 보상 🪙 100코인! · 총 150코인':'')", "const chapter8Now=markForgeStage(forgeStageNo);tryUnlockDetective();$('winner-icon').textContent='🔨';$('winner').textContent='CHAPTER 7 · STAGE '+forgeStageNo+' 클리어!';$('summary').textContent=t+'초 · 대장간 방어 성공 · 🪙 '+baseReward+'코인 획득!'+(bonus?' · 👑 왕도깨비 추가 보상 🪙 100코인! · 총 150코인':'')+(chapter8Now?' · 🥊 CHAPTER 8 해금!':'')", 'ch7 unlock ch8')
once("else if(mode==='forge'){$('winner-icon').textContent='👹';$('winner').textContent='CHAPTER 7 · STAGE '+forgeStageNo+' 실패';$('summary').textContent=t+'초 · 대장장이가 쓰러졌어. 대장간을 다시 지켜 봐.'}else{", "else if(mode==='forge'){$('winner-icon').textContent='👹';$('winner').textContent='CHAPTER 7 · STAGE '+forgeStageNo+' 실패';$('summary').textContent=t+'초 · 대장장이가 쓰러졌어. 대장간을 다시 지켜 봐.'}else if(mode==='boxing'&&engine.result===0){const coinReward=awardStageCoins(boxingStageNo),psyRoll=boxingStageNo===3?tryUnlockPsychic():null;markBoxingStage(boxingStageNo);tryUnlockDetective();$('winner-icon').textContent='🥊';$('winner').textContent='CHAPTER 8 · STAGE '+boxingStageNo+' 클리어!';$('summary').textContent=t+'초 · 복싱장 승리 · 🪙 '+coinReward+'코인 획득!'+(psyRoll==='won'?' · 🎁 10% 보상 성공! 🧘‍♂️ 초능력자 획득!':psyRoll==='miss'?' · 🎲 초능력자 획득 실패 (10%)':'')}else if(mode==='boxing'){$('winner-icon').textContent='🥊';$('winner').textContent='CHAPTER 8 · STAGE '+boxingStageNo+' 실패';$('summary').textContent=t+'초 · 복서가 쓰러졌어. 다시 도전해 봐.'}else{", 'boxing result')

# Loop update + init chapter8
once("updateOceanStage();updateForgeStage();hud()", "updateOceanStage();updateForgeStage();updateBoxingStage();hud()", 'boxing loop')
once("updateChapter6UI();updateCasinoSystemUI();", "updateChapter6UI();updateChapter7UI();updateChapter8UI();updateCasinoSystemUI();", 'init chapter8')

p.write_text(s,encoding='utf-8')
print('v3.66 patch applied')
