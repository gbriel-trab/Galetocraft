"""Morcegalo (#010, Sombrio): galo-morcego noturno de plumagem roxa em blocos, orelhas de morcego e asas membranosas."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, clamp

LUZ_FRIA = (255, 244, 250)
def tom(c, f):
    """Luz da ficha ("neon na sombra"): f > 0 clareia um pouco para a luz; f < 0 só escurece multiplicando, sem lavar
    para o cinza (o jogo ainda sombreia as faces sozinho)."""
    f = clamp(f, -1, 1)
    if f >= 0: return mix(c, LUZ_FRIA, f * 0.32)
    k = 1 + f * 0.6
    return tuple(int(round(v * k)) for v in c)

def mat_cor(cor_fn, **kw):
    """Como galo_base.mat_cor, mas com a luz acima (cores saturadas)."""
    def f(c):
        base = cor_fn(c["p"], c["face"])
        return None if base is None else tom(base, g.contexto_luz(c, **kw))
    return f

ID = "morcegalo"; NOME = "Morcegalo"; NUMERO = 10
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 26.5, -6.0), 9.0)
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
CRISTA = (226, 80, 166)            # crista (vistas: (240,86,179), sombra (186,40,133))
CRISTA_CLARA = (246, 138, 206)
CREME = (252, 216, 185)            # garra da asa (paleta)
CREME_ROSA = (250, 200, 226)       # ponta da cauda (vistas: (250,214,227))
CREME_CLARO = (255, 234, 236)
BICO = (246, 196, 186)             # bico (neutra: (247,188,183); vistas: (244,195,193))
BICO_CLARO = (252, 220, 210)
BICO_ESC = (230, 170, 160)
CANELA = (248, 204, 186)           # pernas e dedos (vistas: (228,172,170); 'Garras': (240,190,185))
GARRA = (78, 44, 108)              # garras roxo-escuras (vistas: (89,54,109); paleta (58,30,101))
P_ROXO = (58, 30, 101); P_VIOLETA = (140, 85, 184); P_LILAS = (192, 139, 232); P_LAVANDA = (232, 186, 240)
P_MAGENTA = (215, 81, 151); P_CREME = (252, 216, 185); P_OURO = (253, 184, 4); P_MARROM = (97, 71, 73)
P_LAV_TOPO = (247, 208, 251); P_ROSA_CLARO = (232, 136, 200); P_VIOLETA_ROSA = (179, 82, 185)
INDIGO = (62, 32, 108)             # base das penas do corpo (vistas: (80,42,125) no lado, (59,25,82) embaixo)
INDIGO_2 = (74, 40, 124)
VIOLETA_PENA = (140, 88, 206)      # pontas serrilhadas das penas do corpo (vistas: (131,95,168))
PEITO_CLARO = (220, 172, 230)      # centro do peito (vistas: (213,162,216))
PEITO_BORDA = (196, 132, 210)      # bordas do peito (vistas: (194,121,206), (200,134,199))
SELA_CLARA = (226, 200, 240)       # xadrez das costas (traseira: (230,187,232))

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
def mat_bloco(cor, cima=.24, baixo=-.32, lado=-.04, borda=-.14, faixas=True, so_baixo=False):
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
        elif face in ("north", "south"): l -= .0
        if g.na_borda(c): l -= .2
        return tom(cor, l)
    return f

def pena_foice(nome, base, segs, rot0, curvas):
    """Pena-foice (cresce para +z): segmentos encadeados ('<nome>_0', '_1'...) cada vez mais finos (o último é a
    ponta fina) e cada junta gira mais que a anterior ('curvas'), formando o arco. Os cortes (vistos de costas)
    alternam violeta e lilás."""
    def mat(k, c0, c1):
        m = mat_pena_faixa(c0, c1, 2, False)
        def f(c):
            if c["face"] in ("north", "south"): return P_VIOLETA if k % 2 == 0 else P_LILAS
            return m(c)
        return f
    def seg(k, pos):
        L, w, h, c0, c1 = segs[k]
        px, py, pz = pos
        filhos = [peca(f"{nome}_{k}", [px - w / 2, py - h / 2, pz], [px + w / 2, py + h / 2, pz + L], mat(k, c0, c1))]
        if k + 1 < len(segs):
            filhos.append(seg(k + 1, (px, py - 0.15 * h, pz + L - .25)))
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
OLHO_U = -0.95                       # o olho fica junto da base do bico, na ponta da frente da faceta
OLHO_RU, OLHO_RV = 2.05, 1.6           # ~25% da largura da cabeça (frente da ficha: 3,0 de 11,5)
OLHO_ALTO, OLHO_BRAVO = 0.36, 0.3    # pálpebra: cobre ~40% de cima, em diagonal descendo para o bico
IRIS = ((200, 56, 24), (238, 118, 30))
ESCLERA = (253, 200, 60)            # amarelo da neutra (amostrado: (250,228,126))
PALPEBRA = (58, 24, 88)

def cor_cabeca(p, face):
    """Cabeça roxo-índigo escura; faixa de bochecha #8c55b8 sob o olho, nos lados."""
    x, y, z = p
    if face == "up": return tom(ROXO_ESC, .06)
    if face in ("east", "west") and OLHO_Y - OLHO_RV - 2.0 < y < OLHO_Y - OLHO_RV - 0.2 and z < -2.0: return P_VIOLETA
    return ROXO_ESC if y > 23.0 else mix(ROXO_ESC, ROXO_NOITE, .45)

