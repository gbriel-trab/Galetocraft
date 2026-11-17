"""Espinhocó (#011, Planta): galo-porco-espinho da floresta, bola de espinhos bege nas costas e plumagem de folhas."""
import math, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, mat_cor, arredondado, arredondado2, octogono, pintar_olho

ID = "espinhoco"; NOME = "Espinhocó"; NUMERO = 11
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 27.5, -7.0), 7.5)
ONDAS = []
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (Paleta de Cores da ficha) ----------------
CREME = (246, 222, 174); CREME_ESC = (220, 182, 128)
BEGE = (240, 192, 124); CARAMELO = (206, 138, 72)
MARROM = (148, 92, 54); MARROM_ESC = (104, 64, 42); CHOCOLATE = (66, 42, 34)
VERDE_ESC = (110, 148, 30); VERDE = (157, 191, 42); VERDE_CLARO = (196, 220, 78); NERVURA = (220, 234, 130)
CONTORNO_FOLHA = (54, 86, 22)
AMARELO_BICO = (248, 198, 38); LARANJA_BICO = (226, 138, 22)
VERM = (216, 38, 32); VERM_ESC = (150, 20, 24); VERM_CLARO = (244, 84, 64)
GARRA = (72, 64, 70); GARRA_CLARA = (108, 100, 106)
CANELA = (184, 118, 60); CANELA_CLARA = (210, 148, 84)

# ---------------- utilidades ----------------
def ruido(x, y, z, passo=0.5):
    """Valor fixo em -1..1 por 'voxel' de textura (variação sutil de tom, como os blocos da ficha)."""
    n = (int(math.floor(x / passo)) * 73856093) ^ (int(math.floor(y / passo)) * 19349663) ^ (int(math.floor(z / passo)) * 83492791)
    n = (n ^ (n >> 13)) * 1274126177
    return ((n >> 8) & 0xffff) / 32767.5 - 1.0

