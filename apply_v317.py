from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if old not in s:
        raise SystemExit(f'PATCH FAILED: {label}')
    s=s.replace(old,new,count)

# Version badge and patch note header
rep('BATTLE <b>v3.16</b>','BATTLE <b>v3.17</b>','version badge')
rep('📒 패치노트 · v3.16','📒 패치노트 · v3.17','patch note summary')

# Add v3.17 patch note before v3.16
anchor='<div class="patch-body"><div class="patch-version"><h3>v3.16 · 회전 방패 기사</h3>'
insert='''<div class="patch-body"><div class="patch-version"><h3>v3.17 · 누적 방패 & 경찰</h3><ul><li>기사: 방패가 막은 피해를 누적해 500에 도달하면 충격파 발동. 충격파 발동 후 누적 피해는 0으로 초기화.</li><li>모아이: 독·맹독·화상 등 지속 상태이상에 면역.</li><li>신규 캐릭터 👮‍♂️ 경찰 추가: 1초마다 테이저건 피해 30 + 0.2초 기절.</li><li>경찰은 HP 30% 이하에서 경기당 1회, 3초 동안 0.3초마다 8방향으로 피해 100 총탄을 난사.</li></ul></div><div class="patch-version"><h3>v3.16 · 회전 방패 기사</h3>'''
rep(anchor,insert,'patch note insert')

# Update knight roster wording and add police after puffer
old_knight="{id:'knight',name:'기사',icon:'🛡️',tag:'회전 방패 · 검격',hp:1000,damage:95,speed:125,cooldown:.95,description:'적에게 접근해 검격 95로 공격해. 작은 방패가 주변을 회전하며 충전된 방패는 공격 1회를 완전히 막아. 사용한 방패는 10초 뒤 재충전되고, 500 이상 피해를 막으면 전장 충격파를 발동해.',detail:'검격 95 · 공격 간격 0.95초 · 방패 1회 완전 방어 / 사용 후 10초 재충전 · 500+ 피해 방어 시 충격파 100 / 자신 제외 전원 3초 기절'},"
new_knight="{id:'knight',name:'기사',icon:'🛡️',tag:'회전 방패 · 누적 충격파',hp:1000,damage:95,speed:125,cooldown:.95,description:'적에게 접근해 검격 95로 공격해. 회전 방패가 투사체를 막고 충전 중에는 방어 범위 안의 투사체를 확정 차단해. 방패가 막은 피해가 누적 500에 도달하면 전장 충격파를 발동해.',detail:'검격 95 · 공격 간격 0.95초 · 방패로 막은 피해 누적 500 → 충격파 100 / 자신 제외 전원 3초 기절 · 발동 후 누적 0'},"
rep(old_knight,new_knight,'knight roster')

puffer="{id:'puffer',name:'복어',icon:'🐡',tag:'8방향 가시 · 맹독',hp:1000,damage:20,speed:145,cooldown:1,description:'1초마다 상하좌우와 대각선까지 8방향으로 가시를 동시에 발사해. 가시 피해는 20이며, 맞은 적은 3초 동안 0.5초마다 10 피해를 받는 맹독에 걸려. 맹독은 기존 독과 중첩 가능하고, 복어 몸에 직접 닿은 적은 독에 걸려.',detail:'8방향 가시 20 · 발사 간격 1초 · 맹독 3초 / 0.5초마다 10 · 기존 독과 중첩 · 몸 접촉 시 독'}"
police="""{id:'puffer',name:'복어',icon:'🐡',tag:'8방향 가시 · 맹독',hp:1000,damage:20,speed:145,cooldown:1,description:'1초마다 상하좌우와 대각선까지 8방향으로 가시를 동시에 발사해. 가시 피해는 20이며, 맞은 적은 3초 동안 0.5초마다 10 피해를 받는 맹독에 걸려. 맹독은 기존 독과 중첩 가능하고, 복어 몸에 직접 닿은 적은 독에 걸려.',detail:'8방향 가시 20 · 발사 간격 1초 · 맹독 3초 / 0.5초마다 10 · 기존 독과 중첩 · 몸 접촉 시 독'}
,{id:'police',name:'경찰',icon:'👮‍♂️',tag:'테이저 · 총 난사',hp:1000,damage:30,speed:155,cooldown:1,description:'1초마다 테이저건을 발사해 피해 30과 0.2초 기절을 줘. 체력이 30% 이하가 되면 경기당 1회, 3초 동안 사방팔방으로 총을 난사해.',detail:'테이저 30 / 1초 · 명중 시 기절 0.2초 · HP 30% 이하 1회 총 난사 · 3초 동안 0.3초마다 8방향 · 총탄 100'}"""
rep(puffer,police,'police roster')

