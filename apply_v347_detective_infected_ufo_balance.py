from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(a,b,count=1):
    global s
    n=s.count(a)
    if n<count: raise SystemExit(f'missing pattern: {a[:120]!r}')
    s=s.replace(a,b,count)

# version + notes
rep('BATTLE <b>v3.46</b>','BATTLE <b>v3.47</b>')
rep('📒 패치노트 · v3.46</summary><div class="patch-body">',
    '📒 패치노트 · v3.47</summary><div class="patch-body"><div class="patch-version"><h3>v3.47 · 탐정 & 감염 UFO 샌드박스 조정</h3><ul><li>🛸👾 감염 UFO는 샌드박스에서 HP 1250, 파멸의 레이저 주기 10초로 롤백. CHAPTER 4 STAGE 3은 HP 1500 / 8초 유지.</li><li>신규 캐릭터 🕵️‍♂️ 탐정 추가. 🔎 돋보기를 2초마다 던져 피해 75.</li><li>돋보기 적중 시 일반 대상은 2초 동안 크기가 2배가 되며, 커진 대상에게 향하는 투사체는 유도 공격으로 전환. 보스는 크기 증가 면역.</li></ul></div>')

# roster: sandbox infected ufo rollback + detective
old="{id:'infected_ufo',name:'감염 UFO',icon:'🛸👾',tag:'파멸의 레이저',hp:1500,damage:350,speed:105,cooldown:10,unlock:'infectedUfo',description:'8초마다 아주 두꺼운 파멸의 레이저를 예고 후 발사해. 레이저는 맵 끝까지 관통하고 피해 350을 줘.',detail:'HP 1500 · 파멸의 레이저 350 / 8초 · 발사 전 1초 피격 예고 · 맵 관통'},"
if old not in s:
    old="{id:'infected_ufo',name:'감염 UFO',icon:'🛸👾',tag:'파멸의 레이저',hp:1500,damage:350,speed:105,cooldown:10,unlock:'infectedUfo',description:'10초마다 아주 두꺼운 파멸의 레이저를 예고 후 발사해. 레이저는 맵 끝까지 관통하고 피해 350을 줘.',detail:'HP 1500 · 파멸의 레이저 350 / 10초 · 발사 전 1초 피격 예고 · 맵 관통'},"
new="{id:'infected_ufo',name:'감염 UFO',icon:'🛸👾',tag:'파멸의 레이저',hp:1250,damage:350,speed:105,cooldown:10,unlock:'infectedUfo',description:'샌드박스에서는 10초마다 아주 두꺼운 파멸의 레이저를 예고 후 발사해. 피해 350.',detail:'HP 1250 · 파멸의 레이저 350 / 10초 · 발사 전 1초 피격 예고 · 맵 관통'},\n{id:'detective',name:'탐정',icon:'🕵️‍♂️',tag:'돋보기 · 추적 표식',hp:1000,damage:75,speed:150,cooldown:2,unlock:'detective',description:'2초마다 🔎 돋보기를 던져 피해 75. 적중한 일반 적은 2초 동안 몸집이 2배가 되고, 그동안 그 적을 향하는 투사체는 유도 공격으로 바뀐다. 보스는 크기 증가에 면역.',detail:'HP 1000 · 🔎 피해 75 / 2초 · 일반 적 2초간 크기 2배 · 확대 중 해당 적을 향하는 투사체 유도 · 보스 크기 증가 면역'},"
rep(old,new)

# unlock storage/state
rep("INFECTED_UFO_UNLOCK_KEY='neonRumble.infectedUfoUnlocked.v1',LEGACY_SKELETON_UNLOCK_KEY", "INFECTED_UFO_UNLOCK_KEY='neonRumble.infectedUfoUnlocked.v1',DETECTIVE_UNLOCK_KEY='neonRumble.detectiveUnlocked.v1',LEGACY_SKELETON_UNLOCK_KEY")
rep('zombieMageUnlocked=false,infectedUfoUnlocked=false;', 'zombieMageUnlocked=false,infectedUfoUnlocked=false,detectiveUnlocked=false;')
rep("infectedUfoUnlocked=localStorage.getItem(INFECTED_UFO_UNLOCK_KEY)==='1'", "infectedUfoUnlocked=localStorage.getItem(INFECTED_UFO_UNLOCK_KEY)==='1';detectiveUnlocked=localStorage.getItem(DETECTIVE_UNLOCK_KEY)==='1'")
rep("(c?.unlock==='infectedUfo'&&!infectedUfoUnlocked)||(c?.unlock==='moneyManShop'", "(c?.unlock==='infectedUfo'&&!infectedUfoUnlocked)||(c?.unlock==='detective'&&!detectiveUnlocked)||(c?.unlock==='moneyManShop'")
rep("function tryUnlockInfectedUfo(){if(infectedUfoUnlocked)return 'already';if(Math.random()>=.05)return 'miss';infectedUfoUnlocked=true;try{localStorage.setItem(INFECTED_UFO_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return 'won'}",
    "function tryUnlockInfectedUfo(){if(infectedUfoUnlocked)return 'already';if(Math.random()>=.05)return 'miss';infectedUfoUnlocked=true;try{localStorage.setItem(INFECTED_UFO_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return 'won'}\nfunction tryUnlockDetective(){if(detectiveUnlocked)return 'already';if(Math.random()>=.03)return 'miss';detectiveUnlocked=true;try{localStorage.setItem(DETECTIVE_UNLOCK_KEY,'1')}catch{}if($('character-search'))$('character-search').value='';refreshUnlockCards();return 'won'}")

