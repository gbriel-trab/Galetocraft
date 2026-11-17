"""Pirococó (#001, Fogo, mítico): o galo-fênix das chamas, refeito do zero sobre a ficha HD-2D (2026-11-15).

Galo de briga imponente, inclinado para a frente: elmo-máscara roxo com coroa dourada, gema vermelha em losango e
3 chifres de ouro (2 grandes e 1 pequeno acima da gema); rosto e garganta creme, olho vermelho bravo e bico amarelo
curvo; juba de chamas vermelhas varrendo para trás; peitoral roxo compacto no alto do peito com a fênix em chama e a
camada em V lilás com a divisa dourada; capa de asas em FILEIRAS de cor (coberteiras lilás e roxas, depois vermelho,
laranja e amarelo nas pontas) varrida para trás e acabando acima das pernas; cauda em leque de foices de chama com 3
correntes de contas douradas e pingentes de losango com gema; canela dourada à mostra, caneleiras roxas em 2 faixas
e pés amarelos grandes de garras escuras.

Ideias da montagem:
- toda pena é um bloco grosso com ponta em losango, orientada por vetores do mundo (direção da ponta e normal da
  face larga), pintada em FAIXAS chapadas (cor dominante + ponta de outra cor, sem degradê dentro da pena) com uma
  metade clara e uma metade escura e contorno escuro só nas beiradas compridas;
- plumas compridas (juba, crista, cauda) são cadeias de 2-3 segmentos que afinam e dobram no plano da face larga;
- a armadura roxa (elmo, peitoral, caneleiras) é um detalhe facetado, nunca a massa principal."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, clamp, tom, na_borda

ID = "pirococo"; NOME = "Pirococó"; NUMERO = 1
ALTURA = 2.8
QUADRUPEDE = False
ROSTO = ((0, 32.4, -8.6), 7.6)
RAIZ = Path(__file__).resolve().parent.parent.parent

# ---------------- paleta oficial (as 9 amostras da ficha HD-2D) ----------------
ROXO_ESC = (70, 38, 108); ROXO = (140, 81, 174); LILAS = (187, 141, 202)
CREME = (244, 226, 200)
AMARELO = (255, 193, 43); LARANJA = (253, 106, 3)
VERM = (231, 39, 31); VERM_ESC = (158, 16, 23)
OURO = (252, 159, 1)
# tons de apoio (luz, sombra e contorno das cores da ficha)
LILAS_CL = (214, 184, 226); ROXO_FUNDO = (46, 22, 74)
VERM_FUNDO = (108, 10, 18)
LARANJA_CL = (255, 146, 24)
AMARELO_CL = (255, 224, 118)
OURO_ESC = (198, 112, 6)
CREME_SOMBRA = (222, 198, 172)
PRETO = (26, 10, 18)
GARRA = (58, 50, 64); GARRA_CL = (120, 112, 126)
CONTORNO = (34, 10, 26)

def contorno(c, f=0.5): return mix(c, CONTORNO, f)

# ---------------- álgebra de orientação (Blockbench: M = Rz·Ry·Rx, graus) ----------------
def _n(v):
    l = math.sqrt(sum(a * a for a in v)); return tuple(a / l for a in v)
def _dot(a, b): return sum(x * y for x, y in zip(a, b))
def _cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def _col(A, j): return (A[0][j], A[1][j], A[2][j])
def _mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def _t(A): return [[A[j][i] for j in range(3)] for i in range(3)]
def _rotm(rx, ry, rz):
    a, b, c = (math.radians(v) for v in (rx, ry, rz))
    Rx = [[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]]
    Ry = [[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]]
    Rz = [[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]]
    return _mm(Rz, _mm(Ry, Rx))

def euler(A):
    """Inverso de _rotm: (rx, ry, rz) em graus com A = Rz·Ry·Rx."""
    sb = max(-1.0, min(1.0, -A[2][0])); b = math.asin(sb)
    if abs(sb) < 0.99999:
        a = math.atan2(A[2][1], A[2][2]); c = math.atan2(A[1][0], A[0][0])
    else:
        c = 0.0; a = math.atan2(-A[1][2], A[1][1])
    return [round(math.degrees(v), 4) for v in (a, b, c)]

def quadro(d, n):
    """Rotação que leva o eixo local -y (a peça pendurada da raiz) para a direção d e o +x local (face larga) para n."""
    d = _n(d)
    n = _n(tuple(n[i] - _dot(n, d) * d[i] for i in range(3)))
    ey = tuple(-a for a in d); ex = n; ez = _cross(ex, ey)
    return [[ex[i], ey[i], ez[i]] for i in range(3)]

def girar_ponto(p, A, piv):
    q = [p[i] - piv[i] for i in range(3)]
    return tuple(sum(A[i][k] * q[k] for k in range(3)) + piv[i] for i in range(3))

# ---------------- penas em faixas ----------------
LUZ_PENA = _n((0.0, 0.7, -0.7))          # a metade da pena virada para cima/frente é a clara
C45 = S45 = math.sqrt(0.5)

def faixa_de(faixas, t, u, lingua):
    """Faixa de cor pela posição t (0 raiz .. 1 ponta). A divisa sobe pelo meio da pena (língua de chama)."""
    te = t + lingua * max(0.0, 1.0 - abs(u))
    for t1, a, b in faixas:
        if te <= t1: return a, b
    return faixas[-1][1], faixas[-1][2]

def mat_pena(faixas, y0, L, zc, cl, lingua=0.12):
    """Pena em bloco pendurada de y0 (comprimento L): faixas chapadas ao longo do comprimento, metade clara (u > 0) e
    metade escura (u < 0) na face larga, contorno escuro só nas beiradas compridas e na ponta, espessura na sombra."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        (bx0, by0, bz0), (bx1, by1, bz1) = c["b"]
        pt = c["nome"].endswith("_pt")
        if pt:                                   # ponta em losango (girada 45° em x em volta do centro)
            cy, cz = (by0 + by1) / 2, (bz0 + bz1) / 2
            dy, dz = y - cy, z - cz
            y, z = cy + dy * C45 - dz * S45, cz + dy * S45 + dz * C45
            hw = (bz1 - bz0) * 0.7071
        else:
            hw = (bz1 - bz0) / 2
        t = clamp((y0 - y) / L)
        u = (z - zc) / max(hw, 1e-6) * cl
        a, b = faixa_de(faixas, t, u, lingua)
        if face in ("east", "west"):
            borda = na_borda(c) if pt else c["i"] in (0, c["tw"] - 1)
            if borda: return contorno(b, 0.45)
            cor = a if u > 0.05 else b
            if t < 0.06: cor = contorno(b, 0.3)
            return cor
        if face == "up": return a
        if face == "down": return contorno(b, 0.35)
        return contorno(b, 0.18)
    return f

def pena(nome, raiz, d, n, L, W, T, faixas, res=3, lingua=0.12, brilho=False):
    """Pena grossa pendurada da raiz: corpo + ponta em losango, orientada pelos vetores do mundo d (para a ponta) e
    n (para onde olha a face larga)."""
    x, y, z = raiz
    A = quadro(d, n)
    cl = 1 if _dot(_col(A, 2), LUZ_PENA) >= 0 else -1
    Lb = L - W * 0.5; s = W / 1.4142
    m = mat_pena(faixas, y, L, z, cl, lingua)
    corpo = peca(nome, [x - T / 2, y - Lb, z - W / 2], [x + T / 2, y + 0.1, z + W / 2], m, res=res, brilho=brilho)
    ponta = peca(nome + "_pt", [x - T / 2 + 0.03, y - Lb - s / 2, z - s / 2], [x + T / 2 - 0.03, y - Lb + s / 2, z + s / 2], m,
                 rot=(45, 0, 0), pivo=(x, y - Lb, z), res=res, brilho=brilho)
    return osso(nome, list(raiz), euler(A), [corpo, ponta])

