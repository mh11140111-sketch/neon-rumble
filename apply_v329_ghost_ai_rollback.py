from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s
old=" if(f.id==='ghost'&&f.health>0&&f.stunUntil<=this.time&&!f.ghostPossessing){const at=this.nearest(f);if(at){const aa=this.aim(f,at),d=distance(f,at);let x,y;if(d>150*f.scale){x=aa.x;y=aa.y}else{x=aa.x*.35-aa.y*.94;y=aa.y*.35+aa.x*.94}const n=Math.hypot(x,y)||1;f.vx=x/n;f.vy=y/n;f.turn=.18}}\n"
if old not in s:
    raise SystemExit('ghost custom AI block not found')
s=s.replace(old,'',1)
# Keep contact damage 15 and possession rules untouched.
assert "this.attack(g,e,15*g.scale)" in s
assert "ghost.ghostPossessing=true" in s
assert "BATTLE <b>v3.29</b>" in s
if s==orig:
    raise SystemExit('no changes')
p.write_text(s,encoding='utf-8')
print('V329_GHOST_AI_ROLLBACK_APPLIED')
