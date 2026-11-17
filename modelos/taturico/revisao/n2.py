"""Taturico (#007, Terra): o galo-tatu das rochas, robusto e defensivo, coberto por uma carapaça de faixas.

Refação (a versão anterior foi rejeitada como "estranha"). Medidas tiradas das 4 vistas da ficha (altura 39,2 u):
pés 0..3, pernas até 9, corpo 8,5..31,5 (z -14 no peito até +21 na ponta da cauda), cabeça 20..33,5 (z -18..-3),
crista até 39,2, bico até z -20,6; largura de frente 28,7 (placas dos ombros).

Como cada elemento da ficha foi resolvido:
- CARAPAÇA: anéis grossos em degrau (perfil de 3 caixas com quinas em escada) da nuca até a garupa. A cor de cada
  bloco depende do ângulo em volta do eixo do corpo (célula de cima larga, depois células de ~35°), alternando
  caramelo / marrom de um anel para o outro: de trás leem como faixas horizontais limpas; de lado, como as colunas
  em xadrez grande da ficha. Sem ruído: 3 tons chapados por bloco (topo claro, lado base, embaixo sombra) e fio escuro.
- CAUDA BLINDADA: cone de anéis menores e mais baixos, cada um um osso (cauda_anel_k) para ondular.
- ELMO ROCHOSO: faixas em arco sobre a cabeça, a da frente partida em V (sobrancelha brava) descendo até a testa,
  por cima dos olhos; placas com a espiral quadrada dos lados da cabeça.
- ROSTO: frente creme pequena só em volta do bico; olho amarelo inteiro numa faceta a 45° (como o Pirococó), com a
  órbita marrom-malva e o alto cortado pela aba do elmo; bico pequeno amarelo em cunha com gancho; barbela vermelha
  em duas tiras finas que abrem em V.
- PEITO: creme, em 3 fileiras de penas-bloco em escama (cada pena com a ponta mais escura), recuando para baixo.
- OMBRO: placa grossa com a espiral quadrada sobre 2 blocos de asa em faixas.
- PATAS FORTES: coluna amarela curta e grossa, pé amarelo, 3 garras cinza na frente e 1 atrás.
"""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, pintar_olho, na_borda

ID = "taturico"; NOME = "Taturico"; NUMERO = 7
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 25.5, -14.5), 9.5)
ONDAS = [("cauda_anel", 4, (1.2, 2.5, 0))]
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (Paleta de Cores da ficha) ----------------
CREME = (250, 224, 192); CREME_SOM = (222, 186, 148)
CARAMELO = (236, 158, 92); CARAMELO_CL = (250, 190, 130)
MARROM = (142, 80, 64); MARROM_ESC = (92, 50, 42)
MALVA = (136, 96, 92)                    # pele em volta do olho
VERM = (210, 36, 34); VERM_CL = (238, 70, 58); VERM_ESC = (150, 20, 24)
AMARELO = (252, 182, 18); AMARELO_CL = (255, 214, 70); AMARELO_ESC = (222, 134, 10)
CINZA = (112, 94, 102); CINZA_CL = (146, 128, 136)
PRETO = (24, 12, 14)

def lado_s(lado): return "d" if lado < 0 else "e"

# ---------------- luz chapada por face ----------------
def luz_face(c, curva=0.22, borda=0.18, cima=0.18, baixo=0.36, frente=0.0):
    """3 tons por bloco: face de cima clara, lados na cor base (leve degradê na faixa), de baixo em sombra;
    fio escuro na borda de cada face."""
    y0, y1 = c["faixa"]
    t = clamp((c["p"][1] - y0) / max(y1 - y0, 1e-6))
    luz = -curva / 2 + curva * t
    f = c["face"]
    if f == "up": luz += cima
    elif f == "down": luz -= baixo
    elif f == "north": luz += frente
    if na_borda(c): luz -= borda
    return luz

def mat_chapado(cor_fn, **kw):
    def f(c):
        base = cor_fn(c["p"], c["face"])
        return None if base is None else tom(base, luz_face(c, **kw))
    return f

def mat_liso(cor, **kw): return mat_chapado(lambda p, f: cor, **kw)

