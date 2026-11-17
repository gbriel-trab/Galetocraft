"""Salambrasa (#012, Fogo): o galo-salamandra das brasas, quadrúpede roxo-grafite com manchas incandescentes,
pescoço alto, cabeça grande de crista em degrau e juba de penas de fogo."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp

ID = "salambrasa"; NOME = "Salambrasa"; NUMERO = 12
ALTURA = 2.45
QUADRUPEDE = True
ROSTO = ((0, 29.5, -21.5), 10.0)
N_RABO = 12
ONDAS = [("rabo", N_RABO, (1.5, 2.5, 0))]
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta: quadros da Paleta de Cores da _ficha (amostrados com PIL) ----------------
# carvão (46,35,44) · cinza-roxo (103,78,95) · malva (131,94,111) · vermelho (202,24,30) · laranja-vermelho (253,69,11)
# laranja (253,115,2) · amarelo (254,201,37) · creme (251,223,198)
GRAFITE = (66, 51, 62); GRAFITE_ESC = (46, 35, 44); GRAFITE_CLARO = (87, 70, 80)        # corpo carvão-arroxeado
MALVA = (110, 92, 104); MALVA_CLARA = (138, 116, 128); MALVA_ESC = (86, 70, 82)          # placas do ombro, viseira, pé
CABECA = (96, 78, 90); CABECA_CLARA = (116, 96, 108); CABECA_ESC = (70, 56, 66)          # cabeça cinza-roxa (quadro 103,78,95)
FACE = (104, 86, 98)
VISEIRA = MALVA; VISEIRA_CLARA = (132, 112, 124); VISEIRA_ESC = MALVA_ESC
BICO = (138, 116, 128); BICO_CLARO = (156, 134, 146); BICO_ESC = (112, 92, 104)          # malva clara
DEDO = (191, 169, 179); DEDO_CLARO = (210, 192, 200); DEDO_ESC = (156, 134, 146)
CRISTA = (200, 40, 42); CRISTA_ESC = (168, 26, 30); CRISTA_CLARA = (232, 68, 58)          # lados / topo das lâminas
VERM = (192, 40, 42); VERM_ESC = (170, 26, 24)
LARANJA = (240, 90, 30); LARANJA_ESC = (253, 69, 11); AMARELO = (245, 197, 24); OURO = (245, 197, 24)
LARANJA_M = (247, 147, 30)
PLACA = (252, 160, 52); PLACA_CLARA = (255, 196, 116); PLACA_ESC = (196, 92, 18)          # escamas da barriga
VENTRE = (247, 147, 30)
CREME = (244, 230, 220)
BRASA = (245, 197, 24); BRASA_BORDA = (247, 147, 30)                                     # manchas: amarelo cheio, halo laranja

def escurecer(c, f):
    """Escurece mantendo o matiz (sem puxar para o oliva)."""
    return tuple(int(v * (1 - f)) for v in c)

# ---------------- manchas incandescentes (hexágonos) ----------------
def mancha(p, face, lista):
    """Cor da mancha no ponto (ou None). lista = [((cx, cy, cz), raio, profundidade)]; raio pode ser (rx, ry, rz).
    Desenho: hexágono chapado (ponta para os lados da face), corpo amarelo, beirada laranja e miolo pouco mais claro.
    Só aparece nas faces a menos de 'profundidade' do centro."""
    x, y, z = p
    for (cx, cy, cz), r, prof in lista:
        rx, ry, rz = r if isinstance(r, tuple) else (r, r, r)
        dx, dy, dz = x - cx, y - cy, z - cz
        if face in ("east", "west"): a, b, n = dz / rz, dy / ry, dx
        elif face in ("north", "south"): a, b, n = dx / rx, dy / ry, dz
        else: a, b, n = dx / rx, dz / rz, dy
        if abs(n) > prof: continue
        cor = hexa(a, b)
        if cor: return cor
    return None

def hexa(a, b, borda=0.16):
    """Mancha da ficha: octógono amarelo cheio com borda laranja fina (a, b normalizados pelo meio-tamanho)."""
    d = max(abs(a), abs(b), (abs(a) + abs(b)) / 1.4)
    if d > 1: return None
    return BRASA_BORDA if d > 1 - borda else BRASA

# manchas da cauda medidas na ficha (vista lateral: centro z, y, largura, altura; vista de trás: x, y, largura, altura)
MANCHAS_CAUDA_LADO = [(23.3, 13.5, 3.0, 3.4), (23.0, 21.9, 3.6, 4.2), (17.1, 26.8, 4.0, 3.0),
                      (15.4, 13.6, 3.4, 2.6), (10.0, 14.0, 3.6, 2.8), (10.2, 28.6, 3.6, 2.4), (19.8, 17.4, 2.8, 3.2)]
MANCHAS_CAUDA_TRAS = [(0.0, 17.6, 4.4, 5.2), (0.0, 10.4, 3.0, 2.6), (0.0, 23.4, 2.4, 1.8),
                      (-3.0, 21.0, 1.6, 2.2), (3.0, 21.0, 1.6, 2.2), (-3.0, 13.8, 1.6, 2.2), (3.0, 13.8, 1.6, 2.2)]

def mancha_cauda(pw, nw):
    x, y, z = pw
    if abs(nw[0]) > 0.7:
        for zc, yc, L, H in MANCHAS_CAUDA_LADO:
            c = hexa((z - zc) / (L / 2), (y - yc) / (H / 2))
            if c: return c
    if nw[2] > 0.6:
        for xc, yc, L, H in MANCHAS_CAUDA_TRAS:
            c = hexa((x - xc) / (L / 2), (y - yc) / (H / 2))
            if c: return c
    return None

FENDAS_DORSO = [(2.4, -5.4), (-2.4, -5.4)]       # rachaduras em Y no alto do dorso, perto do ombro (x, z)

def fenda_dorso(p, face):
    """Rachadura em Y brilhante no topo do lombo (só nas faces de cima do alto do dorso)."""
    if face != "up" or p[1] < 22.2: return None
    for xc, zc in FENDAS_DORSO:
        q = (p[0] - xc, p[2] - zc)
        d = min(dist_seg(q, (0, 0), b) for b in ((0, -1.8), (1.4, 1.2), (-1.4, 1.2)))
        if d < 0.3: return BRASA
        if d < 0.5: return BRASA_BORDA
    return None

def mat_com_manchas(cor_fn, lista, **kw):
    base = g.mat_cor(cor_fn, **kw)
    def f(c):
        m = mancha(c["p"], c["face"], lista) or fenda_dorso(c["p"], c["face"])
        return m if m else base(c)
    return f

def brilho_manchas(lista):
    return lambda c, cor: (mancha(c["p"], c["face"], lista) or fenda_dorso(c["p"], c["face"])) is not None

def dist_seg(p, a, b):
    ab = [b[i] - a[i] for i in range(len(a))]; ap = [p[i] - a[i] for i in range(len(a))]
    t = clamp(sum(ab[i] * ap[i] for i in range(len(a))) / max(sum(v * v for v in ab), 1e-6))
    return math.sqrt(sum((ap[i] - t * ab[i]) ** 2 for i in range(len(a))))

# ---------------- penas em bloco (grossas, com ponta em degrau) ----------------
def mat_pena_bloco(cores, y0, L):
    """Pena grossa pendurada de y0: 3 faixas chapadas (raiz, meio, ponta), face de fora clara, de baixo escura."""
    c0, c1, c2 = cores
    def f(c):
        v = (y0 - c["p"][1]) / L
        base = c0 if v < 0.42 else c1 if v < 0.78 else c2           # vermelho na raiz, laranja, amarelo só na ponta
        face = c["face"]
        if face == "up": base = mix(base, (255, 236, 200), 0.15)
        elif face == "down": base = escurecer(base, 0.18)
        elif face in ("north", "south"): base = escurecer(base, 0.06)
        return escurecer(base, 0.1) if g.na_borda(c) else base
    return f

def pena_bloco(nome, raiz, rot, L, W, cores, esp=1.0, brilho=False):
    """Pena (ou escama) grossa: bloco + ponta em losango (cubo girado 45°), pendurada para baixo da raiz."""
    return g.placa_armadura(nome, raiz, rot, L, W, esp=esp, mat=mat_pena_bloco(cores, raiz[1], 0.72 * L + W / 2))

def pena_cone(nome, raiz, phi, flare, L, W, lado, cores, varre=0, esp=1.0):
    """Pena grossa numa 'saia' em volta do pescoço (phi = 0 lado de fora, negativo = frente)."""
    return osso(nome, list(raiz), [0, -phi * lado, 0], [pena_bloco(nome + "_p", raiz, (-varre, 0, flare * lado), L, W, cores, esp)])

# ---------------- corpo ----------------
VENTRE_Y = 12.4          # terço de baixo do tronco: laranja, com transição para o carvão

def cor_corpo(p, face):
    x, y, z = p
    if face == "down" or y < VENTRE_Y: return VENTRE
    if y < VENTRE_Y + 1.4: return mix(VENTRE, GRAFITE, (y - VENTRE_Y) / 1.4)
    return GRAFITE

# (centro, meio-tamanho, profundidade): 2 fileiras de octógonos de cada lado do tronco, como na ficha
MANCHAS_CORPO = []
for lado in (-1, 1):
    MANCHAS_CORPO += [((5.6 * lado, 16.4, z), (1, 1.2, 1.5), 0.35) for z in (-8.0, -2.4, 3.2, 8.4)]
    MANCHAS_CORPO += [((5.6 * lado, 13.6, z), (1, 1.0, 1.3), 0.35) for z in (-5.2, 0.4, 5.8)]
    MANCHAS_CORPO += [((5.2 * lado, 19.0, z), (1, 1.0, 1.3), 0.35) for z in (-6.0, 1.0)]

def mat_placa(i, n):
    """Escama da barriga nº i (de n, de cima para baixo): laranja da paleta em degradê (pêssego em cima, laranja quente
    embaixo), rente ao corpo; a borda de baixo é um arco (chevron) com uma linha escura de 1 px."""
    c_top = mix(PLACA_CLARA, PLACA, i / max(n - 1, 1) * 1.6)
    c_bot = mix(PLACA, (246, 112, 36), i / max(n - 1, 1))
    def f(c):
        face = c["face"]
        (x0, y0, _), (x1, y1, _) = c["b"]
        v = clamp((y1 - c["p"][1]) / max(y1 - y0, 1e-6))
        u = abs(c["p"][0]) / max(x1, 1e-6)
        if face == "up": return c_top
        if face == "down": return escurecer(c_bot, 0.2)
        linha = 0.86 - 0.3 * u * u                       # borda de baixo em arco: mais baixa no meio
        if face in ("east", "west"): return escurecer(c_bot, 0.08)
        if v > linha + 0.1: return escurecer(c_bot, 0.12)
        if v > linha: return PLACA_ESC
        return mix(c_top, c_bot, v / max(linha, 0.1))
    return f

# ---------------- cauda em gancho ----------------
def rot_x(q, o, ang):
    """Gira o ponto q (x, y, z) em volta do eixo x que passa por o, como o Blockbench (positivo = frente para baixo)."""
    c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    dy, dz = q[1] - o[1], q[2] - o[2]
    return (q[0], o[1] + dy * c - dz * s_, o[2] + dy * s_ + dz * c)

def mat_rabo(w, h, py, z0, L, k, cadeia):
    """Segmento da cauda. Base: dorso ameixa e barriga laranja embaixo; no gancho a faixa laranja corre por fora da
    curva (atrás) e por dentro (em cima). As manchas são desenhadas no MUNDO, onde a ficha as mostra: o ponto é levado
    pela 'cadeia' de giros [(origem, ângulo), ...] (da peça até a raiz da cauda)."""
    def cor(p, face):
        x, y, z = p
        v = (y - (py - h / 2)) / h
        if k < 3:                                   # base: barriga laranja embaixo, com borda baixa nos lados
            if face == "down": return VENTRE
            if v < 0.26: return VENTRE
            if v < 0.36: return mix(VENTRE, GRAFITE, (v - 0.26) / 0.1)
        return GRAFITE
    fundo = g.mat_cor(cor, borda=.0, curva=.2)
    def mundo(c):
        pw = c["p"]; n = g.NORMAL[c["face"]]; nw = n
        for o, ang in cadeia:
            pw = rot_x(pw, o, ang); nw = rot_x(nw, (0, 0, 0), ang)
        return mancha_cauda(pw, nw)
    def f(c):
        return mundo(c) or fundo(c)
    return f, (lambda c, cor_: mundo(c) is not None)

def secao(nome, px, py, z0, z1, w, h, mat, br, **kw):
    """Seção arredondada ao longo de z: 3 blocos (cruz + miolo chanfrado)."""
    r = 0.28 * min(w, h); q = r / 2
    fx = (py - h / 2, py + h / 2)
    return [peca(nome + "_a", [px - w / 2, py - h / 2 + r, z0], [px + w / 2, py + h / 2 - r, z1], mat, faixa=fx, brilho=br, res=3, **kw),
            peca(nome + "_b", [px - w / 2 + r, py - h / 2, z0], [px + w / 2 - r, py + h / 2, z1], mat, faixa=fx, brilho=br, res=3, **kw),
            peca(nome + "_c", [px - w / 2 + q, py - h / 2 + q, z0], [px + w / 2 - q, py + h / 2 - q, z1], mat, faixa=fx, brilho=br, res=3, **kw)]

def cauda_gancho(nome, base, segs):
    """Cadeia de ossos '<nome>_0', '<nome>_1'..., cada um com giro próprio (rx): a cauda corre para trás, sobe e
    enrola num gancho para a frente. segs = [(comprimento, largura, altura, rx)]. Em cada junta um anel girado pela
    metade do ângulo tapa o vão do lado de fora da curva; a ponta termina num toco arredondado."""
    def seg(k, pos, cadeia_pai):
        L, w, h, rx = segs[k]
        px, py, pz = pos
        cad = [((px, py, pz), rx)] + cadeia_pai
        mat, br = mat_rabo(w, h, py, pz, L, k, cad)
        filhos = secao(f"{nome}_{k}", px, py, pz - 0.8, pz + L, w, h, mat, br)       # sobreposto: sem frestas
        if k > 0:
            wp, hp = (segs[k - 1][1] + w) / 2, (segs[k - 1][2] + h) / 2
            e = 0.5 + (hp / 2) * math.tan(math.radians(abs(rx) / 2))
            mj, bj = mat_rabo(wp, hp, py, pz, L, k, [((px, py, pz), -rx / 2)] + cad)
            filhos += secao(f"{nome}_{k}_junta", px, py, pz - e, pz + e, wp, hp, mj, bj, rot=(-rx / 2, 0, 0), pivo=(px, py, pz))
        if k + 1 < len(segs): filhos.append(seg(k + 1, (px, py, pz + L), cad))
        else:
            filhos += secao(f"{nome}_ponta", px, py, pz + L - 0.2, pz + L + 0.9, w * 0.66, h * 0.66, mat, br)
            filhos += secao(f"{nome}_ponta2", px, py, pz + L + 0.7, pz + L + 1.4, w * 0.36, h * 0.36, mat, br)
        return osso(f"{nome}_{k}", [px, py, pz], [rx, 0, 0], filhos)
    return seg(0, base, [])

# ---------------- cabeça ----------------
OLHO_Y = 28.2
FAC_T = 2.4                       # espessura da peça da face diagonal (onde fica o olho)
FAC_A = (2.1, -21.4); FAC_B = (4.9, -17.4)          # superfície da face diagonal (lado +x), da frente para trás
FAC_L = math.hypot(FAC_B[0] - FAC_A[0], FAC_B[1] - FAC_A[1])
FAC_ANG = math.degrees(math.atan2(FAC_B[0] - FAC_A[0], FAC_B[1] - FAC_A[1]))   # ~35°: o olho aparece de frente e de lado
FAC_M = ((FAC_A[0] + FAC_B[0]) / 2, (FAC_A[1] + FAC_B[1]) / 2)
_n = (math.cos(math.radians(FAC_ANG)), -math.sin(math.radians(FAC_ANG)))          # normal de fora (lado +x)
FAC_C = (FAC_M[0] - _n[0] * FAC_T / 2, FAC_M[1] - _n[1] * FAC_T / 2)

def cor_cabeca(p, face):
    """Alto da cabeça cinza-ameixa; da altura do olho para baixo, a 'cara' malva clara (como na ficha)."""
    x, y, z = p
    if face == "up": return CABECA_CLARA
    if y < 27.0 and face != "down": return FACE
    return CABECA

def mat_faceta(lado):
    base = g.mat_cor(cor_cabeca, borda=.0, curva=.25)
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u = z - FAC_C[1]
            o = g.pintar_olho(u + 0.1, y - OLHO_Y, 2.0, 1.75, iris=((160, 34, 14), (224, 74, 30)), esclera=CREME,
                              r_iris=(0.6, 0.82), c_iris=(-0.34, -0.1), r_pup=(0.26, 0.32), bravo=0.3, alto=0.5,

                              contorno=(192, 48, 24))
            if o: return o
        return base(c)
    return f

def mat_viseira(c):
    """Viseira cinza-malva, mais clara que a cabeça; topo 1 tom mais claro."""
    face = c["face"]
    base = VISEIRA_CLARA if face == "up" else VISEIRA_ESC if face == "down" else VISEIRA
    return escurecer(base, 0.12) if g.na_borda(c) else base

def mat_bico(c):
    """Malva clara de uma cor só; faixa de baixo um tom mais escura; narina escura pequena perto da base, de lado."""
    face = c["face"]; x, y, z = c["p"]
    if face in ("east", "west") and -22.4 < z < -21.7 and 27.6 < y < 28.2: return (52, 38, 46)
    if face == "up": return BICO_CLARO
    if face == "down" or y < 26.0: return BICO_ESC
    return escurecer(BICO, 0.06) if g.na_borda(c) else BICO

def mat_crista(c):
    """Lâmina vermelha: lados #c0282a, topo e alto da lâmina mais claros (#e8443a), base mais escura."""
    face = c["face"]
    (_, y0, _), (_, y1, _) = c["b"]
    t = clamp((c["p"][1] - y0) / max(y1 - y0, 1e-6))
    if face == "up": return CRISTA_CLARA
    if face == "down": return CRISTA_ESC
    base = mix(CRISTA, CRISTA_CLARA, clamp((t - 0.55) / 0.45)) if t > 0.55 else CRISTA
    if face == "south": base = escurecer(base, 0.1)
    return escurecer(base, 0.12) if g.na_borda(c) else base

