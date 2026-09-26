from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n < count:
        raise SystemExit(f'replace mismatch expected >= {count}, found {n}: {old[:180]!r}')
    s=s.replace(old,new,count)

# Patch notes: keep visible version v3.38, add emergency hotfix bullets.
needle="<div class=\"patch-body\"><div class=\"patch-version\"><h3>v3.38 · 피의 저택, 좀비 반란의 밤</h3><ul>"
insert="<div class=\"patch-body\"><div class=\"patch-version\"><h3>v3.38 · 피의 저택, 좀비 반란의 밤</h3><ul><li>긴급 패치: 여자 뱀파이어가 CHAPTER 3의 STAGE 1·2·3 모두 출전하며 HP 1000으로 강화.</li><li>긴급 패치: CHAPTER 3 STAGE 1에서 웨이브 클리어 시 살아 있는 모든 아군이 각자 최대 체력의 30% 회복.</li>"
rep(needle,insert)

# Female Vampire HP 500 -> 1000 in all Chapter 3 stages.
old="function spawnFemaleVampire(){const hero=engine.fighters.find(f=>f.team===0&&!f.summon),v={...hero};v.side=engine.fighters.length;v.team=0;v.summon=true;v.ownerSide=hero.side;v.femaleVampire=true;v.icon='🧛‍♀️';v.name='여자 뱀파이어';v.hp=500;v.health=500;v.boss=false;v.scale=1;v.bodyScale=1;v.radius=33;v.x=150;v.y=500;v.vx=0;v.vy=-1;v.poison=null;v.toxin=null;v.burn=null;v.curse=null;v.trail=[];v.deathOrder=null;v.vampireBat=false;engine.fighters.push(v);return v}"
new="function spawnFemaleVampire(){const hero=engine.fighters.find(f=>f.team===0&&!f.summon),v={...hero};v.side=engine.fighters.length;v.team=0;v.summon=true;v.ownerSide=hero.side;v.femaleVampire=true;v.icon='🧛‍♀️';v.name='여자 뱀파이어';v.hp=1000;v.health=1000;v.boss=false;v.scale=1;v.bodyScale=1;v.radius=33;v.x=150;v.y=500;v.vx=0;v.vy=-1;v.poison=null;v.toxin=null;v.burn=null;v.curse=null;v.trail=[];v.deathOrder=null;v.vampireBat=false;engine.fighters.push(v);return v}"
rep(old,new)

# Stage 3 also gets the female Vampire ally.
old="}else{engine=new Engine('vampire','zombie_mage',Math.random,{mode:'control'});const m=engine.fighters[1];m.hp=2000;m.health=2000;m.bodyScale=1.5;m.radius=49.5;m.speed=105}engine.desertWaveMode=true;"
new="}else{engine=new Engine('vampire','zombie_mage',Math.random,{mode:'control'});const m=engine.fighters[1];m.hp=2000;m.health=2000;m.bodyScale=1.5;m.radius=49.5;m.speed=105;spawnFemaleVampire()}engine.desertWaveMode=true;"
rep(old,new)

# Update battle labels/info to reflect female Vampire in Stage 3 and HP 1000 everywhere.
rep("$('score-label0').textContent=n<3?'🧛 흡혈귀 + 🧛‍♀️':'🧛 흡혈귀';", "$('score-label0').textContent='🧛 흡혈귀 + 🧛‍♀️';")
rep("$('battle-info').textContent=n===1?'CHAPTER 3 STAGE 1 · 좀비 5마리씩 총 5웨이브. 여자 뱀파이어 HP 500 지원.':n===2?'CHAPTER 3 STAGE 2 · 왕좀비 HP 1500 · 3초마다 좀비 소환 · 여자 뱀파이어 지원.':'CHAPTER 3 STAGE 3 · 법사좀비 HP 2000 · 2초마다 유도탄 85 · 명중 시 미니좀비 소환.';",
    "$('battle-info').textContent=n===1?'CHAPTER 3 STAGE 1 · 좀비 5마리씩 총 5웨이브. 여자 뱀파이어 HP 1000 지원 · 웨이브 클리어 시 모든 아군 최대 HP 30% 회복.':n===2?'CHAPTER 3 STAGE 2 · 왕좀비 HP 1500 · 3초마다 좀비 소환 · 여자 뱀파이어 HP 1000 지원.':'CHAPTER 3 STAGE 3 · 법사좀비 HP 2000 · 2초마다 유도탄 85 · 명중 시 미니좀비 소환 · 여자 뱀파이어 HP 1000 지원.';")

# Heal all living allies by 30% max HP after every Stage 1 wave clear, including the final wave.
old="if(mansionStageNo===1){const alive=engine.fighters.some(f=>f.team===1&&f.health>0);if(!alive){if(mansionWave>=5)engine.result=0;else spawnMansionWave()}}else if(mansionStageNo===2){"
new="if(mansionStageNo===1){const alive=engine.fighters.some(f=>f.team===1&&f.health>0);if(!alive){for(const ally of engine.fighters.filter(f=>f.team===0&&f.health>0)){const before=ally.health,heal=ally.hp*.3;ally.health=Math.min(ally.hp,ally.health+heal);const actual=Math.max(0,Math.round(ally.health-before));if(actual>0){ally.healed=(ally.healed||0)+actual;engine.effect(ally,'🏰 WAVE CLEAR +'+actual,'heal')}}if(mansionWave>=5)engine.result=0;else spawnMansionWave()}}else if(mansionStageNo===2){"
rep(old,new)

# Panel copy: Stage 3 ally is now present and all female Vampire appearances use HP 1000.
rep("<small>HP 2000 · 2초마다 유도탄 85 · 명중하면 미니좀비 소환. 여자 뱀파이어는 등장하지 않아.</small>",
    "<small>HP 2000 · 2초마다 유도탄 85 · 명중하면 미니좀비 소환. HP 1000 여자 뱀파이어가 함께 싸워.</small>")
rep("<small>좀비 5마리씩 5웨이브. HP 500 여자 뱀파이어가 함께 싸워.</small>",
    "<small>좀비 5마리씩 5웨이브. HP 1000 여자 뱀파이어가 함께 싸우며 웨이브마다 모든 아군이 최대 HP 30% 회복.</small>")
rep("<small>HP 1500 · 근접 100 · 3초마다 일반 좀비 소환. 여자 뱀파이어가 지원.</small>",
    "<small>HP 1500 · 근접 100 · 3초마다 일반 좀비 소환. HP 1000 여자 뱀파이어가 지원.</small>")

p.write_text(s,encoding='utf-8')
print('v3.38 Chapter 3 vampire/wave heal hotfix applied')