def pluma(nome, raiz, d, n, segs, curva, faixas, dobra=None, res=3, lingua=0.1, brilho=False):
    """Pluma comprida: segmentos encadeados (ossos '<nome>_k') que afinam, com ponta em losango; cada junta dobra
    'curva' graus no plano da face larga, para o lado do vetor do mundo 'dobra'."""
    x, y0, z = raiz
    A0 = quadro(d, n)
    ez = _col(A0, 2)
    cl = 1 if _dot(ez, LUZ_PENA) >= 0 else -1
    sinal = 1 if dobra is None or _dot(ez, dobra) >= 0 else -1
    rx = -abs(curva) * sinal
    Ltot = sum(s_[0] for s_ in segs) + segs[-1][1] * 0.5
    m = mat_pena(faixas, y0, Ltot, z, cl, lingua)
    def seg(k, ytop):
        L, W, T = segs[k]
        pcs = [peca(f"{nome}_{k}", [x - T / 2, ytop - L, z - W / 2], [x + T / 2, ytop + (0.25 if k else 0.1), z + W / 2], m,
                    res=res, brilho=brilho)]
        if k + 1 < len(segs):
            pcs.append(seg(k + 1, ytop - L))
        else:
            s = W / 1.4142
            pcs.append(peca(f"{nome}_pt", [x - T / 2 + 0.03, ytop - L - s / 2, z - s / 2], [x + T / 2 - 0.03, ytop - L + s / 2, z + s / 2],
                            m, rot=(45, 0, 0), pivo=(x, ytop - L, z), res=res, brilho=brilho))
        return osso(f"{nome}_{k}", [x, ytop, z], euler(A0) if k == 0 else [rx, 0, 0], pcs)
    return seg(0, y0)

# faixas: [(t_fim, cor clara, cor escura)] da raiz para a ponta (cada fileira com UMA cor dominante e a ponta de outra)
F_LILAS = [(0.70, LILAS, ROXO), (1.0, LILAS_CL, LILAS)]
F_ROXO = [(0.74, ROXO, ROXO_ESC), (1.0, LILAS, ROXO)]
F_VERM = [(0.80, VERM, VERM_ESC), (1.0, LARANJA_CL, LARANJA)]
F_VERM_ESC = [(0.78, VERM_ESC, VERM_FUNDO), (1.0, VERM, VERM_ESC)]
F_LAR = [(0.74, LARANJA_CL, LARANJA), (1.0, AMARELO, OURO)]
F_AMAR = [(0.76, AMARELO, OURO), (1.0, AMARELO_CL, AMARELO)]
F_JUBA = [(0.58, VERM, VERM_ESC), (0.84, LARANJA_CL, LARANJA), (1.0, AMARELO, OURO)]
F_JUBA_ESC = [(0.70, VERM, VERM_ESC), (1.0, LARANJA_CL, LARANJA)]
F_CRISTA = [(0.42, VERM, VERM_ESC), (0.76, LARANJA_CL, LARANJA), (1.0, AMARELO, OURO)]
F_CAUDA_AM = [(0.30, VERM, VERM_ESC), (0.62, LARANJA_CL, LARANJA), (1.0, AMARELO, OURO)]
F_CAUDA_V = [(0.58, VERM, VERM_ESC), (0.84, LARANJA_CL, LARANJA), (1.0, AMARELO, OURO)]
F_CAUDA_E = [(0.66, VERM_ESC, VERM_FUNDO), (0.88, VERM, VERM_ESC), (1.0, LARANJA_CL, LARANJA)]

# ---------------- materiais sólidos ----------------
def mat_cor(cor_fn, **kw):
    def f(c):
        base = cor_fn(c["p"], c["face"])
        return None if base is None else tom(base, g.contexto_luz(c, **kw))
    return f

def mat_ouro(c):
    """Ouro facetado (chifres, coroa, contas, pingentes): topo claro, frente amarela, lados ouro, embaixo escuro."""
    face = c["face"]
    base = {"up": AMARELO_CL, "down": OURO_ESC, "north": AMARELO, "south": OURO}.get(face, mix(AMARELO, OURO, 0.5))
    return contorno(base, 0.3) if na_borda(c) else base

def mat_roxo(c, frente=ROXO):
    """Armadura roxa facetada: topo lilás, frente roxo, lados roxo mais fundo, baixo roxo escuro, quinas escuras."""
    face = c["face"]
    base = {"up": LILAS, "down": ROXO_ESC, "north": frente}.get(face, mix(ROXO, ROXO_ESC, 0.25))
    return mix(base, ROXO_FUNDO, 0.45) if na_borda(c) else base

def mundo(mat, rot, pivo):
    """Pinta uma peça girada pelo ponto já girado (o desenho fica no plano do mundo)."""
    A = _rotm(*rot)
    def f(c):
        c2 = dict(c); c2["p"] = girar_ponto(c["p"], A, pivo)
        return mat(c2)
    return f

# ================= CABEÇA =================
CY0, CY1 = 28.8, 35.4            # queixo .. alto do crânio (o elmo fica por cima)
ZF = -9.6                        # frente da cara (base do bico)
ZT = -2.8                        # nuca
FRENTE_X = 1.3
FAC_ANG = 40
FAC_L, FAC_T = 3.8, 1.2
_tx, _tz = math.sin(math.radians(FAC_ANG)), math.cos(math.radians(FAC_ANG))
_nx, _nz = math.cos(math.radians(FAC_ANG)), -math.sin(math.radians(FAC_ANG))
LX = FRENTE_X + FAC_L * _tx
ZL = ZF + FAC_L * _tz
FAC_S = (FRENTE_X + _tx * FAC_L / 2, ZF + _tz * FAC_L / 2)
FAC_C = (FAC_S[0] - _nx * FAC_T / 2, FAC_S[1] - _nz * FAC_T / 2)
OLHO_Y = 32.2
OLHO_RU, OLHO_RV = 1.5, 1.15
OLHO_CORTE0, OLHO_CORTE_INC = 0.40, 0.30     # pálpebra brava: corta o topo numa diagonal que desce para o bico

def olho(u, v):
    """Olho vermelho bravo (ficha, expressão neutra): mais largo que alto, a viseira corta o alto numa diagonal que desce
    para o bico; íris vermelha grande, pupila escura do lado do bico e 1 brilho; esclera creme só atrás.
    u: ao longo da face (negativo = para o bico); v: para cima."""
    ru, rv = OLHO_RU, OLHO_RV
    uu = u / ru
    if abs(uu) > 1: return None
    corte = OLHO_CORTE0 + OLHO_CORTE_INC * u
    baixo = -rv * (0.86 - 0.12 * uu) * (1 - max(0.0, -uu) ** 2.4)
    cima = rv * (0.98 - 0.06 * uu) * (1 - max(0.0, -uu) ** 1.8)
    topo = min(cima, corte)
    if v < baixo or v > topo: return None
    if topo - v < 0.15: return PRETO                                       # fio da pálpebra
    ic = -0.12
    du = (uu - ic) / 0.74; dv = v / (rv * 0.96)
    if du * du + dv * dv <= 1 or (uu < ic and v >= baixo):
        if ((uu + 0.3) / 0.2) ** 2 + ((v + 0.05) / 0.55) ** 2 <= 1: return PRETO                 # pupila
        if ((uu + 0.05) / 0.13) ** 2 + ((v - topo + 0.38) / 0.17) ** 2 <= 1: return (255, 250, 240)   # brilho
        cor = VERM if v < topo - 0.45 else mix(VERM, VERM_ESC, 0.7)          # sombra da viseira no alto da íris
        if du * du + dv * dv > 0.8 and uu > ic: cor = VERM_ESC
        return cor
    return CREME if topo - v > 0.3 else CREME_SOMBRA

def cor_cabeca(p, face):
    """Crânio: creme no rosto e na garganta, roxo do elmo no alto e atrás (por baixo das placas), vermelho na nuca."""
    x, y, z = p
    if face == "up" or y > 33.6: return ROXO
    if z > -4.4: return VERM_ESC
    return CREME

