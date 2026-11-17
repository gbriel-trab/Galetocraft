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
ROSTO = ((0, 25.0, -13.4), 7.6)
ONDAS = []
ANIM_PARADO = {}
ANIM_ANDANDO = {}


# ---------------- paleta: AMOSTRADA nos PNGs da ficha (Paleta de Cores + arte + expressão neutra) ----------------
# quadrados da Paleta de Cores: creme (253,226,185) bege (230,159,92) marrom (154,86,43) marrom escuro (110,62,35)
# verde escuro (101,126,13) verde-lima (146,170,7) amarelo (252,192,3) vermelho (224,26,27) cinza (79,63,61).
# Conferidos com a auditoria n27 (#FDE2B9, #E79E5C, #9D562C, #6E3E25, #8FA908, #647F0D, #FDBE02, #E21719, #50403F):
# batem com a paleta da ficha a menos de 5 de diferença por canal.
CREME = (253, 226, 185); CREME_2 = (255, 209, 152)          # creme e creme-caramelo claro (blocos da cara e do peito)
BEGE = (231, 158, 92); CARAMELO = (206, 128, 62)
MARROM = (157, 86, 44); MARROM_ESC = (110, 62, 37); MARROM_CLARO = (146, 92, 62)
SOBR = (92, 65, 56); SOBR_CLARA = (128, 96, 82)             # sobrancelha marrom-acinzentada (#5C4138)
VERDE_LIMA = (150, 176, 10); VERDE_OLIVA = (104, 132, 14)   # metades da folha (#8FA908 / #647F0D, um pouco mais claras)
VERDE_BORDA = (84, 108, 10)
AMARELO_BICO = (253, 190, 2); LARANJA_BICO = (208, 128, 2)  # mandíbula de cima / de baixo
VERM = (226, 23, 25); VERM_ESC = (170, 14, 18)
GARRA = (80, 64, 63); GARRA_CLARA = (108, 90, 88); GARRA_ESC = (52, 40, 40)
CANELA = (231, 158, 92); CANELA_ESC = (196, 120, 58)
# olho (expressão neutra): íris limão-amarelada com crescente verde embaixo, pupila preta do lado do bico, esclera creme
IRIS_LIMAO = (226, 228, 30); IRIS_VERDE = (44, 120, 16); PUPILA = (8, 10, 4); ESCLERA = (253, 238, 210)

def tom(c, f):
    """Luz quente e contida (substitui a de galo_base, que puxa a sombra para o roxo): f > 0 clareia um pouco para
    o creme, f < 0 escurece para um marrom quente (sem avermelhar nem acinzentar)."""
    f = clamp(f, -1, 1)
    if f >= 0: return mix(c, (255, 240, 205), f * .40)
    return mix(c, (int(c[0] * .55), int(c[1] * .42), int(c[2] * .32)), -f * .95)

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

# ---------------- espinhos: cones lisos e grossos (auditoria n27, itens 1 e 2) ----------------
# 4 blocos que afinam devagar (sem placas, sem serrilha) e degradê de família: marrom na raiz, caramelo no meio,
# creme na ponta (nada de cinza nem branco).
SEG_ESPINHO = ((0.00, 0.40, 1.00), (0.36, 0.64, 0.70), (0.60, 0.84, 0.44), (0.80, 1.00, 0.18))
ESP_A = (MARROM, BEGE, CREME)
ESP_B = ((130, 72, 38), (214, 140, 80), (250, 216, 172))       # família um pouco mais escura (espinhos do fundo)

def cor_espinho(v, cores):
    c0, c1, c2 = cores
    if v < 0.5: return mix(c0, c1, v / 0.5)
    return mix(c1, c2, (v - 0.5) / 0.38)

def mat_espinho(y0, L, cores):
    luzes = {"north": 0.0, "east": -.04, "south": -.14, "west": -.08, "up": 0.0, "down": -.18}
    def f(c):
        return tom(cor_espinho(clamp((c["p"][1] - y0) / L), cores), luzes[c["face"]])
    return f