# Fighter state: knight accumulated blocked damage and police ultimate state
old_state="knightShieldReady:false,knightShieldNext:type.id==='knight'?10:0,knightShieldChargedUntil:type.id==='knight'?3:0,knightShieldAngle:0,nextJump:"
new_state="knightShieldReady:false,knightShieldNext:type.id==='knight'?10:0,knightShieldChargedUntil:type.id==='knight'?3:0,knightShieldAngle:0,knightBlockedDamage:0,policeBarrageUsed:false,policeBarrageUntil:0,policeBarrageCd:0,nextJump:"
rep(old_state,new_state,'fighter state')

# Knight cumulative blocked damage. Reset after shockwave.
old_block="blockProjectileWithKnight(f,s,owner){const raw=s.instant?f.health:(s.damage||0);s.life=0;this.effect(f,this.time<f.knightShieldChargedUntil-1e-9?'🛡️ 완전 방어!':'🛡️ 방패 막기!','skill');if(raw>=500)this.knightShockwave(f);if(owner){owner.attack=.12/owner.scale}return true}"
new_block="blockProjectileWithKnight(f,s,owner){const raw=s.instant?f.health:(s.damage||0);s.life=0;f.knightBlockedDamage+=Math.max(0,raw);this.effect(f,this.time<f.knightShieldChargedUntil-1e-9?'🛡️ 완전 방어!':'🛡️ 방패 막기!','skill');if(f.knightBlockedDamage>=500){f.knightBlockedDamage=0;this.knightShockwave(f)}if(owner){owner.attack=.12/owner.scale}return true}"
rep(old_block,new_block,'knight cumulative')

# Moai status immunity: burn, poison, toxin
rep("applyBurn(f,e,friendly=false){if(e.id==='phoenix')return;", "applyBurn(f,e,friendly=false){if(e.id==='phoenix'||e.id==='moai')return;", 'moai burn immunity')
rep("applyPoison(f,e){\n if(f.team===e.team||e.health<=0||this.isStudying(e))return;", "applyPoison(f,e){\n if(e.id==='moai'||f.team===e.team||e.health<=0||this.isStudying(e))return;", 'moai poison immunity')
rep("applyToxin(f,e){\n if(f.team===e.team||e.health<=0||this.isStudying(e))return;", "applyToxin(f,e){\n if(e.id==='moai'||f.team===e.team||e.health<=0||this.isStudying(e))return;", 'moai toxin immunity')
rep("tickBurn(e){if(e.id==='phoenix'){e.burn=null;return}", "tickBurn(e){if(e.id==='phoenix'||e.id==='moai'){e.burn=null;return}", 'moai burn clear')
rep("tickToxin(e){\n const p=e.toxin;", "tickToxin(e){\n if(e.id==='moai'){e.toxin=null;return}const p=e.toxin;", 'moai toxin clear')
rep("tickPoison(e){\n const p=e.poison;", "tickPoison(e){\n if(e.id==='moai'){e.poison=null;return}const p=e.poison;", 'moai poison clear')

# Police methods inserted before pufferSpikes
anchor2="pufferSpikes(f){if(f.id!=='puffer'||f.health<=0||f.cd>1e-9)return;"
helpers="""policeTaser(f,e){if(f.id!=='police'||f.health<=0||f.cd>1e-9)return;const a=this.aim(f,e);this.shots.push({x:f.x+a.x*(f.radius+6),y:f.y+a.y*(f.radius+6),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'taser',radius:6*f.scale,speed:420*f.scale,damage:30*f.scale,life:3*f.scale,bounces:0,stun:.2*f.scale});f.cd=f.cooldown;f.attack=.16/f.scale;this.effect(f,'⚡ 테이저!','skill')}
startPoliceBarrage(f){if(f.id!=='police'||f.health<=0||f.policeBarrageUsed||f.health>f.hp*.3)return;f.policeBarrageUsed=true;f.policeBarrageUntil=this.time+3;f.policeBarrageCd=0;this.effect(f,'🔫 총 난사!','skill');this.emit('👮‍♂️ 경찰이 3초간 총 난사를 시작!')}
policeBarrage(f){if(f.id!=='police'||f.health<=0||this.time>=f.policeBarrageUntil-1e-9)return;if(this.time<f.policeBarrageCd-1e-9)return;f.policeBarrageCd=this.time+.3/f.scale;for(let i=0;i<8;i++){const a=i*Math.PI/4,vx=Math.cos(a),vy=Math.sin(a);this.shots.push({x:f.x+vx*(f.radius+7),y:f.y+vy*(f.radius+7),vx,vy,owner:f.side,team:f.team,target:-1,kind:'bullet',radius:4*f.scale,speed:520*f.scale,damage:100*f.scale,life:2.5*f.scale,bounces:0})}f.attack=.12/f.scale}
"""
if anchor2 not in s: raise SystemExit('PATCH FAILED: police method anchor')
s=s.replace(anchor2,helpers+anchor2,1)

