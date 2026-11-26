"""round-2 candidates for products without a chosen photo: crawl pages (low threshold, generic images dropped),
Easy, Bing and DDG results -> cands2.json + q/rev2.json"""
import json, glob, re, os, collections
D = 'tools/fotos/'
exec(open(D + 'match.py').read().split('# ---- sources')[0])
P = {x['id']: x for x in json.load(open(D + 'productos.json'))}
E = json.load(open(D + 'elegidas.json'))
REJ = set(map(tuple, json.load(open(D + 'rechazadas.json')))) if os.path.exists(D + 'rechazadas.json') else set()
BADI = re.compile(r'logo|banner|placeholder|no-?image|sin-?imagen|favicon|icon|slider', re.I)
SRC = collections.defaultdict(list)
for f in glob.glob(D + 'crawl/*.json'):
    if f.endswith('shopify.json'): continue
    b = os.path.basename(f)[:-5]; pages = json.load(open(f))['pages']
    cnt = collections.Counter(p['i'] for p in pages)
    for p in pages:
        if p['i'] and cnt[p['i']] <= 3 and not BADI.search(p['i']): SRC[b].append({'t': p['t'], 'i': p['i'], 'u': p['u'], 'src': p['u'].split('/')[2], 'c': p.get('c', [])})
for site, items in json.load(open(D + 'crawl/shopify.json')).items():
    for it in items: SRC['jeluz' if 'jeluz' in site else norm(it['v'])].append({'t': it['t'], 'i': it['i'][0], 'u': it['u'], 'src': site.split('//')[1], 'c': it['sku']})
EASY = json.load(open(D + 'easy.json'))
WEB = collections.defaultdict(list)
for f in sorted(glob.glob(D + 'bing_d*.json')):
    for pid, r in json.load(open(f)).items(): WEB[pid] += r['c']
for f in sorted(glob.glob(D + 'ddg_d*.json')):
    for pid, cs in json.load(open(f)).items(): WEB[pid] += [c for c in cs if c.get('i')]
C = {}; out = []
for pid, x in P.items():
    if pid in E: continue
    b = norm(x['b']); k = norm(x['k']); cs = []
    for r in SRC.get(b, []):
        s = sim(x['n'], r['t']) + (1.0 if len(k) >= 3 and any(norm(c) == k for c in r['c']) else 0)
        if s >= 0.15: cs.append(dict(r, sc=round(s, 2), why='código' if s >= 1 else 'nombre'))
    for r in EASY.get(pid, []): cs.append({'t': r['t'], 'i': r['i'], 'u': r['u'], 'src': 'easy', 'sc': round(sim(x['n'], r['t']), 2), 'why': 'easy'})
    for r in WEB.get(pid, []):
        if BADI.search(r['i']): continue
        hay = norm(r.get('t', '') + r.get('u', ''))
        cs.append(dict(r, sc=round(sim(x['n'], r.get('t', '')) + (1.0 if len(k) >= 4 and k in hay else 0) - 0.05, 2), why='web'))
    seen = set(); best = []
    for c in sorted(cs, key=lambda c: -c['sc']):
        if c['i'] in seen or (pid, c['i']) in REJ: continue
        seen.add(c['i']); c.pop('c', None); best.append(c)
    if best: C[pid] = best[:4]; out.append(pid)
json.dump(C, open(D + 'cands2.json', 'w'), ensure_ascii=False)
out.sort(key=lambda p: (P[p]['b'], P[p]['n']))
json.dump(out, open(D + 'q/rev2.json', 'w'))
print('con candidatos', len(out), 'de', len([p for p in P if p not in E]))
print(collections.Counter(P[p]['b'] for p in out).most_common(40))
