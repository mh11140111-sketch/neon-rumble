from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n!=count:
        raise SystemExit(f'replace mismatch expected {count}, found {n}: {old[:180]!r}')
    s=s.replace(old,new,count)

# Cowboy HP 1000 -> 750.
rep("{id:'cowboy',name:'카우보이',icon:'🤠\\n🐴',tag:'말 탑승 · 6발 탄창',hp:1000,damage:100", "{id:'cowboy',name:'카우보이',icon:'🤠\\n🐴',tag:'말 탑승 · 6발 탄창',hp:750,damage:100")
rep("detail:'HP 1000 · 말 탑승 중 이동속도 +100% · 총알 100 · 탄속 약 2.5배", "detail:'HP 750 · 말 탑승 중 이동속도 +100% · 총알 100 · 탄속 약 2.5배")

# Ninja description + one-time clone state.
rep("description:'랜덤하게 벽을 튕기며 0.3초마다 직선 표창을 던져. 10% 확률로 독표창. 가까운 적은 베기로 밀쳐내. 체력 650, 이동 속도 20% 증가.',detail:'표창 10 · 독 10초 / 0.3초마다 5 · 독 중첩 없이 시간 갱신 · 베기 40 / 재사용 0.8초'", "description:'랜덤하게 벽을 튕기며 0.3초마다 직선 표창을 던져. 10% 확률로 독표창. 가까운 적은 베기로 밀쳐내. 체력이 30% 이하가 되면 체력 150의 분신을 경기당 1회 소환하며, 분신의 모든 공격 피해는 본체의 절반이야. 보스 닌자는 분신에도 보스 배율이 적용돼.',detail:'HP 650 · 표창 10 · 독 10초 / 0.3초마다 5 · 베기 40 / 0.8초 · HP 30% 이하 분신 1회 · 분신 HP 150 · 공격 피해 50% · 보스 배율 적용'")
rep("lizardTailSummoned:false,lizardTailSide:null,angryPunchCd:0", "lizardTailSummoned:false,lizardTailSide:null,ninjaCloneSpawned:false,ninjaClone:false,angryPunchCd:0")

# Skeleton balance values and card text.
rep("{id:'skeleton_gun',name:'총잡이 해골',icon:'💀',tag:'🔫 회전총',hp:125,damage:70,speed:155,cooldown:1,stageOnly:true,description:'몸 주위를 도는 총이 가장 가까운 적을 향해 1초마다 피해 70의 총알을 발사해.',detail:'HP 125 · 🔫 회전총 · 총알 70 / 1초'}", "{id:'skeleton_gun',name:'총잡이 해골',icon:'💀',tag:'🔫 회전총',hp:125,damage:70,speed:155,cooldown:2,stageOnly:true,description:'몸 주위를 도는 총이 가장 가까운 적을 향해 2초마다 피해 70의 총알을 발사해.',detail:'HP 125 · 🔫 회전총 · 총알 70 / 2초'}")
rep("{id:'skeleton_drunk',name:'취한 해골',icon:'💀',tag:'🍺 비틀비틀 조준',hp:125,damage:100,speed:145,cooldown:3,stageOnly:true,description:'맥주잔이 적을 노리지만 술에 취해 조준 오차가 커. 3초마다 빗나가기 쉬운 맥주 공격으로 피해 100을 노려.',detail:'HP 125 · 🍺 피해 100 · 쿨타임 3초 · 낮은 명중률'}", "{id:'skeleton_drunk',name:'취한 해골',icon:'💀',tag:'🍺 비틀비틀 조준',hp:125,damage:100,speed:145,cooldown:1.5,stageOnly:true,description:'맥주잔이 적을 노리지만 술에 취해 조준 오차가 커. 1.5초마다 빗나가기 쉬운 맥주 공격으로 피해 100을 노려.',detail:'HP 125 · 🍺 피해 100 · 쿨타임 1.5초 · 낮은 명중률'}")
rep("detail:'💀 해골들 · 3마리 동시 출전 · 각 HP 125 · 총 3라운드 · 🔫70/1초 · 🗡️70/3초 · 🍺100/3초 · 상대 HP 라운드 간 유지'", "detail:'💀 해골들 · 3마리 동시 출전 · 각 HP 125 · 총 3라운드 · 🔫70/2초 · 🗡️70/3초 · 🍺100/1.5초 · 상대 HP 라운드 간 유지'")
rep("f.cd=1/f.scale;f.attack=.16/f.scale;this.effect(f,'🔫 70','skill')", "f.cd=2/f.scale;f.attack=.16/f.scale;this.effect(f,'🔫 70','skill')")
rep("f.cd=3/f.scale;f.attack=.18/f.scale;this.effect(f,'🍺 비틀!','skill')", "f.cd=1.5/f.scale;f.attack=.18/f.scale;this.effect(f,'🍺 비틀!','skill')")

