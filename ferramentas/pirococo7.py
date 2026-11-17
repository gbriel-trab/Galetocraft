"""Pirococó v7 (galo completo) — técnica nova para o visual "Cobblemon":

1. UV POR FACE + 2 pixels de textura por pixel de modelo (D = 2): degradês lisos e detalhes finos.
2. PINTURA EM 3D: a cor de cada pixel da textura é calculada pela POSIÇÃO dele no corpo (luz de cima
   contínua entre peças, sombra suave embaixo, borda escura de acabamento), em vez de pintar caixa a caixa.
   Decalques (olho, sobrancelha, emblema) também são definidos em 3D.
3. FORMAS ORGÂNICAS: volumes arredondados (3 blocos em cruz), tronco em ovo (camadas), pescoço afinando,
   penas curvas (segmentos que afinam e giram), cubos girados (ponta do escudo, diamante da tiara).

Saída: modelos/pirococo/pirococo_v7.bbmodel (formato Bedrock, abre no Blockbench) + .png + prévias.
"""
import base64, io, json, math, sys, uuid
from pathlib import Path
from PIL import Image, ImageDraw

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import previa

D = 2                                   # pixels de textura por pixel de modelo
PASTA = AQUI.parent / "modelos" / "pirococo"
NOME = "pirococo_v7"

# ---------------- paleta ----------------
ROXO_ESC = (86, 36, 140); ROXO = (134, 64, 204); LILAS = (184, 140, 240)
BRANCO = (248, 244, 240)
AMARELO = (255, 198, 34); AMARELO_CLARO = (255, 226, 110); AMARELO_ESC = (240, 150, 20)
LARANJA = (246, 120, 20); LARANJA_ESC = (232, 92, 16)
VERM = (226, 40, 30); VERM_ESC = (184, 24, 26); VERM_VIVO = (246, 70, 40)
OURO = (246, 186, 50); OURO_CLARO = (255, 232, 130); OURO_ESC = (178, 112, 24)
PRETO = (26, 12, 22)

def clamp(v, a=0.0, b=1.0): return max(a, min(b, v))
def mix(a, b, f):
    f = clamp(f)
    return tuple(int(round(a[i] + (b[i] - a[i]) * f)) for i in range(3))
def sombra_de(c): return (int(c[0] * .60), int(c[1] * .38), int(c[2] * .58))
LUZ = (255, 246, 220)
def tom(c, f):
    f = clamp(f, -1, 1)
    return mix(c, LUZ, f * .40) if f >= 0 else mix(c, sombra_de(c), -f * .9)

# ---------------- estrutura ----------------
class Peca:
    """Cubo com UV por face. 'mat(c)' devolve a cor de um pixel a partir do contexto 3D 'c'."""
    def __init__(self, nome, de, ate, mat, rot=(0, 0, 0), pivo=None, faixa=None, brilho=False, res=None):
        self.nome, self.de, self.ate, self.mat = nome, list(de), list(ate), mat
        self.rot = list(rot); self.pivo = list(pivo) if pivo else [(de[i] + ate[i]) / 2 for i in range(3)]
        self.faixa = faixa or (de[1], ate[1])     # faixa de altura usada no degradê (pode ser do grupo)
        self.brilho = brilho; self.uuid = str(uuid.uuid4()); self.uv = {}
        self.res = res or D                       # pixels de textura por unidade (rosto e escudo usam mais)

def osso(nome, origem, rot, filhos):
    return {"name": nome, "origin": list(origem), "rotation": list(rot), "color": 0, "uuid": str(uuid.uuid4()),
            "export": True, "isOpen": True, "visibility": True, "children": [f for f in filhos if f is not None]}

PECAS = []
def peca(*a, **k):
    p = Peca(*a, **k); PECAS.append(p); return p.uuid

# dimensões de cada face em (largura, altura) no espaço do modelo
def dims(face, p):
    w, h, d = (p.ate[i] - p.de[i] for i in range(3))
    return {"north": (w, h), "south": (w, h), "east": (d, h), "west": (d, h), "up": (w, d), "down": (w, d)}[face]

NORMAL = {"north": (0, 0, -1), "south": (0, 0, 1), "east": (1, 0, 0), "west": (-1, 0, 0), "up": (0, 1, 0), "down": (0, -1, 0)}

def ponto(face, p, u, v):
    """Mesmo mapeamento face->UV do Blockbench (u: esquerda->direita, v: cima->baixo na textura)."""
    (x1, y1, z1), (x2, y2, z2) = p.de, p.ate
    dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
    return {"north": (x2 - u * dx, y2 - v * dy, z1), "south": (x1 + u * dx, y2 - v * dy, z2),
            "east": (x2, y2 - v * dy, z2 - u * dz), "west": (x1, y2 - v * dy, z1 + u * dz),
            "up": (x1 + u * dx, y2, z1 + v * dz), "down": (x1 + u * dx, y1, z2 - v * dz)}[face]

# ---------------- materiais (pintura em 3D) ----------------
def contexto_luz(c, borda=.12, topo=.18, baixo=.32, curva=.55):
    """Luz contínua: claro em cima, escuro embaixo (pela altura na faixa do grupo), topo das faces de cima
    mais claro, e um fio escuro na borda de cada face (acabamento 'bem feito')."""
    y0, y1 = c["faixa"]
    t = clamp((c["p"][1] - y0) / max(y1 - y0, 1e-6))
    luz = -curva / 2 + curva * t
    if c["face"] == "up": luz += topo
    if c["face"] == "down": luz -= baixo
    if c["i"] in (0, c["tw"] - 1) or c["j"] in (0, c["th"] - 1): luz -= borda
    return luz

def mat_cor(cor_fn, **kw):
    """cor_fn(p, face) -> cor base no ponto 3D; aplica a luz contínua por cima."""
    def f(c): return tom(cor_fn(c["p"], c["face"]), contexto_luz(c, **kw))
    return f

def mat_pena(c0, c1, eixo, inverte=False, borda=.2):
    """Pena: degradê c0 -> c1 ao longo do eixo do comprimento, luz em cima, contorno escuro."""
    def f(c):
        lo, hi = c["b"][0][eixo], c["b"][1][eixo]
        t = clamp((c["p"][eixo] - lo) / max(hi - lo, 1e-6))
        if inverte: t = 1 - t
        luz = .08
        if c["face"] == "up": luz += .2
        if c["face"] == "down": luz -= .35
        if c["i"] in (0, c["tw"] - 1) or c["j"] in (0, c["th"] - 1): luz -= borda
        return tom(mix(c0, c1, t), luz)
    return f

# ---------------- cabeça ----------------
# Cabeça de galo de briga com ELMO-MÁSCARA de armadura roxa (peças separadas) sobre o rosto branco.
OLHO_C = (2.35, 24.9, -3.9)          # centro do olho (lado +x), na 'janela' entre a viseira e a guarda da bochecha
MAGENTA = (196, 64, 168)

def linha_viseira(z):
    """Altura da borda de baixo do elmo na frente/lado: desce em direção ao bico (cara brava)."""
    return 26.05 + 0.16 * (z + 4.6)

def cor_cranio(p, face):
    x, y, z = p
    roxo = (mix(ROXO, LILAS, 0.5) if face == "up" else mix(ROXO, LILAS, 0.25) if face == "north" else ROXO)
    if face == "up" or y >= linha_viseira(z): return roxo                # casca do elmo (alto e testa)
    if -2.3 <= z <= -1.2 and y >= 23.3: return roxo                      # guarda atrás do olho
    if z > -1.2: return mix(VERM_ESC, VERM, clamp((y - 22.5) / 4))       # atrás da guarda: penas vermelhas
    return BRANCO                                                        # rosto branco e janela do olho

QUINA_X, QUINA_Z = 2.6, -4.4                 # quina vertical reta do rosto (onde fica o olho)
FAC_T = 1.6                                   # espessura da peça da face diagonal
FAC_C = (1.85 - 0.7071 * FAC_T / 2, -3.65 + 0.7071 * FAC_T / 2)   # centro (x, z) da peça (lado +x)
FAC_L = 2.4                                   # comprimento da face diagonal

