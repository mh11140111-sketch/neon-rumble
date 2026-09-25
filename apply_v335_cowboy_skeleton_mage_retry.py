from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n!=count:
        raise SystemExit(f'replace mismatch expected {count}, found {n}: {old[:180]!r}')
    s=s.replace(old,new,count)

# Version / patch notes.
rep('BATTLE <b>v3.34</b>','BATTLE <b>v3.35</b>')
rep('📒 패치노트 · v3.34','📒 패치노트 · v3.35')
anchor='<div class="patch-body"><div class="patch-version"><h3>v3.34 · 사막의 해골 & 밸런스</h3>'
insert='<div class="patch-body"><div class="patch-version"><h3>v3.35 · 사막의 총성이 울리고, 해골 마법이 깨어나다</h3><ul><li>카우보이: 총알 피해 80 → 100.</li><li>카우보이: 총알 탄속을 일반 투사체 대비 약 1.5배 → 약 2.5배로 강화.</li><li>신규 획득 캐릭터 💀🧙 해골 법사: CHAPTER 2 STAGE 3 클리어 시 매번 10% 확률로 획득 가능.</li><li>일반 캐릭터 해골 법사: HP 700. 추적 마법탄과 10초마다 해골 1마리 소환 능력을 사용.</li><li>CHAPTER 2 STAGE 3의 보스 해골 법사는 기존 HP 1000을 유지.</li></ul></div><div class="patch-version"><h3>v3.34 · 사막의 해골 & 밸런스</h3>'
rep(anchor,insert)

# Cowboy buff: avoid matching the multiline emoji literal itself.
rep("tag:'말 탑승 · 6발 탄창',hp:1000,damage:80,speed:150,cooldown:1,description:'🐴 말을 타고 시작해 이동속도가 100% 증가해. 피해 80의 빠른 총알을 1초마다 쏘며 탄창은 6발이야. 6발을 모두 쓰면 6초 동안 재장전하고, 체력이 30% 이하가 되면 말이 사라져 이동속도 증가도 끝나.',detail:'HP 1000 · 말 탑승 중 이동속도 +100% · 총알 80 · 탄속 약 1.5배 · 1초마다 발사 · 탄창 6발 · 재장전 6초 · HP 30% 이하 말 소멸'",
    "tag:'말 탑승 · 6발 탄창',hp:1000,damage:100,speed:150,cooldown:1,description:'🐴 말을 타고 시작해 이동속도가 100% 증가해. 피해 100의 매우 빠른 총알을 1초마다 쏘며 탄창은 6발이야. 6발을 모두 쓰면 6초 동안 재장전하고, 체력이 30% 이하가 되면 말이 사라져 이동속도 증가도 끝나.',detail:'HP 1000 · 말 탑승 중 이동속도 +100% · 총알 100 · 탄속 약 2.5배 · 1초마다 발사 · 탄창 6발 · 재장전 6초 · HP 30% 이하 말 소멸'")
rep("speed:450*f.scale,damage:80*f.scale","speed:750*f.scale,damage:100*f.scale")

# Skeleton Mage rare playable unlock (stage 3 boss HP restored to 1000 below).
rep("{id:'skeleton_mage',name:'해골 법사',icon:'💀🧙',tag:'추적 마법 · 해골 소환',hp:1000,damage:65,speed:140,cooldown:1.45,stageOnly:true,description:'마법사처럼 추적 마법탄을 사용하고 10초마다 해골 1마리를 소환하는 CHAPTER 2 보스.',detail:'HP 1000 · 추적 마법탄 65 · 10초마다 해골 1마리 소환'}",
    "{id:'skeleton_mage',name:'해골 법사',icon:'💀🧙',tag:'추적 마법 · 10초 해골 소환',hp:700,damage:65,speed:140,cooldown:1.45,unlock:'skeletonMage',description:'추적 마법탄을 발사하고 10초마다 총잡이·칼잡이·취한 해골 중 1마리를 소환해. CHAPTER 2 STAGE 3 클리어 시 10% 확률로 획득할 수 있어.',detail:'HP 700 · 추적 마법탄 65 / 1.45초 · 10초마다 해골 1마리 소환 · CHAPTER 2 STAGE 3 클리어 보상 10%'}")

# Separate unlock storage.
rep("const ROBOT_STAGE_KEY='neonRumble.robotStages.v1',SKELETON_UNLOCK_KEY='neonRumble.skeletonBundleUnlocked.v2',LEGACY_SKELETON_UNLOCK_KEY='neonRumble.skeletonUnlocked.v1';\nlet robotStageMask=0,skeletonsUnlocked=false;try{localStorage.removeItem(LEGACY_SKELETON_UNLOCK_KEY);robotStageMask=Number(localStorage.getItem(ROBOT_STAGE_KEY)||0)||0;skeletonsUnlocked=localStorage.getItem(SKELETON_UNLOCK_KEY)==='1'}catch{}",
    "const ROBOT_STAGE_KEY='neonRumble.robotStages.v1',SKELETON_UNLOCK_KEY='neonRumble.skeletonBundleUnlocked.v2',SKELETON_MAGE_UNLOCK_KEY='neonRumble.skeletonMageUnlocked.v1',LEGACY_SKELETON_UNLOCK_KEY='neonRumble.skeletonUnlocked.v1';\nlet robotStageMask=0,skeletonsUnlocked=false,skeletonMageUnlocked=false;try{localStorage.removeItem(LEGACY_SKELETON_UNLOCK_KEY);robotStageMask=Number(localStorage.getItem(ROBOT_STAGE_KEY)||0)||0;skeletonsUnlocked=localStorage.getItem(SKELETON_UNLOCK_KEY)==='1';skeletonMageUnlocked=localStorage.getItem(SKELETON_MAGE_UNLOCK_KEY)==='1'}catch{}")

