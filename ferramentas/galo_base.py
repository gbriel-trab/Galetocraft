"""Biblioteca comum dos geradores das criaturas do Galetocraft (a técnica do Pirococó v7, generalizada).

Cada espécie fica em ferramentas/especies/<id>.py e usa daqui:
- Peca / peca() / osso(): cubos com UV POR FACE e ossos no formato do Blockbench (Bedrock).
- PINTURA EM 3D: cada cubo recebe um material mat(c) que devolve a cor de um pixel da textura a partir do
  ponto 3D dele (c["p"]), da face (c["face"]), da posição na face (c["i"], c["j"] de c["tw"] x c["th"]),
  da faixa de altura do grupo (c["faixa"]) e da caixa do cubo (c["b"]). Devolver None = pixel transparente
  (recorte: penas, chamas, folhas, espinhos são placas finas recortadas, como o fogo do Minecraft).
- Formas prontas: arredondado/arredondado2 (volume com quinas chanfradas), octogono, pena_curva (segmentos
  encadeados que afinam e curvam), pena_placa/pena_cone_placa/pena_cruzada (penas recortadas), chama_cruzada,
  losango (gema), placa_armadura/placa_cone, anel (pontos numa elipse em volta do corpo), pintar_olho.
- gerar(): monta o atlas da textura, a máscara de brilho (_glowmask) e o .bbmodel.
- revisao(): imagens de revisão (vistas da ficha, 3/4 grande e close do rosto).

Convenções (iguais ao Pirococó):
- 16 unidades = 1 bloco; y para cima; a FRENTE da criatura olha para -z (o bico fica em z negativo).
- lado = -1 é o lado DIREITO da criatura (x negativo, sufixo "_d"); lado = +1 é o esquerdo (sufixo "_e").
- Rotação = Rz·Ry·Rx em graus (Blockbench); osso: p -> R (p - origem) + origem.
- D = 2 pixels de textura por unidade (res=4..8 em peças com desenho fino: rosto, emblemas, placas recortadas).
- Construa a criatura já no tamanho final aproximado (2,45 blocos ~ 39 unidades de altura): o exportador
  normaliza a altura, mas a densidade de pixels da textura depende do tamanho em que foi modelada.
"""
import base64, io, json, math, sys, uuid
from pathlib import Path
from PIL import Image, ImageDraw

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))

D = 2                                   # pixels de textura por unidade do modelo (padrão)

# ---------------- cores ----------------
BRANCO = (248, 244, 240); PRETO = (26, 12, 22)
AMARELO = (255, 198, 34); AMARELO_CLARO = (255, 226, 110); AMARELO_ESC = (240, 150, 20)
LARANJA = (246, 120, 20); LARANJA_ESC = (232, 92, 16)
VERM = (226, 40, 30); VERM_ESC = (184, 24, 26); VERM_VIVO = (246, 70, 40)
OURO = (246, 186, 50); OURO_CLARO = (255, 232, 130); OURO_ESC = (178, 112, 24)

def clamp(v, a=0.0, b=1.0): return max(a, min(b, v))
def mix(a, b, f):
    f = clamp(f)
    return tuple(int(round(a[i] + (b[i] - a[i]) * f)) for i in range(3))
def sombra_de(c): return (int(c[0] * .60), int(c[1] * .38), int(c[2] * .58))
LUZ = (255, 246, 220)
def tom(c, f):
    """f > 0 clareia (puxa para a luz quente), f < 0 escurece (sombra puxada para o roxo, como no Pirococó)."""
    f = clamp(f, -1, 1)
    return mix(c, LUZ, f * .40) if f >= 0 else mix(c, sombra_de(c), -f * .9)

