"""Salambrasa (#012, Fogo): o galo-salamandra das brasas, quadrúpede de carvão com manchas incandescentes."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, anel

ID = "salambrasa"; NOME = "Salambrasa"; NUMERO = 12
ALTURA = 2.45
QUADRUPEDE = True
ROSTO = ((0, 29.0, -20.5), 8.5)
ONDAS = [("rabo", 12, (1.5, 2.5, 0))]
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (da ficha) ----------------
CARVAO = (74, 56, 70); CARVAO_ESC = (46, 34, 44); CINZA_ROXO = (108, 90, 106); MALVA = (146, 126, 140)
UNHA = (184, 160, 172); UNHA_CLARA = (214, 196, 204); UNHA_ESC = (150, 126, 140)
BICO = (138, 118, 132); BICO_CLARO = (172, 152, 164); BICO_ESC = (96, 80, 94)
VERM = (214, 40, 36); VERM_ESC = (156, 22, 28); VERM_VIVO = (240, 64, 50); VERM_CLARO = (250, 98, 84)
LARANJA = (246, 120, 24); LARANJA_ESC = (222, 84, 18); AMARELO = (255, 196, 40); AMARELO_CLARO = (255, 230, 120)
CREME = (250, 236, 214)
BRASA_MIOLO = (255, 232, 110); BRASA = (255, 186, 34); BRASA_BORDA = (246, 112, 20)

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

# ---------------- corpo ----------------
VENTRE_Y = 11.4          # abaixo disso o corpo é barriga laranja segmentada

def cor_corpo(p, face):
    x, y, z = p
    if face == "down" or y < VENTRE_Y:
        t = clamp((VENTRE_Y - y) / 2.0)
        base = mix(LARANJA, AMARELO, 0.2 + 0.5 * t)
        if (z + 20) % 2.6 < 0.4: base = mix(base, LARANJA_ESC, 0.8)          # segmentos da barriga
        return base
    if y < VENTRE_Y + 0.7: return mix(LARANJA_ESC, CARVAO, (y - VENTRE_Y) / 0.7)
    return CARVAO

MANCHAS_CORPO = []
for lado in (-1, 1):
    MANCHAS_CORPO += [((1.7 * lado, 20.4, -8.6 + 1.6 * (lado > 0)), 1.0, 1.4),      # dorso
                      ((1.9 * lado, 19.4, -2.6 + 2.4 * (lado > 0)), 1.1, 1.4),
                      ((1.5 * lado, 17.8, 4.6 + 1.8 * (lado > 0)), 0.95, 1.4),
                      ((5.3 * lado, 15.6, -2.4), (1.2, 1.1, 1.3), 1.4),              # flancos
                      ((5.3 * lado, 12.8, 1.4), (0.9, 0.8, 1.0), 1.4),
                      ((5.0 * lado, 15.0, 6.4), (1.0, 1.0, 1.1), 1.4),
                      ((5.4 * lado, 12.6, -8.2), (0.8, 0.8, 0.9), 1.4)]

def mat_placa_ventre(y0, w):
    """Placa da barriga (frente do pescoço): pêssego claro no meio e em cima, laranja nas beiradas e embaixo,
    lados mais escuros para a coluna de placas parecer arredondada."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        v = clamp((y0 - y) / 2.4)                      # 0 em cima .. 1 embaixo
        if face == "down": return LARANJA_ESC
        if face in ("east", "west"): base = mix(LARANJA, LARANJA_ESC, v)
        else:
            u = abs(x) / w
            base = mix(mix(CREME, AMARELO_CLARO, 0.55), LARANJA, clamp(v * 0.9 + u * u * 0.8))
            if face == "up": base = tom(base, 0.15)
        if v > 0.88 or (face == "north" and u > 0.93): base = tom(base, -0.35)
        return base
    return f

