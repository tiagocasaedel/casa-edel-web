"""download files (TLS errors ignored) into dl/ — published as a workflow artifact, not committed.
usage: dl.py <base_url> <listfile.json with relative paths>"""
import urllib.request, urllib.parse, ssl, sys, os, json, concurrent.futures as cf
C = ssl.create_default_context(); C.check_hostname = False; C.verify_mode = ssl.CERT_NONE
H = {'User-Agent': 'Mozilla/5.0'}
base, lst = sys.argv[1], json.load(open(sys.argv[2]))
os.makedirs('dl', exist_ok=True)
def one(rel):
    u = base + urllib.parse.quote(rel)
    try:
        b = urllib.request.urlopen(urllib.request.Request(u, headers=H), timeout=120, context=C).read()
        out = 'dl/' + rel; os.makedirs(os.path.dirname(out), exist_ok=True); open(out, 'wb').write(b); return rel, len(b)
    except Exception as e: return rel, str(e)
with cf.ThreadPoolExecutor(6) as ex:
    for r in ex.map(one, lst): print(*r)
