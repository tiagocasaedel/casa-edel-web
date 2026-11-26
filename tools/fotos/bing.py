"""image search (Bing images) for each product: brand + name + code -> up to 6 image candidates"""
import json, urllib.request, urllib.parse, re, sys, time, html
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36', 'Accept-Language': 'es-AR,es;q=0.9'}
BAD = re.compile(r'facebook|instagram|pinterest|tiktok|youtube|logo|banner|aliexpress|alibaba|temu', re.I)
def get(u):
    try: return urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=15).read(1500000).decode('utf8', 'ignore')
    except Exception: return ''
def search(q):
    b = get('https://www.bing.com/images/search?q=' + urllib.parse.quote(q) + '&setlang=es&cc=AR&first=1')
    out = []
    for m in re.finditer(r'\bm="(\{[^"]+\})"', b):
        try: d = json.loads(html.unescape(m.group(1)))
        except Exception: continue
        if not d.get('murl') or BAD.search(d.get('murl', '') + d.get('purl', '')): continue
        out.append({'i': d['murl'], 'th': d.get('turl', ''), 'u': d.get('purl', ''), 't': html.unescape(d.get('t', ''))[:140], 'src': (d.get('purl', '') or '//?').split('/')[2]})
        if len(out) >= 6: break
    return out, len(b)
tag = sys.argv[1]; Q = json.load(open(f'tools/fotos/q/{tag}.json'))
P = {x['id']: x for x in json.load(open('tools/fotos/productos.json'))}
out = {}; ok = 0
for n, pid in enumerate(Q):
    x = P[pid]
    name = re.sub(r'\bpor (metro|unidad)\b', '', x['n'], flags=re.I).strip()
    q = f"{x['b']} {name} {x['k']}" if x['k'] and len(x['k']) >= 3 else f"{x['b']} {name}"
    r, ln = search(q)
    if len(r) < 2:  # retry without code
        time.sleep(1.5); r2, ln = search(f"{x['b']} {name}"); r += [c for c in r2 if c['i'] not in {d['i'] for d in r}]
    out[pid] = {'q': q, 'c': r[:6]}; ok += bool(r)
    if n % 25 == 0: print(n, ok, ln, flush=True)
    time.sleep(1.5)
json.dump(out, open(f'tools/fotos/bing_{tag}.json', 'w'), ensure_ascii=False)
print('done', len(out), ok)