def rot_m(rx, ry, rz):
    a, b, c = (math.radians(v) for v in (rx, ry, rz))
    Rx = [[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]]
    Ry = [[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]]
    Rz = [[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]]
    mm = lambda A, B: [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return mm(Rz, mm(Ry, Rx))

def mv(A, v): return [sum(A[i][k] * v[k] for k in range(3)) for i in range(3)]

def norm(v):
    n = math.sqrt(sum(a * a for a in v)) or 1.0
    return [a / n for a in v]

def apontar(d):
    """Rotação (rx, ry, 0) do osso que leva o eixo local +y para a direção d."""
    dx, dy, dz = norm(d)
    a = math.degrees(math.acos(clamp(dy, -1, 1)))
    b = math.degrees(math.atan2(dx, dz)) if a > 1e-3 else 0.0
    return [a, b, 0.0]

def torcao_para(d, fora):
    """Giro (em torno do próprio eixo) que deixa a normal local +z o mais virada possível para 'fora'."""
    R = rot_m(*apontar(d)); fora = norm(fora)
    melhor, tm = -9, 0
    for t in range(-180, 180, 5):
        n = mv(R, mv(rot_m(0, t, 0), [0, 0, 1]))
        s = sum(n[i] * fora[i] for i in range(3))
        if s > melhor: melhor, tm = s, t
    return tm

def dir_esf(teta, phi):
    """Direção a partir do eixo de trás (+z): teta = abertura (0 = reto para trás), phi = em volta (0 = cima, 90 = esquerda +x)."""
    t, f = math.radians(teta), math.radians(phi)
    return [math.sin(t) * math.sin(f), math.sin(t) * math.cos(f), math.cos(t)]

# ---------------- espinhos ----------------
def cor_tufo(v): return mix(MARROM_ESC, MARROM, v)

def mat_espinho(y0, L, cor_fn=None):
    """Espinho (blocos): raiz marrom -> caramelo -> bege -> creme na ponta, facetas clara/escura, contorno escuro."""
    def f(c):
        v = clamp((c["p"][1] - y0) / L)
        cor = (cor_fn or cor_espinho)(v)
        luz = {"north": .10, "east": .04, "south": -.06, "west": -.02, "up": .18, "down": -.25}[c["face"]]
        if g.na_borda(c): luz -= .25
        return tom(cor, luz)
    return f

ESP_BASE = (110, 66, 40); ESP_MEIO = (184, 122, 70); ESP_CLARO = (222, 172, 114); ESP_PONTA = (240, 212, 166)

def cor_espinho(v):
    if v < 0.26: return mix(ESP_BASE, ESP_MEIO, v / 0.26)
    if v < 0.52: return mix(ESP_MEIO, ESP_CLARO, (v - 0.26) / 0.26)
    return mix(ESP_CLARO, ESP_PONTA, (v - 0.52) / 0.3)

SEG_ESPINHO = ((0.30, 1.0), (0.24, 0.74), (0.18, 0.5))     # (fração do comprimento, fração da largura)

def mat_ponta(y0, L, yb, Lp, Wp, eixo, centro, luz0, cor_fn=None):
    """Ponta do espinho (placa recortada em triângulo de lados cheios): aresta clara no meio, um lado mais escuro."""
    def f(c):
        x, y, z = c["p"]
        t = (y - yb) / Lp
        if t < -0.01 or t > 1: return None
        u = ((x if eixo == "x" else z) - centro) / (Wp / 2)
        meia = (1 - max(t, 0)) ** 0.75
        if abs(u) > meia: return None
        cor = (cor_fn or cor_espinho)(clamp((y - y0) / L))
        luz = luz0 + (0.1 if abs(u) < 0.14 else -0.08 if u > 0 else 0.0)
        return tom(cor, luz)
    return f

def espinho(nome, raiz, d, L, W, torce=45, cor_fn=None):
    """Espinho grosso em cone de blocos: 3 degraus sólidos que afinam (leem de todos os lados e, de ponta, viram os
    degraus da vista traseira da ficha) e a ponta afiada em X (duas placas recortadas, a 45° dos blocos)."""
    x, y, z = raiz
    m = mat_espinho(y, L, cor_fn)
    pecas, y1 = [], y
    for k, (fl, fw) in enumerate(SEG_ESPINHO):
        h, w = L * fl, W * fw
        pecas.append(peca(f"{nome}_{k}", [x - w / 2, y1, z - w / 2], [x + w / 2, y1 + h, z + w / 2], m, res=3))
        y1 += h - 0.05
    yb = y1 - 0.1; Lp = L - (yb - y); Wp = W * 0.62; e = 0.3
    pecas.append(osso(nome + "_p", [x, yb, z], [0, 45, 0], [
        peca(nome + "_pa", [x - e / 2, yb, z - Wp / 2], [x + e / 2, yb + Lp, z + Wp / 2], mat_ponta(y, L, yb, Lp, Wp, "z", z, .06, cor_fn), res=6),
        peca(nome + "_pb", [x - Wp / 2, yb, z - e / 2], [x + Wp / 2, yb + Lp, z + e / 2], mat_ponta(y, L, yb, Lp, Wp, "x", x, -.04, cor_fn), res=6)]))
    return osso(nome, list(raiz), apontar(d), [osso(nome + "_t", list(raiz), [0, torce, 0], pecas)])

# ---------------- folhas (dobradas na nervura, em V) ----------------
def mat_folha(x0, y0, L, W, s, claro, cores=(VERDE_ESC, VERDE, VERDE_CLARO), nervura=NERVURA, contorno=CONTORNO_FOLHA):
    c0, c1, c2 = cores
    def f(c):
        x, y, z = c["p"]
        u = (x - x0) * s / (W / 2); v = (y - y0) / L
        if v < 0 or v > 1 or u < -0.05: return None
        meia = max(0.14, math.sin(math.pi * clamp(v) ** 0.8)) ** 0.85
        if u > meia: return None
        cor = mix(c0, c1, v / 0.45) if v < 0.45 else mix(c1, c2, (v - 0.45) / 0.55)
        cor = tom(cor, 0.10 if claro else -0.16)
        if u * W / 2 < 0.2 and v < 0.94: return tom(nervura, 0.0 if claro else -0.22)
        if (meia - u) * W / 2 < 0.18: return tom(cor, -0.14)
        return cor
    return f

def folha(nome, raiz, d, L, W, fora=None, torce=None, dobra=20, cores=(VERDE_ESC, VERDE, VERDE_CLARO), esp=0.3,
          nervura=NERVURA, contorno=CONTORNO_FOLHA):
    """Folha lanceolada dobrada na nervura (duas meias placas em V): lê de frente, de lado e de 3/4.
    Cresce na direção d; a face convexa (nervura saltada) fica virada para 'fora'."""
    x, y, z = raiz
    if torce is None: torce = torcao_para(d, fora or [0, 0, -1])
    pa = peca(nome + "_a", [x, y, z - esp / 2], [x + W / 2, y + L, z + esp / 2], mat_folha(x, y, L, W, 1, True, cores, nervura, contorno),
              rot=(0, dobra, 0), pivo=(x, y, z), res=6)
    pb = peca(nome + "_b", [x - W / 2, y, z - esp / 2], [x, y + L, z + esp / 2], mat_folha(x, y, L, W, -1, False, cores, nervura, contorno),
              rot=(0, -dobra, 0), pivo=(x, y, z), res=6)
    return osso(nome, list(raiz), apontar(d), [osso(nome + "_t", list(raiz), [0, torce, 0], [pa, pb])])

# ---------------- cabeça ----------------
HW = 5.2          # meia largura da cabeça
QX = 2.5          # meia largura da frente reta (onde nasce o bico)
ZF = -9.0         # frente da cabeça
FL = math.hypot(HW - QX, HW - QX)       # comprimento da face diagonal (olho)
ZS = ZF + (HW - QX)                     # z onde a face diagonal encontra o lado
FT = 1.8                                # espessura da peça da face diagonal
OLHO_Y = 27.4
CAB_Y0, CAB_Y1 = 23.6, 31.2

def cor_cabeca(p, face):
    x, y, z = p
    r = ruido(x, y, z) * 0.04
    if face == "up" or y > 29.0 + 0.25 * (z + 6):
        return tom(mix(MARROM, CARAMELO, 0.25), r)
    if z < -4.6 and y < (27.0 if abs(x) < QX + 0.2 else 26.6):
        return tom(CREME, r)
    return tom(mix(MARROM, MARROM_ESC, clamp((z + 3) / 3)), r)

def fc_centro(lado):
    mx, mz = (QX + HW) / 2, (ZF + ZS) / 2
    n = (0.7071, -0.7071)
    return (lado * (mx - n[0] * FT / 2), mz - n[1] * FT / 2)

def mat_faceta(lado):
    base = mat_cor(cor_cabeca, borda=.03, curva=.3)
    fora = "east" if lado > 0 else "west"
    cx, cz = fc_centro(lado)
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u = z - cz + 0.05
            cor = pintar_olho(u, y - OLHO_Y, 1.25, 1.0, iris=((96, 132, 14), (200, 226, 64)), c_iris=(-0.12, -0.12),
                              r_iris=(0.8, 0.98), r_pup=(0.3, 0.42), bravo=0.38, alto=0.3, contorno=(60, 40, 30))
            if cor is not None: return cor
            # pele clara em volta do olho
            if (u / 1.6) ** 2 + ((y - OLHO_Y) / 1.25) ** 2 <= 1 and y < 28.6: return tom(CREME, 0.06)
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face == "down": return LARANJA_BICO
    if face in ("east", "west") and abs(z - ZF + 0.9) < 0.28 and abs(y - 26.9) < 0.24: return (120, 70, 20)   # narina
    if face == "north": return mix(AMARELO_BICO, LARANJA_BICO, clamp((26.6 - y) / 2.2))
    return mix(AMARELO_BICO, LARANJA_BICO, clamp((-z - 10.5) / 2.6) * 0.8)

def cor_barbela(p, face):
    x, y, z = p
    c = mix(VERM, VERM_ESC, clamp((23.6 - y) / 3.2) * 0.5)
    if abs(x) < 0.55: c = tom(c, -0.25)
    return c

def montar_cabeca():
    i0 = len(g.PECAS)
    cab = []
    mc = mat_cor(cor_cabeca, borda=.03, curva=.3)
    fx = (CAB_Y0 - 0.6, CAB_Y1 + 0.4)
    cab.append(peca("cranio_a", [-HW, CAB_Y0 + 0.4, ZS], [HW, CAB_Y1 - 0.4, -1.6], mc, faixa=fx, res=4))
    cab.append(peca("cranio_b", [-HW + 0.5, CAB_Y0, ZS - 0.4], [HW - 0.5, CAB_Y1, -1.0], mc, faixa=fx, res=4))
    cab.append(peca("cranio_frente", [-QX, CAB_Y0, ZF], [QX, CAB_Y1 - 0.25, ZS], mc, faixa=fx, res=4))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = fc_centro(lado)
        cab.append(peca("cranio_faceta_" + s, [cx - FT / 2, CAB_Y0 + 0.2, cz - FL / 2], [cx + FT / 2, CAB_Y1 - 0.5, cz + FL / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, OLHO_Y, cz), faixa=fx, res=8))
    # sobrancelhas pesadas (marrom-chocolate) descendo para o bico: cara brava
    msob = g.mat_facetado((112, 76, 56), (88, 58, 44), CHOCOLATE, (40, 26, 22), quina=-0.35)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = fc_centro(lado)
        ox = cx + lado * (FT / 2)
        x0, x1 = sorted((ox - 0.3 * lado, ox + 0.9 * lado))
        cab.append(osso("sobrancelha_" + s, [cx, 29.0, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s, [x0, 28.5, cz - FL / 2 - 0.3], [x1, 29.9, cz + FL / 2 + 0.3], msob,
                 rot=(-16, 0, 0), pivo=(cx, 29.2, cz))]))
        x0, x1 = sorted(((HW - 0.3) * lado, (HW + 0.5) * lado))
        cab.append(peca("sobrancelha_lado_" + s, [x0, 29.3, ZS - 0.2], [x1, 30.5, ZS + 2.4], msob, rot=(-10, 0, 0), pivo=(HW * lado, 29.9, ZS)))
        x0, x1 = sorted((0.2 * lado, (QX + 0.3) * lado))
        cab.append(peca("sobrancelha_frente_" + s, [x0, 28.4, ZF - 0.7], [x1, 29.6, ZF + 0.6], msob,
                        rot=(0, 0, 18 * lado), pivo=((QX + 0.3) * lado, 29.0, ZF)))
    # bico amarelo em cunha com gancho
    mb = mat_cor(cor_bico, borda=.05, curva=.35)
    fb = (24.0, 27.8)
    cab.append(peca("bico_base", [-1.45, 25.3, ZF - 1.5], [1.45, 27.7, ZF + 0.3], mb, faixa=fb, res=4))
    cab.append(peca("bico_meio", [-1.15, 25.2, ZF - 2.8], [1.15, 27.4, ZF - 1.4], mb, rot=(-14, 0, 0), pivo=(0, 27.4, ZF - 1.4), faixa=fb, res=4))
    cab.append(peca("bico_gancho", [-0.7, 24.3, ZF - 3.7], [0.7, 26.6, ZF - 2.6], mat_cor(cor_bico, borda=.05, curva=.6),
                    rot=(-30, 0, 0), pivo=(0, 26.6, ZF - 2.6), faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-1.05, 24.5, ZF - 2.3], [1.05, 25.35, ZF + 0.2], mat_cor(lambda p, f: LARANJA_BICO, borda=.12), res=4))
    # barbela vermelha em dois lóbulos
    mbb = mat_cor(cor_barbela, borda=.08, curva=.4)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.3 * lado, 1.75 * lado))
        cab.append(osso("barbela_" + s, [0.3 * lado, 24.6, ZF - 0.6], [0, 0, 14 * lado], [
            peca("barbela_" + s, [x0, 21.0, ZF - 2.0], [x1, 24.4, ZF + 0.2], mbb, faixa=(20.0, 24.8), res=4),
            peca("barbela_ponta_" + s, [x0 + 0.3 * lado, 20.0, ZF - 1.7], [x1 - 0.2 * lado, 21.2, ZF - 0.1], mbb, faixa=(20.0, 24.8), res=4)]))
    # crista de folhas: leque alto saindo do alto da cabeça
    crista = []
    FRENTE_C = [(0, 0, 10.5, 5.2), (-26, 8, 9.2, 5.0), (26, 8, 9.2, 5.0), (-52, 16, 7.6, 4.6), (52, 16, 7.6, 4.6)]
    for k, (ang, tras, L, W) in enumerate(FRENTE_C):
        d = [math.sin(math.radians(ang)), math.cos(math.radians(ang)), math.tan(math.radians(tras + 14))]
        crista.append(folha(f"crista{k}", (1.8 * math.sin(math.radians(ang)), 30.4, -7.6), d, L, W, fora=[0, 0.2, -1], dobra=32))
    # fileira de trás: varre para trás e fica de lado (lê larga de perfil, como o tufo da ficha)
    TRAS_C = [(-1, 12, 40, 10.0, 5.2), (1, 12, 40, 10.0, 5.2), (-1, 30, 62, 9.0, 5.0), (1, 30, 62, 9.0, 5.0), (0, 0, 78, 8.0, 4.6)]
    for k, (lado, abre, tras, L, W) in enumerate(TRAS_C):
        a, t = math.radians(abre), math.radians(tras)
        d = [lado * math.sin(a), math.cos(t), math.sin(t)]
        crista.append(folha(f"crista_tras{k}", (1.4 * lado, 30.6, -4.4 + 0.4 * k), d, L, W,
                            fora=[lado if lado else 1, 0.3, 0], dobra=28))
    cab.append(osso("crista", [0, 31.0, -5.0], [26, 0, 0], crista))
    # folhas da nuca: descem por cima do pescoço até os ombros
    for k, (ang, L) in enumerate(((0, 8.0), (-32, 7.4), (32, 7.4), (-62, 6.6), (62, 6.6))):
        a = math.radians(ang)
        d = [math.sin(a) * 0.8, -0.55, 0.8]
        cab.append(folha(f"nuca{k}", (2.6 * math.sin(a), 29.4, -1.8), d, L, 4.4, fora=[math.sin(a), 0.8, 0.5]))
    return i0, cab