def espinho(nome, raiz, d, L, W, cores=ESP_A, torce=45):
    x, y, z = raiz
    m = mat_espinho(y, L, cores)
    pecas = []
    for k, (a, b, fw) in enumerate(SEG_ESPINHO):
        w = W * fw
        pecas.append(peca(f"{nome}_{k}", [x - w / 2, y + a * L, z - w / 2], [x + w / 2, y + b * L, z + w / 2], m, res=2))
    return osso(nome, list(raiz), apontar(d), [osso(nome + "_t", list(raiz), [0, torce, 0], pecas)])

# ---------------- folhas: lanceoladas de ponta aguda, nervura dividindo limão e oliva, sem contorno ----------------
def mat_folha(cx, cy, diag=False):
    def f(c):
        x, y, z = c["p"]
        face = c["face"]
        if face in ("north", "south"):
            u = (x - cx) - (y - cy) if diag else (x - cx)
            return VERDE_LIMA if u >= 0 else VERDE_OLIVA
        if face == "up": return VERDE_LIMA
        return VERDE_BORDA
    return f

def folha(nome, raiz, d, L, W, fora=None, esp=1.0, torce=None):
    """Folha grossa que cresce na direção d: losango na base, faixa no meio, losango e um losango menor na ponta
    (ponta aguda). A face larga fica virada para 'fora'."""
    x, y, z = raiz
    if torce is None: torce = torcao_para(d, fora or [0, 0, -1])
    e = esp / 2; h = W / 2
    ya = y + h; yb = y + L - 1.5 * h; yc = y + L - 0.5 * h
    pecas = [peca(nome + "_meio", [x - W * .46, ya, z - e], [x + W * .46, yb, z + e], mat_folha(x, 0), res=3)]
    for k, (yy, lado_q) in enumerate(((ya, W / math.sqrt(2)), (yb, W / math.sqrt(2)), (yc, 0.5 * W / math.sqrt(2)))):
        ee = e * (0.9 if k < 2 else 0.8)
        pecas.append(peca(f"{nome}_l{k}", [x - lado_q / 2, yy - lado_q / 2, z - ee], [x + lado_q / 2, yy + lado_q / 2, z + ee],
                          mat_folha(x, yy, diag=True), rot=(0, 0, 45), pivo=(x, yy, z), res=3))
    return osso(nome, list(raiz), apontar(d), [osso(nome + "_t", list(raiz), [0, torce, 0], pecas)])

# ---------------- cabeça (auditoria itens 3, 4, 5, 8, 9 e 10) ----------------
HW = 5.4          # meia largura da cabeça
QX = 2.0          # meia largura da frente reta (onde nasce o bico)
ZF = -13.8        # frente da cabeça (avançada 1.2 em relação à n27: a cabeça fica à frente do peito)
ZB = -3.6         # nuca
FL = math.hypot(HW - QX, HW - QX)       # comprimento da face diagonal (olho)
ZS = ZF + (HW - QX)                     # z onde a face diagonal encontra o lado
FT = 2.0                                # espessura da peça da face diagonal
CAB_Y0, CAB_Y1 = 20.6, 28.4
OLHO_Y = 25.2
OLHO_RU, OLHO_RV = 1.75, 1.2

def bloco2(a, b, x, y, z, passo=1.6):
    """Dois tons em blocos grandes (legíveis), sem ruído."""
    return a if (math.floor(y / passo) + math.floor((x + z) / passo)) % 2 == 0 else b

def cor_cabeca(p, face):
    x, y, z = p
    if face == "up": return VERDE_OLIVA                                  # o topo fica sob a base da crista
    if y < OLHO_Y - OLHO_RV + 0.1 and z < ZF + 6.6:                       # faixa creme sob o olho, do bico ao meio
        return bloco2(CREME, CREME_2, x, y, z)
    q = (math.floor((y - 20) / 1.6) * 7 + math.floor((z + x) / 1.6) * 3) % 3
    return (MARROM_CLARO, MARROM, (128, 74, 40))[q]

