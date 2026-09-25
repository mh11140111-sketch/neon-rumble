from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if s.count(old)<count:
        raise SystemExit(f'PATCH FAILED: {label}')
    s=s.replace(old,new,count)

# version + notes
rep('BATTLE <b>v3.23</b>','BATTLE <b>v3.24</b>','version')
rep('📒 패치노트 · v3.23','📒 패치노트 · v3.24','notes summary')
anchor='<div class="patch-body"><div class="patch-version"><h3>v3.23 · 밸런스 & 로봇 회전팔</h3>'
insert='<div class="patch-body"><div class="patch-version"><h3>v3.24 · 스테이지 모드 테스트 & 밸런스</h3><ul><li>로봇은 독·맹독에 걸리지 않음.</li><li>거미 포식(포획) 재사용 대기시간 5초 → 8초.</li><li>스테이지 모드 테스트 추가. 주인공은 로봇이며 직접 조작.</li><li>STAGE 1: 빌런 때문에 적이 된 나무 처치.</li><li>STAGE 2: 빌런의 이상한 폭탄으로 보스화된 로봇을 직접 조작해 5명의 적을 처치.</li><li>STAGE 3: 체력과 공격력이 1.5배인 빌런을 혼자 처치.</li></ul></div><div class="patch-version"><h3>v3.23 · 밸런스 & 로봇 회전팔</h3>'
rep(anchor,insert,'v324 notes')

# stage styling
stage_css='''<style id="stage-mode-style">\n.stage-entry{width:100%;margin:18px 0 8px;background:#18263a;border:1px solid #5e7695;font-weight:800}.stage-panel{margin:18px 0;padding:18px;border:1px solid #40536d;border-radius:16px;background:#101b2b}.stage-panel h2{margin:0 0 6px;font-size:22px}.stage-panel>p{margin:0 0 16px;color:#9fb2ca;font-size:13px;line-height:1.7}.stage-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px}.stage-card{text-align:left;min-height:132px;display:flex;flex-direction:column;align-items:flex-start;gap:7px;padding:14px}.stage-card strong{font-size:16px}.stage-card span{font-size:26px}.stage-card small{color:#aebfd4;line-height:1.5}.stage-card b{color:#b8f279;font-size:12px}@media(max-width:560px){.stage-grid{grid-template-columns:1fr}.stage-card{min-height:100px}}\n</style>\n'''
rep('</head><body><main>',stage_css+'</head><body><main>','stage css')

# stage entry lives where the old start button used to be: under match info.
old='''<div class="match-info"><p><span class="cyan" id="detail-label0">왼쪽</span> <span id="detail0"></span></p><p><span class="orange" id="detail-label1">오른쪽</span> <span id="detail1"></span></p></div>\n<p class="hint">일반 모드는 직접 조작 없는 자동 전투 · 조정 모드에서만 왼쪽 캐릭터 이동 가능 · 체력 0이 되면 패배.</p></section>'''
new='''<div class="match-info"><p><span class="cyan" id="detail-label0">왼쪽</span> <span id="detail0"></span></p><p><span class="orange" id="detail-label1">오른쪽</span> <span id="detail1"></span></p></div>\n<button id="stage-entry" class="stage-entry" type="button">🧪 스테이지 모드 · 테스트버전</button>\n<div id="stage-panel" class="stage-panel" hidden><p class="eyebrow">STAGE MODE · TEST</p><h2>🤖 로봇의 스테이지</h2><p>주인공은 로봇이야. 모든 스테이지에서 엄지스틱으로 직접 이동해. 현재 테스트 스테이지는 3개이며 추후 추가 예정.</p><div class="stage-grid"><button class="stage-card" id="stage-1" type="button"><b>STAGE 1</b><span>🤖 VS 🌳</span><strong>조종당한 나무</strong><small>빌런 때문에 적이 된 나무를 쓰러트려.</small></button><button class="stage-card" id="stage-2" type="button"><b>STAGE 2</b><span>👑🤖 VS 5</span><strong>이상한 폭탄</strong><small>보스화된 로봇을 직접 조작해 5명의 적을 쓰러트려.</small></button><button class="stage-card" id="stage-3" type="button"><b>STAGE 3</b><span>🤖 VS 🦹‍♂️</span><strong>강화된 빌런</strong><small>HP와 공격력이 1.5배가 된 빌런을 혼자 쓰러트려.</small></button></div></div>\n<p class="hint">일반 모드는 직접 조작 없는 자동 전투 · 조정 모드에서만 왼쪽 캐릭터 이동 가능 · 체력 0이 되면 패배.</p></section>'''
rep(old,new,'stage html')

