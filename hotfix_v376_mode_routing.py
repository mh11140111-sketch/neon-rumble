from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1, got {n}')
    s=s.replace(old,new,1)

old="""function start(){if(mode==='desert'||mode==='desert-select'){resetDesertTransient();mode='duel'}if(mode==='mansion'||mode==='mansion-select'){resetMansionTransient();mode='duel'}if(mode==='space'||mode==='space-select'){resetSpaceTransient();mode='duel'}if(mode==='casino'||mode==='casino-select'){resetCasinoTransient();mode='duel'}if(mode==='ocean'||mode==='ocean-select'){resetOceanTransient();mode='duel'}if(mode==='forge'||mode==='forge-select'){resetForgeTransient();mode='duel'}if(mode==='boxing'||mode==='boxing-select'){resetBoxingTransient();mode='duel'}if(mode==='lab'||mode==='lab-select'||mode==='hell'||mode==='hell-select'||mode==='newchapter'||mode==='newchapter-select'){engine=null;mode='duel'}engine=mode==='group'?new Engine(relayTeams[0][0],relayTeams[1][0],Math.random,{mode:'group',teams:relayTeams}):mode==='relay'?new Engine(relayTeams[0][0],relayTeams[1][0],Math.random,{mode:'relay',teams:relayTeams}):isBossMode()?new Engine(bossChoice,squad[0],Math.random,{mode:'boss',allies:squad}):mode==='control'?new Engine(selected[0],selected[1],Math.random,{mode:'control'}):new Engine(...selected);if(mode==='boss-control')engine.manualTeam0=true;paused=false;"""
new="""function createEngineForMode(activeMode){
 if(activeMode==='group')return new Engine(relayTeams[0][0],relayTeams[1][0],Math.random,{mode:'group',teams:relayTeams});
 if(activeMode==='relay')return new Engine(relayTeams[0][0],relayTeams[1][0],Math.random,{mode:'relay',teams:relayTeams});
 if(activeMode==='boss'||activeMode==='boss-control')return new Engine(bossChoice,squad[0],Math.random,{mode:'boss',allies:squad});
 if(activeMode==='control')return new Engine(selected[0],selected[1],Math.random,{mode:'control'});
 return new Engine(selected[0],selected[1],Math.random,{mode:'duel'})
}
function verifyStartedMode(activeMode,battleEngine){
 if(!battleEngine)return false;
 if(activeMode==='group')return battleEngine.mode==='group'&&battleEngine.fighters.filter(f=>!f.summon).length>=6;
 if(activeMode==='relay')return battleEngine.mode==='relay';
 if(activeMode==='boss'||activeMode==='boss-control')return battleEngine.mode==='boss';
 if(activeMode==='control')return battleEngine.mode==='control'&&battleEngine.fighters.filter(f=>!f.summon).length===2;
 return battleEngine.mode==='duel'&&battleEngine.fighters.filter(f=>!f.summon).length===2
}
function start(){if(mode==='desert'||mode==='desert-select'){resetDesertTransient();mode='duel'}if(mode==='mansion'||mode==='mansion-select'){resetMansionTransient();mode='duel'}if(mode==='space'||mode==='space-select'){resetSpaceTransient();mode='duel'}if(mode==='casino'||mode==='casino-select'){resetCasinoTransient();mode='duel'}if(mode==='ocean'||mode==='ocean-select'){resetOceanTransient();mode='duel'}if(mode==='forge'||mode==='forge-select'){resetForgeTransient();mode='duel'}if(mode==='boxing'||mode==='boxing-select'){resetBoxingTransient();mode='duel'}if(mode==='lab'||mode==='lab-select'||mode==='hell'||mode==='hell-select'||mode==='newchapter'||mode==='newchapter-select'){engine=null;mode='duel'}const activeMode=mode;engine=createEngineForMode(activeMode);if(!verifyStartedMode(activeMode,engine)){console.error('NEON RUMBLE mode routing blocked',{activeMode,engineMode:engine?.mode,fighters:engine?.fighters?.length});engine=null;alert('전투 모드 연결 오류를 감지해 시작을 중단했어. 모드를 다시 선택해 줘.');return}if(activeMode==='boss-control')engine.manualTeam0=true;paused=false;"""
once(old,new,'replace nested start routing')

# Keep active mode stable throughout labels/event rendering.
once(
"$('event').textContent=mode==='group'?'단체전 시작! 양 팀 3명이 동시에 전투해.':mode==='boss-control'?'조정 보스전 시작! 보스를 엄지스틱으로 직접 이동해.':isBossMode()?'보스전 시작! 도전자 5명이 동시에 전투해.':mode==='control'?'조정 모드 시작! 왼쪽 엄지스틱으로 이동해.':'전투 시작!';",
"$('event').textContent=activeMode==='group'?'단체전 시작! 양 팀 3명이 동시에 전투해.':activeMode==='boss-control'?'조정 보스전 시작! 보스를 엄지스틱으로 직접 이동해.':(activeMode==='boss')?'보스전 시작! 도전자 5명이 동시에 전투해.':activeMode==='control'?'조정 모드 시작! 왼쪽 엄지스틱으로 이동해.':'전투 시작!';",
'event active mode')
once(
"$('squad-hud').hidden=!isBossMode();$('score-label0').textContent=isBossMode()?'보스':'왼쪽';$('score-label1').textContent=isBossMode()?'도전자 팀':'오른쪽';$('battle-mode').textContent=mode==='group'?'GROUP 3V3':mode==='relay'?'RELAY':mode==='boss-control'?'CONTROL BOSS':isBossMode()?'BOSS RAID':mode==='control'?'CONTROL':'DUEL';$('relay-hud').hidden=!['relay','group'].includes(mode);",
"$('squad-hud').hidden=!['boss','boss-control'].includes(activeMode);$('score-label0').textContent=['boss','boss-control'].includes(activeMode)?'보스':'왼쪽';$('score-label1').textContent=['boss','boss-control'].includes(activeMode)?'도전자 팀':'오른쪽';$('battle-mode').textContent=activeMode==='group'?'GROUP 3V3':activeMode==='relay'?'RELAY':activeMode==='boss-control'?'CONTROL BOSS':activeMode==='boss'?'BOSS RAID':activeMode==='control'?'CONTROL':'DUEL';$('relay-hud').hidden=!['relay','group'].includes(activeMode);",
'hud active mode')

# Fix the "both" option persistence regression found during inspection.
once(
"$('setting-start-position').onchange=()=>{settings.startPosition=$('setting-start-position').value==='bottom'?'bottom':'top';saveSettings();applyStartButtonPosition()};",
"$('setting-start-position').onchange=()=>{const v=$('setting-start-position').value;settings.startPosition=['top','bottom','both'].includes(v)?v:'top';saveSettings();applyStartButtonPosition()};",
'start-position both persistence')

p.write_text(s,encoding='utf-8')
print('v3.76 mode routing hardening applied')
