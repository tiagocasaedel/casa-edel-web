import json, urllib.request, urllib.parse, re
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36', 'Accept-Language': 'es-AR,es;q=0.9'}
def get(u):
    try: r = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=20); return r.status, r.read().decode('utf8', 'ignore')
    except Exception as e: return str(e)[:200], ''
out = {}
for q in ['contactor schneider 25a', 'genrod gabinete', 'sica termica 2x16']:
    s, b = get('https://www.easy.com.ar/api/catalog_system/pub/products/search?ft=' + urllib.parse.quote(q) + '&_from=0&_to=4')
    try: out['easy ' + q] = [s, [(p['productName'], p['brand'], p['items'][0]['images'][0]['imageUrl'], p['items'][0].get('referenceId')) for p in json.loads(b)]]
    except Exception as e: out['easy ' + q] = [s, b[:300]]
s, b = get('https://www.se.com/ar/es/product/LC1D25M7/')
m = re.search(r'og:image["\'][^>]+content=["\']([^"\']+)', b); out['se'] = [s, m.group(1) if m else None, len(b)]
for site in ['https://www.sodimac.com.ar', 'https://www.megatone.net', 'https://www.dimelsa.com.ar']:
    s, b = get(site); out[site] = [s, len(b)]
json.dump(out, open('tools/fotos/probe.json', 'w'), ensure_ascii=False, indent=1)
