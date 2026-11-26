"""probe bing image endpoints"""
import urllib.request, urllib.parse, re, time, os
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'
os.makedirs('tools/fotos/dbg', exist_ok=True)
QS = ['Zoloda Canal 100x80 Blanco CKN-100-80-SC-BL', 'Schneider Contactor LC1E0910M7', 'JA Panel plafon LED Redondo 22W', 'Macroled Proyector LED 50W']
V = {
 'html': ('https://www.bing.com/images/search?q={}&form=HDRSC2&first=1', {}),
 'async': ('https://www.bing.com/images/async?q={}&first=0&count=35&mmasync=1', {}),
 'asyncck': ('https://www.bing.com/images/async?q={}&first=0&count=35&mmasync=1', {'Cookie': 'SRCHHPGUSR=ADLT=OFF&HV=1; _EDGE_S=mkt=es-ar'}),
 'htmlen': ('https://www.bing.com/images/search?q={}&mkt=en-US', {'Cookie': 'SRCHHPGUSR=ADLT=OFF'}),
}
for k, (tpl, extra) in V.items():
    for n, q in enumerate(QS):
        h = {'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml', 'Accept-Language': 'es-AR,es;q=0.9,en;q=0.8'}; h.update(extra)
        try: b = urllib.request.urlopen(urllib.request.Request(tpl.format(urllib.parse.quote(q)), headers=h), timeout=20).read().decode('utf8', 'ignore')
        except Exception as e: b = 'ERR ' + str(e)
        m = len(re.findall(r'\bm="\{', b)); mu = len(re.findall(r'murl', b))
        print(k, n, len(b), m, mu, flush=True)
        if n == 0: open(f'tools/fotos/dbg/{k}.html', 'w').write(b)
        time.sleep(2)
