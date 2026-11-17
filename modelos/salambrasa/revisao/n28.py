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

# ---------------- paleta: quadros da Paleta de Cores da _ficha (amostrados com PIL) ----------------
# carvão (46,35,44) · cinza-roxo (103,78,95) · malva (131,94,111) · vermelho (202,24,30) · laranja-vermelho (253,69,11)
# laranja (253,115,2) · amarelo (254,201,37) · creme (251,223,198)
GRAFITE = (66, 51, 62); GRAFITE_ESC = (46, 35, 44); GRAFITE_CLARO = (87, 70, 80)        # corpo carvão-arroxeado
CABECA = (82, 64, 76); CABECA_CLARA = (103, 78, 95); CABECA_ESC = (58, 46, 54)          # cabeça carvão-malva
FACE = (96, 74, 88)                                                                       # um pouco mais clara sob o olho
VISEIRA = (60, 47, 56); VISEIRA_CLARA = (84, 66, 78); VISEIRA_ESC = (46, 35, 44)         # sobrancelha/capacete mais escura
BICO = (131, 94, 111); BICO_CLARO = (150, 116, 130); BICO_ESC = (100, 72, 86)            # malva
DEDO = (180, 162, 172); DEDO_CLARO = (204, 190, 198); DEDO_ESC = (146, 128, 140)         # lavanda-acinzentado claro
CRISTA = (224, 40, 40); CRISTA_ESC = (176, 24, 28); CRISTA_CLARA = (240, 72, 72)         # vermelho vivo, topo mais claro
VERM = (200, 40, 32); VERM_ESC = (170, 26, 24)
LARANJA = (240, 112, 32); LARANJA_ESC = (253, 69, 11); AMARELO = (248, 176, 32); OURO = (248, 192, 32)
PLACA = (244, 160, 80); PLACA_CLARA = (250, 184, 112); PLACA_ESC = (208, 106, 32)         # escudo do peito / barriga
VENTRE = (232, 138, 48)
CREME = (244, 230, 220)
BRASA = (248, 192, 32); BRASA_BORDA = (240, 112, 32)                                     # manchas: amarelo cheio, borda laranja

def escurecer(c, f):
    """Escurece mantendo o matiz (sem puxar para o oliva)."""
    return tuple(int(v * (1 - f)) for v in c)

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
        cor = hexa(a, b)
        if cor: return cor
    return None

def hexa(a, b, borda=0.16):
    """Mancha da ficha: octógono amarelo cheio com borda laranja fina (a, b normalizados pelo meio-tamanho)."""
    d = max(abs(a), abs(b), (abs(a) + abs(b)) / 1.4)
    if d > 1: return None
    return BRASA_BORDA if d > 1 - borda else BRASA

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
        base = c0 if v < 0.42 else c1 if v < 0.78 else c2           # vermelho na raiz, laranja, amarelo só na ponta
        face = c["face"]
        if face == "up": base = mix(base, (255, 236, 200), 0.15)
        elif face == "down": base = escurecer(base, 0.3)
        elif face in ("north", "south"): base = escurecer(base, 0.1)
        return escurecer(base, 0.15) if g.na_borda(c) else base
    return f

def pena_bloco(nome, raiz, rot, L, W, cores, esp=1.0, brilho=False):
    """Pena (ou escama) grossa: bloco + ponta em losango (cubo girado 45°), pendurada para baixo da raiz."""
    return g.placa_armadura(nome, raiz, rot, L, W, esp=esp, mat=mat_pena_bloco(cores, raiz[1], 0.72 * L + W / 2))

def pena_cone(nome, raiz, phi, flare, L, W, lado, cores, varre=0, esp=1.0):
    """Pena grossa numa 'saia' em volta do pescoço (phi = 0 lado de fora, negativo = frente)."""
    return osso(nome, list(raiz), [0, -phi * lado, 0], [pena_bloco(nome + "_p", raiz, (-varre, 0, flare * lado), L, W, cores, esp)])

# ---------------- corpo ----------------
VENTRE_Y = 11.2          # abaixo disso: a faixa laranja da barriga, do peito até a cauda

def cor_corpo(p, face):
    x, y, z = p
    if face == "down" or y < VENTRE_Y: return VENTRE
    return GRAFITE

# (centro, meio-tamanho, profundidade): profundidade pequena = só na face de fora (sem frestas nas faces de baixo)
MANCHAS_CORPO = [((0, 22.0, 0.0), (1.6, 1, 1.3), 0.3),            # 3 em fila no dorso, entre a asa e o quadril
                 ((0, 22.8, -7.8), (1.5, 1, 1.2), 0.3),
                 ((0, 20.4, 7.8), (1.6, 1, 1.3), 0.3)]
