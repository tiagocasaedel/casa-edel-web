"""crawl brand sites: collect product pages (title, image) and find our supplier codes in them"""
import json, urllib.request, urllib.parse, re, sys, html, gzip, time, threading, concurrent.futures as cf
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36', 'Accept-Language': 'es-AR,es;q=0.9'}
def get(u, n=1500000):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=15); b = r.read(n)
        if b[:2] == b'\x1f\x8b': b = gzip.decompress(b)
        return r.geturl(), b.decode('utf8', 'ignore')
    except Exception: return u, ''
SKIP = re.compile(r'\.(jpg|jpeg|png|gif|webp|svg|pdf|zip|css|js|xml|mp4|ico)(\?|$)|/(cart|carrito|checkout|account|mi-cuenta|login|wp-json|feed|tag|author|wp-admin|cdn-cgi)/|[?&](add-to-cart|orderby|filter|sort|page=\d{2,})', re.I)
def norm(s): return re.sub(r'[^a-z0-9]', '', s.lower())
def crawl(site):
    brand, start, codes, limit = site['brand'], site['start'], site['codes'], site.get('limit', 1500)
    host = urllib.parse.urlparse(start).netloc.replace('www.', '')
    seen, queue, pages = set(), [start], []
    for sm in site.get('sitemaps', []): queue.insert(0, sm)
    ncodes = {norm(c): c for c in codes if len(norm(c)) >= 4}
    found = {}
    t0 = time.time()
    while queue and len(seen) < limit and time.time() - t0 < 1500:
        batch = []
        while queue and len(batch) < 8:
            u = queue.pop(0).split('#')[0]
            if u in seen: continue
            seen.add(u); batch.append(u)
        with cf.ThreadPoolExecutor(8) as ex: res = list(ex.map(get, batch))
        for u, b in res:
            if not b: continue
            if '<urlset' in b or '<sitemapindex' in b:
                locs = re.findall(r'<loc>\s*(.*?)\s*</loc>', b)
                prod = [l for l in locs if re.search(r'product|producto|/p/|item|articulo', l, re.I)]
                queue[:0] = [l for l in locs if l.endswith('.xml') or '.xml' in l] + prod + [l for l in locs if l not in prod and '.xml' not in l]
                continue
            og = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', b) or re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image', b)
            t = re.search(r'<h1[^>]*>(.*?)</h1>', b, re.S) or re.search(r'<title>(.*?)</title>', b, re.S)
            title = html.unescape(re.sub(r'<[^>]+>|\s+', ' ', t.group(1))).strip()[:160] if t else ''
            img = urllib.parse.urljoin(u, html.unescape(og.group(1))) if og else ''
            if not img:
                m = re.search(r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)', b) or re.search(r'"image"\s*:\s*\[?\s*"([^"]+\.(?:jpe?g|png|webp)[^"]*)"', b) or re.search(r'<link[^>]+rel=["\']image_src["\'][^>]+href=["\']([^"\']+)', b)
                if m: img = urllib.parse.urljoin(u, html.unescape(m.group(1)))
            if not img:
                for m in re.finditer(r'<img[^>]+(?:data-src|data-lazy-src|src)=["\']([^"\']+\.(?:jpe?g|png|webp)[^"\']*)', b, re.I):
                    v = m.group(1)
                    if re.search(r'logo|icon|banner|slider|favicon|placeholder|whatsapp|facebook|instagram|flag|footer|header|sprite|loader', v, re.I): continue
                    img = urllib.parse.urljoin(u, html.unescape(v)); break
            nb = norm(re.sub(r'<script.*?</script>', '', b, flags=re.S))
            hits = [c for k, c in ncodes.items() if k in nb]
            if img or hits: pages.append({'u': u, 't': title, 'i': img, 'c': hits[:5]})
            for l in re.findall(r'href=["\']([^"\'#]+)', b):
                l = urllib.parse.urljoin(u, html.unescape(l))
                if urllib.parse.urlparse(l).netloc.replace('www.', '') == host and not SKIP.search(l) and l not in seen: queue.append(l)
    return brand, {'pages': pages, 'found': found, 'seen': len(seen)}
S = json.load(open('tools/fotos/sites.json'))
sel = sys.argv[1:]
S = [s for s in S if not sel or s['brand'] in sel]
out = {}
with cf.ThreadPoolExecutor(6) as ex:
    for brand, r in ex.map(crawl, S): out[brand] = r; print(brand, r['seen'], len(r['pages']), len(r['found']), flush=True)
import os; os.makedirs('tools/fotos/crawl', exist_ok=True)
for b, r in out.items(): json.dump(r, open(f'tools/fotos/crawl/{norm(b)}.json', 'w'), ensure_ascii=False)
