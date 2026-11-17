"""Cocórak (#004, Terra, "O Galo das Areias"): galo colossal e pesado, plumagem cor de areia em penas de bloco
cobertas de glifos tribais roxo-escuros, crista vermelha enorme, olhos amarelos bravos e a cauda gigante enrolada
em espiral por cima das costas.

Técnica própria desta espécie: os GLIFOS são decalques projetados em 3D no espaço do MUNDO (depois de aplicar as
rotações de todos os ossos), então um traço do glifo atravessa várias penas em bloco seguidas, como na ficha.
"""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, arredondado, arredondado2, octogono, anel, pintar_olho
from previa import rot as matriz_rot, mv, compor, sub

ID = "cocorak"; NOME = "Cocórak"; NUMERO = 4
ALTURA = 3.0             # colossal: 3 blocos no jogo
QUADRUPEDE = False
ROSTO = ((0, 35.0, -9), 10.5)
N_RABO = 10
INCLINA = 8                       # corpo inclinado: peito alto, traseira descendo para a cauda
K_CAB, SOBE_CAB = 1.12, -2.0      # ajuste final do tamanho e da altura da cabeça
ONDAS = [("rabo", N_RABO, (1.2, 2.0, 0.0))]
ANIM_PARADO = {"barbela": [(0, 0, 0), (5, 0, 2), (0, 0, 0), (4, 0, -2), (0, 0, 0)]}
ANIM_ANDANDO = {"barbela": [(0, 0, 0), (9, 0, 4), (0, 0, 0), (9, 0, -4), (0, 0, 0)]}

# ---------------- paleta (da ficha) ----------------
AREIA = (234, 172, 92); AREIA_CLARA = (248, 208, 136); AREIA_ESC = (204, 136, 64); AREIA_FUNDA = (150, 92, 44)
GLIFO = (44, 26, 54)                      # roxo bem escuro dos padrões tribais (paleta da ficha)
CRISTA = (206, 40, 46); CRISTA_CLARA = (236, 78, 66); CRISTA_ESC = (146, 22, 34)
BICO = (252, 190, 34); BICO_ESC = (226, 128, 16)
PERNA = (226, 152, 60); PERNA_ESC = (182, 108, 40)
GARRA = (40, 26, 52); GARRA_CLARA = (86, 64, 108)
OLHO = (255, 226, 72)
PELE = (196, 44, 48)                      # pele vermelha em volta do olho

# ---------------- mundo: transformação final de cada peça ----------------
MUNDO = {}
PINTAS = {}       # escalas/subidas de g.transformar (a pintura recebe o ponto ORIGINAL; aqui ele volta ao final)

def calcular_mundo(raizes):
    """Guarda, para cada peça (pelo nome), a transformação osso->mundo (com a rotação da própria peça)."""
    pecas = {p.uuid: p for p in g.PECAS}
    nomes = [p.nome for p in g.PECAS]
    assert len(nomes) == len(set(nomes)), "nomes de peça repetidos: " + str({n for n in nomes if nomes.count(n) > 1})
    I = ([[1, 0, 0], [0, 1, 0], [0, 0, 1]], [0, 0, 0])
    def andar(no, M):
        if isinstance(no, str):
            p = pecas[no]
            if any(abs(v) > 1e-9 for v in p.rot):
                R = matriz_rot(*p.rot); M = compor(M, (R, sub(p.pivo, mv(R, p.pivo))))
            MUNDO[p.nome] = M
            PINTAS[p.nome] = list(p.pintas)
            return
        o = no["origin"]; R = matriz_rot(*no["rotation"])
        Mn = compor(M, (R, sub(o, mv(R, o))))
        for f in no["children"]: andar(f, Mn)
    for r in raizes: andar(r, I)

def no_mundo(c):
    A, b = MUNDO[c["nome"]]
    p = list(c["p"]); n = g.NORMAL[c["face"]]
    for C, k, sobe in PINTAS[c["nome"]]:
        p = [C[i] + (p[i] - C[i]) * k + (sobe if i == 1 else 0.0) for i in range(3)]
    return [sum(A[i][k] * p[k] for k in range(3)) + b[i] for i in range(3)], [sum(A[i][k] * n[k] for k in range(3)) for i in range(3)]

def ponto_mundo(nome, p):
    A, b = MUNDO[nome]
    return [sum(A[i][k] * p[k] for k in range(3)) + b[i] for i in range(3)]

def dir_mundo(nome, v):
    A, _ = MUNDO[nome]
    return [sum(A[i][k] * v[k] for k in range(3)) for i in range(3)]

# ---------------- glifos (pixel art) ----------------
G_OLHO = ["...###...",
          "..##.##..",
          ".##...##.",
          "##..#..##",
          ".##...##.",
          "..##.##..",
          "...#.#...",
          "...#.###.",
          "...#....."]
G_SOL = ["..#####..",
         ".##...##.",
         "##.###.##",
         "#.##.##.#",
         "#.#.#.#.#",
         "#.##.##.#",
         "##.###.##",
         ".##...##.",
         "..##.##..",
         "....#....",
         "..###...."]
G_QUADRO = ["#######",
            "#.....#",
            "#.###.#",
            "#.#.#.#",
            "#.###.#",
            "#.....#",
            "###.###"]
G_ESPIRAL = ["#######",
             "......#",
             ".####.#",
             ".#..#.#",
             ".#.##.#",
             ".#....#",
             ".######"]
G_CHEVRON = ["##..................##",
             ".##................##.",
             "..###....#..#....###..",
             "....##..###.###.##....",
             ".....####.....####....",
             "......##.......##.....",
             ".......##.....##......",
             "........##...##.......",
             ".........##.##........",
             "..........###.........",
             "...........#.........."]
G_GANCHO = ["####.",
            "#..#.",
            "#.##.",
            "#....",
            "####."]
G_PASSO = ["##...",
           ".##..",
           "..###",
           "....#"]
