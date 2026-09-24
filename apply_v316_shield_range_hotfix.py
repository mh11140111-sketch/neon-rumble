from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if old not in s:
        raise SystemExit(f'PATCH FAILED: {label}')
    s=s.replace(old,new,count)

old="knightBlocksProjectile(f,s){if(f.id!=='knight'||f.health<=0)return false;const charged=this.time<f.knightShieldChargedUntil-1e-9;if(charged)return true;const p=this.knightShieldPoint(f);return Math.hypot(s.x-p.x,s.y-p.y)<=p.r+(s.radius||5)}"
new="knightBlocksProjectile(f,s){if(f.id!=='knight'||f.health<=0)return false;const charged=this.time<f.knightShieldChargedUntil-1e-9;if(charged&&Math.hypot(s.x-f.x,s.y-f.y)<=f.radius+55+(s.radius||5))return true;const p=this.knightShieldPoint(f);return Math.hypot(s.x-p.x,s.y-p.y)<=p.r+(s.radius||5)}"
rep(old,new,'charged shield range')

old_moon="if(s.kind==='moon'){if(s.returning){const a=this.aim(s,f);s.vx=a.x;s.vy=a.y;s.x+=s.vx*s.speed*dt;s.y+=s.vy*s.speed*dt;if(distance(s,f)<=f.radius+s.radius+7){s.life=0;f.moonShot=null;f.moonHalf=false;f.icon='🌝';this.effect(f,'보름달 복귀','skill');continue}}else{s.x+=s.vx*s.speed*dt;s.y+=s.vy*s.speed*dt;const e=this.enemies(f).find(v=>distance(s,v)<v.radius+s.radius);if(e&&!s.hit){if(e.id==='knight'&&this.knightBlocksProjectile(e,s)){this.blockProjectileWithKnight(e,s,f);s.hit=true;s.returning=true}else{this.attackProjectile(f,e,s);s.hit=true;s.returning=true}}if(s.x<22||s.x>698||s.y<22||s.y>698)s.returning=true}continue}"
new_moon="if(s.kind==='moon'){if(s.returning){const a=this.aim(s,f);s.vx=a.x;s.vy=a.y;s.x+=s.vx*s.speed*dt;s.y+=s.vy*s.speed*dt;if(distance(s,f)<=f.radius+s.radius+7){s.life=0;f.moonShot=null;f.moonHalf=false;f.icon='🌝';this.effect(f,'보름달 복귀','skill');continue}}else{s.x+=s.vx*s.speed*dt;s.y+=s.vy*s.speed*dt;const blocker=this.enemies(f).find(v=>v.id==='knight'&&this.knightBlocksProjectile(v,s));if(blocker){this.blockProjectileWithKnight(blocker,s,f);s.hit=true;s.returning=true;continue}const e=this.enemies(f).find(v=>distance(s,v)<v.radius+s.radius);if(e&&!s.hit){this.attackProjectile(f,e,s);s.hit=true;s.returning=true}if(s.x<22||s.x>698||s.y<22||s.y>698)s.returning=true}continue}"
rep(old_moon,new_moon,'moon shield range')

p.write_text(s,encoding='utf-8')
print('v3.16 charged shield range hotfix applied')
