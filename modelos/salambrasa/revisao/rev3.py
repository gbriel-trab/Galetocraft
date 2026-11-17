"""Salambrasa (#012, Fogo): o galo-salamandra das brasas, quadrúpede de carvão com manchas incandescentes."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, anel

ID = "salambrasa"; NOME = "Salambrasa"; NUMERO = 12
ALTURA = 2.45
QUADRUPEDE = True
ROSTO = ((0, 26.6, -20.5), 8.5)
ONDAS = [("rabo", 12, (1.5, 2.5, 0))]
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (da ficha) ----------------
CARVAO = (74, 56, 70); CARVAO_ESC = (46, 34, 44); CINZA_ROXO = (108, 90, 106); MALVA = (146, 126, 140)
TOPO_CAB = (58, 46, 51)                                    # alto da cabeça, carvão escuro
SOBRAN = (96, 80, 92); SOBRAN_CLARA = (122, 104, 116)      # sobrancelha / viseira
DEDO = (184, 168, 176); DEDO_CLARO = (212, 200, 206); DEDO_ESC = (146, 130, 140)
BICO = (125, 106, 115); BICO_CLARO = (152, 134, 143); BICO_ESC = (94, 78, 88)
CRISTA = (216, 48, 42); CRISTA_ESC = (158, 29, 29); CRISTA_CLARA = (242, 92, 76)
VERM = (214, 40, 36); VERM_ESC = (156, 22, 28); VERM_VIVO = (240, 64, 50)
LARANJA = (246, 120, 24); LARANJA_ESC = (222, 84, 18); AMARELO = (255, 196, 40); AMARELO_CLARO = (255, 230, 120)
BRASA_LAR = (240, 122, 30)                                 # faixa da canela
PLACA = (240, 138, 36); PLACA_LINHA = (201, 95, 18); PLACA_CLARA = (252, 178, 84)
CREME = (250, 236, 214)
BRASA_MIOLO = (255, 232, 110); BRASA = (255, 186, 34); BRASA_BORDA = (246, 112, 20)
FENDA = (255, 90, 26); FENDA_BORDA = (196, 46, 22)

DESCE = 2.4              # o corpo inteiro (com cabeça e cauda) desce isso: pernas mais curtas, como na ficha

# ---------------- manchas incandescentes (decalque 3D em octógono) ----------------
def mancha(p, face, lista):
    """Cor da mancha incandescente no ponto (ou None). lista = [((cx, cy, cz), raio, profundidade)]; raio pode ser
    (rx, ry, rz) para manchas ovais. O desenho é um octógono na face (como as manchas da ficha): miolo claro, corpo
    amarelo e beirada laranja. Só aparece nas faces a menos de 'profundidade' do centro."""
    x, y, z = p
    for (cx, cy, cz), r, prof in lista:
        rx, ry, rz = r if isinstance(r, tuple) else (r, r, r)
        dx, dy, dz = x - cx, y - cy, z - cz
        if face in ("east", "west"): a, b, n = dz / rz, dy / ry, dx
        elif face in ("north", "south"): a, b, n = dx / rx, dy / ry, dz
        else: a, b, n = dx / rx, dz / rz, dy
        if abs(n) > prof: continue
        d = max(abs(a), abs(b), (abs(a) + abs(b)) / 1.38)
        if d <= 1:
            if d < 0.42: return BRASA_MIOLO
            if d < 0.78: return BRASA
            return BRASA_BORDA
    return None

def mat_com_manchas(cor_fn, lista, **kw):
    """Material com luz 3D por baixo e manchas incandescentes (sem sombra) por cima."""
    base = g.mat_cor(cor_fn, **kw)
    def f(c):
        m = mancha(c["p"], c["face"], lista)
        return m if m else base(c)
    return f

def brilho_manchas(lista):
    return lambda c, cor: mancha(c["p"], c["face"], lista) is not None

def dist_seg(p, a, b):
    ab = [b[i] - a[i] for i in range(len(a))]; ap = [p[i] - a[i] for i in range(len(a))]
    t = clamp(sum(ab[i] * ap[i] for i in range(len(a))) / max(sum(v * v for v in ab), 1e-6))
    return math.sqrt(sum((ap[i] - t * ab[i]) ** 2 for i in range(len(a))))

# ---------------- placas da barriga (pintadas rente à superfície do pescoço e do peito) ----------------
def cor_placa(y, passo=1.9, fase=0.0):
    """Faixas de placa laranja: claro em cima de cada placa, linha escura embaixo (segmentos)."""
    t = ((y - fase) % passo) / passo                 # 0 embaixo .. 1 em cima da placa
    if t < 0.13: return PLACA_LINHA
    return mix(PLACA, PLACA_CLARA, clamp((t - 0.13) / 0.87) * 0.6)

# ---------------- corpo ----------------
VENTRE_Y = 11.4          # abaixo disso o corpo é barriga laranja segmentada

def largura_placa_peito(y): return 3.5 - 0.06 * (y - 10)

def cor_corpo(p, face):
    x, y, z = p
    if face == "down" or y < VENTRE_Y:
        t = clamp((VENTRE_Y - y) / 2.0)
        base = mix(LARANJA, AMARELO, 0.2 + 0.5 * t)
        if (z + 20) % 2.6 < 0.4: base = mix(base, LARANJA_ESC, 0.8)          # segmentos da barriga
        return base
    if face == "north" and z < -13.0 and abs(x) < largura_placa_peito(y):      # placas do peito, entre as patas
        return cor_placa(y, fase=0.4)
    if y < VENTRE_Y + 0.7: return mix(LARANJA_ESC, CARVAO, (y - VENTRE_Y) / 0.7)
    return CARVAO

MANCHAS_CORPO = []
for lado in (-1, 1):
    MANCHAS_CORPO += [((1.7 * lado, 20.4, -7.6 + 1.6 * (lado > 0)), 1.0, 1.4),      # dorso
                      ((1.9 * lado, 19.4, -2.6 + 2.4 * (lado > 0)), 1.1, 1.4),
                      ((1.5 * lado, 17.8, 4.6 + 1.8 * (lado > 0)), 0.95, 1.4),
                      ((5.3 * lado, 13.2, -1.6), (1.2, 1.1, 1.3), 1.4),              # flancos (abaixo da asa)
                      ((5.0 * lado, 15.0, 6.4), (1.0, 1.0, 1.1), 1.4),
                      ((5.3 * lado, 12.2, 2.6), (0.8, 0.8, 0.9), 1.4)]
MANCHAS_CORPO += [((0, 19.4, 0.8), 1.4, 1.4)]                                        # mancha grande do meio das costas

# ---------------- cauda em laço ----------------
def mat_rabo(w, h, py, z0, L, k):
    """Segmento da cauda (eixo local +z): dorso de carvão com manchas (grande e pequena alternadas em cima, uma de
    cada lado). Na base (k <= 3) o laranja é a barriga (embaixo); no laço, o dorso manchado fica para fora e só uma
    faixa laranja estreita corre por dentro da curva."""
    zc = z0 + L * 0.5
    base = k <= 3
    yd = py + h / 2 if base else py - h / 2                       # face do dorso
    grande = k % 2 == 1
    lista = [((0.0, yd, zc), ((0.36 if grande else 0.19) * w, 1, (0.44 if grande else 0.24) * L), 1.0)]
    for s in (-1, 1):
        lista.append(((s * w / 2, py - h / 2 + (0.58 if base else 0.42) * h, zc), (1, 0.27 * h, 0.34 * L), 1.0))
    def cor(p, face):
        x, y, z = p
        v = (y - (py - h / 2)) / h                     # 0 embaixo .. 1 em cima (local)
        if not base: v = 1 - v                         # v pequeno = lado de dentro / de baixo
        dentro = face == ("down" if base else "up")
        if base and (dentro or v < 0.2): return mix(AMARELO, LARANJA, clamp(v / 0.2))
        if not base and dentro:
            return mix(LARANJA, LARANJA_ESC, abs(x) / (0.22 * w)) if abs(x) < 0.22 * w else tom(CARVAO, -0.1)
        return CARVAO
    return mat_com_manchas(cor, lista, borda=.03, curva=.4), brilho_manchas(lista)

def cauda_laco(nome, base, segs):
    """Cadeia como a pena_curva (ossos '<nome>_0', '<nome>_1'...), mas com giro próprio em cada junta, para a cauda
    poder correr reta para trás e depois enrolar num laço. segs = [(comprimento, largura, altura, rx)].
    Cada segmento tem seção arredondada (3 blocos: cruz + miolo chanfrado) e avança para trás (ov) para tapar a junta."""
    def seg(k, pos):
        L, w, h, rx = segs[k]
        px, py, pz = pos
        ov = 0.2 + (h / 2) * math.tan(math.radians(abs(rx))) if k > 0 else 0.6
        r = 0.3 * min(w, h); q = r / 2
        mat, br = mat_rabo(w, h, py, pz, L, k)
        fx = (py - h / 2, py + h / 2)
        z0, z1 = pz - ov, pz + L
        filhos = [peca(f"{nome}_{k}_a", [px - w / 2, py - h / 2 + r, z0], [px + w / 2, py + h / 2 - r, z1], mat, faixa=fx, brilho=br, res=3),
                  peca(f"{nome}_{k}_b", [px - w / 2 + r, py - h / 2, z0], [px + w / 2 - r, py + h / 2, z1], mat, faixa=fx, brilho=br, res=3),
                  peca(f"{nome}_{k}_c", [px - w / 2 + q, py - h / 2 + q, z0], [px + w / 2 - q, py + h / 2 - q, z1], mat, faixa=fx, brilho=br, res=3)]
        if k + 1 < len(segs): filhos.append(seg(k + 1, (px, py, z1)))
        return osso(f"{nome}_{k}", [px, py, pz], [rx, 0, 0], filhos)
    return seg(0, base)

# ---------------- cabeça ----------------
K_CAB = 1.12                      # escala da cabeça inteira (com crista, bico e juba)
OLHO_Y = 28.4
FAC_T = 1.4                       # espessura da peça da face diagonal (onde fica o olho)
FAC_L = 3.96                      # comprimento da face diagonal
FAC_M = (3.1, -20.6)              # meio da superfície da face diagonal (lado +x): de (1.7, -22.0) a (4.5, -19.2)
FAC_C = (FAC_M[0] - 0.7071 * FAC_T / 2, FAC_M[1] + 0.7071 * FAC_T / 2)

def cor_cabeca(p, face):
    x, y, z = p
    if face == "up" or y > 30.6: return TOPO_CAB
    return mix(CARVAO, CINZA_ROXO, clamp((y - 25.0) / 5.0))

def mat_faceta(lado):
    base = g.mat_cor(cor_cabeca, borda=.0, curva=.3)
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u = z - FAC_C[1]
            o = g.pintar_olho(u - 0.05, y - OLHO_Y, 1.6, 1.42, iris=((150, 24, 10), (240, 86, 30)), esclera=CREME,
                              r_iris=(0.58, 0.78), c_iris=(-0.32, -0.12), r_pup=(0.27, 0.36), bravo=0.42, alto=0.36,
                              contorno=CARVAO_ESC)
            if o: return o
        return base(c)
    return f

def mat_sobrancelha(c):
    """Sobrancelha grossa (viseira) que avança sobre os olhos: malva-carvão, mais clara em cima."""
    face = c["face"]
    base = SOBRAN_CLARA if face == "up" else CARVAO_ESC if face == "down" else \
        mix(SOBRAN, SOBRAN_CLARA, 0.35) if face == "north" else SOBRAN
    return tom(base, -0.28) if g.na_borda(c) else base

def cor_bico(p, face):
    x, y, z = p
    if face == "up": return BICO_CLARO
    if face in ("east", "west") and abs(z + 23.6) < 0.3 and abs(y - 28.0) < 0.2: return CARVAO_ESC   # narina
    if face == "down": return BICO_ESC
    return mix(tom(BICO, -0.12), BICO, clamp((y - 25.6) / 3.0))

# ---------------- crista de brasa ----------------
def mat_crista(c):
    face = c["face"]
    (_, y0, _), (_, y1, _) = c["b"]
    t = clamp((c["p"][1] - y0) / max(y1 - y0, 1e-6))
    if face == "up": base = CRISTA_CLARA
    elif face == "down": base = CRISTA_ESC
    elif face == "north": base = mix(CRISTA, CRISTA_CLARA, 0.25 * t)
    elif face == "south": base = mix(CRISTA_ESC, CRISTA, 0.4 * t)
    else: base = mix(CRISTA_ESC, CRISTA, 0.35 + 0.65 * t)
    return tom(base, -0.25) if g.na_borda(c) else base

def tufo_crista(nome, x0, x1, yb, z0, z1, h, inc):
    """Tufo da crista: bloco grosso que nasce da testa e inclina 'inc' graus para trás a partir da base, com um
    degrau mais estreito no alto (o 'pixel' chanfrado das fichas)."""
    zc = (z0 + z1) / 2; xm = (x0 + x1) / 2
    return osso(nome, [xm, yb, zc], [inc, 0, 0], [
        peca(nome, [x0, yb, z0], [x1, yb + h - 0.7, z1], mat_crista, res=3),
        peca(nome + "_topo", [x0 + 0.4, yb + h - 0.8, z0 + 0.35], [x1 - 0.4, yb + h, z1 - 0.35], mat_crista, res=3)])

# ---------------- ombro: placa lisa com a fenda em Y + leque de penas (asa dobrada) ----------------
FENDA_Y = [((0.0, -0.5), (-2.2, 0.3)), ((-2.2, 0.3), (-4.9, -2.6)), ((-2.2, 0.3), (-4.7, 3.0))]   # (y, z) relativos ao ombro

def mat_placa_ombro(P, lado):
    fora = "east" if lado > 0 else "west"
    def fenda(c):
        if c["face"] not in (fora, "up"): return None
        q = (c["p"][1] - P[1], c["p"][2] - P[2])
        d = min(dist_seg(q, a, b) for a, b in FENDA_Y)
        if d < 0.17: return BRASA_MIOLO
        if d < 0.36: return FENDA
        if d < 0.5: return FENDA_BORDA
        return None
    def f(c):
        cr = fenda(c)
        if cr: return cr
        face = c["face"]
        base = mix(CARVAO, CINZA_ROXO, 0.55) if face == "up" else CARVAO_ESC if face == "down" else \
            mix(CARVAO, CINZA_ROXO, 0.3) if face == fora else CARVAO
        (_, y0, _), (_, y1, _) = c["b"]
        base = mix(base, CARVAO_ESC, clamp((y1 - c["p"][1]) / max(y1 - y0, 1e-6)) * 0.35)
        return tom(base, -0.25) if g.na_borda(c) else base
    return f, (lambda c, cor: fenda(c) is not None)

def ombro(lado):
    """Uma placa lisa de carvão no ombro cruzada por uma fenda contínua em Y; embaixo, um leque para trás ao longo do
    flanco: 2 fileiras de coberteiras escuras sobre 6 penas vermelho -> laranja -> amarelo."""
    s = "d" if lado < 0 else "e"
    P = (4.9 * lado, 20.8, -8.4)
    m, br = mat_placa_ombro(P, lado)
    x0, x1 = sorted((P[0], P[0] + 1.3 * lado))
    placa = g.arredondado(f"placa_ombro_{s}", [x0, P[1] - 5.4, P[2] - 3.6], [x1, P[1], P[2] + 3.6], m, r=0.5, res=5, brilho=br)
    asa = [osso(f"ombro_{s}", list(P), [-8, 0, 38 * lado], placa)]
    escuras = (CINZA_ROXO, CARVAO, CARVAO_ESC)
    # penas de fogo (embaixo), coberteiras (por cima): (x, y, z, comprimento, largura, varrida, abertura, cores)
    penas = [(5.5, 16.8, -10.6 + 1.7 * k, 8.6 - 0.3 * abs(k - 2.5), 3.3, 54 + 4 * k, 12,
              [(VERM, LARANJA, AMARELO), (VERM_VIVO, LARANJA, AMARELO), (VERM, LARANJA_ESC, AMARELO)][k % 3]) for k in range(6)]
    penas += [(5.9, 17.6, -10.0 + 2.1 * k, 5.6, 3.4, 74 + 3 * k, 16, escuras) for k in range(4)]
    penas += [(6.2, 18.4, -9.6 + 2.2 * k, 4.4, 3.4, 78 + 3 * k, 20, escuras) for k in range(3)]
    for k, (x, y, z, L, W, var, fl, cores) in enumerate(penas):
        asa.append(g.pena_placa(f"asa{k}_{s}", (x * lado, y, z), (-var, 0, fl * lado), L, W, cores, curva=0.2))
    return osso("asa_" + s, [5.0 * lado, 19.0, -8.0], [0, 0, 0], asa)

# ---------------- pescoço ----------------
def mat_pescoco(z_frente):
    """Pescoço de carvão; na frente (face norte e o fio da frente dos lados) as placas laranja segmentadas,
    estreitando para cima. Coordenadas locais da peça (antes do giro)."""
    base = g.mat_cor(lambda p, f: CARVAO, borda=.03, curva=.3)
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        w = 2.6 - 0.09 * (y - 15.0)
        if (face == "north" and abs(x) < w) or (face in ("east", "west") and z < z_frente + 0.8):
            return cor_placa(y)
        return base(c)
    return f

# ---------------- pernas ----------------
def dedos(nome, xc, zf):
    """3 dedos grandes cinza-claros para a frente (cada um ~1/3 do pé, em leque) + 1 menor atrás."""
    def mat_dedo(z_ponta):
        def f(c):
            face = c["face"]; z = c["p"][2]
            base = DEDO_CLARO if face == "up" else DEDO_ESC if face == "down" else DEDO if face == "north" else mix(DEDO, DEDO_ESC, .3)
            if z < z_ponta and face != "down": base = tom(base, 0.18)           # unha
            return tom(base, -0.28) if g.na_borda(c) else base
        return f
    pp = []
    for k, (dx, giro) in enumerate(((-2.3, 12), (0.0, 0), (2.3, -12))):
        x0 = xc + dx; z0 = zf + 1.0
        pp.append(osso(f"{nome}_dedo{k}", [x0, 0, z0], [0, giro, 0], [
            peca(f"{nome}_dedo{k}", [x0 - 1.1, 0, z0 - 4.4], [x0 + 1.1, 2.4, z0], mat_dedo(z0 - 3.6), res=3)]))
    pp.append(peca(nome + "_dedo_tras", [xc - 0.85, 0, zf + 0.8], [xc + 0.85, 1.6, zf + 3.0], mat_dedo(-999), res=3))
    return pp

def perna(nome, xc, zc, tras):
    """Pernas curtas e grossas: coxa de carvão, faixa cor de brasa só no joelho/canela, tornozelo escuro e dedos."""
    lado = -1 if xc < 0 else 1
    pp = []
    escuro = g.mat_cor(lambda p, f: CARVAO, borda=.06, curva=.4)
    if tras:
        lista = [((xc + 3.1 * lado, 9.6, zc), (1, 1.15, 1.35), 1.4)]
        pp += g.arredondado2(nome + "_coxa", [xc - 3.1, 5.4, zc - 4.0], [xc + 3.1, 13.2, zc + 3.8],
                             mat_com_manchas(lambda p, f: CARVAO, lista, borda=.04, curva=.4), r=1.7, brilho=brilho_manchas(lista),
                             rot=(-20, 0, 6 * lado), pivo=(xc, 12.6, zc))
        zp = zc + 2.5
    else:
        pp += g.arredondado2(nome + "_braco", [xc - 2.7, 5.8, zc - 2.8], [xc + 2.7, 11.6, zc + 2.8], escuro, r=1.4,
                             rot=(0, 0, 8 * lado), pivo=(xc, 6.0, zc))
        zp = zc
    mo = g.mat_cor(lambda p, f: BRASA_LAR, borda=.08, curva=.35)
    pp += g.octogono(nome + "_canela", [xc - 2.4, 3.7, zp - 2.4], [xc + 2.4, 6.6, zp + 2.4], mo, r=0.8)
    pp += g.octogono(nome + "_tornozelo", [xc - 2.05, 1.9, zp - 2.05], [xc + 2.05, 4.0, zp + 2.05], escuro, r=0.7)
    pp += dedos(nome, xc, zp)
    return osso(nome, [xc, 11.6, zc], [0, 0, 0], pp)

# ---------------- montagem ----------------
def montar():
    # ---------- cabeça: alto escuro, sobrancelha grossa sobre os olhos, bochechas chanfradas, bico em cunha ----------
    i_cab = len(g.PECAS)
    cab = []
    mcab = g.mat_cor(cor_cabeca, borda=.04, curva=.3)
    fx = (24.8, 31.6)
    cab += g.arredondado2("cranio", [-4.4, 26.0, -19.8], [4.4, 31.4, -15.0], mcab, r=1.0, faixa=fx, res=3)
    cab.append(peca("cranio_frente", [-1.7, 25.8, -22.0], [1.7, 31.0, -19.4], mcab, faixa=fx, res=3))
    cab += g.arredondado("bochecha", [-3.2, 24.9, -20.3], [3.2, 26.9, -15.6], mcab, r=0.6, faixa=fx, res=3)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 26.3, cz - FAC_L / 2], [cx + FAC_T / 2, 31.0, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, 28.4, cz), faixa=fx, res=8))
        # sobrancelha grossa: avança sobre o olho e desce para o bico (V bravo), emendada no alto escuro da cabeça
        x0, x1 = sorted((-0.3 * lado, 4.6 * lado))
        cab.append(peca("sobrancelha_" + s, [x0, 29.3, -23.2], [x1, 31.2, -18.6], mat_sobrancelha, rot=(0, 0, 13 * lado),
                        pivo=(4.6 * lado, 31.2, -21.0), res=3))
    # bico em cunha (~metade da cabeça): base larga em losango (de frente um V abaixo dos olhos), cume que afina e
    # os 2 últimos voxels caindo num gancho
    mb = g.mat_cor(cor_bico, borda=.05, curva=.3)
    fb = (25.4, 29.4)
    a = 1.8
    cab.append(peca("bico_v", [-a, 28.1 - a, -23.1], [a, 28.1 + a, -21.6], mb, rot=(0, 0, 45), pivo=(0, 28.1, -22.35), faixa=fb))
    cab.append(peca("bico_cume", [-1.3, 27.2, -24.6], [1.3, 28.9, -22.6], mb, rot=(-12, 0, 0), pivo=(0, 28.9, -22.6), faixa=fb))
    cab.append(peca("bico_ponta", [-0.85, 27.3, -25.8], [0.85, 28.6, -24.4], mb, rot=(-12, 0, 0), pivo=(0, 28.9, -22.6), faixa=fb))
    cab.append(peca("bico_gancho", [-0.65, 26.4, -26.0], [0.65, 27.5, -25.1], mb, rot=(-12, 0, 0), pivo=(0, 28.9, -22.6), faixa=fb))
    # crista: tufos vermelhos que nascem da testa, baixos na frente e altos atrás, inclinados ~30° para trás;
    # de frente ocupa a largura da cabeça, com o tufo do meio mais alto
    crista = []
    for k, (z0, z1, hm, hl) in enumerate([(-22.4, -18.8, 3.2, 2.2), (-20.6, -16.6, 5.6, 3.4), (-18.4, -14.2, 8.0, 4.6)]):
        crista.append(tufo_crista(f"crista_meio{k}", -1.65, 1.65, 30.6, z0, z1, hm, 30))
        for lado in (-1, 1):
            x0, x1 = sorted((1.3 * lado, 4.4 * lado))
            crista.append(tufo_crista(f"crista_{'d' if lado < 0 else 'e'}{k}", x0, x1, 30.4, z0 + 0.3, z1 - 0.1, hl, 30))
    cab.append(osso("crista", [0, 31.0, -18], [0, 0, 0], crista))
    # pelagem ígnea: penas que nascem das bochechas e da nuca e apontam para trás/baixo, sobre os ombros
    CAMADAS = [  # (y, raio x, raio z, z centro, abertura, varrida, comprimento, largura, cores, phis)
        (28.8, 4.3, 1.8, -16.6, 30, 52, 5.2, 3.0, (VERM, VERM_VIVO, LARANJA), [5, 45, 88]),
        (26.8, 4.0, 2.4, -16.8, 24, 44, 6.0, 3.2, (VERM, LARANJA, AMARELO), [-15, 25, 60, 88]),
        (25.0, 3.6, 2.6, -16.4, 18, 34, 6.0, 3.2, (VERM_VIVO, LARANJA, AMARELO), [10, 45, 80]),
    ]
    for f_, (y0, ax, az, zc, fl, var, L, W, cores, phis) in enumerate(CAMADAS):
        for k, phi in enumerate(phis):
            for lado in (-1, 1):
                if phi >= 84 and lado < 0: continue           # a pena de trás do meio é uma só
                x, z = anel(ax, az, zc, phi, lado)
                if phi >= 84: x = 0
                nome = f"juba{f_}{k}_{'d' if lado < 0 else 'e'}"
                if -30 < phi < 30:   # dos lados: em X, para não virar risco visto de frente
                    cab.append(g.pena_cruzada(nome, (x, y0, z), (-var, 0, fl * lado), L, W, cores, curva=0.15 * lado))
                else:
                    cab.append(g.pena_cone_placa(nome, (x, y0, z), phi, fl, L, W, cores, lado, varre=var if phi < 80 else 0,
                                                 curva=0.2 * lado))
    g.transformar(i_cab, cab, (0, 25.5, -17.0), k=K_CAB)
    cabeca = osso("cabeca", [0, 25.5, -16.5], [0, 0, 0], cab)

    # ---------- pescoço em S, de carvão, com as placas laranja rentes na frente ----------
    pesc = []
    pesc += g.octogono("pescoco_baixo", [-3.7, 16.5, -16.0], [3.7, 23.0, -9.4], mat_pescoco(-16.0), r=1.1, faixa=(15, 27),
                       rot=(-28, 0, 0), pivo=(0, 16.5, -12.8))
    pesc += g.octogono("pescoco_alto", [-3.4, 21.0, -19.2], [3.4, 27.0, -13.2], mat_pescoco(-19.2), r=1.0, faixa=(15, 27),
                       rot=(6, 0, 0), pivo=(0, 21.0, -16.3))
    pesc.append(cabeca)
    pescoco = osso("pescoco", [0, 18.0, -12.5], [0, 0, 0], pesc)

    # ---------- tronco de salamandra (curto, o dorso sobe para o pescoço) ----------
    corpo = []
    mt = mat_com_manchas(cor_corpo, MANCHAS_CORPO, borda=.03, curva=.5)
    bt = brilho_manchas(MANCHAS_CORPO)
    fc = (9.0, 20.6)
    corpo += g.arredondado2("peito", [-5.4, 9.8, -15.0], [5.4, 20.4, -4.0], mt, r=2.6, faixa=fc, brilho=bt)
    corpo += g.arredondado2("meio", [-5.3, 9.6, -6.0], [5.3, 19.4, 3.0], mt, r=2.6, faixa=fc, brilho=bt)
    corpo += g.arredondado2("quadril", [-5.0, 9.8, 1.0], [5.0, 17.8, 9.4], mt, r=2.6, faixa=fc, brilho=bt)
    corpo += [ombro(-1), ombro(1)]
    # cauda grossa na base, afinando sem parar até ~1/3 na ponta, que enrola num laço para cima
    Ls = [4.2, 4.1, 4.0, 3.9, 3.8, 3.7, 3.6, 3.5, 3.4, 3.3, 3.2, 3.1]
    Rs = [14, -4, -16, -28, -32, -28, -16, -24, -32, -26, -8, 4]
    Hs = [7.4, 7.0, 6.5, 6.0, 5.6, 5.2, 4.8, 4.4, 4.0, 3.6, 3.2, 2.8]
    Ws = [9.4, 9.2, 8.9, 8.5, 8.0, 7.4, 6.8, 6.1, 5.4, 4.6, 3.8, 3.1]
    corpo.append(osso("cauda", [0, 14.2, 7.5], [0, 0, 0], [cauda_laco("rabo", (0, 14.2, 7.5), list(zip(Ls, Ws, Hs, Rs)))]))
    corpo.append(pescoco)
    tronco = osso("corpo", [0, 13.0, 6.0], [0, 0, 0], corpo)
    g.transformar(0, [tronco], (0, 0, 0), k=1.0, sobe=-DESCE)        # corpo mais baixo: pernas ~25% mais curtas

    pernas = [perna("perna_fd", -5.8, -9.8, False), perna("perna_fe", 5.8, -9.8, False),
              perna("perna_td", -5.7, 3.8, True), perna("perna_te", 5.7, 3.8, True)]
    return [tronco] + pernas

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
