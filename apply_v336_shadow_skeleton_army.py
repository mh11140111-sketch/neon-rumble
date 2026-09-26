from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    found=s.count(old)
    if found!=count:
        raise SystemExit(f'replace mismatch expected {count}, found {found}: {old[:180]!r}')
    s=s.replace(old,new,count)

# Visible version + patch notes
rep('<span class="badge">BATTLE <b>v3.35</b></span>','<span class="badge">BATTLE <b>v3.36</b></span>')
rep('<details class="patch-notes"><summary>📒 패치노트 · v3.35</summary><div class="patch-body"><div class="patch-version"><h3>v3.35 · 사막의 총성이 울리고, 해골 마법이 깨어나다</h3>',
    '<details class="patch-notes"><summary>📒 패치노트 · v3.36</summary><div class="patch-body"><div class="patch-version"><h3>v3.36 · 그림자 분신과 해골 군단의 역습</h3><ul><li>카우보이: 체력 1000 → 800.</li><li>닌자: 체력이 30% 이하가 되면 경기당 1회 분신 1개 소환. 분신 HP 150, 공격력은 본체의 50%.</li><li>해골들 총잡이: 공격 간격 1초 → 2초.</li><li>해골들 취한 해골: 공격 간격 3초 → 1.5초.</li><li>조정 모드 히어로: 변신 후 돌진 ↔ 후퇴 방향 전환을 자동으로 수행하도록 수정.</li><li>해골들: 보스전·릴레이·단체전에서도 총잡이+칼잡이+취한 해골 3마리가 동시에 등장하고, 세 마리 전멸 시 다음 세트가 등장하는 3라운드 규칙을 동일 적용.</li><li>보스 해골들 전용 크기: 일반 보스의 3배가 아닌 1.5배로 적용. 다른 캐릭터의 보스 크기는 기존 그대로 유지.</li></ul></div><div class="patch-version"><h3>v3.35 · 사막의 총성이 울리고, 해골 마법이 깨어나다</h3>')

# Roster balance text/data
rep("{id:'cowboy',name:'카우보이',icon:'🤠\\n🐴',tag:'말 탑승 · 6발 탄창',hp:1000,damage:100,speed:150,cooldown:1,description:'🐴 말을 타고 시작해 이동속도가 100% 증가해. 피해 100의 매우 빠른 총알을 1초마다 쏘며 탄창은 6발이야. 6발을 모두 쓰면 6초 동안 재장전하고, 체력이 30% 이하가 되면 말이 사라져 이동속도 증가도 끝나.',detail:'HP 1000 · 말 탑승 중 이동속도 +100% · 총알 100 · 탄속 약 2.5배 · 1초마다 발사 · 탄창 6발 · 재장전 6초 · HP 30% 이하 말 소멸'},",
    "{id:'cowboy',name:'카우보이',icon:'🤠\\n🐴',tag:'말 탑승 · 6발 탄창',hp:800,damage:100,speed:150,cooldown:1,description:'🐴 말을 타고 시작해 이동속도가 100% 증가해. 체력은 800. 피해 100의 매우 빠른 총알을 1초마다 쏘며 탄창은 6발이야. 6발을 모두 쓰면 6초 동안 재장전하고, 체력이 30% 이하가 되면 말이 사라져 이동속도 증가도 끝나.',detail:'HP 800 · 말 탑승 중 이동속도 +100% · 총알 100 · 탄속 약 2.5배 · 1초마다 발사 · 탄창 6발 · 재장전 6초 · HP 30% 이하 말 소멸'},")
rep("{id:'ninja',name:'닌자',icon:'🥷',tag:'표창 · 독 · 베기',hp:650,damage:10,speed:228,cooldown:.3,description:'랜덤하게 벽을 튕기며 0.3초마다 직선 표창을 던져. 10% 확률로 독표창. 가까운 적은 베기로 밀쳐내. 체력 650, 이동 속도 20% 증가.',detail:'표창 10 · 독 10초 / 0.3초마다 5 · 독 중첩 없이 시간 갱신 · 베기 40 / 재사용 0.8초'}",
    "{id:'ninja',name:'닌자',icon:'🥷',tag:'표창 · 독 · 베기 · 분신',hp:650,damage:10,speed:228,cooldown:.3,description:'랜덤하게 벽을 튕기며 0.3초마다 직선 표창을 던져. 10% 확률로 독표창. 가까운 적은 베기로 밀쳐내. 체력이 30% 이하가 되면 경기당 1회 HP 150의 분신을 소환하고, 분신 공격력은 본체의 절반이야.',detail:'HP 650 · 표창 10 · 독 10초 / 0.3초마다 5 · 베기 40 / 재사용 0.8초 · HP 30% 이하 분신 1회 · 분신 HP 150 / 공격력 50%'}")
