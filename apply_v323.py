from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if s.count(old)<count:
        raise SystemExit(f'PATCH FAILED: {label} ({s.count(old)}/{count})')
    s=s.replace(old,new,count)

# version / notes
rep('BATTLE <b>v3.22</b>','BATTLE <b>v3.23</b>','version')
rep('📒 패치노트 · v3.22','📒 패치노트 · v3.23','notes title')
anchor='<div class="patch-body"><div class="patch-version"><h3>v3.22 · 편의성 & 달 귀환타</h3>'
insert='<div class="patch-body"><div class="patch-version"><h3>v3.23 · 밸런스 & 로봇 회전팔</h3><ul><li>지니 회전팔 피해 100 → 125.</li><li>모아이 충격파 명중 시 30% 확률로 3초 기절.</li><li>기사에게 상시 피해 감소 30% 추가.</li><li>궁수 화살 피해 70 → 85.</li><li>나무는 화상·독·맹독 지속 피해를 2배로 받음.</li><li>로봇 신규 패시브: 🦾 로봇팔이 주변을 항상 천천히 회전하며, 닿은 적에게 피해 70 + 1초 기절.</li></ul></div><div class="patch-version"><h3>v3.22 · 편의성 & 달 귀환타</h3>'
rep(anchor,insert,'notes body')

# archer
rep("{id:'archer',name:'궁수',icon:'🏹',tag:'무작위 사격',hp:1000,damage:70,speed:155,cooldown:.38,description:'0.38초마다 랜덤한 방향으로 화살을 발사. 화살은 벽에서 한 번 튕겨.',detail:'화살 70 · 사격 간격 0.38초 · 조준 없음'}",
    "{id:'archer',name:'궁수',icon:'🏹',tag:'무작위 사격',hp:1000,damage:85,speed:155,cooldown:.38,description:'0.38초마다 랜덤한 방향으로 피해 85의 화살을 발사. 화살은 벽에서 한 번 튕겨.',detail:'화살 85 · 사격 간격 0.38초 · 조준 없음'}",'archer')

# knight text
rep("description:'적에게 접근해 검격 95로 공격해. 회전 방패가 투사체를 막고 충전 중에는 방어 범위 안의 투사체를 확정 차단해. 방패가 막은 피해가 누적 500에 도달하면 전장 충격파를 발동해.',detail:'검격 95 · 공격 간격 0.95초 · 방패로 막은 피해 누적 500 → 충격파 100 / 자신 제외 전원 3초 기절 · 발동 후 누적 0'",
    "description:'받는 피해가 항상 30% 감소해. 적에게 접근해 검격 95로 공격하고, 회전 방패가 투사체를 막아. 방패가 막은 피해가 누적 500에 도달하면 전장 충격파를 발동해.',detail:'피해 감소 30% · 검격 95 · 공격 간격 0.95초 · 방패로 막은 피해 누적 500 → 충격파 100 / 자신 제외 전원 3초 기절 · 발동 후 누적 0'",'knight text')

# tree text
rep("description:'제자리에 뿌리내려 대각선까지 8방향으로 짧은 뿌리를 펼쳐. 1초마다 길어지며, 닿은 상대에게 지속 피해와 40% 감속. 피해를 줄 때마다 현재 체력의 3% 회복(보스도 3%).',detail:'8방향 · 뿌리 시작 12 · 초당 길이 +18 · 접촉 시 0.5초마다 피해 25 · 명중 시 현재 체력 3% 회복 · 이동 불가'",
    "description:'제자리에 뿌리내려 대각선까지 8방향으로 뿌리를 펼쳐. 닿은 상대에게 지속 피해와 감속을 주지만 화상·독·맹독 지속 피해는 2배로 받아.',detail:'8방향 · 뿌리 시작 12 · 초당 길이 +18 · 접촉 시 0.5초마다 피해 25 · 명중 시 현재 체력 3% 회복 · 화상/독/맹독 피해 ×2 · 이동 불가'",'tree text')

