from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s

def rep(old,new,label,count=1):
    global s
    if old not in s: raise SystemExit(label+' anchor missing')
    s=s.replace(old,new,count)

# Version and patch notes
rep('BATTLE <b>v3.55</b>','BATTLE <b>v3.56</b>','version')
rep('📒 패치노트 · v3.55','📒 패치노트 · v3.56','patch title')
marker='<div class="patch-body">'
patch='''<div class="patch-version"><h3>v3.56 · 용의 강림</h3><ul><li>🎰 도박장 1회 이용료를 200코인에서 50코인으로 인하.</li><li>🐉 신규 캐릭터 용 추가: 비의 분노와 신기루 사용.</li><li>비의 분노는 5초 동안 0.1초마다 빗방울 피해 10을 무작위 대상에게 주며 아군도 맞을 수 있음. 빗방울마다 5% 확률로 번개 피해 150.</li><li>신기루는 5초 동안 모든 공격을 회피하고 효과 종료 후 15초 쿨타임.</li><li>용 사망 시 HP 50 여의주로 변해 도망치며 5초 생존 시 용으로 부활. 보스전에도 적용.</li></ul></div>'''
if patch not in s: rep(marker,marker+patch,'patch notes')

# Casino price 200 -> 50 only in v3.55 casino system.
rep('1회 200코인으로 슬롯머신을 돌려 전용 꾸미기와 캐릭터를 노려 봐.','1회 50코인으로 슬롯머신을 돌려 전용 꾸미기와 캐릭터를 노려 봐.','casino panel price')
rep('🎰 200코인으로 돌리기','🎰 50코인으로 돌리기','casino button')
rep("spin.disabled=!ok||casinoSpinning||coins<200","spin.disabled=!ok||casinoSpinning||coins<50",'casino ui price')
rep("if(coins<200){alert('코인이 부족해! 슬롯머신은 200코인이 필요해.');return}coins-=200;","if(coins<50){alert('코인이 부족해! 슬롯머신은 50코인이 필요해.');return}coins-=50;",'casino spin price')

# Dragon roster entry.
dragon="""{id:'dragon',name:'용',icon:'🐉',tag:'비의 분노 · 신기루 · 여의주 부활',hp:1000,damage:0,speed:150,cooldown:0,description:'10초마다 5초 동안 비의 분노를 사용해 0.1초마다 무작위 대상에게 빗방울 피해 10을 준다. 빗방울마다 5% 확률로 거대한 번개 피해 150. 15초마다 5초 신기루로 모든 공격을 회피한다. 사망하면 HP 50 여의주가 되어 도망치고 5초 생존 시 부활한다.',detail:'HP 1000 · 비 5초 / 0.1초마다 10 · 빗방울마다 번개 5% / 150 · 비 종료 후 쿨타임 10초 · 신기루 5초 완전 회피 / 종료 후 15초 쿨타임 · 여의주 HP 50 / 5초 후 부활'},
"""
anchor="{id:'zombie_mage',name:'법사좀비'"
if "id:'dragon'" not in s: rep(anchor,dragon+anchor,'dragon roster')

# Constructor state.
old="mermanWaveNext:type.id==='merman'?3/scale:9999,oceanFishNext:(type.id==='tropical_fish'||type.id==='fish')?2/scale:9999,slashCd:0"
new="mermanWaveNext:type.id==='merman'?3/scale:9999,oceanFishNext:(type.id==='tropical_fish'||type.id==='fish')?2/scale:9999,dragonRainNext:type.id==='dragon'?10/scale:9999,dragonRaining:false,dragonRainUntil:0,dragonRainDropNext:0,dragonMirageNext:type.id==='dragon'?15/scale:9999,dragonMirageUntil:0,dragonOrb:false,dragonOrbUntil:0,dragonBaseHp:0,dragonBaseSpeed:0,dragonBaseRadius:0,dragonBaseBodyScale:0,slashCd:0"
rep(old,new,'dragon constructor state')

