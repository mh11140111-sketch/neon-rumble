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
rep('BATTLE <b>v3.40</b>','BATTLE <b>v3.41</b>')
rep('<summary>📒 패치노트 · v3.40</summary><div class="patch-body">',
    '<summary>📒 패치노트 · v3.41</summary><div class="patch-body"><div class="patch-version"><h3>v3.41 · 돈의 폭풍, 머니맨 등장</h3><ul><li>신규 캐릭터 🤑 머니맨 추가. 상점에서 150코인으로 구매해야 캐릭터 선택 화면에서 사용할 수 있음.</li><li>💰 돈가방: 적중 시 피해 20 + 돈의 행복 2중첩, 적중 지점에서 💵 돈을 8방향으로 발사. 💵 피해 50 + 돈의 행복 1중첩.</li><li>💸 나는 돈: 5초마다 느린 투사체를 발사. 기본 피해 100이며 대상의 돈의 행복 1중첩마다 피해 +10.</li><li>돈의 행복: 최대 5중첩. 1중첩당 대상이 주는 피해 10 감소, 5초마다 1중첩 감소.</li></ul></div>')

# Shop copy: characters are now purchasable.
rep('스테이지를 클리어해 모은 코인으로 꾸미기 아이템을 구매할 수 있어.','스테이지를 클리어해 모은 코인으로 장신구·아우라·캐릭터를 구매할 수 있어.')
rep('<div class="shop-coming">🧑‍🤝‍🧑 캐릭터 상품 · 추후 업데이트 예정</div>','<div class="shop-coming">🤑 캐릭터 상품 추가 · 구매한 캐릭터는 선택 화면에서 바로 사용할 수 있어.</div>')

# Add Money Man to the roster after Firefighter.
firefighter="""{id:'firefighter',name:'소방관',icon:'👨‍🚒',tag:'화상 면역 · 소방도끼 · 소방차',hp:1000,damage:70,speed:160,cooldown:.5,description:'화상에 완전히 면역이야. 적이 가까이 오면 🪓 소방도끼로 피해 70을 주며 0.5초마다 휘둘러. 10초마다 HP 500의 🚒 소방차를 타고 10초 동안 물을 뿌려.',detail:'HP 1000 · 화상 면역 · 🪓 70 / 0.5초 · 🚒 10초마다 탑승 · 소방차 HP 500 · 유지 10초 · 💧 피해 10 / 0.3초 · 화상 아군 우선 치료 + HP 10'},"""
moneyman="""{id:'moneyman',name:'머니맨',icon:'🤑',tag:'돈가방 · 나는 돈 · 돈의 행복',hp:1000,damage:20,speed:155,cooldown:1.5,unlock:'moneyManShop',description:'💰 돈가방을 던져 피해 20과 돈의 행복 2중첩을 주고 적중 지점에서 💵 돈을 8방향으로 뿌려. 5초마다 느린 💸 나는 돈을 던지며, 돈의 행복 중첩이 많을수록 더 강해져.',detail:'HP 1000 · 💰 돈가방 20 / 1.5초 · 적중 시 💵 8방향 각 50 · 💸 5초마다 100 + 돈의 행복 중첩당 10 · 돈의 행복 최대 5중첩 · 중첩당 상대 피해 −10 · 5초마다 1중첩 감소'},"""
rep(firefighter,firefighter+'\n'+moneyman)

# Purchase-gated character lock.
old="function characterLocked(c){return !!c?.stageOnly||(c?.unlock==='skeleton'&&!skeletonsUnlocked)||(c?.unlock==='skeletonMage'&&!skeletonMageUnlocked)||(c?.unlock==='zombieMage'&&!zombieMageUnlocked)}"
new="function moneyManOwned(){try{const a=JSON.parse(localStorage.getItem('neonRumble.shopOwned.v1')||'[]');return Array.isArray(a)&&a.includes('moneyman')}catch{return false}}\nfunction characterLocked(c){return !!c?.stageOnly||(c?.unlock==='skeleton'&&!skeletonsUnlocked)||(c?.unlock==='skeletonMage'&&!skeletonMageUnlocked)||(c?.unlock==='zombieMage'&&!zombieMageUnlocked)||(c?.unlock==='moneyManShop'&&!moneyManOwned())}"
rep(old,new)

