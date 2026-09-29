from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

def all_replace(old,new,label,min_count=1):
    global s
    n=s.count(old)
    if n<min_count:
        raise SystemExit(f'{label}: expected >= {min_count}, got {n}')
    s=s.replace(old,new)
    return n

# Version + patch notes
once('<span class="badge">BATTLE <b>v3.63</b></span>','<span class="badge">BATTLE <b>v3.64</b></span>','version')
once('<details class="patch-notes"><summary>📒 패치노트 · v3.63</summary><div class="patch-body">', '<details class="patch-notes"><summary>📒 패치노트 · v3.64</summary><div class="patch-body"><div class="patch-version"><h3>v3.64 · 밸런스 · 도박장 · 캐릭터 전용 스킨</h3><ul><li>🐉 용 여의주의 신통력 공격 주기 3초 → 2.7초.</li><li>🦸 남자가 히어로로 변신하면 HP 100 회복, 기존 상태이상 전부 해제 후 히어로 상태 동안 모든 상태이상 면역. 돌진 중 전용 대쉬 잔상 이펙트 추가.</li><li>🎰 도박장 이용료 50 → 100코인. 중복 캐릭터 보상 400 → 200코인, 중복 장식품 보상 250 → 150코인.</li><li>🛒 캐릭터 전용 스킨 4종 추가. 각 700코인: 🧛‍♂️ 뱀파이어, 👾 외계인, 🧙‍♂️ 마법사, 🧞 알라딘의 지니.</li></ul></div>', 'patch notes')

# Dragon 2.7s
once("description:'3초마다 여의주의 신통력", "description:'2.7초마다 여의주의 신통력", 'dragon desc')
once("detail:'HP 1000 · 신통력 70 / 3초", "detail:'HP 1000 · 신통력 70 / 2.7초", 'dragon detail')
once("dragonMysticNext:type.id==='dragon'?3/scale:9999", "dragonMysticNext:type.id==='dragon'?2.7/scale:9999", 'dragon initial')
once("f.dragonMysticNext=this.time+3/f.scale;", "f.dragonMysticNext=this.time+2.7/f.scale;", 'dragon attack')
once("f.dragonMysticNext=this.time+3/f.scale", "f.dragonMysticNext=this.time+2.7/f.scale", 'dragon revive')

