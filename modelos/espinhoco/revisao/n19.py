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

# ---------------- paleta: AMOSTRADA nos PNGs da ficha (Paleta de Cores + arte + expressão neutra) ----------------
# paleta da ficha: creme (253,226,185) bege (230,159,92) marrom (154,86,43) marrom escuro (110,62,35)
# verde escuro (101,126,13) verde-lima (146,170,7) amarelo (252,192,3) vermelho (224,26,27) cinza (79,63,61).
# As cores-base ficam um pouco mais claras que o alvo, porque a luz das faces (no jogo e na prévia) escurece ~20%.
CREME = (255, 230, 190); CREME_ESC = (236, 190, 136)
BEGE = (238, 168, 98); CARAMELO = (206, 128, 62)
MARROM = (164, 92, 44); MARROM_ESC = (118, 64, 34); CHOCOLATE = (78, 58, 58); CHOCOLATE_CLARO = (128, 88, 64)
VERDE_ESC = (122, 142, 14); VERDE = (168, 186, 18); VERDE_CLARO = (206, 218, 52); CONTORNO_FOLHA = (74, 90, 8)
AMARELO_BICO = (255, 200, 12); AMARELO_ESC = (236, 156, 8); LARANJA_BICO = (196, 112, 12)
VERM = (234, 34, 30); VERM_ESC = (168, 16, 20)
GARRA = (84, 66, 64); GARRA_CLARA = (116, 96, 92); GARRA_ESC = (48, 36, 36)
CANELA = (214, 132, 58); CANELA_CLARA = (238, 162, 88)
OLHO_IRIS = ((84, 140, 8), (186, 226, 44))
ESCLERA = (252, 246, 232)

def tom(c, f):
    """Luz QUENTE (substitui a de galo_base, que puxa a sombra para o roxo e acinzenta): f > 0 clareia para um
    creme quente, f < 0 escurece para o marrom-escuro quente das sombras da ficha (~(60,30,8))."""
    f = clamp(f, -1, 1)
    if f >= 0: return mix(c, (255, 244, 214), f * .45)
    return mix(c, (int(c[0] * .42), int(c[1] * .26), int(c[2] * .10)), -f * .95)

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
# cores de família (amostradas na arte): raiz marrom-escura -> caramelo -> bege -> creme na ponta
ESP_CLARO = ((112, 58, 24), (204, 128, 64), (248, 188, 124), (255, 238, 204))
ESP_ESCURO = ((92, 46, 18), (170, 98, 44), (220, 150, 84), (246, 208, 158))
SEG_ESPINHO = ((0.00, 0.40, 1.00), (0.36, 0.62, 0.72), (0.58, 0.78, 0.46))   # (início, fim, largura): miolo grosso
PONTA_ESP = (0.72, 0.68)                                                       # ponta afiada: começa em 72%, largura 68%

def cor_espinho(v, cores):
    """Degradê liso ao longo do espinho (v = 0 na raiz, 1 na ponta)."""
    c0, c1, c2, c3 = cores
    if v < 0.3: return mix(c0, c1, v / 0.3)
    if v < 0.62: return mix(c1, c2, (v - 0.3) / 0.32)
    return mix(c2, c3, (v - 0.62) / 0.3)

def mat_espinho(y0, L, cores):
    """Miolo do espinho: degradê de família ao longo do comprimento, 2 faces claras e 2 em sombra (facetas)."""
    luzes = {"north": .12, "east": .04, "south": -.16, "west": -.08, "up": .10, "down": -.22}
    def f(c):
        v = clamp((c["p"][1] - y0) / L)
        luz = luzes[c["face"]]
        if c["face"] not in ("up", "down") and (c["i"] == 0 or c["i"] == c["tw"] - 1): luz -= .12
        return tom(cor_espinho(v, cores), luz)
    return f

def mat_ponta(y0, L, yb, Lp, Wp, eixo, centro, luz0, cores):
    """Ponta afiada (triângulo de lados retos): aresta clara no meio, uma metade em sombra."""
    def f(c):
        x, y, z = c["p"]
        t = (y - yb) / Lp
        if t < -0.01 or t > 1: return None
        u = ((x if eixo == "x" else z) - centro) / (Wp / 2)
        meia = 1 - max(t, 0)
        if abs(u) > meia: return None
        luz = luz0 + (0.12 if abs(u) < 0.16 else -0.14 if u > 0 else 0.02)
        if meia - abs(u) < 0.12: luz -= 0.12
        return tom(cor_espinho(clamp((y - y0) / L), cores), luz)
    return f

