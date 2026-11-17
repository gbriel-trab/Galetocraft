"""Taturico (#007, Terra): o galo-tatu das rochas, robusto e defensivo, coberto por uma carapaça de faixas.

Refação (a versão anterior foi rejeitada como "estranha"). Medidas tiradas das 4 vistas da ficha (altura 39,2 u):
pés 0..3, pernas até 9, corpo 8,5..31,5 (z -14 no peito), cabeça 20..33,5 (z -18..-3), crista até 39,2,
bico até z -21; largura de frente 28,7 (placas dos ombros).

Como cada elemento da ficha foi resolvido (cores = paleta da ficha, amostrada com PIL):
- CARAPAÇA: 5 cintas curvas sobrepostas (arcos de placas giradas, como as cintas de um tatu), cada uma um pouco
  mais baixa que a da frente. Cada placa tem duas cores chapadas, marrom-malva #8f4f3f e laranja-tan #ed9f5e,
  num xadrez de blocos grandes por fora; de trás e de frente, a beirada é marrom em cima e laranja embaixo
  (arcos empilhados como na traseira da ficha). Nada mais escuro que #572d27.
- CAUDA BLINDADA: cone de 5 anéis fechados que diminuem, inclinado ~25° para baixo e terminando numa ponta laranja
  (cada anel é um osso cauda_anel_k, para ondular).
- ELMO ROCHOSO: 3 cintas em arco sobre a cabeça (mesma regra de cores) + aba em V marrom-malva com blocos laranja
  sobre os olhos (a cara brava vem só da aba).
- ROSTO (expressão neutra da ficha): creme #fcdfbe em volta do olho, só uma linha marrom na pálpebra de baixo; olho
  redondo com íris dourada #f7bc0a, pupila preta grande para a frente, brilho e esclera clara atrás; bico GRANDE em
  cunha (de frente: trapézio de ~1/3 da cara que afina para baixo; de lado: comprido, gancho para baixo e narina
  preta), amarelo #fca702/#f7bc0a em cima e laranja embaixo; barbelas largas #cf2523 quase verticais até o meio
  do peito; placas da cabeça da altura do olho até a base do bico, com o meandro de ângulos retos na frente e a
  moldura com fenda no lado.
- PEITO: creme quente #fcdfbe em fileiras de penas em escama + saia de penas-bloco.
- OMBRO: placa grossa com o emblema da ficha em traço grosso e ângulos retos (moldura + dente).
- PATAS FORTES: pernas #fca702 curtas e grossas, 3 dedos amarelos com garra cinza-malva #7f5e67 na ponta e 1 atrás.
"""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, clamp, na_borda

ID = "taturico"; NOME = "Taturico"; NUMERO = 7
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 24.5, -15.5), 8.6)
ONDAS = [("cauda_anel", 5, (1.2, 2.5, 0))]
ANIM_PARADO = {"barbela": [(0, 0, 0), (5, 0, 2), (0, 0, 0), (4, 0, -2), (0, 0, 0)]}
ANIM_ANDANDO = {"barbela": [(0, 0, 0), (9, 0, 4), (0, 0, 0), (9, 0, -4), (0, 0, 0)]}

# ---------------- paleta (quadro "Paleta de Cores" da ficha, amostrado com PIL) ----------------
CREME = (252, 223, 190); CREME_SOM = (234, 196, 158)        # #fcdfbe
LARANJA = (237, 159, 94); LARANJA_SOM = (205, 116, 62)      # #ed9f5e / #cd743e
MALVA = (143, 79, 63); MALVA_ESC = (106, 58, 48)            # #8f4f3f / entre #8f4f3f e #5a2f29
PISO = (87, 45, 39)                                         # #572d27: nada da carapaça fica mais escuro
VERM = (207, 37, 35); VERM_CL = (240, 76, 66); VERM_ESC = (160, 22, 24)   # #cf2523
AMARELO = (252, 167, 2); AMARELO_CL = (247, 188, 10)        # #fca702 / #f7bc0a
LARANJA_BICO = (236, 128, 8)
CINZA = (127, 94, 103); CINZA_CL = (152, 120, 128)          # #7f5e67
PRETO = (20, 10, 8)

