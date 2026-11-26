"""for products still on 3D/reference images, take a sibling's real photo (same product, other colour) and recolour it.
writes fotos/web/<hash>.webp and updates fotos.json; list of (target, source) in tools/fotos/recolor.json"""
import json, re, hashlib, collections, sys, numpy as np
from PIL import Image
from scipy import ndimage
P = json.load(open('tools/fotos/productos.json')); F = json.load(open('fotos.json'))
CW = {'blanco': (238, 238, 235), 'blanca': (238, 238, 235), 'negro': (38, 38, 40), 'negra': (38, 38, 40), 'gris': (128, 130, 133), 'marfil': (236, 228, 205),
      'arena': (205, 190, 160), 'beige': (220, 205, 175), 'rojo': (190, 35, 35), 'roja': (190, 35, 35), 'verde': (40, 110, 60), 'azul': (40, 70, 150),
      'celeste': (120, 180, 220), 'rosa': (235, 170, 190), 'dorado': (200, 160, 80), 'oro': (200, 160, 80), 'cobre': (184, 115, 70), 'plata': (190, 192, 196),
      'plateado': (190, 192, 196), 'plateada': (190, 192, 196), 'platil': (190, 192, 196), 'acero': (170, 172, 175), 'niquel': (175, 175, 172), 'níquel': (175, 175, 172),
      'grafito': (70, 72, 75), 'oxido': (120, 72, 45), 'óxido': (120, 72, 45), 'naranja': (230, 120, 30), 'amarillo': (230, 200, 40), 'marrón': (110, 70, 40),
      'marron': (110, 70, 40), 'violeta': (120, 60, 160), 'bronce': (150, 110, 60), 'bronceada': (150, 110, 60)}
COL = r'\b(' + '|'.join(sorted(CW, key=len, reverse=True)) + r')\b'
def key(x): return (x['b'], re.sub(r'\s+', ' ', re.sub(COL, '', x['n'].lower())).strip(' -'))
def color(x):
    m = re.findall(COL, x['n'].lower()); return m[-1] if m else None
G = collections.defaultdict(list)
for x in P: G[key(x)].append(x)
def bgmask(rgb):
    near = (rgb.min(2) > 240); lab, n = ndimage.label(near)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    return np.isin(lab, list(border))
def recolor(rgb, T):
    rgb = rgb.astype(float); obj = ~bgmask(rgb.astype('uint8'))
    L = rgb.mean(2); sat = (rgb.max(2) - rgb.min(2)) / 255
    sel = obj & (sat < 0.25); m = np.median(L[sel]) if sel.sum() > 50 else 128
    k = 0.45 if np.mean(T) < m else 0.9
    reg = sel & (np.abs(L - m) < 70)
    out = rgb.copy()
    for c in range(3): out[..., c] = np.where(reg, np.clip(T[c] + (L - m) * k, 0, 255), rgb[..., c])
    return out.astype('uint8')
done = []
for x in P:
    if not (F.get(x['id']) or '').startswith(('fotos/r3d/', 'fotos/ref/')): continue
    tc = color(x)
    if not tc: continue
    sibs = [y for y in G[key(x)] if y is not x and (F.get(y['id']) or '').startswith('fotos/web/') and color(y)]
    if not sibs: continue
    y = sibs[0]
    rgb = np.asarray(Image.open(F[y['id']]).convert('RGB'))
    out = recolor(rgb, CW[tc])
    name = 'fotos/web/' + hashlib.md5(x['id'].encode()).hexdigest()[:12] + '.webp'
    Image.fromarray(out).save(name, 'WEBP', quality=84); F[x['id']] = name; done.append([x['id'], y['id']])
json.dump(F, open('fotos.json', 'w'), ensure_ascii=False, indent=1)
json.dump(done, open('tools/fotos/recolor.json', 'w'))
print('recoloreados', len(done))
