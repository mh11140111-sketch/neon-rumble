from pathlib import Path
s=Path('index.html').read_text(encoding='utf-8')
keys=['attack(f,e,dmg','formEgg(f){','step(dt){','tick(dt){','update(){','advance(dt','for(const f of this.fighters)','draw(ctx)','render(ctx)','isStudying(e)','if(e.health<=0){if(this.formEgg(e))continue']
for k in keys:
 print('\n###',k)
 i=s.find(k)
 print('INDEX',i)
 if i>=0: print(s[max(0,i-2500):i+7000])
