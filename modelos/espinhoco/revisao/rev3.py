"""Espinhocó (#011, Planta): galo-porco-espinho da floresta, cúpula de espinhos nas costas e plumagem de folhas."""
import math, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, mat_cor, arredondado, arredondado2, octogono, pintar_olho

ID = "espinhoco"; NOME = "Espinhocó"; NUMERO = 11
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 26.8, -7.4), 6.9)
ONDAS = []
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (Paleta de Cores da ficha) ----------------
CREME = (246, 222, 174); CREME_ESC = (220, 182, 128)
BEGE = (240, 192, 124); CARAMELO = (206, 138, 72)
MARROM = (148, 92, 54); MARROM_ESC = (104, 64, 42); CHOCOLATE = (66, 42, 34)
VERDE_ESC = (100, 134, 30); VERDE = (148, 180, 44); VERDE_CLARO = (190, 212, 74); NERVURA = (214, 228, 126)
CONTORNO_FOLHA = (54, 86, 22)
AMARELO_BICO = (250, 200, 40); AMARELO_ESC = (232, 158, 26); LARANJA_BICO = (214, 124, 22)
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
        if v < 0.06 or v > 1 or u < -0.05: return None
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
OLHO_Y = 27.2
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
            cor = pintar_olho(u - 0.25, y - OLHO_Y, 1.6, 1.3, iris=((104, 150, 16), (196, 232, 70)), c_iris=(-0.2, -0.08),
                              r_iris=(0.66, 0.8), r_pup=(0.27, 0.36), bravo=0.32, alto=0.42, contorno=(60, 40, 30))
            if cor is not None: return cor
            # pele clara em volta do olho
            if ((u - 0.25) / 1.95) ** 2 + ((y - OLHO_Y) / 1.6) ** 2 <= 1 and y < 28.6: return tom(CREME, 0.06)
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face == "down": return LARANJA_BICO
    if face in ("east", "west") and abs(z - ZF + 0.7) < 0.3 and abs(y - 27.2) < 0.26: return (120, 66, 18)   # narina
    if y < 25.3 and z > ZF - 3.0: return LARANJA_BICO                                                     # beirada de baixo
    return mix(AMARELO_BICO, AMARELO_ESC, clamp((26.8 - y) / 2.6))