def mat_faceta(lado):
    """Face diagonal do rosto: branca, com o olho na face de fora (local +x girado 45°)."""
    base = mat_cor(cor_cranio_faceta, borda=.03, curva=.35)
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u = z - FAC_C[1]                        # ao longo da face (negativo = para o bico)
            dy = y - 24.75
            e = (u / 1.05) ** 2 + (dy / 1.02) ** 2
            if e <= 1:
                iu, iy = u + 0.25, dy + 0.02                                          # íris puxada para a frente
                di = (iu / 0.68) ** 2 + (iy / 0.78) ** 2
                if ((u + 0.22) / 0.13) ** 2 + ((dy - 0.2) / 0.13) ** 2 <= 1: return (255, 255, 255)   # brilho
                if ((u + 0.36) / 0.34) ** 2 + ((dy + 0.02) / 0.38) ** 2 <= 1: return PRETO  # pupila redonda olhando para o bico
                if di <= 1: return mix((150, 10, 30), (236, 44, 44), clamp((0.5 - iy) / 1.1))
                if e > 0.86: return tom(BRANCO, -0.18)
                return mix(BRANCO, (215, 205, 220), clamp(dy / 1.02))
        return base(c)
    return f

def cor_cranio_faceta(p, face):
    x, y, z = p
    if face == "up" or y >= 26.1: return mix(ROXO, LILAS, 0.25)
    return BRANCO
def decal_olho(c):
    """Olho grande na quina reta do rosto: esclera branca, íris vermelha, pupila e brilho. A maior parte fica na
    face do lado (lê inteiro de perfil) e um pedaço dobra a quina (lê de frente, como na ficha)."""
    if c["face"] not in ("east", "west", "north"): return None
    x, y, z = c["p"]; s = 1 if x >= 0 else -1
    if abs(x) < 1.5: return None
    dx, dy, dz = abs(x) - QUINA_X, y - 24.7, z - (QUINA_Z + 0.55)
    if (dx / 1.0) ** 2 + (dy / 1.05) ** 2 + (dz / 1.55) ** 2 > 1: return None
    if ((dy - 0.36) / 0.2) ** 2 + ((dz - 0.12) / 0.2) ** 2 + (dx / 0.3) ** 2 <= 1: return (255, 255, 255)   # brilho
    ix, iy, iz = dx, dy + 0.02, z - (QUINA_Z + 0.45)
    di = (ix / 0.72) ** 2 + (iy / 0.8) ** 2 + (iz / 0.72) ** 2
    if di <= 0.24: return PRETO
    if di <= 1: return mix((150, 10, 30), (236, 44, 44), clamp((0.5 - iy) / 1.1))
    return mix(BRANCO, (215, 205, 220), clamp(dy / 1.05))

def mat_cranio():
    base = mat_cor(cor_cranio, borda=.03, curva=.35)
    def f(c):
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face == "down": return LARANJA
    if face in ("east", "west") and abs(z + 6.55) < 0.25 and abs(y - 25.05) < 0.2: return (140, 70, 20)  # narina
    if face in ("east", "west", "north") and 23.72 < y < 23.92 and z > -6.9: return (110, 40, 20)       # linha da boca
    if face == "north": return mix((255, 200, 46), (246, 138, 24), clamp((24.6 - y) / 1.6))       # de frente: cunha amarela, ponta laranja
    return mix((255, 192, 40), (246, 138, 24), clamp((-z - 6.2) / 1.8))

def mat_armadura(y0=None, L=None, ponta=False):
    """Armadura roxa facetada: em cima lilás (luz), frente um pouco mais clara, lados roxo, embaixo roxo escuro,
    quinas escurecidas; nas placas de ombro a raiz clareia e a ponta puxa para magenta."""
    def f(c):
        face = c["face"]
        if face == "up": base = LILAS
        elif face == "down": base = ROXO_ESC
        elif face == "north": base = mix(ROXO, LILAS, 0.28)
        else: base = ROXO
        if ponta and L:
            v = clamp((y0 - c["p"][1]) / L)
            base = mix(base, MAGENTA, clamp((v - 0.55) / 0.45) * 0.65)
            if v < 0.25 and face != "down": base = mix(base, LILAS, 0.5 * (1 - v / 0.25))
        if c["i"] in (0, c["tw"] - 1) or c["j"] in (0, c["th"] - 1): base = tom(base, -0.3)
        return base
    return f

def mat_hexagono(W, H, cy, cx):
    """Gema da testa: hexágono alongado (pontas em cima e embaixo), moldura de ouro e gema vermelha facetada."""
    def f(c):
        if c["face"] not in ("north", "south"): return None          # bordas da placa invisíveis (sem risco de perfil)
        x, y, z = c["p"]
        u = (x - cx) / (W / 2); v = (y - cy) / (H / 2)
        lim = 1.0 if abs(v) < 0.45 else max(0.0, 1.0 - (abs(v) - 0.45) / 0.55)
        if abs(u) > lim or abs(v) > 1: return None
        borda = min((lim - abs(u)) * W / 2, (1 - abs(v)) * H / 2)
        if borda < 0.09: return OURO_ESC
        if borda < 0.34: return mix(AMARELO_CLARO, OURO, clamp((0.3 - v) / 1.0))
        if u < 0 and v > 0: return (255, 120, 110)                       # faceta clara
        if u > 0 and v < 0: return VERM_ESC                              # faceta escura
        return VERM_VIVO
    return f

def cor_pescoco(p, face):
    x, y, z = p
    if z < -2.4 and abs(x) < 1.6: return BRANCO                  # garganta branca descendo até o peitoral
    return mix(VERM, LARANJA, clamp((y - 19) / 4.5))

def cor_barriga(p, face):
    """Penas fofas da barriga e das coxas: laranja em cima, dourado embaixo, com fileiras de pontas de pena."""
    x, y, z = p
    base = mix(AMARELO, LARANJA, clamp((y - 7.6) / 4.0))
    if y < 7.4 + 0.25 + 0.35 * abs(math.sin(x * 2.4 + z * 1.6)): return mix(base, LARANJA_ESC, 0.35)   # pontas de pena só embaixo
    return base

def cor_tronco(p, face):
    x, y, z = p
    return mix(VERM, LARANJA, clamp((-z + 1.0) / 5.5) * .8)

# ---------------- escudo (menor, no peito) ----------------
ESC_K = 1.00                  # escala do escudo em relação ao desenho base
ESC_X = 4.2 * ESC_K           # meia largura da placa
ESC_BASE = 15.7               # fim da placa (abaixo dela, a ponta em V)
ESC_TOPO = ESC_BASE + 3.4 * ESC_K
ESC_CY = ESC_BASE
ESC_H = 4.2 * ESC_K           # meia diagonal da ponta em V

def _emb_base(X, Y):
    """Desenho base da fênix (placa de 8,4 de largura, base em 16,4, topo do campo em 19,8)."""
    ax = abs(X)
    e = (ax / 0.75) ** 2 + ((Y - 17.0) / 1.0) ** 2              # corpo
    if e <= 1: return LARANJA if e < .35 else AMARELO
    if ax ** 2 + (Y - 18.85) ** 2 <= 0.55 ** 2: return AMARELO  # cabeça
    if ax < 0.22 and 17.9 < Y < 18.4: return AMARELO            # pescoço
    if 0.55 <= ax <= 2.85:                                      # asas abertas em W, pontas viradas para cima
        u = (ax - 0.55) / 2.3
        yc = 17.5 + 0.7 * u + 1.4 * u ** 3
        ht = 0.85 - 0.35 * u
        baixo = yc - ht - 0.5 * abs(math.sin(u * math.pi * 2.5))
        if baixo <= Y <= yc + ht: return AMARELO if Y > yc - 0.3 * ht else LARANJA
    return None

