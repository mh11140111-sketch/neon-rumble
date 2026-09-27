from pathlib import Path
s=Path('index.html').read_text(encoding='utf-8')
for k in ["for(const s of this.shots){","s.kind==='moneybag'","s.icon","fillText(s","shots){ctx","this.shots.forEach","kind==='rain'","attackProjectile(f,e,s)"]:
 print('\n###',k)
 i=s.find(k)
 print('INDEX',i)
 if i>=0: print(s[max(0,i-2400):i+7000])