# Skeleton boss body is only 1.5x, while normal boss combat scaling remains intact.
rep("const boss=this.mode==='boss'&&side===0,scale=boss?2:1,bodyScale=(boss?3:1)*(type.id==='moai'?1.5:1)", "const boss=this.mode==='boss'&&side===0,scale=boss?2:1,bodyScale=(boss?(skeletonBundle?1.5:3):1)*(type.id==='moai'?1.5:1)")

# Replace sandbox-only trio expansion with all-mode bundle expansion and reusable helper.
old=""" // In sandbox-style 1v1/control play, the unlocked Skeletons character is one slot made of three simultaneous fighters.\n if(this.mode==='duel'||this.mode==='control'){\n  for(const owner of [...this.fighters])if(owner.skeletonBundle){\n   owner.skeletonBundleLeader=owner.side;owner.skeletonBundleRound=1;owner.name='해골들';\n   const mateIds=['skeleton_sword','skeleton_drunk'],ys=[-82,82];\n   mateIds.forEach((id,i)=>{const t=ROSTER.find(x=>x.id===id),side=this.fighters.length,angle=this.rand(-1,1)+(owner.team?Math.PI:0),hp=t.hp*(owner.boss?2.5:1),m={...owner,...t,name:'해골들',side,team:owner.team,boss:owner.boss,scale:owner.scale,bodyScale:owner.bodyScale,radius:owner.radius,hp,health:hp,damage:t.damage*owner.scale,speed:t.speed*owner.scale,cooldown:t.cooldown/owner.scale,skeletonBundle:true,skeletonBundleLeader:owner.side,skeletonBundleRound:1,x:owner.x,y:clamp(owner.y+ys[i],60,660),vx:Math.cos(angle),vy:Math.sin(angle),attack:0,cd:0,stunUntil:0,burn:null,poison:null,toxin:null,curse:null,slow:0,slowPower:0,rootSlow:0,rootSlowPower:0,capturedBy:null,captureTarget:null,trail:[],deathOrder:null,possessedByGhost:null};this.fighters.push(m)})\n  }\n }\n for(const owner of [...this.fighters])if(owner.id==='aladdin')this.spawnGenie(owner);\n}\nspawnGenie(owner){"""
new=""" // Skeletons are always a three-fighter set in every selectable mode.\n for(const owner of [...this.fighters])if(owner.skeletonBundle)this.spawnSkeletonBundleMates(owner);\n for(const owner of [...this.fighters])if(owner.id==='aladdin')this.spawnGenie(owner);\n}\nspawnSkeletonBundleMates(owner){\n if(!owner||!owner.skeletonBundle||owner.skeletonBundleMate)return;\n this.skeletonBundleSerial=(this.skeletonBundleSerial||0)+1;const key='skeleton-bundle-'+this.skeletonBundleSerial+'-'+owner.side+'-'+this.time;\n owner.skeletonBundleLeader=owner.side;owner.skeletonBundleKey=key;owner.skeletonBundleRound=1;owner.skeletonBundleMate=false;owner.name='해골들';\n const mateIds=['skeleton_sword','skeleton_drunk'],ys=[-82,82];\n mateIds.forEach((id,i)=>{const t=ROSTER.find(x=>x.id===id),side=this.fighters.length,angle=this.rand(-1,1)+(owner.team?Math.PI:0),hp=t.hp*(owner.boss?2.5:1),m={...owner,...t,name:'해골들',side,team:owner.team,boss:owner.boss,scale:owner.scale,bodyScale:owner.bodyScale,radius:owner.radius,hp,health:hp,damage:t.damage*owner.scale,speed:t.speed*owner.scale,cooldown:t.cooldown/owner.scale,skeletonBundle:true,skeletonBundleLeader:owner.side,skeletonBundleKey:key,skeletonBundleMate:true,skeletonBundleRound:1,x:owner.x,y:clamp(owner.y+ys[i],60,660),vx:Math.cos(angle),vy:Math.sin(angle),attack:0,cd:0,stunUntil:0,burn:null,poison:null,toxin:null,curse:null,slow:0,slowPower:0,rootSlow:0,rootSlowPower:0,capturedBy:null,captureTarget:null,trail:[],deathOrder:null,possessedByGhost:null};this.fighters.push(m)})\n}\nspawnGenie(owner){"""
rep(old,new)