# ---------------- anéis da carapaça ----------------
def mat_anel(k, yt, cel, claro=CARAMELO, escuro=MARROM):
    """Bloco de anel: faixas HORIZONTAIS pela altura, contadas do alto do anel (yt) em degraus de 'cel' unidades,
    alternando caramelo / marrom; a paridade muda de um anel para o outro (k). De trás: faixas limpas em arco;
    de lado: colunas em xadrez grande, como na ficha."""
    def f(c):
        y = c["p"][1]
        idx = int(math.floor((yt - y) / cel + 1e-6))
        base = claro if (idx + k) % 2 == 0 else escuro
        luz = luz_face(c, curva=0.2, borda=0.2, frente=-0.06)
        if c["face"] == "south": luz += 0.05
        return tom(base, luz)
    return f

def mat_celulas_x(k, cel, claro=CARAMELO, escuro=MARROM):
    """Blocos alternados ao longo de x (aba do elmo)."""
    def f(c):
        idx = int(math.floor(abs(c["p"][0]) / cel))
        base = claro if (idx + k) % 2 == 0 else escuro
        return tom(base, luz_face(c, curva=0.2, borda=0.22))
    return f

PERFIL_CORPO = [(1.0, 0.08, 0.55), (0.88, 0.03, 0.76), (0.70, 0.0, 0.92), (0.46, 0.0, 1.0)]   # (largura, de, até) em frações
PERFIL_ELMO = [(1.0, 0.0, 0.42), (0.88, 0.0, 0.74), (0.62, 0.0, 1.0)]

def anel(nome, k, z0, z1, W, yb, yt, perfil=PERFIL_CORPO, mat=None, cel=None, res=2):
    """Anel grosso em degrau (eixo z): caixas cada vez mais estreitas e mais altas (quinas em escada).
    yb/yt = baixo/alto; W = meia largura. Cada caixa sai um pouco mais para a frente e para trás (sem z-fighting)."""
    h = yt - yb
    m = mat or mat_anel(k, yt, cel or max(2.2, h / 5.2))
    fx = (yb, yt)
    out = []
    for i, (fw, fa, fb) in enumerate(perfil):
        e = 0.04 * i
        out.append(peca(f"{nome}_{i}", [-W * fw, yb + fa * h, z0 - e], [W * fw, yb + fb * h, z1 + e], m, faixa=fx, res=res))
    return out

# ---------------- glifo: espiral quadrada ----------------
ESPIRAL = ["#########",
           "#.......#",
           "#.#####.#",
           "#.#...#.#",
           "#.#.#.#.#",
           "#.#.###.#",
           "#.#.....#",
           "#.#######",
           "#........"]

def glifo(c, bitmap, margem=0.13, espelha=False):
    u = (c["i"] + .5) / c["tw"]; v = (c["j"] + .5) / c["th"]
    if espelha: u = 1 - u
    a = (u - margem) / (1 - 2 * margem); b = (v - margem) / (1 - 2 * margem)
    if not (0 <= a < 1 and 0 <= b < 1): return "fundo"
    n = len(bitmap)
    return "traco" if bitmap[int(b * n)][int(a * n)] == "#" else "fundo"

def mat_placa_glifo(face_glifo, espelha=False):
    """Placa marrom grossa com a espiral quadrada caramelo na face 'face_glifo'."""
    def f(c):
        if c["face"] == face_glifo:
            r = glifo(c, ESPIRAL, espelha=espelha)
            v = (c["j"] + .5) / c["th"]
            base = CARAMELO if r == "traco" else MARROM
            luz = 0.06 - 0.16 * v
            if na_borda(c): luz -= 0.25
            return tom(base, luz)
        return tom(MARROM, luz_face(c, borda=.22))
    return f

# ---------------- cabeça ----------------
OLHO_Y = 25.0
FAC_T = 1.6
FAC_A, FAC_B = (2.6, -16.9), (6.6, -12.9)          # a faceta do olho vai de A (junto do bico) a B (lado da cabeça)
FAC_S = ((FAC_A[0] + FAC_B[0]) / 2, (FAC_A[1] + FAC_B[1]) / 2)
FAC_C = (FAC_S[0] - 0.7071 * FAC_T / 2, FAC_S[1] + 0.7071 * FAC_T / 2)
FAC_L = math.hypot(FAC_B[0] - FAC_A[0], FAC_B[1] - FAC_A[1]) + 0.3
ABA_Y, ABA_ANG = 26.0, 11                         # aba do elmo: altura da beirada de baixo no meio e inclinação do V