rep("function unlockSkeletons(){if(skeletonsUnlocked)return false;skeletonsUnlocked=true;try{localStorage.setItem(SKELETON_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';for(const b of $('roster').children){const c=ROSTER.find(v=>v.id===b.dataset.character);b.hidden=!!c?.stageOnly||(c?.unlock==='skeleton'&&!skeletonsUnlocked)}return true}",
    "function characterLocked(c){return !!c?.stageOnly||(c?.unlock==='skeleton'&&!skeletonsUnlocked)||(c?.unlock==='skeletonMage'&&!skeletonMageUnlocked)}\nfunction refreshUnlockCards(){for(const b of $('roster').children){const c=ROSTER.find(v=>v.id===b.dataset.character);b.hidden=characterLocked(c)}}\nfunction unlockSkeletons(){if(skeletonsUnlocked)return false;skeletonsUnlocked=true;try{localStorage.setItem(SKELETON_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return true}\nfunction tryUnlockSkeletonMage(){if(skeletonMageUnlocked)return 'already';if(Math.random()>=.1)return 'miss';skeletonMageUnlocked=true;try{localStorage.setItem(SKELETON_MAGE_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return 'won'}")

# Locked character visibility in roster/search/random.
rep("b.hidden=!!c.stageOnly||(c.unlock==='skeleton'&&!skeletonsUnlocked);","b.hidden=characterLocked(c);")
rep("b.hidden=!!q&&!hay.includes(q)","b.hidden=characterLocked(c)||(!!q&&!hay.includes(q))")
rep("const playable=ROSTER.filter(c=>!c.stageOnly&&(!c.unlock||skeletonsUnlocked))","const playable=ROSTER.filter(c=>!characterLocked(c))")

# Playable Skeleton Mage summons a normal skeleton every 10 sec. Stage mode keeps its own summon loop.
rep("}else if(f.id==='skeleton_mage'&&f.cd<=1e-9){this.shots.push({x:f.x+a.x*(f.radius+6),y:f.y+a.y*(f.radius+6),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'magic',radius:5*f.scale,speed:200*f.scale,damage:65*f.scale,life:5*f.scale,bounces:0});f.cd=1.45/f.scale;f.attack=.18/f.scale;this.effect(f,'💀 마법탄!','skill')}\n}",
    "}else if(f.id==='skeleton_mage'){if(f.cd<=1e-9){this.shots.push({x:f.x+a.x*(f.radius+6),y:f.y+a.y*(f.radius+6),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'magic',radius:5*f.scale,speed:200*f.scale,damage:65*f.scale,life:5*f.scale,bounces:0});f.cd=1.45/f.scale;f.attack=.18/f.scale;this.effect(f,'💀 마법탄!','skill')}if(!this.desertWaveMode){if(!Number.isFinite(f.skeletonMageSummonNext))f.skeletonMageSummonNext=this.time+10/f.scale;if(this.time>=f.skeletonMageSummonNext-1e-9){f.skeletonMageSummonNext=this.time+10/f.scale;const ids=['skeleton_gun','skeleton_sword','skeleton_drunk'],id=ids[Math.floor(this.random()*ids.length)],tmp=new Engine('boxer',id,this.random,{mode:'control'}).fighters[1],ang=this.rand(-Math.PI,Math.PI);tmp.side=this.fighters.length;tmp.team=f.team;tmp.summon=true;tmp.ownerSide=f.side;tmp.noSkeletonRevive=true;tmp.revivals=0;tmp.boss=false;tmp.scale=1;tmp.bodyScale=1;tmp.radius=33;tmp.x=clamp(f.x+Math.cos(ang)*82,55,665);tmp.y=clamp(f.y+Math.sin(ang)*82,55,665);tmp.trail=[];this.fighters.push(tmp);this.effect(f,'💀 해골 소환!','skill');this.emit('💀🧙 해골 법사가 '+tmp.name+'을 소환!')}}}\n}")

# Stage 3 boss still has 1000 HP.
rep("if(n===3){engine=new Engine('cowboy','skeleton_mage',Math.random,{mode:'control'});engine.fighters[1].noSkeletonRevive=true}",
    "if(n===3){engine=new Engine('cowboy','skeleton_mage',Math.random,{mode:'control'});engine.fighters[1].hp=1000;engine.fighters[1].health=1000;engine.fighters[1].noSkeletonRevive=true}")

# 10% acquisition roll every stage 3 clear until obtained.
rep("else if(mode==='desert'&&engine.result===0){const skNow=desertStageNo===3?unlockSkeletons():false;$('winner-icon').textContent='🏜️';$('winner').textContent='CHAPTER 2 · STAGE '+desertStageNo+' 클리어!';$('summary').textContent=t+'초 · 사막 돌파 성공'+(skNow?' · 💀 해골들 캐릭터 해금!':'')}",
    "else if(mode==='desert'&&engine.result===0){const skNow=desertStageNo===3?unlockSkeletons():false,mageRoll=desertStageNo===3?tryUnlockSkeletonMage():null;$('winner-icon').textContent='🏜️';$('winner').textContent='CHAPTER 2 · STAGE '+desertStageNo+' 클리어!';$('summary').textContent=t+'초 · 사막 돌파 성공'+(skNow?' · 💀 해골들 캐릭터 해금!':'')+(mageRoll==='won'?' · 🎁 10% 보상 성공! 💀🧙 해골 법사 획득!':mageRoll==='miss'?' · 🎲 해골 법사 획득 실패 (10%)':'')}")

p.write_text(s,encoding='utf-8')
print('v3.35 retry patch applied')
