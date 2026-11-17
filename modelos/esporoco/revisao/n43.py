"""Esporocó (#003, Grama): a galoa das plantas tóxicas — um arbusto de folhas-pena grossas em camadas, crista
foliar vermelha em blocos, flores rosas de miolo brilhante nos ombros e UM cipó espinhento grosso que sai do
traseiro e enrola numa espiral grande atrás do corpo."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, clamp, na_borda

ID = "esporoco"; NOME = "Esporocó"; NUMERO = 3
ALTURA = 2.45
QUADRUPEDE = False
ROSTO = ((0, 28.0, -7.5), 7.6)
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (amostrada com PIL nos PNGs da ficha; veja modelos/esporoco/detalhes.md) ----------------
VERDE_ESC = (46, 86, 12); VERDE = (88, 136, 18); VERDE_CLARO = (132, 188, 50); LIMA = (156, 200, 62)
SOMBRA_FOLHA = (20, 38, 10)                                    # vão escuro entre as folhas
CREME = (248, 204, 122); CREME_ESC = (222, 168, 92); CREME_CLARO = (251, 222, 168)
VERMELHO = (220, 26, 30); VERM_CLARO = (240, 44, 40); VERM_ESC = (156, 14, 26)
ROSA = (240, 70, 128); ROSA_CLARO = (252, 120, 166); MAGENTA = (226, 40, 112); MAGENTA_ESC = (150, 18, 70)
AMARELO = (240, 150, 16); AMARELO_CLARO = (252, 182, 44); LARANJA = (210, 122, 14); MARROM = (134, 83, 16)
PRETO = (22, 14, 20); BRANCO = (246, 228, 216)

LUZ_QUENTE = (255, 248, 214)
def tom(c, f):
    """Luz da ficha: f > 0 clareia para a luz quente; f < 0 só escurece (sem puxar para o roxo: os verdes da
    ficha continuam amarelados na sombra)."""
    f = clamp(f, -1, 1)
    if f >= 0: return mix(c, LUZ_QUENTE, f * 0.4)
    k = 1 + f * 0.65
    return tuple(int(round(v * k)) for v in c)

def claro(c, f):
    """Clareia multiplicando (mantém a saturação da ficha, sem lavar para o branco)."""
    return tuple(min(255, int(round(v * (1 + f)))) for v in c)

def mat_cor(cor_fn, **kw):
    """Como galo_base.mat_cor, mas com a sombra desta espécie (tom acima)."""
    def f(c):
        base = cor_fn(c["p"], c["face"])
        return None if base is None else tom(base, g.contexto_luz(c, **kw))
    return f

# ---------------- folha-pena em BLOCO (corpo grosso + ponta em losango) ----------------
def mat_folha_bloco(cor, y0, L, zc, W, claro_lado=-1):
    """Folha grossa: na face larga, metade clara e metade base (folha dobrada) com nervura clara; raiz um pouco
    mais escura; contorno escuro só nas beiradas compridas e na ponta. Faces da espessura em sombra chapada."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        v = clamp((y0 - y) / max(L, 1e-6))
        if face in ("east", "west"):
            u = (z - zc) / (W / 2)
            base = claro(cor, 0.14) if u * claro_lado > 0 else claro(cor, -0.06)
            if abs(u) < 0.09 and v < 0.85: base = claro(base, 0.15)
            if v < 0.18: base = tom(base, -0.16)
            if c["nome"].endswith("_pt"):
                if na_borda(c): base = tom(base, -0.3)
            elif c["i"] in (0, c["tw"] - 1): base = tom(base, -0.3)
            return base
        if face == "up": return tom(cor, 0.05)
        if face == "down": return tom(cor, -0.45)
        return tom(cor, -0.24)
    return f

def folha_bloco(nome, raiz, phi, lado, L, W, cor, flare=18, varre=0, T=0.8, claro=-1, brilho=False):
    """Folha-pena grossa pendurada da raiz. phi = ângulo em volta do corpo (0 = para fora, -90 = frente,
    +90 = trás); flare abre a ponta para fora; varre puxa a ponta na direção tangente (para trás nos lados)."""
    x, y, z = raiz
    Lb = L - W * 0.5                     # corpo da folha; a ponta em losango (da largura toda) faz a ponta de lança
    s = W / 1.4142
    m = mat_folha_bloco(cor, y, L, z, W, claro)
    corpo = peca(nome, [x - T / 2, y - Lb, z - W / 2], [x + T / 2, y, z + W / 2], m, res=2, brilho=brilho)
    ponta = peca(nome + "_pt", [x - T / 2 + 0.03, y - Lb - s / 2, z - s / 2], [x + T / 2 - 0.03, y - Lb + s / 2, z + s / 2], m,
                 rot=(45, 0, 0), pivo=(x, y - Lb, z), res=2, brilho=brilho)
    return osso(nome, list(raiz), [0, -phi * lado, 0], [osso(nome + "_p", list(raiz), [-varre, 0, flare * lado], [corpo, ponta])])

# ---------------- flor tóxica (5 pétalas grossas rosas, miolo amarelo que brilha) ----------------
ROSA_VIVO = (240, 49, 131); ROSA_LUZ = (245, 98, 148); ROSA_BORDA = (196, 30, 100)
MIOLO = (255, 228, 90); MIOLO_CENTRO = (255, 246, 176); ESTAME = (255, 210, 58)

