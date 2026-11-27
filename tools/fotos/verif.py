"""baja las miniaturas de Bing de la verificación (tmp_img_busqueda) y las publica en la rama huérfana verif-tmp"""
import os
import json, urllib.request, urllib.parse, os, io, ssl, concurrent.futures as cf, subprocess, shutil
from PIL import Image
U='https://pduvxjjvtedpykgwlews.supabase.co/rest/v1/tmp_img_busqueda?select=id,q,res&order=id&offset='+'1000'+'&limit=1000'
K='sb_publishable_qJQBYucTCga_qpEh_g6yxQ_8oQf9VI6'
rows=[]
for off in (0,1000,2000):
    rows+=json.loads(urllib.request.urlopen(urllib.request.Request(U.replace('offset=1000','offset=%d'%off),headers={'apikey':K,'Authorization':'Bearer '+K})).read())
os.makedirs('vt',exist_ok=True); json.dump(rows,open('vt/rows.json','w'),ensure_ascii=False)
C=ssl.create_default_context(); C.check_hostname=False; C.verify_mode=ssl.CERT_NONE
H={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/124 Safari/537.36'}
jobs=[(r['id'],n,c['th']) for r in rows for n,c in enumerate(r['res'] or []) if c.get('th')]
def one(j):
    i,n,th=j
    try:
        b=urllib.request.urlopen(urllib.request.Request('https://tse1.mm.bing.net/th?id='+urllib.parse.quote(th)+'&pid=15.1&w=300&h=300',headers=H),timeout=40,context=C).read()
        im=Image.open(io.BytesIO(b)).convert('RGB'); im.thumbnail((300,300)); os.makedirs(f'vt/{i}',exist_ok=True); im.save(f'vt/{i}/{n}.jpg',quality=80); return 1
    except Exception: return 0
with cf.ThreadPoolExecutor(16) as ex: print('ok',sum(ex.map(one,jobs)),'de',len(jobs))
subprocess.run(['git','worktree','add','--orphan','-b','verif-tmp2','/tmp/wt'],check=True)
shutil.copytree('vt','/tmp/wt/vt')
subprocess.run('cd /tmp/wt && git add -A && git -c user.name=fotos-bot -c user.email=fotos-bot@users.noreply.github.com commit -qm vt && git push -f origin verif-tmp2',shell=True,check=True)
shutil.rmtree('vt')