def olho(u, v):
    return pintar_olho(u, v, 1.55, 1.4, iris=((196, 110, 0), (255, 196, 30)), esclera=(250, 240, 222), pupila=PRETO,
                       r_iris=(0.6, 0.74), c_iris=(-0.26, -0.06), r_pup=(0.3, 0.38), bravo=0.32, alto=0.42,
                       contorno=(70, 40, 40))

def mat_faceta(lado):
    """Faceta a 45°: órbita malva com o olho inteiro na face de fora; creme só embaixo, junto do bico."""
    fora = "east" if lado > 0 else "west"
    def cor(p, face):
        x, y, z = p
        u = z - FAC_C[1]
        if y < OLHO_Y - 1.5 and u < 0.8: return CREME
        return MALVA
    base = mat_chapado(cor, borda=.06, curva=.2)
    def f(c):
        if c["face"] == fora:
            x, y, z = c["p"]
            o = olho(z - FAC_C[1], y - OLHO_Y)
            if o is not None: return o
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face in ("east", "west") and abs(z + 18.5) < 0.3 and abs(y - 25.9) < 0.3: return (110, 50, 10)   # narina
    if face == "down": return AMARELO_ESC
    return mix(AMARELO_CL, AMARELO, clamp((26.6 - y) / 2.6) * .7 + clamp((-z - 18) / 2.6) * .4)

def cabeca_pecas():
    cab = []
    fx = (20.0, 30.0)
    mcreme = mat_liso(CREME, borda=.08, curva=.25)
    # crânio (lados malva, embaixo creme) e frente creme pequena em volta do bico
    cab.append(peca("cranio", [-7.6, 20.6, -12.8], [7.6, 30.0, -3.2],
                    mat_chapado(lambda p, f: CREME if p[1] < 23.0 else MALVA, borda=.06), faixa=fx, res=2))
    cab.append(peca("rosto_frente", [-2.9, 20.4, -17.1], [2.9, 27.2, -12.6], mcreme, faixa=fx, res=4))
    for lado in (-1, 1):
        s = lado_s(lado)
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 20.6, cz - FAC_L / 2], [cx + FAC_T / 2, 27.6, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, OLHO_Y, cz), faixa=fx, res=8))
    # bico pequeno em cunha: base, meio e gancho; maxila de baixo mais escura
    mb = mat_chapado(cor_bico, borda=.08, curva=.25)
    fb = (22.4, 27.2)
    cab.append(peca("bico_base", [-2.2, 23.4, -18.7], [2.2, 27.0, -16.9], mb, faixa=fb, res=4))
    cab.append(peca("bico_meio", [-1.8, 23.6, -20.0], [1.8, 26.6, -18.5], mb, rot=(-10, 0, 0), pivo=(0, 26.6, -18.5), faixa=fb, res=4))
    cab.append(peca("bico_ponta", [-1.3, 22.8, -21.0], [1.3, 25.4, -19.8], mb, rot=(-24, 0, 0), pivo=(0, 25.4, -19.8), faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-1.7, 22.5, -18.9], [1.7, 23.5, -16.9], mat_liso(AMARELO_ESC, borda=.12), res=4))
    # barbela: duas tiras vermelhas finas pendendo e abrindo em V
    mv_ = mat_chapado(lambda p, f: mix(VERM_CL, VERM, clamp((22.5 - p[1]) / 5)), borda=.12, curva=.3)
    for lado in (-1, 1):
        x0, x1 = sorted((0.2 * lado, 2.0 * lado))
        cab.append(osso("barbela_" + lado_s(lado), [1.0 * lado, 22.6, -17.0], [0, 0, 20 * lado], [
            peca("barbela_" + lado_s(lado), [x0, 15.6, -17.9], [x1, 22.6, -16.4], mv_, faixa=(15.6, 22.6), res=4)]))
    # elmo: aba da frente em V (sobrancelha brava) + 3 faixas em arco até a nuca
    for lado in (-1, 1):
        x0, x1 = sorted((0.0, 8.9 * lado))
        cab.append(peca("elmo_aba_" + lado_s(lado), [x0, ABA_Y, -18.4], [x1, ABA_Y + 3.0, -13.6],
                        mat_celulas_x(0, 2.9), rot=(0, 0, ABA_ANG * lado), pivo=(0, ABA_Y, -16.0),
                        faixa=(ABA_Y, ABA_Y + 3.0), res=4))
    for k, (z0, z1, W, yb, yt) in enumerate([(-15.2, -10.6, 8.5, 27.2, 32.0), (-11.0, -6.2, 8.6, 26.4, 33.4), (-6.6, -2.6, 8.2, 25.6, 32.6)]):
        cab += anel(f"elmo{k}", k + 1, z0, z1, W, yb, yt, perfil=PERFIL_ELMO, cel=2.4, res=3)
    # placas com a espiral quadrada dos lados da cabeça (viradas um pouco para a frente)
    for lado in (-1, 1):
        cx, cz = 8.7 * lado, -8.4
        fora = "east" if lado > 0 else "west"
        cab.append(peca("placa_cab_" + lado_s(lado), [cx - 1.0, 22.6, cz - 3.4], [cx + 1.0, 29.0, cz + 3.4],
                        mat_placa_glifo(fora, espelha=lado < 0), rot=(0, 26 * lado, 0), pivo=(cx, 25.8, cz), res=6))
    # crista vermelha em blocos: lâmina do meio (3 degraus) + 2 lâminas dos lados mais baixas
    mcr = mat_chapado(lambda p, f: mix(VERM_CL, VERM, clamp((38.5 - p[1]) / 6.5)) if f != "down" else VERM_ESC, borda=.14, curva=.3)
    crista = [
        peca("crista_frente", [-1.7, 30.4, -18.0], [1.7, 35.2, -12.4], mcr, rot=(-14, 0, 0), pivo=(0, 31.0, -12.4), faixa=(30, 39.2)),
        peca("crista_meio", [-1.7, 32.4, -13.0], [1.7, 39.2, -6.8], mcr, faixa=(30, 39.2)),
        peca("crista_tras", [-1.7, 31.6, -7.4], [1.7, 37.2, -1.2], mcr, rot=(10, 0, 0), pivo=(0, 31.6, -7.4), faixa=(30, 39.2)),
    ]
    for lado in (-1, 1):
        x0, x1 = sorted((1.6 * lado, 5.0 * lado))
        crista.append(peca("crista_lado_" + lado_s(lado), [x0, 33.0, -11.6], [x1, 37.4, -5.0], mcr, faixa=(30, 39.2)))
    cab.append(osso("crista", [0, 32.0, -8.0], [0, 0, 0], crista))
    return cab

