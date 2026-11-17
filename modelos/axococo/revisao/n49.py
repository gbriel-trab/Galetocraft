"""Axococó (#008, Água): o galo-axolote das águas. Cabeça grande em bloco rosa-claro com olhos bravos de aro azul,
bico amarelo largo e barbela em dois lóbulos; três brânquias de axolote em degrau de cada lado; crista aquática
magenta em blocos; corpo em ovo deitado com peito creme em fileiras de penas; asas com a espiral azul quadrada da
'Plumagem Úmida'; leque de foices azuis grossas na cauda; pernas amarelas e patas anfíbias de dedos roxo-cinza.
Refeito do zero (rodadas n*) seguindo as 4 vistas da ficha: blocos grossos, 2-3 tons chapados por bloco."""
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
CREME = (252, 224, 210)          # creme-pêssego (252,227,211)          # peito (252,215,200) / paleta (252,227,211)
CREME_SOMBRA = (246, 189, 178)
ROSA_PALIDO = (252, 214, 212)    # bochecha (252,205,202)-(252,224,216)
ROSA_CLARO = (251, 176, 204)     # cabeça (251,173,195), asa (250,181,209), paleta (253,173,212)
ROSA_LUZ = (253, 212, 228)       # brilho da asa (253,219,234)
ROSA = (252, 120, 161)           # brânquia
ROSA_GUELRA = (255, 152, 183)    # haste clara da brânquia
ROSA_FORTE = (245, 67, 120)      # pente da brânquia
GUELRA_MAG = (230, 58, 109)
GUELRA_MIOLO = (252, 162, 192)   # miolo da brânquia (detalhe "Brânquias": (250,135,162)/(251,152,174))
GUELRA_BAIXO = (251, 106, 137)   # lado de baixo da haste
GUELRA_PONTA = (240, 52, 105)    # barbas rosa-choque e ponta (paleta (251,60,125); detalhe (226,35,81))
GUELRA_MEDIO = (251, 104, 137)   # barbas rosa-médio (251,106,137)
SOBRANCELHA = (236, 112, 152)    # capuz rosa-escuro por cima do olho
ROSA_MEDIO = (248, 150, 190)     # rêmiges e beirada de baixo da asa (detalhe "Plumagem Úmida": (250,157,202))
MAGENTA = (236, 42, 96)          # crista (229,34,88)/(241,45,104)
MAGENTA_ESC = (188, 16, 61)
CRISTA_TOPO = (240, 64, 108)     # topos da crista, um tom mais claro
AZUL_CEU = (69, 173, 239)        # cauda clara
AZUL_CLARO = (50, 140, 240)      # cauda média (43,143,242)
AZUL = (40, 99, 182)             # paleta
AZUL_ROYAL = (0, 58, 161)        # paleta
ESPIRAL = (44, 113, 202)         # detalhe "Plumagem Úmida": (44,113,202)/(58,131,228)
ESPIRAL_CLARO = (58, 131, 228)
CAUDA_BASE = (24, 64, 160)       # base e borda interna das lâminas
CAUDA_MEIO = (46, 112, 200)
CAUDA_PONTA = (90, 176, 240)
AMARELO = (251, 172, 3)          # bico (251,172,3) / pé (249,159,2)-(252,177,6)
AMARELO_CLARO = (253, 201, 42)   # alto do bico
LARANJA = (225, 132, 1)          # sombra do bico
PERNA_LADO = (240, 150, 4)       # lado da perna, um tom abaixo (249,159,2)
VERMELHO = (238, 48, 66)         # barbela
VERMELHO_ESC = (203, 15, 33)
ROXO = (90, 68, 103)             # dedos (detalhe "Patas Anfíbias": (90,68,103)/(101,77,114))
ROXO_CLARO = (101, 77, 114)
BRANCO = (252, 250, 248); PRETO = (20, 12, 22)
IRIS = (232, 160, 32)
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
    """Rosa-claro; bochecha e garganta mais claras (quase creme) embaixo do olho."""
    x, y, z = p
    if face == "up": return ROSA_CLARO
    if y < 25.0 and z < -6.8: return ROSA_PALIDO if y > 22.2 else CREME          # bochecha clara embaixo do olho
    return ROSA_CLARO

