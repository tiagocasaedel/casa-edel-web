"""exporta los productos visibles (como los ve la web) a tools/fotos/revision/productos.json"""
import urllib.request, json, os
B='https://pduvxjjvtedpykgwlews.supabase.co/rest/v1/'; K='sb_publishable_qJQBYucTCga_qpEh_g6yxQ_8oQf9VI6'
rows=[]; f=0
while True:
    r=urllib.request.Request(B+'productos?select=id,nombre,marca,rubro,subrubro,codigo,codigo_alquimia,foto,variantes,precio&visible=is.true&order=id',headers={'apikey':K,'Authorization':'Bearer '+K,'Range':f'{f}-{f+999}'})
    p=json.load(urllib.request.urlopen(r)); rows+=p; f+=1000
    if len(p)<1000: break
os.makedirs('tools/fotos/revision',exist_ok=True)
json.dump(rows,open('tools/fotos/revision/productos.json','w'),ensure_ascii=False)
print(len(rows))