def mat_petala(R):
    """Pétala grossa (quadro "Flor tóxica"): rosa-choque com a faixa do meio mais clara, pontinhos de estame
    amarelos junto do miolo; espessura em rosa mais escuro."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        (x0, y0, z0), (x1, y1, z1) = c["b"]
        pt = c["nome"].endswith("_pt")
        if face in ("north", "south"):                                   # (de costas a flor aparece igual)
            u = (x - (x0 + x1) / 2) / max((x1 - x0) / 2, 1e-6)
            t = (y - y0) / max(y1 - y0, 1e-6)
            base = ROSA_LUZ if abs(u) < 0.34 else ROSA_VIVO
            if not pt and t < 0.4 and abs(u) < 0.6 and (c["i"] + c["j"]) % 3 == 0: base = ESTAME     # estames
            return base
        return ROSA_BORDA
    return f

def miolo_flor(nome, x, y, z0, z1, r):
    """Miolo octogonal (2 blocos, um girado 45°): amarelo brilhante com o centro quase branco."""
    def m(c):
        if c["face"] in ("north", "south"):
            d = math.hypot(c["i"] + 0.5 - c["tw"] / 2, c["j"] + 0.5 - c["th"] / 2) / (c["tw"] / 2)
            return MIOLO_CENTRO if d < 0.45 else MIOLO
        return (240, 190, 50)
    q = r * 0.83
    return [peca(nome, [x - r, y - q, z0], [x + r, y + q, z1], m, res=8, brilho=True),
            peca(nome + "_b", [x - q, y - r, z0 + 0.02], [x + q, y + r, z1 - 0.02], m, res=8, brilho=True)]

def flor_grossa(nome, centro, rot, R, T=0.8):
    """Flor de 5 pétalas em bloco (cada uma corpo + ponta em losango, levemente em concha), virada para -z local,
    girada por 'rot'; miolo amarelo saliente que brilha."""
    x, y, z = centro
    filhos = []
    W = R * 0.6; Lb = R * 0.6; s = W / 1.4142
    m = mat_petala(R)
    for k in range(5):
        nk = f"{nome}_p{k}"
        y0 = y + R * 0.1
        pet = [peca(nk, [x - W / 2, y0, z - T / 2], [x + W / 2, y0 + Lb, z + T / 2], m, res=4),
               peca(nk + "_pt", [x - s / 2, y0 + Lb - s / 2, z - T / 2 + 0.03], [x + s / 2, y0 + Lb + s / 2, z + T / 2 - 0.03],
                    m, rot=(0, 0, 45), pivo=(x, y0 + Lb, z), res=4)]
        filhos.append(osso(nk, [x, y, z], [-14, 0, 72 * k + 10], pet))
    filhos += miolo_flor(nome + "_miolo", x, y, z - T / 2 - 0.6, z + T / 2, R * 0.24)
    return osso(nome, list(centro), list(rot), filhos)

def mat_flor(R, cx, cy):
    """Flor plana (placa): 5 pétalas pontudas, metade clara, borda magenta, miolo amarelo."""
    def f(c):
        x, y, z = c["p"]
        dx, dy = x - cx, y - cy
        r = math.hypot(dx, dy) / R
        if r > 1.0: return None
        if r < 0.1: return MIOLO_CENTRO
        if r < 0.2: return MIOLO
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
        cor = ROSA_LUZ if abs(b) < 0.08 else ROSA_VIVO
        if a < 0.36 and abs(b) < 0.12 and int((x + y) * 6) % 2 == 0: cor = ESTAME          # estames
        if borda < 0.05: cor = ROSA_BORDA
        return cor
    return f

def flor_brilha(c, cor): return cor[0] > 240 and cor[1] > 200 and cor[2] < 180

def flor(nome, centro, rot, R, esp=0.7):
    """Flor plana (pétala é fina na ficha) virada para -z local, com miolo saliente que brilha."""
    x, y, z = centro
    m = R * 0.22
    return osso(nome, list(centro), list(rot), [
        peca(nome + "_petalas", [x - R, y - R, z - esp / 2], [x + R, y + R, z + esp / 2], mat_flor(R, x, y), res=6, brilho=flor_brilha),
        *miolo_flor(nome + "_miolo", x, y, z - esp / 2 - 0.4, z + esp / 2 + 0.4, m)])

# ---------------- cipó espinhento (UMA cadeia grossa em espiral) ----------------
CIPO = (70, 134, 46); CIPO_CLARO = (96, 164, 58); CIPO_ESC = (40, 84, 28); CIPO_JUNTA = (50, 104, 36)
BOTAO = (248, 176, 150)

def mat_cipo(c):
    """Cipó em tijolos (como o quadro "Cauda de cipós"): nas faces do lado, 2 fileiras de blocos com as juntas
    desencontradas (fileira de fora mais clara); face de fora clara, de dentro escura; segmentos alternam o tom."""
    face = c["face"]; x, y, z = c["p"]
    (x0, y0, z0), (x1, y1, z1) = c["b"]
    k = int(c["nome"].rsplit("_", 1)[-1]) if c["nome"].rsplit("_", 1)[-1].isdigit() else 0
    alt = 0.07 if k % 2 else -0.03
    q = (z - z0) / max(z1 - z0, 1e-6)
    if face == "up": base = CIPO_CLARO                                   # (+y local = lado de fora do laço, que é convexo)
    elif face == "down": base = CIPO_ESC
    elif face in ("north", "south"): base = CIPO
    else:
        t = (y - y0) / max(y1 - y0, 1e-6)                                # 1 = lado de fora
        fora = t > 0.5
        base = mix(CIPO, CIPO_CLARO, 0.4) if fora else CIPO
        if abs(t - 0.5) < 0.05: return CIPO_JUNTA                        # junta suave entre as fileiras
        jq = 0.5 if fora else 0.0                                        # juntas desencontradas
        if min(abs(q - jq), abs(q - jq - 1), abs(q - jq + 1)) < 0.04: return CIPO_JUNTA
    if face in ("up", "down") and abs(q - 0.5) < 0.04: return CIPO_JUNTA
    base = tom(base, alt)
    if na_borda(c): base = tom(base, -0.15)
    return base

def mat_espinho(c):
    face = c["face"]; y = c["p"][1]
    y0, y1 = c["faixa"]
    t = clamp((y - y0) / max(y1 - y0, 1e-6))
    base = mix((206, 186, 120), (240, 210, 150), t / 0.6)
    if t > 0.75: base = mix(base, (247, 150, 149), (t - 0.75) / 0.25)
    if face in ("east", "south"): base = tom(base, -0.16)
    if face == "down": base = tom(base, -0.3)
    if na_borda(c): base = tom(base, -0.15)
    return base

ESPINHO = (239, 212, 169); ESPINHO_CLARO = (246, 230, 190); ESPINHO_ROSA = (245, 176, 176)

def mat_espinho_placa(y0, L, W, eixo, centro, sombra, rosa):
    """Cone do espinho em placa (triângulo): creme liso, um lado um pouco mais escuro (volume) e, em 1/3 deles,
    a ponta rosada (como na traseira da ficha)."""
    def f(c):
        x, y, z = c["p"]
        v = (y - y0) / L
        u = ((z if eixo == "z" else x) - centro) / (W / 2)
        if not (0.0 <= v <= 1.0) or abs(u) > (1 - v) * 1.02: return None
        base = mix(ESPINHO, ESPINHO_CLARO, clamp(v / 0.6))
        if rosa and v > 0.62: base = mix(base, ESPINHO_ROSA, clamp((v - 0.62) / 0.2))
        if (u > 0) == sombra: base = tom(base, -0.12)
        return base
    return f

def espinho(nome, base, rot, L=2.6, W=1.1, rosa=False):
    """Espinho cônico liso (quadro "Cauda de cipós"): cone em X de duas placas triangulares (lê como cone de
    todos os lados), creme; aponta para +y local."""
    x, y, z = base
    W = W * 1.6; e = 0.3
    yb = y - 0.3
    Lt = y + L - yb
    return osso(nome, list(base), list(rot), [osso(nome + "_x", list(base), [0, 45, 0], [
        peca(f"{nome}_a", [x - e / 2, yb, z - W / 2], [x + e / 2, y + L, z + W / 2], mat_espinho_placa(yb, Lt, W, "z", z, True, rosa), res=6),
        peca(f"{nome}_c", [x - W / 2, yb, z - e / 2], [x + W / 2, y + L, z + e / 2], mat_espinho_placa(yb, Lt, W, "x", x, False, rosa), res=6)])])

def botao(nome, centro, R=0.9):
    """Botão floral fechado cor de pêssego (traseira da ficha): losango pequeno com a ponta mais clara."""
    x, y, z = centro
    m = mat_cor(lambda p, f_: (246, 188, 160) if p[1] > y else BOTAO, borda=.1, curva=.3)
    return peca(nome, [x - R / 2, y - R, z - R / 2], [x + R / 2, y + R, z + R / 2], m, rot=(0, 45, 0), pivo=(x, y, z), res=4)

def cipo(nome, base, rot0, comps, larguras, curvas, espinhos=None, flores=None, folhas=None, botoes=None):
    """Cipó: segmentos (ossos '<nome>_k') que crescem em +z local e dobram 'curvas[k]' graus em x a cada junta
    (negativo = para cima). espinhos = {k: [direção]} ('fora' = -y local, o lado convexo da espiral;
    'd' = -x, 'e' = +x); flores = {k: (lado, R)}; folhas = {k: lado}."""
    espinhos = espinhos or {}; flores = flores or {}; folhas = folhas or {}; botoes = botoes or {}
    def seg(k, pos):
        w = larguras[k]; L = comps[k]
        px, py, pz = pos
        cprox = curvas[min(k + 1, len(curvas) - 1)]
        cprox = cprox[0] if isinstance(cprox, tuple) else cprox
        ov = 0.55 * w * math.tan(math.radians(max(abs(cprox), 10)) / 2) + 0.15
        filhos = [peca(f"{nome}_{k}", [px - w / 2, py - w / 2, pz - ov], [px + w / 2, py + w / 2, pz + L], mat_cipo, res=2)]
        for j, d in enumerate(espinhos.get(k, [])):
            zc = pz + L * 0.5
            rot = {"fora": (180, 0, 0), "cima": (0, 0, 0), "e": (0, 0, -80), "d": (0, 0, 80)}[d]
            off = {"fora": (0, -w / 2 + 0.1, 0), "cima": (0, w / 2 - 0.1, 0), "e": (w / 2 - 0.2, 0, 0), "d": (-w / 2 + 0.2, 0, 0)}[d]
            filhos.append(espinho(f"{nome}_esp{k}_{j}", (px + off[0], py + off[1], zc + off[2]), rot,
                                  L=2.2 + 0.5 * w / 2, W=1.1 + 0.3 * w / 2, rosa=(k + j) % 3 == 0))
        if k in flores:
            d, R = flores[k]
            sx = 1 if d == "e" else -1
            filhos.append(flor(f"{nome}_flor{k}", (px + sx * (w / 2 + 0.3), py, pz + L / 2), (0, -90 * sx, 0), R))
        if k in folhas:
            sx = folhas[k]
            filhos.append(folha_bloco(f"{nome}_folha{k}", (px + sx * w * 0.3, py - w * 0.3, pz + L * 0.4), 0, sx, 4.2, 2.6,
                                      VERDE_CLARO, flare=35, varre=-20, T=0.8))
        for j, (dx, dy) in enumerate(botoes.get(k, [])):
            filhos.append(botao(f"{nome}_botao{k}_{j}", (px + dx * (w / 2 + 0.5), py + dy * (w / 2 + 0.5), pz + L * 0.5)))
        if k + 1 < len(larguras): filhos.append(seg(k + 1, (px, py, pz + L)))
        ck = curvas[k] if isinstance(curvas[k], tuple) else (curvas[k], 0)
        return osso(f"{nome}_{k}", list(pos), list(rot0) if k == 0 else [ck[0], ck[1], 0], filhos)
    return seg(0, tuple(base))

# ---------------- crista foliar (lâminas grossas vermelhas em blocos sobrepostos) ----------------
def mat_crista(c0, c1, ei, inv, k=0.0):
    """Lâmina da crista em blocos sobrepostos: a cada ~2,6 unidades de comprimento um degrau (fio escuro embaixo,
    faixa clara em cima do bloco seguinte); 2 tons na face larga (beirada da frente clara). k muda o tom da lâmina."""
    V, VC, VE = claro(VERMELHO, k), claro(VERM_CLARO, k), claro(VERM_ESC, k)
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
        elif d > 2.15: base = claro(base, 0.1)                              # topo claro do bloco
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
LARANJA_BICO = (249, 170, 14); LARANJA_BICO_CLARO = (255, 194, 74); LARANJA_BICO_ESC = (224, 138, 16)
BICO_FRENTE = (238, 152, 14)

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
    if ru * 0.8 < u < ru * 1.42 and corte - 0.05 + 0.5 * (u - ru * 0.8) < v < corte + 0.36 + 0.5 * (u - ru * 0.8):
        return PRETO                                                                         # asa do delineado
    if v > corte + 0.4: return None
    if e > 1: return None
    if e > 0.86 and v < 0: return (60, 30, 50)                                               # fio de baixo
    iu, iv = u / ru + 0.12, v / rv + 0.05
    di = (iu / 0.4) ** 2 + (iv / 0.72) ** 2
    if ((iu + 0.12) / 0.11) ** 2 + ((iv - 0.18) / 0.16) ** 2 <= 1: return (255, 255, 255)
    if (iu / 0.15) ** 2 + (iv / 0.36) ** 2 <= 1: return (28, 8, 22)                     # pupila oval vertical
    if di <= 1:
        cor = mix((238, 96, 166), (200, 48, 126), clamp((0.3 - iv) / 0.8))     # íris magenta viva, miolo claro embaixo
        if di > 0.68: cor = (138, 26, 85)                                      # anel escuro
        return cor
    if v > corte - 0.24: return (201, 179, 201)                                            # linha lilás sob a pálpebra
    return (240, 226, 212)

def cor_cabeca(p, face):
    x, y, z = p
    if face == "down": return CREME if z < ZF + 2.5 and abs(x) < 2.6 else VERDE
    if face == "up": return VERDE_CLARO
    if face in ("east", "west") and y < 26.4 and z < ZL + 1.2: return (250, 222, 166)    # faixa creme da bochecha (de perfil)
    if z > ZL + 0.5: return mix(VERDE, VERDE_CLARO, 0.75)                   # lados e nuca mais claros (ficha)
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
            if y < 26.45: return (252, 228, 176) if u < 1.6 else mix(VERDE, VERDE_CLARO, 0.5)   # bochecha creme
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
    if face in ("east", "west") and abs(z - (ZF - 0.8)) < 0.25 and abs(y - 26.8) < 0.2: return MARROM   # narina
    if face == "up": return LARANJA_BICO_CLARO
    if face == "north": return mix(LARANJA_BICO, BICO_FRENTE, 0.25) if y > 25.6 else mix(LARANJA_BICO, BICO_FRENTE, 0.6)
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
        # ponte da viseira: da sobrancelha até o meio da testa, descendo para o centro
        x0, x1 = sorted((0.0, (FRENTE_X + 0.7) * lado))
        cab.append(peca("sobrancelha_ponte_" + s, [x0, 29.3, ZF - 0.5], [x1, 30.5, ZF + 1.0], mat_folha_cab(VERDE_CLARO),
                        rot=(0, 0, 16 * lado), pivo=((FRENTE_X + 0.7) * lado, 29.9, ZF), res=3))
        # costeleta verde-clara sob o olho, abrindo para fora na altura do bico (alarga a base do rosto)
        cab.append(folha_bloco("costeleta_" + s, ((LX - 0.6) * lado, 26.4, ZL - 0.6), -20, lado, 3.6, 2.8, LIMA, flare=55, varre=10, T=1.0))
        # blocos de pena verdes do lado da cabeça (bochecha de trás e nuca), abrindo para fora e para trás
        for k, (y0, z0, L, W, fl, va, cor) in enumerate([(26.6, ZL + 1.4, 3.8, 3.2, 30, 50, VERDE_CLARO),
                                                        (29.6, ZL + 1.6, 4.2, 2.8, 22, 60, mix(VERDE, VERDE_CLARO, .5)),
                                                        (27.6, -3.6, 4.6, 3.0, 26, 66, VERDE)]):
            cab.append(folha_bloco(f"cab_folha{k}_{s}", (LX * lado - 0.2 * lado, y0, z0), 0, lado, L, W, cor, flare=fl, varre=va, T=1.2))
    # bico laranja em cunha: base, meio e ponta curvada; mandíbula de baixo menor
    mb = mat_cor(cor_bico, borda=.06, curva=.3)
    fb = (24.4, 27.6)
    # de frente: cunha em V que estreita para baixo (base cheia -> 2/3 -> 1/3); de lado projeta ~1/3 da cabeça
    cab.append(peca("bico_base", [-1.45, 25.4, ZF - 1.3], [1.45, 27.6, ZF + 0.3], mb, faixa=fb, res=4))
    cab.append(peca("bico_meio", [-0.98, 25.2, ZF - 2.3], [0.98, 27.2, ZF - 1.1], mb, rot=(-8, 0, 0), pivo=(0, 27.2, ZF - 1.1), faixa=fb, res=4))
    cab.append(peca("bico_ponta", [-0.5, 24.7, ZF - 3.0], [0.5, 26.6, ZF - 2.0], mb, rot=(-16, 0, 0), pivo=(0, 26.6, ZF - 2.0), faixa=fb, res=4))
    cab.append(peca("bico_baixo", [-0.9, 24.4, ZF - 1.7], [0.9, 25.45, ZF + 0.3], mat_cor(lambda p, f_: LARANJA_BICO_ESC, borda=.1), res=4))
    # barbela: 2 lóbulos vermelhos grossos lado a lado, presos logo sob o bico (cada um ~metade da largura do bico)
    mbar = mat_cor(lambda p, f_: mix((142, 26, 40), (196, 36, 52), clamp((p[1] - 20.8) / 2.6)), borda=.12, curva=.3)
    for lado in (-1, 1):
        x0, x1 = sorted((0.05 * lado, 1.4 * lado))
        cab += g.arredondado("barbela_" + ("d" if lado < 0 else "e"), [x0, 20.9, ZF - 1.9], [x1, 24.5, ZF - 0.4], mbar, r=0.4,
                             faixa=(20.9, 24.5), res=4)
    # crista foliar: lâminas grossas vermelhas em blocos, da testa para cima e penteadas para trás
    crista = []
    crista.append(peca("crista_testa", [-1.05, 29.35, ZF - 0.5], [1.05, 31.45, ZF + 0.9],
                       mat_cor(lambda p, f_: VERM_CLARO if f_ in ("up", "north") else VERMELHO, borda=.2, curva=.3),
                       rot=(0, 0, 45), pivo=(0, 30.4, ZF + 0.25), res=3))
    # lâminas do meio: finas (1,3 de espessura), em pares desencontrados em x (de frente formam o lobo central),
    # varridas 10° a 120° para trás; as de trás descem pela nuca até a altura do olho
    for k, (x, z, rx, L, h) in enumerate([(-0.65, -9.2, 10, 7.6, 3.2), (0.65, -8.0, 22, 8.6, 3.4), (-0.65, -6.4, 34, 9.2, 3.4),
                                          (0.65, -4.8, 48, 9.0, 3.2), (-0.65, -3.4, 66, 8.4, 3.0), (0.65, -2.6, 92, 7.0, 2.8),
                                          (-0.65, -2.4, 116, 6.6, 2.6)]):
        crista.append(lamina_reta(f"crista_c{k}", (x, 30.9 - 0.08 * k, z), (rx, 0, 0), L, 1.35, h, k=0.08 * (k % 2) - 0.04))
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        # lobos dos lados: lâminas largas de frente e finas de perfil, abrindo para fora e varridas para trás
        for k, (z, rx, rz, L) in enumerate([(-7.6, 6, 30, 6.4), (-5.2, 30, 30, 6.6), (-3.2, 70, 22, 6.4)]):
            crista.append(lamina_reta(f"crista_l{k}_{s_}", (1.7 * lado, 30.8, z), (rx, 0, -rz * lado), L, 3.0, 1.3, ponta="z",
                                      k=-0.1 * k))
    cab.append(osso("crista", [0, 31.0, -6.0], [0, 0, 0], crista))
    return cab

# ---------------- peitilho em V ----------------
BIB_FILAS = [(23.4, 21.2, 2.7), (21.6, 19.2, 2.3), (19.6, 17.2, 1.85), (17.6, 15.2, 1.4), (15.6, 13.6, 0.95)]  # (y topo, y base, meia largura)
BIB_Z = -10.1
BIB_CREME = (242, 214, 170); BIB_CLARO = (250, 230, 196); BIB_SOMBRA = (217, 185, 138)

def mat_peitilho(y_base, hw):
    """Fileira do babador: penas creme pontudas e lisas (metade um pouco mais clara), com uma sombra leve só na
    beirada de baixo de cada pena (o vão entre as pontas mostra a pena de baixo, também creme)."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        if face == "up": return BIB_CLARO
        if face == "down": return BIB_SOMBRA
        if face != "north": return BIB_CREME
        n = max(2, round(2 * hw / 1.7)); larg = 2 * hw / n
        q = ((x + hw) / larg) % 1.0                                # posição dentro da pena (0..1)
        ponta = y_base + 0.7 * abs(2 * q - 1)                     # beirada em V de cada pena
        if y < ponta - 0.1: return mix(BIB_CREME, BIB_SOMBRA, 0.5)
        if y < ponta + 0.22: return BIB_SOMBRA
        return BIB_CLARO if q < 0.5 else BIB_CREME
    return f

