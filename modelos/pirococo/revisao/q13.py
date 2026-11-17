"""Pirococó (#001, Fogo, mítico): o Galo-Fênix das Chamas Eternas, modelado sobre a ficha do Galetário (2026-11-15).

Galo de briga imponente: elmo de PRATA com a gema vermelha em losango na testa e 2 chifres dourados grandes que
sobem e dobram para trás; rosto e pescoço brancos, toques roxos na bochecha, olho vermelho bravo, bico amarelo curvo
e barbela vermelha; juba ENORME de espetos vermelhos varrendo para trás (de costas, um bloco vermelho redondo);
ombreiras de prata facetadas e gola roxa; peitoral de prata compacto no alto do peito com a fênix-estrela vermelha,
laranja e amarela; frente de penas brancas; capa de asas com as fileiras de cima roxas e lilás e depois VERMELHO
descendo em degradê para o laranja e o amarelo nas pontas, acabando acima das pernas; 3 correntes longas de elos
dourados com gema oval que saem quase na horizontal e terminam em pingentes de folha com gema, mais um leque curto de
plumas de chama; pernas com punho dourado, anéis de prata e faixa vermelha, pés dourados grandes e garras escuras.

Ideias da montagem:
- toda pena é um bloco grosso com ponta em losango, orientada por vetores do mundo (direção da ponta e normal da
  face larga), pintada em FAIXAS chapadas (cor dominante + ponta de outra cor) com uma metade clara e uma escura;
- o degradê vermelho -> laranja -> amarelo da capa vem de fileira para fileira (cada fileira um passo do degradê);
- espetos da juba e plumas são cadeias de segmentos que afinam (ossos '<nome>_k');
- a armadura de prata (elmo, ombreiras, peitoral, anéis) é um detalhe facetado, nunca a massa principal."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, clamp, tom, na_borda

ID = "pirococo"; NOME = "Pirococó"; NUMERO = 1
ALTURA = 2.8
QUADRUPEDE = False
ROSTO = ((0, 33.2, -8.0), 7.6)
RAIZ = Path(__file__).resolve().parent.parent.parent
REF_ARTE = RAIZ / "modelos" / "referencias" / "001_pirococo_galetario_arte.png"

# ---------------- paleta oficial (as 9 amostras "Voxel" da ficha do Galetário) ----------------
ROXO_ESC = (103, 6, 137); ROXO_VIVO = (154, 21, 184); LILAS = (237, 181, 234)
BRANCO = (254, 236, 233); PRATA = (215, 214, 223)
AMARELO = (253, 161, 1); LARANJA = (253, 109, 1); VERM = (197, 5, 20); OURO = (254, 178, 1)
# tons de apoio (luz, sombra e contorno das cores da ficha)
VERM_CL = (228, 30, 46); VERM_ESC = (130, 4, 22); VERM_FUNDO = (92, 2, 18)
LARANJA_CL = (254, 132, 10)
AMARELO_CL = (255, 208, 72); OURO_ESC = (200, 112, 4)
PRATA_CL = (242, 241, 248); PRATA_ESC = (170, 166, 186); PRATA_FUNDO = (118, 112, 138)
BRANCO_SOMBRA = (238, 206, 210)
LILAS_CL = (248, 214, 246); ROXO_FUNDO = (66, 4, 88)
PRETO = (26, 10, 18)
GARRA = (52, 46, 60); GARRA_CL = (100, 96, 112)
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
            if borda: return contorno(b, 0.4)
            cor = a if u > 0.05 else b
            if t < 0.06: cor = contorno(b, 0.3)
            return cor
        if face == "up": return a
        if face == "down": return contorno(b, 0.35)
        return contorno(b, 0.15)
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
    """Pluma/espeto comprido: segmentos encadeados (ossos '<nome>_k') que afinam, com ponta em losango; cada junta
    dobra 'curva' graus no plano da face larga, para o lado do vetor do mundo 'dobra'."""
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

# faixas: [(t_fim, cor clara, cor escura)] da raiz para a ponta
F_LILAS = [(0.70, LILAS, ROXO_VIVO), (1.0, LILAS_CL, LILAS)]
F_ROXO = [(0.72, ROXO_VIVO, ROXO_ESC), (1.0, LILAS, ROXO_VIVO)]
F_VERM = [(0.80, VERM_CL, VERM), (1.0, LARANJA_CL, LARANJA)]
F_VERM_PURO = [(1.0, VERM_CL, VERM)]
F_VERM_LAR = [(0.46, VERM_CL, VERM), (0.84, LARANJA_CL, LARANJA), (1.0, OURO, AMARELO)]
F_LAR_AM = [(0.46, LARANJA_CL, LARANJA), (1.0, OURO, AMARELO)]
F_BRANCO = [(0.80, BRANCO, BRANCO_SOMBRA), (1.0, PRATA_CL, PRATA)]
F_JUBA_IN = [(0.76, VERM_CL, VERM), (1.0, LARANJA_CL, LARANJA)]
F_JUBA_OUT = [(0.60, VERM_CL, VERM), (0.86, LARANJA_CL, LARANJA), (1.0, OURO, AMARELO)]
F_JUBA_ROXO = [(0.70, ROXO_VIVO, ROXO_ESC), (1.0, LILAS, ROXO_VIVO)]
F_CRISTA = [(0.50, VERM_CL, VERM), (0.82, LARANJA_CL, LARANJA), (1.0, OURO, AMARELO)]
F_CAUDA = [(0.50, VERM_CL, VERM), (0.78, LARANJA_CL, LARANJA), (1.0, OURO, AMARELO)]

# ---------------- materiais sólidos ----------------
def mat_cor(cor_fn, **kw):
    def f(c):
        base = cor_fn(c["p"], c["face"])
        return None if base is None else tom(base, g.contexto_luz(c, **kw))
    return f

def mat_ouro(c):
    """Ouro facetado (chifres, punhos, pés, elos, pingentes): topo claro, frente ouro, lados amarelo-ouro, embaixo escuro."""
    face = c["face"]
    base = {"up": AMARELO_CL, "down": OURO_ESC, "north": OURO, "south": AMARELO}.get(face, mix(OURO, AMARELO, 0.5))
    return contorno(base, 0.3) if na_borda(c) else base

def mat_prata(c, frente=PRATA):
    """Prata facetada (elmo, ombreiras, peitoral, anéis): topo claro, frente prata, lados um tom abaixo, baixo escuro."""
    face = c["face"]
    base = {"up": PRATA_CL, "down": PRATA_ESC, "north": frente}.get(face, mix(PRATA, PRATA_ESC, 0.3))
    return mix(base, PRATA_FUNDO, 0.5) if na_borda(c) else base

def mat_prata_blocos(passo=1.6):
    """Prata em blocos (ombreiras): faixas de 'passo' com uma junta escura, como as peças empilhadas da ficha."""
    def f(c):
        x, y, z = c["p"]
        cor = mat_prata(c, frente=PRATA_CL)
        if c["face"] == "up" and ((x % 2.2) < 0.16 or (z % 2.2) < 0.16): cor = mix(cor, PRATA, 0.7)
        return cor
    return f

def mat_roxo(c, frente=ROXO_VIVO):
    face = c["face"]
    base = {"up": LILAS, "down": ROXO_ESC, "north": frente}.get(face, mix(ROXO_VIVO, ROXO_ESC, 0.35))
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
OLHO_RU, OLHO_RV = 1.5, 1.2
OLHO_CORTE0, OLHO_CORTE_INC = 0.45, 0.34     # pálpebra brava: o elmo corta o topo numa diagonal que desce para o bico

def olho(u, v):
    """Olho vermelho bravo (expressão neutra da ficha): a borda do elmo corta o alto numa diagonal que desce para o
    bico; íris vermelha grande, pupila escura do lado do bico e 1 brilho; branco só numa cunha atrás.
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
        if ((uu + 0.05) / 0.13) ** 2 + ((v - topo + 0.38) / 0.17) ** 2 <= 1: return (255, 250, 245)   # brilho
        cor = VERM_CL if v < topo - 0.45 else VERM                            # sombra do elmo no alto da íris
        if du * du + dv * dv > 0.8 and uu > ic: cor = VERM_ESC
        return cor
    return BRANCO if topo - v > 0.3 else BRANCO_SOMBRA