for lado in (-1, 1):
    MANCHAS_CORPO += [((5.9 * lado, 14.4, 1.0), (1, 1.2, 1.5), 0.3),      # flanco
                      ((5.6 * lado, 17.0, 7.4), (1, 1.1, 1.4), 0.3)]      # quadril

def mat_placa(c):
    """Placa laranja da barriga: em cima pêssego claro, frente laranja com cantos arredondados (mais escuros), fio
    escuro na beirada de baixo; de lado um pouco mais escura."""
    face = c["face"]
    (x0, y0, _), (x1, y1, _) = c["b"]
    v = clamp((y1 - c["p"][1]) / max(y1 - y0, 1e-6))
    u = abs(c["p"][0]) / max(x1, 1e-6)
    if face == "up": return PLACA_CLARA
    if face == "down": return PLACA_ESC
    base = PLACA_CLARA if v < 0.2 else PLACA
    if face in ("east", "west"): base = escurecer(PLACA, 0.1)
    if v > 0.85 or (face == "north" and u > 0.9): base = PLACA_ESC        # linha escura entre as faixas
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
            if face == "down": return VENTRE
            if v < 0.3: return VENTRE
            return GRAFITE
        if face == "down": return GRAFITE
        if face == "up": return GRAFITE
        if k < 7:
            return VENTRE if v < 0.24 else GRAFITE
        return VENTRE if v > 0.8 else GRAFITE
    fundo = g.mat_cor(cor, borda=.0, curva=.2)
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
        filhos = secao(f"{nome}_{k}", px, py, pz - 0.8, pz + L, w, h, mat, br)       # sobreposto: sem frestas
        if k > 0:
            wp, hp = (segs[k - 1][1] + w) / 2, (segs[k - 1][2] + h) / 2
            e = 0.5 + (hp / 2) * math.tan(math.radians(abs(rx) / 2))
            mj, bj = mat_rabo(wp, hp, py, pz, L, k, [((px, py, pz), -rx / 2)] + cad)
            filhos += secao(f"{nome}_{k}_junta", px, py, pz - e, pz + e, wp, hp, mj, bj, rot=(-rx / 2, 0, 0), pivo=(px, py, pz))
        if k + 1 < len(segs): filhos.append(seg(k + 1, (px, py, pz + L), cad))
        else:
            filhos += secao(f"{nome}_ponta", px, py, pz + L - 0.2, pz + L + 1.0, w * 0.7, h * 0.7, mat, br)
        return osso(f"{nome}_{k}", [px, py, pz], [rx, 0, 0], filhos)
    return seg(0, base, [])

# ---------------- cabeça ----------------
OLHO_Y = 28.3
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
    if y < 27.0 and face != "down": return FACE
    return CABECA