def mat_rosto(c):
    """Rosto creme chapado (sem a sombra da luz contínua, que deixava o branco cinza): só a face de baixo mais escura."""
    cor = cor_cabeca(c["p"], c["face"])
    if c["face"] == "down": return CREME_SOMBRA if cor == CREME else contorno(cor, 0.3)
    return cor

def mat_faceta(lado):
    base = mat_rosto
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        u, v = z - FAC_C[1] - 0.1, y - OLHO_Y
        if c["face"] == fora:
            cor = olho(u, v)
            if cor is not None: return cor
            if v > OLHO_CORTE0 + OLHO_CORTE_INC * u + 0.1: return ROXO      # viseira desce sobre o olho
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face == "down": return OURO_ESC
    if face == "up": return AMARELO_CL
    if face in ("east", "west") and abs(z - (ZF - 1.7)) < 0.3 and abs(y - 31.55) < 0.24: return (120, 50, 10)   # narina
    if face == "north":
        larg = 0.3 + 0.8 * clamp((y - 29.6) / 2.4)
        return mix(AMARELO_CL, AMARELO, clamp((31.9 - y) / 1.6)) if abs(x) < larg else OURO
    return mix(AMARELO_CL, AMARELO, clamp((32.0 - y) / 1.0)) if y > 30.9 else mix(AMARELO, OURO, clamp((30.9 - y) / 1.2))

def mat_gema(cx, cy, W, H):
    """Gema da testa: hexágono alto (pontas em cima e embaixo) com moldura de ouro e gema vermelha facetada."""
    meio = (H - W) / 2
    def f(c):
        x, y, z = c["p"]
        if c["face"] != "north": return mat_ouro(c)
        u = (x - cx) / (W / 2); v = (y - cy)
        lim = 1.0 if abs(v) <= meio else max(0.0, 1.0 - (abs(v) - meio) / (W / 2))
        borda = lim - abs(u)
        if borda < 0.1: return OURO_ESC
        if borda < 0.36: return AMARELO_CL if (u < 0 and v > 0) else (AMARELO if v > -meio else OURO)
        if (u + 0.2) ** 2 + ((v - 0.6) / 1.6) ** 2 < 0.03: return (255, 225, 215)
        if u < 0 and v > 0: return (246, 86, 70)
        if u > 0 and v < 0: return VERM_ESC
        return VERM
    return f

def so_gema(c, cor): return cor[0] > 140 and cor[1] < 110 and cor[2] < 110

def hexagono(nome, centro, W, H, esp, mat, res=8, brilho=False, plano="x"):
    """Hexágono alto (retângulo + 2 quadrados girados 45° nas pontas). plano='x': face larga para a frente (-z)."""
    cx, cy, cz = centro
    meio = (H - W) / 2; q = W / 1.4142
    pcs = [peca(nome, [cx - W / 2, cy - meio, cz - esp / 2], [cx + W / 2, cy + meio, cz + esp / 2], mat, res=res, brilho=brilho)]
    for nm, yy in ((nome + "_cima", cy + meio), (nome + "_baixo", cy - meio)):
        rot = (0, 0, 45); piv = (cx, yy, cz)
        pcs.append(peca(nm, [cx - q / 2, yy - q / 2, cz - esp / 2 + 0.03], [cx + q / 2, yy + q / 2, cz + esp / 2 - 0.03],
                        mundo(mat, rot, piv), rot=rot, pivo=piv, res=res, brilho=brilho))
    return pcs

def chifre(nome, base, d, n, segs, curva, dobra):
    """Chifre de ouro: segmentos facetados que afinam (pluma com material de ouro)."""
    x, y0, z = base
    A0 = quadro(d, n)
    ez = _col(A0, 2)
    rx = -abs(curva) * (1 if _dot(ez, dobra) >= 0 else -1)
    def seg(k, ytop):
        L, W, T = segs[k]
        pcs = [peca(f"{nome}_{k}", [x - T / 2, ytop - L, z - W / 2], [x + T / 2, ytop + (0.3 if k else 0.0), z + W / 2], mat_ouro, res=3)]
        if k + 1 < len(segs): pcs.append(seg(k + 1, ytop - L))
        else:
            s = W / 1.4142
            pcs.append(peca(f"{nome}_pt", [x - T / 2 + 0.03, ytop - L - s / 2, z - s / 2], [x + T / 2 - 0.03, ytop - L + s / 2, z + s / 2],
                            mat_ouro, rot=(45, 0, 0), pivo=(x, ytop - L, z), res=3))
        return osso(f"{nome}_{k}", [x, ytop, z], euler(A0) if k == 0 else [rx, 0, 0], pcs)
    return seg(0, y0)

