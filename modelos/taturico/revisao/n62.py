"""Taturico (#007, Terra): o galo-tatu das rochas, robusto e defensivo, coberto por uma carapaça de faixas.

Refação (a versão anterior foi rejeitada como "estranha"). Medidas tiradas das 4 vistas da ficha (altura 39,2 u):
pés 0..3, pernas até 9, corpo 8,5..32 (z -14 no peito), cabeça 20..33,5 (z -18..-3), crista até 39,2.

Regra do dono: geometria antes de textura. Nada de placa grande, lisa e chapada nem de cubinho solto: volumes em
degrau, inclinados e encaixados, que já leem como a ficha sem textura. Cores = paleta da ficha (amostrada com PIL),
2 tons por bloco, quadrados grandes (nada mais escuro que #572d27).

Como cada elemento da ficha foi resolvido:
- CARAPAÇA: 5 cintas em caixa (perfil de 4 degraus, sem giro: a textura não estica) da nuca à garupa, cada uma mais
  baixa que a da frente (o dorso é mais alto logo atrás da cabeça); cada cinta tem uma ABA na beirada de trás, um
  pouco maior, que se sobrepõe à cinta seguinte como telha (degrau visível no contorno). Xadrez grande de marrom-malva
  #8f4f3f e laranja-tan #ed9f5e; de trás, os arcos empilhados da traseira da ficha (marrom em cima, laranja embaixo).
- CAUDA BLINDADA: cone telescópico de 5 anéis sólidos e arredondados, cada um menor e encaixado no anterior,
  inclinado 30° para baixo, terminando em ponta (ossos cauda_anel_k, ondulam).
- ELMO ROCHOSO: aba em V que avança sobre os olhos e corta o alto deles, uma segunda fileira em V atrás e acima,
  o topo e a nuca em degrau, e as têmporas descendo até a altura do olho; xadrez marrom-malva/laranja.
- ROSTO (expressão neutra): creme #fcdfbe; olho em meia-lua cortado pela aba (linha da pálpebra #5a2f29 colada
  nela, mais baixa do lado do bico), íris âmbar #fca702 ocupando quase tudo, pupila preta, brilho pequeno e só uma
  cunha de esclera atrás; bico de rapina em trapézio que afina para baixo (fatias empilhadas), gancho na ponta e
  narina preta; barbelas em 2 lóbulos largos em cima que afinam, abrindo pouco, + lóbulo do meio sob o bico;
  placas da bochecha grossas, giradas 35° para fora, e a placa com fenda na têmpora, logo atrás do olho.
- ASAS: 3 placas empilhadas recuando para baixo (a de cima, o ombro, mais larga e chanfrada) e a placa do ombro
  chanfrada com o emblema: borda marrom, anel tan, fundo marrom e o toco tan no meio.
- PEITO: creme quente em fileiras de escamas + franja de penas-bloco até logo acima das coxas.
- PATAS FORTES: pernas #fca702 (sombra #e08a00 só embaixo), 3 dedos amarelos e garras #7f5e67 grandes, mais altas
  que o dedo; garra de trás também grande.
"""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, clamp, na_borda

ID = "taturico"; NOME = "Taturico"; NUMERO = 7
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 24.6, -16.6), 7.4)
ONDAS = [("cauda_anel", 5, (1.2, 2.5, 0))]
ANIM_PARADO = {"barbela": [(0, 0, 0), (5, 0, 2), (0, 0, 0), (4, 0, -2), (0, 0, 0)]}
ANIM_ANDANDO = {"barbela": [(0, 0, 0), (9, 0, 4), (0, 0, 0), (9, 0, -4), (0, 0, 0)]}

# ---------------- paleta (quadro "Paleta de Cores" da ficha, amostrado com PIL) ----------------
CREME = (252, 223, 190); CREME_SOM = (246, 198, 156)        # #fcdfbe e sombra pêssego
LARANJA = (237, 159, 94); LARANJA_SOM = (205, 116, 62)      # #ed9f5e / #cd743e
MALVA = (143, 79, 63); MALVA_ESC = (106, 58, 48)            # #8f4f3f / entre #8f4f3f e #5a2f29
PALPEBRA = (90, 47, 41)                                     # #5a2f29
PISO = (87, 45, 39)                                         # #572d27: nada fica mais escuro
VERM = (207, 37, 35); VERM_CL = (240, 76, 66); VERM_ESC = (160, 22, 24)   # #cf2523
AMARELO = (252, 167, 2); AMARELO_CL = (252, 190, 30); AMARELO_SOM = (224, 138, 0)   # #fca702 / #e08a00
LARANJA_BICO = (236, 128, 8)
CINZA = (127, 94, 103); CINZA_CL = (154, 122, 130)          # #7f5e67 / topo #9a7a82
PRETO = (20, 10, 8)