def mat_faceta(lado):
    base = g.mat_cor(cor_cabeca, borda=.0, curva=.25)
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u = z - FAC_C[1]
            o = g.pintar_olho(u + 0.1, y - OLHO_Y, 1.95, 1.6, iris=((150, 30, 14), (216, 64, 28)), esclera=CREME,
                              r_iris=(0.6, 0.82), c_iris=(-0.34, -0.1), r_pup=(0.26, 0.32), bravo=0.3, alto=0.3,

                              contorno=(192, 48, 24))
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
    if face == "up" and 0.5 < abs(x) < 1.0 and -23.9 < z < -23.2: return (52, 38, 46)    # narina
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
        if d < 0.38: return BRASA
        if d < 0.62: return BRASA_BORDA
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
    for k in range(5):   # leque de penas longas sob as escamas, para trás e para baixo, umas sobre as outras
        raiz = (6.0 * lado + 0.15 * lado * k, 19.4 - 0.2 * k, -10.4 + 1.6 * k)
        filhos.append(pena_bloco(f"fogo{k}_{s}", raiz, (-(54 + 4 * k), 0, 20 * lado), 9.4 - 0.5 * k, 2.4,
                                 (VERM, LARANJA, OURO), esp=1.2))
    # ombreira: olha meio para a frente, cobre o alto da pata
    m0, b0 = mat_escama(lado, (0, 0, 0), False)
    filhos.append(escama(f"ombreira_{s}", (6.4 * lado, 21.4, -11.2), (-14, 0, 14 * lado), 38 * lado, 4.6, 4.2, m0, b0))
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
    escuro = g.mat_cor(lambda p, f: GRAFITE, borda=.05, curva=.2)
    def cor_faixa(p, f, tras=tras):
        y0, y1 = (3.6, 7.0) if tras else (4.2, 9.0)
        t = (p[1] - y0) / (y1 - y0)
        return escurecer(LARANJA, 0.3) if 0.42 < t < 0.56 else LARANJA
    faixa = g.mat_cor(cor_faixa, borda=.04, curva=.1)
    if tras:     # coxa grande com uma mancha incandescente do lado de fora
        lado = 1 if xc > 0 else -1
        mc = [((xc + 2.2 * lado, 12.2, zc - 0.2), (1, 1.6, 1.8), 0.9)]
        xt = xc - 0.6 * lado
        pp += g.arredondado2(nome + "_coxa", [xt - 2.8, 7.4, zc - 3.8], [xt + 2.8, 15.4, zc + 3.6],
                             mat_com_manchas(lambda p, f: GRAFITE, mc, borda=.05, curva=.2), r=2.0, brilho=brilho_manchas(mc))
    else:
        pp += g.arredondado2(nome + "_braco", [xc - 2.8, 7.0, zc - 2.7], [xc + 2.8, 14.6, zc + 2.7], escuro, r=1.2,

                            rot=(16, 0, 0), pivo=(xc, 7.2, zc))
    yf0, yf1 = (3.6, 7.0) if tras else (4.2, 9.0)        # faixa laranja: mais baixa atrás, mais alta na frente
    pp += g.octogono(nome + "_faixa", [xc - 2.35, yf0, zc - 2.35], [xc + 2.35, yf1, zc + 2.35], faixa, r=0.7)
    pp += g.octogono(nome + "_tornozelo", [xc - 2.45, 2.4, zc - 2.45], [xc + 2.45, yf0 + 0.2, zc + 2.45], escuro, r=0.7)
    pp += pata(nome, xc, zc)
    return osso(nome, [xc, 12.0, zc], [0, 0, 0], pp)

# ---------------- deslocar um grupo inteiro (a pintura continua nas coordenadas de quando foi modelado) ----------------
def deslocar(desde, nos, dz, dy=0.0):
    """Empurra em z (dz) as peças criadas desde o índice 'desde' e os ossos 'nos'. Os materiais recebem o ponto de
    volta nas coordenadas originais, então desenhos que dependem da posição (o olho, as faixas) não mudam."""
    def volta(c):
        c = dict(c); x, y, z = c["p"]; c["p"] = (x, y - dy, z - dz)
        b0, b1 = c["b"]; c["b"] = ([b0[0], b0[1] - dy, b0[2] - dz], [b1[0], b1[1] - dy, b1[2] - dz])
        return c
    for pc in g.PECAS[desde:]:
        for arr in (pc.de, pc.ate, pc.pivo): arr[2] += dz; arr[1] += dy
        m = pc.mat; pc.mat = lambda c, m=m: m(volta(c))
        if callable(pc.brilho):
            b = pc.brilho; pc.brilho = lambda c, cor, b=b: b(volta(c), cor)
    def visita(no):
        if isinstance(no, dict):
            no["origin"][2] += dz; no["origin"][1] += dy
            for f in no["children"]: visita(f)
    for no in nos: visita(no)