G_DENTE = ["#.#.#",
           "#####",
           "..#..",
           "..#.."]
G_ZIGUE = ["#...#...#...#...#",
           "##.###.###.###.##",
           ".###.###.###.###.",
           "..#...#...#...#.."]
G_V = ["#.....#",
       "##...##",
       ".##.##.",
       "..###..",
       "...#..."]
G_CRUZ = [".###.",
          "##.##",
          "#...#",
          "##.##",
          ".###."]

DECALQUES = []

def norm(v):
    m = math.sqrt(sum(a * a for a in v)) or 1.0
    return [a / m for a in v]

def cruz(a, b): return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]

def decalque(bitmap, centro, normal, eixo_u, cel, frente=4.0, tras=4.0, espelho=False, dmin=0.35):
    """Glifo projetado ao longo de 'normal' sobre tudo o que estiver entre centro - tras*n e centro + frente*n.
    eixo_u: direção das colunas do desenho (a 'direita' do glifo); a 'subida' é normal x eixo_u."""
    n = norm(normal); u = norm(eixo_u)
    u = norm([u[i] - n[i] * sum(u[k] * n[k] for k in range(3)) for i in range(3)])
    v = cruz(n, u)
    if espelho: u = [-a for a in u]
    DECALQUES.append(dict(bm=bitmap, c=list(centro), n=n, u=u, v=v, cel=cel, frente=frente, tras=tras,
                          W=len(bitmap[0]), H=len(bitmap), dmin=dmin))

def glifo_em(pw, nw):
    for d in DECALQUES:
        n = d["n"]
        if nw[0] * n[0] + nw[1] * n[1] + nw[2] * n[2] < d["dmin"]: continue
        r = [pw[i] - d["c"][i] for i in range(3)]
        s = r[0] * n[0] + r[1] * n[1] + r[2] * n[2]
        if s > d["frente"] or s < -d["tras"]: continue
        cu = (r[0] * d["u"][0] + r[1] * d["u"][1] + r[2] * d["u"][2]) / d["cel"] + d["W"] / 2
        cv = d["H"] / 2 - (r[0] * d["v"][0] + r[1] * d["v"][1] + r[2] * d["v"][2]) / d["cel"]
        if 0 <= cu < d["W"] and 0 <= cv < d["H"] and d["bm"][int(cv)][int(cu)] == "#":
            return True
    return False

# ---------------- material de areia (luz e glifos no espaço do mundo) ----------------
def _hash(a, b, c=0):
    h = math.sin(a * 127.1 + b * 311.7 + c * 74.7) * 43758.5453
    return h - math.floor(h)

def mat_areia(faixa=(0.0, 44.0), ladrilho=(2.4, 2.0), base=AREIA, borda=.14, ponta=None, glifos=True, sulco=.30, ponta_k=.35):
    """Penas cor de areia: degradê de luz pela altura no mundo, faces de cima claras, de baixo escuras;
    'ladrilho' = penas pintadas em fileiras desencontradas (None = peça lisa, ela já é uma pena em bloco);
    'ponta' = (eixo local, inverte): a ponta da pena em bloco clareia; glifos projetados por cima."""
    y0, y1 = faixa
    def f(c):
        pw, nw = no_mundo(c)
        t = clamp((pw[1] - y0) / (y1 - y0))
        luz = -0.2 + 0.34 * t
        luz += 0.18 * nw[1] if nw[1] > 0 else 0.36 * nw[1]
        cor = base
        if ladrilho:
            ax = max(range(3), key=lambda i: abs(nw[i]))
            h, v = (pw[0], pw[2]) if ax == 1 else (pw[2], pw[1]) if ax == 0 else (pw[0], pw[1])
            if ax == 1: v = -v
            W, H = ladrilho
            lin = math.floor(v / H); fv = v / H - lin
            off = (lin % 2) * W / 2 + (lin % 3) * 0.37
            col = math.floor((h + off) / W); fh = (h + off) / W - col
            rnd = _hash(lin, col, ax)
            luz += (rnd - 0.5) * 0.16
            cor = mix(base, AREIA_CLARA if rnd > 0.6 else AREIA_ESC, abs(rnd - 0.5) * 0.7)
            if fv < 0.13: luz -= sulco                    # ponta escura da pena (borda de baixo)
            elif fv > 0.8: luz -= sulco / 3                   # sombra embaixo da pena de cima
            else: luz += 0.06 * (0.8 - fv)
            if fh < 0.06 or fh > 0.97: luz -= 0.14
        if ponta is not None:
            ei, inv = ponta
            lo, hi = c["b"][0][ei], c["b"][1][ei]
            tt = clamp((c["p"][ei] - lo) / max(hi - lo, 1e-6))
            if inv: tt = 1 - tt
            cor = mix(cor, AREIA_CLARA, ponta_k * tt)
            rnd = _hash(*[round(v, 0) for v in MUNDO[c["nome"]][1]])
            cor = mix(cor, AREIA_ESC if rnd < 0.5 else AREIA_CLARA, abs(rnd - 0.5) * 0.5)
        if g.na_borda(c): luz -= borda
        if glifos and glifo_em(pw, nw):
            return tom(GLIFO, 0.1 + 0.25 * luz if nw[1] > 0.5 else 0.2 * luz)
        return tom(cor, luz)
    return f

def mat_voxel(c0, c1, eixo=1, cel=1.0, borda=.22, inverte=False):
    """Bloco 'de cubinhos' (crista, barbela, perna): degradê c0 -> c1 no eixo, cada célula de 'cel' unidades
    com um leve sorteio de tom, como os cubos da arte."""
    def f(c):
        lo, hi = c["b"][0][eixo], c["b"][1][eixo]
        t = clamp((c["p"][eixo] - lo) / max(hi - lo, 1e-6))
        if inverte: t = 1 - t
        cor = mix(c0, c1, t)
        x, y, z = c["p"]
        rnd = _hash(math.floor(x / cel), math.floor(y / cel), math.floor(z / cel))
        luz = 0.06 + (rnd - 0.5) * 0.14
        if c["face"] == "up": luz += 0.18
        if c["face"] == "down": luz -= 0.32
        if g.na_borda(c): luz -= borda
        return tom(cor, luz)
    return f

