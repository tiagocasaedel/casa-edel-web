"""fetch a text resource ignoring TLS and grep for patterns"""
import urllib.request, ssl, re, sys
C = ssl.create_default_context(); C.check_hostname = False; C.verify_mode = ssl.CERT_NONE
H = {'User-Agent': 'Mozilla/5.0'}
u, pat = sys.argv[1], sys.argv[2]
b = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=30, context=C).read().decode('utf8', 'ignore')
print('##', len(b))
for m in sorted(set(re.findall(pat, b)))[:200]: print('  ', m)
