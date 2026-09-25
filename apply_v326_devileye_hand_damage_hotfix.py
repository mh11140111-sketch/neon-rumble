from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old1="damage:25*hs,armor:0"
new1="damage:(persistent?50:25)*hs,armor:0"
old2="kind:'curseorb',radius:8*h.scale,speed:230*h.scale,damage:25*h.scale,life:4"
new2="kind:'curseorb',radius:8*h.scale,speed:230*h.scale,damage:h.damage,life:4"
if old1 not in s:
    raise SystemExit('cursed hand damage property pattern not found')
if old2 not in s:
    raise SystemExit('cursed hand projectile damage pattern not found')
s=s.replace(old1,new1,1)
s=s.replace(old2,new2,1)
p.write_text(s,encoding='utf-8')
print('Devil Eye persistent hand damage rollback applied')
