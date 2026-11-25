import json, urllib.request, re, concurrent.futures as cf
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'}
def get(u):
    try: r = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=12); return r.status, r.geturl(), r.read(400000).decode('utf8', 'ignore')
    except Exception as e: return str(e)[:80], u, ''
C = json.load(open('tools/fotos/dominios_in.json'))
def probe(item):
    brand, doms = item; res = []
    for d in doms:
        for pre in ('https://www.', 'https://'):
            s, fu, b = get(pre + d + '/')
            if b:
                sm = []
                s2, _, rb = get(pre + d + '/robots.txt'); sm += re.findall(r'(?im)^sitemap:\s*(\S+)', rb)
                for p in ('/sitemap.xml', '/sitemap_index.xml', '/product-sitemap.xml'):
                    s3, _, sb = get(pre + d + p)
                    if '<urlset' in sb or '<sitemapindex' in sb: sm.append(pre + d + p)
                t = re.search(r'<title>(.*?)</title>', b, re.S)
                res.append({'d': d, 'final': fu, 'title': t.group(1).strip()[:80] if t else '', 'sitemaps': sorted(set(sm))[:6], 'tn': 'tiendanube' in b or 'nuvemshop' in b, 'woo': 'woocommerce' in b, 'shopify': 'shopify' in b})
                break
    return brand, res
with cf.ThreadPoolExecutor(12) as ex: out = dict(ex.map(probe, C.items()))
json.dump(out, open('tools/fotos/dominios.json', 'w'), ensure_ascii=False, indent=1)