def cor_cabeca(p, face):
    """Crânio: rosto branco, prata do elmo no alto, toque roxo na bochecha atrás do olho, vermelho na nuca."""
    x, y, z = p
    if face == "up" or y > 33.8: return PRATA
    if z > -4.0: return VERM
    if z > ZL + 0.9 and y > 30.2: return ROXO_VIVO
    return BRANCO

def mat_rosto(c):
    cor = cor_cabeca(c["p"], c["face"])
    if c["face"] == "down": return BRANCO_SOMBRA if cor == BRANCO else contorno(cor, 0.3)
    return cor

def mat_faceta(lado):
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        u, v = z - FAC_C[1] - 0.1, y - OLHO_Y
        if c["face"] == fora:
            cor = olho(u, v)
            if cor is not None: return cor
            if v > OLHO_CORTE0 + OLHO_CORTE_INC * u + 0.1: return PRATA       # borda do elmo desce sobre o olho
        return mat_rosto(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face == "down": return AMARELO
    if face == "up": return AMARELO_CL
    if face in ("east", "west") and abs(z - (ZF - 1.7)) < 0.3 and abs(y - 31.6) < 0.24: return (110, 50, 10)   # narina
    if face == "north":
        larg = 0.3 + 0.8 * clamp((y - 29.6) / 2.4)
        return mix(AMARELO_CL, OURO, clamp((31.9 - y) / 1.6)) if abs(x) < larg else AMARELO
    return mix(AMARELO_CL, OURO, clamp((32.0 - y) / 1.0)) if y > 30.9 else mix(OURO, AMARELO, clamp((30.9 - y) / 1.2))

def mat_gema(cx, cy, W, H, moldura="prata"):
    """Gema: hexágono alto (pontas em cima e embaixo) com moldura (prata ou ouro) e gema vermelha facetada."""
    meio = (H - W) / 2
    fora = mat_prata if moldura == "prata" else mat_ouro
    m_cl, m_md, m_esc = (PRATA_CL, PRATA, PRATA_ESC) if moldura == "prata" else (AMARELO_CL, OURO, OURO_ESC)
    def f(c):
        x, y, z = c["p"]
        if c["face"] != "north": return fora(c)
        u = (x - cx) / (W / 2); v = (y - cy)
        lim = 1.0 if abs(v) <= meio else max(0.0, 1.0 - (abs(v) - meio) / (W / 2))
        borda = lim - abs(u)
        if borda < 0.1: return m_esc
        if borda < 0.36: return m_cl if (u < 0 and v > 0) else (m_md if v > -meio else m_esc)
        if (u + 0.2) ** 2 + ((v - 0.6) / 1.6) ** 2 < 0.03: return (255, 225, 220)
        if u < 0 and v > 0: return (240, 60, 66)
        if u > 0 and v < 0: return VERM_ESC
        return VERM
    return f

def so_gema(c, cor): return cor[0] > 120 and cor[1] < 90 and cor[2] < 90

def hexagono(nome, centro, W, H, esp, mat, res=8, brilho=False):
    """Hexágono alto (retângulo + 2 quadrados girados 45° nas pontas), face larga para a frente (-z)."""
    cx, cy, cz = centro
    meio = (H - W) / 2; q = W / 1.4142
    pcs = [peca(nome, [cx - W / 2, cy - meio, cz - esp / 2], [cx + W / 2, cy + meio, cz + esp / 2], mat, res=res, brilho=brilho)]
    for nm, yy in ((nome + "_cima", cy + meio), (nome + "_baixo", cy - meio)):
        rot = (0, 0, 45); piv = (cx, yy, cz)
        pcs.append(peca(nm, [cx - q / 2, yy - q / 2, cz - esp / 2 + 0.03], [cx + q / 2, yy + q / 2, cz + esp / 2 - 0.03],
                        mundo(mat, rot, piv), rot=rot, pivo=piv, res=res, brilho=brilho))
    return pcs

def chifre(nome, base, d, n, segs, curva, dobra):
    """Chifre de ouro de seção quadrada: segmentos que afinam e dobram (o 'sete' da ficha), ponta em cunha."""
    x, y0, z = base
    A0 = quadro(d, n)
    ez = _col(A0, 2)
    rx = -abs(curva) * (1 if _dot(ez, dobra) >= 0 else -1)
    def seg(k, ytop):
        L, W, T = segs[k]
        pcs = [peca(f"{nome}_{k}", [x - T / 2, ytop - L, z - W / 2], [x + T / 2, ytop + (0.35 if k else 0.0), z + W / 2], mat_ouro, res=3)]
        if k + 1 < len(segs): pcs.append(seg(k + 1, ytop - L))
        else:
            s = W / 1.4142
            pcs.append(peca(f"{nome}_pt", [x - T / 2 + 0.03, ytop - L - s / 2, z - s / 2], [x + T / 2 - 0.03, ytop - L + s / 2, z + s / 2],
                            mat_ouro, rot=(45, 0, 0), pivo=(x, ytop - L, z), res=3))
        return osso(f"{nome}_{k}", [x, ytop, z], euler(A0) if k == 0 else [rx, 0, 0], pcs)
    return seg(0, y0)

def cabeca_ossos():
    cab = []
    fx = (CY0, CY1)
    # crânio: volume chanfrado atrás + frente estreita; as facetas diagonais (com o olho) fecham a quina
    cab += g.arredondado2("cranio", [-LX, CY0, ZL - 0.4], [LX, CY1, ZT], mat_rosto, r=1.4, faixa=fx, res=3)
    cab += g.arredondado("cranio_frente", [-FRENTE_X - 0.3, CY0 + 0.2, ZF], [FRENTE_X + 0.3, CY1 - 1.0, ZL + 0.5], mat_rosto, r=0.5, faixa=fx, res=3)
    mbr = lambda c: BRANCO if c["face"] != "down" else BRANCO_SOMBRA
    cab += g.arredondado("queixo", [-2.3, CY0 - 0.6, ZF + 0.6], [2.3, 30.6, ZL + 3.0], mbr, r=0.6, res=3)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, CY0 + 0.3, cz - FAC_L / 2], [cx + FAC_T / 2, CY1 - 0.6, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, FAC_ANG * lado, 0), pivo=(cx, OLHO_Y, cz), faixa=fx, res=8))
        # borda do elmo sobre o olho: placa de prata grossa descendo para o bico (o V bravo da ficha)
        ox0, ox1 = sorted((cx + FAC_T / 2 * lado - 0.5 * lado, cx + FAC_T / 2 * lado + 0.75 * lado))
        ang = math.degrees(math.atan(OLHO_CORTE_INC))
        zc0 = cz + 0.1
        yb = OLHO_Y + OLHO_CORTE0 + 0.12
        def mvis(c):
            if c["face"] == "down": return PRATA_FUNDO
            return mat_prata(c, frente=PRATA_CL)
        cab.append(osso("viseira_" + s, [cx, yb, zc0], [0, FAC_ANG * lado, 0], [
            peca("viseira_" + s, [ox0, yb, cz - FAC_L / 2 - 0.4], [ox1, yb + 1.6, cz + FAC_L / 2 + 0.8],
                 mvis, rot=(-ang, 0, 0), pivo=(cx, yb, zc0), res=4)]))
        # toque roxo na bochecha: blocos roxos atrás do olho, do elmo até o queixo
        bx0, bx1 = sorted(((LX - 0.35) * lado, (LX + 0.45) * lado))
        cab.append(peca("bochecha_" + s, [bx0, 29.6, ZL + 0.6], [bx1, 33.4, ZL + 2.6], lambda c: mat_roxo(c, frente=ROXO_VIVO), res=4))
        cab.append(peca("bochecha2_" + s, [bx0, 31.4, ZL + 2.5], [bx1, 33.8, ZT + 0.4], lambda c: mat_roxo(c, frente=ROXO_ESC), res=3))
    # casca do elmo (alto da cabeça), as asas do elmo nos lados e a ponte em V que desce entre os olhos
    cab += g.arredondado("elmo_topo", [-LX - 0.35, 33.6, ZF - 0.4], [LX + 0.35, 36.0, ZT + 0.4], mat_prata, r=0.5, res=3)
    q = 1.5 * 1.4142
    cab.append(peca("elmo_ponte", [-1.15, 32.9, ZF - 0.55], [1.15, 34.0, ZF + 1.4], lambda c: mat_prata(c, frente=PRATA_CL), res=4))
    cab.append(peca("elmo_ponte_v", [-q / 2, 33.0 - q / 2, ZF - 0.5], [q / 2, 33.0 + q / 2, ZF + 1.3], mat_prata, rot=(0, 0, 45),
                    pivo=(0, 33.0, ZF), res=4))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.3 * lado, (LX + 0.8) * lado))
        # abas do elmo: placas que descem do pico da gema para as têmporas (de frente, a tiara em V invertido da ficha)
        cab.append(osso("elmo_aba_" + s, [0.3 * lado, 36.4, ZF - 0.6], [0, 0, -24 * lado], [
            peca("elmo_aba_" + s, [x0, 35.0, ZF - 0.7], [x1, 36.4, ZF + 3.6], lambda c: mat_prata(c, frente=PRATA_CL), res=4)]))
    # gema vermelha em moldura de prata no pico da testa, subindo acima do elmo
    gx, gy, gz, GW, GH = 0.0, 35.9, ZF - 1.05, 2.7, 5.2
    cab += hexagono("gema", (gx, gy, gz), GW, GH, 1.0, mat_gema(gx, gy, GW, GH), res=8, brilho=so_gema)
    # bico curvo: base alta (tampa + quilha em V de frente), meio que cai e gancho; mandíbula curta embaixo
    mb = mat_cor(cor_bico, borda=.05, curva=.25)
    def mq(c):
        f_ = c["face"]
        cor = AMARELO_CL if f_ in ("up", "east") else (OURO if f_ in ("north", "south") else mix(OURO, AMARELO, 0.5))
        return contorno(cor, 0.25) if na_borda(c) else cor
    fb = (29.4, 32.4)
    cab.append(peca("bico_tampa", [-1.4, 30.9, ZF - 2.3], [1.4, 32.6, ZF + 0.7], mb, faixa=fb, res=4))
    q = 1.4 * 1.4142
    cab.append(peca("bico_quilha", [-q / 2, 30.9 - q / 2, ZF - 2.2], [q / 2, 30.9 + q / 2, ZF + 0.6], mq, rot=(0, 0, 45),
                    pivo=(0, 30.9, ZF), faixa=fb, res=4))
    piv = (0, 32.4, ZF - 2.0)
    cab.append(peca("bico_meio", [-1.1, 30.6, ZF - 4.0], [1.1, 32.4, ZF - 1.9], mb, rot=(-20, 0, 0), pivo=piv, faixa=fb, res=4))
    cab.append(peca("bico_gancho", [-0.62, 29.3, ZF - 5.1], [0.62, 31.5, ZF - 3.6],
                    mat_cor(lambda p, f_: AMARELO_CL if f_ == "up" else mix(OURO, AMARELO, clamp((31.0 - p[1]) / 1.2)), borda=.1, curva=.2),
                    rot=(-32, 0, 0), pivo=(0, 31.5, ZF - 3.6), faixa=(29.3, 31.5), res=4))
    cab.append(peca("bico_baixo", [-0.85, 29.5, ZF - 2.6], [0.85, 30.4, ZF + 0.5],
                    mat_cor(lambda p, f_: (150, 60, 8) if (f_ != "down" and p[1] > 30.2) else AMARELO, borda=.08), res=4))
    # barbela vermelha: 2 lóbulos que pendem sob o bico
    def mbar(c):
        y = c["p"][1]; face = c["face"]
        base = VERM_CL if y > 28.0 else VERM
        if face in ("north", "down") or na_borda(c): base = contorno(base, 0.15) if face != "north" else base
        return base
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.05 * lado, 0.95 * lado))
        cab.append(osso("barbela_" + s, [0.0, 29.6, ZF - 0.6], [-6, 0, -4 * lado], [
            peca("barbela_" + s, [x0, 26.6, ZF - 1.3], [x1, 29.7, ZF + 0.2], mbar, res=4)]))
    cab.append(crista_ossos())
    cab += juba_ossos()
    return cab

