"""Arma el presupuesto de Casa Edel en PDF (A4) y una imagen PNG de cada página.

Uso: python3 armar.py pedido.json salida.pdf
  (la carpeta de este archivo tiene que estar dentro del repo casa-edel-web: usa img/, fonts/, fotos/, products.json)

pedido.json:
{
  "numero": "0042",                 # opcional (si falta: AAMMDD-HHMM)
  "cliente": "Juan Pérez",          # opcional
  "contacto": "342 555-1234",       # opcional
  "validez_dias": 3,                # opcional, por defecto 3
  "descuento_extra": 5,             # opcional: % extra sobre el total (además del 35% web)
  "nota": "Entrega a coordinar",    # opcional
  "items": [
    {"cod": "1007R", "alq": "31", "desc": "Cable Unipolar 1x2,50 mm Rojo", "marca": "Fonseca",
     "presentacion": "Rollo x 100 m", "cant": 2, "unidad": "rollos",
     "lista": 166408.29,            # precio de LISTA unitario (del LISTADO); el web se calcula (-35%)
     "desc_pct": 0}                 # opcional: % extra solo para este renglón
  ],
  "faltantes": ["Lámpara rara que no figura"]   # opcional: cosas pedidas que no se cotizaron
}
"""
import json, sys, os, html, datetime, math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WEB_DTO = 0.35
esc = lambda s: html.escape(str(s or ''))

def money(x):
    s = f"{round(x):,}".replace(',', '.')
    return f"$ {s}"

def fmt_q(q):
    return (f"{q:.2f}".rstrip('0').rstrip('.')).replace('.', ',') if q != int(q) else str(int(q))

def web_index():
    """código empresa -> (nombre web, marca, foto) usando los datos publicados de la web"""
    idx = {}
    try:
        P = json.load(open(ROOT / 'products.json'))
        F = json.load(open(ROOT / 'fotos.json'))
        A = json.load(open(ROOT / 'img/atlas.json'))
    except Exception:
        return idx
    def foto(pid, i):
        if pid in F and (ROOT / F[pid]).exists(): return F[pid]
        a = A.get(i)
        if a and (ROOT / f'img/hd/{a[0]}-{a[1]}.webp').exists(): return f'img/hd/{a[0]}-{a[1]}.webp'
        return None
    for p in P:
        base = foto(p['id'], p.get('i'))
        if p.get('k'): idx.setdefault(p['k'], (p['n'], p.get('b'), base))
        for v in p.get('v') or []:
            if v.get('k'): idx.setdefault(v['k'], (p['n'], p.get('b'), foto(p['id'], v.get('i')) if v.get('i') else base))
    return idx

def build(order):
    W = web_index()
    try: ALQ = json.load(open(ROOT / 'alquimia.json'))
    except Exception: ALQ = {}
    rows, sub = [], 0.0
    for n, it in enumerate(order['items'], 1):
        cod = str(it.get('cod') or '').strip()
        wn = W.get(cod) or W.get(cod.split('/')[0]) or (None, None, None)
        alq = str(it.get('alq') or ALQ.get(cod, '') or '')
        name = it.get('desc') or wn[0] or cod
        marca = it.get('marca') or wn[1] or ''
        img = it.get('foto') or wn[2]
        q = float(it.get('cant') or 1)
        unit = float(it['lista']) * (1 - WEB_DTO) * (1 - float(it.get('desc_pct') or 0) / 100)
        tot = unit * q; sub += tot
        rows.append(dict(n=n, cod=cod, alq=alq, name=name, marca=marca, pres=it.get('presentacion', ''),
                         q=q, uni=it.get('unidad', 'u.'), unit=unit, tot=tot, img=img,
                         dp=float(it.get('desc_pct') or 0)))
    dx = float(order.get('descuento_extra') or 0)
    dto = sub * dx / 100
    total = sub - dto
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))
    numero = order.get('numero') or now.strftime('%y%m%d-%H%M')
    vd = int(order.get('validez_dias') or 3)
    return rows, sub, dx, dto, total, now, numero, vd