# Robot poison/toxin immunity
rep("if(e.id==='moai'||f.team===e.team||e.health<=0||this.isStudying(e))return;\n const damage=5*f.scale", "if(e.id==='moai'||e.id==='robot'||f.team===e.team||e.health<=0||this.isStudying(e))return;\n const damage=5*f.scale", 'robot poison immunity')
rep("if(e.id==='moai'||f.team===e.team||e.health<=0||this.isStudying(e))return;const damage=10*f.scale", "if(e.id==='moai'||e.id==='robot'||f.team===e.team||e.health<=0||this.isStudying(e))return;const damage=10*f.scale", 'robot toxin immunity')
rep("if(e.id==='moai'){e.toxin=null;return}", "if(e.id==='moai'||e.id==='robot'){e.toxin=null;return}", 'robot toxin clear')
rep("if(e.id==='moai'){e.poison=null;return}", "if(e.id==='moai'||e.id==='robot'){e.poison=null;return}", 'robot poison clear')

# Spider capture/feast cooldown 8 sec
rep('nextCapture:5/scale','nextCapture:8/scale','spider initial cooldown')
rep('f.nextCapture=this.time+5/f.scale','f.nextCapture=this.time+8/f.scale','spider repeat cooldown')
rep("detail:'포획 5초마다", "detail:'포획 8초마다", 'spider detail')
rep("description:'벽에 닿아 실을 걸고 다른 벽에 닿으면 두 지점 사이에 거미줄을 설치해. 거미줄에 닿은 적은 40% 감속 및 0.5초마다 30 피해. 몸에 닿으면 즉시 중독돼. 5초마다 적을 포획해 돌진하고,", "description:'벽에 닿아 실을 걸고 다른 벽에 닿으면 두 지점 사이에 거미줄을 설치해. 거미줄에 닿은 적은 40% 감속 및 0.5초마다 30 피해. 몸에 닿으면 즉시 중독돼. 8초마다 적을 포획해 돌진하고,", 'spider description')

# Villain stage power multiplier for stage 3 damaging bombs only.
rep("this.bombShot(f,e,dynamite?'🧨':'💣',(dynamite?70:50)*f.scale,false)", "this.bombShot(f,e,dynamite?'🧨':'💣',(dynamite?70:50)*f.scale*(f.stagePower||1),false)", 'villain stage power')

# Allow stage-controlled team 0 without changing engine's boss rules.
rep("const manual=this.mode==='control'&&f.team===0;", "const manual=(this.mode==='control'||this.manualTeam0)&&f.team===0;", 'manual stage flag')

# UI state additions + stage control support.
rep("lastHits=0,lastMessage='';const canvas", "lastHits=0,lastMessage='',stageNo=1;const canvas", 'stage state')
rep("if(mode!=='control'||!stick||stick.hidden)return;", "if(!['control','stage'].includes(mode)||!stick||stick.hidden)return;", 'stick move stage')
rep("stick.addEventListener('pointerdown',e=>{if(mode!=='control')return;", "stick.addEventListener('pointerdown',e=>{if(!['control','stage'].includes(mode))return;", 'stick down stage')