def emblema(x, y):
    """Fênix grande: asas em W de borda a borda da placa, corpo descendo para dentro do V."""
    return _emb_base(x / 1.17, 16.0 + (y - (ESC_BASE - 2.0)) / 1.32)

def campo(y): return mix(VERM_VIVO, VERM_ESC, clamp((ESC_TOPO - y) / 6.0))

def mat_escudo_placa():
    def f(c):
        x, y, z = c["p"]
        if c["face"] != "north": return tom(ROXO, contexto_luz(c))
        if y > ESC_TOPO: return mix(ROXO, LILAS, clamp((y - ESC_TOPO) / 0.5))
        if abs(x) > ESC_X - 0.85 * ESC_K: return tom(ROXO, .06 if x < 0 else -.06)
        return emblema(x, y) or campo(y)
    return f

def mat_escudo_ponta():
    meio = (ESC_H - 0.75 * ESC_K * 1.4142) / 1.4142
    def f(c):
        x, y, z = c["p"]
        if c["face"] != "north": return tom(ROXO, contexto_luz(c, borda=.15))
        if max(abs(x), abs(y - ESC_CY)) < meio:
            xw = 0.7071 * x - 0.7071 * (y - ESC_CY); yw = ESC_CY + 0.7071 * x + 0.7071 * (y - ESC_CY)
            return emblema(xw, yw) or campo(yw)
        return tom(ROXO, -.04)
    return f

def arredondado(nome, de, ate, mat, r=1.0, faixa=None, **kw):
    """Volume com as quinas chanfradas: 3 blocos em cruz (cada eixo encolhido em r de cada lado)."""
    (x0, y0, z0), (x1, y1, z1) = de, ate
    faixa = faixa or (y0, y1)
    return [peca(nome + "_a", [x0 + r, y0 + r, z0], [x1 - r, y1 - r, z1], mat, faixa=faixa, **kw),
            peca(nome + "_b", [x0, y0 + r, z0 + r], [x1, y1 - r, z1 - r], mat, faixa=faixa, **kw),
            peca(nome + "_c", [x0 + r, y0, z0 + r], [x1 - r, y1, z1 - r], mat, faixa=faixa, **kw)]

def pena_curva(nome, base, segs, rot0, curva, eixo_comp, mat_fn, lado=1, brilho_ponta=False):
    """Pena curva: segmentos encadeados (ossos) que afinam e giram 'curva' graus a cada um.
    segs = [(comprimento, largura, altura, cor0, cor1)], cresce no eixo 'eixo_comp' ('y', '-y', 'z' ou '-x').
    Em '-y' (penas da asa, para baixo): largura = espessura em x, altura = largura da pena em z."""
    x, y, z = base
    def seg(k, pos):
        L, w, h, c0, c1 = segs[k]
        px, py, pz = pos
        if eixo_comp == "y":
            de, ate, prox, ei = [px - w / 2, py, pz - h / 2], [px + w / 2, py + L, pz + h / 2], (px, py + L - .2, pz), 1
        elif eixo_comp == "-y":
            de, ate, prox, ei = [px - w / 2, py - L, pz - h / 2], [px + w / 2, py, pz + h / 2], (px, py - L + .2, pz), 1
        elif eixo_comp == "z":
            de, ate, prox, ei = [px - w / 2, py - h / 2, pz], [px + w / 2, py + h / 2, pz + L], (px, py, pz + L - .2), 2
        else:  # para fora em x (lado -1 = direita, cresce para -x)
            if lado < 0: de, ate, prox = [px - L, py - h / 2, pz - w / 2], [px, py + h / 2, pz + w / 2], (px - L + .2, py, pz)
            else: de, ate, prox = [px, py - h / 2, pz - w / 2], [px + L, py + h / 2, pz + w / 2], (px + L - .2, py, pz)
            ei = 0
        inv = (lado < 0 and eixo_comp == "-x") or eixo_comp == "-y"
        filhos = [peca(f"{nome}_{k}", de, ate, mat_fn(c0, c1, ei, inv), brilho=brilho_ponta and k == len(segs) - 1)]
        if k + 1 < len(segs): filhos.append(seg(k + 1, prox))
        r = rot0 if k == 0 else curva
        return osso(f"{nome}_{k}", list(pos), r, filhos)
    return seg(0, (x, y, z))

def arredondado2(nome, de, ate, mat, r=1.0, faixa=None, **kw):
    """Volume bem arredondado (borda em 2 degraus): os 3 blocos em cruz + um bloco do meio que preenche
    metade das quinas. Continua 'quadradinho' de Minecraft, mas deixa de ler como cubo."""
    (x0, y0, z0), (x1, y1, z1) = de, ate
    h = r / 2
    faixa = faixa or (y0, y1)
    return arredondado(nome, de, ate, mat, r=r, faixa=faixa, **kw) + [
        peca(nome + "_d", [x0 + h, y0 + h, z0 + h], [x1 - h, y1 - h, z1 - h], mat, faixa=faixa, **kw)]

def octogono(nome, de, ate, mat, r=0.6, faixa=None):
    """Prisma de 8 lados (quinas verticais chanfradas): 2 blocos em cruz. Bom para bota em carretel."""
    (x0, y0, z0), (x1, y1, z1) = de, ate
    return [peca(nome + "_a", [x0 + r, y0, z0], [x1 - r, y1, z1], mat, faixa=faixa),
            peca(nome + "_b", [x0, y0, z0 + r], [x1, y1, z1 - r], mat, faixa=faixa)]

def mat_asa(c0, c1, ei, inv, borda=.2):
    """Pena da asa: degradê ao longo do comprimento, raque (veio) clara no meio da face larga
    e a beirada de trás um pouco mais escura, para as penas sobrepostas se separarem."""
    base = mat_pena(c0, c1, ei, inv, borda)
    def f(c):
        cor = base(c)
        if c["face"] in ("east", "west"):
            (_, _, z0), (_, _, z1) = c["b"]
            d = (c["p"][2] - (z0 + z1) / 2) / max((z1 - z0) / 2, 1e-6)    # -1 (frente) .. 1 (trás)
            if abs(d) < .16: cor = tom(cor, .16)
            elif d > .55: cor = tom(cor, -.22 * (d - .55) / .45)
        return cor
    return f

def cor_coxa(xc, y0=7.2):
    """'Calça' de penas amarelo-laranja; a barra de baixo tem pontas de pena recortadas."""
    def f(p, face):
        x, y, z = p
        a = math.atan2(z, x - xc)
        barra = y0 + 0.6 + 0.7 * abs(math.sin(a * 3.0))
        if y < barra: return mix(LARANJA_ESC, LARANJA, clamp((y - y0) / 1.3))
        return mix(LARANJA, AMARELO, clamp((y - barra) / 2.6))
    return f

def cor_dedo(junta_z):
    def f(p, face):
        if abs(p[2] - junta_z) < .22 and face != "down": return AMARELO_ESC   # dobra do dedo
        return AMARELO
    return f

def anel(ax, az, zc, phi, lado):
    """Ponto numa elipse em volta do corpo: phi = 0 lado de fora, negativo = frente, positivo = trás."""
    r = math.radians(phi)
    return lado * ax * math.cos(r), zc + az * math.sin(r)

def pena_ponta(nome, raiz, rot, L, W, cores, mat_fn, esp=1.0):
    """Pena RETA que afina até a ponta em 3 degraus, para baixo a partir da raiz (largura em z).
    cores = 3 cores (raiz, meio, ponta)."""
    x, y, z = raiz
    partes = [(0.55, 1.0, 1.0, cores[0], cores[1]), (0.28, 0.62, 0.85, cores[1], cores[2]), (0.17, 0.28, 0.7, cores[2], cores[2])]
    pecas, y0 = [], y
    for k, (fl, fw, fe, c0, c1) in enumerate(partes):
        h, w, e = L * fl, W * fw, esp * fe
        pecas.append(peca(f"{nome}_{k}", [x - e / 2, y0 - h, z - w / 2], [x + e / 2, y0, z + w / 2], mat_fn(c0, c1, 1, True)))
        y0 -= h - 0.05
    return osso(nome, list(raiz), list(rot), pecas)

