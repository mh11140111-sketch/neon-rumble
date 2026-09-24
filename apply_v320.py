from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if old not in s:
        raise SystemExit(f'PATCH FAILED: {label}')
    s=s.replace(old,new,count)

# Version + patch notes
rep('BATTLE <b>v3.19</b>','BATTLE <b>v3.20</b>','version badge')
rep('📒 패치노트 · v3.19','📒 패치노트 · v3.20','patch summary')
anchor='<div class="patch-body"><div class="patch-version"><h3>v3.19 · 만능 로봇</h3>'
insert='<div class="patch-body"><div class="patch-version"><h3>v3.20 · 알라딘 & 밸런스</h3><ul><li>로봇: 모든 공격 피해 +20. 회전 레이저 70, 만능로봇팔 50.</li><li>달: 반달 조각이 적을 관통하도록 변경. 궁극기 준비 시간 35초 → 45초.</li><li>신규 캐릭터 👳‍♀️ 알라딘: 기본 체력 500, 전투 시작 시 체력 1500의 🧞‍♂️ 지니 소환.</li><li>지니: 3초마다 큰 팔을 휘둘러 범위 안 적에게 피해 50. 지니 사망 시 최대 2회 부활하며, 부활할 때마다 알라딘의 최대/현재 체력과 지니 공격력이 절반이 됨.</li><li>알라딘이 사망하면 지니 생존 여부와 무관하게 알라딘은 패배 처리. 보스 알라딘의 지니도 보스 배율 적용.</li></ul></div><div class="patch-version"><h3>v3.19 · 만능 로봇</h3>'
rep(anchor,insert,'patch notes')

# Robot balance text + damage
rep("{id:'robot',name:'로봇',icon:'🤖',tag:'회전 레이저 · 만능로봇팔',hp:1000,damage:50,speed:150,cooldown:5,description:'5초마다 맵 전체를 천천히 한 바퀴 도는 레이저를 발사해 피해 50. 7초마다 만능로봇팔로 자신을 제외한 모든 캐릭터를 밀쳐내고 피해 30과 1초 기절을 줘.',detail:'레이저 50 · 5초마다 · 4초간 1회전 · 회전당 대상별 1회 피격 · 로봇팔 30 · 7초 · 전장 전체 밀치기 · 기절 1초'}",
    "{id:'robot',name:'로봇',icon:'🤖',tag:'회전 레이저 · 만능로봇팔',hp:1000,damage:70,speed:150,cooldown:5,description:'5초마다 맵 전체를 천천히 한 바퀴 도는 레이저를 발사해 피해 70. 7초마다 만능로봇팔로 자신을 제외한 모든 캐릭터를 밀쳐내고 피해 50과 1초 기절을 줘.',detail:'레이저 70 · 5초마다 · 4초간 1회전 · 회전당 대상별 1회 피격 · 로봇팔 50 · 7초 · 전장 전체 밀치기 · 기절 1초'}",
    'robot roster balance')
rep('this.attack(f,e,50*f.scale)','this.attack(f,e,70*f.scale)','robot laser damage',1)
rep('this.attack(f,e,30*f.scale,true)','this.attack(f,e,50*f.scale,true)','robot arm damage',1)

