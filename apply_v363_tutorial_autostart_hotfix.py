from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="const KEY='neonRumble.tutorialSeen.v1';"
new="const KEY='neonRumble.tutorialSeen.v2';"
n=s.count(old)
if n!=1:
    raise SystemExit(f'expected 1 tutorial key match, got {n}')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('v3.63 tutorial autostart hotfix applied')