def mat_manto(c0, c1, ei, inv):
    """Placa do manto: violeta saturado com só um fio lilás de brilho no alto e na face de cima."""
    base = mat_asa(c0, c1, ei, inv)
    def f(c):
        y0, y1 = c["b"][0][1], c["b"][1][1]
        if c["face"] == "up" or (c["face"] not in ("down",) and c["p"][1] > y1 - 0.35 and y1 - y0 > 2.0): return LILAS
        if c["face"] == "down": return ROXO
        return base(c)
    return f

def pena_cone(nome, raiz, phi, flare, L, W, cores, mat_fn, lado, varre=0):
    """Pena reta numa 'saia' em volta do corpo: o osso de fora gira em y (face larga para fora no ângulo phi);
    a pena varre para trás e abre 'flare' graus para fora."""
    return osso(nome, list(raiz), [0, -phi * lado, 0],
                [pena_ponta(nome + "_p", raiz, (-varre, 0, flare * lado), L, W, cores, mat_fn)])

# ---------------- placas recortadas: a forma (pena, chama, losango) é pintada e o resto fica transparente ----------------
def forma_pena(u, v, curva=0.0):
    """u: -1..1 na largura, v: 0 (raiz) .. 1 (ponta). Larga, afina numa ponta; 'curva' entorta a ponta."""
    uc = u - curva * v * v
    meia = 0.8 + 0.2 * min(1.0, v / 0.4) if v < 0.55 else max(0.0, 1.0 - ((v - 0.55) / 0.45) ** 1.5)
    return abs(uc) <= meia, meia - abs(uc), uc

def mat_placa_pena(cores, y0, L, centro, W, curva=0.0, fio=None, eixo="z"):
    """Pena pendurada para baixo: recorte em forma de pena, 3 faixas de cor nítidas (raiz, meio, ponta),
    raque discreta, contorno escuro e 'fio' de brilho na borda de cima, se pedido."""
    c0, c1, c2 = cores
    def f(c):
        x, y, z = c["p"]
        v = (y0 - y) / L
        u = ((z if eixo == "z" else x) - centro) / (W / 2)
        if not (-0.01 <= v <= 1.0): return None
        ok, borda, uc = forma_pena(u, max(v, 0.0), curva)
        if not ok: return None
        if v < 0.42: cor = tom(c0, 0.1 - 0.25 * v)
        elif v < 0.74: cor = tom(c1, 0.08 - 0.2 * (v - 0.42))
        else: cor = tom(c2, 0.1 - 0.15 * (v - 0.74))
        if fio and borda < 0.14 and v < 0.6: return fio
        if abs(uc) < 0.06 and v < 0.8: cor = tom(cor, .12)
        if borda < 0.1: return tom(cor, -.4)
        return cor
    return f

def pena_placa(nome, raiz, rot, L, W, cores, esp=0.3, curva=0.0, fio=None, res=4, eixo="z"):
    x, y, z = raiz
    if eixo == "z":
        de, ate, centro = [x - esp / 2, y - L, z - W / 2], [x + esp / 2, y, z + W / 2], z
    else:
        de, ate, centro = [x - W / 2, y - L, z - esp / 2], [x + W / 2, y, z + esp / 2], x
    return osso(nome, list(raiz), list(rot), [peca(nome, de, ate, mat_placa_pena(cores, y, L, centro, W, curva, fio, eixo), res=res)])

def pena_cruzada(nome, raiz, rot, L, W, cores, curva=0.0):
    """Pena em X girado 45°: nenhuma das duas placas fica de perfil nas vistas de frente, lado e costas."""
    return osso(nome, list(raiz), list(rot), [osso(nome + "_x", list(raiz), [0, 45, 0], [
        pena_placa(nome + "_a", raiz, (0, 0, 0), L, W, cores, curva=curva, eixo="z"),
        pena_placa(nome + "_b", raiz, (0, 0, 0), L, W, cores, curva=0.0, eixo="x")])])

def pena_cone_placa(nome, raiz, phi, flare, L, W, cores, lado, varre=0, curva=0.25, fio=None):
    """Placa-pena numa 'saia' em volta do corpo: o osso de fora gira em y (face larga para fora no ângulo phi);
    a pena varre para trás e abre 'flare' graus para fora."""
    return osso(nome, list(raiz), [0, -phi * lado, 0],
                [pena_placa(nome + "_p", raiz, (-varre, 0, flare * lado), L, W, cores, curva=curva, fio=fio)])

def mat_chama(L, y0, W, eixo, centro, curl):
    """Chama recortada: vermelho na base, laranja, amarelo na ponta, miolo claro e contorno escuro."""
    def f(c):
        x, y, z = c["p"]
        v = (y - y0) / L
        u = ((z if eixo == "z" else x) - centro) / (W / 2)
        if not (0.0 <= v <= 1.0): return None
        uc = u - curl * v * v
        meia = (1.0 - v ** 2.0) * (1.0 if v > 0.12 else 0.72 + 2.3 * v)
        if abs(uc) > meia: return None
        borda = meia - abs(uc)
        cor = mix(VERM, LARANJA, v / 0.6) if v < 0.6 else mix(LARANJA, AMARELO, min(1.0, (v - 0.6) / 0.3))
        if borda < 0.08: cor = tom(cor, -.35)
        return cor
    return f

def chama_cruzada(nome, base, rot, L, W, curl=0.4, esp=0.25, brilho=True):
    """Chama em X girado 45° (como o fogo do Minecraft): nenhuma placa fica de perfil nas vistas principais."""
    x, y, z = base
    return osso(nome, list(base), list(rot), [osso(nome + "_x", list(base), [0, 45, 0], [
        peca(nome + "_a", [x - esp / 2, y, z - W / 2], [x + esp / 2, y + L, z + W / 2], mat_chama(L, y, W, "z", z, curl), res=4, brilho=brilho),
        peca(nome + "_b", [x - W / 2, y, z - esp / 2], [x + W / 2, y + L, z + esp / 2], mat_chama(L, y, W, "x", x, 0.0), res=4, brilho=brilho)])])

def mat_losango(W, H, cy, eixo, centro):
    """Losango alto: moldura de ouro e gema vermelha com reflexo."""
    def f(c):
        x, y, z = c["p"]
        u = ((z if eixo == "z" else x) - centro) / (W / 2); v = (y - cy) / (H / 2)
        d = abs(u) + abs(v)
        if d > 1.0: return None
        if d > 0.93: return OURO_ESC
        if d > 0.6: return mix(OURO_CLARO, OURO, clamp((0.3 - v) / 1.2))
        if (u + 0.18) ** 2 + (v - 0.22) ** 2 < 0.025: return (255, 190, 180)
        return mix(VERM_VIVO, VERM_ESC, clamp((0.5 - v) / 1.1))
    return f

def so_gema(c, cor): return cor[0] > 150 and cor[1] < 100 and cor[2] < 100

def losango(nome, centro, W, H, eixo="x", esp=0.4, res=6):
    x, y, z = centro
    if eixo == "x":   # placa de frente (fina em z)
        return peca(nome, [x - W / 2, y - H / 2, z - esp / 2], [x + W / 2, y + H / 2, z + esp / 2], mat_losango(W, H, y, "x", x), res=res, brilho=so_gema)
    return peca(nome, [x - esp / 2, y - H / 2, z - W / 2], [x + esp / 2, y + H / 2, z + W / 2], mat_losango(W, H, y, "z", z), res=res, brilho=so_gema)

def mat_ouro_facetado(c):
    """Ouro de armadura: em cima claro, frente amarelo, lados ouro, embaixo escuro, quinas escurecidas."""
    face = c["face"]
    base = AMARELO_CLARO if face == "up" else AMARELO if face == "north" else OURO_ESC if face == "down" else mix(AMARELO, OURO, .5)
    if c["i"] in (0, c["tw"] - 1) or c["j"] in (0, c["th"] - 1): base = tom(base, -0.3)
    return base

