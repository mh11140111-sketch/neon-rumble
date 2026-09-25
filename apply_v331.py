from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Version badge + patch notes
assert 'BATTLE <b>v3.30</b>' in s
assert '📒 패치노트 · v3.30' in s
assert '<div class="patch-body"><div class="patch-version"><h3>v3.30 · 유령 리워크 & 눈사람 밸런스</h3>' in s
s=s.replace('BATTLE <b>v3.30</b>','BATTLE <b>v3.31</b>',1)
s=s.replace('📒 패치노트 · v3.30','📒 패치노트 · v3.31',1)
new_notes='''<div class="patch-body"><div class="patch-version"><h3>v3.31 · 카우보이 & 밸런스</h3><ul><li>분노한 남자: 2회 부활한 🤬 상태의 근접 🤜 공격 재사용 대기시간 1초 → 1.5초.</li><li>신규 캐릭터 🤠 카우보이: 🐴 탑승 중 이동속도 +100%. 총알 피해 80, 빠른 탄속, 1초마다 발사.</li><li>카우보이: 탄창 6발. 모두 사용하면 6초 동안 재장전하며 재장전 중에는 공격할 수 없음.</li><li>카우보이: 체력이 30% 이하가 되면 말이 사라지고 이동속도 +100% 효과도 사라짐.</li></ul></div><div class="patch-version"><h3>v3.30 · 유령 리워크 & 눈사람 밸런스</h3>'''
s=s.replace('<div class="patch-body"><div class="patch-version"><h3>v3.30 · 유령 리워크 & 눈사람 밸런스</h3>',new_notes,1)

# Angry Man final punch cooldown 1.0 -> 1.5 sec
old="f.angryPunchCd=1/f.scale;if(dealt>0&&e.health>0)"
assert old in s
s=s.replace(old,"f.angryPunchCd=1.5/f.scale;if(dealt>0&&e.health>0)",1)

# Update Angry Man text
s=s.replace('최종 단계에서는 🤜 피해 85 + 기절 1초를 주며 근접 공격 쿨타임은 1초야.','최종 단계에서는 🤜 피해 85 + 기절 1초를 주며 근접 공격 쿨타임은 1.5초야.',1)
s=s.replace('최종 🤜85 + 기절 1초 / 쿨타임 1초','최종 🤜85 + 기절 1초 / 쿨타임 1.5초',1)

# Add Cowboy to roster after Ghost
needle="{id:'ghost',name:'유령',icon:'👻',tag:'3초 대쉬 · 접촉 30 · 시체 빙의',hp:1000,damage:30,speed:170,cooldown:0,description:'3초마다 가장 가까운 적에게 짧게 대쉬해. 적과 닿으면 피해 30을 주고 0.3초 동안 모든 충돌과 공격을 통과해. 팀전에서는 처음 죽은 아군이나 아군 소환수의 시체에 경기당 1회 빙의해.',detail:'HP 1000 · 3초마다 적 방향 대쉬 · 접촉 피해 30 + 0.3초 통과 · 팀전 1회 시체 빙의 · 소환수 빙의 가능 · 빙의체 HP 300 / 최대 HP가 300 미만이면 풀 회복 · 빙의체 사망 시 유령 복귀'}"
assert needle in s
cowboy="{id:'cowboy',name:'카우보이',icon:'🤠🐴',tag:'말 탑승 · 6발 탄창',hp:1000,damage:80,speed:150,cooldown:1,description:'🐴 말을 타고 시작해 이동속도가 100% 증가해. 피해 80의 빠른 총알을 1초마다 쏘며 탄창은 6발이야. 6발을 모두 쓰면 6초 동안 재장전하고, 체력이 30% 이하가 되면 말이 사라져 이동속도 증가도 끝나.',detail:'HP 1000 · 말 탑승 중 이동속도 +100% · 총알 80 · 탄속 약 1.5배 · 1초마다 발사 · 탄창 6발 · 재장전 6초 · HP 30% 이하 말 소멸'}"
s=s.replace(needle,needle+',\n'+cowboy,1)

