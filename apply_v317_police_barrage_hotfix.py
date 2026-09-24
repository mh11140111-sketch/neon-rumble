from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if old not in s:
        raise SystemExit(f'PATCH FAILED: {label}')
    s=s.replace(old,new,count)

# Police roster text: submarine patch, version/patch notes unchanged.
old="{id:'police',name:'경찰',icon:'👮‍♂️',tag:'테이저 · 총 난사',hp:1000,damage:30,speed:155,cooldown:1,description:'1초마다 테이저건을 발사해 피해 30과 0.2초 기절을 줘. 체력이 30% 이하가 되면 경기당 1회, 3초 동안 사방팔방으로 총을 난사해.',detail:'테이저 30 / 1초 · 명중 시 기절 0.2초 · HP 30% 이하 1회 총 난사 · 3초 동안 0.3초마다 8방향 · 총탄 100'}"
new="{id:'police',name:'경찰',icon:'👮‍♂️',tag:'테이저 · 총 난사',hp:1000,damage:30,speed:155,cooldown:1,description:'1초마다 테이저건을 발사해 피해 30과 0.2초 기절을 줘. 체력이 30% 이하가 되면 경기당 1회, 3초 동안 조준 없이 무작위 방향으로 총을 연속 발사해.',detail:'테이저 30 / 1초 · 명중 시 기절 0.2초 · HP 30% 이하 1회 총 난사 · 3초 동안 0.38초마다 1발 · 무작위 방향 · 총탄 100 · 벽 반사 없음'}"
rep(old,new,'police roster')

old_barrage="policeBarrage(f){if(f.id!=='police'||f.health<=0||this.time>=f.policeBarrageUntil-1e-9)return;if(this.time<f.policeBarrageCd-1e-9)return;f.policeBarrageCd=this.time+.3/f.scale;for(let i=0;i<8;i++){const a=i*Math.PI/4,vx=Math.cos(a),vy=Math.sin(a);this.shots.push({x:f.x+vx*(f.radius+7),y:f.y+vy*(f.radius+7),vx,vy,owner:f.side,team:f.team,target:-1,kind:'bullet',radius:4*f.scale,speed:520*f.scale,damage:100*f.scale,life:2.5*f.scale,bounces:0})}f.attack=.12/f.scale}"
new_barrage="policeBarrage(f){if(f.id!=='police'||f.health<=0||this.time>=f.policeBarrageUntil-1e-9)return;if(this.time<f.policeBarrageCd-1e-9)return;f.policeBarrageCd=this.time+.38/f.scale;const a=this.random()*Math.PI*2,vx=Math.cos(a),vy=Math.sin(a);this.shots.push({x:f.x+vx*(f.radius+7),y:f.y+vy*(f.radius+7),vx,vy,owner:f.side,team:f.team,target:-1,kind:'bullet',radius:4*f.scale,speed:520*f.scale,damage:100*f.scale,life:2.5*f.scale,bounces:0});f.attack=.12/f.scale}"
rep(old_barrage,new_barrage,'police barrage')

p.write_text(s,encoding='utf-8')
print('v3.17 police barrage submarine hotfix applied')
