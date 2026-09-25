from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

old="kind:'giantslash',radius:24*f.scale,speed:430*f.scale,damage:150*f.scale,life:2.2,bounces:0"
new="kind:'giantslash',radius:24*f.scale,speed:430*f.scale,damage:150*f.scale,life:2.2,bounces:0,fxBorn:this.time"
if old not in s:
    raise SystemExit('giantslash projectile pattern not found')
s=s.replace(old,new,1)

old="if(s.kind==='magic'){e.slow=Math.max(e.slow,1.2*f.scale);e.slowPower=Math.max(e.slowPower,f.magicSlowStrength)}}"
new="if(s.kind==='giantslash'&&typeof triggerGiantSlashShake==='function')triggerGiantSlashShake();if(s.kind==='magic'){e.slow=Math.max(e.slow,1.2*f.scale);e.slowPower=Math.max(e.slowPower,f.magicSlowStrength)}}"
if old not in s:
    raise SystemExit('attackProjectile tail pattern not found')
s=s.replace(old,new,1)

old="else if(s.kind==='taser'){ctx.strokeStyle='#ffe66d';"
new="else if(s.kind==='giantslash'){const age=Math.max(0,engine.time-(s.fxBorn??engine.time)),flash=Math.max(.38,1-age/.35);ctx.save();ctx.globalAlpha=flash;ctx.lineCap='round';ctx.shadowColor='#dff7ff';ctx.shadowBlur=24;ctx.strokeStyle='#fff7c2';ctx.lineWidth=12*s.radius/24;ctx.beginPath();ctx.arc(0,0,42*s.radius/24,-1.05,1.05);ctx.stroke();ctx.shadowBlur=12;ctx.strokeStyle='#bdefff';ctx.lineWidth=7*s.radius/24;ctx.beginPath();ctx.arc(-10*s.radius/24,0,55*s.radius/24,-.95,.95);ctx.stroke();ctx.globalAlpha=flash*.45;ctx.strokeStyle='#f4cf67';ctx.lineWidth=4*s.radius/24;ctx.beginPath();ctx.arc(-22*s.radius/24,0,68*s.radius/24,-.82,.82);ctx.stroke();ctx.restore()}else if(s.kind==='taser'){ctx.strokeStyle='#ffe66d';"
if old not in s:
    raise SystemExit('projectile draw insertion point not found')
s=s.replace(old,new,1)

old="function loop(now){const dt=Math.max(0,Math.min((now-last)/1000,.08));"
new="let giantSlashShakeTimer=null;function triggerGiantSlashShake(){if(!canvas)return;const seq=[[-7,2],[6,-3],[-5,-2],[4,2],[0,0]];let i=0;if(giantSlashShakeTimer)clearInterval(giantSlashShakeTimer);giantSlashShakeTimer=setInterval(()=>{const [x,y]=seq[i++]||[0,0];canvas.style.transform=`translate(${x}px,${y}px)`;if(i>=seq.length){clearInterval(giantSlashShakeTimer);giantSlashShakeTimer=null;canvas.style.transform=''}},36)}\nfunction loop(now){const dt=Math.max(0,Math.min((now-last)/1000,.08));"
if old not in s:
    raise SystemExit('loop insertion point not found')
s=s.replace(old,new,1)

p.write_text(s,encoding='utf-8')
print('v3.26 giant slash visual FX hotfix applied')
