import json, urllib.request, urllib.parse, re, time, concurrent.futures as cf
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'}
def get(u):
    for i in range(3):
        try: return json.loads(urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=20).read())
        except Exception: time.sleep(2)
    return []
P = json.load(open('tools/fotos/productos.json'))
STOP = set('de del la el los las con sin para por y x en a mm cm m u unidad metro'.split())
def q(x):
    w = [t for t in re.sub(r'[^\wñáéíóú/,.-]', ' ', x['n'].lower()).split() if t not in STOP][:5]
    return x['b'] + ' ' + ' '.join(w)
def one(x):
    res = []
    for qq in (q(x), x['b'] + ' ' + x['k']):
        for p in get('https://www.easy.com.ar/api/catalog_system/pub/products/search?ft=' + urllib.parse.quote(qq) + '&_from=0&_to=7'):
            try:
                if p['brand'].lower().strip() != x['b'].lower().strip(): continue
                im = p['items'][0]['images'][0]['imageUrl']
                if all(r['i'] != im for r in res): res.append({'t': p['productName'], 'i': im, 'u': 'https://www.easy.com.ar/' + p.get('linkText', '') + '/p'})
            except Exception: pass
        if res: break
    return x['id'], res[:6]
with cf.ThreadPoolExecutor(6) as ex: out = dict(ex.map(one, P))
json.dump(out, open('tools/fotos/easy.json', 'w'), ensure_ascii=False)
print(sum(1 for v in out.values() if v))