# ---------------- formas ----------------
def pena_bloco(nome, raiz, rot, L, W, E, mat, eixo="z", estreita=0.58):
    """Pena em BLOCO (grossa, como os cubos da ficha) pendurada para baixo a partir da raiz: corpo + ponta
    mais estreita em degrau. eixo='z': largura em z (face larga para os lados); 'x': largura em x."""
    x, y, z = raiz
    L1 = L * 0.68; L2 = L - L1 + 0.1
    if eixo == "z":
        a = peca(nome, [x - E / 2, y - L1, z - W / 2], [x + E / 2, y, z + W / 2], mat)
        b = peca(nome + "_p", [x - E * 0.42, y - L1 - L2 + 0.1, z - W * estreita / 2], [x + E * 0.42, y - L1 + 0.1, z + W * estreita / 2], mat)
    else:
        a = peca(nome, [x - W / 2, y - L1, z - E / 2], [x + W / 2, y, z + E / 2], mat)
        b = peca(nome + "_p", [x - W * estreita / 2, y - L1 - L2 + 0.1, z - E * 0.42], [x + W * estreita / 2, y - L1 + 0.1, z + E * 0.42], mat)
    return osso(nome, list(raiz), list(rot), [a, b])

def pena_anel(nome, raiz, phi, flare, L, W, E, lado, mat, varre=0):
    """Pena em bloco numa saia em volta do corpo (face larga para fora no ângulo phi, ponta abrindo 'flare')."""
    return osso(nome, list(raiz), [0, -phi * lado, 0], [pena_bloco(nome + "_r", raiz, (-varre, 0, flare * lado), L, W, E, mat)])


def mat_placa(base, y0, L, W, centro, eixo="z", curva=0.0, contorno=-.38):
    """Pena-placa recortada (alfa) pendurada para BAIXO a partir de y0: o recorte é o de g.forma_pena e a cor vem
    do material de areia no mundo (luz contínua e glifos atravessando as penas vizinhas)."""
    largas = ("east", "west") if eixo == "z" else ("north", "south")
    def f(c):
        if c["face"] not in largas: return None          # bordas finas invisíveis: nada de 'lasca' vista de perfil
        x, y, z = c["p"]
        v = (y0 - y) / L
        u = ((z if eixo == "z" else x) - centro) / (W / 2)
        if not (-0.01 <= v <= 1.0): return None
        ok, borda, uc = g.forma_pena(u, max(v, 0.0), curva)
        if not ok: return None
        cor = base(c)
        if borda < 0.12: return tom(cor, contorno)
        if v > 0.72: cor = tom(cor, 0.06)                 # ponta da pena pega luz
        return cor
    return f

def placa(nome, raiz, rot, L, W, base, eixo="z", esp=0.32, curva=0.0, res=3):
    """Placa fina de pena (alfa) pendurada para baixo a partir da raiz: eixo='z' face larga para os lados."""
    x, y, z = raiz
    if eixo == "z": de, ate, centro = [x - esp / 2, y - L, z - W / 2], [x + esp / 2, y, z + W / 2], z
    else: de, ate, centro = [x - W / 2, y - L, z - esp / 2], [x + W / 2, y, z + esp / 2], x
    return osso(nome, list(raiz), list(rot), [peca(nome, de, ate, mat_placa(base, y, L, W, centro, eixo, curva), res=res)])

def placa_anel(nome, raiz, phi, flare, L, W, lado, base, varre=0, curva=0.15):
    """Fileira de telhado: placa com a face larga para fora no ângulo phi, ponta para baixo/trás, abrindo 'flare'."""
    return osso(nome, list(raiz), [0, -phi * lado, 0], [placa(nome + "_p", raiz, (-varre, 0, flare * lado), L, W, base, curva=curva * lado)])

def barril(nome, camadas, mat, zc=0.0):
    """Volume de ovo em camadas: cada camada (y0, y1, meia largura x, meia profundidade z, dz) é um prisma de 8 lados
    + um bloco girado 45° (quase redondo visto de cima). Camadas mais estreitas em cima e embaixo = ovo."""
    ids = []
    for k, (y0, y1, hx, hz, dz) in enumerate(camadas):
        c = zc + dz; r = 0.36 * min(hx, hz)
        ids += octogono(f"{nome}{k}", [-hx, y0, c - hz], [hx, y1, c + hz], mat, r=r, faixa=(4, 34))
        q = 0.80 * min(hx, hz)
        ids.append(peca(f"{nome}{k}_g", [-q, y0 + 0.05, c - q], [q, y1 - 0.05, c + q], mat, rot=(0, 45, 0), pivo=(0, (y0 + y1) / 2, c), faixa=(4, 34)))
    return ids

# ---------------- cabeça ----------------
OLHO_Y = 35.3
FAC_A, FAC_B = (4.7, -8.6), (2.0, -11.3)      # quina chanfrada do rosto (lado +x), o olho fica nela
FAC_T = 2.0
FAC_L = math.dist(FAC_A, FAC_B)
_m = ((FAC_A[0] + FAC_B[0]) / 2, (FAC_A[1] + FAC_B[1]) / 2)
FAC_C = (_m[0] - 0.7071 * FAC_T / 2, _m[1] + 0.7071 * FAC_T / 2)
SOBRANCELHA = mat_voxel((38, 24, 46), (68, 48, 78), 1, borda=.15)

def pele(c, escuro=0.0):
    return tom(PELE, -0.08 - escuro - (0.3 if g.na_borda(c) else 0.0))

