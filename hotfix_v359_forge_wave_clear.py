from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="function resetForgeTransient(){forgeStageNo=1;forgeWave=0;if(engine)engine.forgeMode=false}"
new="function resetForgeTransient(){forgeStageNo=1;forgeWave=0;if(engine){engine.forgeMode=false;engine.desertWaveMode=false}}"
if old not in s: raise SystemExit('reset anchor missing')
s=s.replace(old,new,1)
old="}engine.forgeMode=true;paused=false;acc=0;last=performance.now();"
new="}engine.forgeMode=true;engine.desertWaveMode=true;paused=false;acc=0;last=performance.now();"
if old not in s: raise SystemExit('start anchor missing')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('patched v3.59 forge wave clear')
