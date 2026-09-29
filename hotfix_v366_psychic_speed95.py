from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="{id:'psychic',name:'초능력자',icon:'🧘‍♂️',tag:'염력탄 · 벽 밀치기 · 투사체 궤도',hp:1000,damage:50,speed:120,cooldown:2,unlock:'psychic'"
new="{id:'psychic',name:'초능력자',icon:'🧘‍♂️',tag:'염력탄 · 벽 밀치기 · 투사체 궤도',hp:1000,damage:50,speed:95,cooldown:2,unlock:'psychic'"
if s.count(old)!=1:
    raise SystemExit(f'psychic roster anchor count={s.count(old)}')
s=s.replace(old,new,1)
# Keep this as an unannounced balance hotfix: no patch-note edits, no version change.
if 'BATTLE <b>v3.66</b>' not in s:
    raise SystemExit('version changed unexpectedly')
if "speed:95,cooldown:2,unlock:'psychic'" not in s:
    raise SystemExit('speed95 marker missing')
p.write_text(s,encoding='utf-8')
print('v3.66 psychic speed 95 hotfix applied')
