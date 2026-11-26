"""probe a site ignoring TLS errors: print links and images"""
import urllib.request, ssl, re, sys, html
C = ssl.create_default_context(); C.check_hostname = False; C.verify_mode = ssl.CERT_NONE
H = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36'}
for u in sys.argv[1:]:
    try: b = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=30, context=C).read().decode('utf8', 'ignore')
    except Exception as e: print('##', u, 'ERR', e); continue
    print('##', u, len(b))
    ls = []
    for m in re.finditer(r'(?:href|src)=["\']([^"\'#]+)', b):
        x = html.unescape(m.group(1))
        if x not in ls: ls.append(x)
    for x in ls[:120]: print('  ', x)
