"""Espinhocó (#011, Planta): galo-porco-espinho da floresta, bola de espinhos grossos nas costas e plumagem de folhas.

Refeito (série n*) depois da rejeição: tudo em BLOCOS GROSSOS com 2 ou 3 tons chapados (nada de placas finas,
franjas ou ruído), proporções medidas nas 4 vistas da ficha e rosto copiado da expressão neutra.
Medidas da ficha (altura total ~39 unidades, pés em y=0, centro das pernas em z=0):
- crista de folhas 29..39, cabeça 20.6..29.4 (larga: ±5.4), bico até z=-16, barbela até y=17;
- peito creme em degraus 9.5..21, corpo marrom até y=6, pernas curtas (canela 1.3..5);
- de lado o corpo inteiro tem ~41 de comprimento: espinhos até z=+26 atrás, y=36.5 em cima e y=6 embaixo;
- de frente/trás ~27 de largura (folhas dos ombros e espinhos laterais até x=±13.5)."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, pintar_olho

ID = "espinhoco"; NOME = "Espinhocó"; NUMERO = 11
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 25.0, -12.0), 7.4)
ONDAS = []
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (Paleta de Cores da ficha) ----------------
CREME = (244, 226, 196); CREME_ESC = (224, 196, 158)
BEGE = (226, 182, 136); CARAMELO = (190, 130, 82)
MARROM = (142, 90, 56); MARROM_ESC = (104, 66, 42); CHOCOLATE = (70, 46, 36); CHOCOLATE_CLARO = (112, 78, 58)
VERDE_ESC = (98, 132, 30); VERDE = (140, 172, 40); VERDE_CLARO = (182, 208, 66); CONTORNO_FOLHA = (66, 94, 24)
AMARELO_BICO = (250, 204, 44); AMARELO_ESC = (230, 160, 26); LARANJA_BICO = (206, 122, 24)
VERM = (214, 40, 34); VERM_ESC = (156, 22, 26)
GARRA = (78, 70, 76); GARRA_CLARA = (112, 104, 110); GARRA_ESC = (44, 38, 44)
CANELA = (196, 124, 60); CANELA_CLARA = (220, 152, 84)
OLHO_IRIS = ((90, 140, 14), (178, 222, 56))

# ---------------- utilidades de rotação ----------------
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
    """Giro (em torno do próprio eixo) que deixa a normal local -z o mais virada possível para 'fora'."""
    R = rot_m(*apontar(d)); fora = norm(fora)
    melhor, tm = -9, 0
    for t in range(-180, 180, 5):
        n = mv(R, mv(rot_m(0, t, 0), [0, 0, -1]))
        s = sum(n[i] * fora[i] for i in range(3))
        if s > melhor: melhor, tm = s, t
    return tm

# ---------------- materiais chapados (2 ou 3 tons por bloco) ----------------
def borda_px(c, n=1):
    return c["i"] < n or c["j"] < n or c["i"] >= c["tw"] - n or c["j"] >= c["th"] - n

def mat_bloco(cor_fn, cima=.14, baixo=-.30, lado=-.04, borda=-.16, faixas=True):
    """Bloco chapado: face de cima clara, de baixo em sombra, laterais na cor base com uma faixa clara no alto e
    uma de sombra embaixo (3 tons), e um fio escuro na borda de cada face."""
    def f(c):
        cor = cor_fn(c["p"], c["face"])
        if cor is None: return None
        face = c["face"]
        if face == "up": luz = cima
        elif face == "down": luz = baixo
        else:
            luz = lado if face in ("east", "west") else 0.0
            if faixas:
                (_, y0, _), (_, y1, _) = c["b"]
                t = (c["p"][1] - y0) / max(y1 - y0, 1e-6)
                if t > .84: luz += .10
                elif t < .16: luz -= .14
        if borda_px(c): luz += borda
        return tom(cor, luz)
    return f

def mat_tons(cima, base, baixo, lado=None, borda=-.18):
    """Bloco de 3 tons fixos: cima / laterais / baixo (lado = tom das faces leste-oeste, se diferente)."""
    def f(c):
        face = c["face"]
        cor = cima if face == "up" else baixo if face == "down" else (lado or base) if face in ("east", "west") else base
        return tom(cor, borda) if borda_px(c) else cor
    return f

# ---------------- espinhos: cones grossos em 3 degraus ----------------
ESP_CLARO = ((168, 116, 78), (214, 170, 126), (234, 204, 164), (246, 228, 198))   # raiz -> ponta (espinho claro)
ESP_ESCURO = ((124, 80, 50), (176, 124, 84), (214, 176, 134), (236, 210, 172))     # espinho do fundo (mais marrom)
SEG_ESPINHO = ((0.00, 0.42, 1.00), (0.38, 0.66, 0.72), (0.62, 0.86, 0.46), (0.82, 1.00, 0.20))   # (início, fim, largura) em frações

def mat_espinho(cor):
    """Degrau do espinho: 2 faces claras, 2 escuras (facetas), ponta clara, contorno escuro."""
    luzes = {"north": .10, "east": .02, "south": -.14, "west": -.06, "up": .14, "down": -.26}
    def f(c):
        luz = luzes[c["face"]]
        if c["face"] not in ("up", "down") and (c["i"] == 0 or c["i"] == c["tw"] - 1): luz -= .16
        return tom(cor, luz)
    return f

def espinho(nome, raiz, d, L, W, cores=ESP_CLARO, torce=45):
    x, y, z = raiz
    pecas = []
    for k, (a, b, fw) in enumerate(SEG_ESPINHO):
        w = W * fw
        pecas.append(peca(f"{nome}_{k}", [x - w / 2, y + a * L, z - w / 2], [x + w / 2, y + b * L, z + w / 2],
                          mat_espinho(cores[k]), res=2))
    return osso(nome, list(raiz), apontar(d), [osso(nome + "_t", list(raiz), [0, torce, 0], pecas)])

# ---------------- folhas grossas (lanceoladas, em 3 degraus, 2 tons divididos na nervura) ----------------
FOLHA_PADRAO = (VERDE_CLARO, VERDE, VERDE_ESC)

def mat_folha(cx, cores=FOLHA_PADRAO):
    claro, medio, escuro = cores
    def f(c):
        x = c["p"][0]
        face = c["face"]
        if face in ("north", "south"):
            cor = claro if x >= cx else medio
            if c["i"] == 0 or c["i"] == c["tw"] - 1: cor = tom(cor, -.20)
            return cor
        if face == "up": return tom(claro, -.05)
        return tom(escuro, -.08 if borda_px(c) else 0)
    return f

def folha(nome, raiz, d, L, W, fora=None, cores=FOLHA_PADRAO, esp=1.0, torce=None):
    """Folha grossa (espessura esp) que cresce na direção d: corpo largo, meio estreito e ponta.
    A face larga fica virada para 'fora'."""
    x, y, z = raiz
    if torce is None: torce = torcao_para(d, fora or [0, 0, -1])
    m = mat_folha(x, cores)
    e = esp / 2
    pecas = [peca(nome + "_0", [x - W * .28, y, z - e * .9], [x + W * .28, y + L * .20, z + e * .9], m, res=3),
             peca(nome + "_1", [x - W * .50, y + L * .16, z - e], [x + W * .50, y + L * .62, z + e], m, res=3),
             peca(nome + "_2", [x - W * .31, y + L * .58, z - e * .9], [x + W * .31, y + L * .84, z + e * .9], m, res=3),
             peca(nome + "_3", [x - W * .13, y + L * .80, z - e * .8], [x + W * .13, y + L, z + e * .8], m, res=3)]
    return osso(nome, list(raiz), apontar(d), [osso(nome + "_t", list(raiz), [0, torce, 0], pecas)])

# ---------------- cabeça ----------------
HW = 5.4          # meia largura da cabeça
QX = 2.0          # meia largura da frente reta (onde nasce o bico)
ZF = -12.6        # frente da cabeça
ZB = -3.6         # nuca
FL = math.hypot(HW - QX, HW - QX)       # comprimento da face diagonal (olho)
ZS = ZF + (HW - QX)                     # z onde a face diagonal encontra o lado
FT = 2.0                                # espessura da peça da face diagonal
CAB_Y0, CAB_Y1 = 20.6, 29.4
OLHO_Y = 25.4
Y_CREME = 23.9                          # abaixo disto a cara é creme

def cor_cabeca(p, face):
    x, y, z = p
    if face == "up": return mix(MARROM, CARAMELO, .3)
    if y < Y_CREME and z < -6.5: return CREME
    # blocos marrons grandes (mosaico legível da ficha: 2 tons em quadrados de 2 unidades)
    q = (math.floor((y - 20) / 2.2) + math.floor((z + x) / 2.2)) % 3
    return MARROM if q else mix(MARROM, CARAMELO, .35)

def fc_centro(lado):
    mx, mz = (QX + HW) / 2, (ZF + ZS) / 2
    n = (0.7071, -0.7071)
    return (lado * (mx - n[0] * FT / 2), mz - n[1] * FT / 2)

def mat_faceta(lado):
    base = mat_bloco(cor_cabeca, borda=-.06, faixas=False)
    fora = "east" if lado > 0 else "west"
    cx, cz = fc_centro(lado)
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u = z - cz
            cor = pintar_olho(u + 0.15, y - OLHO_Y, 1.55, 1.25, iris=OLHO_IRIS, c_iris=(-0.22, -0.06),
                              r_iris=(0.6, 0.78), r_pup=(0.26, 0.32), bravo=0.30, alto=0.5, contorno=CHOCOLATE)
            if cor is not None: return cor
            if y < OLHO_Y + 0.6: return CREME
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face == "down": return LARANJA_BICO
    if face in ("east", "west") and abs(z + 14.3) < 0.35 and abs(y - 24.7) < 0.3: return (110, 60, 20)   # narina
    if face == "up": return mix(AMARELO_BICO, (255, 236, 130), .4)
    return mix(AMARELO_BICO, AMARELO_ESC, clamp((24.4 - y) / 3.0))

def montar_cabeca():
    cab = []
    mc = mat_bloco(cor_cabeca, borda=-.06, faixas=False)
    cab.append(peca("cranio_a", [-HW, CAB_Y0 + 0.8, ZS], [HW, CAB_Y1 - 0.8, ZB], mc, res=4))
    cab.append(peca("cranio_b", [-HW + 0.8, CAB_Y0, ZS - 0.4], [HW - 0.8, CAB_Y1, ZB + 0.6], mc, res=4))
    cab.append(peca("cranio_frente", [-QX - 0.3, CAB_Y0, ZF], [QX + 0.3, CAB_Y1 - 0.5, ZS], mc, res=4))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = fc_centro(lado)
        cab.append(peca("cranio_faceta_" + s, [cx - FT / 2, CAB_Y0 + 0.3, cz - FL / 2], [cx + FT / 2, CAB_Y1 - 0.6, cz + FL / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, OLHO_Y, cz), res=8))
    # bochechas creme em bloco (um pouco mais largas que a cabeça, como na frente da ficha)
    mbo = mat_bloco(lambda p, f: CREME, borda=-.10)
    cab.append(peca("bochechas", [-HW - 0.4, CAB_Y0 - 0.2, ZS + 0.6], [HW + 0.4, Y_CREME - 0.1, -6.6], mbo, res=4))
    # sobrancelhas: lajes chocolate grossas, descendo para o bico (cara brava)
    msob = mat_tons(CHOCOLATE_CLARO, CHOCOLATE, (40, 26, 22), lado=mix(CHOCOLATE, CHOCOLATE_CLARO, .3))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = fc_centro(lado)
        ox = cx + lado * (FT / 2)
        x0, x1 = sorted((ox - 0.8 * lado, ox + 1.2 * lado))
        cab.append(osso("sobrancelha_" + s, [cx, 27.3, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s, [x0, 26.5, cz - FL / 2 - 1.7], [x1, 28.4, cz + FL / 2 + 0.9], msob,
                 rot=(-17, 0, 0), pivo=(cx, 27.3, cz), res=4)]))
        x0, x1 = sorted(((HW - 0.6) * lado, (HW + 0.8) * lado))
        cab.append(peca("sobrancelha_lado_" + s, [x0, 27.7, ZS - 0.6], [x1, 29.4, ZS + 3.4], msob,
                        rot=(-6, 0, 0), pivo=(HW * lado, 28.5, ZS), res=4))
    # bico: 3 degraus que estreitam e descem (de frente vira um triângulo; de lado, gancho para baixo)
    mb = mat_bloco(cor_bico, borda=-.12, faixas=False)
    cab.append(peca("bico_base", [-2.1, 22.6, -13.9], [2.1, 25.8, -12.3], mb, res=4))
    cab.append(peca("bico_meio", [-1.55, 22.3, -15.2], [1.55, 25.4, -13.7], mb, res=4))
    cab.append(peca("bico_gancho", [-0.95, 21.2, -16.1], [0.95, 24.8, -14.9], mb, res=4))
    cab.append(peca("bico_baixo", [-1.25, 21.6, -14.5], [1.25, 22.7, -12.4], mat_tons(AMARELO_ESC, LARANJA_BICO, (150, 80, 16)), res=4))
    # barbela: dois lóbulos vermelhos em bloco, pendurados sob o bico
    mbb = mat_bloco(lambda p, f: VERM if abs(p[0]) > 0.9 else mix(VERM, VERM_ESC, .45), borda=-.14)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.25 * lado, 2.5 * lado))
        x2, x3 = sorted((0.6 * lado, 2.2 * lado))
        cab.append(osso("barbela_" + s, [0.25 * lado, 22.4, -13.2], [0, 0, 7 * lado], [
            peca("barbela_" + s, [x0, 18.6, -14.1], [x1, 22.4, -12.3], mbb, res=4),
            peca("barbela_ponta_" + s, [x2, 17.4, -13.9], [x3, 18.8, -12.5], mbb, res=4)]))
    # crista de folhas grossas: leque da frente (de frente lê como a coroa da ficha) e leque de trás (de lado)
    crista = []
    # leque da frente: (ângulo para o lado, inclinação para trás, L, W, quanto a face vira para o lado)
    CF = [(0, -10, 10.8, 4.2, 0.0), (-22, -6, 9.2, 4.0, 0.8), (22, -6, 9.2, 4.0, 0.8), (-46, 0, 7.0, 3.6, 1.0),
          (46, 0, 7.0, 3.6, 1.0)]
    for k, (ang, tras, L, W, vira) in enumerate(CF):
        a, t = math.radians(ang), math.radians(tras)
        d = [math.sin(a), math.cos(a), math.sin(t)]
        crista.append(folha(f"crista{k}", (1.4 * math.sin(a), 28.6, -10.4), d, L, W, esp=1.3,
                            fora=[math.copysign(vira, ang) if ang else 0, 0, -1]))
    # leque de cima e de trás: folhas de lado (de perfil fazem a massa da crista da ficha)
    CT = [(0, -40, 9.6, 4.8, -10.4), (0, -12, 10.4, 4.8, -9.0), (-12, 16, 10.0, 4.6, -8.0), (12, 16, 10.0, 4.6, -8.0),
          (0, 38, 9.4, 4.6, -6.6), (-16, 56, 8.0, 4.2, -5.6), (16, 56, 8.0, 4.2, -5.6)]
    for k, (ang, tras, L, W, z0) in enumerate(CT):
        a, t = math.radians(ang), math.radians(tras)
        d = [math.sin(a), math.cos(t), math.sin(t)]
        crista.append(folha(f"crista_tras{k}", (1.0 * math.sin(a), 28.8, z0), d, L, W, esp=1.3,
                            fora=[1 if k % 2 == 0 else -1, 0.1, 0]))
    cab.append(osso("crista", [0, 29.0, -8.0], [0, 0, 0], crista))
    return cab

# ---------------- corpo ----------------
def meia_peito(y):
    """Meia largura do peito creme na altura y: largo sob a barbela, afinando em degraus até a barriga."""
    return 1.0 + 4.0 * clamp((y - 9.5) / 11.0)

def cor_corpo(p, face):
    x, y, z = p
    if z < -9.6 and abs(x) < meia_peito(y) + 0.8 and y > 9.0:
        return CREME if abs(x) < meia_peito(y) else BEGE
    # penas marrons em escamas grandes (fileiras de 2 unidades, desencontradas)
    fila = math.floor((24 - y) / 2.0)
    fy = ((24 - y) / 2.0) % 1.0
    ang = math.atan2(x, -z) * 7.0
    fx = ((ang + (0.5 if fila % 2 else 0)) / 2.4) % 1.0
    base = MARROM if y > 11 else MARROM_ESC
    if fy > 0.75: return tom(base, -.22)
    if fx < 0.1: return tom(base, -.12)
    return base

def cor_peito(p, face):
    x, y, z = p
    if face == "north":
        borda = meia_peito(y) - abs(x)
        return CREME if borda > 1.0 else mix(CREME, CREME_ESC, .6)
    return CREME_ESC

def montar():
    cab = montar_cabeca()
    cabeca = osso("cabeca", [0, 22.0, -8.0], [0, 0, 0], cab)
    mp = mat_bloco(lambda p, f: CREME if p[2] < -9 else MARROM, borda=-.06, faixas=False)
    pescoco = osso("pescoco", [0, 21.0, -7.0], [0, 0, 0], [
        peca("pescoco", [-4.6, 18.6, -11.6], [4.6, 23.0, -4.0], mp, res=2),
        cabeca])

    corpo = []
    mt = mat_bloco(cor_corpo, borda=-.04, faixas=False)
    corpo += g.arredondado2("tronco", [-7.6, 6.2, -11.4], [7.6, 22.6, 8.6], mt, r=3.0)
    corpo += g.arredondado("dorso", [-6.6, 12.0, -6.0], [6.6, 25.6, 9.6], mt, r=2.4)
    # 'Flor Peitoral': fileiras de blocos creme que estreitam para baixo (degraus em V)
    mpe = mat_bloco(cor_peito, borda=-.12)
    PEITO = [(19.0, 21.4, 4.8, -12.9), (17.0, 19.2, 4.1, -12.8), (15.0, 17.2, 3.3, -12.6), (13.0, 15.2, 2.5, -12.3),
             (11.0, 13.2, 1.6, -11.9)]
    for k, (y0, y1, w, zf) in enumerate(PEITO):
        corpo.append(peca(f"peito{k}", [-w, y0, zf], [w, y1, -10.6], mpe, res=2))

    # ---------- espinhos: bola de cones grossos das costas ----------
    # raiz numa elipsoide das costas, ponta numa elipsoide maior (medida nas vistas da ficha)
    C0, R0 = (0.0, 18.6, 3.0), (6.4, 7.6, 6.4)
    C1, R1 = (0.0, 20.0, 5.0), (13.4, 16.4, 19.6)
    R1_BAIXO = 16.0
    esp_corpo, cauda = [], []
    N = 90; n = 0
    ouro = math.pi * (3 - math.sqrt(5))
    for i in range(N):
        sy = 1 - 2 * (i + 0.5) / N
        r = math.sqrt(1 - sy * sy)
        th = ouro * i
        sx, sz = r * math.cos(th), r * math.sin(th)
        if sz < -0.10: continue                       # nada apontando para a frente
        if sy < -0.62 and sz < 0.5: continue          # nem para baixo (pernas)
        if sz < 0.35 and sy < -0.25: continue         # nem debaixo da barriga
        ry = R1[1] if sy > 0 else R1_BAIXO
        raiz = (C0[0] + R0[0] * sx, C0[1] + R0[1] * sy, C0[2] + R0[2] * sz)
        k_ = (abs(sx) ** 2.7 + abs(sy) ** 2.7 + abs(sz) ** 2.7) ** (-1 / 2.7)   # superelipse: diagonais mais cheias
        k_ = 1 + (k_ - 1) * 0.8
        ponta = (C1[0] + R1[0] * sx * (1 - 0.45 * max(sy, 0)), C1[1] + ry * sy * k_, C1[2] + R1[2] * sz * k_)
        d = [ponta[k] - raiz[k] for k in range(3)]
        L = math.sqrt(sum(v * v for v in d)) + 0.6
        W = 3.9 if L > 9 else 3.3
        cores = ESP_ESCURO if (i * 7) % 5 == 0 else ESP_CLARO
        q = espinho(f"espinho{n}", raiz, d, L, W, cores, torce=45)
        (cauda if sz > 0.55 and sy < 0.25 else esp_corpo).append(q)
        n += 1
    corpo.append(osso("espinhos", list(C0), [0, 0, 0], esp_corpo))
    corpo.append(osso("cauda", [0, 15.0, 8.0], [0, 0, 0], cauda))

    # ---------- asas: 'Plumagem Folhosa' (folhas grossas descendo dos ombros, abertas para fora) ----------
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = []
        # (x, y, z da raiz, para trás (0 = para baixo, 90 = para trás), abertura para fora, L, W)
        ASA = [(6.4, 21.2, -10.4, 2, 26, 13.8, 4.6), (7.0, 21.4, -8.4, 22, 30, 13.6, 4.8), (7.2, 21.4, -6.2, 42, 30, 13.0, 4.8),
               (7.2, 21.8, -4.2, 64, 26, 11.6, 4.6), (7.0, 22.6, -3.0, 84, 22, 9.6, 4.2),
               (6.2, 23.8, -9.6, 20, 56, 8.0, 4.0), (6.4, 24.0, -6.8, 56, 50, 8.2, 4.0)]
        for k, (x0, y0, z0, tras, abre, L, W) in enumerate(ASA):
            t, a = math.radians(tras), math.radians(abre)
            d = [lado * math.sin(a), -math.cos(t) * math.cos(a), math.sin(t) * math.cos(a)]
            asa.append(folha(f"asa{k}_{s}", (x0 * lado, y0, z0), d, L, W, fora=[lado, 0.2, -0.2]))
        corpo.append(osso("asa_" + s, [6.6 * lado, 22.0, -7.0], [0, 0, 0], asa))

    corpo.append(pescoco)
    tronco = osso("corpo", [0, 9.0, 0.0], [0, 0, 0], corpo)

    # ---------- pernas curtas e firmes, 3 dedos com garras escuras grossas + 1 atrás ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 4.1 * lado; zc = 0.0
        pp = []
        mcx = mat_tons(mix(MARROM, CARAMELO, .4), MARROM, MARROM_ESC, lado=mix(MARROM, MARROM_ESC, .3))
        pp += g.octogono("coxa_" + s, [xc - 2.4, 4.6, zc - 2.4], [xc + 2.4, 9.0, zc + 2.4], mcx, r=0.8)
        mca = mat_tons(CANELA_CLARA, CANELA, mix(CANELA, MARROM_ESC, .5), lado=mix(CANELA, MARROM, .3))
        pp += g.octogono("canela_" + s, [xc - 1.8, 1.0, zc - 1.8], [xc + 1.8, 5.0, zc + 1.8], mca, r=0.5)
        mpe = mat_tons(CANELA_CLARA, CANELA, mix(CANELA, MARROM_ESC, .5))
        mg = mat_tons(GARRA_CLARA, GARRA, GARRA_ESC, lado=mix(GARRA, GARRA_ESC, .4))
        pp.append(peca("pe_" + s, [xc - 2.4, 0.0, zc - 2.4], [xc + 2.4, 1.4, zc + 1.8], mpe))
        for nome, giro, dx in (("meio", 0, 0), ("fora", -14 * lado, 2.0 * lado), ("dentro", 14 * lado, -2.0 * lado)):
            x0, z0 = xc + dx, zc - 2.2
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - .8, 0, z0 - 2.8], [x0 + .8, 1.4, z0 + 0.3], mpe),
                peca(f"garra_{nome}_{s}", [x0 - .85, 0.0, z0 - 5.0], [x0 + .85, 1.9, z0 - 2.7], mg)]))
        pp.append(peca("dedo_tras_" + s, [xc - .7, 0, zc + 1.6], [xc + .7, 1.2, zc + 3.0], mpe))
        pp.append(peca("garra_tras_" + s, [xc - .8, 0, zc + 2.9], [xc + .8, 1.5, zc + 4.4], mg))
        return osso("perna_" + s, [xc, 9.0, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
