from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s

def rep(old,new,label,count=1):
    global s
    if old not in s:
        raise SystemExit(label+' anchor missing')
    s=s.replace(old,new,count)

rep('BATTLE <b>v3.57</b>','BATTLE <b>v3.58</b>','version')
rep('📒 패치노트 · v3.57','📒 패치노트 · v3.58','patch title')
marker='<div class="patch-body">'
patch='''<div class="patch-version"><h3>v3.58 · 용 밸런스 & 슬롯 아이템 추가</h3><ul><li>🐉 비의 분노: 빗방울 피해 10 → 5. 번개 피해 150과 5% 발생 확률은 그대로.</li><li>🎰 슬롯머신 일반 이모티콘 뽑기 풀에 🍀 ⭐️ 🥇 🥈 🥉 추가.</li><li>🎰 기존 뽑기 확률 5% 7 / 15% 🪙 / 30% 🍇 / 50% 이모티콘은 그대로 유지.</li></ul></div>'''
if patch not in s:
    rep(marker,marker+patch,'patch note')

rep("kind:'dragon_rain',icon:'💧',radius:8*f.scale,speed:520*f.scale,damage:10*f.scale","kind:'dragon_rain',icon:'💧',radius:8*f.scale,speed:520*f.scale,damage:5*f.scale",'dragon rain damage')

old="else{const emojiPool=[...new Set(ROSTER.map(c=>c.icon).filter(Boolean))];for(let i=0;i<3;i++)f.slotQueue.push({fireAt:this.time+i*.12/f.scale,kind:'slotemoji',icon:emojiPool[Math.floor(this.random()*emojiPool.length)]||'🎲',damage:Math.floor(this.rand(25,31)),speed:normalSpeed,spread:.06});this.effect(f,'🎰 이모티콘!','skill')}"
new="else{const emojiPool=[...new Set([...ROSTER.map(c=>c.icon).filter(Boolean),'🍀','⭐️','🥇','🥈','🥉'])];for(let i=0;i<3;i++)f.slotQueue.push({fireAt:this.time+i*.12/f.scale,kind:'slotemoji',icon:emojiPool[Math.floor(this.random()*emojiPool.length)]||'🎲',damage:Math.floor(this.rand(25,31)),speed:normalSpeed,spread:.06});this.effect(f,'🎰 이모티콘!','skill')}"
rep(old,new,'slot emoji pool')

required=['BATTLE <b>v3.58</b>',"damage:5*f.scale","'🍀','⭐️','🥇','🥈','🥉'","if(r<.05)","else if(r<.20)","else if(r<.50)"]
for x in required:
    if x not in s: raise SystemExit('missing marker '+x)
if s==orig: raise SystemExit('no changes')
p.write_text(s,encoding='utf-8')
print('v3.58 patch applied')