def fc_centro(lado):
    mx, mz = (QX + HW) / 2, (ZF + ZS) / 2
    n = (0.7071, -0.7071)
    return (lado * (mx - n[0] * FT / 2), mz - n[1] * FT / 2)

def olho_neutro(u, v):
    """Olho da expressão neutra, numa face plana. u: ao longo da face (negativo = para o bico), v: para cima.
    Semicerrado: o topo é cortado reto pela sobrancelha, mais baixo do lado do bico (um 'D' deitado).
    Íris limão com crescente verde embaixo, pupila preta encostada no lado do bico com 1 ponto de brilho,
    esclera creme só atrás da íris."""
    ru, rv = OLHO_RU, OLHO_RV
    if (abs(u) / ru) ** 4 + (abs(v) / rv) ** 4 > 1: return None
    if v > rv * (0.30 + 0.32 * u / ru): return None                     # pálpebra/sobrancelha cobre ~40% de cima
    pu, pv = -0.95, 0.05
    dp = math.hypot(u - pu, v - pv)
    if math.hypot(u - (pu + 0.2), v - (pv + 0.22)) < 0.14: return (255, 255, 240)   # brilho
    if dp < 0.48: return PUPILA
    if u < 0.25:
        if dp < 0.95 and v < pv + 0.15: return IRIS_VERDE
        if v < -rv + 0.2: return mix(IRIS_LIMAO, IRIS_VERDE, .4)
        return IRIS_LIMAO
    if v < -rv + 0.16: return (214, 186, 150)                            # junta com o bloco creme de baixo
    return ESCLERA

