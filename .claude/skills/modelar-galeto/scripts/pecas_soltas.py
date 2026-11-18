"""Procura peças soltas (flutuando, sem encostar no resto) e confere o chão, na pose neutra e ao longo das animações.

É a falha mais comum de modelos 3D feitos por código (3DCodeBench, 2026) e o olho deixa passar fácil em miniatura.

Como mede:
- cada cubo vira uma caixa no espaço do mundo, com a pose aplicada; cubos escondidos (escala 0) ficam de fora;
- dois cubos se tocam quando as caixas se cruzam ou ficam a menos de --folga px (teste de eixos separadores, que
  vale também para planos);
- o maior grupo de cubos ligados é o corpo; os outros grupos são peças soltas;
- nas animações, só aparecem as peças que estavam presas na pose neutra e se soltaram;
- chão: o ponto mais baixo deveria ficar em y = 0 (16 px = 1 bloco); mais de --chao px acima ou abaixo é aviso.
- modelos antigos com ossos `_lodN` (níveis de detalhe): todos os níveis entram juntos, o que pode esconder um vão.

Uso: python pecas_soltas.py MODELO.geo.json [--anim ARQ.animation.json] [--pose NOME@t ...] [--folga 0.25] [--chao 1]
Sem --pose, cada animação é amostrada em 0, 1/4, 1/2 e 3/4 da duração. Sai com código 1 se achar problema.
"""
import argparse, json, sys
from pathlib import Path

import numpy as np


def _achar_ferramentas():
    """analisar_geo.py e previa.py: nesta pasta, no ferramentas/ do repositório ou na skill engenharia-reversa-cobblemon."""
    aqui = Path(__file__).resolve().parent
    candidatos = [aqui] + [p / "ferramentas" for p in aqui.parents] + \
                 [aqui.parent.parent / "engenharia-reversa-cobblemon" / "scripts"]
    for c in candidatos:
        if (c / "analisar_geo.py").exists() and (c / "previa2.py").exists():
            sys.path.insert(0, str(c))
            return c
    sys.exit("não achei analisar_geo.py e previa2.py: rode dentro do repositório Galetocraft ou instale a skill "
             "engenharia-reversa-cobblemon")


_achar_ferramentas()
import analisar_geo as ag  # noqa: E402
from previa import rot, mv, add, sub, compor  # noqa: E402

ALIAS = {"parado": ("ground_idle", "idle"), "andar": ("ground_walk", "walk"), "dormir": ("sleep",)}


# ----------------------------------------------------------------------------------------------------------------
# Caixas no mundo
# ----------------------------------------------------------------------------------------------------------------
def caixas(geo, pose_bedrock=None):
    """[(osso, índice do cubo, 8 cantos (8x3), 3 direções (3x3))] dos cubos visíveis, em px do Blockbench."""
    saida, cont = [], {}
    for osso, c, M in ag.transformar(geo, pose_bedrock):
        i = cont[osso] = cont.get(osso, -1) + 1
        x, y, z = c["origin"]; w, h, d = c["size"]; inf = c.get("inflate", 0)
        de = [-(x + w) - inf, y - inf, z - inf]; ate = [-x + inf, y + h + inf, z + d + inf]
        if c.get("rotation") and any(abs(v) > 1e-9 for v in c["rotation"]):
            px, py, pz = c.get("pivot", [0, 0, 0]); o = [-px, py, pz]
            R = rot(-c["rotation"][0], -c["rotation"][1], c["rotation"][2])
            M = compor(M, (R, sub(o, mv(R, o))))
        A, b = M
        cantos = np.array([add(mv(A, [cx, cy, cz]), b) for cx in (de[0], ate[0]) for cy in (de[1], ate[1])
                           for cz in (de[2], ate[2])])
        E = np.array([cantos[4] - cantos[0], cantos[2] - cantos[0], cantos[1] - cantos[0]])
        n = np.linalg.norm(E, axis=1)
        if (n > 1e-4).sum() < 2:          # escondido (escala 0) ou uma linha: não aparece
            continue
        D = E.copy()
        if (n > 1e-4).sum() == 2:          # plano: a direção da espessura é a normal
            i0 = int(np.argmin(n)); j, k = [a for a in range(3) if a != i0]
            D[i0] = np.cross(E[j], E[k])
        D = D / np.linalg.norm(D, axis=1, keepdims=True)
        saida.append((osso, i, cantos, D))
    return saida


def vao(a, b):
    """Maior vão entre duas caixas (px) pelos eixos separadores; <= 0 quer dizer que se cruzam."""
    Ca, Da = a[2], a[3]; Cb, Db = b[2], b[3]
    eixos = [*Da, *Db, np.cross(Da[1], Da[2]), np.cross(Da[2], Da[0]), np.cross(Da[0], Da[1]),
             np.cross(Db[1], Db[2]), np.cross(Db[2], Db[0]), np.cross(Db[0], Db[1])]
    eixos += [np.cross(u, v) for u in Da for v in Db]
    L = np.array(eixos); n = np.linalg.norm(L, axis=1); L = L[n > 1e-6] / n[n > 1e-6, None]
    pa = Ca @ L.T; pb = Cb @ L.T
    return float(np.max(np.maximum(pb.min(0) - pa.max(0), pa.min(0) - pb.max(0))))


