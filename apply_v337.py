from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n < count:
        raise SystemExit(f'replace mismatch expected >= {count}, found {n}: {old[:180]!r}')
    s=s.replace(old,new,count)

# Visible version and patch notes.
rep('BATTLE <b>v3.36</b>','BATTLE <b>v3.37</b>')
rep('📒 패치노트 · v3.36','📒 패치노트 · v3.37')
needle='<div class="patch-body"><div class="patch-version"><h3>v3.36 · 그림자의 분신, 사막 군단의 재편</h3>'
notes='''<div class="patch-body"><div class="patch-version"><h3>v3.37 · 화염을 가르는 소방대, 더 빨라진 해골 군단</h3><ul><li>해골들: 취한 해골 공격 간격 1.5초 → 1초.</li><li>해골들: 총잡이 해골 공격 간격 2초 → 1.5초.</li><li>쿨가이: 샤우팅 공격 간격 8초 → 4초.</li><li>버그 수정: 달의 반달 조각이 기사 방패에 막혀 소멸해도 즉시 회수 상태로 복구되어 다시 공격 가능.</li><li>신규 캐릭터 👨‍🚒 소방관: 화상 완전 면역. 근접 시 🪓 소방도끼로 피해 70 / 0.5초.</li><li>소방관: 15초마다 HP 500의 🚒 소방차에 탑승하며 10초 동안 유지. 탑승 중 0.3초마다 물을 발사해 적에게 피해 10.</li><li>소방차: 화상 상태의 아군을 최우선으로 물 공격. 해당 아군의 화상을 즉시 치료하고 물 피해량과 같은 HP 10을 회복.</li></ul></div><div class="patch-version"><h3>v3.36 · 그림자의 분신, 사막 군단의 재편</h3>'''
rep(needle,notes)

# Balance data/text.
rep("{id:'coolguy',name:'쿨가이',icon:'👤',tag:'부채꼴 샤우팅',hp:1000,damage:200,speed:160,cooldown:8,description:'8초마다 가장 가까운 적 방향으로 자기 몸에서 시작하는 부채꼴 샤우팅 공격을 해. 범위 안 모든 적에게 피해 200을 주며 공격 순간 🗣️ 모습으로 변해.',detail:'HP 1000 · 부채꼴 샤우팅 200 · 공격 주기 8초 · 범위 내 모든 적 타격 · 공격 중 🗣️ 변신 · 전용 웅장한 샤우팅 사운드'},",
    "{id:'coolguy',name:'쿨가이',icon:'👤',tag:'부채꼴 샤우팅',hp:1000,damage:200,speed:160,cooldown:4,description:'4초마다 가장 가까운 적 방향으로 자기 몸에서 시작하는 부채꼴 샤우팅 공격을 해. 범위 안 모든 적에게 피해 200을 주며 공격 순간 🗣️ 모습으로 변해.',detail:'HP 1000 · 부채꼴 샤우팅 200 · 공격 주기 4초 · 범위 내 모든 적 타격 · 공격 중 🗣️ 변신 · 전용 웅장한 샤우팅 사운드'},")
rep("{id:'skeleton_gun',name:'총잡이 해골',icon:'💀',tag:'🔫 회전총',hp:125,damage:70,speed:155,cooldown:2,stageOnly:true,description:'몸 주위를 도는 총이 가장 가까운 적을 향해 2초마다 피해 70의 총알을 발사해.',detail:'HP 125 · 🔫 회전총 · 총알 70 / 2초'},",
    "{id:'skeleton_gun',name:'총잡이 해골',icon:'💀',tag:'🔫 회전총',hp:125,damage:70,speed:155,cooldown:1.5,stageOnly:true,description:'몸 주위를 도는 총이 가장 가까운 적을 향해 1.5초마다 피해 70의 총알을 발사해.',detail:'HP 125 · 🔫 회전총 · 총알 70 / 1.5초'},")
rep("{id:'skeleton_drunk',name:'취한 해골',icon:'💀',tag:'🍺 비틀비틀 조준',hp:125,damage:100,speed:145,cooldown:1.5,stageOnly:true,description:'맥주잔이 적을 노리지만 술에 취해 조준 오차가 커. 1.5초마다 빗나가기 쉬운 맥주 공격으로 피해 100을 노려.',detail:'HP 125 · 🍺 피해 100 · 쿨타임 1.5초 · 낮은 명중률'},",
    "{id:'skeleton_drunk',name:'취한 해골',icon:'💀',tag:'🍺 비틀비틀 조준',hp:125,damage:100,speed:145,cooldown:1,stageOnly:true,description:'맥주잔이 적을 노리지만 술에 취해 조준 오차가 커. 1초마다 빗나가기 쉬운 맥주 공격으로 피해 100을 노려.',detail:'HP 125 · 🍺 피해 100 · 쿨타임 1초 · 낮은 명중률'},")