def cabeca_ossos():
    cab = []
    mc = mat_rosto
    fx = (CY0, CY1)
    # crânio: volume chanfrado atrás + frente estreita; as facetas diagonais (com o olho) fecham a quina
    cab += g.arredondado2("cranio", [-LX, CY0, ZL - 0.4], [LX, CY1, ZT], mc, r=1.4, faixa=fx, res=3)
    cab += g.arredondado("cranio_frente", [-FRENTE_X - 0.3, CY0 + 0.2, ZF], [FRENTE_X + 0.3, CY1 - 1.0, ZL + 0.5], mc, r=0.5, faixa=fx, res=3)
    # queixo e garganta creme (afinam para trás embaixo do bico)
    mcr = lambda c: CREME if c["face"] != "down" else CREME_SOMBRA
    cab += g.arredondado("queixo", [-2.3, CY0 - 0.6, ZF + 0.6], [2.3, 30.6, ZL + 3.0], mcr, r=0.6, res=3)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, CY0 + 0.3, cz - FAC_L / 2], [cx + FAC_T / 2, CY1 - 0.6, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, FAC_ANG * lado, 0), pivo=(cx, OLHO_Y, cz), faixa=fx, res=8))
        # viseira do elmo: barra roxa grossa sobre o olho, descendo para o bico (o V bravo da ficha)
        ox0, ox1 = sorted((cx + FAC_T / 2 * lado - 0.5 * lado, cx + FAC_T / 2 * lado + 0.7 * lado))
        ang = math.degrees(math.atan(OLHO_CORTE_INC))
        zc0 = cz + 0.1
        yb = OLHO_Y + OLHO_CORTE0 + 0.12
        def mvis(c):
            if c["face"] == "down": return ROXO_FUNDO
            return mat_roxo(c, frente=ROXO)
        cab.append(osso("viseira_" + s, [cx, yb, zc0], [0, FAC_ANG * lado, 0], [
            peca("viseira_" + s, [ox0, yb, cz - FAC_L / 2 - 0.4], [ox1, yb + 1.5, cz + FAC_L / 2 + 0.6],
                 mvis, rot=(-ang, 0, 0), pivo=(cx, yb, zc0), res=4)]))
        # guarda da bochecha: barra roxa vertical logo atrás do olho, do elmo até o queixo
        bx0, bx1 = sorted(((LX - 0.35) * lado, (LX + 0.5) * lado))
        cab.append(peca("elmo_guarda_" + s, [bx0, 29.4, ZL + 0.5], [bx1, 34.2, ZL + 2.4],
                        lambda c: mat_roxo(c, frente=LILAS), res=4))
        # placa do lado do elmo atrás da guarda (a juba sai por trás dela)
        lx0, lx1 = sorted(((LX - 0.3) * lado, (LX + 0.3) * lado))
        cab.append(peca("elmo_lado_" + s, [lx0, 31.4, ZL + 2.3], [lx1, 34.8, ZT + 0.2], mat_roxo, res=3))
    # casca do elmo (alto da cabeça) e ponte do nariz (o V da viseira encontra a base do bico)
    cab += g.arredondado("elmo_topo", [-LX - 0.35, 33.6, ZF - 0.4], [LX + 0.35, 36.0, ZT + 0.4], mat_roxo, r=0.5, res=3)
    cab.append(peca("elmo_ponte", [-1.0, 32.6, ZF - 0.55], [1.0, 34.0, ZF + 1.2], mat_roxo, res=4))
    # coroa: faixa dourada pela testa e pelos lados
    cab.append(peca("coroa_frente", [-LX - 0.45, 35.0, ZF - 0.9], [LX + 0.45, 36.2, ZF - 0.35], mat_ouro, res=4))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted(((LX + 0.2) * lado, (LX + 0.6) * lado))
        cab.append(peca("coroa_lado_" + s, [x0, 35.0, ZF - 0.9], [x1, 36.2, ZF + 3.6], mat_ouro, res=4))
    # gema em moldura de ouro (hexágono alto) no meio da testa, subindo acima do elmo
    gx, gy, gz, GW, GH = 0.0, 36.3, ZF - 1.25, 2.6, 4.4
    cab += hexagono("gema", (gx, gy, gz), GW, GH, 1.0, mat_gema(gx, gy, GW, GH), res=8, brilho=so_gema)
    # bico curvo: base alta (tampa + quilha em V de frente), meio que cai e gancho; mandíbula curta embaixo
    mb = mat_cor(cor_bico, borda=.05, curva=.25)
    def mq(c):
        f_ = c["face"]
        cor = AMARELO_CL if f_ in ("up", "east") else (AMARELO if f_ in ("north", "south") else mix(AMARELO, OURO, 0.4))
        return contorno(cor, 0.25) if na_borda(c) else cor
    fb = (29.4, 32.4)
    # base: tampa reta + quilha em V (de frente o bico é uma cunha que afina para baixo)
    cab.append(peca("bico_tampa", [-1.3, 31.0, ZF - 2.3], [1.3, 32.4, ZF + 0.7], mb, faixa=fb, res=4))
    q = 1.3 * 1.4142
    cab.append(peca("bico_quilha", [-q / 2, 31.0 - q / 2, ZF - 2.2], [q / 2, 31.0 + q / 2, ZF + 0.6], mq, rot=(0, 0, 45),
                    pivo=(0, 31.0, ZF), faixa=fb, res=4))
    # meio: menor e já caindo (mesmo pivô para a tampa e a quilha)
    piv = (0, 32.2, ZF - 2.1)
    cab.append(peca("bico_meio", [-1.0, 30.9, ZF - 4.1], [1.0, 32.2, ZF - 1.9], mb, rot=(-14, 0, 0), pivo=piv, faixa=fb, res=4))
    q = 1.0 * 1.4142
    cab.append(peca("bico_quilha2", [-q / 2, 30.9 - q / 2, ZF - 4.0], [q / 2, 30.9 + q / 2, ZF - 2.0], mq, rot=(-14, 0, 45),
                    pivo=(0, 30.9, ZF - 2.0), faixa=fb, res=4))
    # gancho: ponta estreita que desce
    cab.append(peca("bico_gancho", [-0.6, 29.7, ZF - 5.3], [0.6, 31.5, ZF - 3.7],
                    mat_cor(lambda p, f_: AMARELO_CL if f_ == "up" else mix(AMARELO, OURO, clamp((31.0 - p[1]) / 1.2)), borda=.1, curva=.2),
                    rot=(-38, 0, 0), pivo=(0, 31.5, ZF - 3.7), faixa=(29.7, 31.5), res=4))
    cab.append(peca("bico_baixo", [-0.85, 29.5, ZF - 2.6], [0.85, 30.4, ZF + 0.5],
                    mat_cor(lambda p, f_: (150, 60, 8) if (f_ != "down" and p[1] > 30.2) else OURO, borda=.08), res=4))
    cab.append(crista_ossos())
    cab += juba_ossos()
    return cab

def crista_ossos():
    """Crista e chifres: 2 chifres grandes de ouro que sobem dos lados da coroa curvando para trás, 1 pequeno acima
    da gema e a chama vermelha da crista entre eles."""
    pc = []
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        pc.append(chifre("chifre_" + s, ((LX + 0.35) * lado, 35.6, ZF + 1.6), (0.16 * lado, 1.0, 0.12), (lado, 0, 0),
                         [(3.6, 2.0, 1.8), (3.4, 1.7, 1.5), (2.8, 1.3, 1.2)], 13, (0, 0, 1)))
    pc.append(chifre("chifre_meio", (0.0, 38.0, ZF - 1.0), (0, 1.0, 0.25), (1, 0, 0), [(1.3, 1.2, 0.9)], 0, (0, 0, 1)))
    for k, (x, y, z, d, L) in enumerate([(0.0, 35.6, -6.6, (0, 1.0, 0.45), 6.6), (-1.3, 35.4, -5.6, (-0.2, 1.0, 0.55), 5.6),
                                         (1.3, 35.4, -5.6, (0.2, 1.0, 0.55), 5.6)]):
        pc.append(pluma(f"crista{k}", (x, y, z), d, (1, 0, 0), [(L * 0.5, 2.6, 1.1), (L * 0.32, 2.0, 0.9)], 14, F_CRISTA,
                        dobra=(0, 0, 1)))
    return osso("crista", [0, 35.8, -6.0], [0, 0, 0], pc)

# juba de chamas: (x, y, z da raiz, direção, comprimento, largura, faixas, dobra da ponta)
JUBA = [
    ((1.5, 35.6, -4.4), (0.14, 0.80, 0.58), 9.6, 3.8, F_JUBA),
    ((2.7, 34.4, -3.8), (0.22, 0.45, 0.86), 10.4, 4.0, F_JUBA),
    ((3.2, 32.6, -3.4), (0.24, 0.12, 0.96), 10.2, 4.0, F_JUBA),
    ((3.2, 30.6, -3.4), (0.24, -0.30, 0.92), 8.8, 3.8, F_JUBA_ESC),
    ((3.5, 29.8, -5.4), (0.62, -0.60, 0.45), 5.2, 2.8, F_JUBA_ESC),       # costeleta: emoldura o rosto de frente
]
JUBA_MEIO = [((0.0, 35.2, -2.8), (0.0, 0.58, 0.82), 10.8, 4.2, F_JUBA),
             ((0.0, 32.6, -2.4), (0.0, 0.08, 1.0), 10.2, 4.2, F_JUBA),
             ((0.0, 29.8, -2.8), (0.0, -0.5, 0.86), 7.8, 4.0, F_JUBA_ESC)]

def juba_ossos():
    """Juba de chamas em camadas: penas largas que varrem para trás e para cima a partir da nuca (pouca abertura para
    os lados, nada de 'porco-espinho'), a ponta dobrando para cima como uma labareda."""
    pc = []
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        for k, ((x, y, z), (dx, dy, dz), L, W, fx) in enumerate(JUBA):
            n = (lado, 0.0, 0.15 if k < 4 else -0.4)
            pc.append(pluma(f"juba{k}_{s}", (x * lado, y, z), (dx * lado, dy, dz), n, [(L * 0.46, W, 1.2), (L * 0.3, W * 0.7, 1.0)],
                            16, fx, dobra=(0, 1, 0)))
    for k, ((x, y, z), d, L, W, fx) in enumerate(JUBA_MEIO):
        pc.append(pluma(f"nuca{k}", (x, y, z), d, (1, 0, 0), [(L * 0.46, W, 1.3), (L * 0.3, W * 0.7, 1.1)], 14, fx, dobra=(0, 1, 0)))
    return pc

# ================= PESCOÇO, TRONCO E PEITORAL =================
def cor_tronco(p, face):
    x, y, z = p
    a = z if face in ("east", "west") else x
    fila = math.floor(y / 1.8)
    fa = ((a + (fila % 2) * 1.2) % 2.4) / 2.4
    if face != "up" and (y % 1.8) / 1.8 < 0.14 + 0.12 * (2 * abs(fa - 0.5)) ** 2: return VERM_FUNDO
    return VERM_ESC

