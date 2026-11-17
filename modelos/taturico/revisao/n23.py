"""Taturico (#007, Terra): o galo-tatu das rochas, robusto e defensivo, coberto por uma carapaça de faixas.

Refação (a versão anterior foi rejeitada como "estranha"). Medidas tiradas das 4 vistas da ficha (altura 39,2 u):
pés 0..3, pernas até 9, corpo 8,5..31,5 (z -14 no peito até +21 na ponta da cauda), cabeça 20..33,5 (z -18..-3),
crista até 39,2, bico até z -20,6; largura de frente 28,7 (placas dos ombros).

Como cada elemento da ficha foi resolvido:
- CARAPAÇA: anéis grossos em degrau (perfil de 4 caixas com quinas em escada) da nuca até a garupa. A cor troca
  exatamente nos degraus (e a cada ~4 u abaixo deles), alternando caramelo / marrom e invertendo de um anel para o
  outro: de trás leem como faixas horizontais limpas; de lado, como as colunas em xadrez grande da ficha. Sem ruído:
  3 tons chapados por bloco (topo claro, lado base, embaixo sombra) e fio escuro na borda.
- CAUDA BLINDADA: cone de anéis menores e mais baixos, cada um um osso (cauda_anel_k) para ondular.
- ELMO ROCHOSO: faixas em arco sobre a cabeça, a da frente partida em V (sobrancelha brava) descendo até a testa,
  por cima dos olhos; placas com a espiral quadrada dos lados da cabeça.
- ROSTO: frente creme pequena só em volta do bico; olho amarelo inteiro numa faceta a 45° (como o Pirococó), com a
  órbita marrom-malva e o alto cortado pela aba do elmo; bico pequeno amarelo em cunha com gancho; barbela vermelha
  em duas tiras finas que abrem em V.
- PEITO: creme, 3 fileiras largas pintadas em escama + saia de 6 penas-bloco, recuando em degraus para baixo.
- OMBRO: placa grossa com a espiral quadrada sobre 2 blocos de asa em faixas.
- PATAS FORTES: coluna amarela curta e grossa, calcanhar e 3 dedos amarelos, 3 garras cinza na frente e 1 atrás.
"""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, clamp, pintar_olho, na_borda

ID = "taturico"; NOME = "Taturico"; NUMERO = 7
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 25.5, -15.0), 10.0)
ONDAS = [("cauda_anel", 3, (1.5, 3.0, 0))]
ANIM_PARADO = {"barbela": [(0, 0, 0), (5, 0, 2), (0, 0, 0), (4, 0, -2), (0, 0, 0)]}
ANIM_ANDANDO = {"barbela": [(0, 0, 0), (9, 0, 4), (0, 0, 0), (9, 0, -4), (0, 0, 0)]}

# ---------------- paleta (amostrada com PIL nos PNGs da ficha) ----------------
# (a luz do jogo e da prévia escurece os lados em 20-40%: as cores base ficam no lado claro das amostras)
CREME = (252, 210, 172); CREME_SOM = (230, 168, 118)      # bochecha (250,197,161)
PEITO = (246, 206, 162); PEITO_SOM = (222, 160, 108)      # peito creme-bronzeado (233,177,121)
CARAMELO = (242, 168, 104); CARAMELO_CL = (252, 196, 136) # faixa clara (237,159,94)
MARROM = (164, 86, 58); MARROM_ESC = (90, 34, 14)         # faixa marrom (155,79,41)-(157,82,63) e sombra
ROSTO_ESC = (116, 62, 36)                                 # pele em volta do olho (109,62,34)
ORBITA = (36, 10, 4)                                      # contorno do olho, quase preto
VERM = (236, 44, 40); VERM_CL = (255, 96, 86); VERM_ESC = (176, 16, 18)
AMARELO = (255, 196, 22); AMARELO_CL = (255, 222, 52); AMARELO_ESC = (232, 132, 10)
LARANJA_BICO = (232, 124, 10)
CINZA = (128, 96, 106); CINZA_CL = (156, 124, 134)
PRETO = (24, 8, 4)

def tom(c, f):
    """Luz quente: f > 0 clareia para um creme quente, f < 0 escurece para um marrom-avermelhado (as sombras da
    ficha são marrom-quase-preto, não roxas)."""
    f = clamp(f, -1, 1)
    if f >= 0: return mix(c, (255, 240, 214), f * 0.35)
    return mix(c, (int(c[0] * .42), int(c[1] * .28), int(c[2] * .2)), -f)

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