# Hero description + permanent status immunity after transform
once("description:'출전 후 20초 동안 이동만 해. 살아남으면 🦸 히어로로 변신해 돌진 피해 250 → 후퇴 → 재돌진을 반복해.'", "description:'출전 후 20초 동안 이동만 해. 살아남으면 🦸 히어로로 변신해 HP 100을 회복하고 모든 상태이상에 면역이 되며, 돌진 피해 250 → 후퇴 → 재돌진을 반복해.'", 'hero desc')
once("detail:'기본 체력 1000 · 변신 전 공격 없음 · 돌진당 1회 타격 · 후퇴 0.65초 · 변신 시 상태이상 해제 · 변신 후 속도 +50%'", "detail:'기본 체력 1000 · 변신 전 공격 없음 · 변신 시 HP +100 · 모든 상태이상 해제/면역 · 돌진당 1회 타격 · 후퇴 0.65초 · 변신 후 속도 +50% · 돌진 잔상'", 'hero detail')
old_transform="transformHero(f){if(f.id!=='hero'||f.heroReady||f.health<=0||this.time<f.transformAt-1e-9)return;f.heroReady=true;f.icon='🦸';f.name='히어로';f.speed*=1.5;f.poison=null;f.toxin=null;f.burn=null;f.venom=null;f.stunUntil=0;f.slow=0;f.slowPower=0;f.rootSlow=0;f.rootSlowPower=0;if(f.capturedBy!==null){const captor=this.fighters[f.capturedBy];if(captor)this.releaseCapture(captor);f.capturedBy=null}this.effect(f,'변신 · 상태이상 해제!','skill')}"
new_transform="""heroStatusImmune(f){return !!(f&&f.id==='hero'&&f.heroReady)}
clearHeroStatus(f){if(!this.heroStatusImmune(f))return;f.poison=null;f.toxin=null;f.burn=null;f.venom=null;f.curse=null;f.bleed=null;f.stunUntil=0;f.slow=0;f.slowPower=0;f.rootSlow=0;f.rootSlowPower=0;f.charmUntil=0;f.charmSource=null;f.moneyHappiness=0;f.moneyHappyNext=0;f.cowUntil=0;f.jailedUntil=0;f.jailPending=false;f.airborneUntil=0;if((f.magnifiedUntil||0)>0&&f.magnifyBaseRadius){f.radius=f.magnifyBaseRadius;f.magnifiedUntil=0;f.magnifyBaseRadius=0}if(f.capturedBy!==null){const captor=this.fighters[f.capturedBy];if(captor)this.releaseCapture(captor);f.capturedBy=null}}
transformHero(f){if(f.id!=='hero'||f.heroReady||f.health<=0||this.time<f.transformAt-1e-9)return;f.heroReady=true;f.icon='🦸';f.name='히어로';f.speed*=1.5;const heal=Math.min(f.hp-f.health,100*f.scale);f.health+=heal;f.healed+=heal;this.clearHeroStatus(f);this.effect(f,'🦸 변신! HP +'+Math.round(heal)+' · 상태이상 면역','skill');this.emit('🦸 히어로 변신! HP 100 회복 · 모든 상태이상 면역') }"""
once(old_transform,new_transform,'hero transform')
once("stepFighter(f,e,dt){\n if((f.charmUntil||0)>this.time)", "stepFighter(f,e,dt){\n if(this.heroStatusImmune(f))this.clearHeroStatus(f);\n if((f.charmUntil||0)>this.time)", 'hero per-step immunity')
once("if(f.dash>0)f.trail.push({x:f.x,y:f.y,life:.2});", "if(f.dash>0)f.trail.push({x:f.x,y:f.y,life:.2});if(f.id==='hero'&&f.heroReady&&f.heroPhase==='rush')f.trail.push({x:f.x,y:f.y,life:.26});", 'hero dash trail')
# Block common status applicators immediately
once("applyCurse(source,e){\n if(!source||!e||source.team===e.team||e.health<=0||this.isStudying(e)||e.id==='cursedhand')return false;", "applyCurse(source,e){\n if(!source||!e||source.team===e.team||e.health<=0||this.isStudying(e)||e.id==='cursedhand'||this.heroStatusImmune(e))return false;", 'hero curse immune')
once("applyBurn(f,e,friendly=false){if(e.id==='phoenix'||e.id==='moai'||e.id==='firefighter')return;", "applyBurn(f,e,friendly=false){if(e.id==='phoenix'||e.id==='moai'||e.id==='firefighter'||this.heroStatusImmune(e))return;", 'hero burn immune')
once("applyPoison(f,e){\n if(e.id==='moai'||e.id==='robot'||f.team===e.team||e.health<=0||this.isStudying(e))return;", "applyPoison(f,e){\n if(e.id==='moai'||e.id==='robot'||this.heroStatusImmune(e)||f.team===e.team||e.health<=0||this.isStudying(e))return;", 'hero poison immune')
once("applyToxin(f,e){\n if(e.id==='moai'||e.id==='robot'||f.team===e.team||e.health<=0||this.isStudying(e))return;", "applyToxin(f,e){\n if(e.id==='moai'||e.id==='robot'||this.heroStatusImmune(e)||f.team===e.team||e.health<=0||this.isStudying(e))return;", 'hero toxin immune')
once("applyBleed(f,e){if(!f||!e||e.health<=0||f.team===e.team)return;", "applyBleed(f,e){if(!f||!e||e.health<=0||f.team===e.team||this.heroStatusImmune(e))return;", 'hero bleed immune')
once("applyMoneyHappiness(e,amount){if(!e||e.health<=0)return;", "applyMoneyHappiness(e,amount){if(!e||e.health<=0||this.heroStatusImmune(e))return;", 'hero money immune')
once("else if(s.kind==='love_stun'){hit.stunUntil=Math.max(hit.stunUntil,this.time+1*f.scale);this.effect(hit,'💖 기절 1초!','skill')}else if(s.kind==='love_charm'){hit.charmUntil=Math.max(hit.charmUntil||0,this.time+3*f.scale);hit.charmSource=f.side;this.effect(hit,'💓 유혹 3초!','skill')}", "else if(s.kind==='love_stun'){if(!this.heroStatusImmune(hit)){hit.stunUntil=Math.max(hit.stunUntil,this.time+1*f.scale);this.effect(hit,'💖 기절 1초!','skill')}}else if(s.kind==='love_charm'){if(!this.heroStatusImmune(hit)){hit.charmUntil=Math.max(hit.charmUntil||0,this.time+3*f.scale);hit.charmSource=f.side;this.effect(hit,'💓 유혹 3초!','skill')}}", 'hero love status immune')

