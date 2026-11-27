"""baja reemplazos de la revisión 27/11 a tools/fotos/reemp2/<n>.jpg"""
import urllib.request, urllib.parse, ssl, os, io
from PIL import Image
C = ssl.create_default_context(); C.check_hostname = False; C.verify_mode = ssl.CERT_NONE
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'}
L = {
'3188':['https://maginelectricidad.com.ar/wp-content/uploads/2025/12/Candil-111.png',''],
}
os.makedirs('tools/fotos/reemp5', exist_ok=True)
for k, (u, th) in L.items():
    ok = False
    for url in ([u] if u else []) + (['https://tse1.mm.bing.net/th?id=' + urllib.parse.quote(th) + '&pid=15.1&w=700&h=700'] if th else []):
        try:
            b = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=60, context=C).read()
            im = Image.open(io.BytesIO(b)).convert('RGB')
            if min(im.size) < 150: continue
            im.save(f'tools/fotos/reemp5/{k}.jpg', quality=92); print(k, 'ok', im.size, url[:60]); ok = True; break
        except Exception as e: print(k, 'error', url[:60], e)
    if not ok: print(k, 'FALLO')
