from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,count=1):
    global s
    n=s.count(old)
    if n < count:
        raise SystemExit(f'replace mismatch expected >= {count}, found {n}: {old[:180]!r}')
    s=s.replace(old,new,count)

# Version + patch notes.
rep('BATTLE <b>v3.41</b>','BATTLE <b>v3.42</b>')
rep('<summary>📒 패치노트 · v3.41</summary><div class="patch-body">',
    '<summary>📒 패치노트 · v3.42</summary><div class="patch-body"><div class="patch-version"><h3>v3.42 · 머니맨 밸런스 & 상점 확장</h3><ul><li>밸런스: 🤑 머니맨 HP 1000 → 650.</li><li>밸런스: 돈의 행복 중첩 유지/감소 주기 5초 → 3초. 최대 5중첩과 중첩당 상대 피해 −10은 유지.</li><li>신규 아우라 🌈 무지개 아우라 추가. 가격 130코인.</li><li>신규 장신구 🎩 마술모자 추가. 가격 30코인.</li></ul></div>')

# Money Man HP 1000 -> 650 and status duration 5s -> 3s.
rep("{id:'moneyman',name:'머니맨',icon:'🤑',tag:'돈가방 · 나는 돈 · 돈의 행복',hp:1000,damage:20,speed:155,cooldown:1.5,unlock:'moneyManShop',description:'💰 돈가방을 던져 피해 20과 돈의 행복 2중첩을 주고 적중 지점에서 💵 돈을 8방향으로 뿌려. 5초마다 느린 💸 나는 돈을 던지며, 돈의 행복 중첩이 많을수록 더 강해져.',detail:'HP 1000 · 💰 돈가방 20 / 1.5초 · 적중 시 💵 8방향 각 50 · 💸 5초마다 100 + 돈의 행복 중첩당 10 · 돈의 행복 최대 5중첩 · 중첩당 상대 피해 −10 · 5초마다 1중첩 감소'},",
    "{id:'moneyman',name:'머니맨',icon:'🤑',tag:'돈가방 · 나는 돈 · 돈의 행복',hp:650,damage:20,speed:155,cooldown:1.5,unlock:'moneyManShop',description:'💰 돈가방을 던져 피해 20과 돈의 행복 2중첩을 주고 적중 지점에서 💵 돈을 8방향으로 뿌려. 5초마다 느린 💸 나는 돈을 던지며, 돈의 행복 중첩이 많을수록 더 강해져.',detail:'HP 650 · 💰 돈가방 20 / 1.5초 · 적중 시 💵 8방향 각 50 · 💸 5초마다 100 + 돈의 행복 중첩당 10 · 돈의 행복 최대 5중첩 · 중첩당 상대 피해 −10 · 3초마다 1중첩 감소'},")
rep("applyMoneyHappiness(e,amount){if(!e||e.health<=0)return;const before=e.moneyHappiness||0;e.moneyHappiness=Math.min(5,before+amount);if(before<=0||!Number.isFinite(e.moneyHappyNext))e.moneyHappyNext=this.time+5;this.effect(e,'💰 돈의 행복 '+e.moneyHappiness+'중첩','skill')}",
    "applyMoneyHappiness(e,amount){if(!e||e.health<=0)return;const before=e.moneyHappiness||0;e.moneyHappiness=Math.min(5,before+amount);if(before<=0||!Number.isFinite(e.moneyHappyNext))e.moneyHappyNext=this.time+3;this.effect(e,'💰 돈의 행복 '+e.moneyHappiness+'중첩','skill')}")
rep("tickMoneyHappiness(e){if(!e)return;if(e.health<=0){e.moneyHappiness=0;e.moneyHappyNext=0;return}if(!(e.moneyHappiness>0))return;if(!Number.isFinite(e.moneyHappyNext)||e.moneyHappyNext<=0)e.moneyHappyNext=this.time+5;while(e.moneyHappiness>0&&this.time>=e.moneyHappyNext-1e-9){e.moneyHappiness--;e.moneyHappyNext+=5;if(e.moneyHappiness>0)this.effect(e,'💰 행복 '+e.moneyHappiness+'중첩','skill');else{e.moneyHappyNext=0;this.effect(e,'💰 돈의 행복 종료','skill')}}}",
    "tickMoneyHappiness(e){if(!e)return;if(e.health<=0){e.moneyHappiness=0;e.moneyHappyNext=0;return}if(!(e.moneyHappiness>0))return;if(!Number.isFinite(e.moneyHappyNext)||e.moneyHappyNext<=0)e.moneyHappyNext=this.time+3;while(e.moneyHappiness>0&&this.time>=e.moneyHappyNext-1e-9){e.moneyHappiness--;e.moneyHappyNext+=3;if(e.moneyHappiness>0)this.effect(e,'💰 행복 '+e.moneyHappiness+'중첩','skill');else{e.moneyHappyNext=0;this.effect(e,'💰 돈의 행복 종료','skill')}}}")

