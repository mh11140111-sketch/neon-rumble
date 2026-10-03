from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    n=s.count(old)
    if n!=1:
        raise SystemExit(f'{label}: expected 1, got {n}')
    s=s.replace(old,new,1)

once("dathisgood55:'graveFx'","deathisgood55:'graveFx'","code registry")
once("else if(code==='dathisgood55'){graveFxUnlocked=true;try{localStorage.setItem(GRAVE_FX_KEY,'1')}catch{}if(out)out.textContent='✅ 코드 적용 완료 · ༼☠︎༽ 사망 위치 무덤 효과 해금!'}",
     "else if(code==='deathisgood55'){graveFxUnlocked=true;try{localStorage.setItem(GRAVE_FX_KEY,'1')}catch{}if(out)out.textContent='✅ 코드 적용 완료 · ༼☠︎༽ 사망 위치 무덤 효과 해금!'}",
     'redeem branch')
once("else if(r<.199)line='쓰러진 자리에도 흔적은 남지. dathisgood55';",
     "else if(r<.199)line='쓰러진 자리에도 흔적은 남지. deathisgood55';",
     'devil hint')

if "dathisgood55" in s:
    raise SystemExit('old typo code still present')

p.write_text(s,encoding='utf-8')
print('grave code corrected to deathisgood55')