def olho(u, v):
    """Olho da neutra: dourado (#fdb804) clareando para creme junto da íris, íris laranja-avermelhada puxada para o
    bico, pupila escura e brilho branco no alto perto do bico; o terço de cima fica sob a sobrancelha (corte reto
    inclinado descendo para o bico)."""
    uu = u - OLHO_U
    e = (uu / OLHO_RU) ** 2 + (v / OLHO_RV) ** 2
    if e > 1: return None
    corte = OLHO_ALTO + OLHO_BRAVO * (uu / OLHO_RU)
    if v / OLHO_RV > corte + 0.14: return PALPEBRA
    if v / OLHO_RV > corte: return (42, 20, 80)                 # sombra da sobrancelha logo acima do olho
    iu, iv = uu / OLHO_RU + 0.32, v / OLHO_RV + 0.12            # íris puxada para o bico
    di = (iu / 0.46) ** 2 + (iv / 0.66) ** 2
    if ((iu + 0.12) / 0.13) ** 2 + ((iv - 0.25) / 0.17) ** 2 <= 1: return (255, 255, 255)   # brilho
    if (iu / 0.2) ** 2 + (iv / 0.32) ** 2 <= 1: return (42, 14, 16)                         # pupila
    if di <= 1: return (208, 68, 26) if di < 0.6 else (176, 44, 20)                         # íris
    if e > 0.86: return (110, 52, 24)                                                       # contorno
    return mix(P_OURO, (253, 235, 193), clamp(1.1 - di * 0.55))                            # dourado -> creme

def mat_faceta(lado):
    base = mat_bloco(ROXO_ESC, faixas=False, borda=-.12)
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            cor = olho(z - FAC_C[1], y - OLHO_Y)
            if cor: return cor
            if OLHO_Y - OLHO_RV - 2.0 < y < OLHO_Y - OLHO_RV - 0.2: return P_VIOLETA        # bochecha
            if y < 23.0: return tom(mix(ROXO_ESC, ROXO_NOITE, .5), -.05)
        return base(c)
    return f

def brilho_olho(c, cor):
    return cor[0] > 200 and 120 < cor[1] < 240 and cor[2] < 200 and cor[0] - cor[2] > 50

def cor_bico(p, face):
    """Bico creme-rosado: topo #fcd8b9, frente (242,196,180), lados (224,170,160); narina #614749 no alto do lado."""
    x, y, z = p
    if face in ("east", "west") and abs(y - 25.6) < 0.28 and abs(z + 10.5) < 0.3: return P_MARROM
    if face == "up": return P_CREME
    if face == "down": return (214, 160, 150)
    if face == "north": return (244, 198, 182)
    return (232, 180, 168)