# moai text
rep("description:'일반 이동은 하지 않고 3초마다 점프로 위치를 바꿔. 착지할 때 맵 전체에 충격파를 일으켜 적 전원에게 피해 70. 몸 크기는 일반 캐릭터의 1.5배.',detail:'일반 이동 불가 · 점프 3초마다 · 전장 전체 충격파 70 · 기본 크기 1.5배'",
    "description:'일반 이동은 하지 않고 3초마다 점프로 위치를 바꿔. 착지 충격파는 적 전원에게 피해 70을 주고 30% 확률로 3초 기절시켜.',detail:'일반 이동 불가 · 점프 3초마다 · 전장 전체 충격파 70 · 명중 시 30% 확률 3초 기절 · 기본 크기 1.5배'",'moai text')

# robot text
rep("description:'5초마다 맵 전체를 천천히 한 바퀴 도는 레이저를 발사해 피해 70. 7초마다 만능로봇팔로 자신을 제외한 모든 캐릭터를 밀쳐내고 피해 50과 1초 기절을 줘.',detail:'레이저 70 · 5초마다 · 4초간 1회전 · 회전당 대상별 1회 피격 · 로봇팔 50 · 7초 · 전장 전체 밀치기 · 기절 1초'",
    "description:'5초마다 회전 레이저를 발사하고 7초마다 만능로봇팔을 사용해. 추가로 🦾 로봇팔 하나가 몸 주변을 항상 천천히 돌며 닿은 적에게 피해 70과 1초 기절을 줘.',detail:'레이저 70 · 5초마다 · 만능로봇팔 50 / 7초 · 상시 회전팔 70 + 기절 1초 · 같은 대상 연속 피격 방지'",'robot text')

# aladdin / genie text + damage
rep('회전팔 100 / 3초','회전팔 125 / 3초','aladdin detail')
rep('관통 피해 100을 줘','관통 피해 125를 줘','aladdin desc')
rep("damage:100*scale*(owner.geniePower||1)","damage:125*scale*(owner.geniePower||1)",'genie spawn damage')
rep("g.damage=100*owner.scale*owner.geniePower","g.damage=125*owner.scale*owner.geniePower",'genie revive damage')
rep("' HP · 회전팔 100 · 부활 '","' HP · 회전팔 125 · 부활 '",'ability text')

# knight armor
rep("armor:0,lifesteal:type.id==='vampire'?.35*scale:0","armor:type.id==='knight'?.3:0,lifesteal:type.id==='vampire'?.35*scale:0",'knight armor')

# tree takes double DOT damage
rep("Math.round(p.damage*(1-e.armor))","Math.round(p.damage*(e.id==='tree'?2:1)*(1-e.armor))",'burn dot',1)
# toxin and poison are the next two identical formulas
rep("Math.round(p.damage*(1-e.armor))","Math.round(p.damage*(e.id==='tree'?2:1)*(1-e.armor))",'toxin dot',1)
rep("Math.round(p.damage*(1-e.armor))","Math.round(p.damage*(e.id==='tree'?2:1)*(1-e.armor))",'poison dot',1)

