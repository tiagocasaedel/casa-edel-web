"""debug: list image urls found on some pages"""
import urllib.request, re, sys, html
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36', 'Accept-Language': 'es-AR,es;q=0.9'}
for u in sys.argv[1:]:
    try: b = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=25).read().decode('utf8', 'ignore')
    except Exception as e: print('##', u, 'ERR', e); continue
    t = re.search(r'<title>(.*?)</title>', b, re.S)
    print('##', u, len(b), (t.group(1).strip()[:80] if t else ''))
    seen = []
    for m in re.finditer(r'''(?:src|data-src|data-zoom-image|href|content|data-lazy)=["']([^"']+\.(?:jpe?g|png|webp)[^"']*)|url\(["']?([^"')]+\.(?:jpe?g|png|webp))''', b, re.I):
        x = html.unescape(m.group(1) or m.group(2))
        if x not in seen: seen.append(x)
    for x in seen[:25]: print('   ', x)
