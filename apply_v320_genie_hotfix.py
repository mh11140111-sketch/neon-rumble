from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def rep(old,new,label,count=1):
    global s
    if old not in s:
        raise SystemExit(f'PATCH FAILED: {label}')
    s=s.replace(old,new,count)

# Genie must be a complete independent combat unit. Missing armor caused NaN damage/HP.
rep("damage:50*scale*(owner.geniePower||1),speed:180*scale",
    "damage:50*scale*(owner.geniePower||1),armor:0,lifesteal:0,rootSlowStrength:0,magicSlowStrength:0,speed:180*scale",
    'genie combat stats')
rep("trail:[],summon:true,ownerSide:owner.side}",
    "trail:[],summon:true,ownerSide:owner.side,genieResolved:false}",
    'genie lifecycle state')

# HUD counts only primary fighters. Summons keep their own in-arena HP bar and Aladdin HUD shows Genie HP separately.
old="for(let team=0;team<2;team++){const fs=engine.fighters.filter(f=>f.team===team),f=fs[0],hp=fs.reduce((n,x)=>n+x.health,0),max=fs.reduce((n,x)=>n+x.hp,0),live=fs.filter(x=>x.health>0).length;"
new="for(let team=0;team<2;team++){const allFs=engine.fighters.filter(f=>f.team===team),fs=allFs.filter(f=>!f.summon),f=fs[0],hp=fs.reduce((n,x)=>n+(Number.isFinite(x.health)?x.health:0),0),max=fs.reduce((n,x)=>n+(Number.isFinite(x.hp)?x.hp:0),0),live=fs.filter(x=>x.health>0).length;"
rep(old,new,'primary-only hud')

old="function ability(f){return f.id==='aladdin'?('🧞‍♂️ 지니 '+(f.genieRevives||0)+'/2 부활 사용 · 지니 공격력 x'+(f.geniePower||1)):f.id==='knight'?"
new="function ability(f){if(f.id==='aladdin'){const g=engine.fighters.find(x=>x.id==='genie'&&x.ownerSide===f.side);const ghp=g&&Number.isFinite(g.health)?Math.max(0,Math.ceil(g.health)):0,gmax=g&&Number.isFinite(g.hp)?Math.ceil(g.hp):(1500*(f.boss?2.5:1));return '👳‍♀️ 알라딘 '+Math.ceil(f.health)+' / '+Math.ceil(f.hp)+' HP · 🧞‍♂️ 지니 '+ghp+' / '+gmax+' HP · 부활 '+(f.genieRevives||0)+'/2 · 지니 공격력 x'+(f.geniePower||1)}return f.id==='knight'?"
rep(old,new,'aladdin genie hud')

# Make the summon visually explicit as its own unit label.
old="(f.boss?'BOSS':mode==='boss'?f.side+'번':f.team?'R':'L')+' · '+f.name"
new="(f.id==='genie'?(f.boss?'BOSS 지니':'지니'):(f.boss?'BOSS':mode==='boss'?f.side+'번':f.team?'R':'L'))+' · '+f.name"
rep(old,new,'genie independent label')

# Defensive cleanup: if any prior NaN state somehow exists during a hot reload, normalize Genie HP.
old="genieSkill(g,dt){\n if(g.id!=='genie'||g.health<=0)return;"
new="genieSkill(g,dt){\n if(g.id!=='genie')return;if(!Number.isFinite(g.hp))g.hp=1500*(g.boss?2.5:1);if(!Number.isFinite(g.health))g.health=g.hp;if(g.health<=0)return;"
rep(old,new,'genie nan guard')

# The current v3.20 code already excludes both Aladdin and Genie from generic contact attacks.
if "'aladdin','genie'].includes(f.id)" not in s:
    raise SystemExit('PATCH FAILED: genie contact exclusion missing')

p.write_text(s,encoding='utf-8')
print('v3.20 genie independent-unit hotfix applied')