def mat_ouro_seg(c0, c1, ei, inv):
    return mat_ouro_facetado

def mat_escudo_baixo(ponta, topo, k):
    """Camada de baixo do peitoral: V estreito e fechado (meia largura = k*(y-ponta)), moldura roxa clara
    e a cauda de chama da fênix (amarelo no meio, laranja, vermelho junto da moldura). Fora do V: transparente."""
    n = math.sqrt(1 + k * k)
    def f(c):
        x, y, z = c["p"]
        if y < ponta or y > topo: return None
        w = k * (y - ponta); ax = abs(x)
        if ax > w + 1e-6: return None
        d = (w - ax) / n                                    # distância até a borda do V
        if c["face"] != "north":
            return tom(mix(ROXO, LILAS, .3), -0.1 if c["face"] in ("east", "west", "down") else 0.05)
        if d < 0.12: return ROXO_ESC
        if d < 0.7: return tom(mix(ROXO, LILAS, 0.35), 0.08 if x < 0 else -0.04)
        wi = max(w - 0.7 * n, 0.01)
        sx = ax / wi + 0.10 * math.sin(y * 3.1 + ax * 1.7)  # bordas onduladas da chama
        if sx < 0.42: return AMARELO_CLARO if y > ponta + 3.2 and sx < 0.2 else AMARELO
        if sx < 0.78: return LARANJA
        return VERM_VIVO
    return f

def placa_armadura(nome, raiz, rot, L, W, esp=0.7):
    """Placa de armadura grossa e pontuda (para baixo a partir da raiz): corpo + ponta em losango."""
    x, y, z = raiz
    m = mat_armadura(y, L * 0.72 + W / 2, ponta=True)
    cy = y - L * 0.72; sq = W / 1.4142
    return osso(nome, list(raiz), list(rot), [
        peca(nome, [x - esp / 2, cy, z - W / 2], [x + esp / 2, y, z + W / 2], m, res=4),
        peca(nome + "_ponta", [x - esp / 2 + 0.02, cy - sq / 2, z - sq / 2], [x + esp / 2 - 0.02, cy + sq / 2, z + sq / 2], m,
             rot=(45, 0, 0), pivo=(x, cy, z), res=4)])

def placa_cone(nome, raiz, phi, flare, L, W, lado, varre=0, esp=0.7):
    return osso(nome, list(raiz), [0, -phi * lado, 0], [placa_armadura(nome + "_p", raiz, (-varre, 0, flare * lado), L, W, esp)])

INCLINA = 24          # o corpo do galo é inclinado: peito alto na frente, traseira descendo