def fenix(x, y, e=0.0):
    """Emblema da fênix do peitoral (quadro "Peitoral Fênix"): asas em V bem abertas com 3 pontas de chama no alto de
    cada uma, cabeça pequena no meio e o corpo descendo em ponta. 'e' encolhe a forma (para as camadas de cor)."""
    ax = abs(x)
    # asas: faixa entre a borda de baixo (sobe para fora) e a de cima (com as pontas de chama)
    if ax <= 3.75 - e:
        baixo = 20.0 + 0.95 * max(0.0, ax - 0.4) + e
        dente = 0.55 * abs(((ax * 1.15) % 1.0) - 0.5) * 2 if ax > 1.4 else 0.0
        cima = 22.6 + 0.62 * ax - dente - e
        if baixo <= y <= min(cima, 24.6 - e): return True
    # corpo e cauda em ponta para baixo
    if 18.1 + e * 1.6 <= y <= 22.4 - e and ax <= 0.42 * (y - 18.1) - e * 0.6: return True
    # cabeça
    if ax ** 2 + (y - 23.0) ** 2 <= (0.62 - e) ** 2: return True
    return False

def mat_peitoral(c):
    """Placa de cima do peitoral: roxo com fio lilás na beirada e a fênix (contorno vermelho, laranja e miolo amarelo)."""
    x, y, z = c["p"]
    if c["face"] != "north": return mat_roxo(c)
    if fenix(x, y):
        if not fenix(x, y, 0.3): return VERM
        if not fenix(x, y, 0.62): return LARANJA
        return AMARELO
    if na_borda(c): return ROXO_FUNDO
    return ROXO

def mat_v_lilas(c):
    """Camada de baixo em V (lilás) com a divisa dourada (a cauda da fênix) no meio."""
    x, y, z = c["p"]
    if c["face"] != "north":
        return mat_roxo(c, frente=LILAS)
    ax = abs(x)
    yv = 16.3 + ax                     # linha da divisa (V)
    if na_borda(c): return mix(ROXO, ROXO_FUNDO, 0.4)
    if yv - 0.05 <= y <= yv + 0.75 and ax < 3.0: return AMARELO if y > yv + 0.3 else OURO
    return LILAS

def tronco_ossos():
    pcs = []
    mt = mat_cor(cor_tronco, borda=.0, curva=.25)
    pcs += g.arredondado2("tronco", [-5.0, 13.0, -8.3], [5.0, 25.2, 2.0], mt, r=2.0, faixa=(12, 26), res=2)
    pcs += g.arredondado("tronco_tras", [-4.4, 12.4, 0.5], [4.4, 21.6, 8.4], mt, r=1.5, faixa=(12, 22), res=2)
    pcs += g.arredondado("uropigio", [-2.8, 17.8, 6.2], [2.8, 23.2, 10.6], mt, r=1.0, res=2)
    # peitoral: placa de cima (retângulo + losango embaixo = escudo de 5 lados) com a fênix
    zf = -9.45
    pcs.append(peca("peitoral", [-4.3, 21.4, zf], [4.3, 25.2, zf + 1.4], mat_peitoral, res=8))
    s = 4.3 * 1.4142
    rot = (0, 0, 45); piv = (0.0, 21.4, zf + 0.7)
    pcs.append(peca("peitoral_v", [-s / 2, 21.4 - s / 2, zf + 0.1], [s / 2, 21.4 + s / 2, zf + 1.3], mundo(mat_peitoral, rot, piv),
                    rot=rot, pivo=piv, res=8))
    # camada de baixo em V, lilás, um pouco atrás
    s2 = 4.55 * 1.4142
    piv2 = (0.0, 20.0, zf + 1.0)
    pcs.append(peca("peitoral_v2", [-s2 / 2, 20.0 - s2 / 2, zf + 0.45], [s2 / 2, 20.0 + s2 / 2, zf + 1.6], mundo(mat_v_lilas, rot, piv2),
                    rot=rot, pivo=piv2, res=8))
    # gola facetada no alto do peitoral (losango roxo que aponta para baixo, entre as penas do pescoço)
    q = 1.5 * 1.4142
    piv3 = (0.0, 25.0, zf - 0.1)
    pcs.append(peca("peitoral_gola", [-q / 2, 25.0 - q / 2, zf - 0.6], [q / 2, 25.0 + q / 2, zf + 0.9],
                    lambda c: mat_roxo(c, frente=mix(ROXO, LILAS, 0.45)), rot=rot, pivo=piv3, res=6))
    # penas da barriga: 2 fileiras viradas para a frente (vermelho com ponta laranja; laranja com ponta amarela)
    for k, x in enumerate((-3.6, -1.2, 1.2, 3.6)):
        pcs.append(pena(f"barriga0_{k}", (x, 18.8, -8.0 + 0.25 * (k % 2)), (0.1 * x, -1.0, 0.2), (0.1 * x, 0, -1.0), 7.4, 3.0, 1.0, F_VERM))
    for k, x in enumerate((-2.5, 0.0, 2.5)):
        pcs.append(pena(f"barriga1_{k}", (x, 15.6, -7.2 - 0.2 * (k % 2)), (0.12 * x, -1.0, 0.25), (0.1 * x, 0, -1.0), 7.0, 3.2, 1.0, F_LAR))
    # costas: penas vermelho-escuras deitadas para trás (de costas leem como a faixa escura do meio)
    for k, (x, y, z, L) in enumerate(((-1.6, 24.6, 0.6, 7.4), (1.6, 24.6, 0.6, 7.4), (0.0, 24.8, -0.6, 8.0),
                                      (-1.4, 21.6, 4.4, 6.4), (1.4, 21.6, 4.4, 6.4))):
        pcs.append(pena(f"costas{k}", (x, y, z), (0.1 * x, -0.45, 1.0), (0, 1, 0.2), L, 3.2, 1.0, F_VERM_ESC if k < 3 else F_JUBA_ESC))
    return pcs

def pescoco_ossos():
    pc = []
    def cor_pesc(p, f_):
        x, y, z = p
        if f_ == "north" or z < -6.2: return CREME
        return VERM_ESC if z > -4.0 else VERM
    mp = mat_cor(cor_pesc, borda=.0, curva=.25)
    pc += g.octogono("pescoco", [-2.5, 23.6, -7.6], [2.5, 30.6, -2.8], mp, r=0.9, faixa=(23, 31))
    # garganta creme: cunha do queixo até a gola do peitoral, com as pontas das penas brancas embaixo
    def cor_garg(c):
        x, y, z = c["p"]; face = c["face"]
        if face == "down": return CREME_SOMBRA
        if face == "north":
            # pontas das penas brancas por cima da gola do peitoral (borda de baixo em dentes)
            dente = 0.7 * abs(((x * 0.9) % 1.0) - 0.5) * 2
            if y < 25.2 + dente: return CREME_SOMBRA
        return CREME
    pc += g.arredondado("garganta", [-2.0, 24.6, -8.9], [2.0, 29.6, -6.6], cor_garg, r=0.5, res=4)
    # gola de penas vermelhas: desce do pescoço sobre os ombros, dos lados da garganta (face larga para a frente)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        for k, (x, z, d, n, L) in enumerate(((2.4, -7.0, (0.5, -1.0, -0.1), (0.5, 0, -1.0), 5.4),
                                             (3.0, -5.2, (0.65, -1.0, 0.15), (1.0, 0, -0.6), 5.8),
                                             (2.8, -3.4, (0.55, -1.0, 0.55), (1.0, 0, 0.2), 5.6))):
            pc.append(pena(f"gola{k}_{s}", (x * lado, 27.8, z), (d[0] * lado, d[1], d[2]), (n[0] * lado, n[1], n[2]), L, 2.8, 1.0,
                           F_JUBA_ESC))
    return pc