def tom(c, f):
    """Luz quente: f > 0 clareia para um creme quente, f < 0 escurece para um marrom-avermelhado."""
    f = clamp(f, -1, 1)
    if f >= 0: return mix(c, (255, 240, 214), f * 0.35)
    return mix(c, (int(c[0] * .45), int(c[1] * .32), int(c[2] * .26)), -f)

def piso(c):
    """Nada da carapaça fica mais escuro que #572d27 (a ficha não tem pixels quase pretos)."""
    return c if sum(c) >= sum(PISO) else PISO

def lado_s(lado): return "d" if lado < 0 else "e"

# ---------------- luz chapada por face ----------------
def luz_face(c, curva=0.1, borda=0.12, cima=0.1, baixo=0.25, frente=0.0):
    """Tons por bloco: face de cima clara, lados na cor base, de baixo em sombra; fio escuro leve na borda."""
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

# faixas da vista de TRÁS, lidas na traseira da ficha (altura em unidades, de cima para baixo): cada arco empilhado
# é marrom em cima e laranja embaixo, com o vão marrom-escuro entre eles
FAIXAS_TRAS = [(30.0, 99, "C"), (28.5, 30.0, "E"), (27.1, 28.5, "M"), (24.6, 27.1, "C"), (21.4, 24.6, "E"),
               (19.4, 21.4, "M"), (16.0, 19.4, "C"), (12.8, 16.0, "E"), (10.9, 12.8, "C"), (9.6, 10.9, "E"),
               (8.2, 9.6, "M"), (6.3, 8.2, "C"), (-99, 6.3, "E")]

def cor_traseira(y):
    for y0, y1, k in FAIXAS_TRAS:
        if y0 <= y < y1: return {"C": LARANJA, "M": MALVA, "E": MALVA_ESC}[k]
    return MALVA

# ---------------- cintas da carapaça (caixas em degrau, sem giro) ----------------
PERFIL_CORPO = [(1.0, 0.07, 0.58), (0.88, 0.02, 0.8), (0.7, 0.0, 0.93), (0.46, 0.0, 1.0)]   # (largura, de, até)