# Bundle rounds group by unique bundle key, so relay/team history cannot mix bundles.
rep("const leader=f.skeletonBundleLeader??f.side,members=this.fighters.filter(x=>x.skeletonBundle&&(x.skeletonBundleLeader??x.side)===leader)", "const key=f.skeletonBundleKey||('legacy-'+(f.skeletonBundleLeader??f.side)),members=this.fighters.filter(x=>x.skeletonBundle&&(x.skeletonBundleKey||('legacy-'+(x.skeletonBundleLeader??x.side)))===key)")

# Relay: spawn the other two skeletons whenever the next relay fighter is Skeletons.
rep("this.fighters[side]=fresh;if(fresh.id==='aladdin')this.spawnGenie(fresh);this.shots=this.shots.filter(s=>s.owner!==side);", "this.fighters[side]=fresh;if(fresh.skeletonBundle)this.spawnSkeletonBundleMates(fresh);if(fresh.id==='aladdin')this.spawnGenie(fresh);this.shots=this.shots.filter(s=>s.owner!==side);")

# Ninja clone: one summon at 30% HP, HP 150 (boss HP scaling included), all damage = 50% of owner.
needle="""updateVampire(f){if(f.id!=='vampire'||f.health<=0)return;const low=f.health<=f.hp*.3;if(low&&!f.vampireBat){f.vampireBat=true;f.icon='🦇';f.name='박쥐';f.speed*=2;this.effect(f,'박쥐 변신!','skill')}else if(!low&&f.vampireBat){f.vampireBat=false;f.icon='🧛';f.name='흡혈귀';f.speed/=2;this.effect(f,'흡혈귀 복귀','skill')}}\nmoonSkill(f){"""
insert="""updateVampire(f){if(f.id!=='vampire'||f.health<=0)return;const low=f.health<=f.hp*.3;if(low&&!f.vampireBat){f.vampireBat=true;f.icon='🦇';f.name='박쥐';f.speed*=2;this.effect(f,'박쥐 변신!','skill')}else if(!low&&f.vampireBat){f.vampireBat=false;f.icon='🧛';f.name='흡혈귀';f.speed/=2;this.effect(f,'흡혈귀 복귀','skill')}}\nspawnNinjaClone(owner){if(!owner||owner.id!=='ninja'||owner.health<=0||owner.ninjaClone||owner.ninjaCloneSpawned)return null;owner.ninjaCloneSpawned=true;const side=this.fighters.length,hp=150*(owner.boss?2.5:1),a=this.rand(-Math.PI,Math.PI),c={...owner,name:'닌자 분신',side,team:owner.team,hp,health:hp,damage:owner.damage*.5,x:clamp(owner.x+this.rand(-55,55),55,665),y:clamp(owner.y+this.rand(-55,55),55,665),vx:Math.cos(a),vy:Math.sin(a),attack:0,cd:0,ninjaClone:true,ninjaCloneSpawned:true,summon:true,ownerSide:owner.side,poison:null,toxin:null,burn:null,curse:null,stunUntil:0,slow:0,slowPower:0,rootSlow:0,rootSlowPower:0,capturedBy:null,captureTarget:null,trail:[],deathOrder:null};this.fighters.push(c);this.effect(owner,'🥷 분신 소환!','skill');this.emit('🥷 닌자가 체력 30% 이하에서 분신을 소환!');return c}\nupdateNinjaClone(f){if(f.id==='ninja'&&!f.ninjaClone&&!f.ninjaCloneSpawned&&f.health>0&&f.health<=f.hp*.3)this.spawnNinjaClone(f)}\nmoonSkill(f){"""
rep(needle,insert)
rep("for(const f of this.fighters){this.transformHero(f);this.updateVampire(f);this.moonSkill(f);this.study(f)}", "for(const f of [...this.fighters]){this.transformHero(f);this.updateVampire(f);this.updateNinjaClone(f);this.moonSkill(f);this.study(f)}")

