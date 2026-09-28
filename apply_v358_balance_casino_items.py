from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

# Version badge + patch note
old='<span class="badge">BATTLE <b>v3.57</b></span>'
new='<span class="badge">BATTLE <b>v3.58</b></span>'
assert old in s, 'version badge anchor missing'
s=s.replace(old,new,1)

old='<details class="patch-notes"><summary>📒 패치노트 · v3.57</summary><div class="patch-body"><div class="patch-version"><h3>v3.57 · 여의주의 신통력</h3>'
new='<details class="patch-notes"><summary>📒 패치노트 · v3.58</summary><div class="patch-body"><div class="patch-version"><h3>v3.58 · 밸런스 & 도박장 꾸미기 확장</h3><ul><li>🐉 용: 비의 분노 빗방울 피해 10 → 5.</li><li>🎰 도박장 꾸미기 보상에 🍀 ⭐️ 🥇 🥈 🥉 5종 추가.</li><li>신규 5종도 기존 도박장 꾸미기와 동일하게 중복 획득 시 250코인으로 교환.</li></ul></div><div class="patch-version"><h3>v3.57 · 여의주의 신통력</h3>'
assert old in s, 'patch note anchor missing'
s=s.replace(old,new,1)

# Dragon rain damage
old="kind:'dragon_rain',icon:'💧',radius:8*f.scale,speed:520*f.scale,damage:10*f.scale,life:2.2"
new="kind:'dragon_rain',icon:'💧',radius:8*f.scale,speed:520*f.scale,damage:5*f.scale,life:2.2"
assert old in s, 'dragon rain damage anchor missing'
s=s.replace(old,new,1)

# Casino-only cosmetic definitions
old=" {id:'casino_wheelchair',name:'미니 휠체어',icon:'🦽',price:0,type:'accessory',casinoOnly:true,exclusiveFor:null,desc:'도박장에서만 획득 가능한 휠체어 장식'},"
new=old+"\n {id:'casino_clover',name:'행운의 클로버',icon:'🍀',price:0,type:'accessory',casinoOnly:true,exclusiveFor:null,desc:'도박장에서만 획득 가능한 행운의 클로버 장식'},\n {id:'casino_star',name:'행운의 별',icon:'⭐️',price:0,type:'accessory',casinoOnly:true,exclusiveFor:null,desc:'도박장에서만 획득 가능한 별 장식'},\n {id:'casino_gold_medal',name:'금메달',icon:'🥇',price:0,type:'accessory',casinoOnly:true,exclusiveFor:null,desc:'도박장에서만 획득 가능한 금메달 장식'},\n {id:'casino_silver_medal',name:'은메달',icon:'🥈',price:0,type:'accessory',casinoOnly:true,exclusiveFor:null,desc:'도박장에서만 획득 가능한 은메달 장식'},\n {id:'casino_bronze_medal',name:'동메달',icon:'🥉',price:0,type:'accessory',casinoOnly:true,exclusiveFor:null,desc:'도박장에서만 획득 가능한 동메달 장식'},"
assert old in s, 'casino cosmetic definition anchor missing'
s=s.replace(old,new,1)

# Casino reward pool
old="const CASINO_COSMETIC_IDS=['casino_ribbon_hat','casino_coin_charm','casino_goggles','casino_splash','casino_scooter','casino_wheelchair'];"
new="const CASINO_COSMETIC_IDS=['casino_ribbon_hat','casino_coin_charm','casino_goggles','casino_splash','casino_scooter','casino_wheelchair','casino_clover','casino_star','casino_gold_medal','casino_silver_medal','casino_bronze_medal'];"
assert old in s, 'casino cosmetic ids anchor missing'
s=s.replace(old,new,1)

# Reel animation icons only; reward odds stay unchanged.
old="const pool=['🎰','👒','🪙','🥽','🫟','🛴','🦽','🤑','💎','❌'];"
new="const pool=['🎰','👒','🪙','🥽','🫟','🛴','🦽','🍀','⭐️','🥇','🥈','🥉','🤑','💎','❌'];"
assert old in s, 'casino reel visual pool anchor missing'
s=s.replace(old,new,1)

# Safety checks
assert 'BATTLE <b>v3.58</b>' in s
assert "damage:5*f.scale" in s
for marker in ['casino_clover','casino_star','casino_gold_medal','casino_silver_medal','casino_bronze_medal']:
    assert marker in s, marker

p.write_text(s,encoding='utf-8')
print('v3.58 patch applied')