def grupos(cx, folga):
    """Grupos de cubos ligados (listas de índices), do maior para o menor."""
    n = len(cx); pai = list(range(n))

    def raiz(i):
        while pai[i] != i:
            pai[i] = pai[pai[i]]; i = pai[i]
        return i
    mins = np.array([c[2].min(0) for c in cx]); maxs = np.array([c[2].max(0) for c in cx])
    for i in range(n):
        perto = np.where(np.all(mins[i + 1:] <= maxs[i] + folga, 1) & np.all(maxs[i + 1:] >= mins[i] - folga, 1))[0] + i + 1
        for j in perto:
            if raiz(i) != raiz(j) and vao(cx[i], cx[j]) <= folga:
                pai[raiz(i)] = raiz(j)
    g = {}
    for i in range(n):
        g.setdefault(raiz(i), []).append(i)
    return sorted(g.values(), key=len, reverse=True)


def analisar(geo, pose_bedrock=None, folga=0.25):
    """{'corpo': set de (osso, i), 'soltas': [(lista de (osso, i), distância, peça do corpo mais perto)], 'chao'}."""
    cx = caixas(geo, pose_bedrock)
    if not cx:
        return {"corpo": set(), "soltas": [], "chao": 0.0}
    gs = grupos(cx, folga)
    corpo = gs[0]
    soltas = []
    for g in gs[1:]:
        dist, j = min((vao(cx[i], cx[j]), j) for i in g for j in corpo)
        soltas.append(([(cx[i][0], cx[i][1]) for i in g], dist, (cx[j][0], cx[j][1])))
    return {"corpo": {(cx[i][0], cx[i][1]) for i in corpo}, "soltas": soltas,
            "chao": float(min(c[2][:, 1].min() for c in cx))}


def _nomes(pecas):
    por_osso = {}
    for osso, i in pecas:
        por_osso.setdefault(osso, []).append(i)
    itens = [f"{o} (cubo {', '.join(map(str, v))})" if len(v) < 4 else f"{o} ({len(v)} cubos)"
             for o, v in por_osso.items()]
    if len(itens) > 4:
        itens = itens[:3] + [f"e mais {len(itens) - 3} ossos ({len(pecas)} cubos no grupo)"]
    return ", ".join(itens)


def poses_padrao(anims):
    """[(rótulo, pose)] com cada animação em 0, 1/4, 1/2 e 3/4 da duração."""
    saida = []
    for nome, a in anims.items():
        curto = nome.split(".")[-1]
        dur = float(a.get("animation_length") or 0)
        tempos = [0.0] if dur <= 0 else [round(dur * f, 3) for f in (0, 0.25, 0.5, 0.75)]
        saida += [(f"{curto}@{t:g}", ag.pose(a, t)) for t in tempos]
    return saida


def conferir(geo, anims=None, poses=None, folga=0.25, chao=1.0):
    """Texto do relatório e a lista de problemas."""
    L, problemas = [], []
    base = analisar(geo, None, folga)
    L.append(f"pose neutra: {len(base['corpo'])} cubos no corpo, {len(base['soltas'])} grupo(s) solto(s), "
             f"ponto mais baixo y = {base['chao']:+.2f} px")
    for pecas, dist, perto in base["soltas"]:
        problemas.append(f"pose neutra: a {dist:.2f} px de {perto[0]} (cubo {perto[1]}): {_nomes(pecas)}")
    if abs(base["chao"]) > chao:
        problemas.append(f"pose neutra: o ponto mais baixo está em y = {base['chao']:+.2f} px (deveria ser ~0)")
    if poses is None:
        poses = poses_padrao(anims or {})
    for rot_, p in poses:
        r = analisar(geo, p, folga)
        novas = [s_ for s_ in r["soltas"] if any(x in base["corpo"] for x in s_[0])]
        estado = "ok" if not novas else f"{len(novas)} grupo(s) se soltaram"
        anim_base = rot_.split("@")[0]
        importa_chao = any(anim_base in v or anim_base == k for k, v in ALIAS.items())
        aviso_chao = importa_chao and abs(r["chao"]) > chao
        L.append(f"{rot_:>18}: {estado}; ponto mais baixo y = {r['chao']:+.2f} px{'  <- chão' if aviso_chao else ''}")
        for pecas, d, perto in novas:
            problemas.append(f"{rot_}: se soltou a {d:.2f} px de {perto[0]} (cubo {perto[1]}): {_nomes(pecas)}")
        if aviso_chao:
            problemas.append(f"{rot_}: o ponto mais baixo está em y = {r['chao']:+.2f} px (afunda ou flutua)")
    return "\n".join(L), problemas


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("modelo")
    ap.add_argument("--anim", help="arquivo .animation.json")
    ap.add_argument("--pose", action="append", default=[], help="animação e tempo, ex.: walk@0.25 (repetível)")
    ap.add_argument("--folga", type=float, default=0.25, help="vão máximo (px) para contar como encostado (0,1 à frente é técnica contra z-fighting)")
    ap.add_argument("--chao", type=float, default=1.0, help="distância (px) do chão que vira aviso")
    a = ap.parse_args()
    geo = ag.carregar_geo(a.modelo)
    anims = json.loads(Path(a.anim).read_text(encoding="utf-8"))["animations"] if a.anim else {}
    poses = None
    if a.pose:
        poses = []
        for p in a.pose:
            nome, _, t = p.partition("@")
            chave = next((k for k in anims if k.split(".")[-1] == nome), None)
            if chave is None:
                sys.exit(f"animação '{nome}' não existe; há: {', '.join(k.split('.')[-1] for k in anims)}")
            poses.append((p, ag.pose(anims[chave], float(t or 0))))
    texto, problemas = conferir(geo, anims, poses, a.folga, a.chao)
    print(texto)
    print()
    if problemas:
        print(f"{len(problemas)} problema(s) — confira se é de propósito (fogo, aura, peça que só aparece num estado):")
        for p in problemas:
            print("  - " + p)
        sys.exit(1)
    print("nenhuma peça solta e o chão está no lugar.")


if __name__ == "__main__":
    main()
