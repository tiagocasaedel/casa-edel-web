"""Busca artículos en el LISTADO.XLS de Alquimia.
Uso: python3 buscar.py LISTADO.XLS "cable 2,5 rojo" "termica 2x20" ...
Cada palabra tiene que aparecer en la descripción, la marca o los códigos (sin importar tildes ni mayúsculas).
Muestra: cod_art (Alquimia) | cod_aso (empresa) | descripción | precio de lista | precio web (-35%)."""
import sys, re, unicodedata, xlrd, json
def norm(s): return re.sub(r'\s+',' ',unicodedata.normalize('NFD',str(s)).encode('ascii','ignore').decode().lower().replace('.',',')).strip()
def load(path):
    sh = xlrd.open_workbook(path).sheet_by_index(0)
    h = [str(c).strip() for c in sh.row_values(0)]
    rows = []
    for i in range(1, sh.nrows):
        r = dict(zip(h, sh.row_values(i)))
        try: pr = float(r.get('precio') or 0)
        except: continue
        cot = float(r.get('cotizacion') or 1) or 1
        rows.append({'alq': str(r.get('cod_art','')).strip().split('.')[0], 'cod': str(r.get('cod_aso','')).strip(),
                     'desc': str(r.get('des_art','')).strip(), 'marca': str(r.get('nom_marca','')).strip(),
                     'lista': round(pr * cot, 2)})
    return rows
if __name__ == '__main__':
    rows = load(sys.argv[1]); out = '--json' in sys.argv
    for q in [a for a in sys.argv[2:] if a != '--json']:
        toks = norm(q).split()
        hits = [r for r in rows if all(t in norm(r['desc']+' '+r['marca']+' '+r['cod']+' '+r['alq']) for t in toks)]
        if out: print(json.dumps({'q': q, 'hits': hits[:15]}, ensure_ascii=False)); continue
        print(f'\n## {q}  ({len(hits)} resultados)')
        for r in hits[:15]:
            print(f"{r['alq']:>7} | {r['cod']:<14} | {r['desc'][:70]:<70} | lista $ {r['lista']:>12,.2f} | web $ {r['lista']*0.65:>12,.2f}")
