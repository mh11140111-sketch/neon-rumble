from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

def rep(old, new, label, count=1):
    global s
    if old not in s:
        raise SystemExit(f'PATCH FAILED: {label}')
    s = s.replace(old, new, count)

# Version + patch notes
rep('BATTLE <b>v3.14</b>', 'BATTLE <b>v3.15</b>', 'version badge')
rep('📒 패치노트 · v3.14', '📒 패치노트 · v3.15', 'patch summary')
rep('<div class="patch-body"><div class="patch-version"><h3>v3.14 · 팀 배틀 & 모아이</h3>', '<div class="patch-body"><div class="patch-version"><h3>v3.15 · 독침 복어</h3><ul><li>흡혈귀가 🦇 박쥐 상태일 때 흡혈 회복량이 30% 증가. 일반 흡혈귀는 실제 피해의 35% → 45.5% 회복.</li><li>신규 캐릭터 🐡 복어 추가: 8방향으로 가시를 동시에 발사하며 가시 피해 20.</li><li>복어 가시에 맞은 적은 맹독에 걸림: 3초 동안 0.5초마다 10 피해. 기존 독과 동시에 적용 가능.</li><li>복어 몸에 직접 닿은 적은 기존 독에 걸림.</li></ul></div><div class="patch-version"><h3>v3.14 · 팀 배틀 & 모아이</h3>', 'patch v3.15 block')

# Vampire bat lifesteal +30% relative increase
rep("const heal=Math.min(f.hp-f.health,Math.round(n*f.lifesteal));", "const heal=Math.min(f.hp-f.health,Math.round(n*f.lifesteal*(f.id==='vampire'&&f.vampireBat?1.3:1)));", 'vampire bat lifesteal')
s = s.replace("체력이 30% 이하가 되면 🦇 박쥐로 변신해 이동속도가 100% 증가하고, 30%를 넘게 회복하면 다시 흡혈귀로 돌아와.", "체력이 30% 이하가 되면 🦇 박쥐로 변신해 이동속도가 100% 증가하고 흡혈 회복량도 30% 증가해. 30%를 넘게 회복하면 다시 흡혈귀로 돌아와.", 1)
s = s.replace("HP 30% 이하: 박쥐 / 이동속도 ×2 · HP 30% 초과: 흡혈귀 복귀", "HP 30% 이하: 박쥐 / 이동속도 ×2 / 흡혈 회복량 ×1.3 · HP 30% 초과: 흡혈귀 복귀", 1)

# Add puffer to roster after Moai
moai = "{id:'moai',name:'모아이',icon:'🗿',tag:'점프 · 전장 충격파',hp:1000,damage:70,speed:0,cooldown:3,description:'일반 이동은 하지 않고 3초마다 점프로 위치를 바꿔. 착지할 때 맵 전체에 충격파를 일으켜 적 전원에게 피해 70. 몸 크기는 일반 캐릭터의 1.5배.',detail:'일반 이동 불가 · 점프 3초마다 · 전장 전체 충격파 70 · 기본 크기 1.5배'}"
puffer = "{id:'puffer',name:'복어',icon:'🐡',tag:'8방향 가시 · 맹독',hp:1000,damage:20,speed:145,cooldown:1,description:'1초마다 상하좌우와 대각선까지 8방향으로 가시를 동시에 발사해. 가시 피해는 20이며, 맞은 적은 3초 동안 0.5초마다 10 피해를 받는 맹독에 걸려. 맹독은 기존 독과 중첩 가능하고, 복어 몸에 직접 닿은 적은 독에 걸려.',detail:'8방향 가시 20 · 발사 간격 1초 · 맹독 3초 / 0.5초마다 10 · 기존 독과 중첩 · 몸 접촉 시 독'}"
rep(moai + "\n];", moai + "\n," + puffer + "\n];", 'puffer roster')

# Fighter state: separate toxin status so it can coexist with poison
rep("poison:null,slashCd:0", "poison:null,toxin:null,slashCd:0", 'toxin field')

# Puffer 8-direction spike skill
anchor = "moaiJump(f){if(f.id!=='moai'||f.health<=0||this.time<f.nextJump-1e-9)return;"
if anchor not in s:
    raise SystemExit('PATCH FAILED: moai method anchor')
insert_at = s.index('stepFighter(f,e,dt){', s.index(anchor))
puffer_method = "pufferSpikes(f){if(f.id!=='puffer'||f.health<=0||f.cd>1e-9)return;for(let i=0;i<8;i++){const a=i*Math.PI/4,vx=Math.cos(a),vy=Math.sin(a);this.shots.push({x:f.x+vx*(f.radius+7),y:f.y+vy*(f.radius+7),vx,vy,owner:f.side,team:f.team,target:-1,kind:'spike',radius:5*f.scale,speed:360*f.scale,damage:20*f.scale,life:3*f.scale,bounces:0,toxin:true})}f.cd=f.cooldown;f.attack=.18/f.scale;this.effect(f,'8방향 가시!','skill')}\n"
s = s[:insert_at] + puffer_method + s[insert_at:]

# Fire puffer spikes from stepFighter
rep("if(f.id==='moon'&&f.cd<=1e-9)this.moonThrow(f,e);", "if(f.id==='moon'&&f.cd<=1e-9)this.moonThrow(f,e);\n if(f.id==='puffer'&&f.cd<=1e-9)this.pufferSpikes(f);", 'puffer firing')

