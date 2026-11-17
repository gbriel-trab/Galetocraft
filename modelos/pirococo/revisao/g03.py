"""Pirococó (#001, Fogo, mítico): o Galo-Fênix das Chamas Eternas, modelado sobre a 3ª ficha do Galetário
(001_pirococo_g2_*, 2026-11-16). A versão anterior, de armadura prata, está guardada em modelos/pirococo/alternativa_q18.py.

Galo de briga imponente com armadura ROXA de frisos DOURADOS:
- elmo roxo com moldura dourada em V, a gema vermelha num engaste dourado em losango no meio da testa, máscara roxa
  em volta dos olhos e 2 chifres dourados altos e angulosos (sobem, dobram e sobem de novo);
- rosto e pescoço brancos, olho vermelho bravo, bico amarelo e barbela vermelha grande;
- juba de penas achatadas e afiladas, vermelhas e vermelho-escuras, varrendo para trás (quase sem laranja);
- ombreiras roxas grandes e angulosas com borda dourada e peitoral roxo em V com moldura dourada e gema vermelha;
- peito de penas brancas e lilás "estruturadas" em camadas pontudas, abaixo do peitoral, com corpo e flancos roxos;
- asas com as fileiras de cima roxas e, nas laterais, penas de chama vermelhas com pontas laranja e amarelas;
- cauda de fênix tripla: leque grande de penas longas em FOICE que varrem para trás e curvam para cima, vermelho ->
  laranja -> amarelo (sem correntes);
- pernas longas e fortes: coxa de penas roxas, canela dourada com braçadeiras douradas no joelho e no tornozelo,
  pés dourados e garras claras.

Ideias da montagem:
- toda pena é um bloco grosso com ponta em losango, orientada por vetores do mundo (direção da ponta e normal da
  face larga), pintada em FAIXAS chapadas (cor dominante + ponta de outra cor) com uma metade clara e uma escura;
- penas longas (juba, foices) são cadeias de segmentos que afinam e curvam (ossos '<nome>_k');
- a armadura é um detalhe facetado: placas roxas com o friso dourado pintado na borda, nunca a massa principal."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, clamp, tom, na_borda

ID = "pirococo"; NOME = "Pirococó"; NUMERO = 1
ALTURA = 2.8
QUADRUPEDE = False
ROSTO = ((0, 33.0, -8.0), 7.6)
RAIZ = Path(__file__).resolve().parent.parent.parent
REF_ARTE = RAIZ / "modelos" / "referencias" / "001_pirococo_g2_arte.png"

# ---------------- paleta oficial (as 8 amostras da 3ª ficha) ----------------
ROXO_ESC = (102, 37, 114); ROXO = (160, 60, 171); LILAS = (215, 159, 210)
BRANCO = (248, 227, 230)
AMARELO = (254, 187, 38); LARANJA = (253, 133, 2)
VERM = (236, 25, 39); VERM_ESC = (176, 12, 29)
# tons de apoio (luz, sombra e contorno das cores da ficha)
ROXO_CL = (186, 96, 196); ROXO_FUNDO = (66, 20, 76); LILAS_CL = (236, 200, 232)
VERM_FUNDO = (118, 6, 22)
AMARELO_CL = (255, 222, 110); OURO = (240, 160, 20); OURO_ESC = (186, 108, 8)
BRANCO_SOMBRA = (226, 198, 210)
PRETO = (26, 10, 18)
GARRA = (246, 240, 244); GARRA_SOMBRA = (206, 186, 206)
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
    """Pena longa: segmentos encadeados (ossos '<nome>_k') que afinam, com ponta em losango; cada junta dobra 'curva'
    graus no plano da face larga, para o lado do vetor do mundo 'dobra'."""
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
F_ROXO = [(0.74, ROXO, ROXO_ESC), (1.0, LILAS, ROXO)]
F_ROXO_ESC = [(0.74, ROXO_ESC, ROXO_FUNDO), (1.0, ROXO, ROXO_ESC)]
F_ROXO_VERM = [(0.62, ROXO, ROXO_ESC), (1.0, VERM, VERM_ESC)]
# (o laranja só aparece como a metade escura da ponta amarela: a ficha é vermelha com pontas laranja e amarelas)
F_CHAMA1 = [(0.76, VERM, VERM_ESC), (0.86, LARANJA, VERM), (1.0, AMARELO, OURO)]
F_CHAMA2 = [(0.66, VERM, VERM_ESC), (0.78, LARANJA, VERM), (1.0, AMARELO, OURO)]
F_CHAMA3 = [(0.58, VERM, VERM_ESC), (0.70, LARANJA, VERM), (1.0, AMARELO, OURO)]
F_BRANCO = [(0.80, BRANCO, BRANCO_SOMBRA), (1.0, LILAS_CL, LILAS)]
F_LILAS_CL = [(0.80, LILAS_CL, LILAS), (1.0, BRANCO, BRANCO_SOMBRA)]
F_JUBA = [(1.0, VERM, VERM_ESC)]
F_JUBA_ESC = [(0.86, VERM_ESC, VERM_FUNDO), (1.0, VERM, VERM_ESC)]
F_JUBA_PONTA = [(0.88, VERM, VERM_ESC), (1.0, LARANJA, VERM)]
F_FOICE = [(0.46, VERM, VERM_ESC), (0.64, LARANJA, VERM), (1.0, AMARELO, OURO)]

# ---------------- materiais sólidos ----------------
def mat_cor(cor_fn, **kw):
    def f(c):
        base = cor_fn(c["p"], c["face"])
        return None if base is None else tom(base, g.contexto_luz(c, **kw))
    return f

def mat_ouro(c):
    """Ouro facetado (chifres, frisos, braçadeiras, canela, pés): topo claro, frente amarelo-ouro, lados ouro, embaixo escuro."""
    face = c["face"]
    base = {"up": AMARELO_CL, "down": OURO_ESC, "north": AMARELO, "south": OURO}.get(face, mix(AMARELO, OURO, 0.5))
    return contorno(base, 0.3) if na_borda(c) else base

def mat_roxo(c, frente=ROXO):
    """Armadura roxa facetada: topo roxo claro, frente roxo, lados um tom abaixo, baixo escuro, quinas escuras."""
    face = c["face"]
    base = {"up": ROXO_CL, "down": ROXO_ESC, "north": frente}.get(face, mix(ROXO, ROXO_ESC, 0.35))
    return mix(base, ROXO_FUNDO, 0.45) if na_borda(c) else base

def mundo(mat, rot, pivo):
    """Pinta uma peça girada pelo ponto já girado (o desenho fica no plano do mundo)."""
    A = _rotm(*rot)
    def f(c):
        c2 = dict(c); c2["p"] = girar_ponto(c["p"], A, pivo)
        return mat(c2)
    return f

def barra(nome, a, b, larg, esp, mat, n=(1.0, 0.0, 0.0), res=4):
    """Barra (friso, chifre reto) do ponto a ao ponto b, seção larg x esp, com a face larga para n."""
    d = tuple(b[i] - a[i] for i in range(3)); L = math.sqrt(_dot(d, d))
    x, y, z = a
    pc = peca(nome, [x - esp / 2, y - L - 0.2, z - larg / 2], [x + esp / 2, y + 0.2, z + larg / 2], mat, res=res)
    return osso(nome, list(a), euler(quadro(d, n)), [pc])

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
OLHO_CORTE0, OLHO_CORTE_INC = 0.45, 0.34     # pálpebra brava: a máscara corta o topo numa diagonal que desce para o bico

def olho(u, v):
    """Olho vermelho bravo (expressão neutra da ficha): a máscara roxa corta o alto numa diagonal que desce para o
    bico; íris vermelha grande, pupila escura do lado do bico e 1 brilho; branco só numa cunha atrás, contorno preto.
    u: ao longo da face (negativo = para o bico); v: para cima."""
    ru, rv = OLHO_RU, OLHO_RV
    uu = u / ru
    if abs(uu) > 1: return None
    corte = OLHO_CORTE0 + OLHO_CORTE_INC * u
    baixo = -rv * (0.86 - 0.12 * uu) * (1 - max(0.0, -uu) ** 2.4)
    cima = rv * (0.98 - 0.06 * uu) * (1 - max(0.0, -uu) ** 1.8)
    topo = min(cima, corte)
    if v < baixo or v > topo: return None
    if topo - v < 0.18: return PRETO                                       # fio da pálpebra
    ic = -0.12
    du = (uu - ic) / 0.74; dv = v / (rv * 0.96)
    if du * du + dv * dv <= 1 or (uu < ic and v >= baixo):
        if ((uu + 0.3) / 0.2) ** 2 + ((v + 0.05) / 0.55) ** 2 <= 1: return PRETO                 # pupila
        if ((uu + 0.05) / 0.13) ** 2 + ((v - topo + 0.38) / 0.17) ** 2 <= 1: return (255, 250, 245)   # brilho
        cor = VERM if v < topo - 0.45 else VERM_ESC                           # sombra da máscara no alto da íris
        if du * du + dv * dv > 0.8 and uu > ic: cor = VERM_FUNDO
        return cor
    return BRANCO if topo - v > 0.3 else BRANCO_SOMBRA

def cor_cabeca(p, face):
    """Crânio: rosto branco, roxo do elmo no alto, máscara roxa atrás do olho, vermelho na nuca."""
    x, y, z = p
    if face == "up" or y > 33.8: return ROXO
    if z > -4.0: return VERM_ESC
    if z > ZL + 0.9 and y > 30.2: return ROXO
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
            if v > OLHO_CORTE0 + OLHO_CORTE_INC * u + 0.1: return ROXO          # a máscara desce sobre o olho
            if u > OLHO_RU * 0.85: return ROXO                                  # e fecha atrás dele
        return mat_rosto(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face == "down": return OURO
    if face == "up": return AMARELO_CL
    if face in ("east", "west") and abs(z - (ZF - 1.7)) < 0.3 and abs(y - 31.6) < 0.24: return (110, 50, 10)   # narina
    if face == "north":
        larg = 0.3 + 0.8 * clamp((y - 29.6) / 2.4)
        return mix(AMARELO_CL, AMARELO, clamp((31.9 - y) / 1.6)) if abs(x) < larg else OURO
    return mix(AMARELO_CL, AMARELO, clamp((32.0 - y) / 1.0)) if y > 30.9 else mix(AMARELO, OURO, clamp((30.9 - y) / 1.2))

def mat_gema(cx, cy, W, H):
    """Gema: hexágono alto (pontas em cima e embaixo) com engaste de ouro e gema vermelha facetada."""
    meio = (H - W) / 2
    def f(c):
        x, y, z = c["p"]
        if c["face"] != "north": return mat_ouro(c)
        u = (x - cx) / (W / 2); v = (y - cy)
        lim = 1.0 if abs(v) <= meio else max(0.0, 1.0 - (abs(v) - meio) / (W / 2))
        borda = lim - abs(u)
        if borda < 0.1: return OURO_ESC
        if borda < 0.38: return AMARELO_CL if (u < 0 and v > 0) else (AMARELO if v > -meio else OURO)
        if (u + 0.2) ** 2 + ((v - 0.5) / 1.6) ** 2 < 0.03: return (255, 225, 220)
        if u < 0 and v > 0: return (250, 80, 84)
        if u > 0 and v < 0: return VERM_ESC
        return VERM
    return f

def so_gema(c, cor): return cor[0] > 150 and cor[1] < 100 and cor[2] < 100

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

def chifre(nome, base, d, n, segs, curvas, dobra):
    """Chifre de ouro anguloso de seção quadrada: segmentos que afinam; cada junta dobra 'curvas[k]' graus (positivo
    = para o lado de 'dobra'): sobe, dobra e sobe de novo. Ponta em cunha."""
    x, y0, z = base
    A0 = quadro(d, n)
    sinal = 1 if _dot(_col(A0, 2), dobra) >= 0 else -1
    def seg(k, ytop):
        L, W, T = segs[k]
        pcs = [peca(f"{nome}_{k}", [x - T / 2, ytop - L, z - W / 2], [x + T / 2, ytop + (0.45 if k else 0.0), z + W / 2], mat_ouro, res=3)]
        if k + 1 < len(segs): pcs.append(seg(k + 1, ytop - L))
        else:
            s = W / 1.4142
            pcs.append(peca(f"{nome}_pt", [x - T / 2 + 0.03, ytop - L - s / 2, z - s / 2], [x + T / 2 - 0.03, ytop - L + s / 2, z + s / 2],
                            mat_ouro, rot=(45, 0, 0), pivo=(x, ytop - L, z), res=3))
        rot = euler(A0) if k == 0 else [-curvas[k - 1] * sinal, 0, 0]
        return osso(f"{nome}_{k}", [x, ytop, z], rot, pcs)
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
        # máscara roxa sobre o olho: aba grossa descendo para o bico (o V bravo da ficha)
        ox0, ox1 = sorted((cx + FAC_T / 2 * lado - 0.5 * lado, cx + FAC_T / 2 * lado + 0.75 * lado))
        ang = math.degrees(math.atan(OLHO_CORTE_INC))
        zc0 = cz + 0.1
        yb = OLHO_Y + OLHO_CORTE0 + 0.12
        def mvis(c):
            if c["face"] == "down": return ROXO_FUNDO
            return mat_roxo(c, frente=ROXO_CL)
        cab.append(osso("viseira_" + s, [cx, yb, zc0], [0, FAC_ANG * lado, 0], [
            peca("viseira_" + s, [ox0, yb, cz - FAC_L / 2 - 0.4], [ox1, yb + 1.6, cz + FAC_L / 2 + 0.8],
                 mvis, rot=(-ang, 0, 0), pivo=(cx, yb, zc0), res=4)]))
        # máscara roxa atrás do olho (bochecha) e protetor da têmpora, de onde sai o chifre
        bx0, bx1 = sorted(((LX - 0.35) * lado, (LX + 0.5) * lado))
        cab.append(peca("bochecha_" + s, [bx0, 29.8, ZL + 0.5], [bx1, 35.0, ZL + 3.0], lambda c: mat_roxo(c, frente=ROXO), res=4))
        bx0, bx1 = sorted(((LX - 0.3) * lado, (LX + 0.42) * lado))
        cab.append(peca("elmo_guarda_" + s, [bx0, 31.6, ZL + 2.8], [bx1, 35.6, ZT + 0.6], lambda c: mat_roxo(c, frente=ROXO_ESC), res=3))
    # CAPACETE roxo cobrindo o alto da cabeça, com a crista roxa do meio e a ponte em V que desce entre os olhos
    def roxo_liso(c):
        face = c["face"]
        if face == "up": return ROXO_CL
        if face == "down": return ROXO_ESC
        return mix(ROXO, ROXO_CL, 0.35) if face == "north" else (ROXO if c["p"][1] > 34.4 else mix(ROXO, ROXO_ESC, 0.4))
    cab += g.arredondado2("elmo_casco", [-LX - 0.4, 33.0, ZF - 0.3], [LX + 0.4, 36.7, ZT + 0.8], roxo_liso, r=1.3, res=3)
    # crista roxa do elmo: uma aleta em losango no alto da testa, atrás da moldura dourada
    q = 1.4 * 1.4142
    cab.append(peca("elmo_crista", [-0.55, 36.6 - q / 2, ZF + 2.2], [0.55, 36.6 + q / 2, ZF + 4.6], lambda c: mat_roxo(c, frente=ROXO_CL),
                    rot=(45, 0, 0), pivo=(0, 36.6, ZF + 3.4), res=3))
    q = 1.5 * 1.4142
    cab.append(peca("elmo_ponte", [-1.15, 32.9, ZF - 0.55], [1.15, 34.0, ZF + 1.4], lambda c: mat_roxo(c, frente=ROXO_CL), res=4))
    cab.append(peca("elmo_ponte_v", [-q / 2, 33.0 - q / 2, ZF - 0.5], [q / 2, 33.0 + q / 2, ZF + 1.3], mat_roxo, rot=(0, 0, 45),
                    pivo=(0, 33.0, ZF), res=4))
    # moldura dourada em V: 2 frisos que descem das têmporas (base dos chifres) até a gema no meio da testa
    gx, gy, gz = 0.0, 33.9, ZF - 0.75
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        a = ((LX + 0.2) * lado, 36.2, ZL + 1.2)
        b = (0.9 * lado, gy + 0.8, ZF - 0.6)
        cab.append(barra("elmo_friso_" + s, a, b, 1.0, 0.9, mat_ouro, n=(0.0, 0.6, -0.8)))
    # gema vermelha num engaste dourado em losango no meio da testa
    cab += hexagono("gema", (gx, gy, gz), 2.4, 3.6, 1.0, mat_gema(gx, gy, 2.4, 3.6), res=8, brilho=so_gema)
    # bico amarelo curvo, largo de frente: base alta (tampa + quilha em V), meio que cai e gancho; mandíbula curta embaixo
    mb = mat_cor(cor_bico, borda=.05, curva=.25)
    def mq(c):
        f_ = c["face"]
        cor = AMARELO_CL if f_ in ("up", "east") else (AMARELO if f_ in ("north", "south") else mix(AMARELO, OURO, 0.5))
        return contorno(cor, 0.25) if na_borda(c) else cor
    fb = (29.4, 32.4)
    cab.append(peca("bico_tampa", [-1.75, 30.8, ZF - 2.3], [1.75, 32.7, ZF + 0.7], mb, faixa=fb, res=4))
    q = 1.75 * 1.4142
    cab.append(peca("bico_quilha", [-q / 2, 30.8 - q / 2, ZF - 2.2], [q / 2, 30.8 + q / 2, ZF + 0.6], mq, rot=(0, 0, 45),
                    pivo=(0, 30.8, ZF), faixa=fb, res=4))
    piv = (0, 32.5, ZF - 2.0)
    cab.append(peca("bico_meio", [-1.4, 30.5, ZF - 4.0], [1.4, 32.5, ZF - 1.9], mb, rot=(-20, 0, 0), pivo=piv, faixa=fb, res=4))
    cab.append(peca("bico_gancho", [-0.9, 29.2, ZF - 5.1], [0.9, 31.5, ZF - 3.6],
                    mat_cor(lambda p, f_: AMARELO_CL if f_ == "up" else mix(AMARELO, OURO, clamp((31.0 - p[1]) / 1.2)), borda=.1, curva=.2),
                    rot=(-32, 0, 0), pivo=(0, 31.5, ZF - 3.6), faixa=(29.2, 31.5), res=4))
    cab.append(peca("bico_baixo", [-1.15, 29.4, ZF - 2.6], [1.15, 30.4, ZF + 0.5],
                    mat_cor(lambda p, f_: (150, 60, 8) if (f_ != "down" and p[1] > 30.2) else OURO, borda=.08), res=4))
    # barbela vermelha grande: 2 lóbulos que pendem sob o bico
    def mbar(c):
        y = c["p"][1]; face = c["face"]
        if face == "down": return VERM_ESC
        base = VERM if y > 27.6 else VERM_ESC
        return contorno(base, 0.2) if na_borda(c) and face not in ("north",) else base
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.05 * lado, 1.1 * lado))
        cab.append(osso("barbela_" + s, [0.0, 29.8, ZF - 0.5], [-6, 0, -4 * lado], [
            peca("barbela_" + s, [x0, 26.0, ZF - 1.4], [x1, 29.9, ZF + 0.3], mbar, res=4)]))
    cab.append(crista_ossos())
    cab += juba_ossos()
    return cab

def _dir(elev, fora, lado):
    """Direção de uma pena da juba: para trás, 'elev' graus acima da horizontal e 'fora' para o lado."""
    a = math.radians(elev)
    return (fora * lado, math.sin(a), math.cos(a))

def crista_ossos():
    """Chifres e penas do alto: 2 chifres dourados altos e angulosos que saem das têmporas (na ponta da moldura em V):
    sobem, dobram para fora e para trás e sobem de novo; e as penas de chama do alto da juba."""
    pc = []
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        dobra = (0.75 * lado, 0.0, 0.66)
        n = (-0.66, 0.0, 0.75 * lado)                      # eixo da dobra perpendicular a 'dobra'
        pc.append(chifre("chifre_" + s, ((LX + 0.2) * lado, 36.0, ZL + 1.4), (0.12 * lado, 1.0, 0.08), n,
                         [(4.0, 2.3, 2.3), (3.6, 2.0, 2.0), (4.4, 1.7, 1.7)], [72, -72], dobra))
    for k, (x, y, z, elev, fora, L, W, fx) in enumerate(JUBA_ALTO):
        lado = 1 if x >= 0 else -1
        n = (0.38, 0.0, -0.92) if x == 0 else (0.75 * lado, 0.66, 0.0)
        T0, T1 = (1.35, 1.2) if x == 0 else (1.05, 0.9)
        pc.append(pluma(f"crista{k}", (x, y, z), _dir(elev, fora, lado), n,
                        [(L * 0.52, W, T0), (L * 0.30, W * 0.68, T1)], 10, fx, dobra=(0, 0, 1)))
    return osso("crista", [0, 35.8, -6.0], [0, 0, 0], pc)

# JUBA de PENAS achatadas e afiladas (base larga, ponta em losango), em camadas, nascendo da nuca e de trás do elmo e
# varrendo para trás e para cima como chama; vermelhas e vermelho-escuras, quase sem laranja; as do meio, mais longas.
# alto (no osso da crista): (x, y, z da raiz, elevação, abertura, comprimento, largura, faixas)
JUBA_ALTO = [(0.0, 36.6, -3.6, 66, 0.0, 8.4, 3.4, F_JUBA_PONTA),
             (-1.4, 36.0, -3.4, 48, 0.16, 10.2, 3.2, F_JUBA), (1.4, 36.0, -3.4, 48, 0.16, 10.2, 3.2, F_JUBA)]
# lados (espelhadas): (y da raiz, elevação, abertura, comprimento, largura, faixas)
JUBA_LADO = [(36.0, 54, 0.50, 10.8, 3.8, F_JUBA_ESC), (34.6, 30, 0.58, 13.0, 4.0, F_JUBA_PONTA), (33.0, 12, 0.55, 13.6, 4.0, F_JUBA),
             (31.4, -6, 0.42, 11.6, 4.0, F_JUBA_ESC), (29.8, -26, 0.14, 8.4, 3.8, F_JUBA)]
# meio (de trás): (x, y, z da raiz, elevação, abertura, comprimento, largura, faixas)
JUBA_MEIO = [(0.0, 35.0, -2.6, 40, 0.0, 13.4, 4.2, F_JUBA), (0.0, 33.2, -2.3, 14, 0.0, 13.6, 4.2, F_JUBA_PONTA),
             (-1.5, 32.2, -2.5, 2, 0.18, 12.2, 3.8, F_JUBA_ESC), (1.5, 32.2, -2.5, 2, 0.18, 12.2, 3.8, F_JUBA_ESC),
             (0.0, 30.8, -2.6, -22, 0.0, 9.6, 4.0, F_JUBA)]
JUBA_MIOLO = ([-4.4, 29.2, -4.2], [4.4, 38.0, 1.6])

def mat_juba_miolo(c):
    """Miolo da juba pintado como PENAS SOBREPOSTAS: fileiras de pontas em losango (vermelho e vermelho-escuro) com o
    contorno escuro embaixo de cada fileira."""
    x, y, z = c["p"]; face = c["face"]
    if face == "down": return VERM_FUNDO
    a = x if face in ("north", "south", "up") else z
    b = y if face != "up" else -z
    fila = math.floor(b / 1.6)
    fa = ((a + (fila % 2) * 1.1) % 2.2) / 2.2
    fb = (b % 1.6) / 1.6
    if fb < 0.18 + 0.5 * abs(fa - 0.5): return VERM_FUNDO
    return VERM if fa < 0.5 else VERM_ESC

def juba_ossos():
    pc = list(g.arredondado2("juba_miolo", JUBA_MIOLO[0], JUBA_MIOLO[1], mat_juba_miolo, r=1.8, res=3))
    # a face larga das penas fica a ~45° (entre o lado e o alto): de lado leem como leque de chama e de costas como o
    # bloco vermelho de penas sobrepostas, sem virar lâmina de perfil
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        for k, (y, elev, fora, L, W, fx) in enumerate(JUBA_LADO):
            pc.append(pluma(f"juba{k}_{s}", (2.7 * lado, y, -3.4), _dir(elev, fora, lado), (0.72 * lado, 0.69, 0.0),
                            [(L * 0.52, W, 1.05), (L * 0.30, W * 0.68, 0.9)], 10, fx, dobra=(0, 1, 0)))
    for k, (x, y, z, elev, fora, L, W, fx) in enumerate(JUBA_MEIO):
        sx = (1.0 if k % 2 == 0 else -1.0) if x == 0 else (1.0 if x > 0 else -1.0)
        lado = 1 if x >= 0 else -1
        pc.append(pluma(f"nuca{k}", (x, y, z), _dir(elev, fora, lado), (0.7 * sx, 0.71, 0.0),
                        [(L * 0.52, W, 1.1), (L * 0.30, W * 0.68, 0.95)], 10, fx, dobra=(0, 1, 0)))
    return pc

# ================= PESCOÇO, TRONCO, OMBREIRAS E PEITORAL =================
def cor_tronco(p, face):
    x, y, z = p
    a = z if face in ("east", "west") else x
    fila = math.floor(y / 1.8)
    fa = ((a + (fila % 2) * 1.2) % 2.4) / 2.4
    if face != "up" and (y % 1.8) / 1.8 < 0.14 + 0.12 * (2 * abs(fa - 0.5)) ** 2: return ROXO_ESC
    return ROXO

def borda_ouro(c, dist):
    """Placa roxa com friso dourado: a face de cima/frente leva o friso a 'dist' da beirada; as laterais são douradas."""
    x, y, z = c["p"]; face = c["face"]
    (x0, y0, z0), (x1, y1, z1) = c["b"]
    if face in ("up", "north"):
        if face == "up": e = min(x - x0, x1 - x, z - z0, z1 - z)
        else: e = min(x - x0, x1 - x, y - y0, y1 - y)
        if e < dist: return OURO_ESC if e < 0.15 else (AMARELO_CL if face == "up" else AMARELO)
        return ROXO_CL if face == "up" else ROXO
    if face == "down": return ROXO_ESC
    return OURO if not na_borda(c) else OURO_ESC

def aba_ouro(c, lado):
    """Aba da ponta da ombreira: a face de fora roxa com o friso dourado em volta; o resto dourado."""
    x, y, z = c["p"]; face = c["face"]
    fora = "east" if lado > 0 else "west"
    if face != fora: return mat_ouro(c)
    (x0, y0, z0), (x1, y1, z1) = c["b"]
    e = min(y - y0, y1 - y, z - z0, z1 - z)
    if e < 0.15: return OURO_ESC
    if e < 0.75: return AMARELO
    return ROXO

def escudo(x, y):
    """Escudo do peitoral (retângulo de cima + V embaixo): distância até a borda (negativa = fora)."""
    return min(4.2 - abs(x), 25.6 - y, (y - 17.6 - abs(x)) / 1.4142)

def mat_peitoral(c):
    """Peitoral roxo em V com moldura dourada e um segundo V dourado por dentro (quadro "Peitoral (Fênix)")."""
    x, y, z = c["p"]
    if c["face"] != "north": return mat_ouro(c) if c["face"] != "down" else ROXO_ESC
    e = escudo(x, y)
    if e < 0.12: return OURO_ESC
    if e < 0.75: return AMARELO if y > 20.0 else OURO
    if abs(y - (19.8 + abs(x))) < 0.38 and abs(x) < 2.8: return AMARELO                 # V de dentro
    return ROXO_CL if y > 23.6 else ROXO

def tronco_ossos():
    pcs = []
    mt = mat_cor(cor_tronco, borda=.0, curva=.25)
    pcs += g.arredondado2("tronco", [-4.8, 12.6, -8.0], [4.8, 25.0, 2.0], mt, r=2.0, faixa=(12, 26), res=2)
    pcs += g.arredondado("tronco_tras", [-4.2, 12.2, 0.5], [4.2, 21.4, 8.2], mt, r=1.5, faixa=(12, 22), res=2)
    pcs += g.arredondado("uropigio", [-2.8, 14.6, 6.0], [2.8, 22.4, 10.6], mt, r=1.0, res=2)
    # peitoral roxo em V com moldura dourada
    zf = -9.2
    pcs.append(peca("peitoral", [-4.2, 21.8, zf], [4.2, 25.6, zf + 1.3], mat_peitoral, res=8))
    s = 4.2 * 1.4142
    rot = (0, 0, 45); piv = (0.0, 21.8, zf + 0.65)
    pcs.append(peca("peitoral_v", [-s / 2, 21.8 - s / 2, zf + 0.1], [s / 2, 21.8 + s / 2, zf + 1.2], mundo(mat_peitoral, rot, piv),
                    rot=rot, pivo=piv, res=8))
    # gema vermelha no centro, num engaste dourado em losango
    gy = 23.5
    pcs += hexagono("peitoral_gema", (0.0, gy, zf - 0.35), 2.2, 3.0, 0.8, mat_gema(0.0, gy, 2.2, 3.0), res=8, brilho=so_gema)
    # penas brancas e lilás "estruturadas" em camadas pontudas abaixo do peitoral (fileiras sobrepostas, alternando)
    FILAS = [(19.0, (-3.3, -1.65, 0.0, 1.65, 3.3), -8.0), (16.6, (-2.5, -0.85, 0.85, 2.5), -7.8),
             (14.2, (-1.7, 0.0, 1.7), -7.5), (11.9, (-0.85, 0.85), -7.2)]
    for f, (y, xs, z) in enumerate(FILAS):
        for k, x in enumerate(xs):
            fx = F_BRANCO if (f + k) % 2 == 0 else F_LILAS_CL
            # pontas abrindo para os lados (o leque pontudo das "penas estruturadas")
            pcs.append(pena(f"peito{f}_{k}", (x, y, z - 0.12 * (k % 2)), (0.16 * x, -1.0, 0.22), (0.12 * x, 0, -1.0), 5.0, 2.3, 0.9,
                            fx, res=4))
        if f >= 1:
            xl = abs(xs[0]) + 1.4
            for lado in (-1, 1):
                pcs.append(pena(f"peito_lado{f}_{'d' if lado < 0 else 'e'}", (xl * lado, y + 0.3, z + 0.35), (0.14 * lado, -1.0, 0.2),
                                (0.3 * lado, 0, -1.0), 4.8, 2.4, 0.9, F_ROXO, res=3))
    # costas: penas vermelhas no meio (a faixa vermelha de costas) e roxas dos lados
    for k, (x, y, z, L, fx) in enumerate(((-1.6, 24.4, 0.6, 7.4, F_ROXO), (1.6, 24.4, 0.6, 7.4, F_ROXO), (0.0, 24.6, -0.6, 8.0, F_JUBA),
                                          (-1.4, 21.4, 4.4, 6.4, F_ROXO_VERM), (1.4, 21.4, 4.4, 6.4, F_ROXO_VERM))):
        pcs.append(pena(f"costas{k}", (x, y, z), (0.1 * x, -0.45, 1.0), (0, 1, 0.2), L, 3.2, 1.0, fx))
    return pcs

def ombreiras_ossos():
    """Ombreiras roxas grandes e angulosas com borda dourada (quadro "Ombreira (Armadura)"): uma placa larga que sai do
    ombro quase na horizontal e uma segunda mais baixa e mais para fora, as duas com o friso dourado em volta."""
    ossos = []
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        # placa de cima larga e fina, quase na horizontal, e a aba da ponta caindo (perfil em L, como na ficha)
        x0, x1 = sorted((2.6 * lado, 11.2 * lado))
        cima = g.arredondado("ombreira_" + s, [x0, 25.4, -5.0], [x1, 27.0, 4.0], lambda c: borda_ouro(c, 0.9), r=0.4, res=3)
        x0, x1 = sorted((10.0 * lado, 11.4 * lado))
        aba = [peca("ombreira_aba_" + s, [x0, 22.0, -4.6], [x1, 26.0, 3.6], lambda c: aba_ouro(c, lado), res=3)]
        ossos.append(osso("ombreira_" + s, [2.6 * lado, 27.0, -0.5], [0, 0, -8 * lado],
                          cima + [osso("ombreira_aba_" + s, [10.6 * lado, 26.0, -0.5], [0, 0, 12 * lado], aba)]))
    return ossos

def pescoco_ossos():
    pc = []
    def cor_pesc(p, f_):
        x, y, z = p
        if f_ == "north" or z < -6.2: return BRANCO
        return VERM_ESC if z > -4.4 else BRANCO_SOMBRA
    def escama_branca(c):
        """Penas brancas em escama no pescoço: fileiras desencontradas com a borda de baixo em arco rosado."""
        x, y, z = c["p"]; face = c["face"]
        if face == "down": return BRANCO_SOMBRA
        if face == "up": return BRANCO
        a = x if face in ("north", "south") else z
        fila = math.floor(y / 1.3)
        fa = ((a + (fila % 2) * 0.8) % 1.6) / 1.6
        fb = (y % 1.3) / 1.3
        if fb < 0.16 + 0.35 * (2 * abs(fa - 0.5)) ** 2: return BRANCO_SOMBRA
        return BRANCO
    mp = mat_cor(cor_pesc, borda=.0, curva=.2)
    pc += g.octogono("pescoco", [-2.2, 24.4, -8.0], [2.2, 31.0, -3.4], mp, r=0.8, faixa=(24, 31))
    pc += g.arredondado("garganta", [-2.1, 25.0, -8.8], [2.1, 30.4, -6.6], escama_branca, r=0.5, res=4)
    # gola roxa na base do pescoço, entre as ombreiras
    def cor_gola(c):
        x, y, z = c["p"]; face = c["face"]
        if face == "up": return ROXO_CL
        if face == "down": return ROXO_FUNDO
        return ROXO if (y % 1.2) > 0.25 else ROXO_ESC
    pc += g.octogono("gola_roxa", [-3.4, 23.8, -8.6], [3.4, 26.6, -2.0], cor_gola, r=1.0)
    return pc

# ================= ASAS =================
# fileiras de cima para baixo: (y da raiz, ângulos no anel, raio x, raio z, comprimento, largura, abertura, varrida, faixas)
# as de cima roxas (sob as ombreiras); nas laterais, penas de chama vermelhas com pontas laranja e amarelas
ASA = [
    (24.0, (-48, -20, 8, 36), 4.8, 5.8, 7.8, 3.3, 34, 18, F_ROXO),
    (22.6, (-56, -30, -4, 22, 48, 72), 5.0, 6.0, 9.6, 3.4, 30, 24, F_ROXO_VERM),
    (21.0, (-60, -36, -12, 12, 36, 60, 82), 5.8, 6.4, 12.6, 3.8, 34, 28, F_CHAMA1),
    (19.6, (-58, -34, -10, 14, 38, 62, 84), 6.0, 6.6, 14.0, 4.0, 34, 32, F_CHAMA2),
    (18.2, (-54, -30, -6, 18, 42, 66, 88), 6.0, 6.6, 15.2, 4.0, 34, 36, F_CHAMA3),
]
ASA_ZC = -0.4

def asa_ossos(lado):
    """Asa: 5 fileiras em telha, as de cima roxas e depois as penas de chama (vermelho -> laranja -> amarelo nas
    pontas); as pontas abrem um pouco para fora e varrem para trás e acabam acima das pernas."""
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

# ================= CAUDA DE FÊNIX TRIPLA =================
RAIZ_CAUDA = (0.0, 19.4, 8.6)
# 3 foices de cada lado, em ângulos desencontrados (de lado são 6 foices em leque): (lado, elevação, abertura, comprimento)
FOICES = [(-1, 50, 0.10, 22.0), (1, 32, 0.12, 23.0), (-1, 16, 0.18, 23.0), (1, 0, 0.20, 22.0), (-1, -16, 0.26, 20.0), (1, -32, 0.28, 18.0)]

def cauda_ossos():
    """Cauda de fênix tripla: leque grande de penas longas em FOICE (4 segmentos que afinam e curvam para cima),
    varrendo para trás e para cima, vermelho -> laranja -> amarelo nas pontas. Sem correntes."""
    pc = []
    for k, (lado, elev, fora, L) in enumerate(FOICES):
        a = math.radians(elev)
        d = (fora * lado, math.sin(a), math.cos(a))
        raiz = (0.9 * lado, 20.6 - 0.25 * k, 9.2 + 0.1 * k)
        segs = [(L * 0.30, 5.8, 1.3), (L * 0.27, 5.0, 1.2), (L * 0.22, 3.9, 1.1), (L * 0.17, 2.8, 1.0)]
        pc.append(pluma(f"foice{k}", raiz, d, (lado, 0.0, 0.0), segs, 10, F_FOICE, dobra=(0, 1, 0), lingua=0.08))
    return osso("cauda", list(RAIZ_CAUDA), [0, 0, 0], pc)

ONDAS = [(f"foice{k}", 4, (1.6, 1.4, 0.0)) for k in range(len(FOICES))]
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ================= PERNAS =================
def perna(lado):
    """Perna longa e forte: coxa e calça de penas roxas, canela dourada com braçadeira no joelho e no tornozelo
    (quadro "Braçadeira de Pernas"), pés dourados e garras claras."""
    s = "d" if lado < 0 else "e"; xc = 3.4 * lado; zc = 0.4
    pp = []
    pp += g.arredondado("coxa_" + s, [xc - 2.1, 9.0, zc - 2.2], [xc + 2.1, 14.2, zc + 2.0], mat_cor(cor_tronco, borda=.0, curva=.25),
                        r=0.8, res=3)
    for k, phi in enumerate((-80, -10, 60, 130)):
        r_ = math.radians(phi)
        nrm = (math.cos(r_) * lado, 0.0, math.sin(r_))
        raiz = (xc + 1.5 * nrm[0], 12.4, zc + 1.5 * nrm[2])
        pp.append(pena(f"calca{k}_{s}", raiz, (0.18 * nrm[0], -1.0, 0.18 * nrm[2] + 0.08), nrm, 4.4, 3.0, 0.9, F_ROXO))
    def cor_canela(p, f_):
        if f_ == "down": return OURO_ESC
        return AMARELO if (p[1] % 1.2) > 0.2 else OURO
    pp += g.octogono("tarso_" + s, [xc - 1.45, 2.4, zc - 1.45], [xc + 1.45, 9.6, zc + 1.45], mat_cor(cor_canela, borda=.06, curva=.2),
                     r=0.45, faixa=(2.4, 9.6))
    # braçadeiras douradas: a do joelho, larga e em 2 degraus, e a do tornozelo
    pp += g.octogono("joelheira_" + s, [xc - 2.3, 6.2, zc - 2.3], [xc + 2.3, 8.2, zc + 2.3], mat_ouro, r=0.65)
    pp += g.octogono("joelheira2_" + s, [xc - 1.95, 8.2, zc - 1.95], [xc + 1.95, 9.0, zc + 1.95], mat_ouro, r=0.55)
    pp += g.octogono("tornozeleira_" + s, [xc - 2.05, 2.4, zc - 2.05], [xc + 2.05, 4.2, zc + 2.05], mat_ouro, r=0.6)
    # pés dourados com dedos grossos e garras claras
    def cor_pe(p, f_):
        if f_ == "down": return OURO_ESC
        if f_ in ("up", "east", "west") and (p[2] % 1.5) < 0.26: return OURO
        return AMARELO_CL if f_ == "up" else AMARELO
    mpe = mat_cor(cor_pe, borda=.12, curva=.3)
    mg = lambda c: GARRA if c["face"] in ("up", "north", "east", "west") and not na_borda(c) else GARRA_SOMBRA
    pp.append(peca("pe_" + s, [xc - 1.8, 0.0, zc - 1.8], [xc + 1.8, 2.4, zc + 1.6], mpe, faixa=(0, 2.4), res=2))
    for nome, giro, dx, comp in (("meio", 0, 0.0, 4.4), ("fora", -22 * lado, 1.4 * lado, 3.9), ("dentro", 16 * lado, -1.3 * lado, 3.5)):
        x0, z0 = xc + dx, zc - 1.2
        pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
            peca(f"dedo_{nome}_{s}", [x0 - 0.95, 0, z0 - comp], [x0 + 0.95, 2.0, z0 + 0.4], mpe, faixa=(0, 2.0), res=2),
            peca(f"garra_{nome}_{s}", [x0 - 0.7, 0.0, z0 - comp - 1.5], [x0 + 0.7, 1.5, z0 - comp + 0.2], mg, res=2)]))
    pp.append(peca("dedo_tras_" + s, [xc - 0.8, 0, zc + 1.0], [xc + 0.8, 1.6, zc + 3.2], mpe, faixa=(0, 1.6), res=2))
    pp.append(peca("garra_tras_" + s, [xc - 0.6, 0, zc + 3.1], [xc + 0.6, 1.2, zc + 4.3], mg, res=2))
    return osso("perna_" + s, [xc, 13.2, zc], [0, 0, 0], pp)

# ================= LOD =================
# Peças estruturais nunca somem de longe. Penas e foices somem INTEIRAS (corpo, segmentos e ponta juntos).
import json as _json, re as _re
ESTRUTURA = _re.compile(r"^(bico|barbela|cranio|queixo|faceta|viseira|bochecha|elmo|gema|chifre|juba_miolo|tronco|uropigio|peitoral|"
                        r"ombreira|pescoco|garganta|gola_roxa|coxa|tarso|joelheira|tornozeleira|pe_|dedo_|garra_)")

def unidade(nome):
    """Nome da pena/foice a que a peça pertence (corpo, segmentos e ponta)."""
    n = _re.sub(r"_pt$", "", nome)
    m = _re.match(r"^((?:crista|foice|nuca)\d+|juba\d+_[de])(?:_\d+)?$", n)
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
K_CAB, SOBE_CAB = 0.94, 1.0      # cabeça logo acima das ombreiras, com o pescoço curto e a barbela à frente
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
PALETA = {"roxo_esc": ROXO_ESC, "roxo": ROXO, "lilas": LILAS, "branco": BRANCO, "amarelo": AMARELO, "laranja": LARANJA,
          "verm": VERM, "verm_esc": VERM_ESC}
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
    return {"roxo+lilas": p["roxo_esc"] + p["roxo"] + p["lilas"], "vermelho": p["verm"] + p["verm_esc"], "laranja": p["laranja"],
            "amarelo-ouro": p["amarelo"], "branco": p["branco"]}

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
    # arte lado a lado: a ilustração grande da 3ª ficha e o modelo num ângulo parecido, na mesma altura
    ref = Image.open(REF_ARTE).convert("RGB")
    FUNDO = (24, 26, 34)
    YAW = 42
    mod = previa2.desenhar((faces, tex), YAW, -6, escala=14, fundo=FUNDO, margem=10)
    a = np.asarray(mod).astype(int)
    m = np.abs(a - np.array(FUNDO)).max(-1) > 10
    ys, xs = np.nonzero(m)
    mod = mod.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    topo, chao = 25, 720                                # da ponta dos chifres ao chão, na ilustração
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