# ---------------- estrutura ----------------
class Peca:
    """Cubo com UV por face. 'mat(c)' devolve a cor de um pixel a partir do contexto 3D 'c' (ou None = transparente).
    brilho: False, True (o cubo todo brilha no escuro) ou função (c, cor) -> bool (só alguns pixels brilham)."""
    def __init__(self, nome, de, ate, mat, rot=(0, 0, 0), pivo=None, faixa=None, brilho=False, res=None):
        self.nome, self.de, self.ate, self.mat = nome, list(de), list(ate), mat
        self.rot = list(rot); self.pivo = list(pivo) if pivo else [(de[i] + ate[i]) / 2 for i in range(3)]
        self.faixa = faixa or (de[1], ate[1])     # faixa de altura usada no degradê (pode ser a do grupo)
        self.brilho = brilho; self.uuid = str(uuid.uuid4()); self.uv = {}
        self.res = res or D
        self.pintas = []                          # transformações aplicadas depois (a pintura usa o ponto original)

def osso(nome, origem, rot, filhos):
    return {"name": nome, "origin": list(origem), "rotation": list(rot), "color": 0, "uuid": str(uuid.uuid4()),
            "export": True, "isOpen": True, "visibility": True, "children": [f for f in filhos if f is not None]}

PECAS = []
def peca(*a, **k):
    """Cria a peça, registra e devolve o uuid (é o que vai na lista 'filhos' de um osso)."""
    p = Peca(*a, **k); PECAS.append(p); return p.uuid

def reiniciar(): PECAS.clear()

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

def transformar(desde, nos, centro, k=1.0, sobe=0.0):
    """Escala (fator k em volta de 'centro') e sobe (em y) todas as peças criadas a partir do índice 'desde' de
    PECAS e os ossos da lista 'nos'. A pintura continua usando as coordenadas ORIGINAIS (os materiais não mudam).
    Útil para ajustar o tamanho da cabeça inteira depois de modelada (como o K_CAB do Pirococó)."""
    for pc in PECAS[desde:]:
        for arr in (pc.de, pc.ate, pc.pivo):
            for i in range(3): arr[i] = centro[i] + (arr[i] - centro[i]) * k
            arr[1] += sobe
        pc.pintas.append((tuple(centro), k, sobe))
    def visita(no):
        if isinstance(no, dict):
            o = no["origin"]
            for i in range(3): o[i] = centro[i] + (o[i] - centro[i]) * k
            o[1] += sobe
            for f in no["children"]: visita(f)
    for no in nos: visita(no)

# ---------------- materiais (pintura em 3D) ----------------
def na_borda(c): return c["i"] in (0, c["tw"] - 1) or c["j"] in (0, c["th"] - 1)

def contexto_luz(c, borda=.12, topo=.18, baixo=.32, curva=.55):
    """Luz contínua: claro em cima, escuro embaixo (pela altura na faixa do grupo), face de cima mais clara,
    e um fio escuro na borda de cada face (acabamento)."""
    y0, y1 = c["faixa"]
    t = clamp((c["p"][1] - y0) / max(y1 - y0, 1e-6))
    luz = -curva / 2 + curva * t
    if c["face"] == "up": luz += topo
    if c["face"] == "down": luz -= baixo
    if na_borda(c): luz -= borda
    return luz

def mat_cor(cor_fn, **kw):
    """cor_fn(p, face) -> cor base no ponto 3D; aplica a luz contínua por cima (kw vai para contexto_luz)."""
    def f(c):
        base = cor_fn(c["p"], c["face"])
        return None if base is None else tom(base, contexto_luz(c, **kw))
    return f

def mat_solido(cor, **kw): return mat_cor(lambda p, f: cor, **kw)

def mat_pena(c0, c1, eixo, inverte=False, borda=.2):
    """Pena (bloco): degradê c0 -> c1 ao longo do eixo do comprimento, luz em cima, contorno escuro."""
    def f(c):
        lo, hi = c["b"][0][eixo], c["b"][1][eixo]
        t = clamp((c["p"][eixo] - lo) / max(hi - lo, 1e-6))
        if inverte: t = 1 - t
        luz = .08
        if c["face"] == "up": luz += .2
        if c["face"] == "down": luz -= .35
        if na_borda(c): luz -= borda
        return tom(mix(c0, c1, t), luz)
    return f

