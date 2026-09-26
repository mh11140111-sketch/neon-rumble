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

# Visible version + patch notes
rep('<span class="badge">BATTLE <b>v3.35</b></span>','<span class="badge">BATTLE <b>v3.36</b></span>')
rep('<details class="patch-notes"><summary>📒 패치노트 · v3.35</summary><div class="patch-body">',
    '<details class="patch-notes"><summary>📒 패치노트 · v3.36</summary><div class="patch-body"><div class="patch-version"><h3>v3.36 · 그림자의 분신, 사막 군단의 재편</h3><ul><li>카우보이: HP 1000 → 800.</li><li>닌자: HP가 30% 이하가 되면 경기당 1회 분신 1개 소환. 분신 HP 150, 닌자 공격 피해는 본체의 50%.</li><li>해골들: 총잡이 해골 공격 간격 1초 → 2초.</li><li>해골들: 취한 해골 공격 간격 3초 → 1.5초.</li><li>조정 모드 히어로: 변신 후 직접 이동 입력이 돌진/후퇴를 방해하던 문제 수정. 변신 후 돌진 → 후퇴를 자동 반복.</li><li>해골들: 보스전·릴레이·단체전에서도 총잡이·칼잡이·취한 해골 3마리가 동시에 출전하고 총 3라운드를 진행하도록 수정.</li><li>보스 해골들: 일반 보스의 3배 크기 대신 해골들 전용 1.5배 크기 적용. 공격력·체력 등 보스 능력 배율은 유지.</li></ul></div>')

# Roster balance text/data
s=re.sub(r"\{id:'cowboy',name:'카우보이',icon:'🤠\\\n🐴',tag:'말 탑승 · 6발 탄창',hp:1000,damage:100,", "{id:'cowboy',name:'카우보이',icon:'🤠\\\n🐴',tag:'말 탑승 · 6발 탄창',hp:800,damage:100,", s, count=1)
rep("detail:'HP 1000 · 말 탑승 중 이동속도 +100% · 총알 100 · 탄속 약 2.5배 · 1초마다 발사 · 탄창 6발 · 재장전 6초 · HP 30% 이하 말 소멸'", "detail:'HP 800 · 말 탑승 중 이동속도 +100% · 총알 100 · 탄속 약 2.5배 · 1초마다 발사 · 탄창 6발 · 재장전 6초 · HP 30% 이하 말 소멸'")
rep("{id:'ninja',name:'닌자',icon:'🥷',tag:'표창 · 독 · 베기',hp:650,damage:10,speed:228,cooldown:.3,description:'랜덤하게 벽을 튕기며 0.3초마다 직선 표창을 던져. 10% 확률로 독표창. 가까운 적은 베기로 밀쳐내. 체력 650, 이동 속도 20% 증가.',detail:'표창 10 · 독 10초 / 0.3초마다 5 · 독 중첩 없이 시간 갱신 · 베기 40 / 재사용 0.8초'}",
    "{id:'ninja',name:'닌자',icon:'🥷',tag:'표창 · 독 · 베기 · 분신',hp:650,damage:10,speed:228,cooldown:.3,description:'랜덤하게 벽을 튕기며 0.3초마다 직선 표창을 던져. 10% 확률로 독표창. 가까운 적은 베기로 밀쳐내. HP가 30% 이하가 되면 경기당 1회 HP 150의 분신 1개를 소환하며 분신의 공격 피해는 본체의 절반이야.',detail:'HP 650 · 표창 10 · 독 10초 / 0.3초마다 5 · 베기 40 / 재사용 0.8초 · HP 30% 이하 분신 1회 · 분신 HP 150 / 공격 피해 50%'}")
rep("{id:'skeleton_gun',name:'총잡이 해골',icon:'💀',tag:'🔫 회전총',hp:125,damage:70,speed:155,cooldown:1,stageOnly:true,description:'몸 주위를 도는 총이 가장 가까운 적을 향해 1초마다 피해 70의 총알을 발사해.',detail:'HP 125 · 🔫 회전총 · 총알 70 / 1초'}",
    "{id:'skeleton_gun',name:'총잡이 해골',icon:'💀',tag:'🔫 회전총',hp:125,damage:70,speed:155,cooldown:2,stageOnly:true,description:'몸 주위를 도는 총이 가장 가까운 적을 향해 2초마다 피해 70의 총알을 발사해.',detail:'HP 125 · 🔫 회전총 · 총알 70 / 2초'}")
