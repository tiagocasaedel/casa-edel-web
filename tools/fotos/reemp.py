"""baja fotos de reemplazo (para sacar marcas de agua de otros comercios) a tools/fotos/reemp/<clave>.jpg"""
import urllib.request, ssl, os, io
from PIL import Image
C = ssl.create_default_context(); C.check_hostname = False; C.verify_mode = ssl.CERT_NONE
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'}
L = {
 'farol': ['https://www.iniciativasnuevas.com.ar/img/productos/grandes/farol-cuadrado-para-columna_92.png','OIP.5bKalUA5qTFL7veCfnCNTAHaHa'],
 'farolrect': ['https://lumipack.com.ar/wp-content/uploads/2018/09/Farol-de-3-caras-aplique-GRANDE.jpg','OIP.XG9paCaCukOktdMk0A3TTgHaHa'],
 'cable075cel': ['https://http2.mlstatic.com/D_NQ_NP_923776-MLA90658889799_082025-O.webp','OIP.ngcnadvgkrIgTqP5jhhGvQHaGe'],
 'campana': ['https://http2.mlstatic.com/D_Q_NP_2X_714203-MLA96182587623_102025-E.webp','OIP.Qn1jG7kYIYEyyrQrJzZpwwHaHa'],
 'variador': ['https://f.fcdn.app/imgs/dad4d5/www.luminotecnia.com.py/lminpy/1a25/original/catalogo/MOL000061_MOL000061_0/1920-1200/interruptor-variador-de-ventilador-300w-atenea-blanco-interruptor-variador-de-ventilador-300w-atenea-blanco.jpg','OIP.O1Dsw4K3YYu5QvRKrhsaIgHaFj'],
 'ly2': ['https://http2.mlstatic.com/D_NQ_NP_784904-MLA45739804688_042021-O.webp','OIP.6XTzxAcj5ZiyHiDZrVjtfAAAAA'],
 'velben': ['https://http2.mlstatic.com/D_NQ_NP_714150-MLA92279339246_092025-O.webp','OIP.smF6nLkDtN5tmh8zIfw9iQHaHb'],
 'cerradura': ['https://http2.mlstatic.com/D_NQ_NP_989195-MPE70589347586_072023-O.webp','OIP.qiZCwikKPfX9AkxlqFb90AHaG2'],
 'buscapolo': ['https://gigawatt.com.ar/wp-content/uploads/2026/04/POLEDETECT_0.jpg','OIP.SwZu0qM9xZPo4xyHqq96bQHaHa'],
 'luznegra': ['https://cdn.elgrantlapalero.com/media/catalog/product/cache/74c1057f7991b4edb2bc7bdaa94de933/a/d/ad14350_1.jpg','OIP.68nRs66ZAmPR3DxC4hygYgHaHa'],
 'tecltoma': ['http://www.teclastar.com.ar/img/productos/usos-especiales-2-45284.jpg','OIP.t1fJ3zpZ5aiDak17c64nnQAAAA'],
 'par38': ['https://http2.mlstatic.com/D_NQ_NP_698827-MLU73579840898_122023-O.webp','OIP.VA_hKTCXOQuDwrqOyEBwDQAAAA'],
 'fwbidir': ['https://fwiluminacionsrl.com.ar/img/productos/grandes/2850-2b.jpg','OIP.8ZdG7BNhTxZcxfwBw0iqeQHaF7'],
 'cable150neg': ['https://http2.mlstatic.com/D_NQ_NP_694831-MLA94156789393_102025-O.webp','OIP.9OnNTKYATgK7_iV8hA7pzwHaF0'],
 'cable250mar': ['https://http2.mlstatic.com/D_NQ_NP_841313-MLA90580466557_082025-O.webp','OIP.DtlJXP1qi8qc4VV87GuiOgHaGW'],
}
os.makedirs('tools/fotos/reemp', exist_ok=True)
for k, (u, th) in L.items():
    ok = False
    for url in (u, 'https://tse1.mm.bing.net/th?id=' + th + '&pid=15.1&w=600&h=600'):
        try:
            b = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=60, context=C).read()
            im = Image.open(io.BytesIO(b)).convert('RGB')
            if min(im.size) < 120: continue
            im.save(f'tools/fotos/reemp/{k}.jpg', quality=92); print(k, 'ok', im.size, url[:60]); ok = True; break
        except Exception as e: print(k, 'error', url[:60], e)
    if not ok: print(k, 'FALLO')