def mat_cunha(base, y0, w, queda):
    """Recorta o fundo do bloco em V (de frente vira cunha: larga em cima, ponta embaixo no meio)."""
    def f(c):
        x, y, z = c["p"]
        if y < y0 + queda * abs(x) / w - 1e-3: return None
        return base(c)
    return f

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
    cab.append(peca("cranio_a", [-HW, CAB_Y0 + 0.7, ZS], [HW, CAB_Y1 - 0.9, -1.8], mc, faixa=fx, res=4))
    cab.append(peca("cranio_b", [-HW + 0.7, CAB_Y0, ZS - 0.4], [HW - 0.7, CAB_Y1, -1.0], mc, faixa=fx, res=4))
    cab.append(peca("cranio_nuca", [-HW + 1.5, CAB_Y0 + 0.6, -1.2], [HW - 1.5, CAB_Y1 - 0.8, -0.2], mc, faixa=fx, res=4))
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
    # bico grande em gancho, em camadas que afinam e descem para a frente: de frente é uma cunha que termina
    # em ponta embaixo; de perfil o alto do bico curva para baixo até o gancho, por cima do bico de baixo
    mb = mat_cor(cor_bico, borda=.0, curva=.3)
    fb = (23.4, 28.2)
    for k, (w, y0, y1, z0, z1) in enumerate(((2.0, 25.3, 28.0, ZF - 1.6, ZF + 0.4), (1.5, 24.8, 27.6, ZF - 2.9, ZF - 1.0),
                                             (0.95, 24.0, 26.8, ZF - 3.9, ZF - 2.4), (0.5, 23.3, 25.4, ZF - 4.3, ZF - 3.3))):
        cab.append(peca(f"bico{k}", [-w, y0, z0], [w, y1, z1], mat_cunha(mb, y0, w, (1.4, 1.4, 1.0, 0.5)[k]), faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-0.75, 24.5, ZF - 2.2], [0.75, 26.6, ZF + 0.3],
                    mat_cor(lambda p, f: LARANJA_BICO if f == "down" else AMARELO_ESC, borda=.12), res=4))
    # barbela: dois lóbulos vermelhos grossos, quase encostados, pendurados logo abaixo do bico
    mbb = mat_cor(cor_barbela, borda=.06, curva=.4)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.12 * lado, 2.0 * lado))
        cab.append(osso("barbela_" + s, [0.12 * lado, 24.4, ZF - 0.8], [0, 0, 3 * lado], [
            peca("barbela_" + s, [x0, 20.9, ZF - 1.9], [x1, 24.4, ZF + 0.2], mbb, faixa=(19.6, 24.4), res=4),
            peca("barbela_ponta_" + s, [x0 + 0.3 * lado, 19.8, ZF - 1.6], [x1 - 0.3 * lado, 21.0, ZF - 0.1], mbb, faixa=(19.6, 24.4), res=4)]))
    # crista de folhas: leque alto saindo do alto da cabeça
    crista = []
    FRENTE_C = [(0, 0, 10.5, 6.2), (-26, 8, 9.4, 6.0), (26, 8, 9.4, 6.0), (-52, 16, 7.8, 5.4), (52, 16, 7.8, 5.4)]
    for k, (ang, tras, L, W) in enumerate(FRENTE_C):
        d = [math.sin(math.radians(ang)), math.cos(math.radians(ang)), math.tan(math.radians(tras + 14))]
        crista.append(folha(f"crista{k}", (1.8 * math.sin(math.radians(ang)), 30.0, -8.4), d, L, W, fora=[0, 0.2, -1], dobra=32))
    # fileira de trás: varre para trás e fica de lado (lê larga de perfil, como o tufo da ficha)
    TRAS_C = [(-1, 12, 40, 10.0, 6.0), (1, 12, 40, 10.0, 6.0), (-1, 30, 62, 9.0, 5.8), (1, 30, 62, 9.0, 5.8), (0, 0, 78, 9.0, 5.6)]
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
        peca("pescoco", [-3.2, 19.6, -8.6], [3.2, 24.0, -1.0], mp, faixa=(18, 26)),
        cabeca])

    corpo = []
    mt = mat_cor(cor_corpo, borda=.03, curva=.5)
    corpo += arredondado2("tronco", [-7.2, 7.4, -7.4], [7.2, 23.4, 6.6], mt, r=3.0, faixa=(6, 25))
    corpo += arredondado("barriga", [-5.8, 5.6, -6.2], [5.8, 11.0, 5.4], mt, r=1.8, faixa=(5, 25))
    corpo += arredondado2("dorso", [-7.0, 9.0, -2.0], [7.0, 26.6, 9.8], mt, r=3.2, faixa=(6, 27))
    corpo += arredondado("peito", [-4.2, 10.5, -8.2], [4.2, 22.5, -5.0], mt, r=1.0, faixa=(6, 25))
    # 'Flor Peitoral': 4 camadas de penas creme com pontas recortadas, a de cima por cima da de baixo
    for k, (yb, yt) in enumerate(((19.2, 23.4), (16.4, 20.6), (13.6, 17.8), (10.8, 15.0))):
        w = max(meia_peito(yb + (yt - yb) * t / 10) for t in range(11)) + 0.5
        z0 = -9.3 + 0.25 * k
        corpo.append(peca(f"peito_camada{k}", [-w, yb, z0], [w, yt, z0 + 0.6], mat_camada(yb, yt), res=5))

    # ---------- espinhos: cúpula densa da nuca até o rabo e descendo pelos flancos até a altura da coxa ----------
    # As raízes ficam numa elipsoide em volta das costas (enterradas na massa traseira); cada espinho sai na normal
    # da superfície puxada para trás e para cima, então de lado a cúpula irradia e de trás é uma bola que cobre o corpo.
    rnd = random.Random(11)
    CB, RX, RY, RZ = (0.0, 17.6, 2.2), 6.8, 9.0, 7.8
    FILAS = [(-32, 6, 96, 11.5), (-8, 8, 100, 14.0), (16, 8, 100, 15.5), (40, 7, 94, 15.0), (62, 6, 84, 13.5), (82, 3, 60, 12.0)]
    cauda, esp_corpo = [], []
    n = 0
    for fila, (elev, qtd, abre, L) in enumerate(FILAS):
        for k in range(qtd):
            az = -abre + 2 * abre * (k + 0.5 * (fila % 2) * (qtd > 1)) / max(qtd - 1 + 0.5 * (fila % 2), 1)
            az = clamp(az, -abre, abre)
            v, u = math.radians(elev), math.radians(az)
            sx, sy, sz = math.cos(v) * math.sin(u), math.sin(v), math.cos(v) * math.cos(u)
            nrm = norm([sx / RX, sy / RY, sz / RZ])
            d = norm([nrm[0], nrm[1] + 0.3, nrm[2] + 0.85])
            prof = 0.66                                          # fração do raio onde nasce (base enterrada)
            raiz = (CB[0] + RX * sx * prof, CB[1] + RY * sy * prof, CB[2] + RZ * sz * prof)
            Lk = L * rnd.uniform(0.94, 1.06) * (1 - 0.22 * abs(math.sin(u)))
            Wk = 4.4 if elev < 70 else 4.0
            q = espinho(f"espinho{n}", raiz, d, Lk, Wk, torce=45)
            (cauda if abs(az) < 40 and elev < 30 else esp_corpo).append(q)
            n += 1
    corpo.append(osso("espinhos", list(CB), [0, 0, 0], esp_corpo))
    corpo.append(osso("cauda", [0, 15.0, 8.0], [0, 0, 0], cauda))

    # ---------- asas: plumagem de folhas nos ombros, descendo pelos lados ----------
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = []
        # (y raiz, z raiz, ângulo para trás (0 = para baixo, 90 = para trás), abertura p/ fora, L, W)
        MANTO = [  # (x raiz, y raiz, z raiz, para trás (0 = para baixo, 90 = para trás), abertura p/ fora, L, W)
                 # fileira de baixo: folhas compridas, rentes ao corpo (as 'rêmiges'), até o meio do corpo
                 (6.4, 21.4, -3.0, 34, 16, 9.0, 4.2), (6.4, 21.6, -0.6, 48, 16, 9.6, 4.2), (6.4, 21.6, 1.8, 62, 18, 9.4, 4.2),
                 (6.2, 21.2, 4.0, 74, 20, 8.4, 4.0),
                 # fileira do meio: mais curtas e abertas por cima (as 'coberteiras')
                 (6.0, 23.8, -4.6, 22, 28, 7.6, 4.0), (6.0, 24.0, -2.0, 40, 28, 8.0, 4.2), (6.0, 24.0, 0.6, 56, 28, 7.6, 4.0),
                 # fileira de cima: sai do pescoço e cobre o ombro
                 (4.4, 26.0, -3.4, 30, 36, 6.6, 3.8), (4.4, 26.2, -1.0, 46, 36, 7.0, 4.0), (4.2, 26.0, 1.4, 62, 36, 6.6, 3.8),
                 # da frente: desce do lado do peito
                 (6.0, 21.0, -6.0, -6, 30, 10.0, 3.8)]
        for k, (x0, y0, z0, tras, abre, L, W) in enumerate(MANTO):
            t, a = math.radians(tras), math.radians(abre)
            d = [lado * math.sin(a), -math.cos(t) * math.cos(a), math.sin(t) * math.cos(a)]
            asa.append(folha(f"asa{k}_{s}", (x0 * lado, y0, z0), d, L, W * 1.3, fora=[lado, 0.3, -0.1]))
        corpo.append(osso("asa_" + s, [6.0 * lado, 23.0, -1.0], [0, 0, 0], asa))
    # folhas de colar em volta do peito (emolduram a 'Flor Peitoral')
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        for k, (x0, y0, ang, L) in enumerate(((3.6, 23.0, 16, 10.0),)):
            a = math.radians(ang)
            d = [lado * math.sin(a), -math.cos(a), -0.25]
            corpo.append(folha(f"colar{k}_{s}", (x0 * lado, y0, -7.4), d, L, 4.4, fora=[lado * 0.5, 0.2, -1]))

    corpo.append(pescoco)
    tronco = osso("corpo", [0, 11.0, 1.0], [0, 0, 0], corpo)

    # ---------- pernas curtas e grossas, pés de 3 dedos com garras escuras ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 3.4 * lado; zc = -0.5
        pp = []
        pp += arredondado("coxa_" + s, [xc - 2.5, 5.0, zc - 2.7], [xc + 2.5, 10.0, zc + 2.5], mat_cor(cor_coxa, borda=.04, curva=.4), r=0.8, faixa=(5, 12))
        pp += octogono("canela_" + s, [xc - 2.0, 1.4, zc - 1.9], [xc + 2.0, 6.0, zc + 1.9], mat_cor(cor_canela, borda=.08, curva=.4), r=0.6, faixa=(1.5, 7))
        mpe = mat_cor(lambda p, f: tom(CANELA_CLARA, .1) if f == "up" else CANELA_CLARA, borda=.12, curva=.5)
        mg = g.mat_facetado(GARRA_CLARA, GARRA, mix(GARRA, (40, 36, 40), .3), (34, 30, 34), quina=-0.3)
        pp.append(peca("pe_" + s, [xc - 2.2, 0.0, zc - 2.2], [xc + 2.2, 1.8, zc + 1.6], mpe, faixa=(0, 2.2)))
        for nome, giro, dx in (("meio", 0, 0), ("fora", -16 * lado, 1.7 * lado), ("dentro", 16 * lado, -1.7 * lado)):
            x0, z0 = xc + dx, zc - 2.1
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - .8, 0, z0 - 1.6], [x0 + .8, 1.6, z0 + 0.3], mpe, faixa=(0, 2.2)),
                peca(f"garra_{nome}_{s}", [x0 - .9, 0.0, z0 - 3.4], [x0 + .9, 2.0, z0 - 1.5], mg, faixa=(0, 2.0)),
                peca(f"garra_ponta_{nome}_{s}", [x0 - .6, 0.0, z0 - 4.4], [x0 + .6, 1.2, z0 - 3.3], mg, faixa=(0, 2.0))]))
        pp.append(peca("dedo_tras_" + s, [xc - .7, 0, zc + 1.4], [xc + .7, 1.3, zc + 2.8], mpe, faixa=(0, 2.0)))
        pp.append(peca("garra_tras_" + s, [xc - .8, 0, zc + 2.7], [xc + .8, 1.4, zc + 3.9], mg, faixa=(0, 2.0)))
        return osso("perna_" + s, [xc, 10.0, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
