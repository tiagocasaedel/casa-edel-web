"""search product photos on the web for a batch, keep candidate URLs and build review sheets"""
import json, urllib.request, urllib.parse, re, sys, os, io, html, concurrent.futures as cf
from PIL import Image, ImageDraw, ImageFont
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36', 'Accept-Language': 'es-AR,es;q=0.9'}
def get(u, t=15, h=H):
    try:
        r = urllib.request.urlopen(urllib.request.Request(u, headers=h), timeout=t); return r.read()
    except Exception: return b''
def bing(q):
    b = get('https://www.bing.com/images/async?q=' + urllib.parse.quote(q) + '&first=0&count=30&mmasync=1').decode('utf8', 'ignore')
    out = []
    for m in re.finditer(r'm="(\{.*?\})"', b):
        try: d = json.loads(html.unescape(m.group(1)))
        except Exception: continue
        if d.get('murl'): out.append({'u': d['murl'], 't': d.get('t', ''), 'p': d.get('purl', ''), 's': 'bing'})
    return out
def ddg_pages(q):
    b = get('https://html.duckduckgo.com/html/?q=' + urllib.parse.quote(q)).decode('utf8', 'ignore')
    urls = []
    for m in re.finditer(r'uddg=([^&"]+)', b):
        u = urllib.parse.unquote(m.group(1))
        if u not in urls: urls.append(u)
    out = []
    for u in [u for u in urls if not re.search(r'youtube|facebook|instagram|pinterest|\.pdf', u)][:6]:
        p = get(u, 12).decode('utf8', 'ignore')
        for rx in (r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image'):
            m = re.search(rx, p)
            if m:
                t = re.search(r'<title>(.*?)</title>', p, re.S)
                out.append({'u': urllib.parse.urljoin(u, html.unescape(m.group(1))), 't': html.unescape(t.group(1).strip())[:120] if t else '', 'p': u, 's': 'ddg'}); break
    return out
def thumb(u):
    b = get(u, 12)
    if len(b) < 2000: return None
    try:
        im = Image.open(io.BytesIO(b)); im.load()
        if min(im.size) < 150: return None
        im = im.convert('RGBA'); bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im); im = bg.convert('RGB')
        im.thumbnail((150, 150)); c = Image.new('RGB', (150, 150), 'white'); c.paste(im, ((150 - im.width) // 2, (150 - im.height) // 2)); return c
    except Exception: return None
def main(batch):
    Q = json.load(open(f'tools/fotos/q/{batch}.json'))
    res = {}
    def one(x):
        c = ddg_pages(x['q'])
        if len(c) < 2: c += ddg_pages(x['q2'])
        good = []
        for cand in c:
            th = thumb(cand['u'])
            if th: good.append((cand, th))
            if len(good) == 5: break
        return x, good
    with cf.ThreadPoolExecutor(3) as ex: results = list(ex.map(one, Q))
    os.makedirs('tools/fotos/r', exist_ok=True); os.makedirs('tools/fotos/s', exist_ok=True)
    font = ImageFont.load_default()
    rows = 12; S = 150; L = 260
    for si in range(0, len(results), rows):
        chunk = results[si:si + rows]
        sh = Image.new('RGB', (L + 5 * S, len(chunk) * (S + 6)), 'white'); d = ImageDraw.Draw(sh)
        for r, (x, good) in enumerate(chunk):
            y = r * (S + 6); d.line([(0, y + S + 3), (L + 5 * S, y + S + 3)], fill='#bbb')
            words = (str(si + r) + ') ' + x['n']).split(); lines = ['']
            for w in words:
                if len(lines[-1]) + len(w) > 34: lines.append('')
                lines[-1] += w + ' '
            for i, ln in enumerate(lines[:7]): d.text((4, y + 4 + i * 14), ln, fill='black', font=font)
            d.text((4, y + S - 16), 'cod ' + x.get('k', ''), fill='#555', font=font)
            for i, (cand, th) in enumerate(good):
                sh.paste(th, (L + i * S, y)); d.rectangle([L + i * S, y, L + i * S + 14, y + 12], fill='black'); d.text((L + i * S + 3, y), str(i), fill='white', font=font)
        sh.save(f'tools/fotos/s/{batch}_{si // rows:02d}.jpg', quality=70)
    for x, good in results: res[x['id']] = [c for c, _ in good]
    json.dump(res, open(f'tools/fotos/r/{batch}.json', 'w'), ensure_ascii=False)
if __name__ == '__main__':
    for b in sys.argv[1:] or sorted(f[:-5] for f in os.listdir('tools/fotos/q') if not os.path.exists(f'tools/fotos/r/{f}')):
        main(b)