# ---------------- peito ----------------
def mat_pena_peito(y0, y1):
    """Pena-bloco do peito: creme, ponta de baixo mais escura (escama), fio escuro separando as penas."""
    def cor(p, face):
        t = clamp((p[1] - y0) / max(y1 - y0, 1e-6))
        return CREME_SOM if t < 0.28 else CREME
    return mat_chapado(cor, borda=.12, curva=.18)

def peito_pecas():
    pp = []
    FILEIRAS = [  # (y0, y1, z frente, profundidade, meia largura, n penas)
        (16.4, 21.4, -16.4, 4.0, 6.0, 5),
        (12.4, 17.2, -14.6, 4.2, 7.0, 6),
        (8.4, 13.2, -12.0, 4.2, 7.2, 6),
    ]
    for k, (y0, y1, zf, prof, w, n) in enumerate(FILEIRAS):
        larg = 2 * w / n
        for i in range(n):
            x0 = -w + i * larg
            alonga = 0.7 if (i + k) % 2 == 0 else 0.0
            dz = 0.05 * (i % 2)
            pp.append(peca(f"peito{k}_{i}", [x0 + 0.02, y0 - alonga, zf + dz], [x0 + larg - 0.02, y1, zf + prof + dz],
                           mat_pena_peito(y0 - alonga, y1), faixa=(y0 - alonga, y1), res=2))
    return pp

# ---------------- cauda ----------------
def cauda_blindada():
    """Cone de anéis encaixados, cada um menor e mais baixo; cada anel é um osso (cauda_anel_k) filho do anterior."""
    ANEIS = [  # (z0, z1, meia largura, y baixo, y alto)
        (14.2, 17.6, 9.2, 7.4, 20.6),
        (16.8, 19.4, 7.0, 7.2, 17.8),
        (18.6, 20.6, 5.0, 7.1, 15.6),
        (19.8, 21.4, 3.2, 7.3, 13.6),
    ]
    def seg(k):
        z0, z1, W, yb, yt = ANEIS[k]
        filhos = anel(f"cauda_anel{k}", k + 1, z0, z1, W, yb, yt, cel=2.6)
        if k + 1 < len(ANEIS): filhos.append(seg(k + 1))
        return osso(f"cauda_anel_{k}", [0, (yb + yt) / 2, z0], [0, 0, 0], filhos)
    return osso("cauda", [0, 14.0, 14.2], [0, 0, 0], [seg(0)])