rep("{id:'skeleton_drunk',name:'취한 해골',icon:'💀',tag:'🍺 비틀비틀 조준',hp:125,damage:100,speed:145,cooldown:3,stageOnly:true,description:'맥주잔이 적을 노리지만 술에 취해 조준 오차가 커. 3초마다 빗나가기 쉬운 맥주 공격으로 피해 100을 노려.',detail:'HP 125 · 🍺 피해 100 · 쿨타임 3초 · 낮은 명중률'}",
    "{id:'skeleton_drunk',name:'취한 해골',icon:'💀',tag:'🍺 비틀비틀 조준',hp:125,damage:100,speed:145,cooldown:1.5,stageOnly:true,description:'맥주잔이 적을 노리지만 술에 취해 조준 오차가 커. 1.5초마다 빗나가기 쉬운 맥주 공격으로 피해 100을 노려.',detail:'HP 125 · 🍺 피해 100 · 쿨타임 1.5초 · 낮은 명중률'}")
rep("detail:'💀 해골들 · 3마리 동시 출전 · 각 HP 125 · 총 3라운드 · 🔫70/1초 · 🗡️70/3초 · 🍺100/3초 · 상대 HP 라운드 간 유지'",
    "detail:'💀 해골들 · 3마리 동시 출전 · 각 HP 125 · 총 3라운드 · 🔫70/2초 · 🗡️70/3초 · 🍺100/1.5초 · 상대 HP 라운드 간 유지'")

# Skeleton boss body size: only Skeletons boss uses 1.5x body instead of generic 3x.
rep("const boss=this.mode==='boss'&&side===0,scale=boss?2:1,bodyScale=(boss?3:1)*(type.id==='moai'?1.5:1),team=",
    "const boss=this.mode==='boss'&&side===0,scale=boss?2:1,bodyScale=(boss?(skeletonBundle?1.5:3):1)*(type.id==='moai'?1.5:1),team=")

# Replace duel/control-only trio creation with reusable all-mode trio spawning.
pattern=r"\n // In sandbox-style 1v1/control play, the unlocked Skeletons character is one slot made of three simultaneous fighters\.\n if\(this\.mode==='duel'\|\|this\.mode==='control'\)\{.*?\n \}\n for\(const owner of \[\.\.\.this\.fighters\]\)if\(owner\.id==='aladdin'\)this\.spawnGenie\(owner\);\n\}\nspawnGenie\(owner\)\{"
replacement="""
 // Skeletons is always one logical pick made of three simultaneous fighters, in every selectable mode.
 for(const owner of [...this.fighters])if(owner.skeletonBundle)this.spawnSkeletonBundleMates(owner);
 for(const owner of [...this.fighters])if(owner.id==='aladdin')this.spawnGenie(owner);
}
spawnSkeletonBundleMates(owner){
 if(!owner||!owner.skeletonBundle)return;const leader=owner.skeletonBundleLeader??owner.side;owner.skeletonBundleLeader=leader;owner.skeletonBundleRound=owner.skeletonBundleRound||1;owner.name='해골들';const current=this.fighters.filter(x=>x.skeletonBundle&&(x.skeletonBundleLeader??x.side)===leader);if(current.length>=3)return;
 const mateIds=['skeleton_sword','skeleton_drunk'],ys=[-82,82];mateIds.forEach((id,i)=>{const t=ROSTER.find(x=>x.id===id),side=this.fighters.length,angle=this.rand(-1,1)+(owner.team?Math.PI:0),hp=t.hp*(owner.boss?2.5:1),m={...owner,...t,name:'해골들',side,team:owner.team,boss:owner.boss,scale:owner.scale,bodyScale:owner.bodyScale,radius:owner.radius,hp,health:hp,damage:t.damage*owner.scale,speed:t.speed*owner.scale,cooldown:t.cooldown/owner.scale,skeletonBundle:true,skeletonBundleLeader:leader,skeletonBundleRound:owner.skeletonBundleRound||1,summon:false,ownerSide:leader,x:owner.x,y:clamp(owner.y+ys[i],60,660),vx:Math.cos(angle),vy:Math.sin(angle),attack:0,cd:0,stunUntil:0,burn:null,poison:null,toxin:null,curse:null,slow:0,slowPower:0,rootSlow:0,rootSlowPower:0,capturedBy:null,captureTarget:null,trail:[],deathOrder:null,possessedByGhost:null};this.fighters.push(m)});
}
spawnGenie(owner){"""
s,n=re.subn(pattern,replacement,s,count=1,flags=re.S)
if n!=1: raise SystemExit(f'skeleton trio constructor block mismatch: {n}')