def espinho(nome, raiz, d, L, W, cores=ESP_CLARO, torce=45):
    """Espinho liso e afiado: miolo de 3 blocos grossos que afinam (a base some no corpo) e a ponta em X de duas
    placas recortadas em triângulo, alinhadas às quinas do miolo (de qualquer lado lê como um cone pontudo)."""
    x, y, z = raiz
    pecas = []
    for k, (a, b, fw) in enumerate(SEG_ESPINHO):
        w = W * fw
        pecas.append(peca(f"{nome}_{k}", [x - w / 2, y + a * L, z - w / 2], [x + w / 2, y + b * L, z + w / 2],
                          mat_espinho(y, L, cores), res=2))
    yb = y + PONTA_ESP[0] * L; Lp = y + L - yb; Wp = W * PONTA_ESP[1]; e = 0.5
    pecas.append(osso(nome + "_p", [x, yb, z], [0, 45, 0], [
        peca(nome + "_pa", [x - e / 2, yb, z - Wp / 2], [x + e / 2, yb + Lp, z + Wp / 2], mat_ponta(y, L, yb, Lp, Wp, "z", z, .02, cores), res=4),
        peca(nome + "_pb", [x - Wp / 2, yb, z - e / 2], [x + Wp / 2, yb + Lp, z + e / 2], mat_ponta(y, L, yb, Lp, Wp, "x", x, -.06, cores), res=4)]))
    return osso(nome, list(raiz), apontar(d), [osso(nome + "_t", list(raiz), [0, torce, 0], pecas)])

# ---------------- folhas grossas (lanceoladas, em 3 degraus, 2 tons divididos na nervura) ----------------
FOLHA_PADRAO = (VERDE_CLARO, VERDE, VERDE_ESC)

def mat_folha(cx, cy, cores=FOLHA_PADRAO, diag=False):
    """Folha: as duas metades da face larga em 2 tons (clara / média, divididas na nervura), laterais escuras.
    diag=True: peça girada 45° no próprio plano (losango), então a nervura é a diagonal da caixa."""
    claro, medio, escuro = cores
    def f(c):
        x, y, z = c["p"]
        face = c["face"]
        if face in ("north", "south"):
            u = (x - cx) - (y - cy) if diag else (x - cx)
            cor = claro if u >= 0 else medio
            if not diag and (c["i"] == 0 or c["i"] == c["tw"] - 1): cor = tom(cor, -.18)
            if diag and borda_px(c): cor = tom(cor, -.18)
            return cor
        if face == "up": return tom(claro, -.05)
        return tom(escuro, -.08 if borda_px(c) else 0)
    return f

def folha(nome, raiz, d, L, W, fora=None, cores=FOLHA_PADRAO, esp=1.0, torce=None):
    """Folha grossa (espessura esp) que cresce na direção d: hexágono alongado e pontudo nas duas pontas
    (losango da base + faixa do meio + losango da ponta). A face larga fica virada para 'fora'."""
    x, y, z = raiz
    if torce is None: torce = torcao_para(d, fora or [0, 0, -1])
    e = esp / 2
    h = W / 2                      # meia diagonal dos losangos
    a = W / math.sqrt(2)           # lado do quadrado girado
    ya, yb = y + h, y + L - h
    pecas = [peca(nome + "_meio", [x - W * .46, ya, z - e], [x + W * .46, yb, z + e], mat_folha(x, 0, cores), res=3)]
    for k, yc in enumerate((ya, yb)):
        pecas.append(peca(f"{nome}_{'base' if k == 0 else 'ponta'}", [x - a / 2, yc - a / 2, z - e * .9], [x + a / 2, yc + a / 2, z + e * .9],
                          mat_folha(x, yc, cores, diag=True), rot=(0, 0, 45), pivo=(x, yc, z), res=3))
    return osso(nome, list(raiz), apontar(d), [osso(nome + "_t", list(raiz), [0, torce, 0], pecas)])