# Casino pricing/rewards
all_replace('1회 50코인','1회 100코인','casino panel price',1)
once('🎰 50코인으로 돌리기','🎰 100코인으로 돌리기','casino button')
once('중복 꾸미기 → 250코인 · 중복 캐릭터 → 400코인','중복 꾸미기 → 150코인 · 중복 캐릭터 → 200코인','casino odds')
once("spin.disabled=!ok||casinoSpinning||coins<50", "spin.disabled=!ok||casinoSpinning||coins<100", 'casino enable')
once("if(coins<50){alert('코인이 부족해! 슬롯머신은 50코인이 필요해.');return}coins-=50;", "if(coins<100){alert('코인이 부족해! 슬롯머신은 100코인이 필요해.');return}coins-=100;", 'casino charge')
once("coins+=250;text=item.icon+' '+item.name+' 중복! 대신 🪙 250코인 획득!'", "coins+=150;text=item.icon+' '+item.name+' 중복! 대신 🪙 150코인 획득!'", 'casino cosmetic duplicate')
once("coins+=400;text=(item?item.icon:'🎰')+' '+(item?item.name:'캐릭터')+' 중복! 대신 🪙 400코인 획득!'", "coins+=200;text=(item?item.icon:'🎰')+' '+(item?item.name:'캐릭터')+' 중복! 대신 🪙 200코인 획득!'", 'casino character duplicate')
# tutorial current casino text
all_replace('🎰 도박장은 CHAPTER 5를 모두 클리어하면 열리고 50코인으로 돌릴 수 있어.', '🎰 도박장은 CHAPTER 5를 모두 클리어하면 열리고 100코인으로 돌릴 수 있어.', 'tutorial casino price', 1)

# Add character skins to shop
skin_items=""" {id:'skin_vampire',name:'뱀파이어 스킨',icon:'🧛‍♂️',price:700,type:'skin',skinFor:'vampire',skinTarget:'fighter',exclusiveFor:'vampire',desc:'🧛 흡혈귀 전용 스킨'},
 {id:'skin_alien',name:'외계인 스킨',icon:'👾',price:700,type:'skin',skinFor:'alien',skinTarget:'fighter',exclusiveFor:'alien',desc:'👽 외계인 전용 스킨'},
 {id:'skin_mage',name:'마법사 스킨',icon:'🧙‍♂️',price:700,type:'skin',skinFor:'mage',skinTarget:'fighter',exclusiveFor:'mage',desc:'🧙 마법사 전용 스킨'},
 {id:'skin_genie',name:'알라딘의 지니 스킨',icon:'🧞',price:700,type:'skin',skinFor:'aladdin',skinTarget:'genie',exclusiveFor:'aladdin',desc:'👳‍♀️ 알라딘이 소환하는 지니 전용 스킨'},
"""
once(" {id:'aura_red',name:'빨간 아우라'", skin_items+" {id:'aura_red',name:'빨간 아우라'", 'skin shop items')