def mat_asa(c0, c1, ei, inv, borda=.2):
    """Pena (bloco) da asa: como mat_pena + raque clara no meio da face larga e beirada de trás mais escura."""
    base = mat_pena(c0, c1, ei, inv, borda)
    def f(c):
        cor = base(c)
        if c["face"] in ("east", "west"):
            (_, _, z0), (_, _, z1) = c["b"]
            d = (c["p"][2] - (z0 + z1) / 2) / max((z1 - z0) / 2, 1e-6)
            if abs(d) < .16: cor = tom(cor, .16)
            elif d > .55: cor = tom(cor, -.22 * (d - .55) / .45)
        return cor
    return f

def mat_facetado(cima, frente, lado, baixo, quina=-0.3):
    """Material 'facetado' (armadura, metal, casco, pedra): uma cor por direção de face e quinas escurecidas."""
    def f(c):
        face = c["face"]
        base = cima if face == "up" else baixo if face == "down" else frente if face == "north" else lado
        return tom(base, quina) if na_borda(c) else base
    return f

def mat_seg(mat):
    """Adapta um material comum para o formato (c0, c1, eixo, inverte) usado por pena_curva."""
    return lambda c0, c1, ei, inv: mat

# ---------------- formas ----------------
def arredondado(nome, de, ate, mat, r=1.0, faixa=None, **kw):
    """Volume com as quinas chanfradas: 3 blocos em cruz (cada eixo encolhido r de cada lado). Devolve 3 uuids."""
    (x0, y0, z0), (x1, y1, z1) = de, ate
    faixa = faixa or (y0, y1)
    return [peca(nome + "_a", [x0 + r, y0 + r, z0], [x1 - r, y1 - r, z1], mat, faixa=faixa, **kw),
            peca(nome + "_b", [x0, y0 + r, z0 + r], [x1, y1 - r, z1 - r], mat, faixa=faixa, **kw),
            peca(nome + "_c", [x0 + r, y0, z0 + r], [x1 - r, y1, z1 - r], mat, faixa=faixa, **kw)]

def arredondado2(nome, de, ate, mat, r=1.0, faixa=None, **kw):
    """Bem arredondado (borda em 2 degraus): os 3 blocos em cruz + um bloco do meio. Devolve 4 uuids."""
    (x0, y0, z0), (x1, y1, z1) = de, ate
    h = r / 2
    faixa = faixa or (y0, y1)
    return arredondado(nome, de, ate, mat, r=r, faixa=faixa, **kw) + [
        peca(nome + "_d", [x0 + h, y0 + h, z0 + h], [x1 - h, y1 - h, z1 - h], mat, faixa=faixa, **kw)]

def octogono(nome, de, ate, mat, r=0.6, faixa=None, **kw):
    """Prisma de 8 lados (quinas verticais chanfradas): 2 blocos em cruz."""
    (x0, y0, z0), (x1, y1, z1) = de, ate
    return [peca(nome + "_a", [x0 + r, y0, z0], [x1 - r, y1, z1], mat, faixa=faixa, **kw),
            peca(nome + "_b", [x0, y0, z0 + r], [x1, y1, z1 - r], mat, faixa=faixa, **kw)]

def pena_curva(nome, base, segs, rot0, curva, eixo_comp, mat_fn, lado=1, brilho_ponta=False, res=None):
    """Cadeia curva: segmentos encadeados (um osso por segmento, nomes '<nome>_0', '<nome>_1'...) que afinam e
    giram 'curva' graus (rx, ry, rz) a cada um. Serve para penas grossas, chifres, caudas, tentáculos, cipós.
    segs = [(comprimento, largura, altura, cor0, cor1)]; cresce no eixo 'eixo_comp': 'y', '-y', 'z', '-z' ou '-x'
    ('-x' = para fora: lado -1 cresce para -x). mat_fn(c0, c1, eixo, inverte) -> material (ex.: mat_pena)."""
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
        elif eixo_comp == "-z":
            de, ate, prox, ei = [px - w / 2, py - h / 2, pz - L], [px + w / 2, py + h / 2, pz], (px, py, pz - L + .2), 2
        else:
            if lado < 0: de, ate, prox = [px - L, py - h / 2, pz - w / 2], [px, py + h / 2, pz + w / 2], (px - L + .2, py, pz)
            else: de, ate, prox = [px, py - h / 2, pz - w / 2], [px + L, py + h / 2, pz + w / 2], (px + L - .2, py, pz)
            ei = 0
        inv = (lado < 0 and eixo_comp == "-x") or eixo_comp in ("-y", "-z")
        filhos = [peca(f"{nome}_{k}", de, ate, mat_fn(c0, c1, ei, inv), brilho=brilho_ponta and k == len(segs) - 1, res=res)]
        if k + 1 < len(segs): filhos.append(seg(k + 1, prox))
        r = rot0 if k == 0 else curva
        return osso(f"{nome}_{k}", list(pos), r, filhos)
    return seg(0, (x, y, z))

