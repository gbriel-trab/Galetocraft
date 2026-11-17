"""Salambrasa (#012, Fogo): o galo-salamandra das brasas, quadrúpede roxo-grafite com manchas incandescentes,
pescoço alto, cabeça grande de crista em degrau e juba de penas de fogo."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp

ID = "salambrasa"; NOME = "Salambrasa"; NUMERO = 12
ALTURA = 2.45
QUADRUPEDE = True
ROSTO = ((0, 28.5, -21.0), 10.0)
N_RABO = 12
ONDAS = [("rabo", N_RABO, (1.5, 2.5, 0))]
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (amostrada com PIL na ficha: Paleta de Cores, _arte e _vistas) ----------------
GRAFITE = (124, 52, 66); GRAFITE_ESC = (66, 26, 38); GRAFITE_CLARO = (128, 66, 82)      # corpo ameixa (arte 99,45,58)
CABECA = (116, 64, 80); CABECA_CLARA = (146, 92, 108); CABECA_ESC = (78, 40, 54)        # cabeça (arte 110,57,72)
FACE = (150, 100, 114); FACE_CLARA = (176, 124, 136)                                     # malva clara em volta do olho
VISEIRA = (118, 66, 82); VISEIRA_CLARA = (152, 98, 114); VISEIRA_ESC = (78, 40, 54)
BICO = (150, 90, 104); BICO_CLARO = (178, 120, 132); BICO_ESC = (108, 62, 76)           # malva (arte 150,87,97)
DEDO = (170, 104, 118); DEDO_CLARO = (200, 140, 152); DEDO_ESC = (128, 74, 88)          # arte 167,99,113
CRISTA = (220, 30, 30); CRISTA_ESC = (168, 18, 24); CRISTA_CLARA = (251, 83, 82)         # paleta 202,24,30 / topo 251,83,82
VERM = (226, 40, 26); VERM_ESC = (176, 22, 22)
LARANJA = (253, 115, 2); LARANJA_ESC = (253, 69, 11); AMARELO = (254, 201, 37); AMARELO_CLARO = (255, 226, 110)
PLACA = (255, 146, 56); PLACA_CLARA = (255, 194, 118); PLACA_ESC = (232, 104, 34)           # arte 240,112,40
CREME = (254, 229, 215)
BRASA_MIOLO = (255, 230, 90); BRASA = (253, 206, 0); BRASA_BORDA = (253, 120, 10)

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

def hexa(a, b):
    """Cor do hexágono (a, b normalizados) ou None."""
    d = max(abs(b) / 0.87, abs(a) + abs(b) * 0.58)
    if d > 1: return None
    return BRASA_MIOLO if d < 0.45 else BRASA if d < 0.8 else BRASA_BORDA

# manchas da cauda medidas na ficha (vista lateral: centro z, y, largura, altura; vista de trás: x, y, largura, altura)
MANCHAS_CAUDA_LADO = [(25.9, 13.5, 3.8, 4.4), (25.6, 21.9, 4.8, 5.6), (22.4, 17.2, 3.8, 4.4), (19.7, 26.6, 5.8, 4.4),
                      (18.0, 14.0, 4.4, 3.4), (13.0, 14.2, 4.6, 3.6), (12.8, 28.8, 4.8, 3.2), (8.0, 28.0, 3.4, 3.0)]
MANCHAS_CAUDA_TRAS = [(0.0, 17.6, 6.6, 7.2), (0.0, 10.4, 5.2, 4.4), (0.0, 23.8, 3.8, 2.4),
                      (-4.7, 21.5, 3.2, 4.2), (4.7, 21.5, 3.2, 4.2), (-4.9, 14.5, 2.6, 3.6), (4.9, 14.5, 2.6, 3.6)]
MANCHAS_CAUDA_CIMA = [(0.0, 18.6, 3.2, 2.6), (0.0, 13.0, 3.0, 2.4)]          # (x, z, largura, comprimento) no alto do gancho

def mancha_cauda(pw, nw):
    x, y, z = pw
    if abs(nw[0]) > 0.7:
        for zc, yc, L, H in MANCHAS_CAUDA_LADO:
            c = hexa((z - zc) / (L / 2), (y - yc) / (H / 2))
            if c: return c
    if nw[2] > 0.2:
        for xc, yc, L, H in MANCHAS_CAUDA_TRAS:
            c = hexa((x - xc) / (L / 2), (y - yc) / (H / 2))
            if c: return c
    if nw[1] > 0.6 and y > 24:
        for xc, zc, L, C in MANCHAS_CAUDA_CIMA:
            c = hexa((x - xc) / (L / 2), (z - zc) / (C / 2))
            if c: return c
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
VENTRE_Y = 12.2          # abaixo disso o corpo é barriga laranja em placas

def cor_corpo(p, face):
    x, y, z = p
    if face == "down" or y < VENTRE_Y:
        base = PLACA if (z + 30) % 3.0 > 0.45 else PLACA_ESC          # placas da barriga
        return base
    return GRAFITE

MANCHAS_CORPO = [((0, 22.8, -6.6), (2.4, 1, 2.0), 1.2), ((0, 22.0, 0.8), (2.6, 1, 2.2), 1.2), ((0, 20.4, 7.6), (2.4, 1, 2.0), 1.2)]
for lado in (-1, 1):   # posições medidas na vista lateral da ficha (z, y)
    MANCHAS_CORPO += [((5.9 * lado, 14.3, 1.2), (1, 1.4, 1.8), 1.2),        # flanco, grande
                      ((5.9 * lado, 11.9, -2.2), (1, 0.9, 0.8), 1.2),       # flanco, pequena
                      ((5.6 * lado, 11.6, 5.4), (1, 0.8, 0.8), 1.2),
                      ((4.7 * lado, 19.4, -2.2), (1, 1.0, 1.9), 1.3),       # alto do dorso
                      ((4.4 * lado, 18.2, 5.0), (1, 1.2, 1.9), 1.3)]

def mat_placa(c):
    """Placa laranja da barriga: em cima pêssego claro, frente laranja com cantos arredondados (mais escuros), fio
    escuro na beirada de baixo; de lado um pouco mais escura."""
    face = c["face"]
    (x0, y0, _), (x1, y1, _) = c["b"]
    v = clamp((y1 - c["p"][1]) / max(y1 - y0, 1e-6))
    u = abs(c["p"][0]) / max(x1, 1e-6)
    if face == "up": return PLACA_CLARA
    if face == "down": return PLACA_ESC
    base = PLACA_CLARA if v < 0.22 else PLACA
    if face in ("east", "west"): base = tom(PLACA, -0.15)
    if v > 0.86 or (face == "north" and u > 0.86 and v > 0.5): base = PLACA_ESC
    return base

# ---------------- cauda em gancho ----------------
def rot_x(q, o, ang):
    """Gira o ponto q (x, y, z) em volta do eixo x que passa por o, como o Blockbench (positivo = frente para baixo)."""
    c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    dy, dz = q[1] - o[1], q[2] - o[2]
    return (q[0], o[1] + dy * c - dz * s_, o[2] + dy * s_ + dz * c)

def mat_rabo(w, h, py, z0, L, k, cadeia):
    """Segmento da cauda. Base: dorso ameixa e barriga laranja embaixo; no gancho a faixa laranja corre por fora da
    curva (atrás) e por dentro (em cima). As manchas são desenhadas no MUNDO, onde a ficha as mostra: o ponto é levado
    pela 'cadeia' de giros [(origem, ângulo), ...] (da peça até a raiz da cauda)."""
    base = k < 4
    def cor(p, face):
        x, y, z = p
        v = (y - (py - h / 2)) / h
        if base:
            if face == "down": return PLACA
            if v < 0.34: return LARANJA
            if v < 0.42: return LARANJA_ESC
            return GRAFITE
        if face == "down": return GRAFITE
        if face == "up": return LARANJA if abs(x) < 0.2 * w else GRAFITE
        if k < 7:
            if v < 0.26: return LARANJA
            if v < 0.34: return LARANJA_ESC
            return GRAFITE
        if v > 0.84: return LARANJA
        if v > 0.76: return LARANJA_ESC
        return GRAFITE
    fundo = g.mat_cor(cor, borda=.0, curva=.3)
    def mundo(c):
        pw = c["p"]; n = g.NORMAL[c["face"]]; nw = n
        for o, ang in cadeia:
            pw = rot_x(pw, o, ang); nw = rot_x(nw, (0, 0, 0), ang)
        return mancha_cauda(pw, nw)
    def f(c):
        return mundo(c) or fundo(c)
    return f, (lambda c, cor_: mundo(c) is not None)

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
    def seg(k, pos, cadeia_pai):
        L, w, h, rx = segs[k]
        px, py, pz = pos
        cad = [((px, py, pz), rx)] + cadeia_pai
        mat, br = mat_rabo(w, h, py, pz, L, k, cad)
        filhos = secao(f"{nome}_{k}", px, py, pz - (0.8 if k == 0 else 0.3), pz + L, w, h, mat, br)
        if k > 0:
            wp, hp = (segs[k - 1][1] + w) / 2, (segs[k - 1][2] + h) / 2
            e = 0.5 + (hp / 2) * math.tan(math.radians(abs(rx) / 2))
            mj, bj = mat_rabo(wp, hp, py, pz, L, k, [((px, py, pz), -rx / 2)] + cad)
            filhos += secao(f"{nome}_{k}_junta", px, py, pz - e, pz + e, wp, hp, mj, bj, rot=(-rx / 2, 0, 0), pivo=(px, py, pz))
        if k + 1 < len(segs): filhos.append(seg(k + 1, (px, py, pz + L), cad))
        else:
            filhos += secao(f"{nome}_ponta", px, py, pz + L - 0.2, pz + L + 1.2, w * 0.74, h * 0.74, mat, br)
        return osso(f"{nome}_{k}", [px, py, pz], [rx, 0, 0], filhos)
    return seg(0, base, [])

# ---------------- cabeça ----------------
OLHO_Y = 27.7
FAC_T = 2.4                       # espessura da peça da face diagonal (onde fica o olho)
FAC_A = (2.1, -21.4); FAC_B = (4.9, -17.4)          # superfície da face diagonal (lado +x), da frente para trás
FAC_L = math.hypot(FAC_B[0] - FAC_A[0], FAC_B[1] - FAC_A[1])
FAC_ANG = math.degrees(math.atan2(FAC_B[0] - FAC_A[0], FAC_B[1] - FAC_A[1]))   # ~35°: o olho aparece de frente e de lado
FAC_M = ((FAC_A[0] + FAC_B[0]) / 2, (FAC_A[1] + FAC_B[1]) / 2)
_n = (math.cos(math.radians(FAC_ANG)), -math.sin(math.radians(FAC_ANG)))          # normal de fora (lado +x)
FAC_C = (FAC_M[0] - _n[0] * FAC_T / 2, FAC_M[1] - _n[1] * FAC_T / 2)

def cor_cabeca(p, face):
    """Alto da cabeça cinza-ameixa; da altura do olho para baixo, a 'cara' malva clara (como na ficha)."""
    x, y, z = p
    if face == "up": return CABECA_CLARA
    if y < 28.6 and face != "down": return FACE
    return CABECA

def mat_faceta(lado):
    base = g.mat_cor(cor_cabeca, borda=.0, curva=.25)
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u = z - FAC_C[1]
            o = g.pintar_olho(u + 0.15, y - OLHO_Y, 2.3, 1.85, iris=((170, 40, 8), (232, 84, 14)), esclera=CREME,
                              r_iris=(0.48, 0.66), c_iris=(-0.44, -0.12), r_pup=(0.22, 0.3), bravo=0.32, alto=0.42,

                              contorno=(150, 40, 40))
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
def mat_escama(lado, P, com_fenda=True):
    fora = "east" if lado > 0 else "west"
    FENDA = [((0.0, 0.0), (2.0, -1.7)), ((0.0, 0.0), (-2.1, -1.6)), ((0.0, 0.0), (0.0, 2.6))]
    def fenda(c):
        if not com_fenda or c["face"] != fora: return None
        q = (c["p"][2] - P[2], c["p"][1] - P[1])
        d = min(dist_seg(q, a, b) for a, b in FENDA)
        if d < 0.26: return BRASA_MIOLO
        if d < 0.5: return BRASA
        if d < 0.66: return BRASA_BORDA
        return None
    def f(c):
        cr = fenda(c)
        if cr: return cr
        face = c["face"]
        base = GRAFITE_CLARO if face == "up" else GRAFITE_ESC if face == "down" else \
            mix(GRAFITE, GRAFITE_CLARO, 0.35) if face == fora else GRAFITE
        return tom(base, -0.25) if g.na_borda(c) else base
    return f, (lambda c, cor: fenda(c) is not None)

def escama(nome, raiz, rot, giro, L, W, m, br, esp=1.3):
    """Escama grafite grossa, pendurada da raiz, com ponta em losango; 'giro' (em y) vira a face larga."""
    x, y, z = raiz
    cy = y - L * 0.72; sq = W / 1.4142
    return osso(nome + "_giro", list(raiz), [0, giro, 0], [osso(nome, list(raiz), list(rot), [
        peca(nome, [x - esp / 2, cy, z - W / 2], [x + esp / 2, y, z + W / 2], m, res=4, brilho=br),
        peca(nome + "_ponta", [x - esp / 2 + 0.02, cy - sq / 2, z - sq / 2], [x + esp / 2 - 0.02, cy + sq / 2, z + sq / 2], m,
             rot=(45, 0, 0), pivo=(x, cy, z), res=4, brilho=br)])])

def ombro(lado):
    """Asinha do ombro: uma ombreira grafite sobre o alto da pata da frente, 3 escamas grossas deitadas para trás como
    uma asa dobrada (a do meio com a fenda em Y que brilha) e, por baixo, um leque de penas de fogo para trás."""
    s = "d" if lado < 0 else "e"
    filhos = []
    cores_fogo = [(VERM, LARANJA, AMARELO), (VERM, LARANJA_ESC, LARANJA), (LARANJA_ESC, LARANJA, AMARELO), (VERM, LARANJA_ESC, AMARELO)]
    for k in range(5):   # leque grande de penas de fogo (na ficha vai do ombro até o meio do corpo)
        raiz = (6.0 * lado, 17.6 - 0.4 * k, -9.0 + 2.0 * k)
        filhos.append(pena_bloco(f"fogo{k}_{s}", raiz, (-(62 + 5 * k), 0, 22 * lado), 9.6 - 0.6 * k, 3.4,
                                 cores_fogo[k % 4], esp=1.6))
    # ombreira: olha meio para a frente, cobre o alto da pata
    m0, b0 = mat_escama(lado, (0, 0, 0), False)
    filhos.append(escama(f"ombreira_{s}", (6.4 * lado, 19.6, -11.4), (-14, 0, 12 * lado), 38 * lado, 6.6, 4.8, m0, b0))
    # asa dobrada: escamas deitadas para trás, em camadas
    for k, (z, y, L, W, rx) in enumerate([(-6.2, 21.0, 7.0, 3.8, -66), (-9.0, 21.6, 8.4, 4.6, -60), (-11.0, 21.0, 6.6, 4.0, -52)]):
        raiz = (6.0 * lado + 0.3 * lado * k, y, z)
        m, br = mat_escama(lado, (raiz[0], y - 3.0, z), k == 1)
        filhos.append(escama(f"escama{k}_{s}", raiz, (rx, 0, 22 * lado), 0, L, W, m, br))
    return osso("asa_" + s, [5.6 * lado, 20.0, -8.0], [0, 0, 0], filhos)

# ---------------- pernas ----------------
def mat_dedo(c):
    face = c["face"]
    base = DEDO_CLARO if face == "up" else DEDO_ESC if face == "down" else tom(DEDO, 0.06) if face == "north" else DEDO
    return tom(base, -0.2) if g.na_borda(c) else base

def pata(nome, xc, zc):
    """Pata: base roxa e 3 dedos grandes cinza-claros em leque para a frente + 1 atrás."""
    pp = []
    pp.append(peca(nome + "_pata", [xc - 3.0, 0.4, zc - 2.6], [xc + 3.0, 3.4, zc + 2.4],
                   g.mat_cor(lambda p, f: GRAFITE, borda=.08, curva=.4), res=3))
    for k, (dx, giro) in enumerate(((-2.4, 17), (0.0, 0), (2.4, -17))):
        x0 = xc + dx; z0 = zc - 1.2
        pp.append(osso(f"{nome}_dedo{k}", [x0, 0, z0], [0, giro, 0],
                       [peca(f"{nome}_dedo{k}", [x0 - 1.15, 0, z0 - 4.6], [x0 + 1.15, 2.9, z0], mat_dedo, res=3)]))
    pp.append(peca(nome + "_dedo_tras", [xc - 0.8, 0, zc + 1.8], [xc + 0.8, 1.6, zc + 3.6], mat_dedo, res=3))
    return pp

def perna(nome, xc, zc, tras):
    """Perna: alto roxo, faixa laranja, tornozelo roxo e pata de dedos claros."""
    pp = []
    escuro = g.mat_cor(lambda p, f: GRAFITE, borda=.05, curva=.4)
    faixa = g.mat_cor(lambda p, f: mix(LARANJA_ESC, AMARELO, clamp((p[1] - 3.8) / 4.6)), borda=.04, curva=.1)
    if tras:     # coxa grande com uma mancha incandescente do lado de fora
        lado = 1 if xc > 0 else -1
        mc = [((xc + 2.2 * lado, 12.2, zc - 0.2), (1, 1.6, 1.8), 0.9)]
        xt = xc - 0.6 * lado
        pp += g.arredondado2(nome + "_coxa", [xt - 2.8, 7.4, zc - 3.8], [xt + 2.8, 15.4, zc + 3.6],
                             mat_com_manchas(lambda p, f: GRAFITE, mc, borda=.05, curva=.4), r=2.0, brilho=brilho_manchas(mc))
    else:
        pp += g.arredondado2(nome + "_braco", [xc - 2.8, 7.0, zc - 2.7], [xc + 2.8, 14.6, zc + 2.7], escuro, r=1.2,

                            rot=(16, 0, 0), pivo=(xc, 7.2, zc))
    pp += g.octogono(nome + "_faixa", [xc - 2.35, 4.0, zc - 2.35], [xc + 2.35, 8.4, zc + 2.35], faixa, r=0.7)
    pp += g.octogono(nome + "_tornozelo", [xc - 2.45, 2.4, zc - 2.45], [xc + 2.45, 4.2, zc + 2.45], escuro, r=0.7)
    pp += pata(nome, xc, zc)
    return osso(nome, [xc, 12.0, zc], [0, 0, 0], pp)

# ---------------- deslocar um grupo inteiro (a pintura continua nas coordenadas de quando foi modelado) ----------------
def deslocar(desde, nos, dz):
    """Empurra em z (dz) as peças criadas desde o índice 'desde' e os ossos 'nos'. Os materiais recebem o ponto de
    volta nas coordenadas originais, então desenhos que dependem da posição (o olho, as faixas) não mudam."""
    def volta(c):
        c = dict(c); x, y, z = c["p"]; c["p"] = (x, y, z - dz)
        b0, b1 = c["b"]; c["b"] = ([b0[0], b0[1], b0[2] - dz], [b1[0], b1[1], b1[2] - dz])
        return c
    for pc in g.PECAS[desde:]:
        for arr in (pc.de, pc.ate, pc.pivo): arr[2] += dz
        m = pc.mat; pc.mat = lambda c, m=m: m(volta(c))
        if callable(pc.brilho):
            b = pc.brilho; pc.brilho = lambda c, cor, b=b: b(volta(c), cor)
    def visita(no):
        if isinstance(no, dict):
            no["origin"][2] += dz
            for f in no["children"]: visita(f)
    for no in nos: visita(no)

DZ_CAB = -2.0            # a cabeça (e a juba) vão para a frente: o bico fica sobre as patas da frente, como na ficha

# ---------------- montagem ----------------
def montar():
    i_cab = len(g.PECAS)
    # ---------- cabeça grande: bloco grafite, faces diagonais com o olho, viseira grossa, bico em gancho ----------
    cab = []
    mcab = g.mat_cor(cor_cabeca, borda=.03, curva=.3)
    fx = (23.0, 31.0)
    cab += g.arredondado("cranio", [-4.9, 23.6, -18.4], [4.9, 31.0, -12.6], mcab, r=0.8, faixa=fx, res=3)
    cab.append(peca("cranio_frente", [-2.3, 23.8, -21.5], [2.3, 30.6, -18.0], mcab, faixa=fx, res=3))
    cab.append(peca("queixo", [-3.6, 23.0, -20.2], [3.6, 24.6, -14.0], g.mat_cor(lambda p, f: CABECA_ESC, borda=.06), faixa=fx, res=3))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 23.9, cz - FAC_L / 2], [cx + FAC_T / 2, 30.4, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, FAC_ANG * lado, 0), pivo=(cx, 27.0, cz), faixa=fx, res=8))
        # viseira: metade da sobrancelha grossa, descendo um pouco para o meio (V bravo) e para a frente
        x0, x1 = sorted((0.0, 5.1 * lado))
        cab.append(peca("viseira_" + s, [x0, 29.4, -23.0], [x1, 31.6, -15.0], mat_viseira, rot=(-6, 0, 10 * lado),
                        pivo=(5.2 * lado, 31.6, -18.0), res=3))
    cab.append(peca("viseira_meio", [-1.6, 28.7, -22.9], [1.6, 30.6, -16.0], mat_viseira, rot=(-6, 0, 0), pivo=(0, 30.6, -18.0), res=3))
    # bico: cunha inclinada que termina num gancho para baixo; mandíbula de baixo recuada
    cab.append(peca("bico", [-1.7, 26.2, -24.0], [1.7, 28.6, -21.0], mat_bico, rot=(-6, 0, 0), pivo=(0, 28.6, -21.0), res=4))
    cab.append(peca("bico_meio", [-1.15, 24.6, -25.6], [1.15, 27.4, -21.2], mat_bico, rot=(-8, 0, 0), pivo=(0, 27.4, -21.2), res=4))
    cab.append(peca("bico_gancho", [-0.6, 23.0, -26.6], [0.6, 25.4, -24.8], mat_bico, rot=(-14, 0, 0), pivo=(0, 25.4, -24.8), res=4))

    cab.append(peca("bico_baixo", [-0.8, 24.2, -23.2], [0.8, 25.2, -20.8], g.mat_cor(lambda p, f: BICO_ESC, borda=.08), res=4))
    # crista de brasa: lâminas vermelhas em degrau; a da frente já sobe sobre a viseira, a do meio é a mais alta
    # (e estreita: de frente é a 'coluna' de cima), as de trás caem por cima da nuca
    cr = []
    LAMINAS = [  # (meia largura, y0, y1, z0, z1, inclinação para trás): moicano estreito, o mais alto no meio
        (2.0, 31.0, 35.6, -22.2, -18.8, 2),
        (2.2, 30.8, 38.0, -20.2, -16.4, 6),
        (1.8, 31.0, 39.4, -17.6, -13.8, 6),
        (2.2, 30.6, 36.8, -14.8, -11.2, 12),
        (2.0, 29.8, 34.4, -12.4, -9.2, 22),
    ]
    for k, (xm, y0, y1, z0, z1, inc) in enumerate(LAMINAS):
        cr.append(bloco_crista(f"crista{k}", [-xm, y0, z0], [xm, y1, z1], rot=(inc, 0, 0), pivo=(0, y0, z1)))
    for lado in (-1, 1):   # degraus mais baixos dos lados do moicano (de frente: a 'cruz' em escada da ficha)
        s = "d" if lado < 0 else "e"
        for k, (xa, xb, y0, y1, z0, z1, inc) in enumerate([(1.8, 4.8, 30.9, 34.0, -21.0, -17.0, 4),
                                                           (1.8, 4.2, 30.7, 35.0, -15.4, -11.4, 12)]):
            x0, x1 = sorted((xa * lado, xb * lado))
            cr.append(bloco_crista(f"crista_degrau{k}_{s}", [x0, y0, z0], [x1, y1, z1], rot=(inc, 0, 0), pivo=(0, y0, z1)))
    for lado in (-1, 1):     # lóbulos vermelhos dos lados da nuca (aparecem de frente e de trás)
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((4.8 * lado, 6.5 * lado))
        cr.append(bloco_crista("crista_lado_" + s, [x0, 25.6, -16.0], [x1, 30.6, -12.6]))
    cab.append(osso("crista", [0, 31.0, -16.0], [0, 0, 0], cr))
    # penas das bochechas: vermelhas -> laranja, varrendo para trás por baixo e atrás do olho
    boch = []
    for k, (x, y0, z0, L, rx, rz) in enumerate([(4.4, 29.2, -14.2, 6.6, -76, 16), (4.4, 27.2, -15.4, 7.0, -64, 22),
                                                (4.4, 25.4, -13.2, 7.4, -56, 30), (3.8, 25.0, -17.8, 6.2, -30, 20)]):
        for lado in (-1, 1):
            s = "d" if lado < 0 else "e"
            cores = [(CRISTA, VERM, LARANJA), (VERM, LARANJA_ESC, LARANJA), (LARANJA_ESC, LARANJA, AMARELO),
                     (LARANJA_ESC, LARANJA, AMARELO)][k]
            boch.append(pena_bloco(f"bochecha{k}_{s}", (x * lado, y0, z0), (rx, 0, rz * lado), L, 3.4, cores, esp=1.3))
    cab.append(osso("bochechas", [0, 26, -15], [0, 0, 0], boch))
    cabeca = osso("cabeca", [0, 24.0, -16.0], [0, 0, 0], cab)
    # juba: penas grossas em volta do alto do pescoço, abrindo para os lados
    juba = []
    C1, C2, C3 = (VERM, LARANJA, AMARELO), (LARANJA_ESC, LARANJA, AMARELO), (LARANJA, AMARELO, AMARELO_CLARO)
    JUBA = [  # (x, y, z, phi, abertura, varrida, comprimento, largura, cores) do lado esquerdo (+x); o direito é espelho
        (2.8, 24.2, -19.8, -90, 6, 34, 6.4, 3.4, C1),       # 'babador' de frente, abrindo para os lados
        (4.2, 25.2, -16.6, -30, 24, 34, 9.0, 3.8, C1),      # leque dos lados e de trás, varrendo para trás
        (4.6, 25.4, -13.6, 10, 26, 46, 10.0, 4.0, C1),
        (3.8, 25.6, -10.6, 55, 24, 58, 9.6, 3.8, C2),
        (4.6, 22.6, -14.4, -5, 30, 34, 8.6, 3.8, C2),
        (4.4, 22.4, -11.0, 35, 28, 46, 8.8, 3.8, C3),
        (3.6, 22.0, -8.8, 70, 24, 54, 8.0, 3.4, C3),
    ]
    for k, (x, y0, z, phi, fl, var, L, W, cores) in enumerate(JUBA):
        for lado in (-1, 1):
            juba.append(pena_cone(f"juba{k}_{'d' if lado < 0 else 'e'}", (x * lado, y0, z), phi, fl, L, W, lado, cores,
                                  varre=var, esp=1.4))
    juba.append(pena_cone("juba_nuca", (0, 25.4, -9.6), 90, 0, 9.0, 4.0, 1, C2, varre=50, esp=1.8))
    juba = osso("juba", [0, 22.0, -14.0], [0, 0, 0], juba)
    deslocar(i_cab, [cabeca, juba], DZ_CAB)

    # ---------- pescoço em S: a base sai inclinada do peito, o alto sobe ereto até a cabeça; placas laranja na frente ----------
    pesc = []
    def mat_pesc(z_frente):
        return g.mat_cor(lambda p, f: PLACA_ESC if p[2] < z_frente + 1.6 else GRAFITE, borda=.03, curva=.3)
    PESC = [  # (nome, meia largura, y0, y1, z0, z1, inclinação, pivô)
        ("pescoco_baixo", 3.4, 6.4, 23.6, -16.8, -10.2, -40, (0, 15.0, -16.8)),

        ("pescoco_alto", 3.4, 17.6, 25.4, -21.8, -15.6, -12, (0, 22.0, -19.0)),

    ]
    for nome, xm, y0, y1, z0, z1, inc, pv in PESC:
        pesc += g.octogono(nome, [-xm, y0, z0], [xm, y1, z1], mat_pesc(z0), r=1.0, faixa=(9, 27), rot=(inc, 0, 0), pivo=pv)

    # placas: 7 degraus de frente vertical seguindo a linha da garganta ao peito (medida na ficha)
    def z_frente(y):
        return -21.6 - (y - 20.0) * 0.25 if y >= 20 else -12.6 - (y - 10.0) * 0.84
    for k, (yb, ya, w) in enumerate([(22.4, 24.6, 3.2), (20.3, 22.6, 3.9), (18.2, 20.5, 4.5), (16.1, 18.4, 4.9),
                                     (14.0, 16.3, 5.0), (11.9, 14.2, 4.7), (9.8, 12.1, 4.0)]):
        zf = z_frente((ya + yb) / 2) - 0.5
        pesc.append(peca(f"placa{k}", [-w, yb, zf], [w, ya, zf + 2.6], mat_placa, res=3))
    pesc += [juba, cabeca]
    pescoco = osso("pescoco", [0, 16.0, -13.0], [0, 0, 0], pesc)

    # ---------- tronco de salamandra ----------
    corpo = []
    mt = mat_com_manchas(cor_corpo, MANCHAS_CORPO, borda=.02, curva=.45)
    bt = brilho_manchas(MANCHAS_CORPO)
    fc = (8.4, 22.6)
    corpo += g.arredondado2("peito", [-5.8, 8.8, -13.6], [5.8, 22.8, -3.0], mt, r=2.4, faixa=fc, brilho=bt)
    corpo += g.arredondado2("meio", [-5.9, 8.8, -5.0], [5.9, 22.0, 5.0], mt, r=2.4, faixa=fc, brilho=bt)
    corpo += g.arredondado2("quadril", [-5.6, 8.8, 3.0], [5.6, 20.4, 13.4], mt, r=2.4, faixa=fc, brilho=bt)
    corpo += [ombro(-1), ombro(1)]
    # cauda grossa: corre para trás, sobe pela traseira e volta por cima num gancho para a frente
    Ls = [4.4, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.6, 3.2, 2.8, 2.6, 2.0]
    Rs = [18, -18, -32, -30, -26, -24, -26, -26, -16, -4, 2, 4]
    Hs = [7.8, 7.6, 7.4, 7.2, 7.0, 6.8, 6.5, 6.0, 5.5, 5.0, 4.6, 4.2]
    Ws = [10.4, 10.6, 10.8, 11.0, 10.8, 10.2, 9.4, 8.6, 7.8, 7.0, 6.4, 5.8]
    corpo.append(osso("cauda", [0, 13.5, 11.5], [0, 0, 0], [cauda_gancho("rabo", (0, 13.5, 11.5), list(zip(Ls, Ws, Hs, Rs)))]))
    corpo.append(pescoco)
    tronco = osso("corpo", [0, 14.0, 6.0], [0, 0, 0], corpo)

    pernas = [perna("perna_fd", -7.0, -10.8, False), perna("perna_fe", 7.0, -10.8, False),
              perna("perna_td", -7.0, 8.4, True), perna("perna_te", 7.0, 8.4, True)]
    return [tronco] + pernas

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
