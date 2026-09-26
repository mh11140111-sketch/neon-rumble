from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n < count:
        raise SystemExit(f'replace mismatch expected >= {count}, found {n}: {old[:200]!r}')
    s=s.replace(old,new,count)

# Version + patch notes
rep('BATTLE <b>v3.45</b>','BATTLE <b>v3.46</b>')
rep('<summary>📒 패치노트 · v3.45</summary><div class="patch-body">',
    '<summary>📒 패치노트 · v3.46</summary><div class="patch-body"><div class="patch-version"><h3>v3.46 · 감염 UFO 밸런스</h3><ul><li>🛸👾 감염 UFO 체력은 샌드박스와 CHAPTER 4 STAGE 3 모두 1500으로 통일.</li><li>파멸의 레이저 발사 주기 10초 → 8초. 샌드박스와 스테이지 모두 동일 적용.</li></ul></div>')

# Sandbox roster: keep HP 1500 and reduce attack interval 10 -> 8.
rep("{id:'infected_ufo',name:'감염 UFO',icon:'🛸👾',tag:'파멸의 레이저',hp:1500,damage:350,speed:105,cooldown:10,unlock:'infectedUfo',description:'10초마다 아주 두꺼운 파멸의 레이저를 예고 후 발사해. 레이저는 맵 끝까지 관통하고 피해 350을 줘.',detail:'HP 1500 · 파멸의 레이저 350 / 10초 · 발사 전 1초 피격 예고 · 맵 관통'},",
    "{id:'infected_ufo',name:'감염 UFO',icon:'🛸👾',tag:'파멸의 레이저',hp:1500,damage:350,speed:105,cooldown:8,unlock:'infectedUfo',description:'8초마다 아주 두꺼운 파멸의 레이저를 예고 후 발사해. 레이저는 맵 끝까지 관통하고 피해 350을 줘.',detail:'HP 1500 · 파멸의 레이저 350 / 8초 · 발사 전 1초 피격 예고 · 맵 관통'},")

# Combat logic: doom laser every 8 seconds.
rep("if(!Number.isFinite(f.doomNext))f.doomNext=this.time+10", "if(!Number.isFinite(f.doomNext))f.doomNext=this.time+8")
rep("f.doomNext=this.time+10;this.emit('🛸👾 파멸의 레이저 발사! 피해 350')", "f.doomNext=this.time+8;this.emit('🛸👾 파멸의 레이저 발사! 피해 350')")

# Chapter 4 stage 3 initial timer + UI text.
rep("boss.hp=1500;boss.health=1500;boss.doomNext=10", "boss.hp=1500;boss.health=1500;boss.doomNext=8")
rep("CHAPTER 4 STAGE 3 · 감염 UFO가 10초마다 1초 피격 예고 후 두꺼운 파멸의 레이저를 발사. 피해 350 · 맵 관통.",
    "CHAPTER 4 STAGE 3 · 감염 UFO가 8초마다 1초 피격 예고 후 두꺼운 파멸의 레이저를 발사. 피해 350 · 맵 관통.")

# HUD countdown default.
rep("if(f.id==='infected_ufo')return '🛸👾 파멸 레이저 '+Math.max(0,(f.doomNext||10)-engine.time).toFixed(1)+'초 · 피해 350'",
    "if(f.id==='infected_ufo')return '🛸👾 파멸 레이저 '+Math.max(0,(f.doomNext||8)-engine.time).toFixed(1)+'초 · 피해 350'")

p.write_text(s,encoding='utf-8')
print('Applied v3.46 infected UFO balance patch')