def tom(c, f):
    """Luz quente: f > 0 clareia para um creme quente, f < 0 escurece para um marrom-avermelhado."""
    f = clamp(f, -1, 1)
    if f >= 0: return mix(c, (255, 240, 214), f * 0.35)
    return mix(c, (int(c[0] * .45), int(c[1] * .32), int(c[2] * .26)), -f)

def piso(c):
    """Não deixa a carapaça ficar mais escura que #572d27 (a ficha não tem pixels quase pretos)."""
    if sum(c) >= sum(PISO): return c
    return PISO

def lado_s(lado): return "d" if lado < 0 else "e"

# ---------------- luz chapada por face ----------------
def luz_face(c, curva=0.12, borda=0.14, cima=0.12, baixo=0.3, frente=0.0):
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

# ---------------- cintas da carapaça (placas curvas) ----------------
def mat_placa_cinta(k, m, baixa, T, my):
    """Placa de uma cinta, pintada nas coordenadas da caixa ANTES de girar:
    - face de fora ('up'): xadrez de blocos grandes (metade do comprimento x metade da profundidade), laranja e
      marrom-malva; as placas de baixo usam os tons de sombra da paleta;
    - beirada de trás e da frente: marrom-malva na metade de fora, laranja na de dentro (arcos empilhados);
    - face de dentro e pontas: marrom-malva escuro."""
    claro, escuro = (LARANJA_SOM, MALVA_ESC) if baixa else (LARANJA, MALVA)
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        (bx0, by0, bz0), (bx1, by1, bz1) = c["b"]
        luz = -0.08 if na_borda(c) else 0.0
        if face == "up":
            hl = 1 if (x - bx0) / max(bx1 - bx0, 1e-6) >= 0.5 else 0
            hz = 1 if (z - bz0) / max(bz1 - bz0, 1e-6) >= 0.5 else 0
            cor = claro if (hl + hz + abs(m) + k) % 2 == 0 else escuro
            luz += 0.06
        elif face in ("south", "north"):
            fora = (y - (my - T)) / T >= 0.5
            cor = escuro if fora else claro
            if face == "north": luz -= 0.04
        elif face == "down":
            cor = MALVA_ESC; luz -= 0.1
        else:
            cor = escuro
        return piso(tom(cor, luz))
    return f

# contorno das cintas (fração da meia largura, fração da altura abaixo do topo): o fim do arco volta para dentro,
# então de trás o corpo fica em ovo / pinha (estreito em cima, largo no meio, fechando embaixo)
ARCO = [(0.0, 0.0), (0.33, -0.03), (0.61, -0.1), (0.82, -0.24), (0.96, -0.45), (1.02, -0.66), (0.97, -0.86), (0.86, -1.0)]
ARCO_ELMO = [(0.0, 0.0), (0.55, -0.04), (0.86, -0.2), (1.0, -0.55), (1.02, -1.0)]

def placa(nome, a, b, z0, z1, T, mat, res=2, folga=0.3):
    """Caixa de espessura T entre os pontos a e b do contorno (o lado de fora fica na linha a-b), girada em z."""
    (xa, ya), (xb, yb) = a, b
    dx, dy = xb - xa, yb - ya
    comp = math.hypot(dx, dy) + folga
    ang = math.degrees(math.atan2(dy, dx))
    mx, my = (xa + xb) / 2, (ya + yb) / 2
    return peca(nome, [mx - comp / 2, my - T, z0], [mx + comp / 2, my, z1], mat(my), rot=(0, 0, ang),
                pivo=(mx, my, (z0 + z1) / 2), res=res)

def cinta(nome, k, z0, z1, W, yb, yt, T, arco=ARCO):
    """Cinta aberta em arco sobre o dorso (do lado direito ao esquerdo, até a altura yb), feita de placas giradas."""
    H = yt - yb
    pts = [(W * a, yt + H * b) for a, b in arco]
    n = len(pts) - 1
    out = []
    def mat_m(m):
        return lambda my: mat_placa_cinta(k, m, abs(m) >= n - 1, T, my)
    e = lambda m: 0.03 * (abs(m) % 2)                         # afasta as pontas vizinhas (sem z-fighting)
    out.append(placa(f"{nome}_0", (-pts[1][0], pts[1][1]), pts[1], z0, z1, T, mat_m(0), folga=0.05))
    for i in range(1, n):
        out.append(placa(f"{nome}_+{i}", pts[i], pts[i + 1], z0 - e(i), z1 + e(i), T, mat_m(i)))
        out.append(placa(f"{nome}_-{i}", (-pts[i + 1][0], pts[i + 1][1]), (-pts[i][0], pts[i][1]), z0 - e(i), z1 + e(i), T, mat_m(-i)))
    return out

