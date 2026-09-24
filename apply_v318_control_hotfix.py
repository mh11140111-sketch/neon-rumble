from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old="this.random=random;this.mode=['boss','relay','group'].includes(options.mode)?options.mode:'duel';"
new="this.random=random;this.mode=['boss','relay','group','control'].includes(options.mode)?options.mode:'duel';"
if old not in s:
    raise SystemExit('PATCH FAILED: mode whitelist')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
print('v3.18 control mode whitelist hotfix applied')