DZ_CAB = -2.5; DY_CAB = 1.0            # a cabeça (e a juba) vão para a frente: o bico fica sobre as patas da frente, como na ficha

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
        cab.append(peca("viseira_" + s, [x0, 28.9, -22.6], [x1, 31.4, -15.0], mat_viseira, rot=(-4, 0, 10 * lado),
                        pivo=(5.2 * lado, 31.4, -18.0), res=3))
    cab.append(peca("viseira_meio", [-1.6, 28.6, -22.5], [1.6, 30.4, -16.0], mat_viseira, rot=(-4, 0, 0), pivo=(0, 30.4, -18.0), res=3))
    # bico: cunha inclinada que termina num gancho para baixo; mandíbula de baixo recuada
    cab.append(peca("bico", [-1.7, 26.6, -24.8], [1.7, 28.4, -21.0], mat_bico, res=4))            # topo reto
    cab.append(peca("bico_baixo", [-1.0, 25.4, -24.2], [1.0, 26.8, -21.0], mat_bico, res=4))      # de frente afina em V
    cab.append(peca("bico_gancho", [-0.8, 25.4, -25.6], [0.8, 27.8, -24.4], mat_bico, rot=(-18, 0, 0),
                    pivo=(0, 27.8, -24.4), res=4))
    # crista de brasa: lâminas vermelhas em degrau; a da frente já sobe sobre a viseira, a do meio é a mais alta
    # (e estreita: de frente é a 'coluna' de cima), as de trás caem por cima da nuca
    cr = []
    LAMINAS = [  # (meia largura, y0, y1, z0, z1, inclinação para trás): moicano estreito, o mais alto no meio
        (2.0, 30.8, 34.2, -21.0, -17.6, 14),
        (2.2, 30.8, 36.8, -18.8, -15.0, 18),
        (1.8, 30.8, 39.0, -16.2, -12.4, 20),
        (2.2, 30.4, 36.2, -13.4, -9.8, 24),
        (2.0, 29.6, 33.8, -11.0, -7.8, 30),
    ]
    for k, (xm, y0, y1, z0, z1, inc) in enumerate(LAMINAS):
        cr.append(bloco_crista(f"crista{k}", [-xm, y0, z0], [xm, y1, z1], rot=(inc, 0, 0), pivo=(0, y0, z1)))
    for lado in (-1, 1):   # degraus mais baixos dos lados do moicano (de frente: a 'cruz' em escada da ficha)
        s = "d" if lado < 0 else "e"
        for k, (xa, xb, y0, y1, z0, z1, inc) in enumerate([(1.8, 4.8, 30.8, 33.2, -20.2, -16.2, 14),
                                                           (1.8, 4.4, 30.6, 33.8, -14.6, -10.6, 22)]):
            x0, x1 = sorted((xa * lado, xb * lado))
            cr.append(bloco_crista(f"crista_degrau{k}_{s}", [x0, y0, z0], [x1, y1, z1], rot=(inc, 0, 0), pivo=(0, y0, z1)))
    for lado in (-1, 1):     # lóbulos vermelhos dos lados da nuca (aparecem de frente e de trás)
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((4.8 * lado, 6.2 * lado))
        cr.append(bloco_crista("crista_lado_" + s, [x0, 26.6, -15.4], [x1, 29.8, -13.0]))
    cab.append(osso("crista", [0, 31.0, -16.0], [0, 0, 0], cr))
    # penas das bochechas: vermelhas -> laranja, varrendo para trás por baixo e atrás do olho
    boch = []
    for k, (x, y0, z0, L, rx, rz) in enumerate([(4.4, 29.0, -13.6, 6.4, -70, 14), (4.4, 27.0, -14.6, 6.8, -58, 18),
                                                (4.4, 25.4, -13.0, 7.0, -48, 22)]):
        for lado in (-1, 1):
            s = "d" if lado < 0 else "e"
            cores = [(CRISTA, VERM, LARANJA), (VERM, LARANJA, AMARELO), (VERM, LARANJA, AMARELO)][k]
            boch.append(pena_bloco(f"bochecha{k}_{s}", (x * lado, y0, z0), (rx, 0, rz * lado), L, 3.0, cores, esp=1.3))
    cab.append(osso("bochechas", [0, 26, -15], [0, 0, 0], boch))
    cabeca = osso("cabeca", [0, 24.0, -16.0], [0, 0, 0], cab)
    # juba: penas grossas em volta do alto do pescoço, abrindo para os lados
    juba = []
    C1 = (VERM, LARANJA, AMARELO)                      # degradê da ficha: vermelho na raiz -> laranja -> amarelo
    JUBA = [  # (x, y, z, phi, abertura, varrida, comprimento, largura, cores) do lado esquerdo (+x); o direito é espelho
        (2.4, 24.4, -19.8, -70, 10, 14, 7.0, 3.0, C1),      # frente da garganta, dos lados do bico
        (3.8, 24.6, -17.8, -35, 12, 18, 7.8, 3.2, C1),
        (4.4, 24.8, -15.4, 0, 12, 22, 8.2, 3.4, C1),        # lados
        (4.0, 25.0, -13.0, 35, 12, 26, 7.8, 3.2, C1),       # atrás da cabeça
        (3.2, 22.4, -18.8, -50, 10, 12, 6.6, 3.0, C1),      # 2ª camada, mais baixa
        (4.2, 22.4, -16.2, -10, 12, 16, 7.0, 3.2, C1),
    ]
    for k, (x, y0, z, phi, fl, var, L, W, cores) in enumerate(JUBA):
        for lado in (-1, 1):
            juba.append(pena_cone(f"juba{k}_{'d' if lado < 0 else 'e'}", (x * lado, y0, z), phi, fl, L, W, lado, cores,
                                  varre=var, esp=1.4))
    juba = osso("juba", [0, 22.0, -14.0], [0, 0, 0], juba)
    deslocar(i_cab, [cabeca, juba], DZ_CAB, DY_CAB)

    # ---------- pescoço em S: a base sai inclinada do peito, o alto sobe ereto até a cabeça; placas laranja na frente ----------
    pesc = []
    def mat_pesc(z_frente):
        # a frente do pescoço é laranja (placas) também dos lados, como na vista lateral da ficha
        return g.mat_cor(lambda p, f: PLACA if p[2] < z_frente + 3.0 else GRAFITE, borda=.03, curva=.2)
    PESC = [  # (nome, meia largura, y0, y1, z0, z1, inclinação, pivô)
        ("pescoco_baixo", 3.4, 6.4, 23.6, -16.8, -10.2, -40, (0, 15.0, -16.8)),

        ("pescoco_alto", 3.4, 17.6, 26.4, -22.2, -16.0, -12, (0, 22.0, -19.4)),

    ]
    for nome, xm, y0, y1, z0, z1, inc, pv in PESC:
        pesc += g.octogono(nome, [-xm, y0, z0], [xm, y1, z1], mat_pesc(z0), r=1.0, faixa=(9, 27), rot=(inc, 0, 0), pivo=pv)

    # escudo do peito: 5 faixas coladas na frente do pescoço (0,4 à frente), cada uma inclinada como a curva da
    # garganta ao peito; contorno oval (estreito em cima e embaixo, largo no meio)
    def z_frente(y):
        return -22.0 - (y - 20.0) * 0.25 if y >= 20 else -12.8 - (y - 10.0) * 0.86
    for k, (yb, ya, w) in enumerate([(22.2, 25.4, 2.8), (19.0, 22.4, 3.9), (15.8, 19.2, 4.5), (12.6, 16.0, 4.3), (9.6, 12.8, 3.4)]):
        yc = (ya + yb) / 2; zc = z_frente(yc)
        ang = math.degrees(math.atan(0.25 if yc >= 20 else 0.86))
        pesc.append(peca(f"placa{k}", [-w, yb, zc - 0.4], [w, ya, zc + 1.2], mat_placa, rot=(-ang, 0, 0),
                         pivo=(0, yc, zc), res=3))
    pesc += [juba, cabeca]
    pescoco = osso("pescoco", [0, 16.0, -13.0], [0, 0, 0], pesc)

    # ---------- tronco de salamandra ----------
    corpo = []
    mt = mat_com_manchas(cor_corpo, MANCHAS_CORPO, borda=.02, curva=.22)
    bt = brilho_manchas(MANCHAS_CORPO)
    fc = (8.4, 22.6)
    corpo += g.arredondado2("peito", [-5.8, 8.8, -13.6], [5.8, 22.8, -3.0], mt, r=2.4, faixa=fc, brilho=bt)
    corpo += g.arredondado2("meio", [-5.9, 8.8, -5.0], [5.9, 22.0, 5.0], mt, r=2.4, faixa=fc, brilho=bt)
    corpo += g.arredondado2("quadril", [-5.6, 8.8, 3.0], [5.6, 20.4, 13.4], mt, r=2.4, faixa=fc, brilho=bt)
    corpo += [ombro(-1), ombro(1)]
    # cauda grossa: corre para trás, sobe pela traseira e volta por cima num gancho para a frente
    Ls = [4.4, 3.8, 3.8, 3.8, 3.8, 3.8, 3.8, 3.6, 3.2, 2.8, 2.6, 2.0]
    Rs = [18, -18, -32, -30, -26, -24, -26, -26, -14, -2, 12, 14]
    Hs = [7.8, 7.6, 7.4, 7.0, 6.6, 6.2, 5.7, 5.1, 4.5, 3.9, 3.3, 2.8]
    Ws = [10.4, 10.6, 10.6, 10.2, 9.6, 8.8, 7.8, 6.8, 5.8, 4.8, 4.0, 3.4]
    corpo.append(osso("cauda", [0, 13.5, 11.5], [0, 0, 0], [cauda_gancho("rabo", (0, 13.5, 11.5), list(zip(Ls, Ws, Hs, Rs)))]))
    corpo.append(pescoco)
    tronco = osso("corpo", [0, 14.0, 6.0], [0, 0, 0], corpo)

    pernas = [perna("perna_fd", -7.0, -10.8, False), perna("perna_fe", 7.0, -10.8, False),
              perna("perna_td", -7.0, 8.4, True), perna("perna_te", 7.0, 8.4, True)]
    return [tronco] + pernas

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