# ---------------- cauda em laço ----------------
def mat_rabo(w, h, py, z0, L, k):
    """Segmento da cauda (eixo local +z): dorso de carvão com uma mancha oval em cima e uma de cada lado. Na base
    (k <= 3) o laranja é a barriga (embaixo); no laço, o dorso manchado fica para fora e só uma faixa laranja
    estreita corre por dentro da curva."""
    zc = z0 + L * 0.5
    base = k <= 3
    yd = py + h / 2 if base else py - h / 2                       # face do dorso
    lista = [((0.0, yd, zc), (0.26 * w, 1, 0.36 * L), 1.0)]
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
OLHO_Y = 28.5
FAC_T = 1.4                       # espessura da peça da face diagonal (onde fica o olho)
FAC_L = 3.96                      # comprimento da face diagonal
FAC_M = (3.1, -20.6)              # meio da superfície da face diagonal (lado +x): de (1.7, -22.0) a (4.5, -19.2)
FAC_C = (FAC_M[0] - 0.7071 * FAC_T / 2, FAC_M[1] + 0.7071 * FAC_T / 2)

def cor_cabeca(p, face):
    x, y, z = p
    if face == "up": return MALVA
    return mix(CARVAO, CINZA_ROXO, clamp((y - 25.0) / 5.5))

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

def mat_visor(c):
    """Viseira (testa e sobrancelhas): cinza-malva facetado, mais claro em cima, quinas escurecidas."""
    face = c["face"]
    base = mix(MALVA, (190, 172, 184), 0.4) if face == "up" else CARVAO if face == "down" else \
        mix(CINZA_ROXO, MALVA, 0.55) if face == "north" else mix(CINZA_ROXO, MALVA, 0.3)
    return tom(base, -0.28) if g.na_borda(c) else base

def cor_bico(p, face):
    x, y, z = p
    if face == "up": return BICO_CLARO
    if face in ("east", "west") and abs(z + 23.2) < 0.32 and abs(y - 28.2) < 0.22: return CARVAO_ESC   # narina
    return mix(BICO, BICO_CLARO, clamp((y - 25.5) / 3.5) * 0.6)

# ---------------- crista de brasa ----------------
def mat_crista(c):
    face = c["face"]
    (_, y0, _), (_, y1, _) = c["b"]
    t = clamp((c["p"][1] - y0) / max(y1 - y0, 1e-6))
    if face == "up": base = VERM_CLARO
    elif face == "down": base = VERM_ESC
    elif face == "north": base = mix(VERM, VERM_VIVO, t)
    elif face == "south": base = mix(VERM_ESC, VERM, 0.5 + 0.4 * t)
    else: base = mix(mix(VERM_ESC, VERM, 0.4), VERM, t)
    return tom(base, -0.28) if g.na_borda(c) else base

def bloco_crista(nome, xm, yb, z0, z1, h, inc):
    """Bloco da crista: caixa quase alinhada que inclina 'inc' graus para trás a partir da base, com um degrau
    mais estreito no alto (o 'pixel' chanfrado das fichas)."""
    zc = (z0 + z1) / 2; d = z1 - z0
    return osso(nome, [0, yb, zc], [inc, 0, 0], [
        peca(nome, [-xm, yb, z0], [xm, yb + h - 0.6, z1], mat_crista, res=3),
        peca(nome + "_topo", [-xm + 0.45, yb + h - 0.7, z0 + 0.3], [xm - 0.45, yb + h, z1 - 0.3], mat_crista, res=3)])

# ---------------- placas quentes do ombro (telhas com a fenda em Y) ----------------
FENDA_Y = [((0.2, -0.6), (-1.9, 0.4)), ((-1.9, 0.4), (-4.9, -1.7)), ((-1.9, 0.4), (-4.4, 3.2))]   # (y, z) relativos ao ombro

