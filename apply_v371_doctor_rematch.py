from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

# version + release note
once('BATTLE <b>v3.70</b>','BATTLE <b>v3.71</b>','version')
old_summary='<summary>📒 패치노트 · v3.70</summary><div class="patch-body">'
new_summary='<summary>📒 패치노트 · v3.71</summary><div class="patch-body"><div class="patch-version"><h3>v3.71 · 의사 밸런스 · CH9 재시작 수정</h3><ul><li>👨‍⚕️ 의사 주사기 적 피해 80 → 70, 아군 즉시 회복 50 → 30. 샌드박스와 CH9 STAGE 3 모두 동일.</li><li>🧪 CH9 STAGE 3 결과창의 다시 플레이가 새 전투를 만들지 못하고 즉시 승리하던 문제 수정.</li></ul></div>'
once(old_summary,new_summary,'patch notes')

# doctor roster
old="{id:'doctor',name:'의사',icon:'👨‍⚕️',tag:'💉 주사기 · 약물치료',hp:1000,damage:80,speed:145,cooldown:1,unlock:'doctor',description:'가장 가까운 캐릭터를 향해 💉 주사기를 겨눈다. 적이 닿으면 피해 80과 독, 아군이 닿으면 즉시 HP 50 회복과 3초 약물치료를 부여한다. 약물치료는 0.5초마다 HP 10을 회복한다.',detail:'HP 1000 · 💉 적 80+독 · 아군 즉시 +50 · 약물치료 3초 / 0.5초마다 +10 · CH9 STAGE 3 10% 획득'},"
new="{id:'doctor',name:'의사',icon:'👨‍⚕️',tag:'💉 주사기 · 약물치료',hp:1000,damage:70,speed:145,cooldown:1,unlock:'doctor',description:'가장 가까운 캐릭터를 향해 💉 주사기를 겨눈다. 적이 닿으면 피해 70과 독, 아군이 닿으면 즉시 HP 30 회복과 3초 약물치료를 부여한다. 약물치료는 0.5초마다 HP 10을 회복한다.',detail:'HP 1000 · 💉 적 70+독 · 아군 즉시 +30 · 약물치료 3초 / 0.5초마다 +10 · CH9 STAGE 3 10% 획득'},"
once(old,new,'doctor roster')

# runtime doctor damage/heal
once("const dealt=this.attack(f,t,80*f.scale);if(dealt>0&&t.health>0)this.applyPoison(f,t);this.effect(t,'💉 80 + 독!','skill')", "const dealt=this.attack(f,t,70*f.scale);if(dealt>0&&t.health>0)this.applyPoison(f,t);this.effect(t,'💉 70 + 독!','skill')", 'doctor enemy hit')
once("const heal=Math.min(50*f.scale,t.hp-t.health);t.health+=heal;t.healed+=heal;t.drugTreatment={next:this.time+.5,expires:this.time+3};", "const heal=Math.min(30*f.scale,t.hp-t.health);t.health+=heal;t.healed+=heal;t.drugTreatment={next:this.time+.5,expires:this.time+3};", 'doctor ally heal')

# UI labels / chapter info
once("if(f.id==='doctor')return '👨‍⚕️ 💉 적 80+독 · 아군 +50+약물치료';", "if(f.id==='doctor')return '👨‍⚕️ 💉 적 70+독 · 아군 +30+약물치료';", 'doctor ability label')
once("'CHAPTER 9 STAGE 3 · 의사의 💉 주사기는 적에게 80+독, 아군에게 +50 및 3초 약물치료.'", "'CHAPTER 9 STAGE 3 · 의사의 💉 주사기는 적에게 70+독, 아군에게 +30 및 3초 약물치료.'", 'CH9 stage3 info')

# Critical CH9 replay fix: replay must rebuild a LAB engine, not fall through to generic start().
old_rematch="$('rematch').onclick=()=>mode==='stage'?startStage(stageNo):mode==='desert'?startDesertStage(desertStageNo):mode==='mansion'?startMansionStage(mansionStageNo):mode==='space'?startSpaceStage(spaceStageNo):mode==='casino'?startCasinoStage(casinoStageNo):mode==='ocean'?startOceanStage(oceanStageNo):mode==='forge'?startForgeStage(forgeStageNo):mode==='boxing'?startBoxingStage(boxingStageNo):start();"
new_rematch="$('rematch').onclick=()=>mode==='stage'?startStage(stageNo):mode==='desert'?startDesertStage(desertStageNo):mode==='mansion'?startMansionStage(mansionStageNo):mode==='space'?startSpaceStage(spaceStageNo):mode==='casino'?startCasinoStage(casinoStageNo):mode==='ocean'?startOceanStage(oceanStageNo):mode==='forge'?startForgeStage(forgeStageNo):mode==='boxing'?startBoxingStage(boxingStageNo):mode==='lab'?startLabStage(labStageNo):start();"
once(old_rematch,new_rematch,'CH9 rematch routing')

# Ensure entering normal start/selection from a lab battle cannot retain lab state/result.
old_start="if(mode==='boxing'||mode==='boxing-select'){resetBoxingTransient();mode='duel'}engine=mode==='group'?"
new_start="if(mode==='boxing'||mode==='boxing-select'){resetBoxingTransient();mode='duel'}if(mode==='lab'){engine=null;mode='duel'}engine=mode==='group'?"
once(old_start,new_start,'generic start lab reset')
old_sel="if(mode==='boxing'||mode==='boxing-select'){resetBoxingTransient();mode='duel'}engine=null;paused=false;"
new_sel="if(mode==='boxing'||mode==='boxing-select'){resetBoxingTransient();mode='duel'}if(mode==='lab'){engine=null;mode='duel'}engine=null;paused=false;"
once(old_sel,new_sel,'selection lab reset')

p.write_text(s,encoding='utf-8')
print('v3.71 patch applied')