def bloco_crista(nome, de, ate, rot=(0, 0, 0), pivo=None):
    return peca(nome, de, ate, mat_crista, rot=rot, pivo=pivo, res=3)

# ---------------- ombro: escamas escuras com a fenda em Y + penas de fogo ----------------
def mat_escama(lado, P, com_fenda=True):
    fora = "east" if lado > 0 else "west"
    FENDA = [((0.0, 0.0), (2.0, -1.7)), ((0.0, 0.0), (-2.1, -1.6)), ((0.0, 0.0), (0.0, 2.6))]
    def fenda(c):
        if not com_fenda or c["face"] != fora: return None
        q = (c["p"][2] - P[2], c["p"][1] - P[1])
        d = min(dist_seg(q, a, b) for a, b in FENDA)
        if d < 0.38: return BRASA
        if d < 0.62: return BRASA_BORDA
        return None
    def f(c):
        cr = fenda(c)
        if cr: return cr
        face = c["face"]
        base = MALVA_CLARA if face == "up" else MALVA_ESC if face == "down" else MALVA
        return MALVA_CLARA if g.na_borda(c) and face == fora else base
    return f, (lambda c, cor: fenda(c) is not None)

def escama(nome, raiz, rot, giro, L, W, m, br, esp=1.3):
    """Escama grafite grossa, pendurada da raiz, com ponta em losango; 'giro' (em y) vira a face larga."""
    x, y, z = raiz
    cy = y - L * 0.72; sq = W / 1.4142
    return osso(nome + "_giro", list(raiz), [0, giro, 0], [osso(nome, list(raiz), list(rot), [
        peca(nome, [x - esp / 2, cy, z - W / 2], [x + esp / 2, y, z + W / 2], m, res=4, brilho=br),
        peca(nome + "_ponta", [x - esp / 2 + 0.02, cy - sq / 2, z - sq / 2], [x + esp / 2 - 0.02, cy + sq / 2, z + sq / 2], m,
             rot=(45, 0, 0), pivo=(x, cy, z), res=4, brilho=br)])])