def no_v(x, y):
    """Dentro do V creme do peito (de frente)?"""
    return 13.4 < y < 23.6 and abs(x) < 2.8 - (23.4 - y) * 0.19

def peitilho():
    pecas = []
    for k, (y1, y0, hw) in enumerate(BIB_FILAS):
        z = BIB_Z - 0.15 * (len(BIB_FILAS) - k)                  # a de cima fica por cima da de baixo
        pecas.append(peca(f"peitilho{k}", [-hw, y0, z - 0.8], [hw, y1, z + 0.6], mat_peitilho(y0, hw), faixa=(13, 24), res=4))
    # ponta do V
    q = 1.5 / 1.4142
    pecas.append(peca("peitilho_ponta", [-q / 2, 13.6 - q / 2, BIB_Z - 0.8], [q / 2, 13.6 + q / 2, BIB_Z + 0.4],
                      mat_cor(lambda p, f_: BIB_CREME if f_ == "north" else BIB_SOMBRA, borda=.1, curva=.1), rot=(0, 0, 45),
                      pivo=(0, 13.6, BIB_Z), res=4))
    return pecas

# ---------------- cauda: dois laços de cipó, um de cada lado ----------------
# Cada cipó nasce no alto da garupa e sobe já curvo, sem trecho reto. Ele arqueia para trás por cima, desce pelo lado
# de fora e enrola para dentro, deixando o laço aberto embaixo (em C). Os dois ficam em planos laterais (paralelos ao
# corpo), em x = ±LACO_X: de costas aparecem como dois arcos verticais com um vão entre eles.
LACO_X = 4.2
LACOS = {  # nome: (x, raiz (z, y), centro (z, y), semi-eixos (a, b), ângulo inicial, ângulo final, largura inicial)
    "cipo_a": (LACO_X, (5.0, 17.6), (15.0, 20.2), (7.0, 7.4), 194, -150, 3.7),     # laço externo grande
    "cipo_b": (-LACO_X, (5.0, 15.6), (14.2, 16.8), (4.8, 4.6), 196, -150, 3.2),    # laço interno menor
}