def mat_faceta(lado):
    base = mat_bloco(cor_cabeca, borda=-.06, faixas=False)
    fora = "east" if lado > 0 else "west"
    cx, cz = fc_centro(lado)
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u = z - cz + 0.1
            cor = olho_neutro(u, y - OLHO_Y)
            if cor is not None: return cor
            if y < OLHO_Y - OLHO_RV + 0.1: return bloco2(CREME, CREME_2, x, y, z)
            return MARROM_CLARO
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face == "down": return LARANJA_BICO
    if face in ("east", "west") and ZF - 1.3 < z < ZF - 0.7 and 25.2 < y < 25.8: return (40, 24, 10)   # narina
    if face == "up": return mix(AMARELO_BICO, (255, 230, 110), .3)
    if face == "north": return AMARELO_BICO if y > 22.9 else mix(AMARELO_BICO, LARANJA_BICO, .5)
    return mix(AMARELO_BICO, LARANJA_BICO, .15 + .5 * clamp((24.0 - y) / 2.5))

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
    # sobrancelhas: lajes grossas marrom-acinzentadas em V, dentro da largura da cabeça, terminando na base do bico;
    # atrás, só um tufo curto (do outro lado, em 3/4, aparece só ele)
    msob = mat_tons(SOBR_CLARA, SOBR, (52, 36, 32), lado=mix(SOBR, SOBR_CLARA, .25))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = fc_centro(lado)
        ox = cx + lado * (FT / 2)
        x0, x1 = sorted((ox - 1.3 * lado, ox + 0.45 * lado))
        cab.append(osso("sobrancelha_" + s, [cx, 27.0, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s, [x0, 26.4, cz - FL / 2 - 0.4], [x1, 28.0, cz + FL / 2 + 0.5], msob,
                 rot=(-18, 0, 0), pivo=(cx, 27.2, cz), res=4)]))
        x0, x1 = sorted(((HW - 1.0) * lado, (HW + 0.25) * lado))
        cab.append(peca("sobrancelha_tufo_" + s, [x0, 27.0, ZS - 0.2], [x1, 28.4, ZS + 1.8], msob, res=4))
    # bico maciço: avança ~1/3 da cabeça, 3 blocos que estreitam e descem (de frente, triângulo para baixo com o
    # topo reto entre as sobrancelhas; de lado, gancho 1 bloco abaixo da mandíbula de cima)
    mb0 = mat_bloco(cor_bico, borda=-.12, faixas=False)
    mb1 = mat_bloco(cor_bico, borda=0, faixas=False)
    mb = lambda c: (mb1 if c["face"] == "north" else mb0)(c)
    cab.append(peca("bico_base", [-1.4, 23.2, ZF - 1.7], [1.4, 26.2, ZF + 0.3], mb, res=4))
    cab.append(peca("bico_meio", [-0.95, 22.7, ZF - 2.9], [0.95, 25.7, ZF - 1.6], mb, res=4))
    cab.append(peca("bico_gancho", [-0.5, 21.9, ZF - 3.6], [0.5, 25.0, ZF - 2.8], mb, res=4))
    cab.append(peca("bico_baixo", [-0.6, 21.9, ZF - 2.2], [0.6, 23.2, ZF + 0.2],
                    mat_tons(mix(LARANJA_BICO, AMARELO_BICO, .3), LARANJA_BICO, (150, 88, 4)), res=4))
    # barbela: dois lobos largos que se tocam no meio sob o bico e abrem para baixo (Λ), grossos de lado
    mbb = mat_bloco(lambda p, f: VERM_ESC if f in ("east", "west") and abs(p[0]) < 0.6 else VERM, borda=-.10)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.02 * lado, 2.3 * lado))
        x2, x3 = sorted((0.3 * lado, 2.0 * lado))
        cab.append(osso("barbela_" + s, [0.0, 22.8, ZF - 0.6], [0, 0, 10 * lado], [
            peca("barbela_" + s, [x0, 18.8, ZF - 1.7], [x1, 22.8, ZF + 0.3], mbb, res=4),
            peca("barbela_ponta_" + s, [x2, 17.7, ZF - 1.5], [x3, 19.0, ZF + 0.1], mbb, res=4)]))
    # crista: folhas planas pontudas iguais às da asa; a central é a maior; saem da testa, varrem ~35° para trás
    # e vão até a nuca, cobrindo o topo
    crista = []
    yt = CAB_Y1 - 0.6
    CF = [(0, 32, 12.5, 4.6, 0.0, 3.4), (-20, 36, 10.5, 4.0, 0.7, 3.8), (20, 36, 10.5, 4.0, 0.7, 3.8),
          (-40, 40, 8.0, 3.4, 1.0, 4.2), (40, 40, 8.0, 3.4, 1.0, 4.2)]
    for k, (ang, tras, L, W, vira, dz) in enumerate(CF):
        a, t = math.radians(ang), math.radians(tras)
        d = [math.sin(a) * math.cos(t), math.cos(a) * math.cos(t), math.sin(t)]
        crista.append(folha(f"crista{k}", (1.4 * math.sin(a) * 1.6, yt, ZF + dz), d, L, W, esp=1.2,
                            fora=[math.copysign(vira, ang) if ang else 0, 0.3, -1]))
    for k, (ang, tras, L, W, dz) in enumerate(((-6, 54, 10.5, 4.0, 6.2), (6, 54, 10.5, 4.0, 6.2), (0, 68, 9.5, 3.8, 8.4))):
        a, t = math.radians(ang), math.radians(tras)
        d = [math.sin(a), math.cos(t), math.sin(t)]
        crista.append(folha(f"crista_tras{k}", (1.2 * math.sin(a), yt, ZF + dz), d, L, W, esp=1.2,
                            fora=[1 if k % 2 == 0 else -1, 0.1, 0]))
    for k, lado in enumerate((-1, 1)):
        crista.append(folha(f"crista_topo{k}", (2.0 * lado, yt, ZF + 5.4), [0.55 * lado, 0.55, 0.62], 6.6, 4.0, esp=1.1,
                            fora=[lado * 0.6, 1, 0]))
        crista.append(folha(f"crista_nuca{k}", (2.2 * lado, yt - 0.4, ZB - 1.2), [0.25 * lado, 0.7, 0.7], 8.6, 4.0, esp=1.2,
                            fora=[lado, 0.2, 0]))
    cab.append(osso("crista", [0, CAB_Y1, ZF + 5.0], [0, 0, 0], crista))
    return cab

