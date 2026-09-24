from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if old not in s:
        raise SystemExit(f'PATCH FAILED: {label}')
    s=s.replace(old,new,count)

# Version + patch notes
rep('BATTLE <b>v3.15</b>','BATTLE <b>v3.16</b>','version')
rep('📒 패치노트 · v3.15','📒 패치노트 · v3.16','patch summary')
rep('<div class="patch-body"><div class="patch-version"><h3>v3.15 · 독침 복어</h3>', '<div class="patch-body"><div class="patch-version"><h3>v3.16 · 회전 방패 기사</h3><ul><li>기사 리워크: 기존 상시 피해 감소 30%를 제거하고 회전 방패 시스템으로 변경.</li><li>작은 방패가 기사 주변을 회전하며, 충전된 방패는 들어오는 공격 1회를 완전히 막음. 방패는 사용 후 10초 뒤 재충전.</li><li>방패로 막은 공격의 원래 피해가 500 이상이면 기사 중심 충격파 발동: 자신을 제외한 모든 캐릭터에게 피해 100 및 3초 기절.</li><li>기사의 기존 전투 방식은 유지: 적에게 접근해 검격 95, 공격 간격 0.95초.</li></ul></div><div class="patch-version"><h3>v3.15 · 독침 복어</h3>', 'patch block')

# Knight roster text
rep("{id:'knight',name:'기사',icon:'🛡️',tag:'방어 · 검격',hp:1000,damage:95,speed:125,cooldown:.95,description:'방패로 받는 피해를 항상 30% 줄이고, 상대에게 접근해 검으로 공격해.',detail:'검격 95 · 받는 피해 −30% · 공격 간격 0.95초'}", "{id:'knight',name:'기사',icon:'🛡️',tag:'회전 방패 · 검격',hp:1000,damage:95,speed:125,cooldown:.95,description:'적에게 접근해 검격 95로 공격해. 작은 방패가 주변을 회전하며 충전된 방패는 공격 1회를 완전히 막아. 사용한 방패는 10초 뒤 재충전되고, 500 이상 피해를 막으면 전장 충격파를 발동해.',detail:'검격 95 · 공격 간격 0.95초 · 방패 1회 완전 방어 / 사용 후 10초 재충전 · 500+ 피해 방어 시 충격파 100 / 자신 제외 전원 3초 기절'}", 'knight roster')

# Remove old armor and add shield state
rep("armor:type.id==='knight'?.3*scale:0,lifesteal:", "armor:0,lifesteal:", 'remove knight armor')
rep("vampireBat:false,dodgeChance:type.id==='invisible'?.5:0,nextJump:", "vampireBat:false,dodgeChance:type.id==='invisible'?.5:0,knightShieldReady:type.id==='knight',knightShieldNext:0,knightShieldAngle:0,nextJump:", 'shield state')

# Boss rule text cleanup
s=s.replace('기사 피해 감소는 60%, ', '기사는 회전 방패로 공격 1회를 완전 방어하고 사용 후 10초 뒤 재충전해. 500 이상 피해를 막으면 충격파를 발동해. ', 1)

# Insert knight shield methods before attack()
needle='attack(f,e,dmg,friendly=false,bypassDodge=false){\n'
if needle not in s:
    raise SystemExit('PATCH FAILED: attack anchor')
methods="""updateKnightShield(f,dt){if(f.id!=='knight'||f.health<=0)return;f.knightShieldAngle=(f.knightShieldAngle+dt*2.8)%(Math.PI*2);if(!f.knightShieldReady&&this.time>=f.knightShieldNext-1e-9){f.knightShieldReady=true;this.effect(f,'🛡️ 방패 재충전','skill')}}
knightShockwave(f){if(f.id!=='knight'||f.health<=0)return;this.effects.push({x:f.x,y:f.y,text:'방패 충격파!',kind:'shockwave',side:f.side,team:f.team,life:.9});this.emit('🛡️ 기사가 강력한 공격을 막아 충격파를 발동!');this.resolvingBlast=true;for(const e of this.fighters){if(e===f||e.health<=0)continue;this.attack(f,e,100,true);if(e.health>0)e.stunUntil=Math.max(e.stunUntil,this.time+3)}this.resolvingBlast=false;this.checkEnd()}
"""
s=s.replace(needle,methods+needle,1)

# Shield intercepts direct/melee/projectile/shockwave attacks through central attack path.
rep("if(this.result!==null||f.health<=0||e.health<=0||(!friendly&&f.team===e.team)||this.isStudying(e))return 0;\n if(e.id==='invisible'", "if(this.result!==null||f.health<=0||e.health<=0||(!friendly&&f.team===e.team)||this.isStudying(e))return 0;\n if(e.id==='knight'&&e.knightShieldReady){e.knightShieldReady=false;e.knightShieldNext=this.time+10;this.effect(e,'🛡️ 완전 방어!','skill');if(dmg>=500)this.knightShockwave(e);return 0}\n if(e.id==='invisible'", 'shield intercept')

# Refresh / rotate shield even while stunned; old movement/attack behavior stays unchanged.
rep("this.transformHero(f);this.updateVampire(f);this.moonSkill(f);\n if(f.moonUltPhase", "this.transformHero(f);this.updateVampire(f);this.moonSkill(f);this.updateKnightShield(f,dt);\n if(f.moonUltPhase", 'shield update')

# Ability HUD
rep("function ability(f){return f.id==='puffer'?", "function ability(f){return f.id==='knight'?(f.knightShieldReady?'🛡️ 방패 준비 · 다음 공격 완전 방어':'🛡️ 재충전 '+Math.max(0,f.knightShieldNext-engine.time).toFixed(1)+'초'):f.id==='puffer'?", 'knight hud')

# Rotating shield visual around every living knight. Full opacity when ready, dim while charging.
draw_anchor="for(const f of engine.fighters){if(f.moonUltPhase==='air')continue;const c=colors[f.team],r=f.radius;ctx.globalAlpha=f.health<=0?.15:(f.id==='invisible'?.38:1);"
if draw_anchor not in s:
    raise SystemExit('PATCH FAILED: draw anchor')
draw_new="for(const f of engine.fighters){if(f.moonUltPhase==='air')continue;const c=colors[f.team],r=f.radius;ctx.globalAlpha=f.health<=0?.15:(f.id==='invisible'?.38:1);if(f.id==='knight'&&f.health>0){const a=f.knightShieldAngle||engine.time*2.8,sr=r+24,sx=f.x+Math.cos(a)*sr,sy=f.y+Math.sin(a)*sr;ctx.save();ctx.globalAlpha=f.knightShieldReady?1:.28;ctx.font='24px \\\"Apple Color Emoji\\\",\\\"Segoe UI Emoji\\\",sans-serif';ctx.fillText('🛡️',sx,sy);ctx.restore();ctx.globalAlpha=f.id==='invisible'?.38:1;}"
s=s.replace(draw_anchor,draw_new,1)

# Shockwave screen cue styling uses existing effect pipeline; add distinct color.
s=s.replace("v.kind==='forge'?'#ffd394':colors[v.team]", "v.kind==='shockwave'?'#d9efff':v.kind==='forge'?'#ffd394':colors[v.team]", 1)

p.write_text(s,encoding='utf-8')
print('v3.16 patch applied')