# Add Money Man as a 150-coin character product.
anchor=""" {id:'robot_antenna',name:'로봇 전용 안테나',icon:'📡',price:90,type:'accessory',exclusiveFor:'robot',desc:'🤖 로봇 전용 꾸미기'},"""
rep(anchor,anchor+"\n {id:'moneyman',name:'머니맨',icon:'🤑',price:150,type:'character',exclusiveFor:null,desc:'구매하면 캐릭터 선택 화면에서 영구 사용 가능'},")

# Shop handles character products and wardrobe excludes them.
rep("function buyCosmetic(id){const item=SHOP_ITEMS.find(x=>x.id===id);if(!item||ownedCosmetics.includes(id))return;if(coins<item.price){alert('코인이 부족해!');return}coins-=item.price;ownedCosmetics.push(id);saveEconomy();updateCoinUI();renderShop();renderWardrobe()}",
    "function buyCosmetic(id){const item=SHOP_ITEMS.find(x=>x.id===id);if(!item||ownedCosmetics.includes(id))return;if(coins<item.price){alert('코인이 부족해!');return}coins-=item.price;ownedCosmetics.push(id);saveEconomy();updateCoinUI();if(item.type==='character')refreshUnlockCards();renderShop();renderWardrobe()}")
rep("function equipCosmetic(id){if(id!==null&&!ownedCosmetics.includes(id))return;const item=id?SHOP_ITEMS.find(x=>x.id===id):null;if(!item)return;const slot=item.type==='aura'?equippedAura:equippedAccessory;",
    "function equipCosmetic(id){if(id!==null&&!ownedCosmetics.includes(id))return;const item=id?SHOP_ITEMS.find(x=>x.id===id):null;if(!item||item.type==='character')return;const slot=item.type==='aura'?equippedAura:equippedAccessory;")
rep("const typeName=item.type==='aura'?'아우라':'장신구';row.innerHTML='<span class=\"item-icon\">'+item.icon+'</span><span><strong>'+item.name+'</strong><small>'+item.desc+' · '+item.price+'코인</small><span class=\"item-type\">'+typeName+'</span></span>';",
    "const typeName=item.type==='character'?'캐릭터':item.type==='aura'?'아우라':'장신구';row.innerHTML='<span class=\"item-icon\">'+item.icon+'</span><span><strong>'+item.name+'</strong><small>'+item.desc+' · '+item.price+'코인</small><span class=\"item-type\">'+typeName+'</span></span>';",
    1)
rep("const items=SHOP_ITEMS.filter(x=>ownedCosmetics.includes(x.id));if(!items.length)","const items=SHOP_ITEMS.filter(x=>ownedCosmetics.includes(x.id)&&x.type!=='character');if(!items.length)",1)

# Money Happiness status: stacking + timed decay.
attack_anchor="""attack(f,e,dmg,friendly=false,bypassDodge=false){
 if(this.result!==null||f.health<=0||e.health<=0||(!friendly&&f.team===e.team)||this.isStudying(e)||(e.id==='ghost'&&e.ghostPhaseUntil>this.time))return 0;
 if(e.id==='invisible'&&!bypassDodge){"""
attack_new="""attack(f,e,dmg,friendly=false,bypassDodge=false){
 if(this.result!==null||f.health<=0||e.health<=0||(!friendly&&f.team===e.team)||this.isStudying(e)||(e.id==='ghost'&&e.ghostPhaseUntil>this.time))return 0;
 dmg=Math.max(0,dmg-10*(f.moneyHappiness||0));
 if(e.id==='invisible'&&!bypassDodge){"""
rep(attack_anchor,attack_new)