CSS = """
@font-face{font-family:'Plex';font-weight:400;src:url(ROOT/fonts/plex-cond-400.woff2) format('woff2')}
@font-face{font-family:'Plex';font-weight:500;src:url(ROOT/fonts/plex-cond-500.woff2) format('woff2')}
@font-face{font-family:'Plex';font-weight:600;src:url(ROOT/fonts/plex-cond-600.woff2) format('woff2')}
@font-face{font-family:'Plex';font-weight:700;src:url(ROOT/fonts/plex-cond-700.woff2) format('woff2')}
@page{size:A4;margin:0}
*{box-sizing:border-box;border-radius:0}
html,body{margin:0;background:#fff}
body{font-family:'Plex',Arial,sans-serif;color:#111;font-size:9.2pt;line-height:1.2;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;min-height:297mm;padding:9mm 12mm 7mm;display:flex;flex-direction:column}
header{display:grid;grid-template-columns:1fr 62mm;gap:8mm;align-items:stretch;padding-bottom:4mm;border-bottom:.5mm solid #1b2a5e}
header img{height:13mm;display:block}
.emp{margin-top:2.5mm;font-size:8pt;color:#333;line-height:1.35}
.emp b{font-weight:600;color:#111}
.doc{border:.3mm solid #1b2a5e;display:flex;flex-direction:column}
.doc h1{margin:0;padding:1.6mm 3mm;background:#1b2a5e;color:#fff;font-size:12pt;font-weight:600;letter-spacing:.14em;text-align:center}
.doc dl{margin:0;padding:1.6mm 3mm;display:grid;grid-template-columns:auto 1fr;gap:.7mm 3mm;font-size:9pt;flex:1;align-content:center}
.doc dt{color:#444}.doc dd{margin:0;text-align:right;font-weight:600}
.client{margin:3mm 0;display:flex;border:.25mm solid #777}
.client div{padding:1.4mm 3mm;border-right:.25mm solid #777;min-width:32mm}
.client div:first-child{flex:1}.client div:last-child{border-right:0}
.client small{display:block;font-size:7.2pt;text-transform:uppercase;letter-spacing:.08em;color:#444;font-weight:500}
.client span{font-weight:600;font-size:10pt}
table{width:100%;border-collapse:collapse;border:.25mm solid #777}
thead{display:table-header-group}
thead th{white-space:nowrap;font-size:7.6pt;text-transform:uppercase;letter-spacing:.06em;color:#fff;background:#1b2a5e;font-weight:600;padding:1.5mm 2mm;text-align:left;border-right:.2mm solid #4a5788}
thead th:last-child{border-right:0}
th.r,td.r{text-align:right}
tbody td{padding:1mm 2mm;border-bottom:.15mm solid #aaa;border-right:.15mm solid #ccc;vertical-align:middle}
tbody td:last-child{border-right:0}
tbody tr{break-inside:avoid}
.nm{font-weight:500}
.sub{font-size:7.8pt;color:#444;font-weight:400}
.nowrap{white-space:nowrap}
.cod{font-weight:600}.ref{font-size:8.2pt;color:#333}
.num{font-variant-numeric:tabular-nums;white-space:nowrap}
.imp{font-weight:600}
.tag{font-size:7.5pt;font-weight:600;margin-left:1mm}
.miss{margin-top:3mm;font-size:8.6pt;border:.25mm solid #777;padding:1.6mm 3mm;break-inside:avoid}
.miss b{font-weight:600}
.tot{display:grid;grid-template-columns:1fr 72mm;gap:8mm;margin-top:3.5mm;break-inside:avoid;align-items:start}
.notes{font-size:8.2pt;color:#222;line-height:1.4}
.notes h4{margin:0 0 .8mm;font-size:7.6pt;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:#111}
.notes ol{margin:0;padding-left:4mm}
.sum{border:.25mm solid #777}
.sum .l{display:flex;justify-content:space-between;padding:1.3mm 3mm;border-bottom:.15mm solid #aaa}
.sum .big{display:flex;justify-content:space-between;align-items:baseline;padding:1.9mm 3mm;background:#1b2a5e;color:#fff}
.sum .big span{font-size:9.5pt;font-weight:600;letter-spacing:.14em}
.sum .big b{font-size:14pt;font-weight:700}
"""

def money2(x):
    a = f"{x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    return f"$ {a}"