def crista_ossos():
    """Chifres e crista: 2 chifres grandes de ouro que sobem do alto do elmo e dobram para trás, e a chama vermelha da
    crista atrás da gema, entre eles."""
    pc = []
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        pc.append(chifre("chifre_" + s, (2.3 * lado, 35.6, ZF + 3.8), (0.16 * lado, 1.0, -0.10), (lado, 0, 0),
                         [(4.0, 2.3, 2.3), (3.8, 2.0, 2.0), (3.2, 1.6, 1.6)], 28, (0, 0, 1)))
    # chama da crista: espetos vermelhos curtos atrás da gema, entre os chifres
    for k, (x, y, z, d, L, W) in enumerate([(0.0, 35.8, ZF + 2.4, (0, 1.0, 0.3), 5.0, 2.4), (-1.1, 35.6, ZF + 3.0, (-0.4, 1.0, 0.4), 4.2, 2.1),
                                            (1.1, 35.6, ZF + 3.0, (0.4, 1.0, 0.4), 4.2, 2.1)]):
        n = (0, 0, -1) if k == 0 else (0.6 * (1 if x > 0 else -1), 0, -0.8)
        pc.append(pluma(f"crista{k}", (x, y, z), d, n, [(L * 0.55, W, W * 0.85), (L * 0.3, W * 0.66, W * 0.6)], 6, F_CRISTA, dobra=(0, 0, 1)))
    return osso("crista", [0, 35.8, -6.0], [0, 0, 0], pc)

