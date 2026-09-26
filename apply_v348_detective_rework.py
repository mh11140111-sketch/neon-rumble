from pathlib import Path
import re

p=Path('index.html')
s=p.read_text(encoding='utf-8')
orig=s

# Version labels
s=s.replace('BATTLE <b>v3.47</b>','BATTLE <b>v3.48</b>',1)
s=s.replace('📒 패치노트 · v3.47','📒 패치노트 · v3.48',1)

# Patch note
marker='<div class="patch-body">'
patch='''<div class="patch-version"><h3>v3.48 · 탐정 리워크</h3><ul><li>🕵️‍♂️ 탐정의 기본 투사체를 🔎 돋보기로 표시.</li><li>신규 스킬 「범인 잡기」 추가. 10초마다 모든 상대를 2초 동안 쇠창살 감옥에 가둠.</li><li>감옥은 기절과 별도 상태이며, 감옥이 끝난 뒤 대상별로 50% 기절 3초 / 30% 피해 100 / 15% 기절 10초 + 피해 100 / 5% 즉사 판정.</li></ul></div>'''
if marker in s and 'v3.48 · 탐정 리워크' not in s:
    s=s.replace(marker,marker+patch,1)

# Detective roster text
s=s.replace("tag:'돋보기 · 추적 표식'","tag:'돋보기 · 범인 잡기'",1)
s=s.replace("description:'2초마다 🔎 돋보기를 던져 피해 75. 적중한 일반 적은 2초 동안 몸집이 2배가 되고, 그동안 그 적을 향하는 투사체는 유도 공격으로 바뀐다. 보스는 크기 증가에 면역.'",
            "description:'2초마다 🔎 돋보기를 던져 피해 75. 10초마다 모든 상대를 2초 동안 감옥에 가둔 뒤 확률 판정을 적용한다.'",1)
s=s.replace("detail:'HP 1000 · 🔎 피해 75 / 2초 · 일반 적 2초간 크기 2배 · 확대 중 해당 적을 향하는 투사체 유도 · 보스 크기 증가 면역'",
            "detail:'HP 1000 · 🔎 피해 75 / 2초 · 범인 잡기 10초 · 감옥 2초 · 이후 확률 판정'",1)

# Add separate jail skill before detectiveSkill.
needle='detectiveSkill(f,e){'
if needle in s and 'detectiveJailSkill(f){' not in s:
    jail=r'''detectiveJailSkill(f){
 const pool=this.fighters||this.units||[];
 if(f.id!=='detective'||f.health<=0)return;
 // Resolve / maintain existing prison states first.
 for(const e of pool){
  if(!e||e===f||e.health<=0||e.team===f.team)continue;
  if((e.jailedUntil||0)>this.time){
   // Prison is a separate state; stunUntil is only used as the movement/attack gate while jailed.
   e.stunUntil=Math.max(e.stunUntil||0,this.time+.08);
  }else if(e.jailPending){
   e.jailPending=false;
   e.jailedUntil=0;
   if(Number.isFinite(e.jailSavedStunUntil))e.stunUntil=Math.max(e.jailSavedStunUntil,this.time);
   const r=Math.random();
   if(r<.05){
    e.health=0;
    this.effect(e,'🚨 즉사!','skill');
   }else if(r<.20){
    e.health=Math.max(0,e.health-100*f.scale);
    e.stunUntil=Math.max(e.stunUntil||0,this.time+10/f.scale);
    this.effect(e,'🚔 기절 10초 + 피해 100!','skill');
   }else if(r<.50){
    e.health=Math.max(0,e.health-100*f.scale);
    this.effect(e,'🚔 피해 100!','skill');
   }else{
    e.stunUntil=Math.max(e.stunUntil||0,this.time+3/f.scale);
    this.effect(e,'🚔 기절 3초!','skill');
   }
  }
 }
 if(!Number.isFinite(f.jailNext))f.jailNext=this.time+10/f.scale;
 if(this.time<f.jailNext-1e-9)return;
 f.jailNext=this.time+10/f.scale;
 let caught=0;
 for(const e of pool){
  if(!e||e===f||e.health<=0||e.team===f.team)continue;
  e.jailSavedStunUntil=e.stunUntil||0;
  e.jailedUntil=this.time+2/f.scale;
  e.jailPending=true;
  e.stunUntil=Math.max(e.stunUntil||0,e.jailedUntil);
  caught++;
 }
 if(caught)this.effect(f,'🚔 범인 잡기!','skill');
}
'''
    s=s.replace(needle,jail+needle,1)

# Invoke jail skill wherever Detective's normal skill is updated.
s=s.replace('this.detectiveSkill(f,e);','this.detectiveJailSkill(f);this.detectiveSkill(f,e);')

# Force magnifier projectile to render as the requested emoji when projectile text rendering is available.
# Insert a lightweight draw pass before requestAnimationFrame when a canvas context named ctx and shots list exist.
# Prefer an existing projectile rendering branch if present.
if "s.kind==='magnifier'" in s and "fillText('🔎'" not in s:
    # Try common projectile draw pattern: before any generic arc rendering for shots.
    pat=r"(for\(const s of this\.shots\)\{)"
    repl=r"\1if(s.kind==='magnifier'){ctx.save();ctx.font=`${Math.max(16,s.radius*2.6)}px 'Apple Color Emoji','Segoe UI Emoji',sans-serif`;ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText('🔎',s.x,s.y);ctx.restore();continue;}"
    s,n=re.subn(pat,repl,s,count=1)

# Add jail bars overlay in the fighter draw loop using common fighter loop signature.
if 'jailedUntil' in s and 'JAIL BARS v3.48' not in s:
    patterns=[r"(for\(const f of this\.fighters\)\{)",r"(for\(const f of fighters\)\{)"]
    overlay="""/* JAIL BARS v3.48 */if((f.jailedUntil||0)>this.time){ctx.save();const rr=Math.max(20,f.radius*1.25);ctx.lineWidth=Math.max(3,rr*.08);ctx.strokeStyle='rgba(190,205,220,.95)';ctx.fillStyle='rgba(20,28,38,.22)';ctx.fillRect(f.x-rr,f.y-rr,f.x+rr-(f.x-rr),rr*2);ctx.strokeRect(f.x-rr,f.y-rr,rr*2,rr*2);for(let bx=-.66;bx<=.66;bx+=.33){ctx.beginPath();ctx.moveTo(f.x+rr*bx,f.y-rr);ctx.lineTo(f.x+rr*bx,f.y+rr);ctx.stroke();}ctx.restore();}"""
    for pat in patterns:
        s,n=re.subn(pat,r"\1"+overlay,s,count=1)
        if n: break

if s==orig:
    raise SystemExit('No v3.48 changes applied')

required=['BATTLE <b>v3.48</b>','v3.48 · 탐정 리워크','detectiveJailSkill(f){','jailPending','🚔 범인 잡기!']
missing=[x for x in required if x not in s]
if missing:
    raise SystemExit('Missing markers: '+repr(missing))

p.write_text(s,encoding='utf-8')
print('v3.48 detective rework applied')