# silent 3% roll on every stage clear
rep("const coinReward=awardStageCoins(stageNo),unlockedNow=stageNo===2?unlockControlBoss():false,chapterNow=markRobotStage(stageNo);", "const coinReward=awardStageCoins(stageNo),unlockedNow=stageNo===2?unlockControlBoss():false,chapterNow=markRobotStage(stageNo);tryUnlockDetective();")
rep("const coinReward=awardStageCoins(desertStageNo),chapter3Now=markDesertStage(desertStageNo),skNow=desertStageNo===3?unlockSkeletons():false,mageRoll=desertStageNo===3?tryUnlockSkeletonMage():null;", "const coinReward=awardStageCoins(desertStageNo),chapter3Now=markDesertStage(desertStageNo),skNow=desertStageNo===3?unlockSkeletons():false,mageRoll=desertStageNo===3?tryUnlockSkeletonMage():null;tryUnlockDetective();")
rep("const coinReward=awardStageCoins(mansionStageNo),zRoll=mansionStageNo===3?tryUnlockZombieMage():null,chapter4Now=markMansionStage(mansionStageNo);", "const coinReward=awardStageCoins(mansionStageNo),zRoll=mansionStageNo===3?tryUnlockZombieMage():null,chapter4Now=markMansionStage(mansionStageNo);tryUnlockDetective();")
rep("const coinReward=awardStageCoins(spaceStageNo),ufoRoll=spaceStageNo===3?tryUnlockInfectedUfo():null;", "const coinReward=awardStageCoins(spaceStageNo),ufoRoll=spaceStageNo===3?tryUnlockInfectedUfo():null;tryUnlockDetective();")

# infected UFO interval becomes per fighter: sandbox 10, stage override 8
oldskill="infectedUfoSkill(f,e){if(f.id!=='infected_ufo'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0)return;if(!Number.isFinite(f.doomNext))f.doomNext=this.time+8;"
rep(oldskill,"infectedUfoSkill(f,e){if(f.id!=='infected_ufo'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0)return;const doomInterval=f.doomInterval||10;if(!Number.isFinite(f.doomNext))f.doomNext=this.time+doomInterval;")
rep("f.doomNext=this.time+8;this.emit('🛸👾 파멸의 레이저 발사! 피해 350')", "f.doomNext=this.time+doomInterval;this.emit('🛸👾 파멸의 레이저 발사! 피해 350')")
rep("boss.hp=1500;boss.health=1500;boss.doomNext=10", "boss.hp=1500;boss.health=1500;boss.doomInterval=8;boss.doomNext=8")
rep("감염 UFO가 10초마다 1초 피격 예고", "감염 UFO가 8초마다 1초 피격 예고")

# detective attack method + magnifier hit effect
needle="moneyManSkill(f,e){"
insert="detectiveSkill(f,e){if(f.id!=='detective'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0||f.cd>1e-9)return;const a=this.aim(f,e);this.shots.push({x:f.x+a.x*(f.radius+8),y:f.y+a.y*(f.radius+8),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'magnifier',radius:8*f.scale,speed:330*f.scale,damage:75*f.scale,life:5,bounces:0});f.cd=2/f.scale;f.attack=.18/f.scale;this.effect(f,'🔎 돋보기!','skill')}\n"
rep(needle,insert+needle)
rep("if(f.id==='moneyman')this.moneyManSkill(f,e);", "if(f.id==='moneyman')this.moneyManSkill(f,e);if(f.id==='detective')this.detectiveSkill(f,e);")
rep("if(s.kind==='moneybag'){if(e.health>0)this.applyMoneyHappiness(e,2);", "if(s.kind==='magnifier'&&e.health>0&&!e.boss){if(!((e.magnifiedUntil||0)>this.time)){e.magnifyBaseRadius=e.radius;e.radius*=2}e.magnifiedUntil=this.time+2;this.effect(e,'🔎 확대 2초!','skill')}if(s.kind==='moneybag'){if(e.health>0)this.applyMoneyHappiness(e,2);")

# restore size each frame before skill dispatch
rep("this.transformHero(f);this.updateVampire(f);", "if((f.magnifiedUntil||0)>0&&this.time>=f.magnifiedUntil){if(f.magnifyBaseRadius)f.radius=f.magnifyBaseRadius;f.magnifiedUntil=0;f.magnifyBaseRadius=0}this.transformHero(f);this.updateVampire(f);")

# while target is enlarged, projectile steers toward it
rep("if((s.kind==='magic'||s.kind==='curseorb'||s.kind==='zombiemagic')&&target){", "if((s.kind==='magic'||s.kind==='curseorb'||s.kind==='zombiemagic'||((target?.magnifiedUntil||0)>this.time))&&target){")

p.write_text(s,encoding='utf-8')
print('v3.47 patch applied')
