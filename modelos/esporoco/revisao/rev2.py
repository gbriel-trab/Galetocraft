"""Esporocó (#003, Grama): a galoa das plantas tóxicas — plumagem de folhas verdes, crista foliar vermelha,
flores rosas de miolo brilhante e cauda de cipós espinhentos enrolados."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, mat_cor, anel, na_borda

ID = "esporoco"; NOME = "Esporocó"; NUMERO = 3
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 27.5, -2.5), 7.5)
# cipós da cauda (cadeias '<nome>_k'): ondulam devagar, mais em rx (no plano do enrolamento)
ONDAS = [("cipo_a", 17, (1.6, 1.0, 0.5)), ("cipo_b", 15, (1.8, 1.0, 0.5))]
ANIM_PARADO = {}
ANIM_ANDANDO = {}
INCLINA = -7             # o corpo se inclina para a frente (peito e cabeça à frente das pernas)

# ---------------- paleta (da 'Paleta de Cores' da ficha) ----------------
VERDE_ESC = (36, 81, 27); VERDE = (81, 137, 34); VERDE_CLARO = (133, 196, 70); LIMA = (168, 214, 84)
CREME = (239, 212, 169); CREME_ESC = (214, 176, 132)
VERMELHO = (190, 34, 50); VERM_CLARO = (228, 62, 64); VERM_ESC = (130, 18, 38)
ROSA = (232, 80, 154); ROSA_CLARO = (255, 150, 200); MAGENTA = (240, 49, 131); MAGENTA_ESC = (168, 24, 92)
AMARELO = (249, 170, 14); AMARELO_CLARO = (255, 214, 90); LARANJA = (236, 128, 18); MARROM = (134, 83, 16)
PRETO = (22, 14, 20); BRANCO = (250, 246, 242)
GLOW = (255, 236, 120)
VERDES = [VERDE, mix(VERDE, VERDE_CLARO, .5), mix(VERDE_ESC, VERDE, .5), VERDE, VERDE_CLARO, mix(VERDE_ESC, VERDE, .7), mix(VERDE, VERDE_CLARO, .3)]

def hash2(a, b):
    """Número pseudoaleatório fixo em 0..1 para a célula (a, b)."""
    h = math.sin(a * 127.1 + b * 311.7) * 43758.5453
    return h - math.floor(h)

# ---------------- folhas recortadas (plumagem vegetal) ----------------
def forma_folha(u, v):
    """Folha: talo estreito na raiz, larga no meio, ponta fina. u: -1..1, v: 0 (raiz) .. 1 (ponta)."""
    if v < 0.4: meia = 0.6 + 0.4 * math.sin(v / 0.4 * math.pi / 2)
    else: meia = max(0.0, 1.0 - ((v - 0.4) / 0.6) ** 1.25)
    return abs(u) <= meia, meia - abs(u), u

def mat_folha(cor, y0, L, centro, W, eixo="z", dobra=True):
    """Folha pendurada para baixo a partir de y0: metade clara e metade escura (folha dobrada, como as da
    ficha), nervura central clara, raiz um pouco mais escura e contorno escuro."""
    def f(c):
        x, y, z = c["p"]
        v = (y0 - y) / L
        u = ((z if eixo == "z" else x) - centro) / (W / 2)
        if not (-0.01 <= v <= 1.0): return None
        ok, borda, uc = forma_folha(u, max(v, 0.0))
        if not ok: return None
        base = tom(cor, -0.18 + 0.3 * min(v, 0.6))
        if dobra: base = tom(base, 0.14 if uc < 0 else -0.12)
        if abs(uc) < 0.08 and v < 0.85: base = tom(base, 0.28)
        if borda < 0.08: return tom(base, -0.38)
        return base
    return f

def folha(nome, raiz, rot, L, W, cor, esp=0.35, eixo="z", res=4):
    x, y, z = raiz
    if eixo == "z":
        de, ate, centro = [x - esp / 2, y - L, z - W / 2], [x + esp / 2, y, z + W / 2], z
    else:
        de, ate, centro = [x - W / 2, y - L, z - esp / 2], [x + W / 2, y, z + esp / 2], x
    return osso(nome, list(raiz), list(rot), [peca(nome, de, ate, mat_folha(cor, y, L, centro, W, eixo), res=res)])

def folha_cone(nome, raiz, phi, flare, L, W, cor, lado, varre=0, esp=0.35):
    """Folha numa 'saia' em volta do corpo (como pena_cone_placa): phi = ângulo em volta, flare = abre para fora."""
    return osso(nome, list(raiz), [0, -phi * lado, 0], [folha(nome + "_p", raiz, (-varre, 0, flare * lado), L, W, cor, esp)])

# ---------------- plumagem pintada (escamas de folha no volume do corpo) ----------------
def cor_folhagem(p, face, zc=0.8, linha=1.9, coluna=2.4, topo=26.0, paleta=None, contraste=1.0):
    """Escamas de folhas sobrepostas pintadas em 3D (fileiras em y, colunas em volta do eixo vertical):
    a folha de cima cobre a de baixo; cada folha sorteia um verde da paleta e é dobrada (meia clara/meia escura)."""
    x, y, z = p
    pal = paleta or VERDES
    s = math.atan2(x, -(z - zc)) * 5.0                       # comprimento de arco aproximado em volta do corpo
    Y = (topo - y) / linha
    for dr in (1, 0):                                         # a fileira de cima (r-1) fica por cima
        r = math.floor(Y) - dr
        v = (Y - r) / 1.55                                    # folha com 1,55 fileira de comprimento
        if v > 1.0 or v < 0: continue
        desl = 0.5 * (r % 2)
        col = math.floor(s / coluna + desl)
        u = ((s / coluna + desl) - col - 0.5) * 2.2
        ok, borda, uc = forma_folha(u, v)
        if not ok: continue
        cor = pal[int(hash2(r, col) * len(pal)) % len(pal)]
        k = contraste
        cor = tom(cor, k * (-0.15 + 0.25 * min(v, 0.6)))
        cor = tom(cor, k * (0.12 if uc < 0 else -0.1))
        if abs(uc) < 0.07 and v < 0.8: cor = tom(cor, k * 0.22)
        if borda < 0.1: cor = tom(cor, -0.42 * k)
        return cor
    return tom(mix(VERDE_ESC, VERDE, .5), -0.1 * contraste)

# ---------------- flor tóxica (5 pétalas rosas, miolo amarelo que brilha) ----------------
def mat_flor(R, cx, cy):
    """Placa da flor (fina em z): 5 pétalas pontudas com dobra clara/escura, borda magenta, estames amarelos."""
    def f(c):
        x, y, z = c["p"]
        dx, dy = x - cx, y - cy
        r = math.hypot(dx, dy) / R
        if r > 1.0: return None
        if r < 0.2: return (255, 236, 140)
        ang = math.degrees(math.atan2(dy, dx))
        melhor = None
        for k in range(5):
            d = (ang - (90 + 72 * k) + 180) % 360 - 180
            a = r * math.cos(math.radians(d)); b = r * math.sin(math.radians(d))
            if a <= 0: continue
            hw = 0.5 * (0.3 + 0.7 * a / 0.55) if a < 0.55 else 0.5 * max(0.0, (1.0 - a) / 0.45) ** 0.8
            if abs(b) <= hw:
                borda = hw - abs(b)
                if melhor is None or borda > melhor[0]: melhor = (borda, a, b)
        if melhor is None: return None
        borda, a, b = melhor
        cor = mix(MAGENTA, ROSA, clamp((a - 0.1) / 0.3))
        cor = mix(cor, ROSA_CLARO, 0.45) if b > 0 else cor
        if borda < 0.05: cor = MAGENTA_ESC
        # estames: riscos amarelos curtos entre o miolo e as pétalas
        if 0.2 <= r < 0.38 and abs(b) < 0.035: return AMARELO
        if 0.36 <= r < 0.42 and abs(b) < 0.07: return AMARELO_CLARO
        return cor
    return f

def flor_brilha(c, cor): return cor[0] > 230 and cor[1] > 150 and cor[2] < 140

def flor(nome, centro, rot, R, esp=0.3):
    """Flor plana virada para -z (local), girada por 'rot'; miolo saliente amarelo com brilho."""
    x, y, z = centro
    m = R * 0.28
    def miolo(c):
        if c["face"] != "north": return (255, 214, 96)
        d = max(abs(c["i"] + 0.5 - c["tw"] / 2) / (c["tw"] / 2), abs(c["j"] + 0.5 - c["th"] / 2) / (c["th"] / 2))
        return mix((255, 250, 200), (255, 222, 110), clamp(d * 1.1 - 0.1))
    return osso(nome, list(centro), list(rot), [
        peca(nome + "_petalas", [x - R, y - R, z - esp / 2], [x + R, y + R, z + esp / 2], mat_flor(R, x, y), res=8,
             brilho=flor_brilha),
        peca(nome + "_miolo", [x - m, y - m, z - esp / 2 - 0.35], [x + m, y + m, z], miolo, res=6, brilho=True)])

# ---------------- cipó espinhento (cadeia curva com espinhos e flores) ----------------
def mat_cipo(c):
    """Cipó verde-escuro em blocos: face de fora (local +y) mais clara, juntas escuras a cada bloco."""
    face = c["face"]; x, y, z = c["p"]
    if face == "up": base = mix(VERDE_ESC, VERDE, 0.75)
    elif face == "down": base = tom(VERDE_ESC, -0.25)
    elif face in ("north", "south"): base = mix(VERDE_ESC, VERDE, 0.3)
    else:
        (_, y0, _), (_, y1, _) = c["b"]
        t = (y - y0) / max(y1 - y0, 1e-6)
        base = mix(VERDE_ESC, VERDE, 0.15 + 0.55 * t)
    blocos = math.floor(z / 1.1)
    base = tom(base, (hash2(blocos, len(face)) - 0.5) * 0.18)
    if face in ("up", "down", "east", "west") and (z / 1.1 - blocos) < 0.12: base = tom(base, -0.3)
    if na_borda(c): base = tom(base, -0.3)
    return base

def mat_espinho(c):
    """Espinho em blocos: base verde-creme, meio creme, ponta rosa; lados sombreados, quinas escuras."""
    face = c["face"]; y = c["p"][1]
    y0, y1 = c["faixa"]
    t = clamp((y - y0) / max(y1 - y0, 1e-6))
    base = mix((176, 196, 118), (240, 230, 190), t / 0.55) if t < 0.62 else mix((248, 170, 196), (236, 86, 146), (t - 0.62) / 0.38)
    if face in ("east", "south"): base = tom(base, -0.15)
    if face == "down": base = tom(base, -0.3)
    if face == "up": base = tom(base, 0.1)
    if na_borda(c): base = tom(base, -0.22)
    return base

def espinho(nome, base, rot, L=1.8, W=1.1):
    """Espinho cônico sólido: base, meio e ponta (blocos que afinam) apontando para +y local."""
    x, y, z = base
    fx = (y, y + L)
    w2, w3 = W * 0.66, W * 0.34
    return osso(nome, list(base), list(rot), [
        peca(nome + "_base", [x - W / 2, y - 0.3, z - W / 2], [x + W / 2, y + L * 0.4, z + W / 2], mat_espinho, faixa=fx, res=4),
        peca(nome + "_meio", [x - w2 / 2, y + L * 0.38, z - w2 / 2], [x + w2 / 2, y + L * 0.72, z + w2 / 2], mat_espinho, faixa=fx, res=4),
        peca(nome + "_ponta", [x - w3 / 2, y + L * 0.7, z - w3 / 2], [x + w3 / 2, y + L, z + w3 / 2], mat_espinho, faixa=fx, res=4)])

def cipo(nome, base, rot0, L, larguras, curvas, espinhos=None, flores=None):
    """Cipó: segmentos (ossos '<nome>_k') que crescem em +z local e dobram 'curvas[k]' graus em x a cada junta
    (positivo = para baixo). Cada segmento invade o anterior para a junta não abrir na curva.
    espinhos = {k: [direção...]} com 'fora' (+y local), 'd' (-x), 'e' (+x), 'dentro' (-y);
    flores = {k: (direção, R)}."""
    espinhos = espinhos or {}; flores = flores or {}
    def seg(k, pos):
        w = larguras[k]
        px, py, pz = pos
        ov = 0.6 * w * math.tan(math.radians(max(abs(curvas[min(k + 1, len(curvas) - 1)]), 10)) / 2) + 0.15
        filhos = [peca(f"{nome}_{k}", [px - w / 2, py - w / 2, pz - ov], [px + w / 2, py + w / 2, pz + L], mat_cipo, res=3)]
        for j, d in enumerate(espinhos.get(k, [])):
            zc = pz + L * (0.35 + 0.3 * j)
            rot = {"fora": (0, 0, 0), "e": (0, 0, -55), "d": (0, 0, 55), "dentro": (180, 0, 0)}[d]
            off = {"fora": (0, w / 2 - 0.1, 0), "e": (w / 2 - 0.3, w / 2 - 0.3, 0), "d": (-w / 2 + 0.3, w / 2 - 0.3, 0), "dentro": (0, -w / 2 + 0.1, 0)}[d]
            b = (px + off[0], py + off[1], zc + off[2])
            filhos.append(espinho(f"{nome}_esp{k}_{j}", b, rot, L=2.0 + 0.8 * w / 2, W=1.0 + 0.5 * w / 2))
        if k in flores:
            d, R = flores[k]
            if d == "e": filhos.append(flor(f"{nome}_flor{k}", (px + w / 2 + 0.25, py, pz + L / 2), (0, -90, 0), R))
            elif d == "d": filhos.append(flor(f"{nome}_flor{k}", (px - w / 2 - 0.25, py, pz + L / 2), (0, 90, 0), R))
            else: filhos.append(flor(f"{nome}_flor{k}", (px, py + w / 2 + 0.25, pz + L / 2), (90, 0, 0), R))
        if k + 1 < len(larguras): filhos.append(seg(k + 1, (px, py, pz + L)))
        return osso(f"{nome}_{k}", list(pos), list(rot0) if k == 0 else [curvas[k], 0, 0], filhos)
    return seg(0, tuple(base))

# ---------------- cadeia de lâminas (crista foliar) ----------------
def mat_crista(c):
    """Lâmina da crista: vermelho com luz em cima, nervura clara na face larga e contorno escuro."""
    face = c["face"]; x, y, z = c["p"]
    (x0, y0, z0), (x1, y1, z1) = c["b"]
    if face == "up": base = VERM_CLARO
    elif face == "down": base = VERM_ESC
    elif face in ("east", "west"):
        t = (z - z0) / max(z1 - z0, 1e-6)                                   # 0 = frente da lâmina
        base = mix(VERM_CLARO, VERMELHO, clamp(t * 1.6))                    # beirada da frente clara
        if t > 0.8: base = tom(base, -0.18)
        if abs(t - 0.42) < 0.05: base = tom(base, 0.16)                     # nervura
    else:                                                                   # faces largas: folha com nervura
        t = (x - x0) / max(x1 - x0, 1e-6)
        base = mix(VERM_CLARO if face == "north" else VERMELHO, VERM_ESC, clamp((abs(t - 0.5) - 0.18) * 1.6))
        if abs(t - 0.5) < 0.05: base = tom(base, 0.22)
        vy = (y - y0) / max(y1 - y0, 1e-6)                                  # veios diagonais saindo da nervura
        if abs(t - 0.5) > 0.08 and abs(((vy * 2.0 - abs(t - 0.5) * 1.6) % 1.0) - 0.5) < 0.05: base = tom(base, -0.12)
    if face in ("up", "down"):
        if na_borda(c): base = tom(base, -0.3)
    elif c["i"] in (0, c["tw"] - 1): base = tom(base, -0.35)               # só as beiradas compridas (sem anéis)
    return base

def lamina(nome, base, rot0, segs, curva):
    """Lâmina grossa em segmentos (cresce em +y local, dobra 'curva' graus em x por junta = para trás).
    segs = [(comprimento, espessura x, largura z)]."""
    def seg(k, pos):
        L, w, h = segs[k]
        px, py, pz = pos
        filhos = [peca(f"{nome}_{k}", [px - w / 2, py - 0.7, pz - h / 2], [px + w / 2, py + L, pz + h / 2], mat_crista, res=3)]
        if k + 1 < len(segs): filhos.append(seg(k + 1, (px, py + L, pz + 0.1 * h)))
        return osso(f"{nome}_{k}", list(pos), list(rot0) if k == 0 else [curva, 0, 0], filhos)
    return seg(0, tuple(base))

# ---------------- cabeça ----------------
K_CAB = 1.2               # escala da cabeça inteira (com crista) em volta da base do pescoço
CAB_Y0, CAB_Y1 = 24.0, 30.6
FX, FZ = 1.9, -4.3            # canto da frente (onde começa a faceta do olho)
SX, SZ = 4.0, -2.0            # canto do lado
FAC_T = 1.4
FAC_L = math.hypot(SX - FX, SZ - FZ)
NX, NZ = (SZ - FZ) / FAC_L, -(SX - FX) / FAC_L     # normal de fora da faceta (lado +x)
FAC_C = ((FX + SX) / 2 - NX * FAC_T / 2, (FZ + SZ) / 2 - NZ * FAC_T / 2)
OLHO_Y = 28.15
OLHO_U = -0.12                # deslocamento do centro do olho ao longo da faceta (+ = para trás)
LARANJA_BICO = (242, 164, 30); LARANJA_BICO_CLARO = (255, 200, 84); LARANJA_BICO_ESC = (214, 118, 18)
MASCARA = mix(LIMA, VERDE_CLARO, .35)

def cor_cabeca(p, face):
    """Cabeça: máscara lima na altura dos olhos, faixa lima da bochecha, queixo e bochechas de baixo creme,
    testa verde e lados/nuca com escamas de folha discretas."""
    x, y, z = p
    if face == "down": return CREME if z < 0.5 else VERDE_CLARO
    frente = z < -1.2
    if frente and y < 26.05 and abs(x) < 2.3: return CREME                  # queixo e bochechas creme
    if frente and y < 26.95: return LIMA                                    # faixa lima da bochecha
    if frente and y < 29.5 and face != "up": return MASCARA                 # máscara clara dos olhos
    if z > -1.2 and y < 25.6: return mix(CREME, VERDE_CLARO, clamp((z + 1.2) / 2.5))
    if frente: return mix(VERDE, VERDE_CLARO, .25)                          # testa
    return cor_folhagem(p, face, zc=0.6, linha=1.5, coluna=1.9, topo=31.6, contraste=0.4,
                        paleta=[VERDE, mix(VERDE, VERDE_CLARO, .6), VERDE, mix(VERDE, VERDE_CLARO, .3)])

def olho(u, v):
    """Olho neutro da ficha: mais largo que alto, pálpebra de cima pesada e reta (verde-escura com fio preto)
    cobrindo o terço de cima, cílios no canto de fora, íris rosa, pupila e brilho branco no canto de cima."""
    ru, rv = 1.36, 1.0
    corte = rv * (0.3 + 0.1 * (u / ru))                 # linha da pálpebra, um pouco mais baixa para o bico
    # cílios: 3 riscos no canto de fora (para trás), subindo e abrindo
    for k, (a0, ang, comp) in enumerate(((0.62, 62, 0.55), (0.86, 40, 0.6), (1.05, 18, 0.5))):
        bx, by = a0 * ru, rv * (0.3 + 0.1 * a0) + 0.08 - 0.06 * k
        dx, dy = u - bx, v - by
        t = dx * math.cos(math.radians(ang)) + dy * math.sin(math.radians(ang))
        n = -dx * math.sin(math.radians(ang)) + dy * math.cos(math.radians(ang))
        if 0 <= t <= comp and abs(n) < 0.12 - 0.12 * t: return PRETO
    e = (u / ru) ** 2 + (v / rv) ** 2
    if e <= 1.12 and corte - 0.05 <= v <= corte + 0.17: return PRETO                       # fio da pálpebra
    if e <= 1.0 and v > corte + 0.17: return tom(VERDE, -0.25)                             # pálpebra verde-escura
    if ru * 0.88 < u < ru * 1.18 and abs(v - corte) < 0.1: return PRETO                    # rabinho do delineado
    if e > 1: return None
    iu, iv = u / ru + 0.16, v / rv + 0.05
    di = (iu / 0.46) ** 2 + (iv / 0.62) ** 2
    if ((iu + 0.12) / 0.13) ** 2 + ((iv - 0.2) / 0.16) ** 2 <= 1: return (255, 255, 255)
    if (iu / 0.2) ** 2 + (iv / 0.3) ** 2 <= 1: return (54, 6, 36)
    if di <= 1:
        cor = mix((246, 96, 170), MAGENTA, clamp((0.3 - iv) / 1.0))
        if di > 0.7: cor = MAGENTA_ESC
        return cor
    if e > 0.82: return (190, 180, 192)
    return mix(BRANCO, (222, 212, 224), clamp((corte - v) / 1.4))

def mat_faceta(lado):
    base = mat_cor(cor_cabeca, borda=.03, curva=.3)
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            cor = olho(z - FAC_C[1] - OLHO_U, y - OLHO_Y)
            if cor is not None: return cor
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face == "down": return LARANJA_BICO_ESC
    if face in ("east", "west") and abs(z + 5.55) < 0.22 and abs(y - 27.05) < 0.16: return MARROM   # narina
    if face == "up": return mix(LARANJA_BICO_CLARO, LARANJA_BICO, clamp((-z - 4.5) / 2.2))
    if 25.9 < y < 26.06: return (140, 64, 12)                                                       # linha da boca
    if face == "north": return mix(LARANJA_BICO_CLARO, LARANJA_BICO, clamp((27.6 - y) / 2.0))
    return mix(LARANJA_BICO, LARANJA_BICO_ESC, clamp((-z - 5.0) / 1.8) * 0.6)

def cabeca_ossos():
    cab = []
    mc = mat_cor(cor_cabeca, borda=.03, curva=.3)
    fx = (CAB_Y0, CAB_Y1)
    # crânio arredondado (quinas em 2 degraus), mais largo atrás e afinando para a frente
    cab += g.arredondado2("cranio", [-SX, CAB_Y0, SZ - 0.6], [SX, CAB_Y1, 3.4], mc, r=1.1, faixa=fx, res=4)
    cab += g.arredondado("cranio_frente", [-FX - 0.05, CAB_Y0 + 0.2, FZ], [FX + 0.05, CAB_Y1 - 0.3, SZ + 0.2], mc, r=0.45, faixa=fx, res=4)
    ang = math.degrees(math.atan2(SX - FX, SZ - FZ))          # giro da faceta em y (normal de fora = (NX, NZ))
    mbrow = mat_cor(lambda p, f_: VERDE_CLARO if f_ == "up" else tom(VERDE_ESC, 0.15), borda=.15, curva=.2)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, CAB_Y0 + 0.4, cz - FAC_L / 2], [cx + FAC_T / 2, CAB_Y1 - 0.5, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, ang * lado, 0), pivo=(cx, 27.5, cz), faixa=fx, res=8))
        # sobrancelha em V verde-escura: um pedaço na faceta (sobre o olho) e outro na frente, descendo para o meio
        fx0, fx1 = sorted((cx + FAC_T / 2 * lado - 0.05 * lado, cx + FAC_T / 2 * lado + 0.45 * lado))
        cab.append(osso("sobrancelha_" + s, [cx, 29.6, cz], [0, ang * lado, 0], [
            peca("sobrancelha_" + s, [fx0, 29.25, cz - FAC_L / 2 - 0.1], [fx1, 30.05, cz + FAC_L / 2 - 0.2], mbrow,
                 rot=(-9, 0, 0), pivo=(cx, 29.65, cz))]))
        x0, x1 = sorted((0.15 * lado, (FX + 0.15) * lado))
        cab.append(peca("sobrancelha_frente_" + s, [x0, 29.25, FZ - 0.45], [x1, 30.05, FZ + 0.1], mbrow,
                        rot=(0, 0, 17 * lado), pivo=((FX + 0.15) * lado, 29.65, FZ - 0.2)))
        # degrau lima da bochecha, logo abaixo do olho (na faceta)
        bx0, bx1 = sorted((cx + FAC_T / 2 * lado - 0.05 * lado, cx + FAC_T / 2 * lado + 0.14 * lado))
        cab.append(osso("bochecha_" + s, [cx, 26.5, cz], [0, ang * lado, 0], [
            peca("bochecha_" + s, [bx0, 26.0, cz - FAC_L / 2 + 0.15], [bx1, 26.9, cz + FAC_L / 2 - 0.05],
                 mat_cor(lambda p, f_: LIMA if f_ != "down" else CREME, borda=.15, curva=.2))]))
    # bico laranja em cunha: base larga, meio afinando e ponta curvada para baixo; mandíbula de baixo menor
    mb = mat_cor(cor_bico, borda=.05, curva=.3)
    fb = (25.0, 27.8)
    cab.append(peca("bico_base", [-1.25, 25.95, -5.15], [1.25, 27.75, FZ + 0.2], mb, faixa=fb))
    cab.append(peca("bico_meio", [-1.05, 25.95, -6.15], [1.05, 27.4, -5.0], mb, rot=(-13, 0, 0), pivo=(0, 27.4, -5.0), faixa=fb))
    cab.append(peca("bico_ponta", [-0.75, 25.0, -6.7], [0.75, 26.8, -5.8], mb, rot=(-34, 0, 0), pivo=(0, 26.8, -5.8), faixa=fb))
    cab.append(peca("bico_ponta2", [-0.42, 24.55, -6.55], [0.42, 25.3, -5.95], mat_cor(lambda p, f_: LARANJA_BICO_ESC, borda=.1), rot=(-34, 0, 0), pivo=(0, 26.8, -5.8), faixa=fb))
    cab.append(peca("bico_baixo", [-0.8, 25.35, -5.6], [0.8, 25.95, FZ + 0.2], mat_cor(lambda p, f_: LARANJA_BICO_ESC, borda=.12)))
    # barbela: 3 gotas vermelhas curtas de tamanhos diferentes logo abaixo do bico
    mbar = mat_cor(lambda p, f_: mix(VERM_ESC, VERM_CLARO, clamp((p[1] - 23.4) / 2.2)), borda=.14, curva=.4)
    for nome, x0, x1, y0, zf in (("barbela_meio", -0.5, 0.45, 23.55, -5.0), ("barbela_e", 0.45, 1.05, 24.25, -4.85),
                                 ("barbela_d", -1.0, -0.5, 24.6, -4.8)):
        cab.append(peca(nome, [x0, y0, zf], [x1, 25.45, -4.3], mbar, faixa=(23.4, 25.5)))
    # folhas das bochechas e da nuca (emolduram o rosto, apontando para trás e para baixo)
    for k, (phi, y0, L, W, fl, cor) in enumerate([(30, 26.4, 4.0, 3.8, 14, VERDE_CLARO), (62, 27.0, 4.6, 4.0, 12, VERDE)]):
        for lado in (-1, 1):
            x, z = anel(SX - 0.7, 2.6, 0.8, phi, lado)
            cab.append(folha_cone(f"bochecha{k}_{'d' if lado < 0 else 'e'}", (x, y0, z), phi, fl, L, W, cor, lado, varre=24, esp=0.45))
    # crista foliar: lâminas vermelhas largas que nascem no alto da testa e são penteadas para trás e para baixo
    crista = []
    crista.append(peca("crista_ponta_testa", [-0.85, 29.0, FZ - 0.35], [0.85, 30.7, FZ + 0.6],
                       mat_cor(lambda p, f_: VERM_CLARO if f_ in ("up", "north") else VERMELHO, borda=.2, curva=.3),
                       rot=(0, 0, 45), pivo=(0, 29.85, FZ)))
    # (comprimento, largura em x, espessura): largas de frente, grossas de perfil
    crista.append(lamina("crista_frente", (0, 30.0, -3.0), (-14, 0, 0),
                         [(2.1, 3.2, 2.6), (2.1, 3.0, 2.5), (2.0, 2.8, 2.3), (2.0, 2.4, 2.0), (1.8, 1.9, 1.7), (1.5, 1.2, 1.4)], 26))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        crista.append(lamina("crista_" + s, (2.0 * lado, 29.9, -2.0), (-4, 0, -8 * lado),
                             [(2.0, 2.6, 2.3), (2.0, 2.4, 2.2), (1.9, 2.1, 2.0), (1.8, 1.7, 1.7), (1.4, 1.1, 1.4)], 25))
        crista.append(lamina("crista_lado_" + s, (3.0 * lado, 29.6, -0.2), (40, 0, -12 * lado),
                             [(2.1, 2.4, 2.2), (2.0, 2.2, 2.0), (1.9, 1.9, 1.7), (1.7, 1.5, 1.4), (1.4, 1.0, 1.3)], 30))
    crista.append(lamina("crista_tras", (0, 30.2, 1.0), (60, 0, 0),
                         [(2.2, 3.0, 2.3), (2.1, 2.8, 2.2), (2.0, 2.4, 2.0), (1.9, 2.0, 1.7), (1.6, 1.5, 1.4), (1.3, 1.0, 1.3)], 26))
    cab.append(osso("crista", [0, 30.4, 0], [0, 0, 0], crista))
    return cab

# ---------------- corpo ----------------
def cor_peito(p, face):
    """Peitilho creme em V (do pescoço até o meio do peito) com bordas em pontas de pena; resto: folhagem."""
    x, y, z = p
    if z < -2.0:
        hw = 0.0 + (y - 13.5) * 0.33
        bico = 0.5 * abs(math.sin(y * 1.9))
        if abs(x) < hw - bico:
            return mix(CREME, (252, 236, 206), clamp((y - 15) / 6))
    return cor_folhagem(p, face)

def mat_peito():
    def f(c):
        cor = cor_peito(c["p"], c["face"])
        return tom(cor, g.contexto_luz(c, borda=0.0, topo=.1, baixo=.25, curva=.4))
    return f

def montar():
    # ---------- cabeça ----------
    i_cab = len(g.PECAS)
    cab = cabeca_ossos()
    g.transformar(i_cab, cab, (0.0, 24.0, -1.0), k=K_CAB, sobe=-0.3)
    cabeca = osso("cabeca", [0, 24.0, -1.0], [0, 0, 0], cab)
    mp = mat_peito()
    pescoco = osso("pescoco", [0, 21.5, -0.5], [-INCLINA, 0, 0], [
        peca("pescoco", [-2.5, 20.5, -3.4], [2.5, 24.8, 1.6], mp, faixa=(14, 26), res=3),
        cabeca])

    corpo = []
    corpo += g.arredondado2("tronco", [-5.4, 10.4, -4.6], [5.4, 22.0, 8.4], mp, r=2.4, faixa=(9, 24), res=3)
    corpo += g.arredondado("peito", [-4.0, 12.6, -5.8], [4.0, 21.6, -3.0], mp, r=1.0, faixa=(9, 24), res=3)
    # peitilho creme: penas-folha em escama, da garganta até o meio do peito (V)
    PEITILHO = [(-1.3, 23.8, -4.6, 14, 3.8, 3.0), (1.3, 23.8, -4.6, 14, 3.8, 3.0),
                (-1.7, 21.8, -5.95, 6, 3.8, 3.0), (0.0, 22.2, -6.0, 6, 4.0, 3.0), (1.7, 21.8, -5.95, 6, 3.8, 3.0),
                (-1.0, 19.4, -6.1, 3, 3.8, 2.8), (1.0, 19.4, -6.1, 3, 3.8, 2.8), (0.0, 17.2, -6.15, 0, 3.6, 2.6)]
    for k, (x, y, z, rx, L, W) in enumerate(PEITILHO):
        corpo.append(folha(f"peitilho{k}", (x, y, z - 0.03 * k), (rx, 0, 0), L, W, CREME if k % 3 else (248, 230, 200), eixo="x", esp=0.4))

    # ---------- plumagem de folhas em anéis ----------
    ANEIS = [  # (y, raio x, raio z, z do centro, abertura, varrida, comprimento, largura, phis)
        (24.0, 3.2, 3.4, -0.6, 22, 6, 4.8, 3.8, [-30, 5, 40, 75]),            # pescoço (hackles)
        (21.4, 5.0, 6.2, 1.6, 11, 8, 5.2, 4.0, [-60, -32, -4, 24, 52, 80]),
        (17.8, 5.6, 7.0, 1.8, 9, 10, 5.6, 4.2, [-68, -42, -16, 10, 36, 62, 88]),
        (15.0, 5.6, 6.8, 1.8, 10, 6, 5.8, 4.4, [-76, -50, -24, 2, 28, 54, 80]),  # saia
    ]
    n = 0
    for f_, (y0, ax, az, zc, fl, va, L, W, phis) in enumerate(ANEIS):
        for lado in (-1, 1):
            s = "d" if lado < 0 else "e"
            for k, phi in enumerate(phis):
                x, z = anel(ax, az, zc, phi, lado)
                cor = VERDES[(n * 3 + k) % len(VERDES)]; n += 1
                corpo.append(folha_cone(f"plum{f_}{k}_{s}", (x, y0 - 0.35 * (k % 2), z), phi, fl, L * (0.92 + 0.12 * (k % 2)), W, cor, lado, varre=va, esp=0.45))
    # folhas da frente, dos lados do peitilho e da barriga (escondem as quinas do peito)
    FRENTE = [(20.8, 3.5, -5.85, -72, 4.4, 3.4, VERDE_CLARO), (17.6, 3.0, -5.9, -78, 4.8, 3.6, VERDE),
              (14.4, 2.0, -5.95, -84, 5.0, 3.8, LIMA), (20.0, 4.8, -4.4, -58, 4.8, 3.6, VERDE)]
    for k, (y0, x, z, phi, L, W, cor) in enumerate(FRENTE):
        for lado in (-1, 1):
            corpo.append(folha_cone(f"frente{k}_{'d' if lado < 0 else 'e'}", (x * lado, y0, z), phi, 6, L, W, cor, lado, varre=-6, esp=0.4))
    corpo.append(folha("barriga", (0, 13.4, -6.0), (-6, 0, 0), 5.0, 3.8, VERDE_CLARO, eixo="x", esp=0.4))
    # nuca e costas no meio
    corpo.append(folha_cone("plum_costas0", (0, 22.8, 4.0), 90, 26, 4.8, 3.2, VERDE, 1, varre=10))
    corpo.append(folha_cone("plum_costas1", (0, 20.2, 8.0), 90, 20, 5.0, 3.4, VERDE_CLARO, 1, varre=14))

    # ---------- asas dobradas: massa de escamas de folha + folhas soltas na beirada, flor grande no ombro ----------
    ASA = [  # folhas da beirada de baixo/trás (saem de dentro da massa): (y raiz, z raiz, varrida, comprimento, largura, abertura, cor)
        (16.6, -0.8, 18, 5.8, 4.4, 10, mix(VERDE_CLARO, LIMA, .5)), (16.8, 1.8, 30, 6.4, 4.4, 12, VERDE_CLARO),
        (17.0, 4.4, 42, 6.8, 4.2, 14, mix(VERDE_CLARO, LIMA, .5)), (17.4, 6.8, 54, 6.4, 4.0, 16, VERDE_CLARO),
    ]
    masa = mat_cor(lambda p, f_: cor_folhagem(p, f_, zc=1.0, linha=1.7, coluna=1.9, topo=23.0,
                                              paleta=[VERDE_CLARO, LIMA, mix(VERDE_CLARO, LIMA, .5), VERDE_CLARO, mix(VERDE, VERDE_CLARO, .6)]),
                   borda=0.0, topo=.08, baixo=.2, curva=.3)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = []
        x0, x1 = sorted((4.9 * lado, 6.7 * lado))
        asa.append(osso("asa_massa_" + s, [5.8 * lado, 21.0, -2.0], [14, 0, 4 * lado],
                        g.arredondado2("asa_massa_" + s, [x0, 14.2, -2.6], [x1, 21.4, 8.0], masa, r=0.85, faixa=(13, 23), res=3)))
        for k, (y0, z0, va, L, W, fl, cor) in enumerate(ASA):
            asa.append(folha_cone(f"asa{k}_{s}", (6.0 * lado, y0 - 0.4 * k * 0, z0), 0, fl, L, W, cor, lado, varre=va))
        asa.append(flor("flor_ombro_" + s, (7.1 * lado, 19.6, -1.2), (0, -40 * lado, 0), 3.1))
        corpo.append(osso("asa_" + s, [5.2 * lado, 21.0, 0.0], [0, 0, 0], asa))

    # ---------- cauda: dois cipós espinhentos em espiral (um de cada lado), enrolando para dentro ----------
    cauda = []
    A = [0] + [21] * 12 + [30, 38, 44, 48]
    cauda.append(cipo("cipo_a", (-3.0, 17.5, 7.6), (-95, 0, 0), 2.7, [2.8 - 0.075 * k for k in range(len(A))], A,
                      espinhos={2: ["fora"], 5: ["fora"], 8: ["fora"], 11: ["fora"], 14: ["fora"]},
                      flores={4: ("d", 1.9), 9: ("d", 1.8), 15: ("d", 1.5)}))
    B = [0] + [25] * 10 + [34, 40, 46, 50]
    cauda.append(cipo("cipo_b", (3.0, 16.5, 8.0), (-90, 0, 0), 2.5, [2.6 - 0.075 * k for k in range(len(B))], B,
                      espinhos={3: ["fora"], 6: ["fora"], 9: ["fora"], 12: ["fora"]},
                      flores={2: ("e", 1.8), 7: ("e", 1.9), 12: ("e", 1.5)}))
    corpo.append(osso("cauda", [0, 17.0, 7.6], [0, 0, 0], cauda))

    corpo.append(pescoco)
    tronco = osso("corpo", [0, 12.0, 1.0], [INCLINA, 0, 0], corpo)

    # ---------- pernas: coxa verde-escura, canela amarelo-laranja em anéis, pé de 3 dedos + 1 atrás ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 2.7 * lado; zc = 2.0
        pp = []
        def cor_canela(p, f_):
            base = mix(LARANJA, AMARELO, clamp((p[1] - 1.5) / 5.0))
            if f_ not in ("up", "down") and (p[1] - 1.6) % 1.7 < 0.18: base = tom(base, -0.3)   # escamas em anéis
            return base
        mperna = mat_cor(cor_canela, borda=.12, curva=.4)
        mcoxa = mat_cor(lambda p, f_: cor_folhagem(p, f_, zc=zc, linha=1.2, coluna=1.3, topo=12.0,
                                                   paleta=[VERDE_ESC, mix(VERDE_ESC, VERDE, .4), VERDE_ESC]),
                        borda=.0, curva=.3)
        pp += g.octogono("coxa_" + s, [xc - 1.75, 6.8, zc - 1.75], [xc + 1.75, 11.4, zc + 1.75], mcoxa, r=0.6, faixa=(7, 12), res=3)
        pp += g.octogono("canela_" + s, [xc - 1.4, 1.6, zc - 1.4], [xc + 1.4, 7.0, zc + 1.4], mperna, r=0.45, faixa=(0, 8.4), res=3)
        mdedo = mat_cor(lambda p, f_: LARANJA if f_ == "down" else AMARELO, borda=.18, curva=.5)
        for nome, giro, dx in (("meio", 0, 0), ("fora", -20 * lado, 1.3 * lado), ("dentro", 20 * lado, -1.3 * lado)):
            x0, z0 = xc + dx, zc - 0.6
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - .9, 0, z0 - 3.9], [x0 + .9, 1.8, z0 + 0.6], mdedo, faixa=(0, 1.8)),
                peca(f"unha_{nome}_{s}", [x0 - .6, 0, z0 - 4.7], [x0 + .6, 1.2, z0 - 3.8], mat_cor(lambda p, f_: LARANJA, borda=.2), faixa=(0, 1.8))]))
        pp.append(peca("dedo_tras_" + s, [xc - .6, 0, zc + 0.6], [xc + .6, 1.3, zc + 2.6], mdedo, faixa=(0, 1.8)))
        return osso("perna_" + s, [xc, 10.5, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
