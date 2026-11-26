"""search Argentine online electrical stores (Tiendanube / WooCommerce) for each product -> tiendas_<tag>.json"""
import json, urllib.request, urllib.parse, re, sys, time, html, ssl, threading, concurrent.futures as cf
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36', 'Accept-Language': 'es-AR,es;q=0.9'}
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
TN = ['complementoselectricos.com.ar', 'store.sermatel.com.ar', 'e631.com.ar', 'laelectrica.com.ar', 'electrocity.com.ar', 'cavego.ar',
      'www.electricidadmava.com.ar', 'distribuidorabarbiero.mitiendanube.com', 'luzin.com.ar', 'gimenezelectricidad2.mitiendanube.com',
      'sanjosedistribuciones.com.ar', 'www.perbe.com.ar', 'www.proelectric.ar']
WC = ['malpassielectrica.com.ar', 'gencoelec.com.ar', 'www.pimesa.com.ar', 'electrovir.com.ar', 'electrinet.com.ar']
def get(u, t=20):
    try: return urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=t, context=CTX).read(2500000).decode('utf8', 'ignore')
    except Exception: return ''
def tn(store, q):
    b = get(f'https://{store}/search/?q=' + urllib.parse.quote(q)); out = []
    for m in re.finditer(r'<img[^>]+>', b):
        tag = m.group(0)
        src = re.search(r'(?:data-srcset|srcset|data-src|src)=["\']([^"\']*(?:mitiendanube|cloudfront)[^"\']*/products/[^"\' ,]+)', tag)
        alt = re.search(r'alt=["\']([^"\']+)', tag)
        if not src or not alt: continue
        u = src.group(1); u = ('https:' + u) if u.startswith('//') else u
        u = re.sub(r'-(\d+)-(\d+)\.(webp|jpg|png|jpeg)', r'-1024-1024.\3', u)
        if any(o['i'] == u for o in out): continue
        out.append({'t': html.unescape(alt.group(1))[:140], 'i': u, 'u': f'https://{store}/search/?q=' + urllib.parse.quote(q), 'src': store})
        if len(out) >= 4: break
    return out
def wc(store, q):
    b = get(f'https://{store}/wp-json/wc/store/v1/products?per_page=4&search=' + urllib.parse.quote(q)); out = []
    try: js = json.loads(b)
    except Exception: return out
    for p in js if isinstance(js, list) else []:
        if p.get('images'): out.append({'t': html.unescape(p['name'])[:140], 'i': p['images'][0]['src'], 'u': p.get('permalink', ''), 'src': store, 'sku': p.get('sku', '')})
    return out
STOP = set('de del la el los las con sin para por y x en a u unidad metro mts mt c/u'.split())
def query(x):
    w = [t for t in re.sub(r'["()/.,]', ' ', re.sub(r'\bpor (metro|unidad)\b', '', x['n'], flags=re.I)).split() if t.lower() not in STOP][:4]
    return x['b'] + ' ' + ' '.join(w)
tag = sys.argv[1]; Q = json.load(open(f'tools/fotos/q/{tag}.json'))
if len(sys.argv) > 2: Q = Q[:int(sys.argv[2])]
P = {x['id']: x for x in json.load(open('tools/fotos/productos.json'))}
out = {pid: [] for pid in Q}; lock = threading.Lock(); stats = {}
def run_store(store, fn):
    n = 0
    for pid in Q:
        x = P[pid]
        for q in ([f"{x['b']} {x['k']}"] if len(x['k']) >= 4 else []) + [query(x)]:
            r = fn(store, q); time.sleep(0.8)
            if r:
                with lock: out[pid] += r
                n += 1; break
    stats[store] = n; print(store, n, flush=True)
with cf.ThreadPoolExecutor(len(TN) + len(WC)) as ex:
    for s in TN: ex.submit(run_store, s, tn)
    for s in WC: ex.submit(run_store, s, wc)
json.dump(out, open(f'tools/fotos/tiendas_{tag}.json', 'w'), ensure_ascii=False)
print('done', sum(1 for v in out.values() if v), 'de', len(out))
