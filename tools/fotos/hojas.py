"""download candidate thumbnails and build review sheets: tools/fotos/s/<tag>_NN.jpg"""
import json, urllib.request, io, os, sys, concurrent.futures as cf
from PIL import Image, ImageDraw, ImageFont
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'}
D = 'tools/fotos/'
tag = sys.argv[1]
ids = json.load(open(D + f'q/{tag}.json'))
C = json.load(open(D + 'cands.json')); P = {x['id']: x for x in json.load(open(D + 'productos.json'))}
def thumb(u, S=150):
    try:
        b = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=20).read()
        im = Image.open(io.BytesIO(b)); im.load(); im = im.convert('RGBA'); bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im); im = bg.convert('RGB')
        im.thumbnail((S, S)); c = Image.new('RGB', (S, S), 'white'); c.paste(im, ((S - im.width) // 2, (S - im.height) // 2)); return c
    except Exception: return None
jobs = [(pid, j, c['i']) for pid in ids for j, c in enumerate(C.get(pid, [])[:4])]
with cf.ThreadPoolExecutor(12) as ex: th = dict(zip([(a, b) for a, b, _ in jobs], ex.map(lambda t: thumb(t[2]), jobs)))
try: font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 12); small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 10)
except Exception: font = small = ImageFont.load_default()
S, L, R, CW = 150, 250, 8, 160
os.makedirs(D + 's', exist_ok=True)
def wrap(t, n):
    out = ['']
    for w in t.split():
        if len(out[-1]) + len(w) > n: out.append('')
        out[-1] += w + ' '
    return out
for si in range(0, len(ids), R):
    chunk = ids[si:si + R]; rh = S + 36
    sh = Image.new('RGB', (L + 4 * CW, len(chunk) * rh), 'white'); d = ImageDraw.Draw(sh)
    for r, pid in enumerate(chunk):
        y = r * rh; x = P[pid]
        d.line([(0, y + rh - 2), (L + 4 * CW, y + rh - 2)], fill='#999', width=2)
        for i, ln in enumerate(wrap(f"{si + r}) {x['n']}", 30)[:6]): d.text((4, y + 4 + i * 15), ln, fill='black', font=font)
        d.text((4, y + S - 4), f"{x['b']} · {x['k']}", fill='#444', font=small)
        for j, c in enumerate(C.get(pid, [])[:4]):
            im = th.get((pid, j)); X = L + j * CW
            if im: sh.paste(im, (X, y + 2))
            else: d.text((X + 10, y + 60), '(no baja)', fill='red', font=small)
            d.rectangle([X, y + 2, X + 16, y + 16], fill='black'); d.text((X + 4, y + 3), str(j), fill='white', font=small)
            for k, ln in enumerate(wrap(f"[{c['why'][:3]} {c['sc']}] {c['t']}", 28)[:2]): d.text((X, y + S + 4 + k * 12), ln, fill='#225' if c['why'] == 'código' else '#333', font=small)
    sh.save(D + f's/{tag}_{si // R:02d}.jpg', quality=62)
print('ok', len(ids))