# ---------------- corpo ----------------
def meia_peito(y):
    """Meia largura do peito creme na altura y (largo embaixo da barbela, afinando até a barriga)."""
    return 3.0 + 2.2 * clamp((y - 10.6) / 7.5) ** 0.7 - 1.6 * clamp((y - 19.5) / 4.0) ** 1.5

def dente(x, passo=1.35):
    """Onda triangular 0..1 (pontas de pena)."""
    t = (x / passo) % 1.0
    return 1 - abs(t - 0.5) * 2

def mat_camada(yb, yt):
    """Camada de penas creme do peito: pontas recortadas embaixo (dentes), sombra perto da ponta,
    risco escuro entre as penas e luz em cima."""
    def f(c):
        x, y, z = c["p"]
        if abs(x) > meia_peito(y) + 0.5: return None
        borda = yb + 1.0 * (1 - dente(x))
        if y < borda: return None
        t = clamp((y - borda) / 1.8)
        cor = mix(CREME_ESC, CREME, t)
        if c["face"] == "north":
            if y < borda + 0.35: cor = tom(cor, -0.22)
            elif dente(x) < 0.12 and y < borda + 1.6: cor = tom(cor, -0.12)
            if y > yt - 0.4: cor = tom(cor, 0.12)
        elif c["face"] in ("east", "west", "down"): cor = tom(cor, -0.18)
        else: cor = tom(cor, 0.15)
        return tom(cor, ruido(x, y, z) * 0.04)
    return f