rep("detail:'💀 해골들 · 3마리 동시 출전 · 각 HP 125 · 총 3라운드 · 🔫70/2초 · 🗡️70/3초 · 🍺100/1.5초 · 상대 HP 라운드 간 유지'",
    "detail:'💀 해골들 · 3마리 동시 출전 · 각 HP 125 · 총 3라운드 · 🔫70/1.5초 · 🗡️70/3초 · 🍺100/1초 · 상대 HP 라운드 간 유지'")

# New firefighter roster entry.
firefighter="""{id:'firefighter',name:'소방관',icon:'👨‍🚒',tag:'화상 면역 · 소방도끼 · 소방차',hp:1000,damage:70,speed:160,cooldown:.5,description:'화상에 완전히 면역이야. 적이 가까이 오면 🪓 소방도끼로 피해 70을 주며 0.5초마다 휘둘러. 15초마다 HP 500의 🚒 소방차를 타고 10초 동안 물을 뿌려.',detail:'HP 1000 · 화상 면역 · 🪓 70 / 0.5초 · 🚒 15초마다 탑승 · 소방차 HP 500 · 유지 10초 · 💧 피해 10 / 0.3초 · 화상 아군 우선 치료 + HP 10'},
"""
rep("{id:'skeleton_mage',name:'해골 법사'",firefighter+"{id:'skeleton_mage',name:'해골 법사'")

# Runtime balance.
rep("f.coolGuyNext=this.time+8/f.scale", "f.coolGuyNext=this.time+4/f.scale")
rep("coolGuyNext:type.id==='coolguy'?8/scale:9999", "coolGuyNext:type.id==='coolguy'?4/scale:9999")
rep("f.cd=2/f.scale;f.attack=.16/f.scale;this.effect(f,'🔫 70','skill')", "f.cd=1.5/f.scale;f.attack=.16/f.scale;this.effect(f,'🔫 70','skill')")
rep("f.cd=1.5/f.scale;f.attack=.18/f.scale;this.effect(f,'🍺 비틀!','skill')", "f.cd=1/f.scale;f.attack=.18/f.scale;this.effect(f,'🍺 비틀!','skill')")

# Moon shield recovery bug.
old="blockProjectileWithKnight(f,s,owner){const raw=s.instant?f.health:(s.damage||0);s.life=0;f.knightBlockedDamage+=Math.max(0,raw);this.effect(f,this.time<f.knightShieldChargedUntil-1e-9?'🛡️ 완전 방어!':'🛡️ 방패 막기!','skill');if(f.knightBlockedDamage>=500){f.knightBlockedDamage=0;this.knightShockwave(f)}if(owner){owner.attack=.12/owner.scale}return true}"
new="blockProjectileWithKnight(f,s,owner){const raw=s.instant?f.health:(s.damage||0);s.life=0;if(s.kind==='moon'&&owner){owner.moonShot=null;owner.moonHalf=false;owner.icon='🌝';this.effect(owner,'반달 조각 회수!','skill')}f.knightBlockedDamage+=Math.max(0,raw);this.effect(f,this.time<f.knightShieldChargedUntil-1e-9?'🛡️ 완전 방어!':'🛡️ 방패 막기!','skill');if(f.knightBlockedDamage>=500){f.knightBlockedDamage=0;this.knightShockwave(f)}if(owner){owner.attack=.12/owner.scale}return true}"
rep(old,new)

# Fire immunity.
rep("applyBurn(f,e,friendly=false){if(e.id==='phoenix'||e.id==='moai')return;", "applyBurn(f,e,friendly=false){if(e.id==='phoenix'||e.id==='moai'||e.id==='firefighter')return;")
rep("tickBurn(e){if(e.id==='phoenix'||e.id==='moai'){e.burn=null;return}", "tickBurn(e){if(e.id==='phoenix'||e.id==='moai'||e.id==='firefighter'){e.burn=null;return}")