# olho imponente (fase 7): fenda alongada, pálpebra pesada cortando o alto em diagonal até o bico
OLHO_RU, OLHO_RV = 1.7, 1.1              # meia largura e meia altura do olho inteiro (antes do corte)
LID_A, LID_B = 0.40, 0.42                 # linha da pálpebra: v = LID_A + LID_B * u (desce para o bico, u < 0)
FUNDO_A, FUNDO_B = -0.78, 0.08            # borda de baixo quase reta, subindo de leve para trás
IRIS_C = (-0.55, -0.2); IRIS_R = (1.15, 1.0)
PUPILA_C = (-0.98, -0.3); PUPILA_R = (0.3, 0.4)
IRIS_CLARA = (255, 232, 52); IRIS_ESC = (240, 152, 12)

def olho_bravo(u, v):
    """Cor do pixel do olho em (u, v) (unidades; u < 0 = para o bico, v para cima) ou None fora dele."""
    if (u / OLHO_RU) ** 2 + (v / OLHO_RV) ** 2 > 1: return None
    topo = LID_A + LID_B * u; fundo = FUNDO_A + FUNDO_B * u
    if v > topo or v < fundo: return None
    if topo - v < 0.14: return (36, 20, 26)                                   # fio escuro da pálpebra (1 px)
    pu, pv = u - PUPILA_C[0], v - PUPILA_C[1]
    if (pu - 0.13) ** 2 + (pv - 0.2) ** 2 < 0.012: return (255, 255, 236)    # 1 px de brilho no alto da pupila
    if (pu / PUPILA_R[0]) ** 2 + (pv / PUPILA_R[1]) ** 2 <= 1: return (24, 12, 16)
    iu, iv = (u - IRIS_C[0]) / IRIS_R[0], (v - IRIS_C[1]) / IRIS_R[1]
    if iu * iu + iv * iv <= 1:
        cor = mix(IRIS_CLARA, IRIS_ESC, clamp(0.25 + 0.6 * iv))               # mais escura em cima
        if topo - v < 0.3: cor = tom(cor, -0.14)                             # sombra da sobrancelha (1 tom) no alto da íris
        if iu * iu + iv * iv > 0.82: cor = tom(cor, -0.12)                   # aro da íris
        return cor
    cor = mix((252, 222, 96), (232, 180, 56), clamp((v - fundo) / 0.8))     # cunha de esclera atrás, amarelada
    return tom(cor, -0.14) if topo - v < 0.3 else cor

def mat_faceta(lado, areia):
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u = z - FAC_C[1] - 0.1; dy = y - OLHO_Y
            o = olho_bravo(u, dy)
            if o: return o
            # pele vermelha: em volta do olho e descendo para a frente até o bico (fica embaixo da sobrancelha)
            # (só embaixo e na frente do olho: nada de aro vermelho em volta, que arredonda o olhar)
            topo = LID_A + LID_B * u
            baixo = -1.9 + 0.3 * u if u < 0 else -1.9 + 0.95 * u        # cunha: funda junto ao bico, sobe para trás
            if dy < topo + 0.05 and -2.9 < u < 1.95 and dy > baixo:
                return pele(c, 0.15 * clamp(-dy / 2))
        return areia(c)
    return f

def mat_rosto(areia):
    """Peças da frente da cabeça: abaixo dos olhos a pele é vermelha (rodeia a base do bico)."""
    def f(c):
        x, y, z = c["p"]
        if c["face"] == "north" and abs(x) > 1.7 and 33.0 < y < 35.5: return pele(c)   # faixa vermelha do olho até o bico
        return areia(c)
    return f

def so_olho(c, cor): return cor[0] > 200 and cor[1] > 120 and cor[2] < 140