rep("{id:'skeleton_gun',name:'총잡이 해골',icon:'💀',tag:'🔫 회전총',hp:125,damage:70,speed:155,cooldown:1,stageOnly:true,description:'몸 주위를 도는 총이 가장 가까운 적을 향해 1초마다 피해 70의 총알을 발사해.',detail:'HP 125 · 🔫 회전총 · 총알 70 / 1초'},",
    "{id:'skeleton_gun',name:'총잡이 해골',icon:'💀',tag:'🔫 회전총',hp:125,damage:70,speed:155,cooldown:2,stageOnly:true,description:'몸 주위를 도는 총이 가장 가까운 적을 향해 2초마다 피해 70의 총알을 발사해.',detail:'HP 125 · 🔫 회전총 · 총알 70 / 2초'},")
rep("{id:'skeleton_drunk',name:'취한 해골',icon:'💀',tag:'🍺 비틀비틀 조준',hp:125,damage:100,speed:145,cooldown:3,stageOnly:true,description:'맥주잔이 적을 노리지만 술에 취해 조준 오차가 커. 3초마다 빗나가기 쉬운 맥주 공격으로 피해 100을 노려.',detail:'HP 125 · 🍺 피해 100 · 쿨타임 3초 · 낮은 명중률'},",
    "{id:'skeleton_drunk',name:'취한 해골',icon:'💀',tag:'🍺 비틀비틀 조준',hp:125,damage:100,speed:145,cooldown:1.5,stageOnly:true,description:'맥주잔이 적을 노리지만 술에 취해 조준 오차가 커. 1.5초마다 빗나가기 쉬운 맥주 공격으로 피해 100을 노려.',detail:'HP 125 · 🍺 피해 100 · 쿨타임 1.5초 · 낮은 명중률'},")
rep("{id:'skeletons',name:'해골들',icon:'💀💀💀',tag:'3마리 동시 출전 · 3라운드',hp:125,damage:70,speed:155,cooldown:1,unlock:'skeleton',description:'샌드박스에서 🔫 총잡이·🗡️ 칼잡이·🍺 취한 해골 3마리가 한 세트로 동시에 출전해. 3마리가 모두 쓰러지면 새 세트가 등장하며 총 3라운드까지 진행돼. 다음 라운드로 넘어가도 상대 체력은 절대 회복되지 않아.',detail:'💀 해골들 · 3마리 동시 출전 · 각 HP 125 · 총 3라운드 · 🔫70/1초 · 🗡️70/3초 · 🍺100/3초 · 상대 HP 라운드 간 유지'},",
    "{id:'skeletons',name:'해골들',icon:'💀💀💀',tag:'3마리 동시 출전 · 3라운드',hp:125,damage:70,speed:155,cooldown:2,unlock:'skeleton',description:'모든 전투 모드에서 🔫 총잡이·🗡️ 칼잡이·🍺 취한 해골 3마리가 한 세트로 동시에 출전해. 3마리가 모두 쓰러지면 새 세트가 등장하며 총 3라운드까지 진행돼. 다음 라운드로 넘어가도 상대 체력은 절대 회복되지 않아.',detail:'💀 해골들 · 3마리 동시 출전 · 각 HP 125 · 총 3라운드 · 🔫70/2초 · 🗡️70/3초 · 🍺100/1.5초 · 상대 HP 라운드 간 유지'},")

# Skeleton boss uses 1.5x body size only; other bosses remain 3x.
rep("const boss=this.mode==='boss'&&side===0,scale=boss?2:1,bodyScale=(boss?3:1)*(type.id==='moai'?1.5:1),team=",
    "const boss=this.mode==='boss'&&side===0,scale=boss?2:1,bodyScale=(boss?(skeletonBundle?1.5:3):1)*(type.id==='moai'?1.5:1),team=")

# Skeleton trio now exists in every selectable combat mode, not only duel/control.
rep(" // In sandbox-style 1v1/control play, the unlocked Skeletons character is one slot made of three simultaneous fighters.\n if(this.mode==='duel'||this.mode==='control'){",
    " // The unlocked Skeletons character is one slot made of three simultaneous fighters in every combat mode.\n {")

