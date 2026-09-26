from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

old="""  if(s.x<22||s.x>698||s.y<22||s.y>698){if(s.bounces>0){if(s.x<22||s.x>698)s.vx=-s.vx;if(s.y<22||s.y>698)s.vy=-s.vy;s.x=clamp(s.x,22,698);s.y=clamp(s.y,22,698);s.bounces--}else s.life=0}
  if(s.life>0){const knights=this.enemies(f).filter(v=>v.id==='knight'&&v.health>0);"""
new="""  if(s.x<22||s.x>698||s.y<22||s.y>698){if(s.kind==='moneybag'){const bx=clamp(s.x,22,698),by=clamp(s.y,22,698);this.moneyBagBurst(f,bx,by);s.x=bx;s.y=by;s.life=0}else if(s.bounces>0){if(s.x<22||s.x>698)s.vx=-s.vx;if(s.y<22||s.y>698)s.vy=-s.vy;s.x=clamp(s.x,22,698);s.y=clamp(s.y,22,698);s.bounces--}else s.life=0}
  if(s.life>0){const knights=this.enemies(f).filter(v=>v.id==='knight'&&v.health>0);"""

if old not in s:
    raise SystemExit('moneybag wall collision anchor not found')
if s.count(old) != 1:
    raise SystemExit(f'unexpected wall collision anchor count: {s.count(old)}')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('v3.42 submarine hotfix applied: moneybag bursts on wall impact')