# ---------------- montagem ----------------
def montar():
    # ======================= CABEÇA E PESCOÇO =======================
    cabeca = osso("cabeca", [0, 22.0, -9.0], [0, 0, 0], cabeca_pecas())
    pescoco = osso("pescoco", [0, 18.0, -8.0], [0, 0, 0], [
        peca("pescoco", [-6.2, 15.0, -15.6], [6.2, 23.0, -6.0], mat_liso(CREME, borda=.04), faixa=(15, 23)),
        cabeca])

    # ======================= CORPO =======================
    corpo = []
    corpo.append(peca("tronco", [-10.6, 8.6, -11.0], [10.6, 27.0, 12.0],
                      mat_chapado(lambda p, f: CREME if p[2] < -6 else MARROM, borda=.05), faixa=(8.6, 27)))
    corpo += peito_pecas()
    # carapaça: anéis em degrau da nuca até a garupa
    FAIXAS = [  # (z0, z1, meia largura, y baixo, y alto)
        (-5.4, -0.6, 12.6, 8.0, 31.2),
        (-1.4, 3.6, 13.2, 7.7, 31.8),
        (2.8, 8.0, 13.5, 7.6, 30.8),
        (7.2, 11.6, 13.0, 7.6, 28.6),
        (10.8, 15.0, 12.0, 7.6, 26.6),
    ]
    for k, (z0, z1, W, yb, yt) in enumerate(FAIXAS):
        corpo += anel(f"faixa{k}", k, z0, z1, W, yb, yt)

    # asas: 2 blocos em faixas na frente do ombro + a placa grossa com a espiral
    for lado in (-1, 1):
        s = lado_s(lado)
        asa = []
        for k, (y0, y1, z0, z1) in enumerate([(15.0, 22.4, -11.0, -2.0), (8.6, 15.4, -10.2, -1.0)]):
            a0, a1 = sorted((8.6 * lado, 12.9 * lado))
            asa += [peca(f"asa_bloco{k}_{s}", [a0, y0, z0], [a1, y1, z1],
                         mat_anel(k, y1, 3.6), faixa=(y0, y1), res=2)]
        fora = "east" if lado > 0 else "west"
        cx, cz = 13.6 * lado, -2.0
        asa.append(peca("ombro_placa_" + s, [cx - 1.1, 9.4, cz - 7.0], [cx + 1.1, 22.0, cz + 7.0],
                        mat_placa_glifo(fora, espelha=lado < 0), rot=(6, 4 * lado, 0), pivo=(cx, 15.7, cz), res=4))
        corpo.append(osso("asa_" + s, [11.0 * lado, 21.0, -2.0], [0, 0, 0], asa))

    corpo.append(cauda_blindada())
    corpo.append(pescoco)
    tronco = osso("corpo", [0, 9.0, 0.0], [0, 0, 0], corpo)

    # ======================= PERNAS =======================
    def perna(lado):
        s = lado_s(lado); xc = 6.6 * lado; zc = 0.0
        pp = []
        mam = mat_liso(AMARELO, borda=.14, curva=.3)
        pp += g.arredondado("perna_" + s, [xc - 3.5, 2.8, zc - 4.4], [xc + 3.5, 9.6, zc + 4.4], mam, r=0.6, faixa=(0, 9.6))
        pp.append(peca("pe_" + s, [xc - 3.8, 0.0, zc - 6.6], [xc + 3.8, 3.2, zc + 4.2], mam, faixa=(0, 9.6)))
        mg = mat_chapado(lambda p, f: CINZA_CL if f == "up" else CINZA, borda=.2, curva=.3)
        for k, dx in enumerate((-2.55, 0.0, 2.55)):
            x = xc + dx
            pp.append(peca(f"garra{k}_{s}", [x - 1.1, 0.0, zc - 10.0], [x + 1.1, 2.8, zc - 6.4], mg, faixa=(0, 2.8)))
        pp.append(peca("garra_tras_" + s, [xc - 1.5, 0.0, zc + 4.0], [xc + 1.5, 2.6, zc + 7.6], mg, faixa=(0, 2.6)))
        return osso("perna_" + s, [xc, 9.6, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
