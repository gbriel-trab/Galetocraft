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
K_CAB, SOBE_CAB = 1.06, -1.4      # ajuste final do tamanho e da altura da cabeça
ONDAS = [("rabo", N_RABO, (1.2, 2.0, 0.0))]
ANIM_PARADO = {"barbela": [(0, 0, 0), (5, 0, 2), (0, 0, 0), (4, 0, -2), (0, 0, 0)]}
ANIM_ANDANDO = {"barbela": [(0, 0, 0), (9, 0, 4), (0, 0, 0), (9, 0, -4), (0, 0, 0)]}

# ---------------- paleta (da ficha) ----------------
AREIA = (234, 172, 92); AREIA_CLARA = (248, 208, 136); AREIA_ESC = (204, 136, 64); AREIA_FUNDA = (150, 92, 44)
GLIFO = (56, 36, 58)                      # roxo quase preto dos padrões tribais
CRISTA = (206, 40, 46); CRISTA_CLARA = (236, 78, 66); CRISTA_ESC = (146, 22, 34)
BICO = (252, 190, 34); BICO_ESC = (226, 128, 16)
PERNA = (226, 152, 60); PERNA_ESC = (182, 108, 40)
GARRA = (48, 32, 56); GARRA_CLARA = (92, 70, 106)
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

def decalque(bitmap, centro, normal, eixo_u, cel, frente=4.0, tras=4.0, espelho=False):
    """Glifo projetado ao longo de 'normal' sobre tudo o que estiver entre centro - tras*n e centro + frente*n.
    eixo_u: direção das colunas do desenho (a 'direita' do glifo); a 'subida' é normal x eixo_u."""
    n = norm(normal); u = norm(eixo_u)
    u = norm([u[i] - n[i] * sum(u[k] * n[k] for k in range(3)) for i in range(3)])
    v = cruz(n, u)
    if espelho: u = [-a for a in u]
    DECALQUES.append(dict(bm=bitmap, c=list(centro), n=n, u=u, v=v, cel=cel, frente=frente, tras=tras,
                          W=len(bitmap[0]), H=len(bitmap)))

def glifo_em(pw, nw):
    for d in DECALQUES:
        n = d["n"]
        if nw[0] * n[0] + nw[1] * n[1] + nw[2] * n[2] < 0.35: continue
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

def mat_areia(faixa=(0.0, 44.0), ladrilho=(2.4, 2.0), base=AREIA, borda=.14, ponta=None, glifos=True):
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
            if fv < 0.13: luz -= 0.30                     # ponta escura da pena (borda de baixo)
            elif fv > 0.8: luz -= 0.10                    # sombra embaixo da pena de cima
            else: luz += 0.06 * (0.8 - fv)
            if fh < 0.06 or fh > 0.97: luz -= 0.14
        if ponta is not None:
            ei, inv = ponta
            lo, hi = c["b"][0][ei], c["b"][1][ei]
            tt = clamp((c["p"][ei] - lo) / max(hi - lo, 1e-6))
            if inv: tt = 1 - tt
            cor = mix(cor, AREIA_CLARA, 0.35 * tt)
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

# ---------------- cabeça ----------------
OLHO_Y = 35.3
FAC_A, FAC_B = (4.7, -8.6), (2.0, -11.3)      # quina chanfrada do rosto (lado +x), o olho fica nela
FAC_T = 2.0
FAC_L = math.dist(FAC_A, FAC_B)
_m = ((FAC_A[0] + FAC_B[0]) / 2, (FAC_A[1] + FAC_B[1]) / 2)
FAC_C = (_m[0] - 0.7071 * FAC_T / 2, _m[1] + 0.7071 * FAC_T / 2)