def montar_cabeca():
    cab = []
    ma = mat_areia(faixa=(29, 40), ladrilho=(2.3, 1.9), sulco=.18)
    # crânio liso: um volume chanfrado, uma tampa mais estreita e a NUCA inclinada (cai da tampa para o pescoço,
    # sem a escadinha de blocos de antes)
    cab += arredondado("cranio", [-4.9, 30.8, -8.8], [4.9, 36.2, -2.6], ma, r=1.6)
    cab += arredondado("cranio_alto", [-3.9, 35.4, -8.4], [3.9, 38.2, -3.6], ma, r=1.2)
    cab.append(peca("nuca", [-4.1, 31.2, -4.4], [4.1, 37.9, -1.7], ma, rot=(-24, 0, 0), pivo=(0, 31.2, -3.0)))
    cab += arredondado("testa", [-2.4, 30.8, -12.1], [2.4, 37.4, -8.0], mat_rosto(ma), r=0.9)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 31.2, cz - FAC_L / 2], [cx + FAC_T / 2, 37.3, cz + FAC_L / 2],
                        mat_faceta(lado, ma), rot=(0, 45 * lado, 0), pivo=(cx, 35, cz), res=8, brilho=so_olho))
        # sobrancelha pesada e SALIENTE (sai ~0,9 da face), inclinada descendo para o bico: a borda de baixo
        # coincide com a linha da pálpebra pintada, então ela corta o alto do olho (o V bravo)
        fo = cx + FAC_T / 2 * lado
        fx0, fx1 = sorted((fo - 0.5 * lado, fo + 0.8 * lado))
        ang = math.degrees(math.atan(LID_B))
        yb = OLHO_Y + LID_A + 0.02
        cab.append(osso("sobrancelha_q_" + s, [cx, yb, cz + 0.1], [0, 45 * lado, 0], [
            peca("sobrancelha_q_" + s, [fx0, yb, cz - 2.65], [fx1, yb + 1.45, cz + 1.9], SOBRANCELHA,
                 rot=(-ang, 0, 0), pivo=(fo, yb, cz + 0.1))]))
    # bico curto em triângulo, curvado para baixo, ponta mais escura
    def cor_bico(p, face):
        x, y, z = p
        t = clamp((-z - 12.0) / 4.0)
        if face == "down": return BICO_ESC
        if face == "north": return mix(BICO, (240, 150, 24), t)
        return mix(BICO, (222, 124, 18), t * t)
    mb = g.mat_cor(cor_bico, borda=.06, curva=.45)
    cab.append(peca("bico_base", [-1.9, 32.2, -13.6], [1.9, 35.4, -11.6], mb, faixa=(31, 36)))
    cab.append(peca("bico_meio", [-1.35, 32.5, -15.0], [1.35, 35.0, -13.4], mb, rot=(-16, 0, 0), pivo=(0, 35.0, -13.4), faixa=(31, 36)))
    cab.append(peca("bico_ponta", [-0.8, 32.0, -15.8], [0.8, 34.3, -14.7], g.mat_cor(cor_bico, borda=.06, curva=.2), rot=(-20, 0, 0), pivo=(0, 34.3, -14.7), faixa=(31, 36)))
    cab.append(peca("bico_baixo", [-1.3, 31.6, -14.2], [1.3, 32.4, -11.6], g.mat_cor(lambda p, f: BICO_ESC, borda=.1)))
    # barbela: dois lobos vermelhos grandes pendurados embaixo do bico até o peito (osso próprio: balança)
    mv_ = mat_voxel(CRISTA_CLARA, CRISTA_ESC, 1, inverte=True, cel=1.2)
    barb = []
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x = 1.3 * lado
        barb.append(osso("barbela_" + s, [x, 32.0, -12.6], [12, 0, -5 * lado], [
            peca("barbela_" + s, [x - 1.25, 26.6, -13.8], [x + 1.25, 32.0, -11.4], mv_),
            peca("barbela2_" + s, [x - 0.95, 25.0, -13.5], [x + 0.95, 26.8, -11.7], mv_)]))
    cab.append(osso("barbela", [0, 32.0, -12.4], [0, 0, 0], barb))
    # crista: leque de lâminas vermelhas em cubos, do alto da testa para trás
    crista = []
    mc = mat_voxel(CRISTA_ESC, CRISTA_CLARA, 1)
    crista.append(peca("crista_base", [-1.5, 37.4, -11.0], [1.5, 39.4, -2.8], mc))
    LAM = [(-10.4, 0.0, 2, 6.2, 4.0), (-8.6, 0.0, 22, 8.8, 4.4), (-6.6, 0.0, 40, 10.0, 4.4),
           (-4.8, 0.0, 56, 10.2, 4.2), (-3.4, 0.0, 70, 9.4, 4.0), (-2.6, 0.0, 84, 8.0, 3.6), (-2.0, 0.0, 100, 6.0, 3.2)]
    for k, (z, x, rx, L, W) in enumerate(LAM):
        crista.append(lamina(f"crista{k}", (x, 39.0, z), (rx, 0, 0), L, W, 2.6, mc))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        crista.append(lamina("crista_lado_" + s, (1.0 * lado, 38.8, -7.4), (16, 0, -16 * lado), 7.0, 3.2, 2.0, mc))
    cab.append(osso("crista", [0, 38.4, -7.0], [0, 0, 0], crista))
    return cab

def lamina(nome, base, rot, L, W, E, mat):
    """Lâmina da crista PARA CIMA: bloco + ponta mais estreita (degrau), largura W em z, espessura E em x."""
    x, y, z = base
    L1 = L * 0.62
    return osso(nome, list(base), list(rot), [
        peca(nome, [x - E / 2, y, z - W / 2], [x + E / 2, y + L1, z + W / 2], mat),
        peca(nome + "_p", [x - E * 0.4, y + L1 - 0.1, z - W * 0.3], [x + E * 0.4, y + L, z + W * 0.3], mat)])

# ---------------- cauda enrolada ----------------
RABO = [  # (comprimento, largura x, espessura, curva rx do osso): sai logo atrás do corpo, sobe e enrola por cima das costas
    (7.5, 14.0, 10.5, 4), (8.0, 15.0, 10.5, -8), (7.0, 15.5, 10.5, -20), (6.0, 15.5, 10.4, -28), (5.6, 15.0, 10.2, -30),
    (5.4, 12.0, 10.0, -30), (5.2, 10.4, 9.6, -30), (5.0, 9.6, 9.2, -28), (4.6, 9.0, 8.6, -26), (4.2, 8.2, 7.8, -24)]
RABO_Y = 16.8

