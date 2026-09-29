from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

method="""psychicMaintainRange(f,e,dt){
 if(!f||f.id!=='psychic'||!e||f.health<=0||e.health<=0||f.stunUntil>this.time)return;
 const dx=e.x-f.x,dy=e.y-f.y,d=Math.max(1,Math.hypot(dx,dy)),nx=dx/d,ny=dy/d;
 const target=150*f.scale,near=125*f.scale,far=180*f.scale,spd=f.speed*f.scale;
 let mx=0,my=0;
 if(d<near){mx=-nx;my=-ny}
 else if(d>far){mx=nx;my=ny}
 else{const dir=(f.side%2===0?1:-1);mx=-ny*dir;my=nx*dir}
 const margin=78*f.scale,b=this.bounds(f);
 if(f.x<Math.max(b.low,margin))mx+=.9;if(f.x>Math.min(b.high,720-margin))mx-=.9;
 if(f.y<Math.max(b.low,margin))my+=.9;if(f.y>Math.min(b.high,720-margin))my-=.9;
 const m=Math.hypot(mx,my)||1;mx/=m;my/=m;
 const step=spd*dt*.78;f.x+=mx*step;f.y+=my*step;this.keepInside(f);f.vx=mx;f.vy=my;
}
"""
anchor='psychicSkill(f,e){'
if method.split('{',1)[0] in s:
    raise SystemExit('range AI already installed')
if s.count(anchor)!=1:
    raise SystemExit(f'psychicSkill anchor count {s.count(anchor)}')
s=s.replace(anchor,method+anchor,1)
old="if(f.id==='merman')this.mermanSkill(f,e);if(f.id==='psychic')this.psychicSkill(f,e);if(f.id==='dragon')"
new="if(f.id==='merman')this.mermanSkill(f,e);if(f.id==='psychic'){this.psychicMaintainRange(f,e,dt);this.psychicSkill(f,e)}if(f.id==='dragon')"
if s.count(old)!=1:
    raise SystemExit(f'psychic call anchor count {s.count(old)}')
s=s.replace(old,new,1)
# Update current v3.66 description/detail to describe spacing AI.
s=s.replace("description:'2초마다 염력 마법탄으로 피해 20과 넉백. 5초마다 상대를 벽으로 날려 피해 50과 1초 기절. 가까운 적 투사체를 자기 주위 궤도로 끌어당겨 되돌려 이용한다.'","description:'적과 궤도 공격에 유리한 거리를 유지하며 이동한다. 2초마다 염력 마법탄으로 피해 20과 넉백. 5초마다 상대를 벽으로 날려 피해 50과 1초 기절. 가까운 적 투사체를 자기 주위 궤도로 끌어당겨 되돌려 이용한다.'")
p.write_text(s,encoding='utf-8')
print('v3.66 psychic range AI hotfix applied')