def mat_faceta(lado, areia):
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u = z - FAC_C[1]; dy = y - OLHO_Y
            o = pintar_olho(u - 0.1, dy + 0.1, 1.55, 1.05, iris=((240, 158, 16), (255, 244, 150)), esclera=OLHO,
                            r_iris=(0.56, 0.7), c_iris=(-0.3, -0.12), r_pup=(0.24, 0.36), brilho=(255, 255, 230),
                            bravo=0.55, alto=0.32, contorno=GLIFO)
            if o: return o
            e = ((u + 0.15) / 1.9) ** 2 + ((dy + 0.75) / 1.6) ** 2
            if e <= 1: return tom(PELE, -0.05 - 0.25 * clamp(-dy / 2.5) if not g.na_borda(c) else -0.3)
        return areia(c)
    return f

def so_olho(c, cor): return cor[0] > 200 and cor[1] > 120 and cor[2] < 140

def montar_cabeca():
    cab = []
    ma = mat_areia(faixa=(29, 40), ladrilho=(1.7, 1.4))
    cab += arredondado2("cranio", [-4.9, 30.8, -8.8], [4.9, 38.3, -2.4], ma, r=1.6)
    cab += arredondado("testa", [-2.4, 30.8, -12.1], [2.4, 37.9, -8.0], ma, r=0.8)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 31.4, cz - FAC_L / 2], [cx + FAC_T / 2, 38.0, cz + FAC_L / 2],
                        mat_faceta(lado, ma), rot=(0, 45 * lado, 0), pivo=(cx, 35, cz), res=8, brilho=so_olho))
        # sobrancelha: placa escura grossa sobre o olho, descendo para o bico (cara brava)
        fx0, fx1 = sorted((cx + FAC_T / 2 * lado - 0.3 * lado, cx + FAC_T / 2 * lado + 0.9 * lado))
        cab.append(osso("sobrancelha_q_" + s, [cx, 36.6, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_q_" + s, [fx0, 35.9, cz - 2.6], [fx1, 37.2, cz + 1.9], mat_voxel(GLIFO, (84, 60, 84), 1, borda=.15),
                 rot=(-20, 0, 0), pivo=(cx, 36.6, cz))]))
        # parte de trás da sobrancelha, no lado da cabeça
        x0, x1 = sorted((4.4 * lado, 5.3 * lado))
        cab.append(peca("sobrancelha_l_" + s, [x0, 36.6, -9.0], [x1, 37.6, -5.6], mat_voxel(GLIFO, (84, 60, 84), 1, borda=.15),
                        rot=(-6, 0, 0), pivo=(4.8 * lado, 37, -7)))
        # sobrancelha da frente: da quina desce para o bico (V bravo de frente)
        x0, x1 = sorted((0.2 * lado, 2.6 * lado))
        cab.append(peca("sobrancelha_f_" + s, [x0, 35.9, -12.6], [x1, 37.1, -11.7], mat_voxel(GLIFO, (84, 60, 84), 1, borda=.15),
                        rot=(0, 0, 24 * lado), pivo=(2.6 * lado, 36.5, -12.1)))
    # bico grande em cunha com gancho
    def cor_bico(p, face):
        x, y, z = p
        if face in ("east", "west") and abs(z + 13.7) < 0.35 and abs(y - 34.6) < 0.3: return (150, 76, 20)   # narina
        if face in ("east", "west", "north") and 32.55 < y < 32.85: return (120, 50, 20)                      # linha da boca
        if face == "down": return BICO_ESC
        return mix(BICO, BICO_ESC, clamp((-z - 13.2) / 4.0) * 0.7 + clamp((33.5 - y) / 2.0) * 0.3)
    mb = g.mat_cor(cor_bico, borda=.08, curva=.4)
    cab.append(peca("bico_base", [-2.1, 32.4, -14.6], [2.1, 35.6, -11.6], mb, faixa=(31, 36)))
    cab.append(peca("bico_meio", [-1.6, 32.5, -16.3], [1.6, 35.2, -14.4], mb, rot=(-10, 0, 0), pivo=(0, 35.2, -14.4), faixa=(31, 36)))
    cab.append(peca("bico_gancho", [-1.15, 31.2, -17.3], [1.15, 34.0, -16.1], g.mat_cor(cor_bico, borda=.08, curva=.6),
                    rot=(-22, 0, 0), pivo=(0, 34.0, -16.1), faixa=(31, 36)))
    cab.append(peca("bico_baixo", [-1.5, 31.4, -15.4], [1.5, 32.6, -11.6], g.mat_cor(lambda p, f: BICO_ESC, borda=.12)))
    # barbela: dois blocos vermelhos compridos pendurados embaixo do bico (osso próprio: balança)
    mv_ = mat_voxel(CRISTA_CLARA, CRISTA_ESC, 1, inverte=True)
    barb = []
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x = 1.2 * lado
        barb.append(osso("barbela_" + s, [x, 31.8, -12.6], [-22, 0, -8 * lado], [
            peca("barbela_" + s, [x - 1.15, 25.4, -14.0], [x + 1.15, 31.8, -11.8], mv_),
            peca("barbela2_" + s, [x - 0.85, 24.0, -13.7], [x + 0.85, 25.6, -12.1], mv_)]))
    cab.append(osso("barbela", [0, 31.8, -12.4], [0, 0, 0], barb))
    cab.append(peca("papada", [-2.4, 30.0, -12.2], [2.4, 31.8, -10.0], mat_voxel(CRISTA, CRISTA_ESC, 1, inverte=True)))
    # crista: leque de lâminas vermelhas em cubos, do alto da testa para trás
    crista = []
    mc = mat_voxel(CRISTA_ESC, CRISTA_CLARA, 1)
    crista.append(peca("crista_base", [-1.5, 37.4, -11.0], [1.5, 39.6, -2.8], mc))
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
RABO = [  # (comprimento, largura x, espessura, curva rx do osso): desce atrás, sobe e enrola para a frente
    (8.5, 14.0, 12.0, 18), (8.5, 15.5, 11.2, -10), (8.0, 16.5, 9.6, -20), (7.6, 16.5, 9.2, -27), (6.8, 14.6, 8.6, -30),
    (6.2, 12.0, 8.0, -32), (5.8, 9.0, 7.2, -34), (5.4, 8.6, 6.4, -36), (5.0, 8.2, 5.6, -38), (4.6, 7.4, 4.8, -42)]

