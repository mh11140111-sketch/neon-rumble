from pathlib import Path
s=Path('index.html').read_text(encoding='utf-8')
keys=['const ROSTER=[','checkEnd(){','checkEnd()','damageTarget','attackProjectile','health<=0','phoenix','egg','invuln','dodge','evasion','stepFighter(f)','update(dt)','this.fighters','isBossMode()']
for k in keys:
 print('\n###',k)
 i=s.find(k)
 print('INDEX',i)
 if i>=0: print(s[max(0,i-1800):i+5000])
