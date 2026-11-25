import json, urllib.request, urllib.parse, re
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36', 'Accept-Language': 'es-AR,es;q=0.9', 'Accept': 'text/html,application/xhtml+xml'}
def get(u, h=H):
    try: r = urllib.request.urlopen(urllib.request.Request(u, headers=h), timeout=20); return r.status, r.read().decode('utf8', 'ignore')
    except Exception as e: return str(e)[:200], ''
q = 'Schneider contactor tripolar 25A bobina 220V'
out = {}
s, b = get('https://listado.mercadolibre.com.ar/' + urllib.parse.quote(q.replace(' ', '-')))
out['ml'] = [s, b[:1500], re.findall(r'https?://[^"\s]*mlstatic[^"\s]*', b)[:8]]
s, b = get('https://www.bing.com/images/search?q=' + urllib.parse.quote(q) + '&first=1')
out['bing'] = [s, re.findall(r'murl[^,]{0,200}', b)[:5], re.findall(r'https?://[^"\s&]+\.(?:jpg|jpeg|png|webp)', b)[:10], b[:800]]
s, b = get('https://www.google.com/search?tbm=isch&q=' + urllib.parse.quote(q))
out['google'] = [s, re.findall(r'https?://[^"\s\\]+\.(?:jpg|jpeg|png|webp)', b)[:10], len(b)]
s, b = get('https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(q))
out['ddg_html'] = [s, len(b), re.findall(r'uddg=([^&"]+)', b)[:5]]
json.dump(out, open('tools/fotos/probe.json', 'w'), ensure_ascii=False, indent=1)
