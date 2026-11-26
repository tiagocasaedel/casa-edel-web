"""rank Bing image results (+ ddg web results) per product into cands2.json; writes q/rev2.json"""
import json, glob, re, sys
sys.path.insert(0, 'tools/fotos')
D = 'tools/fotos/'
exec(open(D + 'match.py').read().split('# ---- sources')[0])  # norm/toks/sim only
P = {x['id']: x for x in json.load(open(D + 'productos.json'))}
E = json.load(open(D + 'elegidas.json'))
C = {}
for f in sorted(glob.glob(D + 'bing_d*.json')):
    for pid, r in json.load(open(f)).items():
        if pid in E: continue
        x = P[pid]; k = norm(x['k']); b = norm(x['b'])
        cs = []
        for rank, c in enumerate(r['c']):
            hay = norm(c['t'] + ' ' + c['u'] + ' ' + c['i'])
            s = sim(x['n'], c['t']) + (1.0 if len(k) >= 3 and k in hay else 0) + (0.3 if b in hay else 0) - 0.04 * rank
            cs.append(dict(c, sc=round(s, 2), why='código' if len(k) >= 3 and k in hay else 'web'))
        C[pid] = cs
for f in sorted(glob.glob(D + 'ddg_d*.json')):
    for pid, cs in json.load(open(f)).items():
        if pid in E or not cs: continue
        x = P[pid]
        for c in cs:
            if not c.get('i') or re.search(r'logo|banner|placeholder', c['i'], re.I): continue
            C.setdefault(pid, []).append(dict(c, sc=round(sim(x['n'], c.get('t', '')) - 0.1, 2), why='web'))
out = []
for pid, cs in C.items():
    seen = set(); best = []
    for c in sorted(cs, key=lambda c: -c['sc']):
        if c['i'] in seen: continue
        seen.add(c['i']); best.append(c)
    if best: C[pid] = best[:4]; out.append(pid)
json.dump({p: C[p] for p in out}, open(D + 'cands2.json', 'w'), ensure_ascii=False)
out.sort(key=lambda p: (P[p]['b'], P[p]['n']))
json.dump(out, open(D + 'q/rev2.json', 'w'))
print('para revisar', len(out), 'sin nada', len([p for p in P if p not in E and p not in C]))