# Extend projectile resolution for Money Man and insert skills before Snowman.
old_attack_projectile="""rootTouches(f,e){return this.rootSegments(f).some(s=>{const dx=s.x2-s.x1,dy=s.y2-s.y1,len=dx*dx+dy*dy,t=len?clamp(((e.x-s.x1)*dx+(e.y-s.y1)*dy)/len,0,1):0;return Math.hypot(e.x-s.x1-t*dx,e.y-s.y1-t*dy)<=e.radius+5*f.scale})}
attackProjectile(f,e,s){if(this.isStudying(e))return;if(s.curseOnly){const cd=f.cd,attack=f.attack;this.attack(f,e,s.damage);f.cd=cd;f.attack=attack;if(e.health>0)this.applyCurse(f,e);return}const cd=f.cd,attack=f.attack;this.attack(f,e,s.instant?e.health/Math.max(.000001,1-e.armor):s.damage);f.cd=cd;f.attack=attack;if(s.burn&&e.health>0)this.applyBurn(f,e);if(s.poison&&e.health>0)this.applyPoison(f,e);if(s.toxin&&e.health>0)this.applyToxin(f,e);if(s.stun&&e.health>0)e.stunUntil=Math.max(e.stunUntil,this.time+s.stun);if(s.kind==='giantslash'&&typeof triggerGiantSlashShake==='function')triggerGiantSlashShake();if(s.kind==='magic'){e.slow=Math.max(e.slow,1.2*f.scale);e.slowPower=Math.max(e.slowPower,f.magicSlowStrength)}if(s.kind==='zombiemagic'&&e.health>0){const z=this.spawnZombieMinion(f,'zombie',e,true);if(z){this.effect(z,'🧟 미니좀비!','skill');this.emit('🧌 유도탄 적중 · 미니좀비 소환!')}}}"""
new_attack_projectile="""rootTouches(f,e){return this.rootSegments(f).some(s=>{const dx=s.x2-s.x1,dy=s.y2-s.y1,len=dx*dx+dy*dy,t=len?clamp(((e.x-s.x1)*dx+(e.y-s.y1)*dy)/len,0,1):0;return Math.hypot(e.x-s.x1-t*dx,e.y-s.y1-t*dy)<=e.radius+5*f.scale})}
applyMoneyHappiness(e,amount){if(!e||e.health<=0)return;const before=e.moneyHappiness||0;e.moneyHappiness=Math.min(5,before+amount);if(before<=0||!Number.isFinite(e.moneyHappyNext))e.moneyHappyNext=this.time+5;this.effect(e,'💰 돈의 행복 '+e.moneyHappiness+'중첩','skill')}
tickMoneyHappiness(e){if(!e)return;if(e.health<=0){e.moneyHappiness=0;e.moneyHappyNext=0;return}if(!(e.moneyHappiness>0))return;if(!Number.isFinite(e.moneyHappyNext)||e.moneyHappyNext<=0)e.moneyHappyNext=this.time+5;while(e.moneyHappiness>0&&this.time>=e.moneyHappyNext-1e-9){e.moneyHappiness--;e.moneyHappyNext+=5;if(e.moneyHappiness>0)this.effect(e,'💰 행복 '+e.moneyHappiness+'중첩','skill');else{e.moneyHappyNext=0;this.effect(e,'💰 돈의 행복 종료','skill')}}}
moneyBagBurst(f,x,y){for(let i=0;i<8;i++){const a=i*Math.PI/4,vx=Math.cos(a),vy=Math.sin(a),spawn=f.radius+24;this.shots.push({x:x+vx*spawn,y:y+vy*spawn,vx,vy,owner:f.side,team:f.team,target:-1,kind:'cash',radius:6*f.scale,speed:330*f.scale,damage:50*f.scale,life:2.8,bounces:0})}this.effects.push({x,y,text:'💵 8방향!',kind:'skill',side:f.side,team:f.team,life:.7})}
moneyManSkill(f,e){if(f.id!=='moneyman'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0)return;if(!Number.isFinite(f.moneyFlyNext))f.moneyFlyNext=this.time+5/f.scale;if(f.cd<=1e-9){const a=this.aim(f,e);this.shots.push({x:f.x+a.x*(f.radius+8),y:f.y+a.y*(f.radius+8),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'moneybag',radius:10*f.scale,speed:320*f.scale,damage:20*f.scale,life:4,bounces:0});f.cd=1.5/f.scale;f.attack=.18/f.scale;this.effect(f,'💰 돈가방!','skill')}if(this.time>=f.moneyFlyNext-1e-9){f.moneyFlyNext=this.time+5/f.scale;const a=this.aim(f,e);this.shots.push({x:f.x+a.x*(f.radius+9),y:f.y+a.y*(f.radius+9),vx:a.x,vy:a.y,owner:f.side,team:f.team,target:e.side,kind:'flyingmoney',radius:10*f.scale,speed:145*f.scale,damage:100*f.scale,life:7,bounces:0});f.attack=.22/f.scale;this.effect(f,'💸 나는 돈!','skill')}}
attackProjectile(f,e,s){if(this.isStudying(e))return;if(s.curseOnly){const cd=f.cd,attack=f.attack;this.attack(f,e,s.damage);f.cd=cd;f.attack=attack;if(e.health>0)this.applyCurse(f,e);return}const cd=f.cd,attack=f.attack,dmg=s.kind==='flyingmoney'?(100+10*(e.moneyHappiness||0))*f.scale:(s.instant?e.health/Math.max(.000001,1-e.armor):s.damage);this.attack(f,e,dmg);f.cd=cd;f.attack=attack;if(s.kind==='moneybag'){if(e.health>0)this.applyMoneyHappiness(e,2);this.moneyBagBurst(f,e.x,e.y)}if(s.kind==='cash'&&e.health>0)this.applyMoneyHappiness(e,1);if(s.burn&&e.health>0)this.applyBurn(f,e);if(s.poison&&e.health>0)this.applyPoison(f,e);if(s.toxin&&e.health>0)this.applyToxin(f,e);if(s.stun&&e.health>0)e.stunUntil=Math.max(e.stunUntil,this.time+s.stun);if(s.kind==='giantslash'&&typeof triggerGiantSlashShake==='function')triggerGiantSlashShake();if(s.kind==='magic'){e.slow=Math.max(e.slow,1.2*f.scale);e.slowPower=Math.max(e.slowPower,f.magicSlowStrength)}if(s.kind==='zombiemagic'&&e.health>0){const z=this.spawnZombieMinion(f,'zombie',e,true);if(z){this.effect(z,'🧟 미니좀비!','skill');this.emit('🧌 유도탄 적중 · 미니좀비 소환!')}}}"""
rep(old_attack_projectile,new_attack_projectile)