# Skin storage and helpers
once("EQUIP_RIGHT_AURA_KEY='neonRumble.equip.rightAura.v2',EQUIP_BACKGROUND_KEY='neonRumble.equip.background.v1';", "EQUIP_RIGHT_AURA_KEY='neonRumble.equip.rightAura.v2',EQUIP_LEFT_SKIN_KEY='neonRumble.equip.leftSkin.v1',EQUIP_RIGHT_SKIN_KEY='neonRumble.equip.rightSkin.v1',EQUIP_BACKGROUND_KEY='neonRumble.equip.background.v1';", 'skin storage keys')
once("let coins=0,ownedCosmetics=[],equippedAccessory=[null,null],equippedAura=[null,null],equippedBackground=null,wardrobeSide=0;", "let coins=0,ownedCosmetics=[],equippedAccessory=[null,null],equippedAura=[null,null],equippedSkin=[null,null],equippedBackground=null,wardrobeSide=0;", 'skin state')
once("equippedAura[0]=localStorage.getItem(EQUIP_LEFT_AURA_KEY)||null;equippedAura[1]=localStorage.getItem(EQUIP_RIGHT_AURA_KEY)||null;equippedBackground=", "equippedAura[0]=localStorage.getItem(EQUIP_LEFT_AURA_KEY)||null;equippedAura[1]=localStorage.getItem(EQUIP_RIGHT_AURA_KEY)||null;equippedSkin[0]=localStorage.getItem(EQUIP_LEFT_SKIN_KEY)||null;equippedSkin[1]=localStorage.getItem(EQUIP_RIGHT_SKIN_KEY)||null;equippedBackground=", 'skin load')
once("const keys=[EQUIP_LEFT_ACCESSORY_KEY,EQUIP_RIGHT_ACCESSORY_KEY],auraKeys=[EQUIP_LEFT_AURA_KEY,EQUIP_RIGHT_AURA_KEY];for(let i=0;i<2;i++){if(equippedAccessory[i])localStorage.setItem(keys[i],equippedAccessory[i]);else localStorage.removeItem(keys[i]);if(equippedAura[i])localStorage.setItem(auraKeys[i],equippedAura[i]);else localStorage.removeItem(auraKeys[i])}", "const keys=[EQUIP_LEFT_ACCESSORY_KEY,EQUIP_RIGHT_ACCESSORY_KEY],auraKeys=[EQUIP_LEFT_AURA_KEY,EQUIP_RIGHT_AURA_KEY],skinKeys=[EQUIP_LEFT_SKIN_KEY,EQUIP_RIGHT_SKIN_KEY];for(let i=0;i<2;i++){if(equippedAccessory[i])localStorage.setItem(keys[i],equippedAccessory[i]);else localStorage.removeItem(keys[i]);if(equippedAura[i])localStorage.setItem(auraKeys[i],equippedAura[i]);else localStorage.removeItem(auraKeys[i]);if(equippedSkin[i])localStorage.setItem(skinKeys[i],equippedSkin[i]);else localStorage.removeItem(skinKeys[i])}", 'skin save')
once("function equippedItem(side,type){const id=type==='aura'?equippedAura[side?1:0]:equippedAccessory[side?1:0];return SHOP_ITEMS.find(x=>x.id===id)||null}", "function equippedItem(side,type){const id=type==='aura'?equippedAura[side?1:0]:type==='skin'?equippedSkin[side?1:0]:equippedAccessory[side?1:0];return SHOP_ITEMS.find(x=>x.id===id)||null}", 'equipped item skin')
once("function currentAura(side){return equippedItem(side,'aura')}\nfunction currentBackground()", "function currentAura(side){return equippedItem(side,'aura')}\nfunction currentSkin(side){return equippedItem(side,'skin')}\nfunction skinEquipAllowed(item,side){if(!item||item.type!=='skin')return true;const choices=currentChoices();return !!(choices&&choices[side]===item.skinFor)}\nfunction currentSkinForFighter(f){if(!f)return null;const item=currentSkin(f.team?1:0);if(!item)return null;if(item.skinTarget==='genie')return f.id==='genie'?item:null;if(f.summon)return null;if(item.skinFor!==f.id)return null;if(f.id==='vampire'&&f.vampireBat)return null;if(f.id==='alien'&&f.ufoMounted)return null;return item}\nfunction displaySkinIcon(side,id,base){const item=currentSkin(side);if(!item||item.skinTarget==='genie'||item.skinFor!==id)return base;return item.icon}\nfunction currentBackground()", 'skin helpers')