# Ninja clone damage is half for shuriken, slash and poison ticks.
rep("damage:f.id==='nerd'?f.minDamage+Math.floor(this.random()*(f.maxDamage-f.minDamage+1)):f.damage", "damage:f.id==='nerd'?f.minDamage+Math.floor(this.random()*(f.maxDamage-f.minDamage+1)):f.damage")
# f.damage is already halved on clone; hard-coded ninja attacks need explicit multiplier.
rep("this.attack(f,e,40*f.scale);f.cd=cd;f.slashCd=.8/f.scale", "this.attack(f,e,40*f.scale*(f.ninjaClone?.5:1));f.cd=cd;f.slashCd=.8/f.scale")
rep("const damage=5*f.scale,interval=.3/f.scale,old=e.poison;", "const damage=5*f.scale*(f.id==='ninja'&&f.ninjaClone?.5:1),interval=.3/f.scale,old=e.poison;")

# Hero in control mode: manual movement before transformation, automatic rush/retreat after transformation.
old=""" const manual=(this.mode==='control'||this.manualTeam0)&&f.team===0;if(manual){f.vx=Number(this.controlX)||0;f.vy=Number(this.controlY)||0;f.turn=1}else if(f.dash<=0){if(f.turn<=0)this.turn(f);if(['knight','vampire','smith','skeleton_sword'].includes(f.id)){const a=this.aim(f,e),k=(f.id==='smith'?.65:1.8)*f.scale;const x=f.vx+a.x*k*dt,y=f.vy+a.y*k*dt,n=Math.hypot(x,y)||1;f.vx=x/n;f.vy=y/n}}\n const prey=f.captureTarget!==null?this.fighters[f.captureTarget]:null;if(prey&&!manual){const aim=this.aim(f,prey);f.vx=aim.x;f.vy=aim.y}\n if(!manual&&f.id==='hero'&&f.heroReady){if(f.heroPhase==='retreat'&&this.time>=f.retreatUntil-1e-9)f.heroPhase='rush';if(f.heroPhase==='rush'){const aim=this.aim(f,e);f.vx=aim.x;f.vy=aim.y}}"""
new=""" const manual=(this.mode==='control'||this.manualTeam0)&&f.team===0,heroAuto=f.id==='hero'&&f.heroReady;if(manual&&!heroAuto){f.vx=Number(this.controlX)||0;f.vy=Number(this.controlY)||0;f.turn=1}else if(!heroAuto&&f.dash<=0){if(f.turn<=0)this.turn(f);if(['knight','vampire','smith','skeleton_sword'].includes(f.id)){const a=this.aim(f,e),k=(f.id==='smith'?.65:1.8)*f.scale;const x=f.vx+a.x*k*dt,y=f.vy+a.y*k*dt,n=Math.hypot(x,y)||1;f.vx=x/n;f.vy=y/n}}\n const prey=f.captureTarget!==null?this.fighters[f.captureTarget]:null;if(prey&&!(manual&&!heroAuto)){const aim=this.aim(f,prey);f.vx=aim.x;f.vy=aim.y}\n if(heroAuto){if(f.heroPhase==='retreat'&&this.time>=f.retreatUntil-1e-9)f.heroPhase='rush';if(f.heroPhase==='rush'){const aim=this.aim(f,e);f.vx=aim.x;f.vy=aim.y}}"""
rep(old,new)

# Patch notes under current v3.35 release.
marker="</li></ul></div><div class=\"patch-version\"><h3>v3.34 · 사막의 해골 & 밸런스</h3>"
addition=("</li><li>밸런스: 카우보이 기본 체력 1000 → 750.</li>"
          "<li>닌자: HP 30% 이하에서 HP 150 분신을 경기당 1회 소환. 분신 공격 피해는 본체의 50%이며 보스 배율도 적용.</li>"
          "<li>해골들: 총잡이 해골 공격 간격 1초 → 2초, 취한 해골 공격 간격 3초 → 1.5초.</li>"
          "<li>버그 수정: 조정 모드 히어로가 변신 후 돌진 ↔ 후퇴를 자동으로 수행하도록 수정.</li>"
          "<li>버그 수정: 해골들이 보스전·단체전·릴레이에서도 3마리 동시 출전 + 총 3라운드로 정상 작동. 해골들 보스의 크기는 1.5배만 증가.</li>"
          "</ul></div><div class=\"patch-version\"><h3>v3.34 · 사막의 해골 & 밸런스</h3>")
rep(marker,addition)

p.write_text(s,encoding='utf-8')
print('v3.35 balance/mode fixes applied')
