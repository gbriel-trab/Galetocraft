"""Morcegalo (#010, Sombrio): galo-morcego noturno de plumagem roxa em blocos, orelhas de morcego e asas membranosas."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp

ID = "morcegalo"; NOME = "Morcegalo"; NUMERO = 10
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 26.5, -6.0), 9.0)
ONDAS = [("rabo0", 4, (2, 2, 0)), ("rabo1", 4, (2, -2, 0)), ("rabo2", 4, (2, 2, 0))]
ANIM_PARADO = {
    "orelha_d": [(0, 0, 0), (0, 0, 4), (0, 0, 0), (-3, 2, 0), (0, 0, 0), (0, 0, 0)],
    "orelha_e": [(0, 0, 0), (0, 0, -4), (0, 0, 0), (0, 0, 0), (-3, -2, 0), (0, 0, 0)],
}
ANIM_ANDANDO = {
    "orelha_d": [(0, 0, 0), (-4, 0, 3), (0, 0, 0), (-4, 0, 3), (0, 0, 0)],
    "orelha_e": [(0, 0, 0), (-4, 0, -3), (0, 0, 0), (-4, 0, -3), (0, 0, 0)],
}

# ---------------- paleta (Paleta de Cores da ficha) ----------------
ROXO_NOITE = (64, 28, 98)          # sombra do corpo/cabeça (vistas: (59,25,82))
ROXO_ESC = (94, 46, 142)           # lado do corpo, cabeça (vistas: (80,42,125))
ROXO = (124, 60, 178)
ROXO_MED = (156, 88, 198)          # paleta: (140,85,184)
MOLDURA = (110, 56, 160)           # moldura da orelha e borda da asa (vistas: (94,47,133))
VIOLETA = (164, 68, 210)           # cauda (vistas: (160,64,204))
VIOLETA_CLARO = (198, 96, 236)
LILAS = (198, 140, 228)            # paleta: (192,139,232)
LILAS_ROSA = (206, 132, 200)       # faixa clara da cauda
LAVANDA = (226, 176, 234)          # peito (vistas: (213,162,216))
LAV_CLARO = (240, 208, 246)
MAGENTA = (214, 80, 156)           # barbela (vistas: (212,78,154)); paleta (215,81,151)
MAGENTA_ESC = (160, 50, 130)
ROSA = (226, 106, 190)             # membrana/orelha (arte: (200,90,189))
ROSA_CLARO = (242, 150, 216)
CRISTA = (232, 82, 172)            # crista (vistas: (240,86,179))
CREME = (252, 216, 185)            # garra da asa (paleta)
CREME_ROSA = (250, 200, 226)       # ponta da cauda (vistas: (250,214,227))
CREME_CLARO = (255, 234, 236)
BICO = (246, 202, 198)             # bico (vistas: (244,195,193))
BICO_CLARO = (255, 228, 222)
BICO_ESC = (220, 160, 156)
CANELA = (238, 186, 182)           # pernas e dedos (vistas: (228,172,170))
GARRA = (90, 54, 112)              # garras roxo-escuras (vistas: (89,54,109))

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
            l += .08 if v > .86 else -.12 if v < .12 else 0.0   # só um fio claro em cima e escuro embaixo
        elif face in ("north", "south"): cor = mix(cor, LAVANDA, .45)   # corte (visto de costas): lilás claro, como na traseira
        if g.na_borda(c): l -= .2
        return tom(cor, l)
    return f

def pena_foice(nome, base, segs, rot0, curvas):
    """Pena grossa em foice (cresce para +z): segmentos encadeados ('<nome>_0', '_1'...) que curvam cada vez mais
    ('curvas' em graus, uma por junta) e terminam numa ponta afiada (bloco girado 45°, um losango visto de lado)."""
    def seg(k, pos):
        L, w, h, c0, c1 = segs[k]
        px, py, pz = pos
        filhos = [peca(f"{nome}_{k}", [px - w / 2, py - h / 2, pz], [px + w / 2, py + h / 2, pz + L], mat_pena_faixa(c0, c1, 2, False))]
        if k + 1 < len(segs):
            filhos.append(seg(k + 1, (px, py, pz + L - .2)))
        else:
            q = h * 0.72
            filhos.append(peca(f"{nome}_ponta", [px - w * 0.36, py - q / 2, pz + L - q / 2], [px + w * 0.36, py + q / 2, pz + L + q / 2],
                               mat_pena_faixa(c1, c1, 2, False), rot=(45, 0, 0), pivo=(px, py, pz + L)))
        r = list(rot0) if k == 0 else [curvas[k - 1], 0, 0]
        return osso(f"{nome}_{k}", list(pos), r, filhos)
    return seg(0, tuple(base))

def anel_q(ax, az, zc, phi, lado, n=3.0):
    """Ponto (x, z) numa superelipse em volta do corpo (quinas mais cheias que a elipse):
    phi = 0 lado de fora, -90 = frente, +90 = costas."""
    r = math.radians(phi)
    c, s = math.cos(r), math.sin(r)
    return lado * ax * math.copysign(abs(c) ** (2 / n), c), zc + az * math.copysign(abs(s) ** (2 / n), s)

def placa_degrau(nome, x, yt, z, W, H, T, giro, mat, passos=((0.5, 1.1),), recua=0.12, incl=0.0, v=False):
    """Placa grossa (pena em bloco) com a face larga para a frente (-z) girada 'giro' graus em y, e a beirada de
    baixo em degraus (cada passo: fração da largura, altura). Devolve o osso."""
    filhos = [peca(nome, [x - W / 2, yt - H, z - T / 2], [x + W / 2, yt, z + T / 2], mat)]
    y = yt - H
    if v:                                                   # ponta em V (chevron): quadrado girado 45° embaixo
        q = W / 1.4142 * 0.98
        filhos.append(peca(f"{nome}_v", [x - q / 2, y - q / 2, z - T / 2 + recua], [x + q / 2, y + q / 2, z + T / 2 - recua], mat,
                           rot=(0, 0, 45), pivo=(x, y, z)))
        passos = ()
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
IRIS = ((200, 56, 24), (238, 118, 30))
ESCLERA = (252, 222, 100)            # amarelo claro da ficha (vistas: (252,224,116))

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
    return cor[0] > 200 and 90 < cor[1] < 240 and cor[2] < 140

def cor_bico(p, face):
    x, y, z = p
    if face == "up" and abs(abs(x) - 0.95) < 0.32 and abs(z + 10.2) < 0.35: return (110, 60, 70)   # narinas
    if face == "down": return BICO_ESC
    if face == "up": return BICO_CLARO
    return BICO if y > 22.6 else mix(BICO, BICO_ESC, .6)

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
    # bico de rapina em gancho curto: cera junto da cara, mandíbula de cima inclinada para baixo e o gancho em V
    # (quadrado girado 45° em z). De frente é uma cunha que afina até a ponta; de lado o topo cai até o gancho.
    mb = g.mat_cor(cor_bico, borda=.05, curva=.05, topo=.12, baixo=.3)
    fb = (20.5, 26.5)
    cab.append(peca("bico_cera", [-2.3, 22.8, -10.0], [2.3, 26.2, -8.8], mb, faixa=fb, res=4))
    giro = dict(rot=(-22, 0, 0), pivo=(0, 26.0, -9.6))
    cab.append(peca("bico_cima", [-1.9, 23.7, -12.4], [1.9, 26.0, -9.6], mb, faixa=fb, res=4, **giro))
    q = 2.7
    cab.append(osso("bico_v", [0, 26.0, -9.6], [-22, 0, 0], [
        peca("bico_gancho", [-q / 2, 23.7 - q / 2, -12.9], [q / 2, 23.7 + q / 2, -10.0], mb, faixa=fb, res=4,
             rot=(0, 0, 45), pivo=(0, 23.7, -11.5))]))
    cab.append(peca("bico_baixo", [-1.2, 21.7, -11.0], [1.2, 22.9, -8.9], mat_bloco(BICO_ESC, borda=-.1), res=4))
    # barbela: dois lóbulos magenta em blocos, pendurados embaixo do bico
    mbar = mat_bloco(MAGENTA, borda=-.12)
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
    mcr = mat_bloco(CRISTA, cima=.3, borda=-.15)
    for k, (zc, topo, d) in enumerate([(-9.8, 35.2, 2.4), (-7.6, 34.8, 2.3), (-5.4, 33.8, 2.2), (-3.3, 32.4, 2.1)]):
        crista.append(peca(f"crista{k}_a", [-1.1, 29.4, zc - d / 2], [1.1, topo - 2.6, zc + d / 2], mcr, res=4))
        crista.append(peca(f"crista{k}_b", [-1.6, topo - 2.6, zc - d / 2 - 0.15], [1.6, topo - 1.2, zc + d / 2 - 0.1], mcr, res=4))
        crista.append(peca(f"crista{k}_c", [-0.85, topo - 1.25, zc - d / 2 - 0.3], [0.85, topo, zc + d / 2 - 0.4], mcr, res=4))
    cab.append(osso("crista", [0, 30.0, -4.0], [0, 0, 0], crista))
    # orelhas de morcego
    for lado in (-1, 1):
        cab.append(orelha(lado))
    return cab

# ---------------- orelhas ----------------
OR_A = (2.2, 29.4, -3.8)             # raiz da orelha (lado +x)
OR_GIRO = (2, -40, -2)                # giro da orelha (lado +x): de frente para fora e para a frente
OR_POLI = [(0.0, 0.0), (4.6, 5.2), (12.2, 9.4), (12.3, -1.4), (10.8, -3.8), (6.2, -3.8), (1.9, -2.4)]
OR_DENTRO = [(1.7, -0.2), (5.0, 3.8), (10.8, 6.8), (11.0, -1.1), (10.0, -2.8), (6.0, -2.8), (2.4, -1.8)]

def mat_orelha(lado):
    """Pele da orelha: magenta escuro junto da moldura de cima, rosa claro embaixo e para fora, uma dobra mais
    escura no meio (como em 'Orelhas Noturnas'); costas roxo-escuras."""
    ax, ay, az = OR_A
    def f(c):
        x, y, z = c["p"]
        u, v = (x - ax * lado) * lado, y - ay
        if not dentro_poli(u, v, OR_POLI): return None
        if c["face"] == "south" or not dentro_poli(u, v, OR_DENTRO):
            return mix(MOLDURA, ROXO_MED, .25) if c["face"] == "south" else MOLDURA
        d = dist_borda(u, v, OR_DENTRO)
        if d < 0.45: return MAGENTA_ESC
        t = clamp((u * 0.35 - v * 0.55 + 2.5) / 5.0)          # 0 = alto/dentro, 1 = baixo/fora
        cor = MAGENTA if t < 0.33 else ROSA if t < 0.66 else ROSA_CLARO
        if dist_seg(u, v, (3.0, 0.2), (10.0, 4.6)) < 0.45: cor = mix(cor, MAGENTA_ESC, .6)   # dobra
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
    mo = mat_moldura(MOLDURA)
    filhos.append(barra("orelha_dentro_" + s, P(0.3, 0.3), P(4.7, 5.0), 1.6, az - 0.75, az + 0.65, mo, estica=1.0))
    filhos.append(barra("orelha_dentro2_" + s, P(4.6, 5.0), P(12.0, 9.1), 1.6, az - 0.75, az + 0.65, mo, estica=1.2))
    filhos.append(barra("orelha_fora_" + s, P(12.1, 9.1), P(12.1, -1.5), 1.6, az - 0.75, az + 0.65, mo, estica=1.0))
    filhos.append(barra("orelha_ponta_" + s, P(12.1, -1.2), P(10.5, -3.7), 1.4, az - 0.7, az + 0.6, mo, estica=0.6))
    rx, ry, rz = OR_GIRO
    return osso("orelha_" + s, [ax, ay, az], [rx, ry * lado, rz * lado], filhos)

# ---------------- asas membranosas ----------------
WZ = 0.2
ASA_GIRO = 30
_k = 1 / math.cos(math.radians(ASA_GIRO))
def _u(x): return 7.6 + (x - 7.6) * _k        # posição no plano da asa a partir do x visto de frente
ASA = {"S": (7.6, 20.4), "W": (_u(14.0), 24.7), "C": (_u(22.8), 23.0), "T1": (_u(24.8), 11.6),
       "N1": (_u(22.4), 16.0), "T2": (_u(19.8), 12.0), "N2": (_u(16.6), 15.2), "T3": (_u(14.2), 10.4),
       "N3": (_u(11.8), 13.6), "B": (_u(8.6), 10.4)}
A = ASA
ASA_POLI = [A["S"], A["W"], A["C"], A["T1"]] + curva(A["T1"], A["N1"], A["T2"]) + [A["T2"]] + \
           curva(A["T2"], A["N2"], A["T3"]) + [A["T3"]] + curva(A["T3"], A["N3"], A["B"]) + [A["B"]]
DEDOS = [(A["W"], A["C"], 1.6), (A["C"], A["T1"], 1.2), (A["W"], A["T2"], 0.9), (A["W"], A["T3"], 0.9), (A["S"], A["W"], 1.8)]

def mat_membrana(lado):
    """Membrana em faixas chapadas: magenta escuro embaixo do braço, rosa no meio, rosa claro na beirada recortada;
    sombra junto dos dedos (como em 'Asa Membranosa')."""
    def f(c):
        x, y, z = c["p"]
        u = x * lado
        if not dentro_poli(u, y, ASA_POLI): return None
        db = dist_borda(u, y, ASA_POLI)
        for t in ("T1", "T3"):
            tx, ty = A[t]
            r = 1.8 if t == "T1" else 1.2
            if math.hypot(u - tx, y - ty) < r and y < ty + r - 0.1: return CREME if y > ty + 0.5 else tom(CREME, -.2)
        dd = min(dist_seg(u, y, a, b) - e / 2 for a, b, e in DEDOS)
        if dd < 0: return ROXO_ESC
        if db < 1.3 and y < 17.5: cor = ROSA_CLARO
        elif y > 20.0: cor = (150, 48, 132)
        elif y > 17.0: cor = (186, 66, 160)
        elif y > 14.0: cor = ROSA
        else: cor = mix(ROSA, ROSA_CLARO, .5)
        if dd < 0.6: cor = mix(cor, MAGENTA_ESC, .6)
        if db < 0.25: cor = tom(MAGENTA_ESC, -.2)
        if c["face"] == "south": cor = tom(cor, .22)
        return cor
    return f

def asa(lado):
    s = "d" if lado < 0 else "e"
    P = lambda k: (A[k][0] * lado, A[k][1])
    us = [p[0] for p in ASA_POLI]; ys = [p[1] for p in ASA_POLI]
    x0, x1 = sorted((min(us) * lado, max(us) * lado))
    filhos = [peca("membrana_" + s, [x0, min(ys), WZ - 0.25], [x1, max(ys), WZ + 0.25], mat_membrana(lado), res=3)]
    mo = mat_moldura(MOLDURA)
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
    t3x, t3y = P("T3")
    filhos.append(peca("garra_dedo_" + s, [t3x - 0.5, t3y - 1.1, WZ - 0.5], [t3x + 0.5, t3y + 0.9, WZ + 0.5], mg))
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
    (18.2, 4.0, 9.0, 7.0, -0.6, ROXO, [-34, -8, 18, 44, 68]),
    (14.6, 4.0, 9.3, 7.4, -0.4, mix(ROXO, ROXO_ESC, .5), [-36, -8, 20, 48]),
    (11.0, 3.6, 9.2, 7.3, -0.3, ROXO_ESC, [-40, -12, 16]),
]

# peitoral: fileiras de placas lavanda em degraus (y do alto, x das placas, largura, z da frente, cor)
PEITO = [
    (21.6, [0.0, 3.0, 5.7], 3.4, -9.7, mix(VIOLETA, LILAS, .6)),
    (19.4, [1.5, 4.4, 6.6], 3.4, -9.6, LAV_CLARO),
    (17.2, [0.0, 3.1, 5.9], 3.4, -9.4, LAV_CLARO),
    (15.0, [1.5, 4.2], 3.1, -9.1, LAVANDA),
    (12.9, [0.0], 3.0, -8.7, mix(LAVANDA, LILAS, .5)),
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
        for k, phi in enumerate(phis + ([90] if r < 3 else [])):
            for lado in ((1,) if phi == 90 else (-1, 1)):
                x, z = anel_q(ax, az, zc, phi, lado)
                cor_k = tom(cor, .1) if (k + r) % 2 == 0 else cor
                if phi >= 40 and r < 3:                     # costas: blocos lilás e violeta alternados (traseira da ficha)
                    cor_k = mix(LILAS, LAVANDA, .4) if (k + r) % 2 == 0 else VIOLETA
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
                ang = math.degrees(math.asin(clamp(abs(x) / R, 0, 0.82)))
                z = zf + R - math.sqrt(max(R * R - x * x, 0)) + 0.7
                cor_k = cor if (k + t) % 2 == 0 else mix(cor, LILAS, .35)
                peito.append(placa_degrau(f"peito{t}{k}_{'d' if lado < 0 else 'e'}", x, yt, z, W, 2.9, 1.4,
                                          -ang * (1 if x > 0 else -1), mat_bloco(cor_k, borda=-.12),
                                          v=True, incl=7))
    corpo.append(osso("peitoral", [0, 16, -8], [0, 0, 0], peito))

    # ---------- asas ----------
    corpo.append(asa(-1)); corpo.append(asa(1))

    # ---------- cauda: leque cheio de penas grossas em foice, faixas roxo -> violeta -> lilás-rosa -> creme ----------
    cauda = []
    # faixas amostradas na ficha (pena de cima, da raiz à ponta): roxo escuro, violeta (175,80,225) em ~60%,
    # lilás-rosa curto e a ponta creme-rosada (250,210,230) em ~35%, afinando e curvando
    SEGS = [(5.6, 4.4, 5.4, ROXO, VIOLETA), (5.4, 4.2, 5.8, VIOLETA, VIOLETA_CLARO), (4.8, 3.8, 5.2, VIOLETA_CLARO, LILAS_ROSA),
            (4.4, 3.2, 4.0, CREME_ROSA, CREME_CLARO)]     # gorda no meio (crescente), fina nas pontas
    SEGS_BAIXO = [(5.6, 4.4, 5.4, ROXO_ESC, ROXO), (5.4, 4.2, 5.8, ROXO, VIOLETA)] + [(4.8, 3.8, 5.2, VIOLETA, VIOLETA_CLARO), (4.4, 3.2, 4.0, VIOLETA_CLARO, LILAS_ROSA)]
    def pena_cauda(nome, x, y, z, rot0, cv, esc=1.0, baixo=False):
        segs = [(L * esc, w, h, c0, c1) for L, w, h, c0, c1 in (SEGS_BAIXO if baixo else SEGS)]
        return pena_foice(nome, (x, y, z), segs, rot0, (cv * 0.7, cv, cv * 1.5))
    # leque do meio (x = 0), medido na lateral da ficha: 5 foices separadas, abertas em leque de ~45° para cima até
    # ~60° para baixo; as de cima são as mais compridas, as de baixo curtas
    for k, (y, rx, cv, esc) in enumerate([(19.6, -36, 17, 0.92), (17.2, -18, 17, 1.0), (14.8, 0, 17, 0.95),
                                          (12.6, 16, 15, 0.76), (11.4, 26, 13, 0.46)]):
        cauda.append(pena_cauda(f"rabo{k}", 0.0, y, 6.0, (rx, 0, 0), cv, esc, baixo=k >= 3))
    # dois pares de penas dos lados, embaixo, abrindo para fora (de costas o leque desce em diagonal)
    for k, (x, y, rx, ry, cv, esc) in enumerate([(3.0, 16.0, -9, 14, 17, 0.78), (3.2, 13.6, 8, 24, 16, 0.68)]):
        for lado in (-1, 1):
            cauda.append(pena_cauda(f"rabo{5 + k}_{'d' if lado < 0 else 'e'}", x * lado, y, 5.8,
                                    (rx, ry * lado, 0), cv, esc, baixo=True))
    corpo.append(osso("cauda", [0, 16.0, 5.6], [0, 0, 0], cauda))

    corpo.append(pescoco)
    tronco = osso("corpo", [0, 11.0, 0], [0, 0, 0], corpo)

    # ---------- pernas: canela creme grossa, pé de 3 dedos com garras escuras + 1 atrás ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 4.6 * lado; zc = -0.6
        pp = []
        pp.append(peca("coxa_" + s, [xc - 2.2, 6.0, zc - 2.2], [xc + 2.2, 9.5, zc + 2.2], mat_bloco(ROXO_ESC)))
        mcan = mat_bloco(CANELA, borda=-.12)
        pp += g.octogono("canela_" + s, [xc - 1.6, 2.0, zc - 1.6], [xc + 1.6, 7.2, zc + 1.6], mcan, r=0.5)
        pp.append(peca("pe_" + s, [xc - 2.5, 0.0, zc - 2.6], [xc + 2.5, 2.8, zc + 1.8], mcan))
        mdedo = mat_bloco(CANELA, borda=-.15)
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