def caminho_laco(raiz, centro, eixos, t0, t1):
    """Amostra o laço (elipse que encolhe no fim) a partir da raiz, em segmentos que afinam. Devolve
    (comprimentos, rot0, curvas) para cipo(); o cipó cresce em +z local e rx negativo o faz subir."""
    zc, yc = centro; a, b = eixos
    def ponto(t):
        f = 1.0 if t > -50 else max(0.4, 1.0 - 0.6 * (-50 - t) / (-50 - t1))
        r = math.radians(t)
        return (zc + f * a * math.cos(r), yc + f * b * math.sin(r))
    dens = [ponto(t0 - i * 0.5) for i in range(int((t0 - t1) * 2) + 1)]
    pts = [dens[0]]; alvo = 2.6; acc = 0.0; k = 0
    for p, q in zip(dens, dens[1:]):
        acc += math.dist(p, q)
        if acc >= alvo:
            pts.append(q); acc = 0.0; k += 1
            alvo = max(1.4, 2.6 - 0.07 * k)
    comps, curvas, h_ant, rot0 = [], [], None, (0, 0, 0)
    for p, q in zip(pts, pts[1:]):
        h = math.degrees(math.atan2(q[1] - p[1], q[0] - p[0]))
        if h_ant is None: rot0 = (-h, 0, 0); curvas.append(0)
        else: curvas.append(-((h - h_ant + 180) % 360 - 180))
        comps.append(math.dist(p, q)); h_ant = h
    return comps, rot0, curvas