# Firetruck shield: while mounted, incoming direct attacks damage the truck instead of the firefighter.
attack_anchor="if(e.id==='invisible'&&!bypassDodge){if(this.random()<e.dodgeChance){e.dodgeChance=.5;this.effect(e,'공격 무시!','skill');const reflected=50*e.scale;this.attack(e,f,reflected,false,true);return 0}else{e.dodgeChance=Math.min(1,e.dodgeChance+.1);this.effect(e,'회피 '+Math.round(e.dodgeChance*100)+'%','skill')}}\n f.attack=.35/f.scale;f.cd=f.cooldown;"
attack_new="if(e.id==='invisible'&&!bypassDodge){if(this.random()<e.dodgeChance){e.dodgeChance=.5;this.effect(e,'공격 무시!','skill');const reflected=50*e.scale;this.attack(e,f,reflected,false,true);return 0}else{e.dodgeChance=Math.min(1,e.dodgeChance+.1);this.effect(e,'회피 '+Math.round(e.dodgeChance*100)+'%','skill')}}\n if(e.id==='firefighter'&&e.firetruckMounted&&e.firetruckHp>0){const n=Math.min(e.firetruckHp,Math.max(0,Math.round(dmg*(1-e.armor))));e.firetruckHp-=n;f.damageDealt+=n;f.hits++;f.attack=.35/f.scale;f.cd=f.cooldown;this.effect(e,'🚒 −'+n,'hit');if(e.firetruckHp<=0){e.firetruckMounted=false;e.firetruckUntil=0;e.icon='👨‍🚒';this.effect(e,'🚒 소방차 파괴!','skill');this.emit('🚒 소방차가 파괴됐어!')}return n}\n f.attack=.35/f.scale;f.cd=f.cooldown;"
rep(attack_anchor,attack_new)

# Firefighter skill before skeletonSkill.
anchor="skeletonSkill(f,e){\n"
fire_skill="""firefighterSkill(f,e){
 if(f.id!=='firefighter'||f.health<=0)return;
 if(!Number.isFinite(f.firetruckNext)){f.firetruckNext=this.time+15/f.scale;f.firetruckUntil=0;f.firetruckMounted=false;f.firetruckHp=0;f.firefighterWaterNext=0}
 if(f.firetruckMounted&&(this.time>=f.firetruckUntil-1e-9||f.firetruckHp<=0)){f.firetruckMounted=false;f.firetruckUntil=0;f.icon='👨‍🚒';this.effect(f,'🚒 하차','skill')}
 if(!f.firetruckMounted&&this.time>=f.firetruckNext-1e-9){f.firetruckMounted=true;f.firetruckHp=500*(f.boss?2.5:1);f.firetruckUntil=this.time+10/f.scale;f.firetruckNext=this.time+15/f.scale;f.firefighterWaterNext=this.time;f.icon='🚒';this.effect(f,'🚒 소방차 탑승!','skill');this.emit('👨‍🚒 소방관이 소방차에 탑승!')}
 if(f.firetruckMounted){
  if(this.time<f.firefighterWaterNext-1e-9)return;f.firefighterWaterNext=this.time+.3/f.scale;
  const burning=this.fighters.filter(a=>a!==f&&a.team===f.team&&a.health>0&&a.burn).sort((a,b)=>distance(f,a)-distance(f,b))[0];
  if(burning){burning.burn=null;const heal=Math.min(10*f.scale,burning.hp-burning.health);burning.health+=heal;burning.healed+=heal;this.effect(burning,'💧 화상 치료 +'+Math.round(heal),'heal');this.effect(f,'🚒 아군 진화!','skill');return}
  if(!e||e.health<=0)return;const a=this.aim(f,e);this.shots.push({x:f.x+a.x*(f.radius+10),y:f.y+a.y*(f.radius+10),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'water',radius:7*f.scale,speed:430*f.scale,damage:10*f.scale,life:3,bounces:0});f.attack=.1/f.scale;return
 }
 if(f.cd<=1e-9&&e&&e.health>0&&distance(f,e)<=f.radius+e.radius+42*f.scale){const dealt=this.attack(f,e,70*f.scale);if(dealt>0){f.cd=.5/f.scale;this.effect(f,'🪓 70','skill')}}
}
"""
rep(anchor,fire_skill+anchor)

# Invoke firefighter skill and exclude from generic body attacks.
rep("if(f.id==='coolguy')this.coolGuySkill(f,e);if(f.id.startsWith('skeleton_'))this.skeletonSkill(f,e);",
    "if(f.id==='coolguy')this.coolGuySkill(f,e);if(f.id==='firefighter')this.firefighterSkill(f,e);if(f.id.startsWith('skeleton_'))this.skeletonSkill(f,e);")
rep("'ghost','cowboy','chef','coolguy','skeleton_gun'", "'ghost','cowboy','chef','coolguy','firefighter','skeleton_gun'")

p.write_text(s,encoding='utf-8')
print('v3.37 patch applied')