def montar_cauda(ma_nucleo, ma_pena):
    y0 = RABO_Y
    def seg(k, z):
        L, W, T, curva = RABO[k]
        s = f"rabo_{k}"
        za = z - (1.4 if k else 0.0)          # o núcleo entra no segmento anterior: fecha a cunha de fora da curva
        filhos = [peca(s + "_a", [-W / 2, y0 - T / 2 + 1.0, za], [W / 2, y0 + T / 2 - 1.0, z + L], ma_nucleo),
                  peca(s + "_b", [-W / 2 + 1.2, y0 - T / 2, za], [W / 2 - 1.2, y0 + T / 2, z + L], ma_nucleo)]
        # penas de fora (lado de fora da curva = -y): duas placas grossas lado a lado, deitadas em telha sobre o
        # segmento seguinte (uma peça só cada: nada de dedinhos soltos na borda da espiral)
        yb = y0 - T / 2
        for j, xo in enumerate((-W * 0.24, W * 0.24)):
            filhos.append(osso(f"{s}_pf{j}", [xo, yb + 0.6, z + 0.15 * L], [8 + 4 * j, 5 * (j * 2 - 1), 0], [
                peca(f"{s}_pf{j}", [xo - W * 0.25, yb - 0.9, z + 0.15 * L], [xo + W * 0.25, yb + 0.6, z + 1.3 * L + 0.5 * j], ma_pena)]))
        # camadas dos lados: placas grossas que passam do fim do segmento e abrem um pouco para fora
        for lado in ((-1, 1) if k < 5 else ()):
            ld = "d" if lado < 0 else "e"
            xb = lado * (W / 2 - 0.6)
            x0, x1 = sorted((xb - 0.4 * lado, xb + 1.1 * lado))
            filhos.append(osso(f"{s}_pl{ld}", [xb, y0, z + 0.15 * L], [4, 8 * lado, 0], [
                peca(f"{s}_pl{ld}", [x0, y0 - T * 0.5 - 0.3, z + 0.15 * L], [x1, y0 + T * 0.4, z + 1.2 * L], ma_pena)]))
        # pena de dentro (lado de dentro da curva, +y)
        if k <= 7:
            yt = y0 + T / 2
            filhos.append(osso(s + "_pd", [0, yt - 0.8, z + 0.25 * L], [-16, 0, 0], [
                peca(s + "_pd", [-W * 0.4, yt - 0.8, z + 0.25 * L], [W * 0.4, yt + 0.9, z + 1.2 * L], ma_pena)]))
        if k + 1 < len(RABO): filhos.append(seg(k + 1, z + L - 0.4))
        else:
            # ponta da espiral: uma pena grossa que continua a curva e afina em degrau (fecha o fim do segmento,
            # que antes ficava como uma caixa cortada) + duas penas laterais abrindo de leve
            zp = z + L - 0.8
            filhos.append(osso(f"{s}_ponta", [0, y0, zp], [-20, 0, 0], [
                peca(f"{s}_ponta", [-2.9, y0 - 2.9, zp], [2.9, y0 + 1.9, zp + 4.4], ma_pena),
                peca(f"{s}_ponta_p", [-1.6, y0 - 2.4, zp + 4.3], [1.6, y0 + 0.6, zp + 7.0], ma_pena)]))
            for j, ry in enumerate((-30, 30)):
                filhos.append(osso(f"{s}_leque{j}", [0, y0, zp], [-18, ry, 0], [
                    peca(f"{s}_leque{j}", [-1.8, y0 - 2.0, zp], [1.8, y0 + 1.4, zp + 5.2], ma_pena)]))
        return osso(s, [0, y0, z], [curva, 0, 0], filhos)
    return seg(0, 10.0)

# ---------------- asa ----------------
ASA_RECOLHE = 0          # a asa fica a prumo, apoiada no bojo da barriga (nem espeta para fora nem afunda nele)
ASA_MAT = None

def pena_asa(nome, raiz, varre, flare, L, W, E, lado, mat, degrau=True, giro=0):
    """Pena da asa em BLOCO grosso pendurada da raiz, deitada no flanco: a face larga olha para fora (±x), a ponta
    varre para trás ('varre' graus) e abre só 'flare' graus (telha: cobre a raiz da fileira de baixo); 'giro' vira a
    face para a frente (as penas da beirada da frente dobram em volta do ombro: de frente não aparecem de quina)."""
    x, y, z = raiz
    xi = x - lado * E / 2                         # o bloco cresce para dentro a partir da face de fora
    x0, x1 = sorted((xi - E / 2, xi + E / 2))
    if not degrau:
        filhos = [peca(nome, [x0, y - L, z - W / 2], [x1, y, z + W / 2], mat)]
    else:
        L1 = L * 0.7
        xa, xb = sorted((xi - E * 0.42, xi + E * 0.42))
        filhos = [peca(nome, [x0, y - L1, z - W / 2], [x1, y, z + W / 2], mat),
                  peca(nome + "_p", [xa, y - L + 0.05, z - W * 0.3], [xb, y - L1 + 0.1, z + W * 0.3], mat)]
    return osso(nome, list(raiz), [-varre, giro * lado, flare * lado], filhos)

def montar_asa(lado, s):
    ma = mat_areia(faixa=(8, 32), ladrilho=(2.2, 1.9))
    mp = mat_areia(faixa=(8, 32), ladrilho=None, ponta=(1, True), borda=.12, ponta_k=.08)
    asa = []
    # escudo: ombro em cúpula (as cobertas fecham o alto), parte de baixo mais estreita e puxada para trás (gota)
    x0, x1 = sorted((9.6 * lado, 14.5 * lado))
    asa += arredondado2("asa_ombro_" + s, [x0, 19.8, -10.4], [x1, 26.2, 6.0], ma, r=2.6)
    x0, x1 = sorted((10.0 * lado, 14.3 * lado))
    asa += arredondado("asa_baixo_" + s, [x0, 13.6, -7.2], [x1, 21.0, 7.8], ma, r=1.6)
    # cobertas: 3 penas largas e curtas deitadas no alto do ombro (raiz para dentro, ponta para fora: cúpula)
    for k, (z, varre, giro) in enumerate([(-7.0, 6, 34), (-2.2, 10, 8), (2.6, 15, 0)]):
        asa.append(pena_asa(f"asa_c{k}_{s}", (13.5 * lado, 26.7, z), varre, 20, 5.9, 4.7, 1.25, lado, mp, giro=giro))
    # secundárias: 4 penas médias, a raiz escondida embaixo das cobertas
    for k, (z, varre, giro) in enumerate([(-8.2, 9, 30), (-4.0, 13, 6), (0.0, 17, 0), (4.0, 22, 0)]):
        asa.append(pena_asa(f"asa_m{k}_{s}", (15.2 * lado, 23.0, z), varre, 5, 7.6, 4.5, 1.3, lado, mp, giro=giro))
    # primárias: 4 penas longas, varrendo cada vez mais para trás, rentes ao corpo
    for k, (z, varre, giro) in enumerate([(-5.6, 18, 18), (-1.6, 25, 0), (2.2, 33, 0), (5.8, 42, 0)]):
        asa.append(pena_asa(f"asa_p{k}_{s}", (15.0 * lado, 18.8, z), varre, 1, 9.8, 4.2, 1.2, lado, mp, giro=giro))
    return asa

# ---------------- montagem ----------------
TRONCO = [  # camadas do barril: (y0, y1, meia largura, meia profundidade, deslocamento z)
    (6.4, 9.2, 10.2, 9.6, 0.4), (9.0, 13.2, 12.8, 11.6, 0.2), (13.0, 18.2, 13.4, 12.2, 0.0),
    (18.0, 22.2, 12.6, 11.8, -0.4), (22.0, 25.6, 11.0, 10.6, -0.8), (25.4, 28.6, 8.8, 9.0, -1.2)]