# Add stage UI toggling before currentChoices.
needle="function currentChoices(){return mode==='boss'?[bossChoice,squad[Math.max(0,bossSlot)]]:['relay','group'].includes(mode)?relayTeams.map((t,i)=>t[relaySlots[i]]):selected}"
replacement="""function updateStageUI(){const on=mode==='stage';document.querySelector('.section-title').hidden=on;document.querySelector('.versus').hidden=on;$('start').hidden=on;document.querySelector('.pick-heading').hidden=on;$('character-search').hidden=on;$('roster').hidden=on;document.querySelector('.match-info').hidden=on;$('stage-entry').hidden=on;$('stage-panel').hidden=!on;if(on){$('relay-rules').hidden=true;$('relay-picker').hidden=true;$('squad-picker').hidden=true;$('boss-rules').hidden=true}$('mode-duel').setAttribute('aria-pressed',String(mode==='duel'));$('mode-boss').setAttribute('aria-pressed',String(mode==='boss'));$('mode-relay').setAttribute('aria-pressed',String(mode==='relay'));$('mode-group').setAttribute('aria-pressed',String(mode==='group'));$('mode-control').setAttribute('aria-pressed',String(mode==='control'))}\nfunction currentChoices(){return mode==='boss'?[bossChoice,squad[Math.max(0,bossSlot)]]:['relay','group'].includes(mode)?relayTeams.map((t,i)=>t[relaySlots[i]]):selected}"""
rep(needle,replacement,'stage ui function')

# Ensure normal UI comes back before regular update logic, then stage hiding occurs last.
rep("function updateSelection(){\n const choices=currentChoices()", "function updateSelection(){\n const stageWas=mode==='stage';if(!stageWas){document.querySelector('.section-title').hidden=false;document.querySelector('.versus').hidden=false;$('start').hidden=false;document.querySelector('.pick-heading').hidden=false;$('character-search').hidden=false;$('roster').hidden=false;document.querySelector('.match-info').hidden=false;$('stage-entry').hidden=false}\n const choices=currentChoices()", 'update selection restore')
rep("$('start').textContent=mode==='group'?'단체전 시작 · 3 vs 3 동시전투':mode==='relay'?'릴레이 전투 시작 · 팀당 3명':mode==='boss'?'보스전 시작 · 1 vs 5':mode==='control'?'조정 모드 시작 · 왼쪽 직접 이동':'이 조합으로 전투 시작';\n}", "$('start').textContent=mode==='group'?'단체전 시작 · 3 vs 3 동시전투':mode==='relay'?'릴레이 전투 시작 · 팀당 3명':mode==='boss'?'보스전 시작 · 1 vs 5':mode==='control'?'조정 모드 시작 · 왼쪽 직접 이동':'이 조합으로 전투 시작';updateStageUI();\n}", 'update stage ui call')

# Stage entry/button handlers and runtime builder.
handlers="""$('mode-relay').onclick=()=>{mode='relay';side=0;updateSelection()};$('mode-group').onclick=()=>{mode='group';side=0;updateSelection()};$('mode-control').onclick=()=>{mode='control';side=0;bossSlot=-1;updateSelection()};"""
handlers_new=handlers+"""\n$('stage-entry').onclick=()=>{mode='stage';stageNo=1;updateSelection();window.scrollTo({top:0,behavior:'auto'})};\n$('stage-1').onclick=()=>startStage(1);$('stage-2').onclick=()=>startStage(2);$('stage-3').onclick=()=>startStage(3);"""
rep(handlers,handlers_new,'stage handlers')

# Insert startStage before normal start().
start_marker="function start(){engine=mode==='group'?"
stage_func="""function startStage(n){stageNo=n;mode='stage';if(n===1){engine=new Engine('robot','tree',Math.random,{mode:'control'})}else if(n===2){engine=new Engine('robot','boxer',Math.random,{mode:'boss',allies:['boxer','archer','knight','mage','vampire']});engine.manualTeam0=true}else{engine=new Engine('robot','villain',Math.random,{mode:'control'});const v=engine.fighters.find(f=>f.id==='villain'&&f.team===1);if(v){v.hp*=1.5;v.health=v.hp;v.damage*=1.5;v.stagePower=1.5}}paused=false;acc=0;last=performance.now();lastHits=0;lastMessage='';$('selection').hidden=true;$('battle').hidden=false;$('result').hidden=true;$('pause-label').hidden=true;$('pause').disabled=false;$('pause').textContent='일시정지';$('control-stick').hidden=false;$('control-label').hidden=false;$('control-label').textContent=n===2?'보스 로봇 이동':'로봇 이동';resetStick();$('squad-hud').hidden=true;$('relay-hud').hidden=true;$('score-label0').textContent=n===2?'👑 보스 로봇':'🤖 로봇';$('score-label1').textContent=n===1?'조종당한 나무':n===2?'적 5명':'강화 빌런';$('battle-mode').textContent='STAGE '+n;const story=n===1?'STAGE 1 · 빌런 때문에 적이 된 나무를 쓰러트려!':n===2?'STAGE 2 · 빌런의 이상한 폭탄! 보스화된 로봇으로 5명을 쓰러트려!':'STAGE 3 · HP와 공격력이 1.5배가 된 빌런을 쓰러트려!';$('event').textContent=story;$('battle-info').textContent=story;fit();hud();draw();window.scrollTo({top:0,behavior:'auto'});tone(650)}\n"""
rep(start_marker,stage_func+start_marker,'startStage insertion')

