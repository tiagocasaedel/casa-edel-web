"""baja reemplazos de la revisión 27/11 a tools/fotos/reemp2/<n>.jpg"""
import urllib.request, urllib.parse, ssl, os, io
from PIL import Image
C = ssl.create_default_context(); C.check_hostname = False; C.verify_mode = ssl.CERT_NONE
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'}
L = {
'2951':['','OIP.b80SoN0OnDBrEu9EdPNubAAAAA'],
'2952':['','OIP.cBGuj2qQH2safe6MnqJ_VgAAAA'],
'2960':['','OIP.20HI20vevVLZRZv3LxW37gHaHa'],
'2961':['','OIP.MwpkIz1dxDD2JJMf2EHcdgHaHa'],
'2962':['','OIP.yRa-BmDes7W1NzF-s2yO8wHaGj'],
'2963':['','OIP.T-SVWe-QdK4ec-GDTFlOtAAAAA'],
}
os.makedirs('tools/fotos/reemp4', exist_ok=True)
for k, (u, th) in L.items():
    ok = False
    for url in ([u] if u else []) + ['https://tse1.mm.bing.net/th?id=' + urllib.parse.quote(th) + '&pid=15.1&w=700&h=700']:
        try:
            b = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=60, context=C).read()
            im = Image.open(io.BytesIO(b)).convert('RGB')
            if min(im.size) < 150: continue
            im.save(f'tools/fotos/reemp4/{k}.jpg', quality=92); print(k, 'ok', im.size, url[:60]); ok = True; break
        except Exception as e: print(k, 'error', url[:60], e)
    if not ok: print(k, 'FALLO')