# Moon balance: 45 sec + piercing crescent
old_moon="{id:'moon',name:'달',icon:'🌝',tag:'반달 조각 · 월하강림',hp:1000,damage:80,speed:150,cooldown:2,description:'2초마다 🌜 반달 조각을 던져 피해 80. 조각이 날아간 동안 자신은 🌛 반달이 되고, 조각이 돌아오면 다시 🌝 보름달이 돼. 전투가 35초를 넘기면 궁극기를 준비해.',detail:'반달 조각 80 · 쿨타임 2초 · 35초 후 궁극기 · 5초 예고 뒤 전장 전체 즉사 · 무적 무시 · 팀 구분 없음'}"
new_moon="{id:'moon',name:'달',icon:'🌝',tag:'관통 반달 · 월하강림',hp:1000,damage:80,speed:150,cooldown:2,description:'2초마다 🌜 반달 조각을 던져 피해 80. 반달 조각은 적을 관통하고 맵 끝에 닿으면 돌아와. 전투가 45초를 넘기면 궁극기를 준비해.',detail:'관통 반달 80 · 쿨타임 2초 · 45초 후 궁극기 · 5초 예고 뒤 전장 전체 즉사 · 무적 무시 · 팀 구분 없음'}"
rep(old_moon,new_moon,'moon roster')
rep('moonUltAt:35/scale','moonUltAt:45/scale','moon ult timer')
old_throw="moonThrow(f,e){if(f.id!=='moon'||f.cd>1e-9||f.moonHalf||f.moonUltPhase==='air')return;const a=this.aim(f,e),shot={x:f.x+a.x*(f.radius+8),y:f.y+a.y*(f.radius+8),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'moon',icon:'🌜',damage:80*f.scale,radius:11*f.scale,speed:330*f.scale,life:6,returning:false,hit:false};"
new_throw="moonThrow(f,e){if(f.id!=='moon'||f.cd>1e-9||f.moonHalf||f.moonUltPhase==='air')return;const a=this.aim(f,e),shot={x:f.x+a.x*(f.radius+8),y:f.y+a.y*(f.radius+8),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'moon',icon:'🌜',damage:80*f.scale,radius:11*f.scale,speed:330*f.scale,life:6,returning:false,hitTargets:{}};"
rep(old_throw,new_throw,'moon projectile state')
old_hit="const blocker=this.enemies(f).find(v=>v.id==='knight'&&this.knightBlocksProjectile(v,s));if(blocker){this.blockProjectileWithKnight(blocker,s,f);s.hit=true;s.returning=true;continue}const e=this.enemies(f).find(v=>distance(s,v)<v.radius+s.radius);if(e&&!s.hit){this.attackProjectile(f,e,s);s.hit=true;s.returning=true}if(s.x<22||s.x>698||s.y<22||s.y>698)s.returning=true"
new_hit="const blocker=this.enemies(f).find(v=>v.id==='knight'&&this.knightBlocksProjectile(v,s));if(blocker){this.blockProjectileWithKnight(blocker,s,f);s.returning=true;continue}for(const e of this.enemies(f)){if(s.hitTargets[e.side])continue;if(distance(s,e)<e.radius+s.radius){this.attackProjectile(f,e,s);s.hitTargets[e.side]=true;if(this.result!==null)break}}if(s.x<22||s.x>698||s.y<22||s.y>698)s.returning=true"
rep(old_hit,new_hit,'moon piercing')

# Add Aladdin roster entry
robot_new="{id:'robot',name:'로봇',icon:'🤖',tag:'회전 레이저 · 만능로봇팔',hp:1000,damage:70,speed:150,cooldown:5,description:'5초마다 맵 전체를 천천히 한 바퀴 도는 레이저를 발사해 피해 70. 7초마다 만능로봇팔로 자신을 제외한 모든 캐릭터를 밀쳐내고 피해 50과 1초 기절을 줘.',detail:'레이저 70 · 5초마다 · 4초간 1회전 · 회전당 대상별 1회 피격 · 로봇팔 50 · 7초 · 전장 전체 밀치기 · 기절 1초'}"
aladdin="{id:'aladdin',name:'알라딘',icon:'👳‍♀️',tag:'지니 소환 · 2회 부활',hp:500,damage:50,speed:165,cooldown:0,description:'전투 시작과 동시에 체력 1500의 🧞‍♂️ 지니를 소환해. 지니는 3초마다 큰 팔을 휘둘러 범위 피해 50. 지니가 쓰러지면 최대 2회 부활하며, 부활할 때마다 알라딘의 최대/현재 체력과 지니 공격력이 절반이 돼.',detail:'알라딘 HP 500 · 지니 HP 1500 · 범위 공격 50 / 3초 · 지니 최대 2회 부활 · 부활마다 알라딘 체력 및 지니 공격력 1/2 · 알라딘 사망 시 지니와 무관하게 패배'}"
rep(robot_new+'\n];',robot_new+',\n'+aladdin+'\n];','aladdin roster')

