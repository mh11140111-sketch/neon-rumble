from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n < count:
        raise SystemExit(f'replace mismatch expected >= {count}, found {n}: {old[:240]!r}')
    s=s.replace(old,new,count)

# Keep version v3.46, extend the existing v3.46 patch note.
rep('<div class="patch-version"><h3>v3.46 · 감염 UFO 체력 상향</h3><ul><li>🛸👾 감염 UFO 체력 +500.</li><li>샌드박스 HP 1000 → 1500.</li><li>CHAPTER 4 STAGE 3 HP 1000 → 1500.</li></ul></div>',
    '<div class="patch-version"><h3>v3.46 · 감염 UFO 밸런스</h3><ul><li>🛸👾 감염 UFO 체력 +500.</li><li>샌드박스 HP 1000 → 1500.</li><li>CHAPTER 4 STAGE 3 HP 1000 → 1500.</li><li>파멸의 레이저 공격 주기 10초 → 8초. 샌드박스·스테이지 모두 동일 적용.</li></ul></div>')

# Character data shown in sandbox / unlock roster.
rep("{id:'infected_ufo',name:'감염 UFO',icon:'🛸👾',tag:'파멸의 레이저',hp:1500,damage:350,speed:105,cooldown:10,unlock:'infectedUfo',description:'10초마다 아주 두꺼운 파멸의 레이저를 예고 후 발사해. 레이저는 맵 끝까지 관통하고 피해 350을 줘.',detail:'HP 1500 · 파멸의 레이저 350 / 10초 · 발사 전 1초 피격 예고 · 맵 관통'},",
    "{id:'infected_ufo',name:'감염 UFO',icon:'🛸👾',tag:'파멸의 레이저',hp:1500,damage:350,speed:105,cooldown:8,unlock:'infectedUfo',description:'8초마다 아주 두꺼운 파멸의 레이저를 예고 후 발사해. 레이저는 맵 끝까지 관통하고 피해 350을 줘.',detail:'HP 1500 · 파멸의 레이저 350 / 8초 · 발사 전 1초 피격 예고 · 맵 관통'},")

# Runtime timing used by both sandbox and Chapter 4 stage battles.
rep("if(!Number.isFinite(f.doomNext))f.doomNext=this.time+10;","if(!Number.isFinite(f.doomNext))f.doomNext=this.time+8;")
rep("f.doomNext=this.time+10;this.emit('🛸👾 파멸의 레이저 발사! 피해 350')","f.doomNext=this.time+8;this.emit('🛸👾 파멸의 레이저 발사! 피해 350')")

p.write_text(s,encoding='utf-8')
print('Applied v3.46 infected UFO attack-speed patch r3')
