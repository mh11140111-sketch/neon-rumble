from pathlib import Path
s=Path('index.html').read_text(encoding='utf-8')
keys=['dragonRainDrop(f){','stepFighter(f,e,dt){','attackProjectile(f,e,s)','slowPower','rootSlowPower','if(s.kind===\'wave\')','for(const s of engine.shots)','id:\'dragon\'']
for k in keys:
 print('\n###',k)
 i=s.find(k)
 print('INDEX',i)
 if i>=0: print(s[max(0,i-2200):i+6500])
