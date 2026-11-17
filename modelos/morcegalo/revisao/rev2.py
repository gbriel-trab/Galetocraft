"""Morcegalo (#010, Sombrio): galo-morcego noturno de plumagem roxa, orelhas de morcego e asas membranosas."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, anel

ID = "morcegalo"; NOME = "Morcegalo"; NUMERO = 10
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 28.3, -7.2), 9.8)
ONDAS = [("rabo0", 5, (2, 3, 0)), ("rabo2", 5, (2, -3, 0)), ("rabo4", 5, (2, 2, 0))]
ANIM_PARADO = {
    "orelha_d": [(0, 0, 0), (0, 0, 4), (0, 0, 0), (-3, 2, 0), (0, 0, 0), (0, 0, 0)],
    "orelha_e": [(0, 0, 0), (0, 0, -4), (0, 0, 0), (0, 0, 0), (-3, -2, 0), (0, 0, 0)],
}
ANIM_ANDANDO = {
    "orelha_d": [(0, 0, 0), (-4, 0, 3), (0, 0, 0), (-4, 0, 3), (0, 0, 0)],
    "orelha_e": [(0, 0, 0), (-4, 0, -3), (0, 0, 0), (-4, 0, -3), (0, 0, 0)],
}

# ---------------- paleta (da ficha) ----------------
ROXO_NOITE = (58, 31, 99)
ROXO_ESC = (80, 44, 136)
ROXO = (108, 62, 176)
ROXO_MED = (140, 85, 184)
LILAS = (191, 139, 232)
LAVANDA = (232, 186, 240)
LAV_CLARO = (246, 222, 252)
MAGENTA = (215, 81, 151)
MAGENTA_ESC = (172, 50, 118)
ROSA = (234, 122, 198)
VIOLETA = (166, 98, 214)
ROSA_CLARO = (248, 170, 220)
CREME = (252, 216, 185)
CREME_CLARO = (255, 236, 214)
CREME_ESC = (224, 168, 150)
AMBAR = (253, 184, 2)
AMBAR_ESC = (232, 96, 10)
GARRA = (70, 46, 84)
GARRA_CLARA = (108, 78, 118)
PRETO = (26, 12, 22)

# ---------------- geometria 2D (placas recortadas) ----------------
def dentro_poli(x, y, poli):
    dentro = False
    n = len(poli)
    for i in range(n):
        x1, y1 = poli[i]; x2, y2 = poli[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            dentro = not dentro
    return dentro

def dist_seg(px, py, a, b):
    ax, ay = a; bx, by = b
    dx, dy = bx - ax, by - ay
    t = clamp(((px - ax) * dx + (py - ay) * dy) / max(dx * dx + dy * dy, 1e-9))
    return math.hypot(px - ax - t * dx, py - ay - t * dy)

def dist_borda(px, py, poli):
    return min(dist_seg(px, py, poli[i], poli[(i + 1) % len(poli)]) for i in range(len(poli)))

def curva(p0, n, p2, k=6):
    """Pontos de uma curva (Bézier quadrática) de p0 a p2 passando perto de n (sem as pontas)."""
    q = (2 * n[0] - (p0[0] + p2[0]) / 2, 2 * n[1] - (p0[1] + p2[1]) / 2)
    pts = []
    for i in range(1, k):
        t = i / k
        pts.append(((1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * q[0] + t * t * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * q[1] + t * t * p2[1]))
    return pts

def barra(nome, a, b, esp, z0, z1, mat, res=None, estica=0.0):
    """Barra (osso da asa, moldura da orelha) entre dois pontos a, b do plano x-y: caixa deitada em x girada em z."""
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    L = math.hypot(b[0] - a[0], b[1] - a[1]) + estica
    ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    return peca(nome, [mx - L / 2, my - esp / 2, z0], [mx + L / 2, my + esp / 2, z1], mat, rot=(0, 0, ang),
                pivo=(mx, my, (z0 + z1) / 2), res=res)

def mat_osso_roxo(claro=ROXO_MED, meio=ROXO, escuro=ROXO_NOITE):
    """Moldura óssea roxa (asa, orelha): clara em cima, roxa na frente/trás, escura embaixo, quinas escurecidas."""
    def f(c):
        face = c["face"]
        base = mix(claro, LILAS, .25) if face == "up" else escuro if face == "down" else meio if face in ("north", "south") \
            else mix(meio, escuro, .35)
        if g.na_borda(c): base = tom(base, -.3)
        return base
    return f

# ---------------- cabeça ----------------
CAB_Y0, CAB_Y1 = 21.6, 30.2          # faixa de altura da cabeça
FR_X, FR_Z = 2.1, -9.0               # quina da frente (onde a faceta começa)
LD_X, LD_Z = 5.4, -5.7               # quina do lado (onde a faceta termina)
FAC_T = 1.6
FAC_L = math.hypot(LD_X - FR_X, LD_Z - FR_Z)
_n = (0.7071, -0.7071)               # normal da faceta (lado +x): para fora e para a frente
FAC_C = ((FR_X + LD_X) / 2 - _n[0] * FAC_T / 2, (FR_Z + LD_Z) / 2 - _n[1] * FAC_T / 2)
OLHO_Y = 25.9
OLHO_RU, OLHO_RV = 1.7, 1.2          # raios do olho (na faceta)
K_CAB = 1.12                         # escala da cabeça inteira (em volta da base do pescoço)
SOBE_CAB = 1.0                       # a cabeça sobe um pouco: aparece um pescoço curto com plumas
BICO = (245, 217, 192); BICO_CLARO = (253, 236, 218); BICO_ESC = (222, 178, 156); BICO_SOMBRA = (186, 134, 124)
CRISTA = (208, 79, 143); CRISTA_CLARA = (242, 140, 196)
IRIS = (242, 178, 28)

def palpebra(u):
    """Altura (relativa ao centro do olho) da pálpebra reta: desce em direção ao bico (u negativo)."""
    return OLHO_RV * (0.22 + 0.42 * u / OLHO_RU)

def cor_cabeca(p, face):
    x, y, z = p
    base = mix(ROXO_ESC, ROXO, clamp((y - 22.0) / 7.0))
    if face == "up": base = mix(ROXO, ROXO_MED, .4)
    if z > -1.0 and y > 27.6: base = mix(base, ROXO_MED, .45)          # 'capacete' mais claro na nuca
    if y < 23.4: base = mix(base, ROXO_NOITE, .35)                       # queixo mais escuro
    # bico de viúva: V roxo-escuro descendo pela testa até entre os olhos
    if face == "north" and z < -8.5 and y > 25.4 and abs(x) < 0.25 + (y - 26.2) * 0.26 and y > 26.2:
        base = mix(ROXO_NOITE, ROXO_ESC, .25)
    return base

def olho_morcegalo(u, v):
    """Olho âmbar-amarelo semicerrado (neutro, atento): pálpebra reta roxo-escura caindo para o bico,
    pupila escura, brilho pequeno e contorno escuro."""
    ru, rv = OLHO_RU, OLHO_RV
    e = (u / ru) ** 2 + (v / rv) ** 2
    if e > 1: return None
    lp = palpebra(u)
    if v > lp + 0.16: return ROXO_NOITE                                   # pálpebra (some embaixo da sobrancelha)
    if v > lp - 0.04: return (40, 18, 46)                                 # beirada da pálpebra (sombra)
    if ((u + 0.15) / 0.22) ** 2 + ((v - lp + 0.32) / 0.2) ** 2 <= 1: return (255, 250, 230)   # brilho
    pu, pv = u + 0.35, v + 0.05
    if (pu / 0.42) ** 2 + (pv / 0.6) ** 2 <= 1: return PRETO             # pupila
    if e > 0.78: return (96, 44, 30)                                      # contorno
    return mix((252, 214, 70), mix(IRIS, AMBAR_ESC, .45), clamp(0.15 + 0.6 * e - 0.4 * v / rv))

def mat_faceta(lado):
    base = g.mat_cor(cor_cabeca, borda=.03, curva=.3)
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            cor = olho_morcegalo(z - FAC_C[1], y - OLHO_Y)
            if cor: return cor
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face in ("east", "west") and abs(z + 9.75) < 0.28 and abs(y - 24.75) < 0.22: return (110, 64, 70)   # narina
    if face == "down": return BICO_ESC
    if face == "up": return BICO_CLARO
    if face in ("east", "west"): return mix(BICO, BICO_ESC, clamp((24.6 - y) / 3.0))
    return mix(BICO_CLARO, BICO, clamp((25.2 - y) / 2.5))

def cabeca_morcegalo():
    cab = []
    mc = g.mat_cor(cor_cabeca, borda=.03, curva=.3)
    faixa = (CAB_Y0, CAB_Y1)
    cab += g.arredondado2("cranio", [-LD_X, CAB_Y0, -6.0], [LD_X, CAB_Y1, 1.2], mc, r=1.9, faixa=faixa, res=4)
    cab.append(peca("cranio_frente", [-FR_X, 22.0, FR_Z], [FR_X, 29.4, -5.6], mc, faixa=faixa, res=4))
    sob = g.mat_cor(lambda p, f: ROXO_NOITE if f != "up" else ROXO_ESC, borda=.15)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 22.2, cz - FAC_L / 2], [cx + FAC_T / 2, 28.8, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, OLHO_Y, cz), faixa=faixa, res=8,
                        brilho=lambda c, cor: cor[0] > 200 and 60 < cor[1] < 235 and cor[2] < 100))   # olho âmbar brilha no escuro
        # sobrancelha da faceta: colada na pálpebra, descendo para o bico
        ox = cx + (FAC_T / 2) * lado
        x0, x1 = sorted((ox - 0.15 * lado, ox + 0.5 * lado))
        yb = OLHO_Y + palpebra(0) - 0.05
        cab.append(osso("sobrancelha_" + s, [cx, yb, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s, [x0, yb, cz - FAC_L / 2 - 0.2], [x1, yb + 0.85, cz + FAC_L / 2], sob,
                 rot=(-14, 0, 0), pivo=(cx, yb, cz))]))
        # sobrancelha da frente: o V bravo por cima do bico
        x0, x1 = sorted((0.1 * lado, 2.4 * lado))
        cab.append(peca("sobrancelha_fr_" + s, [x0, 26.0, FR_Z - 0.5], [x1, 26.9, FR_Z + 0.2], sob,
                        rot=(0, 0, 20 * lado), pivo=(2.4 * lado, 26.45, FR_Z)))
    # bico de rapina creme-pêssego em degraus: cera larga, mandíbula de cima projetada, gancho para baixo
    mb = g.mat_cor(cor_bico, borda=.05, curva=.15)
    fb = (20.5, 26.0)
    cab.append(peca("bico_cera", [-1.9, 22.5, -10.2], [1.9, 25.5, -8.7], mb, faixa=fb, res=4))
    cab.append(peca("bico_meio", [-1.5, 22.9, -12.6], [1.5, 25.25, -10.0], mb, rot=(-10, 0, 0), pivo=(0, 25.25, -10.0), faixa=fb, res=4))
    cab.append(peca("bico_gancho", [-0.9, 22.0, -13.4], [0.9, 24.6, -12.0], mb, rot=(-16, 0, 0), pivo=(0, 24.6, -12.0), faixa=fb, res=4))
    cab.append(peca("bico_ponta", [-0.45, 21.2, -13.05], [0.45, 22.1, -12.15], mb, rot=(-16, 0, 0), pivo=(0, 24.6, -12.0), faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-1.25, 21.5, -10.9], [1.25, 22.55, -8.7],
                    g.mat_cor(lambda p, f: BICO_SOMBRA if f == "down" else BICO_ESC, borda=.1, curva=.2), res=4))
    # barbela: dois lóbulos rosa-magenta pendurados embaixo do bico
    mbar = g.mat_cor(lambda p, f: mix(MAGENTA, (196, 52, 112), clamp((21.5 - p[1]) / 3.5)), borda=.1, curva=.5)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.05 * lado, 1.8 * lado))
        cab += g.arredondado2("barbela_" + s, [x0, 18.6 + (0.5 if lado > 0 else 0), -10.5], [x1, 22.2, -8.5], mbar, r=0.85, res=4)
    # crista serrilhada magenta: 5 pontas em degraus inclinadas para trás, a mais alta na frente
    crista = []
    mcr = g.mat_cor(lambda p, f: mix(CRISTA, CRISTA_CLARA, clamp((p[1] - 30.0) / 5.0)), borda=.12, curva=.35)
    crista.append(peca("crista_base", [-1.2, 29.7, -7.4], [1.2, 30.6, 1.4], mcr, faixa=(29.6, 35.6), res=4))
    for k, (z0, h) in enumerate([(-7.6, 5.4), (-5.6, 4.6), (-3.6, 3.8), (-1.6, 3.0), (0.4, 2.2)]):
        y = 30.5
        for i, (w, d, fr) in enumerate([(1.15, 2.4, 0.3), (0.95, 1.8, 0.27), (0.72, 1.2, 0.23), (0.45, 0.6, 0.2)]):
            hh = h * fr                                          # (meia largura, profundidade, fração da altura)
            zz = z0 + 0.42 * i + (2.4 - d) * 0.5                 # cada degrau afina e recua: a ponta inclina para trás
            crista.append(peca(f"crista{k}_{i}", [-w, y - 0.05, zz], [w, y + hh, zz + d], mcr, faixa=(29.6, 35.6), res=4))
            y += hh - 0.05
    cab.append(osso("crista", [0, 30.0, -3.0], [0, 0, 0], crista))
    # orelhas de morcego
    for lado in (-1, 1):
        cab.append(orelha(lado))
    return cab

# ---------------- orelhas ----------------
OR_A = (3.6, 29.4, -2.4)             # raiz da orelha (lado +x)
OR_POLI = [(-0.4, -1.4), (6.0, -2.4), (9.2, -2.7), (10.2, -1.7), (10.2, 2.6), (9.4, 3.3), (10.4, 8.8), (9.7, 9.5), (0.0, 1.8)]
OR_DENTRO = [(1.3, -0.6), (6.2, -1.5), (8.8, -1.7), (9.0, 2.4), (8.2, 3.5), (9.0, 7.3), (1.7, 1.8)]

def mat_orelha(lado):
    ax, ay, az = OR_A
    def f(c):
        x, y, z = c["p"]
        u, v = (x - ax * lado) * lado, y - ay
        if not dentro_poli(u, v, OR_POLI): return None
        if c["face"] == "south" or not dentro_poli(u, v, OR_DENTRO):
            cor = mix(ROXO_ESC, ROXO, clamp(v / 12))
            return tom(cor, -.35) if dist_borda(u, v, OR_POLI) < 0.18 else cor
        d = dist_borda(u, v, OR_DENTRO)
        cor = mix(ROSA_CLARO, ROSA, clamp(1 - d / 1.6))
        cor = mix(cor, MAGENTA, clamp((2.5 - v) / 4) * .5)
        if d < 0.25: cor = tom(MAGENTA_ESC, -.2)
        return cor
    return f

def orelha(lado):
    s = "d" if lado < 0 else "e"
    ax, ay, az = OR_A
    ax *= lado
    P = lambda u, v: (ax + u * lado, ay + v)
    pts = [P(u, v) for u, v in OR_POLI]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    filhos = [peca("orelha_pele_" + s, [min(xs), min(ys), az - 0.1], [max(xs), max(ys), az + 0.25], mat_orelha(lado), res=4)]
    mo = mat_osso_roxo(ROXO_MED, ROXO, ROXO_NOITE)
    filhos.append(barra("orelha_fora_" + s, P(9.7, -2.1), P(10.0, 9.1), 1.0, az - 0.5, az + 0.45, mo, estica=0.6))
    filhos.append(barra("orelha_dentro_" + s, P(10.0, 9.1), P(0.0, 0.7), 1.0, az - 0.5, az + 0.45, mo, estica=0.4))
    return osso("orelha_" + s, [ax, ay, az], [8, -31 * lado, 0], filhos)

# ---------------- asas membranosas ----------------
WZ = 0.8
ASA = {"S": (7.6, 20.8), "W": (14.6, 26.2), "C": (22.6, 23.2), "T1": (24.8, 10.4), "N1": (21.4, 14.4),
       "T2": (17.4, 9.6), "N2": (14.0, 13.4), "T3": (10.6, 10.8), "B": (8.8, 13.8)}
A = ASA
ASA_POLI = [A["S"], A["W"], A["C"], A["T1"]] + curva(A["T1"], A["N1"], A["T2"]) + [A["T2"]] + \
           curva(A["T2"], A["N2"], A["T3"]) + [A["T3"], A["B"]]
DEDOS = [(A["W"], A["C"], 1.2), (A["C"], A["T1"], 1.0), (A["W"], A["T2"], 0.7), (A["W"], A["T3"], 0.6), (A["S"], A["W"], 1.4)]

def mat_membrana(lado):
    def f(c):
        x, y, z = c["p"]
        u = x * lado
        if not dentro_poli(u, y, ASA_POLI): return None
        db = dist_borda(u, y, ASA_POLI)
        # ponta creme nas garras de baixo
        for t in ("T1", "T2"):
            tx, ty = A[t]
            if math.hypot(u - tx, y - ty) < 1.7 and y < ty + 1.6: return mix(CREME, CREME_ESC, clamp((y - ty) / 1.6))
        dd = min(dist_seg(u, y, a, b) - e / 2 for a, b, e in DEDOS)
        if dd < 0: return mix(ROXO, ROXO_MED, .3) if c["face"] == "north" else ROXO
        cor = mix((250, 182, 226), ROSA, clamp((24 - y) / 7))
        cor = mix(cor, MAGENTA, clamp((16 - y) / 6))
        cor = tom(cor, .14 * clamp((dd - 0.8) / 2.5))                            # miolo de cada painel mais claro
        if dd < 0.6: cor = mix(cor, MAGENTA_ESC, (0.6 - dd) / 0.6 * .55)          # sombra junto dos ossos
        if db < 0.18: cor = tom(MAGENTA_ESC, -.25)
        if c["face"] == "south": cor = tom(cor, -.12)
        return cor
    return f

def asa(lado):
    s = "d" if lado < 0 else "e"
    P = lambda k: (A[k][0] * lado, A[k][1])
    us = [p[0] for p in ASA_POLI]; ys = [p[1] for p in ASA_POLI]
    x0, x1 = sorted((min(us) * lado, max(us) * lado))
    filhos = [peca("membrana_" + s, [x0, min(ys), WZ - 0.15], [x1, max(ys), WZ + 0.15], mat_membrana(lado), res=4)]
    mo = mat_osso_roxo()
    filhos.append(barra("braco_" + s, P("S"), P("W"), 1.7, WZ - 0.8, WZ + 0.8, mo, estica=0.8))
    filhos.append(barra("antebraco_" + s, P("W"), P("C"), 1.4, WZ - 0.65, WZ + 0.65, mo, estica=1.0))
    filhos.append(barra("dedo_fora_" + s, P("C"), P("T1"), 1.1, WZ - 0.55, WZ + 0.55, mo, estica=0.4))
    filhos.append(barra("dedo_meio_" + s, P("W"), P("T2"), 0.75, WZ - 0.4, WZ + 0.4, mo))
    filhos.append(barra("dedo_dentro_" + s, P("W"), P("T3"), 0.6, WZ - 0.35, WZ + 0.35, mo))
    wx, wy = P("W")
    filhos.append(peca("pulso_" + s, [wx - 1.1, wy - 1.1, WZ - 0.9], [wx + 1.1, wy + 1.1, WZ + 0.9], mo))
    # garra creme na ponta de fora
    tx, ty = P("T1")
    mg = g.mat_cor(lambda p, f: mix(CREME_CLARO, CREME_ESC, clamp((ty + 1.0 - p[1]) / 2.2)), borda=.12)
    filhos.append(peca("garra_asa_" + s, [tx - 0.55, ty - 1.4, WZ - 0.5], [tx + 0.55, ty + 1.2, WZ + 0.5], mg,
                       rot=(0, 0, 8 * lado), pivo=(tx, ty, WZ)))
    sx, sy = P("S")
    return osso("asa_" + s, [sx, sy, WZ], [0, -30 * lado, 0], filhos)

# ---------------- corpo ----------------
def mat_rabo(c0, c1, ei, inv):
    """Pena grossa da cauda: degradê ao longo do comprimento, beirada de baixo mais escura nas faces do lado."""
    base = g.mat_pena(c0, c1, ei, inv, borda=.14)
    def f(c):
        cor = base(c)
        if c["face"] in ("east", "west"):
            y0, y1 = c["b"][0][1], c["b"][1][1]
            t = (c["p"][1] - y0) / max(y1 - y0, 1e-6)
            if t < 0.28: cor = tom(cor, -.25)
            elif t > 0.8: cor = tom(cor, .1)
        return cor
    return f

def escama(s_, y, larg=3.2, alt=2.8):
    """Penas sobrepostas em fileiras (telhado): devolve (fileira, coluna, fu, d) do ponto (s_, y), s_ = arco em volta
    do corpo. A beirada de baixo de cada pena é em V; d = altura acima da própria beirada (em fileiras)."""
    def borda(r):
        t = s_ / larg + 0.5 * (r % 2); fu = t - math.floor(t)
        return r * alt - 0.45 * alt * (1 - abs(fu - 0.5) * 2), math.floor(t), fu
    r = math.floor(y / alt)
    b1, c1, fu1 = borda(r + 1)
    if y >= b1: r, b, c, fu = r + 1, b1, c1, fu1
    else: b, c, fu = borda(r)
    return r, c, fu, (y - b) / alt

def cor_plumagem(p, face):
    """Plumagem em fileiras grandes de penas (beirada em V suave), sem pontilhado: frente lavanda (sob o peitoral),
    costas com penas lilás e roxas alternadas, lados roxo escuro -> médio."""
    x, y, z = p
    if z < -4.0 and abs(x) < 6.0 - (21.5 - y) * 0.3 and y > 9.5: return mix(LILAS, LAVANDA, .3)   # sob o peitoral (V)
    a = math.atan2(x, z)                                 # 0 = costas, ±pi = frente
    r, c, fu, d = escama(a * 8.4, y, larg=4.6, alt=3.4)
    if abs(a) < 0.9 and y > 9.0:
        base = mix(LILAS, LAVANDA, .25) if (r + c) % 2 == 0 else mix(ROXO_MED, VIOLETA, .5)
    else:
        base = mix(ROXO_ESC, ROXO_MED, clamp((y - 7) / 14))
    if d * 3.4 < 0.55: return mix(base, ROXO_NOITE, .28)                   # beirada da pena (faixa contínua, sem pontilhado)
    return mix(base, tom(base, -.22), clamp(d - 0.45))                     # sombra no alto da pena

def mat_degrau(cor, yt, h, lat=LILAS):
    """Bloco do peitoral: frente clara em cima e lavanda embaixo, lados lilás, embaixo na sombra."""
    def f(c):
        face, y = c["face"], c["p"][1]
        t = clamp((yt - y) / h)
        if face == "up": base = tom(cor, .25)
        elif face == "down": base = tom(mix(cor, lat, .5), -.35)
        elif face == "north": base = mix(tom(cor, .18), mix(cor, lat, .3), t)
        else: base = mix(mix(cor, lat, .45), tom(lat, -.15), t)
        if g.na_borda(c): base = tom(base, -.18)
        return base
    return f

def degrau(nome, yt, rx, rz, phi, W, cor, lado, h=3.0, prof=1.6, lat=LILAS, pontas=2):
    """Um bloco do peitoral no anel do peito (face larga para fora no ângulo phi) com 2 pontas em losango embaixo."""
    x, z = anel(rx, rz, 0.0, phi, lado)
    m = mat_degrau(cor, yt, h + 1.2, lat)
    zc = z + prof / 2 - 0.4                         # a face da frente fica 0,4 à frente do anel
    filhos = [peca(nome, [x - W / 2, yt - h, zc - prof / 2], [x + W / 2, yt, zc + prof / 2], m, res=4)]
    q = 1.55 if pontas == 2 else W * 0.62
    for i, dx in enumerate((-W / 4, W / 4) if pontas == 2 else (0.0,)):
        filhos.append(peca(f"{nome}_ponta{i}", [x + dx - q / 2, yt - h - q / 2, zc - prof / 2 + 0.06],
                           [x + dx + q / 2, yt - h + q / 2, zc + prof / 2 - 0.06], m, rot=(0, 0, 45), pivo=(x + dx, yt - h, zc), res=4))
    return osso(nome, [x, yt, z], [0, -(phi + 90) * lado, 0], filhos)

def mat_chevron(cor, yb, h):
    """Camada do peitoral: frente clara em cima, lilás embaixo, com dentes de pena em V sombreados na beirada de baixo."""
    lat = LILAS
    def f(c):
        face = c["face"]
        x, y, z = c["p"]
        (x0, y0, _), (x1, y1, _) = c["b"]
        t = clamp((y1 - y) / max(y1 - y0, 1e-6))
        if face == "up": base = tom(cor, .22)
        elif face == "down": base = tom(mix(cor, lat, .5), -.4)
        elif face == "north":
            base = mix(tom(cor, .14), mix(cor, lat, .35), t)
            if t > 0.82: base = tom(mix(cor, lat, .5), -.1)            # beirada de baixo um pouco mais escura
        else: base = mix(mix(cor, lat, .45), tom(lat, -.15), t)
        if g.na_borda(c): base = tom(base, -.16)
        return base
    return f

def chevron(nome, yb, zf, mw, h, cor, lado, prof=1.8, ang=24, giro=15):
    """Meia camada do peitoral: bloco do meio para fora, girado em z (a ponta de fora sobe: V visto de frente)
    dentro de um osso girado em y (abraça o peito). A ponta do V fica em (0, yb, zf)."""
    x1 = mw * lado
    xa, xb = sorted((0.0, x1))
    m = mat_chevron(cor, yb, h)
    filhos = [peca(nome, [xa, yb, zf], [xb, yb + h, zf + prof], m, rot=(0, 0, ang * lado), pivo=(0, yb, zf + prof / 2), res=4)]
    return osso(nome, [0, yb, zf + prof / 2], [0, -giro * lado, 0], filhos)

def so_faces_largas(mat, pc):
    """Envolve o material de uma placa fina: só as duas faces largas são pintadas."""
    dx, dz = pc.ate[0] - pc.de[0], pc.ate[2] - pc.de[2]
    largas = ("east", "west") if dx < dz else ("north", "south")
    return lambda c: mat(c) if c["face"] in largas else None

def cone_grosso(nome, raiz, phi, flare, L, W, cores, lado, varre=0, esp=0.5, curva=0.15):
    """Placa-pena numa saia em volta de um anel (como g.pena_cone_placa), mas com espessura própria."""
    return osso(nome, list(raiz), [0, -phi * lado, 0],
                [g.pena_placa(nome + "_p", raiz, (-varre, 0, flare * lado), L, W, cores, esp=esp, curva=curva)])

def mat_coxa(xc):
    """'Calça' de penas roxas: barra de baixo em pontas de pena mais escuras."""
    def cor(p, face):
        x, y, z = p
        a = math.atan2(z, x - xc)
        barra = 4.6 + 0.5 + 0.7 * abs(math.sin(a * 3.0))
        if y < barra: return mix(ROXO_NOITE, ROXO_ESC, clamp((y - 4.6) / 1.2))
        return mix(ROXO_ESC, ROXO_MED, clamp((y - barra) / 4.0))
    return g.mat_cor(cor, borda=.05, curva=.4)

def forma_babado(u, v):
    meia = 1.0 if v < 0.45 else max(0.0, 1.0 - (v - 0.45) / 0.55)
    return abs(u) <= meia, meia - abs(u), u

def montar():
    # ---------- cabeça ----------
    i_cab = len(g.PECAS)
    cab = cabeca_morcegalo()
    g.transformar(i_cab, cab, (0.0, 21.8, -3.0), K_CAB, sobe=SOBE_CAB)   # cabeça um pouco maior e mais alta
    cabeca = osso("cabeca", [0, 22.0 + SOBE_CAB, -3.0], [0, 0, 0], cab)
    mp = g.mat_cor(cor_plumagem, borda=.04, curva=.3)
    # pescoço curto + plumas (hackles) roxas caindo da nuca por cima dos ombros
    plumas = []
    for k, (phi, y0, L, W, fl) in enumerate([(14, 23.4, 4.6, 4.0, 14), (44, 23.8, 5.0, 4.2, 12), (70, 24.0, 5.4, 4.4, 10),
                                              (90, 24.0, 5.6, 4.6, 10)]):
        for lado in ((1,) if phi == 90 else (-1, 1)):
            x, z = anel(4.3, 4.0, -2.4, phi, lado)
            plumas.append(cone_grosso(f"pluma{k}_{'d' if lado < 0 else 'e'}", (x, y0, z), phi, fl, L, W,
                                      (ROXO_ESC, ROXO, ROXO_MED), lado, varre=6, esp=0.45))
    pescoco = osso("pescoco", [0, 20.5, -2.5], [0, 0, 0], [
        peca("pescoco", [-3.9, 18.6, -7.0], [3.9, 23.6, 1.6], mp, faixa=(8, 24)),
        osso("plumas", [0, 23.5, -1.0], [0, 0, 0], plumas),
        cabeca])

    corpo = []
    mt = g.mat_cor(cor_plumagem, borda=.03, curva=.5)
    corpo += g.arredondado2("tronco", [-7.4, 11.5, -7.0], [7.4, 21.2, 6.0], mt, r=2.6, faixa=(7, 21.2))
    corpo += g.arredondado2("barriga", [-8.8, 7.0, -6.6], [8.8, 16.4, 6.4], mt, r=3.0, faixa=(7, 21.2))
    # peito estufado: volume da frente, em degraus, que empurra o peitoral para fora
    corpo += g.arredondado2("peito", [-5.2, 9.0, -8.9], [5.2, 21.0, -4.0], mt, r=2.6, faixa=(7, 21.2))

    # ---------- peitoral sombrio: 4 camadas grandes em V (chevrons), lavanda clara em cima -> lilás embaixo ----------
    CAMADAS = [  # (y da ponta do V, z da frente, meia largura, altura, cor)
        (18.4, -9.9, 6.6, 4.4, LAV_CLARO),
        (15.2, -9.9, 6.4, 4.4, LAVANDA),
        (12.0, -9.6, 5.6, 4.2, mix(LAVANDA, LILAS, .5)),
        (9.2, -8.9, 4.2, 3.6, mix(LAVANDA, LILAS, .9)),
    ]
    peito = []
    for t, (yb, zf, mw, h, cor) in enumerate(CAMADAS):
        for lado in (-1, 1):
            peito.append(chevron(f"peito{t}_{'d' if lado < 0 else 'e'}", yb, zf, mw, h, cor, lado))
    corpo.append(osso("peitoral", [0, 16, -5], [0, 0, 0], peito))

    # ---------- franja de penas escuras embaixo do corpo ----------
    franja = []
    for k, phi in enumerate([-40, 0, 40, 80]):
        for lado in (-1, 1):
            x, z = anel(8.3, 6.3, 0.0, phi, lado)
            franja.append(g.pena_cone_placa(f"franja{k}_{'d' if lado < 0 else 'e'}", (x, 10.6, z), phi, 8, 4.0, 4.4,
                                            (ROXO_ESC, ROXO, ROXO_MED), lado, curva=0.1, forma=forma_babado))
    corpo.append(osso("franja", [0, 11, 0], [0, 0, 0], franja))

    # ---------- asas ----------
    corpo.append(asa(-1)); corpo.append(asa(1))

    # ---------- cauda: penas em foice nascendo alto no quadril, subindo e curvando para trás e para baixo ----------
    cauda = []
    V1, V2 = (118, 58, 188), (160, 88, 220)
    for k, (rx, cv, esc, xo) in enumerate([(-68, 24, 1.2, 0.0), (-52, 22, 1.08, 0.45), (-36, 20, 0.97, -0.45),
                                            (-20, 18, 0.86, 0.35), (-4, 15, 0.74, 0.0)]):
        escura = k % 2 == 1                                   # listras roxo / lilás vistas por trás
        c0, c1 = (ROXO_ESC, V1) if escura else (ROXO, V2)
        segs = [(4.6 * esc, 1.9, 4.4, c0, c1), (4.4 * esc, 1.7, 4.0, c1, mix(c1, VIOLETA, .5)),
                (3.8 * esc, 1.4, 3.3, mix(c1, VIOLETA, .5), ROSA), (2.4 * esc, 1.0, 2.3, ROSA_CLARO, CREME),
                (1.4 * esc, 0.6, 1.2, CREME, CREME_CLARO)]
        cauda.append(g.pena_curva(f"rabo{k}", (xo * 0.6, 19.0 - 0.7 * k, 5.0 + 0.15 * k), segs, (rx, 0, 0), (cv, 0, 0), "z", mat_rabo))
    corpo.append(osso("cauda", [0, 18.0, 5.4], [0, 0, 0], cauda))

    corpo.append(pescoco)
    tronco = osso("corpo", [0, 11.0, 0], [0, 0, 0], corpo)

    # ---------- pernas: canela creme-pêssego, pé de 3 dedos com garras escuras + 1 atrás ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 5.8 * lado; zc = -0.6
        pp = []
        pp += g.arredondado("coxa_" + s, [xc - 2.7, 4.6, zc - 2.7], [xc + 2.7, 10.6, zc + 2.5], mat_coxa(xc), r=0.9)
        mcan = g.mat_cor(lambda p, f: mix(CREME, CREME_ESC, clamp((6.5 - p[1]) / 8)), borda=.08, curva=.4)
        pp += g.octogono("canela_" + s, [xc - 1.75, 2.0, zc - 1.75], [xc + 1.75, 7.6, zc + 1.75], mcan, r=0.6, faixa=(0, 7.4))
        pp.append(peca("pe_" + s, [xc - 2.3, 0.0, zc - 2.4], [xc + 2.3, 2.6, zc + 1.8], mcan, faixa=(0, 7.4)))
        mdedo = g.mat_cor(lambda p, f: CREME_ESC if f == "down" else CREME, borda=.18, curva=.5)
        mgar = g.mat_cor(lambda p, f: GARRA_CLARA if f == "up" else GARRA, borda=.18, curva=.4)
        for nome, giro, dx in (("meio", 0, 0), ("fora", -18 * lado, 2.2 * lado), ("dentro", 18 * lado, -2.2 * lado)):
            x0, z0 = xc + dx * 0.6, zc - 1.6
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - .9, 0, z0 - 3.2], [x0 + .9, 2.0, z0 + 0.4], mdedo, faixa=(0, 2.2)),
                peca(f"garra_{nome}_{s}", [x0 - .8, 0, z0 - 4.6], [x0 + .8, 1.9, z0 - 3.1], mgar, faixa=(0, 2.0))]))
        pp.append(peca("dedo_tras_" + s, [xc - .6, 0, zc + 1.2], [xc + .6, 1.3, zc + 3.0], mdedo, faixa=(0, 2.0)))
        pp.append(peca("garra_tras_" + s, [xc - .55, 0, zc + 2.9], [xc + .55, 1.2, zc + 3.9], mgar, faixa=(0, 1.8)))
        return osso("perna_" + s, [xc, 9.0, zc], [0, 0, 0], pp)

    # placas finas (membrana, pele da orelha, plumas, franja): as beiradas de 0,3-0,5 não são pintadas,
    # assim nunca aparecem como lascas soltas (o close do rosto corta as faces grandes e deixava só as beiradas)
    for pc in g.PECAS:
        if pc.nome.startswith(("membrana_", "orelha_pele_", "pluma", "franja")):
            pc.mat = so_faces_largas(pc.mat, pc)
    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