# Rematch stage correctly.
rep("$('start').onclick=start;$('rematch').onclick=start;", "$('start').onclick=start;$('rematch').onclick=()=>mode==='stage'?startStage(stageNo):start();", 'stage rematch')

# Player input in stage loop.
rep("if(mode==='control'){engine.controlX=stickX;engine.controlY=stickY}else", "if(mode==='control'||mode==='stage'){engine.controlX=stickX;engine.controlY=stickY}else", 'stage control loop')

# Stage arena title.
rep("ctx.fillText(mode==='group'?'GROUP BATTLE · 3 VS 3':mode==='relay'?'RELAY · 3 VS 3':mode==='boss'?'BOSS RAID · 1 VS 5':'NEON ARENA · 1 VS 1',360,44);", "ctx.fillText(mode==='stage'?'STAGE '+stageNo:mode==='group'?'GROUP BATTLE · 3 VS 3':mode==='relay'?'RELAY · 3 VS 3':mode==='boss'?'BOSS RAID · 1 VS 5':'NEON ARENA · 1 VS 1',360,44);", 'stage arena title')

# Stage loss returns to stage selection; stage clear has its own result text.
old_result="""if(engine.result!==null&&$('result').hidden){const winners=engine.fighters.filter(f=>f.team===engine.result),f=winners[0],survivors=winners.filter(f=>f.health>0);$('winner-icon').textContent=mode==='boss'?(engine.result===0?'👑':'🏆'):f.icon;$('winner').textContent=mode==='group'?(engine.result?'오른쪽':'왼쪽')+' 팀 단체전 승리!':mode==='relay'?(engine.result?'오른쪽':'왼쪽')+' 팀 릴레이 승리!':mode==='boss'?(engine.result===0?'보스 '+f.name+' 승리!':'도전자 팀 승리!'):(f.team?'오른쪽':'왼쪽')+' '+f.name+' 승리!';$('summary').textContent=t+'초의 전투 · 생존 '+survivors.length+'명 · 남은 체력 '+Math.ceil(survivors.reduce((n,f)=>n+f.health,0))+' HP';$('result').hidden=false;$('pause').disabled=true;tone(760)}"""
new_result="""if(engine.result!==null&&$('result').hidden){if(mode==='stage'&&engine.result!==0){selection();return}const winners=engine.fighters.filter(f=>f.team===engine.result),f=winners[0],survivors=winners.filter(f=>f.health>0);if(mode==='stage'){$('winner-icon').textContent='🏁';$('winner').textContent='STAGE '+stageNo+' 클리어!';$('summary').textContent=t+'초 · 로봇 생존 · 다음 스테이지도 테스트해 봐.'}else{$('winner-icon').textContent=mode==='boss'?(engine.result===0?'👑':'🏆'):f.icon;$('winner').textContent=mode==='group'?(engine.result?'오른쪽':'왼쪽')+' 팀 단체전 승리!':mode==='relay'?(engine.result?'오른쪽':'왼쪽')+' 팀 릴레이 승리!':mode==='boss'?(engine.result===0?'보스 '+f.name+' 승리!':'도전자 팀 승리!'):(f.team?'오른쪽':'왼쪽')+' '+f.name+' 승리!';$('summary').textContent=t+'초의 전투 · 생존 '+survivors.length+'명 · 남은 체력 '+Math.ceil(survivors.reduce((n,f)=>n+f.health,0))+' HP'}$('result').hidden=false;$('pause').disabled=true;tone(760)}"""
rep(old_result,new_result,'stage result handling')

p.write_text(s,encoding='utf-8')
print('NEON RUMBLE v3.24 applied')
