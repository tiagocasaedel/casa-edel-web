"""download resources ignoring TLS into tools/fotos/dbg/ (for inspection)"""
import urllib.request, ssl, sys, os, re
C = ssl.create_default_context(); C.check_hostname = False; C.verify_mode = ssl.CERT_NONE
H = {'User-Agent': 'Mozilla/5.0'}
os.makedirs('tools/fotos/dbg', exist_ok=True)
for u in sys.argv[1:]:
    try: b = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=60, context=C).read()
    except Exception as e: print('ERR', u, e); continue
    n = re.sub(r'[^a-zA-Z0-9.]+', '_', u.split('//')[1])[-80:]
    open('tools/fotos/dbg/' + n, 'wb').write(b[:3000000]); print(u, len(b))