def cabeca_morcegalo():
    cab = []
    mc = mat_bloco(ROXO_ESC, faixas=False, borda=-.12)
    mcab = mat_cor(cor_cabeca, borda=.1, curva=.25)
    cab += g.arredondado2("cranio", [-LD_X, CAB_Y0, LD_Z - 0.1], [LD_X, CAB_Y1, 1.8], mcab, r=1.4, res=3)
    cab.append(peca("cara", [-FR_X, 21.4, FR_Z], [FR_X, 29.2, -6.0], mcab, faixa=(CAB_Y0, CAB_Y1), res=3))
    def msob_f(c):
        face = c["face"]
        if face == "up": return P_VIOLETA
        if face == "down": return (42, 20, 80)
        return tom(ROXO_ESC, -.08) if g.na_borda(c) else ROXO_ESC
    msob = msob_f
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 21.6, cz - FAC_L / 2], [cx + FAC_T / 2, 28.8, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, OLHO_Y, cz), res=8, brilho=brilho_olho))
        # sobrancelha brava: aba grossa por cima do olho, descendo para o bico
        ox = cx + (FAC_T / 2) * lado
        x0, x1 = sorted((ox - 0.4 * lado, ox + 1.1 * lado))
        yb = OLHO_Y + OLHO_ALTO * OLHO_RV - 0.1
        cab.append(osso("sobrancelha_" + s, [cx, yb, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s, [x0, yb, cz - FAC_L / 2 - 0.4], [x1, yb + 2.0, cz + FAC_L / 2 - 0.6], msob,
                 rot=(-22, 0, 0), pivo=(cx, yb, cz), res=4)]))
        # a sobrancelha continua pela frente, em V por cima do bico
        x0, x1 = sorted((0.0, 2.9 * lado))
        cab.append(peca("sobrancelha_fr_" + s, [x0, 26.3, FR_Z - 1.3], [x1, 28.3, FR_Z + 0.4], msob,
                        rot=(0, 0, 22 * lado), pivo=(2.9 * lado, 27.3, FR_Z), res=4))
    # bico de rapina curto: base larga (~1/3 da cabeça), meio mais estreito e o gancho na ponta curvando para baixo;
    # altura ~1/3 da cabeça (termina pouco abaixo dos olhos); avança ~1/4 da profundidade da cabeça
    mb = mat_cor(cor_bico, borda=.03, curva=.0, topo=.0, baixo=.0)
    fb = (23.0, 26.6)
    # 3 degraus que estreitam para baixo (de frente: triângulo) e avançam para a frente (de lado: gancho)
    cab.append(peca("bico_base", [-2.1, 24.6, FR_Z - 1.6], [2.1, 26.5, FR_Z + 0.3], mb, faixa=fb, res=4))
    cab.append(peca("bico_meio", [-1.4, 23.5, FR_Z - 2.5], [1.4, 25.6, FR_Z - 0.6], mb, faixa=fb, res=4))
    cab.append(peca("bico_gancho", [-0.7, 22.6, FR_Z - 3.1], [0.7, 24.4, FR_Z - 1.6], mb, rot=(-12, 0, 0),
                    pivo=(0, 24.4, FR_Z - 1.6), faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-1.0, 23.0, FR_Z - 1.4], [1.0, 23.8, FR_Z + 0.3], mat_bloco((222, 166, 156), borda=-.05), res=4))
    # testa em degrau (capacete) por cima do bico, entre as sobrancelhas
    cab.append(peca("testa", [-FR_X - 0.4, 26.6, FR_Z - 1.0], [FR_X + 0.4, 29.0, FR_Z + 0.4], msob, res=3))
    # boné: aba saliente na base do crânio, sobre o pescoço
    cab.append(peca("nuca_aba", [-LD_X + 0.6, 21.6, 0.6], [LD_X - 0.6, 22.6, 2.8], msob, res=3))
    # barbela: 2 lóbulos curtos e largos (cada um ~metade da largura do bico), arredondados, logo sob o bico,
    # terminando no topo do peito
    mbar = mat_cor(lambda p, f_: P_MAGENTA if p[1] > 21.6 else (194, 62, 147), borda=.08, curva=.15)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.05 * lado, 2.0 * lado))
        y0 = 20.6 if lado < 0 else 21.0
        cab += g.arredondado("barbela_" + s, [x0, y0, FR_Z - 1.5], [x1, 23.6, FR_Z + 0.1], mbar, r=0.5, faixa=(y0, 23.6), res=4)
    # crista: leque magenta grande entre as orelhas. De frente é uma torre de degraus (base ~4,4, topo ~2,4); de lado
    # nasce na testa, entre as sobrancelhas, e sobe em degraus para trás até a nuca (lateral da ficha: o mais alto
    # fica atrás, junto da orelha). Topo dos blocos rosa claro.
    crista = []
    def mcr_f(c):
        face = c["face"]
        if face == "up": return P_ROSA_CLARO
        if face == "down": return (168, 58, 120)
        cor = P_MAGENTA if face in ("north", "south") else (210, 72, 146)
        return tom(cor, -.12) if g.na_borda(c) else cor
    for k, (zc, y0, topo) in enumerate([(-9.6, 27.4, 30.6), (-7.6, 28.4, 31.8), (-6.2, 28.8, 32.8), (-4.8, 29.0, 33.6),
                                        (-3.3, 29.2, 34.0)]):
        crista.append(peca(f"crista{k}_a", [-2.1, y0, zc - 0.95], [2.1, topo - 1.5, zc + 0.95], mcr_f, res=3))
        crista.append(peca(f"crista{k}_b", [-1.2, topo - 1.55, zc - 0.75], [1.2, topo, zc + 0.85], mcr_f, res=3))
    cab.append(osso("crista", [0, 30.0, -4.0], [0, 0, 0], crista))
    # orelhas de morcego
    for lado in (-1, 1):
        cab.append(orelha(lado))
    return cab

