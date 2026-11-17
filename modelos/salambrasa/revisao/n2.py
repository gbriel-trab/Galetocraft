"""Salambrasa (#012, Fogo): o galo-salamandra das brasas, quadrúpede roxo-grafite com manchas incandescentes,
pescoço alto, cabeça grande de crista em degrau e juba de penas de fogo."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, anel

ID = "salambrasa"; NOME = "Salambrasa"; NUMERO = 12
ALTURA = 2.45
QUADRUPEDE = True
ROSTO = ((0, 28.5, -19.0), 10.0)
N_RABO = 12
ONDAS = [("rabo", N_RABO, (1.5, 2.5, 0))]
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (da ficha) ----------------
GRAFITE = (84, 60, 80); GRAFITE_ESC = (52, 36, 50); GRAFITE_CLARO = (112, 88, 108)
CABECA = (96, 78, 94); CABECA_CLARA = (122, 104, 120); CABECA_ESC = (66, 52, 66)
VISEIRA = (104, 86, 102); VISEIRA_CLARA = (132, 114, 130); VISEIRA_ESC = (70, 56, 70)
BICO = (128, 114, 126); BICO_CLARO = (156, 142, 154); BICO_ESC = (92, 80, 92)
DEDO = (186, 168, 180); DEDO_CLARO = (214, 200, 210); DEDO_ESC = (146, 128, 142)
CRISTA = (222, 44, 40); CRISTA_ESC = (164, 26, 30); CRISTA_CLARA = (246, 86, 70)
VERM = (220, 50, 34); VERM_ESC = (170, 30, 28)
LARANJA = (246, 124, 26); LARANJA_ESC = (222, 86, 20); AMARELO = (255, 190, 40); AMARELO_CLARO = (255, 222, 110)
PLACA = (246, 150, 60); PLACA_CLARA = (255, 186, 100); PLACA_ESC = (214, 98, 30)
CREME = (252, 240, 226)
BRASA_MIOLO = (255, 226, 90); BRASA = (255, 192, 32); BRASA_BORDA = (250, 128, 22)

# ---------------- manchas incandescentes (hexágonos) ----------------
def mancha(p, face, lista):
    """Cor da mancha no ponto (ou None). lista = [((cx, cy, cz), raio, profundidade)]; raio pode ser (rx, ry, rz).
    Desenho: hexágono chapado (ponta para os lados da face), corpo amarelo, beirada laranja e miolo pouco mais claro.
    Só aparece nas faces a menos de 'profundidade' do centro."""
    x, y, z = p
    for (cx, cy, cz), r, prof in lista:
        rx, ry, rz = r if isinstance(r, tuple) else (r, r, r)
        dx, dy, dz = x - cx, y - cy, z - cz
        if face in ("east", "west"): a, b, n = dz / rz, dy / ry, dx
        elif face in ("north", "south"): a, b, n = dx / rx, dy / ry, dz
        else: a, b, n = dx / rx, dz / rz, dy
        if abs(n) > prof: continue
        d = max(abs(b) / 0.87, abs(a) + abs(b) * 0.58)
        if d <= 1:
            if d < 0.45: return BRASA_MIOLO
            if d < 0.8: return BRASA
            return BRASA_BORDA
    return None

def mat_com_manchas(cor_fn, lista, **kw):
    base = g.mat_cor(cor_fn, **kw)
    def f(c):
        m = mancha(c["p"], c["face"], lista)
        return m if m else base(c)
    return f

def brilho_manchas(lista):
    return lambda c, cor: mancha(c["p"], c["face"], lista) is not None

def dist_seg(p, a, b):
    ab = [b[i] - a[i] for i in range(len(a))]; ap = [p[i] - a[i] for i in range(len(a))]
    t = clamp(sum(ab[i] * ap[i] for i in range(len(a))) / max(sum(v * v for v in ab), 1e-6))
    return math.sqrt(sum((ap[i] - t * ab[i]) ** 2 for i in range(len(a))))

# ---------------- penas em bloco (grossas, com ponta em degrau) ----------------
def mat_pena_bloco(cores, y0, L):
    """Pena grossa pendurada de y0: 3 faixas chapadas (raiz, meio, ponta), face de fora clara, de baixo escura."""
    c0, c1, c2 = cores
    def f(c):
        v = (y0 - c["p"][1]) / L
        base = c0 if v < 0.36 else c1 if v < 0.7 else c2
        face = c["face"]
        if face == "up": base = tom(base, 0.22)
        elif face == "down": base = tom(base, -0.4)
        elif face in ("north", "south"): base = tom(base, -0.12)
        return tom(base, -0.18) if g.na_borda(c) else base
    return f

def pena_bloco(nome, raiz, rot, L, W, cores, esp=1.0, brilho=False):
    """Pena (ou escama) grossa: bloco + ponta em losango (cubo girado 45°), pendurada para baixo da raiz."""
    return g.placa_armadura(nome, raiz, rot, L, W, esp=esp, mat=mat_pena_bloco(cores, raiz[1], 0.72 * L + W / 2))

def pena_cone(nome, raiz, phi, flare, L, W, lado, cores, varre=0, esp=1.0):
    """Pena grossa numa 'saia' em volta do pescoço (phi = 0 lado de fora, negativo = frente)."""
    return osso(nome, list(raiz), [0, -phi * lado, 0], [pena_bloco(nome + "_p", raiz, (-varre, 0, flare * lado), L, W, cores, esp)])

# ---------------- corpo ----------------
VENTRE_Y = 11.6          # abaixo disso o corpo é barriga laranja em placas

def cor_corpo(p, face):
    x, y, z = p
    if face == "down" or y < VENTRE_Y:
        base = PLACA if (z + 30) % 3.0 > 0.45 else PLACA_ESC          # placas da barriga
        return base
    return GRAFITE

MANCHAS_CORPO = [((0, 22.0, -5.0), (2.0, 1, 1.7), 1.2), ((0, 21.4, 2.0), (2.1, 1, 1.8), 1.2), ((0, 20.0, 8.6), (1.9, 1, 1.6), 1.2)]
for lado in (-1, 1):
    MANCHAS_CORPO += [((5.8 * lado, 17.2, -3.4), (1, 1.5, 1.7), 1.2),
                      ((5.8 * lado, 14.0, 2.8), (1, 1.4, 1.6), 1.2),
                      ((5.6 * lado, 17.6, 8.2), (1, 1.3, 1.5), 1.2),
                      ((3.6 * lado, 21.6, 5.4), (1.1, 1, 1.2), 1.2)]

def mat_placa(c):
    """Placa laranja do peito/pescoço: pêssego claro em cima, laranja no meio, fio escuro na beirada de baixo."""
    face = c["face"]
    (_, y0, _), (_, y1, _) = c["b"]
    v = clamp((y1 - c["p"][1]) / max(y1 - y0, 1e-6))
    if face == "up": return PLACA_CLARA
    if face == "down": return PLACA_ESC
    base = PLACA_CLARA if v < 0.3 else PLACA
    if face in ("east", "west"): base = tom(base, -0.15)
    if v > 0.82: base = PLACA_ESC
    return base

# ---------------- cauda em gancho ----------------
def mat_rabo(w, h, py, z0, L, k):
    """Segmento da cauda (eixo local +z). Na base (k < 4): dorso grafite com hexágonos e barriga laranja embaixo. No
    gancho, o lado de fora da curva (a face de baixo local, que de trás aparece) é grafite com hexágonos grandes e uma
    faixa laranja corre pelos lados, junto da barriga; por dentro da curva fica laranja."""
    zc = z0 + L * 0.5
    base = k < 4
    lista = []
    if base and k % 2 == 0: lista.append(((0.0, py + h / 2, zc), (0.3 * w, 1, 0.42 * L), 0.8))
    if not base: lista.append(((0.0, py - h / 2, zc), (0.3 * w, 1, 0.46 * L), 0.8))
    for s in (-1, 1):
        lista.append(((s * w / 2, py + 0.14 * h, zc), (1, 0.3 * h, 0.46 * L), 0.8))
    def cor(p, face):
        x, y, z = p
        v = (y - (py - h / 2)) / h
        if base:
            if face == "down": return PLACA
            if v < 0.2: return LARANJA
            if v < 0.28: return LARANJA_ESC
            return GRAFITE
        if face == "up": return LARANJA
        if face == "down": return GRAFITE
        if v < 0.16: return LARANJA
        if v < 0.24: return LARANJA_ESC
        if v > 0.88: return LARANJA_ESC
        return GRAFITE
    return mat_com_manchas(cor, lista, borda=.0, curva=.3), brilho_manchas(lista)

def secao(nome, px, py, z0, z1, w, h, mat, br, **kw):
    """Seção arredondada ao longo de z: 3 blocos (cruz + miolo chanfrado)."""
    r = 0.28 * min(w, h); q = r / 2
    fx = (py - h / 2, py + h / 2)
    return [peca(nome + "_a", [px - w / 2, py - h / 2 + r, z0], [px + w / 2, py + h / 2 - r, z1], mat, faixa=fx, brilho=br, res=3, **kw),
            peca(nome + "_b", [px - w / 2 + r, py - h / 2, z0], [px + w / 2 - r, py + h / 2, z1], mat, faixa=fx, brilho=br, res=3, **kw),
            peca(nome + "_c", [px - w / 2 + q, py - h / 2 + q, z0], [px + w / 2 - q, py + h / 2 - q, z1], mat, faixa=fx, brilho=br, res=3, **kw)]

def cauda_gancho(nome, base, segs):
    """Cadeia de ossos '<nome>_0', '<nome>_1'..., cada um com giro próprio (rx): a cauda corre para trás, sobe e
    enrola num gancho para a frente. segs = [(comprimento, largura, altura, rx)]. Em cada junta um anel girado pela
    metade do ângulo tapa o vão do lado de fora da curva; a ponta termina num toco arredondado."""
    def seg(k, pos):
        L, w, h, rx = segs[k]
        px, py, pz = pos
        mat, br = mat_rabo(w, h, py, pz, L, k)
        filhos = secao(f"{nome}_{k}", px, py, pz - (0.8 if k == 0 else 0.3), pz + L, w, h, mat, br)
        if k > 0:
            wp, hp = (segs[k - 1][1] + w) / 2, (segs[k - 1][2] + h) / 2
            e = 0.5 + (hp / 2) * math.tan(math.radians(abs(rx) / 2))
            filhos += secao(f"{nome}_{k}_junta", px, py, pz - e, pz + e, wp, hp, mat, br, rot=(-rx / 2, 0, 0), pivo=(px, py, pz))
        if k + 1 < len(segs): filhos.append(seg(k + 1, (px, py, pz + L)))
        else:
            filhos += secao(f"{nome}_ponta", px, py, pz + L - 0.2, pz + L + 1.2, w * 0.74, h * 0.74, mat, br)
        return osso(f"{nome}_{k}", [px, py, pz], [rx, 0, 0], filhos)
    return seg(0, base)

# ---------------- cabeça ----------------
OLHO_Y = 27.4
FAC_T = 2.4                       # espessura da peça da face diagonal (onde fica o olho)
FAC_A = (1.7, -21.2); FAC_B = (4.9, -18.0)          # superfície da face diagonal (lado +x), da frente para trás
FAC_L = math.hypot(FAC_B[0] - FAC_A[0], FAC_B[1] - FAC_A[1])
FAC_M = ((FAC_A[0] + FAC_B[0]) / 2, (FAC_A[1] + FAC_B[1]) / 2)
FAC_C = (FAC_M[0] - 0.7071 * FAC_T / 2, FAC_M[1] + 0.7071 * FAC_T / 2)

def cor_cabeca(p, face):
    x, y, z = p
    if face == "up": return CABECA_CLARA
    return CABECA

def mat_faceta(lado):
    base = g.mat_cor(cor_cabeca, borda=.0, curva=.25)
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u = z - FAC_C[1]
            o = g.pintar_olho(u + 0.1, y - OLHO_Y, 1.75, 1.6, iris=((176, 34, 12), (246, 96, 30)), esclera=CREME,
                              r_iris=(0.5, 0.66), c_iris=(-0.42, -0.08), r_pup=(0.24, 0.3), bravo=0.3, alto=0.5,
                              contorno=CABECA_ESC)
            if o: return o
        return base(c)
    return f

def mat_viseira(c):
    face = c["face"]
    base = VISEIRA_CLARA if face == "up" else VISEIRA_ESC if face == "down" else VISEIRA
    if face == "north": base = tom(VISEIRA, 0.06)
    return tom(base, -0.22) if g.na_borda(c) else base

def mat_bico(c):
    face = c["face"]; x, y, z = c["p"]
    base = BICO_CLARO if face == "up" else BICO_ESC if face == "down" else BICO
    if face in ("north",): base = tom(BICO, 0.05)
    return tom(base, -0.15) if g.na_borda(c) else base

def mat_crista(c):
    """Bloco vermelho chapado: em cima claro, lados na base, frente um pouco mais clara, embaixo escuro."""
    face = c["face"]
    if face == "up": base = CRISTA_CLARA
    elif face == "down": base = CRISTA_ESC
    elif face == "north": base = tom(CRISTA, 0.08)
    elif face == "south": base = tom(CRISTA, -0.15)
    else: base = CRISTA
    return tom(base, -0.2) if g.na_borda(c) else base

def bloco_crista(nome, de, ate, rot=(0, 0, 0), pivo=None):
    return peca(nome, de, ate, mat_crista, rot=rot, pivo=pivo, res=3)

# ---------------- ombro: escamas escuras com a fenda em Y + penas de fogo ----------------
def mat_escama(lado, P):
    fora = "east" if lado > 0 else "west"
    FENDA = [((0.0, 0.0), (1.4, -1.0)), ((0.0, 0.0), (-1.6, -1.2)), ((0.0, 0.0), (0.2, 1.8))]
    def fenda(c):
        if c["face"] != fora: return None
        q = (c["p"][2] - P[2], c["p"][1] - P[1])
        d = min(dist_seg(q, a, b) for a, b in FENDA)
        if d < 0.22: return BRASA_MIOLO
        if d < 0.42: return BRASA
        return None
    def f(c):
        cr = fenda(c)
        if cr: return cr
        face = c["face"]
        base = GRAFITE_CLARO if face == "up" else GRAFITE_ESC if face == "down" else \
            mix(GRAFITE, GRAFITE_CLARO, 0.35) if face == fora else GRAFITE
        return tom(base, -0.25) if g.na_borda(c) else base
    return f, (lambda c, cor: fenda(c) is not None)

def ombro(lado):
    """Asinha do ombro: 3 escamas grafite grossas (a maior com a fenda em Y que brilha) e, por baixo, um leque de
    penas de fogo grossas apontando para trás e para baixo."""
    s = "d" if lado < 0 else "e"
    P = (6.2 * lado, 21.0, -8.0)
    filhos = []
    cores_fogo = [(VERM, LARANJA, AMARELO), (VERM_ESC, VERM, LARANJA), (LARANJA_ESC, LARANJA, AMARELO), (VERM, LARANJA_ESC, LARANJA)]
    for k in range(4):
        raiz = (6.0 * lado, 17.4 - 0.2 * k, -9.0 + 2.2 * k)
        filhos.append(pena_bloco(f"fogo{k}_{s}", raiz, (-(62 + 6 * k), 0, 22 * lado), 8.0 - 0.6 * k, 2.6, cores_fogo[k], esp=0.9))
    for k, (dz, dy, L, W) in enumerate([(3.4, -0.6, 6.0, 3.8), (-1.8, 0.4, 7.0, 4.4), (0.8, 0.0, 8.0, 4.8)]):
        raiz = (P[0] + 0.3 * lado * (2 - k), P[1] + dy, P[2] + dz)
        m, br = mat_escama(lado, (raiz[0], raiz[1] - 2.6, raiz[2]))
        x, y, z = raiz; esp = 1.1
        cy = y - L * 0.72; sq = W / 1.4142
        filhos.append(osso(f"escama{k}_{s}", list(raiz), [-48, 0, 24 * lado], [
            peca(f"escama{k}_{s}", [x - esp / 2, cy, z - W / 2], [x + esp / 2, y, z + W / 2], m, res=4, brilho=br),
            peca(f"escama{k}_{s}_ponta", [x - esp / 2 + 0.02, cy - sq / 2, z - sq / 2], [x + esp / 2 - 0.02, cy + sq / 2, z + sq / 2], m,
                 rot=(45, 0, 0), pivo=(x, cy, z), res=4, brilho=br)]))
    return osso("asa_" + s, [5.6 * lado, 20.0, -8.0], [0, 0, 0], filhos)

# ---------------- pernas ----------------
def mat_dedo(c):
    face = c["face"]
    base = DEDO_CLARO if face == "up" else DEDO_ESC if face == "down" else tom(DEDO, 0.06) if face == "north" else DEDO
    return tom(base, -0.2) if g.na_borda(c) else base

def pata(nome, xc, zc):
    """Pata: base roxa e 3 dedos grandes cinza-claros em leque para a frente + 1 atrás."""
    pp = []
    pp.append(peca(nome + "_pata", [xc - 2.7, 0.4, zc - 2.6], [xc + 2.7, 2.8, zc + 2.4],
                   g.mat_cor(lambda p, f: GRAFITE, borda=.08, curva=.4), res=3))
    for k, (dx, giro) in enumerate(((-2.0, 12), (0.0, 0), (2.0, -12))):
        x0 = xc + dx; z0 = zc - 1.2
        pp.append(osso(f"{nome}_dedo{k}", [x0, 0, z0], [0, giro, 0],
                       [peca(f"{nome}_dedo{k}", [x0 - 0.9, 0, z0 - 3.4], [x0 + 0.9, 2.2, z0], mat_dedo, res=3)]))
    pp.append(peca(nome + "_dedo_tras", [xc - 0.8, 0, zc + 1.8], [xc + 0.8, 1.6, zc + 3.6], mat_dedo, res=3))
    return pp

def perna(nome, xc, zc, tras):
    """Perna: alto roxo, faixa laranja, tornozelo roxo e pata de dedos claros."""
    pp = []
    escuro = g.mat_cor(lambda p, f: GRAFITE, borda=.05, curva=.4)
    faixa = g.mat_cor(lambda p, f: mix(LARANJA_ESC, AMARELO, clamp((p[1] - 4.6) / 2.8)), borda=.06, curva=.2)
    if tras:
        pp += g.arredondado2(nome + "_coxa", [xc - 2.8, 7.4, zc - 3.6], [xc + 2.8, 16.0, zc + 3.4], escuro, r=1.4)
    else:
        pp += g.arredondado(nome + "_braco", [xc - 2.4, 7.4, zc - 2.4], [xc + 2.4, 14.0, zc + 2.4], escuro, r=0.8)
    pp += g.octogono(nome + "_faixa", [xc - 2.25, 4.6, zc - 2.25], [xc + 2.25, 7.6, zc + 2.25], faixa, r=0.7)
    pp += g.octogono(nome + "_tornozelo", [xc - 2.35, 2.4, zc - 2.35], [xc + 2.35, 4.8, zc + 2.35], escuro, r=0.7)
    pp += pata(nome, xc, zc)
    return osso(nome, [xc, 12.0, zc], [0, 0, 0], pp)

# ---------------- montagem ----------------
def montar():
    # ---------- cabeça grande: bloco grafite, faces diagonais com o olho, viseira grossa, bico em gancho ----------
    cab = []
    mcab = g.mat_cor(cor_cabeca, borda=.03, curva=.3)
    fx = (23.0, 31.0)
    cab += g.arredondado("cranio", [-4.9, 23.6, -18.4], [4.9, 31.0, -12.6], mcab, r=0.8, faixa=fx, res=3)
    cab.append(peca("cranio_frente", [-2.0, 23.8, -21.4], [2.0, 30.6, -18.0], mcab, faixa=fx, res=3))
    cab.append(peca("queixo", [-3.6, 23.0, -20.2], [3.6, 24.6, -14.0], g.mat_cor(lambda p, f: CABECA_ESC, borda=.06), faixa=fx, res=3))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 23.9, cz - FAC_L / 2], [cx + FAC_T / 2, 30.4, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, 27.0, cz), faixa=fx, res=8))
        # viseira: metade da sobrancelha grossa, descendo um pouco para o meio (V bravo) e para a frente
        x0, x1 = sorted((0.0, 5.1 * lado))
        cab.append(peca("viseira_" + s, [x0, 29.3, -22.2], [x1, 31.8, -15.0], mat_viseira, rot=(-6, 0, 4 * lado),
                        pivo=(5.2 * lado, 31.8, -18.0), res=3))
    # bico: base larga, meio que afina, gancho para baixo e mandíbula de baixo recuada
    cab.append(peca("bico_base", [-2.0, 24.8, -22.8], [2.0, 28.6, -20.8], mat_bico, res=4))
    cab.append(peca("bico_meio", [-1.6, 25.4, -24.6], [1.6, 28.3, -22.6], mat_bico, res=4))
    cab.append(peca("bico_ponta", [-1.2, 25.8, -26.0], [1.2, 27.9, -24.4], mat_bico, res=4))
    cab.append(peca("bico_gancho", [-0.9, 24.0, -26.2], [0.9, 26.0, -24.9], mat_bico, res=4))
    cab.append(peca("bico_baixo", [-1.3, 24.0, -24.0], [1.3, 25.0, -20.8], g.mat_cor(lambda p, f: BICO_ESC, borda=.08), res=4))
    # crista de brasa: blocos vermelhos em degrau, mais alta no meio, caindo para trás por cima da nuca
    cr = []
    cr.append(bloco_crista("crista_base", [-5.0, 31.0, -19.0], [5.0, 34.4, -11.0]))
    cr.append(bloco_crista("crista_frente", [-3.4, 32.0, -21.4], [3.4, 35.4, -17.4], rot=(-10, 0, 0), pivo=(0, 32.0, -17.4)))
    cr.append(bloco_crista("crista_topo", [-2.2, 34.0, -18.0], [2.2, 39.2, -12.4], rot=(12, 0, 0), pivo=(0, 34.0, -14.0)))
    cr.append(bloco_crista("crista_meio", [-4.2, 33.4, -13.6], [4.2, 37.0, -8.0], rot=(20, 0, 0), pivo=(0, 33.4, -11.0)))
    cr.append(bloco_crista("crista_nuca", [-4.4, 29.2, -11.6], [4.4, 33.4, -5.4], rot=(28, 0, 0), pivo=(0, 33.0, -11.0)))
    cab.append(osso("crista", [0, 31.0, -16.0], [0, 0, 0], cr))
    # penas das bochechas: vermelhas -> laranja, varrendo para trás por baixo e atrás do olho
    boch = []
    for k, (y0, z0, L, rx, rz) in enumerate([(29.2, -14.2, 6.4, -72, 22), (27.0, -15.6, 6.8, -58, 30), (25.2, -13.0, 7.0, -50, 40)]):
        for lado in (-1, 1):
            s = "d" if lado < 0 else "e"
            cores = [(CRISTA, VERM, LARANJA), (VERM, LARANJA_ESC, LARANJA), (LARANJA_ESC, LARANJA, AMARELO)][k]
            boch.append(pena_bloco(f"bochecha{k}_{s}", (4.4 * lado, y0, z0), (rx, 0, rz * lado), L, 3.4, cores, esp=1.1))
    cab.append(osso("bochechas", [0, 26, -15], [0, 0, 0], boch))
    cabeca = osso("cabeca", [0, 24.0, -16.0], [0, 0, 0], cab)

    # ---------- pescoço alto e ereto, com placas laranja na frente e a juba de penas em volta ----------
    pesc = []
    INC = -24                                                   # inclinação do pescoço (o alto vai para a frente)
    PV = (0, 14.0, -13.0)
    mpe = g.mat_cor(lambda p, f: PLACA_ESC if (f == "north" or p[2] < -15.6) else GRAFITE, borda=.03, curva=.3)
    pesc += g.octogono("pescoco", [-3.5, 13.0, -16.4], [3.5, 27.0, -10.0], mpe, r=1.0, faixa=(13, 27), rot=(INC, 0, 0), pivo=PV)
    for k in range(3):
        ya = 25.4 - k * 3.4; w = 2.8 + 0.5 * k
        pesc.append(peca(f"placa_pesc{k}", [-w, ya - 3.6, -16.9], [w, ya, -16.2], mat_placa, rot=(INC, 0, 0), pivo=PV, res=3))
    juba = []
    CAMADAS = [  # (y, raio x, raio z, z centro, abertura, varrida, comprimento, largura, cores, phis)
        (24.6, 4.0, 3.2, -14.6, 50, 36, 8.0, 3.8, (VERM, LARANJA, AMARELO), [-20, 15, 50, 90]),
        (21.6, 4.3, 3.6, -13.6, 56, 26, 7.6, 3.8, (LARANJA_ESC, LARANJA, AMARELO), [-30, 0, 35, 70]),
    ]
    for f_, (y0, ax, az, zc, fl, var, L, W, cores, phis) in enumerate(CAMADAS):
        for k, phi in enumerate(phis):
            for lado in (-1, 1):
                if phi >= 88 and lado < 0: continue
                x, z = anel(ax, az, zc, phi, lado)
                if phi >= 88: x = 0
                juba.append(pena_cone(f"juba{f_}{k}_{'d' if lado < 0 else 'e'}", (x, y0, z), phi, fl if phi < 88 else 0,
                                      L, W, lado, cores, varre=var, esp=1.0))
    pesc.append(osso("juba", [0, 22.0, -14.0], [0, 0, 0], juba))
    pesc.append(cabeca)
    pescoco = osso("pescoco", [0, 16.0, -12.0], [0, 0, 0], pesc)

    # ---------- tronco de salamandra ----------
    corpo = []
    mt = mat_com_manchas(cor_corpo, MANCHAS_CORPO, borda=.02, curva=.45)
    bt = brilho_manchas(MANCHAS_CORPO)
    fc = (9.5, 22.6)
    corpo += g.arredondado2("peito", [-5.8, 9.8, -14.0], [5.8, 22.4, -3.0], mt, r=2.4, faixa=fc, brilho=bt)
    corpo += g.arredondado2("meio", [-5.9, 9.6, -5.0], [5.9, 22.2, 5.0], mt, r=2.4, faixa=fc, brilho=bt)
    corpo += g.arredondado2("quadril", [-5.6, 10.0, 3.0], [5.6, 20.8, 13.4], mt, r=2.4, faixa=fc, brilho=bt)
    for k, (ya, w) in enumerate([(17.2, 4.4), (14.0, 4.2), (11.0, 3.4)]):
        corpo.append(peca(f"placa_peito{k}", [-w, ya - 3.6, -14.7], [w, ya, -13.8], mat_placa, rot=(INC * 0.7, 0, 0),
                          pivo=(0, ya, -14.4), res=3))
    corpo += [ombro(-1), ombro(1)]
    # cauda grossa: corre para trás, sobe e enrola num gancho para a frente
    Ls = [4.2, 4.0, 3.8, 3.8, 3.8, 3.6, 3.4, 3.3, 3.2, 3.1, 2.8, 2.2]
    Rs = [12, 4, -22, -36, -34, -30, -26, -22, -16, -10, -4, 6]
    Hs = [8.0, 7.8, 7.6, 7.4, 7.2, 7.0, 6.7, 6.4, 6.1, 5.8, 5.5, 5.2]
    Ws = [10.4, 10.2, 10.0, 9.7, 9.3, 8.8, 8.3, 7.8, 7.3, 6.8, 6.3, 5.8]
    corpo.append(osso("cauda", [0, 15.0, 11.5], [0, 0, 0], [cauda_gancho("rabo", (0, 15.0, 11.5), list(zip(Ls, Ws, Hs, Rs)))]))
    corpo.append(pescoco)
    tronco = osso("corpo", [0, 14.0, 6.0], [0, 0, 0], corpo)

    pernas = [perna("perna_fd", -6.6, -7.6, False), perna("perna_fe", 6.6, -7.6, False),
              perna("perna_td", -6.6, 10.4, True), perna("perna_te", 6.6, 10.4, True)]
    return [tronco] + pernas

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
