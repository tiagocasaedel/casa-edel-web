"""merge the web-search results (ddg_d*.json) into cands.json, ranked by name similarity; writes q/rev2.json"""
import json, glob, re, sys
sys.path.insert(0, 'tools/fotos')
from match import sim  # noqa: E402  (match.py runs on import and rewrites cands.json; keep its output)
D = 'tools/fotos/'
C = json.load(open(D + 'cands.json'))
P = {x['id']: x for x in json.load(open(D + 'productos.json'))}
E = json.load(open(D + 'elegidas.json'))
BAD = re.compile(r'logo|placeholder|no-?image|sin-?imagen|default|banner', re.I)
out = []
for f in sorted(glob.glob(D + 'ddg_d[0-9]*.json')):
    for pid, cs in json.load(open(f)).items():
        if pid in E: continue
        x = P[pid]; good = []
        for c in cs:
            if not c.get('i') or BAD.search(c['i']) or 'duckduckgo' in c.get('src', ''): continue
            s = sim(x['n'], c.get('t', '')) + (0.3 if x['b'].lower() in c.get('t', '').lower() else 0) + (0.5 if x['k'].lower() in (c.get('t', '') + c.get('u', '')).lower() else 0)
            good.append(dict(c, sc=round(s, 2), why='web'))
        good.sort(key=lambda c: -c['sc'])
        old = [c for c in C.get(pid, []) if c.get('why') != 'web']
        seen = set(); merged = []
        for c in good + old:
            if c['i'] in seen: continue
            seen.add(c['i']); merged.append(c)
        if merged: C[pid] = merged[:4]; out.append(pid)
json.dump(C, open(D + 'cands.json', 'w'), ensure_ascii=False)
out.sort(key=lambda p: (P[p]['b'], P[p]['n']))
json.dump(out, open(D + 'q/rev2.json', 'w'))
print('para revisar', len(out))
