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
CREME = (248, 222, 186); CREME_CL = (252, 234, 204); CREME_SOM = (222, 184, 144)
BEGE = (238, 168, 104)           # bege/tan claro das faixas
BEGE_CL = (250, 196, 136)
CARAMELO = (205, 118, 64)
MARROM = (150, 84, 66)           # marrom avermelhado (malva) das faixas
MARROM_ESC = (92, 50, 46)
VERM = (212, 36, 32); VERM_ESC = (156, 20, 24); VERM_CL = (240, 76, 60)
AMARELO = (252, 174, 20); AMARELO_CL = (255, 212, 84); AMARELO_ESC = (214, 124, 8)
OURO_BICO = (245, 184, 0); OURO_BICO_CL = (255, 214, 64); OURO_BICO_ESC = (212, 138, 0)
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
        claro = k % 2 == 1                                     # a faixa inteira de uma cor: listras limpas
        base = BEGE if claro else MARROM
        if face == "south": base = BEGE_CL if claro else mix(MARROM, BEGE, .3)      # beirada de trás
        luz = {"up": .10, "south": .04, "north": -.3, "down": -.45}.get(face, -.15)
        luz += -0.2 + 0.28 * alt + (0.05 if (m + cz) % 2 else -0.02) + 0.02 * grao(c["p"])   # células de placa bem sutis
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

def mat_placa_elmo(k):
    """Placa maciça do elmo: uma cor por placa (alternando), beirada de trás clara, células de placa bem sutis."""
    def f(c):
        p = c["p"]; face = c["face"]
        claro = k % 2 == 0
        base = BEGE if claro else MARROM
        if face == "south": base = BEGE_CL if claro else mix(MARROM, BEGE, .3)
        cel = (int(math.floor(p[0] / 2.8)) + int(math.floor(p[2] / 2.8))) % 2
        y0, y1 = c["faixa"]
        luz = -0.2 + 0.32 * clamp((p[1] - y0) / (y1 - y0)) + {"up": .1, "down": -.4, "north": -.05}.get(face, -.08)
        luz += (0.05 if cel else -0.02) + 0.02 * grao(p)
        if na_borda(c) and face in ('south', 'north'): luz -= .15
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
        luz = {"up": .14, "down": -.4, "north": -.02, "south": -.12}.get(face, -.1)
        if na_borda(c): luz -= .3
        return tom(mix(fundo, borda, .2), luz)
    return f

def mat_creme(c0=CREME, c1=CREME_SOM, **kw):
    return mat_cor(lambda p, f: mix(c0, c1, .2 + .1 * grao(p, 0.6)), **kw)

LINHAS_PEITO = [17.2, 14.2, 11.2, 8.2]      # base de cada fileira de penas (de cima para baixo)

def cor_peito_v(p, face, larg=2.4):
    """Peito: 4 fileiras de penas creme com ponta em V (a de cima mais clara); abaixo do V aparece a fileira de baixo."""
    x, y, z = p
    h = x if face in ("north", "south", "up", "down") else z
    t = (h / larg) % 1.0
    for k, yb in enumerate(LINHAS_PEITO):
        if y >= yb or k == len(LINHAS_PEITO) - 1:
            base = mix(CREME_CL, CREME_SOM, 0.08 + 0.2 * k)
            v = yb + 1.3 * abs(2 * t - 1)                      # ponta em V (mais baixa no meio da pena)
            if k + 1 < len(LINHAS_PEITO) and y < v:          # abaixo do V: a fileira de baixo, na sombra
                return mix(mix(CREME_CL, CREME_SOM, 0.28 + 0.2 * k), CREME_SOM, .6)
            if y < v + 0.36: return mix(CREME_SOM, CARAMELO, .3)  # contorno da ponta
            return mix(base, CREME_SOM, .05 * (1 + grao(p, 0.7)))
    return CREME

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
        claro = k % 2 == 1                                                 # anel inteiro de uma cor (alternando)
        base = BEGE if claro else MARROM
        if face == "south": base = BEGE_CL if claro else mix(MARROM, BEGE, .3)   # beirada de trás
        t = clamp((y - (yc - Ry)) / (2 * Ry))
        luz = -0.28 + 0.38 * t + {"up": .12, "down": -.35, "north": -.3}.get(face, 0) + 0.05 * grao(c["p"])
        if na_borda(c): luz -= .2
        return tom(base, luz)
    return [peca(nome + "_a", [-R + r, yc - Ry, z0], [R - r, yc + Ry, z0 + L], mat, res=2),
            peca(nome + "_b", [-R, yc - Ry + r, z0 + 0.04], [R, yc + Ry - r, z0 + L - 0.04], mat, res=2)]