# ---------------- corpo ----------------
def meia_peito(y):
    """Meia largura do peito creme na altura y: largo sob a barbela, afinando em degraus até a barriga."""
    return 0.9 + 4.4 * clamp((y - 9.2) / 12.0)

def cor_corpo(p, face):
    x, y, z = p
    if z < -9.6 and abs(x) < meia_peito(y) + 0.5 and y > 9.0:
        return CREME if abs(x) < meia_peito(y) else BEGE
    # penas marrons em escamas grandes (fileiras de 2 unidades, desencontradas)
    fila = math.floor((24 - y) / 2.0)
    fy = ((24 - y) / 2.0) % 1.0
    ang = math.atan2(x, -z) * 7.0
    fx = ((ang + (0.5 if fila % 2 else 0)) / 2.4) % 1.0
    base = MARROM if y > 11 and z < 0 else MARROM_ESC          # o dorso, à sombra dos espinhos, é marrom-escuro
    if fy > 0.78: return tom(base, -.14)
    if fx < 0.08: return tom(base, -.08)
    return base

def cor_peito(p, face):
    """'Flor Peitoral': blocos escalonados em dois tons (creme e creme-caramelo), beirada bege."""
    x, y, z = p
    if face == "north":
        if meia_peito(y + 1.0) - abs(x) < 0: return BEGE
        fila = math.floor((y - 9.2) / 2.0)
        col = math.floor((x + 0.85 * (fila % 2)) / 1.7)
        return CREME if (col + fila) % 2 == 0 else CREME_2
    return CREME_2