def anel(ax, az, zc, phi, lado):
    """Ponto (x, z) numa elipse em volta do corpo: phi = 0 lado de fora, negativo = frente, positivo = trás."""
    r = math.radians(phi)
    return lado * ax * math.cos(r), zc + az * math.sin(r)

# ---------------- placas recortadas (pena, folha, espinho, chama...) ----------------
def forma_pena(u, v, curva=0.0):
    """u: -1..1 na largura, v: 0 (raiz) .. 1 (ponta). Larga, afina numa ponta; 'curva' entorta a ponta.
    Devolve (dentro?, distância até a borda, u corrigido)."""
    uc = u - curva * v * v
    meia = 0.8 + 0.2 * min(1.0, v / 0.4) if v < 0.55 else max(0.0, 1.0 - ((v - 0.55) / 0.45) ** 1.5)
    return abs(uc) <= meia, meia - abs(uc), uc

def mat_placa_pena(cores, y0, L, centro, W, curva=0.0, fio=None, eixo="z", forma=None, raque=True, contorno=-.4):
    """Pena pendurada para baixo a partir de y0: recorte em forma de pena, 3 faixas de cor (raiz, meio, ponta),
    raque discreta, contorno escuro e 'fio' de cor na borda de cima, se pedido.
    'forma(u, v) -> (dentro, borda, uc)' troca o recorte (padrão: forma_pena com 'curva')."""
    c0, c1, c2 = cores
    forma = forma or (lambda u, v: forma_pena(u, v, curva))
    def f(c):
        x, y, z = c["p"]
        v = (y0 - y) / L
        u = ((z if eixo == "z" else x) - centro) / (W / 2)
        if not (-0.01 <= v <= 1.0): return None
        ok, borda, uc = forma(u, max(v, 0.0))
        if not ok: return None
        if v < 0.42: cor = tom(c0, 0.1 - 0.25 * v)
        elif v < 0.74: cor = tom(c1, 0.08 - 0.2 * (v - 0.42))
        else: cor = tom(c2, 0.1 - 0.15 * (v - 0.74))
        if fio and borda < 0.14 and v < 0.6: return fio
        if raque and abs(uc) < 0.06 and v < 0.8: cor = tom(cor, .12)
        if borda < 0.1: return tom(cor, contorno)
        return cor
    return f

def pena_placa(nome, raiz, rot, L, W, cores, esp=0.3, curva=0.0, fio=None, res=4, eixo="z", forma=None, brilho=False):
    """Placa fina (espessura 'esp') pendurada para BAIXO a partir da raiz, comprimento L, largura W.
    eixo='z': a face larga olha para os lados (±x); eixo='x': a face larga olha para frente/trás (±z).
    Gire o osso (rot) para apontar a pena para onde quiser (ex.: rot x = +90 deita para trás... teste na prévia)."""
    x, y, z = raiz
    if eixo == "z":
        de, ate, centro = [x - esp / 2, y - L, z - W / 2], [x + esp / 2, y, z + W / 2], z
    else:
        de, ate, centro = [x - W / 2, y - L, z - esp / 2], [x + W / 2, y, z + esp / 2], x
    return osso(nome, list(raiz), list(rot), [peca(nome, de, ate, mat_placa_pena(cores, y, L, centro, W, curva, fio, eixo, forma),
                                                    res=res, brilho=brilho)])

