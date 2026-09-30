from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1 match, got {n}')
    s=s.replace(old,new,1)

# Version / patch notes
once('BATTLE <b>v3.68</b>','BATTLE <b>v3.69</b>','version')
once('<summary>📒 패치노트 · v3.68</summary><div class="patch-body">', '<summary>📒 패치노트 · v3.69</summary><div class="patch-body"><div class="patch-version"><h3>v3.69 · 편의성 · 신규 캐릭터 털복숭이</h3><ul><li>📦 랜덤 코인상자 제작비 100 → 250코인.</li><li>📺 낡은TV 노이즈 상태에서 TV 화면에 실제 잡음 시각효과가 표시되도록 개선.</li><li>🫈 털복숭이 추가. 가까운 적을 1.5초마다 할퀴어 피해 10~100, 50% 확률로 출혈 부여.</li><li>🫈 자신이 마지막으로 공격한 상대가 사망하면 상대가 죽기 직전 체력만큼 회복.</li></ul></div>', 'patch notes')

# New character
anchor="{id:'old_tv',name:'낡은TV',icon:'📺',tag:'화면 노이즈 · 🔲 연사',hp:1000,damage:40,speed:125,cooldown:0,unlock:'oldTv',description:'3.5초마다 5초 동안 화면에 실제 노이즈가 생긴다. 노이즈 상태에서는 0.1~2초의 무작위 간격으로 🔲을 1~3연발하며, 한 발 피해는 40이고 탄속은 기본~2배 사이에서 무작위로 정해진다.',detail:'HP 1000 · 노이즈 3.5초마다 / 5초 유지 · 🔲 1~3연발 · 발당 40 · 발사 간격 0.1~2초 · 탄속 ×1~2 · CH7 클리어 후 제작소에서 획득'},"
fur="{id:'furball',name:'털복숭이',icon:'🫈',tag:'할퀴기 · 출혈 · 처치 회복',hp:1000,damage:55,speed:165,cooldown:1.5,description:'상대가 가까이 접근하면 할퀴기 이펙트와 함께 피해 10~100을 주며 50% 확률로 출혈을 부여한다. 자신이 마지막으로 공격한 상대가 사망하면 그 상대가 죽기 직전 체력만큼 회복한다.',detail:'HP 1000 · 이동속도 165 · 할퀴기 10~100 / 1.5초 · 출혈 50% · 마지막 공격 대상 사망 시 죽기 직전 HP만큼 회복'},"
once(anchor,anchor+'\n'+fur,'furball roster')

# Death reward helper + attack pre-death health
attack_anchor="attack(f,e,dmg,friendly=false,bypassDodge=false){\n"
helper="""furballDeathHeal(dead,preHp){\n if(!dead||dead.health>0)return;\n const hp=Math.max(0,Math.round(Number(preHp)||0));\n for(const f of this.fighters){if(f.id!=='furball'||f.health<=0||f.furballLastTargetSide!==dead.side)continue;const heal=Math.min(f.hp-f.health,hp);if(heal>0){f.health+=heal;f.healed+=heal;this.effect(f,'🫈 +'+heal,'heal');this.emit('🫈 털복숭이가 마지막 공격 대상의 죽기 직전 체력 '+heal+' 회복!')}f.furballLastTargetSide=null}\n}\nfurballSkill(f,e){\n if(!f||f.id!=='furball'||f.health<=0||f.stunUntil>this.time||!e||e.health<=0||f.cd>1e-9)return;\n if(distance(f,e)>f.radius+e.radius+52*f.scale)return;\n const dmg=(10+Math.floor(this.random()*91))*f.scale,ang=Math.atan2(e.y-f.y,e.x-f.x);f.furballLastTargetSide=e.side;\n const dealt=this.attack(f,e,dmg);f.cd=1.5/f.scale;f.slashFx=.28/f.scale;f.slashAngle=ang;this.effect(e,'🫈 할퀴기 '+Math.round(dmg)+'!','skill');\n if(dealt>0&&e.health>0&&this.random()<.5)this.applyBleed(f,e);\n}\n"""
once(attack_anchor,helper+attack_anchor,'furball helpers')
once(" f.attack=.35/f.scale;f.cd=f.cooldown;let n=Math.min(e.health,Math.round(dmg*(1-e.armor)));e.health-=n;f.damageDealt+=n;f.hits++;", " f.attack=.35/f.scale;f.cd=f.cooldown;const preDeathHp=e.health;let n=Math.min(e.health,Math.round(dmg*(1-e.armor)));e.health-=n;f.damageDealt+=n;f.hits++;", 'attack pre hp')
once(" if(e.health===0){e.trail=[];this.emit((e.boss?'보스 ':this.mode==='boss'?'도전자 '+e.side+'번 ':'')+e.name+' 탈락!');this.checkEnd()}", " if(e.health===0){this.furballDeathHeal(e,preDeathHp);e.trail=[];this.emit((e.boss?'보스 ':this.mode==='boss'?'도전자 '+e.side+'번 ':'')+e.name+' 탈락!');this.checkEnd()}", 'direct death reward')