def mat_cinta(k, limites, zc, baixo_escuro=False):
    """Bloco de cinta: células grandes chapadas. Na vertical, as faixas entre os degraus do perfil ('limites');
    na horizontal, a metade da frente e a de trás da cinta (corte em zc): xadrez de marrom-malva e laranja-tan.
    Atrás: as faixas da traseira da ficha. Embaixo: marrom-escuro."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        if face == "south":
            cor = cor_traseira(y); luz = -0.06 if na_borda(c) else 0.0
        elif face == "down":
            cor = MALVA_ESC; luz = -0.05
        else:
            idx = sum(1 for L in limites if y < L - 1e-6)
            meia = 1 if z >= zc else 0
            cor = LARANJA if (idx + meia + k) % 2 == 0 else MALVA
            if baixo_escuro and idx >= len(limites) - 1: cor = LARANJA_SOM if cor is LARANJA else MALVA_ESC
            luz = luz_face(c, curva=0.08, borda=0.1, cima=0.08)
        return piso(tom(cor, luz))
    return f

def limites_perfil(perfil, yb, yt, cel=4.2):
    """Alturas onde a cor troca: nos degraus do perfil (menos o do topo, fino) e, abaixo do último, a cada ~cel."""
    h = yt - yb
    tops = sorted({yb + fb * h for _, _, fb in perfil}, reverse=True)[1:]
    lim = tops[:]
    baixo = tops[-1] if tops else yt
    n = max(1, round((baixo - yb) / cel))
    lim += [baixo - (baixo - yb) / n * i for i in range(1, n)]
    return lim

def cinta(nome, k, z0, z1, W, yb, yt, aba=0.0, sobra=0.4):
    """Cinta em degrau + ABA na beirada de trás (comprimento 'aba', 'sobra' maior em largura e altura), que se
    sobrepõe à cinta seguinte como telha. Cada caixa sai um pouco mais para a frente/trás (sem z-fighting)."""
    h = yt - yb
    lim = limites_perfil(PERFIL_CORPO, yb, yt)
    m = mat_cinta(k, lim, (z0 + z1) / 2)
    out = []
    for i, (fw, fa, fb) in enumerate(PERFIL_CORPO):
        e = 0.04 * i
        out.append(peca(f"{nome}_{i}", [-W * fw, yb + fa * h, z0 - e], [W * fw, yb + fb * h, z1 - aba + e], m,
                        faixa=(yb, yt), res=2))
    if aba <= 0: return out          # sem aba: as cintas leem como rolos grossos (como na arte conceitual)
    Wa, ya = W + sobra, yt + sobra * 0.8
    ha = ya - yb
    ma = mat_cinta(k, limites_perfil(PERFIL_CORPO, yb, ya), z1 - 99)       # mesma cor da metade de trás da cinta
    for i, (fw, fa, fb) in enumerate(PERFIL_CORPO):
        e = 0.04 * i
        out.append(peca(f"{nome}_aba{i}", [-Wa * fw, yb + fa * ha, z1 - aba - 0.02 - e], [Wa * fw, yb + fb * ha, z1 + e], ma,
                        faixa=(yb, ya), res=2))
    return out

# ---------------- cauda (anéis sólidos arredondados) ----------------
def mat_anel_cauda(k, W, H, yc):
    """Anel da cauda: por fora, xadrez de quadrados grandes (setores de 60° x metade do comprimento), metade de cima
    mais marrom e a de baixo mais tan; na frente e atrás, beirada marrom e miolo tan."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        (bx0, by0, bz0), (bx1, by1, bz1) = c["b"]
        luz = -0.06 if na_borda(c) else 0.0
        if face in ("south", "north"):
            cor = MALVA if math.hypot(x / W, (y - yc) / H) > 0.6 else LARANJA
        else:
            setor = int(math.floor((math.degrees(math.atan2(abs(x), y - yc)) + 30) / 60))
            hz = 1 if (z - bz0) / max(bz1 - bz0, 1e-6) >= 0.5 else 0
            cor = LARANJA if (setor + hz + k) % 2 == 0 else MALVA
            if face == "up": luz += 0.08
            if face == "down": luz -= 0.08
        return piso(tom(cor, luz))
    return f

def anel_cauda(nome, k, z0, z1, W, H, yc):
    m = mat_anel_cauda(k, W, H, yc)
    return [peca(f"{nome}_{i}", [-W * fw, yc - H * fh, z0 - 0.04 * i], [W * fw, yc + H * fh, z1 + 0.04 * i], m,
                 faixa=(yc - H, yc + H), res=2)
            for i, (fw, fh) in enumerate([(1.0, 0.66), (0.7, 1.0)])]

# ---------------- glifos (traço grosso, ângulos retos, como na ficha) ----------------
EMBLEMA_OMBRO = ["#######",    # anel tan; dentro, fundo marrom e o toco tan subindo do meio de baixo
                 "#.....#",
                 "#.....#",
                 "#..#..#",
                 "#..#..#",
                 "#######"]
MEANDRO_CAB = ["#####",        # placa da bochecha: meandro de ângulos retos
               "....#",
               "###.#",
               "#.#.#",
               "#...#",
               "#####"]
FENDA_CAB = ["#######",        # placa da têmpora: moldura com fenda escura no meio
             "#.....#",
             "#.....#",
             "#######"]

def glifo(c, bitmap, margem=0.13, espelha=False):
    u = (c["i"] + .5) / c["tw"]; v = (c["j"] + .5) / c["th"]
    if espelha: u = 1 - u
    a = (u - margem) / (1 - 2 * margem); b = (v - margem) / (1 - 2 * margem)
    if not (0 <= a < 1 and 0 <= b < 1): return "fundo"
    return "traco" if bitmap[int(b * len(bitmap))][int(a * len(bitmap[0]))] == "#" else "fundo"

