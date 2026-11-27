"""Nota de pedido a proveedor de Casa Edel, para imprimir (A4). Mismo estilo que armar.py.

Uso: python3 pedido.py pedido_prov.json salida.pdf

pedido_prov.json:
{
  "proveedor": "Candil",
  "numero": "0001",                  # opcional (si falta: AAMMDD-HHMM)
  "fecha": "13/11/2026",             # opcional (si falta: hoy)
  "descuento_pct": 19,               # opcional: descuento general sobre el subtotal
  "nota": "...",                     # opcional
  "items": [
    {"cod": "PL222218-30 BT", "alq": "8914", "desc": "Plafón LED 18W ...", "cant": 40,
     "precio": 10099.00, "bonif": 0, "obs": ""}
  ]
}
Los precios son los del proveedor (no se aplica el 35% web).
"""
import json, sys, datetime
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from armar import CSS, ROOT, esc, fmt_q

def m2(x):
    return '$ ' + f"{x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

EXTRA = """
td.chk{width:11mm}
.firmas{display:grid;grid-template-columns:1fr 1fr 1fr;gap:8mm;margin-top:16mm;font-size:8pt;color:#333;break-inside:avoid}
.firmas div{border-top:.25mm solid #333;padding-top:1.2mm;text-align:center}
.obs{font-size:8pt}
"""

def html(o):
    now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-3)))
    fecha = o.get('fecha') or now.strftime('%d/%m/%Y')
    numero = o.get('numero') or now.strftime('%y%m%d-%H%M')
    rows, sub, units = [], 0.0, 0
    for it in o['items']:
        q = float(it['cant']); p = float(it['precio']); b = float(it.get('bonif') or 0)
        imp = q * p * (1 - b / 100); sub += imp; units += q
        rows.append(f"""<tr><td class="cod num">{esc(it.get('alq') or '-')}</td><td class="ref num">{esc(it['cod'])}</td>
<td class="nm">{esc(it['desc'])}</td><td class="r num">{fmt_q(q)}</td><td class="r num">{m2(p)}</td>
<td class="r num">{fmt_q(b) + '%' if b else '-'}</td><td class="r num imp">{m2(imp)}</td>
<td class="obs">{esc(it.get('obs') or '')}</td><td class="chk"></td></tr>""")
    dp = float(o.get('descuento_pct') or 0)
    dto = float(o['descuento_monto']) if o.get('descuento_monto') else round(sub * dp / 100, 2); total = sub - dto
    dline = f'<div class="l"><span>Descuento {fmt_q(dp)}%</span><span class="num">- {m2(dto)}</span></div>' if dp else ''
    nota = f'<div class="miss"><b>Observaciones.</b> {esc(o["nota"])}</div>' if o.get('nota') else ''
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS.replace('ROOT', ROOT.as_uri())}{EXTRA}</style></head><body>
<div class="page">
<header><div><img src="{(ROOT/'img/logo-casaedel.png').as_uri()}" alt="Electricidad Casa Edel">
<div class="emp"><b>Casa central:</b> Marcial Candioti 2906, Santa Fe<br><b>Casa Edel Express:</b> Av. Aristóbulo del Valle 5837, Santa Fe<br><b>WhatsApp:</b> +54 9 342 595-6706</div></div>
<div class="doc"><h1>NOTA DE PEDIDO</h1><dl><dt>N°</dt><dd>{esc(numero)}</dd><dt>Fecha</dt><dd>{esc(fecha)}</dd><dt>Uso</dt><dd>Interno</dd></dl></div></header>
<div class="client"><div><small>Proveedor</small><span>{esc(o['proveedor'])}</span></div><div><small>Artículos</small><span>{len(rows)}</span></div><div><small>Unidades</small><span>{fmt_q(units)}</span></div></div>
<table><thead><tr><th style="width:13mm">Código</th><th style="width:28mm">Cód. prov.</th><th>Descripción</th><th class="r" style="width:12mm">Cant.</th>
<th class="r" style="width:21mm">Precio</th><th class="r" style="width:12mm">Bonif.</th><th class="r" style="width:23mm">Importe</th><th style="width:25mm">Promoción</th><th style="width:11mm">Recib.</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>
{nota}
<div class="tot"><div class="notes"><h4>Control de recepción</h4><ol>
<li>Marcar en "Recib." cada renglón al llegar la mercadería.</li>
<li>Anotar al costado faltantes o diferencias de precio con la factura.</li></ol></div>
<div class="sum"><div class="l"><span>Subtotal</span><span class="num">{m2(sub)}</span></div>{dline}
<div class="big"><span>TOTAL</span><b class="num">{m2(total)}</b></div></div></div>
<div class="firmas"><div>Pedido por</div><div>Recibido por</div><div>Fecha de recepción</div></div>
</div></body></html>""", sub, dto, total

def main(src, out):
    o = json.load(open(src))
    h, sub, dto, total = html(o)
    out = Path(out).resolve(); tmp = out.with_suffix('.html'); tmp.write_text(h)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page()
        pg.goto(tmp.as_uri()); pg.wait_for_timeout(400)
        pg.pdf(path=str(out), format='A4', print_background=True, prefer_css_page_size=True)
        b.close()
    print(f'OK {out} · subtotal {m2(sub)} · dto {m2(dto)} · total {m2(total)}')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