# ---------------- cabeça ----------------
HW = 5.4          # meia largura da cabeça
QX = 2.0          # meia largura da frente reta (onde nasce o bico)
ZF = -12.6        # frente da cabeça
ZB = -3.6         # nuca
FL = math.hypot(HW - QX, HW - QX)       # comprimento da face diagonal (olho)
ZS = ZF + (HW - QX)                     # z onde a face diagonal encontra o lado
FT = 2.0                                # espessura da peça da face diagonal
CAB_Y0, CAB_Y1 = 20.6, 28.9
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
            cor = pintar_olho(u + 0.1, y - OLHO_Y, 1.75, 1.45, iris=OLHO_IRIS, c_iris=(-0.24, -0.1), esclera=ESCLERA,
                              r_iris=(0.66, 0.84), r_pup=(0.24, 0.32), bravo=0.30, alto=0.48, contorno=CHOCOLATE)
            if cor is not None: return cor
            if y < OLHO_Y - 0.5: return CREME
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face == "down": return LARANJA_BICO
    if face in ("east", "west") and abs(z + 14.6) < 0.4 and abs(y - 25.2) < 0.4: return (40, 24, 10)    # narina quadrada
    if face == "up": return mix(AMARELO_BICO, (255, 236, 120), .35)
    if face in ("east", "west"): return mix(AMARELO_BICO, AMARELO_ESC, .35 + .4 * clamp((24.4 - y) / 3.0))
    # de frente: aresta clara no meio, metades mais escuras (lê como cunha)
    if abs(x) < 0.45: return mix(AMARELO_BICO, AMARELO_ESC, clamp((24.0 - y) / 3.0))
    return mix(AMARELO_BICO, AMARELO_ESC, .45)

