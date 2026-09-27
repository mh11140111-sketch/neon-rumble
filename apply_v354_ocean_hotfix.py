from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s

# 1) Merman wave push: very strong knockback while wave overlaps target.
old="e.x+=s.vx*s.speed*.62*dt;e.y+=s.vy*s.speed*.62*dt;this.keepInside(e)"
new="e.x+=s.vx*s.speed*3.0*dt;e.y+=s.vy*s.speed*3.0*dt;this.keepInside(e)"
if old not in s:
    raise SystemExit('merman wave push anchor missing')
s=s.replace(old,new,1)

# 2) Shark can bite normally even when not dashing. Dash hit still applies bleed.
old2="if(f.id==='shark'&&f.health>0&&f.stunUntil<=this.time&&f.dash>0&&!f.sharkDashHit){const dealt=this.attack(f,e,50*f.scale);if(dealt>0){f.sharkDashHit=true;f.dash=0;if(e.health>0)this.applyBleed(f,e)}continue}"
new2="if(f.id==='shark'&&f.health>0&&f.stunUntil<=this.time){if(f.dash>0&&!f.sharkDashHit){const dealt=this.attack(f,e,50*f.scale);if(dealt>0){f.sharkDashHit=true;f.dash=0;if(e.health>0)this.applyBleed(f,e)}continue}else if(f.dash<=0&&f.cd<=1e-9){this.attack(f,e,50*f.scale);f.cd=1/f.scale;this.effect(f,'🦈 물기 50','skill');continue}}"
if old2 not in s:
    raise SystemExit('shark contact anchor missing')
s=s.replace(old2,new2,1)

# Keep v3.54 visible version unchanged; add hidden/internal patch note only as code comment.
marker="/* Add characters to ROSTER and their behavior to stepFighter. No UI changes required. */"
if marker in s and 'v3.54 submarine ocean hotfix' not in s:
    s=s.replace(marker,marker+"\n/* v3.54 submarine ocean hotfix: stronger merman wave push + shark normal bite */",1)

if s==orig:
    raise SystemExit('no changes made')
p.write_text(s,encoding='utf-8')
print('v3.54 ocean submarine hotfix applied')
