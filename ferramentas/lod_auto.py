"""Escolhe sozinho as peças que somem de longe (LOD) de uma espécie, do mesmo jeito que foi feito à mão no Pirococó:
renderiza a criatura no tamanho em que ela aparece na tela (1080p, FOV 70) a 16, 32 e 48 blocos e esconde, em
ordem de custo-benefício (faces economizadas / pixels mudados), os grupos de peças enquanto a imagem mudar no
máximo LIMITE% dos pixels da silhueta (acumulado, em várias vistas).

Saída: modelos/<id>/lods.json  {nível: [regex exata dos nomes das peças]} (lido por exportar_especie.py).
Uso: python lod_auto.py <id>"""
import copy, json, re, sys
from pathlib import Path
import numpy as np

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))
import previa2
from exportar_v7 import altura_opaca
from exportar_especie import carregar_especie

NIVEIS = [(1, 16, 1.0), (2, 32, 2.0), (3, 48, 3.0)]     # (nível, distância em blocos, % máx. acumulado)
VISTAS = ((0, -4), (35, -4), (100, -4), (215, -4))
FUNDO = np.array([30, 33, 39])
PX_POR_UNIDADE_A_1_BLOCO = 1080 / (2 * np.tan(np.radians(35))) / 16    # ~48,2 px por unidade a 1 bloco

def chave(nome):
    """Grupo da peça: o nome sem os sufixos de lado, índice e parte (garra_meio_d -> garra_meio, conta_0_3 -> conta)."""
    partes = nome.split("_")
    while len(partes) > 1 and (partes[-1].isdigit() or len(partes[-1]) == 1): partes.pop()
    return "_".join(partes)

def main(id_):
    esp = carregar_especie(id_)
    modelo = RAIZ / "modelos" / id_ / f"{id_}.bbmodel"
    tmp = RAIZ / "modelos" / id_ / "revisao" / "_lod_tmp.bbmodel"; tmp.parent.mkdir(parents=True, exist_ok=True)
    base = json.loads(modelo.read_text(encoding="utf-8"))
    k = getattr(esp, "ALTURA", 2.45) * 16 / altura_opaca(modelo)
    d0 = previa2.carregar(str(modelo))
    # cantos de todas as faces como faces degeneradas: o enquadramento fica igual mesmo sem as peças escondidas
    extra = [([c, c, c], uv, n) for (cs, uv, n) in d0[0] for c in list(cs) + [[cs[1][i] + cs[2][i] - cs[0][i] for i in range(3)]]]
    faces_de = {e["uuid"]: len(e["faces"]) for e in base["elements"]}
    grupos = {}
    for e in base["elements"]:
        grupos.setdefault(chave(e["name"]), []).append(e)

    cache = {}
    def render(sem, dist):
        """Imagens (uma por vista) sem os uuids de 'sem', na distância 'dist'."""
        chave_c = (frozenset(sem), dist)
        if chave_c in cache: return cache[chave_c]
        novo = copy.deepcopy(base); novo["elements"] = [e for e in novo["elements"] if e["uuid"] not in sem]
        tmp.write_text(json.dumps(novo), encoding="utf-8")
        d1 = previa2.carregar(str(tmp)); d1 = (d1[0] + extra, d1[1])
        esc = PX_POR_UNIDADE_A_1_BLOCO * k / dist
        ims = [np.asarray(previa2.desenhar(d1, y, p, escala=esc, margem=4, fundo=tuple(FUNDO)).convert("RGB")).astype(int) for y, p in VISTAS]
        cache[chave_c] = ims
        return ims

    def dif(sem, dist):
        a_s, b_s = render(set(), dist), render(sem, dist)
        ds = []
        for a, b in zip(a_s, b_s):
            silh = (np.abs(a - FUNDO).max(axis=2) > 8) | (np.abs(b - FUNDO).max(axis=2) > 8)
            ds.append(100 * ((np.abs(a - b).max(axis=2) > 40) & silh).sum() / max(silh.sum(), 1))
        return max(ds)

    # cada grupo sozinho em cada distância
    medida = {}
    for g, els in grupos.items():
        uu = {e["uuid"] for e in els}
        if sum(faces_de[u] for u in uu) < 4: continue
        medida[g] = {dist: dif(uu, dist) for _, dist, _ in NIVEIS}
    removidos, lods = set(), {}
    for nivel, dist, lim in NIVEIS:
        cands = [g for g in medida if g not in removidos and medida[g][dist] < lim]
        custo = lambda g: sum(faces_de[e["uuid"]] for e in grupos[g]) / max(medida[g][dist], 0.05)
        escolhidos = []
        sem = {e["uuid"] for g in removidos for e in grupos[g]}
        for g in sorted(cands, key=custo, reverse=True):
            teste = sem | {e["uuid"] for e in grupos[g]}
            if dif(teste, dist) <= lim:
                sem = teste; escolhidos.append(g); removidos.add(g)
        nomes = sorted({e["name"] for g in escolhidos for e in grupos[g]})
        faces = sum(faces_de[e["uuid"]] for g in escolhidos for e in grupos[g])
        print(f"nível {nivel} ({dist}+ blocos): {len(escolhidos)} grupos, {faces} faces, dif {dif(sem, dist):.1f}% -> {', '.join(escolhidos) or '-'}")
        if nomes: lods[nivel] = ["^(?:" + "|".join(re.escape(n) for n in nomes) + ")$"]
    tmp.unlink(missing_ok=True)
    total = sum(faces_de.values())
    print(f"faces no modelo (antes de otimizar): {total}")
    (RAIZ / "modelos" / id_ / "lods.json").write_text(json.dumps(lods, indent=1, ensure_ascii=False), encoding="utf-8")
    print("->", RAIZ / "modelos" / id_ / "lods.json")

if __name__ == "__main__":
    main(sys.argv[1])