def mat_cor_baixo():
    """Bico de baixo: amarelo-alaranjado, com a linha escura da boca no alto das laterais."""
    def f(c):
        x, y, z = c["p"]
        if c["face"] in ("east", "west", "north") and y > 23.2: return (70, 34, 10)
        return tom(mix(AMARELO_ESC, LARANJA_BICO, .3), {"up": .1, "down": -.3}.get(c["face"], -.05))
    return f

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
    cab += g.octogono("bochechas", [-HW - 0.3, CAB_Y0 - 0.2, ZF + 1.1], [HW + 0.3, 23.5, -6.4], mbo, r=1.6, res=4)
    # sobrancelhas: lajes chocolate grossas, descendo para o bico (cara brava)
    msob = mat_tons(CHOCOLATE_CLARO, CHOCOLATE, (40, 26, 22), lado=mix(CHOCOLATE, CHOCOLATE_CLARO, .3))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = fc_centro(lado)
        ox = cx + lado * (FT / 2)
        x0, x1 = sorted((ox - 0.8 * lado, ox + 1.2 * lado))
        cab.append(osso("sobrancelha_" + s, [cx, 27.3, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s, [x0, 26.2, cz - FL / 2 - 1.7], [x1, 28.1, cz + FL / 2 + 0.9], msob,
                 rot=(-17, 0, 0), pivo=(cx, 27.3, cz), res=4)]))
        x0, x1 = sorted(((HW - 0.6) * lado, (HW + 0.8) * lado))
        cab.append(peca("sobrancelha_lado_" + s, [x0, 27.0, ZS - 0.9], [x1, 28.6, ZS + 3.0], msob,
                        rot=(-4, 0, 0), pivo=(HW * lado, 27.8, ZS), res=4))
    # bico: 3 degraus que estreitam e descem (de frente vira um triângulo; de lado, gancho para baixo)
    mb = mat_bloco(cor_bico, borda=-.12, faixas=False)
    # cunha pequena e afilada: de frente, larga no alto (entre os olhos) e com a ponta embaixo no meio
    cab.append(peca("bico_base", [-1.75, 25.0, -13.6], [1.75, 26.7, -12.3], mb, res=4))
    cab.append(peca("bico_meio", [-1.3, 23.9, -14.6], [1.3, 26.2, -13.2], mb, res=4))
    cab.append(peca("bico_meio2", [-0.85, 22.7, -15.5], [0.85, 25.6, -14.2], mb, res=4))
    cab.append(peca("bico_gancho", [-0.45, 21.5, -16.2], [0.45, 24.6, -15.2], mb, res=4))
    cab.append(peca("bico_baixo", [-0.9, 21.9, -15.0], [0.9, 23.7, -12.4], mat_cor_baixo(), res=4))
    # barbela: dois lóbulos vermelhos em bloco, pendurados sob o bico
    mbb = mat_bloco(lambda p, f: VERM_ESC if f in ("east", "west") and abs(p[0]) < 1.0 else VERM, borda=-.12)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.35 * lado, 2.2 * lado))
        x2, x3 = sorted((0.55 * lado, 2.0 * lado))
        cab.append(osso("barbela_" + s, [0.35 * lado, 22.4, -13.2], [0, 0, -2 * lado], [
            peca("barbela_" + s, [x0, 18.9, -14.3], [x1, 22.9, -12.3], mbb, res=4),
            peca("barbela_ponta_" + s, [x2, 17.8, -14.1], [x3, 19.1, -12.5], mbb, res=4)]))
    # crista de folhas grossas: leque da frente (de frente lê como a coroa da ficha) e leque de trás (de lado)
    crista = []
    # leque da frente: (ângulo para o lado, inclinação para trás, L, W, quanto a face vira para o lado)
    CF = [(0, 2, 12.6, 3.8, 0.0), (-17, 6, 10.2, 3.4, 0.8), (17, 6, 10.2, 3.4, 0.8), (-34, 12, 7.4, 3.0, 1.0),
          (34, 12, 7.4, 3.0, 1.0)]
    for k, (ang, tras, L, W, vira) in enumerate(CF):
        a, t = math.radians(ang), math.radians(tras)
        d = [math.sin(a), math.cos(a), math.sin(t)]
        crista.append(folha(f"crista{k}", (1.6 * math.sin(a), 27.8, -9.4), d, L, W, esp=1.3,
                            fora=[math.copysign(vira, ang) if ang else 0, 0, -1]))
    # leque de cima e de trás: folhas de lado (de perfil fazem a massa da crista da ficha)
    CT = [(0, -22, 10.0, 4.0, -9.0), (0, 8, 11.6, 4.0, -7.8), (-6, 30, 11.0, 3.8, -6.8), (6, 30, 11.0, 3.8, -6.8), (0, 52, 10.0, 3.8, -5.8)]
    for k, (ang, tras, L, W, z0) in enumerate(CT):
        a, t = math.radians(ang), math.radians(tras)
        d = [math.sin(a), math.cos(t), math.sin(t)]
        crista.append(folha(f"crista_tras{k}", (1.0 * math.sin(a), 28.2, z0), d, L, W, esp=1.3,
                            fora=[1 if k % 2 == 0 else -1, 0.1, 0]))
    # folhas da nuca: fecham o vão entre a cabeça e a bola de espinhos (de perfil)
    for k, lado in enumerate((-1, 1)):
        crista.append(folha(f"crista_nuca{k}", (2.2 * lado, 28.0, -5.0), [0.25 * lado, 0.75, 0.66], 8.6, 4.4, esp=1.2,
                            fora=[lado, 0.2, 0]))
    cab.append(osso("crista", [0, 29.0, -8.0], [0, 0, 0], crista))
    return cab

# ---------------- corpo ----------------
def meia_peito(y):
    """Meia largura do peito creme na altura y: largo sob a barbela, afinando em degraus até a barriga."""
    return 0.9 + 4.4 * clamp((y - 9.2) / 12.0)