# Relay waits for all Skeletons members, and can spawn the trio when a relay slot becomes active.
rep("for(let side=0;side<2;side++){const old=this.fighters[side];if(old.health>0)continue;",
    "for(let side=0;side<2;side++){const old=this.fighters[side];if(old.skeletonBundle){const leader=old.skeletonBundleLeader??old.side,members=this.fighters.filter(x=>x.skeletonBundle&&(x.skeletonBundleLeader??x.side)===leader);if(members.some(x=>x.health>0))continue}if(old.health>0)continue;")
rep("this.fighters[side]=fresh;if(fresh.id==='aladdin')this.spawnGenie(fresh);",
    "this.fighters[side]=fresh;if(fresh.skeletonBundle){fresh.skeletonBundleLeader=side;this.spawnSkeletonBundleMates(fresh)}if(fresh.id==='aladdin')this.spawnGenie(fresh);")

# Ninja clone: once at <=30% HP, HP 150, half offensive damage. Clone is a summon and cannot clone itself.
rep("lizardSkill(f){if(f.id==='lizard'&&!f.lizardTailSummoned&&f.health>0&&f.health<=f.hp*.3)this.spawnLizardTail(f)}",
"""lizardSkill(f){if(f.id==='lizard'&&!f.lizardTailSummoned&&f.health>0&&f.health<=f.hp*.3)this.spawnLizardTail(f)}
ninjaCloneSkill(owner){
 if(!owner||owner.id!=='ninja'||owner.ninjaClone||owner.ninjaCloneSummoned||owner.health<=0||owner.health>owner.hp*.3)return null;owner.ninjaCloneSummoned=true;const base=new Engine('ninja','ninja',this.random,{mode:'control'}).fighters[0],side=this.fighters.length,a=this.rand(-Math.PI,Math.PI);base.side=side;base.team=owner.team;base.boss=false;base.scale=owner.scale;base.bodyScale=owner.bodyScale;base.radius=owner.radius;base.hp=150;base.health=150;base.damage=owner.damage*.5;base.speed=owner.speed;base.cooldown=owner.cooldown;base.x=clamp(owner.x+Math.cos(a)*58,55,665);base.y=clamp(owner.y+Math.sin(a)*58,55,665);base.vx=Math.cos(a);base.vy=Math.sin(a);base.ninjaClone=true;base.ninjaCloneSummoned=true;base.summon=true;base.ownerSide=owner.side;base.trail=[];base.poison=null;base.toxin=null;base.burn=null;base.curse=null;base.stunUntil=0;this.fighters.push(base);this.effect(owner,'🥷 분신 소환!','skill');this.effect(base,'분신 · HP 150','skill');this.emit('🥷 닌자가 HP 30% 이하에서 분신을 소환!');return base
}""")
rep("step(dt){if(this.result!==null||dt<=0)return;this.updateAirborne();for(const f of this.fighters)if(f.id==='lizard')this.lizardSkill(f);this.stepRound(dt);",
    "step(dt){if(this.result!==null||dt<=0)return;this.updateAirborne();for(const f of [...this.fighters]){if(f.id==='lizard')this.lizardSkill(f);if(f.id==='ninja')this.ninjaCloneSkill(f)}this.stepRound(dt);")
rep("const damage=5*f.scale,interval=.3/f.scale,old=e.poison;",
    "const damage=5*f.scale*(f.ninjaClone?.5:1),interval=.3/f.scale,old=e.poison;")
rep("this.attack(f,e,40*f.scale);f.cd=cd;f.slashCd=.8/f.scale;",
    "this.attack(f,e,40*f.scale*(f.ninjaClone?.5:1));f.cd=cd;f.slashCd=.8/f.scale;")

# Hero in manual control: after transformation, automatic rush/retreat owns movement.
rep("const manual=(this.mode==='control'||this.manualTeam0)&&f.team===0;if(manual){",
    "const heroAuto=f.id==='hero'&&f.heroReady,manual=(this.mode==='control'||this.manualTeam0)&&f.team===0&&!heroAuto;if(manual){")

# Skeleton attack cadence runtime values.
rep("f.cd=1/f.scale;f.attack=.16/f.scale;this.effect(f,'🔫 70','skill')", "f.cd=2/f.scale;f.attack=.16/f.scale;this.effect(f,'🔫 70','skill')")
rep("f.cd=3/f.scale;f.attack=.18/f.scale;this.effect(f,'🍺 비틀!','skill')", "f.cd=1.5/f.scale;f.attack=.18/f.scale;this.effect(f,'🍺 비틀!','skill')")

p.write_text(s,encoding='utf-8')
print('v3.36 patch applied')
