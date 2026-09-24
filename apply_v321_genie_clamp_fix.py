from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="const phase=clamp(engine.time-f.genieArmStart,0,1),ga=phase*Math.PI*6"
new="const phase=Math.max(0,Math.min(1,engine.time-f.genieArmStart)),ga=phase*Math.PI*6"
if old not in s:
    raise SystemExit('PATCH FAILED: genie draw clamp expression not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('Fixed Genie draw clamp scope crash')
