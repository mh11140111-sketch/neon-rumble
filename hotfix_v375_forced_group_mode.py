from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
bad="engine=mode='group'?new Engine(relayTeams[0][0],relayTeams[1][0],Math.random,{mode:'group',teams:relayTeams})"
good="engine=mode==='group'?new Engine(relayTeams[0][0],relayTeams[1][0],Math.random,{mode:'group',teams:relayTeams})"
if s.count(bad)!=1:
    raise SystemExit(f'expected exactly one broken group assignment, got {s.count(bad)}')
s=s.replace(bad,good,1)
if "engine=mode='group'?" in s:
    raise SystemExit('broken assignment still present')
p.write_text(s,encoding='utf-8')
print('fixed forced 3v3 mode bug')