def pena_cruzada(nome, raiz, rot, L, W, cores, curva=0.0, forma=None, brilho=False):
    """Pena em X girado 45°: nenhuma das duas placas fica de perfil nas vistas de frente, lado e costas."""
    return osso(nome, list(raiz), list(rot), [osso(nome + "_x", list(raiz), [0, 45, 0], [
        pena_placa(nome + "_a", raiz, (0, 0, 0), L, W, cores, curva=curva, eixo="z", forma=forma, brilho=brilho),
        pena_placa(nome + "_b", raiz, (0, 0, 0), L, W, cores, curva=0.0, eixo="x", forma=forma, brilho=brilho)])])

def pena_cone_placa(nome, raiz, phi, flare, L, W, cores, lado, varre=0, curva=0.25, fio=None, forma=None, brilho=False):
    """Placa-pena numa 'saia' em volta do corpo: o osso de fora gira em y (face larga para fora no ângulo phi);
    a pena varre para trás ('varre' graus) e abre 'flare' graus para fora."""
    return osso(nome, list(raiz), [0, -phi * lado, 0],
                [pena_placa(nome + "_p", raiz, (-varre, 0, flare * lado), L, W, cores, curva=curva, fio=fio, forma=forma, brilho=brilho)])

def mat_chama(L, y0, W, eixo, centro, curl, cores=(VERM, LARANJA, AMARELO)):
    """Chama recortada para CIMA a partir de y0: cor0 na base, cor1 no meio, cor2 na ponta, contorno escuro."""
    c0, c1, c2 = cores
    def f(c):
        x, y, z = c["p"]
        v = (y - y0) / L
        u = ((z if eixo == "z" else x) - centro) / (W / 2)
        if not (0.0 <= v <= 1.0): return None
        uc = u - curl * v * v
        meia = (1.0 - v ** 2.0) * (1.0 if v > 0.12 else 0.72 + 2.3 * v)
        if abs(uc) > meia: return None
        borda = meia - abs(uc)
        cor = mix(c0, c1, v / 0.6) if v < 0.6 else mix(c1, c2, min(1.0, (v - 0.6) / 0.3))
        if borda < 0.08: cor = tom(cor, -.35)
        return cor
    return f

def chama_cruzada(nome, base, rot, L, W, curl=0.4, esp=0.25, brilho=True, cores=(VERM, LARANJA, AMARELO)):
    """Chama (ou qualquer forma de 'labareda' para CIMA) em X girado 45°, como o fogo do Minecraft."""
    x, y, z = base
    return osso(nome, list(base), list(rot), [osso(nome + "_x", list(base), [0, 45, 0], [
        peca(nome + "_a", [x - esp / 2, y, z - W / 2], [x + esp / 2, y + L, z + W / 2], mat_chama(L, y, W, "z", z, curl, cores), res=4, brilho=brilho),
        peca(nome + "_b", [x - W / 2, y, z - esp / 2], [x + W / 2, y + L, z + esp / 2], mat_chama(L, y, W, "x", x, 0.0, cores), res=4, brilho=brilho)])])

def mat_losango(W, H, cy, eixo, centro, moldura=(OURO_ESC, OURO_CLARO, OURO), gema=(VERM_VIVO, VERM_ESC), reflexo=(255, 190, 180)):
    """Losango: moldura (escura, clara, média) e gema com reflexo."""
    def f(c):
        x, y, z = c["p"]
        u = ((z if eixo == "z" else x) - centro) / (W / 2); v = (y - cy) / (H / 2)
        d = abs(u) + abs(v)
        if d > 1.0: return None
        if d > 0.93: return moldura[0]
        if d > 0.6: return mix(moldura[1], moldura[2], clamp((0.3 - v) / 1.2))
        if (u + 0.18) ** 2 + (v - 0.22) ** 2 < 0.025: return reflexo
        return mix(gema[0], gema[1], clamp((0.5 - v) / 1.1))
    return f