def anel_fechado(nome, k, z0, z1, W, H, yc, T, n=8):
    """Anel fechado (cauda): polígono de n placas em volta do eixo z, percorrido no sentido horário."""
    pts = [(W * math.cos(math.radians(90 - 360 * i / n)), yc + H * math.sin(math.radians(90 - 360 * i / n))) for i in range(n + 1)]
    out = []
    for i in range(n):
        m = min(i, n - i)
        mt = (lambda m_: (lambda my: mat_placa_cinta(k, m_, m_ >= 3, T, my)))(m)
        out.append(placa(f"{nome}_{i}", pts[i], pts[i + 1], z0 - 0.03 * (i % 2), z1 + 0.03 * (i % 2), T, mt, folga=0.25))
    return out

# ---------------- glifos (traço grosso, ângulos retos, como na ficha) ----------------
EMBLEMA_OMBRO = ["#####",      # moldura laranja grossa; dentro, o "dente" escuro em ∩ e o toco laranja do meio
                 "#...#",
                 "#.#.#",
                 "#####"]
MEANDRO_CAB = ["#####",        # face da frente da placa da cabeça: meandro de ângulos retos
               "....#",
               "###.#",
               "#.#.#",
               "#...#",
               "#####"]
FENDA_CAB = ["#######",        # face do lado da placa da cabeça: moldura com fenda escura no meio
             "#.....#",
             "#.....#",
             "#######"]

def glifo(c, bitmap, margem=0.13, espelha=False):
    u = (c["i"] + .5) / c["tw"]; v = (c["j"] + .5) / c["th"]
    if espelha: u = 1 - u
    a = (u - margem) / (1 - 2 * margem); b = (v - margem) / (1 - 2 * margem)
    if not (0 <= a < 1 and 0 <= b < 1): return "fundo"
    return "traco" if bitmap[int(b * len(bitmap))][int(a * len(bitmap[0]))] == "#" else "fundo"

def mat_placa_glifo(glifos, espelha=False, margem=0.12):
    """Placa marrom-malva grossa; 'glifos' = {face: bitmap} desenhados em laranja #ed9f5e."""
    def f(c):
        bm = glifos.get(c["face"])
        if bm:
            r = glifo(c, bm, margem=margem, espelha=espelha)
            v = (c["j"] + .5) / c["th"]
            base = LARANJA if r == "traco" else MALVA
            luz = 0.04 - 0.1 * v
            if na_borda(c): luz -= 0.2
            return piso(tom(base, luz))
        return piso(tom(MALVA, luz_face(c, borda=.18)))
    return f

def mat_aba():
    """Aba do elmo: marrom-malva com um bloco laranja a cada três (blocos de 2,9 u ao longo de x)."""
    def f(c):
        idx = int(math.floor(abs(c["p"][0]) / 2.9))
        base = LARANJA if idx % 3 == 1 else MALVA
        return piso(tom(base, luz_face(c, curva=0.15, borda=0.18)))
    return f

# ---------------- cabeça ----------------
OLHO_Y = 25.4
FAC_T = 1.6
FAC_A, FAC_B = (2.7, -16.3), (6.6, -12.4)          # a faceta do olho vai de A (junto do bico) a B (lado da cabeça)
FAC_S = ((FAC_A[0] + FAC_B[0]) / 2, (FAC_A[1] + FAC_B[1]) / 2)
FAC_C = (FAC_S[0] - 0.7071 * FAC_T / 2, FAC_S[1] + 0.7071 * FAC_T / 2)
FAC_L = math.hypot(FAC_B[0] - FAC_A[0], FAC_B[1] - FAC_A[1]) + 0.3
ABA_Y, ABA_ANG = 26.0, 16
K_CAB, K_CAB_C = 1.07, (0.0, 22.0, -13.0)            # escala da cabeça inteira (ajuste fino)

