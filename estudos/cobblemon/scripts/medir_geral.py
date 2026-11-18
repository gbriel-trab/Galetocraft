# Medição global dos modelos do Cobblemon (ver LEIA_ME.md). Uso: python -I medir_geral.py <pasta_de_trabalho>
import json, sys, os, math, glob, statistics as st
from collections import Counter
from PIL import Image
RAIZ=sys.argv[1]; M=RAIZ+'/repo/M'; T=RAIZ+'/tex/T'
rows=[]; bone_names=Counter(); rot_vals=Counter(); errs=0
for d in sorted(os.listdir(M)):
    for f in glob.glob(f'{M}/{d}/*.geo.json'):
        try: g=json.load(open(f,encoding='utf-8-sig'))
        except Exception as e: errs+=1; continue
        for geo in g.get('minecraft:geometry',[]):
            desc=geo['description']; tw,th=desc.get('texture_width'),desc.get('texture_height')
            bones=geo.get('bones',[]); cubes=[]; per_face=0; planes=0; rotc=0; infl=0; mirror=0
            ys=[];xs=[];zs=[]; minside=[]
            for b in bones:
                bone_names[b['name'].lower()]+=1
                for c in b.get('cubes',[]):
                    cubes.append(c); o=c['origin']; s=c['size']; i=c.get('inflate',0)
                    if isinstance(c.get('uv'),dict): per_face+=1
                    if min(abs(v) for v in s)<1e-6: planes+=1
                    if c.get('rotation') and any(abs(v)>1e-6 for v in c['rotation']):
                        rotc+=1
                        for v in c['rotation']:
                            if abs(v)>1e-6: rot_vals[round(abs(v),1)]+=1
                    if i: infl+=1
                    if c.get('mirror'): mirror+=1
                    xs+= [o[0],o[0]+s[0]]; ys+=[o[1],o[1]+s[1]]; zs+=[o[2],o[2]+s[2]]
                    nz=[abs(v) for v in s if abs(v)>1e-6]
                    if nz: minside.append(min(nz))
            ident=desc.get('identifier','')
            base=os.path.basename(f).replace('.geo.json','')
            png=f'{T}/{d}/{base}.png'
            pw=ph=None
            if os.path.exists(png):
                try: pw,ph=Image.open(png).size
                except: pass
            rows.append(dict(d=d,f=base,tw=tw,th=th,pw=pw,ph=ph,bones=len(bones),cubes=len(cubes),pf=per_face,planes=planes,rot=rotc,infl=infl,mirror=mirror,
                             H=(max(ys)-min(ys)) if ys else 0, W=(max(xs)-min(xs)) if xs else 0, L=(max(zs)-min(zs)) if zs else 0,
                             minside=st.median(minside) if minside else 0))
json.dump(rows,open(RAIZ+'/stats.json','w'))
print('modelos',len(rows),'erros',errs)
def q(k,rs=rows):
    v=sorted(r[k] for r in rs if r[k] is not None)
    return f'{k}: min {v[0]} p10 {v[len(v)//10]} mediana {v[len(v)//2]} p90 {v[9*len(v)//10]} max {v[-1]}'
for k in ['bones','cubes','H','W','L','minside']: print(q(k))
tot=sum(r['cubes'] for r in rows)
for k in ['pf','planes','rot','infl','mirror']: print(k, f'{100*sum(r[k] for r in rows)/tot:.1f}% dos cubos;', f'{100*sum(1 for r in rows if r[k])/len(rows):.0f}% dos modelos usam')
print('tex declarada', Counter(f"{r['tw']}x{r['th']}" for r in rows).most_common(10))
print('png real', Counter(f"{r['pw']}x{r['ph']}" for r in rows).most_common(10))
print('png/declarada', Counter(round(r['pw']/r['tw'],2) for r in rows if r['pw'] and r['tw']).most_common(6))
print('angulos rot cubo', rot_vals.most_common(25))
print('ossos', bone_names.most_common(70))