def cor_corpo(p, face):
    x, y, z = p
    r = ruido(x, y, z) * 0.05
    # peito creme ('Flor Peitoral'): escudo arredondado que afina para baixo
    if z < -4.5 and abs(x) < meia_peito(y) and y > 10.6:
        return tom(CREME, r + 0.04 * clamp((y - 16) / 6))
    # penas marrons em escamas
    fila = math.floor((26 - y) / 1.4)
    fy = ((26 - y) / 1.4) % 1.0
    fx = ((x + z + (0.7 if fila % 2 else 0)) / 1.4) % 1.0
    base = mix(MARROM, MARROM_ESC, clamp((14 - y) / 6))
    if fy > 0.7 - 0.3 * abs(fx - 0.5): base = tom(base, -0.18)
    return tom(base, r)

def cor_coxa(p, face):
    x, y, z = p
    r = ruido(x, y, z) * 0.05
    a = math.atan2(z, abs(x) - 3.4)
    barra = 5.9 + 0.7 * abs(math.sin(a * 3.0))
    if y < barra: return tom(MARROM_ESC, r)
    return tom(mix(MARROM, CARAMELO, clamp((y - 7) / 6) * 0.4), r)

def cor_canela(p, face):
    x, y, z = p
    c = mix(CANELA, CANELA_CLARA, clamp((y - 2) / 4) * 0.5)
    if (y * 1.25) % 1.0 < 0.14: c = tom(c, -0.15)       # escamas da canela
    return c

