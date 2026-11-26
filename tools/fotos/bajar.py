"""download the chosen photos, put them on a white square and point fotos.json at them"""
import json, urllib.request, io, os, hashlib, concurrent.futures as cf
from PIL import Image, ImageChops
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'}
E = json.load(open('tools/fotos/elegidas.json'))
os.makedirs('fotos/web', exist_ok=True)
def one(item):
    pid, url = item
    name = 'fotos/web/' + hashlib.md5(pid.encode()).hexdigest()[:12] + '.webp'
    try:
        b = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=30).read()
        im = Image.open(io.BytesIO(b)); im.load(); im = im.convert('RGBA')
        bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im); im = bg.convert('RGB')
        diff = ImageChops.difference(im, Image.new('RGB', im.size, (255, 255, 255))).convert('L').point(lambda v: 255 if v > 12 else 0)
        bb = diff.getbbox() or (0, 0) + im.size
        im = im.crop(bb); s = int(max(im.size) * 1.1)
        c = Image.new('RGB', (s, s), 'white'); c.paste(im, ((s - im.width) // 2, (s - im.height) // 2))
        c.resize((600, 600), Image.LANCZOS).save(name, 'WEBP', quality=82)
        return pid, name
    except Exception as e:
        print('fallo', pid, url[:80], e); return pid, None
with cf.ThreadPoolExecutor(10) as ex: res = list(ex.map(one, E.items()))
F = json.load(open('fotos.json'))
ok = 0
for pid, name in res:
    if name: F[pid] = name; ok += 1
json.dump(F, open('fotos.json', 'w'), ensure_ascii=False, indent=1)
print('ok', ok, 'de', len(E))
