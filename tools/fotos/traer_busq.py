"""pull browser image-search results from the temporary Supabase table -> cands4.json + q/rev4.json (ranked)"""
import json, urllib.request, re
D = 'tools/fotos/'
exec(open(D + 'match.py').read().split('# ---- sources')[0])
U = 'https://pduvxjjvtedpykgwlews.supabase.co/rest/v1/tmp_img_busqueda?select=id,res&limit=5000'
K = 'sb_publishable_qJQBYucTCga_qpEh_g6yxQ_8o'
rows = json.loads(urllib.request.urlopen(urllib.request.Request(U, headers={'apikey': K, 'Authorization': 'Bearer ' + K})).read())
P = {x['id']: x for x in json.load(open(D + 'productos.json'))}; F = json.load(open('fotos.json'))
C = {}
for r in rows:
    x = P.get(r['id'])
    if not x or not (F.get(x['id']) or '').startswith(('fotos/r3d/', 'fotos/ref/')): continue
    k = norm(x['k']); cs = []
    for n, c in enumerate(r['res'] or []):
        hay = norm(c['t'] + ' ' + c['u'] + ' ' + c['i']); kc = len(k) >= 4 and k in hay
        cs.append(dict(c, sc=round(sim(x['n'], c['t']) + (1 if kc else 0) - 0.03 * n, 2), why='código' if kc else 'web', src=(c['u'].split('/') + ['', '', ''])[2]))
    cs.sort(key=lambda c: -c['sc'])
    if cs: C[x['id']] = cs[:4]
out = sorted(C, key=lambda p: (P[p]['b'], P[p]['n']))
json.dump(C, open(D + 'cands4.json', 'w'), ensure_ascii=False); json.dump(out, open(D + 'q/rev4.json', 'w'))
print('filas', len(rows), 'para revisar', len(out))
