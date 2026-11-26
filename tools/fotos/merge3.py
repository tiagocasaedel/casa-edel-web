"""round-3 candidates from online store searches (tiendas_t*.json) -> cands3.json + q/rev3.json"""
import json, glob
D = 'tools/fotos/'
exec(open(D + 'match.py').read().split('# ---- sources')[0])
P = {x['id']: x for x in json.load(open(D + 'productos.json'))}; E = json.load(open(D + 'elegidas.json'))
REJ = set(map(tuple, json.load(open(D + 'rechazadas.json'))))
C = {}
for f in glob.glob(D + 'tiendas_t[1-9].json'):
    for k, v in json.load(open(f)).items():
        if k in E: continue
        x = P[k]; kk = norm(x['k']); cs = []
        for c in v:
            s = sim(x['n'], c['t']); kc = len(kk) >= 4 and kk in norm(c['t'] + c.get('sku', ''))
            if (s >= 0.3 or kc) and (k, c['i']) not in REJ:
                cs.append(dict(c, sc=round(s + (1 if kc else 0) + (0.2 if norm(x['b']) in norm(c['t']) else 0), 2), why='código' if kc else 'web'))
        seen = set(); best = []
        for c in sorted(cs, key=lambda c: -c['sc']):
            if c['i'] in seen: continue
            seen.add(c['i']); best.append(c)
        if best: C[k] = best[:4]
out = sorted(C, key=lambda p: (P[p]['b'], P[p]['n']))
json.dump(C, open(D + 'cands3.json', 'w'), ensure_ascii=False); json.dump(out, open(D + 'q/rev3.json', 'w'))
print(len(out))