RABO_Y = 16.8

def montar_cauda(ma_nucleo, ma_pena):
    y0 = RABO_Y
    def seg(k, z):
        L, W, T, curva = RABO[k]
        s = f"rabo_{k}"
        za = z - (1.2 if k else 0.0)          # o núcleo entra no segmento anterior: fecha a cunha de fora da curva
        filhos = [peca(s + "_a", [-W / 2, y0 - T / 2 + 0.8, za], [W / 2, y0 + T / 2 - 0.8, z + L], ma_nucleo),
                  peca(s + "_b", [-W / 2 + 1.0, y0 - T / 2, za], [W / 2 - 1.0, y0 + T / 2, z + L], ma_nucleo)]
        # pena de fora (lado de fora da curva = -y): bloco largo passando do fim do segmento, ponta em degrau
        yb = y0 - T / 2
        filhos.append(osso(s + "_pf", [0, yb + 0.6, z + 0.2 * L], [4 if k < 3 else 18, 0, 0], [
            peca(s + "_pf", [-W * 0.44, yb - 1.0, z + 0.2 * L], [W * 0.44, yb + 0.6, z + 1.2 * L], ma_pena),
            peca(s + "_pf2", [-W * 0.26, yb - 0.8, z + 1.15 * L], [W * 0.26, yb + 0.4, z + 1.5 * L], ma_pena)]))
        # pena solta espetada para fora (contorno de fora serrilhado, como a plumagem da ficha)
        if 3 <= k <= 7:
            xo = W * 0.22 * (1 if k % 2 else -1)
            filhos.append(osso(s + "_pe", [xo, yb + 0.4, z + 0.55 * L], [32, 8 * (1 if k % 2 else -1), 0], [
                peca(s + "_pe", [xo - W * 0.17, yb - 0.8, z + 0.55 * L], [xo + W * 0.17, yb + 0.4, z + 1.25 * L + 1.2], ma_pena),
                peca(s + "_pe2", [xo - W * 0.09, yb - 0.6, z + 1.25 * L + 1.1], [xo + W * 0.09, yb + 0.2, z + 1.25 * L + 2.4], ma_pena)]))
        # camadas dos lados: placas grossas que passam do fim do segmento e abrem um pouco para fora
        for lado in ((-1, 1) if k < 6 else ()):
            ld = "d" if lado < 0 else "e"
            xb = lado * (W / 2 - 0.6)
            x0, x1 = sorted((xb - 0.4 * lado, xb + 1.1 * lado))
            filhos.append(osso(f"{s}_pl{ld}", [xb, y0, z + 0.15 * L], [4, 9 * lado, 0], [
                peca(f"{s}_pl{ld}", [x0, y0 - T * 0.5 - 0.3, z + 0.15 * L], [x1, y0 + T * 0.32, z + 0.95 * L], ma_pena),
                peca(f"{s}_pl{ld}_p", [x0 + 0.1, y0 - T * 0.42, z + 0.9 * L], [x1 - 0.1, y0 + T * 0.02, z + 1.3 * L], ma_pena)]))
        # pena de dentro (lado de dentro da curva, +y), só onde aparece
        if k <= 7:
            yt = y0 + T / 2
            filhos.append(osso(s + "_pd", [0, yt - 0.8, z + 0.25 * L], [-18, 0, 0], [
                peca(s + "_pd", [-W * 0.4, yt - 0.8, z + 0.25 * L], [W * 0.4, yt + 1.0, z + 1.2 * L], ma_pena)]))
        if k + 1 < len(RABO): filhos.append(seg(k + 1, z + L - 0.4))
        else:
            # leque de penas na ponta da espiral
            for j, (ry, rx, Lp, Wp) in enumerate([(-30, -34, 5.0, 4.0), (0, -46, 5.8, 4.4), (30, -34, 5.0, 4.0)]):
                zp = z + L - 0.8
                filhos.append(osso(f"{s}_leque{j}", [0, y0, zp], [rx, ry, 0], [
                    peca(f"{s}_leque{j}", [-Wp / 2, y0 - 1.6, zp], [Wp / 2, y0 + 1.0, zp + Lp], ma_pena),
                    peca(f"{s}_leque{j}_p", [-Wp * 0.3, y0 - 1.3, zp + Lp - 0.1], [Wp * 0.3, y0 + 0.7, zp + Lp + 1.6], ma_pena)]))
        return osso(s, [0, y0, z], [curva, 0, 0], filhos)
    return seg(0, 10.5)

