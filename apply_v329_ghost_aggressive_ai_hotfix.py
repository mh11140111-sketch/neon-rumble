from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s
old="""if(f.id==='aladdin'&&f.health>0&&f.stunUntil<=this.time){const at=this.nearest(f);if(at){const aa=this.aim(f,at),d=distance(f,at),cx=360-f.x,cy=360-f.y,edge=f.x<105||f.x>615||f.y<105||f.y>615;let x,y;if(edge){const n=Math.hypot(cx,cy)||1;x=cx/n;y=cy/n}else if(d<330*f.scale){x=-aa.x-aa.y*.35;y=-aa.y+aa.x*.35}else{x=-aa.y;y=aa.x}const n=Math.hypot(x,y)||1;f.vx=x/n;f.vy=y/n;f.turn=.35}}"""
new=old+"""\n if(f.id==='ghost'&&f.health>0&&f.stunUntil<=this.time&&!f.ghostPossessing){const at=this.nearest(f);if(at){const aa=this.aim(f,at);f.vx=aa.x;f.vy=aa.y;f.turn=.12}}"""
if old not in s: raise SystemExit('ghost AI hook anchor missing')
s=s.replace(old,new,1)
if s==orig: raise SystemExit('no changes')
p.write_text(s,encoding='utf-8')
print('V329_GHOST_AGGRESSIVE_AI_OK')
