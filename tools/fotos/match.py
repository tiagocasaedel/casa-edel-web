"""merge every source into candidate photos per product (run locally, writes tools/fotos/cands.json)"""
import json, re, os, glob, collections
D = 'tools/fotos/'
P = json.load(open(D + 'productos.json'))
STOP = set('de del la el los las con sin para por y x en a u unidad metro mts mt c/u'.split())
SYN = {'termomagnetico': 'termica', 'termomagnética': 'termica', 'térmica': 'termica', 'interruptor': 'int', 'diferencial': 'disyuntor', 'tomacorriente': 'toma', 'lámpara': 'lampara', 'módulo': 'modulo', 'combinación': 'combinacion'}
def norm(s): return re.sub(r'[^a-z0-9]', '', str(s).lower())
def toks(s):
    s = s.lower().replace('×', 'x')
    s = re.sub(r'(\d)\s*x\s*(\d)', r'\1x\2', s)
    out = []
    for t in re.split(r'[^\wñáéíóú/.,x]+', s):
        t = t.strip('.,/')
        if not t or t in STOP: continue
        t = SYN.get(t, t)
        t = t.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
        out.append(t.replace(',', '.'))
    return out
def sim(a, b):
    A, B = set(toks(a)), set(toks(b))
    if not A or not B: return 0
    nums = {t for t in A if re.search(r'\d', t)}
    s = len(A & B) / len(A | B)
    if nums: s += 0.25 * len(nums & B) / len(nums) - 0.15 * (len(nums - B) > 0 and len({t for t in B if re.search(r'\d', t)}) > 0)
    return s
# ---- sources: list of (brand_or_None, title, img, url, skus/codes, source)
SRC = collections.defaultdict(list)   # brand(norm) -> items
CODE = {}                              # (brand, code) -> item
for site, items in json.load(open(D + 'crawl/shopify.json')).items():
    brand = 'jeluz' if 'jeluz' in site else None
    for it in items:
        b = brand or norm(it['v'])
        rec = {'t': it['t'], 'i': it['i'][0], 'u': it['u'], 'src': site.split('//')[1]}
        SRC[b].append(rec)
        for k in it['sku']: CODE[(b, norm(k))] = rec
for f in glob.glob(D + 'crawl/*.json'):
    if f.endswith('shopify.json'): continue
    b = os.path.basename(f)[:-5]; d = json.load(open(f))
    for i, pg in enumerate(d['pages']):
        if not pg['i']: continue
        rec = {'t': pg['t'], 'i': pg['i'], 'u': pg['u'], 'src': pg['u'].split('/')[2]}
        if len(pg.get('c', [])) <= 2: SRC[b].append(rec)
        if len(pg.get('c', [])) == 1: CODE.setdefault((b, norm(pg['c'][0])), rec)
EASY = json.load(open(D + 'easy.json')) if os.path.exists(D + 'easy.json') else {}
out = {}
for x in P:
    b = norm(x['b']); cands = []
    if (b, norm(x['k'])) in CODE:
        r = CODE[(b, norm(x['k']))]; cands.append(dict(r, sc=2.0, why='código'))
    for r in SRC.get(b, []):
        s = sim(x['n'], r['t'])
        if s >= 0.28: cands.append(dict(r, sc=round(s, 2), why='nombre'))
    for r in EASY.get(x['id'], []):
        s = sim(x['n'], r['t'])
        if s >= 0.12: cands.append({'t': r['t'], 'i': r['i'], 'u': r['u'], 'src': 'easy', 'sc': round(s, 2), 'why': 'easy'})
    seen = set(); best = []
    for c in sorted(cands, key=lambda c: -c['sc']):
        if c['i'] in seen: continue
        seen.add(c['i']); best.append(c)
    if best: out[x['id']] = best[:4]
json.dump(out, open(D + 'cands.json', 'w'), ensure_ascii=False)
byb = collections.Counter(x['b'] for x in P if x['id'] in out)
print('con candidatos', len(out), 'por código', sum(1 for v in out.values() if v[0]['why'] == 'código'))
print(byb.most_common(25))