def cauda_blindada():
    """Cone de anéis encaixados com a barriga quase reta (perto de y = 7) e o dorso descendo em degraus: cada anel é
    um osso (cauda_anel_k) filho do anterior, para a cauda ondular."""
    ANEIS = [(5.8, 5.4, 4.4), (4.9, 4.5, 4.0), (4.0, 3.6, 3.8), (3.0, 2.7, 3.4), (2.0, 1.8, 3.0)]   # (raio x, raio y, comprimento)
    Y0, PASSO, INCL = 12.6, 3.4, 30
    def seg(k, z0):
        R, Ry, L = ANEIS[k]
        yc = Y0                                # eixo reto: cone que afina por igual
        filhos = anel_cauda(f"cauda_anel{k}", k, z0, yc, R, Ry, L)
        if k + 1 < len(ANEIS): filhos.append(seg(k + 1, z0 + PASSO))
        else:   # ponta: bico bege
            filhos.append(peca("cauda_ponta", [-0.9, yc - 0.8, z0 + L - 0.4], [0.9, yc + 0.8, z0 + L + 1.4],
                               mat_cor(lambda p, f: BEGE_CL, borda=.2)))
        return osso(f"cauda_anel_{k}", [0, yc, z0], [INCL if k == 0 else 1, 0, 0], filhos)
    return osso("cauda", [0, Y0, 13.6], [0, 0, 0], [seg(0, 13.6)])

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
    if face in ("east", "west") and abs(z + 16.4) < 0.42 and abs(y - 25.7) < 0.42: return (110, 50, 10)   # narina
    if face == "down": return AMARELO_ESC
    if face in ("east", "west") and 23.0 < y < 23.35: return (150, 70, 6)                                # linha da boca
    return mix(OURO_BICO_CL, OURO_BICO, clamp((26.8 - y) / 2.0) * .8 + clamp((-z - 16) / 4) * .3)

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
    cab.append(peca("bico_base", [-2.6, 23.0, -17.2], [2.6, 27.0, FACE_Z + 0.3], mb, faixa=fb, res=4))
    cab.append(peca("bico_meio", [-2.2, 22.9, -19.2], [2.2, 26.7, -17.0], mb, faixa=fb, res=4))
    cab.append(peca("bico_gancho", [-1.6, 22.2, -20.3], [1.6, 25.6, -19.0], mb, rot=(-14, 0, 0), pivo=(0, 25.6, -19.0), faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-1.8, 22.2, -17.6], [1.8, 23.0, FACE_Z + 0.3], mat_cor(lambda p, f: OURO_BICO_ESC, borda=.12), res=4))

    # barbela vermelha: dois lóbulos abrindo em V embaixo do bico
    mv_ = mat_cor(lambda p, f: mix(VERM_CL, VERM, clamp((21.5 - p[1]) / 2.5)), borda=.1, curva=.5)
    cab.append(peca("barbela_meio", [-2.2, 20.0, -16.6], [2.2, 22.4, -14.4], mv_, faixa=(15, 22)))
    for lado in (-1, 1):
        x0, x1 = sorted((0.15 * lado, 3.3 * lado))
        cab += [osso("barbela_" + lado_s(lado), [0.4 * lado, 22.0, -15.5], [0, 0, 6 * lado],
                     arredondado("barbela_" + lado_s(lado), [x0, 16.6, -16.8], [x1, 22.0, -14.2], mv_, r=0.5, faixa=(15, 22)))]

    # elmo rochoso: aba em V bravo + duas faixas arredondadas em xadrez
    for lado in (-1, 1):
        x0, x1 = sorted((0.0, 8.8 * lado))
        cab.append(peca("elmo_aba_" + lado_s(lado), [x0, 26.4, -15.4], [x1, 30.4, -10.6], mat_casco(cel=2.9, fase=0 if lado > 0 else 1, eixos=(0, 2), aba="north"),
                        rot=(0, 0, 14 * lado), pivo=(0, 26.4, -13.0), faixa=(26, 34), res=2))
    # domo FECHADO de 3 placas maciças arredondadas (cada uma um pouco maior que a da frente, em degrau),
    # coladas no crânio e alternando bege/marrom como as faixas do corpo
    for k, (z0, z1) in enumerate([(-14.0, -9.2), (-9.6, -4.4), (-4.8, 1.2)]):
        x, y1 = 8.5 + 0.3 * k, 33.0 + 0.3 * k
        cab += arredondado2(f"elmo{k}", [-x, 26.6, z0], [x, y1, z1], mat_placa_elmo(k), r=3.2, faixa=(26, 34))

    # placa da bochecha com a espiral quadrada (glifo), girada para a frente
    for lado in (-1, 1):
        cx, cz = 8.7 * lado, -7.6
        fora = "east" if lado > 0 else "west"
        cab.append(peca("bochecha_" + lado_s(lado), [cx - 1.7, 19.4, cz - 3.9], [cx + 1.7, 27.8, cz + 3.9],
                        mat_placa_glifo(fora, espelha=lado < 0), rot=(0, 28 * lado, 0), pivo=(cx, 24.4, cz), res=6))

    # crista vermelha em blocos: três lâminas no meio + duas abas laterais (cruz vista de frente)
    mcr = mat_cor(lambda p, f: mix(VERM_CL, VERM, clamp((36.5 - p[1]) / 5)) if f != "down" else VERM_ESC, borda=.12, curva=.5)
    crista = []
    for k, (z0, z1, alto, giro) in enumerate([(-13.6, -10.4, 4.0, -20), (-10.6, -7.0, 5.4, -7), (-7.2, -3.6, 5.6, 7), (-3.8, -0.4, 4.4, 20)]):
        crista.append(osso(f"crista_bloco{k}", [0, 31.4, (z0 + z1) / 2], [giro, 0, 0], [
            peca(f"crista_bloco{k}", [-1.6, 30.6, z0], [1.6, 31.4 + alto, z1], mcr, faixa=(31, 37.5))]))
    cab.append(osso("crista", [0, 31.4, -7.0], [0, 0, 0], crista))

    cabeca = osso("cabeca", [0, 21.0, -8.0], [0, 0, 0], cab)
    g.transformar(i_cab, [cabeca], K_CAB_C, k=K_CAB, sobe=K_CAB_SOBE)   # cabeça grande, como na ficha
    pescoco = osso("pescoco", [0, 19.0, -6.0], [0, 0, 0], [
        peca("pescoco", [-7.4, 15.0, -12.0], [7.4, 27.0, -1.0], mat_cor(lambda p, f: mix(CREME, CREME_SOM, .35), borda=.03, curva=.3), faixa=(7, 27)),
        cabeca])

    # ======================= CORPO =======================
    corpo = []
    casco = mat_cor(lambda p, f: MARROM, borda=.05)
    creme = mat_cor(lambda p, f: CREME_SOM)
    def mat_tronco(c): return creme(c) if c["p"][2] < -5 else casco(c)
    corpo += arredondado2("tronco", [-10.4, 7.6, -12.4], [10.4, 26.0, 13.0], mat_tronco, r=3.0)
    # peito creme: massa arredondada + 2 fileiras de penas sobrepostas (beirada de baixo com pontas de pena)
    corpo += arredondado("peito", [-8.6, 7.8, -14.6], [8.6, 20.6, -5.0], mat_cor(cor_peito_v, borda=0, curva=.2, baixo=.25),
                         r=1.8, faixa=(7, 21), res=4)
    # carapaça do dorso: faixas da nuca até a garupa
    FAIXAS = [  # (zc, y do alto, meia largura, altura, comprimento, inclinação)
        (1.4, 29.8, 10.6, 13.5, 6.4, 0),
        (5.2, 33.2, 12.4, 20.5, 6.8, 4),
        (9.8, 32.6, 12.8, 20.5, 6.6, 16),
        (13.8, 30.0, 12.2, 18.5, 6.2, 32),
        (16.6, 26.0, 10.4, 14.0, 5.6, 52),
    ]
    for k, (zc, yt, W, H, L, inc) in enumerate(FAIXAS):
        corpo.append(faixa(f"faixa{k}", k, zc, yt, W, H, L, inc))

    # asas: faixas de asa em xadrez sob a grande placa do ombro com a espiral
    for lado in (-1, 1):
        s = lado_s(lado)
        asa = []
        x0, x1 = sorted((9.6 * lado, 12.4 * lado))
        fora = "east" if lado > 0 else "west"
        cx, cz = 12.9 * lado, -2.0
        asa.append(peca("ombro_placa_" + s, [cx - 1.7, 9.8, cz - 5.8], [cx + 1.7, 21.4, cz + 5.8],
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

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