def montar():
    def fogo(c0, c1, ei, inv): return mat_pena(c0, c1, ei, inv, borda=.12)
    # ---------- cabeça de galo de briga ----------
    i_cab = len(PECAS)
    cab = []
    mc = mat_cranio()
    cab.append(peca("cranio_a", [-2.6, 23.5, -2.9], [2.6, 26.5, 2.4], mc, faixa=(22.8, 27.2), res=4))   # lados (atrás das faces diagonais)
    cab.append(peca("cranio_b", [-1.9, 22.8, -3.5], [1.9, 27.2, 1.7], mc, faixa=(22.8, 27.2), res=4))   # miolo alto
    cab.append(peca("cranio_c", [-2.3, 23.1, -2.9], [2.3, 26.9, 2.1], mc, faixa=(22.8, 27.2), res=4))
    cab.append(peca("cranio_frente", [-1.15, 23.1, -4.4], [1.15, 26.9, -3.0], mc, faixa=(22.8, 27.2), res=4))  # frente estreita
    for lado in (-1, 1):
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("cranio_faceta_" + ("d" if lado < 0 else "e"), [cx - FAC_T / 2, 23.4, cz - FAC_L / 2],
                        [cx + FAC_T / 2, 26.4, cz + FAC_L / 2], mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, 24.9, cz),
                        faixa=(22.8, 27.2), res=8))
    # elmo-máscara de armadura roxa: placa no alto, viseiras sobre os olhos, guardas atrás dos olhos, aletas para trás
    arm = mat_armadura()
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        x0, x1 = sorted((1.6 * lado, 2.6 * lado))
        x0, x1 = sorted((2.15 * lado, 2.5 * lado))
        x0, x1 = sorted((2.5 * lado, 2.95 * lado))
        cab.append(peca("viseira_" + s_, [x0, 25.75, -3.2], [x1, 26.55, -1.2], arm))
        # viseira da quina: na face diagonal, por cima do olho, descendo para o bico (corta o alto do olho: cara brava)
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        fx0, fx1 = sorted((cx + FAC_T / 2 * lado - 0.1 * lado, cx + FAC_T / 2 * lado + 0.38 * lado))
        cab.append(osso("viseira_quina_" + s_, [cx, 25.9, cz], [0, 45 * lado, 0], [
            peca("viseira_quina_" + s_, [fx0, 25.2, cz - 1.45], [fx1, 26.05, cz + 1.3], arm, rot=(-17, 0, 0), pivo=(cx, 25.6, cz))]))
        # sobrancelha da frente: da quina desce para o bico (V bravo visto de frente)
        x0, x1 = sorted((0.25 * lado, 1.45 * lado))
        cab.append(peca("sobrancelha_" + s_, [x0, 25.45, -4.8], [x1, 26.2, -4.3], arm,
                        rot=(0, 0, 20 * lado), pivo=(1.45 * lado, 25.85, -4.55)))
        # aleta pequena varrendo para trás no alto
        x0, x1 = sorted((0.7 * lado, 1.25 * lado))
        cab.append(peca("aleta_" + s_, [x0, 26.9, -0.6], [x1, 27.7, 2.6], arm, rot=(-28, 0, 0), pivo=(0.95 * lado, 26.9, -0.6)))
        x0, x1 = sorted((2.5 * lado, 2.9 * lado))
        cab.append(peca("guarda_" + s_, [x0, 23.3, -2.3], [x1, 26.0, -1.2], arm))
    cab.append(peca("mascara_v", [-0.6, 25.0, -4.8], [0.6, 26.2, -4.3], arm, rot=(0, 0, 45), pivo=(0, 25.6, -4.55)))
    # gema da testa: hexágono alongado vermelho facetado em moldura de ouro, passando um pouco do alto do elmo
    cab.append(peca("tiara_gema", [-1.15, 25.4, -4.95], [1.15, 28.9, -4.87], mat_hexagono(2.3, 3.5, 27.15, 0.0), res=6, brilho=so_gema))
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        # braço diagonal: sai do lado da moldura da gema e sobe para fora
        cx, cy = 2.0 * lado, 27.35
        cab.append(peca("chifre_braco_" + s_, [cx - 1.45, cy - 0.85, -5.15], [cx + 1.45, cy + 0.85, -3.95], mat_ouro_facetado,
                        rot=(0, 0, 36 * lado), pivo=(cx, cy, -4.55)))
        # ponta vertical alta, um pouco para fora e curvando para trás no alto
        cab.append(pena_curva("chifre_" + s_, (3.05 * lado, 27.8, -4.55),
                              [(1.7, 1.75, 1.5, AMARELO, AMARELO), (1.4, 1.55, 1.3, AMARELO, AMARELO), (1.0, 1.3, 1.1, AMARELO, AMARELO)],
                              (2, 0, -3 * lado), (6, 0, 0), "y", mat_ouro_seg))
    # chifre pequeno no centro, acima do cristal
    cab.append(pena_curva("chifre_meio", (0, 28.75, -4.6), [(0.9, 0.8, 0.7, AMARELO, AMARELO), (0.7, 0.5, 0.45, AMARELO, AMARELO)],
                          (0, 0, 0), (0, 0, 0), "y", mat_ouro_seg))
    # bico robusto e comprido, com degrau de gancho na ponta e narina; bico de baixo mais claro
    mb = mat_cor(cor_bico, borda=.05, curva=.35)
    cab.append(peca("bico_base", [-1.1, 23.75, -6.05], [1.1, 25.65, -4.3], mb, faixa=(22.5, 25.8)))
    cab.append(peca("bico_meio", [-0.9, 23.7, -7.25], [0.9, 25.35, -6.0], mb, rot=(-9, 0, 0), pivo=(0, 25.35, -6.0), faixa=(22.5, 25.8)))
    cab.append(peca("bico_gancho", [-0.64, 22.85, -8.0], [0.64, 24.7, -7.15], mat_cor(cor_bico, borda=.05, curva=.6),
                    rot=(-24, 0, 0), pivo=(0, 24.7, -7.15), faixa=(22.5, 25.8)))
    cab.append(peca("bico_baixo", [-0.8, 23.05, -6.7], [0.8, 23.72, -4.3], mat_cor(lambda p, f: LARANJA_ESC, borda=.1)))
    # babado de penas vermelhas espetadas saindo de trás da bochecha, emoldurando o rosto
    for k, (phi, y0, L, W, fl) in enumerate([(30, 24.6, 4.0, 2.8, 40), (62, 25.0, 4.2, 2.8, 32),
                                              (8, 23.3, 4.2, 3.0, 34), (42, 23.4, 4.6, 3.0, 26)]):
        for lado in (-1, 1):
            x, z = anel(2.4, 2.5, -0.6, phi, lado)
            cab.append(pena_cone_placa(f"rufo{k}_{'d' if lado < 0 else 'e'}", (x, y0, z), phi, fl, L, W,
                                       (VERM_VIVO, VERM, LARANJA), lado, varre=0, curva=0.1))
    # crista: 5 chamas em leque (V) saindo do alto da cabeça, inclinadas para trás; a do meio ~1 cabeça de altura
    cab.append(chama_cruzada("crista_meio", (0, 27.0, -1.6), (46, 0, 0), 6.4, 5.0, curl=0.5))
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        cab.append(chama_cruzada("crista_" + s_, (1.2 * lado, 26.9, -0.8), (50, 0, -16 * lado), 5.6, 4.4, curl=0.45))
        cab.append(chama_cruzada("crista_fora_" + s_, (1.8 * lado, 26.7, 0.6), (56, 0, -28 * lado), 4.6, 3.8, curl=0.4))
    # juba: plumas vermelhas (em X) que descem da nuca por cima do pescoço até o manto
    juba = []
    for k, phi in enumerate((50, 76)):
        for lado in (-1, 1):
            x, z = anel(2.1, 2.3, 0.6, phi, lado)
            juba.append(pena_cone_placa(f"juba{k}_{'d' if lado < 0 else 'e'}", (x, 26.6 - 0.4 * k, z), phi, 16, 7.0 - 0.4 * k, 3.6,
                                        (VERM_VIVO, VERM, LARANJA), lado, varre=0, curva=0.1))
    x, z = anel(2.1, 2.3, 0.6, 90, 1)
    juba.append(pena_cone_placa("juba_nuca", (0, 26.8, z), 90, 14, 7.6, 4.0, (VERM_VIVO, VERM, LARANJA), 1, varre=0, curva=0.0))
    cab.append(osso("juba", [0, 26.0, 1.5], [0, 0, 0], juba))
    K_CAB, C_CAB, SOBE = 1.0, (0.0, 22.6, -1.0), 0.0
    for pc in PECAS[i_cab:]:
        for arr in (pc.de, pc.ate, pc.pivo):
            for i in range(3): arr[i] = C_CAB[i] + (arr[i] - C_CAB[i]) * K_CAB
            arr[1] += SOBE
        pc.pintas = getattr(pc, "pintas", []) + [(C_CAB, K_CAB, SOBE)]
    def escala(no):
        if isinstance(no, dict):
            o = no["origin"]
            for i in range(3): o[i] = C_CAB[i] + (o[i] - C_CAB[i]) * K_CAB
            o[1] += SOBE
            for f in no["children"]: escala(f)
    for no in cab: escala(no)
    cabeca = osso("cabeca", [0, 22.6 + SOBE, -1.0], [12, 0, 0], cab)

    # ---------- pescoço de galo: fino e um pouco para a frente (desfaz a inclinação do corpo) ----------
    mp = mat_cor(cor_pescoco, borda=.06, curva=.3)
    pescoco = osso("pescoco", [0, 19.5, -1.0], [-INCLINA - 16, 0, 0], [
        peca("pescoco_baixo", [-2.3, 18.4, -3.4], [2.3, 21.6, 1.6], mp, faixa=(18.4, 26.0)),
        peca("pescoco_alto", [-1.9, 21.4, -3.5], [1.9, 23.6, 1.2], mp, faixa=(18.4, 26.0)),
        cabeca])

    # ---------- corpo em ovo, mais estreito, com peito arredondado e o escudo menor ----------
    mt = mat_cor(cor_tronco, borda=.03, curva=.55)
    corpo = []
    corpo += arredondado("tronco", [-3.7, 13.6, -4.0], [3.7, 19.6, 5.0], mt, r=1.3, faixa=(10.4, 19.6))
    corpo += arredondado("barriga", [-2.9, 10.6, -3.3], [2.9, 14.2, 4.1], mat_cor(cor_barriga, borda=.03, curva=.3), r=1.0, faixa=(7.4, 14.2))
    corpo += arredondado("peito", [-3.0, 12.4, -5.0], [3.0, 18.4, -3.2], mt, r=0.5, faixa=(10.4, 19.6))
    # barriga de penas: desce até perto das botas e cobre as coxas (com o corpo inclinado fica mais baixa atrás)
    me = mat_escudo_placa()
    corpo.append(peca("escudo", [-ESC_X, ESC_BASE, -5.25], [ESC_X, ESC_TOPO, -4.4], me, res=6))
    corpo.append(peca("escudo_topo", [-ESC_X + 0.5, ESC_BASE, -5.2], [ESC_X - 0.5, ESC_TOPO + 0.45, -4.4], me, res=6))
    hs = ESC_H / 1.4142
    corpo.append(peca("escudo_ponta", [-hs, ESC_CY - hs, -5.2], [hs, ESC_CY + hs, -4.5], mat_escudo_ponta(),
                      rot=(0, 0, 45), pivo=(0, ESC_CY, -4.85), res=6))
    PB, TB, KB = ESC_BASE - ESC_H - 3.6, ESC_BASE - 0.75, 0.5     # ponta, topo e abertura do V de baixo
    wb = KB * (TB - PB)
    corpo.append(peca("escudo_baixo", [-wb, PB, -5.12], [wb, TB, -4.5], mat_escudo_baixo(PB, TB, KB), res=6))
    corpo.append(peca("escudo_gola", [-1.15, ESC_TOPO - 0.75, -5.65], [1.15, ESC_TOPO + 1.55, -5.1],
                      mat_cor(lambda p, f: mix(ROXO, LILAS, clamp((p[1] - ESC_TOPO + 0.75) / 2.3)), borda=.15),
                      rot=(0, 0, 45), pivo=(0, ESC_TOPO + 0.4, -5.375)))

    AX, AZ, ZC = 3.7, 4.5, 0.5
    # manto roxo: 2 camadas de 3 penas retas e pontudas por ombro (lilás por cima, roxo embaixo)
    OMBREIRA = [   # (y, raio x, raio z, abertura, comprimento, largura, phis)
        (19.9, 3.6, 3.4, 46, 6.4, 4.6, [-40, -6, 28, 62]),     # camada de baixo (mais longa)
        (20.8, 3.3, 3.1, 58, 5.0, 4.4, [-28, 8, 44]),           # camada de cima (mais aberta, curta)
    ]
    # asas dobradas: 3 fileiras de penas retas, mesma varrida dentro da fileira (vermelho, laranja, dourado)
    T = math.tan(math.radians(18))
    # leque: (varrida p/ trás, comprimento, largura, z da raiz, y da raiz, abertura p/ fora, cores)
    LEQUE = [(8, 11.4, 4.6, -1.8, 18.4, 16, (VERM, LARANJA, AMARELO)), (17, 13.2, 4.8, -0.7, 18.7, 19, (VERM_ESC, VERM, LARANJA)),
             (27, 14.8, 5.0, 0.4, 18.9, 22, (VERM, LARANJA, AMARELO)), (37, 15.2, 5.0, 1.5, 19.0, 24, (VERM_VIVO, LARANJA, AMARELO)),
             (47, 14.0, 4.8, 2.5, 18.8, 24, (VERM, LARANJA_ESC, AMARELO)), (57, 12.0, 4.4, 3.4, 18.5, 22, (VERM_ESC, LARANJA, AMARELO))]
    # penas de peito/barriga sob o V do peitoral, cobrindo a barriga e as coxas (só a canela curta aparece)
    FRENTE = [(13.7, -46, 3.6, 3.4, (VERM, VERM_VIVO, LARANJA)),
              (12.2, -50, 6.0, 4.2, (VERM, LARANJA, AMARELO)),
              (10.2, -42, 5.0, 4.0, (LARANJA, LARANJA, AMARELO)),
              (12.6, -34, 6.6, 4.4, (VERM, LARANJA, AMARELO)), (10.6, -24, 5.6, 4.2, (LARANJA, LARANJA, AMARELO))]
    LEQUE_DENTRO = [(12, 11.0, 3.0, -1.4, 18.0, 14, (LARANJA, LARANJA, AMARELO)), (28, 13.0, 3.0, 0.2, 18.2, 18, (LARANJA_ESC, LARANJA, AMARELO)),
                    (44, 12.6, 3.0, 1.8, 18.2, 19, (LARANJA, AMARELO, AMARELO)), (60, 10.0, 2.8, 3.2, 18.0, 17, (LARANJA_ESC, LARANJA, AMARELO))]
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        manto = []
        for f, (y0, rx, rz, fl, L, W, phis) in enumerate(OMBREIRA):
            for k, phi in enumerate(phis):
                x, z = anel(rx, rz, ZC, phi, lado)
                manto.append(placa_cone(f"manto{f}{k}_{s}", (x, y0, z), phi, fl, L * (0.92, 1.04, 1.0, 0.9)[k], W, lado))
        corpo.append(osso("ombro_" + s, [3.4 * lado, 20.4, 0.5], [0, 0, 0], manto))
        asa = []
        for k, (varre, L, W, z0, y0, fl, cores) in enumerate(LEQUE):
            x0 = (4.4 + 0.2 * (k % 2)) * lado
            asa.append(pena_cone_placa(f"asa{k}_{s}", (x0, y0, z0), 0, fl, L, W, cores, lado, varre=varre, curva=0.25))
        for k, (y0, phi, L, W, cores) in enumerate(FRENTE):
            x, z = anel(AX + 0.3, AZ + 0.3, ZC, phi, lado)
            asa.append(pena_cone_placa(f"frente{k}_{s}", (x, y0, z), phi, 12, L, W, cores, lado, varre=6, curva=0.2))
        corpo.append(osso("asa_" + s, [4.0 * lado, 18.8, 0.5], [0, 0, 0], asa))

    # ---------- cauda curta: 3 chamas viradas para cima ----------
    cauda = [chama_cruzada("cauda_meio", (0, 15.6, 5.4), (26, 0, 0), 7.6, 5.6, curl=0.4),
             chama_cruzada("cauda_cima", (0, 16.4, 5.0), (14, 0, 0), 5.4, 4.4, curl=0.35),
             chama_cruzada("cauda_d", (-1.6, 15.2, 5.2), (24, 0, 20), 6.2, 4.8, curl=0.35),
             chama_cruzada("cauda_e", (1.6, 15.2, 5.2), (24, 0, -20), 5.6, 4.4, curl=0.35)]
    corpo.append(osso("cauda", [0, 16, 4.6], [0, 0, 0], cauda))

    # ---------- 3 correntes de contas com pingente de diamante (pingente desfaz também a inclinação do corpo) ----------
    conta = mat_cor(lambda p, f: AMARELO, borda=.15, curva=.3)
    ouro_p = mat_cor(lambda p, f: mix(AMARELO, OURO, .5), borda=.25, curva=.6)
    def gema_p(c):
        return mix((255, 150, 140), VERM_VIVO, clamp(c["j"] / 2)) if c["face"] in ("north", "south") and c["j"] < 2 \
            else mix(VERM_VIVO, VERM_ESC, c["j"] / max(c["th"] - 1, 1))
    ouro_p = mat_cor(lambda p, f: AMARELO if f in ("north", "south") else OURO, borda=.22, curva=.5)
    def gema_p(c):
        x, y, z = c["p"]
        if c["face"] not in ("north", "south"): return OURO
        return (255, 130, 120) if c["i"] < c["tw"] // 2 and c["j"] < c["th"] // 2 else VERM_VIVO
    ouro_px = mat_cor(lambda p, f: AMARELO if f in ("east", "west") else OURO, borda=.22, curva=.5)
    def gema_px(c):
        if c["face"] not in ("east", "west"): return OURO
        return (255, 130, 120) if c["i"] < c["tw"] // 2 and c["j"] < c["th"] // 2 else VERM_VIVO
    def corrente(i, base, n, rot0, curva, gira, t=1.5, passo=1.75):
        def elo(k, pos):
            px, py, pz = pos
            tk = t if k % 2 == 0 else t * 0.8                       # contas grande/pequena, com folga entre elas
            o = (t - tk) / 2
            filhos = [peca(f"conta_{i}_{k}", [px - tk / 2, py - o - tk, pz - tk / 2], [px + tk / 2, py - o, pz + tk / 2], conta,
                           rot=(0, 45, 0), pivo=(px, py - t / 2, pz), faixa=(py - t, py))]
            prox = (px, py - passo, pz)
            if k + 1 < n:
                filhos.append(elo(k + 1, prox))
            else:
                qx, qy, qz = prox; cy = qy - 2.3
                filhos.append(osso(f"pingente_{i}", list(prox), [-(rot0[0] + curva * (n - 1)) - INCLINA, 0, 0], [
                    osso(f"pingente_{i}_gira", list(prox), [0, gira, 0], [
                        peca(f"pingente_{i}", [qx - 1.6, cy - 1.6, qz - .6], [qx + 1.6, cy + 1.6, qz + .6], ouro_p,
                             rot=(0, 0, 45), pivo=(qx, cy, qz)),
                        peca(f"pingente_{i}_gema", [qx - .8, cy - .8, qz - .85], [qx + .8, cy + .8, qz + .85], gema_p,
                             rot=(0, 0, 45), pivo=(qx, cy, qz), brilho=True)])]))
            return osso(f"corrente_{i}_{k}", list(pos), list(rot0) if k == 0 else [curva, 0, 0], filhos)
        return elo(0, base)
    # penas vermelhas de baixo da cauda, atrás das pernas (de frente tapam o vão entre as pernas, como na ficha)
    corpo.append(pena_placa("sob_cauda", (0, 12.2, 4.0), (-INCLINA, 0, 0), 8.2, 3.0, (VERM_ESC, VERM, LARANJA_ESC), eixo="x"))
    # correntes compridas: saem da traseira, fazem um arco para trás e descem; pingentes no chão atrás dos calcanhares
    corpo.append(corrente(0, (0, 14.4, 5.2), 9, (-106, 0, 0), 7.5, 40, t=1.35, passo=1.75))
    corpo.append(corrente(1, (-2.0, 14.6, 4.8), 8, (-102, -10, 0), 8.5, -40, t=1.35, passo=1.75))
    corpo.append(corrente(2, (2.0, 14.6, 4.8), 8, (-102, 10, 0), 8.5, 40, t=1.35, passo=1.75))

    corpo.append(pescoco)
    tronco = osso("corpo", [0, 15, 0], [INCLINA, 0, 0], corpo)
    SOBE_CORPO = 0.4
    for pc in PECAS[i_cab:]:
        pc.de[1] += SOBE_CORPO; pc.ate[1] += SOBE_CORPO; pc.pivo[1] += SOBE_CORPO
        pc.pintas = getattr(pc, "pintas", []) + [((0.0, 0.0, 0.0), 1.0, SOBE_CORPO)]
    def sobe(no):
        if isinstance(no, dict):
            no["origin"][1] += SOBE_CORPO
            for f in no["children"]: sobe(f)
    sobe(tronco)

    # ---------- pernas: coxa de penas (sobrecoxa), bota roxa em carretel, pé de 3 dedos com garra + 1 atrás ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 2.5 * lado; zc = 1.8
        pp = []
        mc = mat_cor(lambda p, f: mix(AMARELO, LARANJA, clamp((p[1] - 5.4) / 4.0)), borda=.05, curva=.4)
        pp.append(peca("coxa_" + s, [xc - 1.6, 8.2, zc - 1.6], [xc + 1.6, 11.0, zc + 1.6], mat_cor(cor_barriga, borda=.04, curva=.3), faixa=(5.4, 11.0)))
        pp.append(peca("canela_" + s, [xc - 1.15, 5.3, zc - 1.15], [xc + 1.15, 8.4, zc + 1.15], mat_cor(cor_barriga, borda=.04, curva=.3), faixa=(5.4, 11.0)))
        pp += octogono("bota_topo_" + s, [xc - 2.1, 4.5, zc - 2.1], [xc + 2.1, 5.5, zc + 2.1], mat_cor(lambda p, f: mix(ROXO, LILAS, .55), borda=.2), r=.7)
        pp += octogono("bota_meio_" + s, [xc - 1.6, 3.1, zc - 1.6], [xc + 1.6, 4.6, zc + 1.6], mat_cor(lambda p, f: ROXO, borda=.1), r=.5)
        pp += octogono("bota_base_" + s, [xc - 2.1, 2.1, zc - 2.1], [xc + 2.1, 3.1, zc + 2.1], mat_cor(lambda p, f: mix(ROXO, LILAS, .55), borda=.2), r=.7)
        md = mat_cor(lambda p, f: LARANJA if f == "down" else AMARELO, borda=.2, curva=.5)
        mg = mat_cor(lambda p, f: AMARELO_ESC, borda=.2, curva=.5)
        for nome, giro, dx in (("meio", 0, 0), ("fora", -18 * lado, 1.9 * lado), ("dentro", 18 * lado, -1.9 * lado)):
            x0, z0 = xc + dx, zc - 1.7
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - .9, 0, z0 - 2.6], [x0 + .9, 2.2, z0 + 0.6], md, faixa=(0, 2.2)),
                peca(f"dedo2_{nome}_{s}", [x0 - .8, 0, z0 - 4.0], [x0 + .8, 1.7, z0 - 2.6], md, faixa=(0, 2.2)),
                osso(f"garra_{nome}_{s}", [x0, 1.0, z0 - 4.0], [-28, 0, 0], [
                    peca(f"garra_{nome}_{s}", [x0 - .4, 0.2, z0 - 4.9], [x0 + .4, 1.0, z0 - 4.0], mg, faixa=(0, 2.0))])]))
        pp.append(peca("dedo_tras_" + s, [xc - .6, 0, zc + 1.4], [xc + .6, 1.4, zc + 3.4], md, faixa=(0, 2.0)))
        return osso("perna_" + s, [xc, 11.0, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

# ---------------- textura (atlas com UV por face) e saída ----------------
def gerar():
    outliner = montar()
    faces = []
    for p in PECAS:
        for face in NORMAL:
            fw, fh = dims(face, p)
            tw, th = max(1, math.ceil(round(fw * p.res, 3))), max(1, math.ceil(round(fh * p.res, 3)))
            if fw <= 1e-6 or fh <= 1e-6: continue
            faces.append((p, face, tw, th))
    largura = 512
    faces.sort(key=lambda f: (-f[3], -f[2]))
    x = y = lh = 0
    pos = {}
    for p, face, tw, th in faces:
        if x + tw > largura: x, y, lh = 0, y + lh, 0
        pos[(p.uuid, face)] = (x, y); x += tw; lh = max(lh, th)
    altura = 64
    while altura < y + lh: altura *= 2
    img = Image.new("RGBA", (largura, altura), (0, 0, 0, 0)); px = img.load()
    brilho = Image.new("RGBA", (largura, altura), (0, 0, 0, 0)); pb = brilho.load()
    for p, face, tw, th in faces:
        x0, y0 = pos[(p.uuid, face)]
        tfs = getattr(p, "pintas", [])
        def inv(q, tfs=tfs):
            q = list(q)
            for C, k, sobe in reversed(tfs):
                q = [C[i] + (q[i] - (sobe if i == 1 else 0.0) - C[i]) / k for i in range(3)]
            return tuple(q)
        b = (list(inv(p.de)), list(inv(p.ate)))
        for i in range(tw):
            for j in range(th):
                u, v = (i + .5) / tw, (j + .5) / th
                pt = ponto(face, p, u, v)
                c = {"p": inv(pt), "face": face, "i": i, "j": j, "tw": tw, "th": th,
                     "faixa": p.faixa, "b": b, "nome": p.nome}
                cor = p.mat(c)
                if cor is None: continue                     # recorte: fora da forma fica transparente
                px[x0 + i, y0 + j] = tuple(cor) + (255,)
                if p.brilho is True or (callable(p.brilho) and p.brilho(c, cor)): pb[x0 + i, y0 + j] = tuple(cor) + (255,)
        p.uv[face] = [x0, y0, x0 + tw, y0 + th]
    img.save(PASTA / f"{NOME}.png"); brilho.save(PASTA / f"{NOME}_glowmask.png")
    buf = io.BytesIO(); img.save(buf, format="PNG")
    elements = [{"name": p.nome, "box_uv": False, "rescale": False, "locked": False, "from": p.de, "to": p.ate,
                 "autouv": 0, "color": 0, "origin": p.pivo, "rotation": p.rot,
                 "faces": {f: {"uv": uv, "texture": 0} for f, uv in p.uv.items()}, "type": "cube", "uuid": p.uuid}
                for p in PECAS]
    bb = {"meta": {"format_version": "4.10", "model_format": "bedrock", "box_uv": False}, "name": NOME,
          "model_identifier": "pirococo", "visible_box": [4, 3.5, 1.5], "resolution": {"width": largura, "height": altura},
          "elements": elements, "outliner": outliner,
          "textures": [{"path": "", "name": f"{NOME}.png", "folder": "", "namespace": "", "id": "0", "width": largura,
                        "height": altura, "uv_width": largura, "uv_height": altura, "particle": False, "render_mode": "default",
                        "visible": True, "internal": True, "saved": False, "uuid": str(uuid.uuid4()), "relative_path": "",
                        "source": "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()}], "animations": []}
    caminho = PASTA / f"{NOME}.bbmodel"
    caminho.write_text(json.dumps(bb, indent=1), encoding="utf-8")
    return caminho, len(PECAS), (largura, altura)

if __name__ == "__main__":
    caminho, n, tam = gerar()
    q = previa.carregar(str(caminho))
    vistas = [("Frente", 0, -6), ("3/4", -38, -12), ("Lado", 90, -5)]
    ims = [(v, previa.desenhar(q, y, p, escala=22)) for v, y, p in vistas]
    H = max(i.height for _, i in ims) + 24
    folha = Image.new("RGB", (sum(i.width for _, i in ims) + 20, H), (22, 24, 29)); x = 0
    for v, i in ims:
        folha.paste(i, (x, 24 + (H - 24 - i.height))); ImageDraw.Draw(folha).text((x + 8, 6), v, fill=(220, 220, 220))
        x += i.width + 10
    folha.save(PASTA / f"{NOME}_previa.png")
    print(f"{n} pecas, textura {tam}")