# New shop items.
rep(" {id:'gold_crown',name:'황금 왕관',icon:'👑',price:70,type:'accessory',exclusiveFor:null,desc:'모든 캐릭터가 장착 가능'},",
    " {id:'gold_crown',name:'황금 왕관',icon:'👑',price:70,type:'accessory',exclusiveFor:null,desc:'모든 캐릭터가 장착 가능'},\n {id:'magic_hat',name:'마술모자',icon:'🎩',price:30,type:'accessory',exclusiveFor:null,desc:'모든 캐릭터가 장착 가능한 마술모자'},")
rep(" {id:'aura_space',name:'우주 아우라',icon:'🌌',price:120,type:'aura',auraStyle:'space',exclusiveFor:null,desc:'별빛과 우주 에너지가 회전하는 희귀 아우라'}",
    " {id:'aura_space',name:'우주 아우라',icon:'🌌',price:120,type:'aura',auraStyle:'space',exclusiveFor:null,desc:'별빛과 우주 에너지가 회전하는 희귀 아우라'},\n {id:'aura_rainbow',name:'무지개 아우라',icon:'🌈',price:130,type:'aura',auraStyle:'rainbow',exclusiveFor:null,desc:'무지개빛 에너지가 계속 색을 바꾸며 회전하는 아우라'}")

# Rainbow aura renderer.
needle="""ctx.globalAlpha=.9;ctx.strokeStyle='#9b72ff';ctx.lineWidth=4*f.scale;ctx.shadowColor='#79dfff';ctx.shadowBlur=22;ctx.beginPath();ctx.arc(0,0,r*.93,0,Math.PI*2);ctx.stroke()}else{const col=item.auraStyle==='red'?'#ff384d':item.auraStyle==='green'?'#65ff71':'#b45cff',light=item.auraStyle==='red'?'#ff9a72':item.auraStyle==='green'?'#b9ff8b':'#e2a4ff';"""
replace="""ctx.globalAlpha=.9;ctx.strokeStyle='#9b72ff';ctx.lineWidth=4*f.scale;ctx.shadowColor='#79dfff';ctx.shadowBlur=22;ctx.beginPath();ctx.arc(0,0,r*.93,0,Math.PI*2);ctx.stroke()}else if(item.auraStyle==='rainbow'){ctx.shadowBlur=24;for(let k=0;k<6;k++){const hue=(t*95+k*60)%360;ctx.globalAlpha=.26;ctx.strokeStyle='hsl('+hue+' 95% 65%)';ctx.shadowColor='hsl('+hue+' 100% 60%)';ctx.lineWidth=7*f.scale;ctx.beginPath();ctx.arc(0,0,r*(.78+k*.065),t*.45+k*Math.PI/3,t*.45+k*Math.PI/3+1.65);ctx.stroke()}for(let i=0;i<12;i++){const a=t*.5+i*Math.PI/6,rr=r*(.82+.13*Math.sin(t*3+i));ctx.globalAlpha=.42;ctx.fillStyle='hsl('+((t*110+i*30)%360)+' 100% 70%)';ctx.beginPath();ctx.arc(Math.cos(a)*rr,Math.sin(a)*rr,3*f.scale,0,Math.PI*2);ctx.fill()}}else{const col=item.auraStyle==='red'?'#ff384d':item.auraStyle==='green'?'#65ff71':'#b45cff',light=item.auraStyle==='red'?'#ff9a72':item.auraStyle==='green'?'#b9ff8b':'#e2a4ff';"""
rep(needle,replace)

p.write_text(s,encoding='utf-8')
print('Applied NEON RUMBLE v3.42 Money Man balance + rainbow aura + magic hat')
