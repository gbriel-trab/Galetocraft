"""Otimiza um .bbmodel (formato Blockbench, UV por face) para o jogo SEM mudar o visual:

1. Achata os ossos estáticos: só ficam os ossos animados (e os pais deles). A transformação de cada osso
   removido é "assada" no próprio cubo (rotação em 3 eixos em volta do centro do cubo), como faz o
   "Optimize" do Blockbench. Menos ossos = menos contas de matriz e de animação por quadro.
2. Corta faces que não aparecem:
   - faces cuja textura é 100% transparente;
   - bordas finas (<= 0,35) das placas recortadas (penas e chamas) quando quase toda a borda é transparente;
   - faces escondidas dentro de outro cubo sólido do mesmo grupo rígido.
3. Separa os cubos que brilham num osso filho '<osso>_brilho' (mesmo pivô, sem rotação), para a camada de
   brilho desenhar só eles em vez do modelo inteiro.
4. LOD (nível de detalhe): os cubos cujo nome casa com os padrões de 'lods' {nível: [regex]} vão para ossos filhos
   '<osso>_lod<n>' (ou '<osso>_brilho_lod<n>'); o jogo esconde esses ossos de longe. Cubos de LOD nunca são usados
   para esconder faces de outros cubos (senão, quando somem de longe, abririam buraco).

Uso como módulo: novo, relatorio = otimizar(bbmodel_dict, textura_rgba, brilho_rgba, ossos_animados, lods)"""
import copy, math, re, uuid
import numpy as np