def mat_telha(P, lado, ponta_y=None):
    """Telha de rocha (carvão facetado) do ombro; a fenda de lava em Y é a mesma para todas as telhas (coordenadas
    do osso do ombro), então ela atravessa as telhas sobrepostas."""
    fora = "east" if lado > 0 else "west"
    def fenda(c):
        if c["face"] != fora: return None
        q = (c["p"][1] - P[1], c["p"][2] - P[2])
        d = min(dist_seg(q, a, b) for a, b in FENDA_Y)
        if d < 0.2: return BRASA_MIOLO
        if d < 0.36: return BRASA
        if d < 0.52: return BRASA_BORDA
        return None
    def f(c):
        cr = fenda(c)
        if cr: return cr
        face = c["face"]
        base = mix(CINZA_ROXO, MALVA, 0.25) if face == "up" else CARVAO_ESC if face == "down" else \
            mix(CARVAO, CINZA_ROXO, 0.45) if face == fora else CARVAO
        (_, y0, _), (_, y1, _) = c["b"]
        base = mix(base, CARVAO, clamp((y1 - c["p"][1]) / max(y1 - y0, 1e-6)) * 0.45)
        return tom(base, -0.38) if g.na_borda(c) else base
    return f, (lambda c, cor: fenda(c) is not None)

def ombro(lado):
    """3-4 escamas escuras sobrepostas como telhas, cruzadas pela fenda em Y; abaixo um tufo de penas de fogo
    (asa dobrada)."""
    s = "d" if lado < 0 else "e"
    P = (5.0 * lado, 20.0, -9.0)
    m, br = mat_telha(P, lado)
    telhas = []
    # (linha, z do centro, largura, altura): fila de cima com 2, fila de baixo com 2 deslocadas (tijolo)
    for k, (fila, zc, W, H) in enumerate([(0, -1.8, 3.8, 3.0), (0, 1.8, 3.8, 3.0), (1, 0.0, 3.8, 3.0), (1, 3.6, 3.6, 2.8)]):
        y1 = P[1] - 2.3 * fila; y0 = y1 - H
        xi = P[0] + lado * (0.35 * fila); xo = xi + lado * 0.9
        x0, x1 = sorted((xi, xo)); z = P[2] + zc
        sq = W / 1.4142 * 0.8
        telhas.append(peca(f"telha{k}_{s}", [x0, y0, z - W / 2], [x1, y1, z + W / 2], m, res=5, brilho=br))
        telhas.append(peca(f"telha{k}_{s}_ponta", [x0 + 0.03, y0 - sq / 2, z - sq / 2], [x1 - 0.03, y0 + sq / 2, z + sq / 2], m,
                           rot=(45, 0, 0), pivo=((x0 + x1) / 2, y0, z), res=5, brilho=br))
    asa = [osso(f"ombro_{s}", list(P), [-14, 0, 24 * lado], telhas)]
    # tufo de penas de fogo por baixo das telhas (vermelho na raiz, laranja, amarelo na ponta)
    for k, (z0, y0, L, W, var, fl, phi, cores) in enumerate([
            (-11.2, 17.4, 7.0, 3.4, 46, 26, -38, (VERM, LARANJA, AMARELO)),
            (-9.4, 17.6, 8.2, 3.6, 56, 22, -18, (VERM_VIVO, LARANJA, AMARELO)),
            (-7.4, 17.8, 8.8, 3.6, 64, 20, 0, (VERM, LARANJA_ESC, AMARELO)),
            (-5.4, 17.8, 8.6, 3.4, 72, 18, 14, (VERM_VIVO, LARANJA, AMARELO)),
            (-3.4, 17.6, 7.6, 3.2, 80, 16, 26, (VERM_ESC, VERM, LARANJA))]):
        raiz = (5.5 * lado, y0, z0)
        asa.append(osso(f"asa_fogo{k}_{s}_giro", list(raiz), [0, -phi * lado, 0],
                        [g.pena_placa(f"asa_fogo{k}_{s}", raiz, (-var, 0, fl * lado), L, W, cores, curva=0.2)]))
    return osso("asa_" + s, [5.0 * lado, 19.0, -8.0], [0, 0, 0], asa)

