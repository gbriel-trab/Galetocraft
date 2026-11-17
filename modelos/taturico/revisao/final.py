"""Taturico (#007, Terra): o galo-tatu das rochas, robusto e defensivo, coberto por uma carapaça de faixas.

Como cada elemento da ficha foi resolvido:
- CARAPAÇA DE FAIXAS: cada faixa é um ARCO de placas giradas (polilinha arredondada sobre o dorso), pintado em
  xadrez bege/marrom e com a beirada de trás clara; as faixas se sobrepõem em degrau e inclinam para trás.
- ELMO ROCHOSO: aba em V bravo sobre os olhos + duas faixas arredondadas em xadrez no alto da cabeça; placa da
  bochecha com o glifo de espiral quadrada.
- ROSTO: frente creme estreita + faces diagonais (45°) com o olho amarelo inteiro numa face plana (como o Pirococó).
- CARAPAÇA DO OMBRO: placa grande no lado da asa com a espiral quadrada (glifo), sobre faixas de asa em xadrez.
- CAUDA BLINDADA: cone de anéis octogonais encaixados, cada um menor e mais baixo (osso por anel, ondula).
- PATAS FORTES: coluna amarela grossa, dedos amarelos e garras cinza-escuras em bloco chanfrado.
"""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, mat_cor, arredondado, arredondado2, pintar_olho, na_borda

ID = "taturico"; NOME = "Taturico"; NUMERO = 7
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 26, -13), 10)
ONDAS = [("cauda_anel", 5, (1.2, 2.5, 0))]
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (Paleta de Cores da ficha) ----------------
CREME = (250, 218, 178); CREME_SOM = (224, 180, 140)
BEGE = (238, 160, 94)            # bege-laranja das faixas
BEGE_CL = (250, 196, 136)
CARAMELO = (205, 118, 64)
MARROM = (158, 90, 74)           # marrom arroxeado das faixas
MARROM_ESC = (96, 52, 44)
VERM = (212, 36, 32); VERM_ESC = (156, 20, 24); VERM_CL = (240, 76, 60)
AMARELO = (252, 174, 20); AMARELO_CL = (255, 212, 84); AMARELO_ESC = (214, 124, 8)
CINZA = (98, 78, 88); CINZA_CL = (132, 112, 122); CINZA_ESC = (70, 56, 64)
PRETO = (24, 12, 14)

# ---------------- utilidades ----------------
def grao(p, passo=0.5):
    """Ruído fixo por 'voxel' (passo em unidades): -1..1. Dá o granulado de pedra/couro do estilo voxel."""
    a = (int(math.floor(p[0] / passo)) * 73856093) ^ (int(math.floor(p[1] / passo)) * 19349663) ^ (int(math.floor(p[2] / passo)) * 83492791)
    return ((a & 0xffff) / 0xffff) * 2 - 1

def lado_s(lado): return "d" if lado < 0 else "e"

# ---------------- glifo: espiral quadrada ----------------
ESPIRAL = ["#######",
           "#.....#",
           "#.###.#",
           "#.#.#.#",
           "#.#...#",
           "#.#####",
           "#......"]

def glifo(c, bitmap, margem=0.16, espelha=False):
    """Posição do pixel na face (pelo i, j da textura) -> 'borda' (moldura da placa), 'traco' ou 'fundo'."""
    u = (c["i"] + .5) / c["tw"]; v = (c["j"] + .5) / c["th"]
    if espelha: u = 1 - u
    if min(u, v, 1 - u, 1 - v) < margem * 0.45: return "borda"
    a = (u - margem) / (1 - 2 * margem); b = (v - margem) / (1 - 2 * margem)
    if not (0 <= a < 1 and 0 <= b < 1): return "fundo"
    n = len(bitmap)
    return "traco" if bitmap[int(b * n)][int(a * n)] == "#" else "fundo"