# ---------------- orelhas ----------------
OR_A = (2.2, 29.4, -3.8)             # raiz da orelha (lado +x)
OR_GIRO = (2, -43, -2)                # giro da orelha (lado +x): de frente para fora e para a frente
OR_POLI = [(0.0, 0.0), (4.6, 5.2), (12.2, 9.4), (12.3, -1.4), (10.8, -3.8), (6.2, -3.8), (1.9, -2.4)]
OR_DENTRO = [(1.7, -0.2), (5.0, 3.8), (10.8, 6.8), (11.0, -1.1), (10.0, -2.8), (6.0, -2.8), (2.4, -1.8)]

def mat_orelha(lado):
    """Pele da orelha: rosa-magenta vivo (#d153ab) com degraus mais claros (#e888c8) para baixo e para fora;
    costas roxas maciças."""
    ax, ay, az = OR_A
    def f(c):
        x, y, z = c["p"]
        u, v = (x - ax * lado) * lado, y - ay
        if not dentro_poli(u, v, OR_POLI): return None
        if c["face"] == "south" or not dentro_poli(u, v, OR_DENTRO):
            return MOLDURA_ESC if c["face"] == "south" else MOLDURA_ESC
        t = clamp((u * 0.35 - v * 0.55 + 2.5) / 5.0)
        return (209, 83, 171) if t < 0.45 else (222, 108, 186) if t < 0.75 else P_ROSA_CLARO
    return f

MOLDURA_ESC = (90, 47, 146)        # borda da orelha (#5a2f92), topo (#8c55b8)

def mat_moldura(cor=ROXO_ESC):
    """Moldura grossa (orelha, asa): clara em cima, base nas faces largas, escura embaixo e nas quinas."""
    def f(c):
        face = c["face"]
        if face == "up": return P_VIOLETA
        l = -.4 if face == "down" else 0.0 if face in ("north", "south") else -.1
        if g.na_borda(c): l -= .15
        return tom(cor, l)
    return f

def orelha(lado):
    s = "d" if lado < 0 else "e"
    ax, ay, az = OR_A
    ax *= lado
    P = lambda u, v: (ax + u * lado, ay + v)
    pts = [P(u, v) for u, v in OR_POLI]
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    # pele rebaixada atrás da moldura (concha) e grossa
    filhos = [peca("orelha_pele_" + s, [min(xs), min(ys), az + 0.05], [max(xs), max(ys), az + 1.05], mat_orelha(lado), res=3)]
    mo = mat_moldura(MOLDURA_ESC)
    for nome, a, b, e in (("dentro", (0.3, 0.3), (4.7, 5.0), 2.0), ("dentro2", (4.6, 5.0), (12.0, 9.1), 2.0),
                          ("fora", (12.1, 9.1), (12.1, -1.5), 2.0), ("ponta", (12.1, -1.2), (10.5, -3.7), 1.8)):
        filhos.append(barra(f"orelha_{nome}_" + s, P(*a), P(*b), e, az - 1.0, az + 1.1, mo, estica=1.2))
    # costas da orelha com a beirada de baixo em escada
    filhos.append(peca("orelha_degrau_" + s, sorted([P(5.8, -3.8)[0], P(10.6, -3.8)[0]])[:1] + [ay - 4.6, az + 0.9],
                       sorted([P(5.8, -3.8)[0], P(10.6, -3.8)[0]])[1:] + [ay - 3.4, az + 1.6], mo))
    rx, ry, rz = OR_GIRO
    return osso("orelha_" + s, [ax, ay, az], [rx, ry * lado, rz * lado], filhos)