# moai stun chance after successful shockwave damage
old="moaiJump(f){if(f.id!=='moai'||f.health<=0||this.time<f.nextJump-1e-9)return;const {low,high}=this.bounds(f);f.x=this.rand(low,high);f.y=this.rand(low,high);f.vx=0;f.vy=0;f.nextJump=this.time+3/f.scale;f.jumpFx=.8;this.effects.push({x:f.x,y:f.y,text:'충격파!',kind:'shockwave',side:f.side,team:f.team,life:.8});this.resolvingBlast=true;for(const e of [...this.enemies(f)])if(e.health>0)this.attack(f,e,70*f.scale);this.resolvingBlast=false;this.checkEnd();this.emit('🗿 모아이 착지! 전장 전체 충격파')}"
new="moaiJump(f){if(f.id!=='moai'||f.health<=0||this.time<f.nextJump-1e-9)return;const {low,high}=this.bounds(f);f.x=this.rand(low,high);f.y=this.rand(low,high);f.vx=0;f.vy=0;f.nextJump=this.time+3/f.scale;f.jumpFx=.8;this.effects.push({x:f.x,y:f.y,text:'충격파!',kind:'shockwave',side:f.side,team:f.team,life:.8});this.resolvingBlast=true;for(const e of [...this.enemies(f)]){if(e.health<=0)continue;const dealt=this.attack(f,e,70*f.scale);if(dealt>0&&e.health>0&&this.random()<.3){e.stunUntil=Math.max(e.stunUntil,this.time+3*f.scale);this.effect(e,'기절 3초!','skill')}}this.resolvingBlast=false;this.checkEnd();this.emit('🗿 모아이 착지! 전장 전체 충격파')}"
rep(old,new,'moai stun')

# robot passive rotating arm: initialize, rotate, collide; 1-second per-target rehit guard.
rep("robotSkill(f){\n if(f.id!=='robot'||f.health<=0)return;\n if(f.robotLaserNext===undefined){f.robotLaserNext=this.time+5/f.scale;f.robotLaserStart=-1;f.robotLaserUntil=-1;f.robotLaserHits={};f.robotArmNext=this.time+7/f.scale}",
    "robotSkill(f,dt){\n if(f.id!=='robot'||f.health<=0)return;\n if(f.robotLaserNext===undefined){f.robotLaserNext=this.time+5/f.scale;f.robotLaserStart=-1;f.robotLaserUntil=-1;f.robotLaserHits={};f.robotArmNext=this.time+7/f.scale;f.robotOrbitAngle=0;f.robotOrbitHits={}}\n f.robotOrbitAngle=(f.robotOrbitAngle+dt*.85*f.scale)%(Math.PI*2);const oa=f.robotOrbitAngle,or=f.radius+62*f.scale,ox=f.x+Math.cos(oa)*or,oy=f.y+Math.sin(oa)*or;for(const e of this.enemies(f)){if(e.health<=0||Math.hypot(e.x-ox,e.y-oy)>e.radius+24*f.scale||((f.robotOrbitHits[e.side]||0)>this.time))continue;const dealt=this.attack(f,e,70*f.scale);if(dealt>0){f.robotOrbitHits[e.side]=this.time+1/f.scale;if(e.health>0){e.stunUntil=Math.max(e.stunUntil,this.time+1*f.scale);this.effect(e,'🦾 70 · 기절!','skill')}}if(this.result!==null)return}",
    'robot skill signature/passive')
rep("if(f.id==='robot')this.robotSkill(f);","if(f.id==='robot')this.robotSkill(f,dt);",'robot call')

# Draw always-orbiting robot arm with safe primitive canvas calls.
needle="if(f.id==='knight'&&f.health>0){const a=f.knightShieldAngle||engine.time*2.8"
insert_draw="if(f.id==='robot'&&f.health>0&&Number.isFinite(f.robotOrbitAngle)){const ra=f.robotOrbitAngle,rr=f.radius+62*f.scale,rx=f.x+Math.cos(ra)*rr,ry=f.y+Math.sin(ra)*rr;ctx.save();ctx.strokeStyle='#7ca8d8';ctx.lineWidth=10*f.scale;ctx.beginPath();ctx.moveTo(f.x,f.y);ctx.lineTo(rx,ry);ctx.stroke();ctx.font=(30*f.scale)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🦾',rx,ry);ctx.restore();}"
if needle not in s: raise SystemExit('PATCH FAILED: robot draw anchor')
s=s.replace(needle,insert_draw+needle,1)

p.write_text(s,encoding='utf-8')
print('NEON RUMBLE v3.23 applied')
