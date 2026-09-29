from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="{id:'psychic',name:'초능력자',icon:'🧘‍♂️',tag:'염력탄 · 벽 밀치기 · 투사체 궤도',hp:550,damage:30,speed:95,cooldown:2,unlock:'psychic',description:'적과 궤도 공격에 유리한 거리를 유지하며 이동하고 가끔 벽 근처까지 붙는다. 2초마다 염력 마법탄으로 피해 30과 넉백. 5초마다 상대를 벽으로 날려 피해 60과 1초 기절. 가까운 적 투사체를 자기 주위 궤도로 끌어당겨 되돌려 이용한다.',detail:'HP 550 · 염력탄 30 / 2초 + 넉백 · 벽 밀치기 60 / 5초 + 기절 1초 · 적 투사체 궤도 포획 · 궤도탄 벽 접촉 시 자신이 원래 피해 · CH8 STAGE 3 10% 획득'},"
new="{id:'psychic',name:'초능력자',icon:'🧘‍♂️',tag:'염력탄 · 벽 밀치기 · 투사체 궤도',hp:750,damage:30,speed:95,cooldown:2,unlock:'psychic',description:'적과 궤도 공격에 유리한 거리를 유지하며 이동하고 가끔 벽 근처까지 붙는다. 2초마다 염력 마법탄으로 피해 30과 넉백. 5초마다 상대를 벽으로 날려 피해 60과 1초 기절. 가까운 적 투사체를 자기 주위 궤도로 끌어당겨 되돌려 이용한다.',detail:'HP 750 · 염력탄 30 / 2초 + 넉백 · 벽 밀치기 60 / 5초 + 기절 1초 · 적 투사체 궤도 포획 · 궤도탄 벽 접촉 시 자신이 원래 피해 · CH8 STAGE 3 10% 획득'},"
if s.count(old)!=1: raise SystemExit(f'psychic roster expected 1 match, got {s.count(old)}')
s=s.replace(old,new,1)
if "BATTLE <b>v3.67</b>" not in s: raise SystemExit('v3.67 marker missing')
if "hp:750,damage:30,speed:95" not in s: raise SystemExit('hp750 marker missing')
p.write_text(s,encoding='utf-8')
print('v3.67 psychic HP 750 hotfix applied')