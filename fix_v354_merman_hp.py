from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="{id:'merman',name:'인어',icon:'🧜‍♂️',tag:'파도 · 밀치기',hp:1000,damage:100,speed:145,cooldown:3,unlock:'merman'"
new="{id:'merman',name:'인어',icon:'🧜‍♂️',tag:'파도 · 밀치기',hp:1200,damage:100,speed:145,cooldown:3,unlock:'merman'"
if old not in s: raise SystemExit('merman roster hp anchor missing')
s=s.replace(old,new,1)
s=s.replace("detail:'HP 1000 · 🌊 피해 100 / 3초 · 파도 접촉 중 밀치기'","detail:'HP 1200 · 🌊 피해 100 / 3초 · 파도 접촉 중 밀치기'",1)
s=s.replace("b.hp=1000;b.health=1000;b.mermanWaveNext=3","b.hp=1200;b.health=1200;b.mermanWaveNext=3",1)
s=s.replace("STAGE 3 · 인어 HP 1000","STAGE 3 · 인어 HP 1200",1)
if "id:'merman'" not in s or "hp:1200" not in s: raise SystemExit('verification failed')
p.write_text(s,encoding='utf-8')
print('v3.54 merman HP fixed to 1200')