# ================= CAPA DE ASAS =================
# fileiras de cima para baixo: (y da raiz, ângulos no anel, raio x, raio z, comprimento, largura, abertura, varrida, faixas)
ASA = [
    (25.4, (-50, -22, 6, 34), 4.6, 5.6, 8.0, 3.4, 56, 14, F_LILAS),
    (24.0, (-58, -32, -6, 20, 46, 70), 4.9, 6.0, 9.6, 3.4, 50, 20, F_ROXO),
    (22.2, (-62, -38, -14, 10, 34, 58, 80), 5.1, 6.4, 11.4, 3.6, 46, 26, F_VERM),
    (20.4, (-60, -36, -12, 12, 36, 60, 82), 5.2, 6.6, 14.0, 4.0, 45, 30, F_LAR),
    (18.8, (-56, -32, -8, 16, 40, 64, 86), 5.2, 6.6, 15.6, 4.0, 46, 34, F_AMAR),
]
ASA_ZC = -0.4

def asa_ossos(lado):
    """Asa caída como capa: 5 fileiras em telha, cada uma de uma cor (lilás, roxo, vermelho, laranja, amarelo). As
    pontas abrem para fora como um sino (de frente, a capa em A da ficha) e varrem para trás (de lado, asa dobrada de
    galo); a fileira de baixo acaba acima das pernas, deixando a canela dourada à mostra."""
    s = "d" if lado < 0 else "e"
    pcs = []
    for f, (y, phis, ax, az, L, W, abre, varre, fx) in enumerate(ASA):
        ta, tv = math.tan(math.radians(abre)), math.tan(math.radians(varre))
        for k, phi in enumerate(phis):
            r = math.radians(phi)
            x, z = lado * ax * math.cos(r), ASA_ZC + az * math.sin(r)
            nrm = (lado * math.cos(r), 0.0, math.sin(r))
            # abre no sentido radial (menos na frente), e a varrida leva todas as pontas para trás
            d = (lado * math.cos(r) * ta, -1.0, max(0.0, math.sin(r)) * ta * 0.6 + tv)
            pcs.append(pena(f"asa{f}_{k}_{s}", (x, y - 0.3 * (k % 2), z), d, nrm, L, W, 1.15, fx))
    return osso("asa_" + s, [4.8 * lado, 24.6, -1.0], [0, 0, 0], pcs)

# ================= CAUDA E CORRENTES =================
RAIZ_CAUDA = (0.0, 20.6, 8.6)
# plumas em foice: (nome, raiz, direção inicial, segmentos (comprimento, largura, espessura), dobra por junta, faixas)
F_CAUDA_AMAR = [(0.34, LARANJA_CL, LARANJA), (1.0, AMARELO, OURO)]
def _pl(ang, lat):
    """Direção inicial de uma pluma: 'ang' graus acima da horizontal (para trás) e um pouco para o lado."""
    a = math.radians(ang)
    return (lat, math.sin(a), math.cos(a))
_SEG = lambda k: [(5.0 * k, 4.4, 1.2), (4.4 * k, 3.6, 1.1), (3.6 * k, 2.6, 1.0)]
# leque vertical de foices (como as plumas de um galo): todas no plano do meio, alternando um pouco de lado, da mais
# alta (quase em pé) à mais baixa (deitada), cada uma curvando para trás e para baixo na ponta
PLUMAS = [
    ("pluma0", (0.0, 22.4, 9.0), _pl(74, 0.0), _SEG(1.0), 30, F_CAUDA_AM),
    ("pluma1", (-0.8, 22.0, 9.4), _pl(60, -0.10), _SEG(1.0), 28, F_CAUDA_V),
    ("pluma2", (0.8, 21.6, 9.6), _pl(46, 0.10), _SEG(0.98), 26, F_CAUDA_AM),
    ("pluma3", (-0.8, 21.0, 9.8), _pl(33, -0.16), _SEG(0.95), 24, F_CAUDA_E),
    ("pluma4", (0.8, 20.4, 9.8), _pl(21, 0.16), _SEG(0.92), 22, F_CAUDA_V),
    ("pluma5", (-0.8, 19.8, 9.6), _pl(9, -0.22), _SEG(0.88), 18, F_CAUDA_AMAR),
    ("pluma6", (0.8, 19.4, 9.4), _pl(-3, 0.22), _SEG(0.84), 16, F_CAUDA_AMAR),
]
N_CONTAS = 8
PASSO = 2.4
CORRENTES = [("corrente_d", (-2.0, 18.4, 10.6), (-0.22, -0.10, 0.97), -1),
             ("corrente_c", (0.0, 18.0, 11.0), (0.0, -0.18, 0.98), 1),
             ("corrente_e", (2.0, 18.4, 10.6), (0.22, -0.10, 0.97), 1)]
ONDAS = ([(n, N_CONTAS, (3.0, 2.0, 1.5)) for n, _, _, _ in CORRENTES]
         + [(p[0], len(p[3]), (2.0, 1.5, 0.0)) for p in PLUMAS])
ANIM_PARADO = {f"{n}_pingente": [(0, 0, 0), (4, 0, 7 * s_), (0, 0, 0), (-4, 0, -7 * s_), (0, 0, 0)]
               for (n, _, _, _), s_ in zip(CORRENTES, (1, -1, 1))}
ANIM_ANDANDO = {f"{n}_pingente": [(0, 0, 0), (8, 0, 10 * s_), (0, 0, 0), (-8, 0, -10 * s_), (0, 0, 0)]
                for (n, _, _, _), s_ in zip(CORRENTES, (1, -1, 1))}

