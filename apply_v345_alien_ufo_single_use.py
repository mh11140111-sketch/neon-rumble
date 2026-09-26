from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n < count:
        raise SystemExit(f'replace mismatch expected >= {count}, found {n}: {old[:220]!r}')
    s=s.replace(old,new,count)

# visible version + patch note
rep('BATTLE <b>v3.44</b>','BATTLE <b>v3.45</b>')
rep('<summary>📒 패치노트 · v3.44</summary><div class="patch-body">',
    '<summary>📒 패치노트 · v3.45</summary><div class="patch-body"><div class="patch-version"><h3>v3.45 · 외계인 UFO 일회용 변경</h3><ul><li>👽 외계인의 🛸 UFO 탑승은 전투당 1회만 가능하도록 변경.</li><li>UFO가 파괴되면 해당 전투에서는 다시 탑승하지 않음. UFO HP 300, 랜덤 적 5초간 🐄 소 변환, 탑승 중 일반 공격은 기존과 동일.</li></ul></div>')

# UFO destroyed: do not schedule another mount
rep("if(e.ufoHp<=0){e.ufoMounted=false;e.ufoHp=0;e.icon='👽';e.ufoNext=this.time+10;this.effect(e,'🛸 UFO 파괴!','skill');this.emit('🛸 UFO가 파괴되어 외계인이 탈출!')}return n}",
    "if(e.ufoHp<=0){e.ufoMounted=false;e.ufoHp=0;e.ufoUsed=true;e.ufoNext=Infinity;e.icon='👽';this.effect(e,'🛸 UFO 파괴!','skill');this.emit('🛸 UFO가 파괴됐어. 이번 전투에서는 다시 탑승하지 않아!')}return n}")

# UFO mount: only once per battle
rep("updateAlienUfo(f){if(f.id!=='alien'||f.health<=0)return;if(!Number.isFinite(f.ufoNext))f.ufoNext=this.time+10;if(!f.ufoMounted&&this.time>=f.ufoNext-1e-9){f.ufoMounted=true;f.ufoHp=300;f.icon='🛸';",
    "updateAlienUfo(f){if(f.id!=='alien'||f.health<=0)return;if(f.ufoUsed)return;if(!Number.isFinite(f.ufoNext))f.ufoNext=this.time+10;if(!f.ufoMounted&&this.time>=f.ufoNext-1e-9){f.ufoUsed=true;f.ufoMounted=true;f.ufoHp=300;f.icon='🛸';")

# wording in existing v3.44 note to avoid implying remount after destruction
rep('UFO HP가 0이 되면 외계인으로 복귀하고 10초 뒤 다시 탑승.',
    'UFO HP가 0이 되면 외계인으로 복귀하며, v3.45부터 해당 전투에서는 다시 탑승하지 않음.')

p.write_text(s,encoding='utf-8')
print('Applied v3.45 Alien UFO single-use patch')