# ---------------- anéis da carapaça ----------------
# ---------------- desenho da carapaça lido da ficha ----------------
# modelos/taturico/grade_ficha.json (gerado por modelos/taturico/grade_ficha.py) guarda, para cada direção de face
# (north/east/south/west), uma grade de 1 x 1 unidade com a classe de cor que a ficha mostra naquele ponto da vista
# correspondente. As faces dos anéis seguem essa grade: as faixas ficam com a largura, a altura e a ordem de cores
# da ficha (de trás: clara, marrom, sombra; de lado: o xadrez grande no mesmo lugar).
import json
_GRADE_ARQ = Path(__file__).resolve().parents[2] / "modelos" / "taturico" / "grade_ficha.json"
GRADE = json.loads(_GRADE_ARQ.read_text(encoding="utf-8")) if _GRADE_ARQ.exists() else {}
COR_CLASSE = {"C": (242, 168, 104), "M": (168, 90, 62), "E": (112, 50, 30), "P": (60, 20, 8),
              "W": (250, 208, 158), "Y": (245, 160, 16), "R": (212, 38, 34), "G": (124, 94, 104)}

def classe_ficha(face, p, aceita="CMEPW"):
    g = GRADE.get(face)
    if not g: return None
    x, y, z = p
    h = z if face in ("east", "west") else x
    j = int(round(h - g["h0"])); i = int(round(g["y0"] - y))
    L = g["linhas"]
    if not (0 <= i < len(L) and 0 <= j < len(L[i])): return None
    k = L[i][j]
    return k if k in aceita else None