def cor_corpo(p, face):
    x, y, z = p
    if z < -9.6 and abs(x) < meia_peito(y) + 0.5 and y > 9.0:
        return CREME_ESC if abs(x) < meia_peito(y) else CARAMELO
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
    """Mosaico de blocos creme (2 tons próximos, blocos de 1.8 x 2 desencontrados por fileira), beirada bege."""
    x, y, z = p
    if face == "north":
        borda = meia_peito(y + 1.0) - abs(x)
        if borda < 0: return mix(CREME_ESC, CARAMELO, .5)      # beirada bege-caramelo, puxando para o marrom
        # escamas: cada fileira de 2 unidades tem escamas de 1.8 com a ponta em U embaixo
        fila = math.floor((y - 9.2) / 2.0)
        v = ((y - 9.2) / 2.0) % 1.0
        u = ((x + 0.9 * (fila % 2)) / 1.8) % 1.0 - 0.5
        curva = 0.42 * (2 * u) ** 2
        if v < curva - 0.10: return CREME_ESC                   # vão entre as pontas das escamas
        if v < curva + 0.08: return mix(CREME_ESC, CARAMELO, .35)  # contorno da escama
        cor = CREME if borda > 1.0 else mix(CREME, CREME_ESC, .5)
        return tom(cor, .08) if v > 0.8 else cor
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
    mpe = mat_bloco(cor_peito, borda=-.10, faixas=False)
    mpe_res = 4
    PEITO = [(19.0, 21.4, 5.2, -12.9), (17.0, 19.2, 4.6, -12.8), (15.0, 17.2, 3.9, -12.6), (13.0, 15.2, 3.2, -12.3),
             (11.0, 13.2, 2.4, -11.9), (9.2, 11.2, 1.6, -11.5)]
    for k, (y0, y1, w, zf) in enumerate(PEITO):
        corpo.append(peca(f"peito{k}", [-w, y0, zf], [w, y1, -10.6], mpe, res=mpe_res))

    # saia de penas marrons em bloco na barriga (borda de baixo em degraus, como na ficha)
    msaia = mat_tons(mix(MARROM, CARAMELO, .25), MARROM_ESC, (70, 44, 30), lado=mix(MARROM_ESC, MARROM, .3))
    for k, ang in enumerate(range(-160, 180, 36)):
        a = math.radians(ang)
        px, pz = 7.0 * math.sin(a), -1.4 - 9.6 * math.cos(a)
        corpo.append(peca(f"saia{k}", [px - 1.6, 5.2, pz - 0.7], [px + 1.6, 8.6, pz + 0.7], msaia,
                          rot=(0, -ang, 0), pivo=(px, 6.9, pz)))

    # ---------- espinhos: bola de cones grossos das costas ----------
    # raiz numa elipsoide das costas, ponta numa elipsoide maior (medida nas vistas da ficha)
    C0, R0 = (0.0, 18.6, 3.0), (6.8, 8.0, 7.0)
    C1, R1 = (0.0, 20.0, 5.0), (12.8, 16.6, 18.0)
    R1_BAIXO = 14.6
    esp_corpo, cauda = [], []
    N = 80; n = 0
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
        # explosão: nenhum espinho aponta reto para trás; todos abrem para fora a partir do centro das costas
        dn = norm(d)
        teta = math.degrees(math.acos(clamp(dn[2], -1, 1)))
        fi = math.atan2(dn[0], dn[1]) if math.hypot(dn[0], dn[1]) > 0.08 else math.atan2(sx, sy)
        teta2 = math.radians(max(teta, 32 + 0.48 * teta))
        d = [math.sin(teta2) * math.sin(fi), math.sin(teta2) * math.cos(fi), math.cos(teta2)]
        L *= 1.0 + 0.26 * clamp((60 - teta) / 60)
        if d[1] < -0.45:                               # os de baixo não descem até o chão
            d[1] = -0.45; d = norm(d); L *= 0.9
        W = 5.2 if L > 9 else 4.2
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
        ASA = [(6.4, 21.4, -10.6, 4, 20, 15.0, 4.8), (7.0, 21.4, -8.6, 24, 24, 14.6, 5.0), (7.2, 21.6, -6.6, 48, 26, 13.0, 5.0),
               (7.2, 22.0, -4.6, 72, 24, 11.2, 4.8), (7.0, 22.8, -3.2, 96, 18, 9.6, 4.4),
               (6.4, 24.0, -9.8, 40, 46, 8.4, 4.4), (6.4, 24.4, -7.4, 84, 36, 8.4, 4.2)]
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
        for nome, giro, dx in (("meio", 0, 0), ("fora", -20 * lado, 2.3 * lado), ("dentro", 20 * lado, -2.3 * lado)):
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