# Dragon methods before formEgg.
anchor='formEgg(f){'
methods="""dragonMirageActive(f){return !!(f&&f.id==='dragon'&&!f.dragonOrb&&(f.dragonMirageUntil||0)>this.time)}
dragonRainDrop(f){
 const targets=this.fighters.filter(e=>e!==f&&e.health>0&&e.moonUltPhase!=='air');if(!targets.length)return;
 const e=targets[Math.floor(this.random()*targets.length)];this.effects.push({x:e.x+this.rand(-25,25),y:e.y-45,text:'💧',kind:'rain',side:f.side,team:f.team,life:.35});this.attack(f,e,10*f.scale,true);
 if(this.random()<.05){const live=this.fighters.filter(v=>v!==f&&v.health>0&&v.moonUltPhase!=='air');if(live.length){const t=live[Math.floor(this.random()*live.length)];this.effects.push({x:t.x,y:t.y,text:'⚡ 거대한 번개!',kind:'doom',side:f.side,team:f.team,life:.7});this.attack(f,t,150*f.scale,true)}}
}
updateDragon(f,dt){
 if(f.id!=='dragon'||f.health<=0||f.dragonOrb)return;
 if(this.dragonMirageActive(f)){f.poison=null;f.toxin=null;f.burn=null;f.curse=null;f.bleed=null;f.stunUntil=0}
 if(!f.dragonRaining&&this.time>=(f.dragonRainNext||9999)-1e-9){f.dragonRaining=true;f.dragonRainUntil=this.time+5/f.scale;f.dragonRainDropNext=this.time;this.effect(f,'🌧️ 비의 분노 5초!','skill');this.emit('🐉 비의 분노! 아군도 비를 맞을 수 있어')}
 if(f.dragonRaining){while(f.dragonRainDropNext<=this.time+1e-9&&f.dragonRainDropNext<=f.dragonRainUntil+1e-9){this.dragonRainDrop(f);f.dragonRainDropNext+=.1/f.scale}if(this.time>=f.dragonRainUntil-1e-9){f.dragonRaining=false;f.dragonRainNext=this.time+10/f.scale;this.effect(f,'🌧️ 비 종료 · 쿨타임 시작','skill')}}
 if(this.time>=(f.dragonMirageNext||9999)-1e-9&&!this.dragonMirageActive(f)){f.dragonMirageUntil=this.time+5/f.scale;f.dragonMirageNext=Infinity;f.poison=null;f.toxin=null;f.burn=null;f.curse=null;f.bleed=null;f.stunUntil=0;this.effects.push({x:360,y:360,text:'🌫️ 신기루 · 모든 공격 회피',kind:'skill',side:f.side,team:f.team,life:1.2});this.effect(f,'🌫️ 신기루 5초!','skill')}
 if(f.dragonMirageNext===Infinity&&f.dragonMirageUntil>0&&this.time>=f.dragonMirageUntil-1e-9){f.dragonMirageUntil=0;f.dragonMirageNext=this.time+15/f.scale;this.effect(f,'🌫️ 신기루 종료 · 쿨타임 시작','skill')}
}
updateDragonOrb(f,dt){if(f.id!=='dragon'||!f.dragonOrb||f.health<=0)return;const es=this.enemies(f);const e=es.reduce((a,b)=>!a||distance(f,b)<distance(f,a)?b:a,null);if(e){const d=Math.max(1,distance(f,e));f.vx=(f.x-e.x)/d;f.vy=(f.y-e.y)/d}else this.turn(f);const sp=80;f.x+=f.vx*sp*dt;f.y+=f.vy*sp*dt;this.keepInside(f)}
formDragonOrb(f){if(!f||f.id!=='dragon'||f.dragonOrb||f.health>0)return false;f.dragonBaseHp=f.dragonBaseHp||f.hp;f.dragonBaseSpeed=f.dragonBaseSpeed||f.speed;f.dragonBaseRadius=f.dragonBaseRadius||f.radius;f.dragonBaseBodyScale=f.dragonBaseBodyScale||f.bodyScale;f.dragonOrb=true;f.name='여의주';f.icon='🔮';f.hp=50;f.health=50;f.speed=80;f.radius=Math.max(16,(f.boss?24:18));f.dragonOrbUntil=this.time+5;f.dragonRaining=false;f.dragonRainUntil=0;f.dragonMirageUntil=0;f.dragonMirageNext=Infinity;f.poison=null;f.toxin=null;f.burn=null;f.curse=null;f.bleed=null;f.stunUntil=0;f.capturedBy=null;f.trail=[];this.shots=this.shots.filter(s=>s.owner!==f.side);this.effect(f,'🔮 여의주 · 5초 생존!','skill');this.emit('🐉 용이 여의주로 변했어! 5초 동안 살아남으면 부활');return true}
reviveDragon(f){if(!f||f.id!=='dragon'||!f.dragonOrb||f.health<=0)return;f.dragonOrb=false;f.name='용';f.icon='🐉';f.hp=f.dragonBaseHp||1000*(f.boss?2.5:1);f.health=f.hp;f.speed=f.dragonBaseSpeed||150*f.scale;f.radius=f.dragonBaseRadius||33*(f.boss?3:1);f.bodyScale=f.dragonBaseBodyScale||(f.boss?3:1);f.dragonOrbUntil=0;f.dragonRainNext=this.time+10/f.scale;f.dragonMirageNext=this.time+15/f.scale;f.dragonMirageUntil=0;f.dragonRaining=false;f.poison=null;f.toxin=null;f.burn=null;f.curse=null;f.bleed=null;f.stunUntil=0;f.deathOrder=null;this.effect(f,'🐉 용 부활!','skill');this.emit('🔮 여의주가 5초를 버텨 용으로 부활!')}
"""
if 'dragonMirageActive(f)' not in s: rep(anchor,methods+anchor,'dragon methods')

