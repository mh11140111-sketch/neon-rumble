from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

old_roster="{id:'snail',name:'달팽이',icon:'🐌',tag:'초저속 · 초고화력 · 껍질 방어',hp:1000,damage:6767676767,speed:28,cooldown:1,description:'매우 느리게 가장 가까운 적을 계속 추적하며, 0.3초 이상 연속 접촉해야 근접 공격 피해 6,767,676,767을 준다. HP 30% 이하가 되면 전투당 1회 5초 동안 껍질에 숨어 받는 피해를 1/5로 줄이고 0.5초마다 HP 20을 회복한다.',detail:'HP 1000 · 이동속도 28 · 0.3초 연속 접촉 후 근접 6,767,676,767 · HP 30% 이하 1회 · 껍질 5초 · 피해 80% 감소 · 0.5초마다 HP 20 회복'},"
new_roster="{id:'snail',name:'달팽이',icon:'🐌',tag:'초저속 · 초고화력 · 껍질 방어',hp:1000,damage:6767676767,speed:28,cooldown:1,description:'매우 느리게 가장 가까운 적을 계속 추적하며, 적과 접촉하면 즉시 근접 공격 피해 6,767,676,767을 준다. HP 30% 이하가 되면 전투당 1회 5초 동안 껍질에 숨어 받는 피해를 1/5로 줄이고 0.5초마다 HP 20을 회복한다.',detail:'HP 1000 · 이동속도 28 · 접촉 즉시 근접 6,767,676,767 · HP 30% 이하 1회 · 껍질 5초 · 피해 80% 감소 · 0.5초마다 HP 20 회복'},"
once(old_roster,new_roster,'snail roster instant text')

once("psychicPushNext:type.id==='psychic'?5/scale:9999,psychicOrbitAngle:0,snailContactSide:null,snailContactTime:0,airborneUntil:0,",
     "psychicPushNext:type.id==='psychic'?5/scale:9999,psychicOrbitAngle:0,airborneUntil:0,",
     'remove snail contact state')

contact_block=" if(f.id==='snail'){const touching=e&&e.health>0&&distance(f,e)<=f.radius+e.radius+6;if(!touching){f.snailContactSide=null;f.snailContactTime=0}else{if(f.snailContactSide!==e.side){f.snailContactSide=e.side;f.snailContactTime=0}f.snailContactTime=(f.snailContactTime||0)+dt;if(f.snailContactTime>=.3-1e-9&&f.cd<=1e-9){this.attack(f,e,f.damage);f.cd=f.cooldown;f.attack=.22/f.scale;f.snailContactTime=0;this.effect(f,'🐌 0.3초 접촉 공격!','skill')}}}\n"
once(contact_block,"",'remove snail delayed contact attack')

once("'goblin','goblin_king','psychic','snail'].includes(f.id)",
     "'goblin','goblin_king','psychic'].includes(f.id)",
     'restore snail generic instant melee')

if "BATTLE <b>v3.67</b>" not in s: raise SystemExit('v3.67 marker missing')
if "speed:28,cooldown:1" not in s: raise SystemExit('snail speed changed unexpectedly')
if "접촉 즉시 근접 6,767,676,767" not in s: raise SystemExit('instant attack text missing')
if "f.snailContactTime>=.3" in s: raise SystemExit('old delayed contact logic remains')
if "'psychic','snail'].includes(f.id)" in s: raise SystemExit('snail still excluded from generic melee')

p.write_text(s,encoding='utf-8')
print('v3.67 snail instant attack hotfix applied')
