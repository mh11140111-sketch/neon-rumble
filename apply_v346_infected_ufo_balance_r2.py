from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n < count:
        raise SystemExit(f'replace mismatch expected >= {count}, found {n}: {old[:220]!r}')
    s=s.replace(old,new,count)

rep('BATTLE <b>v3.45</b>','BATTLE <b>v3.46</b>')
rep('<summary>📒 패치노트 · v3.45</summary><div class="patch-body">','<summary>📒 패치노트 · v3.46</summary><div class="patch-body"><div class="patch-version"><h3>v3.46 · 감염 UFO 밸런스</h3><ul><li>🛸👾 감염 UFO: 샌드박스·스테이지 모두 HP 1000 → 1500.</li><li>파멸의 레이저 재사용 대기시간 10초 → 8초. 샌드박스·스테이지 모두 동일 적용.</li></ul></div>')
rep("{id:'infected_ufo',name:'감염 UFO',icon:'🛸👾',tag:'파멸의 레이저',hp:1000,damage:350,speed:105,cooldown:10,unlock:'infectedUfo'","{id:'infected_ufo',name:'감염 UFO',icon:'🛸👾',tag:'파멸의 레이저',hp:1500,damage:350,speed:105,cooldown:8,unlock:'infectedUfo'")
rep("detail:'HP 1000 · 파멸의 레이저 350 / 10초 · 발사 전 1초 피격 예고 · 맵 관통'","detail:'HP 1500 · 파멸의 레이저 350 / 8초 · 발사 전 1초 피격 예고 · 맵 관통'")
rep("if(!Number.isFinite(f.doomNext))f.doomNext=this.time+10;","if(!Number.isFinite(f.doomNext))f.doomNext=this.time+8;")
rep("f.doomNext=this.time+10;this.emit('🛸👾 파멸의 레이저 발사! 피해 350')","f.doomNext=this.time+8;this.emit('🛸👾 파멸의 레이저 발사! 피해 350')")
s=s.replace("id:'infected_ufo',hp:1000", "id:'infected_ufo',hp:1500")
s=s.replace('id:"infected_ufo",hp:1000', 'id:"infected_ufo",hp:1500')
p.write_text(s,encoding='utf-8')
print('Applied v3.46 infected UFO balance patch')
