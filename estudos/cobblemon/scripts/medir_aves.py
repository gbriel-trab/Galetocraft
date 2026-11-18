# Tabela de aves e criaturas de fogo do Cobblemon (ver LEIA_ME.md). Uso: python -I medir_aves.py <pasta_de_trabalho>
import json,glob,sys,os
from collections import Counter
D=sys.argv[1]
rows={ (r['d'],r['f']):r for r in json.load(open(D+'/stats.json'))}
SEL=['0255_torchic','0256_combusken','0257_blaziken','0661_fletchling','0662_fletchinder','0663_talonflame','0146_moltres','0250_hooh','0627_rufflet','0628_braviary','0016_pidgey','0018_pidgeot','0397_staravia','0398_staraptor','0722_rowlet','0724_decidueye','0821_rookidee','0823_corviknight','0701_hawlucha','0083_farfetchd','0865_sirfetchd','0733_toucannon','0441_chatot','0006_charizard','0059_arcanine','0448_lucario','0727_incineroar','0815_cinderace','0655_delphox','0144_articuno','0145_zapdos','0085_dodrio']
print(f"{'especie':22} {'H':>5} {'W':>5} {'L':>5} {'cub':>4} {'oss':>4} {'tex':>8} {'plan%':>5} {'rot%':>5} {'infl%':>5} {'bScale':>6} {'H_mundo':>7} {'hitbox':>10} {'altReal':>7}")
for d in SEL:
    name=d.split('_',1)[1]
    r=rows.get((d,name))
    if not r:
        c=[v for k,v in rows.items() if k[0]==d]; 
        if not c: print(d,'?'); continue
        r=c[0]
    sp=glob.glob(f'{D}/sp/S/*/{name}.json'); bs=hb=alt=None
    if sp:
        j=json.load(open(sp[0])); bs=j.get('baseScale'); hb=j.get('hitbox'); alt=j.get('height')
    hm=r['H']*bs/16 if bs else None
    print(f"{name:22} {r['H']:5.1f} {r['W']:5.1f} {r['L']:5.1f} {r['cubes']:4} {r['bones']:4} {str(r['tw'])+'x'+str(r['th']):>8} {100*r['planes']/r['cubes']:5.0f} {100*r['rot']/r['cubes']:5.0f} {100*r['infl']/r['cubes']:5.0f} {bs!s:>6} {hm if hm is None else round(hm,2)!s:>7} {(str(hb['width'])+'x'+str(hb['height'])) if hb else '-':>10} {alt/10 if alt else '-'!s:>7}")
