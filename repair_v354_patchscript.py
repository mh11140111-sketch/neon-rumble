from pathlib import Path
p=Path('apply_v354_chapter6.py')
s=p.read_text(encoding='utf-8')
if 'import re\n' not in s:
    s=s.replace('from pathlib import Path\n','from pathlib import Path\nimport re\n',1)
old="""proj_anchor=\"s.x+=s.vx*s.speed*dt;s.y+=s.vy*s.speed*dt;\\n   if(s.x<22||s.x>698||s.y<22||s.y>698){\"
wave_block=\"\"\"s.x+=s.vx*s.speed*dt;s.y+=s.vy*s.speed*dt;
   if(s.kind==='wave'){for(const e of this.enemies(f)){if(e.health<=0||distance(s,e)>=e.radius+s.radius)continue;s.hitTargets=s.hitTargets||{};if(!s.hitTargets[e.side]){this.attackProjectile(f,e,s);s.hitTargets[e.side]=true;if(this.result!==null)break}if(e.health>0){e.x+=s.vx*s.speed*.62*dt;e.y+=s.vy*s.speed*.62*dt;this.keepInside(e)}}if(s.x<22||s.x>698||s.y<22||s.y>698)s.life=0;continue}
   if(s.x<22||s.x>698||s.y<22||s.y>698){\"\"\"
rep(proj_anchor,wave_block,'wave projectile physics')
"""
new="""wave_pattern=r\"s\\.x\\+=s\\.vx\\*s\\.speed\\*dt;s\\.y\\+=s\\.vy\\*s\\.speed\\*dt;(?P<ws>\\s*)if\\(s\\.x<22\\|\\|s\\.x>698\\|\\|s\\.y<22\\|\\|s\\.y>698\\)\\{\"
m=re.search(wave_pattern,s)
if not m: raise SystemExit('wave projectile physics regex anchor missing')
ws=m.group('ws')
wave_block=\"s.x+=s.vx*s.speed*dt;s.y+=s.vy*s.speed*dt;\"+ws+\"if(s.kind==='wave'){for(const e of this.enemies(f)){if(e.health<=0||distance(s,e)>=e.radius+s.radius)continue;s.hitTargets=s.hitTargets||{};if(!s.hitTargets[e.side]){this.attackProjectile(f,e,s);s.hitTargets[e.side]=true;if(this.result!==null)break}if(e.health>0){e.x+=s.vx*s.speed*.62*dt;e.y+=s.vy*s.speed*.62*dt;this.keepInside(e)}}if(s.x<22||s.x>698||s.y<22||s.y>698)s.life=0;continue}\"+ws+\"if(s.x<22||s.x>698||s.y<22||s.y>698){\"
s=re.sub(wave_pattern,lambda _m:wave_block,s,count=1)
"""
if old not in s:
    raise SystemExit('old wave patch block not found in patch script')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('v3.54 patch script repaired')