# ---------------- montagem ----------------
def montar():
    MUNDO.clear(); PINTAS.clear(); DECALQUES.clear()
    ma = mat_areia(faixa=(4, 34))
    mp = mat_areia(faixa=(4, 34), ladrilho=None, ponta=(1, True), borda=.2)

    # ---------- cabeça e pescoço ----------
    i_cab = len(g.PECAS)
    cab = montar_cabeca()
    g.transformar(i_cab, cab, (0.0, 31.0, -7.0), k=K_CAB, sobe=SOBE_CAB)
    cabeca = osso("cabeca", [0, 31.0 + SOBE_CAB, -7.0], [0, 0, 0], cab)
    pesc = []
    pesc += arredondado("pescoco", [-5.6, 24.5, -10.2], [5.6, 31.0, -1.5], mat_areia(faixa=(20, 36), ladrilho=(1.9, 1.6)), r=1.4)
    for k, (phi, y, L) in enumerate([(-90, 28.0, 5.6), (-62, 28.2, 6.0), (-30, 28.6, 6.6), (2, 29.2, 7.0), (36, 29.8, 7.0), (72, 30.4, 6.6)]):
        for lado in (-1, 1):
            if phi == -90: continue
            x, z = anel(5.6, 5.4, -6.2, phi, lado)
            pesc.append(pena_anel(f"gola{k}_{'d' if lado < 0 else 'e'}", (x, y, z), phi, 22, L, 4.2, 1.5, lado, mp, varre=4))
    for k, (phi, y, L) in enumerate([(-76, 25.2, 5.6), (-44, 25.4, 6.0), (-12, 25.8, 6.2), (22, 26.4, 6.0)]):
        for lado in (-1, 1):
            x, z = anel(7.4, 6.8, -5.6, phi, lado)
            pesc.append(pena_anel(f"gola_b{k}_{'d' if lado < 0 else 'e'}", (x, y, z), phi, 30, L, 4.6, 1.5, lado, mp, varre=2))
    pesc.append(cabeca)
    pescoco = osso("pescoco", [0, 26.0, -5.0], [-INCLINA, 0, 0], pesc)

    # ---------- corpo: ovo enorme, peito alto, traseira larga ----------
    corpo = []
    corpo += arredondado2("tronco", [-11.0, 8.0, -11.0], [11.0, 27.4, 11.5], ma, r=3.6)
    corpo += arredondado("barriga", [-13.0, 6.6, -9.6], [13.0, 19.0, 9.8], ma, r=3.0)
    corpo += arredondado("peito", [-9.0, 11.5, -13.6], [9.0, 26.6, -6.0], ma, r=2.6)
    # corpo += arredondado("dorso", [-8.6, 24.0, -6.5], [8.6, 29.6, 4.0], ma, r=2.2)
    corpo += arredondado("anca", [-9.4, 10.0, 8.0], [9.4, 24.0, 14.6], ma, r=2.6)

    # saia de penas embaixo da barriga (contorno serrilhado de frente e de lado)
    for k, phi in enumerate([-86, -62, -38, -14, 10, 34, 58]):
        for lado in (-1, 1):
            x, z = anel(11.0, 11.4, 0.4, phi, lado)
            corpo.append(pena_anel(f"saia{k}_{'d' if lado < 0 else 'e'}", (x, 12.6 + 0.4 * (k % 2), z), phi, 16,
                                   6.0 + 0.6 * (k % 2), 4.4, 1.6, lado, mp, varre=4))
    # sela: penas em bloco nas costas, deitadas para trás em direção à cauda (tira o degrau do dorso)
    for k, (x, y, z, L, W) in enumerate([(0.0, 29.8, -2.0, 7.0, 6.0), (-4.6, 29.0, -1.4, 6.6, 5.0), (4.6, 29.0, -1.4, 6.6, 5.0),
                                         (0.0, 27.6, 3.6, 7.0, 6.4), (-5.0, 26.8, 4.0, 6.4, 5.2), (5.0, 26.8, 4.0, 6.4, 5.2),
                                         (0.0, 24.6, 8.4, 6.4, 6.8), (-5.4, 23.8, 8.6, 6.0, 5.4), (5.4, 23.8, 8.6, 6.0, 5.4)]):
        corpo.append(pena_bloco(f"sela{k}", (x, y, z), (-(46 - 6 * (k // 3)), -x * 1.6, 0), L, W, 1.6, mp, eixo="x"))
    # fileira do peito (penas em bloco sob a gola)

    # ---------- asas: ombro redondo, asa grossa e penas em bloco na barra ----------
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = []
        x0, x1 = sorted((10.2 * lado, 15.2 * lado))
        asa += arredondado2("ombro_" + s, [x0, 18.5, -10.4], [x1, 27.4, 1.6], ma, r=2.6)
        x0, x1 = sorted((11.8 * lado, 15.6 * lado))
        asa += arredondado("asa_" + s, [x0, 13.0, -9.0], [x1, 24.0, 8.6], ma, r=1.4)
        for k, (z, L, varre, fl) in enumerate([(-7.6, 5.6, 6, 8), (-4.4, 6.4, 10, 10), (-1.2, 7.0, 14, 11),
                                               (2.0, 7.4, 20, 12), (5.2, 7.2, 28, 12), (8.0, 6.6, 38, 12)]):
            asa.append(pena_anel(f"asa{k}_{s}", (14.4 * lado, 14.6, z), 0, fl, L, 3.8, 2.6, lado, mp, varre=varre))
        for k, (y, z, L, varre) in enumerate([(22.4, -8.2, 5.0, 4), (22.6, -4.4, 5.4, 6), (22.8, -0.6, 5.4, 10)]):
            asa.append(pena_anel(f"cobertura{k}_{s}", (15.4 * lado, y, z), 0, 10, L, 4.0, 2.0, lado, mp, varre=varre))
        for k, (y, z, L, varre) in enumerate([(27.4, -8.0, 5.2, 2), (27.6, -4.2, 5.6, 4), (27.4, -0.4, 5.4, 8)]):
            asa.append(pena_anel(f"ombreira{k}_{s}", (14.2 * lado, y, z), 0, 28, L, 4.2, 2.2, lado, mp, varre=varre))
        corpo.append(osso("asa_" + s, [12.0 * lado, 25.0, -3.0], [0, 0, 4 * lado], asa))

    # ---------- cauda gigante enrolada ----------
    cauda = montar_cauda(mat_areia(faixa=(0, 42), ladrilho=(2.8, 2.2)), mat_areia(faixa=(0, 42), ladrilho=(3.0, 2.4), ponta=(2, False), borda=.2))
    corpo.append(osso("cauda", [0, RABO_Y, 10.5], [0, 0, 0], [cauda]))
    corpo.append(pescoco)
    tronco = osso("corpo", [0, 13.0, 0], [INCLINA, 0, 0], corpo)

    # ---------- pernas grossas: coxa de penas, canela laranja, dedos grossos e garras escuras ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 6.2 * lado; zc = 1.0
        pp = []
        pp += arredondado("coxa_" + s, [xc - 3.4, 6.0, zc - 3.6], [xc + 3.4, 13.0, zc + 3.6], mat_areia(faixa=(3, 14), ladrilho=(1.8, 1.5)), r=1.2)
        for k, phi in enumerate([-60, 0, 60]):
            x, z = anel(3.3, 3.3, zc, phi, 1)
            pp.append(pena_anel(f"calca{k}_{s}", (xc + x * lado, 8.0, z), phi, 18, 3.8, 3.2, 1.2, lado, mp))
        mperna = mat_voxel(PERNA, PERNA_ESC, 1, inverte=True, cel=1.2)
        pp += octogono("canela_" + s, [xc - 2.7, 2.0, zc - 2.7], [xc + 2.7, 7.4, zc + 2.7], mperna, r=0.9)
        mdedo = mat_voxel(PERNA, PERNA_ESC, 1, inverte=True, cel=1.2)
        mg = mat_voxel(GARRA_CLARA, GARRA, 1, inverte=True, cel=0.8, borda=.25)
        for nome, giro, dx in (("meio", 0, 0), ("fora", -22 * lado, 2.0 * lado), ("dentro", 22 * lado, -2.0 * lado)):
            x0, z0 = xc + dx * 0.6, zc - 1.0
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - 1.3, 0, z0 - 4.6], [x0 + 1.3, 2.7, z0 + 0.8], mdedo),
                osso(f"garra_{nome}_{s}", [x0, 0.0, z0 - 4.6], [0, 0, 0], [
                    peca(f"garra_{nome}_{s}", [x0 - 1.05, 0.0, z0 - 6.6], [x0 + 1.05, 2.3, z0 - 4.3], mg),
                    peca(f"garra2_{nome}_{s}", [x0 - 0.7, 0.0, z0 - 7.6], [x0 + 0.7, 1.3, z0 - 6.5], mg)])]))
        pp.append(peca("dedo_tras_" + s, [xc - 0.9, 0, zc + 1.0], [xc + 0.9, 1.8, zc + 3.6], mdedo))
        pp.append(peca("garra_tras_" + s, [xc - 0.7, 0, zc + 3.4], [xc + 0.7, 1.4, zc + 4.8], mg))
        return osso("perna_" + s, [xc, 12.0, zc], [0, 0, 0], pp)

    raizes = [tronco, perna(-1), perna(1)]
    calcular_mundo(raizes)
    glifos()
    return raizes