# juba de espetos: (azimute em volta do eixo para trás: 0 = cima, 90 = lado, 180 = baixo; abertura a partir do eixo de
# trás; comprimento; largura; faixas). Espelhada para os 2 lados (azimute ±). Os espetos saem de um MIOLO redondo
# vermelho atrás da cabeça (de costas, o bloco vermelho grande da ficha).
JUBA_MIOLO = ([-5.0, 28.4, -4.6], [5.0, 39.6, 1.0])
JUBA_COLS = (-4.0, -1.35, 1.35, 4.0)
# fileiras de espetos de baixo para cima: (y da raiz, inclinação para cima, comprimento, largura, faixas de dentro e de fora)
JUBA_FILAS = [
    (29.0, -0.40, 7.0, 3.0, F_JUBA_ROXO, F_JUBA_IN),
    (31.4, -0.05, 9.6, 3.2, F_JUBA_OUT, F_JUBA_IN),
    (33.8, 0.32, 10.2, 3.2, F_JUBA_OUT, F_JUBA_IN),
    (36.2, 0.70, 9.2, 3.2, F_JUBA_IN, F_JUBA_OUT),
    (38.4, 1.30, 5.6, 3.0, F_JUBA_OUT, F_JUBA_IN),
]
# espetos dos lados do rosto (de frente, a juba emoldura a cabeça): (y, direção, comprimento)
JUBA_LADO = [(30.4, (0.8, -0.25, 0.6), 5.6), (34.0, (0.8, 0.35, 0.55), 6.2)]

def mat_juba_miolo(c):
    """Miolo da juba: vermelho em blocos (as pontas quadradas dos espetos de trás pintadas como cubos encaixados)."""
    x, y, z = c["p"]; face = c["face"]
    a = x if face in ("north", "south", "up", "down") else z
    b = y if face != "up" and face != "down" else z
    bloco = (math.floor(a / 1.8) + math.floor(b / 1.8)) % 2
    base = VERM_CL if bloco else VERM
    if face == "down": return VERM_ESC
    if face == "up": return VERM_CL
    return base

def juba_ossos():
    """Juba ENORME de espetos vermelhos de seção quadrada, em grade atrás da cabeça (4 colunas x 4 fileiras) e todos
    apontando para TRÁS, abrindo um pouco para os lados e para cima: de costas as pontas formam o bloco vermelho grande
    da ficha, de lado é o leque de espetos varrendo para trás e para cima, de frente aparecem dos lados e em cima da
    cabeça. As do meio têm ponta laranja e amarela; as de baixo, perto do pescoço, são roxas."""
    pc = list(g.arredondado2("juba_miolo", JUBA_MIOLO[0], JUBA_MIOLO[1], mat_juba_miolo, r=2.0, res=2))
    for f, (y, sobe, L, W, f_in, f_out) in enumerate(JUBA_FILAS):
        for c, x in enumerate(JUBA_COLS):
            dentro = abs(x) < 2
            d = (x * 0.14, sobe, 1.0)
            Lk = L * (1.0 if dentro else 0.84)
            pc.append(pluma(f"juba{f}{c}", (x, y + (0.3 if dentro else 0.0), -2.8), d, (1.0 if x >= 0 else -1.0, 0.0, 0.0),
                            [(Lk * 0.55, W, W * 0.92), (Lk * 0.32, W * 0.7, W * 0.66)], 4, f_in if dentro else f_out, dobra=(0, 1, 0)))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        for k, (y, (dx, dy, dz), L) in enumerate(JUBA_LADO):
            pc.append(pluma(f"jubalado{k}_{s}", (3.4 * lado, y, -4.6), (dx * lado, dy, dz), (lado, 0.0, 0.0),
                            [(L * 0.55, 2.6, 2.3), (L * 0.32, 1.8, 1.6)], 4, F_JUBA_IN, dobra=(0, 1, 0)))
    return pc

# ================= PESCOÇO, TRONCO, OMBREIRAS E PEITORAL =================
def cor_tronco(p, face):
    x, y, z = p
    a = z if face in ("east", "west") else x
    fila = math.floor(y / 1.8)
    fa = ((a + (fila % 2) * 1.2) % 2.4) / 2.4
    if face != "up" and (y % 1.8) / 1.8 < 0.14 + 0.12 * (2 * abs(fa - 0.5)) ** 2: return VERM_ESC
    return VERM

def estrela(x, y, e=0.0):
    """Emblema da fênix-estrela (quadro "Peitoral Flamejante"): estrela vermelha alta no meio, asas abertas para os
    lados e para cima e a cauda em ponta para baixo. 'e' encolhe a forma (camadas de cor)."""
    ax = abs(x)
    # asas: faixa que sobe para fora, afinando até a ponta
    if 0.4 <= ax <= 3.3 - e:
        t = (ax - 0.4) / 2.9
        baixo = 21.6 + 1.6 * t + e
        cima = 22.7 + 1.9 * t - 1.3 * t * t - e
        if baixo <= y <= cima: return True
    # estrela do meio (losango alto) e a chama de cima
    if ax / max(1.05 - e, 0.05) + abs(y - 22.6) / max(2.5 - e * 1.6, 0.05) <= 1: return True
    # cauda em ponta
    if 19.4 + e * 1.8 <= y <= 21.8 and ax <= 0.5 * (y - 19.4) - e * 0.7: return True
    return False

def mat_peitoral(c):
    """Placa do peitoral: prata com a fênix-estrela (contorno vermelho, laranja e miolo amarelo-ouro)."""
    x, y, z = c["p"]
    if c["face"] != "north": return mat_prata(c)
    if estrela(x, y):
        if abs(x) / 1.05 + abs(y - 22.6) / 2.5 <= 1 and not (0.4 <= abs(x) and 21.6 <= y <= 24.6 and abs(x) > 0.75):
            return VERM if abs(x) / 1.05 + abs(y - 22.6) / 2.5 > 0.55 else VERM_CL
        if not estrela(x, y, 0.28): return VERM
        if not estrela(x, y, 0.58): return LARANJA
        return OURO
    if na_borda(c): return PRATA_ESC
    return PRATA_CL if y > 23.6 else PRATA

