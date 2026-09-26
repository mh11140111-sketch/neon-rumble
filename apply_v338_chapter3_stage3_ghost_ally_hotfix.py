from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n < count:
        raise SystemExit(f'replace mismatch expected >= {count}, found {n}: {old[:180]!r}')
    s=s.replace(old,new,count)

# Keep visible version v3.38; append hotfix note.
needle='<div class="patch-body"><div class="patch-version"><h3>v3.38 · 피의 저택, 좀비 반란의 밤</h3><ul>'
insert='<div class="patch-body"><div class="patch-version"><h3>v3.38 · 피의 저택, 좀비 반란의 밤</h3><ul><li>긴급 패치: CHAPTER 3 STAGE 3에 HP 500의 👻 유령 아군이 추가되어 흡혈귀·여자 뱀파이어와 함께 전투.</li>'
rep(needle,insert)

# Add dedicated Stage 3 ghost ally helper next to female Vampire helper.
old="function spawnMansionWave(){mansionWave++;const spots=[[500,120],[610,235],[625,410],[535,570],[440,360]];for(const [x,y] of spots)makeMansionEnemy('zombie',x,y);$('event').textContent='🏰 WAVE '+mansionWave+' / 5 · 좀비 5마리 침입!'}"
new="function spawnMansionGhost(){const tmp=new Engine('vampire','ghost',Math.random,{mode:'control'}).fighters[1];tmp.side=engine.fighters.length;tmp.team=0;tmp.summon=true;tmp.ownerSide=0;tmp.mansionGhostAlly=true;tmp.name='유령';tmp.icon='👻';tmp.hp=500;tmp.health=500;tmp.boss=false;tmp.scale=1;tmp.bodyScale=1;tmp.radius=33;tmp.x=235;tmp.y=555;tmp.vx=0;tmp.vy=-1;tmp.trail=[];tmp.poison=null;tmp.toxin=null;tmp.burn=null;tmp.curse=null;tmp.deathOrder=null;tmp.stunUntil=0;tmp.capturedBy=null;tmp.captureTarget=null;tmp.possessedByGhost=null;engine.fighters.push(tmp);return tmp}\nfunction spawnMansionWave(){mansionWave++;const spots=[[500,120],[610,235],[625,410],[535,570],[440,360]];for(const [x,y] of spots)makeMansionEnemy('zombie',x,y);$('event').textContent='🏰 WAVE '+mansionWave+' / 5 · 좀비 5마리 침입!'}"
rep(old,new)

# Stage 3: spawn Ghost ally after female Vampire.
old="}else{engine=new Engine('vampire','zombie_mage',Math.random,{mode:'control'});const m=engine.fighters[1];m.hp=2000;m.health=2000;m.bodyScale=1.5;m.radius=49.5;m.speed=105;spawnFemaleVampire()}engine.desertWaveMode=true;"
new="}else{engine=new Engine('vampire','zombie_mage',Math.random,{mode:'control'});const m=engine.fighters[1];m.hp=2000;m.health=2000;m.bodyScale=1.5;m.radius=49.5;m.speed=105;spawnFemaleVampire();spawnMansionGhost()}engine.desertWaveMode=true;"
rep(old,new)

# HUD / battle info.
rep("$('score-label0').textContent='🧛 흡혈귀 + 🧛‍♀️';", "$('score-label0').textContent=n===3?'🧛 + 🧛‍♀️ + 👻':'🧛 흡혈귀 + 🧛‍♀️';")
rep("'CHAPTER 3 STAGE 3 · 법사좀비 HP 2000 · 2초마다 유도탄 85 · 명중 시 미니좀비 소환 · 여자 뱀파이어 HP 1000 지원.';",
    "'CHAPTER 3 STAGE 3 · 법사좀비 HP 2000 · 2초마다 유도탄 85 · 명중 시 미니좀비 소환 · 여자 뱀파이어 HP 1000 + 유령 HP 500 지원.';")

# Stage selection card.
rep('<button class="stage-card" id="mansion-3" type="button"><b>STAGE 3</b><span>🧛🧛‍♀️ VS 🧌</span><strong>법사좀비의 저주</strong><small>HP 2000 법사좀비의 유도탄과 미니좀비 소환을 돌파. HP 1000 여자 뱀파이어가 함께 싸워.</small></button>',
    '<button class="stage-card" id="mansion-3" type="button"><b>STAGE 3</b><span>🧛🧛‍♀️👻 VS 🧌</span><strong>법사좀비의 저주</strong><small>HP 2000 법사좀비를 상대해. HP 1000 여자 뱀파이어와 HP 500 유령이 함께 싸워.</small></button>')

p.write_text(s,encoding='utf-8')
print('v3.38 Chapter 3 Stage 3 ghost ally hotfix applied')