# ---------------- asas membranosas ----------------
WZ = 0.2
ASA_GIRO = 30
_k = 1 / math.cos(math.radians(ASA_GIRO))
def _u(x): return 7.6 + (x - 7.6) * _k        # posição no plano da asa a partir do x visto de frente
_W = (13.4, 26.8)                              # pulso (visto de frente), na altura da base das orelhas
def _dedo(ang, L): return (_W[0] + L * math.cos(math.radians(ang)), _W[1] - L * math.sin(math.radians(ang)))
_T2, _T3 = _dedo(58, 15.0), _dedo(75, 15.4)        # dedos em leque: ~30° (borda), 58° e 75° abaixo da horizontal
ASA = {"S": (7.6, 20.4), "W": (_u(_W[0]), _W[1]), "C": (_u(22.6), 23.2), "T1": (_u(24.8), 12.2),
       "N1": (_u(23.0), 17.2), "T2": (_u(_T2[0]), _T2[1]), "N2": (_u(19.2), 16.2), "T3": (_u(_T3[0]), _T3[1]),
       "N3": (_u(12.8), 15.0), "B": (_u(8.8), 11.6)}
A = ASA
ASA_POLI = [A["S"], A["W"], A["C"], A["T1"]] + curva(A["T1"], A["N1"], A["T2"]) + [A["T2"]] + \
           curva(A["T2"], A["N2"], A["T3"]) + [A["T3"]] + curva(A["T3"], A["N3"], A["B"]) + [A["B"]]
DEDOS = [(A["W"], A["C"], 1.6), (A["C"], A["T1"], 1.2), (A["W"], A["T2"], 0.9), (A["W"], A["T3"], 0.9), (A["S"], A["W"], 1.8)]

def mat_membrana(lado):
    """Membrana em degradê liso a partir dos ossos: violeta-rosa (#b352b9) junto do braço e dos dedos, magenta
    (#d75197) no meio e rosa claro (#e888c8) longe deles; só as pontas do recorte são creme (#fcd8b9)."""
    def f(c):
        x, y, z = c["p"]
        u = x * lado
        if not dentro_poli(u, y, ASA_POLI): return None
        for t in ("T1", "T2", "T3"):
            tx, ty = A[t]
            if y < ty + 1.9 and math.hypot(u - tx, y - ty) < 2.0: return P_CREME
        dd = min(dist_seg(u, y, a, b) - e / 2 for a, b, e in DEDOS)
        if dd < 0: return MOLDURA_ESC
        t = clamp(dd / 3.2)
        cor = P_VIOLETA_ROSA if t < 0.25 else P_MAGENTA if t < 0.6 else P_ROSA_CLARO
        if c["face"] == "south": cor = tom(cor, .1)
        return cor
    return f

def asa(lado):
    s = "d" if lado < 0 else "e"
    P = lambda k: (A[k][0] * lado, A[k][1])
    us = [p[0] for p in ASA_POLI]; ys = [p[1] for p in ASA_POLI]
    x0, x1 = sorted((min(us) * lado, max(us) * lado))
    filhos = [peca("membrana_" + s, [x0, min(ys), WZ - 0.25], [x1, max(ys), WZ + 0.25], mat_membrana(lado), res=3)]
    mo = mat_moldura(MOLDURA_ESC)
    filhos.append(barra("braco_" + s, P("S"), P("W"), 2.6, WZ - 1.1, WZ + 1.1, mo, estica=1.0))
    filhos.append(barra("antebraco_" + s, P("W"), P("C"), 1.8, WZ - 0.85, WZ + 0.85, mo, estica=1.2))
    filhos.append(barra("dedo_fora_" + s, P("C"), P("T1"), 1.4, WZ - 0.7, WZ + 0.7, mo, estica=0.4))
    filhos.append(barra("dedo_meio_" + s, P("W"), P("T2"), 1.0, WZ - 0.5, WZ + 0.5, mo))
    filhos.append(barra("dedo_dentro_" + s, P("W"), P("T3"), 1.0, WZ - 0.5, WZ + 0.5, mo))
    wx, wy = P("W")
    filhos.append(peca("pulso_" + s, [wx - 1.4, wy - 1.4, WZ - 1.15], [wx + 1.4, wy + 1.4, WZ + 1.15], mo))
    cx, cy = P("C")
    filhos.append(peca("cotovelo_" + s, [cx - 1.0, cy - 1.0, WZ - 0.9], [cx + 1.0, cy + 1.0, WZ + 0.9], mo))
    sx, sy = P("S")
    return osso("asa_" + s, [sx, sy, WZ], [0, -ASA_GIRO * lado, 0], filhos)