# ---------------- pernas ----------------
def dedos(nome, xc, zf):
    """3 dedos grandes para a frente (cada um ~1/3 do pé, um cubo de altura, em leque) + 1 curto atrás, malva claro,
    com a ponta (unha) mais clara. Sem sola embaixo."""
    def mat_dedo(z_ponta):
        def f(c):
            face = c["face"]; z = c["p"][2]
            base = UNHA_CLARA if face == "up" else UNHA_ESC if face == "down" else UNHA if face == "north" else mix(UNHA, UNHA_ESC, .35)
            if z < z_ponta and face != "down": base = tom(base, 0.22)           # unha
            return tom(base, -0.3) if g.na_borda(c) else base
        return f
    pp = []
    for k, (dx, giro) in enumerate(((-2.15, 13), (0.0, 0), (2.15, -13))):
        x0 = xc + dx; z0 = zf + 0.9
        pp.append(osso(f"{nome}_dedo{k}", [x0, 0, z0], [0, giro, 0], [
            peca(f"{nome}_dedo{k}", [x0 - 1.0, 0, z0 - 4.3], [x0 + 1.0, 2.5, z0], mat_dedo(z0 - 3.5), res=3)]))
    pp.append(peca(nome + "_dedo_tras", [xc - 0.85, 0, zf + 0.6], [xc + 0.85, 1.7, zf + 2.9], mat_dedo(-999), res=3))
    return pp

def perna(nome, xc, zc, tras):
    lado = -1 if xc < 0 else 1
    pp = []
    escuro = g.mat_cor(lambda p, f: CARVAO, borda=.06, curva=.4)
    if tras:
        # coxa grossa inclinada para trás; o joelho fica atrás do quadril e a canela desce dali
        lista = [((xc + 2.9 * lado, 12.4, zc), (1, 1.15, 1.35), 1.4)]
        pp += g.arredondado2(nome + "_coxa", [xc - 2.9, 7.6, zc - 3.8], [xc + 2.9, 16.0, zc + 3.6],
                             mat_com_manchas(lambda p, f: CARVAO, lista, borda=.04, curva=.4), r=1.6, brilho=brilho_manchas(lista),
                             rot=(-20, 0, 6 * lado), pivo=(xc, 15.6, zc))
        zp = zc + 2.6
        yt = 8.6
    else:
        pp += g.arredondado2(nome + "_braco", [xc - 2.4, 9.2, zc - 2.6], [xc + 2.4, 13.6, zc + 2.6], escuro, r=1.3,
                             rot=(0, 0, 10 * lado), pivo=(xc, 9.2, zc))
        zp = zc
        yt = 10.6
    # faixa laranja (mais larga em cima), tornozelo de carvão
    mo = g.mat_cor(lambda p, f: mix(LARANJA_ESC, AMARELO, clamp((p[1] - 5.0) / (yt - 5.0))), borda=.08, curva=.3)
    ym = (5.0 + yt) / 2 + 0.4
    pp += g.octogono(nome + "_canela", [xc - 2.45, ym - 0.2, zp - 2.45], [xc + 2.45, yt, zp + 2.45], mo, r=0.8)
    pp += g.octogono(nome + "_canela2", [xc - 2.05, 4.8, zp - 2.05], [xc + 2.05, ym, zp + 2.05], mo, r=0.7)
    pp += g.octogono(nome + "_tornozelo", [xc - 1.85, 2.2, zp - 1.85], [xc + 1.85, 5.0, zp + 1.85],
                     g.mat_cor(lambda p, f: CARVAO, borda=.1, curva=.4), r=0.6)
    pp += dedos(nome, xc, zp)
    return osso(nome, [xc, 14.0, zc], [0, 0, 0], pp)