def mat_anel(k, limites, claro=CARAMELO, escuro=MARROM, W=None):
    """Bloco de anel. Nas faces laterais, de trás e da frente, a cor vem da grade lida da ficha (classe_ficha);
    onde a grade não cobre (e nas faces de cima/baixo), faixas horizontais separadas nas alturas 'limites', que
    coincidem com os degraus do perfil, alternando caramelo / marrom de um anel para o outro (k)."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        if face in ("east", "west", "south", "north"):
            kl = classe_ficha(face, c["p"])
            if kl:
                luz = -0.1 if na_borda(c) else 0.0
                return tom(COR_CLASSE[kl], luz)
        idx = sum(1 for L in limites if y < L - 1e-6)
        base = claro if (idx + k) % 2 == 0 else escuro
        return tom(base, luz_face(c, frente=-0.04))
    return f

def limites_perfil(perfil, yb, yt, cel):
    """Alturas onde a cor troca: nos degraus do perfil (menos o degrau do topo, fino demais) e, abaixo do último
    degrau, a cada ~'cel' unidades."""
    h = yt - yb
    tops = sorted({yb + fb * h for _, _, fb in perfil}, reverse=True)[1:]
    lim = tops[:]
    baixo = tops[-1] if tops else yt
    n = max(1, round((baixo - yb) / cel))
    passo = (baixo - yb) / n
    lim += [baixo - passo * i for i in range(1, n)]
    return lim

def mat_celulas_x(k, cel, claro=CARAMELO, escuro=MARROM):
    """Blocos alternados ao longo de x (aba do elmo)."""
    def f(c):
        idx = int(math.floor(abs(c["p"][0]) / cel))
        base = claro if (idx + k) % 2 == 0 else escuro
        return tom(base, luz_face(c, curva=0.2, borda=0.22))
    return f

PERFIL_CORPO = [(1.0, 0.07, 0.58), (0.88, 0.02, 0.8), (0.7, 0.0, 0.93), (0.46, 0.0, 1.0)]   # (largura, de, até) em frações
PERFIL_ELMO = [(1.0, 0.0, 0.55), (0.9, 0.0, 0.82), (0.72, 0.0, 1.0)]

def anel(nome, k, z0, z1, W, yb, yt, perfil=PERFIL_CORPO, mat=None, cel=None, res=2):
    """Anel grosso em degrau (eixo z): caixas cada vez mais estreitas e mais altas (quinas em escada).
    yb/yt = baixo/alto; W = meia largura. Cada caixa sai um pouco mais para a frente e para trás (sem z-fighting).
    As trocas de cor caem nos degraus do perfil: cada bloco visível tem uma cor só."""
    h = yt - yb
    m = mat or mat_anel(k, limites_perfil(perfil, yb, yt, cel or 4.2), W=W)
    fx = (yb, yt)
    out = []
    for i, (fw, fa, fb) in enumerate(perfil):
        e = 0.04 * i
        out.append(peca(f"{nome}_{i}", [-W * fw, yb + fa * h, z0 - e], [W * fw, yb + fb * h, z1 + e], m, faixa=fx, res=res))
    return out

# ---------------- glifos (desenhados como na ficha) ----------------
EMBLEMA_OMBRO = ["..#########..",   # moldura caramelo grossa de cantos arredondados + toco subindo do meio de baixo
                 ".###########.",
                 "###.......###",
                 "###.......###",
                 "##.........##",
                 "##.........##",
                 "##...###...##",
                 "##...###...##",
                 "##...###...##",
                 "###..###..###",
                 "#############",
                 ".###########.",
                 "..#########.."]
ESPIRAL_G = [".#######.",          # placa da cabeça: espiral em "G" de cantos arredondados
             "##.....##",
             "#.......#",
             "#...#####",
             "#...#...#",
             "#...#.#.#",
             "#.....#.#",
             "##....#.#",
             ".######.."]

def glifo(c, bitmap, margem=0.13, espelha=False):
    u = (c["i"] + .5) / c["tw"]; v = (c["j"] + .5) / c["th"]
    if espelha: u = 1 - u
    a = (u - margem) / (1 - 2 * margem); b = (v - margem) / (1 - 2 * margem)
    if not (0 <= a < 1 and 0 <= b < 1): return "fundo"
    n = len(bitmap)
    return "traco" if bitmap[int(b * n)][int(a * n)] == "#" else "fundo"

def mat_placa_glifo(face_glifo, espelha=False, bitmap=EMBLEMA_OMBRO, margem=0.12):
    """Placa marrom grossa com o glifo caramelo ('bitmap') na face 'face_glifo'."""
    def f(c):
        if c["face"] == face_glifo:
            r = glifo(c, bitmap, margem=margem, espelha=espelha)
            v = (c["j"] + .5) / c["th"]
            base = CARAMELO if r == "traco" else MARROM
            luz = 0.06 - 0.16 * v
            if na_borda(c): luz -= 0.25
            return tom(base, luz)
        return tom(MARROM, luz_face(c, borda=.22))
    return f

# ---------------- cabeça ----------------
OLHO_Y = 25.5
FAC_T = 1.6
FAC_A, FAC_B = (2.7, -16.5), (6.6, -12.6)          # a faceta do olho vai de A (junto do bico) a B (lado da cabeça)
FAC_S = ((FAC_A[0] + FAC_B[0]) / 2, (FAC_A[1] + FAC_B[1]) / 2)
FAC_C = (FAC_S[0] - 0.7071 * FAC_T / 2, FAC_S[1] + 0.7071 * FAC_T / 2)
FAC_L = math.hypot(FAC_B[0] - FAC_A[0], FAC_B[1] - FAC_A[1]) + 0.3
ABA_Y, ABA_ANG = 25.8, 16
K_CAB, K_CAB_C = 1.07, (0.0, 22.0, -13.0)            # escala da cabeça inteira (ajuste fino)

def olho(u, v):
    return pintar_olho(u, v, 1.85, 1.7, iris=((205, 128, 14), (255, 190, 16)), esclera=(236, 214, 170), pupila=PRETO,
                       r_iris=(0.82, 0.92), c_iris=(-0.14, -0.1), r_pup=(0.36, 0.44), bravo=0.45, alto=0.32,
                       contorno=ORBITA)

def mat_faceta(lado):
    """Faceta a 45°: pele marrom-escura com o olho inteiro na face de fora e uma órbita quase preta em volta;
    creme só embaixo do olho, na metade junto do bico."""
    fora = "east" if lado > 0 else "west"
    def cor(p, face):
        x, y, z = p
        u = z - FAC_C[1]
        if y < OLHO_Y - 1.5: return CREME
        return ROSTO_ESC
    base = mat_chapado(cor, borda=.06, curva=.16)
    def f(c):
        if c["face"] == fora:
            x, y, z = c["p"]
            u, v = z - FAC_C[1], y - OLHO_Y
            o = olho(u, v)
            if o is not None: return o
            if (u / 2.3) ** 2 + (v / 2.05) ** 2 <= 1 and v > -1.2: return mix(ORBITA, ROSTO_ESC, 0.35)   # órbita
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face in ("east", "west") and abs(z + 18.5) < 0.3 and abs(y - 25.3) < 0.3: return (110, 50, 10)   # narina
    if face == "down": return AMARELO_ESC
    if face == "up": return AMARELO_CL
    return mix(AMARELO_CL, AMARELO, clamp((26.6 - y) / 3.0))          # claro em cima, base embaixo (sem escurecer a ponta)

def cabeca_pecas():
    cab = []
    fx = (20.0, 30.0)
    mcreme = mat_liso(CREME, borda=.08, curva=.25)
    # crânio (lados malva, embaixo creme) e frente creme pequena em volta do bico
    cab.append(peca("cranio", [-7.4, 20.6, -12.2], [7.4, 29.0, -4.0],
                    mat_chapado(lambda p, f: PEITO if p[1] < 22.0 else ROSTO_ESC, borda=.06), faixa=fx, res=2))
    cab.append(peca("rosto_frente", [-2.9, 20.4, -17.1], [2.9, 27.2, -12.6], mcreme, faixa=fx, res=4))
    for lado in (-1, 1):
        s = lado_s(lado)
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 20.6, cz - FAC_L / 2], [cx + FAC_T / 2, 27.6, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, OLHO_Y, cz), faixa=fx, res=8))
    # bico pequeno em cunha: base, meio e gancho; maxila de baixo mais escura
    mb = mat_chapado(cor_bico, borda=.08, curva=.25)
    fb = (22.4, 27.2)
    # de frente: cunha estreita (centro amarelo, lados laranja inclinados para trás, ponta mais estreita embaixo)
    cab.append(peca("bico_centro", [-1.45, 22.7, -20.1], [1.45, 26.6, -16.9], mb, faixa=fb, res=4))
    mlado = mat_chapado(lambda p, f: AMARELO_CL if f == "up" else mix(AMARELO, LARANJA_BICO, 0.6), borda=.08, curva=.25)
    for lado in (-1, 1):
        x0, x1 = sorted((1.2 * lado, 2.4 * lado))
        cab.append(peca("bico_lado_" + lado_s(lado), [x0, 23.1, -19.0], [x1, 26.3, -16.9], mlado,
                        rot=(0, 30 * lado, 0), pivo=(1.2 * lado, 24.7, -16.9), faixa=fb, res=4))
    cab.append(peca("bico_ponta", [-0.95, 21.8, -21.0], [0.95, 24.6, -19.8], mb, rot=(-14, 0, 0), pivo=(0, 24.6, -19.8), faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-0.9, 22.0, -19.2], [0.9, 22.8, -16.9], mat_liso(AMARELO_ESC, borda=.12), res=4))
    # barbela: duas tiras vermelhas finas pendendo e abrindo em V
    mv_ = mat_chapado(lambda p, f: mix(VERM_CL, VERM, clamp((22.5 - p[1]) / 5)), borda=.12, curva=.3)
    tiras = []
    for lado in (-1, 1):
        x0, x1 = sorted((0.25 * lado, 2.45 * lado))
        tiras.append(osso("barbela_" + lado_s(lado), [0.6 * lado, 22.4, -17.0], [0, 0, 7 * lado], [
            peca("barbela_" + lado_s(lado), [x0, 16.8, -17.8], [x1, 22.4, -16.6], mv_, faixa=(16.8, 22.4), res=4)]))
    cab.append(osso("barbela", [0, 22.6, -17.2], [0, 0, 0], tiras))          # osso animado (balança)
    # elmo: aba da frente em V (sobrancelha brava) + 3 faixas em arco até a nuca
    for lado in (-1, 1):
        x0, x1 = sorted((0.0, 8.0 * lado))
        cab.append(peca("elmo_aba_" + lado_s(lado), [x0, ABA_Y, -18.2], [x1, ABA_Y + 3.0, -14.6],
                        mat_celulas_x(0, 2.9), rot=(0, 0, ABA_ANG * lado), pivo=(0, ABA_Y, -16.0),
                        faixa=(ABA_Y, ABA_Y + 3.0), res=4))
    for k, (z0, z1, W, yb, yt) in enumerate([(-15.2, -10.6, 8.5, 27.2, 32.0), (-11.0, -6.2, 8.6, 26.4, 33.4), (-6.6, -2.6, 8.2, 25.6, 32.6)]):
        cab += anel(f"elmo{k}", k + 1, z0, z1, W, yb, yt, perfil=PERFIL_ELMO, cel=2.4, res=3)
    # placas com a espiral quadrada dos lados da cabeça (viradas um pouco para a frente)
    for lado in (-1, 1):
        cx, cz = 9.0 * lado, -8.4
        fora = "east" if lado > 0 else "west"
        cab.append(peca("placa_cab_" + lado_s(lado), [cx - 1.1, 21.2, cz - 4.0], [cx + 1.1, 28.6, cz + 4.0],
                        mat_placa_glifo(fora, espelha=lado < 0, bitmap=ESPIRAL_G), rot=(0, 40 * lado, 0), pivo=(cx, 24.9, cz), res=5))
    # crista vermelha em blocos: lâmina do meio (3 degraus) + 2 lâminas dos lados mais baixas
    mcr = mat_chapado(lambda p, f: mix(VERM_CL, VERM, clamp((38.5 - p[1]) / 6.5)) if f != "down" else VERM_ESC, borda=.14, curva=.3)
    crista = [
        peca("crista_bico", [-1.7, 30.4, -18.0], [1.7, 33.4, -14.2], mcr, faixa=(30, 38.1)),
        peca("crista_frente", [-1.7, 31.6, -14.6], [1.7, 36.6, -11.2], mcr, faixa=(30, 38.1)),
        peca("crista_meio", [-1.7, 32.4, -11.6], [1.7, 38.1, -6.4], mcr, faixa=(30, 38.1)),
        peca("crista_tras", [-1.7, 31.6, -6.8], [1.7, 36.6, -1.6], mcr, faixa=(30, 38.1)),
    ]
    for lado in (-1, 1):
        x0, x1 = sorted((1.6 * lado, 5.0 * lado))
        crista.append(peca("crista_lado_" + lado_s(lado), [x0, 32.4, -12.0], [x1, 35.2, -4.6], mcr, faixa=(30, 38.1)))
    cab.append(osso("crista", [0, 32.0, -8.0], [0, 0, 0], crista))
    return cab

# ---------------- peito ----------------
def mat_escamas(y0, y1, larg=2.4, ponta=1.4):
    """Fileira de penas do peito numa peça só: tiras verticais de 'larg' unidades; embaixo, as pontas das penas
    (alternando comprimento) mais escuras com um fio entre elas: lê como penas em escama."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        a = x if face in ("north", "south", "up", "down") else z
        idx = int(math.floor(a / larg))
        fr = a / larg - idx
        lim = y0 + ponta + (0.7 if idx % 2 else 0.0)
        luz = luz_face(c, curva=0.16, borda=0.14, cima=0.06)
        if face in ("up", "down"): return tom(PEITO, luz)
        if y < lim:
            cor = PEITO_SOM
            if fr < 0.1: luz -= 0.22
            if lim - y < 0.3: luz += 0.1
        else:
            cor = PEITO
            if y - lim < 0.35: luz -= 0.2          # fio de sombra da pena de cima
        return tom(cor, luz)
    return f

