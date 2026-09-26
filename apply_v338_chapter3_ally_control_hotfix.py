from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n < count:
        raise SystemExit(f'replace mismatch expected >= {count}, found {n}: {old[:180]!r}')
    s=s.replace(old,new,count)

# In Chapter 3, only the main Vampire is player-controlled.
# The female Vampire must remain an autonomous ally.
rep("const manual=(this.mode==='control'||this.manualTeam0)&&f.team===0,heroAuto=f.id==='hero'&&f.heroReady;",
    "const manual=(this.mode==='control'||this.manualTeam0)&&f.team===0&&!(this.mansionMode&&f.summon),heroAuto=f.id==='hero'&&f.heroReady;")

# Mark Chapter 3 engines so summon/allied team-0 fighters are not tied to the control stick.
rep("engine.desertWaveMode=true;paused=false;acc=0;last=performance.now();lastHits=0;lastMessage='';$('selection').hidden=true;$('battle').hidden=false;$('result').hidden=true;$('pause-label').hidden=true;$('pause').disabled=false;$('pause').textContent='일시정지';resetStick();refreshControlUI();$('squad-hud').hidden=true;$('relay-hud').hidden=true;$('score-label0').textContent=n<3?'🧛 흡혈귀 + 🧛‍♀️':'🧛 흡혈귀';",
    "engine.desertWaveMode=true;engine.mansionMode=true;paused=false;acc=0;last=performance.now();lastHits=0;lastMessage='';$('selection').hidden=true;$('battle').hidden=false;$('result').hidden=true;$('pause-label').hidden=true;$('pause').disabled=false;$('pause').textContent='일시정지';resetStick();refreshControlUI();$('squad-hud').hidden=true;$('relay-hud').hidden=true;$('score-label0').textContent=n<3?'🧛 흡혈귀 + 🧛‍♀️':'🧛 흡혈귀';")

p.write_text(s,encoding='utf-8')
print('v3.38 Chapter 3 ally-control hotfix applied')