def mat_placa_glifo(glifos, espelha=False, margem=0.14):
    """Placa marrom-malva grossa; 'glifos' = {face: bitmap} desenhados em laranja-tan."""
    def f(c):
        bm = glifos.get(c["face"])
        if bm:
            r = glifo(c, bm, margem=margem, espelha=espelha)
            base = LARANJA if r == "traco" else MALVA
            luz = -0.14 if na_borda(c) else 0.02
            return piso(tom(base, luz))
        return piso(tom(MALVA, luz_face(c, borda=.12)))
    return f

def mat_xadrez(cel, k=0, eixo=0, so_malva=False):
    """Xadrez de quadrados grandes ('cel' unidades) ao longo do eixo dado e da altura: marrom-malva e laranja-tan."""
    def f(c):
        p = c["p"]
        a = int(math.floor(abs(p[eixo]) / cel)); b = int(math.floor(p[1] / cel))
        cor = LARANJA if (a + b + k) % 2 == 0 else MALVA
        if so_malva and (a + k) % 3 != 1: cor = MALVA
        return piso(tom(cor, luz_face(c, curva=0.08, borda=0.12, cima=0.08)))
    return f

# ---------------- cabeça ----------------
OLHO_Y = 25.4
FAC_T = 1.6
FAC_A, FAC_B = (2.7, -16.3), (6.6, -12.4)          # a faceta do olho vai de A (junto do bico) a B (lado da cabeça)
FAC_S = ((FAC_A[0] + FAC_B[0]) / 2, (FAC_A[1] + FAC_B[1]) / 2)
FAC_C = (FAC_S[0] - 0.7071 * FAC_T / 2, FAC_S[1] + 0.7071 * FAC_T / 2)
FAC_L = math.hypot(FAC_B[0] - FAC_A[0], FAC_B[1] - FAC_A[1]) + 0.3
ABA_Y, ABA_ANG = 24.4, 22                           # beirada de baixo da aba no meio e inclinação do V (sobrancelha brava)
K_CAB, K_CAB_C = 1.07, (0.0, 22.0, -13.0)            # escala da cabeça inteira (ajuste fino)

def corte_aba(u):
    """Altura (relativa ao centro do olho) da beirada de baixo da aba em cima do olho, no ponto u da faceta."""
    x = FAC_S[0] + 0.7071 * u
    return ABA_Y + x * math.tan(math.radians(ABA_ANG)) - OLHO_Y

OLHO_RU, OLHO_RV, OLHO_DU = 2.1, 1.4, -0.3          # fenda alongada (~1,5 : 1), puxada para o bico

def olho(u, v):
    """Olhar imponente (Fase 7): fenda alongada para trás, cortada no alto pela aba do elmo numa diagonal que desce
    até o bico (só ~60% da altura aparece), borda de baixo quase reta subindo para trás; íris dourada forte quase do
    tamanho do olho, com sombra da aba no alto, pupila preta encostada no lado do bico e 1 px de brilho; esclera só
    numa cunha atrás; linha escura de 1 px só no alto (pálpebra). u < 0 = para o bico."""
    u = u - OLHO_DU
    e = (u / OLHO_RU) ** 2 + (v / OLHO_RV) ** 2
    if e > 1: return None
    vc = corte_aba(u + OLHO_DU)
    if v > vc: return None
    if v < -0.9 * OLHO_RV + 0.12 * u: return None                 # borda de baixo reta, subindo para trás
    if vc - v < 0.2: return PALPEBRA
    nu, nv = u / OLHO_RU, v / OLHO_RV
    if nu > 0.62: return mix((250, 232, 200), (236, 208, 168), clamp(-nv))   # cunha de esclera atrás
    pu, pv = nu + 0.42, nv + 0.05                                 # pupila no lado do bico
    if ((pu - 0.1) / 0.1) ** 2 + ((nv - vc / OLHO_RV + 0.32) / 0.14) ** 2 <= 1: return (255, 255, 255)
    if (pu / 0.2) ** 2 + (pv / 0.5) ** 2 <= 1: return PRETO
    iris = mix(AMARELO_CL, (226, 128, 6), clamp((0.3 - nv) / 1.3))
    if vc - v < 0.55: iris = tom(iris, -0.25)                     # sombra da aba no alto da íris
    return iris