def ombro(lado):
    """Asinha do ombro: uma ombreira grafite sobre o alto da pata da frente, 3 escamas grossas deitadas para trás como
    uma asa dobrada (a do meio com a fenda em Y que brilha) e, por baixo, um leque de penas de fogo para trás."""
    s = "d" if lado < 0 else "e"
    filhos = []
    cores_fogo = [(VERM, LARANJA, AMARELO), (VERM, LARANJA_ESC, LARANJA), (LARANJA_ESC, LARANJA, AMARELO), (VERM, LARANJA_ESC, AMARELO)]
    # leque de penas pontudas caindo para trás (~30° abaixo da horizontal); as de baixo chegam ao meio do tronco
    for k, (y, z, rx, L) in enumerate([(20.4, -10.6, -82, 11.6), (19.8, -9.4, -74, 13.2), (19.2, -8.2, -66, 14.2),
                                       (18.6, -7.0, -58, 14.0), (18.0, -6.0, -50, 12.4)]):
        raiz = (6.5 * lado + 0.12 * lado * k, y, z)
        filhos.append(pena_bloco(f"fogo{k}_{s}", raiz, (rx, 0, 14 * lado), L, 3.0, (VERM, LARANJA, OURO), esp=1.1))
    # ombreira: olha meio para a frente, cobre o alto da pata
    m0, b0 = mat_escama(lado, (0, 0, 0), False)
    filhos.append(escama(f"ombreira_{s}", (6.3 * lado, 20.8, -11.4), (-20, 0, 14 * lado), 38 * lado, 4.6, 4.2, m0, b0))
    # asa dobrada: escamas deitadas para trás, em camadas
    for k, (z, y, L, W, rx) in enumerate([(-4.8, 20.2, 7.6, 3.8, -74), (-7.2, 20.6, 8.6, 4.4, -68), (-9.6, 20.8, 9.2, 4.6, -62),
                                          (-11.6, 20.4, 7.4, 4.0, -56)]):
        raiz = (5.9 * lado + 0.25 * lado * k, y, z)
        m, br = mat_escama(lado, (raiz[0], y - 2.6, z), k in (1, 2))  # fenda em Y em 2 placas
        filhos.append(escama(f"escama{k}_{s}", raiz, (rx, 0, 16 * lado), 0, L, W, m, br, esp=1.1))
    return osso("asa_" + s, [5.6 * lado, 20.0, -8.0], [0, 0, 0], filhos)