_LACOS = {n: caminho_laco(v[1], v[2], v[3], v[4], v[5]) for n, v in LACOS.items()}
# os cipós da cauda (cadeias 'cipo_a_k' e 'cipo_b_k') ondulam devagar no plano lateral
ONDAS = [(n, len(c[0]), (1.2, 0.3, 0.3)) for n, c in _LACOS.items()]

# ---------------- corpo ----------------
def montar():
    cab = cabeca_ossos()
    cabeca = osso("cabeca", [0, 24.5, -6.5], [0, 0, 0], cab)
    mnuc = mat_cor(lambda p, f_: CREME if (f_ == "north" or p[2] < -9.5) and no_v(p[0], p[1]) else VERDE, borda=.0, curva=.3)
    pescoco = osso("pescoco", [0, 22.0, -6.5], [0, 0, 0], [
        peca("pescoco", [-3.8, 20.0, -10.9], [3.8, 25.0, -3.4], mnuc, faixa=(18, 26), res=2),
        cabeca])

    corpo = []
    mnucleo = mat_cor(lambda p, f_: CREME if p[2] < -9.5 and no_v(p[0], p[1]) else (VERDE if p[2] < -8.5 or f_ == "up" else SOMBRA_FOLHA),
                      borda=.0, curva=.4)
    corpo += g.arredondado2("tronco", [-7.6, 9.4, -10.2], [7.6, 17.6, 6.0], mnucleo, r=2.2, faixa=(8, 24), res=2)
    corpo += g.arredondado2("tronco_cima", [-6.0, 14.0, -10.6], [6.0, 21.6, 5.0], mnucleo, r=2.0, faixa=(8, 24), res=2)

    # peitilho creme em V: fileiras em degrau, cada uma com a beirada de baixo em pontas de pena, e ponta no meio do peito
    corpo += peitilho()

    # anéis de folhas-pena grossas em volta do corpo (de cima para baixo: cada anel mais largo, abrindo para fora)
    ANEIS = [  # (y raiz, raio x, raio z, z centro, flare, varre, L, W, phis, cores)
        (24.4, 5.0, 4.4, -6.0, 24, 46, 6.6, 2.8, [-6, 16, 38, 60, 84], [LIMA, VERDE_CLARO, LIMA, VERDE_CLARO, LIMA]),
        (21.4, 6.2, 8.6, -2.4, 24, 40, 6.8, 3.2, [-50, -30, -10, 10, 30, 52, 74], [LIMA, LIMA, VERDE_CLARO, LIMA, VERDE_CLARO, LIMA, VERDE_CLARO]),
        (17.4, 8.0, 9.2, -2.2, 22, 34, 7.0, 3.4, [-56, -32, -8, 16, 40, 64, 86], [VERDE_CLARO, VERDE, VERDE_CLARO, VERDE, VERDE_CLARO, VERDE, VERDE_CLARO]),
        (14.0, 7.8, 7.8, -1.2, 18, 22, 6.0, 3.4, [-78, -52, -26, 0, 26, 52, 78], [VERDE_ESC, VERDE, VERDE_ESC, VERDE, VERDE_ESC, VERDE, VERDE_ESC]),
    ]
    for a, (y0, ax, az, zc, fl, va, L, W, phis, cores) in enumerate(ANEIS):
        for lado in (-1, 1):
            s = "d" if lado < 0 else "e"
            for k, phi in enumerate(phis):
                r = math.radians(phi)
                x, z = lado * ax * math.cos(r), zc + az * math.sin(r)
                frente = phi < -60                      # folhas da frente: menores (camadas finas em V, como na ficha)
                corpo.append(folha_bloco(f"folha{a}{k}_{s}", (x, y0 - 0.4 * (k % 2), z), phi, lado,
                                         L * (0.95 + 0.08 * (k % 2)) * (0.85 if frente else 1), W * (0.8 if frente else 1),
                                         (VERDE_CLARO if a == 2 else VERDE) if frente else cores[k % len(cores)], flare=fl * (0.4 if phi < -60 else 1), varre=(-6 if phi < -30 else va * (1 if phi < 50 else 0.5))))
    # barriga: 2 camadas de folhas verde-claras em chevron (V) sob o babador, convergindo para o eixo
    for k, (x, y, z, L, va, cor) in enumerate([(-1.9, 15.6, -10.9, 5.0, 22, VERDE_CLARO), (1.9, 15.6, -10.9, 5.0, -22, VERDE_CLARO),
                                               (-3.6, 14.4, -10.5, 5.2, 18, VERDE), (3.6, 14.4, -10.5, 5.2, -18, VERDE),
                                               (-1.6, 12.6, -10.7, 5.0, 20, VERDE_CLARO), (1.6, 12.6, -10.7, 5.0, -20, VERDE_CLARO),
                                               (0.0, 11.2, -10.6, 4.4, 0, VERDE)]):
        corpo.append(folha_bloco(f"barriga{k}", (x, y, z), -90, 1, L, 3.0, cor, flare=-6, varre=va, T=0.9))
    # folhas que pendem sob a raiz dos cipós (garupa de baixo)
    for lado in (-1, 1):
        corpo.append(folha_bloco("garupa_" + ("d" if lado < 0 else "e"), (2.6 * lado, 15.0, 6.2), 80, lado, 7.0, 3.2, VERDE,
                                 flare=20, varre=0, T=0.8))
    # costas no meio
    for k, (y, z, L) in enumerate([(21.6, 5.0, 6.0), (17.6, 7.0, 6.4), (13.6, 7.2, 6.4)]):
        corpo.append(folha_bloco(f"costas{k}", (0, y, z), 90, 1, L, 4.0, VERDE if k % 2 else VERDE_CLARO, flare=24, T=1.1))

    # ---------- ombros: flor grande + folhas largas da asa (osso animável asa_d / asa_e) ----------
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = [flor_grossa("flor_ombro_" + s, (9.6 * lado, 17.4, -4.2), (0, -45 * lado, 0), 3.9)]
        for k, (y0, z0, L, W, cor) in enumerate([(19.6, -1.0, 6.6, 4.2, VERDE_CLARO), (19.2, 2.4, 7.0, 4.2, VERDE)]):
            asa.append(folha_bloco(f"asa{k}_{s}", (7.6 * lado, y0, z0), 10, lado, L, W, cor, flare=30, varre=42, T=1.2))
        corpo.append(osso("asa_" + s, [7.0 * lado, 20.0, -1.0], [0, 0, 0], asa))

    # ---------- cauda: dois laços de cipó (externo grande em C e interno menor), espinhos, flores e botões ----------
    cauda = []
    for nome, (x, raiz, centro, eixos, t0, t1, w0) in LACOS.items():
        comps, rot0, curvas = _LACOS[nome]
        n = len(comps)
        larguras = [w0 - (w0 - 1.5) * k / (n - 1) for k in range(n)]
        fora = 1 if x > 0 else -1
        lado = "e" if fora > 0 else "d"; dentro = "d" if fora > 0 else "e"
        if nome == "cipo_a":
            esp = {2: ["cima"], 3: [lado], 4: ["cima"], 6: ["cima"], 7: [dentro], 8: ["cima"], 9: [lado], 10: ["cima"],
                   12: ["cima"], 13: [lado]}
            flo = {3: (lado, 2.3), 9: (dentro, 2.3), 14: (lado, 2.2), 17: (dentro, 2.0)}
            bot = {n - 1: [(0, 1)], 11: [(fora, 0.3)], 5: [(-fora, 0.4)]}
        else:
            esp = {2: ["cima"], 4: [lado], 5: ["cima"], 7: ["cima"]}
            flo = {3: (lado, 2.1), 8: (dentro, 1.9)}
            bot = {n - 1: [(0, 1)], 6: [(fora, 0.3)]}
        z0 = centro[0] + eixos[0] * math.cos(math.radians(t0)); y0 = centro[1] + eixos[1] * math.sin(math.radians(t0))
        cauda.append(cipo(nome, (x, y0, z0), rot0, comps, larguras, curvas, espinhos=esp, flores=flo, botoes=bot))
    # flores grandes dentro do laço externo (a ficha enche o miolo da volta de flores)
    cauda.append(flor("flor_laco0", (LACO_X * 0.5, 21.6, 13.2), (0, -90, 0), 2.6))
    cauda.append(flor("flor_laco1", (-LACO_X * 0.5, 19.2, 16.6), (0, 90, 0), 2.4))
    corpo.append(osso("cauda", [0, 16.6, 5.0], [0, 0, 0], cauda))

    corpo.append(pescoco)
    tronco = osso("corpo", [0, 9.0, 0.0], [0, 0, 0], corpo)

    # ---------- pernas: coxa verde + penas creme, canela laranja em blocos, pé de 3 dedos grossos + 1 atrás ----------
    def perna(lado):
        s = "d" if lado < 0 else "e"; xc = 3.3 * lado; zc = 0.0
        pp = []
        def cor_canela(p, f_):
            base = (249, 170, 14) if f_ != "down" else (224, 146, 12)
            if f_ == "up": return (255, 194, 74)
            if f_ not in ("up", "down") and abs(p[1] - 3.3) < 0.12: base = (224, 146, 12)   # emenda suave do bloco
            return base
        mperna = mat_cor(cor_canela, borda=.1, curva=.3)
        pp += g.octogono("coxa_" + s, [xc - 1.6, 5.0, zc - 1.6], [xc + 1.6, 9.4, zc + 1.6],
                         mat_cor(lambda p, f_: (36, 81, 27), borda=.12, curva=.3), r=0.5, faixa=(5, 9.4), res=2)
        pp += g.octogono("canela_" + s, [xc - 1.45, 1.8, zc - 1.5], [xc + 1.45, 5.2, zc + 1.5], mperna, r=0.4, faixa=(0, 6), res=3)
        # tufos creme pontudos colados à base da plumagem, na frente da coxa (sem cobrir o verde da coxa)
        for k, dx in enumerate((-0.9, 1.0)):
            pp.append(folha_bloco(f"coxa_pena{k}_{s}", (xc + dx * lado, 10.8, -3.4), -90, 1, 3.4, 2.6, BIB_CREME if k else BIB_CLARO,
                                  flare=6, T=0.8))
        mdedo = mat_cor(lambda p, f_: (255, 194, 74) if f_ == "up" else ((224, 146, 12) if f_ in ("down", "north") else (249, 170, 14)),
                        borda=.12, curva=.35)
        for nome, giro, dx, comp in (("meio", 0, 0, 5.4), ("fora", -8 * lado, 1.25 * lado, 4.6), ("dentro", 8 * lado, -1.25 * lado, 4.6)):
            x0, z0 = xc + dx, zc - 0.4
            pp.append(osso(f"dedo_{nome}_{s}", [x0, 0, z0], [0, giro, 0], [
                peca(f"dedo_{nome}_{s}", [x0 - .72, 0, z0 - comp], [x0 + .72, 2.0, z0 + 0.6], mdedo, faixa=(0, 2.0), res=2)]))
        pp.append(peca("dedo_tras_" + s, [xc - .7, 0, zc + 0.6], [xc + .7, 1.8, zc + 3.0], mdedo, faixa=(0, 1.8), res=2))
        return osso("perna_" + s, [xc, 9.0, zc], [0, 0, 0], pp)

    return [tronco, perna(-1), perna(1)]

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
