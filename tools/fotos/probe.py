import json, urllib.request, urllib.parse, re, sys
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36', 'Accept-Language': 'es-AR,es;q=0.9'}
def get(u, h=H):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers=h), timeout=20); return r.status, r.read()
    except Exception as e: return str(e)[:200], b''
out = {}
q = 'Schneider contactor tripolar 25A bobina 220V LC1D25'
s, b = get('https://api.mercadolibre.com/sites/MLA/search?limit=5&q=' + urllib.parse.quote(q)); out['ml_api'] = [s, b[:600].decode('utf8', 'ignore')]
s, b = get('https://listado.mercadolibre.com.ar/' + urllib.parse.quote(q.replace(' ', '-'))); out['ml_html'] = [s, len(b), re.findall(r'https://http2\.mlstatic\.com/[^"\s]+?\.(?:webp|jpg)', b.decode('utf8', 'ignore'))[:5]]
s, b = get('https://www.bing.com/images/search?q=' + urllib.parse.quote(q) + '&form=HDRSC2'); out['bing'] = [s, len(b), re.findall(r'murl&quot;:&quot;(.*?)&quot;', b.decode('utf8', 'ignore'))[:5]]
s, b = get('https://duckduckgo.com/?q=' + urllib.parse.quote(q) + '&iax=images&ia=images'); vqd = re.search(r'vqd=["\']?([\d-]+)', b.decode('utf8', 'ignore')); out['ddg_vqd'] = [s, vqd.group(1) if vqd else None]
if vqd:
    s, b = get('https://duckduckgo.com/i.js?l=ar-es&o=json&q=' + urllib.parse.quote(q) + '&vqd=' + vqd.group(1) + '&f=,,,&p=1', dict(H, Referer='https://duckduckgo.com/'))
    try: out['ddg'] = [s, [(r['title'], r['image']) for r in json.loads(b)['results'][:5]]]
    except Exception as e: out['ddg'] = [s, str(e), b[:200].decode('utf8', 'ignore')]
json.dump(out, open('tools/fotos/probe.json', 'w'), ensure_ascii=False, indent=1)