def peito_pecas():
    pp = []
    # 2 fileiras largas (peças únicas pintadas) + a saia de penas-bloco separadas embaixo
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
    """Cone de anéis encaixados, cada um menor e mais baixo; cada anel é um osso (cauda_anel_k) filho do anterior."""
    ANEIS = [  # (z0, z1, meia largura, y baixo, y alto)
        (14.2, 18.2, 9.4, 7.4, 20.2),
        (17.4, 20.2, 6.6, 7.0, 16.8),
        (19.4, 21.4, 3.8, 6.6, 13.4),
    ]
    def seg(k):
        z0, z1, W, yb, yt = ANEIS[k]
        filhos = anel(f"cauda_anel{k}", k + 1, z0, z1, W, yb, yt, cel=3.0)
        if k + 1 < len(ANEIS): filhos.append(seg(k + 1))
        else:   # ponta da cauda: bloquinho caramelo saindo do último anel
            filhos.append(peca("cauda_ponta", [-1.4, yb + 0.6, z1 - 0.2], [1.4, yb + 3.6, z1 + 1.3],
                               mat_liso(CARAMELO, borda=.2), faixa=(yb, yb + 3.6)))
        return osso(f"cauda_anel_{k}", [0, (yb + yt) / 2, z0], [0, 0, 0], filhos)
    return osso("cauda", [0, 14.0, 14.2], [0, 0, 0], [seg(0)])