def olho(u, v):
    """Olho redondo da expressão neutra: íris dourada grande, pupila preta (~40% do olho) puxada para o bico,
    brilho branco, esclera clara atrás e a pálpebra de baixo marrom. u < 0 = para o bico."""
    ru, rv = 1.8, 1.75
    e = (u / ru) ** 2 + (v / rv) ** 2
    if e > 1: return None
    iu, iv = u / ru + 0.2, v / rv
    if ((iu - 0.16) / 0.15) ** 2 + ((iv - 0.32) / 0.15) ** 2 <= 1: return (255, 255, 255)
    if (iu / 0.38) ** 2 + (iv / 0.42) ** 2 <= 1: return PRETO
    if (iu / 0.74) ** 2 + (iv / 0.8) ** 2 <= 1: return mix(AMARELO_CL, (214, 140, 6), clamp((0.6 - iv) / 1.4))
    if e > 0.84: return MALVA if v < 0 else CREME_SOM
    return mix((252, 246, 236), (226, 214, 198), clamp(-v / rv))

def mat_faceta(lado):
    """Faceta a 45°: creme #fcdfbe com o olho inteiro na face de fora e a linha marrom da pálpebra de baixo."""
    fora = "east" if lado > 0 else "west"
    base = mat_chapado(lambda p, f: CREME if p[1] > OLHO_Y - 2.2 else CREME_SOM, borda=.05, curva=.14)
    def f(c):
        if c["face"] == fora:
            x, y, z = c["p"]
            u, v = z - FAC_C[1], y - OLHO_Y
            o = olho(u, v)
            if o is not None: return o
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face in ("east", "west") and -17.9 < z < -17.3 and 25.5 < y < 26.1: return PRETO        # narina
    if face == "up": return AMARELO_CL
    if face == "down": return LARANJA_BICO
    return mix(AMARELO_CL, AMARELO, clamp((26.0 - y) / 2.0))

