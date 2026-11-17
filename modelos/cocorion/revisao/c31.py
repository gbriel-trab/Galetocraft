"""Cocórion (#005, Ar): o Galo dos Ventos, galo guerreiro branco e esguio, juba branca espetada em camadas,
cicatrizes vermelhas, asas em capa com a espiral verde do vento, hakama preta com faixa branca e katana na cintura.

Versão refeita do zero (rodadas c*). Ideias da montagem:
- poucas peças grandes: cabeça, pescoço e tronco em volumes chanfrados (arredondado2), sem cubinhos soltos;
- juba de espetos largos e curtos (pirâmides em degraus, de seção em losango), todos varridos para trás e para cima
  num fluxo único, encostados uns nos outros como telhas;
- asas em capa: duas camadas de penas largas que pendem do ombro, afinam em ponta e abrem pouco embaixo;
- cauda de penas em foice esguias (creme e verde) num leque alto e estreito;
- a luz é pintada pela normal NO MUNDO de cada face e por um degradê de altura único para o corpo todo
  (calculados depois da montagem, a partir da árvore de ossos), por isso as peças se fundem em vez de se destacarem."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
import previa                                  # matriz de rotação na mesma ordem do Blockbench
from galo_base import peca, osso, mix, clamp, na_borda

ID = "cocorion"; NOME = "Cocórion"; NUMERO = 5
ALTURA = 2.4
QUADRUPEDE = False
ROSTO = ((0, 29.0, -5.0), 7.5)
N_CAUDA, SEG_CAUDA = 8, 4
ONDAS = [(f"cauda{k}", SEG_CAUDA, (1.4, 1.0, 0.0)) for k in range(N_CAUDA)]
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (amostrada na ficha; a mesma das versões anteriores) ----------------
BRANCO = (252, 241, 232); CLARO = (255, 250, 244); SOMBRA_B = (214, 198, 192)
LINHA = (226, 212, 204)                    # risco suave entre as penas
CARVAO = (44, 45, 46); CARVAO_CL = (62, 64, 66); PRETO_H = (24, 25, 24)
VERDE = (58, 106, 48); VERDE_ESC = (36, 74, 30); VERDE_CL = (78, 130, 62)
AMAR = (255, 192, 14); AMAR_ESC = (226, 138, 0); AMAR_CL = (255, 214, 70)
LARANJA_B = (236, 158, 10)
VERM = (210, 50, 38); VERM_ESC = (150, 30, 22); VERM_X = (190, 42, 32)
OURO = (250, 184, 12); OURO_CL = (255, 214, 80); OURO_ESC = (190, 122, 8)
SOBR = (34, 33, 34)
GARRA = (40, 40, 42)

LADO_KATANA = -1          # o lado -x aparece à direita de quem olha de frente (como a katana da ficha)
LADO_CICATRIZ = 1         # o lado +x é o que a arte mostra (asterisco na bochecha e cruz na testa)

# ---------------- transformações (calculadas depois da montagem) ----------------
TRANSF = {}               # nome da peça -> lista [(nome_do_osso, R, origem)] da raiz até a peça

def preparar_transformacoes(raizes):
    """Percorre a árvore de ossos e guarda, para cada peça, a cadeia de rotações até ela (inclusive a da peça)."""
    pecas = {p.uuid: p for p in g.PECAS}
    def andar(no, cadeia):
        if isinstance(no, str):
            p = pecas.get(no)
            if p is None: return
            c = list(cadeia)
            if any(abs(v) > 1e-9 for v in p.rot): c.append(("__peca__", previa.rot(*p.rot), list(p.pivo)))
            TRANSF[p.nome] = c
            return
        r = no["rotation"]
        c = cadeia + ([(no["name"], previa.rot(*r), list(no["origin"]))] if any(abs(v) > 1e-9 for v in r) else [])
        for f in no["children"]: andar(f, c)
    for no in raizes: andar(no, [])

def para_mundo(nome, p, ate=None):
    """Leva o ponto p (coordenadas da peça) para o mundo; com 'ate', para o referencial desenhado do osso 'ate'
    (aplica só as rotações abaixo dele)."""
    cadeia = TRANSF.get(nome, [])
    if ate is not None:
        for k, (n, _, _) in enumerate(cadeia):
            if n == ate: cadeia = cadeia[k + 1:]; break
    q = list(p)
    for _, R, o in reversed(cadeia):
        v = previa.mv(R, [q[i] - o[i] for i in range(3)])
        q = [v[i] + o[i] for i in range(3)]
    return q

def normal_mundo(nome, face):
    n = list(g.NORMAL[face])
    for _, R, _ in reversed(TRANSF.get(nome, [])): n = previa.mv(R, n)
    return n

# ---------------- luz ----------------
def escuro(c): return (int(c[0] * .68), int(c[1] * .64), int(c[2] * .68))
def tons(c, f):
    f = clamp(f, -1, 1)
    return mix(c, CLARO, f) if f >= 0 else mix(c, escuro(c), -f)

FAIXA_Y = (4.0, 38.0)     # degradê de altura único (no mundo) para tudo

# ---------------- pixel-art de penas (telhas) no branco ----------------
TELHA_BORDA = (201, 194, 189)            # #C9C2BD: borda de baixo de cada pena
TELHA_LUZ = (255, 247, 230)              # luz creme no alto de cada pena
TELHA_W, TELHA_H = 3.0, 2.4              # tamanho de uma pena (unidades)
TELHA_INVERTE = ("juba",)                # peças que crescem para +y (a ponta da pena fica para cima na textura)
CAMADA_DE_BAIXO = ("asa_l", "costas")    # penas que ficam por baixo de outra camada
TELHA_FORA = ("juba", "katana", "barbela", "bico")   # sem telhas (desenho próprio)

def branco_de_pena(cor):
    return min(cor) > 205 and max(cor) - min(cor) < 40

def telha(c, cor):
    """Penas em telha desenhadas na face (3 tons): luz creme no alto, a cor no meio e a borda de baixo em V
    cinza-claro; as fileiras se desencontram. Só no branco, nas faces laterais."""
    face = c["face"]
    if face in ("up", "down") or not branco_de_pena(cor) or c["nome"].startswith(TELHA_FORA): return cor
    (x0, y0, z0), (x1, y1, z1) = c["b"]
    fw = (x1 - x0) if face in ("north", "south") else (z1 - z0)
    fh = y1 - y0
    u = (c["i"] + .5) / c["tw"] * fw
    v = (c["j"] + .5) / c["th"] * fh
    if c["nome"].startswith(TELHA_INVERTE): v = fh - v
    fila = math.floor(v / TELHA_H)
    fx = ((u + (fila % 2) * TELHA_W / 2) % TELHA_W) / TELHA_W
    fy = (v % TELHA_H) / TELHA_H                       # 0 = alto da pena, 1 = ponta
    fundo = 0.6 + 0.4 * (1 - abs(2 * fx - 1))           # ponta em V no meio da pena
    if fy > fundo: return mix(cor, TELHA_BORDA, .45)    # o que aparece abaixo da ponta é a pena de baixo, na sombra
    if fy > fundo - 0.16: return TELHA_BORDA if branco_de_pena(cor) else cor
    if fy < 0.3 and fx < 0.75: return mix(cor, TELHA_LUZ, .85)
    return cor

def mat_luz(cor_fn, topo=.22, baixo=-.42, grad=.36, borda=.0, frente=.04, faixa=FAIXA_Y, penas=True, atras=.22, dentro=.18):
    """Luz pela normal NO MUNDO (cima clara, baixo na sombra), degradê de altura no mundo igual para todas as peças,
    penas em telha no branco e oclusão: o que fica atrás (nuca, trás da juba) e as faces viradas para dentro do corpo
    (dentro da capa) descem um tom, para as camadas descolarem umas das outras."""
    def f(c):
        base = cor_fn(c)
        if base is None: return None
        eh_branco = branco_de_pena(base)
        if penas: base = telha(c, base)
        nome = c["nome"]
        nx, ny, nz = normal_mundo(nome, c["face"])
        k = topo * ny if ny > 0 else -baixo * ny
        k += -frente * nz
        xw, yw, zw = para_mundo(nome, c["p"])
        k += grad * (clamp((yw - faixa[0]) / (faixa[1] - faixa[0])) - 0.6)
        if eh_branco:
            k -= atras * clamp((zw - 1.0) / 8.0)
            if nome.startswith(CAMADA_DE_BAIXO): k -= 0.16                     # camada de baixo: um tom abaixo
            # sombra de contato sob a cabeça (separa cabeça e juba do peito e da capa)
            if 20.5 < yw < 25.0 and zw < 2.5 and abs(xw) < 7.5 and not nome.startswith(("juba", "barbela")):
                k -= 0.2 * (1 - abs(yw - 23.4) / 2.6)
            if abs(xw) > 2.0 and nx * xw < 0: k -= dentro * min(1.0, -nx * (1 if xw > 0 else -1) * 1.0)
        if borda and na_borda(c): k -= borda
        return tons(base, k)
    return f

def cor_fixa(cor): return lambda c: cor

def com_raiz(cor_fn, y0, L, sentido, k=.55, ate=.4):
    """Sombra de oclusão na raiz da pena (onde ela entra por baixo da camada de cima): o branco perto da raiz puxa
    para o cinza quente e clareia até a ponta. Dá a leitura de 'telhas' em camadas, como na arte."""
    def f(c):
        cor = cor_fn(c)
        if cor is None or sum(cor) < 600: return cor
        t = (c["p"][1] - y0) * sentido / max(L, 1e-6)
        if t < ate: return mix(cor, SOMBRA_B, k * (1 - clamp(t / ate)) ** 1.5)
        return cor
    return f

def escama(a, y, larg=2.4, alt=1.8, k=.09):
    """Penas em escama, grandes e suaves: só um arco fino embaixo de cada pena."""
    fila = math.floor(y / alt)
    fa = ((a + (fila % 2) * larg / 2) % larg) / larg
    fy = (y % alt) / alt
    return fy < k + 0.14 * (2 * abs(fa - 0.5)) ** 2

def risco_x(a, y, ca, cy, r, w=0.3, torto=0.0):
    da, dy = a - ca, y - cy
    if max(abs(da), abs(dy)) > r: return False
    j = torto * math.sin(round(da * 2) * 1.7 + round(dy * 2) * 0.9)
    return abs(da - dy + j) < w or abs(da + dy - j) < w

# ---------------- rotações ----------------
def norm(v):
    n = math.sqrt(sum(a * a for a in v)) or 1.0
    return [a / n for a in v]

def apontar(d):
    """Rotação (rx, ry, 0) que leva o eixo local +y para a direção d."""
    dx, dy, dz = norm(d)
    a = math.degrees(math.acos(clamp(dy, -1, 1)))
    b = math.degrees(math.atan2(dx, dz)) if a > 1e-3 else 0.0
    return [a, b, 0.0]

def torcao_para(d, fora):
    """Giro (em volta do próprio eixo) que deixa a normal local -z o mais virada possível para 'fora'."""
    R = previa.rot(*apontar(d)); fora = norm(fora)
    melhor, tm = -9, 0
    for t in range(-180, 180, 5):
        n = previa.mv(R, previa.mv(previa.rot(0, t, 0), [0, 0, -1]))
        s_ = sum(n[i] * fora[i] for i in range(3))
        if s_ > melhor: melhor, tm = s_, t
    return tm

# ---------------- pena da juba: lâmina grossa deitada na juba, em telha, com a ponta solta ----------------
def cor_juba(xc, yp):
    """Pena da juba: na face larga, metade clara e metade base (como uma pirâmide com aresta no meio); a ponta em
    losango segue a diagonal; espessura no tom de base."""
    base = mix(BRANCO, SOMBRA_B, .42)
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        if face in ("north", "south"):
            u = x - xc
            (_, y0, _), (_, y1, _) = c["b"]
            if yp is None and (y - y0) < 0.45 and not c["nome"].endswith("_0"): return TELHA_BORDA   # sombra sob o degrau
            return TELHA_LUZ if u < 0 else mix(BRANCO, TELHA_BORDA, .55)     # duas facetas: luz e sombra
        if face == "up": return CLARO
        return base
    return f

def pena_juba(nome, raiz, d, L, W, T, fora):
    """Espeto da juba: lâmina grossa (largura W, espessura T) que cresce na direção d e afina em 3 degraus até a ponta
    em losango (como os espetos em blocos da arte); a face larga fica virada para 'fora' (a normal da juba)."""
    x, y, z = raiz
    m = mat_luz(com_raiz(cor_juba(x, None), y, L, 1, k=.6, ate=.45))
    ws = (W, W * 0.6, W * 0.3); ts = (T, T * 0.9, T * 0.8)
    cortes = (0.0, 0.34, 0.6, 0.86)
    pcs = []
    for k in range(3):
        w, t = ws[k], ts[k]
        pcs.append(peca(f"{nome}_{k}", [x - w / 2, y + L * cortes[k] - (1.2 if k == 0 else 0.15), z - t / 2],
                        [x + w / 2, y + L * cortes[k + 1], z + t / 2], m))
    s_ = ws[2] / 1.4142; yp = y + L - ws[2] / 2
    pcs.append(peca(f"{nome}_3", [x - s_ / 2, yp - s_ / 2, z - ts[2] / 2 + .04], [x + s_ / 2, yp + s_ / 2, z + ts[2] / 2 - .04],
                    mat_luz(com_raiz(cor_juba(x, yp), y, L, 1, k=.6, ate=.45)), rot=(0, 0, 45), pivo=(x, yp, z)))
    return osso(nome, list(raiz), apontar(d), [osso(nome + "_t", list(raiz), [0, torcao_para(d, fora), 0], pcs)])

# ---------------- lâmina de pena (gola, costas, capa) ----------------
def cor_lamina(cx, eixo_u, cy=None, diag=False, claro=BRANCO, base=None, desenho=None):
    """Pena larga em 2 tons chapados: metade clara e metade base divididas por uma raque clara; 'desenho(c)' pinta
    por cima (a espiral da asa)."""
    base = base or mix(BRANCO, SOMBRA_B, .45)
    def f(c):
        if desenho:
            d = desenho(c)
            if d is not None: return d
        x, y, z = c["p"]; face = c["face"]
        larga = ("east", "west") if eixo_u == "z" else ("north", "south")
        if face in larga:
            u = (z if eixo_u == "z" else x) - cx
            if diag: u = u + (y - cy)
            if abs(u) < 0.14: return CLARO
            return claro if u < 0 else base
        if face == "up": return claro
        return base
    return f

def lamina(nome, raiz, rot, L, W, T=1.0, eixo="z", claro=BRANCO, base=None, desenho=None, res=None, fr=(0.62, 0.2, 0.62),
           cor=None):
    """Pena larga pendurada da raiz (para -y): corpo, faixa que estreita e ponta em losango.
    eixo='z': a face larga olha para ±x; eixo='x': olha para ±z. 'cor(yp)' troca a pintura (yp = centro da ponta,
    None para o corpo)."""
    x, y, z = raiz
    Lb, Lm, wm = L * fr[0], L * fr[1], W * fr[2]
    s = wm / 1.4142
    yp = y - Lb - Lm
    cx = z if eixo == "z" else x
    if cor is not None:
        c0, c1 = cor(None), cor(yp)
    else:
        c0 = cor_lamina(cx, eixo, claro=claro, base=base, desenho=desenho)
        c1 = cor_lamina(cx, eixo, yp, True, claro=claro, base=base, desenho=desenho)
    m, mp = mat_luz(com_raiz(c0, y, L, -1)), mat_luz(com_raiz(c1, y, L, -1))
    if eixo == "z":
        pcs = [peca(nome, [x - T / 2, y - Lb, z - W / 2], [x + T / 2, y, z + W / 2], m, res=res),
               peca(nome + "_m", [x - T / 2 + .03, y - Lb - Lm, z - wm / 2], [x + T / 2 - .03, y - Lb + .1, z + wm / 2], m, res=res),
               peca(nome + "_p", [x - T / 2 + .06, yp - s / 2, z - s / 2], [x + T / 2 - .06, yp + s / 2, z + s / 2], mp,
                    rot=(45, 0, 0), pivo=(x, yp, z), res=res)]
    else:
        pcs = [peca(nome, [x - W / 2, y - Lb, z - T / 2], [x + W / 2, y, z + T / 2], m, res=res),
               peca(nome + "_m", [x - wm / 2, y - Lb - Lm, z - T / 2 + .03], [x + wm / 2, y - Lb + .1, z + T / 2 - .03], m, res=res),
               peca(nome + "_p", [x - s / 2, yp - s / 2, z - T / 2 + .06], [x + s / 2, yp + s / 2, z + T / 2 - .06], mp,
                    rot=(0, 0, 45), pivo=(x, yp, z), res=res)]
    return osso(nome, list(raiz), list(rot), pcs)

# ---------------- cabeça ----------------
EY = 29.2                                   # altura do olho
FX, ZF, QX = 1.5, -7.0, 4.2                 # meia largura da frente, z da frente, meia largura do crânio
ZQ = ZF + (QX - FX)
FAC_T = 1.5
FAC_L = (QX - FX) * 1.4142
FAC_O = ((FX + QX) / 2, (ZF + ZQ) / 2)
FAC_C = (FAC_O[0] - 0.7071 * FAC_T / 2, FAC_O[1] + 0.7071 * FAC_T / 2)
OLHO_U, OLHO_RU, OLHO_RV = 0.0, 1.75, 1.2
SOB_K = 0.40                                # inclinação da sobrancelha (desce para o bico)
SOB_Y = 0.72

def olho(u, v):
    """Olho estreito da ficha: topo cortado na diagonal pela sobrancelha; íris verde-viva no lado do bico, pupila
    preta com brilho; esclera branca atrás."""
    du = u - OLHO_U
    ru, rv = OLHO_RU, OLHO_RV
    if abs(du) > ru or abs(v) > rv: return None
    cq = max(0.0, abs(du) - (ru - 0.34)) / 0.34, max(0.0, abs(v) - (rv - 0.34)) / 0.34
    if cq[0] ** 2 + cq[1] ** 2 > 1: return None
    if v > SOB_Y - 0.06 + SOB_K * du: return None
    if du < ru * 0.38:
        if du > ru * 0.26: return (18, 70, 14)                               # contorno de trás da íris
        pu = du + ru * 0.32
        if (pu / 0.36) ** 2 + ((v + 0.08) / 0.52) ** 2 <= 1:
            if ((pu - 0.12) / 0.15) ** 2 + ((v - 0.18) / 0.15) ** 2 <= 1: return (255, 255, 255)
            return (8, 10, 8)
        return mix((96, 232, 64), (26, 140, 22), clamp((0.45 - v) / 1.3))
    return (250, 250, 248)

def mat_faceta(lado):
    """Face diagonal do rosto: olho inteiro numa face plana; asterisco na bochecha do lado da arte, riscos do outro."""
    fora = "east" if lado > 0 else "west"
    def cor(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u, v = z - FAC_C[1], y - EY
            o = olho(u, v)
            if o is not None: return o
            if lado == LADO_CICATRIZ:
                if risco_x(u, v, 0.15, -2.05, 0.7, 0.16, torto=0.08) or (abs(v + 2.05) < 0.14 and abs(u - 0.15) < 0.55):
                    return VERM
            else:
                if abs((v + 1.6) - 0.8 * (u - 0.8)) < 0.13 and abs(u - 0.8) < 0.45: return VERM
                if (u - 0.0) ** 2 + (v + 1.9) ** 2 < 0.04: return VERM
        return BRANCO
    return mat_luz(cor, grad=.2)

def cor_testa(c):
    """Testa: pequena cruz vermelha de traço fino acima do olho do lado da arte."""
    x, y, z = c["p"]
    if c["face"] == "north":
        da, dy = x - 1.0 * LADO_CICATRIZ, y - 31.35
        if max(abs(da), abs(dy)) < 0.5 and (abs(da - dy) < 0.15 or abs(da + dy) < 0.15): return VERM
        if abs(da + 0.62 * LADO_CICATRIZ) < 0.12 and abs(dy - 0.42) < 0.12: return VERM
    return BRANCO

def montar_cabeca():
    cab = []
    mb = mat_luz(cor_fixa(BRANCO), grad=.2)
    # crânio: volume bem chanfrado; a frente estreita e as facetas do olho fazem o rosto afinar para o bico
    cab += g.arredondado2("cranio", [-QX, 25.0, ZQ - 0.3], [QX, 32.0, 2.2], mb, r=1.6)
    cab.append(peca("rosto_frente", [-FX - 0.05, 25.3, ZF], [FX + 0.05, 31.0, ZQ + 0.4], mb))
    cab.append(peca("testa", [-2.6, 30.6, ZF + 0.2], [2.6, 32.8, ZQ + 1.6], mat_luz(cor_testa, grad=.2),
                    rot=(28, 0, 0), pivo=(0, 30.6, ZF + 0.2), res=6))
    cab += g.arredondado("queixo", [-2.4, 24.6, ZF + 0.9], [2.4, 26.4, ZQ + 2.6], mb, r=0.6, rot=(-14, 0, 0), pivo=(0, 26.4, ZQ + 2.6))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 25.4, cz - FAC_L / 2], [cx + FAC_T / 2, 31.0, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, EY, cz), res=8))
        # sobrancelha: bloco preto grosso apoiado no olho, descendo para o bico (V de frente); vai até a juba
        xo = cx + FAC_T / 2 * lado
        x0, x1 = sorted((xo - 0.5 * lado, xo + 0.4 * lado))
        yb = EY + SOB_Y + 0.1
        rs = (-math.degrees(math.atan(SOB_K)), 0, 0)
        msob = mat_luz(cor_fixa(SOBR), topo=.35, baixo=-.25, grad=0.0)
        cab.append(osso("sobrancelha_" + s, [cx, EY, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s, [x0, yb - 0.1, cz - FAC_L / 2 - 0.5], [x1, yb + 1.1, cz + FAC_L / 2 + 0.15], msob,
                 rot=rs, pivo=(cx, yb, cz + OLHO_U))]))
    # bico em cunha: base larga, gancho estreito curvado para baixo; mandíbula mais escura e recuada
    def cor_bico(c):
        x, y, z = c["p"]
        if c["face"] in ("east", "west") and abs(z - (ZF - 0.9)) < 0.28 and abs(y - 28.9) < 0.24: return PRETO_H
        if c["face"] == "up": return AMAR_CL
        return AMAR if c["face"] != "down" else AMAR_ESC
    mbi = mat_luz(cor_bico, topo=.2, baixo=-.35, grad=0.0)
    # de lado é uma cunha que afina para a frente e termina num gancho que desce; de frente estreita para baixo
    cab.append(peca("bico_base", [-1.8, 27.5, ZF - 1.5], [1.8, 29.6, ZF + 0.5], mbi, res=4))
    cab.append(peca("bico_meio", [-1.35, 27.6, ZF - 3.1], [1.35, 29.3, ZF - 1.3], mbi, res=4,
                    rot=(-8, 0, 0), pivo=(0, 29.3, ZF - 1.3)))
    cab.append(peca("bico_gancho", [-0.9, 26.5, ZF - 4.0], [0.9, 28.6, ZF - 2.7], mbi, res=4,
                    rot=(-34, 0, 0), pivo=(0, 28.6, ZF - 2.8)))
    cab.append(peca("bico_baixo", [-1.2, 26.5, ZF - 2.5], [1.2, 27.6, ZF + 0.4],
                    mat_luz(cor_fixa(AMAR_ESC), topo=.05, grad=0.0, penas=False), res=4, rot=(10, 0, 0), pivo=(0, 27.6, ZF + 0.4)))
    # barbelas: dois lóbulos vermelhos compridos sob o bico (lado a lado, com um vão escuro no meio)
    def cor_barb(c):
        if abs(c["p"][0]) < 0.18: return VERM_ESC
        return mix((232, 56, 42), (186, 36, 28), clamp((26.0 - c["p"][1]) / 3.4))
    mbar = mat_luz(cor_barb, grad=0.0, topo=.1)
    for lado, fim in ((-1, 23.0), (1, 23.4)):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((0.0, 1.45 * lado)); x2, x3 = sorted((0.15 * lado, 1.2 * lado))
        cab.append(osso("barbela_" + s, [0.0, 26.6, ZF - 1.0], [0, 0, -2 * lado], [
            peca("barbela_a_" + s, [x0, fim + 1.2, ZF - 1.8], [x1, 26.7, ZF - 0.2], mbar, res=4),
            peca("barbela_b_" + s, [x2, fim, ZF - 1.6], [x3, fim + 1.3, ZF - 0.45], mbar, res=4)]))
    cab.append(montar_crista())
    return osso("cabeca", [0, 26.0, -1.5], [0, 0, 0], cab)

K_CAB = 1.1                                # a cabeça inteira (com a juba) um pouco maior, como na arte

def cabeca_grande():
    ini = len(g.PECAS)
    cab = montar_cabeca()
    g.transformar(ini, [cab], (0.0, 26.0, -2.0), k=K_CAB, sobe=0.0)
    return cab

# penas da juba: (raiz, direção, comprimento). Deitadas sobre a juba como telhas (a face larga segue a normal da
# juba), todas varridas para trás num fluxo só, com a ponta levantada; o lado +x (o da arte) um pouco mais cheio.
def espeto_fino(nome, raiz, d, L, W, T, fora):
    """Espeto fino da juba (3 peças): base larga, faixa que estreita e ponta em losango, sobrepostas (sem salto
    grande entre os degraus); a face larga fica virada para 'fora'."""
    x, y, z = raiz
    wm = W * 0.58; s_ = wm / 1.4142
    yp = y + L - wm / 2
    m = mat_luz(com_raiz(cor_juba(x, None), y, L, 1, k=.55, ate=.5))
    mp = mat_luz(com_raiz(cor_juba(x, yp), y, L, 1, k=.55, ate=.5))
    pcs = [peca(nome + "_0", [x - W / 2, y - 1.2, z - T / 2], [x + W / 2, y + L * 0.46, z + T / 2], m),
           peca(nome + "_1", [x - wm / 2, y + L * 0.36, z - T * 0.45], [x + wm / 2, yp + 0.15, z + T * 0.45], m),
           peca(nome + "_2", [x - s_ / 2, yp - s_ / 2, z - T * 0.4], [x + s_ / 2, yp + s_ / 2, z + T * 0.4], mp,
                rot=(0, 0, 45), pivo=(x, yp, z))]
    return osso(nome, list(raiz), apontar(d), [osso(nome + "_t", list(raiz), [0, torcao_para(d, fora), 0], pcs)])

# ---------------- juba em 3 anéis concêntricos em volta de um polo inclinado para trás ----------------
JUBA_C = (0.0, 30.4, -0.6)                       # centro do crânio (os espetos irradiam dele)
JUBA_POLO = norm([0.0, 0.72, 0.69])              # eixo da coroa: para cima e para trás
_E1 = [1.0, 0.0, 0.0]
_E2 = [0.0, JUBA_POLO[2], -JUBA_POLO[1]]         # perpendicular ao polo, para cima e para a frente
# (ângulo ao polo, azimutes, raio da raiz, comprimento, largura, varrida para trás)
JUBA_ANEIS = [
    (84, (-112, -84, -56, -28, 0, 28, 56, 84, 112), 4.3, 4.4, 2.5, .45),            # frente baixa: testa e têmporas
    (56, (-160, -128, -96, -64, -32, 0, 32, 64, 96, 128, 160), 3.9, 6.0, 2.8, .65),  # meio
    (26, (-150, -105, -60, -15, 30, 75, 120, 165), 3.4, 7.6, 3.1, .5),               # trás alto
]

def juba_espetos():
    """Lista (raiz, direção, comprimento, largura, para onde a face olha) dos espetos dos 3 anéis. Cada anel tem
    ângulo coerente; os espetos varrem um pouco para trás; nenhum cobre o rosto; o lado +x (o da arte) é 6% mais
    comprido."""
    out = []
    for r, (th, azs, R, L, W, var) in enumerate(JUBA_ANEIS):
        t = math.radians(th)
        for k, a in enumerate(azs):
            a_ = math.radians(a + (7 if r == 1 and k % 2 else 0))
            d0 = [math.cos(t) * JUBA_POLO[i] + math.sin(t) * (math.cos(a_) * _E2[i] + math.sin(a_) * _E1[i]) for i in range(3)]
            if d0[1] < -0.8 or (d0[2] < -0.55 and d0[1] < 0.45): continue        # rosto e queixo livres
            d = norm([d0[0], d0[1] + var * 0.25, d0[2] + var])
            raiz = [JUBA_C[i] + R * d0[i] for i in range(3)]
            Lk = L * (1.06 if d0[0] > 0.05 else 1.0) * (0.92 if k % 2 else 1.0)
            fora = [1.0 if d0[0] >= 0 else -1.0, 0.2, 0.0] if abs(d0[0]) > 0.15 else [(-1) ** k, 0.2, 0.0]
            out.append((raiz, d, Lk, W, fora))
    return out

def montar_crista():
    """Juba: base arredondada que cobre o alto, a nuca e os lados do crânio e uma coroa de espetos finos em 3 anéis
    (frente baixa, meio, trás alto)."""
    crista = []
    crista += g.arredondado2("crista_base", [-4.3, 27.0, -3.8], [4.3, 34.2, 3.6], mat_luz(cor_fixa(BRANCO)), r=1.8)
    for k, (raiz, d, L, W, fora) in enumerate(juba_espetos()):
        crista.append(espeto_fino(f"juba{k}", raiz, d, L, W, W * 0.46, fora))
    return osso("crista", [0, 32.0, -1.0], [0, 0, 0], crista)

# ---------------- tronco ----------------
def cor_tronco(c):
    x, y, z = c["p"]
    face = c["face"]
    if face == "north" and z < -4.8:
        if risco_x(x, y, 0.0, 19.6, 2.3, 0.36, torto=0.08):
            pontas = max(abs(x), abs(y - 19.6)) > 1.9
            return VERM_ESC if pontas and (round(x * 2) + round(y * 2)) % 2 == 0 else VERM_X
    a = z if face in ("east", "west") else x
    if face != "up" and escama(a, y): return LINHA
    return BRANCO

def montar_tronco():
    """Tronco de ave esguio: núcleo chanfrado que afunila para a cintura e peito com projeção moderada."""
    pc = []
    mt = mat_luz(cor_tronco)
    pc += g.arredondado2("torax", [-3.5, 15.4, -4.2], [3.5, 23.0, 3.2], mt, r=1.6, res=3)
    pc += g.arredondado2("cintura", [-3.0, 13.0, -3.4], [3.0, 17.0, 2.8], mt, r=1.1, res=3)
    pc += g.arredondado("peito", [-2.9, 16.2, -5.4], [2.9, 22.4, -3.4], mt, r=0.9, rot=(-6, 0, 0), pivo=(0, 16.2, -4.4), res=3)
    # costas: 3 penas largas deitadas, do pescoço até a cintura
    for k, (x, y, L) in enumerate(((-1.5, 23.2, 7.0), (1.5, 23.0, 7.4), (0.0, 19.6, 6.4))):
        pc.append(lamina(f"costas{k}", (x, y, 3.0 + 0.3 * (k == 2)), (-12, 0, 0), L, 3.6, T=0.9, eixo="x"))
    return pc

# ---------------- hakama ----------------
def cor_hakama(c):
    x, y, z = c["p"]
    face = c["face"]
    a = z if face in ("east", "west") else x
    if face == "up": return CARVAO_CL
    if y < 7.4 and face != "down": return PRETO_H
    return CARVAO if math.floor((a + 0.3) / 1.4) % 2 == 0 else (56, 58, 60)

# ---------------- asas ----------------
# espiral do vento (quadro "Padrão da asa"): um "9" de traço grosso cuja perna desce, vira para trás e enrola de volta
# para cima num gancho pequeno. Coordenadas (a, v): a > 0 = para a frente da criatura, v para cima.
GLIFO_P = [(-0.78, 2.35), (0.59, 2.35), (0.59, 0.78), (-2.35, 0.78), (-2.35, 4.5), (2.75, 4.5), (3.33, 3.53),
           (3.33, -1.96), (1.96, -4.7), (-1.96, -5.5), (-5.6, -5.1), (-6.4, -3.6), (-5.88, -1.6), (-3.6, -1.4),
           (-3.33, -2.75)]
GLIFO_C = (17.6, 0.8)                    # (y, z) do centro da espiral no plano da asa
GLIFO_K = 0.62
GLIFO_W = 0.86

def _dist_seg(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    t = clamp(((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy + 1e-9))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))

def glifo(y, z):
    a, v = -(z - GLIFO_C[1]) / GLIFO_K, (y - GLIFO_C[0]) / GLIFO_K
    if not (-7.5 < a < 4.5 and -6.6 < v < 5.6): return False
    # traço quadrado (máx. das distâncias em a e v), como os blocos da ficha
    for i in range(len(GLIFO_P) - 1):
        (ax, ay), (bx, by) = GLIFO_P[i], GLIFO_P[i + 1]
        if _dist_seg(a, v, ax, ay, bx, by) < GLIFO_W: return True
    return False

def cor_capa(desenho):
    """Pena da capa: branca com escamas suaves na face de fora (a espiral por cima); a metade de baixo da ponta em
    losango um pouco mais escura (dá volume à serrilha)."""
    base = mix(BRANCO, SOMBRA_B, .35)
    def fabrica(yp):
        def f(c):
            d = desenho(c)
            if d is not None: return d
            x, y, z = c["p"]; face = c["face"]
            if face in ("east", "west"):
                if yp is not None and y < yp - 0.2: return base
                if escama(z, y, 2.8, 2.4, .07): return LINHA
                return BRANCO
            if face == "up": return CLARO
            return base
        return f
    return fabrica

def montar_asa(lado):
    """Asa em capa (como a ficha): ombro arredondado e duas camadas de penas largas em LEQUE que saem do ombro e
    abrem para baixo (estreita em cima, larga embaixo, borda de baixo serrilhada pelas pontas). A espiral é
    desenhada no plano da asa: cada pena leva o ponto para o referencial do osso da asa."""
    s = "d" if lado < 0 else "e"
    xi = 3.7 * lado
    PIV = (xi, 23.6, ZH)                 # a asa gira presa pela frente do ombro (como uma capa aberta)
    fora = "east" if lado > 0 else "west"
    osso_asa = "asa_" + s
    def desenho(c):
        if c["face"] != fora: return None
        q = para_mundo(c["nome"], c["p"], ate=osso_asa)
        return VERDE if glifo(q[1], q[2]) else None
    cc = cor_capa(desenho)
    pc = []
    # penas longas (por dentro): leque de 5, da frente (inclinada para a frente) para trás (mais aberta e comprida)
    for k, (zr, L, rx, ry) in enumerate(((-1.8, 11.8, 10, 10), (-0.8, 12.8, 3, 5), (0.2, 13.4, -5, 0), (1.2, 13.4, -12, -5),
                                         (2.2, 12.8, -19, -10))):
        pc.append(lamina(f"asa_l{k}_{s}", (xi + 0.35 * lado, 22.8, zr), (rx, ry * lado, 0), L, 3.5, T=1.0, cor=cc, res=4,
                         fr=(0.6, 0.18, 0.62)))
    # cobertura (por fora): leque de 4 penas largas e mais curtas
    for k, (zr, L, rx, ry) in enumerate(((-1.5, 8.8, 9, 9), (-0.4, 9.6, 1, 3), (0.7, 9.6, -8, -3), (1.8, 9.0, -16, -9))):
        pc.append(lamina(f"asa_c{k}_{s}", (xi + 1.25 * lado, 24.2, zr), (rx, ry * lado, 0), L, 4.0, T=1.0, cor=cc, res=4,
                         fr=(0.6, 0.18, 0.62)))
    x0, x1 = sorted((xi - 0.9 * lado, xi + 2.3 * lado))
    pc += g.arredondado2("asa_ombro_" + s, [x0, 20.8, -3.4], [x1, 25.4, 2.0],
                         mat_luz(lambda c: VERDE if desenho(c) else BRANCO), r=1.2, res=4)
    # pena verde por dentro (aparece atrás e embaixo, como na ficha)
    pc.append(lamina(f"asa_v_{s}", (xi - 0.2 * lado, 19.0, 4.6), (-18, 0, 0), 10.0, 2.8, T=0.8, claro=VERDE, base=VERDE_ESC))
    return osso(osso_asa, list(PIV), [0, ASA_RY * lado, ASA_RZ * lado], pc)

ZH = -3.6                 # z da dobradiça da capa (frente do ombro)
ASA_RY, ASA_RZ = 16, 13   # a capa vira a face para a frente (a espiral aparece de frente) e abre embaixo

# ---------------- cauda ----------------
CREME = (250, 238, 220); CREME_LUZ = (255, 248, 232)

def mat_pena_cauda(t0, t1, verde):
    """Pena da cauda em pixel-art de 3 tons ao longo da pena: as creme têm luz creme em cima, creme no meio e a borda
    de baixo cinza-claro (com um toque verde na raiz); as verdes têm um fio verde-claro em cima, verde no meio e
    verde-escuro embaixo. A face de baixo fica na sombra."""
    def cor(c):
        (_, y0, z0), (_, y1, z1) = c["b"]
        fy = (c["p"][1] - y0) / max(y1 - y0, 1e-6)              # 0 = embaixo, 1 = em cima
        t = t0 + (t1 - t0) * clamp((c["p"][2] - z0) / max(z1 - z0, 1e-6))
        face = c["face"]
        # seções da pena (pixel-art da ficha): a cada ~2,4 unidades ao longo da pena o tom alterna um pouco
        barba = face in ("east", "west") and math.floor((c["p"][2] - z0 + 0.6 * (c["nome"][-1] == "1")) / 2.4) % 2 == 1
        if verde:
            if barba and 0.24 <= fy <= 0.78: return mix(VERDE, VERDE_ESC, .45)
            if face == "up": return VERDE_CL
            if face == "down": return VERDE_ESC
            if fy > 0.78: return VERDE_CL
            if fy < 0.24: return VERDE_ESC
            return VERDE
        if face == "up": return CREME_LUZ
        if face == "down": return TELHA_BORDA
        if t < 0.22 and fy < 0.5: return VERDE
        if barba and 0.2 <= fy <= 0.76: return mix(CREME, TELHA_BORDA, .35)
        if fy > 0.76: return CREME_LUZ
        if fy < 0.2: return TELHA_BORDA
        return CREME
    return mat_luz(cor, grad=0.15, penas=False, atras=0.08, dentro=0.0)

def pena_cauda(nome, raiz, rot0, curvas, L, H, esp, verde=False):
    """Pena em foice: 4 blocos encadeados bem sobrepostos (ossos '<nome>_k'), estreita na raiz, alta no meio e
    afinando até a ponta em losango menor (ponta separada); 'curvas' dobra cada junta para baixo aos poucos (sem salto
    grande de ângulo entre os segmentos)."""
    fr = [0.24, 0.27, 0.26, 0.23]
    alt = [0.55, 0.92, 0.82, 0.6]
    ee = [0.9, 1.0, 0.92, 0.8]
    n = len(fr)
    def seg(k, pos, t0):
        px, py, pz = pos
        h = H * alt[k]; Ls = L * fr[k]; e = esp * ee[k]
        r = list(rot0) if k == 0 else [curvas[k - 1], 0, 0]
        t1 = t0 + fr[k]
        ov = 1.3 if k > 0 else 0.4
        filhos = [peca(f"{nome}_{k}", [px - e / 2, py - h * 0.5, pz - ov], [px + e / 2, py + h * 0.5, pz + Ls],
                       mat_pena_cauda(t0, t1, verde), res=3)]
        if k + 1 < n:
            filhos.append(seg(k + 1, (px, py, pz + Ls - 0.1), t1))
        else:
            q = h * 0.8 / 1.4142
            filhos.append(peca(f"{nome}_pt", [px - e * 0.38, py - q / 2, pz + Ls - q / 2 + 0.3], [px + e * 0.38, py + q / 2, pz + Ls + q / 2 + 0.3],
                               mat_pena_cauda(0.95, 1.0, verde), rot=(45, 0, 0), pivo=(px, py, pz + Ls + 0.3), res=3))
        return osso(f"{nome}_{k}", list(pos), r, filhos)
    return seg(0, raiz, 0.0)

# pares (creme larga por cima, verde logo abaixo): (raiz y, elevação, dobras das 3 juntas, comprimento, altura).
# Sobem e dobram a ponta para trás e para baixo (a soma das dobras passa da elevação: a ponta termina descendo).
CAUDA_PARES = [(21.4, 76, (20, 28, 36), 23.0, 5.4), (20.2, 56, (16, 23, 30), 25.0, 5.6),
               (19.0, 36, (12, 17, 23), 24.5, 5.4), (17.8, 14, (7, 10, 14), 20.0, 4.8)]

def montar_cauda():
    """Leque de penas em foice que sai de trás da capa e sobe para trás: cada par tem uma creme por cima e uma verde
    logo abaixo; os pares abrem para os dois lados alternadamente."""
    penas = []
    for k, (y, e, cv, L, H) in enumerate(CAUDA_PARES):
        sx = 1 if k % 2 == 0 else -1
        penas.append(pena_cauda(f"cauda{2 * k}", (0.55 * sx, y, 3.2), (-e, 9 * sx, 0), cv, L, H, 1.1, False))
        penas.append(pena_cauda(f"cauda{2 * k + 1}", (-0.35 * sx, y - 1.3, 3.5), (-(e - 10), 6 * sx, 0),
                                tuple(v * 0.9 for v in cv), L * 0.95, H * 0.9, 1.0, True))
    return osso("cauda", [0, 17.0, 3.4], [0, 0, 0], penas)

# ---------------- katana ----------------
def mat_metal(cima, frente, lado, baixo):
    return g.mat_facetado(cima, frente, lado, baixo, quina=-0.3)

def mat_cabo(c):
    x, y, z = c["p"]
    t = (z - c["b"][0][2]) % 1.2
    meio = abs((c["j"] + 0.5) / c["th"] - 0.5) if c["face"] in ("east", "west") else abs((c["i"] + 0.5) / c["tw"] - 0.5)
    if c["face"] in ("east", "west", "up", "down") and 0.3 < t < 0.9 and meio < 0.3: return BRANCO
    return VERDE_ESC if na_borda(c) else VERDE

def montar_katana(base):
    """Katana ao longo de z (cabo para a frente, bainha para trás) a partir da tsuba em 'base'."""
    bx, by, bz = base
    def pc_(nome, de, ate, mat, **kw):
        return g.peca(nome, [de[0] + bx, de[1] + by, de[2] + bz], [ate[0] + bx, ate[1] + by, ate[2] + bz], mat, **kw)
    ouro = mat_metal(OURO_CL, OURO, mix(OURO, OURO_ESC, .4), OURO_ESC)
    bainha = mat_metal((70, 72, 78), (36, 38, 42), (28, 30, 34), (16, 16, 20))
    return [pc_("katana_cabo", [-0.7, -0.7, -6.2], [0.7, 0.7, -0.3], mat_cabo, res=4),
            pc_("katana_pomo", [-0.8, -0.8, -6.8], [0.8, 0.8, -6.15], ouro, res=4),
            pc_("katana_tsuba_a", [-1.7, -0.6, -0.4], [1.7, 0.6, 0.2], ouro, res=4),
            pc_("katana_tsuba_b", [-0.6, -1.7, -0.35], [0.6, 1.7, 0.15], ouro, res=4),
            pc_("katana_bainha", [-0.55, -0.7, 0.1], [0.55, 0.7, 14.0], bainha),
            pc_("katana_kojiri", [-0.6, -0.75, 13.8], [0.6, 0.75, 14.9], ouro, res=4)]

# ---------------- pernas ----------------
def cor_perna(c):
    """Perna amarela com faixas de escama (linha mais escura a cada ~1,2 de altura)."""
    if c["face"] == "down": return AMAR_ESC
    if c["face"] != "up" and (c["p"][1] % 1.2) < 0.16: return mix(AMAR, AMAR_ESC, 0.6)
    return AMAR

def perna(lado):
    """Hakama de uma perna até o joelho (prisma chanfrado que abre embaixo + pregas inclinadas) e perna de ave grossa
    com pé grande de 3 dedos com garras pretas e 1 atrás."""
    s = "d" if lado < 0 else "e"; xc = 2.7 * lado; zc = 0.3
    pp = []
    def bx(a, b): return sorted((a * lado, b * lado))
    mh = mat_luz(cor_hakama, grad=0.3, topo=.15, baixo=-.4)
    x0, x1 = bx(0.1, 4.4)
    pp += g.octogono("hakama_" + s, [x0, 6.8, -4.2], [x1, 14.6, 3.9], mh, r=1.0, rot=(0, 0, 8 * lado), pivo=(2.0 * lado, 14.6, 0))
    for k, (a, b, inc, abre) in enumerate(((0.2, 2.2, 10, 4), (2.1, 4.1, 6, 10))):
        x0, x1 = bx(a, b)
        pp.append(peca(f"prega{k}_" + s, [x0, 6.8, -4.8], [x1, 14.2, -3.9], mh, rot=(inc, 0, abre * lado),
                       pivo=((a + b) / 2 * lado, 14.2, -4.3)))
    x0, x1 = bx(3.8, 4.7)
    pp.append(peca("prega_lado_" + s, [x0, 7.0, -3.2], [x1, 14.2, 3.0], mh, rot=(0, 0, 12 * lado), pivo=(4.2 * lado, 14.2, 0)))
    ma = mat_luz(cor_perna, grad=0.2, topo=.2, baixo=-.3)
    # perna de ave: canela de cima mais grossa (sai da hakama), tornozelo marcado e canela de baixo mais fina
    pp += g.octogono("coxa_" + s, [xc - 1.85, 4.6, zc - 1.85], [xc + 1.85, 9.0, zc + 1.85], ma, r=0.7)
    pp += g.octogono("tarso_" + s, [xc - 1.45, 1.2, zc - 1.3], [xc + 1.45, 5.0, zc + 1.6], ma, r=0.5)
    mg = mat_luz(cor_fixa(GARRA), grad=0.0, topo=.3)
    mdedo = mat_luz(lambda c: AMAR if c["face"] != "down" else AMAR_ESC, grad=0.0, topo=.2, baixo=-.3)
    for nome, dx, ang, comp in (("meio", 0.0, 0, 4.2), ("fora", 1.9 * lado, 26 * lado, 3.4), ("dentro", -1.9 * lado, -22 * lado, 3.2)):
        x0 = xc + dx
        pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, zc - 0.6], [0, -ang, 0], [
            peca(f"dedo_{nome}_{s}", [x0 - .95, 0, zc - 0.6 - comp], [x0 + .95, 2.0, zc + 0.8], mdedo),
            peca(f"garra_{nome}_{s}", [x0 - .8, 0.0, zc - 0.6 - comp - 1.5], [x0 + .8, 1.7, zc - 0.4 - comp], mg)]))
    mtras = mat_luz(lambda c: GARRA if c["p"][2] > zc + 2.9 else (AMAR if c["face"] != "down" else AMAR_ESC), grad=0.0)
    pp.append(peca("dedo_tras_" + s, [xc - .75, 0, zc + 1.0], [xc + .75, 1.5, zc + 4.0], mtras))
    return osso("perna_" + s, [xc, 13.5, zc], [0, 0, 0], pp)

# ---------------- montagem ----------------
def montar():
    TRANSF.clear()
    g.D = 3                                  # 3 px por unidade: dá para desenhar as penas em telha com 3 tons
    corpo = []
    corpo += montar_tronco()
    # cintura da hakama e faixa branca com nó e duas tiras
    mh = mat_luz(cor_hakama, grad=0.3, topo=.15, baixo=-.4)
    corpo += g.arredondado("hakama_cint", [-3.7, 12.6, -4.1], [3.7, 15.0, 3.7], mh, r=0.5)
    mf = mat_luz(cor_fixa(BRANCO), grad=0.0)
    corpo += g.arredondado("faixa", [-3.85, 14.2, -4.35], [3.85, 15.8, 3.9], mf, r=0.4)
    # nó na frente-lado (lado +x, o da arte), laço de duas orelhas e duas pontas em blocos que descem sobre a hakama
    nx, nz = 1.9, -4.9
    corpo.append(peca("no_faixa", [nx - 0.9, 13.5, nz - 0.6], [nx + 0.9, 16.1, nz + 0.7], mf, rot=(0, -20, 0), pivo=(nx, 14.8, nz)))
    corpo.append(peca("laco_a", [nx - 2.3, 14.3, nz - 0.4], [nx - 0.6, 15.7, nz + 0.4], mf, rot=(0, -20, 22), pivo=(nx - 0.6, 15.0, nz)))
    corpo.append(peca("laco_b", [nx + 0.6, 14.3, nz - 0.4], [nx + 2.1, 15.7, nz + 0.4], mf, rot=(0, -20, -22), pivo=(nx + 0.6, 15.0, nz)))
    for k, (dx, y0, inc) in enumerate(((-0.45, 7.6, -6), (0.5, 9.0, 7))):
        x = nx + dx
        corpo.append(osso(f"no_ponta{k}", [x, 13.8, nz], [4, -20, inc], [
            peca(f"no_ponta{k}_a", [x - 0.55, 10.8, nz - 0.35], [x + 0.55, 13.9, nz + 0.35], mf),
            peca(f"no_ponta{k}_b", [x - 0.65, y0, nz - 0.4], [x + 0.65, 11.0, nz + 0.4], mf)]))
    corpo.append(peca("hakama_meio_f", [-1.6, 7.0, -4.6], [1.6, 13.2, -3.8], mh, rot=(9, 0, 0), pivo=(0, 13.2, -4.2)))
    corpo.append(peca("hakama_meio_t", [-1.6, 7.2, 3.4], [1.6, 13.2, 4.2], mh, rot=(-9, 0, 0), pivo=(0, 13.2, 3.8)))
    KAT = (3.8 * LADO_KATANA, 15.0, -4.6)
    corpo.append(osso("katana", list(KAT), [30, 22 * (-LADO_KATANA), 0], montar_katana(KAT)))
    mp = mat_luz(cor_tronco)
    pescoco = osso("pescoco", [0, 22.5, -1.2], [0, 0, 0], [
        *g.arredondado2("pescoco", [-2.7, 21.0, -5.0], [2.7, 26.6, 1.4], mp, r=1.2),
        cabeca_grande()])
    corpo.append(pescoco)
    for lado in (-1, 1):
        corpo.append(montar_asa(lado))
    corpo.append(montar_cauda())
    tronco = osso("corpo", [0, 13.5, 0], [0, 0, 0], corpo)
    raizes = [tronco, perna(-1), perna(1)]
    preparar_transformacoes(raizes)
    return raizes

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
