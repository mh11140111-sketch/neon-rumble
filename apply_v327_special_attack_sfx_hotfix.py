from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

old="effect(f,text,kind='hit'){if(kind==='forge')this.effects=this.effects.filter(v=>v.kind!==kind||v.side!==f.side);this.effects.push({x:f.x,y:f.y-f.radius-7,text,kind,side:f.side,team:f.team,life:.8})}"
new="effect(f,text,kind='hit'){if(kind==='forge')this.effects=this.effects.filter(v=>v.kind!==kind||v.side!==f.side);this.effects.push({x:f.x,y:f.y-f.radius-7,text,kind,side:f.side,team:f.team,life:.8});if(typeof globalThis.NRPlaySpecialSfx==='function')globalThis.NRPlaySpecialSfx(f,text,kind)}"
if old not in s: raise SystemExit('Engine.effect pattern not found')
s=s.replace(old,new,1)

anchor="function playSfx(kind){if(!sound)return;if(kind==='start'){tone(420,.07,.03,'square');tone(650,.1,.025,'triangle',.07)}else if(kind==='hit'){playImpactSfx()}else if(kind==='victory'){tone(520,.09,.035,'triangle');tone(660,.09,.035,'triangle',.1);tone(820,.15,.04,'triangle',.2)}else if(kind==='select'){tone(540,.07,.025,'triangle')}else tone(300,.06,.02,'triangle')}"
if anchor not in s: raise SystemExit('playSfx anchor not found')
insert=r'''const specialSfxLast=Object.create(null);
function specialSfxGate(key,gap=.08){const a=ensureAudio();if(!a)return null;const now=a.currentTime,last=specialSfxLast[key]??-999;if(now-last<gap)return null;specialSfxLast[key]=now;return a}
function sfxSweep(from,to,duration=.12,volume=.035,type='sawtooth',delay=0){const a=ensureAudio();if(!a)return;try{const t=a.currentTime+delay,o=a.createOscillator(),g=a.createGain();o.type=type;o.frequency.setValueAtTime(Math.max(20,from),t);o.frequency.exponentialRampToValueAtTime(Math.max(20,to),t+duration);g.gain.setValueAtTime(volume,t);g.gain.exponentialRampToValueAtTime(.001,t+duration);o.connect(g);g.connect(a.destination);o.start(t);o.stop(t+duration+.01)}catch{}}
function sfxNoise(duration=.08,volume=.04,cutoff=1800,delay=0){const a=ensureAudio();if(!a)return;try{const t=a.currentTime+delay,len=Math.max(1,Math.floor(a.sampleRate*duration)),buf=a.createBuffer(1,len,a.sampleRate),data=buf.getChannelData(0);for(let i=0;i<len;i++)data[i]=(Math.random()*2-1)*(1-i/len);const src=a.createBufferSource(),filter=a.createBiquadFilter(),g=a.createGain();src.buffer=buf;filter.type='lowpass';filter.frequency.value=cutoff;g.gain.setValueAtTime(volume,t);g.gain.exponentialRampToValueAtTime(.001,t+duration);src.connect(filter);filter.connect(g);g.connect(a.destination);src.start(t);src.stop(t+duration)}catch{}}
function playSpecialAttackSfx(f,text,kind){if(!sound||!f||kind==='hit'||kind==='heal'||kind==='forge')return;const id=f.id||'',tx=String(text||'');let key='';
 if(tx.includes('거대검격'))key='giantslash';else if(tx.includes('회전 레이저'))key='laser';else if(tx.includes('만능로봇팔'))key='robotarm';else if(tx.includes('반달 조각'))key='moon';else if(tx.includes('궁극기 준비'))key='moonult';else if(id==='genie'&&tx.includes('회전'))key='genie';else if(tx.includes('저주탄'))key='curse';else if(id==='devileye'&&tx.includes('저주받은 손'))key='curseSummon';else if(tx.includes('눈송이'))key='snow';else if(tx.includes('👎'))key='thumb';else if(tx.includes('🤜'))key='punch';else if(tx.includes('테이저'))key='taser';else if(tx.includes('총 난사'))key='barrage';else if(tx.includes('투척')&&(id==='villain'||tx.includes('💣')||tx.includes('🧨')||tx.includes('☠️')))key='bomb';else if(tx.includes('가시'))key='spike';else if(tx.includes('불꽃'))key='flame';else if(tx.includes('충격파'))key='shockwave';else if(tx.includes('돌진'))key='dash';
 if(!key)return;const gap={thumb:.12,taser:.13,curse:.14,genie:.22,flame:.12}[key]??.18;if(!specialSfxGate(key,gap))return;
 if(key==='giantslash'){sfxNoise(.13,.055,2600);sfxSweep(920,110,.18,.055,'sawtooth');tone(95,.16,.075,'sine')}
 else if(key==='laser'){sfxSweep(150,980,.28,.038,'sawtooth');sfxSweep(980,430,.22,.025,'sine',.12)}
 else if(key==='robotarm'){tone(78,.16,.08,'sine');sfxNoise(.1,.045,900);sfxSweep(260,90,.12,.035,'square')}
 else if(key==='moon'){sfxNoise(.11,.035,4200);sfxSweep(760,240,.14,.036,'sine')}
 else if(key==='moonult'){tone(62,.42,.065,'sine');sfxSweep(100,520,.38,.03,'sawtooth')}
 else if(key==='genie'){sfxNoise(.15,.035,3000);sfxSweep(260,760,.16,.028,'triangle');sfxSweep(760,220,.17,.024,'triangle',.07)}
 else if(key==='curse'||key==='curseSummon'){sfxSweep(key==='curse'?510:240,key==='curse'?135:620,.18,.032,'sine');tone(key==='curse'?78:105,.2,.035,'triangle')}
 else if(key==='snow'){sfxNoise(.07,.028,6500);tone(1450,.055,.025,'triangle');tone(980,.07,.02,'sine',.025)}
 else if(key==='thumb'){sfxSweep(210,95,.07,.035,'square');sfxNoise(.045,.025,1000)}
 else if(key==='punch'){tone(72,.12,.085,'sine');sfxNoise(.07,.055,850);sfxSweep(220,70,.08,.03,'square')}
 else if(key==='taser'){sfxSweep(1650,520,.065,.035,'square');sfxSweep(2400,900,.045,.025,'square',.035)}
 else if(key==='barrage'){sfxNoise(.12,.05,3800);sfxSweep(320,105,.09,.03,'square')}
 else if(key==='bomb'){sfxSweep(420,150,.09,.025,'triangle');sfxNoise(.08,.035,1700)}
 else if(key==='spike'){sfxNoise(.07,.03,5200);sfxSweep(1350,470,.08,.025,'triangle')}
 else if(key==='flame'){sfxNoise(.14,.04,2400);sfxSweep(170,90,.14,.028,'sawtooth')}
 else if(key==='shockwave'){tone(58,.22,.08,'sine');sfxNoise(.12,.04,700)}
 else if(key==='dash'){sfxNoise(.08,.03,3200);sfxSweep(380,150,.08,.022,'triangle')}
}
window.NRPlaySpecialSfx=playSpecialAttackSfx;
'''
s=s.replace(anchor,insert+anchor,1)

p.write_text(s,encoding='utf-8')
print('v3.27 special attack SFX hotfix applied')