# Police action in stepFighter
rep(" if(f.id==='puffer'&&f.cd<=1e-9)this.pufferSpikes(f);", " if(f.id==='police'){this.startPoliceBarrage(f);this.policeBarrage(f);if(this.time>=f.policeBarrageUntil-1e-9&&f.cd<=1e-9)this.policeTaser(f,e)}\n if(f.id==='puffer'&&f.cd<=1e-9)this.pufferSpikes(f);", 'police step')

# Projectile stun for taser
old_proj="if(s.toxin&&e.health>0)this.applyToxin(f,e);if(s.kind==='magic'){e.slow=Math.max(e.slow,1.2*f.scale);e.slowPower=Math.max(e.slowPower,f.magicSlowStrength)}}"
new_proj="if(s.toxin&&e.health>0)this.applyToxin(f,e);if(s.stun&&e.health>0)e.stunUntil=Math.max(e.stunUntil,this.time+s.stun);if(s.kind==='magic'){e.slow=Math.max(e.slow,1.2*f.scale);e.slowPower=Math.max(e.slowPower,f.magicSlowStrength)}}"
rep(old_proj,new_proj,'taser stun')

# Exclude police from melee collision attack
rep("'villain','moon','invisible','moai','puffer'].includes(f.id)", "'villain','moon','invisible','moai','puffer','police'].includes(f.id)", 'police melee exclusion')

# Ability HUD
old_ability="function ability(f){return f.id==='knight'?(engine.time<f.knightShieldChargedUntil?'🛡️ 완전 방어 '+Math.max(0,f.knightShieldChargedUntil-engine.time).toFixed(1)+'초':'🛡️ 회전 방패 · 충전 '+Math.max(0,f.knightShieldNext-engine.time).toFixed(1)+'초')"
new_ability="function ability(f){return f.id==='knight'?(engine.time<f.knightShieldChargedUntil?'🛡️ 완전 방어 '+Math.max(0,f.knightShieldChargedUntil-engine.time).toFixed(1)+'초 · 누적 '+Math.round(f.knightBlockedDamage)+'/500':'🛡️ 회전 방패 · 충전 '+Math.max(0,f.knightShieldNext-engine.time).toFixed(1)+'초 · 누적 '+Math.round(f.knightBlockedDamage)+'/500'):f.id==='police'?(f.policeBarrageUsed?(engine.time<f.policeBarrageUntil?'🔫 총 난사 '+Math.max(0,f.policeBarrageUntil-engine.time).toFixed(1)+'초':'⚡ 테이저 30 · 난사 소진'):'⚡ 테이저 30 · HP 30% 이하 총 난사 대기')"
rep(old_ability,new_ability,'ability hud')

# Draw taser/bullet projectiles before spike branch
old_draw="else if(s.kind==='spike'){ctx.strokeStyle='#e8f5ff';ctx.lineWidth=4;"
new_draw="else if(s.kind==='taser'){ctx.strokeStyle='#ffe66d';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(-10,-4);ctx.lineTo(-2,0);ctx.lineTo(-10,4);ctx.moveTo(1,-4);ctx.lineTo(9,0);ctx.lineTo(1,4);ctx.stroke()}else if(s.kind==='bullet'){circle(0,0,7,'#ffd36b');circle(0,0,3,'#fff')}else if(s.kind==='spike'){ctx.strokeStyle='#e8f5ff';ctx.lineWidth=4;"
rep(old_draw,new_draw,'projectile draw')

p.write_text(s,encoding='utf-8')
print('v3.17 patch applied')