# ---------------- pernas ----------------
def mat_dedo(c):
    face = c["face"]
    base = DEDO_CLARO if face == "up" else DEDO_ESC if face == "down" else tom(DEDO, 0.06) if face == "north" else DEDO
    return tom(base, -0.2) if g.na_borda(c) else base

def pata(nome, xc, zc):
    """Pata: base roxa e 3 dedos grandes cinza-claros em leque para a frente + 1 atrás."""
    pp = []
    pp.append(peca(nome + "_pata", [xc - 2.9, 0.4, zc - 2.6], [xc + 2.9, 3.4, zc + 2.4],
                   g.mat_cor(lambda p, f: MALVA, borda=.06, curva=.3), res=3))                 # pé malva robusto
    for k, (dx, giro, mw, mh, ml) in enumerate(((-2.3, 16, 1.0, 2.5, 3.9), (0.0, 0, 1.2, 2.8, 4.4), (2.3, -16, 1.0, 2.5, 3.9))):
        x0 = xc + dx; z0 = zc - 1.2                                                           # o do meio é maior
        pp.append(osso(f"{nome}_dedo{k}", [x0, 0, z0], [0, giro, 0],
                       [peca(f"{nome}_dedo{k}", [x0 - mw, 0, z0 - ml], [x0 + mw, mh, z0], mat_dedo, res=3)]))
    pp.append(peca(nome + "_dedo_tras", [xc - 0.8, 0, zc + 1.8], [xc + 0.8, 1.6, zc + 3.8], mat_dedo, res=3))
    return pp