def tronco_ossos():
    pcs = []
    mt = mat_cor(cor_tronco, borda=.0, curva=.25)
    pcs += g.arredondado2("tronco", [-4.8, 12.6, -8.0], [4.8, 25.0, 2.0], mt, r=2.0, faixa=(12, 26), res=2)
    pcs += g.arredondado("tronco_tras", [-4.2, 12.2, 0.5], [4.2, 21.4, 8.2], mt, r=1.5, faixa=(12, 22), res=2)
    pcs += g.arredondado("uropigio", [-2.8, 15.0, 6.0], [2.8, 22.6, 10.8], mt, r=1.0, res=2)
    # peitoral de prata: placa de cima (retângulo + losango embaixo = escudo de 5 lados) com a fênix-estrela
    zf = -9.3
    pcs.append(peca("peitoral", [-3.5, 21.4, zf], [3.5, 24.8, zf + 1.3], mat_peitoral, res=8))
    s = 3.5 * 1.4142
    rot = (0, 0, 45); piv = (0.0, 21.4, zf + 0.65)
    pcs.append(peca("peitoral_v", [-s / 2, 21.4 - s / 2, zf + 0.1], [s / 2, 21.4 + s / 2, zf + 1.2], mundo(mat_peitoral, rot, piv),
                    rot=rot, pivo=piv, res=8))
    # ponta de cima (gola facetada que sobe entre as ombreiras)
    q = 1.7 * 1.4142
    piv3 = (0.0, 24.8, zf - 0.1)
    pcs.append(peca("peitoral_gola", [-q / 2, 24.8 - q / 2, zf - 0.5], [q / 2, 24.8 + q / 2, zf + 0.9],
                    lambda c: mat_prata(c, frente=PRATA_CL), rot=rot, pivo=piv3, res=6))
    # frente de penas brancas abaixo do peitoral (as de fora intercaladas de vermelho e laranja)
    for k, x in enumerate((-2.4, -0.8, 0.8, 2.4)):
        pcs.append(pena(f"barriga0_{k}", (x, 19.4, -8.0 + 0.2 * (k % 2)), (0.06 * x, -1.0, 0.18), (0.08 * x, 0, -1.0), 6.2, 2.4, 0.9,
                        F_BRANCO, res=4))
    for k, x in enumerate((-3.2, -1.6, 0.0, 1.6, 3.2)):
        fx = F_BRANCO if abs(x) < 3 else F_VERM
        pcs.append(pena(f"barriga1_{k}", (x, 16.4, -7.6 - 0.2 * (k % 2)), (0.08 * x, -1.0, 0.22), (0.1 * x, 0, -1.0), 6.2, 2.4, 0.9, fx, res=4))
    for k, x in enumerate((-2.8, -0.95, 0.95, 2.8)):
        fx = F_BRANCO if abs(x) < 2 else F_VERM_LAR
        pcs.append(pena(f"barriga2_{k}", (x, 13.6, -7.0 - 0.2 * (k % 2)), (0.1 * x, -1.0, 0.25), (0.1 * x, 0, -1.0), 5.8, 2.6, 0.9, fx, res=4))
    # costas: penas vermelhas deitadas para trás (de costas leem como a faixa vermelha do meio)
    for k, (x, y, z, L) in enumerate(((-1.6, 24.4, 0.6, 7.4), (1.6, 24.4, 0.6, 7.4), (0.0, 24.6, -0.6, 8.0),
                                      (-1.4, 21.4, 4.4, 6.4), (1.4, 21.4, 4.4, 6.4))):
        pcs.append(pena(f"costas{k}", (x, y, z), (0.1 * x, -0.45, 1.0), (0, 1, 0.2), L, 3.2, 1.0, F_VERM_PURO if k < 3 else F_VERM))
    return pcs

def ombreiras_ossos():
    """Ombreiras de prata facetadas: uma casca arredondada sobre o ombro e uma aba mais baixa e mais para fora."""
    ossos = []
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        # casca abaulada (bem chanfrada) sobre o ombro, mais alta e mais para a frente, e a aba de baixo mais para fora
        x0, x1 = sorted((2.6 * lado, 8.6 * lado))
        cima = g.arredondado2("ombreira_" + s, [x0, 22.8, -5.8], [x1, 27.8, 3.2], mat_prata_blocos(1.6), r=2.0, res=3)
        x0, x1 = sorted((5.8 * lado, 10.2 * lado))
        aba = g.arredondado2("ombreira_aba_" + s, [x0, 21.0, -5.2], [x1, 24.0, 2.6], mat_prata_blocos(1.3), r=1.0, res=3)
        ossos.append(osso("ombreira_" + s, [2.6 * lado, 27.8, -1.2], [0, 0, -20 * lado],
                          cima + [osso("ombreira_aba_" + s, [5.8 * lado, 24.0, -1.2], [0, 0, -14 * lado], aba)]))
    return ossos

def pescoco_ossos():
    pc = []
    def cor_pesc(p, f_):
        x, y, z = p
        if f_ == "north" or z < -6.2: return BRANCO
        return VERM if z > -4.4 else BRANCO_SOMBRA
    mp = mat_cor(cor_pesc, borda=.0, curva=.2)
    pc += g.octogono("pescoco", [-2.2, 24.4, -8.0], [2.2, 31.0, -3.4], mp, r=0.8, faixa=(24, 31))
    # garganta branca na frente do pescoço comprido
    pc += g.arredondado("garganta", [-2.0, 25.0, -8.8], [2.0, 30.4, -6.6], lambda c: BRANCO if c["face"] != "down" else BRANCO_SOMBRA,
                        r=0.5, res=3)
    # gola roxa na base do pescoço, entre as ombreiras
    def cor_gola(c):
        x, y, z = c["p"]; face = c["face"]
        if face == "up": return LILAS
        if face == "down": return ROXO_FUNDO
        return ROXO_VIVO if (y % 1.2) > 0.25 else ROXO_ESC
    pc += g.octogono("gola_roxa", [-3.4, 23.8, -8.6], [3.4, 26.4, -2.0], cor_gola, r=1.0)
    return pc

# ================= CAPA DE ASAS =================
# fileiras de cima para baixo: (y da raiz, ângulos no anel, raio x, raio z, comprimento, largura, abertura, varrida, faixas)
# lilás e roxo nos ombros; depois o vermelho domina e desce em degradê para o laranja e o amarelo nas pontas
F_ROXO_VERM = [(0.58, ROXO_VIVO, ROXO_ESC), (1.0, VERM_CL, VERM)]
F_VERM_LAR2 = [(0.70, VERM_CL, VERM), (1.0, LARANJA_CL, LARANJA)]
F_LAR_AM2 = [(0.44, VERM_CL, VERM), (0.70, LARANJA_CL, LARANJA), (1.0, OURO, AMARELO)]
ASA = [
    (24.2, (-48, -20, 8, 36), 4.8, 5.8, 8.0, 3.3, 46, 16, F_ROXO),
    (22.8, (-56, -30, -4, 22, 48, 72), 5.0, 6.0, 10.4, 3.4, 44, 22, F_LILAS),
    (21.2, (-60, -36, -12, 12, 36, 60, 82), 5.1, 6.3, 12.8, 3.6, 45, 28, F_VERM_PURO),
    (19.8, (-58, -34, -10, 14, 38, 62, 84), 5.2, 6.5, 15.0, 3.8, 46, 33, F_VERM_LAR2),
    (18.4, (-54, -30, -6, 18, 42, 66, 88), 5.2, 6.5, 17.0, 3.8, 47, 38, F_LAR_AM2),
]
ASA_ZC = -0.4