def cabeca_pecas():
    cab = []
    fx = (20.0, 30.0)
    mcreme = mat_liso(CREME, borda=.06, curva=.2)
    cab.append(peca("cranio", [-7.4, 20.6, -12.2], [7.4, 29.0, -4.0], mat_liso(CREME_SOM, borda=.06), faixa=fx, res=2))
    cab.append(peca("rosto_frente", [-2.9, 20.4, -16.9], [2.9, 27.2, -12.6], mcreme, faixa=fx, res=4))
    for lado in (-1, 1):
        s = lado_s(lado)
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 20.6, cz - FAC_L / 2], [cx + FAC_T / 2, 27.6, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, OLHO_Y, cz), faixa=fx, res=8))
    # bico grande em cunha: de frente, trapézio de ~1/3 da cara que afina para baixo; de lado, comprido com gancho
    mb = mat_chapado(cor_bico, borda=.06, curva=.18)
    fb = (22.0, 26.4)
    cab.append(peca("bico_sup", [-1.9, 23.6, -20.0], [1.9, 26.2, -16.0], mb, faixa=fb, res=4))
    mflanco = mat_chapado(lambda p, f: AMARELO_CL if f == "up" else mix(AMARELO, LARANJA_BICO, 0.45), borda=.06, curva=.2)
    for lado in (-1, 1):
        x0, x1 = sorted((1.5 * lado, 2.8 * lado))
        cab.append(peca("bico_flanco_" + lado_s(lado), [x0, 24.2, -18.8], [x1, 26.1, -16.0], mflanco,
                        rot=(0, 24 * lado, 0), pivo=(1.5 * lado, 25.2, -16.0), faixa=fb, res=4))
    cab.append(peca("bico_ponta", [-1.25, 22.3, -21.0], [1.25, 25.4, -19.7], mb, rot=(-16, 0, 0), pivo=(0, 25.4, -19.7), faixa=fb, res=4))
    cab.append(peca("bico_inf", [-1.35, 22.2, -19.4], [1.35, 23.7, -16.0], mat_liso(LARANJA_BICO, borda=.1), res=4))
    # barbelas: duas placas vermelhas largas quase verticais, descendo até o meio do peito
    mv_ = mat_chapado(lambda p, f: mix(VERM_CL, VERM, clamp((22.4 - p[1]) / 3.0)), borda=.1, curva=.25)
    tiras = []
    for lado in (-1, 1):
        x0, x1 = sorted((0.25 * lado, 2.85 * lado))
        tiras.append(osso("barbela_" + lado_s(lado), [0.6 * lado, 22.4, -17.0], [0, 0, 8 * lado], [
            peca("barbela_" + lado_s(lado), [x0, 15.4, -18.6], [x1, 22.4, -15.6], mv_, faixa=(15.4, 22.4), res=4)]))
    cab.append(osso("barbela", [0, 22.6, -17.2], [0, 0, 0], tiras))          # osso animado (balança)
    # elmo: aba da frente em V (sobrancelha brava) + 3 cintas em arco até a nuca
    for lado in (-1, 1):
        x0, x1 = sorted((0.0, 8.0 * lado))
        cab.append(peca("elmo_aba_" + lado_s(lado), [x0, ABA_Y, -18.2], [x1, ABA_Y + 3.0, -14.6],
                        mat_aba(), rot=(0, 0, ABA_ANG * lado), pivo=(0, ABA_Y, -16.0), faixa=(ABA_Y, ABA_Y + 3.0), res=4))
    for k, (z0, z1, W, yb, yt) in enumerate([(-15.2, -10.6, 8.8, 26.6, 32.2), (-11.0, -6.2, 9.0, 26.2, 33.4),
                                             (-6.6, -2.6, 8.6, 25.6, 32.6)]):
        cab += cinta(f"elmo{k}", k + 1, z0, z1, W, yb, yt, 2.4, arco=ARCO_ELMO)
    cab.append(peca("elmo_miolo", [-6.4, 26.0, -15.0], [6.4, 31.0, -2.8], mat_liso(MALVA_ESC, borda=0), res=1))
    # placas da cabeça: da altura do olho até a base do bico, ladeando o rosto e salientes para a frente
    for lado in (-1, 1):
        x0, x1 = sorted((7.0 * lado, 11.0 * lado))
        fora = "east" if lado > 0 else "west"
        cab.append(peca("placa_cab_" + lado_s(lado), [x0, 20.8, -14.2], [x1, 27.0, -7.0],
                        mat_placa_glifo({"north": MEANDRO_CAB, fora: FENDA_CAB}, espelha=lado < 0),
                        rot=(0, 10 * lado, 0), pivo=(9.0 * lado, 23.9, -10.6), res=5))
    # crista vermelha em blocos: lâmina do meio (3 degraus inclinados para trás) + 2 lâminas dos lados
    mcr = mat_chapado(lambda p, f: mix(VERM_CL, VERM, clamp((38.5 - p[1]) / 6.5)) if f != "down" else VERM_ESC, borda=.14, curva=.3)
    crista = [
        peca("crista_bico", [-1.7, 30.4, -18.0], [1.7, 33.6, -14.2], mcr, faixa=(30, 38.1)),
        peca("crista_frente", [-1.7, 31.6, -14.6], [1.7, 36.8, -11.2], mcr, faixa=(30, 38.1)),
        peca("crista_meio", [-1.7, 32.4, -11.6], [1.7, 38.1, -6.4], mcr, faixa=(30, 38.1)),
        peca("crista_tras", [-1.7, 31.6, -6.8], [1.7, 37.0, -1.6], mcr, faixa=(30, 38.1)),
    ]
    for lado in (-1, 1):
        x0, x1 = sorted((1.6 * lado, 5.0 * lado))
        crista.append(peca("crista_lado_" + lado_s(lado), [x0, 32.4, -12.0], [x1, 35.4, -4.6], mcr, faixa=(30, 38.1)))
    cab.append(osso("crista", [0, 32.0, -8.0], [0, 0, 0], crista))
    return cab