# Extend death conversion through standard formEgg path.
rep('formEgg(f){\n',"formEgg(f){\n if(f.id==='dragon'&&f.health<=0&&!f.dragonOrb)return this.formDragonOrb(f);\n",'dragon death hook')

# Mirage blocks normal attack path.
attack_guard="if(this.result!==null||f.health<=0||e.health<=0||(!friendly&&f.team===e.team)||this.isStudying(e)||(e.id==='ghost'&&e.ghostPhaseUntil>this.time))return 0;"
rep(attack_guard,attack_guard+"\n if(this.dragonMirageActive(e)){this.effect(e,'🌫️ 회피!','skill');return 0;}",'dragon mirage attack dodge')

# Mirage also avoids major direct global damage paths.
rep("for(const e of [...this.fighters]){if(e===f||e.health<=0)continue;const n=Math.min(e.health,100);","for(const e of [...this.fighters]){if(e===f||e.health<=0||this.dragonMirageActive(e))continue;const n=Math.min(e.health,100);",'knight shockwave mirage')
rep("for(const e of this.fighters){if(e===f||e.health<=0)continue;e.health=0;e.trail=[];","for(const e of this.fighters){if(e===f||e.health<=0||this.dragonMirageActive(e))continue;e.health=0;e.trail=[];",'moon ult mirage')

# Update dragon skills / orb revive in round loop.
old="for(const f of [...this.fighters]){this.transformHero(f);this.updateVampire(f);this.updateNinjaClone(f);this.moonSkill(f);this.study(f)}"
new="for(const f of [...this.fighters]){this.transformHero(f);this.updateVampire(f);this.updateNinjaClone(f);this.moonSkill(f);this.study(f);this.updateDragon(f,dt)}"
rep(old,new,'dragon round update')
old="for(const f of this.fighters)if(f.egg&&f.health>0&&this.time>=f.eggUntil-1e-9)this.revive(f);"
new=old+"for(const f of this.fighters)if(f.id==='dragon'&&f.dragonOrb&&f.health>0&&this.time>=f.dragonOrbUntil-1e-9)this.reviveDragon(f);"
rep(old,new,'dragon orb revive loop')
old="for(const f of this.fighters){if(f.health<=0)continue;if(f.id==='crab_shell'){f.vx=0;f.vy=0;continue}"
new="for(const f of this.fighters){if(f.health<=0)continue;if(f.id==='dragon'&&f.dragonOrb){this.updateDragonOrb(f,dt);continue}if(f.id==='crab_shell'){f.vx=0;f.vy=0;continue}"
rep(old,new,'dragon orb movement')

# Dragon has no default contact attack.
rep("'crab','crab_shell','alien'","'crab','crab_shell','dragon','alien'",'dragon contact exclusion')

required=['BATTLE <b>v3.56</b>',"id:'dragon'",'coins-=50','dragonRainDrop(f)','dragonMirageActive(f)','formDragonOrb(f)','reviveDragon(f)','dragonOrbUntil=this.time+5','this.random()<.05','150*f.scale','10*f.scale,true']
for x in required:
    if x not in s: raise SystemExit('missing marker '+x)
if s==orig: raise SystemExit('no changes')
p.write_text(s,encoding='utf-8')
print('v3.56 dragon patch applied')
