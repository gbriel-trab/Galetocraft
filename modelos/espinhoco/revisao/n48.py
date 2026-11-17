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
SOBR = (86, 54, 38); SOBR_CLARA = (128, 86, 60)             # sobrancelha marrom-acinzentada (#5C4138)
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

# ---------------- paleta da 2ª auditoria (MEDIDA na ficha; onde a auditoria diverge, vale a ficha) ----------------
# Espinhos (faixas de brilho medidas na lateral da ficha): raiz (102,55,27), meio (163,106,64) e (199,145,98),
# claro (237,191,146), ponta (250,229,197). São mais saturados que os ≤35% da auditoria; segui a ficha.
ESP_RAMPA = ((104, 58, 30), (176, 120, 74), (214, 164, 114), (240, 200, 156), (250, 230, 198))
# Folhas: na ficha o verde é lima-AMARELADO (r ≈ g, quase sem azul): mediana (140,146,10), claro (166..200,170..200,15).
LIMA_LUZ = (186, 196, 26); LIMA_BASE = (150, 164, 14); LIMA_SOMBRA = (112, 126, 10); NERVURA = (210, 218, 70)
CREME_BOCH = (246, 224, 190); CREME_BOCH_SOMBRA = (224, 196, 156)
BICO_OURO = (246, 196, 22); BICO_SOMBRA = (217, 154, 16); BOCA = (90, 58, 16)
BARBELA = (216, 35, 30); BARBELA_SOMBRA = (158, 21, 21)
PENA_1 = (139, 90, 53); PENA_2 = (110, 68, 40); PENA_3 = (168, 112, 63)   # penas do corpo (#8B5A35 / #6E4428 / #A8703F)
CANELA_PERNA = (194, 122, 52); CANELA_LUZ = (222, 150, 74); GARRA_ESCURA = (74, 68, 72)
IRIS_VIVA = (206, 226, 30); IRIS_ANEL = (58, 130, 16)

# ---------------- espinhos: cones afiados, 5 segmentos encaixados (cada um ~70% do anterior) e levemente curvos ----------------
SEG_LARG = (1.0, 0.76, 0.54, 0.34, 0.14)   # afina em linha reta até a ponta: cone de base larga como na arte
SEG_COMP = (0.28, 0.24, 0.20, 0.16, 0.12)

def mat_seg_espinho(v0, v1):
    """Segmento do espinho: cor da rampa da ficha pela posição ao longo do espinho; facetas claras e escuras
    alternando em volta; a face de baixo ~15% mais escura; sem moldura na face da ponta."""
    luzes = {"north": .04, "east": -.02, "south": -.16, "west": -.10, "up": -.04, "down": -.16}   # degrau sem "prateleira" clara
    def f(c):
        (_, y0, _), (_, y1, _) = c["b"]
        t = clamp((c["p"][1] - y0) / max(y1 - y0, 1e-6))
        v = (v0 + (v1 - v0) * t) ** 0.8          # arte: o marrom fica só na raiz, o cone é quase todo bege-creme
        k = v * (len(ESP_RAMPA) - 1)
        i = min(int(k), len(ESP_RAMPA) - 2)
        cor = mix(ESP_RAMPA[i], ESP_RAMPA[i + 1], k - i)
        return tom(cor, luzes[c["face"]])
    return f

def espinho(nome, raiz, d, L, W, curva=6.0, torce=0):
    """Cone afiado: 5 segmentos encaixados (ossos em cadeia) que afinam até uma ponta de ~0,6 e curvam 'curva' graus
    por segmento (para cima/para trás)."""
    total = sum(SEG_COMP)
    comps = [L * c / total for c in SEG_COMP]
    def seg(k, pos, v0):
        x, y, z = pos
        Lk, w = comps[k], W * SEG_LARG[k]
        v1 = v0 + comps[k] / L
        filhos = [peca(f"{nome}_{k}", [x - w / 2, y - 0.25, z - w / 2], [x + w / 2, y + Lk + (0.25 if k < len(comps) - 1 else 0), z + w / 2],
                       mat_seg_espinho(v0, min(v1, 1.0)), res=2)]
        if k + 1 < len(comps): filhos.append(seg(k + 1, (x, y + Lk, z), v1))
        return osso(f"{nome}_s{k}", list(pos), [curva if k else 0, 0, 0], filhos)
    return osso(nome, list(raiz), apontar(d), [osso(nome + "_t", list(raiz), [0, torce, 0], [seg(0, raiz, 0.0)])])

