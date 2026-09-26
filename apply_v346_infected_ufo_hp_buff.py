from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n < count:
        raise SystemExit(f'replace mismatch expected >= {count}, found {n}: {old[:220]!r}')
    s=s.replace(old,new,count)

# Version + patch notes
rep('BATTLE <b>v3.45</b>','BATTLE <b>v3.46</b>')
rep('<summary>📒 패치노트 · v3.45</summary><div class="patch-body">',
    '<summary>📒 패치노트 · v3.46</summary><div class="patch-body"><div class="patch-version"><h3>v3.46 · 감염 UFO 체력 상향</h3><ul><li>🛸👾 감염 UFO 체력 +500.</li><li>샌드박스 HP 1000 → 1500.</li><li>CHAPTER 4 STAGE 3 HP 1000 → 1500.</li></ul></div>')

# Sandbox roster HP
rep("{id:'infected_ufo',name:'감염 UFO',icon:'🛸👾',tag:'파멸의 레이저',hp:1000,damage:350,speed:105,cooldown:10,unlock:'infectedUfo',description:'10초마다 아주 두꺼운 파멸의 레이저를 예고 후 발사해. 레이저는 맵 끝까지 관통하고 피해 350을 줘.',detail:'HP 1000 · 파멸의 레이저 350 / 10초 · 발사 전 1초 피격 예고 · 맵 관통'},",
    "{id:'infected_ufo',name:'감염 UFO',icon:'🛸👾',tag:'파멸의 레이저',hp:1500,damage:350,speed:105,cooldown:10,unlock:'infectedUfo',description:'10초마다 아주 두꺼운 파멸의 레이저를 예고 후 발사해. 레이저는 맵 끝까지 관통하고 피해 350을 줘.',detail:'HP 1500 · 파멸의 레이저 350 / 10초 · 발사 전 1초 피격 예고 · 맵 관통'},")

# Chapter 4 Stage 3 boss HP
rep("const boss=engine.fighters[1];boss.hp=1000;boss.health=1000;boss.doomNext=10",
    "const boss=engine.fighters[1];boss.hp=1500;boss.health=1500;boss.doomNext=10")

p.write_text(s,encoding='utf-8')
print('v3.46 infected UFO HP buff applied')
