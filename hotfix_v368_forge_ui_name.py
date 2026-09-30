from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
n=s.count('updateForgeSystemUI()')
if n!=2:
    raise SystemExit(f'expected 2 updateForgeSystemUI refs, got {n}')
s=s.replace('updateForgeSystemUI()','renderForgeSystem()')
if 'updateForgeSystemUI()' in s: raise SystemExit('stale forge UI function remains')
p.write_text(s,encoding='utf-8')
print('v3.68 forge UI runtime hotfix applied')