def glifos():
    """Os decalques de glifo (posições no mundo). Os da cauda acompanham os segmentos já girados."""
    for lado in (-1, 1):
        decalque(G_OLHO, (15.6 * lado, 19.4, -0.6), (lado, 0, 0), (0, 0, -lado), 1.12, frente=3, tras=3.5)
        decalque(G_PASSO, (14.8 * lado, 11.2, 6.0), (lado, 0, 0), (0, 0, -lado), 0.9, frente=3, tras=3.5)
        decalque(G_GANCHO, (11.8 * lado, 13.6, 10.6), (lado, 0, 0), (0, 0, -lado), 0.9, frente=3, tras=3)
        decalque(G_DENTE, (8.2 * lado, 25.0, -6.0), (lado, 0.3, -0.3), (0, 0, -lado), 0.8, frente=2.5, tras=2.5)
        decalque(G_CRUZ, (5.4 * lado, 15.0, -13.0), (0, 0, -1), (-1, 0, 0), 0.9, frente=5, tras=5)
        decalque(G_GANCHO, (5.6 * lado, 26.0, 9.0), (0, 1, 0.3), (lado, 0, 0), 0.9, frente=4, tras=3, espelho=lado < 0)
    for lado in (-1, 1):
        decalque(G_QUADRO, (14.6 * lado, 18.6, -11.0), (0, 0, -1), (-1, 0, 0), 0.75, frente=3, tras=3)
    decalque(G_CHEVRON, (0, 22.6, -14.0), (0, 0, -1), (-1, 0, 0), 0.9, frente=4, tras=4)
    decalque(G_DENTE, (0, 14.4, -13.0), (0, 0, -1), (-1, 0, 0), 0.9, frente=5, tras=5)
    decalque(G_PASSO, (0, 30.0, 2.0), (0, 1, 0), (1, 0, 0), 1.0, frente=3, tras=3)
    # cauda: glifos nos lados de alguns segmentos e o 'sol' na face de fora (vista de trás)
    for k, bm, cel in ((2, G_QUADRO, 1.0), (4, G_ESPIRAL, 1.0), (6, G_OLHO, 0.85), (8, G_CRUZ, 0.8)):
        L, W, T, _ = RABO[k]
        nome = f"rabo_{k}_a"
        p = g.PECAS[[q.nome for q in g.PECAS].index(nome)]
        cz = (p.de[2] + p.ate[2]) / 2
        eixo = norm(dir_mundo(nome, (0, 0, 1)))
        for lado in (-1, 1):
            c = ponto_mundo(nome, (lado * W / 2, RABO_Y, cz))
            decalque(bm, c, (lado, 0, 0), [-e * lado for e in eixo], cel, frente=2.5, tras=2.5)
    for k, bm, cel in ((5, G_SOL, 1.0), (7, G_OLHO, 0.9)):
        L, W, T, _ = RABO[k]
        nome = f"rabo_{k}_a"
        p = g.PECAS[[q.nome for q in g.PECAS].index(nome)]
        cz = (p.de[2] + p.ate[2]) / 2
        n = norm(dir_mundo(nome, (0, -1, 0)))
        c = ponto_mundo(nome, (0, RABO_Y - T / 2, cz))
        decalque(bm, c, n, (1, 0, 0), cel, frente=3, tras=3)

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
