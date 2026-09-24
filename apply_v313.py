from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=None):
    global s
    n=s.count(old)
    if n==0:
        raise SystemExit('pattern not found: '+old[:120])
    if count is not None and n!=count:
        raise SystemExit(f'expected {count} matches, got {n}: '+old[:120])
    s=s.replace(old,new)

# Version + patch notes
rep('BATTLE <b>v3.12</b>','BATTLE <b>v3.13</b>',1)
rep('📒 패치노트 · v3.12','📒 패치노트 · v3.13',1)
marker='<div class="patch-body"><div class="patch-version"><h3>v3.12 · 달의 강림</h3>'
insert='<div class="patch-body"><div class="patch-version"><h3>v3.13 · 보이지 않는 반격</h3><ul><li>불사조 불꽃 직접 피해가 7에서 10으로 증가.</li><li>신규 캐릭터 🫥 투명인간 추가: 기본 50% 확률로 공격을 무시.</li><li>공격 무시에 성공하면 공격한 상대에게 30 피해를 반사하며, 원거리 공격에도 적용.</li><li>공격 무시에 실패할 때마다 이후 무시 확률이 10%p 증가하며 성공 후에도 증가분은 유지.</li></ul></div><div class="patch-version"><h3>v3.12 · 달의 강림</h3>'
rep(marker,insert,1)

# Phoenix balance text / values
rep('불사조가 되어 불꽃 7을 사용해.','불사조가 되어 불꽃 10을 사용해.',1)
rep("f.awakened?'쪼기 '+30*f.scale+' · 불꽃 '+7*f.scale+' · 부활 소진'","f.awakened?'쪼기 '+30*f.scale+' · 불꽃 '+10*f.scale+' · 부활 소진'",1)
rep('damage:7*f.scale','damage:10*f.scale',1)
rep('불꽃 14 및 화상 확률 20%','불꽃 20 및 화상 확률 20%',1)

# Add Invisible Man roster entry after Moon
moon="{id:'moon',name:'달',icon:'🌝',tag:'반달 조각 · 월하강림',hp:1000,damage:80,speed:150,cooldown:2,description:'2초마다 🌜 반달 조각을 던져 피해 80. 조각이 날아간 동안 자신은 🌛 반달이 되고, 조각이 돌아오면 다시 🌝 보름달이 돼. 전투가 30초를 넘기면 궁극기를 준비해.',detail:'반달 조각 80 · 쿨타임 2초 · 30초 후 궁극기 · 5초 예고 뒤 전장 전체 즉사 · 무적 무시 · 팀 구분 없음'}"
invis=moon+"\n,{id:'invisible',name:'투명인간',icon:'🫥',tag:'투명 · 회피 · 반격',hp:1000,damage:0,speed:170,cooldown:0,description:'몸이 투명해 기본 50% 확률로 공격을 무시해. 무시에 성공하면 공격한 상대에게 30 피해를 즉시 반사하고, 원거리 공격도 동일해. 무시에 실패할 때마다 이후 무시 확률이 10%p 증가해.',detail:'기본 공격 없음 · 공격 무시 50% · 성공 시 반사 30 · 실패할 때마다 무시 확률 +10%p · 증가분 유지'}"
rep(moon,invis,1)

# Runtime state
rep("vampireBat:false,moonHalf:false","vampireBat:false,dodgeChance:type.id==='invisible'?.5:0,moonHalf:false",1)

# Invisible dodge/reflection in central damage pipeline. Reflection bypasses dodge recursion.
old="attack(f,e,dmg,friendly=false){\n if(this.result!==null||f.health<=0||e.health<=0||(!friendly&&f.team===e.team)||this.isStudying(e))return 0;\n f.attack=.35/f.scale;f.cd=f.cooldown;let n=Math.min(e.health,Math.round(dmg*(1-e.armor)));"
new="attack(f,e,dmg,friendly=false,bypassDodge=false){\n if(this.result!==null||f.health<=0||e.health<=0||(!friendly&&f.team===e.team)||this.isStudying(e))return 0;\n if(e.id==='invisible'&&!bypassDodge){if(this.random()<e.dodgeChance){this.effect(e,'공격 무시!','skill');const reflected=30*e.scale;this.attack(e,f,reflected,false,true);return 0}else{e.dodgeChance=Math.min(1,e.dodgeChance+.1);this.effect(e,'회피 '+Math.round(e.dodgeChance*100)+'%','skill')}}\n f.attack=.35/f.scale;f.cd=f.cooldown;let n=Math.min(e.health,Math.round(dmg*(1-e.armor)));"
rep(old,new,1)

# Invisible Man has no normal contact attack; only passive reflection.
rep("'hero','villain','moon'].includes(f.id)","'hero','villain','moon','invisible'].includes(f.id)",1)

# Ability HUD
old="function ability(f){return f.id==='moon'?"
new="function ability(f){return f.id==='invisible'?'공격 무시 '+Math.round(f.dodgeChance*100)+'% · 성공 시 반사 '+30*f.scale:f.id==='moon'?"
rep(old,new,1)

# Visual transparency on arena body.
old="for(const f of engine.fighters){if(f.moonUltPhase==='air')continue;const c=colors[f.team],r=f.radius;ctx.globalAlpha=f.health<=0?.15:1;"
new="for(const f of engine.fighters){if(f.moonUltPhase==='air')continue;const c=colors[f.team],r=f.radius;ctx.globalAlpha=f.health<=0?.15:(f.id==='invisible'?.38:1);"
rep(old,new,1)
# Preserve translucency after trail loop where alpha resets.
rep("ctx.globalAlpha=f.health<=0?.15:1;circle(f.x,f.y+10", "ctx.globalAlpha=f.health<=0?.15:(f.id==='invisible'?.38:1);circle(f.x,f.y+10",1)

p.write_text(s,encoding='utf-8')
print('v3.13 patch applied')
