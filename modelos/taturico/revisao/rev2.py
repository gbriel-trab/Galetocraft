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
from galo_base import peca, osso, mix, clamp, arredondado, arredondado2, pintar_olho, na_borda, contexto_luz

ID = "taturico"; NOME = "Taturico"; NUMERO = 7
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 25.5, -15.5), 8)
ONDAS = [("cauda_anel", 5, (1.2, 2.5, 0))]
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (Paleta de Cores da ficha) ----------------
CREME = (240, 221, 191); CREME_CL = (250, 230, 196); CREME_SOM = (218, 186, 146)
BEGE = (236, 148, 74)            # laranja-claro das faixas
BEGE_CL = (250, 184, 112)
CARAMELO = (200, 112, 56)
MARROM = (126, 68, 38)           # marrom chocolate das faixas
MARROM_ESC = (78, 40, 24)
VERM = (212, 36, 32); VERM_ESC = (156, 20, 24); VERM_CL = (240, 76, 60)
AMARELO = (252, 174, 20); AMARELO_CL = (255, 212, 84); AMARELO_ESC = (214, 124, 8)
CINZA = (98, 78, 88); CINZA_CL = (132, 112, 122); CINZA_ESC = (70, 56, 64)
PRETO = (24, 12, 14)

# ---------------- luz quente (sombra puxada para o marrom, não para o roxo) ----------------
LUZ = (255, 244, 220)
def tom(c, f):
    f = clamp(f, -1, 1)
    return mix(c, LUZ, f * .40) if f >= 0 else mix(c, (int(c[0] * .52), int(c[1] * .40), int(c[2] * .30)), -f * .9)

def mat_cor(cor_fn, **kw):
    """Como g.mat_cor, mas com a sombra quente desta espécie."""
    def f(c):
        base = cor_fn(c["p"], c["face"])
        return None if base is None else tom(base, contexto_luz(c, **kw))
    return f

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
        if abs(m) <= 2: claro = k % 2 == 1                      # no alto: a faixa inteira de uma cor (listras de trás)
        else: claro = (m + cz + k) % 2 == 0                     # nos lados: xadrez (como nas vistas laterais)
        base = BEGE if claro else MARROM
        if face == "south": base = BEGE_CL if claro else mix(MARROM, BEGE, .22)      # beirada de trás
        luz = {"up": .10, "south": .02, "north": -.3, "down": -.45}.get(face, -.15)
        luz += -0.18 + 0.26 * alt + 0.025 * grao(c["p"])
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
        luz = -0.25 + 0.35 * t + {"up": .12, "down": -.4}.get(face, 0) + 0.025 * grao(p)
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
            return tom(base, 0.08 - 0.22 * v + 0.02 * grao(c["p"], 0.6))
        luz = {"up": .14, "down": -.4, "north": -.02, "south": -.12}.get(face, -.1)
        if na_borda(c): luz -= .3
        return tom(mix(fundo, BEGE, .12), luz)
    return f

def mat_creme(c0=CREME, c1=CREME_SOM, **kw):
    return mat_cor(lambda p, f: mix(c0, c1, .2 + .1 * grao(p, 0.6)), **kw)

def cor_fileira(y0, base, larg=2.1):
    """Fileira de penas do peito (escamas): pontas arredondadas na barra de baixo; entre as pontas, sombra."""
    def f(p, face):
        x, y, z = p
        h = x if face in ("north", "south", "up", "down") else z
        t = (h / larg) % 1.0
        ponta = y0 + 1.2 * (1 - math.sqrt(max(0.0, 1 - (2 * abs(t - 0.5)) ** 2)))   # ponta arredondada (mais baixa no meio)
        cor = mix(base, CREME_CL, clamp((y - y0 - 1.2) / 3.0) * .5)
        if y < ponta: return tom(CREME_SOM, -0.25)         # vão entre as pontas
        if y < ponta + 0.3: return mix(base, CREME_SOM, .7)        # contorno da ponta
        return mix(cor, CREME_SOM, .06 * (1 + grao(p, 0.7)))
    return f

