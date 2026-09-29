from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Submarine balance patch: keep displayed version and patch-note history unchanged.
if 'BATTLE <b>v3.66</b>' not in s:
    raise SystemExit('v3.66 marker missing')

# Roster stats + visible current character description/detail only.
old="{id:'psychic',name:'초능력자',icon:'🧘‍♂️',tag:'염력탄 · 벽 밀치기 · 투사체 궤도',hp:1000,damage:20,speed:150,cooldown:2,unlock:'psychic',description:'적과 궤도 공격에 유리한 거리를 유지하며 이동한다. 2초마다 염력 마법탄으로 피해 20과 넉백. 5초마다 상대를 벽으로 날려 피해 50과 1초 기절. 가까운 적 투사체를 자기 주위 궤도로 끌어당겨 되돌려 이용한다.',detail:'HP 1000 · 염력탄 20 / 2초 + 넉백 · 벽 밀치기 50 / 5초 + 기절 1초 · 적 투사체 궤도 포획 · 궤도탄 벽 접촉 시 자신이 원래 피해 · CH8 STAGE 3 10% 획득'}"
new="{id:'psychic',name:'초능력자',icon:'🧘‍♂️',tag:'염력탄 · 벽 밀치기 · 투사체 궤도',hp:1000,damage:50,speed:120,cooldown:2,unlock:'psychic',description:'적과 궤도 공격에 유리한 거리를 유지하며 이동한다. 2초마다 염력 마법탄으로 피해 50과 넉백. 5초마다 상대를 벽으로 날려 피해 80과 1초 기절. 가까운 적 투사체를 자기 주위 궤도로 끌어당겨 되돌려 이용한다.',detail:'HP 1000 · 염력탄 50 / 2초 + 넉백 · 벽 밀치기 80 / 5초 + 기절 1초 · 적 투사체 궤도 포획 · 궤도탄 벽 접촉 시 자신이 원래 피해 · CH8 STAGE 3 10% 획득'}"
if s.count(old)!=1:
    raise SystemExit(f'psychic roster anchor mismatch: {s.count(old)}')
s=s.replace(old,new,1)

# Scope runtime changes strictly to psychicSkill.
start=s.find('psychicSkill(f,e){')
end=s.find('psychicCaptureShots(){',start)
if start<0 or end<0:
    raise SystemExit('psychicSkill block not found')
block=s[start:end]

pairs=[
    ('const dealt=this.attack(f,e,50*f.scale);','const dealt=this.attack(f,e,80*f.scale);'),
    ("this.effect(e,'🧘‍♂️ 벽 밀치기 50 · 기절!','skill')","this.effect(e,'🧘‍♂️ 벽 밀치기 80 · 기절!','skill')"),
    ("kind:'psychic_bolt',icon:'🟣',radius:9*f.scale,speed:330*f.scale,damage:20*f.scale","kind:'psychic_bolt',icon:'🟣',radius:9*f.scale,speed:330*f.scale,damage:50*f.scale"),
]
for old2,new2 in pairs:
    if block.count(old2)!=1:
        raise SystemExit(f'psychic runtime anchor mismatch for {old2!r}: {block.count(old2)}')
    block=block.replace(old2,new2,1)
s=s[:start]+block+s[end:]

# Do not edit patch notes: historical v3.66 release note remains as released.
checks=[
    "speed:120,cooldown:2,unlock:'psychic'",
    '염력탄 50 / 2초 + 넉백',
    '벽 밀치기 80 / 5초 + 기절 1초',
    'const dealt=this.attack(f,e,80*f.scale);',
    "damage:50*f.scale,life:4/f.scale",
]
missing=[x for x in checks if x not in s]
if missing:
    raise SystemExit('missing hotfix markers: '+repr(missing))

p.write_text(s,encoding='utf-8')
print('v3.66 psychic stealth balance hotfix applied')