# Run Money Man skill and exclude him from generic melee.
rep("if(f.id==='coolguy')this.coolGuySkill(f,e);if(f.id==='firefighter')this.firefighterSkill(f,e);", "if(f.id==='coolguy')this.coolGuySkill(f,e);if(f.id==='firefighter')this.firefighterSkill(f,e);if(f.id==='moneyman')this.moneyManSkill(f,e);")
rep("'coolguy','firefighter','zombie'", "'coolguy','firefighter','moneyman','zombie'",1)

# Tick Money Happiness once per simulation step.
rep("step(dt){if(this.result!==null||dt<=0)return;this.updateAirborne();for(const f of this.fighters)if(f.id==='lizard')this.lizardSkill(f);this.stepRound(dt);", "step(dt){if(this.result!==null||dt<=0)return;this.updateAirborne();for(const f of this.fighters){if(f.id==='lizard')this.lizardSkill(f);this.tickMoneyHappiness(f)}this.stepRound(dt);")

# Ability HUD description.
rep("function ability(f){if(f.skeletonBundle)return '💀 해골들 · ROUND '", "function ability(f){if(f.id==='moneyman')return '💰 돈가방 20 · 💵 8방향 50 · 💸 '+Math.max(0,(f.moneyFlyNext||5)-engine.time).toFixed(1)+'초 · 행복 최대 5중첩';if(f.skeletonBundle)return '💀 해골들 · ROUND '")
rep("+(f.curse?' · 🧿 저주':'');$('bar'+team).style.width", "+(f.curse?' · 🧿 저주':'')+(f.moneyHappiness?' · 💰 행복 '+f.moneyHappiness+'중첩':'');$('bar'+team).style.width")

# Emoji projectile rendering.
rep("for(const s of engine.shots){ctx.save();ctx.translate(s.x,s.y);ctx.rotate(Math.atan2(s.vy,s.vx));if(s.kind==='beer'){", "for(const s of engine.shots){ctx.save();ctx.translate(s.x,s.y);ctx.rotate(Math.atan2(s.vy,s.vx));if(s.kind==='moneybag'||s.kind==='cash'||s.kind==='flyingmoney'){ctx.rotate(-Math.atan2(s.vy,s.vx));ctx.font=(s.kind==='moneybag'?30:s.kind==='flyingmoney'?31:27)+'px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText(s.kind==='moneybag'?'💰':s.kind==='flyingmoney'?'💸':'💵',0,0)}else if(s.kind==='beer'){")

# Verify user-facing item and purchase lock text are present.
if "id:'moneyman'" not in s or "price:150,type:'character'" not in s:
    raise SystemExit('Money Man shop item missing after patch')
if "unlock:'moneyManShop'" not in s:
    raise SystemExit('Money Man purchase lock missing after patch')

p.write_text(s,encoding='utf-8')
print('Applied v3.41 Money Man + shop purchase patch')
