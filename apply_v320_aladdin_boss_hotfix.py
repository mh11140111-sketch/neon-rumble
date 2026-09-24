from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="if(mode==='boss'){engine.fighters.slice(1).forEach((f,i)=>{$('hero-name'+i).textContent=(i+1)+'. '+f.icon+' '+f.name;$('hero-hp'+i).textContent=f.health>0?Math.ceil(f.health)+' HP'+(f.burn?' · 화상':f.poison?' · 독':'')+(f.egg?' · 알 '+Math.max(0,Math.ceil(f.eggUntil-engine.time))+'초':'')+(f.stunUntil>engine.time?' · 기절':'')+(f.capturedBy!==null?' · 포획':''):'탈락';$('hero-bar'+i).style.width=(f.health/f.hp*100)+'%';$('hero-status'+i).classList.toggle('defeated',f.health<=0)})}"
new="if(mode==='boss'){engine.fighters.filter(f=>f.team===1&&!f.summon).slice(0,5).forEach((f,i)=>{$('hero-name'+i).textContent=(i+1)+'. '+f.icon+' '+f.name;$('hero-hp'+i).textContent=f.health>0?Math.ceil(f.health)+' HP'+(f.burn?' · 화상':f.poison?' · 독':'')+(f.egg?' · 알 '+Math.max(0,Math.ceil(f.eggUntil-engine.time))+'초':'')+(f.stunUntil>engine.time?' · 기절':'')+(f.capturedBy!==null?' · 포획':''):'탈락';$('hero-bar'+i).style.width=(f.health/f.hp*100)+'%';$('hero-status'+i).classList.toggle('defeated',f.health<=0)})}"
if old not in s: raise SystemExit('PATCH FAILED: boss HUD block not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('v3.20 Aladdin boss HUD hotfix applied')