# ---------------- montagem ----------------
def montar():
    # ======================= CABEÇA E PESCOÇO =======================
    i_cab = len(g.PECAS)
    cabeca = osso("cabeca", [0, 22.0, -9.0], [0, 0, 0], cabeca_pecas())
    g.transformar(i_cab, [cabeca], K_CAB_C, k=K_CAB)          # ajuste fino do tamanho da cabeça inteira
    pescoco = osso("pescoco", [0, 18.0, -8.0], [0, 0, 0], [
        peca("pescoco", [-5.4, 15.0, -14.0], [5.4, 23.0, -6.0], mat_liso(PEITO, borda=.04), faixa=(15, 23)),
        cabeca])

    # ======================= CORPO =======================
    corpo = []
    corpo.append(peca("tronco", [-10.0, 8.0, -6.5], [10.0, 25.0, 9.5], mat_liso(MARROM, borda=.05), faixa=(8, 27)))
    corpo += peito_pecas()
    # carapaça: anéis em degrau da nuca até a garupa
    FAIXAS = [  # (z0, z1, meia largura, y baixo, y alto)
        (-5.4, -0.6, 12.6, 8.0, 31.2),
        (-1.4, 3.6, 13.2, 7.7, 31.8),
        (2.8, 8.0, 13.5, 7.6, 30.8),
        (7.2, 11.6, 13.0, 7.6, 28.4),
        (10.8, 15.0, 12.0, 7.6, 25.6),
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
                         mat_anel(k, [y1 - 3.7]), faixa=(y0, y1), res=2)]
        fora = "east" if lado > 0 else "west"
        cx, cz = 13.0 * lado, -2.0
        asa.append(peca("ombro_placa_" + s, [cx - 1.1, 10.2, cz - 7.0], [cx + 1.1, 22.0, cz + 7.0],
                        mat_placa_glifo(fora, espelha=lado < 0), rot=(6, 0, -6 * lado), pivo=(cx, 16.1, cz), res=4))
        corpo.append(osso("asa_" + s, [11.0 * lado, 21.0, -2.0], [0, 0, 0], asa))

    corpo.append(cauda_blindada())
    corpo.append(pescoco)
    tronco = osso("corpo", [0, 9.0, 0.0], [0, 0, 0], corpo)

    # ======================= PERNAS =======================
    def perna(lado):
        s = lado_s(lado); xc = 6.6 * lado; zc = 0.0
        pp = []
        mam = mat_liso(AMARELO, borda=.14, curva=.18)
        pp += g.arredondado("perna_" + s, [xc - 3.5, 3.4, zc - 4.2], [xc + 3.5, 9.6, zc + 4.2], mam, r=0.6, faixa=(0, 9.6))
        pp.append(peca("calcanhar_" + s, [xc - 3.7, 0.0, zc - 3.8], [xc + 3.7, 3.8, zc + 4.0], mam, faixa=(0, 9.6)))
        mg = mat_chapado(lambda p, f: CINZA_CL if f == "up" else CINZA, borda=.2, curva=.3)
        for k, dx in enumerate((-2.75, 0.0, 2.75)):          # 3 dedos amarelos com garra cinza em bloco
            x = xc + dx
            pp.append(peca(f"dedo{k}_{s}", [x - 1.25, 0.0, zc - 6.8], [x + 1.25, 3.0, zc - 3.6], mam, faixa=(0, 9.6)))
            pp.append(peca(f"garra{k}_{s}", [x - 1.2, 0.0, zc - 9.8], [x + 1.2, 3.4, zc - 6.6], mg, faixa=(0, 3.4)))
        pp.append(peca("garra_tras_" + s, [xc - 1.6, 0.0, zc + 3.8], [xc + 1.6, 3.2, zc + 7.4], mg, faixa=(0, 3.2)))
        return osso("perna_" + s, [xc, 9.6, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