# ---------------- corpo ----------------
def cor_tronco(p, face):
    x, y, z = p
    if y > 17.5: return ROXO
    if y > 11.0: return ROXO_ESC
    return mix(ROXO_ESC, ROXO_NOITE, .5)

def pena_fileira(nome, x, yt, z, W, H, T, giro, cor, ponta, incl=8, ponta2=None):
    """Pena larga de uma fileira: bloco roxo-escuro inclinado (telha) e 2 pontas em V embaixo (quadrados girados 45°),
    violeta (#8c55b8); 'ponta2' troca a cor da 2ª ponta (lilás nos flancos)."""
    mb = mat_bloco(cor, cima=.18, so_baixo=True, borda=-.1)
    filhos = [peca(nome, [x - W / 2, yt - H, z - T / 2], [x + W / 2, yt, z + T / 2], mb)]
    q = W * 0.36
    for i, dx in enumerate((-W / 4, W / 4)):
        md = mat_bloco(ponta2 if (i == 1 and ponta2) else ponta, cima=.18, borda=-.08)
        filhos.append(peca(f"{nome}_v{i}", [x + dx - q / 2, yt - H - q / 2, z - T / 2 + 0.12], [x + dx + q / 2, yt - H + q / 2, z + T / 2 - 0.12],
                           md, rot=(0, 0, 45), pivo=(x + dx, yt - H, z)))
    return osso(nome, [x, yt, z], [incl, giro, 0], filhos)

# fileiras de penas em volta do corpo: (y do alto, raio x, raio z, centro z, cor da base, phis)
FILEIRAS = [
    (22.0, 7.8, 6.2, -0.8, INDIGO_2, [-34, 2, 38, 74]),
    (19.2, 8.7, 6.9, -0.6, INDIGO, [-42, -10, 22, 56]),
    (16.4, 9.2, 7.3, -0.4, INDIGO_2, [-34, 2, 38, 74]),
    (13.6, 9.4, 7.4, -0.3, INDIGO, [-42, -10, 22, 56]),
    (10.8, 9.2, 7.3, -0.3, INDIGO_2, [-62, -26, 10, 46]),
]