def losango(nome, centro, W, H, eixo="x", esp=0.4, res=6, brilho=True, **cores):
    """Gema em losango numa placa fina. eixo='x': placa de frente (fina em z); 'z': placa de lado."""
    x, y, z = centro
    if eixo == "x":
        return peca(nome, [x - W / 2, y - H / 2, z - esp / 2], [x + W / 2, y + H / 2, z + esp / 2], mat_losango(W, H, y, "x", x, **cores), res=res, brilho=brilho)
    return peca(nome, [x - esp / 2, y - H / 2, z - W / 2], [x + esp / 2, y + H / 2, z + W / 2], mat_losango(W, H, y, "z", z, **cores), res=res, brilho=brilho)

def placa_armadura(nome, raiz, rot, L, W, esp=0.7, mat=None, cores=None):
    """Placa grossa e pontuda (para baixo a partir da raiz): corpo + ponta em losango (cubo girado 45°).
    cores = (cima, frente, lado, baixo) para um material facetado, ou passe 'mat' pronto."""
    x, y, z = raiz
    m = mat or mat_facetado(*(cores or ((184, 140, 240), (150, 92, 214), (134, 64, 204), (86, 36, 140))))
    cy = y - L * 0.72; sq = W / 1.4142
    return osso(nome, list(raiz), list(rot), [
        peca(nome, [x - esp / 2, cy, z - W / 2], [x + esp / 2, y, z + W / 2], m, res=4),
        peca(nome + "_ponta", [x - esp / 2 + 0.02, cy - sq / 2, z - sq / 2], [x + esp / 2 - 0.02, cy + sq / 2, z + sq / 2], m,
             rot=(45, 0, 0), pivo=(x, cy, z), res=4)])

def placa_cone(nome, raiz, phi, flare, L, W, lado, varre=0, esp=0.7, mat=None, cores=None):
    return osso(nome, list(raiz), [0, -phi * lado, 0], [placa_armadura(nome + "_p", raiz, (-varre, 0, flare * lado), L, W, esp, mat, cores)])

# ---------------- olhos ----------------
def pintar_olho(u, v, ru, rv, iris=((150, 10, 30), (236, 44, 44)), esclera=BRANCO, pupila=PRETO,
                r_iris=(0.62, 0.74), c_iris=(-0.24, 0.0), r_pup=(0.32, 0.36), fenda=False, brilho=(255, 255, 255),
                bravo=0.0, alto=0.62, contorno=None):
    """Olho desenhado em 2D numa face. (u, v) = posição do pixel em unidades do modelo, relativa ao centro do olho:
    u ao longo da face (NEGATIVO = para o bico), v para cima. ru, rv = raios do olho.
    Devolve a cor do pixel ou None (fora do olho: a pele/pena do material de baixo aparece).
    - c_iris: centro da íris em frações de (ru, rv) (negativo = olhando para a frente).
    - fenda=True: pupila em fenda vertical (réptil, morcego, cobra); senão redonda.
    - bravo > 0: corta o alto do olho com uma linha que desce para o bico (sobrancelha brava); 'alto' é a altura
      (em fração de rv) da linha no meio do olho.
    - contorno: cor da beirada do olho (None = esclera sombreada)."""
    e = (u / ru) ** 2 + (v / rv) ** 2
    if e > 1: return None
    if bravo > 0 and v / rv > alto + bravo * (u / ru): return None
    iu, iv = u / ru - c_iris[0], v / rv - c_iris[1]
    di = (iu / r_iris[0]) ** 2 + (iv / r_iris[1]) ** 2
    if brilho and ((iu - 0.18) / 0.16) ** 2 + ((iv - 0.32) / 0.16) ** 2 <= 1: return brilho
    pu, pv = r_pup if not fenda else (r_pup[0] * 0.38, r_pup[1] * 1.9)
    if (iu / pu) ** 2 + (iv / pv) ** 2 <= 1: return pupila
    if di <= 1: return mix(iris[1], iris[0], clamp((0.5 - iv) / 1.3 + 0.2))
    if e > 0.84: return contorno or tom(esclera, -0.2)
    return mix(esclera, tom(esclera, -0.12), clamp(-v / rv))

