"""Esporocó (#003, Grama): a galoa das plantas tóxicas — um arbusto de folhas-pena grossas em camadas, crista
foliar vermelha em blocos, flores rosas de miolo brilhante nos ombros e UM cipó espinhento grosso que sai do
traseiro e enrola numa espiral grande atrás do corpo."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, mat_cor, na_borda

ID = "esporoco"; NOME = "Esporocó"; NUMERO = 3
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 28.0, -7.5), 7.6)
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (da 'Paleta de Cores' da ficha) ----------------
VERDE_ESC = (40, 92, 30); VERDE = (84, 146, 38); VERDE_CLARO = (128, 194, 66); LIMA = (166, 214, 84)
CREME = (240, 216, 172); CREME_ESC = (214, 180, 136)
VERMELHO = (200, 36, 52); VERM_CLARO = (232, 64, 66); VERM_ESC = (140, 20, 40)
ROSA = (236, 92, 162); ROSA_CLARO = (255, 156, 204); MAGENTA = (232, 50, 132); MAGENTA_ESC = (160, 24, 90)
AMARELO = (249, 174, 22); AMARELO_CLARO = (255, 214, 90); LARANJA = (236, 132, 20); MARROM = (134, 83, 16)
PRETO = (22, 14, 20); BRANCO = (250, 246, 242)

# ---------------- folha-pena em BLOCO (corpo grosso + ponta em losango) ----------------
def mat_folha_bloco(cor, y0, L, zc, W, claro_lado=-1):
    """Folha grossa: na face larga, metade clara e metade base (folha dobrada) com nervura clara; raiz um pouco
    mais escura; contorno escuro só nas beiradas compridas e na ponta. Faces da espessura em sombra chapada."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        v = clamp((y0 - y) / max(L, 1e-6))
        if face in ("east", "west"):
            u = (z - zc) / (W / 2)
            base = tom(cor, 0.2) if u * claro_lado > 0 else tom(cor, -0.08)
            if abs(u) < 0.09 and v < 0.85: base = tom(base, 0.2)
            if v < 0.18: base = tom(base, -0.16)
            if c["nome"].endswith("_pt"):
                if na_borda(c): base = tom(base, -0.3)
            elif c["i"] in (0, c["tw"] - 1): base = tom(base, -0.3)
            return base
        if face == "up": return tom(cor, 0.05)
        if face == "down": return tom(cor, -0.45)
        return tom(cor, -0.24)
    return f

def folha_bloco(nome, raiz, phi, lado, L, W, cor, flare=18, varre=0, T=1.1, claro=-1, brilho=False):
    """Folha-pena grossa pendurada da raiz. phi = ângulo em volta do corpo (0 = para fora, -90 = frente,
    +90 = trás); flare abre a ponta para fora; varre puxa a ponta na direção tangente (para trás nos lados)."""
    x, y, z = raiz
    Lb = L - W * 0.36                    # corpo da folha; a ponta (losango mais estreito) faz o degrau e a ponta
    s = W * 0.72 / 1.4142
    m = mat_folha_bloco(cor, y, L, z, W, claro)
    corpo = peca(nome, [x - T / 2, y - Lb, z - W / 2], [x + T / 2, y, z + W / 2], m, res=2, brilho=brilho)
    ponta = peca(nome + "_pt", [x - T / 2 + 0.03, y - Lb - s / 2, z - s / 2], [x + T / 2 - 0.03, y - Lb + s / 2, z + s / 2], m,
                 rot=(45, 0, 0), pivo=(x, y - Lb, z), res=2, brilho=brilho)
    return osso(nome, list(raiz), [0, -phi * lado, 0], [osso(nome + "_p", list(raiz), [-varre, 0, flare * lado], [corpo, ponta])])

# ---------------- flor tóxica (5 pétalas grossas rosas, miolo amarelo que brilha) ----------------
ROSA_VIVO = (246, 74, 160); ROSA_LUZ = (255, 140, 204)