def perna(nome, xc, zc, tras):
    """Perna: alto roxo, faixa laranja, tornozelo roxo e pata de dedos claros."""
    pp = []
    escuro = g.mat_cor(lambda p, f: GRAFITE, borda=.05, curva=.2)
    def cor_faixa(p, f, tras=tras):        # uma faixa só: laranja quente em cima -> laranja-amarelo embaixo
        y0, y1 = (3.6, 7.0) if tras else (4.2, 9.0)
        t = clamp((p[1] - y0) / (y1 - y0))
        return mix(LARANJA_M, LARANJA, t)
    faixa = g.mat_cor(cor_faixa, borda=.04, curva=.1)
    if tras:     # coxa grande com uma mancha incandescente do lado de fora
        lado = 1 if xc > 0 else -1
        mc = [((xc + 2.2 * lado, 12.2, zc - 0.2), (1, 1.6, 1.8), 0.9)]
        xt = xc - 0.6 * lado
        pp += g.arredondado2(nome + "_coxa", [xt - 2.6, 7.4, zc - 3.4], [xt + 2.6, 15.4, zc + 3.2],
                             mat_com_manchas(lambda p, f: GRAFITE, mc, borda=.05, curva=.2), r=2.0, brilho=brilho_manchas(mc))
    else:
        # braço: volume arredondado que afina para baixo (ombro largo dentro do corpo, cotovelo mais estreito)
        pp += g.arredondado2(nome + "_ombro", [xc - 2.4, 10.6, zc - 2.7], [xc + 2.4, 15.4, zc + 2.5], escuro, r=1.4,
                             rot=(16, 0, 0), pivo=(xc, 7.2, zc))
        pp += g.arredondado2(nome + "_braco", [xc - 2.0, 7.0, zc - 2.0], [xc + 2.0, 11.6, zc + 2.0], escuro, r=1.0,

                            rot=(16, 0, 0), pivo=(xc, 7.2, zc))
    yf0, yf1 = (3.6, 7.0) if tras else (4.2, 9.0)        # faixa laranja: mais baixa atrás, mais alta na frente
    pp += g.octogono(nome + "_faixa", [xc - 1.95, yf0, zc - 1.95], [xc + 1.95, yf1, zc + 1.95], faixa, r=0.6)   # canela mais fina
    pp += g.octogono(nome + "_tornozelo", [xc - 2.1, 2.4, zc - 2.1], [xc + 2.1, yf0 + 0.2, zc + 2.1], escuro, r=0.6)
    pp += pata(nome, xc, zc)
    return osso(nome, [xc, 12.0, zc], [0, 0, 0], pp)