def montar():
    # ---------- cabeça, pescoço ----------
    i_cab, cab = montar_cabeca()
    cabeca = osso("cabeca", [0, 25.0, -4.5], [0, 0, 0], cab)
    mp = mat_cor(lambda p, f: tom(CREME, ruido(*p) * .04) if p[2] < -4.0 else tom(MARROM, ruido(*p) * .04), borda=.04, curva=.3)
    pescoco = osso("pescoco", [0, 22.0, -3.5], [0, 0, 0], [
        peca("pescoco", [-3.8, 20.5, -8.4], [3.8, 25.5, -1.0], mp, faixa=(18, 26)),
        cabeca])

    corpo = []
    mt = mat_cor(cor_corpo, borda=.03, curva=.5)
    corpo += arredondado2("tronco", [-6.4, 9.6, -7.2], [6.4, 24.0, 7.0], mt, r=2.4, faixa=(6, 25))
    corpo += arredondado("barriga", [-5.0, 5.8, -6.0], [5.0, 13.0, 5.4], mt, r=1.5, faixa=(5, 25))
    corpo += arredondado2("dorso", [-6.8, 11.0, -2.0], [6.8, 26.0, 9.5], mt, r=2.6, faixa=(6, 27))
    corpo += arredondado("peito", [-4.2, 10.5, -8.2], [4.2, 22.5, -5.0], mt, r=1.0, faixa=(6, 25))
    # 'Flor Peitoral': 4 camadas de penas creme com pontas recortadas, a de cima por cima da de baixo
    for k, (yb, yt) in enumerate(((19.2, 23.4), (16.4, 20.6), (13.6, 17.8), (10.8, 15.0))):
        w = max(meia_peito(yb + (yt - yb) * t / 10) for t in range(11)) + 0.5
        z0 = -9.3 + 0.25 * k
        corpo.append(peca(f"peito_camada{k}", [-w, yb, z0], [w, yt, z0 + 0.6], mat_camada(yb, yt), res=5))

    # ---------- espinhos: leque em volta do eixo de trás ----------
    rnd = random.Random(11)
    C = (0.0, 19.5, 2.0)
    ANEIS = [(0, [0], 17.0), (24, [30 + 60 * k for k in range(6)], 16.5), (36, [51 * k + 10 for k in range(7)], 16.0), (48, [40 * k for k in range(9)], 15.5),
             (72, [36 * k + 18 for k in range(10)], 14.0), (96, [-124, -56, 0, 56, 124], 11.5)]
    cauda, esp_corpo = [], []
    n = 0
    for teta, phis, L in ANEIS:
        for phi in phis:
            phi = ((phi + 180) % 360) - 180
            d = dir_esf(teta, phi)
            if d[1] < -0.62: continue
            if teta > 90 and 5 < abs(phi) < 40: continue
            d = norm([d[0] * 0.62, d[1], d[2] + 0.22])          # leque mais para trás (de frente não abre tanto)
            Lk = L * rnd.uniform(0.92, 1.08) * (0.85 if d[1] < -0.45 else 1.0)
            Wk = 4.0 if teta < 90 else 3.5
            rb = 4.6
            raiz = (C[0] + d[0] * rb, C[1] + d[1] * rb, C[2] + d[2] * rb)
            q = espinho(f"espinho{n}", raiz, d, Lk, Wk, torce=45 if n % 2 else 0)
            (cauda if teta < 25 else esp_corpo).append(q)
            n += 1
    corpo.append(osso("espinhos", list(C), [0, 0, 0], esp_corpo))
    corpo.append(osso("cauda", [0, 18.5, 8.0], [0, 0, 0], cauda))

    # ---------- asas: plumagem de folhas nos ombros, descendo pelos lados ----------
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = []
        # (y raiz, z raiz, ângulo para trás (0 = para baixo, 90 = para trás), abertura p/ fora, L, W)
        MANTO = [  # fileira de baixo: folhas compridas, rentes ao corpo, varrendo para trás (as 'rêmiges')
                 (22.4, -3.0, 34, 16, 9.0, 4.0), (22.6, -0.6, 48, 16, 9.6, 4.0), (22.6, 1.8, 62, 18, 9.4, 4.0),
                 (22.2, 4.0, 74, 20, 8.4, 3.8),
                 # fileira de cima: folhas mais curtas e abertas por cima (as 'coberteiras')
                 (24.4, -4.6, 22, 28, 7.4, 3.8), (24.6, -2.0, 40, 28, 7.8, 4.0), (24.6, 0.6, 56, 28, 7.4, 3.8),
                 # da frente: desce do lado do peito
                 (21.0, -6.0, -6, 30, 10.0, 3.6)]
        for k, (y0, z0, tras, abre, L, W) in enumerate(MANTO):
            t, a = math.radians(tras), math.radians(abre)
            d = [lado * math.sin(a), -math.cos(t) * math.cos(a), math.sin(t) * math.cos(a)]
            asa.append(folha(f"asa{k}_{s}", (6.0 * lado, y0, z0), d, L, W * 1.3, fora=[lado, 0.3, -0.1]))
        corpo.append(osso("asa_" + s, [6.0 * lado, 23.0, -1.0], [0, 0, 0], asa))
    # folhas de colar em volta do peito (emolduram a 'Flor Peitoral')
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        for k, (x0, y0, ang, L) in enumerate(((3.6, 23.0, 16, 10.0), (4.4, 20.0, 26, 9.0))):
            a = math.radians(ang)
            d = [lado * math.sin(a), -math.cos(a), -0.25]
            corpo.append(folha(f"colar{k}_{s}", (x0 * lado, y0, -7.4), d, L, 4.4, fora=[lado * 0.5, 0.2, -1]))

    # penas marrons nos flancos e na barriga (quebram a caixa do tronco embaixo da plumagem de folhas)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        for k, (phi, y0, L, W) in enumerate(((-46, 13.6, 7.0, 4.4), (-8, 14.2, 7.6, 4.6), (30, 14.2, 7.6, 4.6), (66, 13.8, 7.0, 4.4))):
            x, z = g.anel(6.0, 6.6, 0.4, phi, lado)
            fora = [lado * math.cos(math.radians(phi)), 0.1, math.sin(math.radians(phi))]
            d = [fora[0] * 0.35, -1.0, fora[2] * 0.35 + 0.15]
            corpo.append(folha(f"flanco{k}_{s}", (x, y0, z), d, L, W, fora=fora, dobra=24,
                               cores=(MARROM_ESC, MARROM, CARAMELO), nervura=tom(CARAMELO, 0.1), contorno=CHOCOLATE))
    corpo.append(pescoco)
    tronco = osso("corpo", [0, 11.0, 1.0], [0, 0, 0], corpo)

    # ---------- pernas curtas e grossas, pés de 3 dedos com garras escuras ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 3.4 * lado; zc = -0.5
        pp = []
        pp += arredondado("coxa_" + s, [xc - 2.9, 5.2, zc - 3.0], [xc + 2.9, 10.5, zc + 2.8], mat_cor(cor_coxa, borda=.04, curva=.4), r=0.8, faixa=(5, 12))
        pp += octogono("canela_" + s, [xc - 2.0, 1.4, zc - 1.9], [xc + 2.0, 6.0, zc + 1.9], mat_cor(cor_canela, borda=.08, curva=.4), r=0.6, faixa=(1.5, 7))
        mpe = mat_cor(lambda p, f: CANELA_CLARA if f == "up" else CANELA, borda=.15, curva=.5)
        mg = g.mat_facetado(GARRA_CLARA, GARRA, mix(GARRA, (40, 36, 40), .3), (34, 30, 34), quina=-0.3)
        pp.append(peca("pe_" + s, [xc - 2.2, 0.0, zc - 2.2], [xc + 2.2, 1.8, zc + 1.6], mpe, faixa=(0, 2.2)))
        for nome, giro, dx in (("meio", 0, 0), ("fora", -14 * lado, 1.6 * lado), ("dentro", 14 * lado, -1.6 * lado)):
            x0, z0 = xc + dx, zc - 2.0
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - .72, 0, z0 - 1.6], [x0 + .72, 1.5, z0 + 0.2], mpe, faixa=(0, 2.2)),
                peca(f"garra_{nome}_{s}", [x0 - .8, 0.0, z0 - 3.4], [x0 + .8, 1.6, z0 - 1.5], mg, faixa=(0, 2.0))]))
        pp.append(peca("dedo_tras_" + s, [xc - .7, 0, zc + 1.4], [xc + .7, 1.3, zc + 2.8], mpe, faixa=(0, 2.0)))
        pp.append(peca("garra_tras_" + s, [xc - .8, 0, zc + 2.7], [xc + .8, 1.4, zc + 3.9], mg, faixa=(0, 2.0)))
        return osso("perna_" + s, [xc, 10.0, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
