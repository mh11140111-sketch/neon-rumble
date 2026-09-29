from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

# version + patch notes
once('<span class="badge">BATTLE <b>v3.66</b></span>','<span class="badge">BATTLE <b>v3.67</b></span>','version')
once('<details class="patch-notes"><summary>📒 패치노트 · v3.66</summary><div class="patch-body">', '<details class="patch-notes"><summary>📒 패치노트 · v3.67</summary><div class="patch-body"><div class="patch-version"><h3>v3.67 · 밸런스 · 신규 캐릭터 달팽이</h3><ul><li>🧘‍♂️ 초능력자 HP 550. 염력탄 30, 벽 밀치기 60으로 조정.</li><li>🧘‍♂️ 이동 AI 개편: 적과 궤도 거리를 유지하되 주기적으로 벽 회피 보정을 풀어 벽 근처까지 이동할 수 있음.</li><li>🐌 달팽이 추가. 매우 느린 이동속도 20, 근접 피해 6,767,676,767.</li><li>🐌 HP 30% 이하에서 1회, 5초간 껍질에 숨음. 모든 일반 피해 80% 감소, 0.5초마다 HP 20 회복.</li></ul></div>', 'patch notes')

# roster psychic + snail
old_psychic="{id:'psychic',name:'초능력자',icon:'🧘‍♂️',tag:'염력탄 · 벽 밀치기 · 투사체 궤도',hp:1000,damage:50,speed:95,cooldown:2,unlock:'psychic',description:'적과 궤도 공격에 유리한 거리를 유지하며 이동한다. 2초마다 염력 마법탄으로 피해 50과 넉백. 5초마다 상대를 벽으로 날려 피해 80과 1초 기절. 가까운 적 투사체를 자기 주위 궤도로 끌어당겨 되돌려 이용한다.',detail:'HP 1000 · 염력탄 50 / 2초 + 넉백 · 벽 밀치기 80 / 5초 + 기절 1초 · 적 투사체 궤도 포획 · 궤도탄 벽 접촉 시 자신이 원래 피해 · CH8 STAGE 3 10% 획득'},"
new_psychic="{id:'psychic',name:'초능력자',icon:'🧘‍♂️',tag:'염력탄 · 벽 밀치기 · 투사체 궤도',hp:550,damage:30,speed:95,cooldown:2,unlock:'psychic',description:'적과 궤도 공격에 유리한 거리를 유지하며 이동하고 가끔 벽 근처까지 붙는다. 2초마다 염력 마법탄으로 피해 30과 넉백. 5초마다 상대를 벽으로 날려 피해 60과 1초 기절. 가까운 적 투사체를 자기 주위 궤도로 끌어당겨 되돌려 이용한다.',detail:'HP 550 · 염력탄 30 / 2초 + 넉백 · 벽 밀치기 60 / 5초 + 기절 1초 · 적 투사체 궤도 포획 · 궤도탄 벽 접촉 시 자신이 원래 피해 · CH8 STAGE 3 10% 획득'},"
new_snail="{id:'snail',name:'달팽이',icon:'🐌',tag:'초저속 · 초고화력 · 껍질 방어',hp:1000,damage:6767676767,speed:20,cooldown:1,description:'매우매우 느리게 이동하지만 근접 공격 피해가 6,767,676,767이다. HP 30% 이하가 되면 전투당 1회 5초 동안 껍질에 숨어 받는 피해를 1/5로 줄이고 0.5초마다 HP 20을 회복한다.',detail:'HP 1000 · 이동속도 20 · 근접 6,767,676,767 · HP 30% 이하 1회 · 껍질 5초 · 피해 80% 감소 · 0.5초마다 HP 20 회복'},"
once(old_psychic,new_psychic+"\n"+new_snail,'psychic roster + snail')

