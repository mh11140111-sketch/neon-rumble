from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

# 1) CH9 panel must be hidden when any previous chapter/stage selection is opened.
once("function hideStageSelectionPanels(){for(const id of ['stage-panel','desert-panel','mansion-panel','space-panel','casino-panel','ocean-panel','forge-panel','boxing-panel']){const el=$(id);if(el)el.hidden=true}}",
     "function hideStageSelectionPanels(){for(const id of ['stage-panel','desert-panel','mansion-panel','space-panel','casino-panel','ocean-panel','forge-panel','boxing-panel','lab-selection']){const el=$(id);if(el)el.hidden=true}}",
     'hide CH9 panel with old panels')

# updateStageUI is used by all legacy chapter buttons. Always close the dynamically-added CH9 panel there.
once("function updateStageUI(){const on=mode==='stage'",
     "function updateStageUI(){if($('lab-selection'))$('lab-selection').hidden=true;const on=mode==='stage'",
     'close CH9 panel on legacy stage selection')

# 2) Dedicated laboratory battle background.
once("if(wardrobeBg&&!['stage','desert','mansion','space','casino','ocean','forge','boxing'].includes(mode))",
     "if(wardrobeBg&&!['stage','desert','mansion','space','casino','ocean','forge','boxing','lab'].includes(mode))",
     'exclude lab from wardrobe background')

boxing="""else if(mode==='boxing'){const bg=ctx.createLinearGradient(0,0,0,720);bg.addColorStop(0,'#1b2430');bg.addColorStop(.55,'#10151c');bg.addColorStop(1,'#090c11');ctx.fillStyle=bg;ctx.fillRect(0,0,720,720);ctx.save();ctx.globalAlpha=.68;ctx.strokeStyle='#e7e7e7';ctx.lineWidth=5;for(const y of [105,135,165]){ctx.beginPath();ctx.moveTo(55,y);ctx.lineTo(665,y);ctx.stroke();ctx.beginPath();ctx.moveTo(55,720-y);ctx.lineTo(665,720-y);ctx.stroke()}ctx.strokeStyle='#d94c4c';ctx.lineWidth=8;ctx.strokeRect(48,48,624,624);ctx.font='44px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🥊',92,105);ctx.fillText('🥊',628,615);ctx.restore()}else if(mode==='forge')"""
lab="""else if(mode==='boxing'){const bg=ctx.createLinearGradient(0,0,0,720);bg.addColorStop(0,'#1b2430');bg.addColorStop(.55,'#10151c');bg.addColorStop(1,'#090c11');ctx.fillStyle=bg;ctx.fillRect(0,0,720,720);ctx.save();ctx.globalAlpha=.68;ctx.strokeStyle='#e7e7e7';ctx.lineWidth=5;for(const y of [105,135,165]){ctx.beginPath();ctx.moveTo(55,y);ctx.lineTo(665,y);ctx.stroke();ctx.beginPath();ctx.moveTo(55,720-y);ctx.lineTo(665,720-y);ctx.stroke()}ctx.strokeStyle='#d94c4c';ctx.lineWidth=8;ctx.strokeRect(48,48,624,624);ctx.font='44px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🥊',92,105);ctx.fillText('🥊',628,615);ctx.restore()}else if(mode==='lab'){const lg=ctx.createLinearGradient(0,0,0,720);lg.addColorStop(0,'#102b31');lg.addColorStop(.5,'#0a2028');lg.addColorStop(1,'#061219');ctx.fillStyle=lg;ctx.fillRect(0,0,720,720);ctx.save();ctx.globalAlpha=.34;ctx.fillStyle='#7df1e6';for(const x of [86,634]){ctx.fillRect(x-32,92,64,118);ctx.strokeStyle='#b9fff7';ctx.lineWidth=3;ctx.strokeRect(x-32,92,64,118);ctx.beginPath();ctx.arc(x,150,21,0,Math.PI*2);ctx.stroke()}ctx.globalAlpha=.28;ctx.fillStyle='#b6f7ff';ctx.fillRect(245,82,230,52);ctx.strokeStyle='#6cd9e7';ctx.strokeRect(245,82,230,52);ctx.globalAlpha=.5;ctx.font='36px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🧪',94,635);ctx.fillText('🔬',622,625);ctx.fillText('🧬',360,108);ctx.globalAlpha=.18;ctx.strokeStyle='#74d8d0';ctx.lineWidth=4;for(let y=250;y<650;y+=105){ctx.beginPath();ctx.moveTo(55,y);ctx.lineTo(665,y);ctx.stroke()}ctx.restore()}else if(mode==='forge')"""
once(boxing,lab,'laboratory background branch')

once("ctx.strokeStyle=mode==='desert'?'#b87a3c':mode==='mansion'?'#54243f':mode==='space'?'#315a86':mode==='casino'?'#7f5a28':mode==='ocean'?'#1d7896':mode==='forge'?'#8a4b2a':mode==='boxing'?'#7f3940':'#1c2d42';",
     "ctx.strokeStyle=mode==='desert'?'#b87a3c':mode==='mansion'?'#54243f':mode==='space'?'#315a86':mode==='casino'?'#7f5a28':mode==='ocean'?'#1d7896':mode==='forge'?'#8a4b2a':mode==='boxing'?'#7f3940':mode==='lab'?'#2e7778':'#1c2d42';",
     'lab grid color')

once("mode==='boxing'?'BOXING GYM · STAGE '+boxingStageNo:mode==='stage'?'STAGE '+stageNo",
     "mode==='boxing'?'BOXING GYM · STAGE '+boxingStageNo:mode==='lab'?'LABORATORY ESCAPE · STAGE '+labStageNo:mode==='stage'?'STAGE '+stageNo",
     'lab arena label')

p.write_text(s,encoding='utf-8')
print('v3.70 CH9 panel + laboratory background hotfix applied')