# ---------------- deslocar um grupo inteiro (a pintura continua nas coordenadas de quando foi modelado) ----------------
def deslocar(desde, nos, dz, dy=0.0):
    """Empurra em z (dz) as peças criadas desde o índice 'desde' e os ossos 'nos'. Os materiais recebem o ponto de
    volta nas coordenadas originais, então desenhos que dependem da posição (o olho, as faixas) não mudam."""
    def volta(c):
        c = dict(c); x, y, z = c["p"]; c["p"] = (x, y - dy, z - dz)
        b0, b1 = c["b"]; c["b"] = ([b0[0], b0[1] - dy, b0[2] - dz], [b1[0], b1[1] - dy, b1[2] - dz])
        return c
    for pc in g.PECAS[desde:]:
        for arr in (pc.de, pc.ate, pc.pivo): arr[2] += dz; arr[1] += dy
        m = pc.mat; pc.mat = lambda c, m=m: m(volta(c))
        if callable(pc.brilho):
            b = pc.brilho; pc.brilho = lambda c, cor, b=b: b(volta(c), cor)
    def visita(no):
        if isinstance(no, dict):
            no["origin"][2] += dz; no["origin"][1] += dy
            for f in no["children"]: visita(f)
    for no in nos: visita(no)

DZ_CAB = -2.5; DY_CAB = 2.0   # a cabeça vai para a frente e para cima: o pescoço aparece, como na ficha

def lamina(nome, xm, y0, z0, L, esp, inc):
    """Lâmina da crista: placa fina vermelha de comprimento L que nasce em (y0, z0) e tomba 'inc' graus para trás."""
    return bloco_crista(nome, [-xm, y0, z0], [xm, y0 + L, z0 + esp], rot=(inc, 0, 0), pivo=(0, y0, z0 + esp))