def mat_escama(xc, w, y0, base):
    """Pena-escama do peito: ponta de baixo arredondada (fora da curva = sombra do vão), contorno suave, alto claro."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        if face in ("north", "east", "west"):
            u = (x - xc) / (w / 2) if face == "north" else 0.0
            yb = y0 + 1.6 * (1 - math.sqrt(max(0.0, 1 - min(1.0, abs(u)) ** 2)))
            if y < yb: return tom(base, -0.38)
            if y < yb + 0.3: return tom(base, -0.16)
            return tom(mix(base, CREME_CL, clamp((y - y0 - 1.5) / 3) * .45), 0.04 * grao(c["p"], 0.7))
        return tom(base, {"up": .1, "down": -.4}.get(face, -.1))
    return f

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
        claro = k % 2 == 1 if y > yc - 0.3 * Ry else (setor + k) % 2 == 0    # anel de uma cor em cima, xadrez embaixo
        base = BEGE if claro else MARROM
        if face == "south": base = BEGE_CL if claro else mix(MARROM, BEGE, .3)   # beirada de trás
        t = clamp((y - (yc - Ry)) / (2 * Ry))
        luz = -0.28 + 0.38 * t + {"up": .12, "down": -.35, "north": -.3}.get(face, 0) + 0.02 * grao(c["p"])
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
FX = 2.6                 # meia largura da frente estreita (o bico ocupa quase toda)
FAC_T = 2.0              # espessura da face diagonal
FAC_L = 4.6              # comprimento da face diagonal (45°): o olho fica na transição frente/lado, junto do bico
OLHO_Y = 25.9
K_CAB, K_CAB_C, K_CAB_SOBE = 1.2, (0.0, 20.0, -5.0), -0.8   # escala da cabeça inteira (grande e projetada para a frente)

def faceta_centro(lado):
    """Centro (x, z) da peça da face diagonal: a face de fora passa pelo meio da diagonal do rosto."""
    mx, mz = (FX + FAC_L * 0.7071 / 2), FACE_Z + FAC_L * 0.7071 / 2
    return lado * (mx - 0.7071 * FAC_T / 2), mz + 0.7071 * FAC_T / 2

def mat_faceta(lado):
    """Face diagonal do rosto: creme, com o olho inteiro na face de fora (amarelo, pupila preta, pálpebra marrom)."""
    base = mat_creme(c0=(246, 222, 186), c1=(232, 200, 160), borda=.03, curva=.2)
    fora = "east" if lado > 0 else "west"
    cx, cz = faceta_centro(lado)
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u, v = z - cz, y - OLHO_Y
            if (u / 1.5) ** 2 + (v / 1.38) ** 2 <= 1 and not (u / 1.28) ** 2 + (v / 1.18) ** 2 <= 1:
                return tom(MARROM, -0.1)                         # contorno (pálpebra) marrom
            cor = pintar_olho(u, v, 1.28, 1.18, iris=((196, 104, 0), (255, 200, 36)), esclera=(250, 242, 226),
                              r_iris=(0.8, 0.9), c_iris=(-0.16, -0.1), r_pup=(0.42, 0.5), bravo=0.0)
            if cor is not None: return cor
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face in ("east", "west") and abs(z + 15.9) < 0.38 and abs(y - 25.2) < 0.38: return (100, 44, 8)    # narina
    if face == "up" and abs(z + 15.9) < 0.35 and 0.9 < abs(x) < 1.6: return (100, 44, 8)
    if face == "down": return AMARELO_ESC
    if face in ("east", "west") and 23.15 < y < 23.45: return (150, 70, 6)                                 # linha da boca
    return mix(AMARELO_CL, AMARELO, clamp((26.2 - y) / 2.4) * .7 + clamp((-z - 15.5) / 3) * .45)

def montar():
    # ======================= CABEÇA =======================
    i_cab = len(g.PECAS)
    cab = []
    mcreme = mat_creme(c0=(246, 222, 186), c1=(232, 200, 160), borda=.05, curva=.3)
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
    cab.append(peca("bico_base", [-2.3, 23.0, -16.6], [2.3, 26.2, FACE_Z + 0.3], mb, faixa=fb, res=4))
    cab.append(peca("bico_ponta", [-1.9, 23.0, -18.3], [1.9, 25.9, -16.4], mb, rot=(-10, 0, 0), pivo=(0, 25.8, -16.4), faixa=fb, res=4))
    cab.append(peca("bico_gancho", [-1.3, 22.3, -19.1], [1.3, 24.7, -17.9], mat_cor(cor_bico, borda=.06, curva=.6), faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-1.6, 22.5, -16.5], [1.6, 23.1, FACE_Z + 0.3], mat_cor(lambda p, f: mix(AMARELO, AMARELO_ESC, .6), borda=.12), res=4))

    # barbela vermelha: dois lóbulos abrindo em V embaixo do bico
    mv_ = mat_cor(lambda p, f: mix(VERM_CL, VERM, clamp((22.5 - p[1]) / 3.5)), borda=.1, curva=.5)
    for lado in (-1, 1):
        x0, x1 = sorted((0.12 * lado, 1.9 * lado))
        cab += arredondado("barbela_" + lado_s(lado), [x0, 18.9, -16.2], [x1, 23.0, -14.2], mv_, r=0.45, faixa=(18.5, 23))

    # elmo rochoso: aba em V bravo + duas faixas arredondadas em xadrez
    for lado in (-1, 1):
        x0, x1 = sorted((0.0, 9.0 * lado))
        cab.append(peca("elmo_aba_" + lado_s(lado), [x0, 25.6, -17.2], [x1, 29.8, -10.8], mat_casco(cel=2.9, fase=0 if lado > 0 else 1, eixos=(0, 2), aba="north"),
                        rot=(0, 0, 15 * lado), pivo=(0, 25.6, -14.0), faixa=(25, 34), res=2))
        # viseira: placa grossa na face diagonal, cobrindo o terço de cima do olho e descendo para o bico (cara séria)
        cx, cz = faceta_centro(lado)
        ox = cx + lado * FAC_T / 2
        v0, v1 = sorted((ox - 0.3 * lado, ox + 0.7 * lado))
        cab.append(osso("viseira_" + lado_s(lado), [cx, OLHO_Y, cz], [0, 45 * lado, 0], [
            peca("viseira_" + lado_s(lado), [v0, OLHO_Y + 0.5, cz - FAC_L / 2 - 0.4], [v1, OLHO_Y + 2.4, cz + FAC_L / 2 + 0.2],
                 mat_casco(cel=2.3, fase=1, eixos=(2, 1), aba="up"), rot=(-16, 0, 0), pivo=(cx, OLHO_Y + 1.2, cz), faixa=(24, 29), res=4)]))
    cab.append(faixa("elmo1", 1, -10.0, 33.2, 8.6, 6.8, 6.8, -6))
    cab.append(faixa("elmo2", 0, -4.2, 33.8, 9.2, 7.4, 7.0, 4))

    # placa da bochecha com a espiral quadrada (glifo), girada para a frente
    for lado in (-1, 1):
        cx, cz = 8.6 * lado, -7.0
        fora = "east" if lado > 0 else "west"
        cab.append(peca("bochecha_" + lado_s(lado), [cx - 1.6, 20.4, cz - 3.4], [cx + 1.6, 27.4, cz + 3.4],
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
        peca("pescoco", [-7.4, 15.0, -12.0], [7.4, 27.0, -1.0], mat_creme(c0=(240, 214, 176), c1=CREME_SOM, borda=.03, curva=.3), faixa=(7, 27)),
        cabeca])

    # ======================= CORPO =======================
    corpo = []
    casco = mat_casco(cel=2.8, fase=0, eixos=(0, 1), org=(0, 0, 0))
    creme = mat_cor(lambda p, f: CREME_SOM)
    def mat_tronco(c): return creme(c) if c["p"][2] < -5 else casco(c)
    corpo += arredondado2("tronco", [-10.4, 7.6, -12.4], [10.4, 26.0, 13.0], mat_tronco, r=3.0)
    # peito creme: 4 fileiras de penas-escama em "tijolo" (cada fileira meia pena deslocada), cada uma mais para
    # trás que a de cima; as penas das pontas giram para dentro e somem sob as placas marrons
    corpo += arredondado("peito_miolo", [-8.0, 7.8, -12.6], [8.0, 20.6, -6.0], mat_cor(lambda p, f: CREME_SOM, borda=0), r=1.4, faixa=(7, 21))
    FILEIRAS = [(16.4, -14.9, (-4.2, 0.0, 4.2)), (13.3, -14.3, (-7.6, -4.0, 0.0, 4.0, 7.6)),
                (10.3, -13.7, (-6.0, -2.0, 2.0, 6.0)), (7.6, -13.1, (-7.2, -3.6, 0.0, 3.6, 7.2))]
    for k, (y0, zf, xs) in enumerate(FILEIRAS):
        base = mix((248, 226, 190), CREME_SOM, 0.1 + k * 0.17)
        for j, xc in enumerate(xs):
            w = 4.3 if abs(xc) < 7 else 3.2
            zf_ = zf + (0.18 if j % 2 else 0.0) + (0.9 if abs(xc) >= 5.9 else 0.0)
            giro = 0 if abs(xc) < 5.9 else (-30 if xc > 0 else 30)   # a face larga vira para fora
            corpo.append(peca(f"pena_peito{k}_{j}", [xc - w / 2, y0, zf_], [xc + w / 2, y0 + 4.4, zf_ + 2.2],
                              mat_escama(xc, w, y0, base), rot=(0, giro, 0), pivo=(xc, y0, zf_ + 1.1), faixa=(7, 21), res=4))
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
            asa.append(peca(f"asa_faixa{k}_{s}", [a0, y0, z0], [a1, y1, z1], mat_casco(cel=2.8, fase=k + 1, eixos=(2, 1), org=(0, 0, 0)), faixa=(7, 20)))
        fora = "east" if lado > 0 else "west"
        cx, cz = 12.9 * lado, -2.0
        asa.append(peca("ombro_placa_" + s, [cx - 1.7, 10.2, cz - 5.4], [cx + 1.7, 21.0, cz + 5.4],
                        mat_placa_glifo(fora, espelha=lado < 0), rot=(7, 5 * lado, 9 * lado), pivo=(cx, 15.6, cz), res=4))
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

def rosto_so_cabeca(caminho, pasta, prefixo):
    """Refaz <prefixo>_rosto.png só com o osso 'cabeca' (sem recortar faces do corpo pela distância, que deixa
    planos soltos na imagem): frente, 3/4 e perfil."""
    import json
    from PIL import Image
    import previa2
    m = json.loads(Path(caminho).read_text(encoding="utf-8"))
    def acha(no):
        if isinstance(no, dict):
            if no["name"] == "cabeca": return no
            for f in no["children"]:
                r = acha(f)
                if r: return r
    cab = next(r for r in (acha(n) for n in m["outliner"]) if r)
    m["outliner"] = [cab]
    tmp = Path(pasta) / "_so_cabeca.bbmodel"
    tmp.write_text(json.dumps(m), encoding="utf-8")
    q = previa2.carregar(str(tmp))
    ims = [previa2.desenhar(q, y, p, escala=40, fundo=g.FUNDO) for y, p in ((0, -6), (35, -8), (90, -4))]
    f = Image.new("RGB", (sum(i.width for i in ims) + 20, max(i.height for i in ims)), g.FUNDO); x = 0
    for i in ims: f.paste(i, (x, 0)); x += i.width + 10
    f.save(Path(pasta) / f"{prefixo}_rosto.png")
    tmp.unlink()

if __name__ == "__main__":
    caminho = g.rodar(ID, montar, rosto=ROSTO)
    pasta = Path(sys.argv[1]) if len(sys.argv) > 1 else g.RAIZ / "modelos" / ID / "revisao"
    rosto_so_cabeca(caminho, pasta, sys.argv[2] if len(sys.argv) > 2 else "atual")
