from pathlib import Path
p=Path('apply_v364_balance_casino_skins.py')
s=p.read_text(encoding='utf-8')
old="""once(\"f.dragonMysticNext=this.time+3/f.scale;\", \"f.dragonMysticNext=this.time+2.7/f.scale;\", 'dragon attack')
once(\"f.dragonMysticNext=this.time+3/f.scale\", \"f.dragonMysticNext=this.time+2.7/f.scale\", 'dragon revive')"""
new="""n=s.count(\"f.dragonMysticNext=this.time+3/f.scale\")
if n!=2:
    raise SystemExit(f'dragon runtime cooldowns: expected 2, got {n}')
s=s.replace(\"f.dragonMysticNext=this.time+3/f.scale\", \"f.dragonMysticNext=this.time+2.7/f.scale\")"""
if old not in s:
    raise SystemExit('dragon helper block not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('v3.64 helper fixed')
