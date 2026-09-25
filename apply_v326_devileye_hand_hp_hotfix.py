from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="if(!owner)return null;const hs=owner.boss?1.5:1,hp=66*hs,side=this.fighters.length"
new="if(!owner)return null;const hs=owner.boss?1.5:1,hp=(persistent?113:66)*hs,side=this.fighters.length"
if old not in s:
    raise SystemExit('spawnCursedHand HP pattern not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Devil Eye persistent hand HP rollback applied')