def asa_ossos(lado):
    """Asa caída como capa: 5 fileiras em telha, as de cima roxas e lilás, depois vermelho, vermelho-laranja e
    laranja-amarelo (o degradê da ficha). As pontas abrem um pouco para fora e varrem para trás; a fileira de baixo
    acaba acima das pernas, deixando o punho dourado e os anéis à mostra."""
    s = "d" if lado < 0 else "e"
    pcs = []
    for f, (y, phis, ax, az, L, W, abre, varre, fx) in enumerate(ASA):
        ta, tv = math.tan(math.radians(abre)), math.tan(math.radians(varre))
        for k, phi in enumerate(phis):
            r = math.radians(phi)
            x, z = lado * ax * math.cos(r), ASA_ZC + az * math.sin(r)
            nrm = (lado * math.cos(r), 0.0, math.sin(r))
            d = (lado * math.cos(r) * ta, -1.0, max(0.0, math.sin(r)) * ta * 0.6 + tv)
            pcs.append(pena(f"asa{f}_{k}_{s}", (x, y - 0.3 * (k % 2), z), d, nrm, L, W, 1.15, fx))
    return osso("asa_" + s, [4.8 * lado, 24.6, -1.0], [0, 0, 0], pcs)

# ================= CAUDA: LEQUE DE CHAMA E CORRENTES =================
RAIZ_CAUDA = (0.0, 19.4, 8.6)
def _pl(ang, lat):
    a = math.radians(ang)
    return (lat, math.sin(a), math.cos(a))
_SEG = lambda k: [(4.2 * k, 3.6, 1.1), (3.6 * k, 2.9, 1.0), (3.0 * k, 2.1, 0.9)]
PLUMAS = [
    ("pluma0", (0.0, 21.8, 9.0), _pl(48, 0.0), _SEG(1.0), 22, F_CAUDA),
    ("pluma1", (-0.9, 21.4, 9.4), _pl(32, -0.22), _SEG(0.95), 18, F_CAUDA),
    ("pluma2", (0.9, 21.4, 9.4), _pl(32, 0.22), _SEG(0.95), 18, F_CAUDA),
    ("pluma3", (-1.0, 20.6, 9.6), _pl(14, -0.36), _SEG(0.9), 12, F_CAUDA),
    ("pluma4", (1.0, 20.6, 9.6), _pl(14, 0.36), _SEG(0.9), 12, F_CAUDA),
]
N_ELOS = 4
ELO = 3.9                       # comprimento de cada elo oval
PASSO = 4.8                     # elo + argola até o próximo
# 3 correntes longas que saem da base da cauda quase na horizontal, em 3 alturas (como na vista de lado da ficha)
CORRENTES = [("corrente_c", (0.0, 20.2, 10.2), 24, 0.0),
             ("corrente_d", (-1.6, 18.0, 10.4), 0, -0.22),
             ("corrente_e", (1.6, 15.8, 10.2), -24, 0.22)]
ONDAS = ([(n, N_ELOS, (3.0, 2.0, 1.5)) for n, _, _, _ in CORRENTES]
         + [(p[0], len(p[3]), (2.0, 1.5, 0.0)) for p in PLUMAS])
ANIM_PARADO = {f"{n}_pingente": [(0, 0, 0), (4, 0, 7 * s_), (0, 0, 0), (-4, 0, -7 * s_), (0, 0, 0)]
               for (n, _, _, _), s_ in zip(CORRENTES, (1, -1, 1))}
ANIM_ANDANDO = {f"{n}_pingente": [(0, 0, 0), (8, 0, 10 * s_), (0, 0, 0), (-8, 0, -10 * s_), (0, 0, 0)]
                for (n, _, _, _), s_ in zip(CORRENTES, (1, -1, 1))}