# Skeleton attack timings.
rep("f.cd=1/f.scale;f.attack=.16/f.scale;this.effect(f,'🔫 70','skill')","f.cd=2/f.scale;f.attack=.16/f.scale;this.effect(f,'🔫 70','skill')")
rep("damage:100*f.scale,life:3,bounces:0});f.cd=3/f.scale;f.attack=.18/f.scale;this.effect(f,'🍺 비틀!','skill')","damage:100*f.scale,life:3,bounces:0});f.cd=1.5/f.scale;f.attack=.18/f.scale;this.effect(f,'🍺 비틀!','skill')")

# Ninja clone. It is a summon and does not recursively create more clones.
anchor="lizardSkill(f){if(f.id==='lizard'&&!f.lizardTailSummoned&&f.health>0&&f.health<=f.hp*.3)this.spawnLizardTail(f)}\n"
insert="""lizardSkill(f){if(f.id==='lizard'&&!f.lizardTailSummoned&&f.health>0&&f.health<=f.hp*.3)this.spawnLizardTail(f)}
spawnNinjaClone(owner){
 if(!owner||owner.id!=='ninja'||owner.ninjaClone||owner.ninjaCloneSummoned||owner.health<=0||owner.health>owner.hp*.3)return null;
 owner.ninjaCloneSummoned=true;const base=new Engine('ninja','boxer',this.random,{mode:'control'}).fighters[0],side=this.fighters.length,a=this.rand(-Math.PI,Math.PI),c={...base,side,team:owner.team,boss:owner.boss,scale:owner.scale,bodyScale:owner.bodyScale,radius:owner.radius,hp:150,health:150,damage:10*owner.scale,speed:228*owner.scale,cooldown:.3/owner.scale,x:clamp(owner.x+Math.cos(a)*70,55,665),y:clamp(owner.y+Math.sin(a)*70,55,665),vx:Math.cos(a),vy:Math.sin(a),summon:true,ownerSide:owner.side,ninjaClone:true,ninjaCloneSummoned:true,poison:null,toxin:null,burn:null,curse:null,stunUntil:0,capturedBy:null,captureTarget:null,trail:[]};
 this.fighters.push(c);this.effect(owner,'🥷 분신 소환!','skill');this.effect(c,'HP 150 · 공격력 50%','skill');this.emit('🥷 닌자가 체력 30% 이하에서 분신을 소환!');return c
}
ninjaCloneSkill(f){if(f.id==='ninja'&&!f.ninjaClone&&!f.ninjaCloneSummoned&&f.health>0&&f.health<=f.hp*.3)this.spawnNinjaClone(f)}
"""
rep(anchor,insert)
rep(" if(f.id==='lizard')this.lizardSkill(f)\n if(f.id==='devileye')this.devilEyeSkill(f)"," if(f.id==='lizard')this.lizardSkill(f)\n if(f.id==='ninja')this.ninjaCloneSkill(f)\n if(f.id==='devileye')this.devilEyeSkill(f)")

# Clone has half direct, slash and poison damage while keeping normal attack cadence/movement.
rep("const damage=5*f.scale,interval=.3/f.scale,old=e.poison;","const damage=5*f.scale*(f.ninjaClone?.5:1),interval=.3/f.scale,old=e.poison;")
rep(" const cd=f.cd,aim=this.aim(f,e);this.attack(f,e,40*f.scale);"," const cd=f.cd,aim=this.aim(f,e);this.attack(f,e,40*f.scale*(f.ninjaClone?.5:1));")
rep("damage:f.id==='nerd'?f.minDamage+Math.floor(this.random()*(f.maxDamage-f.minDamage+1)):f.damage,life:","damage:f.id==='nerd'?f.minDamage+Math.floor(this.random()*(f.maxDamage-f.minDamage+1)):f.damage*(f.ninjaClone?.5:1),life:")

# Manual-control Hero must still automatically perform the rush/retreat cycle.
rep(" if(!manual&&f.id==='hero'&&f.heroReady){if(f.heroPhase==='retreat'&&this.time>=f.retreatUntil-1e-9)f.heroPhase='rush';if(f.heroPhase==='rush'){const aim=this.aim(f,e);f.vx=aim.x;f.vy=aim.y}}",
    " if(f.id==='hero'&&f.heroReady){if(f.heroPhase==='retreat'&&this.time>=f.retreatUntil-1e-9)f.heroPhase='rush';const aim=this.aim(f,e);if(f.heroPhase==='rush'){f.vx=aim.x;f.vy=aim.y}else if(f.heroPhase==='retreat'){f.vx=-aim.x;f.vy=-aim.y}}")

