from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="""function tone(hz,duration=.08,volume=.035,type='triangle',delay=0){if(!sound)return;try{audio=audio||new(window.AudioContext||window.webkitAudioContext)();if(audio.state==='suspended')audio.resume();const t=audio.currentTime+delay,o=audio.createOscillator(),g=audio.createGain();o.type=type;o.frequency.setValueAtTime(hz,t);g.gain.setValueAtTime(volume,t);g.gain.exponentialRampToValueAtTime(.001,t+duration);o.connect(g);g.connect(audio.destination);o.start(t);o.stop(t+duration)}catch{}}
function playSfx(kind){if(!sound)return;if(kind==='start'){tone(420,.07,.03,'square');tone(650,.1,.025,'triangle',.07)}else if(kind==='hit'){tone(150+Math.random()*90,.045,.022,'square')}else if(kind==='victory'){tone(520,.09,.035,'triangle');tone(660,.09,.035,'triangle',.1);tone(820,.15,.04,'triangle',.2)}else if(kind==='select'){tone(540,.07,.025,'triangle')}else tone(300,.06,.02,'triangle')}
"""
new="""let impactNoiseBuffer=null,lastImpactSfxAt=-1;
function ensureAudio(){if(!sound)return null;try{audio=audio||new(window.AudioContext||window.webkitAudioContext)();if(audio.state==='suspended')audio.resume();return audio}catch{return null}}
function tone(hz,duration=.08,volume=.035,type='triangle',delay=0){const a=ensureAudio();if(!a)return;try{const t=a.currentTime+delay,o=a.createOscillator(),g=a.createGain();o.type=type;o.frequency.setValueAtTime(hz,t);g.gain.setValueAtTime(volume,t);g.gain.exponentialRampToValueAtTime(.001,t+duration);o.connect(g);g.connect(a.destination);o.start(t);o.stop(t+duration)}catch{}}
function playImpactSfx(){const a=ensureAudio();if(!a)return;try{const t=a.currentTime;if(lastImpactSfxAt>=0&&t-lastImpactSfxAt<.025)return;lastImpactSfxAt=t;
 const thud=a.createOscillator(),thudGain=a.createGain();thud.type='sine';thud.frequency.setValueAtTime(115+Math.random()*18,t);thud.frequency.exponentialRampToValueAtTime(52,t+.11);thudGain.gain.setValueAtTime(.095,t);thudGain.gain.exponentialRampToValueAtTime(.001,t+.12);thud.connect(thudGain);thudGain.connect(a.destination);thud.start(t);thud.stop(t+.13);
 const crack=a.createOscillator(),crackGain=a.createGain();crack.type='triangle';crack.frequency.setValueAtTime(820+Math.random()*180,t);crack.frequency.exponentialRampToValueAtTime(190,t+.035);crackGain.gain.setValueAtTime(.038,t);crackGain.gain.exponentialRampToValueAtTime(.001,t+.04);crack.connect(crackGain);crackGain.connect(a.destination);crack.start(t);crack.stop(t+.045);
 if(!impactNoiseBuffer){const len=Math.max(1,Math.floor(a.sampleRate*.09));impactNoiseBuffer=a.createBuffer(1,len,a.sampleRate);const data=impactNoiseBuffer.getChannelData(0);for(let i=0;i<len;i++)data[i]=(Math.random()*2-1)*(1-i/len)}const noise=a.createBufferSource(),filter=a.createBiquadFilter(),noiseGain=a.createGain();noise.buffer=impactNoiseBuffer;filter.type='lowpass';filter.frequency.setValueAtTime(1100,t);filter.Q.value=.8;noiseGain.gain.setValueAtTime(.065,t);noiseGain.gain.exponentialRampToValueAtTime(.001,t+.075);noise.connect(filter);filter.connect(noiseGain);noiseGain.connect(a.destination);noise.start(t);noise.stop(t+.09)
 }catch{}}
function playSfx(kind){if(!sound)return;if(kind==='start'){tone(420,.07,.03,'square');tone(650,.1,.025,'triangle',.07)}else if(kind==='hit'){playImpactSfx()}else if(kind==='victory'){tone(520,.09,.035,'triangle');tone(660,.09,.035,'triangle',.1);tone(820,.15,.04,'triangle',.2)}else if(kind==='select'){tone(540,.07,.025,'triangle')}else tone(300,.06,.02,'triangle')}
"""
if old not in s:
    raise SystemExit('v3.27 sound block not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('v3.27 impact sound hotfix applied')
