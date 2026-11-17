"""Morcegalo (#010, Sombrio): galo-morcego noturno de plumagem roxa em blocos, orelhas de morcego e asas membranosas."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp

ID = "morcegalo"; NOME = "Morcegalo"; NUMERO = 10
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 26.0, -5.5), 9.5)
ONDAS = [("rabo0", 5, (2, 2, 0)), ("rabo1", 5, (2, -2, 0)), ("rabo2", 5, (2, 2, 0))]
ANIM_PARADO = {
    "orelha_d": [(0, 0, 0), (0, 0, 4), (0, 0, 0), (-3, 2, 0), (0, 0, 0), (0, 0, 0)],
    "orelha_e": [(0, 0, 0), (0, 0, -4), (0, 0, 0), (0, 0, 0), (-3, -2, 0), (0, 0, 0)],
}
ANIM_ANDANDO = {
    "orelha_d": [(0, 0, 0), (-4, 0, 3), (0, 0, 0), (-4, 0, 3), (0, 0, 0)],
    "orelha_e": [(0, 0, 0), (-4, 0, -3), (0, 0, 0), (-4, 0, -3), (0, 0, 0)],
}

# ---------------- paleta (Paleta de Cores da ficha) ----------------
ROXO_NOITE = (58, 30, 101)
ROXO_ESC = (78, 42, 132)
ROXO = (104, 60, 172)
ROXO_MED = (140, 85, 184)
VIOLETA = (166, 84, 218)
LILAS = (192, 139, 232)
LAVANDA = (232, 186, 240)
LAV_CLARO = (246, 220, 250)
MAGENTA = (215, 81, 151)
MAGENTA_ESC = (168, 46, 116)
ROSA = (234, 122, 198)
ROSA_CLARO = (246, 164, 220)
CREME = (252, 216, 185)
CREME_CLARO = (255, 236, 214)
CREME_ESC = (226, 176, 156)
CREME_ROSA = (250, 214, 228)
AMARELO = (253, 184, 4)
GARRA = (72, 50, 84)
GARRA_CLARA = (112, 84, 120)

# ---------------- geometria 2D (placas recortadas: membrana da asa e da orelha) ----------------
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

def curva(p0, n, p2, k=5):
    """Pontos de uma curva (Bézier quadrática) de p0 a p2 passando perto de n (sem as pontas)."""
    q = (2 * n[0] - (p0[0] + p2[0]) / 2, 2 * n[1] - (p0[1] + p2[1]) / 2)
    return [((1 - t) ** 2 * p0[0] + 2 * t * (1 - t) * q[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * t * (1 - t) * q[1] + t * t * p2[1]) for t in (i / k for i in range(1, k))]

def barra(nome, a, b, esp, z0, z1, mat, estica=0.0, res=None):
    """Barra grossa (osso da asa, moldura da orelha) entre dois pontos a, b do plano x-y: caixa girada em z."""
    mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    L = math.hypot(b[0] - a[0], b[1] - a[1]) + estica
    ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    return peca(nome, [mx - L / 2, my - esp / 2, z0], [mx + L / 2, my + esp / 2, z1], mat, rot=(0, 0, ang),
                pivo=(mx, my, (z0 + z1) / 2), res=res)

# ---------------- materiais em blocos (2-3 tons chapados) ----------------
def mat_bloco(cor, cima=.24, baixo=-.42, lado=-.06, borda=-.2, faixas=True, so_baixo=False):
    """Bloco sólido: face de cima clara, face de baixo na sombra; nas faces de pé, 3 tons chapados
    (faixa clara no alto, base, sombra no pé) e um fio escuro na borda."""
    def f(c):
        face = c["face"]
        if face == "up": l = cima
        elif face == "down": l = baixo
        else:
            y0, y1 = c["b"][0][1], c["b"][1][1]
            t = (c["p"][1] - y0) / max(y1 - y0, 1e-6)
            l = (.1 if t > .78 else -.16 if t < .24 else 0.0) if faixas else 0.0
            if face in ("east", "west"): l += lado
        if so_baixo and face not in ("up", "down"):
            if c["j"] == c["th"] - 1: l += borda
        elif g.na_borda(c): l += borda
        return tom(cor, l)
    return f

def mat_pena_faixa(c0, c1, ei, inv):
    """Pena grossa da cauda em faixas chapadas: cor c0 no começo do segmento e c1 no último terço."""
    def f(c):
        lo, hi = c["b"][0][ei], c["b"][1][ei]
        t = clamp((c["p"][ei] - lo) / max(hi - lo, 1e-6))
        if inv: t = 1 - t
        cor = c0 if t < 0.62 else c1
        face = c["face"]
        l = .22 if face == "up" else -.42 if face == "down" else 0.0
        if face in ("east", "west"):
            y0, y1 = c["b"][0][1], c["b"][1][1]
            v = (c["p"][1] - y0) / max(y1 - y0, 1e-6)
            l += .1 if v > .74 else -.18 if v < .26 else 0.0
        if g.na_borda(c): l -= .2
        return tom(cor, l)
    return f

def anel_q(ax, az, zc, phi, lado, n=3.0):
    """Ponto (x, z) numa superelipse em volta do corpo (quinas mais cheias que a elipse):
    phi = 0 lado de fora, -90 = frente, +90 = costas."""
    r = math.radians(phi)
    c, s = math.cos(r), math.sin(r)
    return lado * ax * math.copysign(abs(c) ** (2 / n), c), zc + az * math.copysign(abs(s) ** (2 / n), s)

def placa_degrau(nome, x, yt, z, W, H, T, giro, mat, passos=((0.5, 1.1),), recua=0.12, incl=0.0):
    """Placa grossa (pena em bloco) com a face larga para a frente (-z) girada 'giro' graus em y, e a beirada de
    baixo em degraus (cada passo: fração da largura, altura). Devolve o osso."""
    filhos = [peca(nome, [x - W / 2, yt - H, z - T / 2], [x + W / 2, yt, z + T / 2], mat)]
    y = yt - H
    for k, (fr, h) in enumerate(passos):
        w = W * fr; r = recua * (k + 1)
        filhos.append(peca(f"{nome}_p{k}", [x - w / 2, y - h, z - T / 2 + r], [x + w / 2, y + 0.02, z + T / 2 - r], mat))
        y -= h
    return osso(nome, [x, yt, z], [incl, giro, 0], filhos)

# ---------------- cabeça ----------------
CAB_Y0, CAB_Y1 = 21.0, 29.8
FR_X, FR_Z = 1.9, -9.4               # quina da frente (onde a faceta do olho começa)
LD_X, LD_Z = 6.4, -4.9               # quina do lado (onde a faceta termina)
FAC_T = 1.6
FAC_L = math.hypot(LD_X - FR_X, LD_Z - FR_Z)
_n = (0.7071, -0.7071)
FAC_C = ((FR_X + LD_X) / 2 - _n[0] * FAC_T / 2, (FR_Z + LD_Z) / 2 - _n[1] * FAC_T / 2)
OLHO_Y = 25.9
K_CAB = 1.08                         # escala da cabeça inteira (em volta da base)
OLHO_U = -0.9                        # o olho fica um pouco para o lado do bico na faceta
OLHO_RU, OLHO_RV = 1.9, 1.55
OLHO_ALTO, OLHO_BRAVO = 0.62, 0.3    # corte de cima do olho (sobrancelha brava descendo para o bico)
IRIS = ((196, 52, 20), (236, 112, 24))
ESCLERA = (255, 206, 30)

def cor_cabeca(p, face):
    x, y, z = p
    if face == "up": return ROXO
    base = ROXO_ESC if y > 23.0 else mix(ROXO_ESC, ROXO_NOITE, .5)
    if z > -0.5 and y > 27.0: base = mix(ROXO_ESC, ROXO, .35)          # 'capacete' da nuca
    return base

def olho(u, v):
    return g.pintar_olho(u - OLHO_U, v, OLHO_RU, OLHO_RV, iris=IRIS, esclera=ESCLERA, pupila=(34, 8, 18),
                         r_iris=(0.48, 0.72), c_iris=(-0.34, -0.1), r_pup=(0.24, 0.4), brilho=(255, 250, 236),
                         bravo=OLHO_BRAVO, alto=OLHO_ALTO, contorno=(92, 36, 30))

def mat_faceta(lado):
    base = mat_bloco(ROXO_ESC, faixas=False, borda=-.12)
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            cor = olho(z - FAC_C[1], y - OLHO_Y)
            if cor: return cor
            if y < 23.0: return tom(mix(ROXO_ESC, ROXO_NOITE, .5), -.05)
        return base(c)
    return f

def brilho_olho(c, cor):
    return cor[0] > 200 and 90 < cor[1] < 240 and cor[2] < 120

def cor_bico(p, face):
    x, y, z = p
    if face == "up" and y > 26.0 and abs(abs(x) - 1.0) < 0.3 and abs(z + 10.6) < 0.35: return (104, 60, 66)   # narinas
    if face == "down": return CREME_ESC
    if face == "up": return CREME_CLARO
    return (255, 226, 210) if y > 22.4 else mix((255, 226, 210), CREME_ESC, .5)

def msob_testa():
    return mat_bloco(ROXO_ESC, cima=.42, baixo=-.6, borda=-.16, faixas=False)

def cabeca_morcegalo():
    cab = []
    mc = mat_bloco(ROXO_ESC, faixas=False, borda=-.12)
    mcab = g.mat_cor(cor_cabeca, borda=.1, curva=.25)
    cab += g.arredondado2("cranio", [-LD_X, CAB_Y0, LD_Z - 0.1], [LD_X, CAB_Y1, 1.8], mcab, r=1.4, res=3)
    cab.append(peca("cara", [-FR_X, 21.4, FR_Z], [FR_X, 29.2, -6.0], mcab, faixa=(CAB_Y0, CAB_Y1), res=3))
    msob = mat_bloco(ROXO_ESC, cima=.4, baixo=-.6, borda=-.18, faixas=False)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 21.6, cz - FAC_L / 2], [cx + FAC_T / 2, 28.8, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, OLHO_Y, cz), res=8, brilho=brilho_olho))
        # sobrancelha brava: aba grossa por cima do olho, descendo para o bico
        ox = cx + (FAC_T / 2) * lado
        x0, x1 = sorted((ox - 0.3 * lado, ox + 1.0 * lado))
        yb = OLHO_Y + OLHO_ALTO * OLHO_RV - 0.12
        cab.append(osso("sobrancelha_" + s, [cx, yb, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s, [x0, yb, cz - FAC_L / 2 - 0.5], [x1, yb + 1.3, cz + FAC_L / 2 + 0.2], msob,
                 rot=(-16, 0, 0), pivo=(cx, yb, cz), res=4)]))
        # a sobrancelha continua pela frente, em V por cima do bico
        x0, x1 = sorted((0.0, 2.9 * lado))
        cab.append(peca("sobrancelha_fr_" + s, [x0, 26.1, FR_Z - 1.0], [x1, 27.6, FR_Z + 0.4], msob,
                        rot=(0, 0, 17 * lado), pivo=(2.9 * lado, 26.85, FR_Z), res=4))
    # bico de rapina creme em gancho: de frente é um V (camadas que estreitam para baixo), de lado curva para baixo
    mb = g.mat_cor(cor_bico, borda=.1, curva=.05, topo=.1, baixo=.3)
    fb = (20.5, 26.5)
    for nome, x, y0, y1, z0, z1 in (("bico_topo", 2.3, 24.5, 26.2, -12.5, -8.8), ("bico_meio", 1.95, 22.9, 24.6, -13.4, -8.9),
                                    ("bico_gancho", 1.4, 21.4, 23.0, -13.6, -11.2), ("bico_ponta", 0.75, 20.5, 21.5, -13.4, -12.2)):
        cab.append(peca(nome, [-x, y0, z0], [x, y1, z1], mb, faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-1.4, 21.5, -11.3], [1.4, 22.95, -8.9], mat_bloco(CREME_ESC, borda=-.12), res=4))
    # barbela: dois lóbulos magenta em blocos, pendurados embaixo do bico
    mbar = mat_bloco(MAGENTA, borda=-.15)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.08 * lado, 1.9 * lado))
        y0 = 18.0 if lado < 0 else 18.6
        x0, x1 = sorted((0.08 * lado, 2.4 * lado))
        cab.append(peca("barbela_" + s, [x0, y0 + 1.6, -11.2], [x1, 22.0, -8.8], mbar, res=4))
        x0, x1 = sorted((0.3 * lado, 1.9 * lado))
        cab.append(peca("barbela_p_" + s, [x0, y0, -10.6], [x1, y0 + 1.7, -9.1], mbar, res=4))
    # crista magenta em blocos escalonados (o '+' de frente), da testa para trás
    crista = []
    mcr = mat_bloco(MAGENTA, cima=.3, borda=-.18)
    for k, (zc, topo, d) in enumerate([(-8.2, 35.4, 2.3), (-6.0, 34.8, 2.2), (-3.8, 33.6, 2.1), (-1.7, 32.2, 2.0)]):
        crista.append(peca(f"crista{k}_a", [-1.1, 29.4, zc - d / 2], [1.1, topo - 2.6, zc + d / 2], mcr, res=4))
        crista.append(peca(f"crista{k}_b", [-1.6, topo - 2.6, zc - d / 2 - 0.15], [1.6, topo - 1.2, zc + d / 2 - 0.1], mcr, res=4))
        crista.append(peca(f"crista{k}_c", [-0.85, topo - 1.25, zc - d / 2 - 0.3], [0.85, topo, zc + d / 2 - 0.4], mcr, res=4))
    cab.append(osso("crista", [0, 30.0, -4.0], [0, 0, 0], crista))
    # orelhas de morcego
    for lado in (-1, 1):
        cab.append(orelha(lado))
    return cab

# ---------------- orelhas ----------------
OR_A = (2.2, 29.4, -3.2)             # raiz da orelha (lado +x)
OR_GIRO = (6, -40, 0)                # giro da orelha (lado +x): de frente para fora e para a frente
OR_POLI = [(0.0, 0.0), (4.6, 5.6), (12.2, 10.2), (12.3, -1.4), (10.8, -3.8), (6.2, -3.8), (1.9, -2.4)]
OR_DENTRO = [(1.7, -0.2), (5.0, 4.2), (10.8, 7.4), (11.0, -1.1), (10.0, -2.8), (6.0, -2.8), (2.4, -1.8)]

def mat_orelha(lado):
    ax, ay, az = OR_A
    def f(c):
        x, y, z = c["p"]
        u, v = (x - ax * lado) * lado, y - ay
        if not dentro_poli(u, v, OR_POLI): return None
        if c["face"] == "south" or not dentro_poli(u, v, OR_DENTRO):
            return tom(ROXO_ESC, -.1) if c["face"] == "south" else ROXO_ESC
        d = dist_borda(u, v, OR_DENTRO)
        cor = ROSA if d > 1.3 else MAGENTA if d > 0.35 else MAGENTA_ESC
        if d > 1.3 and v > 3.0: cor = ROSA_CLARO
        return cor
    return f

def mat_moldura(cor=ROXO_ESC):
    """Moldura grossa (orelha, asa): clara em cima, base nas faces largas, escura embaixo e nas quinas."""
    def f(c):
        face = c["face"]
        l = .3 if face == "up" else -.45 if face == "down" else 0.0 if face in ("north", "south") else -.12
        if g.na_borda(c): l -= .22
        return tom(cor, l)
    return f

def orelha(lado):
    s = "d" if lado < 0 else "e"
    ax, ay, az = OR_A
    ax *= lado
    P = lambda u, v: (ax + u * lado, ay + v)
    pts = [P(u, v) for u, v in OR_POLI]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    filhos = [peca("orelha_pele_" + s, [min(xs), min(ys), az - 0.35], [max(xs), max(ys), az + 0.35], mat_orelha(lado), res=3)]
    mo = mat_moldura(ROXO_ESC)
    filhos.append(barra("orelha_dentro_" + s, P(0.3, 0.3), P(4.7, 5.4), 1.6, az - 0.75, az + 0.65, mo, estica=1.0))
    filhos.append(barra("orelha_dentro2_" + s, P(4.6, 5.4), P(12.0, 9.9), 1.6, az - 0.75, az + 0.65, mo, estica=1.2))
    filhos.append(barra("orelha_fora_" + s, P(12.1, 9.9), P(12.1, -1.5), 1.6, az - 0.75, az + 0.65, mo, estica=1.0))
    filhos.append(barra("orelha_ponta_" + s, P(12.1, -1.2), P(10.5, -3.7), 1.4, az - 0.7, az + 0.6, mo, estica=0.6))
    rx, ry, rz = OR_GIRO
    return osso("orelha_" + s, [ax, ay, az], [rx, ry * lado, rz * lado], filhos)

# ---------------- asas membranosas ----------------
WZ = 1.2
ASA_GIRO = 30
_k = 1 / math.cos(math.radians(ASA_GIRO))
def _u(x): return 7.6 + (x - 7.6) * _k        # posição no plano da asa a partir do x visto de frente
ASA = {"S": (7.6, 20.6), "W": (_u(14.0), 25.3), "C": (_u(21.8), 22.2), "T1": (_u(23.8), 11.6),
       "N1": (_u(21.6), 16.0), "T2": (_u(19.2), 12.2), "N2": (_u(16.6), 15.4), "T3": (_u(14.2), 10.8),
       "N3": (_u(11.8), 14.2), "B": (_u(8.6), 11.2)}
A = ASA
ASA_POLI = [A["S"], A["W"], A["C"], A["T1"]] + curva(A["T1"], A["N1"], A["T2"]) + [A["T2"]] + \
           curva(A["T2"], A["N2"], A["T3"]) + [A["T3"]] + curva(A["T3"], A["N3"], A["B"]) + [A["B"]]
DEDOS = [(A["W"], A["C"], 1.6), (A["C"], A["T1"], 1.2), (A["W"], A["T2"], 0.9), (A["W"], A["T3"], 0.9), (A["S"], A["W"], 1.8)]

def mat_membrana(lado):
    def painel(u, y):
        """0 = painel de fora (entre a borda e o 1º dedo), 1 = do meio, 2 = de dentro (junto do corpo)."""
        def lado_de(a, b):
            return (b[0] - a[0]) * (y - a[1]) - (b[1] - a[1]) * (u - a[0])
        if lado_de(A["W"], A["T2"]) < 0: return 0
        if lado_de(A["W"], A["T3"]) < 0: return 1
        return 2
    def f(c):
        x, y, z = c["p"]
        u = x * lado
        if not dentro_poli(u, y, ASA_POLI): return None
        db = dist_borda(u, y, ASA_POLI)
        for t in ("T1",):
            tx, ty = A[t]
            if math.hypot(u - tx, y - ty) < 1.8 and y < ty + 1.7: return CREME if y > ty + 0.6 else CREME_ESC
        dd = min(dist_seg(u, y, a, b) - e / 2 for a, b, e in DEDOS)
        if dd < 0: return ROXO_ESC
        k = painel(u, y)
        cor = (ROSA, mix(ROSA, MAGENTA, .45), MAGENTA)[k]
        if y > 20.5: cor = mix(cor, ROSA_CLARO, .5)
        if dd < 0.7: cor = MAGENTA_ESC
        if db < 0.25: cor = tom(MAGENTA_ESC, -.25)
        if c["face"] == "south": cor = tom(cor, -.12)
        return cor
    return f

def asa(lado):
    s = "d" if lado < 0 else "e"
    P = lambda k: (A[k][0] * lado, A[k][1])
    us = [p[0] for p in ASA_POLI]; ys = [p[1] for p in ASA_POLI]
    x0, x1 = sorted((min(us) * lado, max(us) * lado))
    filhos = [peca("membrana_" + s, [x0, min(ys), WZ - 0.25], [x1, max(ys), WZ + 0.25], mat_membrana(lado), res=3)]
    mo = mat_moldura(ROXO_ESC)
    filhos.append(barra("braco_" + s, P("S"), P("W"), 2.0, WZ - 1.0, WZ + 1.0, mo, estica=1.0))
    filhos.append(barra("antebraco_" + s, P("W"), P("C"), 1.8, WZ - 0.85, WZ + 0.85, mo, estica=1.2))
    filhos.append(barra("dedo_fora_" + s, P("C"), P("T1"), 1.4, WZ - 0.7, WZ + 0.7, mo, estica=0.4))
    filhos.append(barra("dedo_meio_" + s, P("W"), P("T2"), 1.0, WZ - 0.5, WZ + 0.5, mo))
    filhos.append(barra("dedo_dentro_" + s, P("W"), P("T3"), 1.0, WZ - 0.5, WZ + 0.5, mo))
    wx, wy = P("W")
    filhos.append(peca("pulso_" + s, [wx - 1.4, wy - 1.4, WZ - 1.15], [wx + 1.4, wy + 1.4, WZ + 1.15], mo))
    cx, cy = P("C")
    filhos.append(peca("cotovelo_" + s, [cx - 1.0, cy - 1.0, WZ - 0.9], [cx + 1.0, cy + 1.0, WZ + 0.9], mo))
    tx, ty = P("T1")
    mg = mat_bloco(CREME, borda=-.15)
    filhos.append(peca("garra_asa_" + s, [tx - 0.75, ty - 1.6, WZ - 0.7], [tx + 0.75, ty + 1.6, WZ + 0.7], mg,
                       rot=(0, 0, 6 * lado), pivo=(tx, ty, WZ)))
    sx, sy = P("S")
    return osso("asa_" + s, [sx, sy, WZ], [0, -ASA_GIRO * lado, 0], filhos)

# ---------------- corpo ----------------
def cor_tronco(p, face):
    x, y, z = p
    if y > 17.5: return ROXO
    if y > 11.0: return ROXO_ESC
    return mix(ROXO_ESC, ROXO_NOITE, .5)

# fileiras de penas em bloco em volta do corpo: (y do alto, altura, raio x, raio z, centro z, cor, phis)
FILEIRAS = [
    (21.6, 3.8, 8.2, 6.4, -0.8, mix(ROXO, ROXO_MED, .5), [-30, -2, 26, 54]),
    (18.2, 4.0, 9.0, 7.0, -0.6, ROXO, [-40, -12, 16, 44, 68]),
    (14.6, 4.0, 9.3, 7.4, -0.4, mix(ROXO, ROXO_ESC, .5), [-58, -30, -2, 26, 54]),
    (11.0, 3.6, 9.2, 7.3, -0.3, ROXO_ESC, [-62, -34, -6, 22, 50]),
]

# peitoral: fileiras de placas lavanda em degraus (y do alto, x das placas, largura, z da frente, cor)
PEITO = [
    (21.2, [0.0, 3.0, 5.7], 3.4, -9.7, mix(LAVANDA, LILAS, .4)),
    (18.8, [1.5, 4.4], 3.4, -9.6, LAV_CLARO),
    (16.4, [0.0, 3.1], 3.4, -9.4, mix(LAVANDA, LILAS, .3)),
    (14.0, [1.5, 4.2], 3.1, -9.1, mix(LAVANDA, LILAS, .55)),
    (11.6, [0.0, 2.9], 3.0, -8.6, LILAS),
]

def montar():
    # ---------- cabeça ----------
    i_cab = len(g.PECAS)
    cab = cabeca_morcegalo()
    g.transformar(i_cab, cab, (0.0, 21.2, -3.0), K_CAB)      # cabeça grande, como na ficha
    cabeca = osso("cabeca", [0, 22.0, -3.0], [0, 0, 0], cab)
    pescoco = osso("pescoco", [0, 20.5, -2.5], [0, 0, 0], [
        peca("pescoco", [-5.0, 19.0, -7.6], [5.0, 23.0, 1.0], mat_bloco(ROXO_ESC, faixas=False)),
        cabeca])

    corpo = []
    mt = g.mat_cor(cor_tronco, borda=.1, curva=.3)
    corpo += g.arredondado2("tronco", [-8.6, 7.0, -7.6], [8.6, 21.8, 6.6], mt, r=3.0)
    corpo += g.arredondado("peito_base", [-6.6, 11.0, -8.8], [6.6, 22.6, -2.0], mt, r=1.6)

    # ---------- plumagem em blocos: fileiras de penas grossas com a ponta em degrau ----------
    plum = []
    for r, (yt, H, ax, az, zc, cor, phis) in enumerate(FILEIRAS):
        for k, phi in enumerate(phis + [90]):
            for lado in ((1,) if phi == 90 else (-1, 1)):
                x, z = anel_q(ax, az, zc, phi, lado)
                cor_k = tom(cor, .1) if (k + r) % 2 == 0 else cor
                if phi >= 60 and r < 3:                     # costas: blocos lilás e roxos alternados (como na traseira da ficha)
                    cor_k = mix(LILAS, LAVANDA, .3) if (k + r) % 2 == 0 else ROXO_MED
                dy = 0.35 if (k + r) % 2 else -0.25           # fileira desencontrada: beirada de baixo em degraus
                plum.append(placa_degrau(f"pena{r}{k}_{'d' if lado < 0 else 'e'}", x, yt + dy, z, 4.8, H, 1.8,
                                         -(phi + 90) * lado, mat_bloco(cor_k, cima=.32, so_baixo=True), passos=((0.55, 1.3),),
                                         incl=9))
    corpo.append(osso("plumagem", [0, 14, 0], [0, 0, 0], plum))

    # ---------- gola: penas lilás em blocos embaixo da cabeça (bochecha e nuca) ----------
    gola = []
    for k, phi in enumerate([-14, 18, 50, 90]):
        for lado in ((1,) if phi == 90 else (-1, 1)):
            x, z = anel_q(6.4, 5.4, -3.0, phi, lado)
            cor = ROXO_MED if k % 2 == 0 else mix(ROXO_MED, LILAS, .45)
            gola.append(placa_degrau(f"gola{k}_{'d' if lado < 0 else 'e'}", x, 23.2, z, 4.4, 3.0, 1.3,
                                     -(phi + 90) * lado, mat_bloco(cor), passos=((0.5, 1.1),)))
    corpo.append(osso("gola", [0, 22, -3], [0, 0, 0], gola))

    # ---------- peitoral sombrio: placas lavanda grossas, em degraus, em V ----------
    peito = []
    R = 9.5
    for t, (yt, xs, W, zf, cor) in enumerate(PEITO):
        for k, xc in enumerate(xs):
            for lado in ((1,) if xc == 0 else (-1, 1)):
                x = xc * lado
                ang = math.degrees(math.asin(clamp(abs(x) / R, 0, 0.95)))
                z = zf + R - math.sqrt(max(R * R - x * x, 0)) + 0.7
                cor_k = cor if (k + t) % 2 == 0 else mix(cor, LILAS, .35)
                peito.append(placa_degrau(f"peito{t}{k}_{'d' if lado < 0 else 'e'}", x, yt, z, W, 2.9, 1.4,
                                          -ang * (1 if x > 0 else -1), mat_bloco(cor_k, borda=-.12),
                                          passos=((0.62, 1.1),), incl=7))
    corpo.append(osso("peitoral", [0, 16, -8], [0, 0, 0], peito))

    # ---------- asas ----------
    corpo.append(asa(-1)); corpo.append(asa(1))

    # ---------- cauda: leque cheio de penas grossas em foice, faixas roxo -> violeta -> lilás-rosa -> creme ----------
    cauda = []
    SEGS = [(5.8, 4.6, 5.0, ROXO_ESC, ROXO), (5.6, 4.3, 4.8, ROXO, VIOLETA), (5.0, 3.8, 4.3, VIOLETA, ROSA_CLARO),
            (4.0, 3.2, 3.5, CREME_ROSA, CREME_ROSA), (2.4, 2.0, 2.0, CREME_ROSA, CREME_CLARO)]
    def pena_cauda(nome, x, y, z, rot0, cv, esc=1.0):
        segs = [(L * esc, w, h, c0, c1) for L, w, h, c0, c1 in SEGS]
        return g.pena_curva(nome, (x, y, z), segs, rot0, (cv, 0, 0), "z", mat_pena_faixa)
    # leque do meio (x = 0): de cima para baixo, cada pena sobe um pouco e cai em foice
    for k, (y, rx, cv, esc) in enumerate([(18.8, -33, 12, 0.9), (16.6, -18, 12, 1.05), (14.2, -6, 12, 1.05),
                                          (12.2, 4, 11, 0.9), (10.8, 10, 9, 0.6)]):
        cauda.append(pena_cauda(f"rabo{k}", 0.0, y, 6.0, (rx, 0, 0), cv, esc))
    # penas dos lados, entre as do meio, abrindo para fora (de costas o leque desce em diagonal)
    for k, (x, y, rx, ry, cv, esc) in enumerate([(3.4, 17.8, -25, 8, 12, 0.95), (3.6, 15.4, -13, 12, 12, 1.0),
                                                 (3.6, 13.0, -1, 18, 11, 0.92), (3.2, 11.4, 7, 24, 10, 0.72)]):
        for lado in (-1, 1):
            cauda.append(pena_cauda(f"rabo{5 + k}_{'d' if lado < 0 else 'e'}", x * lado, y, 5.8,
                                    (rx, ry * lado, 0), cv, esc))
    corpo.append(osso("cauda", [0, 16.0, 5.6], [0, 0, 0], cauda))

    corpo.append(pescoco)
    tronco = osso("corpo", [0, 11.0, 0], [0, 0, 0], corpo)

    # ---------- pernas: canela creme grossa, pé de 3 dedos com garras escuras + 1 atrás ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 4.6 * lado; zc = -0.6
        pp = []
        pp.append(peca("coxa_" + s, [xc - 2.2, 6.0, zc - 2.2], [xc + 2.2, 9.5, zc + 2.2], mat_bloco(ROXO_ESC)))
        mcan = mat_bloco(CREME, borda=-.12)
        pp += g.octogono("canela_" + s, [xc - 1.6, 2.0, zc - 1.6], [xc + 1.6, 7.2, zc + 1.6], mcan, r=0.5)
        pp.append(peca("pe_" + s, [xc - 2.5, 0.0, zc - 2.6], [xc + 2.5, 2.8, zc + 1.8], mcan))
        mdedo = mat_bloco(CREME, borda=-.15)
        mgar = mat_bloco(GARRA, cima=.3, borda=-.15)
        for nome, giro, dx in (("meio", 0, 0), ("fora", -34 * lado, 3.4 * lado), ("dentro", 28 * lado, -3.0 * lado)):
            x0, z0 = xc + dx * 0.7, zc - 1.8
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - 1.05, 0, z0 - 3.0], [x0 + 1.05, 2.5, z0 + 0.4], mdedo),
                peca(f"garra_{nome}_{s}", [x0 - 0.95, 0, z0 - 4.7], [x0 + 0.95, 2.4, z0 - 2.9], mgar)]))
        pp.append(peca("dedo_tras_" + s, [xc - 0.8, 0, zc + 1.4], [xc + 0.8, 1.8, zc + 3.4], mdedo))
        pp.append(peca("garra_tras_" + s, [xc - 0.7, 0, zc + 3.3], [xc + 0.7, 1.7, zc + 4.6], mgar))
        return osso("perna_" + s, [xc, 9.0, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
