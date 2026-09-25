from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n!=count:
        raise SystemExit(f'replace mismatch: expected {count}, found {n}: {old[:180]!r}')
    s=s.replace(old,new,count)

# Add explicit desert transient-state reset helper.
old="let desertStageNo=1,desertWave=0,desertNextMageSummon=10;"
new="let desertStageNo=1,desertWave=0,desertNextMageSummon=10;\nfunction resetDesertTransient(){desertStageNo=1;desertWave=0;desertNextMageSummon=10;if(engine)engine.desertWaveMode=false}"
rep(old,new)

# General battle start must never reuse stale desert state.
old="function start(){engine=mode==='group'?"
new="function start(){if(mode==='desert'||mode==='desert-select'){resetDesertTransient();mode='duel'}engine=mode==='group'?"
rep(old,new)

# Leaving a desert battle/select screen fully resets all desert transient state.
old="function selection(){if(mode==='desert')mode='duel';engine=null;paused=false;acc=0;keys.clear();resetStick();"
new="function selection(){if(mode==='desert'||mode==='desert-select'){resetDesertTransient();mode='duel'}engine=null;paused=false;acc=0;keys.clear();resetStick();"
rep(old,new)

# Centralize regular-mode switching so stale stage-3 state can never survive a mode change.
old="$('choose0').onclick=()=>{side=0;bossSlot=-1;updateSelection()};$('choose1').onclick=()=>{side=1;bossSlot=Math.max(0,bossSlot);updateSelection()};$('random').onclick=()=>{const playable=ROSTER.filter(c=>!c.stageOnly&&(!c.unlock||skeletonsUnlocked)),rand=()=>playable[Math.floor(Math.random()*playable.length)].id;if(isBossMode()){bossChoice=rand();squad=squad.map(rand)}else if(['relay','group'].includes(mode))relayTeams=relayTeams.map(t=>t.map(rand));else selected=selected.map(rand);updateSelection()};$('mode-duel').onclick=()=>{mode='duel';updateSelection()};$('mode-boss').onclick=()=>{mode='boss';bossSlot=-1;updateSelection()};\n$('mode-relay').onclick=()=>{mode='relay';side=0;updateSelection()};$('mode-group').onclick=()=>{mode='group';side=0;updateSelection()};$('mode-control').onclick=()=>{mode='control';side=0;bossSlot=-1;updateSelection()};"
new="$('choose0').onclick=()=>{side=0;bossSlot=-1;updateSelection()};$('choose1').onclick=()=>{side=1;bossSlot=Math.max(0,bossSlot);updateSelection()};$('random').onclick=()=>{const playable=ROSTER.filter(c=>!c.stageOnly&&(!c.unlock||skeletonsUnlocked)),rand=()=>playable[Math.floor(Math.random()*playable.length)].id;if(isBossMode()){bossChoice=rand();squad=squad.map(rand)}else if(['relay','group'].includes(mode))relayTeams=relayTeams.map(t=>t.map(rand));else selected=selected.map(rand);updateSelection()};function switchRegularMode(next){if(mode==='desert'||mode==='desert-select')resetDesertTransient();engine=null;mode=next;updateSelection()}$('mode-duel').onclick=()=>{switchRegularMode('duel')};$('mode-boss').onclick=()=>{bossSlot=-1;switchRegularMode('boss')};\n$('mode-relay').onclick=()=>{side=0;switchRegularMode('relay')};$('mode-group').onclick=()=>{side=0;switchRegularMode('group')};$('mode-control').onclick=()=>{side=0;bossSlot=-1;switchRegularMode('control')};"
rep(old,new)

# Entering Chapter 1 / controlled boss also clears any stale desert transient state.
old="$('stage-entry').onclick=()=>{mode='stage';stageNo=1;updateSelection();window.scrollTo({top:0,behavior:'auto'})};\n$('boss-control-entry').onclick=()=>{if(!controlBossUnlocked)return;mode='boss-control';bossSlot=-1;side=0;updateSelection();window.scrollTo({top:0,behavior:'auto'})};"
new="$('stage-entry').onclick=()=>{if(mode==='desert'||mode==='desert-select')resetDesertTransient();engine=null;mode='stage';stageNo=1;updateSelection();window.scrollTo({top:0,behavior:'auto'})};\n$('boss-control-entry').onclick=()=>{if(!controlBossUnlocked)return;if(mode==='desert'||mode==='desert-select')resetDesertTransient();engine=null;mode='boss-control';bossSlot=-1;side=0;updateSelection();window.scrollTo({top:0,behavior:'auto'})};"
rep(old,new)

# Patch note line documenting final state leak fix.
needle="<li>사막 스테이지 종료 후 일반 모드로 돌아왔을 때 사막 승패 판정이 남아 일반전 진행을 막던 모드 상태 버그 수정.</li>"
rep(needle,needle+"<li>사막 STAGE 3 클리어·패배 후 다른 모드를 선택해도 STAGE 3이 다시 실행되던 잔여 상태 버그 수정. 일반 모드 시작 시 사막 임시 상태를 강제로 초기화.</li>")

p.write_text(s,encoding='utf-8')
print('v3.34 desert stage 3 state guard applied')