def mat_faceta(lado):
    """Faceta a 45°: creme com o olho inteiro na face de fora."""
    fora = "east" if lado > 0 else "west"
    base = mat_liso(CREME, borda=.04, curva=.06)
    def f(c):
        if c["face"] == fora:
            x, y, z = c["p"]
            o = olho(z - FAC_C[1], y - OLHO_Y)
            if o is not None: return o
        return base(c)
    return f

def mat_bico():
    def cor(p, face):
        x, y, z = p
        if face in ("east", "west") and -18.1 < z < -17.5 and 25.1 < y < 25.7: return PRETO        # narina
        if face == "down": return LARANJA_BICO
        if face == "up": return AMARELO_CL
        return AMARELO
    return mat_chapado(cor, borda=.06, curva=.06)

def cabeca_pecas():
    cab = []
    fx = (20.0, 30.0)
    mcreme = mat_liso(CREME, borda=.05, curva=.08)
    cab.append(peca("cranio", [-7.4, 20.6, -12.2], [7.4, 29.0, -4.0], mcreme, faixa=fx, res=2))
    cab.append(peca("rosto_frente", [-2.9, 20.4, -16.2], [2.9, 26.4, -12.6], mcreme, faixa=fx, res=4))
    for lado in (-1, 1):
        s = lado_s(lado)
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 20.6, cz - FAC_L / 2], [cx + FAC_T / 2, 27.6, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, OLHO_Y, cz), faixa=fx, res=8))
    # bico de rapina: fatias empilhadas que afinam para baixo (trapézio de frente) + gancho na ponta
    mb = mat_bico()
    fb = (21.6, 26.0)
    for k, (w, y0, y1, zf) in enumerate([(2.1, 24.6, 25.9, -20.6), (1.6, 23.4, 24.7, -21.2), (1.1, 22.3, 23.5, -20.8)]):
        cab.append(peca(f"bico{k}", [-w, y0, zf], [w, y1, -15.8], mb, faixa=fb, res=4))
    cab.append(peca("bico_gancho", [-0.75, 21.6, -22.0], [0.75, 23.6, -20.7], mb, faixa=fb, res=4))
    # barbelas: 2 lóbulos largos em cima que afinam embaixo, abrindo pouco, + o lóbulo do meio sob o bico
    mv_ = mat_chapado(lambda p, f: mix(VERM_CL, VERM, clamp((22.4 - p[1]) / 3.0)), borda=.08, curva=.15)
    tiras = [peca("barbela_meio", [-0.9, 20.6, -18.4], [0.9, 22.4, -16.8], mv_, faixa=(17, 22.4), res=4)]
    for lado in (-1, 1):
        s = lado_s(lado)
        xa0, xa1 = sorted((0.3 * lado, 2.9 * lado)); xb0, xb1 = sorted((0.6 * lado, 2.4 * lado))
        tiras.append(osso("barbela_" + s, [0.6 * lado, 22.2, -17.2], [0, 0, 8 * lado], [
            peca("barbela_" + s, [xa0, 19.6, -18.6], [xa1, 22.2, -16.0], mv_, faixa=(17, 22.4), res=4),
            peca("barbela_ponta_" + s, [xb0, 17.0, -18.4], [xb1, 19.8, -16.2], mv_, faixa=(17, 22.4), res=4)]))
    cab.append(osso("barbela", [0, 22.6, -17.2], [0, 0, 0], tiras))          # osso animado (balança)
    # elmo: aba em V que avança sobre os olhos, 2ª fileira em V atrás e acima, topo e nuca em degrau, têmporas
    for lado in (-1, 1):
        s = lado_s(lado)
        x0, x1 = sorted((0.0, 8.6 * lado))
        cab.append(peca("elmo_aba_" + s, [x0, ABA_Y, -18.8], [x1, ABA_Y + 3.0, -14.6], mat_xadrez(2.2, 1, so_malva=True),
                        rot=(0, 0, ABA_ANG * lado), pivo=(0, ABA_Y, -16.0), faixa=(ABA_Y, ABA_Y + 3.0), res=4))
        cab.append(peca("elmo_fila2_" + s, [x0 * 0.98, ABA_Y + 2.4, -17.9], [x1 * 0.98, ABA_Y + 5.4, -11.0], mat_xadrez(2.2, 0),
                        rot=(0, 0, 10 * lado), pivo=(0, ABA_Y + 2.4, -14.0), faixa=(ABA_Y + 2.4, ABA_Y + 5.4), res=4))
        t0, t1 = sorted((7.2 * lado, 9.0 * lado))
        cab.append(peca("elmo_tempora_" + s, [t0, 26.0, -16.6], [t1, 30.4, -12.4], mat_xadrez(2.2, 1, eixo=2),
                        faixa=(26, 30.4), res=4))
    cab.append(peca("elmo_topo", [-7.6, 29.2, -16.2], [7.6, 31.6, -8.0], mat_xadrez(2.4, 1), faixa=(29.6, 33.0), res=3))
    cab.append(peca("elmo_topo2", [-6.2, 29.6, -15.4], [6.2, 32.2, -8.6], mat_xadrez(2.4, 0), faixa=(29.6, 33.6), res=3))
    cab.append(peca("elmo_nuca", [-8.3, 25.8, -8.6], [8.3, 32.2, -2.6], mat_xadrez(2.4, 0), faixa=(25.8, 32.2), res=3))
    cab.append(peca("elmo_nuca2", [-7.0, 25.4, -8.0], [7.0, 32.8, -2.2], mat_xadrez(2.4, 1), faixa=(25.4, 32.8), res=3))
    # placa da bochecha (meandro, girada 35° para fora, da altura do olho à base do bico) e placa da têmpora (fenda)
    for lado in (-1, 1):
        s = lado_s(lado)
        fora = "east" if lado > 0 else "west"
        cx = 8.6 * lado
        cab.append(peca("placa_bochecha_" + s, [cx - 1.0, 19.8, -14.7], [cx + 1.0, 26.0, -8.1],
                        mat_placa_glifo({fora: MEANDRO_CAB}, espelha=lado < 0), rot=(0, 35 * lado, 0),
                        pivo=(cx, 22.9, -11.4), res=5))
        p0, p1 = sorted((7.6 * lado, 9.3 * lado))
        cab.append(peca("placa_tempora_" + s, [p0, 24.8, -12.0], [p1, 29.2, -5.6],
                        mat_placa_glifo({fora: FENDA_CAB}, espelha=lado < 0), res=5))
    # crista vermelha em blocos: o bloco da frente desce sobre a aba; lâmina do meio em 3 degraus + 2 lâminas laterais
    mcr = mat_chapado(lambda p, f: mix(VERM_CL, VERM, clamp((38.5 - p[1]) / 6.5)) if f != "down" else VERM_ESC, borda=.12, curva=.25)
    crista = [
        peca("crista_bico", [-1.7, 29.8, -18.4], [1.7, 33.2, -14.6], mcr, faixa=(30, 38.1)),
        peca("crista_frente", [-1.7, 30.6, -15.0], [1.7, 36.8, -11.2], mcr, faixa=(30, 38.1)),
        peca("crista_meio", [-1.7, 31.0, -11.6], [1.7, 38.1, -6.4], mcr, faixa=(30, 38.1)),
        peca("crista_tras", [-1.7, 30.6, -6.8], [1.7, 36.6, -3.4], mcr, faixa=(30, 38.1)),
    ]
    for lado in (-1, 1):
        x0, x1 = sorted((1.6 * lado, 5.0 * lado))
        crista.append(peca("crista_lado_" + lado_s(lado), [x0, 31.4, -12.0], [x1, 35.4, -5.4], mcr, faixa=(30, 38.1)))
    cab.append(osso("crista", [0, 32.0, -8.0], [-5, 0, 0], crista))
    return cab