def montar():
    MUNDO.clear(); PINTAS.clear(); DECALQUES.clear()
    ma = mat_areia(faixa=(4, 34))
    mt = mat_areia(faixa=(4, 34), ladrilho=None, borda=.0)       # base das placas de pena (o recorte faz o contorno)

    # ---------- cabeça e pescoço com colar de penas (hackles) caindo sobre ombros e peito ----------
    i_cab = len(g.PECAS)
    cab = montar_cabeca()
    g.transformar(i_cab, cab, (0.0, 31.0, -7.0), k=K_CAB, sobe=SOBE_CAB)
    cabeca = osso("cabeca", [0, 31.0 + SOBE_CAB, -7.0], [0, 0, 0], cab)
    pesc = []
    pesc += arredondado("pescoco", [-5.2, 24.5, -10.0], [5.2, 30.6, -1.8], mat_areia(faixa=(20, 36), ladrilho=(1.9, 1.6)), r=1.6)
    for k, phi in enumerate([-90, -64, -38, -12, 14, 40, 66, 90]):
        for lado in (-1, 1):
            if phi in (-90, 90) and lado < 0: continue
            x, z = anel(5.0, 5.0, -6.0, phi, lado)
            pesc.append(placa_anel(f"gola{k}_{'d' if lado < 0 else 'e'}", (x, 31.2, z), phi, 30 if phi < 30 else 14,
                                   9.4, 5.8 if phi < 30 else 6.6, lado, mt, varre=4 if phi > 0 else 0))
    for k, phi in enumerate([-78, -50, -22, 8, 38, 68]):
        for lado in (-1, 1):
            x, z = anel(7.0, 6.6, -5.4, phi, lado)
            pesc.append(placa_anel(f"gola_b{k}_{'d' if lado < 0 else 'e'}", (x, 27.6, z), phi, 46, 9.4, 6.2, lado, mt, varre=2))
    pesc.append(cabeca)
    pescoco = osso("pescoco", [0, 26.0, -5.0], [-INCLINA, 0, 0], pesc)

    # ---------- corpo: barril em ovo (mais largo na barriga, afinando para o pescoço) ----------
    corpo = []
    corpo += barril("tronco", TRONCO, ma)
    corpo += arredondado("peito", [-8.6, 12.0, -13.4], [8.6, 25.6, -6.0], ma, r=2.8)
    corpo += arredondado("anca", [-9.0, 10.0, 8.0], [9.0, 23.0, 14.2], ma, r=2.8)

    # telhado de penas (placas alfa) em fileiras ordenadas, todas apontando para baixo
    FILEIRAS = [  # (y da raiz, raio x, raio z, z centro, phis, comprimento, largura, abertura)
        (24.4, 11.6, 11.4, -0.8, [-86, -62, -38], 6.4, 5.6, 10),
        (19.6, 13.0, 12.4, -0.4, [-74, -50, 62, 82], 6.6, 5.8, 10),
        (14.8, 13.6, 12.6, 0.0, [-86, -62, -38, 34, 58, 80], 6.6, 5.6, 10),     # (os do flanco ficam sob a asa)
        (10.6, 12.8, 11.8, 0.2, [-74, -50, -26, -2, 22, 46, 70], 5.6, 5.4, 15)]
    for f, (y, ax, az, zc, phis, L, W, fl) in enumerate(FILEIRAS):
        for k, phi in enumerate(phis):
            for lado in (-1, 1):
                x, z = anel(ax, az, zc, phi, lado)
                corpo.append(placa_anel(f"pena{f}_{k}_{'d' if lado < 0 else 'e'}", (x, y, z), phi, fl, L, W, lado, mt,
                                        varre=6 if phi > 20 else 0))
        if f in (0, 1):
            x, z = anel(ax, az, zc, -90, 1)
            corpo.append(placa_anel(f"pena{f}_meio", (x, y - 1.2, z), -90, fl, L, W, 1, mt))
    # sela: placas deitadas nas costas apontando para a cauda
    for k, (x, y, z, L, W) in enumerate([(0.0, 29.4, -3.0, 7.0, 6.4), (-5.2, 28.0, -2.0, 6.6, 5.6), (5.2, 28.0, -2.0, 6.6, 5.6),
                                         (0.0, 27.6, 2.6, 7.0, 6.8), (-5.6, 26.0, 3.4, 6.4, 5.8), (5.6, 26.0, 3.4, 6.4, 5.8),
                                         (0.0, 25.4, 8.0, 6.4, 7.0), (-5.8, 23.4, 8.6, 6.0, 5.8), (5.8, 23.4, 8.6, 6.0, 5.8)]):
        corpo.append(placa(f"sela{k}", (x, y, z), (-(66 - 4 * (k // 3)), -x * 2.0, 0), L, W, mt, eixo="x"))

    # ---------- asas dobradas: escudo grosso deitado no flanco, penas em BLOCO em telha (cobertas, secundárias,
    # primárias), ponta das penas encostada no corpo (de frente a asa não espeta para fora) ----------
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = montar_asa(lado, s)
        corpo.append(osso("asa_" + s, [11.7 * lado, 27.6, -1.0], [0, 0, -ASA_RECOLHE * lado], asa))

    # ---------- cauda gigante enrolada ----------
    cauda = montar_cauda(mat_areia(faixa=(0, 42), ladrilho=(2.8, 2.2)), mat_areia(faixa=(0, 42), ladrilho=(3.0, 2.4), ponta=(2, False), borda=.2))
    corpo.append(osso("cauda", [0, RABO_Y, 10.0], [0, 0, 0], [cauda]))
    corpo.append(pescoco)
    tronco = osso("corpo", [0, 13.0, 0], [INCLINA, 0, 0], corpo)

    # ---------- pernas grossas: coxa de penas, canela laranja, dedos grossos e garras escuras pontudas ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 6.2 * lado; zc = 1.0
        pp = []
        pp += arredondado("coxa_" + s, [xc - 3.4, 6.4, zc - 3.6], [xc + 3.4, 13.0, zc + 3.6], mat_areia(faixa=(3, 14), ladrilho=(1.8, 1.5)), r=1.3)
        for k, phi in enumerate([-60, 0, 60]):
            x, z = anel(3.4, 3.4, zc, phi, 1)
            pp.append(placa_anel(f"calca{k}_{s}", (xc + x * lado, 9.4, z), phi, 16, 4.6, 4.2, lado, mt))
        mperna = mat_voxel(PERNA, PERNA_ESC, 1, inverte=True, cel=1.2)
        pp += octogono("canela_" + s, [xc - 2.7, 2.0, zc - 2.7], [xc + 2.7, 7.6, zc + 2.7], mperna, r=0.9)
        mdedo = mat_voxel(PERNA, PERNA_ESC, 1, inverte=True, cel=1.2)
        mg = mat_voxel(GARRA_CLARA, GARRA, 1, inverte=True, cel=0.8, borda=.25)
        for nome, giro, dx in (("meio", 0, 0), ("fora", -22 * lado, 2.0 * lado), ("dentro", 22 * lado, -2.0 * lado)):
            x0, z0 = xc + dx * 0.6, zc - 1.0
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - 1.3, 0, z0 - 4.6], [x0 + 1.3, 2.7, z0 + 0.8], mdedo),
                peca(f"garra_{nome}_{s}", [x0 - 1.05, 0.0, z0 - 6.2], [x0 + 1.05, 2.4, z0 - 4.3], mg),
                osso(f"garra_{nome}_{s}", [x0, 0.0, z0 - 6.0], [0, 0, 0], [
                    peca(f"garra2_{nome}_{s}", [x0 - 0.7, 0.0, z0 - 7.4], [x0 + 0.7, 1.7, z0 - 6.0], mg),
                    peca(f"garra3_{nome}_{s}", [x0 - 0.35, 0.0, z0 - 8.4], [x0 + 0.35, 0.9, z0 - 7.3], mg)])]))
        pp.append(peca("dedo_tras_" + s, [xc - 0.9, 0, zc + 1.0], [xc + 0.9, 1.8, zc + 3.6], mdedo))
        pp.append(peca("garra_tras_" + s, [xc - 0.7, 0, zc + 3.4], [xc + 0.7, 1.4, zc + 4.8], mg))
        pp.append(peca("garra_tras2_" + s, [xc - 0.35, 0, zc + 4.7], [xc + 0.35, 0.8, zc + 5.6], mg))
        return osso("perna_" + s, [xc, 12.0, zc], [0, 0, 0], pp)

    raizes = [tronco, perna(-1), perna(1)]
    calcular_mundo(raizes)
    glifos()
    return raizes