# Equip logic skin slot
old_equip="function equipCosmetic(id){if(id!==null&&!ownedCosmetics.includes(id))return;const item=id?SHOP_ITEMS.find(x=>x.id===id):null;if(!item||item.type==='character')return;if(item.type==='background'){equippedBackground=equippedBackground===id?null:id;saveEconomy();renderWardrobe();renderShop();return}const slot=item.type==='aura'?equippedAura:equippedAccessory;slot[wardrobeSide]=slot[wardrobeSide]===id?null:id;saveEconomy();renderWardrobe();renderShop()}"
new_equip="function equipCosmetic(id){if(id!==null&&!ownedCosmetics.includes(id))return;const item=id?SHOP_ITEMS.find(x=>x.id===id):null;if(!item||item.type==='character')return;if(item.type==='background'){equippedBackground=equippedBackground===id?null:id;saveEconomy();renderWardrobe();renderShop();return}if(item.type==='skin'&&!skinEquipAllowed(item,wardrobeSide)){alert('이 스킨의 전용 캐릭터를 먼저 해당 칸에 선택해 줘!');return}const slot=item.type==='aura'?equippedAura:item.type==='skin'?equippedSkin:equippedAccessory;slot[wardrobeSide]=slot[wardrobeSide]===id?null:id;saveEconomy();renderWardrobe();renderShop();updateSelection()}"
once(old_equip,new_equip,'skin equip')

# Shop type label
once("const typeName=item.type==='character'?'캐릭터':item.type==='aura'?'아우라':item.type==='background'?'배경':'장신구';", "const typeName=item.type==='character'?'캐릭터':item.type==='skin'?'전용 스킨':item.type==='aura'?'아우라':item.type==='background'?'배경':'장신구';", 'shop skin label')

# Wardrobe rendering
old_load="const acc=currentAccessory(wardrobeSide),aura=currentAura(wardrobeSide),bg=currentBackground();if($('wardrobe-loadout'))$('wardrobe-loadout').textContent=(wardrobeSide===0?'왼쪽':'오른쪽')+' 캐릭터 · 장신구: '+(acc?acc.icon+' '+acc.name:'없음')+' · 아우라: '+(aura?aura.icon+' '+aura.name:'없음')+' · 배경: '+(bg?bg.icon+' '+bg.name:'기본');"
new_load="const acc=currentAccessory(wardrobeSide),aura=currentAura(wardrobeSide),skin=currentSkin(wardrobeSide),bg=currentBackground();if($('wardrobe-loadout'))$('wardrobe-loadout').textContent=(wardrobeSide===0?'왼쪽':'오른쪽')+' 캐릭터 · 스킨: '+(skin?skin.icon+' '+skin.name:'기본')+' · 장신구: '+(acc?acc.icon+' '+acc.name:'없음')+' · 아우라: '+(aura?aura.icon+' '+aura.name:'없음')+' · 배경: '+(bg?bg.icon+' '+bg.name:'기본');"
once(old_load,new_load,'wardrobe loadout')
once("const typeName=item.type==='aura'?'아우라':item.type==='background'?'배경':'장신구';", "const typeName=item.type==='skin'?'전용 스킨':item.type==='aura'?'아우라':item.type==='background'?'배경':'장신구';", 'wardrobe skin label')
once("const on=item.type==='background'?equippedBackground===item.id:(item.type==='aura'?equippedAura:equippedAccessory)[wardrobeSide]===item.id;b.textContent=on?'장착 해제':'장착';b.onclick=()=>equipCosmetic(item.id);", "const on=item.type==='background'?equippedBackground===item.id:(item.type==='aura'?equippedAura:item.type==='skin'?equippedSkin:equippedAccessory)[wardrobeSide]===item.id,skinLocked=item.type==='skin'&&!skinEquipAllowed(item,wardrobeSide);b.textContent=on?'장착 해제':skinLocked?'전용 캐릭터 선택 필요':'장착';b.disabled=!on&&skinLocked;b.onclick=()=>equipCosmetic(item.id);", 'wardrobe skin button')

# Selection preview + battle drawing skin
once("$('icon'+i).textContent=c.icon;", "$('icon'+i).textContent=displaySkinIcon(i,c.id,c.icon);", 'selection skin preview')
once("}else{ctx.fillText(f.icon,f.x,f.y+1)}const cosmetic=", "}else{const skin=currentSkinForFighter(f);ctx.fillText(skin?skin.icon:f.icon,f.x,f.y+1)}const cosmetic=", 'battle skin render')

# Update casino tutorial/visible labels if exact old odds remain elsewhere
all_replace('중복 꾸미기 → 250코인', '중복 꾸미기 → 150코인', 'duplicate cosmetic visible', 0)
all_replace('중복 캐릭터 → 400코인', '중복 캐릭터 → 200코인', 'duplicate character visible', 0)

p.write_text(s,encoding='utf-8')
print('v3.64 patch applied')
