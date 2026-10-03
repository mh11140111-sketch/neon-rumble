from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1: raise SystemExit(f'{label}: expected 1 got {n}')
    s=s.replace(old,new,1)

# Remove the incorrectly applied self-heal from Skeleton King.
once(
"f.attack=.35/f.scale;f.cd=f.cooldown;const preDeathHp=e.health;let n=Math.min(e.health,Math.round(dmg*(1-e.armor)));e.health-=n;f.damageDealt+=n;f.hits++;if(f.id==='skeleton_king'&&n>0){f.skeletonKingDamageBank=(f.skeletonKingDamageBank||0)+n;while(f.skeletonKingDamageBank>=100){f.skeletonKingDamageBank-=100;const heal=Math.min(50*f.scale,f.hp-f.health);f.health+=heal;f.healed=(f.healed||0)+heal;if(heal)this.effect(f,'👑💀 피해 100 · HP +'+Math.round(heal),'heal')}}",
"f.attack=.35/f.scale;f.cd=f.cooldown;const preDeathHp=e.health;let n=Math.min(e.health,Math.round(dmg*(1-e.armor)));e.health-=n;f.damageDealt+=n;f.hits++;if(f.id==='cowboy'&&e.id==='skeleton_king'&&n>0){f.skeletonKingDamageBank=(f.skeletonKingDamageBank||0)+n;while(f.skeletonKingDamageBank>=100){f.skeletonKingDamageBank-=100;const heal=Math.min(50*f.scale,f.hp-f.health);f.health+=heal;f.healed=(f.healed||0)+heal;if(heal)this.effect(f,'🤠 해골왕 피해 100 · HP +'+Math.round(heal),'heal')}}",
'cowboy heal from skeleton king damage')

# Skeleton King uses attacks only; no skeleton summoning.
once(
" if(!Number.isFinite(f.skGunNext)){f.skGunNext=this.time;f.skSwordNext=this.time;f.skBeerNext=this.time;f.skMagicNext=this.time;f.skSummonNext=this.time+10}",
" if(!Number.isFinite(f.skGunNext)){f.skGunNext=this.time;f.skSwordNext=this.time;f.skBeerNext=this.time;f.skMagicNext=this.time}",
'skeleton king init no summon')
once(
" if(this.time>=f.skSummonNext-1e-9){f.skSummonNext=this.time+10/f.scale;this.spawnSkele44Skeleton(f,f.x,f.y);this.effect(f,'👑💀 해골 소환!','skill')}\n}",
"}",
'remove skeleton king summon')

# Update roster text and stage text.
once(
"{id:'skeleton_king',name:'해골왕',icon:'👑💀',tag:'모든 해골 전투술 · 피해 회복',hp:1500,damage:70,speed:135,cooldown:1,stageOnly:true,description:'총잡이·칼잡이·취한 해골·해골 법사의 공격 방식을 모두 사용한다. 적에게 누적 피해 100을 줄 때마다 자신의 HP를 50 회복한다.',detail:'HP 1500 · 🔫 총알 70 · 🗡️ 칼 70 · 🍺 맥주병 100 · 💀 마법탄 65 · 해골 소환 · 누적 피해 100마다 HP +50'},",
"{id:'skeleton_king',name:'해골왕',icon:'👑💀',tag:'모든 해골 공격 방식 · 소환 없음',hp:1500,damage:70,speed:135,cooldown:1,stageOnly:true,description:'총잡이·칼잡이·취한 해골·해골 법사의 공격 방식은 사용하지만 해골을 소환하지는 않는다. 주인공 카우보이가 해골왕에게 누적 피해 100을 줄 때마다 HP 50을 회복한다.',detail:'HP 1500 · 🔫 총알 70 · 🗡️ 칼 70 · 🍺 맥주병 100 · 💀 마법탄 65 · 해골 소환 없음 · 카우보이는 해골왕에게 누적 피해 100마다 HP +50'},",
'skeleton king roster correction')

once(
"n===2?'NEW-CHAPTER 2 STAGE 2 · 해골왕 HP 1500 · 모든 해골 공격 방식 사용 · 누적 피해 100마다 HP 50 회복.':",
"n===2?'NEW-CHAPTER 2 STAGE 2 · 해골왕 HP 1500 · 총잡이/칼잡이/취한 해골/해골 법사의 공격 방식 사용 · 해골 소환 없음 · 카우보이가 해골왕에게 누적 피해 100을 줄 때마다 HP 50 회복.':",
'stage2 battle info correction')

once(
"<span class=\"card-desc\">HP 1500 · 총잡이/칼잡이/취한 해골/해골 법사의 모든 공격 방식 사용</span>",
"<span class=\"card-desc\">HP 1500 · 총잡이/칼잡이/취한 해골/해골 법사의 공격 방식 사용 · 해골 소환 없음 · 카우보이 누적 피해 100마다 HP +50</span>",
'stage2 card correction')

p.write_text(s,encoding='utf-8')
print('corrected skeleton king stage2 healing and summon behavior')