# ---------------- peito ----------------
def mat_escamas(y0, y1, larg=2.4, ponta=1.4):
    """Fileira de penas do peito numa peça só: tiras verticais de 'larg' unidades; embaixo, as pontas das penas
    (alternando comprimento) num creme sombreado com um fio entre elas: lê como penas em escama."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        a = x if face in ("north", "south", "up", "down") else z
        idx = int(math.floor(a / larg))
        fr = a / larg - idx
        lim = y0 + ponta + (0.7 if idx % 2 else 0.0)
        luz = luz_face(c, curva=0.14, borda=0.12, cima=0.05)
        if face in ("up", "down"): return tom(CREME, luz)
        if y < lim:
            cor = CREME_SOM
            if fr < 0.1: luz -= 0.12
        else:
            cor = CREME
            if y - lim < 0.3: luz -= 0.1          # fio de sombra da pena de cima
        return tom(cor, luz)
    return f

def peito_pecas():
    pp = []
    for k, (y0, y1, z0, z1, w) in enumerate([(18.4, 22.0, -16.8, -11.0, 5.6), (15.2, 19.0, -15.2, -9.0, 6.4),
                                             (12.0, 15.8, -13.8, -8.0, 7.0)]):
        pp.append(peca(f"peito{k}", [-w, y0, z0], [w, y1, z1], mat_escamas(y0, y1), faixa=(y0, y1), res=4))
    n, w, y0, y1 = 6, 7.2, 8.8, 12.6
    larg = 2 * w / n
    for i in range(n):
        x0 = -w + i * larg
        alonga = 0.8 if i % 2 == 0 else 0.0
        pp.append(peca(f"saia{i}", [x0 + 0.03, y0 - alonga, -11.6], [x0 + larg - 0.03, y1, -5.0],
                       mat_escamas(y0 - alonga, y1, larg=larg, ponta=1.2), faixa=(y0 - alonga, y1), res=2))
    return pp

# ---------------- cauda ----------------
def cauda_blindada():
    """Cone de 5 anéis fechados encaixados, cada um menor que o anterior, inclinado ~25° para baixo e terminando
    numa ponta laranja; cada anel é um osso (cauda_anel_k) filho do anterior."""
    ANEIS = [(8.0, 5.8, 3.0), (6.5, 4.7, 2.7), (5.0, 3.6, 2.5), (3.7, 2.7, 2.3), (2.4, 1.8, 2.1)]   # (meia larg., meia alt., compr.)
    PASSO = 1.9
    Z0, YC = 14.6, 14.2
    def seg(k, z0):
        W, H, L = ANEIS[k]
        filhos = anel_fechado(f"cauda_anel{k}", k + 1, z0, z0 + L, W, H, YC, min(2.4, H * 0.75))
        if k + 1 < len(ANEIS): filhos.append(seg(k + 1, z0 + PASSO))
        else:   # ponta laranja afiada
            mp = mat_liso(LARANJA, borda=.15)
            filhos += [peca("cauda_ponta", [-1.3, YC - 1.0, z0 + L - 0.3], [1.3, YC + 1.0, z0 + L + 1.4], mp, faixa=(YC - 1, YC + 1)),
                       peca("cauda_ponta2", [-0.6, YC - 0.5, z0 + L + 1.2], [0.6, YC + 0.5, z0 + L + 2.4], mp, faixa=(YC - 1, YC + 1))]
        return osso(f"cauda_anel_{k}", [0, YC, z0], [0, 0, 0], filhos)
    return osso("cauda", [0, YC, Z0], [28, 0, 0], [seg(0, Z0)])

# ---------------- montagem ----------------
def montar():
    # ======================= CABEÇA E PESCOÇO =======================
    i_cab = len(g.PECAS)
    cabeca = osso("cabeca", [0, 22.0, -9.0], [0, 0, 0], cabeca_pecas())
    g.transformar(i_cab, [cabeca], K_CAB_C, k=K_CAB)          # ajuste fino do tamanho da cabeça inteira
    pescoco = osso("pescoco", [0, 18.0, -8.0], [0, 0, 0], [
        peca("pescoco", [-5.4, 15.0, -14.0], [5.4, 23.0, -6.0], mat_liso(CREME, borda=.04), faixa=(15, 23)),
        cabeca])

    # ======================= CORPO =======================
    corpo = []
    corpo.append(peca("tronco", [-10.0, 8.0, -6.5], [10.0, 26.0, 13.0], mat_liso(MALVA_ESC, borda=0), faixa=(8, 27)))
    corpo += peito_pecas()
    # carapaça: 5 cintas curvas sobrepostas, da nuca até a garupa
    CINTAS = [  # (z0, z1, meia largura, y baixo, y alto, espessura)
        (-5.6, -0.8, 12.2, 9.0, 31.4, 3.2),
        (-1.6, 3.4, 13.0, 8.6, 31.2, 3.4),
        (2.6, 7.8, 13.5, 8.4, 30.2, 3.4),
        (7.0, 11.6, 13.0, 8.4, 28.0, 3.4),
        (10.8, 15.0, 11.6, 8.6, 25.4, 3.2),
        (13.8, 17.0, 9.4, 8.6, 21.6, 3.0),
    ]
    for k, (z0, z1, W, yb, yt, T) in enumerate(CINTAS):
        corpo += cinta(f"cinta{k}", k, z0, z1, W, yb, yt, T)

    # asas: 2 blocos na frente do ombro (quase colados ao peito) + a placa grossa com o emblema
    for lado in (-1, 1):
        s = lado_s(lado)
        asa = []
        for k, (y0, y1, z0, z1) in enumerate([(15.0, 22.4, -11.0, -2.0), (8.6, 15.4, -10.2, -1.0)]):
            a0, a1 = sorted((8.4 * lado, 12.4 * lado))
            asa.append(peca(f"asa_bloco{k}_{s}", [a0, y0, z0], [a1, y1, z1],
                            mat_placa_cinta(k, 1, k == 1, y1 - y0, y1), faixa=(y0, y1), res=2))
        fora = "east" if lado > 0 else "west"
        cx, cz = 13.0 * lado, -2.0
        asa.append(peca("ombro_placa_" + s, [cx - 1.1, 10.2, cz - 7.0], [cx + 1.1, 22.0, cz + 7.0],
                        mat_placa_glifo({fora: EMBLEMA_OMBRO}, espelha=lado < 0), rot=(6, 0, 5 * lado), pivo=(cx, 16.1, cz), res=4))
        corpo.append(osso("asa_" + s, [11.0 * lado, 21.0, -2.0], [0, 0, 0], asa))

    corpo.append(cauda_blindada())
    corpo.append(pescoco)
    tronco = osso("corpo", [0, 9.0, 0.0], [0, 0, 0], corpo)

    # ======================= PERNAS =======================
    def perna(lado):
        s = lado_s(lado); xc = 6.6 * lado; zc = 0.0
        pp = []
        mam = mat_chapado(lambda p, f: AMARELO_CL if f == "up" else AMARELO, borda=.12, curva=.15)
        pp += g.arredondado("perna_" + s, [xc - 3.5, 3.4, zc - 4.2], [xc + 3.5, 9.6, zc + 4.2], mam, r=0.6, faixa=(0, 9.6))
        pp.append(peca("calcanhar_" + s, [xc - 3.7, 0.0, zc - 3.8], [xc + 3.7, 3.8, zc + 4.0], mam, faixa=(0, 9.6)))
        mg = mat_chapado(lambda p, f: CINZA_CL if f == "up" else CINZA, borda=.16, curva=.2)
        for k, dx in enumerate((-2.75, 0.0, 2.75)):          # 3 dedos amarelos, cada um com a garra cinza na ponta
            x = xc + dx
            pp.append(peca(f"dedo{k}_{s}", [x - 1.25, 0.0, zc - 7.6], [x + 1.25, 3.0, zc - 3.6], mam, faixa=(0, 9.6)))
            pp.append(peca(f"garra{k}_{s}", [x - 1.15, 0.0, zc - 9.7], [x + 1.15, 2.6, zc - 7.4], mg, faixa=(0, 2.6)))
        pp.append(peca("garra_tras_" + s, [xc - 1.5, 0.0, zc + 3.8], [xc + 1.5, 2.8, zc + 7.0], mg, faixa=(0, 2.8)))
        return osso("perna_" + s, [xc, 9.6, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