def mat_elo(cy, cz):
    """Elo oval de ouro com a gema vermelha oval no meio das faces compridas (quadro "Cauda de Fênix")."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        if face in ("east", "west"): u, v = y - cy, z - cz
        elif face in ("up", "down"): return mat_ouro(c)
        else: u, v = y - cy, x
        e = (u / (ELO * 0.3)) ** 2 + (v / 0.8) ** 2
        if e <= 1.0:
            if (u - 0.35) ** 2 / 0.09 + (v - 0.22) ** 2 / 0.02 <= 1: return (255, 205, 200)
            return VERM_CL if v > 0.05 else VERM
        if e <= 1.45: return OURO_ESC
        base = AMARELO_CL if v > 0.45 else (OURO if v > -0.3 else AMARELO)
        return contorno(base, 0.3) if na_borda(c) else base
    return f

def mat_pingente(cx, cy, cz, W, H):
    """Pingente em folha: losango alto com moldura de ouro (clara em cima, escura embaixo) e gema vermelha facetada."""
    meio = (H - W) / 2
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        if face not in ("east", "west"): return mat_ouro(c)
        u = (z - cz) / (W / 2); v = y - cy
        lim = 1.0 if abs(v) <= meio else max(0.0, 1.0 - (abs(v) - meio) / (W / 2))
        borda = lim - abs(u)
        if borda < 0.1: return OURO_ESC
        if borda < 0.4: return AMARELO_CL if u > 0.2 else (OURO if u > -0.3 else AMARELO)
        if borda < 0.48: return OURO_ESC
        if (u + 0.15) ** 2 + ((v - 0.6) / 1.6) ** 2 < 0.025: return (255, 225, 220)
        if u < 0 and v > 0: return (240, 60, 66)
        if u > 0 and v < 0: return VERM_ESC
        return VERM
    return f

def corrente(nome, raiz, elev, lat):
    """Corrente longa de elos ovais de ouro com gema (um osso por elo, '<nome>_k'): sai para trás quase na horizontal
    ('elev' graus acima dela, 'lat' para o lado) e cai um pouco a cada elo; no fim, o pingente em folha (osso
    '<nome>_pingente') aponta para trás e para baixo."""
    x, y0, z = raiz
    dirs = []
    for k in range(N_ELOS):
        a = math.radians(elev - 5.0 * k)
        dirs.append(_n((lat, math.sin(a), math.cos(a))))
    quadros = [quadro(dk, (1.0, 0.0, 0.0)) for dk in dirs]
    a_fim = math.radians(elev - 5.0 * N_ELOS - 42)
    q_fim = quadro(_n((lat, math.sin(a_fim), math.cos(a_fim))), (1.0, 0.0, 0.0))
    def elo(k):
        yt = y0 - k * PASSO
        cy = yt - 0.45 - ELO / 2
        m = mat_elo(cy, z)
        R, t = 1.3, 0.7
        pcs = [peca(f"{nome}_{k}", [x - t, cy - ELO / 2, z - R], [x + t, cy + ELO / 2, z + R], m, res=5, brilho=so_gema),
               peca(f"{nome}_{k}p", [x - t * 0.8, cy - ELO / 2 - 0.4, z - R * 0.55], [x + t * 0.8, cy + ELO / 2 + 0.4, z + R * 0.55], m, res=5),
               peca(f"{nome}_{k}m", [x - t * 0.9, cy - ELO / 2 + 0.7, z - R - 0.25], [x + t * 0.9, cy + ELO / 2 - 0.7, z + R + 0.25], m, res=5,
                    brilho=so_gema),
               peca(f"{nome}_{k}c", [x - 0.32, yt - PASSO - 0.15, z - 0.32], [x + 0.32, yt + 0.15, z + 0.32], mat_ouro, res=3)]
        if k + 1 < N_ELOS:
            pcs.append(elo(k + 1))
        else:
            pcs.append(pingente(nome, (x, yt - PASSO, z), _t(quadros[-1]), q_fim))
        rel = quadros[0] if k == 0 else _mm(_t(quadros[k - 1]), quadros[k])
        return osso(f"{nome}_{k}", [x, yt, z], euler(rel), pcs)
    return elo(0)

def pingente(nome, topo, inv_ant, q_fim):
    x, y, z = topo
    W, H, esp = 3.8, 6.8, 1.3
    cy = y - 0.6 - H / 2
    m = mat_pingente(x, cy, z, W, H)
    meio = (H - W) / 2; q = W / 1.4142
    pcs = [peca(f"{nome}_argola", [x - 0.45, cy + H / 2 - 0.4, z - 0.45], [x + 0.45, y + 0.15, z + 0.45], mat_ouro, res=3),
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
    for nome, raiz, elev, lat in CORRENTES:
        pc.append(corrente(nome, raiz, elev, lat))
    return osso("cauda", list(RAIZ_CAUDA), [0, 0, 0], pc)

# ================= PERNAS =================
def perna(lado):
    """Perna: coxa e calça de penas vermelhas, punho dourado largo, 2 anéis de prata, faixa vermelha, tornozelo e
    pés dourados grandes com garras escuras (quadro "Patas Reforçadas")."""
    s = "d" if lado < 0 else "e"; xc = 3.4 * lado; zc = 0.4
    pp = []
    def cor_coxa(p, f_):
        return VERM if (p[1] % 1.6) > 0.3 else VERM_ESC
    pp += g.arredondado("coxa_" + s, [xc - 2.0, 9.6, zc - 2.2], [xc + 2.0, 14.2, zc + 2.0], mat_cor(cor_coxa, borda=.0, curva=.25),
                        r=0.8, res=3)
    for k, phi in enumerate((-80, -10, 60, 130)):
        r_ = math.radians(phi)
        nrm = (math.cos(r_) * lado, 0.0, math.sin(r_))
        raiz = (xc + 1.5 * nrm[0], 12.6, zc + 1.5 * nrm[2])
        pp.append(pena(f"calca{k}_{s}", raiz, (0.22 * nrm[0], -1.0, 0.22 * nrm[2] + 0.1), nrm, 4.2, 3.0, 0.9, F_VERM_PURO))
    def cor_canela(p, f_):
        return VERM if (p[1] % 1.1) > 0.18 else VERM_ESC
    pp += g.octogono("tarso_" + s, [xc - 1.5, 2.6, zc - 1.5], [xc + 1.5, 10.4, zc + 1.5], mat_cor(cor_canela, borda=.06, curva=.2),
                     r=0.45, faixa=(2.6, 10.4))
    # punho dourado, 2 anéis de prata e a faixa vermelha
    def faixa(nome, y0, y1, h, mat, r=0.55):
        return g.octogono(nome, [xc - h, y0, zc - h], [xc + h, y1, zc + h], mat, r=r)
    pp += faixa("punho_" + s, 7.0, 8.8, 2.2, mat_ouro, 0.65)
    pp += faixa("anel_" + s, 6.0, 7.0, 2.0, lambda c: mat_prata(c, frente=PRATA_CL), 0.6)
    pp += faixa("anel2_" + s, 4.95, 6.0, 2.1, mat_prata, 0.6)
    pp += faixa("faixa_verm_" + s, 4.0, 4.95, 1.75, lambda c: VERM if c["face"] not in ("down",) and not na_borda(c) else VERM_ESC, 0.5)
    # tornozelo e pé dourados, dedos grossos e garras escuras em cubo
    def cor_pe(p, f_):
        if f_ == "down": return OURO_ESC
        if f_ in ("up", "east", "west") and (p[2] % 1.5) < 0.26: return mix(AMARELO, OURO_ESC, 0.5)
        return AMARELO_CL if f_ == "up" else OURO
    mpe = mat_cor(cor_pe, borda=.12, curva=.3)
    mg = mat_cor(lambda p, f_: GARRA_CL if f_ == "up" else GARRA, borda=.1, curva=.2)
    pp += g.arredondado("tornozelo_" + s, [xc - 1.9, 2.0, zc - 2.0], [xc + 1.9, 4.1, zc + 1.7], mpe, r=0.5, res=2)
    pp.append(peca("pe_" + s, [xc - 1.9, 0.0, zc - 1.9], [xc + 1.9, 2.4, zc + 1.6], mpe, faixa=(0, 2.4), res=2))
    for nome, giro, dx, comp in (("meio", 0, 0.0, 4.4), ("fora", -20 * lado, 1.4 * lado, 3.9), ("dentro", 14 * lado, -1.3 * lado, 3.5)):
        x0, z0 = xc + dx, zc - 1.2
        pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
            peca(f"dedo_{nome}_{s}", [x0 - 1.0, 0, z0 - comp], [x0 + 1.0, 2.2, z0 + 0.4], mpe, faixa=(0, 2.2), res=2),
            peca(f"garra_{nome}_{s}", [x0 - 0.8, 0.0, z0 - comp - 1.5], [x0 + 0.8, 1.6, z0 - comp + 0.2], mg, faixa=(0, 1.6), res=2)]))
    pp.append(peca("dedo_tras_" + s, [xc - 0.8, 0, zc + 1.0], [xc + 0.8, 1.6, zc + 3.2], mpe, faixa=(0, 1.6), res=2))
    pp.append(peca("garra_tras_" + s, [xc - 0.6, 0, zc + 3.1], [xc + 0.6, 1.2, zc + 4.3], mg, faixa=(0, 1.2), res=2))
    return osso("perna_" + s, [xc, 13.2, zc], [0, 0, 0], pp)

# ================= LOD =================
# Peças estruturais nunca somem de longe. Penas, espetos e plumas somem INTEIROS (corpo, segmentos e ponta juntos).
import json as _json, re as _re
ESTRUTURA = _re.compile(r"^(bico|barbela|cranio|queixo|faceta|viseira|bochecha|elmo|gema|chifre|juba_miolo|tronco|uropigio|peitoral|"
                        r"ombreira|pescoco|garganta|gola_roxa|coxa|tarso|punho|anel|faixa_verm|tornozelo|pe_|dedo_|garra_|corrente)")

def unidade(nome):
    """Nome da pena/espeto/pluma a que a peça pertence (corpo, segmentos e ponta)."""
    n = _re.sub(r"_pt$", "", nome)
    m = _re.match(r"^((?:crista|pluma|juba)\d+|jubalado\d+_[de])(?:_\d+)?$", n)
    if m: return m.group(1)
    return n

def _lods():
    arq = RAIZ / "modelos" / ID / "lods.json"
    bb = RAIZ / "modelos" / ID / f"{ID}.bbmodel"
    if not arq.exists() or not bb.exists(): return None
    nivel = {}
    for n, pads in _json.loads(arq.read_text(encoding="utf-8")).items():
        for pad in pads:
            miolo = pad[len("^(?:"):-len(")$")] if pad.startswith("^(?:") else pad
            for nome in miolo.split("|"):
                nome = nome.replace("\\", "")
                if ESTRUTURA.match(nome): continue
                u = unidade(nome)
                nivel[u] = min(nivel.get(u, 99), int(n))
    if not nivel: return None
    out = {}
    for nome in (e["name"] for e in _json.loads(bb.read_text(encoding="utf-8"))["elements"]):
        if ESTRUTURA.match(nome): continue
        u = unidade(nome)
        if u in nivel: out.setdefault(nivel[u], []).append(nome)
    return {n: ["^(?:" + "|".join(_re.escape(x) for x in sorted(v)) + ")$"] for n, v in sorted(out.items())}

LODS = _lods()

# ================= MONTAGEM =================
K_CAB, SOBE_CAB = 0.94, 1.1      # cabeça no tamanho da arte, alta, sobre o pescoço comprido da ficha
CENTRO_CAB = (0.0, 30.0, -6.0)

def montar():
    corpo = tronco_ossos()
    corpo += ombreiras_ossos()
    corpo.append(asa_ossos(-1)); corpo.append(asa_ossos(1))
    corpo.append(cauda_ossos())
    pesc = pescoco_ossos()
    i_cab = len(g.PECAS)
    cab = osso("cabeca", [0, 30.0, -6.0], [0, 0, 0], cabeca_ossos())
    g.transformar(i_cab, [cab], CENTRO_CAB, k=K_CAB, sobe=SOBE_CAB)
    pesc.append(cab)
    corpo.append(osso("pescoco", [0, 25.0, -5.4], [0, 0, 0], pesc))
    tronco = osso("corpo", [0, 13.2, 0.0], [0, 0, 0], corpo)
    return [tronco, perna(-1), perna(1)]

# ================= REVISÃO EXTRA (branco, arte lado a lado, cores) =================
PALETA = {"roxo_esc": ROXO_ESC, "roxo_vivo": ROXO_VIVO, "lilas": LILAS, "branco": BRANCO, "prata": PRATA,
          "amarelo": AMARELO, "laranja": LARANJA, "verm": VERM, "ouro": OURO}
EXTRA = {"_escuro": (25, 20, 30), "_cinza": (110, 105, 120), "_azul": (40, 50, 110)}

def distribuicao(img):
    """Porcentagem de cada grupo de cor da paleta nos pixels da criatura. Cada pixel vai para a cor da paleta mais
    próxima ADMITINDO luz e sombra (a cor vezes um fator de 0,5 a 1,15); fundo escuro fica de fora."""
    import numpy as np
    a = np.asarray(img.convert("RGB")).astype(float)
    nomes = list(PALETA) + list(EXTRA)
    cs = np.array(list(PALETA.values()) + list(EXTRA.values()), float)
    s = np.clip((a @ cs.T) / (cs ** 2).sum(-1), 0.5, 1.15)
    s[..., len(PALETA):] = 1.0
    d = ((a[..., None, :] - s[..., None] * cs[None, None]) ** 2).sum(-1)
    k = d.argmin(-1); dm = np.sqrt(d.min(-1))
    lum = a.max(-1)
    cont = {n: int(((k == i) & (dm < 60) & (lum > 60)).sum()) for i, n in enumerate(nomes) if not n.startswith("_")}
    tot = max(1, sum(cont.values()))
    p = {n: 100 * v / tot for n, v in cont.items()}
    return {"roxo+lilas": p["roxo_esc"] + p["roxo_vivo"] + p["lilas"], "vermelho": p["verm"], "laranja": p["laranja"],
            "amarelo+ouro": p["amarelo"] + p["ouro"], "branco+prata": p["branco"] + p["prata"]}

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
    # arte lado a lado: a ilustração grande da ficha do Galetário e o modelo num ângulo parecido, na mesma altura
    ref = Image.open(REF_ARTE).convert("RGB")
    FUNDO = (24, 26, 34)
    YAW = 40
    mod = previa2.desenhar((faces, tex), YAW, -6, escala=14, fundo=FUNDO, margem=10)
    a = np.asarray(mod).astype(int)
    m = np.abs(a - np.array(FUNDO)).max(-1) > 10
    ys, xs = np.nonzero(m)
    mod = mod.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    topo, chao = 5, 740                                 # da ponta dos chifres ao chão, na ilustração
    k = (chao - topo) / mod.height
    mod = mod.resize((int(mod.width * k), chao - topo), Image.LANCZOS)
    W = ref.width + mod.width + 40
    lado = Image.new("RGB", (W, ref.height), FUNDO)
    lado.paste(ref, (0, 0)); lado.paste(mod, (ref.width + 30, topo))
    dr = ImageDraw.Draw(lado)
    for yy in range(topo, chao + 1, 70): dr.line([(ref.width + 4, yy), (ref.width + 24, yy)], fill=(90, 90, 110))
    dr.text((ref.width + 34, 8), f"{prefixo} (yaw {YAW})", fill=(235, 235, 235))
    lado.save(pasta / f"{prefixo}_arte_lado.png")
    dist = distribuicao(previa2.desenhar((faces, tex), YAW, -6, escala=8, fundo=(25, 20, 30)))
    vistas = [distribuicao(previa2.desenhar((faces, tex), y, p, escala=6, fundo=(25, 20, 30))) for y, p in ((0, -6), (90, -5), (180, -6), (-90, -5))]
    media = {k_: sum(v[k_] for v in vistas) / 4 for k_ in dist}
    print("cores 3/4 :", "  ".join(f"{k_} {v:.0f}%" for k_, v in dist.items()))
    print("cores 4 vistas:", "  ".join(f"{k_} {v:.0f}%" for k_, v in media.items()))

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
    pasta = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "modelos" / ID / "revisao"
    prefixo = sys.argv[2] if len(sys.argv) > 2 else "atual"
    extras(pasta, prefixo)
