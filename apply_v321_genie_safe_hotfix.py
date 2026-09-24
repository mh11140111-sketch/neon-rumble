from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

old="""genieSkill(g,dt){
 if(g.id!=='genie')return;if(!Number.isFinite(g.hp))g.hp=1500*(g.boss?2.5:1);if(!Number.isFinite(g.health))g.health=g.hp;if(g.health<=0)return;
 const owner=this.fighters[g.ownerSide];if(!owner||owner.health<=0){g.health=0;return}
 if(g.genieArmUntil===undefined){g.genieArmStart=-1;g.genieArmUntil=-1;g.genieArmHits={}}
 g.cd=Math.max(0,g.cd-dt);
 if(g.stunUntil<=this.time){const target=this.nearest(g);if(target){const a=this.aim(g,target);g.vx=a.x;g.vy=a.y;g.x+=g.vx*g.speed*dt;g.y+=g.vy*g.speed*dt;this.keepInside(g)}}
 if(g.cd<=1e-9&&this.time>=g.genieArmUntil-1e-9){g.cd=3/g.scale;g.genieArmStart=this.time;g.genieArmUntil=this.time+1;g.genieArmHits={};g.attack=1;this.effect(g,'🧞‍♂️ 회전팔!','skill');this.emit('🧞‍♂️ 지니가 회전팔 공격!')}
 if(this.time<g.genieArmUntil-1e-9){const phase=clamp((this.time-g.genieArmStart),0,1),a=phase*Math.PI*2*3,len=145*g.scale,dx=Math.cos(a),dy=Math.sin(a);for(const e of this.enemies(g)){if(e.health<=0||g.genieArmHits[e.side])continue;const rx=e.x-g.x,ry=e.y-g.y,along=rx*dx+ry*dy,perp=Math.abs(rx*dy-ry*dx);if(along>=0&&along<=len+e.radius&&perp<=e.radius+24*g.scale){const dealt=this.attack(g,e,g.damage);if(dealt>0)g.genieArmHits[e.side]=true;if(this.result!==null)return}}}
}"""
new="""genieSkill(g,dt){
 if(g.id!=='genie')return;
 if(!Number.isFinite(g.hp))g.hp=1500*(g.boss?2.5:1);
 if(!Number.isFinite(g.health))g.health=g.hp;
 if(g.health<=0)return;
 const owner=this.fighters[g.ownerSide];
 if(!owner||owner.health<=0){g.health=0;return}
 if(!Number.isFinite(g.genieArmStart))g.genieArmStart=-1;
 if(!Number.isFinite(g.genieArmUntil))g.genieArmUntil=-1;
 if(!g.genieArmHits||typeof g.genieArmHits!=='object')g.genieArmHits={};
 g.cd=Math.max(0,Number.isFinite(g.cd)?g.cd-dt:3/g.scale);
 if(g.stunUntil<=this.time){const target=this.nearest(g);if(target){const mv=this.aim(g,target);g.vx=mv.x;g.vy=mv.y;g.x+=mv.x*g.speed*dt;g.y+=mv.y*g.speed*dt;this.keepInside(g)}}
 if(g.cd<=1e-9&&this.time>=g.genieArmUntil-1e-9){g.cd=3/g.scale;g.genieArmStart=this.time;g.genieArmUntil=this.time+1;g.genieArmHits={};g.attack=1;this.effect(g,'🧞‍♂️ 회전팔!','skill');this.emit('🧞‍♂️ 지니가 회전팔 공격!')}
 if(this.time>=g.genieArmUntil-1e-9)return;
 const phase=clamp(this.time-g.genieArmStart,0,1),ang=phase*Math.PI*6,ux=Math.cos(ang),uy=Math.sin(ang),inner=g.radius*.65,outer=inner+125*g.scale;
 const ax=g.x+ux*inner,ay=g.y+uy*inner,bx=g.x+ux*outer,by=g.y+uy*outer,abx=bx-ax,aby=by-ay,ab2=abx*abx+aby*aby;
 for(const e of this.enemies(g)){
  if(e.health<=0||g.genieArmHits[e.side])continue;
  const t=ab2?clamp(((e.x-ax)*abx+(e.y-ay)*aby)/ab2,0,1):0,px=ax+abx*t,py=ay+aby*t;
  if(Math.hypot(e.x-px,e.y-py)<=e.radius+22*g.scale){g.genieArmHits[e.side]=true;this.attack(g,e,g.damage);if(this.result!==null)return}
 }
}"""
if old not in s: raise SystemExit('PATCH FAILED: genieSkill current block not found')
s=s.replace(old,new,1)

start="if(f.id==='genie'&&f.health>0&&f.genieArmUntil>engine.time){"
pos=s.find(start)
if pos<0: raise SystemExit('PATCH FAILED: genie draw start not found')
end_marker="circle(f.x,f.y,r,f.flash>0?'#ffffff':c);circle(f.x,f.y,r-4,'#152338');"
end=s.find(end_marker,pos)
if end<0: raise SystemExit('PATCH FAILED: genie draw end not found')
old_draw=s[pos:end]
new_draw="""if(f.id==='genie'&&f.health>0&&f.genieArmUntil>engine.time){const phase=clamp(engine.time-f.genieArmStart,0,1),ga=phase*Math.PI*6,gs=f.scale,ux=Math.cos(ga),uy=Math.sin(ga),inner=f.radius*.65,outer=inner+125*gs,x1=f.x+ux*inner,y1=f.y+uy*inner,x2=f.x+ux*outer,y2=f.y+uy*outer;ctx.save();ctx.globalAlpha=.96;ctx.lineCap='round';ctx.strokeStyle='#258eff';ctx.lineWidth=34*gs;ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();ctx.strokeStyle='#f0b51f';ctx.lineWidth=11*gs;const cuffX=f.x+ux*(inner+12*gs),cuffY=f.y+uy*(inner+12*gs);ctx.beginPath();ctx.arc(cuffX,cuffY,20*gs,0,Math.PI*2);ctx.stroke();ctx.fillStyle='#258eff';ctx.beginPath();ctx.arc(x2,y2,24*gs,0,Math.PI*2);ctx.fill();ctx.restore();ctx.globalAlpha=f.id==='invisible'?.38:1;}"""
s=s[:pos]+new_draw+s[end:]

p.write_text(s,encoding='utf-8')
print('v3.21 safe genie arm hotfix applied')
