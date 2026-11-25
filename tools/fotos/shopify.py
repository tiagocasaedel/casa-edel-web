import json, urllib.request, time, sys
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'}
out = {}
for site in sys.argv[1:] or ['https://latinafy.com', 'https://jeluz.net']:
    items = []
    for page in range(1, 200):
        try: d = json.loads(urllib.request.urlopen(urllib.request.Request(f'{site}/products.json?limit=250&page={page}', headers=H), timeout=30).read())
        except Exception as e: print(site, page, e); break
        ps = d.get('products', [])
        if not ps: break
        for p in ps:
            imgs = [i['src'] for i in p.get('images', [])][:3]
            if imgs: items.append({'t': p['title'], 'v': p.get('vendor', ''), 'i': imgs, 'u': f"{site}/products/{p['handle']}", 'sku': [v.get('sku') for v in p.get('variants', []) if v.get('sku')][:5], 'tags': p.get('tags', [])[:8] if isinstance(p.get('tags'), list) else p.get('tags', '')[:120]})
        time.sleep(0.5)
    out[site] = items; print(site, len(items), flush=True)
import os; os.makedirs('tools/fotos/crawl', exist_ok=True)
json.dump(out, open('tools/fotos/crawl/shopify.json', 'w'), ensure_ascii=False)