# ---------------- montagem ----------------
def montar():
    # ---------- cabeça em cunha: viseira contínua, bochechas mais estreitas, bico comprido com gancho ----------
    i_cab = len(g.PECAS)
    cab = []
    mcab = g.mat_cor(cor_cabeca, borda=.04, curva=.3)
    fx = (24.8, 33.2)
    cab += g.arredondado2("cranio", [-4.4, 26.0, -19.8], [4.4, 31.4, -15.0], mcab, r=1.0, faixa=fx, res=3)
    cab.append(peca("cranio_frente", [-1.7, 25.8, -22.0], [1.7, 31.0, -19.4], mcab, faixa=fx, res=3))
    cab.append(peca("bochecha", [-3.2, 25.0, -20.3], [3.2, 26.8, -15.6], mcab, faixa=fx, res=3))
    cab.append(peca("queixo", [-2.6, 24.6, -20.6], [2.6, 25.4, -16.2], g.mat_cor(lambda p, f: tom(CARVAO, -0.1), borda=.1), faixa=fx))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 26.3, cz - FAC_L / 2], [cx + FAC_T / 2, 31.0, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, 28.5, cz), faixa=fx, res=8))
    # viseira contínua: placa da testa (com degrau em cima) e as sobrancelhas em V presas na frente dela
    cab += g.arredondado("viseira", [-4.6, 30.2, -22.6], [4.6, 31.9, -14.8], mat_visor, r=0.45, rot=(-5, 0, 0), pivo=(0, 31.9, -14.8), res=3)
    cab.append(peca("viseira_topo", [-3.4, 31.8, -21.4], [3.4, 32.4, -15.2], mat_visor, rot=(-5, 0, 0), pivo=(0, 31.9, -14.8), res=3))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        x0, x1 = sorted((-0.3 * lado, 4.5 * lado))
        cab.append(peca("sobrancelha_" + s, [x0, 29.4, -22.85], [x1, 30.6, -19.6], mat_visor, rot=(0, 0, 13 * lado),
                        pivo=(4.5 * lado, 30.6, -21.0), res=3))
    # bico malva comprido (~2/3 da cabeça), com cume claro, cunha em V embaixo e gancho para baixo
    mb = g.mat_cor(cor_bico, borda=.05, curva=.35)
    fb = (24.6, 29.8)
    # de frente o bico é um triângulo em degraus (cada degrau mais estreito e mais curto) com o gancho na ponta
    for k, (xm, y0, y1, zf) in enumerate([(1.8, 28.0, 29.6, -26.0), (1.3, 26.9, 28.2, -25.4), (0.75, 25.8, 27.1, -24.6)]):
        cab.append(peca(f"bico{k}", [-xm, y0, zf], [xm, y1, -21.6], mb, rot=(-10, 0, 0), pivo=(0, 29.6, -21.6), faixa=fb))
    cab.append(peca("bico_gancho", [-0.6, 26.5, -26.15], [0.6, 28.1, -25.3], g.mat_cor(lambda p, f: tom(BICO, -0.1), borda=.08, curva=.6),
                    rot=(-10, 0, 0), pivo=(0, 29.6, -21.6), faixa=fb))
    cab.append(peca("bico_baixo", [-1.1, 24.9, -24.4], [1.1, 25.8, -21.6], g.mat_cor(lambda p, f: BICO_ESC, borda=.1)))
    # crista de brasa: 5 blocos da testa à nuca, cada um mais alto e mais atrás, todos inclinados ~25° para trás
    crista = []
    for k, (xm, z0, z1, h) in enumerate([(2.6, -22.2, -18.6, 3.2), (2.35, -20.6, -17.0, 4.6), (2.1, -19.0, -15.4, 5.8),
                                         (1.85, -17.4, -13.8, 6.4)]):
        crista.append(bloco_crista(f"crista{k}", xm, 31.9, z0, z1, h, 25))
    cab.append(osso("crista", [0, 32.0, -18], [0, 0, 0], crista))
    # pelagem ígnea: juba densa em volta das bochechas e da garganta, emoldurando o rosto, apontando para baixo/trás
    CAMADAS = [  # (y, raio x, raio z, z centro, abertura, varrida, comprimento, largura, cores, phis)
        (29.4, 4.4, 1.6, -16.4, 30, 52, 5.0, 3.0, (VERM, VERM_VIVO, LARANJA), [0, 40, 84]),
        (27.2, 4.3, 2.2, -16.8, 24, 38, 6.0, 3.2, (VERM, LARANJA, AMARELO), [-30, 5, 40, 84]),
        (25.0, 3.8, 3.4, -17.6, 18, 22, 6.4, 3.4, (VERM_VIVO, LARANJA, AMARELO), [-62, -40, -12, 20, 55, 88]),
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

    # ---------- pescoço em S, com as placas da barriga subindo até embaixo do bico ----------
    pesc = []
    mpe = g.mat_cor(lambda p, f: CARVAO, borda=.04, curva=.3)
    pesc += g.octogono("pescoco_baixo", [-3.3, 16.5, -15.8], [3.3, 23.0, -9.8], mpe, r=1.0, faixa=(15, 27),
                       rot=(-28, 0, 0), pivo=(0, 16.5, -12.8))
    pesc += g.octogono("pescoco_alto", [-3.0, 21.0, -19.0], [3.0, 27.0, -13.6], mpe, r=0.9, faixa=(15, 27),
                       rot=(6, 0, 0), pivo=(0, 21.0, -16.3))
    PTS = [(25.4, -20.4), (22.0, -19.6), (18.0, -17.8), (15.0, -15.6), (11.0, -14.9)]
    def frente(y):   # linha da frente do pescoço e do peito
        for (ya, za), (yb, zb) in zip(PTS, PTS[1:]):
            if y >= yb: return za + (zb - za) * (ya - y) / (ya - yb)
        return PTS[-1][1]
    for k in range(7):
        y0 = 25.2 - 2.1 * k
        zf = frente(y0 - 1.2) - 0.4
        w = 2.2 + 0.26 * k
        pesc.append(peca(f"placa_ventre{k}", [-w, y0 - 2.4, zf], [w, y0, zf + 1.5], mat_placa_ventre(y0, w),
                         rot=(-6 if y0 > 16 else 6, 0, 0), pivo=(0, y0, zf + 0.75)))
    # penas do pescoço logo abaixo da juba da cabeça (só dos lados e atrás: a frente mostra as placas)
    juba = []
    for k, phi in enumerate((-48, -16, 18, 52)):
        for lado in (-1, 1):
            x, z = anel(3.9, 3.4, -14.6, phi, lado)
            nome = f"juba_pesc{k}_{'d' if lado < 0 else 'e'}"
            if -30 < phi < 30:
                juba.append(g.pena_cruzada(nome, (x, 23.4, z), (-22, 0, 14 * lado), 5.4, 3.2, (LARANJA_ESC, LARANJA, AMARELO), curva=0.15 * lado))
            else:
                juba.append(g.pena_cone_placa(nome, (x, 23.4, z), phi, 14, 5.4, 3.2, (LARANJA_ESC, LARANJA, AMARELO), lado, varre=20,
                                              curva=0.2 * lado))
    pesc.append(osso("juba", [0, 23, -14], [0, 0, 0], juba))
    pesc.append(cabeca)
    pescoco = osso("pescoco", [0, 18.0, -12.5], [0, 0, 0], pesc)

    # ---------- tronco de salamandra (mais curto, o dorso sobe para o pescoço) ----------
    corpo = []
    mt = mat_com_manchas(cor_corpo, MANCHAS_CORPO, borda=.03, curva=.5)
    bt = brilho_manchas(MANCHAS_CORPO)
    fc = (9.0, 20.6)
    corpo += g.arredondado2("peito", [-5.4, 9.8, -14.4], [5.4, 20.4, -4.0], mt, r=2.6, faixa=fc, brilho=bt)
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

    pernas = [perna("perna_fd", -5.8, -9.6, False), perna("perna_fe", 5.8, -9.6, False),
              perna("perna_td", -5.7, 3.8, True), perna("perna_te", 5.7, 3.8, True)]
    return [tronco] + pernas

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
