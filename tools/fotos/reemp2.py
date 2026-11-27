"""baja reemplazos de la revisión 27/11 a tools/fotos/reemp2/<n>.jpg"""
import urllib.request, urllib.parse, ssl, os, io
from PIL import Image
C = ssl.create_default_context(); C.check_hostname = False; C.verify_mode = ssl.CERT_NONE
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'}
L = {
'24':['https://www.electromisiones.com.ar/2971-large_default/aplique_candil_para_1_luz_gu10_con_perilla_de_encendido_negro.jpg','OIP.LFhHOuAhjPStJJEx2EhGwAHaHa'],
'26':['https://http2.mlstatic.com/D_NQ_NP_898429-MLA82743780228_032025-O.webp','OIP.e7emA55uLBnYs34aGYzmngHaDc'],
'30':['https://www.electromisiones.com.ar/2972-large_default/aplique_candil_c100_para_2_luces_gu10_negro.jpg','OIP.NoLEPV4D3xtkfQpU7VZg-wHaHa'],
'141':['https://www.electromingo.com/wp-content/uploads/2024/03/tor-2.jpg','OIP.GuZFGLp-ilJPG7a4fVba0gHaHa'],
'846':['https://http2.mlstatic.com/D_NQ_NP_634510-MLU72637327669_112023-O.webp','OIP.vMfPQpptrEDLVWiNDJE4TgAAAA'],
'1215':['https://http2.mlstatic.com/D_NQ_NP_739377-MLA46663978688_072021-O.webp','OIP.vy6PgTEKqt1uim_Sa4fsAAHaHY'],
'1571':['https://http2.mlstatic.com/D_NQ_NP_726644-MLV69481155918_052023-O.webp','OIP.XU0i51ZrTXB0Jca-k24XxQAAAA'],
'1588':['https://www.electromisiones.com.ar/12494-home_default/etiqueta_genrod_q_energy_de_riesgo_electrico_110x150mm.jpg','OIP.m3RtzWNuwcrlxE6U5sBtvAAAAA'],
'2045':['https://http2.mlstatic.com/D_NQ_NP_857016-MLU119997180316_112026-O.webp','OIF.2W8CD95uHXPUPZeuBj+Syw'],
'2054':['https://electricidadindustrial.pe/wp-content/uploads/2025/03/222-412.-CONECTOR-DE-EMPALME-2-POLOS.jpg','OIP.jmcr91Ao6mHSwikt6kV3_wHaH3'],
'2191':['https://http2.mlstatic.com/D_NQ_NP_726414-MLA92690963501_092025-O.webp','OIP.Qdzenyj8oE4F62e1biNEaAAAAA'],
'2783':['https://lummina.com.ar/wp-content/uploads/2024/06/D_878420-MLA76921264761_062024-F.jpg','OIP._sqy6uInVyCegEgr1eGa9wHaFr'],
'2786':['https://lummina.com.ar/wp-content/uploads/2022/04/D_689931-MLA47045688455_082021-F.jpg','OIP.TverwWbxD52ClzrhfDWaAgAAAA'],
'2787':['http://dcdn.mitiendanube.com/stores/003/532/784/products/pl022-1-3-cf806b81981faa7f8c17062951075711-640-0.jpg','OIP.kydyamNiD2ZkTaM6bvS-OwHaJ9'],
'2788':['','OIP.4mg9xBUjyFZGOKyKI-RvwAHaFQ'],
'2837':['','OIP.K6ahvaKICiPbfAZMs83KyQHaHa'],
'2924':['','OIP.2lmRNGLMvFx_ANksDcnxVgAAAA'],
'3275':['','OIP.rJVJkMILfVZgIDjBPcegYwHaHa'],
'3511':['','OIP.Sh3bAr02gV5-x47UPzhuLQAAAA'],
'3561':['','OIP.Fh17_vNjM4Eg2yBbZ6b2tQHaHa'],
}
os.makedirs('tools/fotos/reemp2', exist_ok=True)
for k, (u, th) in L.items():
    ok = False
    for url in ([u] if u else []) + ['https://tse1.mm.bing.net/th?id=' + urllib.parse.quote(th) + '&pid=15.1&w=700&h=700']:
        try:
            b = urllib.request.urlopen(urllib.request.Request(url, headers=H), timeout=60, context=C).read()
            im = Image.open(io.BytesIO(b)).convert('RGB')
            if min(im.size) < 150: continue
            im.save(f'tools/fotos/reemp2/{k}.jpg', quality=92); print(k, 'ok', im.size, url[:60]); ok = True; break
        except Exception as e: print(k, 'error', url[:60], e)
    if not ok: print(k, 'FALLO')