def mat_conta(cx, cy, cz):
    """Conta octogonal de ouro: faces claras em cima, ouro dos lados, escuro embaixo, quinas escuras."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        if face == "up": base = AMARELO_CL
        elif face == "down": base = OURO_ESC
        else: base = AMARELO if y > cy + 0.15 else mix(AMARELO, OURO, 0.7)
        return contorno(base, 0.3) if na_borda(c) else base
    return f

def mat_pingente(cx, cy, cz, W, H):
    """Pingente: losango alto com moldura de ouro (clara em cima, escura embaixo) e gema vermelha facetada."""
    meio = (H - W) / 2
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        if face not in ("east", "west"): return mat_ouro(c)
        u = (z - cz) / (W / 2); v = y - cy
        lim = 1.0 if abs(v) <= meio else max(0.0, 1.0 - (abs(v) - meio) / (W / 2))
        borda = lim - abs(u)
        if borda < 0.1: return OURO_ESC
        if borda < 0.42: return AMARELO_CL if v > 0.3 else (AMARELO if v > -0.6 else OURO)
        if borda < 0.5: return OURO_ESC
        if (u + 0.15) ** 2 + ((v - 0.5) / 1.5) ** 2 < 0.025: return (255, 225, 215)
        if u < 0 and v > 0: return (246, 86, 70)
        if u > 0 and v < 0: return VERM_ESC
        return VERM
    return f

def corrente(nome, raiz, d0, normal, sx=1):
    """Corrente de contas de ouro (um osso por conta, '<nome>_k'): sai para trás e para baixo e vai ficando a prumo;
    no fim, o pingente em losango (osso '<nome>_pingente') pende na vertical."""
    x, y0, z = raiz
    dirs = []
    for k in range(N_CONTAS):
        f = (k / (N_CONTAS - 1)) ** 0.9
        dirs.append(_n(tuple(d0[i] * (1 - f) + (0.0, -1.0, 0.05)[i] * f for i in range(3))))
    quadros = [quadro(dk, normal) for dk in dirs]
    q_fim = quadro((0, -1, 0), _n((1.0, 0.0, 0.45 * sx)))
    def conta(k):
        yt = y0 - k * PASSO
        esc = 1.0 - 0.03 * k
        R, r = 1.12 * esc, 0.7 * esc
        cy = yt - PASSO / 2
        m = mat_conta(x, cy, z)
        pcs = [peca(f"{nome}_{k}", [x - R, cy - R, z - r], [x + R, cy + R, z + r], m, res=4),
               peca(f"{nome}_{k}b", [x - r, cy - R, z - R], [x + r, cy + R, z + R], m, res=4),
               peca(f"{nome}_{k}c", [x - 0.32, yt - PASSO - 0.15, z - 0.32], [x + 0.32, yt + 0.15, z + 0.32], mat_ouro, res=3)]
        if k + 1 < N_CONTAS:
            pcs.append(conta(k + 1))
        else:
            pcs.append(pingente(nome, (x, yt - PASSO, z), _t(quadros[-1]), q_fim))
        rel = quadros[0] if k == 0 else _mm(_t(quadros[k - 1]), quadros[k])
        return osso(f"{nome}_{k}", [x, yt, z], euler(rel), pcs)
    return conta(0)

def pingente(nome, topo, inv_ant, q_fim):
    x, y, z = topo
    W, H, esp = 3.8, 5.6, 1.1
    cy = y - 0.5 - H / 2
    m = mat_pingente(x, cy, z, W, H)
    meio = (H - W) / 2; q = W / 1.4142
    pcs = [peca(f"{nome}_argola", [x - 0.4, cy + H / 2 - 0.3, z - 0.4], [x + 0.4, y + 0.1, z + 0.4], mat_ouro, res=3),
           peca(f"{nome}_pingente", [x - esp / 2, cy - meio, z - W / 2], [x + esp / 2, cy + meio, z + W / 2], m, res=6, brilho=so_gema)]
    for nm, yy in (("_pc", cy + meio), ("_pb", cy - meio)):
        rot = (45, 0, 0); piv = (x, yy, z)
        pcs.append(peca(f"{nome}{nm}", [x - esp / 2 + 0.03, yy - q / 2, z - q / 2], [x + esp / 2 - 0.03, yy + q / 2, z + q / 2],
                        mundo(m, rot, piv), rot=rot, pivo=piv, res=6, brilho=so_gema))
    return osso(f"{nome}_pingente", [x, y, z], euler(_mm(inv_ant, q_fim)), pcs)

def cauda_ossos():
    pc = []
    for nome, raiz, d, segs, curva, fx in PLUMAS:
        pc.append(pluma(nome, raiz, d, (1.0, 0.0, 0.0), segs, curva, fx, dobra=(0, -0.5, 1.0), lingua=0.08))
    for nome, raiz, d0, sx in CORRENTES:
        pc.append(corrente(nome, raiz, d0, (1.0, 0.0, 0.0), sx))
    return osso("cauda", list(RAIZ_CAUDA), [0, 0, 0], pc)

# ================= PERNAS =================
def cor_tarso(p, face):
    """Canela dourada com escamas em faixas horizontais."""
    if face == "down": return OURO_ESC
    if face == "up": return AMARELO_CL
    f = (p[1] % 1.1) / 1.1
    if f < 0.16: return mix(AMARELO, OURO, 0.8)
    return AMARELO

def mat_caneleira(y0, y1, cima, corpo):
    """Faixa da caneleira: aro de cima ('cima'), corpo ('corpo') e fio escuro embaixo."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        if face == "up": return cima
        if face == "down": return ROXO_FUNDO
        if y > y1 - 0.55: base = cima
        elif y < y0 + 0.22: base = ROXO_ESC
        else: base = corpo
        if face in ("east", "west", "south"): base = mix(base, ROXO_ESC, 0.2)
        return base
    return f

def perna(lado):
    s = "d" if lado < 0 else "e"; xc = 3.0 * lado; zc = 0.4
    pp = []
    # coxa emplumada curta (some sob as penas da barriga e da capa) com a borda em pontas de chama
    def cor_coxa(p, f_):
        x, y, z = p
        a = z if f_ in ("east", "west") else x
        dente = 0.5 * abs(((a * 0.8) % 1.0) - 0.5) * 2
        if y < 10.3 + dente: return LARANJA
        return VERM_ESC if (y % 1.6) > 0.3 else VERM_FUNDO
    pp += g.arredondado("coxa_" + s, [xc - 2.0, 10.2, zc - 2.2], [xc + 2.0, 14.6, zc + 2.0], mat_cor(cor_coxa, borda=.0, curva=.25),
                        r=0.8, res=3)
    # "calça" de penas da coxa: cobre o alto da canela e emenda com a barra da capa (acaba acima da caneleira)
    for k, phi in enumerate((-80, -10, 60, 130)):
        r_ = math.radians(phi)
        nrm = (math.cos(r_) * lado, 0.0, math.sin(r_))
        raiz = (xc + 1.5 * nrm[0], 12.8, zc + 1.5 * nrm[2])
        pp.append(pena(f"calca{k}_{s}", raiz, (0.28 * nrm[0], -1.0, 0.28 * nrm[2] + 0.12), nrm, 4.6, 3.0, 0.9,
                       F_LAR if k in (0, 1) else F_VERM))
    mt = mat_cor(cor_tarso, borda=.08, curva=.25)
    pp += g.octogono("tarso_" + s, [xc - 1.15, 1.6, zc - 1.15], [xc + 1.15, 10.6, zc + 1.15], mt, r=0.35, faixa=(1.6, 10.4))
    # caneleiras em 2 faixas: a de cima roxa com aro lilás, a de baixo lilás
    pp += g.octogono("caneleira_" + s, [xc - 1.8, 5.0, zc - 1.8], [xc + 1.8, 7.4, zc + 1.8],
                     mat_caneleira(5.0, 7.4, LILAS, ROXO), r=0.55)
    pp += g.octogono("tornozeleira_" + s, [xc - 1.65, 3.1, zc - 1.65], [xc + 1.65, 4.9, zc + 1.65],
                     mat_caneleira(3.1, 4.9, LILAS_CL, LILAS), r=0.5)
    # pé e dedos grandes amarelos com nós marcados e garras escuras
    def cor_pe(p, f_):
        if f_ == "down": return OURO_ESC
        if f_ in ("up", "east", "west") and (p[2] % 1.5) < 0.28: return mix(AMARELO, OURO, 0.8)
        return AMARELO_CL if f_ == "up" else AMARELO
    mpe = mat_cor(cor_pe, borda=.12, curva=.3)
    mg = mat_cor(lambda p, f_: GARRA_CL if f_ == "up" else GARRA, borda=.1, curva=.2)
    pp.append(peca("pe_" + s, [xc - 1.7, 0.0, zc - 1.8], [xc + 1.7, 2.6, zc + 1.5], mpe, faixa=(0, 2.6), res=2))
    for nome, giro, dx, comp in (("meio", 0, 0.0, 5.2), ("fora", -30 * lado, 1.3 * lado, 4.5), ("dentro", 16 * lado, -1.2 * lado, 4.0)):
        x0, z0 = xc + dx, zc - 1.2
        pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
            peca(f"dedo_{nome}_{s}", [x0 - 0.9, 0, z0 - comp], [x0 + 0.9, 2.0, z0 + 0.4], mpe, faixa=(0, 2.0), res=2),
            peca(f"garra_{nome}_{s}", [x0 - 0.62, 0.3, z0 - comp - 1.6], [x0 + 0.62, 1.6, z0 - comp + 0.3], mg,
                 rot=(-14, 0, 0), pivo=(x0, 1.6, z0 - comp + 0.3), faixa=(0, 1.6), res=2)]))
    pp.append(peca("dedo_tras_" + s, [xc - 0.7, 0, zc + 1.0], [xc + 0.7, 1.4, zc + 3.2], mpe, faixa=(0, 1.4), res=2))
    pp.append(peca("garra_tras_" + s, [xc - 0.5, 0, zc + 3.1], [xc + 0.5, 1.0, zc + 4.2], mg, faixa=(0, 1.0), res=2))
    return osso("perna_" + s, [xc, 13.6, zc], [0, 0, 0], pp)

