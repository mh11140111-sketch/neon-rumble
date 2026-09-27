from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s

def rep(old,new,label,count=1):
    global s
    if old not in s: raise SystemExit(label+' anchor missing')
    s=s.replace(old,new,count)

old="""dragonRainDrop(f){
 const targets=this.fighters.filter(e=>e!==f&&e.health>0&&e.moonUltPhase!=='air');if(!targets.length)return;
 const e=targets[Math.floor(this.random()*targets.length)];this.effects.push({x:e.x+this.rand(-25,25),y:e.y-45,text:'💧',kind:'rain',side:f.side,team:f.team,life:.35});this.attack(f,e,10*f.scale,true);
 if(this.random()<.05){const live=this.fighters.filter(v=>v!==f&&v.health>0&&v.moonUltPhase!=='air');if(live.length){const t=live[Math.floor(this.random()*live.length)];this.effects.push({x:t.x,y:t.y,text:'⚡ 거대한 번개!',kind:'doom',side:f.side,team:f.team,life:.7});this.attack(f,t,150*f.scale,true)}}
}
"""
new="""dragonRainDrop(f){
 const x=this.rand(36,684);
 this.shots.push({x,y:24,vx:0,vy:1,owner:f.side,team:f.team,target:-1,kind:'dragon_rain',icon:'💧',radius:8*f.scale,speed:520*f.scale,damage:10*f.scale,life:2.2,bounces:0});
 if(this.random()<.05){const lx=this.rand(48,672);this.shots.push({x:lx,y:22,vx:0,vy:1,owner:f.side,team:f.team,target:-1,kind:'dragon_lightning',icon:'⚡',radius:22*f.scale,speed:760*f.scale,damage:150*f.scale,life:1.5,bounces:0});this.effects.push({x:lx,y:52,text:'⚡',kind:'doom',side:f.side,team:f.team,life:.22})}
}
"""
rep(old,new,'dragon rain drop projectile conversion')

move_anchor="""  if(s.kind==='wave'){for(const e of this.enemies(f)){if(e.health<=0||distance(s,e)>=e.radius+s.radius)continue;s.hitTargets=s.hitTargets||{};if(!s.hitTargets[e.side]){this.attackProjectile(f,e,s);s.hitTargets[e.side]=true;if(this.result!==null)break}if(e.health>0){e.x+=s.vx*s.speed*3.0*dt;e.y+=s.vy*s.speed*3.0*dt;this.keepInside(e)}}if(s.x<22||s.x>698||s.y<22||s.y>698)s.life=0;continue}
"""
rain_branch="""  if(s.kind==='dragon_rain'||s.kind==='dragon_lightning'){
   const hit=this.fighters.find(e=>e!==f&&e.health>0&&e.moonUltPhase!=='air'&&distance(s,e)<e.radius+s.radius);
   if(hit){this.attack(f,hit,s.damage,true);s.life=0;if(this.result!==null)break}
   if(s.y>698+s.radius)s.life=0;
   continue
  }
"""
if "s.kind==='dragon_rain'||s.kind==='dragon_lightning'" not in s:
    rep(move_anchor,move_anchor+rain_branch,'rain projectile collision')

render_anchor="""for(const s of engine.shots){ctx.save();ctx.translate(s.x,s.y);ctx.rotate(Math.atan2(s.vy,s.vx));if(s.kind==='water'){"""
render_new="""for(const s of engine.shots){ctx.save();ctx.translate(s.x,s.y);ctx.rotate(Math.atan2(s.vy,s.vx));if(s.kind==='dragon_rain'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(Math.max(20,s.radius*2.8))+'px \"Apple Color Emoji\",\"Segoe UI Emoji\",sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('💧',0,0)}else if(s.kind==='dragon_lightning'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.save();ctx.shadowColor='#fff27a';ctx.shadowBlur=22;ctx.font=(Math.max(46,s.radius*2.5))+'px \"Apple Color Emoji\",\"Segoe UI Emoji\",sans-serif';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('⚡',0,0);ctx.restore()}else if(s.kind==='water'){"""
rep(render_anchor,render_new,'rain projectile renderer')

# Keep patch-note description accurate.
s=s.replace('비의 분노는 5초 동안 0.1초마다 빗방울 피해 10을 무작위 대상에게 주며 아군도 맞을 수 있음. 빗방울마다 5% 확률로 번개 피해 150.','비의 분노는 5초 동안 0.1초마다 맵 위 랜덤 X좌표에서 빗방울 투사체가 떨어지며 충돌 시 피해 10. 아군도 맞을 수 있고 빗방울 생성마다 5% 확률로 거대 번개 투사체가 위에서 떨어져 피해 150.')

required=["kind:'dragon_rain'","kind:'dragon_lightning'","speed:520*f.scale","speed:760*f.scale","damage:10*f.scale","damage:150*f.scale","s.kind==='dragon_rain'||s.kind==='dragon_lightning'","e!==f&&e.health>0", "ctx.fillText('⚡',0,0)"]
for x in required:
    if x not in s: raise SystemExit('missing marker '+x)
if s==orig: raise SystemExit('no changes')
p.write_text(s,encoding='utf-8')
print('v3.56 rain projectile hotfix applied')
