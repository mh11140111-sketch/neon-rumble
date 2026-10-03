from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1 got {n}')
    s=s.replace(old,new,1)

once(
"const ids=['skeleton_gun','skeleton_sword','skeleton_drunk','skeleton_mage'],id=ids[Math.floor(this.random()*ids.length)]",
"const ids=['skeleton_gun','skeleton_sword','skeleton_drunk'],id=ids[Math.floor(this.random()*ids.length)]",
'skele44 summon pool')

once(
"description:'1초마다 피해 50의 감염 투사체를 던진다. 적중 시 30% 확률로 랜덤 해골을 소환하고, 직접 처치한 적은 죽기 직전 체력의 2배 HP를 가진 랜덤 해골로 바꾼다.',detail:'HP 1000 · 🧫 투사체 50 / 1초 · 명중 시 해골 소환 30% · 처치 시 죽기 직전 HP×2 랜덤 해골 변환 · NEW-CH2 STAGE 3 10% 획득'",
"description:'1초마다 피해 50의 감염 투사체를 던진다. 적중 시 30% 확률로 총잡이·칼잡이·취한 해골 중 하나를 소환하고, 직접 처치한 적도 죽기 직전 체력의 2배 HP를 가진 세 종류 해골 중 하나로 바꾼다.',detail:'HP 1000 · 🧫 투사체 50 / 1초 · 명중 시 30%로 🔫/🗡️/🍺 해골 소환 · 처치 시 죽기 직전 HP×2로 🔫/🗡️/🍺 해골 변환 · 법사해골 소환 없음 · NEW-CH2 STAGE 3 10% 획득'",
'skele44 text')

once(
"NEW-CHAPTER 2 STAGE 3 · 스켈-44 HP 1000 · 투사체 50/1초 · 적중 시 30% 랜덤 해골 소환 · 직접 처치한 적을 죽기 직전 HP×2 해골로 변환 · 클리어 시 10% 획득.",
"NEW-CHAPTER 2 STAGE 3 · 스켈-44 HP 1000 · 투사체 50/1초 · 적중 시 30%로 총잡이/칼잡이/취한 해골 중 하나 소환 · 직접 처치한 적도 죽기 직전 HP×2로 세 종류 해골 중 하나로 변환 · 법사해골 소환 없음 · 클리어 시 10% 획득.",
'stage3 battle info')

once(
"🧫 50 / 1초 · 적중 시 30% 랜덤 해골 소환 · 처치한 적을 죽기 직전 HP×2 랜덤 해골로 변환 · 클리어 시 10% 획득",
"🧫 50 / 1초 · 적중 시 30%로 🔫/🗡️/🍺 해골만 소환 · 처치 시 죽기 직전 HP×2로 세 종류 중 하나로 변환 · 법사해골 제외 · 클리어 시 10% 획득",
'stage3 card')

p.write_text(s,encoding='utf-8')
print('skele44 summon pool restricted to gun/sword/drunk skeletons')