# Initialize Cowboy state
old="ghostPhaseUntil:0,ghostDashNext:type.id==='ghost'?3/scale:9999,ghostReviveUsed:false"
assert old in s
new="ghostPhaseUntil:0,ghostDashNext:type.id==='ghost'?3/scale:9999,cowboyMounted:type.id==='cowboy',cowboyAmmo:type.id==='cowboy'?6:0,cowboyReloadUntil:0,ghostReviveUsed:false"
s=s.replace(old,new,1)

# Add cowboy skill invocation
old="this.transformHero(f);this.updateVampire(f);this.moonSkill(f);this.updateKnightShield(f,dt);this.knightGiantSlash(f,e);if(f.id==='snowman')this.snowmanShot(f,e);if(f.id==='angryman')this.angryManSkill(f,e,dt);"
assert old in s
new="this.transformHero(f);this.updateVampire(f);this.moonSkill(f);this.updateKnightShield(f,dt);this.knightGiantSlash(f,e);if(f.id==='snowman')this.snowmanShot(f,e);if(f.id==='angryman')this.angryManSkill(f,e,dt);if(f.id==='cowboy')this.cowboySkill(f,e);"
s=s.replace(old,new,1)

# Add Cowboy skill before Angry Man skill
marker="angryManSkill(f,e,dt){"
assert marker in s
cowboy_method="""cowboySkill(f,e){
 if(f.id!=='cowboy'||f.health<=0)return;
 if(f.cowboyMounted&&f.health<=f.hp*.3){f.cowboyMounted=false;f.icon='🤠';this.effect(f,'🐴 말이 떠났다!','skill');this.emit('🤠 카우보이가 말에서 내렸다!')}
 if(f.cowboyReloadUntil>0){if(this.time<f.cowboyReloadUntil-1e-9)return;f.cowboyReloadUntil=0;f.cowboyAmmo=6;this.effect(f,'🔫 장전 완료!','skill')}
 if(f.cd>1e-9)return;
 if(f.cowboyAmmo<=0){f.cowboyReloadUntil=this.time+6/f.scale;this.effect(f,'🔄 재장전 6초','skill');return}
 const a=this.aim(f,e);this.shots.push({x:f.x+a.x*(f.radius+8),y:f.y+a.y*(f.radius+8),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'cowboybullet',radius:6*f.scale,speed:450*f.scale,damage:80*f.scale,life:3,bounces:0});
 f.cowboyAmmo--;f.cd=1/f.scale;f.attack=.16/f.scale;this.effect(f,'🔫 '+f.cowboyAmmo+'/6','skill');
 if(f.cowboyAmmo<=0)f.cowboyReloadUntil=this.time+6/f.scale;
}
"""
s=s.replace(marker,cowboy_method+marker,1)

# Mounted movement speed doubles; dismounted returns to base speed
old="const speed=(f.capturedBy!==null?0:f.id==='hero'&&f.heroReady?(f.heroPhase==='rush'?750:450)*f.scale:prey?610*f.scale:f.dash>0?610*f.scale:f.speed)*(1-Math.max(f.slowPower,f.rootSlowPower));"
assert old in s
new="const speed=(f.capturedBy!==null?0:f.id==='hero'&&f.heroReady?(f.heroPhase==='rush'?750:450)*f.scale:prey?610*f.scale:f.dash>0?610*f.scale:(f.id==='cowboy'&&f.cowboyMounted?f.speed*2:f.speed))*(1-Math.max(f.slowPower,f.rootSlowPower));"
s=s.replace(old,new,1)

# Ensure Cowboy does not use generic contact melee
old="'angryman','lizardtail','ghost'].includes(f.id)"
assert old in s
s=s.replace(old,"'angryman','lizardtail','ghost','cowboy'].includes(f.id)",1)

p.write_text(s,encoding='utf-8')

# Static safeguards
s2=p.read_text(encoding='utf-8')
assert 'BATTLE <b>v3.31</b>' in s2
assert "id:'cowboy'" in s2
assert "damage:80*f.scale" in s2
assert "speed:450*f.scale" in s2
assert "cowboyAmmo:type.id==='cowboy'?6:0" in s2
assert "cowboyReloadUntil=this.time+6/f.scale" in s2
assert "f.cowboyMounted&&f.health<=f.hp*.3" in s2
assert "f.angryPunchCd=1.5/f.scale" in s2
print('v3.31 patch applied and verified')
