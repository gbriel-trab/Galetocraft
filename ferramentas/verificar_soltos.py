"""Confere se sobra cubo solto em cada nível de LOD (0..3) de uma espécie: caixas no mundo (com as rotações dos
ossos e das peças), união por sobreposição com folga 0,15; lista os componentes fora do maior. Uso: python verificar_soltos.py <id>"""
import json, re, sys, importlib.util
from pathlib import Path
import numpy as np
RAIZ = Path(r"C:\Users\gbriel\Desktop\galopiru")
sys.path.insert(0, str(RAIZ / "ferramentas"))
from previa import rot, compor, mv, sub

ID = sys.argv[1]
spec = importlib.util.spec_from_file_location("esp", RAIZ / f"ferramentas/especies/{ID}.py")
esp = importlib.util.module_from_spec(spec); spec.loader.exec_module(esp)
lods = getattr(esp, "LODS", None) or {int(k): v for k, v in json.loads((RAIZ / f"modelos/{ID}/lods.json").read_text(encoding="utf-8")).items()} if (RAIZ / f"modelos/{ID}/lods.json").exists() or getattr(esp, "LODS", None) else {}
bb = json.loads((RAIZ / f"modelos/{ID}/{ID}.bbmodel").read_text(encoding="utf-8"))
els = {e["uuid"]: e for e in bb["elements"]}
caixas = []
def emitir(e, M):
    r = e.get("rotation", [0, 0, 0])
    if any(abs(v) > 1e-9 for v in r):
        o = e["origin"]; R = rot(*r); M = compor(M, (R, sub(o, mv(R, o))))
    A, b = M
    a0, a1 = e["from"], e["to"]
    pts = np.array([mv(A, [x, y, z]) for x in (a0[0], a1[0]) for y in (a0[1], a1[1]) for z in (a0[2], a1[2])]) + np.array(b)
    caixas.append((e["name"], pts.min(0), pts.max(0)))
def andar(no, M):
    if isinstance(no, str):
        if no in els: emitir(els[no], M)
        return
    r = no.get("rotation", [0, 0, 0])
    if any(abs(v) > 1e-9 for v in r):
        o = no["origin"]; R = rot(*r); M = compor(M, (R, sub(o, mv(R, o))))
    for f in no["children"]: andar(f, M)
I = ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], [0, 0, 0])
for no in bb["outliner"]: andar(no, I)

def nivel(nome):
    for n in sorted(lods):
        if any(re.search(p, nome) for p in lods[n]): return n
    return 0
for L in range(4):
    vivas = [c for c in caixas if nivel(c[0]) == 0 or nivel(c[0]) > L]
    pai = list(range(len(vivas)))
    def acha(i):
        while pai[i] != i: pai[i] = pai[pai[i]]; i = pai[i]
        return i
    f = 0.15
    for i in range(len(vivas)):
        for j in range(i + 1, len(vivas)):
            a, b = vivas[i], vivas[j]
            if np.all(a[1] - f <= b[2]) and np.all(b[1] - f <= a[2]): pai[acha(i)] = acha(j)
    comp = {}
    for i in range(len(vivas)): comp.setdefault(acha(i), []).append(vivas[i][0])
    grupos = sorted(comp.values(), key=len, reverse=True)
    print(f"{ID} LOD {L}: {len(vivas)} cubos, {len(grupos)} comp." + ("" if len(grupos) == 1 else f" soltos: {sum(len(g) for g in grupos[1:])} -> {[g[:4] for g in grupos[1:6]]}"))