def page_html(order, data):
    rows, sub, dx, dto, total, now, numero, vd = data
    tr = []
    for r in rows:
        dp = f'<span class="tag">-{fmt_q(r["dp"])}%</span>' if r['dp'] else ''
        tr.append(f"""<tr><td class="cod num">{esc(r['alq'] or '-')}</td><td class="ref num">{esc(r['cod'])}</td>
<td><div class="nm">{esc(r['name'])}{f' <span class="sub">({esc(r["pres"])})</span>' if r['pres'] else ''}</div></td>
<td class="nowrap">{esc(r['marca'])}</td>
<td class="r num">{fmt_q(r['q'])} {esc(r['uni'])}</td>
<td class="r num">{money2(r['unit'])}{dp}</td><td class="r num imp">{money(r['tot'])}</td></tr>""")
    cells = [('Cliente', order.get('cliente') or '-')]
    if order.get('contacto'): cells.append(('Contacto', order['contacto']))
    cells.append(('Artículos', len(rows)))
    clihtml = ''.join(f'<div><small>{k}</small><span>{esc(v)}</span></div>' for k, v in cells)
    obs = [x for x in [order.get('nota')] if x]
    miss = order.get('faltantes') or []
    if miss: obs.append('No incluido en este presupuesto: ' + '; '.join(miss) + '. Se cotiza aparte a pedido.')
    obshtml = f'<div class="miss"><b>Observaciones.</b> {esc(" ".join(obs))}</div>' if obs else ''
    venc = (now + datetime.timedelta(days=vd)).strftime('%d/%m/%Y')
    dline = f'<div class="l"><span>Descuento especial {fmt_q(dx)}%</span><span class="num">- {money(dto)}</span></div>' if dx else ''
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS.replace('ROOT', ROOT.as_uri())}</style></head><body>
<div class="page">
<header><div><img src="{(ROOT/'img/logo-casaedel.png').as_uri()}" alt="Electricidad Casa Edel">
<div class="emp"><b>Casa central:</b> Marcial Candioti 2906, Santa Fe. Lun a vie 7:30 a 16:30<br><b>Casa Edel Express:</b> Av. Aristóbulo del Valle 5837, Santa Fe. Lun a vie 8 a 17, sáb 9:30 a 12:30<br><b>WhatsApp:</b> +54 9 342 595-6706</div></div>
<div class="doc"><h1>PRESUPUESTO</h1><dl><dt>N°</dt><dd>{esc(numero)}</dd><dt>Fecha</dt><dd>{now.strftime('%d/%m/%Y')}</dd><dt>Válido hasta</dt><dd>{venc}</dd></dl></div></header>
<div class="client">{clihtml}</div>
<table><thead><tr><th style="width:13mm">Código</th><th style="width:22mm">Ref.</th><th>Artículo</th><th style="width:18mm">Marca</th><th class="r" style="width:15mm">Cant.</th><th class="r" style="width:20mm">P. unitario</th><th class="r" style="width:19mm">Importe</th></tr></thead>
<tbody>{''.join(tr)}</tbody></table>
{obshtml}
<div class="tot"><div class="notes"><h4>Condiciones</h4><ol>
<li>Precios finales con IVA incluido, válidos por {vd} día{'s' if vd != 1 else ''}.</li>
<li>Sujeto a confirmación de stock al momento de la compra.</li>
<li>Retiro en cualquiera de nuestros locales o entrega a coordinar.</li></ol></div>
<div class="sum"><div class="l"><span>Subtotal</span><span class="num">{money(sub)}</span></div>{dline}
<div class="big"><span>TOTAL</span><b class="num">{money(total)}</b></div></div></div>
</div></body></html>"""

def main(src, out):
    order = json.load(open(src))
    data = build(order)
    h = page_html(order, data)
    out = Path(out).resolve(); tmp = out.with_suffix('.html'); tmp.write_text(h)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 794, 'height': 1123}, device_scale_factor=2)
        pg.goto(tmp.as_uri()); pg.wait_for_timeout(400)
        pg.pdf(path=str(out), format='A4', print_background=True, prefer_css_page_size=True)
        pg.screenshot(path=str(out.with_suffix('.png')), full_page=True)
        b.close()
    rows, sub, dx, dto, total, *_ = data
    print(f'OK {out}  ·  {len(rows)} artículos  ·  subtotal {money(sub)}  ·  dto {fmt_q(dx)}%  ·  total {money(total)}')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
