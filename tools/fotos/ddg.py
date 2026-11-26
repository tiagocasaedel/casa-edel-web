"""slow web search (DuckDuckGo lite) for products without candidates; page og:image as candidate"""
import json, urllib.request, urllib.parse, re, sys, time, html, os, concurrent.futures as cf
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36', 'Accept-Language': 'es-AR,es;q=0.9'}
def get(u, t=15, data=None):
    try: return urllib.request.urlopen(urllib.request.Request(u, data=data, headers=H), timeout=t).read(1500000).decode('utf8', 'ignore')
    except Exception as e: return ''
BAD = re.compile(r'mercadolibre|facebook|instagram|youtube|pinterest|tiktok|\.pdf|amazon\.|aliexpress|wikipedia|scribd|editores-srl', re.I)
def search(q):
    b = get('https://lite.duckduckgo.com/lite/', data=urllib.parse.urlencode({'q': q, 'kl': 'ar-es'}).encode())
    urls = []
    for m in re.finditer(r'<a[^>]+href="([^"]+)"[^>]*class=.result-link', b) or []:
        u = html.unescape(m.group(1))
        if 'uddg=' in u: u = urllib.parse.unquote(re.search(r'uddg=([^&]+)', u).group(1))
        if u.startswith('http') and not BAD.search(u) and u not in urls: urls.append(u)
    if not urls:
        for m in re.finditer(r'href="(https?://[^"]+)"', b):
            u = html.unescape(m.group(1))
            if 'duckduckgo' in u or BAD.search(u): continue
            if u not in urls: urls.append(u)
    return urls[:5], len(b)
def ogimg(u):
    b = get(u, 12)
    m = re.search(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', b) or re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image', b)
    t = re.search(r'<h1[^>]*>(.*?)</h1>', b, re.S) or re.search(r'<title>(.*?)</title>', b, re.S)
    if not m: return None
    return {'i': urllib.parse.urljoin(u, html.unescape(m.group(1))), 't': html.unescape(re.sub(r'<[^>]+>|\s+', ' ', t.group(1))).strip()[:140] if t else '', 'u': u, 'src': u.split('/')[2]}
tag = sys.argv[1]; Q = json.load(open(f'tools/fotos/q/{tag}.json'))
P = {x['id']: x for x in json.load(open('tools/fotos/productos.json'))}
out = {}; stats = [0, 0]
for n, pid in enumerate(Q):
    x = P[pid]
    q = f"{x['b']} {re.sub(r'por (metro|unidad)', '', x['n'])}"
    urls, ln = search(q)
    stats[0] += 1; stats[1] += bool(urls)
    with cf.ThreadPoolExecutor(5) as ex: c = [r for r in ex.map(ogimg, urls) if r]
    out[pid] = c[:4]
    if n % 20 == 0: print(n, stats, ln, flush=True)
    time.sleep(2.0)
json.dump(out, open(f'tools/fotos/ddg_{tag}.json', 'w'), ensure_ascii=False)
print('done', stats, sum(1 for v in out.values() if v))
