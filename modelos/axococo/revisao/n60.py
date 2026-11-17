"""Axococó (#008, Água): o galo-axolote das águas, conferido pela ARTE CONCEITUAL. Cabeça em bloco rosa-chiclete com
olho de pupila grande e azul em L; bico em cunha e barbela em dois lobos longos; três penachos fofos de brânquias de
cada lado, em leque; crista em 3 lobos só no alto; corpo redondo (sino) com peito de telhas creme; asas em escudo
oval com a espiral quadrada da 'Plumagem Úmida' e primárias em escada; foices azuis na cauda; pernas amarelas e
patas anfíbias de dedos roxo-cinza. Volumes inclinados e sobrepostos, 2-3 tons chapados por bloco."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, clamp

ID = "axococo"; NOME = "Axococó"; NUMERO = 8
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 26.5, -12), 10)

# ---------------- paleta (Paleta de Cores da ficha) ----------------
# (cores amostradas nos PNGs da ficha com PIL; veja modelos/axococo/detalhes.md)
CREME = (248, 228, 216)          # creme-pêssego (arte #f8e4d8; paleta (252,227,211))          # peito (252,215,200) / paleta (252,227,211)
CREME_SOMBRA = (232, 200, 184)   # borda de baixo de cada telha do peito (#e8c8b8)
ROSA_PALIDO = (252, 214, 212)    # bochecha (252,205,202)-(252,224,216)
ROSA_CLARO = (248, 164, 192)     # cabeça (251,173,195), asa (250,181,209), paleta (253,173,212)
ROSA_LUZ = (253, 212, 228)       # brilho da asa (253,219,234)
ROSA = (252, 120, 161)           # brânquia
ROSA_GUELRA = (255, 152, 183)    # haste clara da brânquia
ROSA_FORTE = (245, 67, 120)      # pente da brânquia
GUELRA_MAG = (224, 48, 106)      # magenta das pontas das brânquias (arte #e0306a)
GUELRA_CLARO = (248, 168, 192)   # miolo e filamentos das brânquias (arte #f8a8c0)
GUELRA_MIOLO = (252, 162, 192)   # miolo da brânquia (detalhe "Brânquias": (250,135,162)/(251,152,174))
GUELRA_BAIXO = (251, 106, 137)   # lado de baixo da haste
GUELRA_PONTA = (240, 52, 105)    # barbas rosa-choque e ponta (paleta (251,60,125); detalhe (226,35,81))
GUELRA_MEDIO = (251, 104, 137)   # barbas rosa-médio (251,106,137)
SOBRANCELHA = (226, 96, 138)    # capuz rosa-escuro por cima do olho
ROSA_MEDIO = (248, 150, 190)     # rêmiges e beirada de baixo da asa (detalhe "Plumagem Úmida": (250,157,202))
MAGENTA = (236, 42, 96)          # crista (229,34,88)/(241,45,104)
MAGENTA_ESC = (188, 16, 61)
CRISTA_TOPO = (240, 64, 108)     # topos da crista, um tom mais claro
AZUL_CEU = (69, 173, 239)        # cauda clara
AZUL_CLARO = (50, 140, 240)      # cauda média (43,143,242)
AZUL = (40, 99, 182)             # paleta
AZUL_ROYAL = (0, 58, 161)        # paleta
ESPIRAL = (47, 111, 208)         # detalhe "Plumagem Úmida": (44,113,202)/(58,131,228)
ESPIRAL_CLARO = (58, 131, 228)
CAUDA_BASE = (16, 64, 192)       # base e borda interna das lâminas
CAUDA_MEIO = (46, 112, 200)
CAUDA_PONTA = (126, 200, 248)
AMARELO = (248, 176, 0)          # bico (251,172,3) / pé (249,159,2)-(252,177,6)
AMARELO_CLARO = (253, 201, 42)   # alto do bico
LARANJA = (225, 132, 1)          # sombra do bico
PERNA_LADO = (240, 150, 4)       # lado da perna, um tom abaixo (249,159,2)
VERMELHO = (238, 48, 66)         # barbela
VERMELHO_ESC = (203, 15, 33)
ROXO = (90, 68, 103)             # dedos (detalhe "Patas Anfíbias": (90,68,103)/(101,77,114))
ROXO_CLARO = (101, 77, 114)
BRANCO = (252, 250, 248); PRETO = (20, 12, 22)
IRIS = (232, 160, 32)
ESCLERA = (255, 248, 240)
OLHO_AZUL = (53, 139, 225)       # moldura do olho (53,139,225)


# ---------------- luz em 2-3 tons chapados (claro em cima, base, sombra embaixo) ----------------
GANHO = 1.08   # a luz do jogo escurece os lados do modelo; a textura sai um pouco mais clara que a ficha

def tom(c, f):
    """Como g.tom, mas a sombra puxa para um tom mais fundo da MESMA cor (o rosa não vira malva/cinza)."""
    f = clamp(f, -1, 1)
    if f >= 0: r = mix(c, (255, 250, 244), f * .42)
    else: r = mix(c, (int(c[0] * .78), int(c[1] * .50), int(c[2] * .66)), -f * .9)
    return tuple(min(255, int(v * GANHO)) for v in r)

def luz3(c, borda=.07, cima=.20, baixo=-.36, alto=.06, fundo=-.09, faixa=None):
    """Luz chapada: face de cima clara, de baixo escura; nas faces dos lados, faixa de cima um tom mais claro e
    faixa de baixo um tom mais escuro (pela altura do bloco, ou da 'faixa' do grupo); fio escuro na borda."""
    f = c["face"]
    if f == "up": l = cima
    elif f == "down": l = baixo
    else:
        y0, y1 = faixa or (c["b"][0][1], c["b"][1][1])
        t = (c["p"][1] - y0) / max(y1 - y0, 1e-6)
        l = alto if t > .74 else fundo if t < .26 else 0.0
    if g.na_borda(c): l -= borda
    return l

def mat_bloco(cor_fn, **kw):
    """cor_fn(p, face) -> cor base (ou None); aplica a luz chapada."""
    def f(c):
        base = cor_fn(c["p"], c["face"])
        return None if base is None else tom(base, luz3(c, **kw))
    return f

def mat_liso(cor, **kw): return mat_bloco(lambda p, f: cor, **kw)

def mat_degrade(c0, c1, eixo, inverte=False, borda=.14):
    """Bloco de pena com degradê c0 -> c1 no comprimento (em 3 degraus, sem ruído), face de cima clara."""
    def f(c):
        lo, hi = c["b"][0][eixo], c["b"][1][eixo]
        t = clamp((c["p"][eixo] - lo) / max(hi - lo, 1e-6))
        if inverte: t = 1 - t
        t = round(t * 2) / 2
        l = .04
        if c["face"] == "up": l += .18
        if c["face"] == "down": l -= .32
        if g.na_borda(c): l -= borda
        return tom(mix(c0, c1, t), l)
    return f

def no_mundo(mat, ry, pivo):
    """Pinta uma peça girada em y com as coordenadas do MUNDO (a pintura normal usa as da peça sem girar)."""
    a = math.radians(ry); ca, sa = math.cos(a), math.sin(a)
    def f(c):
        x, y, z = (c["p"][i] - pivo[i] for i in range(3))
        c = dict(c); c["p"] = (pivo[0] + x * ca + z * sa, c["p"][1], pivo[2] - x * sa + z * ca)
        return mat(c)
    return f

def caixa(nome, de, ate, mat, **kw): return peca(nome, list(de), list(ate), mat, **kw)

def xs(lado, a, b):
    """Intervalo em x espelhado pelo lado (lado -1 = direita = x negativo)."""
    return sorted((a * lado, b * lado))


# ================= cabeça =================
CAB_X = 8.0          # meia largura da cabeça
CAB_ZF = -14.8       # frente do rosto
FRENTE_X = 3.4       # meia largura da frente reta (onde nasce o bico)
CAB_ZT = -3.8        # nuca
FAC_T = 1.8          # espessura das peças diagonais
OLHO_Y = 26.4        # centro do olho (na altura do alto do bico, como na ficha)
FAIXA_CAB = (20.6, 32.2)

def cor_cabeca(p, face):
    """Rosa-chiclete; o claro é só a bochecha embaixo do olho, em diagonal, e se funde no creme do pescoço."""
    x, y, z = p
    if face == "up": return ROSA_CLARO
    lim = 24.6 - 0.35 * max(0.0, z - (CAB_ZF + 3.0))          # a borda do claro desce para trás (sem corte reto)
    if y < lim and z < -6.0:
        return ROSA_PALIDO if y > 22.0 else CREME
    return ROSA_CLARO

def olho(u, v):
    """Olho neutro da arte (u ao longo da face, negativo = para o bico; v para cima):
    - a pálpebra é o próprio rosa da cabeça cortando o olho na diagonal (mais alta atrás, mais baixa no bico),
      sem linha escura de sobrancelha;
    - esclera branca quente; pupila preta GRANDE (~metade do olho) do lado do bico, na metade de baixo, com
      crescente âmbar embaixo e 1 px de brilho no canto de cima atrás;
    - azul só embaixo e atrás, em L (sem moldura fechada)."""
    lid = 1.0 + 0.32 * u
    if v >= lid or u < -2.6 or u >= 2.4 or v < -2.0: return None
    if v < -1.5 or u >= 1.9: return OLHO_AZUL
    if u < -0.5:
        if v < -1.1: return IRIS
        if v < 0.7:
            if -0.95 <= u and 0.25 <= v: return (255, 255, 255)
            return PRETO
    return ESCLERA

def mat_faceta_olho(fora, cz):
    base = mat_bloco(cor_cabeca, borda=0, faixa=FAIXA_CAB, alto=.04, fundo=-.06)
    def f(c):
        if c["face"] == fora:
            x, y, z = c["p"]
            r = olho(z - cz + 0.3, y - OLHO_Y)
            if r is not None: return r
        return base(c)
    return f

def camada_cabeca(nome, y0, y1, d, zt, mat, olhos=False, res=4):
    """Fatia octogonal da cabeça recuada 'd': frente reta, faces diagonais a 45° (o olho vai inteiro na
    diagonal, que aparece de frente e de lado como na ficha), laterais e nuca."""
    pcs = []
    zf, cx = CAB_ZF + d, CAB_X - d
    fx = FRENTE_X - 0.414 * d
    zs = CAB_ZF + (CAB_X - FRENTE_X) - 0.586 * d
    pcs.append(caixa(nome + "_frente", [-fx - 0.05, y0, zf], [fx + 0.05, y1, zs + 0.5], mat, res=res))
    pcs.append(caixa(nome + "_meio", [-cx, y0, zs - 0.4], [cx, y1, zt - 1.0], mat, res=res))
    pcs.append(caixa(nome + "_nuca", [-cx + 1.0, y0, zt - 1.2], [cx - 1.0, y1, zt], mat, res=res))
    L = (cx - fx) * math.sqrt(2) + 0.25
    for lado in (-1, 1):
        mx, mz = (fx + cx) / 2, (zf + zs) / 2
        pcx, pcz = (mx - 0.7071 * FAC_T / 2) * lado, mz + 0.7071 * FAC_T / 2
        fora = "east" if lado > 0 else "west"
        m = mat_faceta_olho(fora, pcz) if olhos else no_mundo(mat, 45 * lado, (pcx, 0, pcz))
        pcs.append(caixa(f"{nome}_diag_{'d' if lado < 0 else 'e'}", [pcx - FAC_T / 2, y0, pcz - L / 2], [pcx + FAC_T / 2, y1, pcz + L / 2],
                         m, rot=(0, 45 * lado, 0), pivo=(pcx, (y0 + y1) / 2, pcz), res=res))
    return pcs

def cor_bico(p, face):
    """Bico amarelo; uma narina escura em cada LADO, perto da base (nada no alto)."""
    x, y, z = p
    if face in ("east", "west") and abs(z - (CAB_ZF - 1.0)) < 0.3 and abs(y - 25.9) < 0.3: return (74, 26, 0)
    if face == "up": return AMARELO_CLARO
    if face == "down": return LARANJA
    return AMARELO

# ---------------- brânquias: penachos fofos ----------------
def guelra(nome, raiz, lado, L, recuo, eleva, curva=8, pula_baixo=0.0):
    """Brânquia de axolote como na ARTE: um penacho fofo e volumoso. Haste rosa-claro em 3 segmentos que
    afinam (2,8 -> 2,4 -> 2,0) e curvam 'curva' graus a cada segmento; dos dois lados, filamentos de 2 a 3 de
    comprimento (tão compridos quanto a haste é grossa), inclinados para fora e para a ponta, rosa-claro na raiz e
    magenta na ponta; no fim, um tufo cheio magenta com dois filamentos. 'pula_baixo': sem filamentos embaixo
    até essa distância (para a de baixo não encostar na asa). Osso externo sem rotação (é ele que balança na
    animação); o interno dá a direção."""
    x, y, z = raiz
    s = lado
    def ao_longo(a, b): return sorted((x + a * s, x + b * s))
    mh = mat_bloco(lambda p, f: GUELRA_CLARO, borda=.03, alto=.08, fundo=-.06)
    mt = mat_bloco(lambda p, f: GUELRA_MAG, borda=.05, alto=.1, fundo=-.06)
    def filamento(nome_f, a, r, sinal, cor_ponta=GUELRA_MAG):
        x0, x1 = ao_longo(a, a + 1.2)
        if sinal > 0: y0, y1 = y + r - 0.3, y + r + 2.3
        else: y0, y1 = y - r - 2.3, y - r + 0.3
        m = mat_degrade(GUELRA_CLARO, cor_ponta, 1, sinal < 0, borda=.06)
        return caixa(nome_f, [x0, y0, z - 0.65], [x1, y1, z + 0.65], m,
                     rot=(0, 0, -28 * s * sinal), pivo=(x + (a + 0.6) * s, y + sinal * r, z))
    segs = [(0.0, L / 3, 1.4), (L / 3, 2 * L / 3, 1.2), (2 * L / 3, L, 1.0)]
    def segmento(k):
        a0, a1, r = segs[k]
        pcs = []
        x0, x1 = ao_longo(a0 - (1.0 if k == 0 else 0.3), a1 + 0.3)
        pcs.append(caixa(f"{nome}_haste{k}", [x0, y - r, z - r], [x1, y + r, z + r], mh))
        a = a0 + 0.3 + (0.0 if k % 2 == 0 else 0.4)
        n = 0
        while a + 1.2 <= a1 + 0.2:
            pcs.append(filamento(f"{nome}_fc{k}_{n}", a, r, 1))
            if a + 0.8 >= pula_baixo:
                pcs.append(filamento(f"{nome}_fb{k}_{n}", a + 0.8, r, -1))
            a += 1.7; n += 1
        if k + 1 < len(segs): pcs.append(segmento(k + 1))
        else:   # tufo da ponta
            x0, x1 = ao_longo(L - 0.2, L + 2.4)
            pcs.append(caixa(f"{nome}_tufo", [x0, y - 1.3, z - 1.2], [x1, y + 1.3, z + 1.2], mt))
            for j, sinal in enumerate((1, -1)):
                x0, x1 = ao_longo(L + 1.4, L + 2.6)
                y0, y1 = (y + 1.0, y + 3.0) if sinal > 0 else (y - 3.0, y - 1.0)
                pcs.append(caixa(f"{nome}_tufo_f{j}", [x0, y0, z - 0.6], [x1, y1, z + 0.6], mt,
                                 rot=(0, 0, -35 * s * sinal), pivo=(x + (L + 2.0) * s, y + sinal * 1.0, z)))
        return osso(f"{nome}_s{k}", [x + a0 * s, y, z], [0, 0, (curva * s) if k > 0 else 0], pcs)
    dentro = osso(nome + "_dir", list(raiz), [0, -recuo * s, eleva * s], [segmento(0)])
    return osso(nome, list(raiz), [0, 0, 0], [dentro])

GUELRAS = [  # (y da raiz, z da raiz, comprimento, recuo, elevação, curva por segmento, sem filamento embaixo até)
    # leque da arte: saem da lateral entre o olho e a mandíbula; de lado a de cima sobe ~45°, a do meio ~5° e a de
    # baixo desce ~30° até a altura da barbela; de frente a de baixo emoldura o pescoço
    (28.0, -7.0, 10.5, 35, 44, 8, 0.0),
    (25.6, -6.8, 11.5, 45, 5, 4, 0.0),
    (23.2, -7.0, 9.5, 40, -29, -6, 5.0),
]

def anim_guelras():
    """Balanço das brânquias: cada uma oscila em z (sobe e desce) e um pouco em y, fora de fase."""
    parado, andando = {}, {}
    for lado, s_ in ((-1, "d"), (1, "e")):
        for k in range(len(GUELRAS)):
            fase = k * 2 * math.pi / 3 + (0.5 if lado > 0 else 0)
            def kf(a, b):
                q = [(0, round(b * math.cos(2 * math.pi * i / 4 + fase), 2), round(a * lado * math.sin(2 * math.pi * i / 4 + fase), 2))
                     for i in range(4)]
                return q + [q[0]]
            parado[f"guelra_{s_}_{k}"] = kf(6, 4)
            andando[f"guelra_{s_}_{k}"] = kf(11, 6)
    return parado, andando

ANIM_PARADO, ANIM_ANDANDO = anim_guelras()


# ================= cauda: foices =================
def pena_cauda(nome, base, segs, rot0, curva, mat_fn, sobrepoe=1.0):
    """Cadeia de blocos (eixo y; curva = rotação em x de cada junta); cada segmento começa 'sobrepoe' antes do
    fim do anterior, e a foice curva sem abrir fresta. Ossos '<nome>_0', '<nome>_1'..."""
    def seg(k, pos):
        L, w, h, c0, c1 = segs[k]
        px, py, pz = pos
        filhos = [caixa(f"{nome}_{k}", [px - w / 2, py, pz - h / 2], [px + w / 2, py + L, pz + h / 2], mat_fn(c0, c1))]
        if k + 1 < len(segs): filhos.append(seg(k + 1, (px, py + L - sobrepoe, pz)))
        return osso(f"{nome}_{k}", list(pos), list(rot0) if k == 0 else [curva[k - 1], 0, 0], filhos)
    return seg(0, tuple(base))

def mat_foice(c0, c1):
    """Foice com degradê da arte: base e borda de dentro azul-royal, ponta e borda de fora azul-céu."""
    def f(c):
        lo, hi = c["b"][0][1], c["b"][1][1]
        t = clamp((c["p"][1] - lo) / max(hi - lo, 1e-6))
        cor = mix(c0, c1, round(t * 2) / 2)
        l = .04
        if c["face"] in ("east", "west"):
            z0, z1 = c["b"][0][2], c["b"][1][2]
            d = (c["p"][2] - z0) / max(z1 - z0, 1e-6)       # z- = borda de fora/de cima da foice
            if d < .35: cor = mix(cor, CAUDA_PONTA, .5)
            elif d > .7: cor = mix(cor, CAUDA_BASE, .45)
        elif c["face"] == "up": l = .14
        elif c["face"] == "down": l = -.25
        if g.na_borda(c): l -= .05
        return tom(cor, l)
    return f

FOICES = [  # (x, rx inicial, curva de cada junta, comprimentos, largura da faixa, cor raiz, cor ponta, y da raiz)
    # 6 foices largas e finas que sobem da traseira, curvam para trás e para baixo e terminam com a ponta para
    # baixo; a mais baixa chega ao joelho. De trás formam um bloco largo (~1/3 do corpo).
    (0.0, 12, (32, 34, 32), (5.8, 5.6, 5.0, 4.4), 4.8, CAUDA_BASE, CAUDA_PONTA, 18.4),
    (1.7, 45, (26, 28, 26), (5.6, 5.4, 5.0, 4.4), 4.8, CAUDA_BASE, CAUDA_PONTA, 17.0),
    (-1.7, 70, (22, 24, 22), (5.4, 5.2, 4.8, 4.2), 4.6, CAUDA_BASE, CAUDA_PONTA, 16.2),
    (0.9, 95, (18, 20), (5.2, 5.0, 4.4), 4.4, CAUDA_BASE, CAUDA_PONTA, 15.4),
    (-0.9, 120, (14, 14), (5.0, 4.6, 4.0), 4.2, CAUDA_BASE, CAUDA_PONTA, 14.6),
    (0.0, 145, (10, 10), (4.6, 4.2, 3.6), 4.0, CAUDA_BASE, CAUDA_PONTA, 13.8),
]
ONDAS = [(f"cauda_p{k}", len(f[3]), (2.5, 1.5, 0)) for k, f in enumerate(FOICES)]


# ================= corpo =================
def cor_corpo(p, face):
    x, y, z = p
    if z < -8.4 and abs(x) < 6.0: return CREME
    return ROSA_CLARO

def espiral(a, b, ka=0.9, kb=0.85, t=0.66):
    """Espiral da asa como na ARTE e no quadro 'Plumagem Úmida': quadrada, de traço grosso, 2 voltas, miolo em
    gancho na frente e uma cauda longa que corre por baixo para a frente e sobe em diagonal.
    a = para a frente (bico), b = para cima."""
    a, b = a / ka, b / kb
    P = [(0.7, 0.0), (-1.1, 0.0), (-1.1, -2.2), (2.2, -2.2), (2.2, 2.2), (-3.3, 2.2), (-3.3, -4.4), (4.4, -4.4), (6.2, -1.2)]
    for (a0, b0), (a1, b1) in zip(P, P[1:]):
        da, db = a1 - a0, b1 - b0
        tt = clamp(((a - a0) * da + (b - b0) * db) / (da * da + db * db))
        if max(abs(a - a0 - tt * da), abs(b - b0 - tt * db)) < t: return True
    return False


def montar():
    # ================= cabeça (bloco, octogonal em planta) =================
    cab = []
    mc = mat_bloco(cor_cabeca, borda=0, faixa=FAIXA_CAB, alto=.04, fundo=-.06)
    cab += camada_cabeca("queixo", 20.6, 22.2, 0.6, CAB_ZT - 0.6, mc)
    cab += camada_cabeca("cranio", 22.1, 29.7, 0.0, CAB_ZT, mc, olhos=True)
    cab += camada_cabeca("testa", 29.6, 31.6, 0.8, CAB_ZT - 0.4, mc)
    # bico em cunha que afina em degraus até a ponta (base 4x3, ponta 2x2, comprimento ~4) e mandíbula recuada
    mb = mat_bloco(cor_bico, borda=.04, alto=.06, fundo=-.1)
    cab.append(caixa("bico", [-2.0, 24.0, CAB_ZF - 1.8], [2.0, 27.0, CAB_ZF + 0.4], mb))
    cab.append(caixa("bico_meio", [-1.6, 24.3, CAB_ZF - 3.0], [1.6, 26.6, CAB_ZF - 1.6], mb))
    cab.append(caixa("bico_ponta", [-1.0, 24.4, CAB_ZF - 4.0], [1.0, 26.2, CAB_ZF - 2.8], mb))
    cab.append(caixa("bico_baixo", [-1.5, 23.2, CAB_ZF - 2.0], [1.5, 24.2, CAB_ZF + 0.4], mb))
    # barbela: dois lobos longos e pendentes (~1,5x a altura do bico), um pouco afastados embaixo, com o lado de
    # dentro mais escuro
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        dentro = "west" if lado > 0 else "east"
        mbar = mat_bloco(lambda p, f, dentro=dentro: VERMELHO_ESC if f == dentro else VERMELHO, borda=.06, alto=.05, fundo=-.2)
        x0, x1 = xs(lado, 0.3, 2.3)
        lob = [caixa("barbela_" + s_, [x0, 18.0, CAB_ZF - 1.6], [x1, 23.2, CAB_ZF + 0.4], mbar)]
        x0, x1 = xs(lado, 0.6, 2.0)
        lob.append(caixa("barbela_ponta_" + s_, [x0, 17.0, CAB_ZF - 1.3], [x1, 18.2, CAB_ZF + 0.1], mbar))
        cab.append(osso("barbela_" + s_, [1.3 * lado, 23.2, CAB_ZF - 0.6], [0, 0, 5 * lado], lob))
    # crista só no alto (nada na face): 3 lobos que crescem para trás (o da frente pequeno, na borda da testa; o do
    # meio o mais alto) e desce um pouco pela nuca
    mcr = mat_bloco(lambda p, f: CRISTA_TOPO if f == "up" else MAGENTA, borda=.06, alto=.1, fundo=-.14)
    crista = []
    for k, (z0, z1, y0, y1, w) in enumerate([(-14.0, -11.2, 31.2, 34.4, 1.7), (-11.6, -7.8, 31.2, 37.6, 2.0),
                                             (-8.2, -4.8, 31.2, 36.4, 1.9), (-5.2, -2.6, 29.2, 33.6, 1.6)]):
        crista.append(caixa(f"crista_{k}", [-w, y0, z0], [w, y1, z1], mcr))
    crista.append(caixa("crista_topo1", [-1.2, 37.2, -10.8], [1.2, 38.4, -8.4], mcr))
    for lado in (-1, 1):
        for k, (z0, z1, y1) in enumerate([(-12.0, -8.4, 35.2), (-8.6, -5.4, 34.4)]):
            x0, x1 = xs(lado, 1.6, 3.6)
            crista.append(caixa(f"crista_lado{k}_" + ("d" if lado < 0 else "e"), [x0, 31.2, z0], [x1, y1, z1], mcr))
    cab.append(osso("crista", [0, 32, -7.8], [0, 0, 0], crista))
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        for k, (y0, z0, L, rec, ele, cv, pb) in enumerate(GUELRAS):
            cab.append(guelra(f"guelra_{s_}_{k}", (7.4 * lado, y0, z0), lado, L, rec, ele, cv, pb))
    cabeca = osso("cabeca", [0, 22, -8.8], [0, 0, 0], cab)

    # ================= pescoço: o creme sobe afunilando até a mandíbula =================
    pescoco = osso("pescoco", [0, 19, -9], [0, 0, 0], [
        caixa("pescoco", [-4.4, 17.0, -12.4], [4.4, 22.0, -6.0], mat_liso(CREME), res=2), cabeca])

    # ================= tronco: ovo redondo, mais largo embaixo (sino) =================
    corpo = []
    mt = mat_bloco(cor_corpo, faixa=(7.0, 21.0), borda=.03)
    corpo += g.arredondado2("barriga", [-8.2, 8.2, -9.8], [8.2, 15.8, 6.4], mt, r=2.8, res=2)
    corpo += g.arredondado2("tronco", [-6.8, 12.6, -10.8], [6.8, 20.4, 7.2], mt, r=3.0, res=2)
    corpo += g.arredondado("rabadilha", [-5.2, 11.0, 5.0], [5.2, 19.4, 10.6], mt, r=1.6, res=2)
    # peito: telhas de pena desencontradas (meia telha por fileira) em V; de perfil o peito estufa no meio e
    # recolhe em curva até a barriga
    def mat_telha():
        def f(c):
            y0, y1 = c["b"][0][1], c["b"][1][1]
            t = (c["p"][1] - y0) / max(y1 - y0, 1e-6)
            cor = CREME_SOMBRA if (t < .3 and c["face"] != "up") else CREME
            l = .1 if c["face"] == "up" else -.25 if c["face"] == "down" else 0.0
            return tom(cor, l)
        return f
    mp = mat_telha()
    FILAS = [(20.8, 3.4), (18.6, 5.0), (16.4, 6.0), (14.2, 6.4), (12.0, 5.6), (9.8, 4.2), (7.8, 2.2)]   # (alto, meia largura)
    for k, (ya, w) in enumerate(FILAS):
        yb = ya - 2.4
        ym = (ya + yb) / 2
        zf = -10.6 - 2.8 * math.sin(math.pi * clamp((ym - 7.0) / 13.6))
        n = max(1, round(2 * w / 2.8))
        larg = 2 * w / n
        desloc = (larg / 2) if k % 2 else 0.0
        for i in range(n + (1 if k % 2 else 0)):
            x0 = -w + i * larg - desloc
            x1 = x0 + larg
            x0, x1 = max(x0, -w), min(x1, w)
            if x1 - x0 < 0.8: continue
            corpo.append(caixa(f"peito_{k}_{i}", [x0 + 0.05, yb, zf], [x1 - 0.05, ya, zf + 3.0], mp, res=2,
                               rot=(14, 0, 0), pivo=((x0 + x1) / 2, ya, zf + 1.5)))

    # ================= asas: escudo oval colado ao corpo, com a espiral, e primárias em escada =================
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        fora = "east" if lado > 0 else "west"
        def cor_asa(p, face, fora=fora):
            x, y, z = p
            if face == fora and espiral(-(z - 0.2), y - 14.8): return ESPIRAL
            if face == "north" and abs(x) > 9.2 and 13.4 < y < 14.4: return ESPIRAL      # a espiral vista de frente
            return ROSA_CLARO
        ma = mat_bloco(lambda p, f, ca=cor_asa: ca(p, f), borda=.03, alto=.1, fundo=-.1)
        mpr = mat_bloco(lambda p, f: ROSA_CLARO, borda=.03, alto=.1, fundo=-.12)
        x0, x1 = xs(lado, 7.4, 10.4)
        escudo = g.arredondado2("asa_" + s_, [x0, 10.0, -7.0], [x1, 17.8, 4.6], ma, r=1.0, res=4)
        esc = osso("asa_escudo_" + s_, [8.9 * lado, 17.8, -7.0], [-6, 0, 0], escudo)          # borda de cima sobe para trás
        prim = []
        for k, (y0, y1, z1) in enumerate([(14.6, 17.8, 11.0), (13.0, 16.2, 9.0), (11.4, 14.6, 7.0)]):
            x0, x1 = xs(lado, 7.6, 10.0 - 0.2 * k)
            prim.append(caixa(f"asa_primaria{k}_" + s_, [x0, y0, 2.0], [x1, y1, z1], mpr, res=4))
        pri = osso("asa_primarias_" + s_, [8.8 * lado, 16.0, 2.0], [15, 0, 0], prim)              # descem para trás
        corpo.append(osso("asa_" + s_, [8.0 * lado, 18.0, -6.0], [0, -4 * lado, 8 * lado], [esc, pri]))

    # ================= cauda: foices =================
    cauda = []
    BASE = (0.0, 16.0, 9.0)
    for k, (x, rx0, cv, Ls, h, c0, c1, yb) in enumerate(FOICES):
        n = len(Ls)
        segs = [(L, 1.8, h - 0.4 * i, mix(c0, c1, i / n), mix(c0, c1, (i + 0.7) / n)) for i, L in enumerate(Ls)]
        cauda.append(pena_cauda(f"cauda_p{k}", (BASE[0] + x, yb, BASE[2] - 0.3 * k), segs, (rx0, 0, 0), cv,
                                mat_foice, sobrepoe=1.0))
    corpo.append(osso("cauda", list(BASE), [0, 0, 0], cauda))

    corpo.append(pescoco)
    raiz = osso("corpo", [0, 9, 0], [0, 0, 0], corpo)

    # ================= pernas e patas anfíbias =================
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 4.6 * lado; zc = -0.6
        pp = []
        ml = mat_bloco(lambda p, f: PERNA_LADO if f in ("east", "west") else AMARELO, borda=.06, alto=.0, fundo=-.06)
        pp.append(caixa("perna_" + s, [xc - 2.5, 2.2, zc - 2.5], [xc + 2.5, 9.6, zc + 2.5], ml))
        pp.append(caixa("pe_" + s, [xc - 4.3, 1.0, zc - 5.2], [xc + 4.3, 4.1, zc + 2.8], ml))
        mg = mat_bloco(lambda p, f: ROXO_CLARO if f == "up" else ROXO, borda=.1, alto=.0, fundo=.0)
        for k, dx in enumerate((-3.0, 0.0, 3.0)):
            pp.append(caixa(f"dedo_{k}_{s}", [xc + dx - 1.3, 0.0, zc - 9.2], [xc + dx + 1.3, 3.3, zc - 4.4], mg,
                            rot=(0, -14 * (dx / 3.0), 0), pivo=(xc + dx, 1.4, zc - 4.4)))
        pp.append(caixa("dedo_tras_" + s, [xc - 1.2, 0.0, zc + 2.4], [xc + 1.2, 2.6, zc + 5.2], mg))
        return osso("perna_" + s, [xc, 8.5, zc], [0, 0, 0], pp)

    return [raiz, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
