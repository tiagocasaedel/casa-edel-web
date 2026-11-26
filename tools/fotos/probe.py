"""probe which search engines answer from the runner (repeated queries)"""
import urllib.request, urllib.parse, time, re, json
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36', 'Accept-Language': 'es-AR,es;q=0.9'}
def get(u):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=15); return r.status, r.read(800000).decode('utf8', 'ignore')
    except Exception as e: return str(e)[:60], ''
QS = ['Jeluz plafon led 18w', 'Cambre toma doble 10a', 'Kalop termica 2x20', 'Genrod caja estanca', 'San Justo farol']
E = {
 'bing': 'https://www.bing.com/search?q={}&setlang=es&cc=AR',
 'yahoo': 'https://search.yahoo.com/search?p={}',
 'mojeek': 'https://www.mojeek.com/search?q={}',
 'brave': 'https://search.brave.com/search?q={}',
 'startpage': 'https://www.startpage.com/do/search?q={}',
 'ecosia': 'https://www.ecosia.org/search?q={}',
 'ml': 'https://api.mercadolibre.com/sites/MLA/search?q={}&limit=5',
 'mllista': 'https://listado.mercadolibre.com.ar/{}',
 'yandex': 'https://yandex.com/search/?text={}',
 'qwant': 'https://api.qwant.com/v3/search/web?q={}&count=10&locale=es_AR&offset=0&device=desktop',
}
for name, tpl in E.items():
    res = []
    for q in QS:
        s, b = get(tpl.format(urllib.parse.quote(q.replace(' ', '-') if name == 'mllista' else q)))
        links = len(set(re.findall(r'https?://[a-z0-9.-]+\.[a-z]{2,}/[^"\'<> ]{8,}', b)))
        imgs = len(re.findall(r'http2\.mlstatic\.com[^"]+?\.(?:jpg|webp)', b))
        res.append((s, len(b), links, imgs)); time.sleep(3)
    print(name, res, flush=True)