def olho(u, v):
    """Olho neutro da ficha (u ao longo da face, negativo = para o bico; v para cima):
    - capuz rosa-escuro (sobrancelha) logo acima da linha da pálpebra, que desce em diagonal para o bico;
    - branco puro, menor; pupila preta GRANDE (~45% da largura, ~60% da altura) encostada na pálpebra e no lado
      do bico, com 1 px de brilho no canto de cima; aro âmbar só na fileira de baixo da pupila;
    - moldura azul grossa atrás e embaixo."""
    lid = 0.75 + 0.30 * u                                  # linha da pálpebra
    if lid <= v < lid + 0.6 and -2.6 <= u < 2.9: return SOBRANCELHA
    if v >= lid: return None
    if -2.0 <= u < 1.5 and -1.3 <= v:
        if -2.0 <= u < -0.45 and -0.85 <= v:
            if -1.95 <= u < -1.65 and lid - 0.45 <= v < lid - 0.15: return (255, 255, 255)   # brilho de 1 px
            return PRETO
        if -2.0 <= u < -0.45 and -1.2 <= v < -0.85: return IRIS
        return (255, 255, 255)
    if -2.2 <= u < 2.4 and -2.1 <= v: return OLHO_AZUL
    return None

def mat_faceta_olho(fora, cz):
    base = mat_bloco(cor_cabeca, borda=0, faixa=FAIXA_CAB, alto=.04, fundo=-.08)
    def f(c):
        if c["face"] == fora:
            x, y, z = c["p"]
            r = olho(z - cz + 0.3, y - OLHO_Y)      # olho encostado na quina do bico, como na ficha
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
    x, y, z = p
    if face == "up" and abs(z - (CAB_ZF - 1.3)) < 0.3 and abs(abs(x) - 1.1) < 0.3: return (74, 26, 0)   # narina no alto
    if face == "up": return AMARELO_CLARO
    if face == "down": return LARANJA
    return AMARELO

# ---------------- brânquias ----------------
def guelra(nome, raiz, lado, L, recuo, eleva):
    """Brânquia de axolote como a 'Brânquias' da ficha: uma pena larga e felpuda. Haste rosa-claro em 3 degraus que
    afinam para fora e, dos dois lados, uma franja CONTÍNUA de barbas de 2 de comprimento inclinadas para a
    ponta, alternando rosa-médio e rosa-choque e deslocadas em escada (as de baixo meio passo adiante).
    Ponta rombuda em degrau rosa-choque. Osso externo sem rotação (é ele que balança na animação); o interno dá
    a direção."""
    x, y, z = raiz
    s = lado
    pcs = []
    def ao_longo(a, b): return sorted((x + a * s, x + b * s))     # ao longo da brânquia, a partir da raiz
    mh = mat_bloco(lambda p, f: GUELRA_MIOLO, borda=.05, alto=.08, fundo=-.05)
    mm = mat_bloco(lambda p, f: GUELRA_MEDIO, borda=.08, alto=.08, fundo=-.06)
    mx = mat_bloco(lambda p, f: GUELRA_PONTA, borda=.08, alto=.08, fundo=-.06)
    degraus = [(-1.0, 0.45 * L, 0.85, 1.1), (0.43 * L, 0.78 * L, 0.7, 0.95), (0.76 * L, L, 0.55, 0.8)]
    for k, (a, b, r, d) in enumerate(degraus):
        x0, x1 = ao_longo(a, b)
        pcs.append(caixa(f"{nome}_haste{k}", [x0, y - r, z - d], [x1, y + r, z + d], mh))
    def raio(a): return next((r for aa, bb, r, d in degraus if aa <= a <= bb), 0.55)
    n = max(2, int((L - 0.4) / 1.8))
    for k in range(n):
        for lado_f in (1, -1):
            a = 0.4 + 1.8 * k + (0.9 if lado_f < 0 else 0.0)
            if a + 1.0 > L: continue
            r = raio(a + 1.0)
            cor = mm if (k + (lado_f < 0)) % 2 == 0 else mx
            x0, x1 = ao_longo(a, a + 2.0)
            y0, y1 = (y + r - 0.2, y + r + 0.9) if lado_f > 0 else (y - r - 0.9, y - r + 0.2)
            xb = x + (a + 1.0) * s
            pcs.append(caixa(f"{nome}_barba{'c' if lado_f > 0 else 'b'}{k}", [x0, y0, z - 0.85], [x1, y1, z + 0.85], cor,
                             rot=(0, 0, -22 * s * lado_f), pivo=(xb, y + lado_f * r, z)))
    x0, x1 = ao_longo(L - 0.2, L + 1.0)
    pcs.append(caixa(nome + "_ponta", [x0, y - 0.75, z - 0.75], [x1, y + 0.75, z + 0.75], mx))
    x0, x1 = ao_longo(L + 0.9, L + 1.7)
    pcs.append(caixa(nome + "_ponta2", [x0, y - 0.45, z - 0.5], [x1, y + 0.45, z + 0.5], mx))
    dentro = osso(nome + "_dir", list(raiz), [0, -recuo * s, eleva * s], pcs)
    return osso(nome, list(raiz), [0, 0, 0], [dentro])