def mat_petala(R):
    """Pétala grossa: metade clara e metade rosa-viva (dobra), raiz magenta com estames amarelos, ponta com fio
    magenta-escuro; espessura em magenta."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        (x0, y0, z0), (x1, y1, z1) = c["b"]
        pt = c["nome"].endswith("_pt")
        if face == "north":
            u = (x - (x0 + x1) / 2) / max((x1 - x0) / 2, 1e-6)
            base = ROSA_LUZ if u < 0 else ROSA_VIVO
            t = (y - y0) / max(y1 - y0, 1e-6)
            if not pt and t < 0.35:
                base = mix(MAGENTA, base, t / 0.35)
                if abs(u) < 0.5 and 0.08 < t < 0.3 and c["i"] % 2 == 0: base = AMARELO_CLARO   # estames
            if pt and na_borda(c) and c["j"] < c["th"] // 2: base = tom(MAGENTA, -0.1)
            return base
        if face == "south": return tom(MAGENTA, -0.25)
        return ROSA if face == "up" else MAGENTA
    return f

def flor_grossa(nome, centro, rot, R, T=0.8):
    """Flor de 5 pétalas em bloco (cada uma corpo + ponta em losango, levemente em concha), virada para -z local,
    girada por 'rot'; miolo amarelo saliente que brilha."""
    x, y, z = centro
    filhos = []
    W = R * 0.8; Lb = R * 0.56; s = W / 1.4142
    m = mat_petala(R)
    for k in range(5):
        nk = f"{nome}_p{k}"
        y0 = y + R * 0.1
        pet = [peca(nk, [x - W / 2, y0, z - T / 2], [x + W / 2, y0 + Lb, z + T / 2], m, res=4),
               peca(nk + "_pt", [x - s / 2, y0 + Lb - s / 2, z - T / 2 + 0.03], [x + s / 2, y0 + Lb + s / 2, z + T / 2 - 0.03],
                    m, rot=(0, 0, 45), pivo=(x, y0 + Lb, z), res=4)]
        filhos.append(osso(nk, [x, y, z], [-14, 0, 72 * k + 10], pet))
    mm = R * 0.32
    def miolo(c):
        if c["face"] == "north":
            d = max(abs(c["i"] + 0.5 - c["tw"] / 2) / (c["tw"] / 2), abs(c["j"] + 0.5 - c["th"] / 2) / (c["th"] / 2))
            return mix((255, 252, 210), (255, 200, 60), clamp(d * 1.2 - 0.15))
        return (246, 186, 50)
    filhos.append(peca(nome + "_miolo", [x - mm, y - mm, z - T / 2 - 0.7], [x + mm, y + mm, z + T / 2], miolo, res=6, brilho=True))
    return osso(nome, list(centro), list(rot), filhos)

def mat_flor(R, cx, cy):
    """Flor plana (placa): 5 pétalas pontudas, metade clara, borda magenta, miolo amarelo."""
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
            hw = 0.38 * (0.3 + 0.7 * a / 0.5) if a < 0.5 else 0.38 * max(0.0, (1.0 - a) / 0.5) ** 0.9
            if abs(b) <= hw:
                borda = hw - abs(b)
                if melhor is None or borda > melhor[0]: melhor = (borda, a, b)
        if melhor is None: return None
        borda, a, b = melhor
        cor = ROSA_LUZ if b > 0 else ROSA_VIVO
        if a < 0.34: cor = mix(MAGENTA, cor, a / 0.34)
        if borda < 0.06: cor = tom(MAGENTA, -0.15)
        return cor
    return f

def flor_brilha(c, cor): return cor[0] > 230 and cor[1] > 200 and cor[2] < 160

def flor(nome, centro, rot, R, esp=0.7):
    """Flor plana (pétala é fina na ficha) virada para -z local, com miolo saliente que brilha."""
    x, y, z = centro
    m = R * 0.22
    return osso(nome, list(centro), list(rot), [
        peca(nome + "_petalas", [x - R, y - R, z - esp / 2], [x + R, y + R, z + esp / 2], mat_flor(R, x, y), res=6, brilho=flor_brilha),
        peca(nome + "_miolo", [x - m, y - m, z - esp / 2 - 0.4], [x + m, y + m, z], lambda c: (255, 226, 110) if c["face"] == "north" else (240, 180, 50),
             res=4, brilho=True)])

# ---------------- cipó espinhento (UMA cadeia grossa em espiral) ----------------
def mat_cipo(c):
    """Cipó verde em blocos: face de fora mais clara, juntas escuras a cada bloco, 3 tons chapados."""
    face = c["face"]; x, y, z = c["p"]
    if face == "down": base = mix(VERDE, VERDE_CLARO, 0.35)          # (-y local = lado de fora da espiral)
    elif face == "up": base = VERDE_ESC
    elif face in ("north", "south"): base = mix(VERDE_ESC, VERDE, 0.5)
    else:
        (_, y0, _), (_, y1, _) = c["b"]
        t = (y - y0) / max(y1 - y0, 1e-6)
        base = mix(VERDE, VERDE_CLARO, 0.25) if t < 0.5 else mix(VERDE_ESC, VERDE, 0.6)
    (_, _, z0), (_, _, z1) = c["b"]
    if face in ("up", "down", "east", "west"):
        q = (z - z0) / max(z1 - z0, 1e-6)
        if abs(q - 0.5) < 0.04: base = tom(base, -0.22)                # junta no meio do bloco
    if na_borda(c): base = tom(base, -0.3)
    return base

def mat_espinho(c):
    face = c["face"]; y = c["p"][1]
    y0, y1 = c["faixa"]
    t = clamp((y - y0) / max(y1 - y0, 1e-6))
    base = mix((222, 214, 160), (250, 240, 206), t / 0.6)
    if t > 0.8: base = mix(base, (246, 170, 190), (t - 0.8) / 0.2)
    if face in ("east", "south"): base = tom(base, -0.16)
    if face == "down": base = tom(base, -0.3)
    if na_borda(c): base = tom(base, -0.15)
    return base

def espinho(nome, base, rot, L=2.6, W=1.1):
    """Espinho cônico creme: 3 blocos girados 45° que afinam até a ponta, apontando para +y local."""
    x, y, z = base
    fx = (y, y + L)
    filhos = []
    for k, (f0, f1, fw) in enumerate(((-0.25, 0.45, 1.0), (0.4, 0.75, 0.66), (0.7, 1.0, 0.34))):
        w = W * fw
        filhos.append(peca(f"{nome}_{k}", [x - w / 2, y + L * f0, z - w / 2], [x + w / 2, y + L * f1, z + w / 2], mat_espinho,
                           rot=(0, 45, 0), pivo=(x, y, z), faixa=fx, res=4))
    return osso(nome, list(base), list(rot), filhos)

def cipo(nome, base, rot0, comps, larguras, curvas, espinhos=None, flores=None, folhas=None):
    """Cipó: segmentos (ossos '<nome>_k') que crescem em +z local e dobram 'curvas[k]' graus em x a cada junta
    (negativo = para cima). espinhos = {k: [direção]} ('fora' = -y local, o lado convexo da espiral;
    'd' = -x, 'e' = +x); flores = {k: (lado, R)}; folhas = {k: lado}."""
    espinhos = espinhos or {}; flores = flores or {}; folhas = folhas or {}
    def seg(k, pos):
        w = larguras[k]; L = comps[k]
        px, py, pz = pos
        cprox = curvas[min(k + 1, len(curvas) - 1)]
        cprox = cprox[0] if isinstance(cprox, tuple) else cprox
        ov = 0.55 * w * math.tan(math.radians(max(abs(cprox), 10)) / 2) + 0.15
        filhos = [peca(f"{nome}_{k}", [px - w / 2, py - w / 2, pz - ov], [px + w / 2, py + w / 2, pz + L], mat_cipo, res=2)]
        for j, d in enumerate(espinhos.get(k, [])):
            zc = pz + L * 0.5
            rot = {"fora": (180, 0, 0), "e": (0, 0, -70), "d": (0, 0, 70)}[d]
            off = {"fora": (0, -w / 2 + 0.1, 0), "e": (w / 2 - 0.2, 0, 0), "d": (-w / 2 + 0.2, 0, 0)}[d]
            filhos.append(espinho(f"{nome}_esp{k}_{j}", (px + off[0], py + off[1], zc + off[2]), rot,
                                  L=2.6 + 0.6 * w / 2, W=1.2 + 0.3 * w / 2))
        if k in flores:
            d, R = flores[k]
            sx = 1 if d == "e" else -1
            filhos.append(flor(f"{nome}_flor{k}", (px + sx * (w / 2 + 0.3), py, pz + L / 2), (0, -90 * sx, 0), R))
        if k in folhas:
            sx = folhas[k]
            filhos.append(folha_bloco(f"{nome}_folha{k}", (px + sx * w * 0.3, py - w * 0.3, pz + L * 0.4), 0, sx, 4.2, 2.6,
                                      VERDE_CLARO, flare=35, varre=-20, T=0.8))
        if k + 1 < len(larguras): filhos.append(seg(k + 1, (px, py, pz + L)))
        ck = curvas[k] if isinstance(curvas[k], tuple) else (curvas[k], 0)
        return osso(f"{nome}_{k}", list(pos), list(rot0) if k == 0 else [ck[0], ck[1], 0], filhos)
    return seg(0, tuple(base))

# ---------------- crista foliar (lâminas grossas vermelhas em blocos sobrepostos) ----------------
def mat_crista(c0, c1, ei, inv, k=0.0):
    """Lâmina da crista em blocos sobrepostos: a cada ~2,6 unidades de comprimento um degrau (fio escuro embaixo,
    faixa clara em cima do bloco seguinte); 2 tons na face larga (beirada da frente clara). k muda o tom da lâmina."""
    V, VC, VE = tom(VERMELHO, k), tom(VERM_CLARO, k), tom(VERM_ESC, k)
    def f(c):
        face = c["face"]; x, y, z = c["p"]
        (x0, y0, z0), (x1, y1, z1) = c["b"]
        if face == "up": return VC
        if face == "down": return VE
        d = (y - y0) % 2.6
        if face in ("east", "west"):
            q = (z - z0) / max(z1 - z0, 1e-6)
            base = VC if q < 0.4 else V
        elif face == "north": base = mix(V, VC, 0.5)
        else: base = tom(V, -0.18)
        if d < 0.3: base = tom(base, -0.28)                                 # degrau escuro entre os blocos
        elif d > 2.15: base = tom(base, 0.12)                               # topo claro do bloco
        if face not in ("up", "down") and c["i"] in (0, c["tw"] - 1): base = tom(base, -0.3)
        return base
    return f

def lamina(nome, base, rot0, curva, segs):
    """segs = [(comprimento, largura x, espessura z)]: cadeia de blocos que cresce em +y e dobra 'curva'."""
    return g.pena_curva(nome, base, [(L, w, h, VERMELHO, VERMELHO) for L, w, h in segs], rot0, curva, "y", mat_crista, res=3)

def lamina_reta(nome, raiz, rot, L, w, h, ponta="x", k=0.0):
    """Lâmina reta da crista: bloco grosso (w em x, h em z) que cresce em +y a partir da raiz e termina numa
    ponta em losango (ponta='x': pontuda de perfil; 'z': pontuda de frente)."""
    x, y, z = raiz
    m = mat_crista(None, None, 1, False, k)
    lado = h if ponta == "x" else w
    Lb = L - lado * 0.5; q = lado / 1.4142
    corpo = peca(nome, [x - w / 2, y - 0.6, z - h / 2], [x + w / 2, y + Lb, z + h / 2], m, res=3)
    if ponta == "x":
        pt = peca(nome + "_pt", [x - w / 2 + 0.03, y + Lb - q / 2, z - q / 2], [x + w / 2 - 0.03, y + Lb + q / 2, z + q / 2], m,
                  rot=(45, 0, 0), pivo=(x, y + Lb, z), res=3)
    else:
        pt = peca(nome + "_pt", [x - q / 2, y + Lb - q / 2, z - h / 2 + 0.03], [x + q / 2, y + Lb + q / 2, z + h / 2 - 0.03], m,
                  rot=(0, 0, 45), pivo=(x, y + Lb, z), res=3)
    return osso(nome, list(raiz), list(rot), [corpo, pt])

# ---------------- cabeça ----------------
CAB_Y0, CAB_Y1 = 24.2, 31.8
ZF = -10.6                       # frente da cara (onde nasce o bico)
FRENTE_X = 1.45                  # meia largura da frente estreita
FAC_ANG = 50                     # giro da faceta do olho em y (normal 40° fora da frente)
FAC_L, FAC_T = 5.0, 1.8
LX = FRENTE_X + FAC_L * math.sin(math.radians(FAC_ANG))     # meia largura da cabeça
_tx, _tz = math.sin(math.radians(FAC_ANG)), math.cos(math.radians(FAC_ANG))
_nx, _nz = math.cos(math.radians(FAC_ANG)), -math.sin(math.radians(FAC_ANG))
FAC_S = (FRENTE_X + _tx * FAC_L / 2, ZF + _tz * FAC_L / 2)  # centro da superfície da faceta (lado +x)
FAC_C = (FAC_S[0] - _nx * FAC_T / 2, FAC_S[1] - _nz * FAC_T / 2)
ZL = ZF + _tz * FAC_L                                         # onde a faceta encontra o lado da cabeça
OLHO_Y = 28.0
LARANJA_BICO = (244, 166, 32); LARANJA_BICO_CLARO = (255, 204, 84); LARANJA_BICO_ESC = (214, 120, 18)

def olho(u, v):
    """Olho neutro da ficha: amendoado, mais largo que alto; pálpebra de cima com fio preto grosso descendo para o
    bico, cílios no canto de trás, íris magenta grande olhando para a frente, esclera branca com sombra lilás."""
    ru, rv = 2.05, 1.3
    corte = rv * (0.5 + 0.2 * (u / ru))                 # linha da pálpebra (mais baixa para o bico)
    for k, (a0, ang, comp) in enumerate(((0.5, 72, 0.75), (0.75, 50, 0.85), (0.97, 28, 0.8))):
        bx = a0 * ru; by = rv * (0.5 + 0.2 * a0) + 0.12
        dx, dy = u - bx, v - by
        t = dx * math.cos(math.radians(ang)) + dy * math.sin(math.radians(ang))
        n = -dx * math.sin(math.radians(ang)) + dy * math.cos(math.radians(ang))
        if 0 <= t <= comp and abs(n) < 0.19 - 0.15 * t / comp: return PRETO
    # formato amendoado: canto da frente pontudo (para o bico), de trás arredondado
    uu = u / ru
    vv = v / (rv * (1.0 - 0.35 * max(0.0, -uu) ** 1.5))
    e = uu ** 2 + vv ** 2
    if e <= 1.22 and corte - 0.05 <= v <= corte + 0.4: return PRETO                         # fio grosso da pálpebra
    if ru * 0.85 < u < ru * 1.25 and corte - 0.05 < v < corte + 0.22: return PRETO          # rabinho do delineado
    if v > corte + 0.4: return None
    if e > 1: return None
    if e > 0.86 and v < 0: return (60, 30, 50)                                               # fio de baixo
    iu, iv = u / ru + 0.12, v / rv + 0.05
    di = (iu / 0.4) ** 2 + (iv / 0.72) ** 2
    if ((iu + 0.12) / 0.11) ** 2 + ((iv - 0.18) / 0.16) ** 2 <= 1: return (255, 255, 255)
    if (iu / 0.17) ** 2 + (iv / 0.34) ** 2 <= 1: return (60, 6, 40)
    if di <= 1:
        cor = mix((250, 96, 150), (206, 26, 84), clamp((0.35 - iv) / 0.9))     # íris vermelho-magenta
        if di > 0.72: cor = (130, 14, 60)
        return cor
    if v > corte - 0.22: return (214, 200, 222)                                             # sombra lilás sob a pálpebra
    return BRANCO

def cor_cabeca(p, face):
    x, y, z = p
    if face == "down": return CREME if z < ZF + 2.5 and abs(x) < 2.6 else VERDE
    if face == "up": return VERDE_CLARO
    return mix(VERDE, VERDE_CLARO, 0.45)

def mat_faceta(lado):
    base = mat_cor(cor_cabeca, borda=.0, curva=.25)
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        u = z - FAC_C[1]
        if c["face"] == fora:
            cor = olho(u, y - OLHO_Y)
            if cor is not None: return cor
            if y < 26.45: return (252, 238, 204) if u < 0.6 else mix(VERDE, VERDE_CLARO, 0.5)   # bochecha creme
        return base(c)
    return f

def mat_folha_cab(cor):
    """Bloco de pena da cabeça: 2 tons chapados (claro em cima/frente, base) e fio escuro nas beiradas."""
    def f(c):
        face = c["face"]
        if face == "up": b = tom(cor, 0.18)
        elif face == "down": b = tom(cor, -0.4)
        elif face in ("east", "west"): b = cor
        else: b = tom(cor, -0.12)
        if na_borda(c): b = tom(b, -0.22)
        return b
    return f

def cor_bico(p, face):
    x, y, z = p
    if face == "down": return LARANJA_BICO_ESC
    if face in ("east", "west") and abs(z - (ZF - 1.4)) < 0.25 and abs(y - 26.7) < 0.2: return MARROM   # narina
    if face == "up": return LARANJA_BICO_CLARO
    if face == "north": return mix(LARANJA_BICO, (226, 150, 90), 0.35)
    return mix(LARANJA_BICO_CLARO, LARANJA_BICO, clamp((27.3 - y) / 1.6))

def cabeca_ossos():
    cab = []
    mc = mat_cor(cor_cabeca, borda=.0, curva=.25)
    fx = (CAB_Y0, CAB_Y1)
    # crânio: bloco largo atrás + frente estreita (a faceta do olho fecha a quina entre os dois)
    cab += g.arredondado("cranio", [-LX, CAB_Y0, ZL - 0.4], [LX, CAB_Y1, -2.6], mc, r=0.6, faixa=fx, res=3)
    cab.append(peca("cranio_frente", [-FRENTE_X - 0.6, CAB_Y0, ZF], [FRENTE_X + 0.6, CAB_Y1 - 0.2, ZL], mc, faixa=fx, res=3))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, CAB_Y0 + 0.1, cz - FAC_L / 2], [cx + FAC_T / 2, CAB_Y1 - 0.25, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, FAC_ANG * lado, 0), pivo=(cx, OLHO_Y, cz), faixa=fx, res=8))
        # sobrancelha: bloco verde grosso por cima do olho, descendo para o bico
        ox0, ox1 = sorted((cx + FAC_T / 2 * lado - 0.3 * lado, cx + FAC_T / 2 * lado + 0.75 * lado))
        cab.append(osso("sobrancelha_" + s, [cx, 30.0, cz], [0, FAC_ANG * lado, 0], [
            peca("sobrancelha_" + s, [ox0, 29.35, cz - FAC_L / 2 - 0.2], [ox1, 30.65, cz + FAC_L / 2 + 0.3],
                 mat_folha_cab(VERDE_CLARO), rot=(-12, 0, 0), pivo=(cx, 30.2, cz), res=3)]))
        # blocos de pena verdes do lado da cabeça (bochecha de trás e nuca), abrindo para fora e para trás
        for k, (y0, z0, L, W, fl, va, cor) in enumerate([(26.6, ZL + 0.6, 3.8, 3.2, 30, 50, VERDE_CLARO),
                                                        (29.6, ZL + 1.6, 4.2, 2.8, 22, 60, mix(VERDE, VERDE_CLARO, .5)),
                                                        (27.6, -3.6, 4.6, 3.0, 26, 66, VERDE)]):
            cab.append(folha_bloco(f"cab_folha{k}_{s}", (LX * lado - 0.2 * lado, y0, z0), 0, lado, L, W, cor, flare=fl, varre=va, T=1.2))
    # bico laranja em cunha: base, meio e ponta curvada; mandíbula de baixo menor
    mb = mat_cor(cor_bico, borda=.06, curva=.3)
    fb = (24.4, 27.6)
    cab.append(peca("bico_cima", [-1.6, 25.4, ZF - 2.6], [1.6, 27.8, ZF + 0.3], mb, rot=(-8, 0, 0), pivo=(0, 27.8, ZF + 0.3), faixa=fb, res=3))
    cab.append(peca("bico_ponta", [-1.3, 24.8, ZF - 3.9], [1.3, 27.1, ZF - 2.3], mb, rot=(-18, 0, 0), pivo=(0, 26.9, ZF - 2.3), faixa=fb, res=3))
    cab.append(peca("bico_baixo", [-1.25, 24.3, ZF - 2.4], [1.25, 25.5, ZF + 0.3], mat_cor(lambda p, f_: LARANJA_BICO_ESC, borda=.12), res=3))
    # barbela: 3 tiras vermelhas penduradas sob o bico
    mbar = mat_cor(lambda p, f_: mix(VERM_ESC, VERM_CLARO, clamp((p[1] - 20.6) / 3.8)), borda=.14, curva=.4)
    for nome, x0, x1, y0 in (("barbela_d", -1.4, -0.5, 21.4), ("barbela_meio", -0.45, 0.45, 20.6), ("barbela_e", 0.5, 1.4, 21.0)):
        cab.append(peca(nome, [x0, y0, ZF - 1.35], [x1, 24.4, ZF - 0.2], mbar, faixa=(20.6, 24.4), res=3))
    # crista foliar: lâminas grossas vermelhas em blocos, da testa para cima e penteadas para trás
    crista = []
    crista.append(peca("crista_testa", [-1.5, 28.9, ZF - 0.45], [1.5, 31.9, ZF + 0.9],
                       mat_cor(lambda p, f_: VERM_CLARO if f_ in ("up", "north") else VERMELHO, borda=.2, curva=.3),
                       rot=(0, 0, 45), pivo=(0, 30.4, ZF + 0.25), res=3))
    # lâmina da frente: sobe inclinada para a frente (por cima do bico) e vira para trás no alto
    # lâminas grossas em leque no meio (de perfil: da frente, inclinada sobre o bico, até a nuca)
    for k, (z, rx, L, h) in enumerate([(-9.4, -28, 6.8, 4.4), (-7.0, -8, 8.2, 4.6), (-4.6, 18, 8.0, 4.6),
                                       (-3.2, 36, 7.8, 4.4), (-2.8, 58, 7.0, 4.2), (-2.6, 82, 5.8, 3.8)]):
        crista.append(lamina_reta(f"crista_c{k}", (0, 30.8 - 0.25 * k, z), (rx, 0, 0), L, 3.2 - 0.1 * k, h, k=0.1 * (k % 2) - 0.05))
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        # asas da crista: abrem para fora (de frente formam a flor-de-lis da ficha)
        for k, (z, rx, rz, L) in enumerate([(-7.8, -8, 34, 6.4), (-4.8, 26, 30, 6.4)]):
            crista.append(lamina_reta(f"crista_l{k}_{s_}", (1.9 * lado, 30.9, z), (rx, 0, -rz * lado), L, 3.4, 3.4, ponta="z",
                                       k=-0.12 * k))
        # crina: lâmina que cai para trás e para fora sobre a nuca (a crista da ficha passa da cabeça)
        crista.append(lamina_reta(f"crista_crina_{s_}", (2.2 * lado, 30.6, -3.4), (92, 0, -26 * lado), 6.0, 3.0, 3.8, k=-0.08))
    cab.append(osso("crista", [0, 31.0, -6.0], [0, 0, 0], crista))
    return cab

# ---------------- espiral da cauda ----------------
CAUDA_RAIZ = (0.0, 13.6, 4.5)     # onde o cipó sai do traseiro
CAUDA_ZB = 15.5                   # z do ponto de baixo da espiral (fim do trecho reto)
CAUDA_A, CAUDA_B = 8.5, 6.7       # semi-eixos da espiral (no plano dela, horizontal e vertical)
CAUDA_GIRO = 38                   # o plano da espiral gira em y: de costas, a volta vira dois arcos "( )"
CAUDA_VOLTAS = 1.45

def espiral_cipo():
    """Calcula os segmentos do cipó: trecho reto saindo do traseiro e uma espiral (elipse que encolhe) no plano
    girado. Devolve (comprimentos, curvas por junta) para cipo()."""
    y0 = CAUDA_RAIZ[1]
    ls = CAUDA_ZB - CAUDA_RAIZ[2]
    comps = [ls / 3] * 3
    cur = [0, 0, 0]
    yc = y0 + CAUDA_B
    def ponto(t):                                   # t em graus a partir do ponto de baixo
        th = math.radians(t - 90)
        f = 1.0 if t < 150 else max(0.28, 1.0 - 0.72 * (t - 150) / (CAUDA_VOLTAS * 360 - 150))
        return (f * CAUDA_A * math.cos(th), yc + f * CAUDA_B * math.sin(th) + (1 - f) * 0.6)
    # amostra densa e corta em segmentos que afinam
    dens = [ponto(t * 0.5) for t in range(int(CAUDA_VOLTAS * 720) + 1)]
    pts = [dens[0]]; alvo = 2.8; acc = 0.0; k = 0
    for a, b in zip(dens, dens[1:]):
        acc += math.dist(a, b)
        if acc >= alvo:
            pts.append(b); acc = 0.0; k += 1
            alvo = max(1.6, 2.9 - 0.055 * k)
    head_ant = 0.0
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        h = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
        d = (h - head_ant + 180) % 360 - 180
        cur.append((-d, CAUDA_GIRO) if i == 0 else -d)
        comps.append(math.dist(a, b)); head_ant = h
    return comps, cur

_COMPS, _CURVAS = espiral_cipo()
N_CIPO = len(_COMPS)
# o cipó da cauda (cadeia 'cipo_k') ondula devagar no plano da espiral
ONDAS = [("cipo", N_CIPO, (1.0, 0.5, 0.3))]

# ---------------- corpo ----------------
def montar():
    cab = cabeca_ossos()
    cabeca = osso("cabeca", [0, 24.5, -6.5], [0, 0, 0], cab)
    mnuc = mat_cor(lambda p, f_: CREME if (f_ == "north" or p[2] < -9.5) and abs(p[0]) < 2.6 else VERDE, borda=.0, curva=.3)
    pescoco = osso("pescoco", [0, 22.0, -6.5], [0, 0, 0], [
        peca("pescoco", [-3.8, 20.0, -10.9], [3.8, 25.0, -3.4], mnuc, faixa=(18, 26), res=2),
        cabeca])

    corpo = []
    mnucleo = mat_cor(lambda p, f_: VERDE_ESC if p[2] > -9.5 else CREME, borda=.0, curva=.4)
    corpo += g.arredondado2("tronco", [-7.6, 9.4, -10.2], [7.6, 17.6, 6.0], mnucleo, r=2.2, faixa=(8, 24), res=2)
    corpo += g.arredondado2("tronco_cima", [-6.0, 14.0, -10.6], [6.0, 22.4, 5.4], mnucleo, r=2.0, faixa=(8, 24), res=2)

    # peitilho creme: folhas em bloco em V, da garganta até o meio do peito
    BIB = [(-1.7, 24.2, -11.0, 4.6, 3.6), (1.7, 24.2, -11.0, 4.6, 3.6),
           (-2.7, 21.4, -11.2, 4.8, 3.6), (0.0, 21.6, -11.35, 5.0, 3.6), (2.7, 21.4, -11.2, 4.8, 3.6),
           (-1.4, 18.6, -11.45, 4.8, 3.4), (1.4, 18.6, -11.45, 4.8, 3.4), (0.0, 16.4, -11.55, 4.6, 3.2)]
    for k, (x, y, z, L, W) in enumerate(BIB):
        cor = (246, 226, 186) if k % 2 == 0 else (238, 212, 168)
        corpo.append(folha_bloco(f"peitilho{k}", (x, y, z), -90, 1, L, W, cor, flare=8, T=1.0, claro=1 if x <= 0 else -1))

    # anéis de folhas-pena grossas em volta do corpo (de cima para baixo: cada anel mais largo, abrindo para fora)
    ANEIS = [  # (y raiz, raio x, raio z, z centro, flare, varre, L, W, phis, cores)
        (24.4, 5.0, 4.4, -6.0, 22, 30, 5.8, 3.6, [-40, -5, 30, 65], [VERDE_CLARO, VERDE, VERDE_CLARO, VERDE]),
        (21.4, 6.2, 8.6, -2.4, 24, 40, 6.6, 4.2, [-62, -30, 0, 30, 58, 84], [LIMA, VERDE_CLARO, LIMA, VERDE_CLARO, VERDE_CLARO, VERDE]),
        (17.4, 8.2, 9.4, -2.2, 24, 34, 6.8, 4.4, [-72, -44, -14, 16, 46, 76], [VERDE, VERDE_CLARO, LIMA, VERDE_CLARO, VERDE, VERDE_CLARO]),
        (13.4, 8.8, 8.0, -1.2, 22, 22, 6.0, 4.4, [-80, -52, -24, 4, 32, 60, 86], [VERDE, mix(VERDE_ESC, VERDE, .5), VERDE, mix(VERDE, VERDE_CLARO, .4), VERDE, mix(VERDE_ESC, VERDE, .5), VERDE_ESC]),
    ]
    for a, (y0, ax, az, zc, fl, va, L, W, phis, cores) in enumerate(ANEIS):
        for lado in (-1, 1):
            s = "d" if lado < 0 else "e"
            for k, phi in enumerate(phis):
                r = math.radians(phi)
                x, z = lado * ax * math.cos(r), zc + az * math.sin(r)
                corpo.append(folha_bloco(f"folha{a}{k}_{s}", (x, y0 - 0.4 * (k % 2), z), phi, lado, L * (0.95 + 0.08 * (k % 2)), W,
                                         cores[k % len(cores)], flare=fl * (0.4 if phi < -60 else 1), varre=va * (0.3 if phi < -60 else 1 if phi < 50 else 0.5)))
    # barriga (abaixo do peitilho): folhas lima/verde-claras apontando para baixo
    for k, (x, y, L, cor) in enumerate([(-2.2, 15.0, 4.6, LIMA), (2.2, 15.0, 4.6, VERDE_CLARO), (0.0, 13.4, 4.2, VERDE_CLARO)]):
        corpo.append(folha_bloco(f"barriga{k}", (x, y, -10.0 + 0.2 * k), -90, 1, L, 3.8, cor, flare=-24, T=1.1))
    # costas no meio
    for k, (y, z, L) in enumerate([(21.6, 5.0, 6.0), (17.6, 7.0, 6.4), (13.6, 7.2, 6.4)]):
        corpo.append(folha_bloco(f"costas{k}", (0, y, z), 90, 1, L, 4.0, VERDE if k % 2 else VERDE_CLARO, flare=24, T=1.1))

    # ---------- ombros: flor grande + folhas largas da asa (osso animável asa_d / asa_e) ----------
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = [flor_grossa("flor_ombro_" + s, (10.0 * lado, 17.4, -4.0), (0, -48 * lado, 0), 3.9)]
        for k, (y0, z0, L, W, cor) in enumerate([(19.6, -1.0, 6.6, 4.2, VERDE_CLARO), (19.2, 2.4, 7.0, 4.2, LIMA)]):
            asa.append(folha_bloco(f"asa{k}_{s}", (7.6 * lado, y0, z0), 10, lado, L, W, cor, flare=30, varre=42, T=1.2))
        corpo.append(osso("asa_" + s, [7.0 * lado, 20.0, -1.0], [0, 0, 0], asa))

    # ---------- cauda: UM cipó grosso que sai do traseiro e enrola numa espiral grande (plano girado ~30°) ----------
    comps, curvas = _COMPS, _CURVAS
    larguras = [3.5 - 1.6 * k / (N_CIPO - 1) for k in range(N_CIPO)]
    cauda = [cipo("cipo", CAUDA_RAIZ, (0, 0, 0), comps, larguras, curvas,
                  espinhos={4: ["fora"], 6: ["fora"], 8: ["fora"], 10: ["fora"], 12: ["fora"], 14: ["fora"], 16: ["fora"],
                            19: ["fora"], 7: ["e"], 11: ["d"], 15: ["e"]},
                  flores={1: ("d", 2.3), 2: ("e", 2.3), 5: ("d", 2.5), 9: ("e", 2.4), 13: ("d", 2.4), 18: ("e", 2.1),
                          22: ("d", 1.9), 23: ("e", 2.2)},
                  folhas={1: -1, 2: 1})]
    # flor no miolo da espiral (a ficha tem flores dentro da volta)
    cauda.append(flor("flor_espiral", (0.0, CAUDA_RAIZ[1] + CAUDA_B + 0.5, CAUDA_ZB), (0, 90, 0), 2.8))
    corpo.append(osso("cauda", list(CAUDA_RAIZ), [0, 0, 0], cauda))

    corpo.append(pescoco)
    tronco = osso("corpo", [0, 9.0, 0.0], [0, 0, 0], corpo)

    # ---------- pernas: coxa verde + penas creme, canela laranja em blocos, pé de 3 dedos grossos + 1 atrás ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 3.3 * lado; zc = 0.0
        pp = []
        def cor_canela(p, f_):
            base = AMARELO if f_ != "down" else LARANJA
            if f_ not in ("up", "down"):
                q = (p[1] - 1.4) % 1.45
                if q < 0.2: base = tom(LARANJA, -0.1)                      # junta entre os blocos
                elif q > 1.0: base = mix(AMARELO, AMARELO_CLARO, 0.5)
            return base
        mperna = mat_cor(cor_canela, borda=.1, curva=.3)
        pp += g.octogono("coxa_" + s, [xc - 1.6, 5.0, zc - 1.6], [xc + 1.6, 9.4, zc + 1.6],
                         mat_cor(lambda p, f_: VERDE_ESC, borda=.12, curva=.3), r=0.5, faixa=(5, 9.4), res=2)
        pp += g.octogono("canela_" + s, [xc - 1.35, 1.2, zc - 1.35], [xc + 1.35, 5.4, zc + 1.35], mperna, r=0.4, faixa=(0, 6), res=3)
        for k, (dx, y0) in enumerate([(-0.9, 11.4), (1.1, 11.2)]):
            pp.append(folha_bloco(f"coxa_pena{k}_{s}", (xc + dx * lado, y0, -3.8), -90, 1, 5.0, 3.2, CREME if k else (246, 226, 186),
                                  flare=8, T=1.0))
        mdedo = mat_cor(lambda p, f_: AMARELO_CLARO if f_ == "up" else (LARANJA if f_ in ("down", "north") else AMARELO), borda=.14, curva=.4)
        for nome, giro, dx, comp in (("meio", 0, 0, 6.2), ("fora", -14 * lado, 1.4 * lado, 5.0), ("dentro", 14 * lado, -1.4 * lado, 5.0)):
            x0, z0 = xc + dx, zc - 0.4
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - .85, 0, z0 - comp], [x0 + .85, 1.8, z0 + 0.6], mdedo, faixa=(0, 1.8), res=2)]))
        pp.append(peca("dedo_tras_" + s, [xc - .8, 0, zc + 0.6], [xc + .8, 1.4, zc + 3.4], mdedo, faixa=(0, 1.5), res=2))
        return osso("perna_" + s, [xc, 9.0, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