# peitoral: escudo em V de chevrons (y do alto, x das placas, largura, z da frente)
PEITO = [            # na frente da ficha o escudo é largo (~±6) até y~15 e a ponta do V chega perto de y 8
    (19.8, [0.0, 3.3], 3.6, -9.7),       # sem placa de fora no alto: de lado ela virava 'lasca' no pescoço
    (17.6, [1.6, 4.7], 3.4, -9.6),
    (15.4, [0.0, 3.1, 5.6], 3.3, -9.4),
    (13.2, [1.5, 4.2], 3.2, -9.1),
    (11.4, [0.0], 3.2, -8.7),
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
    mt = mat_cor(cor_tronco, borda=.1, curva=.3)
    corpo += g.arredondado2("tronco", [-8.6, 7.0, -7.6], [8.6, 21.8, 6.6], mt, r=3.0)
    corpo += g.arredondado("peito_base", [-6.6, 11.0, -8.6], [6.6, 22.6, -2.0], mt, r=1.6)

    # ---------- plumagem: penas em camadas (telhas inclinadas), fileiras desencontradas em meio bloco, cada pena com
    # a ponta em V violeta; 1 em cada 3 pontas lilás nos flancos; embaixo as pontas fazem a saia sobre as coxas ----
    plum = []
    n = 0
    for r, (yt, ax, az, zc, cor, phis) in enumerate(FILEIRAS):
        for k, phi in enumerate(phis + [90]):
            for lado in ((1,) if phi == 90 else (-1, 1)):
                x, z = anel_q(ax, az, zc, phi, lado)
                base, ponta = cor, P_VIOLETA
                if phi >= 50 and r < 3:                     # sela das costas: tabuleiro lavanda / roxo escuro
                    base, ponta = (P_LAVANDA, P_LILAS) if (k + r) % 2 == 0 else (INDIGO_2, P_VIOLETA)
                n += 1
                plum.append(pena_fileira(f"pena{r}{k}_{'d' if lado < 0 else 'e'}", x, yt, z, 6.0, 2.9, 1.6,
                                         -(phi + 90) * lado, base, ponta, ponta2=P_LILAS if n % 3 == 0 else None))
    corpo.append(osso("plumagem", [0, 14, 0], [0, 0, 0], plum))

    # ---------- gola de penas do pescoço (hackle): pontas violeta e lilás entre a cabeça e o peito ----------
    gola = []
    for k, phi in enumerate([-28, 4, 36, 68, 90]):
        for lado in ((1,) if phi == 90 else (-1, 1)):
            x, z = anel_q(6.6, 5.6, -3.0, phi, lado)
            gola.append(pena_fileira(f"gola{k}_{'d' if lado < 0 else 'e'}", x, 23.6, z, 4.4, 2.2, 1.3,
                                     -(phi + 90) * lado, ROXO_ESC, P_VIOLETA, incl=6, ponta2=P_LILAS))
    corpo.append(osso("gola", [0, 22, -3], [0, 0, 0], gola))

    # ---------- peitoral sombrio: 4 fileiras de escamas em chevron, cada uma mais estreita e um pouco à frente da de
    # cima, com a beirada de baixo em dente de serra; lilás muito claro, topo mais claro, fio lilás embaixo ----------
    def mat_peito(cor):
        def f(c):
            face = c["face"]
            if face == "up": return P_LAV_TOPO
            if face == "down": return P_LILAS
            if face in ("east", "west"): return mix(cor, P_LILAS, .5)
            return P_LILAS if c["j"] >= c["th"] - 1 else cor
        return f
    peito = []
    RP = 9.5
    for t, (yt, hw, zf) in enumerate([(20.2, 6.8, -10.3), (18.0, 5.4, -10.6), (15.8, 4.0, -10.8), (13.6, 2.4, -10.8)]):
        nseg = 3 if hw > 4 else 1
        larg = 2 * hw / nseg
        for k in range(nseg):
            xc = -hw + larg * (k + 0.5)
            ang = math.degrees(math.asin(clamp(xc / RP, -0.6, 0.6)))
            z = zf + RP - math.sqrt(max(RP * RP - xc * xc, 0))
            cor = P_LAVANDA if k == 1 or nseg == 1 else mix(P_LAVANDA, P_LILAS, .35)   # bordas um pouco mais lilás
            m = mat_peito(cor)
            filhos = [peca(f"peito{t}{k}", [xc - larg / 2, yt - 2.4, z], [xc + larg / 2, yt, z + 1.3], m)]
            ndentes = max(1, round(larg / 3.0))
            for d in range(ndentes):
                xd = xc - larg / 2 + larg * (d + 0.5) / ndentes
                q = min(2.1, larg / ndentes * 0.72)
                filhos.append(peca(f"peito{t}{k}_v{d}", [xd - q / 2, yt - 2.4 - q / 2, z + 0.1], [xd + q / 2, yt - 2.4 + q / 2, z + 1.2],
                                   m, rot=(0, 0, 45), pivo=(xd, yt - 2.4, z + 0.65)))
            peito.append(osso(f"peito{t}{k}", [xc, yt, z], [6, -ang, 0], filhos))
    corpo.append(osso("peitoral", [0, 16, -8], [0, 0, 0], peito))

    # ---------- asas ----------
    corpo.append(asa(-1)); corpo.append(asa(1))

    # ---------- cauda: 6 penas-foice em leque; gradiente da ficha: roxo vivo -> violeta -> lilás -> creme-rosado ----------
    cauda = []
    # grossas como na ficha (crescentes de ~5 de altura de lado) e afinando só no fim até a ponta fina
    SEGS = [(5.4, 3.0, 5.6, P_VIOLETA, P_VIOLETA), (5.2, 2.8, 6.2, P_VIOLETA, P_VIOLETA_ROSA),
            (4.6, 2.4, 5.6, P_VIOLETA_ROSA, P_LAVANDA), (4.0, 2.0, 4.4, P_LAVANDA, (250, 182, 182)),
            (3.0, 1.3, 2.4, (250, 182, 182), P_CREME)]          # crescente: mais grossa no meio
    SEGS_BAIXO = [(5.4, 3.0, 5.6, ROXO, P_VIOLETA), (5.2, 2.8, 6.2, P_VIOLETA, P_VIOLETA),
                  (4.6, 2.4, 5.6, P_VIOLETA, P_VIOLETA_ROSA), (4.0, 2.0, 4.4, P_VIOLETA_ROSA, P_LAVANDA),
                  (3.0, 1.3, 2.4, P_LAVANDA, (250, 182, 182))]
    def pena_cauda(nome, x, y, z, rot0, cv, esc=1.0, baixo=False):
        segs = [(L * esc, w, h, c0, c1) for L, w, h, c0, c1 in (SEGS_BAIXO if baixo else SEGS)]
        return pena_foice(nome, (x, y, z), segs, rot0, (cv * 0.6, cv * 0.9, cv * 1.2, cv * 1.5))
    # leque do meio (x = 0): sobem, arqueiam para trás e caem; as de cima são as mais compridas
    for k, (y, rx, cv, esc) in enumerate([(19.6, -36, 14, 0.92), (17.2, -18, 14, 1.0), (14.8, -6, 14, 0.92),
                                          (13.2, -10, 12, 0.58)]):
        cauda.append(pena_cauda(f"rabo{k}", 0.0, y, 6.0, (rx, 0, 0), cv, esc, baixo=k >= 3))
    # dois pares dos lados, embaixo, abrindo para fora (de costas o leque desce em diagonal)
    for k, (x, y, rx, ry, cv, esc) in enumerate([(2.4, 16.0, -12, 14, 14, 0.8), (2.6, 13.8, -2, 24, 12, 0.6)]):
        for lado in (-1, 1):
            cauda.append(pena_cauda(f"rabo{5 + k}_{'d' if lado < 0 else 'e'}", x * lado, y, 5.8,
                                    (rx, ry * lado, 0), cv, esc, baixo=True))
    corpo.append(osso("cauda", [0, 16.0, 5.6], [0, 0, 0], cauda))

    corpo.append(pescoco)
    tronco = osso("corpo", [0, 11.0, 0], [0, 0, 0], corpo)

    # ---------- pernas: canela creme grossa, pé de 3 dedos com garras escuras + 1 atrás ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 5.4 * lado; zc = -0.6
        pp = []
        pp.append(pena_fileira("calca_" + s, xc, 9.6, zc - 1.6, 4.8, 2.8, 1.4, 0, ROXO_ESC, P_VIOLETA, incl=4))
        pp.append(peca("coxa_" + s, [xc - 2.2, 6.4, zc - 1.8], [xc + 2.2, 9.5, zc + 2.2], mat_bloco(ROXO_ESC)))
        mcan = mat_bloco(CANELA, borda=-.12)
        pp += g.octogono("canela_" + s, [xc - 2.0, 2.0, zc - 2.0], [xc + 2.0, 7.2, zc + 2.0], mcan, r=0.6)
        pp.append(peca("pe_" + s, [xc - 2.5, 0.0, zc - 2.6], [xc + 2.5, 2.8, zc + 1.8], mcan))
        mdedo = mat_bloco(CANELA, borda=-.15)
        mgar = mat_bloco(GARRA, cima=.3, borda=-.15)
        for nome, giro, dx in (("meio", 0, 0), ("fora", -30 * lado, 3.8 * lado), ("dentro", 14 * lado, -2.8 * lado)):
            x0, z0 = xc + dx * 0.7, zc - 1.8
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - 1.2, 0, z0 - 3.0], [x0 + 1.2, 2.6, z0 + 0.4], mdedo),
                peca(f"garra_{nome}_{s}", [x0 - 0.95, 0, z0 - 5.0], [x0 + 0.95, 2.3, z0 - 2.9], mgar)]))
        pp.append(peca("dedo_tras_" + s, [xc - 0.8, 0, zc + 1.4], [xc + 0.8, 1.8, zc + 3.4], mdedo))
        pp.append(peca("garra_tras_" + s, [xc - 0.7, 0, zc + 3.3], [xc + 0.7, 1.7, zc + 4.6], mgar))
        return osso("perna_" + s, [xc, 9.0, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