# ---------------- materiais ----------------
def mat_faixa(k, m, z0, z1, alt, ncel=2):
    """Bloco de uma faixa da carapaça: xadrez bege/marrom (célula pelo índice m do bloco no arco e pela posição
    em z), beirada de trás (sul) clara, frente escura; 'alt' (0 embaixo .. 1 no alto) dá a luz de cima."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        cz = min(ncel - 1, max(0, int((z - z0) / ((z1 - z0) / ncel))))
        claro = (m + cz + k) % 2 == 0
        base = BEGE if claro else MARROM
        if face == "south": base = BEGE_CL if claro else mix(BEGE, MARROM, .25)     # beirada clara: faixas listradas de trás
        luz = {"up": .10, "south": .04, "north": -.3, "down": -.45}.get(face, -.15)
        luz += -0.22 + 0.3 * alt + 0.05 * grao(c["p"])
        if na_borda(c): luz -= .2
        return tom(base, luz)
    return f

def mat_casco(cel=3.0, fase=0, eixos=(2, 1), aba="south", org=None):
    """Bloco de casco em xadrez 3D (células de 'cel' unidades nos 2 eixos dados), beirada 'aba' clara."""
    def f(c):
        p = c["p"]; face = c["face"]; b0 = org or c["b"][0]
        a = int(math.floor((p[eixos[0]] - b0[eixos[0]]) / cel + 1e-6))
        b = int(math.floor((p[eixos[1]] - b0[eixos[1]]) / cel + 1e-6))
        claro = (a + b + fase) % 2 == 0
        base = BEGE if claro else MARROM
        if face == aba: base = BEGE_CL if claro else mix(MARROM, BEGE, .3)
        y0, y1 = c["faixa"]
        t = clamp((p[1] - y0) / max(y1 - y0, 1e-6))
        luz = -0.25 + 0.35 * t + {"up": .12, "down": -.4}.get(face, 0) + 0.05 * grao(p)
        if na_borda(c): luz -= .2
        return tom(base, luz)
    return f

def mat_placa_glifo(face_glifo, espelha=False, fundo=MARROM, traco=BEGE, borda=MARROM_ESC):
    """Placa com a espiral quadrada na face 'face_glifo'; o resto da placa é marrom com quinas escuras."""
    def f(c):
        face = c["face"]
        if face == face_glifo:
            r = glifo(c, ESPIRAL, espelha=espelha)
            v = (c["j"] + .5) / c["th"]
            base = {"borda": borda, "traco": traco, "fundo": fundo}[r]
            return tom(base, 0.08 - 0.22 * v + 0.04 * grao(c["p"], 0.6))
        return lado_(c)
    lado_ = mat_casco(cel=2.6, fase=1, eixos=(2, 1))
    return f

def mat_creme(c0=CREME, c1=CREME_SOM, **kw):
    return mat_cor(lambda p, f: mix(c0, c1, .2 + .1 * grao(p, 0.6)), **kw)

def cor_penas_peito(y_base, larg=1.6):
    """Penas do peito: creme com tiras verticais (pontas de pena) na barra de baixo de cada fileira."""
    def f(p, face):
        x, y, z = p
        base = mix(CREME, CREME_SOM, .12 + .08 * grao(p, 0.6))
        if y < y_base + 1.8:
            tira = int(math.floor(x / larg)) % 2
            base = mix(base, CREME_SOM, .75 if tira else .15)
            if y < y_base + 0.4 + 0.5 * tira: base = mix(base, CARAMELO, .4)
        return base
    return f

# ---------------- carapaça de faixas ----------------
ARCO = [(0.0, 0.0), (0.33, -0.025), (0.61, -0.1), (0.82, -0.24), (0.95, -0.43), (1.01, -0.68), (1.03, -1.0)]

def faixa(nome, k, zc, ytopo, W, H, L, inclina, T=2.6, ncel=2, arco=ARCO):
    """Uma faixa da carapaça: arco de placas giradas (topo + 5 de cada lado) em volta do dorso, centrado em z = zc,
    com o alto em y = ytopo, meia largura W e altura H; o osso inclina a faixa 'inclina' graus (para trás)."""
    pts = [(W * a, ytopo + H * b) for a, b in arco]
    segs = [((-pts[1][0], pts[1][1]), pts[1], 0)]
    for i in range(1, len(pts) - 1):
        (xa, ya), (xb, yb) = pts[i], pts[i + 1]
        segs.append(((xa, ya), (xb, yb), i))
        segs.append(((-xb, yb), (-xa, ya), -i))
    filhos = []
    n = len(pts) - 1
    for (xa, ya), (xb, yb), m in segs:
        dx, dy = xb - xa, yb - ya
        comp = math.hypot(dx, dy) + (0.05 if m == 0 else 0.3)
        ang = math.degrees(math.atan2(dy, dx))
        mx, my = (xa + xb) / 2, (ya + yb) / 2
        e = 0.03 * (abs(m) % 2)                       # afasta as beiradas vizinhas (sem z-fighting)
        z0, z1 = zc - L / 2 - e, zc + L / 2 + e
        alt = 1 - abs(m) / n
        filhos.append(peca(f"{nome}_{m:+d}", [mx - comp / 2, my - T, z0], [mx + comp / 2, my, z1],
                           mat_faixa(k, m, z0, z1, alt, ncel), rot=(0, 0, ang), pivo=(mx, my, zc), res=2))
    return osso(nome, [0, ytopo, zc - L / 2], [inclina, 0, 0], filhos)

def anel_cauda(nome, k, z0, yc, R, Ry, L, chanfro=0.32):
    """Anel da cauda (prisma de 8 lados ao longo de z): 2 blocos em cruz pintados em xadrez pelo ângulo."""
    r = R * chanfro
    def mat(c):
        x, y, z = c["p"]; face = c["face"]
        a = math.atan2(y - yc, x)
        setor = int(math.floor((a + math.pi) / (2 * math.pi) * 8 + 0.5)) % 8
        claro = (setor + k) % 2 == 0
        base = BEGE if claro else MARROM
        if face == "south": base = BEGE_CL if claro else BEGE            # beirada de trás clara (listras na vista de trás)
        t = clamp((y - (yc - Ry)) / (2 * Ry))
        luz = -0.28 + 0.38 * t + {"up": .12, "down": -.35, "north": -.3}.get(face, 0) + 0.05 * grao(c["p"])
        if na_borda(c): luz -= .2
        return tom(base, luz)
    return [peca(nome + "_a", [-R + r, yc - Ry, z0], [R - r, yc + Ry, z0 + L], mat, res=2),
            peca(nome + "_b", [-R, yc - Ry + r, z0 + 0.04], [R, yc + Ry - r, z0 + L - 0.04], mat, res=2)]

def cauda_blindada():
    """Cone de anéis encaixados com a barriga quase reta (perto de y = 7) e o dorso descendo em degraus: cada anel é
    um osso (cauda_anel_k) filho do anterior, para a cauda ondular."""
    ANEIS = [(7.2, 7.2, 4.6), (6.0, 5.8, 4.2), (4.7, 4.4, 4.0), (3.4, 3.1, 3.6), (2.2, 2.0, 3.2)]   # (raio x, raio y, comprimento)
    Y0, PASSO, INCL = 15.4, 3.0, 12
    def seg(k, z0):
        R, Ry, L = ANEIS[k]
        yc = Y0 - (ANEIS[0][1] - Ry) * 0.8     # o eixo baixa um pouco: a barriga da cauda fica mais reta
        filhos = anel_cauda(f"cauda_anel{k}", k, z0, yc, R, Ry, L)
        if k + 1 < len(ANEIS): filhos.append(seg(k + 1, z0 + PASSO))
        else:   # ponta: bico bege
            filhos.append(peca("cauda_ponta", [-0.9, yc - 0.8, z0 + L - 0.4], [0.9, yc + 0.8, z0 + L + 1.4],
                               mat_cor(lambda p, f: BEGE_CL, borda=.2)))
        return osso(f"cauda_anel_{k}", [0, yc, z0], [INCL if k == 0 else 1, 0, 0], filhos)
    return osso("cauda", [0, Y0, 11.5], [0, 0, 0], [seg(0, 11.5)])

# ---------------- cabeça ----------------
FACE_Z = -14.6           # plano da frente do rosto
FX = 3.4                 # meia largura da frente estreita
FAC_T = 2.0              # espessura da face diagonal
FAC_L = FX * 0 + 5.4     # comprimento da face diagonal (45°)
OLHO_Y = 25.8
K_CAB, K_CAB_C, K_CAB_SOBE = 1.12, (0.0, 20.5, -9.0), -0.6   # escala da cabeça inteira

def faceta_centro(lado):
    """Centro (x, z) da peça da face diagonal: a face de fora passa pelo meio da diagonal do rosto."""
    mx, mz = (FX + FAC_L * 0.7071 / 2), FACE_Z + FAC_L * 0.7071 / 2
    return lado * (mx - 0.7071 * FAC_T / 2), mz + 0.7071 * FAC_T / 2

def mat_faceta(lado):
    """Face diagonal do rosto: creme, com o olho inteiro na face de fora (amarelo, pupila preta, pálpebra marrom)."""
    base = mat_creme(c0=mix(CREME, (255, 238, 210), .5), c1=CREME, borda=.03, curva=.2)
    fora = "east" if lado > 0 else "west"
    cx, cz = faceta_centro(lado)
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u, v = z - cz, y - OLHO_Y
            if (u / 1.62) ** 2 + (v / 1.42) ** 2 <= 1 and not (u / 1.38) ** 2 + (v / 1.2) ** 2 <= 1 and v / 1.2 < 0.5 - 0.3 * u / 1.38:
                return tom(MARROM, -0.25)                        # contorno (pálpebra) marrom
            cor = pintar_olho(u, v, 1.38, 1.2, iris=((196, 104, 0), (255, 200, 36)), esclera=(250, 242, 226),
                              r_iris=(0.8, 0.92), c_iris=(-0.14, -0.06), r_pup=(0.4, 0.48), bravo=0.3, alto=0.5)
            if cor is not None: return cor
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face in ("east", "west") and abs(z + 16.7) < 0.4 and abs(y - 25.6) < 0.4: return (110, 50, 10)   # narina
    if face == "down": return AMARELO_ESC
    if face in ("east", "west") and 23.0 < y < 23.35: return (150, 70, 6)                                # linha da boca
    return mix(AMARELO_CL, AMARELO, clamp((26.6 - y) / 2.2) * .8 + clamp((-z - 16) / 4) * .4)

def montar():
    # ======================= CABEÇA =======================
    i_cab = len(g.PECAS)
    cab = []
    mcreme = mat_creme(borda=.05, curva=.3)
    fx = (19.6, 28.4)
    cab.append(peca("rosto_frente", [-FX, 19.6, FACE_Z], [FX, 27.8, -10.0], mcreme, faixa=fx, res=4))
    for lado in (-1, 1):
        cx, cz = faceta_centro(lado)
        cab.append(peca("rosto_faceta_" + lado_s(lado), [cx - FAC_T / 2, 19.6, cz - FAC_L / 2], [cx + FAC_T / 2, 27.8, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, 24.0, cz), faixa=fx, res=8))
    cab += arredondado("cranio", [-7.0, 19.4, -11.6], [7.0, 31.6, -1.0], mat_cor(lambda p, f: CREME if p[2] < -8.6 else mix(MARROM, CREME, .2)), r=1.2, faixa=fx)

    # bico em cunha: base, meio e gancho; bico de baixo mais escuro
    mb = mat_cor(cor_bico, borda=.06, curva=.3)
    fb = (21.4, 26.8)
    cab.append(peca("bico_base", [-2.8, 23.0, -17.4], [2.8, 27.2, FACE_Z + 0.3], mb, faixa=fb, res=4))
    cab.append(peca("bico_meio", [-2.3, 22.6, -19.6], [2.3, 26.4, -17.2], mb, rot=(-10, 0, 0), pivo=(0, 26.4, -17.2), faixa=fb, res=4))
    cab.append(peca("bico_gancho", [-1.6, 21.4, -20.9], [1.6, 24.8, -19.2], mb, rot=(-22, 0, 0), pivo=(0, 24.8, -19.2), faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-2.1, 21.4, -17.8], [1.9, 23.25, FACE_Z + 0.3], mat_cor(lambda p, f: mix(AMARELO, AMARELO_ESC, .6), borda=.12), res=4))

    # barbela vermelha: dois lóbulos abrindo em V embaixo do bico
    mv_ = mat_cor(lambda p, f: mix(VERM_CL, VERM, clamp((21.5 - p[1]) / 2.5)), borda=.1, curva=.5)
    cab.append(peca("barbela_meio", [-2.2, 20.0, -16.6], [2.2, 22.4, -14.4], mv_, faixa=(15, 22)))
    for lado in (-1, 1):   # dois lóbulos cheios pendurados, abrindo de leve
        x0, x1 = sorted((0.15 * lado, 3.3 * lado))
        cab += [osso("barbela_" + lado_s(lado), [0.4 * lado, 22.0, -15.5], [0, 0, 6 * lado],
                     arredondado("barbela_" + lado_s(lado), [x0, 16.6, -16.8], [x1, 22.0, -14.2], mv_, r=0.5, faixa=(15, 22)))]

    # elmo rochoso: aba em V bravo + duas faixas arredondadas em xadrez
    for lado in (-1, 1):
        x0, x1 = sorted((0.0, 8.8 * lado))
        cab.append(peca("elmo_aba_" + lado_s(lado), [x0, 26.4, -17.0], [x1, 30.4, -11.0], mat_casco(cel=2.9, fase=0 if lado > 0 else 1, eixos=(0, 2), aba="north"),
                        rot=(0, 0, 14 * lado), pivo=(0, 26.4, -14.0), faixa=(26, 34), res=2))
    cab.append(faixa("elmo1", 1, -10.0, 33.2, 8.6, 6.8, 6.8, -6))
    cab.append(faixa("elmo2", 0, -4.2, 33.8, 9.2, 7.4, 7.0, 4))

    # placa da bochecha com a espiral quadrada (glifo), girada para a frente
    for lado in (-1, 1):
        cx, cz = 8.7 * lado, -7.6
        fora = "east" if lado > 0 else "west"
        cab.append(peca("bochecha_" + lado_s(lado), [cx - 1.7, 19.4, cz - 3.9], [cx + 1.7, 27.8, cz + 3.9],
                        mat_placa_glifo(fora, espelha=lado < 0), rot=(0, 28 * lado, 0), pivo=(cx, 24.4, cz), res=6))

    # crista vermelha em blocos: três lâminas no meio + duas abas laterais (cruz vista de frente)
    mcr = mat_cor(lambda p, f: mix(VERM_CL, VERM, clamp((37 - p[1]) / 6)) if f != "down" else VERM_ESC, borda=.12, curva=.5)
    crista = [
        peca("crista_tras", [-1.8, 31.0, -6.8], [1.8, 37.0, -1.0], mcr, rot=(-8, 0, 0), pivo=(0, 31.0, -4.0), faixa=(30, 39)),
        peca("crista_topo", [-1.8, 32.0, -12.2], [1.8, 39.0, -6.4], mcr, faixa=(30, 39)),
        peca("crista_frente", [-1.8, 31.0, -17.6], [1.8, 35.4, -11.8], mcr, rot=(-24, 0, 0), pivo=(0, 33.0, -11.8), faixa=(30, 39)),
    ]
    for lado in (-1, 1):
        x0, x1 = sorted((1.7 * lado, 4.8 * lado))
        crista.append(peca("crista_aba_" + lado_s(lado), [x0, 32.0, -10.0], [x1, 36.4, -4.4], mcr, faixa=(30, 39)))
    cab.append(osso("crista", [0, 32.0, -6.0], [0, 0, 0], crista))

    cabeca = osso("cabeca", [0, 21.0, -8.0], [0, 0, 0], cab)
    g.transformar(i_cab, [cabeca], K_CAB_C, k=K_CAB, sobe=K_CAB_SOBE)   # cabeça grande, como na ficha
    pescoco = osso("pescoco", [0, 19.0, -6.0], [0, 0, 0], [
        peca("pescoco", [-6.6, 15.0, -12.0], [6.6, 27.0, -1.0], mat_cor(lambda p, f: mix(CREME, CREME_SOM, .35), borda=.03, curva=.3), faixa=(7, 27)),
        cabeca])

    # ======================= CORPO =======================
    corpo = []
    casco = mat_casco(cel=2.8, fase=0, eixos=(0, 1), org=(0, 0, 0))
    creme = mat_cor(lambda p, f: CREME_SOM)
    sombra = mat_cor(lambda p, f: CREME, borda=0, curva=.3)            # mesma cor do lado do rosto: some junto dele
    def mat_tronco(c):
        if c["p"][2] < -5: return creme(c) if c["p"][1] < 20.5 else sombra(c)   # acima do peito: cor do rosto, sem contorno (não lê como fatia solta)
        return casco(c)
    corpo += arredondado2("tronco", [-10.4, 7.6, -9.0], [10.4, 26.0, 13.0], mat_tronco, r=3.0)   # frente recuada: não aparece como fatia ao lado do rosto
    # peito creme: massa arredondada + 2 fileiras de penas sobrepostas (beirada de baixo com pontas de pena)
    corpo += arredondado2("peito", [-8.6, 7.8, -13.0], [8.6, 20.0, -5.0], mat_cor(cor_penas_peito(7.8), borda=.02, curva=.3), r=2.0, faixa=(7, 21))
    for k, (y0, y1, z0, w) in enumerate([(15.0, 20.4, -14.6, 8.2), (10.8, 15.8, -13.8, 8.4)]):
        corpo += arredondado(f"peito{k}", [-w, y0, z0], [w, y1, z0 + 3.0], mat_cor(cor_penas_peito(y0), borda=.02, curva=.3), r=0.9, faixa=(7, 21))
    # carapaça do dorso: faixas da nuca até a garupa
    FAIXAS = [  # (zc, y do alto, meia largura, altura, comprimento, inclinação)
        (2.2, 32.2, 11.0, 16.0, 6.6, 4),
        (6.4, 31.4, 12.6, 21.0, 6.6, 12),
        (10.4, 29.4, 12.8, 20.0, 6.4, 24),
        (13.8, 26.4, 12.0, 17.0, 6.0, 38),
    ]
    for k, (zc, yt, W, H, L, inc) in enumerate(FAIXAS):
        corpo.append(faixa(f"faixa{k}", k, zc, yt, W, H, L, inc))

    # asas: faixas de asa em xadrez sob a grande placa do ombro com a espiral
    for lado in (-1, 1):
        s = lado_s(lado)
        asa = []
        x0, x1 = sorted((9.6 * lado, 12.4 * lado))
        for k, (z0, z1, y0, y1, xi, xo) in enumerate([(4.6, 10.2, 7.8, 19.0, 10.8, 13.4), (8.6, 13.6, 7.6, 17.0, 10.0, 12.6)]):
            a0, a1 = sorted((xi * lado, xo * lado))
            asa.append(peca(f"asa_faixa{k}_{s}", [a0, y0, z0], [a1, y1, z1], mat_casco(cel=2.8, fase=k + 1, eixos=(2, 1)), faixa=(7, 20)))
        fora = "east" if lado > 0 else "west"
        cx, cz = 13.1 * lado, -1.2
        asa.append(peca("ombro_placa_" + s, [cx - 1.3, 9.4, cz - 7.0], [cx + 1.3, 22.2, cz + 7.0],
                        mat_placa_glifo(fora, espelha=lado < 0), rot=(8, 6 * lado, 0), pivo=(cx, 15.8, cz), res=4))
        corpo.append(osso("asa_" + s, [11.0 * lado, 20.0, -1.0], [0, 0, 0], asa))

    corpo.append(cauda_blindada())
    corpo.append(pescoco)
    tronco = osso("corpo", [0, 9.0, 0.5], [0, 0, 0], corpo)

    # ======================= PERNAS =======================
    def perna(lado):
        s = lado_s(lado); xc = 6.6 * lado; zc = 0.6
        pp = []
        mam = mat_cor(lambda p, f: mix(AMARELO, AMARELO_ESC, .1 + .12 * grao(p, 1.0)), borda=.1, curva=.4)
        pp += arredondado("perna_" + s, [xc - 3.6, 3.0, zc - 3.6], [xc + 3.6, 10.0, zc + 4.0], mam, r=0.7, faixa=(0, 10))
        pp.append(peca("pe_" + s, [xc - 3.8, 0.0, zc - 3.4], [xc + 3.8, 3.6, zc + 3.6], mam, faixa=(0, 10)))
        mg = mat_cor(lambda p, f: CINZA_CL if f == "up" else CINZA, borda=.2, curva=.5)
        for k, dx in enumerate((-2.5, 0.0, 2.5)):
            x = xc + dx
            pp.append(peca(f"dedo{k}_{s}", [x - 1.1, 0.0, zc - 5.4], [x + 1.1, 3.0, zc - 3.0], mam, faixa=(0, 10)))
            pp += arredondado(f"garra{k}_{s}", [x - 1.15, 0.0, zc - 8.0], [x + 1.15, 3.6, zc - 5.0], mg, r=0.4, faixa=(0, 3.6))
        pp += arredondado("garra_tras_" + s, [xc - 1.6, 0.0, zc + 3.6], [xc + 1.6, 3.0, zc + 6.4], mg, r=0.4, faixa=(0, 3.6))
        return osso("perna_" + s, [xc, 10.0, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
