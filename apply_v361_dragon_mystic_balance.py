from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

once('<span class="badge">BATTLE <b>v3.60</b></span>','<span class="badge">BATTLE <b>v3.61</b></span>','badge')
once('<details class="patch-notes"><summary>📒 패치노트 · v3.60</summary><div class="patch-body">','<details class="patch-notes"><summary>📒 패치노트 · v3.61</summary><div class="patch-body"><div class="patch-version"><h3>v3.61 · 용 밸런스</h3><ul><li>🐉 여의주의 신통력 공격 주기 2초 → 3초.</li><li>바람·번개·물방울·나뭇잎의 확률·피해·부가효과와 비의 분노·신기루·여의주 부활은 그대로 유지.</li></ul></div>','patch notes')
once("description:'2초마다 여의주의 신통력으로 바람·번개·물방울·나뭇잎 중 하나를 25% 확률로 발사한다.","description:'3초마다 여의주의 신통력으로 바람·번개·물방울·나뭇잎 중 하나를 25% 확률로 발사한다.",'dragon description')
once("detail:'HP 1000 · 신통력 70 / 2초 · 💨","detail:'HP 1000 · 신통력 70 / 3초 · 💨",'dragon detail')
once("dragonMysticNext:type.id==='dragon'?2/scale:9999","dragonMysticNext:type.id==='dragon'?3/scale:9999",'dragon init cooldown')
once('f.dragonMysticNext=this.time+2/f.scale;','f.dragonMysticNext=this.time+3/f.scale;','dragon attack cooldown')
once('f.dragonMysticNext=this.time+2/f.scale;f.dragonMirageUntil=0;','f.dragonMysticNext=this.time+3/f.scale;f.dragonMirageUntil=0;','dragon revive cooldown')

p.write_text(s,encoding='utf-8')
print('v3.61 dragon mystic balance applied')