def glifos():
    """Os decalques de glifo (posições no mundo). Os da cauda acompanham os segmentos já girados."""
    for lado in (-1, 1):
        decalque(G_OLHO, (14.4 * lado, 20.4, -0.6), (lado, 0, 0), (0, 0, -lado), 1.12, frente=2.6, tras=2.0, dmin=0.75)   # na asa
        decalque(G_PASSO, (14.0 * lado, 10.6, 9.0), (lado, 0, 0), (0, 0, -lado), 0.9, frente=3, tras=3)
        decalque(G_V, (12.6 * lado, 12.0, -9.0), (lado, 0, -1), (0, 0, -lado), 0.9, frente=3, tras=3)
        decalque(G_DENTE, (8.6 * lado, 25.0, -6.0), (lado, 0.3, -0.3), (0, 0, -lado), 0.8, frente=2.5, tras=2.5)
        decalque(G_GANCHO, (5.6 * lado, 27.0, 6.0), (0, 1, 0.3), (lado, 0, 0), 0.9, frente=4, tras=3, espelho=lado < 0)
        decalque(G_QUADRO, (15.0 * lado, 19.0, -11.4), (0, 0, -1), (-1, 0, 0), 0.75, frente=3, tras=3)
    decalque(G_CHEVRON, (0, 21.6, -14.0), (0, 0, -1), (-1, 0, 0), 0.9, frente=4, tras=4)
    decalque(G_ZIGUE, (0, 13.6, -13.0), (0, 0, -1), (-1, 0, 0), 0.95, frente=5, tras=5)
    decalque(G_V, (0, 9.4, -12.0), (0, 0, -1), (-1, 0, 0), 0.9, frente=5, tras=5)
    # cauda: glifos nos lados de alguns segmentos e chevrons na face de fora (vista de trás)
    for k, bm, cel in ((2, G_QUADRO, 1.0), (4, G_ESPIRAL, 1.0), (6, G_OLHO, 0.9), (8, G_CRUZ, 0.8)):
        L, W, T, _ = RABO[k]
        nome = f"rabo_{k}_a"
        p = g.PECAS[[q.nome for q in g.PECAS].index(nome)]
        cz = (p.de[2] + p.ate[2]) / 2
        eixo = norm(dir_mundo(nome, (0, 0, 1)))
        for lado in (-1, 1):
            c = ponto_mundo(nome, (lado * W / 2, RABO_Y, cz))
            decalque(bm, c, (lado, 0, 0), [-e * lado for e in eixo], cel, frente=2.5, tras=2.5)
    for k, bm, cel in ((4, G_V, 1.1), (6, G_ZIGUE, 0.8)):
        L, W, T, _ = RABO[k]
        nome = f"rabo_{k}_a"
        p = g.PECAS[[q.nome for q in g.PECAS].index(nome)]
        cz = (p.de[2] + p.ate[2]) / 2
        n = norm(dir_mundo(nome, (0, -1, 0)))
        c = ponto_mundo(nome, (0, RABO_Y - T / 2, cz))
        decalque(bm, c, n, (1, 0, 0), cel, frente=3, tras=3)

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
