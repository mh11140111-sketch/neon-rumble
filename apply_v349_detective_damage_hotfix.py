from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="""}else if(r<.20){
    e.stunUntil=Math.max(e.stunUntil||0,this.time+3/f.scale);
    this.effect(e,'🚔 기절 3초!','skill');"""
new="""}else if(r<.20){
    e.health=Math.max(0,e.health-100*f.scale);
    e.stunUntil=Math.max(e.stunUntil||0,this.time+3/f.scale);
    this.effect(e,'🚔 기절 3초 + 피해 100!','skill');"""
if old not in s:
    raise SystemExit('detective 15% hotfix anchor missing')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('v3.49 detective 15% damage hotfix applied')