# Puffer contact applies existing poison; puffer itself has no normal melee attack
rep("if(f.id==='spider'&&f.health>0&&f.stunUntil<=this.time)this.applyPoison(f,e);", "if(f.id==='spider'&&f.health>0&&f.stunUntil<=this.time)this.applyPoison(f,e);if(f.id==='puffer'&&f.health>0&&f.stunUntil<=this.time)this.applyPoison(f,e);", 'puffer contact poison')
rep("'moon','invisible','moai'].includes(f.id)", "'moon','invisible','moai','puffer'].includes(f.id)", 'puffer melee exclusion')

# Toxin application from spike projectiles
rep("if(s.poison&&e.health>0)this.applyPoison(f,e);if(s.kind==='magic')", "if(s.poison&&e.health>0)this.applyPoison(f,e);if(s.toxin&&e.health>0)this.applyToxin(f,e);if(s.kind==='magic')", 'projectile toxin')

# Tick toxin independently from normal poison/burn
rep("for(const f of this.fighters){if(f.health>0)this.tickPoison(f);if(this.result!==null)return;if(f.health>0)this.tickBurn(f);if(this.result!==null)return;}", "for(const f of this.fighters){if(f.health>0)this.tickPoison(f);if(this.result!==null)return;if(f.health>0)this.tickToxin(f);if(this.result!==null)return;if(f.health>0)this.tickBurn(f);if(this.result!==null)return;}", 'toxin ticking')

# Insert toxin functions before tickPoison
needle = "tickPoison(e){\n const p=e.poison;if(!p||e.health<=0)return;"
if needle not in s:
    raise SystemExit('PATCH FAILED: tickPoison anchor')
toxin_code = "applyToxin(f,e){\n if(f.team===e.team||e.health<=0||this.isStudying(e))return;const damage=10*f.scale,interval=.5/f.scale,old=e.toxin;if(old&&old.expires>=this.time){old.expires=this.time+3*f.scale;if(damage>=old.damage){old.damage=damage;old.interval=interval;old.source=f.side;old.next=Math.min(old.next,this.time+interval)}}else e.toxin={source:f.side,damage,interval,next:this.time+interval,expires:this.time+3*f.scale};this.effect(e,'맹독','poison')\n}\ntickToxin(e){\n const p=e.toxin;if(!p||e.health<=0)return;while(p.next<=this.time+1e-9&&p.next<=p.expires+1e-9){const tick=p.next;p.next+=p.interval;if(e.id==='nerd'&&tick>=e.studyStart-1e-9&&tick<e.studyUntil-1e-9)continue;const source=this.fighters[p.source];if(!source||source.team===e.team){e.toxin=null;return}const n=Math.min(e.health,Math.round(p.damage*(1-e.armor)));e.health-=n;source.damageDealt+=n;this.effect(e,'맹독 −'+n,'poison');if(this.formEgg(e))return;if(e.health===0){e.trail=[];e.toxin=null;this.emit(e.name+' 맹독으로 탈락!');this.checkEnd();return}}if(this.time>=p.expires-1e-9)e.toxin=null;\n}\n"
s = s.replace(needle, toxin_code + needle, 1)

# Clean toxin on transformations / phoenix state changes
s = s.replace("f.poison=null;f.burn=null;f.venom=null;", "f.poison=null;f.toxin=null;f.burn=null;f.venom=null;", 1)
s = s.replace("f.poison=null;f.burn=null;f.stunUntil=0;f.attack=0;", "f.poison=null;f.toxin=null;f.burn=null;f.stunUntil=0;f.attack=0;", 1)
s = s.replace("f.poison=null;f.burn=null;f.stunUntil=0;f.peckCd=0;", "f.poison=null;f.toxin=null;f.burn=null;f.stunUntil=0;f.peckCd=0;", 1)

# Spike drawing
rep("}else if(s.kind==='arrow'){ctx.strokeStyle=colors[s.team];", "}else if(s.kind==='spike'){ctx.strokeStyle='#e8f5ff';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(-10,0);ctx.lineTo(10,0);ctx.moveTo(4,-5);ctx.lineTo(10,0);ctx.lineTo(4,5);ctx.stroke()}else if(s.kind==='arrow'){ctx.strokeStyle=colors[s.team];", 'spike drawing')

# Ability/HUD text
rep("function ability(f){return f.id==='invisible'?", "function ability(f){return f.id==='puffer'?'8방향 가시 20 · 맹독 3초 · 접촉 독':f.id==='invisible'?", 'puffer ability')
s = s.replace("f.vampireBat?'🦇 박쥐 · 이동속도 +100%'", "f.vampireBat?'🦇 박쥐 · 이동속도 +100% · 흡혈 회복 +30%'", 1)
rep("+(f.poison?' · 중독 '+Math.max(0,Math.ceil(f.poison.expires-engine.time))+'초':'')", "+(f.poison?' · 중독 '+Math.max(0,Math.ceil(f.poison.expires-engine.time))+'초':'')+(f.toxin?' · 맹독 '+Math.max(0,Math.ceil(f.toxin.expires-engine.time))+'초':'')", 'toxin HUD')

p.write_text(s, encoding='utf-8')
print('v3.15 patch applied')
# trigger-v315