# ---------------- textura (atlas com UV por face) e saída ----------------
def gerar(nome, pasta, outliner, identificador=None, largura=512):
    """Pinta todas as peças de PECAS num atlas, grava <pasta>/<nome>.bbmodel, .png e _glowmask.png."""
    pasta = Path(pasta); pasta.mkdir(parents=True, exist_ok=True)
    faces = []
    for p in PECAS:
        for face in NORMAL:
            fw, fh = dims(face, p)
            if fw <= 1e-6 or fh <= 1e-6: continue
            tw, th = max(1, math.ceil(round(fw * p.res, 3))), max(1, math.ceil(round(fh * p.res, 3)))
            faces.append((p, face, tw, th))
    faces.sort(key=lambda f: (-f[3], -f[2]))
    x = y = lh = 0
    pos = {}
    for p, face, tw, th in faces:
        if tw > largura: raise ValueError(f"face {p.nome}/{face} mais larga ({tw}px) que o atlas ({largura}px)")
        if x + tw > largura: x, y, lh = 0, y + lh, 0
        pos[(p.uuid, face)] = (x, y); x += tw; lh = max(lh, th)
    altura = 64
    while altura < y + lh: altura *= 2
    img = Image.new("RGBA", (largura, altura), (0, 0, 0, 0)); px = img.load()
    brilho = Image.new("RGBA", (largura, altura), (0, 0, 0, 0)); pb = brilho.load()
    for p, face, tw, th in faces:
        x0, y0 = pos[(p.uuid, face)]
        def inv(q, tfs=p.pintas):
            q = list(q)
            for C, k, sobe in reversed(tfs):
                q = [C[i] + (q[i] - (sobe if i == 1 else 0.0) - C[i]) / k for i in range(3)]
            return tuple(q)
        b = (list(inv(p.de)), list(inv(p.ate)))
        for i in range(tw):
            for j in range(th):
                u, v = (i + .5) / tw, (j + .5) / th
                c = {"p": inv(ponto(face, p, u, v)), "face": face, "i": i, "j": j, "tw": tw, "th": th,
                     "faixa": p.faixa, "b": b, "nome": p.nome}
                cor = p.mat(c)
                if cor is None: continue
                px[x0 + i, y0 + j] = tuple(int(v) for v in cor[:3]) + (255,)
                if p.brilho is True or (callable(p.brilho) and p.brilho(c, cor)): pb[x0 + i, y0 + j] = tuple(int(v) for v in cor[:3]) + (255,)
        p.uv[face] = [x0, y0, x0 + tw, y0 + th]
    img.save(pasta / f"{nome}.png"); brilho.save(pasta / f"{nome}_glowmask.png")
    buf = io.BytesIO(); img.save(buf, format="PNG")
    elements = [{"name": p.nome, "box_uv": False, "rescale": False, "locked": False, "from": p.de, "to": p.ate,
                 "autouv": 0, "color": 0, "origin": p.pivo, "rotation": p.rot,
                 "faces": {f: {"uv": uv, "texture": 0} for f, uv in p.uv.items()}, "type": "cube", "uuid": p.uuid}
                for p in PECAS]
    bb = {"meta": {"format_version": "4.10", "model_format": "bedrock", "box_uv": False}, "name": nome,
          "model_identifier": identificador or nome, "visible_box": [4, 3.5, 1.5], "resolution": {"width": largura, "height": altura},
          "elements": elements, "outliner": outliner,
          "textures": [{"path": "", "name": f"{nome}.png", "folder": "", "namespace": "", "id": "0", "width": largura,
                        "height": altura, "uv_width": largura, "uv_height": altura, "particle": False, "render_mode": "default",
                        "visible": True, "internal": True, "saved": False, "uuid": str(uuid.uuid4()), "relative_path": "",
                        "source": "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()}], "animations": []}
    caminho = pasta / f"{nome}.bbmodel"
    caminho.write_text(json.dumps(bb, indent=1), encoding="utf-8")
    return caminho

# ---------------- imagens de revisão ----------------
FUNDO = (14, 10, 12)

def desenhar_parte(dados, centro, raio, yaw, pitch, escala):
    """Renderiza só as faces INTEIRAS dentro do raio em volta de 'centro' (close do rosto, de uma pata...).
    Faces grandes que só encostam no raio (as do corpo) ficam de fora: senão apareciam como placas soltas."""
    import numpy as np, previa2
    faces, tex = dados
    C = np.array(centro, float)
    def dentro(f):
        p0, p1, p2 = (np.array(q, float) for q in f[0])
        cantos = (p0, p1, p2, p1 + p2 - p0)
        return (np.linalg.norm(sum(cantos) / 4 - C) < raio
                and all(np.linalg.norm(p - C) < 1.8 * raio for p in cantos))
    sel = [f for f in faces if dentro(f)]
    return previa2.desenhar((sel, tex), yaw, pitch, escala=escala, fundo=FUNDO)

def revisao(caminho, pasta, prefixo, rosto=None):
    """Grava <prefixo>_vistas.png (Frente, Lateral Direita, Traseira, Lateral Esquerda, como nas fichas),
    <prefixo>_3-4.png (3/4 grande, como a arte principal) e, se rosto=(centro, raio), <prefixo>_rosto.png
    (só a cabeça de frente, 3/4 e perfil)."""
    import previa2
    pasta = Path(pasta); pasta.mkdir(parents=True, exist_ok=True)
    q = previa2.carregar(str(caminho))
    vistas = [("Frente", 0, -6), ("Lateral Direita", 90, -5), ("Traseira", 180, -6), ("Lateral Esquerda", -90, -5)]
    ims = [(v, previa2.desenhar(q, y, p, escala=10, fundo=FUNDO)) for v, y, p in vistas]
    H = max(i.height for _, i in ims) + 26
    folha = Image.new("RGB", (sum(i.width for _, i in ims) + 12 * len(ims), H), FUNDO); x = 0
    for v, i in ims:
        folha.paste(i, (x, 26 + (H - 26 - i.height))); ImageDraw.Draw(folha).text((x + 6, 6), v, fill=(235, 235, 235)); x += i.width + 12
    folha.save(pasta / f"{prefixo}_vistas.png")
    previa2.desenhar(q, 35, -10, escala=20, fundo=FUNDO).save(pasta / f"{prefixo}_3-4.png")
    if rosto:
        centro, raio = rosto
        ims = [desenhar_parte(q, centro, raio, y, p, 40) for y, p in ((0, -6), (35, -8), (90, -4))]
        f = Image.new("RGB", (sum(i.width for i in ims) + 20, max(i.height for i in ims)), FUNDO); x = 0
        for i in ims: f.paste(i, (x, 0)); x += i.width + 10
        f.save(pasta / f"{prefixo}_rosto.png")
    return pasta / f"{prefixo}_vistas.png"

def rodar(id_, montar, rosto=None):
    """Ponto de entrada das espécies: `python especies/<id>.py [pasta_revisao] [prefixo]`.
    Gera modelos/<id>/<id>.bbmodel (+ .png, _glowmask.png) e as imagens de revisão
    (padrão: modelos/<id>/revisao/atual_*.png)."""
    reiniciar()
    outliner = montar()
    caminho = gerar(id_, RAIZ / "modelos" / id_, outliner, identificador=id_)
    pasta = Path(sys.argv[1]) if len(sys.argv) > 1 else RAIZ / "modelos" / id_ / "revisao"
    prefixo = sys.argv[2] if len(sys.argv) > 2 else "atual"
    revisao(caminho, pasta, prefixo, rosto)
    w, h = Image.open(RAIZ / "modelos" / id_ / f"{id_}.png").size
    print(f"{id_}: {len(PECAS)} peças, textura {w}x{h} -> {caminho}; revisão em {pasta}\\{prefixo}_*.png")
    return caminho
