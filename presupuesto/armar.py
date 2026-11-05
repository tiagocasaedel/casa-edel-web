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
@font-face{font-family:'Archivo';font-weight:100 900;font-stretch:62% 125%;src:url(ROOT/fonts/archivo.woff2) format('woff2')}
@page{size:A4;margin:0}
*{box-sizing:border-box}
html,body{margin:0;background:#fff}
body{font-family:'Archivo',system-ui,sans-serif;color:#141a38;font-size:10.5pt;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:210mm;min-height:297mm;padding:0 0 18mm;position:relative;display:flex;flex-direction:column}
.band{height:5mm;background:linear-gradient(90deg,#c4302a 0 62%,#22306f 62% 100%)}
header{display:flex;justify-content:space-between;align-items:flex-start;padding:9mm 14mm 6mm}
header img{height:17mm}
header .motto{margin:2mm 0 0;font-size:9pt;color:#4f5670;letter-spacing:.02em}
.doc{text-align:right}
.doc h1{margin:0;font-size:26pt;line-height:1;font-stretch:125%;font-weight:800;letter-spacing:-.03em;color:#22306f}
.doc .meta{margin-top:3mm;font-size:9.5pt;color:#4f5670;line-height:1.5}
.doc .meta b{color:#141a38;font-weight:600}
.client{margin:0 14mm 6mm;display:flex;gap:8mm;background:#f5f3ef;border-radius:3mm;padding:4mm 5mm}
.client div{min-width:0}
.client small{display:block;font-size:7.5pt;text-transform:uppercase;letter-spacing:.12em;color:#4f5670;font-weight:600;margin-bottom:1mm}
.client span{font-weight:600;font-size:11pt}
table{width:calc(100% - 28mm);margin:0 14mm;border-collapse:collapse}
thead th{font-size:7.5pt;text-transform:uppercase;letter-spacing:.1em;color:#fff;background:#22306f;font-weight:600;padding:2.6mm 2.5mm;text-align:left}
thead th:first-child{border-radius:2mm 0 0 2mm}thead th:last-child{border-radius:0 2mm 2mm 0}
th.r,td.r{text-align:right}
tbody td{padding:2.4mm 2.5mm;border-bottom:.25mm solid #e7e3da;vertical-align:middle}
tbody tr{break-inside:avoid}
tbody tr:nth-child(even) td{background:#fbfaf8}
.ph{width:13mm;height:13mm;border-radius:2mm;background:#fff center/contain no-repeat;box-shadow:inset 0 0 0 .25mm #e7e3da}
.nm{font-weight:600;line-height:1.25}
.sub{font-size:8.5pt;color:#4f5670;margin-top:.6mm}
.alq{font-weight:700;font-size:11pt;font-stretch:90%}
.emp{font-size:7.5pt;color:#4f5670}
.num{font-variant-numeric:tabular-nums;white-space:nowrap}
.q b{font-size:11pt}
.tag{display:inline-block;margin-left:1.5mm;font-size:7.5pt;font-weight:700;color:#c4302a}
.tot{display:flex;justify-content:space-between;align-items:flex-start;gap:10mm;margin:6mm 14mm 0;break-inside:avoid}
.notes{flex:1;font-size:8.8pt;color:#4f5670;line-height:1.5}
.notes h4{margin:0 0 1.5mm;font-size:7.5pt;text-transform:uppercase;letter-spacing:.12em;color:#141a38}
.notes ul{margin:0;padding-left:4mm}
.sum{width:78mm}
.sum .l{display:flex;justify-content:space-between;padding:1.6mm 0;font-size:10pt}
.sum .l.d{color:#c4302a;font-weight:600}
.sum .big{margin-top:2mm;background:#c4302a;color:#fff;border-radius:3mm;padding:4mm 5mm;display:flex;justify-content:space-between;align-items:baseline}
.sum .big span{font-size:9pt;text-transform:uppercase;letter-spacing:.12em;font-weight:600}
.sum .big b{font-size:19pt;font-stretch:80%;font-weight:800}
.miss{margin:5mm 14mm 0;font-size:9pt;border:.3mm dashed #c27a3a;border-radius:3mm;padding:3mm 4mm;color:#6b4a22;break-inside:avoid}
footer{position:absolute;left:0;right:0;bottom:0;height:18mm;background:#141a38;color:#e8e9f0;display:flex;align-items:center;justify-content:space-between;padding:0 14mm;font-size:8.3pt;line-height:1.45}
footer b{color:#fff}
footer .wa{background:#25d366;color:#08331a;font-weight:700;padding:2mm 3.5mm;border-radius:99mm;font-size:9pt}
"""

def page_html(order, data):
    rows, sub, dx, dto, total, now, numero, vd = data
    hasimg = any(r['img'] for r in rows)
    tr = []
    for r in rows:
        ph = f'<td><div class="ph" style="background-image:url(\'{(ROOT / r["img"]).as_uri()}\')"></div></td>' if hasimg and r['img'] else ('<td></td>' if hasimg else '')
        extra = ' · '.join(x for x in [r['pres'], r['marca']] if x)
        dp = f'<span class="tag">−{fmt_q(r["dp"])}%</span>' if r['dp'] else ''
        tr.append(f"""<tr>{ph}<td><div class="alq num">{esc(r['alq'] or '—')}</div><div class="emp">{esc(r['cod'])}</div></td>
<td><div class="nm">{esc(r['name'])}</div>{f'<div class="sub">{esc(extra)}</div>' if extra else ''}</td>
<td class="r q num"><b>{fmt_q(r['q'])}</b> <span class="emp">{esc(r['uni'])}</span></td>
<td class="r num">{money(r['unit'])}{dp}</td><td class="r num"><b>{money(r['tot'])}</b></td></tr>""")
    cli = [(k, order.get(k)) for k in ('cliente', 'contacto') if order.get(k)]
    clihtml = ''.join(f'<div><small>{"Cliente" if k=="cliente" else "Contacto"}</small><span>{esc(v)}</span></div>' for k, v in cli)
    clihtml += f'<div><small>Artículos</small><span>{len(rows)}</span></div>'
    if order.get('nota'): clihtml += f'<div style="flex:1"><small>Nota</small><span style="font-weight:500;font-size:10pt">{esc(order["nota"])}</span></div>'
    miss = order.get('faltantes') or []
    misshtml = f'<div class="miss"><b>No incluido en este presupuesto:</b> {esc("; ".join(miss))}. Consultanos y te lo cotizamos aparte.</div>' if miss else ''
    venc = (now + datetime.timedelta(days=vd)).strftime('%d/%m/%Y')
    dline = f'<div class="l d"><span>Descuento especial {fmt_q(dx)}%</span><span class="num">− {money(dto)}</span></div>' if dx else ''
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS.replace('ROOT', ROOT.as_uri())}</style></head><body>
<div class="page"><div class="band"></div>
<header><div><img src="{(ROOT/'img/logo-casaedel.png').as_uri()}" alt="Electricidad Casa Edel"><p class="motto">La casa amiga del gremio</p></div>
<div class="doc"><h1>Presupuesto</h1><div class="meta">N° <b>{esc(numero)}</b><br>Fecha <b>{now.strftime('%d/%m/%Y')}</b><br>Válido hasta <b>{venc}</b></div></div></header>
<div class="client">{clihtml}</div>
<table><thead><tr>{'<th style="width:15mm"></th>' if hasimg else ''}<th style="width:22mm">Código</th><th>Artículo</th><th class="r" style="width:22mm">Cant.</th><th class="r" style="width:27mm">Unitario</th><th class="r" style="width:29mm">Subtotal</th></tr></thead>
<tbody>{''.join(tr)}</tbody></table>
{misshtml}
<div class="tot"><div class="notes"><h4>Condiciones</h4><ul>
<li>Precios finales con IVA incluido, válidos por {vd} día{'s' if vd != 1 else ''}.</li>
<li>Sujeto a confirmación de stock al momento de la compra.</li>
<li>Retiro en cualquiera de nuestros locales o entrega a coordinar.</li></ul></div>
<div class="sum"><div class="l"><span>Subtotal</span><span class="num">{money(sub)}</span></div>{dline}
<div class="big"><span>Total</span><b class="num">{money(total)}</b></div></div></div>
<footer><div><b>Casa central</b> · Marcial Candioti 2906, Santa Fe · Lun a vie 7:30 a 16:30<br><b>Casa Edel Express</b> · Av. Aristóbulo del Valle 5837 · Lun a vie 8 a 17 · Sáb 9:30 a 12:30</div>
<div class="wa">WhatsApp +54 9 342 595-6706</div></footer>
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
