"""baja reemplazos de la revisión 27/11 a tools/fotos/reemp2/<n>.jpg"""
import json, urllib.request, urllib.parse, ssl, os, io
from PIL import Image
C = ssl.create_default_context(); C.check_hostname = False; C.verify_mode = ssl.CERT_NONE
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'}
L = json.load(open('tools/fotos/elegidas_verif.json'))
os.makedirs('tools/fotos/reemp7', exist_ok=True)
import hashlib
for pid, (u, th) in L.items():
    k = hashlib.md5(pid.encode()).hexdigest()[:12]
    ok = False
    for url in ([u] if u else []) + (['https://tse1.mm.bing.net/th?id=' + urllib.parse.quote(th) + '&pid=15.1&w=700&h=700'] if th else []):
        try:
            b = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=60, context=C).read()
            im = Image.open(io.BytesIO(b)).convert('RGB')
            if min(im.size) < 150: continue
            im.save(f'tools/fotos/reemp7/{k}.jpg', quality=92); print(k, 'ok', im.size, url[:60]); ok = True; break
        except Exception as e: print(k, 'error', url[:60], e)
    if not ok: print(k, 'FALLO')