# ---------------- peito ----------------
def mat_escamas(y0, y1, larg=2.4, ponta=1.4):
    """Fileira de penas do peito numa peça só: tiras verticais de 'larg' unidades; embaixo, as pontas das penas
    (alternando comprimento) em pêssego com um fio entre elas: lê como penas em escama."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        a = x if face in ("north", "south", "up", "down") else z
        idx = int(math.floor(a / larg))
        fr = a / larg - idx
        lim = y0 + ponta + (0.7 if idx % 2 else 0.0)
        luz = luz_face(c, curva=0.08, borda=0.1, cima=0.05)
        if face in ("up", "down"): return tom(CREME, luz)
        if y < lim:
            cor = CREME_SOM
            if fr < 0.1: luz -= 0.1
        else:
            cor = CREME
            if y - lim < 0.3: luz -= 0.08
        return tom(cor, luz)
    return f

def peito_pecas():
    pp = []
    # 3 fileiras de penas, cada uma em 3 blocos (o do meio mais à frente, os dos lados recuados e um pouco mais
    # baixos): o peito fica arredondado, sem prateleira lisa
    for k, (y0, y1, z0, z1, w) in enumerate([(18.4, 22.0, -16.6, -11.0, 5.6), (15.2, 19.0, -15.4, -9.0, 6.4),
                                             (12.0, 15.8, -14.2, -8.0, 7.0)]):
        m = mat_escamas(y0, y1)
        pp.append(peca(f"peito{k}_meio", [-w * 0.42, y0, z0 - 0.4], [w * 0.42, y1, z1], m, faixa=(y0, y1), res=4))
        for lado in (-1, 1):
            a0, a1 = sorted((w * 0.4 * lado, w * lado))
            pp.append(peca(f"peito{k}_{lado_s(lado)}", [a0, y0 - 0.3, z0 + 0.5], [a1, y1 - 0.2, z1], m, faixa=(y0, y1), res=4))
    n, w, y0, y1 = 6, 7.2, 9.4, 12.6                      # franja regular, terminando logo acima das coxas
    larg = 2 * w / n
    for i in range(n):
        x0 = -w + i * larg
        pp.append(peca(f"saia{i}", [x0 + 0.03, y0, -11.6], [x0 + larg - 0.03, y1, -5.0],
                       mat_escamas(y0, y1, larg=larg, ponta=1.2), faixa=(y0, y1), res=2))
    return pp

# ---------------- cauda ----------------
def cauda_blindada():
    """Cone telescópico de 5 anéis sólidos arredondados, cada um menor e encaixado no anterior, inclinado 30° para
    baixo e terminando em ponta; cada anel é um osso (cauda_anel_k) filho do anterior."""
    ANEIS = [(7.4, 5.4, 2.5), (6.0, 4.4, 2.3), (4.7, 3.4, 2.1), (3.5, 2.6, 1.9), (2.3, 1.7, 1.8)]   # (meia larg., meia alt., compr.)
    PASSO = 1.6                     # arte conceitual: sai da garupa e desce íngreme para trás até perto do chão
    Z0, YC = 13.6, 13.0
    def seg(k, z0):
        W, H, L = ANEIS[k]
        filhos = anel_cauda(f"cauda_anel{k}", k + 1, z0, z0 + L, W, H, YC)
        if k + 1 < len(ANEIS): filhos.append(seg(k + 1, z0 + PASSO))
        else:   # ponta que afina
            mp = mat_liso(LARANJA, borda=.12)
            filhos += [peca("cauda_ponta", [-1.4, YC - 1.1, z0 + L - 0.3], [1.4, YC + 1.1, z0 + L + 1.2], mp, faixa=(YC - 1, YC + 1)),
                       peca("cauda_ponta2", [-0.7, YC - 0.6, z0 + L + 1.0], [0.7, YC + 0.6, z0 + L + 2.2], mp, faixa=(YC - 1, YC + 1))]
        return osso(f"cauda_anel_{k}", [0, YC, z0], [0, 0, 0], filhos)
    return osso("cauda", [0, YC, Z0], [50, 0, 0], [seg(0, Z0)])

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
    corpo.append(peca("tronco", [-10.0, 8.0, -6.5], [10.0, 26.0, 13.0],
                      mat_chapado(lambda p, f: cor_traseira(p[1]) if f == "south" else MALVA, borda=0, curva=0), faixa=(8, 27)))
    corpo += peito_pecas()
    # carapaça: 5 cintas em degrau, a mais alta logo atrás da cabeça, cada uma com aba de telha sobre a seguinte
    CINTAS = [  # (z0, z1, meia largura, y baixo, y alto)
        (-5.6, -0.4, 12.4, 8.8, 31.8),
        (-1.4, 3.8, 13.0, 8.6, 31.2),
        (2.8, 8.2, 13.4, 8.4, 29.8),
        (7.2, 11.8, 12.8, 8.4, 27.6),
        (10.6, 14.2, 11.4, 8.6, 24.8),
    ]
    for k, (z0, z1, W, yb, yt) in enumerate(CINTAS):
        corpo += cinta(f"cinta{k}", k, z0, z1, W, yb, yt)
    # garupa: anel fechado por baixo da última cinta, de onde sai a cauda
    corpo += anel_cauda("garupa", len(CINTAS), 12.8, 15.6, 9.4, 6.4, 15.0)

    # asas: 3 placas empilhadas recuando para baixo (ombro mais largo e chanfrado) + a placa do ombro chanfrada
    for lado in (-1, 1):
        s = lado_s(lado)
        asa = []
        x0, x1 = sorted((8.2 * lado, 12.9 * lado))
        asa += g.arredondado("asa_ombro_" + s, [x0, 17.6, -11.4], [x1, 23.0, -1.6], mat_xadrez(2.6, 0, eixo=2), r=0.8, res=2)
        x0, x1 = sorted((8.6 * lado, 12.8 * lado))
        asa.append(peca("asa_meio_" + s, [x0, 13.4, -10.6], [x1, 18.0, -2.0], mat_xadrez(2.6, 1, eixo=2), faixa=(13.4, 18), res=2))
        x0, x1 = sorted((9.0 * lado, 12.0 * lado))
        asa.append(peca("asa_baixo_" + s, [x0, 10.6, -9.6], [x1, 13.8, -2.6], mat_xadrez(2.6, 0, eixo=2), faixa=(10.6, 13.8), res=2))
        fora = "east" if lado > 0 else "west"
        cx, cz = 13.0 * lado, -3.0
        # placa chanfrada: corpo grosso por dentro + face do emblema um pouco menor por fora
        b0, b1 = sorted((cx - 1.4 * lado, cx + 0.3 * lado))
        asa.append(peca("ombro_placa_corpo_" + s, [b0, 10.4, cz - 6.3], [b1, 22.0, cz + 6.3], mat_liso(MALVA, borda=.12),
                        rot=(6, 0, 5 * lado), pivo=(cx, 16.1, cz), res=2))
        f0, f1 = sorted((cx + 0.2 * lado, cx + 1.0 * lado))
        asa.append(peca("ombro_placa_" + s, [f0, 11.0, cz - 5.7], [f1, 21.4, cz + 5.7],
                        mat_placa_glifo({fora: EMBLEMA_OMBRO}, espelha=lado < 0, margem=0.08),
                        rot=(6, 0, 5 * lado), pivo=(cx, 16.1, cz), res=4))
        corpo.append(osso("asa_" + s, [11.0 * lado, 21.0, -2.0], [0, 0, 0], asa))

    corpo.append(cauda_blindada())
    corpo.append(pescoco)
    tronco = osso("corpo", [0, 9.0, 0.0], [0, 0, 0], corpo)

    # ======================= PERNAS =======================
    def perna(lado):
        s = lado_s(lado); xc = 6.6 * lado; zc = 0.0
        pp = []
        mam = mat_chapado(lambda p, f: AMARELO_SOM if f == "down" else (AMARELO_CL if f == "up" else AMARELO), borda=.06, curva=0)
        pp += g.arredondado("perna_" + s, [xc - 3.5, 3.4, zc - 4.2], [xc + 3.5, 9.6, zc + 4.2], mam, r=0.6, faixa=(0, 9.6))
        pp.append(peca("calcanhar_" + s, [xc - 3.7, 0.0, zc - 3.8], [xc + 3.7, 3.8, zc + 4.0], mam, faixa=(0, 9.6)))
        mg = mat_chapado(lambda p, f: CINZA_CL if f == "up" else CINZA, borda=.12, curva=.1)
        for k, dx in enumerate((-2.75, 0.0, 2.75)):          # 3 dedos amarelos, cada um com a garra grande na ponta
            x = xc + dx
            pp.append(peca(f"dedo{k}_{s}", [x - 1.25, 0.0, zc - 7.4], [x + 1.25, 2.4, zc - 3.6], mam, faixa=(0, 9.6)))
            pp.append(peca(f"garra{k}_{s}", [x - 1.2, 0.0, zc - 10.6], [x + 1.2, 3.6, zc - 7.2], mg, faixa=(0, 3.6)))
        pp.append(peca("garra_tras_" + s, [xc - 1.5, 0.0, zc + 3.8], [xc + 1.5, 3.4, zc + 7.4], mg, faixa=(0, 3.4)))
        return osso("perna_" + s, [xc, 9.6, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
