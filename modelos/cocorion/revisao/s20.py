"""Cocórion (#005, Ar): o Galo dos Ventos, galo guerreiro branco de crista espetada, cicatrizes de batalha, asas em
capa com a espiral verde do vento, calça hakama preta com faixa branca e katana na cintura.

Versão "suave" (rodadas s*): poucas peças grandes e bem desenhadas. Cabeça, pescoço e tronco em volumes chanfrados
(arredondado/arredondado2/octogono); crista de poucas mechas grandes que afinam e varrem para trás a partir de uma
base comum; asa em capa estreita colada ao corpo (3 faixas que abraçam o tronco); cauda de penas finas e compridas
num leque estreito; pernas finas. A luz é pintada em degradê contínuo pelo grupo, sem contraste por cubo."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
import previa                                  # só a matriz de rotação (mesma ordem do Blockbench)
from galo_base import peca, osso, mix, clamp, na_borda

ID = "cocorion"; NOME = "Cocórion"; NUMERO = 5
ALTURA = 2.4
QUADRUPEDE = False
ROSTO = ((0, 29.0, -5.0), 7.5)
N_CAUDA, SEG_CAUDA = 5, 4
ONDAS = [(f"cauda{k}", SEG_CAUDA, (1.6, 1.2, 0.0)) for k in range(N_CAUDA)]
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (amostrada nos PNGs da ficha; veja modelos/cocorion/detalhes.md) ----------------
BRANCO_F = (255, 238, 224); CLARO_F = (255, 247, 238)
LINHA_F = (226, 212, 200)                 # sombra entre as penas (cinza-claro quente)
CARVAO = (44, 45, 44); PRETO_H = (27, 28, 25); CARVAO_CL = (58, 60, 60)
VERDE = (58, 106, 48); VERDE_ESC = (38, 78, 26)
AMAR = (255, 192, 14); AMAR_ESC = (232, 140, 0); AMAR_CL = (255, 214, 70)
LARANJA_B = (238, 162, 10)
VERM = (204, 52, 38); VERM_ESC = (150, 30, 22); VERM_X = (186, 42, 32)
OURO = (250, 184, 12); OURO_CL = (255, 214, 80); OURO_ESC = (190, 122, 8)
PRETO_SOB = (40, 38, 36)
GARRA = (46, 46, 46)

LADO_KATANA = -1          # nas vistas, o lado -x aparece à direita de quem olha de frente (como a katana da ficha)
LADO_CICATRIZ = 1         # X da bochecha e marca da testa do lado que a arte mostra


def escuro(c): return (int(c[0] * .80), int(c[1] * .77), int(c[2] * .80))
def tons(c, f):
    f = clamp(f, -1, 1)
    return mix(c, CLARO_F, f) if f >= 0 else mix(c, escuro(c), -f)

def matriz(*rots):
    M = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    for r in rots: M = previa.mm(M, previa.rot(*r))
    return M

def mat_luz(cor_fn, M=None, borda=.05, grad=0.5, topo=.25, baixo=-.45):
    """Luz chapada pela normal no mundo (face de cima clara, de baixo na sombra) mais um degradê contínuo de
    altura pela faixa do GRUPO (todas as peças do grupo usam a mesma faixa: a luz atravessa as peças sem realçar
    cada cubo). Fio de borda bem leve."""
    def f(c):
        base = cor_fn(c)
        if base is None: return None
        nx, ny, nz = previa.mv(M, g.NORMAL[c["face"]]) if M else g.NORMAL[c["face"]]
        k = topo if ny > 0.6 else baixo if ny < -0.6 else 0.05 * ny
        y0, y1 = c["faixa"]
        k += grad * (clamp((c["p"][1] - y0) / max(y1 - y0, 1e-6)) - 0.6)
        if na_borda(c): k -= borda
        return tons(base, k)
    return f

def cor_fixa(cor): return lambda c: cor

def escama(a, y, larg=2.2, alt=1.7):
    """Penas em escama, grandes e suaves: só uma linha fina em arco embaixo de cada pena."""
    fila = math.floor(y / alt)
    fa = ((a + (fila % 2) * larg / 2) % larg) / larg
    fy = (y % alt) / alt
    return fy < 0.09 + 0.16 * (2 * abs(fa - 0.5)) ** 2

def risco_x(a, y, ca, cy, r, w=0.3, torto=0.0):
    da, dy = a - ca, y - cy
    if max(abs(da), abs(dy)) > r: return False
    j = torto * math.sin(round(da * 2) * 1.7 + round(dy * 2) * 0.9)
    return abs(da - dy + j) < w or abs(da + dy - j) < w

FAIXA_BRANCA = (10.0, 38.0)              # um degradê só para tudo o que é branco (corpo, asas, cabeça, crista)

# ---------------- lâmina de pena (crista, tufos, capa, cauda) ----------------
NERVURA_F = (255, 250, 244)
def cor_lamina(eixo_u, centro, cy=None, diag=False, claro=BRANCO_F, base=None, lado_claro=1):
    """Pena/mecha em 2 tons chapados (como as folhas do Espinhocó aprovado): na face larga, metade clara e metade
    base divididas por uma nervura; a espessura fica na base. Na ponta em losango a divisão segue a diagonal."""
    base = base or mix(BRANCO_F, LINHA_F, 0.75)
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        larga = ("east", "west") if eixo_u == "z" else ("north", "south")
        if face in larga:
            u = (z if eixo_u == "z" else x) - centro
            if diag: u = u + (y - cy)
            if abs(u) < 0.13: return NERVURA_F
            return claro if u * lado_claro > 0 else base
        if face == "up": return claro
        return base
    return f

def mecha(nome, raiz, rot, L, W, T=1.0, curva=10.0, gira=0, lado_claro=-1, fr=(0.55, 0.27, 0.6)):
    """Mecha grande da crista: lâmina larga (W) e fina (T) que nasce dentro do crânio, estreita no meio (dobrando
    'curva' graus) e termina em ponta de losango. Cresce em +y a partir da raiz; 'rot' aponta a mecha; gira=0: larga
    vista de lado; gira=90: larga vista de frente."""
    x, y, z = raiz
    M0 = matriz(rot, (0, gira, 0))
    L0, L1 = L * fr[0], L * fr[1]
    w1 = W * fr[2]
    cl = cor_lamina("z", z, lado_claro=lado_claro)
    p0 = peca(nome + "_0", [x - T / 2, y - 1.2, z - W / 2], [x + T / 2, y + L0, z + W / 2], mat_luz(cl, M0), faixa=FAIXA_BRANCA)
    M1 = previa.mm(M0, previa.rot(curva, 0, 0))
    y1 = y + L0 - 0.2
    p1 = peca(nome + "_1", [x - T / 2 + .03, y1 - 0.3, z - w1 / 2], [x + T / 2 - .03, y1 + L1, z + w1 / 2], mat_luz(cl, M1),
              faixa=FAIXA_BRANCA)
    q = w1 / 1.4142; cy = y1 + L1
    pt = peca(nome + "_p", [x - T / 2 + .06, cy - q / 2, z - q / 2], [x + T / 2 - .06, cy + q / 2, z + q / 2],
              mat_luz(cor_lamina("z", z, cy, True, lado_claro=lado_claro), previa.mm(M1, previa.rot(45, 0, 0))),
              rot=(45, 0, 0), pivo=(x, cy, z), faixa=FAIXA_BRANCA)
    return osso(nome, list(raiz), list(rot), [osso(nome + "_g", list(raiz), [0, gira, 0], [
        p0, osso(nome + "_c", [x, y1, z], [curva, 0, 0], [p1, pt])])])

# ---------------- espeto da juba (pirâmide em degraus) ----------------
PONTA_ROT = (-45.0, 0.0, math.degrees(math.atan(1 / math.sqrt(2))))     # gira o cubo com uma QUINA para +y

def espeto(nome, raiz, d, L, W, curva=10.0):
    """Espeto curto e grosso: base de seção quadrada (girada 45° em volta do próprio eixo, mostra 2 facetas), um
    degrau mais fino que dobra 'curva' graus e a ponta em pirâmide (cubo com a quina para fora): afina em degraus e
    termina pontudo vista de qualquer lado."""
    x, y, z = raiz
    rot = rot_para(d)
    M0 = matriz(rot, (0, 45, 0))
    L0, L1 = L * 0.45, L * 0.3
    w1 = W * 0.62
    cor = lambda c: mix(BRANCO_F, CLARO_F, 0.3)
    p0 = peca(nome + "_0", [x - W / 2, y - 1.2, z - W / 2], [x + W / 2, y + L0, z + W / 2], mat_luz(cor, M0), faixa=FAIXA_BRANCA)
    M1 = previa.mm(M0, previa.rot(curva, 0, 0))
    y1 = y + L0 - 0.2
    p1 = peca(nome + "_1", [x - w1 / 2, y1 - 0.3, z - w1 / 2], [x + w1 / 2, y1 + L1, z + w1 / 2], mat_luz(cor, M1),
              faixa=FAIXA_BRANCA)
    a = w1 * 0.92; cy = y1 + L1 - 0.1
    pt = peca(nome + "_p", [x - a / 2, cy - a / 2, z - a / 2], [x + a / 2, cy + a / 2, z + a / 2],
              mat_luz(cor, previa.mm(M1, previa.rot(*PONTA_ROT))), rot=PONTA_ROT, pivo=(x, cy, z), faixa=FAIXA_BRANCA)
    return osso(nome, list(raiz), list(rot), [osso(nome + "_g", list(raiz), [0, 45, 0], [
        p0, osso(nome + "_c", [x, y1, z], [curva, 0, 0], [p1, pt])])])

# ---------------- cabeça ----------------
EY = 29.2                                   # altura do olho
FX, ZF, QX = 1.2, -6.2, 3.6                 # meia largura da frente, z da frente, meia largura do crânio
ZQ = ZF + (QX - FX)
FAC_T = 1.6
FAC_L = (QX - FX) * 1.4142
FAC_O = ((FX + QX) / 2, (ZF + ZQ) / 2)
FAC_C = (FAC_O[0] - 0.7071 * FAC_T / 2, FAC_O[1] + 0.7071 * FAC_T / 2)
OLHO_U, OLHO_RU, OLHO_RV = 0.1, 1.35, 0.78
SOB_K = 0.42
SOB_Y = 0.6

def olho(u, v):
    """Olho estreito da ficha: topo cortado na diagonal pela sobrancelha; íris verde-viva nos 2/3 do lado do bico,
    pupila preta junto à borda da frente com brilho; esclera branca atrás."""
    du = u - OLHO_U
    ru, rv = OLHO_RU, OLHO_RV
    if abs(du) > ru or abs(v) > rv: return None
    cq = max(0.0, abs(du) - (ru - 0.32)) / 0.32, max(0.0, abs(v) - (rv - 0.32)) / 0.32
    if cq[0] ** 2 + cq[1] ** 2 > 1: return None
    if v > SOB_Y - 0.06 + SOB_K * du: return None
    if du < ru / 3:
        pu = du + ru - 0.5
        if (pu / 0.3) ** 2 + ((v + 0.05) / 0.45) ** 2 <= 1:
            if ((pu - 0.1) / 0.12) ** 2 + ((v - 0.16) / 0.12) ** 2 <= 1: return (255, 255, 255)
            return (10, 12, 10)
        return mix((70, 206, 50), (30, 140, 22), clamp((0.4 - v) / 1.2))
    return (255, 255, 255)

def cor_rosto(c): return BRANCO_F

def mat_faceta(lado):
    """Face diagonal do rosto: olho inteiro numa face plana; X na bochecha do lado da arte, riscos do outro."""
    fora = "east" if lado > 0 else "west"
    def desenho(c):
        x, y, z = c["p"]
        if c["face"] != fora: return None
        u, v = z - FAC_C[1], y - EY
        o = olho(u, v)
        if o is not None: return o
        if lado == LADO_CICATRIZ:
            if risco_x(u, v, 0.2, -1.75, 0.62, 0.15, torto=0.08): return VERM
        else:
            if abs((v + 1.3) - 0.8 * (u - 0.9)) < 0.13 and abs(u - 0.9) < 0.45: return VERM
            if (u - 0.2) ** 2 + (v + 1.6) ** 2 < 0.035: return VERM
        return None
    base = mat_luz(cor_rosto, matriz((0, 45 * lado, 0)), borda=.0)
    def f(c):
        d = desenho(c)
        return d if d is not None else base(c)
    return f

def mat_bico(M=None):
    def cor(c):
        x, y, z = c["p"]
        if c["face"] in ("east", "west") and abs(z - (ZF - 1.0)) < 0.26 and abs(y - 28.55) < 0.22: return PRETO_H
        return AMAR if c["face"] != "down" else AMAR_ESC
    return mat_luz(cor, M, borda=.06, grad=0.0, topo=.2, baixo=-.35)

def cor_testa(c):
    """Testa: pequena cruz vermelha de traço fino acima do olho do lado da arte."""
    x, y, z = c["p"]
    if c["face"] == "north":
        da, dy = x - 1.05 * LADO_CICATRIZ, y - 30.45
        if max(abs(da), abs(dy)) < 0.55 and (abs(da - dy) < 0.15 or abs(da + dy) < 0.15): return VERM
        if abs(da - 0.7) < 0.12 and abs(dy - 0.45) < 0.12: return VERM
    return BRANCO_F

def rot_para(d):
    """Rotação (rx, 0, rz) que aponta o +y local na direção d."""
    n = math.sqrt(sum(v * v for v in d)); dx, dy, dz = (v / n for v in d)
    return (math.degrees(math.asin(dz)), 0, math.degrees(math.atan2(-dx, dy)))

# espetos da juba: (raiz, direção, comprimento, largura da base); levemente assimétricos
ESPETOS = [
    # fileira da frente (sobre a testa): mais em pé
    ((-1.5, 33.0, -2.6), (-0.3, 1, -0.05), 5.0, 2.8), ((0.2, 33.4, -2.8), (0.05, 1, 0.05), 5.8, 3.0),
    ((1.7, 33.0, -2.4), (0.35, 1, 0.0), 5.2, 2.8),
    # alto: para cima e para trás
    ((-2.3, 33.4, -0.4), (-0.5, 1, 0.45), 6.4, 3.0), ((0.0, 33.8, -0.2), (0.0, 1, 0.55), 7.0, 3.2),
    ((2.3, 33.4, 0.0), (0.5, 1, 0.4), 6.6, 3.0),
    # trás de cima
    ((-1.7, 32.8, 2.0), (-0.3, 0.7, 1), 6.6, 3.0), ((0.4, 33.0, 2.2), (0.05, 0.8, 1), 7.0, 3.2),
    ((2.1, 32.6, 2.0), (0.35, 0.6, 1), 6.2, 3.0),
    # nuca
    ((-1.9, 30.4, 3.2), (-0.3, 0.15, 1), 6.0, 3.0), ((0.2, 30.2, 3.4), (0.0, 0.25, 1), 6.6, 3.0),
    ((2.1, 30.2, 3.2), (0.3, 0.05, 1), 5.8, 3.0),
    ((-1.2, 27.8, 3.2), (-0.25, -0.4, 1), 4.8, 2.6), ((1.2, 27.8, 3.2), (0.25, -0.35, 1), 4.6, 2.6),
    # lados de cima
    ((-3.8, 32.0, -0.6), (-1, 0.6, 0.35), 5.2, 2.8), ((3.8, 32.0, -0.4), (1, 0.7, 0.3), 5.6, 2.8),
    # lados (emolduram o rosto) e bochechas que descem para o pescoço
    ((-4.0, 29.4, -1.2), (-1, 0.05, 0.45), 4.8, 2.8), ((4.0, 29.6, -1.0), (1, 0.1, 0.5), 5.0, 2.8),
    ((-3.6, 26.8, -1.8), (-0.6, -0.7, 0.35), 4.4, 2.6), ((3.6, 26.8, -1.8), (0.6, -0.75, 0.3), 4.4, 2.6),
]

def montar_cabeca():
    cab = []
    mb = mat_luz(cor_rosto)
    # crânio: volume bem chanfrado, largo em cima, afinando para o bico pela frente em planos inclinados
    cab += g.arredondado2("cranio", [-QX, 25.4, ZQ - 0.2], [QX, 32.4, 2.4], mb, r=1.8, faixa=FAIXA_BRANCA)
    cab.append(peca("rosto_frente", [-FX - 0.05, 25.3, ZF], [FX + 0.05, 30.4, ZQ + 0.4], mb, faixa=FAIXA_BRANCA))
    cab.append(peca("testa", [-2.4, 29.9, ZF + 0.15], [2.4, 32.0, ZQ + 1.4], mat_luz(cor_testa, matriz((30, 0, 0))),
                    rot=(30, 0, 0), pivo=(0, 29.9, ZF + 0.15), faixa=FAIXA_BRANCA, res=6))
    cab.append(peca("queixo", [-2.2, 24.6, ZF + 0.8], [2.2, 26.2, ZQ + 2.4], mb, rot=(-14, 0, 0), pivo=(0, 26.2, ZQ + 2.4),
                    faixa=FAIXA_BRANCA))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 25.3, cz - FAC_L / 2], [cx + FAC_T / 2, 30.6, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, EY, cz), faixa=FAIXA_BRANCA, res=8))
        # sobrancelha: bloco preto grosso, à frente do olho, descendo para o bico (V de frente)
        xo = cx + FAC_T / 2 * lado
        x0, x1 = sorted((xo - 0.4 * lado, xo + 0.45 * lado))
        yb = EY + SOB_Y
        rs = (-math.degrees(math.atan(SOB_K)), 0, 0)
        msob = mat_luz(cor_fixa(PRETO_SOB), matriz((0, 45 * lado, 0), rs), borda=.0, grad=0.0, topo=.3, baixo=-.2)
        cab.append(osso("sobrancelha_" + s, [cx, EY, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s, [x0, yb, cz - FAC_L / 2 - 0.45], [x1, yb + 1.15, cz + FAC_L / 2 + 0.2], msob,
                 rot=rs, pivo=(cx, yb, cz + OLHO_U))]))
    # bico em cunha: base larga, meio, gancho estreito; mandíbula de baixo mais escura e recuada
    mbi = mat_bico()
    cab.append(peca("bico_cima", [-1.5, 27.5, ZF - 2.3], [1.5, 29.0, ZF + 0.5], mbi, res=4))
    cab.append(peca("bico_ponta", [-0.95, 27.2, ZF - 3.5], [0.95, 28.7, ZF - 1.9], mat_bico(matriz((-16, 0, 0))), res=4,
                    rot=(-16, 0, 0), pivo=(0, 28.7, ZF - 2.0)))
    cab.append(peca("bico_baixo", [-1.0, 26.6, ZF - 1.9], [1.0, 27.55, ZF + 0.4],
                    mat_luz(cor_fixa(LARANJA_B), borda=.1, grad=0.0, topo=.1), res=4))
    # barbelas: dois lóbulos vermelhos compridos sob o bico, o de cá um pouco mais comprido
    def cor_barb(c):
        if abs(c["p"][0]) < 0.2: return VERM_ESC
        return mix((228, 52, 40), (190, 38, 28), clamp((26.0 - c["p"][1]) / 3.0))
    mbar = mat_luz(cor_barb, borda=.15, grad=0.0, topo=.1)
    for lado, fim in ((-1, 23.6), (1, 23.9)):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.0, 1.45 * lado)); x2, x3 = sorted((0.2 * lado, 1.15 * lado))
        cab.append(osso("barbela_" + s, [0.0, 26.4, ZF - 1.0], [0, 0, -3 * lado], [
            peca("barbela_a_" + s, [x0, fim + 0.9, ZF - 1.7], [x1, 26.5, ZF - 0.2], mbar, res=4),
            peca("barbela_b_" + s, [x2, fim, ZF - 1.5], [x3, fim + 1.0, ZF - 0.45], mbar, res=4)]))
    # crista (juba): base arredondada que cobre o alto, a nuca e os lados do crânio (emoldura o rosto) e ~20 espetos
    # curtos e grossos em camadas, que afinam em degraus e abrem para cima, para trás e para os lados
    crista = []
    crista += g.arredondado2("crista_base", [-4.0, 26.6, -3.4], [4.0, 33.6, 3.6], mat_luz(cor_rosto), r=1.6,
                             faixa=FAIXA_BRANCA)
    for k, (raiz, d, L, W) in enumerate(ESPETOS):
        # lâmina de pena curta (2 tons com nervura): larga de lado nas de cima e de trás, larga de frente nas da
        # testa e dos lados (assim a juba é cheia de qualquer ângulo, sem virar cristal)
        gira = 90 if (d[2] < 0.3 or abs(d[0]) > 0.5) else 0
        crista.append(mecha(f"espeto{k}", raiz, rot_para(d), L * 0.9, W * 1.1, T=1.3, curva=12, gira=gira,
                            fr=(0.45, 0.3, 0.6)))
    cab.append(osso("crista", [0, 32.0, -1.0], [0, 0, 0], crista))
    return osso("cabeca", [0, 26.4, -1.0], [0, 0, 0], cab)

K_CAB = 1.2                                # a cabeça inteira (com a crista) fica maior, como na arte

def cabeca_grande():
    ini = len(g.PECAS)
    cab = montar_cabeca()
    g.transformar(ini, [cab], (0.0, EY, -2.0), k=K_CAB, sobe=-1.2)
    return cab

# ---------------- tronco ----------------
def cor_tronco(c):
    x, y, z = c["p"]
    face = c["face"]
    if face == "north" and z < -5.6:
        if risco_x(x, y, 0.0, 19.7, 2.5, 0.38, torto=0.08):
            pontas = max(abs(x), abs(y - 19.7)) > 2.0
            return (142, 31, 26) if pontas and (round(x * 2) + round(y * 2)) % 2 == 0 else VERM_X
    a = z if face in ("east", "west") else x
    if face != "up" and escama(a, y): return mix(BRANCO_F, LINHA_F, 0.6)
    return BRANCO_F

def montar_tronco():
    """Tronco de ave esguio: núcleo bem chanfrado que afunila para a cintura, peito com projeção moderada (quilha
    inclinada), dorso em capa e uma gola de 3 pontas na base do pescoço."""
    pc = []
    mt = mat_luz(cor_tronco)
    # tórax largo e fundo em cima, cintura estreita embaixo, peito projetado para a frente
    pc += g.arredondado2("torax", [-3.7, 17.0, -4.6], [3.7, 24.2, 3.4], mt, r=1.6, faixa=FAIXA_BRANCA, res=3)
    pc += g.arredondado2("cintura", [-3.0, 13.2, -3.6], [3.0, 18.6, 3.0], mt, r=1.2, faixa=FAIXA_BRANCA, res=3)
    pc += g.arredondado("peito", [-3.0, 16.2, -6.4], [3.0, 23.2, -3.4], mat_luz(cor_tronco, matriz((-8, 0, 0))), r=1.0,
                        rot=(-8, 0, 0), pivo=(0, 16.2, -4.4), faixa=FAIXA_BRANCA, res=3)
    mg = mat_luz(lambda c: mix(BRANCO_F, CLARO_F, 0.3), matriz((0, 0, 45)))
    q = 2.6 / 1.4142
    for k, (x, y) in enumerate(((-1.8, 22.3), (0.0, 21.8), (1.8, 22.3))):
        pc.append(peca(f"gola{k}", [x - q / 2, y + 0.4 - q / 2, -6.6], [x + q / 2, y + 0.4 + q / 2, -5.6], mg, rot=(0, 0, 45),
                       pivo=(x, y + 0.4, -6.1), faixa=FAIXA_BRANCA))
    # dorso: capa de penas do pescoço até a raiz da cauda, borda de baixo em 3 pontas
    mc = mat_luz(lambda c: mix(BRANCO_F, LINHA_F, 0.6) if c["face"] == "south" and escama(c["p"][0], c["p"][1]) else BRANCO_F)
    pc += g.arredondado("dorso", [-3.2, 14.2, 2.4], [3.2, 23.6, 4.6], mc, r=0.8, rot=(8, 0, 0), pivo=(0, 23.6, 3.0),
                        faixa=FAIXA_BRANCA)
    q = 2.8 / 1.4142
    for k, x in enumerate((-1.9, 0.0, 1.9)):
        yb = 14.4 - (0.5 if k == 1 else 0.0)
        pc.append(peca(f"dorso_ponta{k}", [x - q / 2, yb - q / 2, 3.6], [x + q / 2, yb + q / 2, 5.0], mc, rot=(0, 0, 45),
                       pivo=(x, yb, 4.3), faixa=FAIXA_BRANCA))
    return pc

def cor_hakama(c):
    x, y, z = c["p"]
    face = c["face"]
    a = z if face in ("east", "west") else x
    if face == "up": return CARVAO_CL
    if y < 6.9 and face != "down": return PRETO_H
    return CARVAO if math.floor((a + 0.3) / 1.5) % 2 == 0 else (54, 56, 58)

# ---------------- asas ----------------
def _curva_glifo():
    pts = []
    te = 2.5 * math.pi
    for k in range(60):
        th = te * k / 59
        r = 0.45 + 0.42 * th
        ph = te - th - math.pi / 2
        pts.append((r * math.cos(ph), r * math.sin(ph)))
    ue, ve = pts[-1]
    return pts + [(ue - 1.0, ve - 1.2), (ue - 2.0, ve - 2.6), (ue - 2.6, ve - 3.4), (ue - 3.1, ve - 3.5), (ue - 3.4, ve - 3.0)]
GLIFO_P = _curva_glifo()
GLIFO_C = (18.6, -0.3)                   # (y, z) do centro da espiral (no plano da asa)
GLIFO_K = 0.72
GLIFO_W = 0.64

def _dist_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    t = clamp(((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy + 1e-9))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))

def glifo(y, z):
    a, v = -(z - GLIFO_C[1]) / GLIFO_K, (y - GLIFO_C[0]) / GLIFO_K
    if not (-9.0 < a < 4.5 and -10.0 < v < 4.5): return False
    return any(_dist_seg(a, v, *GLIFO_P[i], *GLIFO_P[i + 1]) < GLIFO_W for i in range(len(GLIFO_P) - 1))

def mat_asa(lado, M, cor=BRANCO_F, glifo_ok=True, zc=None, cy=None, diag=False, para_asa=None):
    """Pena da capa: face larga em 2 tons (metade da frente clara, de trás na base) com nervura no meio; as penas
    verdes de dentro ficam chapadas. A espiral é desenhada no plano da asa: 'para_asa' leva o ponto da pena para o
    referencial do osso da asa (assim o desenho continua de uma pena para a outra)."""
    fora = "east" if lado > 0 else "west"
    if cor == BRANCO_F and zc is not None:
        c_ = cor_lamina("z", zc, cy, diag, lado_claro=-1)
    elif cor == BRANCO_F:
        def c_(c):
            if c["face"] == fora and escama(c["p"][2], c["p"][1], 2.8, 2.6): return mix(BRANCO_F, LINHA_F, 0.5)
            return BRANCO_F
    else:
        c_ = cor_fixa(cor)
    m = mat_luz(c_, M)
    def f(c):
        if glifo_ok and c["face"] == fora:
            q = para_asa(c["p"]) if para_asa else c["p"]
            if glifo(q[1], q[2]): return VERDE
        return m(c)
    return f

def faixa_asa(nome, lado, zc, W, ytop, L, xi, esp, rx, ry, ROT, glifo_ok=True):
    """Pena da capa pendurada do ombro: corpo largo, meio mais estreito e ponta em losango (afina como uma pena).
    rx abre a pena para trás (negativo) no leque; ry a gira em volta do eixo vertical para abraçar o tronco."""
    x0, x1 = sorted((xi, xi + esp * lado))
    M = matriz(ROT, (rx, ry, 0))
    R = previa.rot(rx, ry, 0); P = (xi, ytop, zc)
    def para_asa(p):
        v = previa.mv(R, [p[i] - P[i] for i in range(3)])
        return [v[i] + P[i] for i in range(3)]
    Lb, Lm = L * 0.72, L * 0.16
    wm = W * 0.62
    yb = ytop - Lb; ym = yb - Lm
    q = wm / 1.4142
    ma = mat_asa(lado, M, glifo_ok=glifo_ok, zc=zc, para_asa=para_asa)
    pcs = [peca(nome, [x0, yb, zc - W / 2], [x1, ytop, zc + W / 2], ma, faixa=FAIXA_BRANCA, res=3),
           peca(nome + "_m", [x0 + 0.03, ym, zc - wm / 2], [x1 - 0.03, yb + 0.2, zc + wm / 2], ma, faixa=FAIXA_BRANCA, res=3),
           peca(nome + "_p", [x0 + 0.06, ym - q / 2, zc - q / 2], [x1 - 0.06, ym + q / 2, zc + q / 2],
                mat_asa(lado, previa.mm(M, previa.rot(45, 0, 0)), glifo_ok=False, zc=zc, cy=ym, diag=True),
                rot=(45, 0, 0), pivo=(xi, ym, zc), faixa=FAIXA_BRANCA, res=3)]
    return osso(nome, [xi, ytop, zc], [rx, ry, 0], pcs)

def montar_asa(lado):
    """Asa em capa estreita colada ao corpo, em 3 camadas de penas como na arte: cobertura curta em cima, cobertura
    média e penas longas embaixo, todas com a ponta à mostra (borda de baixo serrilhada em degraus) e abrindo um
    pouco para trás embaixo; a espiral do vento fica no meio, contínua de uma pena para a outra."""
    s = "d" if lado < 0 else "e"
    xi = 3.25 * lado
    PIV = (xi, 23.6, -0.4)
    ROT = (-3, 0, 16 * lado)
    M = matriz(ROT)
    pc = []
    camadas = [  # (x para fora, topo, [(zc, W, L, rx, ry)])
        (-0.05, 20.6, [(-2.4, 2.6, 13.2, 2, 10), (-0.1, 2.8, 14.8, -7, 0), (2.1, 2.8, 14.2, -17, -8), (3.8, 2.4, 12.6, -28, -14)]),
        (0.25, 24.2, [(-2.6, 3.6, 9.6, 2, 8), (0.3, 3.8, 11.0, -3, 0), (3.0, 3.4, 10.0, -9, -6)]),
    ]
    for c, (dx, topo, penas) in enumerate(camadas):
        for k, (zc, W, L, rx, ry) in enumerate(penas):
            pc.append(faixa_asa(f"asa_c{c}p{k}_" + s, lado, zc, W, topo, L, xi + dx * lado, 1.1, rx, ry * lado, ROT, c > 0))
    x0, x1 = sorted((xi - 1.0 * lado, xi + 1.9 * lado))
    pc += g.arredondado("asa_ombro_" + s, [x0, 21.6, -4.0], [x1, 25.4, 3.4], mat_asa(lado, M, glifo_ok=True), r=1.1,
                        faixa=FAIXA_BRANCA)
    # pena verde por dentro (aparece atrás e embaixo)
    xa0, xa1 = sorted((xi - 0.4 * lado, xi + 0.5 * lado))
    mv = mat_asa(lado, matriz(ROT, (-24, 0, 0)), cor=VERDE, glifo_ok=False)
    q = 2.4 / 1.4142
    pc.append(osso("asa_verde_" + s, [xi, 21.0, 2.6], [-24, 0, 0], [
        peca("asa_verde_" + s, [xa0, 8.6, 1.4], [xa1, 16.0, 3.8], mv, faixa=FAIXA_BRANCA),
        peca("asa_verde_" + s + "_p", [xa0 + 0.03, 8.6 - q / 2, 2.6 - q / 2], [xa1 - 0.03, 8.6 + q / 2, 2.6 + q / 2], mv,
             rot=(45, 0, 0), pivo=(xi, 8.6, 2.6), faixa=FAIXA_BRANCA)]))
    return osso("asa_" + s, list(PIV), list(ROT), pc)

# ---------------- cauda ----------------
def mat_pena_cauda(M, t0, t1, verde):
    """Pena da cauda: creme por cima e nas pontas, verde-escuro embaixo e perto da raiz (alternando por pena)."""
    corte = 0.62 if verde else 0.42           # fração de baixo da pena que é verde
    def cor(c):
        (_, y0, z0), (_, y1, z1) = c["b"]
        fy = (c["p"][1] - y0) / max(y1 - y0, 1e-6)
        t = t0 + (t1 - t0) * clamp((c["p"][2] - z0) / max(z1 - z0, 1e-6))
        face = c["face"]
        ponta = t > 0.8
        if face == "up": return BRANCO_F
        if face == "down": return BRANCO_F if ponta else VERDE_ESC
        if face in ("north", "south"): return mix(BRANCO_F, LINHA_F, 0.7) if ponta else VERDE
        if ponta or fy > corte + 0.1: return BRANCO_F if fy > 0.5 else mix(BRANCO_F, LINHA_F, 0.75)
        if fy > corte: return NERVURA_F
        return VERDE if fy > corte * 0.4 else VERDE_ESC
    return mat_luz(cor, M, grad=0.0)

def pena_cauda(nome, raiz, rot0, curvas, L, H, esp, verde=False):
    """Pena fina e comprida: 4 blocos encadeados e sobrepostos nas juntas (ossos '<nome>_k'), estreita na raiz,
    mais alta no meio e ponta em losango; 'curvas' dá o giro de cada junta."""
    fr = [0.24, 0.28, 0.26, 0.22]
    alt = [0.7, 1.0, 0.95, 0.75]
    ee = [0.9, 1.0, 0.95, 0.85]
    n = len(fr)
    def seg(k, pos, M, t0):
        px, py, pz = pos
        h = H * alt[k]; Ls = L * fr[k]; e = esp * ee[k]
        r = list(rot0) if k == 0 else [curvas[k - 1], 0, 0]
        Mk = previa.mm(M, previa.rot(*r))
        t1 = t0 + fr[k]
        ov = 0.8 if k > 0 else 0.4
        filhos = [peca(f"{nome}_{k}", [px - e / 2, py - h * 0.5, pz - ov], [px + e / 2, py + h * 0.5, pz + Ls],
                       mat_pena_cauda(Mk, t0, t1, verde), faixa=(py - h, py + h), res=3)]
        if k + 1 < n:
            filhos.append(seg(k + 1, (px, py, pz + Ls - 0.1), Mk, t1))
        else:
            q = h * 1.1 / 1.4142
            filhos.append(peca(f"{nome}_pt", [px - e * 0.4, py - q / 2, pz + Ls - q / 2], [px + e * 0.4, py + q / 2, pz + Ls + q / 2],
                               mat_pena_cauda(previa.mm(Mk, previa.rot(45, 0, 0)), 0.95, 1.0, verde), rot=(45, 0, 0),
                               pivo=(px, py, pz + Ls), res=3))
        return osso(f"{nome}_{k}", list(pos), r, filhos)
    return seg(0, raiz, matriz(), 0.0)

def montar_cauda():
    """Leque estreito de 6 penas finas e compridas: sobem e varrem para trás saindo de uma raiz estreita na cintura,
    cada uma curvando a ponta para baixo; abertas pouco para os lados."""
    penas = []
    # (x, raiz y, z, elevação, giro y, curvas, comprimento, altura, espessura, verde)
    P = [(-0.3, 21.0, 3.2, 80, 0, (8, 14, 20), 15.0, 4.0, 1.0, False),
         (0.35, 20.2, 3.4, 65, -7, (10, 16, 21), 16.5, 4.2, 0.9, True),
         (-0.35, 19.4, 3.6, 50, 7, (11, 17, 21), 17.0, 4.2, 1.0, False),
         (0.3, 18.6, 3.7, 35, -8, (11, 16, 19), 16.0, 4.0, 0.9, True),
         (-0.2, 17.8, 3.8, 20, 8, (10, 13, 15), 14.0, 3.6, 0.9, False)]
    for k, (x, y, z, e, ry, cv, L, H, esp, vd) in enumerate(P):
        penas.append(pena_cauda(f"cauda{k}", (x, y, z), (-e, ry, 0), cv, L, H, esp, vd))
    return osso("cauda", [0, 17.6, 3.6], [0, 0, 0], penas)

# ---------------- katana ----------------
def mat_metal(cima, frente, lado, baixo):
    return g.mat_facetado(cima, frente, lado, baixo, quina=-0.3)

def mat_cabo(c):
    x, y, z = c["p"]
    t = (z - c["b"][0][2]) % 1.2
    meio = abs((c["j"] + 0.5) / c["th"] - 0.5) if c["face"] in ("east", "west") else abs((c["i"] + 0.5) / c["tw"] - 0.5)
    if c["face"] in ("east", "west", "up", "down") and 0.3 < t < 0.9 and meio < 0.3: return BRANCO_F
    return VERDE_ESC if na_borda(c) else VERDE

def montar_katana(base):
    """Katana ao longo de z (cabo para a frente, bainha para trás) a partir da tsuba em 'base'."""
    bx, by, bz = base
    def pc_(nome, de, ate, mat, **kw):
        return g.peca(nome, [de[0] + bx, de[1] + by, de[2] + bz], [ate[0] + bx, ate[1] + by, ate[2] + bz], mat, **kw)
    ouro = mat_metal(OURO_CL, OURO, mix(OURO, OURO_ESC, .4), OURO_ESC)
    bainha = mat_metal((70, 72, 78), (36, 38, 42), (28, 30, 34), (16, 16, 20))
    return [pc_("katana_cabo", [-0.7, -0.7, -6.4], [0.7, 0.7, -0.3], mat_cabo, res=4),
            pc_("katana_pomo", [-0.8, -0.8, -7.0], [0.8, 0.8, -6.35], ouro, res=4),
            pc_("katana_tsuba_a", [-1.8, -0.65, -0.4], [1.8, 0.65, 0.2], ouro, res=4),
            pc_("katana_tsuba_b", [-0.65, -1.8, -0.35], [0.65, 1.8, 0.15], ouro, res=4),
            pc_("katana_bainha", [-0.55, -0.7, 0.1], [0.55, 0.7, 14.0], bainha),
            pc_("katana_kurikata", [-0.65, -0.8, 1.6], [0.65, 0.8, 2.3], ouro, res=4),
            pc_("katana_kojiri", [-0.6, -0.75, 13.8], [0.6, 0.75, 15.0], ouro, res=4)]

# ---------------- pernas ----------------
def cor_perna(c):
    """Perna amarela com faixas de escama (linha mais escura a cada ~1,1 de altura); embaixo na sombra."""
    if c["face"] == "down": return AMAR_ESC
    if c["face"] != "up" and (c["p"][1] % 1.1) < 0.16: return mix(AMAR, AMAR_ESC, 0.7)
    return AMAR

def perna(lado):
    """Hakama de uma perna até o joelho (prisma chanfrado que abre embaixo + 2 pregas inclinadas na frente e uma do
    lado) e perna de ave grossa e curta com faixas de escama; pé grande de 3 dedos com garras pretas grossas e 1 atrás."""
    s = "d" if lado < 0 else "e"; xc = 2.3 * lado; zc = 0.4
    pp = []
    def bx(a, b): return sorted((a * lado, b * lado))
    mh = mat_luz(cor_hakama, grad=0.4, topo=.15, baixo=-.4)
    x0, x1 = bx(0.1, 4.6)
    pp += g.octogono("hakama_" + s, [x0, 5.8, -4.5], [x1, 13.6, 4.1], mh, r=1.0, faixa=(5, 14), rot=(0, 0, 9 * lado),
                     pivo=(2.0 * lado, 13.6, 0))
    for k, (a, b, inc, abre) in enumerate(((0.2, 2.2, 12, 5), (2.0, 4.1, 7, 12))):
        x0, x1 = bx(a, b)
        pp.append(peca(f"prega{k}_" + s, [x0, 5.8, -5.1], [x1, 13.2, -4.2], mh, rot=(inc, 0, abre * lado),
                       pivo=((a + b) / 2 * lado, 13.2, -4.6), faixa=(5, 14)))
    x0, x1 = bx(4.0, 4.9)
    pp.append(peca("prega_lado_" + s, [x0, 6.0, -3.4], [x1, 13.2, 3.2], mh, rot=(0, 0, 13 * lado), pivo=(4.4 * lado, 13.2, 0),
                   faixa=(5, 14)))
    ma = mat_luz(cor_perna, grad=0.3, topo=.2, baixo=-.3, borda=.08)
    pp += g.octogono("coxa_" + s, [xc - 1.8, 3.6, zc - 1.8], [xc + 1.8, 9.0, zc + 1.8], ma, r=0.6, faixa=(0, 9))
    pp += g.octogono("tarso_" + s, [xc - 1.4, 1.2, zc - 1.4], [xc + 1.4, 5.0, zc + 1.4], ma, r=0.5, faixa=(0, 9))
    mg = mat_luz(cor_fixa(GARRA), grad=0.0, borda=.1, topo=.3)
    mdedo = mat_luz(lambda c: AMAR if c["face"] != "down" else AMAR_ESC, grad=0.3, topo=.2, baixo=-.3, borda=.08)
    for nome, dx, ang, comp in (("meio", 0.0, 0, 3.4), ("fora", 1.7 * lado, 22 * lado, 2.8), ("dentro", -1.7 * lado, -18 * lado, 2.6)):
        x0 = xc + dx
        pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, zc - 0.6], [0, -ang, 0], [
            peca(f"dedo_{nome}_{s}", [x0 - .9, 0, zc - 0.6 - comp], [x0 + .9, 1.9, zc + 0.8], mdedo, faixa=(0, 8)),
            peca(f"garra_{nome}_{s}", [x0 - .75, 0.0, zc - 0.6 - comp - 1.5], [x0 + .75, 1.6, zc - 0.4 - comp], mg)]))
    mtras = mat_luz(lambda c: GARRA if c["p"][2] > zc + 2.8 else (AMAR if c["face"] != "down" else AMAR_ESC), grad=0.3, borda=.08)
    pp.append(peca("dedo_tras_" + s, [xc - .7, 0, zc + 1.0], [xc + .7, 1.4, zc + 3.9], mtras, faixa=(0, 8)))
    return osso("perna_" + s, [xc, 13.0, zc], [0, 0, 0], pp)

# ---------------- montagem ----------------
def montar():
    corpo = []
    corpo += montar_tronco()
    # cintura da hakama e faixa branca com nó e duas tiras
    mh = mat_luz(cor_hakama, grad=0.4, topo=.15, baixo=-.4)
    corpo += g.arredondado("hakama_cint", [-3.8, 12.4, -4.3], [3.8, 14.8, 3.9], mh, r=0.5, faixa=(6, 14))
    mf = mat_luz(cor_fixa(BRANCO_F), grad=0.0, borda=.1)
    corpo += g.arredondado("faixa", [-3.95, 13.9, -4.55], [3.95, 15.5, 4.1], mf, r=0.35)
    nx = -1.0
    corpo.append(peca("no_faixa", [nx - 0.8, 13.4, -5.6], [nx + 0.8, 15.8, -4.4], mf))
    corpo.append(peca("no_ponta1", [nx - 0.85, 6.6, -5.6], [nx - 0.1, 13.6, -5.2], mf, rot=(0, 0, -5), pivo=(nx - 0.5, 13.6, -5.4)))
    corpo.append(peca("hakama_meio_f", [-1.6, 6.0, -4.85], [1.6, 13.0, -4.0], mh, rot=(10, 0, 0), pivo=(0, 13.0, -4.4)))
    corpo.append(peca("hakama_meio_t", [-1.6, 6.2, 3.6], [1.6, 13.0, 4.4], mh, rot=(-10, 0, 0), pivo=(0, 13.0, 4.0)))
    corpo.append(peca("laco_d", [nx - 2.0, 14.0, -5.5], [nx - 0.5, 15.3, -4.7], mf, rot=(0, 0, 20), pivo=(nx - 0.5, 14.6, -5.1)))
    corpo.append(peca("laco_e", [nx + 0.5, 14.0, -5.5], [nx + 2.0, 15.3, -4.7], mf, rot=(0, 0, -20), pivo=(nx + 0.5, 14.6, -5.1)))
    corpo.append(peca("no_ponta2", [nx + 0.1, 7.6, -5.6], [nx + 0.85, 13.6, -5.2], mf, rot=(0, 0, 5), pivo=(nx + 0.5, 13.6, -5.4)))
    KAT = (3.9 * LADO_KATANA, 14.6, -4.8)
    corpo.append(osso("katana", list(KAT), [32, 24 * (-LADO_KATANA), 0], montar_katana(KAT)))
    mp = mat_luz(cor_tronco)
    pescoco = osso("pescoco", [0, 23.0, -1.0], [0, 0, 0], [
        *g.arredondado2("pescoco", [-2.6, 21.6, -5.6], [2.6, 27.0, 1.4], mp, r=1.1, faixa=FAIXA_BRANCA),
        cabeca_grande()])
    corpo.append(pescoco)
    for lado in (-1, 1):
        corpo.append(montar_asa(lado))
    corpo.append(montar_cauda())
    tronco = osso("corpo", [0, 13.0, 0], [0, 0, 0], corpo)
    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