# ---------------- álgebra (mesma convenção do Blockbench / previa: M = Rz·Ry·Rx, graus) ----------------
def rot(rx, ry, rz):
    a, b, c = (math.radians(v) for v in (rx, ry, rz))
    Rx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
    Ry = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
    Rz = np.array([[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx

def euler_zyx(A):
    """Inverso de rot(): ângulos (rx, ry, rz) em graus com A = Rz·Ry·Rx."""
    sb = -A[2, 0]
    sb = max(-1.0, min(1.0, sb))
    b = math.asin(sb)
    if abs(sb) < 0.99999:
        a = math.atan2(A[2, 1], A[2, 2]); c = math.atan2(A[1, 0], A[0, 0])
    else:                                     # trava de cardan: fixa rz = 0
        c = 0.0; a = math.atan2(-A[1, 2], A[1, 1])
    r = [math.degrees(a), math.degrees(b), math.degrees(c)]
    assert np.allclose(rot(*r), A, atol=1e-6), "decomposição de Euler falhou"
    return [0.0 if abs(v) < 1e-7 else v for v in r]

def transf_osso(no):
    """p -> R (p - o) + o, devolvido como (A, b)."""
    o = np.array(no["origin"], float); R = rot(*no.get("rotation", [0, 0, 0]))
    return R, o - R @ o

def compor(M1, M2):
    A1, b1 = M1; A2, b2 = M2
    return A1 @ A2, A1 @ b2 + b1

I3 = (np.eye(3), np.zeros(3))
EIXO_FACE = {"north": (2, -1), "south": (2, 1), "west": (0, -1), "east": (0, 1), "down": (1, -1), "up": (1, 1)}

# ---------------- textura ----------------
def regiao(face, img):
    u1, v1, u2, v2 = face["uv"]
    x0, x1 = sorted((int(round(u1)), int(round(u2)))); y0, y1 = sorted((int(round(v1)), int(round(v2))))
    if x1 <= x0 or y1 <= y0: return None
    return img[y0:y1, x0:x1, 3]

def otimizar(bb, tex, brilho, manter, lods=None, corta_ocultas=True):
    """tex/brilho: arrays RGBA (altura x largura x 4) da textura e da máscara de brilho.
    lods: {nível: [regex do nome do cubo]}; o menor nível que casar vale."""
    lods = lods or {}
    def nivel(e):
        for n in sorted(lods):
            if any(re.search(p, e["name"]) for p in lods[n]): return n
        return 0
    bb = copy.deepcopy(bb)
    els = {e["uuid"]: e for e in bb["elements"]}
    rel = {"ossos_antes": 0, "ossos_depois": 0, "faces_antes": 0, "transparentes": 0, "bordas": 0, "ocultas": 0, "cubos_brilho": 0,
           "faces_lod": {}}

    # ---- 1. achatar: cada cubo vai para o osso mantido mais próximo, com a transformação dos ossos removidos assada ----
    def contar(no):
        if isinstance(no, dict):
            rel["ossos_antes"] += 1
            for f in no["children"]: contar(f)
    for no in bb["outliner"]: contar(no)

    def assar(e, M):
        """Cubo e sob a transformação relativa M -> novo cubo equivalente (rotação total em volta do centro)."""
        A, b = M
        de, ate = np.array(e["from"], float), np.array(e["to"], float)
        c = (de + ate) / 2
        rot_e = e.get("rotation", [0, 0, 0])
        Re = rot(*rot_e); oe = np.array(e.get("origin", c), float)
        A_tot = A @ Re; b_tot = A @ (oe - Re @ oe) + b            # p -> A (Re (p - oe) + oe) + b
        if np.allclose(A_tot, np.eye(3)) and np.allclose(b_tot, 0): return e
        novo_c = A_tot @ c + b_tot
        d = novo_c - c
        e = dict(e)
        e["from"] = list(de + d); e["to"] = list(ate + d); e["origin"] = list(novo_c)
        e["rotation"] = euler_zyx(A_tot)
        return e

    def achatar(no, M_rel, destino):
        """Percorre o osso 'no' (já decidido como removido), mandando os cubos para 'destino'."""
        Mn = compor(M_rel, transf_osso(no))
        for f in no["children"]:
            if isinstance(f, str):
                if f in els: destino.append(assar(els[f], Mn))
            elif f["name"] in manter or tem_mantido(f):
                raise ValueError(f"osso animado '{f['name']}' dentro de osso removido '{no['name']}'")
            else:
                achatar(f, Mn, destino)

    cache_tem = {}
    def tem_mantido(no):
        k = no["uuid"]
        if k not in cache_tem:
            cache_tem[k] = any(isinstance(f, dict) and (f["name"] in manter or tem_mantido(f)) for f in no["children"])
        return cache_tem[k]

    def reconstruir(no):
        """Osso mantido: cubos diretos + cubos assados dos filhos removidos + filhos mantidos (recursivo)."""
        cubos, filhos = [], []
        for f in no["children"]:
            if isinstance(f, str):
                if f in els: cubos.append(els[f])
            elif f["name"] in manter or tem_mantido(f):
                filhos.append(reconstruir(f))
            else:
                achatar(f, I3, cubos)
        novo = {k: v for k, v in no.items() if k != "children"}
        novo["_cubos"] = cubos; novo["_filhos"] = filhos
        return novo

    raizes = []
    soltos = []
    for no in bb["outliner"]:
        if isinstance(no, str):
            if no in els: soltos.append(els[no])
        elif no["name"] in manter or tem_mantido(no):
            raizes.append(reconstruir(no))
        else:
            achatar(no, I3, soltos)
    if soltos:   # cubos sem osso animado acima: um osso raiz estático
        raizes.append({"name": "estatico", "origin": [0, 0, 0], "rotation": [0, 0, 0], "uuid": str(uuid.uuid4()),
                       "_cubos": soltos, "_filhos": []})

    # ---- 2. cortar faces ----
    def opaca(e, face):
        r = regiao(e["faces"][face], tex)
        return r is not None and r.size > 0 and bool((r > 0).all())

    def solido(e):
        return all(f in e["faces"] and opaca(e, f) for f in EIXO_FACE)

    def local(e):
        """Inversa da transformação do cubo (para testar se um ponto está dentro dele)."""
        R = rot(*e.get("rotation", [0, 0, 0])); o = np.array(e.get("origin", [0, 0, 0]), float)
        return R.T, o

    def dentro(p, e, inv, folga=0.004):
        Rt, o = inv
        q = Rt @ (p - o) + o
        de, ate = e["from"], e["to"]
        return all(min(de[i], ate[i]) + folga < q[i] < max(de[i], ate[i]) - folga for i in range(3))

    def pontos_face(e, face, n=6):
        de, ate = np.array(e["from"], float), np.array(e["to"], float)
        ax, s = EIXO_FACE[face]
        outros = [i for i in range(3) if i != ax]
        R = rot(*e.get("rotation", [0, 0, 0])); o = np.array(e.get("origin", [0, 0, 0]), float)
        normal = R @ np.eye(3)[ax] * s
        pts = []
        for a in np.linspace(0.0, 1.0, n):
            for b_ in np.linspace(0.0, 1.0, n):
                p = de.copy()
                p[ax] = ate[ax] if s > 0 else de[ax]
                p[outros[0]] = de[outros[0]] + (ate[outros[0]] - de[outros[0]]) * a
                p[outros[1]] = de[outros[1]] + (ate[outros[1]] - de[outros[1]]) * b_
                pts.append(R @ (p - o) + o + normal * 0.02)
        return pts

    def limpar(grupo):
        sol = [(e, local(e)) for e in grupo if nivel(e) == 0 and solido(e)]   # só o que nunca some esconde faces
        saida = []
        for e in grupo:
            faces = dict(e["faces"])
            rel["faces_antes"] += len(faces)
            dims = [abs(e["to"][i] - e["from"][i]) for i in range(3)]
            recortada = any(regiao(f, tex) is not None and (regiao(f, tex) == 0).any() for f in faces.values())
            for nome in list(faces):
                r = regiao(faces[nome], tex)
                if r is None or r.size == 0 or not (r > 0).any():
                    del faces[nome]; rel["transparentes"] += 1; continue
                ax, _ = EIXO_FACE[nome]
                lados = [dims[i] for i in range(3) if i != ax]
                if recortada and min(lados) <= 0.35 and dims[ax] > min(lados) and (r > 0).mean() < 0.2:
                    del faces[nome]; rel["bordas"] += 1; continue      # borda fina quase toda transparente
                if corta_ocultas and sol:
                    pts = pontos_face(e, nome)
                    if all(any(dentro(p, o_e, inv) for o_e, inv in sol if o_e is not e) for p in pts):
                        del faces[nome]; rel["ocultas"] += 1; continue
            if faces:
                e2 = dict(e); e2["faces"] = faces; saida.append(e2)
        return saida

    def brilha(e):
        return any(regiao(f, brilho) is not None and (regiao(f, brilho) > 0).any() for f in e["faces"].values())

    # ---- 3. montar outliner + elementos finais (cubos que brilham num osso filho '_brilho') ----
    elementos, novos_outliner = [], []
    def montar(no):
        rel["ossos_depois"] += 1
        cubos = limpar(no["_cubos"])
        elementos.extend(cubos)
        grupos = {}
        for e in cubos:
            n = nivel(e); acende = brilha(e)
            if acende: rel["cubos_brilho"] += 1
            if n: rel["faces_lod"][n] = rel["faces_lod"].get(n, 0) + len(e["faces"])
            grupos.setdefault(("_brilho" if acende else "") + (f"_lod{n}" if n else ""), []).append(e["uuid"])
        filhos = grupos.pop("", [])
        for sufixo in sorted(grupos):
            rel["ossos_depois"] += 1
            filhos.append({"name": no["name"] + sufixo, "origin": list(no["origin"]), "rotation": [0, 0, 0],
                           "uuid": str(uuid.uuid4()), "color": 0, "export": True, "isOpen": False, "locked": False,
                           "visibility": True, "autouv": 0, "children": grupos[sufixo]})
        filhos += [montar(f) for f in no["_filhos"]]
        novo = {k: v for k, v in no.items() if not k.startswith("_")}
        novo["children"] = filhos
        return novo
    for r in raizes: novos_outliner.append(montar(r))
    bb["outliner"] = novos_outliner
    bb["elements"] = elementos
    rel["faces_depois"] = sum(len(e["faces"]) for e in elementos)
    rel["cubos_depois"] = len(elementos)
    return bb, rel
