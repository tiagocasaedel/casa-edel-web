"""for matched product pages whose og:image is a logo/banner: collect the page images and keep the 4 biggest as candidates"""
import json, urllib.request, urllib.parse, re, io, html, sys, concurrent.futures as cf
from PIL import Image
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'}
def get(u, n=3000000):
    try: return urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=20).read(n)
    except Exception: return b''
tag = sys.argv[1]
Q = json.load(open(f'tools/fotos/q/{tag}.json'))   # [[id, page_url], ...]
C = json.load(open('tools/fotos/cands.json'))
def one(item):
    pid, page = item
    b = get(page).decode('utf8', 'ignore')
    srcs = []
    for m in re.finditer(r'(?:src|data-src|data-lazy-src|data-original|href)=["\']([^"\']+\.(?:jpe?g|png|webp)(?:\?[^"\']*)?)["\']', b, re.I):
        u = urllib.parse.urljoin(page, html.unescape(m.group(1)))
        if re.search(r'logo|icon|favicon|banner|slider|whatsapp|facebook|instagram|sprite|flag|bg[-_]|fondo', u, re.I): continue
        if u not in srcs: srcs.append(u)
    sized = []
    for u in srcs[:25]:
        d = get(u)
        try:
            im = Image.open(io.BytesIO(d)); w, h = im.size
            if min(w, h) >= 180 and max(w, h) / min(w, h) < 2.2: sized.append((w * h, u))
        except Exception: pass
    sized.sort(reverse=True)
    return pid, [{'i': u, 't': f'{a}px', 'u': page, 'src': 'pagina', 'sc': 1.0, 'why': 'pag'} for a, u in sized[:4]]
with cf.ThreadPoolExecutor(8) as ex: res = dict(ex.map(one, Q))
for pid, c in res.items():
    if c: C[pid] = c
json.dump(C, open('tools/fotos/cands.json', 'w'), ensure_ascii=False)
json.dump([pid for pid, _ in Q], open(f'tools/fotos/q/{tag}_ids.json', 'w'))
print(sum(1 for c in res.values() if c), 'de', len(Q))