# Spawn genies after primary fighters are created.
constructor_end="   x:starts[side][0],y:starts[side][1],vx:Math.cos(angle),vy:Math.sin(angle),attack:0,cd:0,skill:1.2/scale,turn:1/scale,dash:0,dashHit:false,"
# Give Aladdin companion state on main fighter
rep(constructor_end,constructor_end.replace("attack:0,cd:0,skill:1.2/scale","attack:0,cd:0,skill:1.2/scale,genieRevives:0,geniePower:1"),'aladdin state base')
old_close=" });\n}\nrand(a,b){return a+this.random()*(b-a)}"
new_close=" });\n for(const owner of [...this.fighters])if(owner.id==='aladdin')this.spawnGenie(owner);\n}\nspawnGenie(owner){if(!owner||owner.id!=='aladdin'||owner.health<=0)return null;const boss=owner.boss,scale=owner.scale,hp=1500*(boss?2.5:1),side=this.fighters.length,angle=this.rand(-Math.PI,Math.PI),g={id:'genie',name:'지니',icon:'🧞‍♂️',tag:'큰 팔 휘두르기',description:'3초마다 큰 팔을 휘둘러 범위 공격.',detail:'',side,team:owner.team,boss,scale,bodyScale:boss?3:1,radius:38*(boss?3:1),hp,health:hp,damage:50*scale*(owner.geniePower||1),speed:180*scale,cooldown:3/scale,x:clamp(owner.x+70,60,660),y:clamp(owner.y+70,60,660),vx:Math.cos(angle),vy:Math.sin(angle),attack:0,cd:3/scale,skill:0,turn:0,dash:0,dashHit:false,awakened:false,revivals:0,heroReady:false,vampireBat:false,dodgeChance:0,knightShieldNext:0,knightShieldChargedUntil:0,knightShieldAngle:0,knightBlockedDamage:0,policeBarrageUsed:false,policeBarrageUntil:0,policeBarrageCd:0,nextJump:0,jumpFx:0,moonHalf:false,moonShot:null,moonUltStarted:false,moonUltAt:9999,moonUltLandAt:0,moonUltPhase:'',egg:false,eggUntil:0,stunUntil:0,burn:null,peckCd:0,flameCd:0,captureTarget:null,capturedBy:null,nextCapture:9999,venom:null,webAnchor:null,webs:[],webHits:{},studyUntil:0,nextStudy:9999,studyStart:0,minDamage:0,maxDamage:0,letterIndex:0,poison:null,toxin:null,slashCd:0,slashFx:0,slashAngle:0,idle:0,forgeLevel:0,forgeInterval:1,rootLength:0,rootGrowth:0,rootHits:{},rootSlow:0,rootSlowPower:0,slow:0,slowPower:0,flash:0,damageDealt:0,hits:0,healed:0,trail:[],summon:true,ownerSide:owner.side};this.fighters.push(g);owner.genieSide=g.side;this.effect(owner,'🧞‍♂️ 지니 소환!','skill');return g}\nrand(a,b){return a+this.random()*(b-a)}"
rep(old_close,new_close,'spawn genie')

# End condition ignores summoned genie. Aladdin death therefore cannot be saved by genie.
rep("const alive=[0,1].map(team=>this.fighters.some(f=>f.team===team&&f.health>0));","const alive=[0,1].map(team=>this.fighters.some(f=>!f.summon&&f.team===team&&f.health>0));",'check end summon ignore')

# Genie behavior and resurrection
anchor_skill="robotSkill(f){"
genie_code="""genieSkill(g,dt){
 if(g.id!=='genie'||g.health<=0)return;const owner=this.fighters[g.ownerSide];if(!owner||owner.health<=0){g.health=0;return}
 g.cd=Math.max(0,g.cd-dt);const tx=clamp(owner.x+(owner.team?55:-55)*g.scale,45,675),ty=clamp(owner.y+55*g.scale,45,675),dx=tx-g.x,dy=ty-g.y,d=Math.hypot(dx,dy);if(d>20){g.vx=dx/d;g.vy=dy/d;g.x+=g.vx*g.speed*dt;g.y+=g.vy*g.speed*dt;this.keepInside(g)}
 if(g.cd<=1e-9){g.cd=g.cooldown;g.attack=.35/g.scale;this.effects.push({x:g.x,y:g.y,text:'🧞‍♂️ 팔 휘두르기!',kind:'shockwave',side:g.side,team:g.team,life:.55});for(const e of this.enemies(g)){if(e.health<=0||distance(g,e)>170*g.scale+e.radius)continue;this.attack(g,e,g.damage);if(this.result!==null)return}}
}
reviveGenies(){for(const g of this.fighters){if(g.id!=='genie'||g.health>0||g.genieResolved)continue;const owner=this.fighters[g.ownerSide];if(!owner||owner.health<=0){g.genieResolved=true;continue}if(owner.genieRevives>=2){g.genieResolved=true;this.emit('🧞‍♂️ 지니 최종 소멸!');continue}owner.genieRevives++;owner.geniePower*=.5;owner.hp=Math.max(1,owner.hp*.5);owner.health=Math.min(owner.hp,Math.max(1,owner.health*.5));g.hp=1500*(owner.boss?2.5:1);g.health=g.hp;g.damage=50*owner.scale*owner.geniePower;g.cd=3/owner.scale;g.stunUntil=0;g.poison=null;g.toxin=null;g.burn=null;g.genieResolved=false;this.effect(owner,'지니 부활 '+owner.genieRevives+'/2 · 능력 절반','skill');this.emit('🧞‍♂️ 지니 부활! 알라딘의 체력과 지니 공격력이 절반으로 감소') }}
"""+anchor_skill
rep(anchor_skill,genie_code,'genie methods')