# ---------------- montagem ----------------
def montar():
    i_cab = len(g.PECAS)
    # ---------- cabeça: bloco cinza-roxo, faces diagonais com o olho, viseira em V, bico adunco ----------
    cab = []
    mcab = g.mat_cor(cor_cabeca, borda=.03, curva=.25)
    fx = (23.0, 31.0)
    cab += g.arredondado("cranio", [-4.9, 23.6, -18.4], [4.9, 31.0, -12.6], mcab, r=0.8, faixa=fx, res=3)
    cab.append(peca("cranio_frente", [-2.3, 23.8, -21.5], [2.3, 30.6, -18.0], mcab, faixa=fx, res=3))
    cab.append(peca("queixo", [-3.6, 23.0, -20.2], [3.6, 24.6, -14.0], g.mat_cor(lambda p, f: CABECA_ESC, borda=.06), faixa=fx, res=3))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 23.9, cz - FAC_L / 2], [cx + FAC_T / 2, 30.4, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, FAC_ANG * lado, 0), pivo=(cx, 27.0, cz), faixa=fx, res=8))
        # viseira: cada metade desce ~16° para o meio (V) e passa só 0,5 da face; a borda de baixo corta o alto do olho
        x0, x1 = sorted((0.0, 5.1 * lado))
        cab.append(peca("viseira_" + s, [x0, 29.3, -22.0], [x1, 31.4, -15.0], mat_viseira, rot=(0, 0, 16 * lado),
                        pivo=(5.2 * lado, 31.4, -18.0), res=3))
    cab.append(peca("viseira_meio", [-0.9, 28.2, -22.0], [0.9, 30.2, -16.0], mat_viseira, res=3))      # vértice do V
    # bico: de frente uma cunha em V (degraus 3,4 -> 2,6 -> 1,8 -> 1,0); de lado comprido, dorso reto, ponta curvando
    cab.append(peca("bico0", [-1.7, 27.6, -25.0], [1.7, 28.6, -21.0], mat_bico, res=4))
    cab.append(peca("bico1", [-1.3, 26.6, -25.5], [1.3, 27.7, -21.0], mat_bico, res=4))
    cab.append(peca("bico2", [-0.9, 25.6, -25.7], [0.9, 26.7, -21.2], mat_bico, res=4))
    cab.append(peca("bico3", [-0.5, 24.8, -25.7], [0.5, 25.7, -24.5], mat_bico, res=4))                  # gancho da ponta
    # crista de brasa: 5 lâminas finas em leque, cada uma tombada ~35° para trás, sobrepostas como telhas, a de trás
    # mais alta; de frente estreita, com 2 lâminas laterais mais baixas (a 'cruz' da vista de frente)
    cr = []
    for k, (xm, z0, L, inc) in enumerate([(2.0, -21.8, 4.6, 26), (2.0, -19.8, 5.8, 30), (1.9, -17.8, 6.6, 32),
                                          (1.8, -15.6, 7.0, 34), (1.7, -13.4, 5.4, 38)]):
        cr.append(lamina(f"crista{k}", xm, 30.8, z0, L, 1.9, inc))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        for k, (z0, L, inc) in enumerate([(-20.4, 3.4, 30), (-16.6, 4.0, 36)]):
            x0, x1 = sorted((1.8 * lado, 4.6 * lado))
            cr.append(bloco_crista(f"crista_lado{k}_{s}", [x0, 30.8, z0], [x1, 30.8 + L, z0 + 1.9], rot=(inc, 0, 0),
                                   pivo=(0, 30.8, z0 + 1.9)))
        x0, x1 = sorted((4.8 * lado, 6.2 * lado))     # lóbulos vermelhos na altura do olho, atrás dele
        cr.append(bloco_crista("lobulo_" + s, [x0, 26.6, -15.4], [x1, 29.8, -13.0]))
    cab.append(osso("crista", [0, 31.0, -16.0], [0, 0, 0], cr))
    # penas das bochechas: atrás e abaixo do olho, caindo para trás
    boch = []
    for k, (x, y0, z0, L, rx, rz) in enumerate([(4.4, 29.0, -13.6, 6.4, -64, 12), (4.4, 27.0, -14.6, 6.8, -52, 16),
                                                (4.4, 25.4, -13.0, 7.0, -42, 18)]):
        for lado in (-1, 1):
            s = "d" if lado < 0 else "e"
            cores = [(CRISTA, VERM, LARANJA), (VERM, LARANJA, AMARELO), (VERM, LARANJA, AMARELO)][k]
            boch.append(pena_bloco(f"bochecha{k}_{s}", (x * lado, y0, z0), (rx, 0, rz * lado), L, 2.8, cores, esp=1.2))
    cab.append(osso("bochechas", [0, 26, -15], [0, 0, 0], boch))
    cabeca = osso("cabeca", [0, 24.0, -16.0], [0, 0, 0], cab)
    deslocar(i_cab, [cabeca], DZ_CAB, DY_CAB)

    # ---------- juba (coordenadas finais): nasce atrás e abaixo da bochecha e cai pelas costas do pescoço até a
    # cernelha; de frente só 2 abas pequenas ao lado do queixo. Penas pontudas, algumas carvão misturadas ----------
    C1 = (VERM, LARANJA, AMARELO)                    # degradê da ficha: vermelho -> laranja -> amarelo na ponta
    CC = (GRAFITE, GRAFITE_CLARO, MALVA)             # penas carvão
    juba = []
    JUBA = [  # (x, y, z, phi, abertura, varrida, comprimento, largura, cores) do lado esquerdo (+x); o direito é espelho
        (4.2, 26.2, -19.4, -55, 16, 12, 6.0, 3.2, C1),       # sob a bochecha: de frente é a aba laranja ao lado do queixo
        (4.4, 26.0, -17.6, 0, 18, 26, 8.0, 3.4, C1),
        (3.4, 25.8, -16.6, 25, 14, 34, 8.8, 3.4, C1),
        (1.6, 26.0, -15.6, 35, 8, 42, 8.8, 3.2, C1),
        (4.0, 23.2, -17.6, 5, 16, 24, 8.0, 3.2, C1),
        (3.6, 23.2, -16.2, 25, 14, 32, 7.8, 3.2, CC),
        (1.8, 23.4, -16.0, 35, 8, 38, 8.0, 3.2, C1),
        (3.6, 20.6, -15.6, 20, 14, 30, 7.2, 3.0, C1),
        (1.6, 20.8, -14.8, 35, 8, 36, 7.2, 3.0, CC),
        (3.2, 18.2, -13.4, 30, 12, 32, 6.2, 2.8, C1),
    ]
    for k, (x, y0, z, phi, fl, var, L, W, cores) in enumerate(JUBA):
        for lado in (-1, 1):
            juba.append(pena_cone(f"juba{k}_{'d' if lado < 0 else 'e'}", (x * lado, y0, z), phi, fl, L, W, lado, cores,
                                  varre=var, esp=1.2))
    juba = osso("juba", [0, 22.0, -16.0], [0, 0, 0], juba)

    # ---------- pescoço em S, escuro, com a faixa laranja na frente ----------
    pesc = []
    def mat_pesc(z_frente):
        return g.mat_cor(lambda p, f: VENTRE if (f == "north" or p[2] < z_frente + 1.0) else GRAFITE, borda=.03, curva=.2)
    PESC = [  # (nome, meia largura, y0, y1, z0, z1, inclinação, pivô)
        ("pescoco_baixo", 4.2, 6.4, 23.6, -16.8, -10.2, -40, (0, 15.0, -16.8)),
        ("pescoco_alto", 3.6, 17.6, 28.0, -22.4, -16.2, -12, (0, 22.6, -19.4)),
    ]
    for nome, xm, y0, y1, z0, z1, inc, pv in PESC:
        pesc += g.octogono(nome, [-xm, y0, z0], [xm, y1, z1], mat_pesc(z0), r=1.0, faixa=(9, 28), rot=(inc, 0, 0), pivo=pv)
    # escamas da barriga: 6 faixas em chevron, rentes, seguindo uma curva em S (da garganta, quase vertical, até o
    # peito, que vira para trás por baixo); cada faixa tem um 'recheio' atrás, ligando-a ao pescoço (sem vãos)
    P0, P1, P2 = (25.9, -23.0), (14.0, -21.8), (9.6, -12.6)
    def curva(t):
        y = (1 - t) ** 2 * P0[0] + 2 * t * (1 - t) * P1[0] + t * t * P2[0]
        z = (1 - t) ** 2 * P0[1] + 2 * t * (1 - t) * P1[1] + t * t * P2[1]
        ty = 2 * (1 - t) * (P1[0] - P0[0]) + 2 * t * (P2[0] - P1[0]); tz = 2 * (1 - t) * (P1[1] - P0[1]) + 2 * t * (P2[1] - P1[1])
        return y, z, math.degrees(math.atan2(-tz, -ty))
    recheio = g.mat_cor(lambda p, f: GRAFITE, borda=.02, curva=.1)
    LARG = [3.5, 4.0, 4.3, 4.1, 3.5, 2.7]
    for k, w in enumerate(LARG):
        t = 0.06 + k * 0.17
        yc, zc, ang = curva(t)
        h = 3.2
        pesc.append(peca(f"escama_barriga{k}", [-w, yc - h / 2, zc - 0.5], [w, yc + h / 2, zc + 0.8], mat_placa(k, len(LARG)),
                         rot=(ang, 0, 0), pivo=(0, yc, zc), res=3))
        pesc.append(peca(f"escama_recheio{k}", [-w + 1.2, yc - h / 2 + 0.2, zc + 0.6], [w - 1.2, yc + h / 2 - 0.2, zc + 3.6], recheio,
                         rot=(ang, 0, 0), pivo=(0, yc, zc), res=2))
    pesc += [juba, cabeca]
    pescoco = osso("pescoco", [0, 16.0, -13.0], [0, 0, 0], pesc)

    # ---------- tronco: lombo liso e arqueado (5 seções, a mais alta no meio), terço de baixo laranja ----------
    corpo = []
    mt = mat_com_manchas(cor_corpo, MANCHAS_CORPO, borda=.02, curva=.22)
    bt = brilho_manchas(MANCHAS_CORPO)
    fc = (8.4, 22.6)
    # lombo liso e arqueado: o tronco e duas camadas mais curtas e mais estreitas por cima, cada uma bem chanfrada
    corpo += g.arredondado2("tronco", [-5.6, 8.8, -13.6], [5.6, 20.6, 11.6], mt, r=3.0, faixa=fc, brilho=bt)
    corpo += g.arredondado2("lombo", [-5.2, 12.0, -12.0], [5.2, 21.8, 6.4], mt, r=3.4, faixa=fc, brilho=bt)
    corpo += g.arredondado("lombo_alto", [-4.3, 14.0, -10.0], [4.3, 22.7, 1.6], mt, r=2.6, faixa=fc, brilho=bt)
    corpo += [ombro(-1), ombro(1)]
    # cauda: tubo de seção quase quadrada, afinando até uma ponta arredondada
    Ls = [3.8, 3.4, 3.7, 3.6, 3.6, 3.6, 3.7, 3.6, 3.0, 2.4, 1.8, 1.4]
    Rs = [18, -18, -32, -30, -26, -24, -26, -26, -14, -2, 12, 14]
    Hs = [7.8, 7.6, 7.4, 7.2, 7.0, 6.6, 6.3, 6.0, 5.6, 5.0, 4.4, 3.4]
    Ws = [round(h * 1.15, 2) for h in Hs]
    corpo.append(osso("cauda", [0, 13.5, 9.8], [0, 0, 0], [cauda_gancho("rabo", (0, 13.5, 9.8), list(zip(Ls, Ws, Hs, Rs)))]))
    corpo.append(pescoco)
    tronco = osso("corpo", [0, 14.0, 6.0], [0, 0, 0], corpo)

    pernas = [perna("perna_fd", -7.0, -10.8, False), perna("perna_fe", 7.0, -10.8, False),
              perna("perna_td", -6.8, 6.8, True), perna("perna_te", 6.8, 6.8, True)]
    return [tronco] + pernas

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
