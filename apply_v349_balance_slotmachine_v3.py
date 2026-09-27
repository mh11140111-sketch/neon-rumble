from pathlib import Path
import runpy

# Apply the complete v3.49 patch, then correct the guarded renderer separator
# before syntax validation/commit. The previous runner never committed index.html.
runpy.run_path('apply_v349_balance_slotmachine_v2.py', run_name='__main__')

p=Path('index.html')
s=p.read_text(encoding='utf-8')
bad="ctx.fillText('7',0,0)else if(s.kind==='alienlaser'){"
good="ctx.fillText('7',0,0)}else if(s.kind==='alienlaser'){"
if bad not in s:
    raise SystemExit('slot seven renderer correction anchor missing')
s=s.replace(bad,good,1)

required=[
 "if(s.kind==='slotseven')",
 "ctx.fillText('7',0,0)}else if(s.kind==='alienlaser')",
 "id:'slotmachine'",
 "price:777,type:'character'",
 "m.zombieMageDamage=85",
 "zombieMageDamage)?f.zombieMageDamage:60"
]
missing=[x for x in required if x not in s]
if missing:
    raise SystemExit('v3.49 v3 missing markers: '+repr(missing))

p.write_text(s,encoding='utf-8')
print('v3.49 syntax-safe patch applied')