# ---------------- folhas largas lanceoladas (capa dos ombros, crista): bloco + estreitamento + ponta em losango ----------------
def mat_folha_larga(cx, eixo_u, cy=None, diag=False):
    """Face larga: metade luz e metade base divididas por uma nervura clara de 1 px; espessura em sombra; raiz um pouco
    mais escura. Sem pixels quase pretos e sem contorno serrilhado."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        larga = ("east", "west") if eixo_u == "z" else ("north", "south")
        if face in larga:
            u = (z if eixo_u == "z" else x) - cx
            if diag: u = u + (y - cy) if eixo_u == "z" else u - (y - cy)
            if abs(u) < 0.22: return NERVURA
            return LIMA_LUZ if u > 0 else LIMA_BASE
        if face == "up": return LIMA_BASE
        return LIMA_SOMBRA
    return f

def folha_capa(nome, raiz, phi, lado, L, W, flare=18, varre=0, T=1.0):
    """Folha larga pendurada da raiz (como a folha-pena do Esporocó aprovado): corpo da largura toda, faixa que
    estreita e ponta em losango. phi = ângulo em volta do corpo (0 = para fora, -90 = frente, +90 = trás);
    flare abre a ponta para fora; varre puxa a ponta para trás."""
    x, y, z = raiz
    Lb = L * 0.62; Lm = L * 0.20
    wm = W * 0.62; s = wm / 1.4142
    m = mat_folha_larga(z, "z")
    corpo = peca(nome, [x - T / 2, y - Lb, z - W / 2], [x + T / 2, y, z + W / 2], m, res=3)
    meio = peca(nome + "_m", [x - T / 2 + .02, y - Lb - Lm, z - wm / 2], [x + T / 2 - .02, y - Lb + 0.1, z + wm / 2], m, res=3)
    yp = y - Lb - Lm
    ponta = peca(nome + "_pt", [x - T / 2 + .04, yp - s / 2, z - s / 2], [x + T / 2 - .04, yp + s / 2, z + s / 2],
                 mat_folha_larga(z, "z", yp, diag=True), rot=(45, 0, 0), pivo=(x, yp, z), res=3)
    return osso(nome, list(raiz), [0, -phi * lado, 0], [osso(nome + "_p", list(raiz), [-varre, 0, flare * lado], [corpo, meio, ponta])])

def folha_em_pe(nome, raiz, d, L, W, fora, T=1.0):
    """Folha larga que cresce na direção d (crista): a face larga fica virada para 'fora'."""
    x, y, z = raiz
    torce = torcao_para(d, fora)
    Lb = L * 0.62; Lm = L * 0.20; wm = W * 0.62; s = wm / 1.4142
    m = mat_folha_larga(x, "x")
    pecas = [peca(nome + "_b", [x - W * .32, y, z - T / 2 + .02], [x + W * .32, y + L * .2, z + T / 2 - .02], m, res=3),
             peca(nome, [x - W / 2, y + L * .16, z - T / 2], [x + W / 2, y + Lb, z + T / 2], m, res=3),
             peca(nome + "_m", [x - wm / 2, y + Lb - 0.1, z - T / 2 + .02], [x + wm / 2, y + Lb + Lm, z + T / 2 - .02], m, res=3)]
    yp = y + Lb + Lm
    pecas.append(peca(nome + "_pt", [x - s / 2, yp - s / 2, z - T / 2 + .04], [x + s / 2, yp + s / 2, z + T / 2 - .04],
                      mat_folha_larga(x, "x", yp, diag=True), rot=(0, 0, 45), pivo=(x, yp, z), res=3))
    return osso(nome, list(raiz), apontar(d), [osso(nome + "_t", list(raiz), [0, torce, 0], pecas)])

def pena(nome, raiz, phi, lado, L, W, cor, flare=12, varre=10, T=0.9):
    """Pena do corpo em escama: bloco curto com ponta em V (losango), em 2 tons de marrom; pendura da raiz."""
    x, y, z = raiz
    Lb = L - W * 0.5; s = W / 1.4142
    def m(c):
        face = c["face"]
        if face in ("east", "west"):
            base = cor if (c["p"][2] - z) * lado > 0 else tom(cor, -.10)
            return base
        if face == "up": return tom(cor, .08)
        return tom(cor, -.28)
    corpo = peca(nome, [x - T / 2, y - Lb, z - W / 2], [x + T / 2, y, z + W / 2], m, res=2)
    ponta = peca(nome + "_pt", [x - T / 2 + .03, y - Lb - s / 2, z - s / 2], [x + T / 2 - .03, y - Lb + s / 2, z + s / 2], m,
                 rot=(45, 0, 0), pivo=(x, y - Lb, z), res=2)
    return osso(nome, list(raiz), [0, -phi * lado, 0], [osso(nome + "_p", list(raiz), [-varre, 0, flare * lado], [corpo, ponta])])

# ---------------- cabeça ----------------
HW = 5.4          # meia largura da cabeça
QX = 2.0          # meia largura da frente reta (onde nasce o bico)
ZF = -13.2        # frente da cabeça
ZB = -3.6         # nuca
FL = math.hypot(HW - QX, HW - QX)
ZS = ZF + (HW - QX)
FT = 2.0
CAB_Y0, CAB_Y1 = 20.6, 28.4
OLHO_Y = 25.2
OLHO_RU, OLHO_RV = 1.75, 1.2

def bloco2(a, b, x, y, z, passo=1.6):
    return a if (math.floor(y / passo) + math.floor((x + z) / passo)) % 2 == 0 else b

def cor_cabeca(p, face):
    x, y, z = p
    if face == "up": return (128, 74, 40)                       # coberto pelas folhas da crista
    if y < OLHO_Y - OLHO_RV + 0.1 and z < ZF + 6.6:
        return CREME_BOCH if y > 21.6 else CREME_BOCH_SOMBRA
    q = (math.floor((y - 20) / 1.6) * 7 + math.floor((z + x) / 1.6) * 3) % 3
    return ((139, 90, 53), (160, 104, 62), (139, 90, 53))[q]     # marrom #8B5A35 com blocos castanho-claros

def fc_centro(lado):
    mx, mz = (QX + HW) / 2, (ZF + ZS) / 2
    n = (0.7071, -0.7071)
    return (lado * (mx - n[0] * FT / 2), mz - n[1] * FT / 2)

OLHO_FENDA = (1.95, 1.15)          # meia largura × meia altura: fenda alongada para trás (~1,8 : 1)
SOMBRA_IRIS = (150, 172, 20)        # 1 tom abaixo da íris: a sombra da sobrancelha no alto do olho
PALPEBRA = (58, 36, 24)

def olho_neutro(u, v):
    """Olhar imponente (Fase 7), na face plana do olho. u: ao longo da face (negativo = para o bico), v: para cima.
    Fenda alongada para trás; a pálpebra corta o topo numa diagonal que desce para o bico (só ~55–60% da altura
    aparece); a borda de baixo é reta e sobe um pouco para trás. Íris lima forte ocupando quase tudo, sombra da
    sobrancelha no alto, pupila do lado do bico com 1 ponto de brilho, esclera só numa cunha atrás, linha escura
    de 1 px na pálpebra e nenhum contorno grosso."""
    ru, rv = OLHO_FENDA
    if (abs(u) / ru) ** 3 + (abs(v) / rv) ** 3 > 1: return None
    if v < -rv * 0.82 + 0.20 * (u / ru): return None                     # borda de baixo reta, subindo para trás
    corte = rv * (0.34 + 0.36 * (u / ru))                               # pálpebra: diagonal descendo para o bico
    if v > corte: return None
    if v > corte - 0.15: return PALPEBRA                                 # cílio/pálpebra de 1 px
    if u > ru * 0.72: return ESCLERA                                     # cunha de esclera atrás
    pu, pv = -0.95, -0.08
    dp = math.hypot(u - pu, v - pv)
    if math.hypot(u - (pu + 0.14), v - (pv + 0.22)) < 0.12: return (255, 255, 245)   # brilho no alto da pupila
    if dp < 0.44: return PUPILA
    if v > corte - 0.50: return SOMBRA_IRIS                              # sombra da sobrancelha no alto da íris
    if dp < 0.70 and v < pv - 0.12: return IRIS_ANEL                     # crescente verde sob a pupila
    return IRIS_VIVA

def mat_faceta(lado):
    base = mat_bloco(cor_cabeca, borda=-.06, faixas=False)
    fora = "east" if lado > 0 else "west"
    cx, cz = fc_centro(lado)
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            cor = olho_neutro(z - cz + 0.1, y - OLHO_Y)
            if cor is not None: return cor
            if y < OLHO_Y - OLHO_RV + 0.1: return CREME_BOCH
            return (160, 104, 62)
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face in ("east", "west") and ZF - 1.5 < z < ZF - 0.8 and 25.3 < y < 25.9: return (30, 20, 8)   # narina: no alto da lateral, perto da base (como na ficha)
    if face == "down": return BICO_SOMBRA
    if face == "up": return mix(BICO_OURO, (255, 232, 120), .3)
    if face == "north": return BICO_OURO if y > 23.4 else BICO_SOMBRA
    return mix(BICO_OURO, BICO_SOMBRA, clamp((24.6 - y) / 2.0))

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
    # bochechas: blocos creme SALIENTES em degrau, que avançam à frente da cara e passam da largura da cabeça
    mbo = mat_tons((255, 238, 206), (250, 222, 180), (214, 180, 136), lado=(242, 206, 160), borda=-.05)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((2.4 * lado, (HW + 0.4) * lado))
        cab.append(peca("bochecha_" + s, [x0, 21.7, ZF + 0.9], [x1, 23.5, ZF + 3.8], mbo, res=4))
        x0, x1 = sorted((1.6 * lado, (HW + 0.3) * lado))
        cab.append(peca("bochecha_baixo_" + s, [x0, 20.0, ZF + 0.4], [x1, 21.6, ZF + 5.0], mbo, res=4))
    # sobrancelhas: lajes grossas em V até encostar no topo do bico, e a barra que corre pelo alto da cabeça até a nuca
    msob = mat_tons(SOBR_CLARA, SOBR, (52, 36, 32), lado=mix(SOBR, SOBR_CLARA, .25))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = fc_centro(lado)
        ox = cx + lado * (FT / 2)
        x0, x1 = sorted((ox - 1.3 * lado, ox + 0.65 * lado))   # saliente: avança sobre o olho
        cab.append(osso("sobrancelha_" + s, [cx, 27.0, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s, [x0, 25.85, cz - FL / 2 - 0.7], [x1, 27.45, cz + FL / 2 + 0.3], msob,
                 rot=(-20, 0, 0), pivo=(cx, 26.6, cz), res=4)]))
        x0, x1 = sorted(((HW - 1.1) * lado, (HW + 0.15) * lado))
        cab.append(peca("sobrancelha_lado_" + s, [x0, 27.0, ZS - 0.3], [x1, 28.3, ZB - 1.0], msob, res=4))
    # bico de rapina: base 3,4 × 3, projeta 4 para a frente; os 2 da ponta são o gancho, que desce; mandíbula de
    # baixo menor e recuada, com a linha escura da boca
    mb0 = mat_bloco(cor_bico, borda=0, faixas=False)       # sem contorno: o bico lê como uma massa só
    mb1 = mat_bloco(cor_bico, borda=0, faixas=False)
    mb = lambda c: (mb1 if c["face"] == "north" else mb0)(c)
    # de frente lê como triângulo: o alto largo (3,4) entre as sobrancelhas, a parte de baixo mais estreita e o gancho
    cab.append(peca("bico_base", [-1.7, 25.0, ZF - 2.6], [1.7, 26.3, ZF + 0.3], mb, res=4))
    cab.append(peca("bico_base2", [-1.2, 23.4, ZF - 2.2], [1.2, 25.1, ZF + 0.3], mb, res=4))
    cab.append(peca("bico_gancho", [-0.7, 22.4, ZF - 3.9], [0.7, 26.0, ZF - 2.4], mb, res=4))
    q = 1.7   # losango (quadrado girado 45° no plano da frente): fecha o triângulo numa ponta embaixo, no meio
    cab.append(peca("bico_ponta", [-q / 2, 23.6 - q / 2, ZF - 3.7], [q / 2, 23.6 + q / 2, ZF - 1.6], mb, rot=(0, 0, 45),
                    pivo=(0, 23.6, ZF - 2.6), res=4))
    def mat_baixo(c):
        x, y, z = c["p"]
        if c["face"] in ("east", "west") and y > 23.0: return BOCA
        return tom(BICO_SOMBRA, {"up": .1, "down": -.3}.get(c["face"], 0))
    cab.append(peca("bico_baixo", [-0.9, 22.4, ZF - 2.4], [0.9, 23.4, ZF + 0.2], mat_baixo, res=4))
    # barbela: dois lobos curtos que nascem juntos sob o bico e abrem em V invertido, ponta arredondada
    def mat_bar(c):
        x, y, z = c["p"]; face = c["face"]
        if face in ("east", "west") and abs(x) < 0.7: return BARBELA_SOMBRA      # face interna
        if face == "down": return BARBELA_SOMBRA
        return tom(BARBELA, .06 if face == "up" else (-.06 if face in ("east", "west") else 0))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.05 * lado, 2.05 * lado))
        x2, x3 = sorted((0.25 * lado, 1.55 * lado))
        cab.append(osso("barbela_" + s, [0.0, 22.6, ZF - 0.8], [0, 0, 12 * lado], [
            peca("barbela_" + s, [x0, 19.8, ZF - 1.8], [x1, 22.6, ZF + 0.2], mat_bar, res=4),
            peca("barbela_ponta_" + s, [x2, 19.0, ZF - 1.6], [x3, 20.0, ZF], mat_bar, res=4)]))
    # crista: folhas largas lima iguais às da capa, nascendo na linha da sobrancelha e varrendo ~35° para trás;
    # de frente: central alta, ±20°, ±40° e uma pequena junto de cada sobrancelha; atrás, folhas até a nuca
    crista = []
    yt = CAB_Y1 - 0.8
    CF = [(0, 14, 11.0, 3.6, 0.0, ZF + 3.0, 0.0), (-20, 22, 8.6, 3.4, 0.6, ZF + 3.4, 1.0), (20, 22, 8.6, 3.4, 0.6, ZF + 3.4, 1.0),
          (-40, 30, 6.4, 3.0, 1.0, ZF + 3.8, 2.0), (40, 30, 6.4, 3.0, 1.0, ZF + 3.8, 2.0),
          (-62, 30, 4.4, 2.6, 1.0, ZF + 2.6, 3.4), (62, 30, 4.4, 2.6, 1.0, ZF + 2.6, 3.4)]
    for k, (ang, tras, L, W, vira, z0, x0) in enumerate(CF):
        a, t = math.radians(ang), math.radians(tras)
        d = [math.sin(a) * math.cos(t), math.cos(a) * math.cos(t), math.sin(t)]
        crista.append(folha_em_pe(f"crista{k}", (math.copysign(x0, ang) if ang else 0, yt, z0), d, L, W * 1.2,
                                  fora=[math.copysign(vira, ang) if ang else 0, 0.35, -1]))
    for k, (ang, tras, L, W, z0, fora_x) in enumerate(((-10, 36, 10.4, 3.6, ZF + 5.4, -1), (10, 36, 10.4, 3.6, ZF + 5.4, 1),
                                                       (0, 54, 9.8, 3.6, ZF + 7.6, 1), (-14, 70, 8.0, 3.4, ZB - 1.4, -1),
                                                       (14, 70, 8.0, 3.4, ZB - 1.4, 1))):
        a, t = math.radians(ang), math.radians(tras)
        d = [math.sin(a), math.cos(t), math.sin(t)]
        crista.append(folha_em_pe(f"crista_tras{k}", (1.8 * math.sin(a), yt, z0), d, L, W * 1.2, fora=[fora_x, 0.25, 0]))
    # duas folhas deitadas sobre o alto da cabeça (o topo marrom não aparece)
    for k, lado in enumerate((-1, 1)):
        crista.append(folha_em_pe(f"crista_topo{k}", (1.6 * lado, yt - 0.2, ZF + 4.6), [0.62 * lado, 0.42, 0.66], 7.4, 4.0,
                                  fora=[0.5 * lado, 1, 0]))
    cab.append(osso("crista", [0, CAB_Y1, ZF + 5.0], [0, 0, 0], crista))
    return cab

# ---------------- corpo ----------------
def meia_peito(y):
    """Meia largura do peito creme: largo sob a barbela (de gola a gola), afinando em degraus até a barriga."""
    return 1.2 + 4.6 * clamp((y - 9.2) / 11.6)

def cor_corpo(p, face):
    x, y, z = p
    if z < -9.6 and abs(x) < meia_peito(y) + 0.4 and y > 9.0:
        return CREME if abs(x) < meia_peito(y) else BEGE
    return PENA_1 if y > 11 and z < 0 else PENA_2

def cor_peito(p, face):
    """'Flor Peitoral': cada camada em degrau tem a borda de baixo em pontas (serrilhada) mais escura."""
    x, y, z = p
    if face == "north":
        if meia_peito(y + 1.0) - abs(x) < 0: return BEGE
        y0 = 9.2 + 2.0 * math.floor((y - 9.2) / 2.0)
        dente = 0.55 * (1 - abs(((x / 1.4) % 1.0) - 0.5) * 2)
        if y - y0 < dente: return CREME_2
        return CREME
    return CREME_2

def montar():
    cab = montar_cabeca()
    cabeca = osso("cabeca", [0, 22.0, -8.0], [0, 0, 0], cab)
    mp = mat_bloco(lambda p, f: CREME if p[2] < -9.5 else PENA_1, borda=-.06, faixas=False)
    pescoco = osso("pescoco", [0, 21.0, -7.0], [0, 0, 0], [
        peca("pescoco", [-4.6, 18.6, -12.4], [4.6, 21.2, -4.0], mp, res=2),
        cabeca])

    corpo = []
    # tronco OVAL: miolo bem arredondado (cantos cortados em 2 degraus) + dorso
    mt = mat_bloco(cor_corpo, borda=-.03, faixas=False)
    corpo += g.arredondado2("tronco", [-7.4, 6.4, -11.4], [7.4, 22.6, 8.6], mt, r=4.4)
    corpo += g.arredondado2("dorso", [-6.4, 11.0, -6.6], [6.4, 25.4, 9.8], mt, r=3.6)
    # 'Flor Peitoral': camadas em degrau, cada uma 1 à frente da de baixo, de gola a gola no alto
    mpe = mat_bloco(cor_peito, borda=-.06, faixas=False)
    PEITO = [(19.0, 21.4, 5.8, -13.6), (17.0, 19.2, 5.2, -13.0), (15.0, 17.2, 4.4, -12.6), (13.0, 15.2, 3.5, -12.2),
             (11.0, 13.2, 2.6, -11.9), (9.2, 11.2, 1.7, -11.6)]
    for k, (y0, y1, w, zf) in enumerate(PEITO):
        corpo.append(peca(f"peito{k}", [-w, y0, zf], [w, y1, -10.6], mpe, res=4))

    # penas do corpo em escama (pontas em V sobrepostas): 2 anéis no flanco e a franja de baixo, de comprimentos
    # alternados, até as coxas
    ANEIS = [(14.2, 7.6, 9.4, -1.0, [-58, -32, -6, 20, 46, 72], 4.6, 3.8, (PENA_1, PENA_3)),
             (10.4, 7.8, 9.6, -1.0, [-70, -46, -22, 2, 26, 50, 74], 5.0, 3.8, (PENA_2, PENA_1))]
    for a, (y0, ax, az, zc, phis, L, W, cores) in enumerate(ANEIS):
        for lado in (-1, 1):
            s = "d" if lado < 0 else "e"
            for k, phi in enumerate(phis):
                r = math.radians(phi)
                x, z = lado * ax * math.cos(r), zc + az * math.sin(r)
                corpo.append(pena(f"pena{a}{k}_{s}", (x, y0 - 0.3 * (k % 2), z), phi, lado, L * (1.0 if k % 2 else 0.8), W,
                                  cores[k % 2], flare=10 + 4 * a, varre=8))
    # franja de trás, no meio (entre as duas metades)
    for k, (y, L) in enumerate(((12.6, 4.6), (9.4, 5.0))):
        corpo.append(pena(f"pena_costas{k}", (0, y, 9.6), 90, 1, L, 3.6, PENA_1 if k else PENA_3, flare=14, varre=0))

    # ---------- espinhos: ouriço radial (~28 cones em 3 anéis concêntricos em volta do eixo das costas) ----------
    C0 = (0.0, 19.4, 4.0)
    eixo = norm([0.0, 0.22, 1.0])
    # base ortonormal em volta do eixo
    e1 = norm([1.0, 0.0, 0.0]); e2 = norm([eixo[1] * e1[2] - eixo[2] * e1[1], eixo[2] * e1[0] - eixo[0] * e1[2], eixo[0] * e1[1] - eixo[1] * e1[0]])
    R0 = (6.4, 7.4, 6.4)                 # elipsoide das raízes (dentro do dorso: sobra marrom entre as bases)
    C1, R1 = (0.0, 19.8, 5.0), (12.6, 15.8, 19.6)
    ANEL = [(0, 1, 0), (24, 6, 0), (46, 11, 16), (68, 14, 6), (92, 12, 13)]   # (abertura em graus, quantidade, giro inicial)
    esp_corpo, cauda = [], []
    n = 0
    for anel, (ab, qtd, giro0) in enumerate(ANEL):
        for k in range(qtd):
            fi = math.radians(giro0 + 360 * k / qtd)
            a = math.radians(ab)
            dvec = [math.cos(a) * eixo[i] + math.sin(a) * (math.cos(fi) * e2[i] + math.sin(fi) * e1[i]) for i in range(3)]
            sx, sy, sz = dvec
            if sz < 0.05: continue                                 # nada para a frente
            if sy < -0.55 and sz < 0.5: continue                   # nem para dentro das pernas
            if sy < -0.80: continue
            if abs(sx) > 0.62 and sy > 0.0: continue               # sem "orelhas"/halo atrás da cabeça e dos ombros, de frente
            if ab > 80 and sy < 0.55: continue                     # o anel de fora só aparece em cima (de frente não faz halo)
            raiz = (C0[0] + R0[0] * sx, C0[1] + R0[1] * sy, C0[2] + R0[2] * sz)
            ry = R1[1] if sy > 0 else 13.6
            ponta = (C1[0] + R1[0] * sx * (1 - 0.35 * max(sy, 0)), C1[1] + ry * sy, C1[2] + R1[2] * sz)
            L = math.sqrt(sum((ponta[i] - raiz[i]) ** 2 for i in range(3)))
            L = clamp(L * 0.92, 7.5, 13.6)       # arte: cone visível ~0,23 da altura
            W = 4.8 if L > 10 else 4.2           # arte: base ~0,075 da altura
            curva = -6.0 if sy < 0.6 else 6.0                      # curva leve para cima (os de cima, para trás)
            q = espinho(f"espinho{n}", raiz, dvec, L, W, curva=curva, torce=(k * 23 + anel * 11) % 90)
            (cauda if sz > 0.6 and sy < 0.2 else esp_corpo).append(q)
            n += 1
    corpo.append(osso("espinhos", list(C0), [0, 0, 0], esp_corpo))
    corpo.append(osso("cauda", [0, 15.0, 8.0], [0, 0, 0], cauda))

    # ---------- capa de folhas largas dos ombros (asas): 6 folhas por lado em leque, coladas ao corpo ----------
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = []
        # (x, y, z da raiz, phi em volta do corpo, flare, varre, L, W)
        CAPA = [(4.8, 21.6, -11.0, -62, 10, 6, 13.0, 4.4),    # da frente: borda interna encosta no peito creme
                (5.8, 21.8, -9.8, -36, 22, 16, 13.4, 4.6),
                (6.6, 22.4, -8.2, -12, 24, 32, 12.6, 4.6),
                (6.8, 23.0, -6.4, 8, 18, 50, 11.4, 4.4),
                (6.4, 23.6, -4.6, 24, 16, 66, 10.6, 4.2),
                (5.6, 24.2, -3.0, 40, 14, 80, 9.6, 4.0),      # a de cima: quase horizontal para trás
                (7.2, 21.0, -6.0, 2, 30, 24, 11.0, 4.6)]      # 2ª camada por fora (a capa da arte tem folhas sobrepostas)
        for k, (x0, y0, z0, phi, fl, va, L, W) in enumerate(CAPA):
            # arte: a capa vai da altura da barbela (~22) até ~8 e as folhas têm ~0,25 da altura (não 0,33)
            asa.append(folha_capa(f"asa{k}_{s}", (x0 * lado, y0 - 1.8, z0), phi, lado, L * 0.82, W * 1.2, flare=fl, varre=va, T=1.0))
        corpo.append(osso("asa_" + s, [6.0 * lado, 22.0, -7.0], [0, 0, 0], asa))

    corpo.append(pescoco)
    tronco = osso("corpo", [0, 9.0, 0.0], [0, 0, 0], corpo)

    # ---------- pernas: coxa de penas marrons, canela laranja-castanho, dedos grossos e garras grandes ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 4.1 * lado; zc = 0.0
        pp = []
        mcx = mat_tons(PENA_3, PENA_1, PENA_2, lado=mix(PENA_1, PENA_2, .3))
        pp += g.octogono("coxa_" + s, [xc - 2.5, 4.6, zc - 2.5], [xc + 2.5, 9.0, zc + 2.5], mcx, r=0.8)
        mca = mat_tons(CANELA_LUZ, CANELA_PERNA, mix(CANELA_PERNA, PENA_2, .5), lado=mix(CANELA_PERNA, PENA_2, .25))
        pp += g.octogono("canela_" + s, [xc - 2.0, 1.0, zc - 2.0], [xc + 2.0, 5.0, zc + 2.0], mca, r=0.5)
        mg = mat_tons(mix(GARRA_ESCURA, (140, 130, 134), .3), GARRA_ESCURA, (40, 36, 40), lado=mix(GARRA_ESCURA, (40, 36, 40), .3))
        pp.append(peca("pe_" + s, [xc - 2.4, 0.0, zc - 2.4], [xc + 2.4, 1.7, zc + 1.8], mca))
        for nome, giro, dx in (("meio", 0, 0), ("fora", -20 * lado, 2.3 * lado), ("dentro", 20 * lado, -2.3 * lado)):
            x0, z0 = xc + dx, zc - 2.2
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - .9, 0, z0 - 2.2], [x0 + .9, 1.9, z0 + 0.3], mca),
                peca(f"garra_{nome}_{s}", [x0 - .9, 0.0, z0 - 3.3], [x0 + .9, 2.3, z0 - 2.0], mg),
                peca(f"garra_ponta_{nome}_{s}", [x0 - .65, 0.0, z0 - 4.2], [x0 + .65, 1.3, z0 - 3.2], mg)]))
        pp.append(peca("dedo_tras_" + s, [xc - .9, 0, zc + 1.6], [xc + .9, 1.6, zc + 2.8], mca))
        pp.append(peca("garra_tras_" + s, [xc - .8, 0, zc + 2.7], [xc + .8, 1.8, zc + 3.9], mg))
        return osso("perna_" + s, [xc, 9.0, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