# ================= LOD =================
# Peças estruturais nunca somem de longe. Penas e plumas somem INTEIRAS (corpo, segmentos e ponta no mesmo nível).
import json as _json, re as _re
ESTRUTURA = _re.compile(r"^(bico|cranio|queixo|faceta|viseira|elmo|coroa|gema|chifre|tronco|uropigio|peitoral|pescoco|garganta_|"
                        r"garganta$|coxa|tarso|caneleira|tornozeleira|pe_|dedo_|garra_|corrente)")

def unidade(nome):
    """Nome da pena/pluma a que a peça pertence (corpo, segmentos e ponta)."""
    n = _re.sub(r"_pt$", "", nome)
    m = _re.match(r"^((?:crista|nuca|pluma)\d+|juba\d+_[de])(?:_\d+)?$", n)
    if m: return m.group(1)
    return n

def _lods_filtrados():
    arq = RAIZ / "modelos" / ID / "lods.json"
    if not arq.exists(): return None
    bruto = _json.loads(arq.read_text(encoding="utf-8"))
    nivel = {}
    for n, pads in bruto.items():
        for pad in pads:
            miolo = pad[len("^(?:"):-len(")$")] if pad.startswith("^(?:") else pad
            for nome in miolo.split("|"):
                nome = nome.replace("\\", "")
                if ESTRUTURA.match(nome): continue
                u = unidade(nome)
                nivel[u] = min(nivel.get(u, 99), int(n))
    return nivel

def _lods():
    nivel = _lods_filtrados()
    if not nivel: return None
    # todas as peças do modelo atual que pertencem a cada unidade
    bb = RAIZ / "modelos" / ID / f"{ID}.bbmodel"
    if not bb.exists(): return None
    nomes = [e["name"] for e in _json.loads(bb.read_text(encoding="utf-8"))["elements"]]
    out = {}
    for nome in nomes:
        if ESTRUTURA.match(nome): continue
        u = unidade(nome)
        if u in nivel: out.setdefault(nivel[u], []).append(nome)
    return {n: ["^(?:" + "|".join(_re.escape(x) for x in sorted(v)) + ")$"] for n, v in sorted(out.items())}

LODS = _lods()

# ================= MONTAGEM =================
def montar():
    corpo = tronco_ossos()
    corpo.append(asa_ossos(-1)); corpo.append(asa_ossos(1))
    corpo.append(cauda_ossos())
    pesc = pescoco_ossos()
    pesc.append(osso("cabeca", [0, 29.6, -6.0], [0, 0, 0], cabeca_ossos()))
    corpo.append(osso("pescoco", [0, 24.6, -5.0], [0, 0, 0], pesc))
    tronco = osso("corpo", [0, 13.6, 0.0], [0, 0, 0], corpo)
    return [tronco, perna(-1), perna(1)]

# ================= REVISÃO EXTRA (branco, arte lado a lado, cores) =================
PALETA = {"roxo_esc": ROXO_ESC, "roxo": ROXO, "lilas": LILAS, "creme": CREME, "amarelo": AMARELO, "laranja": LARANJA,
          "verm": VERM, "verm_esc": VERM_ESC, "ouro": OURO}
EXTRA = {"_ceu": (70, 110, 200), "_ceu2": (140, 170, 220), "_verde": (80, 140, 60), "_verde2": (150, 190, 80),
         "_cinza": (120, 120, 130), "_escuro": (25, 20, 30), "_branco": (240, 240, 250), "_azul_esc": (40, 50, 110)}

def distribuicao(img):
    """Porcentagem de cada grupo de cor da paleta nos pixels da criatura. Cada pixel vai para a cor da paleta mais
    próxima ADMITINDO luz e sombra (a cor vezes um fator de 0,5 a 1,15), para a sombra do amarelo contar como amarelo
    e não sumir da conta (a do vermelho já caía no vermelho escuro). Fundo, céu e grama ficam de fora."""
    import numpy as np
    a = np.asarray(img.convert("RGB")).astype(float)
    nomes = list(PALETA) + list(EXTRA)
    cs = np.array(list(PALETA.values()) + list(EXTRA.values()), float)
    s = np.clip((a @ cs.T) / (cs ** 2).sum(-1), 0.5, 1.15)                    # fator de luz de cada cor
    s[..., len(PALETA):] = 1.0
    d = ((a[..., None, :] - s[..., None] * cs[None, None]) ** 2).sum(-1)
    k = d.argmin(-1); dm = np.sqrt(d.min(-1))
    lum = a.max(-1)
    cont = {n: int(((k == i) & (dm < 60) & (lum > 60)).sum()) for i, n in enumerate(nomes) if not n.startswith("_")}
    tot = max(1, sum(cont.values()))
    p = {n: 100 * v / tot for n, v in cont.items()}
    return {"roxo+lilas": p["roxo_esc"] + p["roxo"] + p["lilas"], "verm+verm_esc": p["verm"] + p["verm_esc"],
            "laranja": p["laranja"], "amarelo+ouro": p["amarelo"] + p["ouro"], "creme": p["creme"]}

def extras(pasta, prefixo):
    import numpy as np, previa2
    from PIL import Image, ImageDraw
    pasta = Path(pasta)
    cam = RAIZ / "modelos" / ID / f"{ID}.bbmodel"
    faces, tex = previa2.carregar(str(cam))
    # branco: só a forma (sem textura), para ver volumes e blocos
    branco = tex.copy(); branco[..., :3] = 232
    ims = [previa2.desenhar((faces, branco), y, p, escala=9, fundo=(44, 48, 56)) for y, p in ((35, -10), (90, -5), (0, -6), (180, -6))]
    H = max(i.height for i in ims)
    f = Image.new("RGB", (sum(i.width for i in ims) + 30, H), (44, 48, 56)); x = 0
    for i in ims: f.paste(i, (x, H - i.height)); x += i.width + 10
    f.save(pasta / f"{prefixo}_branco.png")
    # arte lado a lado: a ilustração grande da ficha HD-2D e o modelo num ângulo parecido, na mesma altura
    ref = Image.open(RAIZ / "modelos" / "referencias" / "001_pirococo_ficha_hd2d.webp").convert("RGB").crop((0, 0, 590, 770))
    FUNDO = (24, 26, 34)
    mod = previa2.desenhar((faces, tex), 52, -4, escala=14, fundo=FUNDO, margem=10)
    a = np.asarray(mod).astype(int)
    m = np.abs(a - np.array(FUNDO)).max(-1) > 10
    ys, xs = np.nonzero(m)
    mod = mod.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    alt_arte = 685 - 85                                 # da ponta dos chifres ao chão, na ilustração
    k = alt_arte / mod.height
    mod = mod.resize((int(mod.width * k), alt_arte), Image.LANCZOS)
    W = ref.width + mod.width + 40
    lado = Image.new("RGB", (W, ref.height), FUNDO)
    lado.paste(ref, (0, 0)); lado.paste(mod, (ref.width + 30, 85))
    dr = ImageDraw.Draw(lado)
    for yy in range(85, 700, 60): dr.line([(ref.width + 4, yy), (ref.width + 24, yy)], fill=(90, 90, 110))
    dr.text((ref.width + 34, 8), f"{prefixo} (yaw 52)", fill=(235, 235, 235))
    lado.save(pasta / f"{prefixo}_arte_lado.png")
    dist = distribuicao(previa2.desenhar((faces, tex), 52, -4, escala=8, fundo=(25, 20, 30)))
    vistas = [distribuicao(previa2.desenhar((faces, tex), y, p, escala=6, fundo=(25, 20, 30))) for y, p in ((0, -6), (90, -5), (180, -6), (-90, -5))]
    media = {k_: sum(v[k_] for v in vistas) / 4 for k_ in dist}
    print("cores 3/4 :", "  ".join(f"{k_} {v:.0f}%" for k_, v in dist.items()))
    print("cores 4 vistas:", "  ".join(f"{k_} {v:.0f}%" for k_, v in media.items()))

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
    pasta = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "modelos" / ID / "revisao"
    prefixo = sys.argv[2] if len(sys.argv) > 2 else "atual"
    extras(pasta, prefixo)