GUELRAS = [  # (y da raiz, z da raiz, comprimento, recuo (graus para trás), elevação (graus para cima))
    # leque compacto: raízes atrás da bochecha, da altura da sobrancelha até o canto do bico, quase encostadas
    (28.4, -7.6, 10.0, 50, 30),
    (26.0, -7.4, 11.0, 48, 3),
    (23.8, -7.6, 8.5, 46, -15),
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


# ================= cauda =================
def pena_cauda(nome, base, segs, rot0, curva, mat_fn, sobrepoe=1.0):
    """Cadeia de blocos (eixo y; curva = rotação em x de cada junta) em que cada segmento começa 'sobrepoe' antes do fim do anterior: a foice
    grossa curva sem abrir fresta. Ossos '<nome>_0', '<nome>_1'..."""
    def seg(k, pos):
        L, w, h, c0, c1 = segs[k]
        px, py, pz = pos
        filhos = [caixa(f"{nome}_{k}", [px - w / 2, py, pz - h / 2], [px + w / 2, py + L, pz + h / 2], mat_fn(c0, c1))]
        if k + 1 < len(segs): filhos.append(seg(k + 1, (px, py + L - sobrepoe, pz)))
        return osso(f"{nome}_{k}", list(pos), list(rot0) if k == 0 else [curva[k - 1], 0, 0], filhos)
    return seg(0, tuple(base))

def mat_foice(c0, c1):
    """Segmento da foice: degradê em 2 tons ao longo dele, beirada de fora (z+) um tom mais escuro."""
    def f(c):
        lo, hi = c["b"][0][1], c["b"][1][1]
        t = clamp((c["p"][1] - lo) / max(hi - lo, 1e-6))
        cor = c0 if t < .5 else c1
        l = .04
        if c["face"] in ("east", "west"):
            z0, z1 = c["b"][0][2], c["b"][1][2]
            d = (c["p"][2] - z0) / max(z1 - z0, 1e-6)
            l = .12 if d < .3 else -.12 if d > .72 else .02
        elif c["face"] == "up": l = .14
        elif c["face"] == "down": l = -.3
        if g.na_borda(c): l -= .12
        return tom(cor, l)
    return f

FOICES = [  # (x, rx inicial, curva de cada junta, comprimentos, largura da faixa, cor raiz, cor ponta, y da raiz)
    # 5 foices largas e chatas (faixa ~2,5x a espessura) no MESMO plano vertical (de trás é uma coluna só),
    # com as raízes sobrepostas; a de cima passa acima das costas e cai de leve na ponta, sem gancho.
    (0.15, 25, (16, 16, 16, 14), (5.4, 5.2, 5.0, 4.6, 4.0), 6.2, AZUL_ROYAL, AZUL_CEU, 19.0),
    (-0.15, 55, (13, 13, 13, 12), (5.6, 5.4, 5.2, 4.8, 4.0), 6.2, AZUL_ROYAL, AZUL_CEU, 18.0),
    (0.15, 80, (11, 11, 11), (5.4, 5.2, 5.0, 4.4), 6.0, AZUL_ROYAL, AZUL_CEU, 17.0),
    (-0.15, 105, (9, 9, 9), (5.2, 5.0, 4.6, 4.0), 5.8, AZUL, AZUL_CEU, 16.0),
    (0.15, 130, (6, 6), (5.0, 4.6, 4.0), 5.4, AZUL, AZUL_CEU, 15.0),
]
ONDAS = [(f"cauda_p{k}", len(f[3]), (2.5, 1.5, 0)) for k, f in enumerate(FOICES)]


# ================= corpo =================
def cor_corpo(p, face):
    x, y, z = p
    if z < -9.0 and abs(x) < 6.0: return CREME
    if y < 9.0: return mix(ROSA_CLARO, CREME, .5)
    return ROSA_CLARO

def espiral(a, b, k=1.0, t=0.8):
    """Espiral da 'Plumagem Úmida', medida no quadro da ficha: anel oitavado (cantos cortados em degrau, sem
    canto reto), traço grosso, uma barra interna que entra até o miolo (como um "e"/"@") e uma cauda que sai do
    fundo do anel, corre para a frente e para baixo e sobe na ponta. a = para a frente (bico), b = para cima."""
    a, b = a / k, b / k
    ra, rb = 3.4, 2.6
    def oito(a, b): return max(abs(a) / ra, abs(b) / rb, (abs(a) / ra + abs(b) / rb) / 1.45)
    m = oito(a, b)
    if 1 - t / rb <= m <= 1.0 and not (a > 0.8 and -0.9 < b < 0.6): return True      # anel, aberto na frente
    def seg(a0, b0, a1, b1, w=t):
        da, db = a1 - a0, b1 - b0
        tt = clamp(((a - a0) * da + (b - b0) * db) / (da * da + db * db))
        return math.hypot(a - a0 - tt * da, b - b0 - tt * db) < w
    if seg(2.9, 0.6, 0.4, 0.4) or seg(0.4, 0.4, 0.1, -0.6): return True                 # barra do "e" até o miolo
    if seg(0.6, -rb + 0.3, 3.6, -3.6) or seg(3.6, -3.6, 5.4, -3.4) or seg(5.4, -3.4, 6.4, -1.4): return True   # cauda
    return False


def montar():
    # ================= cabeça (bloco grande, octogonal em planta) =================
    cab = []
    mc = mat_bloco(cor_cabeca, borda=0, faixa=FAIXA_CAB, alto=.04, fundo=-.08)        # sem fio claro nas emendas
    cab += camada_cabeca("queixo", 20.6, 22.2, 0.6, CAB_ZT - 0.6, mc)
    cab += camada_cabeca("cranio", 22.1, 29.7, 0.0, CAB_ZT, mc, olhos=True)
    cab += camada_cabeca("testa", 29.6, 31.6, 0.8, CAB_ZT - 0.4, mc)    # alto liso, sem plaquinhas em volta da crista
    # bico em cunha (como na ficha): de frente é um pentágono, largo em cima e estreito embaixo; de lado afina
    # para a ponta, com um gancho curto um pouco mais baixo. O alto do bico fica na altura do meio do olho.
    mb = mat_bloco(cor_bico, borda=.08, alto=.06, fundo=-.12)
    # cunha simples: de lado, maxila reta com uma só quebra para a ponta quadrada; de frente, trapézio largo em
    # cima (~1/3 da cabeça) que afina embaixo e para logo acima das barbelas
    # a maxila é UMA peça inclinada 13° (o alto desce em rampa da testa até a ponta, que fica embaixo); a
    # mandíbula, mais estreita, faz o trapézio de frente
    cab.append(caixa("bico", [-2.3, 24.0, CAB_ZF - 4.8], [2.3, 26.4, CAB_ZF + 0.4], mb, rot=(-13, 0, 0),
                     pivo=(0, 26.4, CAB_ZF + 0.4)))
    cab.append(caixa("bico_baixo", [-1.6, 22.6, CAB_ZF - 3.2], [1.6, 24.4, CAB_ZF + 0.4], mb))
    # barbela: dois lóbulos separados por uma fresta, presos nas beiradas de baixo do bico e abrindo para fora
    mbar = mat_bloco(lambda p, f: VERMELHO, borda=.12, alto=.05, fundo=-.25)
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        x0, x1 = xs(lado, 0.25, 2.3)
        xm = 1.3 * lado
        lob = [caixa("barbela_" + s_, [x0, 19.8, CAB_ZF - 2.2], [x1, 22.7, CAB_ZF + 0.6], mbar)]
        x0, x1 = xs(lado, 0.5, 2.0)
        lob.append(caixa("barbela_ponta_" + s_, [x0, 19.0, CAB_ZF - 1.9], [x1, 20.0, CAB_ZF + 0.3], mbar))
        cab.append(osso("barbela_" + s_, [xm, 22.6, CAB_ZF - 0.8], [0, 0, 4 * lado], lob))
    # crista aquática em moicano: coluna central estreita (~1/4 da cabeça) em 4 degraus (o mais alto no meio,
    # a ponta de trás descendo até a nuca) e dois blocos laterais mais baixos (~2/3 da altura)
    mcr = mat_bloco(lambda p, f: CRISTA_TOPO if f == "up" else MAGENTA, borda=.1, alto=.1, fundo=-.16)
    crista = []
    # coluna central em degraus da testa (bloco que cai um pouco sobre ela) até a nuca; o mais alto no meio-frente
    for k, (z0, z1, y0, y1) in enumerate([(-16.0, -12.8, 30.4, 35.2), (-13.0, -9.8, 31.0, 38.8), (-10.0, -6.8, 31.0, 37.8),
                                          (-7.0, -4.0, 31.0, 36.2), (-4.2, -2.4, 30.6, 34.2)]):
        crista.append(caixa(f"crista_{k}", [-1.9, y0, z0], [1.9, y1, z1], mcr))
    # colunas laterais a ~80% da central (coroa de 3 pontas de frente)
    for lado in (-1, 1):
        for k, (z0, z1, y1) in enumerate([(-14.0, -9.6, 37.0), (-9.8, -5.6, 35.8)]):
            x0, x1 = xs(lado, 1.8, 4.0)
            crista.append(caixa(f"crista_lado{k}_" + ("d" if lado < 0 else "e"), [x0, 31.0, z0], [x1, y1, z1], mcr))
    cab.append(osso("crista", [0, 32, -7.8], [0, 0, 0], crista))
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        for k, (y0, z0, L, rec, ele) in enumerate(GUELRAS):
            cab.append(guelra(f"guelra_{s_}_{k}", (7.6 * lado, y0, z0), lado, L, rec, ele))
    cabeca = osso("cabeca", [0, 22, -8.8], [0, 0, 0], cab)

    # ================= pescoço curto (a cabeça assenta no peito) =================
    pescoco = osso("pescoco", [0, 19, -9], [0, 0, 0], [
        caixa("pescoco", [-5.4, 17.0, -12.8], [5.4, 21.4, -5.0], mat_liso(CREME), res=2), cabeca])

    # ================= tronco: ovo deitado =================
    corpo = []
    mt = mat_bloco(cor_corpo, faixa=(7.0, 21.0))
    corpo += g.arredondado2("tronco", [-7.6, 7.4, -12.6], [7.6, 20.6, 8.6], mt, r=3.6, res=2)
    corpo += g.arredondado("rabadilha", [-5.6, 11.6, 6.0], [5.6, 20.8, 12.0], mt, r=1.6, res=2)
    # peito creme em fileiras de penas grossas (cada fileira avança sobre a de baixo; a do meio desce mais)
    mp = mat_bloco(lambda p, f: CREME, borda=.06, alto=.05, fundo=-.12)     # separação sutil entre as fileiras
    FILAS = [(20.8, 17.6, 6.2, -14.0), (17.8, 14.8, 6.4, -14.2), (15.0, 12.0, 5.8, -13.6), (12.2, 9.4, 4.6, -12.4),
             (9.6, 7.8, 3.0, -10.4)]
    for k, (ya, yb, w, zf) in enumerate(FILAS):     # cada fileira: lados mais curtos, meio, e a ponta do "V" no centro
        corpo.append(caixa(f"peito_{k}", [-w, yb + 0.6, zf], [w, ya, zf + 5.0], mp, res=2))
        corpo.append(caixa(f"peito_{k}_ponta", [-w * 0.45, yb - (1.0 if k == len(FILAS) - 1 else 0.5), zf - 0.3],
                           [w * 0.45, ya - 0.6, zf + 4.0], mp, res=2))

    # ================= asas em gota, encostadas no corpo =================
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        fora = "east" if lado > 0 else "west"
        def cor_asa(p, face, fora=fora, ponta=None):
            x, y, z = p
            if face == fora and espiral(-(z - 1.0), y - 15.2): return ESPIRAL if y < 14.6 else ESPIRAL_CLARO
            if face == "north" and abs(x) > 9.6 and 11.0 < y < 11.7: return ESPIRAL     # a ponta da espiral vista de frente
            if ponta is not None and z > ponta: return GUELRA_MEDIO                      # fio rosa-escuro na ponta da camada
            return ROSA_CLARO
        asa = []
        def peca_asa(nome, xa, xb, y0, y1, z0, z1, rx=0.0, ponta=None, ca=cor_asa):
            m = mat_bloco(lambda p, f, ca=ca, pt=ponta: ca(p, f, ponta=pt), borda=.06, alto=.12, fundo=-.12)
            x0, x1 = xs(lado, xa, xb)
            asa.append(caixa(nome + "_" + s_, [x0, y0, z0], [x1, y1, z1], m, res=4, rot=(rx, 0, 0), pivo=(x0, y1, z0)))
        # ombro: volume arredondado na frente (a asa é uma gota: frente alta e cheia)
        x0, x1 = xs(lado, 6.8, 10.8)
        mo = mat_bloco(lambda p, f, ca=cor_asa: ca(p, f), borda=.04, alto=.12, fundo=-.12)
        asa += g.arredondado("asa_ombro_" + s_, [x0, 10.8, -8.6], [x1, 20.0, -0.6], mo, r=1.2, res=4)
        # 3 camadas sobrepostas, cada uma mais comprida que a de cima, com o fio rosa-escuro na ponta; a traseira
        # afina em 2 pontas escalonadas. A asa inteira desce um pouco para trás (osso inclinado: a espiral não quebra)
        peca_asa("asa0", 6.8, 10.7, 16.4, 20.0, -6.0, 6.4, ponta=5.8)
        peca_asa("asa1", 6.8, 11.0, 12.6, 16.8, -6.0, 9.0, ponta=8.4)
        peca_asa("asa2", 6.8, 10.6, 9.4, 13.0, -5.0, 11.2, ponta=10.6)
        peca_asa("asa_ponta0", 7.0, 10.2, 13.4, 16.0, 8.6, 12.4, ponta=11.8)
        peca_asa("asa_ponta1", 7.0, 9.8, 10.2, 12.6, 10.8, 14.2, ponta=13.6)
        corpo.append(osso("asa_" + s_, [8.0 * lado, 19.0, -4.0], [7, 0, -3 * lado], asa))   # abraça o corpo e desce para trás

    # ================= cauda: leque de foices azuis grossas que arqueiam para trás e caem =================
    cauda = []
    BASE = (0.0, 16.6, 9.6)
    for k, (x, rx0, cv, Ls, h, c0, c1, yb) in enumerate(FOICES):
        n = len(Ls)
        segs = [(L, 2.5 - 0.12 * i, h - 0.5 * i, mix(c0, c1, i / n), mix(c0, c1, (i + 0.6) / n)) for i, L in enumerate(Ls)]
        cauda.append(pena_cauda(f"cauda_p{k}", (BASE[0] + x, yb, BASE[2] - 0.6 * k), segs, (rx0, 0, 0), cv,
                                mat_foice, sobrepoe=1.2))
    corpo.append(osso("cauda", list(BASE), [0, 0, 0], cauda))

    corpo.append(pescoco)
    raiz = osso("corpo", [0, 9, 0], [0, 0, 0], corpo)

    # ================= pernas e patas anfíbias =================
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 4.6 * lado; zc = -0.6
        pp = []
        ml = mat_bloco(lambda p, f: PERNA_LADO if f in ("east", "west") else AMARELO, borda=.06, alto=.0, fundo=-.06)
        pp.append(caixa("perna_" + s, [xc - 2.5, 2.2, zc - 2.5], [xc + 2.5, 9.6, zc + 2.5], ml))   # ~60% da largura do pé
        pp.append(caixa("pe_" + s, [xc - 4.2, 1.0, zc - 5.0], [xc + 4.2, 3.6, zc + 2.8], ml))
        mg = mat_bloco(lambda p, f: ROXO_CLARO if f == "up" else ROXO, borda=.1, alto=.0, fundo=.0)
        for k, dx in enumerate((-3.0, 0.0, 3.0)):
            pp.append(caixa(f"dedo_{k}_{s}", [xc + dx - 1.25, 0.0, zc - 9.0], [xc + dx + 1.25, 2.8, zc - 4.4], mg))
        pp.append(caixa("dedo_tras_" + s, [xc - 1.1, 0.0, zc + 2.4], [xc + 1.1, 2.0, zc + 5.0], mg))
        return osso("perna_" + s, [xc, 8.5, zc], [0, 0, 0], pp)

    return [raiz, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