# psychic movement: range maintenance, occasional wall contact, no direct double movement
start=s.find('psychicMaintainRange(f,e,dt){')
end=s.find('psychicSkill(f,e){',start)
if start<0 or end<0: raise SystemExit('psychic movement block not found')
new_move="""psychicMaintainRange(f,e,dt){
 if(!f||f.id!=='psychic'||!e||f.health<=0||e.health<=0||f.stunUntil>this.time)return;
 const dx=e.x-f.x,dy=e.y-f.y,d=Math.max(1,Math.hypot(dx,dy)),nx=dx/d,ny=dy/d;
 const near=125*f.scale,far=180*f.scale;let mx=0,my=0;
 if(d<near){mx=-nx;my=-ny}else if(d>far){mx=nx;my=ny}else{const dir=(f.side%2===0?1:-1);mx=-ny*dir;my=nx*dir}
 const wallPhase=((this.time+f.side)%6)<1.4,b=this.bounds(f);
 if(!wallPhase){const margin=70*f.scale,force=.75;if(f.x<Math.max(b.low,margin))mx+=force;if(f.x>Math.min(b.high,720-margin))mx-=force;if(f.y<Math.max(b.low,margin))my+=force;if(f.y>Math.min(b.high,720-margin))my-=force}
 const m=Math.hypot(mx,my)||1;f.vx=mx/m;f.vy=my/m;f.turn=.3;
}
"""
s=s[:start]+new_move+s[end:]

# psychic damage
once('f.psychicPushNext=this.time+5/f.scale;const dealt=this.attack(f,e,80*f.scale);','f.psychicPushNext=this.time+5/f.scale;const dealt=this.attack(f,e,60*f.scale);','psychic push damage')
once("this.effect(e,'🧘‍♂️ 벽 밀치기 80 · 기절!','skill')","this.effect(e,'🧘‍♂️ 벽 밀치기 60 · 기절!','skill')",'psychic push text')
once("kind:'psychic_bolt',icon:'🟣',radius:9*f.scale,speed:330*f.scale,damage:50*f.scale","kind:'psychic_bolt',icon:'🟣',radius:9*f.scale,speed:330*f.scale,damage:30*f.scale",'psychic bolt damage')

# snail shell state helper before psychic movement
anchor='psychicMaintainRange(f,e,dt){'
snail_code="""snailShellSkill(f){
 if(!f||f.id!=='snail'||f.health<=0)return false;
 if(f.snailShellUsed===undefined){f.snailShellUsed=false;f.snailShellUntil=0;f.snailShellNextHeal=0;f.snailBaseArmor=f.armor||0}
 if(!f.snailShellUsed&&f.health<=f.hp*.3){f.snailShellUsed=true;f.snailShellUntil=this.time+5;f.snailShellNextHeal=this.time+.5;f.snailBaseArmor=f.armor||0;f.armor=Math.max(f.armor||0,.8);f.icon='🐚';f.vx=0;f.vy=0;this.effect(f,'🐚 껍질 방어 5초!','skill');this.emit('🐌 달팽이가 껍질에 숨었어! 피해 80% 감소')}
 if(this.time<(f.snailShellUntil||0)-1e-9){while(this.time>=f.snailShellNextHeal-1e-9){const heal=Math.min(20,f.hp-f.health);f.health+=heal;f.healed+=heal;if(heal)this.effect(f,'🐚 +20','heal');f.snailShellNextHeal+=.5}f.vx=0;f.vy=0;f.attack=0;return true}
 if((f.snailShellUntil||0)>0){f.snailShellUntil=0;f.armor=f.snailBaseArmor||0;f.icon='🐌';this.effect(f,'🐌 껍질 해제','skill')}
 return false
}
"""
once(anchor,snail_code+anchor,'snail shell helper')

# invoke shell early; while hidden, stop movement/attack
once(" if(f.id==='lizard')this.lizardSkill(f)\n if(f.id==='smith')this.smithWeaponSkill(f,e)", " if(f.id==='lizard')this.lizardSkill(f)\n if(f.id==='snail'&&this.snailShellSkill(f))return\n if(f.id==='smith')this.smithWeaponSkill(f,e)", 'snail step hook')

p.write_text(s,encoding='utf-8')
print('v3.67 patch applied')
