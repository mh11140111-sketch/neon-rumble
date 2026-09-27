from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="{id:'casino_boss',name:'도박장 사장',icon:'🤵‍♂️',tag:'돈 투척 · 슬롯머신 소환',hp:1500,damage:30,speed:130,cooldown:2,unlock:'casinoBoss'"
new="{id:'casino_boss',name:'도박장 사장',icon:'🤵‍♂️',tag:'돈 투척 · 슬롯머신 소환',hp:800,damage:30,speed:130,cooldown:2,unlock:'casinoBoss'"
if old not in s:
    raise SystemExit('casino boss roster anchor missing')
s=s.replace(old,new,1)
s=s.replace("detail:'HP 1500 · 💵 장당 30 / 2초 · 일반 사용 최대 5장 · 15초마다 🎰 HP 50 소환 · 소환체 6초 유지'","detail:'HP 800 · 💵 장당 30 / 2초 · 일반 사용 최대 5장 · 15초마다 🎰 HP 50 소환 · 소환체 6초 유지'",1)
# Stage 3 must remain HP 1500; verify its explicit override still exists.
if "boss.hp=1500;boss.health=1500" not in s:
    raise SystemExit('CHAPTER 5 STAGE 3 HP 1500 override missing')
p.write_text(s,encoding='utf-8')
print('v3.50 casino boss sandbox HP hotfix applied')
