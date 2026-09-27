from pathlib import Path
s=Path('index.html').read_text(encoding='utf-8')
for k in ['stepFighter(f,e,dt){','slowPower','rootSlowPower','attackProjectile(f,e,s)','dragonMirageActive(f){','dragonRainDrop(f){',"id:'dragon'",'mermanWaveNext:type.id']:
 print('\n###',k)
 i=s.find(k)
 print('INDEX',i)
 if i>=0: print(s[max(0,i-1800):i+6500])