# Hook genie special behavior before normal fighter AI.
old_hook="stepFighter(f,e,dt){\n this.transformHero(f);this.updateVampire(f);this.moonSkill(f);this.updateKnightShield(f,dt);"
new_hook="stepFighter(f,e,dt){\n if(f.id==='genie'){this.genieSkill(f,dt);return}\n this.transformHero(f);this.updateVampire(f);this.moonSkill(f);this.updateKnightShield(f,dt);"
rep(old_hook,new_hook,'genie step hook')

# Revive genies after damage/status processing and before normal actions.
old_revive="for(const f of this.fighters)if(f.egg&&f.health>0&&this.time>=f.eggUntil-1e-9)this.revive(f);\n if(this.result!==null)return;"
new_revive="for(const f of this.fighters)if(f.egg&&f.health>0&&this.time>=f.eggUntil-1e-9)this.revive(f);\n this.reviveGenies();\n if(this.result!==null)return;"
rep(old_revive,new_revive,'genie revive hook')

# Relay: dismiss previous summon and spawn genie for a newly entering Aladdin.
old_relay="this.releaseCapture(old);const other=this.fighters[1-side];if(other.captureTarget===side)this.releaseCapture(other);"
new_relay="this.releaseCapture(old);for(const g of this.fighters)if(g.summon&&g.ownerSide===side)g.health=0;const other=this.fighters[1-side];if(other.captureTarget===side)this.releaseCapture(other);"
rep(old_relay,new_relay,'relay dismiss genie')
old_emit="this.fighters[side]=fresh;this.shots=this.shots.filter(s=>s.owner!==side);this.emit((side?'오른쪽':'왼쪽')+' '+(this.relayIndex[side]+1)+'번 '+fresh.name+' 출전!');"
new_emit="this.fighters[side]=fresh;if(fresh.id==='aladdin')this.spawnGenie(fresh);this.shots=this.shots.filter(s=>s.owner!==side);this.emit((side?'오른쪽':'왼쪽')+' '+(this.relayIndex[side]+1)+'번 '+fresh.name+' 출전!');"
rep(old_emit,new_emit,'relay spawn genie')

# Generic collision: genie uses only its swing, not contact melee.
rep("'police','robot'].includes(f.id)","'police','robot','aladdin','genie'].includes(f.id)",'contact exclusion')

# Draw genie clearly and show its HP. Main generic fighter renderer already handles it.
# Add Aladdin/Genie ability HUD text.
old_ability="function ability(f){return f.id==='knight'?"
new_ability="function ability(f){return f.id==='aladdin'?('🧞‍♂️ 지니 '+(f.genieRevives||0)+'/2 부활 사용 · 지니 공격력 x'+(f.geniePower||1)):f.id==='knight'?"
rep(old_ability,new_ability,'aladdin hud')

# Boss rules text update for Moon and Aladdin/Genie.
rep('보스 달은 반달 조각 160 / 1초, 17.5초 후 궁극기를 준비해 5초 뒤 전장 전체 즉사 공격을 사용해.','보스 달은 관통 반달 조각 160 / 1초, 22.5초 후 궁극기를 준비해 5초 뒤 전장 전체 즉사 공격을 사용해. 보스 알라딘의 지니는 체력 3750, 공격력·속도·공격 주기 등 보스 능력 배율을 함께 적용받아.','boss rules')

p.write_text(s,encoding='utf-8')
print('NEON RUMBLE v3.20 patch applied')