# Relay: a Skeletons slot is defeated only after all three members of its current set are down.
rep("if(this.mode==='relay'){const out=this.fighters.find(f=>f.health<=0&&this.relayIndex[f.side]===2);if(out)this.result=1-out.side;return;}",
    "if(this.mode==='relay'){for(let side=0;side<2;side++){const lead=this.fighters[side];if(!lead)continue;const defeated=lead.skeletonBundle?this.fighters.filter(x=>x.skeletonBundle&&(x.skeletonBundleLeader??x.side)===(lead.skeletonBundleLeader??lead.side)).every(x=>x.health<=0):lead.health<=0;if(defeated&&this.relayIndex[side]===2){this.result=1-side;return}}return;}")
rep(" for(let side=0;side<2;side++){const old=this.fighters[side];if(old.health>0)continue;if(this.relayIndex[side]>=2){this.result=1-side;return}\n  this.releaseCapture(old);for(const g of this.fighters)if(g.summon&&g.ownerSide===side)g.health=0;const other=this.fighters[1-side];if(other.captureTarget===side)this.releaseCapture(other);\n  this.relayIndex[side]++;const id=this.relayTeams[side][this.relayIndex[side]],fresh=new Engine(id,id,this.random).fighters[side];fresh.nextCapture+=this.time;fresh.nextStudy+=this.time;fresh.transformAt+=this.time;fresh.moonUltAt+=this.time;fresh.nextJump+=this.time;this.fighters[side]=fresh;if(fresh.id==='aladdin')this.spawnGenie(fresh);this.shots=this.shots.filter(s=>s.owner!==side);this.emit((side?'오른쪽':'왼쪽')+' '+(this.relayIndex[side]+1)+'번 '+fresh.name+' 출전!');",
    " for(let side=0;side<2;side++){const old=this.fighters[side],oldLeader=old?.skeletonBundle?(old.skeletonBundleLeader??old.side):null,oldMembers=old?.skeletonBundle?this.fighters.filter(x=>x.skeletonBundle&&(x.skeletonBundleLeader??x.side)===oldLeader):[];if(old?.skeletonBundle&&oldMembers.some(x=>x.health>0))continue;if(old.health>0)continue;if(this.relayIndex[side]>=2){this.result=1-side;return}\n  this.releaseCapture(old);for(const g of this.fighters)if((g.summon&&g.ownerSide===side)||(old?.skeletonBundle&&g!==old&&g.skeletonBundle&&(g.skeletonBundleLeader??g.side)===oldLeader))g.health=0;const other=this.fighters[1-side];if(other.captureTarget===side)this.releaseCapture(other);\n  this.relayIndex[side]++;const id=this.relayTeams[side][this.relayIndex[side]],freshEngine=new Engine(id,id,this.random),fresh=freshEngine.fighters[side];fresh.nextCapture+=this.time;fresh.nextStudy+=this.time;fresh.transformAt+=this.time;fresh.moonUltAt+=this.time;fresh.nextJump+=this.time;this.fighters[side]=fresh;if(fresh.skeletonBundle){const srcLeader=fresh.skeletonBundleLeader??fresh.side;fresh.skeletonBundleLeader=side;for(const m of freshEngine.fighters.filter(x=>x!==fresh&&x.skeletonBundle&&(x.skeletonBundleLeader??x.side)===srcLeader)){m.side=this.fighters.length;m.team=side;m.skeletonBundleLeader=side;this.fighters.push(m)}}if(fresh.id==='aladdin')this.spawnGenie(fresh);this.shots=this.shots.filter(s=>s.owner!==side);this.emit((side?'오른쪽':'왼쪽')+' '+(this.relayIndex[side]+1)+'번 '+fresh.name+' 출전!');")

# Static assertions
checks=[
    'BATTLE <b>v3.36</b>',
    'v3.36 · 그림자 분신과 해골 군단의 역습',
    "hp:800,damage:100",
    "spawnNinjaClone(owner)",
    "ninjaClone?.5:1",
    "f.cd=2/f.scale",
    "f.cd=1.5/f.scale",
    "skeletonBundle?1.5:3",
    "The unlocked Skeletons character is one slot made of three simultaneous fighters in every combat mode.",
    "if(f.id==='hero'&&f.heroReady)",
    "freshEngine=new Engine(id,id,this.random)",
]
for c in checks:
    if c not in s: raise SystemExit('missing '+c)
if "if(this.mode==='duel'||this.mode==='control'){" in s:
    raise SystemExit('old skeleton mode gate still present')

p.write_text(s,encoding='utf-8')
print('v3.36 patch applied')