# Bleed death reward (covers Furball's own bleed kill)
once("tickBleed(e){const b=e.bleed;if(!b)return;while(b.next<=this.time+1e-9&&b.next<=b.expires+1e-9){const source=this.fighters[b.source];if(!source||source.team===e.team){e.bleed=null;return}const n=Math.min(e.health,Math.max(0,Math.round(b.damage*(1-e.armor))));e.health-=n;", "tickBleed(e){const b=e.bleed;if(!b)return;while(b.next<=this.time+1e-9&&b.next<=b.expires+1e-9){const source=this.fighters[b.source];if(!source||source.team===e.team){e.bleed=null;return}const preDeathHp=e.health,n=Math.min(e.health,Math.max(0,Math.round(b.damage*(1-e.armor))));e.health-=n;", 'bleed pre hp')
once("e.trail=[];e.bleed=null;this.emit(e.name+' 출혈로 탈락!');this.checkEnd();return", "this.furballDeathHeal(e,preDeathHp);e.trail=[];e.bleed=null;this.emit(e.name+' 출혈로 탈락!');this.checkEnd();return", 'bleed death reward')

# Skill hook and prevent generic contact attack
once("if(f.id==='old_tv')this.oldTvSkill(f,e);", "if(f.id==='old_tv')this.oldTvSkill(f,e);if(f.id==='furball')this.furballSkill(f,e);", 'furball skill hook')
once("'goblin','goblin_king','psychic'].includes(f.id)&&f.cd<=0", "'goblin','goblin_king','psychic','furball'].includes(f.id)&&f.cd<=0", 'generic melee exclusion')

# Ability HUD
once("function ability(f){if(f.id==='old_tv')", "function ability(f){if(f.id==='furball')return '🫈 할퀴기 10~100 / 1.5초 · 출혈 50% · 마지막 공격 대상 사망 시 회복';if(f.id==='old_tv')", 'furball ability')

# Coin box production price 250, TV remains 100
once("function startCraft(id){if(!craftSystemUnlocked()){alert('CHAPTER 7을 먼저 클리어해야 해!');return}if(craftJob){alert('이미 제작 중인 아이템이 있어!');return}if(coins<100){alert('제작에는 100코인이 필요해!');return}if(!['coin_box','old_tv'].includes(id))return;coins-=100;craftJob={id,readyAt:Date.now()+60000};", "function startCraft(id){if(!craftSystemUnlocked()){alert('CHAPTER 7을 먼저 클리어해야 해!');return}if(craftJob){alert('이미 제작 중인 아이템이 있어!');return}if(!['coin_box','old_tv'].includes(id))return;const price=id==='coin_box'?250:100;if(coins<price){alert('제작에는 '+price+'코인이 필요해!');return}coins-=price;craftJob={id,readyAt:Date.now()+60000};", 'craft pricing')
once("for(const x of p.querySelectorAll('[data-craft]'))x.disabled=!ok||!!craftJob||coins<100;", "for(const x of p.querySelectorAll('[data-craft]')){const price=x.dataset.craft==='coin_box'?250:100;x.disabled=!ok||!!craftJob||coins<price}", 'craft button pricing')
once("<p>CHAPTER 7 클리어 시 사용 가능 · 모든 제작 100코인 · 제작시간 1분</p>", "<p>CHAPTER 7 클리어 시 사용 가능 · 제작시간 1분</p>", 'forge description')
once("<button type=\"button\" data-craft=\"coin_box\">100코인 제작</button>", "<button type=\"button\" data-craft=\"coin_box\">250코인 제작</button>", 'coin box button')
# tutorial wording
s=s.replace('CHAPTER 7을 클리어하면 100코인·1분 제작 방식의 🔨 제작소도 열려.','CHAPTER 7을 클리어하면 🔨 제작소가 열려. 낡은TV는 100코인, 랜덤 코인상자는 250코인이며 제작시간은 1분이야.',1)

# TV noise visual overlay: draw on top of fighters before normal effects.
marker='for(const e of engine.effects)'
pos=s.find(marker)
if pos<0:
    raise SystemExit('effects draw marker not found')
noise="""for(const tv of engine.fighters){if(tv.id!=='old_tv'||tv.health<=0||engine.time>=(tv.oldTvNoiseUntil||0)-1e-9)continue;const sc=tv.bodyScale||1,w=48*sc,h=30*sc,x=tv.x-w/2,y=tv.y-h/2-5*sc;ctx.save();ctx.globalAlpha=.88;ctx.fillStyle='#090b0d';ctx.fillRect(x,y,w,h);for(let ni=0;ni<18;ni++){const yy=y+Math.random()*h,hh=1+Math.random()*3;ctx.fillStyle=ni%3===0?'#f7f7f7':ni%3===1?'#737373':'#c9c9c9';ctx.globalAlpha=.35+Math.random()*.55;ctx.fillRect(x,yy,w*(.25+Math.random()*.75),hh)}ctx.globalAlpha=.9;ctx.strokeStyle='#e6f2f2';ctx.lineWidth=2*sc;ctx.strokeRect(x,y,w,h);ctx.restore()}\n"""
s=s[:pos]+noise+s[pos:]

p.write_text(s,encoding='utf-8')
print('v3.69 patch applied')