def montar():
    cab = montar_cabeca()
    cabeca = osso("cabeca", [0, 22.0, -8.0], [0, 0, 0], cab)
    mp = mat_bloco(lambda p, f: bloco2(CREME, CREME_2, *p) if p[2] < -9.5 else MARROM, borda=-.06, faixas=False)
    pescoco = osso("pescoco", [0, 21.0, -7.0], [0, 0, 0], [
        peca("pescoco", [-4.6, 18.6, -12.6], [4.6, 23.0, -4.0], mp, res=2),
        cabeca])

    corpo = []
    mt = mat_bloco(cor_corpo, borda=-.04, faixas=False)
    corpo += g.arredondado2("tronco", [-7.6, 6.2, -11.4], [7.6, 22.6, 8.6], mt, r=3.0)
    corpo += g.arredondado("dorso", [-6.6, 12.0, -6.0], [6.6, 25.6, 9.6], mt, r=2.4)
    # 'Flor Peitoral': fileiras de blocos creme que estreitam para baixo (degraus em V), o creme sobe até a garganta
    mpe = mat_bloco(cor_peito, borda=-.08, faixas=False)
    PEITO = [(19.0, 21.4, 5.2, -13.4), (17.0, 19.2, 4.6, -13.2), (15.0, 17.2, 3.9, -12.9), (13.0, 15.2, 3.2, -12.6),
             (11.0, 13.2, 2.4, -12.2), (9.2, 11.2, 1.6, -11.8)]
    for k, (y0, y1, w, zf) in enumerate(PEITO):
        corpo.append(peca(f"peito{k}", [-w, y0, zf], [w, y1, -10.6], mpe, res=4))

    # penas marrons em bloco: saia da barriga e, nas costas, o 1/3 de baixo (abaixo dos espinhos, até as coxas)
    msaia = mat_tons(MARROM, MARROM_ESC, (70, 44, 30), lado=mix(MARROM_ESC, MARROM, .4))
    for k, ang in enumerate(range(-160, 180, 36)):
        a = math.radians(ang)
        px, pz = 7.0 * math.sin(a), -1.4 - 9.6 * math.cos(a)
        corpo.append(peca(f"saia{k}", [px - 1.6, 5.2, pz - 0.7], [px + 1.6, 8.6, pz + 0.7], msaia,
                          rot=(0, -ang, 0), pivo=(px, 6.9, pz)))
    for fila, (y0, y1, angs) in enumerate(((8.2, 11.6, (130, 155, 180, 205, 230)), (10.8, 14.2, (142, 168, 192, 218)))):
        for k, ang in enumerate(angs):
            a = math.radians(ang)
            px, pz = 7.2 * math.sin(a), -0.6 - 9.8 * math.cos(a)
            corpo.append(peca(f"pena_costas{fila}_{k}", [px - 1.7, y0, pz - 0.8], [px + 1.7, y1, pz + 0.8], msaia,
                              rot=(0, -ang, 0), pivo=(px, (y0 + y1) / 2, pz)))

    # ---------- espinhos: poucos cones grossos irradiando das costas ----------
    C0, R0 = (0.0, 19.6, 3.0), (6.6, 7.6, 7.0)
    C1, R1 = (0.0, 20.0, 5.0), (12.6, 16.6, 18.4)
    R1_BAIXO = 13.6
    esp_corpo, cauda = [], []
    N = 54; n = 0
    ouro = math.pi * (3 - math.sqrt(5))
    for i in range(N):
        sy = 1 - 2 * (i + 0.5) / N
        r = math.sqrt(1 - sy * sy)
        th = ouro * i
        sx, sz = r * math.cos(th), r * math.sin(th)
        if sz < 0.18: continue                        # nada para a frente nem reto para o lado (não cruza as folhas)
        if sy < -0.35 and sz < 0.62: continue         # embaixo, só os que vão para trás (de lado, até o topo da perna)
        ry = R1[1] if sy > 0 else R1_BAIXO
        raiz = (C0[0] + R0[0] * sx, C0[1] + R0[1] * sy, C0[2] + R0[2] * sz)
        k_ = (abs(sx) ** 2.7 + abs(sy) ** 2.7 + abs(sz) ** 2.7) ** (-1 / 2.7)
        k_ = 1 + (k_ - 1) * 0.8
        ponta = (C1[0] + R1[0] * sx * (1 - 0.6 * max(sy, 0)), C1[1] + ry * sy * k_, C1[2] + R1[2] * sz * k_)
        d = [ponta[k] - raiz[k] for k in range(3)]
        L = math.sqrt(sum(v * v for v in d)) + 0.6
        dn = norm(d)
        teta = math.degrees(math.acos(clamp(dn[2], -1, 1)))
        fi = math.atan2(dn[0], dn[1]) if math.hypot(dn[0], dn[1]) > 0.08 else math.atan2(sx, sy)
        teta2 = math.radians(max(teta, 30 + 0.5 * teta))
        d = [math.sin(teta2) * math.sin(fi), math.sin(teta2) * math.cos(fi), math.cos(teta2)]
        L *= 1.0 + 0.24 * clamp((60 - teta) / 60)
        if d[1] < -0.40:
            d[1] = -0.40; d = norm(d)
        W = 7.0 if L > 9 else 6.0
        cores = ESP_B if (i * 7) % 4 == 0 else ESP_A
        q = espinho(f"espinho{n}", raiz, d, L, W, cores, torce=45)
        (cauda if sz > 0.55 and sy < 0.25 else esp_corpo).append(q)
        n += 1
    corpo.append(osso("espinhos", list(C0), [0, 0, 0], esp_corpo))
    corpo.append(osso("cauda", [0, 15.0, 8.0], [0, 0, 0], cauda))

    # ---------- asas: 'Plumagem Folhosa' em leque saindo do ombro (de cima para trás, de baixo para baixo) ----------
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = []
        # (x, y, z da raiz, para trás (0 = para baixo, 90 = para trás), abertura para fora, L, W)
        ASA = [(6.4, 21.6, -10.8, 8, 16, 11.5, 3.2), (6.8, 21.6, -9.2, 26, 18, 11.5, 3.2), (7.0, 21.8, -7.6, 44, 18, 11.0, 3.2),
               (7.0, 22.0, -6.0, 62, 16, 10.5, 3.2), (6.8, 22.4, -4.6, 80, 14, 9.6, 3.0),
               (6.2, 24.4, -11.2, 30, 32, 7.6, 2.8), (6.2, 23.6, -10.0, 58, 28, 8.4, 3.0), (6.4, 23.8, -8.2, 76, 24, 8.4, 3.0),
               (6.4, 24.0, -6.4, 92, 20, 8.0, 2.8)]
        for k, (x0, y0, z0, tras, abre, L, W) in enumerate(ASA):
            t, a = math.radians(tras), math.radians(abre)
            d = [lado * math.sin(a), -math.cos(t) * math.cos(a), math.sin(t) * math.cos(a)]
            asa.append(folha(f"asa{k}_{s}", (x0 * lado, y0, z0), d, L, W, fora=[lado, 0.2, -0.2]))
        corpo.append(osso("asa_" + s, [6.6 * lado, 22.0, -7.0], [0, 0, 0], asa))

    corpo.append(pescoco)
    tronco = osso("corpo", [0, 9.0, 0.0], [0, 0, 0], corpo)

    # ---------- pernas: coxa marrom, canela grossa laranja, dedos em bloco e garras em cunha cinza-escuro ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 4.1 * lado; zc = 0.0
        pp = []
        mcx = mat_tons(mix(MARROM, BEGE, .3), MARROM, MARROM_ESC, lado=mix(MARROM, MARROM_ESC, .3))
        pp += g.octogono("coxa_" + s, [xc - 2.5, 4.6, zc - 2.5], [xc + 2.5, 9.0, zc + 2.5], mcx, r=0.8)
        mca = mat_tons(mix(CANELA, CREME, .3), CANELA, CANELA_ESC, lado=mix(CANELA, CANELA_ESC, .5))
        pp += g.octogono("canela_" + s, [xc - 2.1, 1.0, zc - 2.1], [xc + 2.1, 5.0, zc + 2.1], mca, r=0.5)
        mpe = mat_tons(mix(CANELA, CREME, .3), CANELA, CANELA_ESC, lado=mix(CANELA, CANELA_ESC, .5))
        mg = mat_tons(GARRA_CLARA, GARRA, GARRA_ESC, lado=mix(GARRA, GARRA_ESC, .4))
        pp.append(peca("pe_" + s, [xc - 2.4, 0.0, zc - 2.4], [xc + 2.4, 1.6, zc + 1.8], mpe))
        for nome, giro, dx in (("meio", 0, 0), ("fora", -20 * lado, 2.3 * lado), ("dentro", 20 * lado, -2.3 * lado)):
            x0, z0 = xc + dx, zc - 2.2
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - .85, 0, z0 - 2.2], [x0 + .85, 1.8, z0 + 0.3], mpe),
                peca(f"garra_{nome}_{s}", [x0 - .8, 0.0, z0 - 3.2], [x0 + .8, 2.2, z0 - 2.0], mg),
                peca(f"garra_ponta_{nome}_{s}", [x0 - .6, 0.0, z0 - 4.1], [x0 + .6, 1.3, z0 - 3.1], mg)]))
        pp.append(peca("dedo_tras_" + s, [xc - .8, 0, zc + 1.6], [xc + .8, 1.5, zc + 2.8], mpe))
        pp.append(peca("garra_tras_" + s, [xc - .7, 0, zc + 2.7], [xc + .7, 1.6, zc + 3.8], mg))
        return osso("perna_" + s, [xc, 9.0, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
