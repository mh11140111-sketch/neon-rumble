from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

# Submarine hotfix: keep v3.67 and patch notes untouched.
# 1) Slightly increase snail speed.
once("{id:'snail',name:'달팽이',icon:'🐌',tag:'초저속 · 초고화력 · 껍질 방어',hp:1000,damage:6767676767,speed:20,cooldown:1,description:'매우매우 느리게 이동하지만 근접 공격 피해가 6,767,676,767이다. HP 30% 이하가 되면 전투당 1회 5초 동안 껍질에 숨어 받는 피해를 1/5로 줄이고 0.5초마다 HP 20을 회복한다.',detail:'HP 1000 · 이동속도 20 · 근접 6,767,676,767 · HP 30% 이하 1회 · 껍질 5초 · 피해 80% 감소 · 0.5초마다 HP 20 회복'},",
     "{id:'snail',name:'달팽이',icon:'🐌',tag:'초저속 · 초고화력 · 껍질 방어',hp:1000,damage:6767676767,speed:28,cooldown:1,description:'매우 느리게 가장 가까운 적을 계속 추적하며, 0.3초 이상 연속 접촉해야 근접 공격 피해 6,767,676,767을 준다. HP 30% 이하가 되면 전투당 1회 5초 동안 껍질에 숨어 받는 피해를 1/5로 줄이고 0.5초마다 HP 20을 회복한다.',detail:'HP 1000 · 이동속도 28 · 0.3초 연속 접촉 후 근접 6,767,676,767 · HP 30% 이하 1회 · 껍질 5초 · 피해 80% 감소 · 0.5초마다 HP 20 회복'},",
     'snail roster speed')

# 2) Give snail dedicated continuous-contact state.
once("psychicPushNext:type.id==='psychic'?5/scale:9999,psychicOrbitAngle:0,airborneUntil:0,",
     "psychicPushNext:type.id==='psychic'?5/scale:9999,psychicOrbitAngle:0,snailContactSide:null,snailContactTime:0,airborneUntil:0,",
     'snail contact state')

# 3) Chase the nearest enemy continuously in AI-controlled combat instead of random wandering.
old="const manual=(this.mode==='control'||this.manualTeam0)&&f.team===0&&!(this.mansionMode&&f.summon),heroAuto=f.id==='hero'&&f.heroReady;if(manual&&!heroAuto){f.vx=Number(this.controlX)||0;f.vy=Number(this.controlY)||0;f.turn=1}else if(!heroAuto&&f.dash<=0){if(f.turn<=0)this.turn(f);if(['knight','vampire','smith','skeleton_sword'].includes(f.id)){const a=this.aim(f,e),k=(f.id==='smith'?.65:1.8)*f.scale;const x=f.vx+a.x*k*dt,y=f.vy+a.y*k*dt,n=Math.hypot(x,y)||1;f.vx=x/n;f.vy=y/n}}"
new="const manual=(this.mode==='control'||this.manualTeam0)&&f.team===0&&!(this.mansionMode&&f.summon),heroAuto=f.id==='hero'&&f.heroReady;if(manual&&!heroAuto){f.vx=Number(this.controlX)||0;f.vy=Number(this.controlY)||0;f.turn=1}else if(f.id==='snail'&&!heroAuto&&f.dash<=0){const a=this.aim(f,e);f.vx=a.x;f.vy=a.y;f.turn=.2}else if(!heroAuto&&f.dash<=0){if(f.turn<=0)this.turn(f);if(['knight','vampire','smith','skeleton_sword'].includes(f.id)){const a=this.aim(f,e),k=(f.id==='smith'?.65:1.8)*f.scale;const x=f.vx+a.x*k*dt,y=f.vy+a.y*k*dt,n=Math.hypot(x,y)||1;f.vx=x/n;f.vy=y/n}}"
once(old,new,'snail chase AI')

# 4) Dedicated 0.3 sec continuous-contact attack. Reset if contact breaks or target changes.
anchor="if(f.id==='hero'&&f.heroReady&&f.heroPhase==='rush'&&distance(f,e)<=f.radius+e.radius+5){const aim=this.aim(f,e);this.attack(f,e,250*f.scale);f.heroPhase='retreat';f.retreatHit=false;f.retreatUntil=this.time+.65/f.scale;f.vx=-aim.x;f.vy=-aim.y;this.effect(f,'돌진!','skill')}"
insert=anchor+"\n if(f.id==='snail'){const touching=e&&e.health>0&&distance(f,e)<=f.radius+e.radius+6;if(!touching){f.snailContactSide=null;f.snailContactTime=0}else{if(f.snailContactSide!==e.side){f.snailContactSide=e.side;f.snailContactTime=0}f.snailContactTime=(f.snailContactTime||0)+dt;if(f.snailContactTime>=.3-1e-9&&f.cd<=1e-9){this.attack(f,e,f.damage);f.cd=f.cooldown;f.attack=.22/f.scale;f.snailContactTime=0;this.effect(f,'🐌 0.3초 접촉 공격!','skill')}}}"
once(anchor,insert,'snail contact attack')

# 5) Prevent legacy generic melee from firing instantly on collision.
once("'goblin','goblin_king','psychic'].includes(f.id)",
     "'goblin','goblin_king','psychic','snail'].includes(f.id)",
     'exclude snail generic melee')

# Required invariants.
if "BATTLE <b>v3.67</b>" not in s:
    raise SystemExit('v3.67 marker missing')
if "BATTLE <b>v3.68</b>" in s:
    raise SystemExit('version unexpectedly bumped')
for marker in ["speed:28,cooldown:1","snailContactTime:0","f.snailContactTime>=.3","'psychic','snail'].includes(f.id)"]:
    if marker not in s:
        raise SystemExit('missing marker: '+marker)

p.write_text(s,encoding='utf-8')
print('v3.67 snail submarine hotfix applied')
