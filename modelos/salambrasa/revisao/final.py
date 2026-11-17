"""Salambrasa (#012, Fogo): o galo-salamandra das brasas, quadrúpede de carvão com manchas incandescentes."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, anel

ID = "salambrasa"; NOME = "Salambrasa"; NUMERO = 12
ALTURA = 2.45
QUADRUPEDE = True
ROSTO = ((0, 27.4, -20.0), 10.5)
ONDAS = [("rabo", 12, (1.5, 2.5, 0))]
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (da ficha) ----------------
CARVAO = (74, 56, 70); CARVAO_ESC = (46, 34, 44); CINZA_ROXO = (108, 90, 106); MALVA = (146, 126, 140)
TOPO_CAB = (58, 46, 51)                                    # alto da cabeça, carvão escuro
SOBRAN = (96, 80, 92); SOBRAN_CLARA = (122, 104, 116)      # sobrancelha / viseira
DEDO = (184, 168, 176); DEDO_CLARO = (212, 200, 206); DEDO_ESC = (146, 130, 140)
BICO = (146, 128, 138); BICO_CLARO = (172, 154, 164); BICO_ESC = (104, 88, 98)
CRISTA = (216, 48, 42); CRISTA_ESC = (158, 29, 29); CRISTA_CLARA = (242, 92, 76)
VERM = (214, 40, 36); VERM_ESC = (156, 22, 28); VERM_VIVO = (240, 64, 50)
LARANJA = (246, 120, 24); LARANJA_ESC = (222, 84, 18); AMARELO = (255, 196, 40); AMARELO_CLARO = (255, 230, 120)
CREME = (250, 236, 214)
BRASA_MIOLO = (255, 232, 110); BRASA = (255, 186, 34); BRASA_BORDA = (246, 112, 20)
FENDA = (255, 120, 30)

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

MANCHAS_CORPO = [((0, 20.4, -8.4), 1.5, 1.4), ((0, 19.4, 0.4), 1.6, 1.4), ((0, 17.8, 6.8), 1.3, 1.4)]   # dorso: grandes
for lado in (-1, 1):
    MANCHAS_CORPO += [((2.6 * lado, 19.4, -3.6), 1.1, 1.4), ((2.4 * lado, 17.8, 4.0), 1.0, 1.4),     # dorso: em volta
                      ((5.3 * lado, 13.6, -1.8), (1.2, 1.1, 1.3), 1.4),                               # flancos
                      ((5.3 * lado, 12.4, 2.8), (0.9, 0.85, 1.0), 1.4),
                      ((5.0 * lado, 15.2, 6.6), (1.1, 1.0, 1.1), 1.4),
                      ((5.0 * lado, 12.4, 8.0), (0.8, 0.8, 0.9), 1.4),
                      ((5.4 * lado, 15.2, -11.6), (0.9, 0.9, 1.0), 1.4)]

def mat_placa_ventre(y0, w, alto=2.0):
    """Placa da barriga (pescoço e peito): pêssego claro no meio e em cima, laranja nas beiradas e embaixo, linha
    escura na beirada de baixo: a fileira de placas fica segmentada e arredondada."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        v = clamp((y0 - y) / alto)                     # 0 em cima .. 1 embaixo
        if face == "down": return LARANJA_ESC
        if face in ("east", "west"): base = mix(LARANJA, LARANJA_ESC, v)
        else:
            u = abs(x) / w
            base = mix(mix(CREME, AMARELO_CLARO, 0.55), LARANJA, clamp(v * 0.9 + u * u * 0.8))
            if face == "up": base = tom(base, 0.15)
        if v > 0.86 or (face == "north" and u > 0.92): base = tom(base, -0.35)
        return base
    return f

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
    return mat_com_manchas(cor, lista, borda=.0, curva=.4), brilho_manchas(lista)

def secao(nome, px, py, z0, z1, w, h, mat, br, **kw):
    """Seção arredondada ao longo de z: 3 blocos (cruz + miolo chanfrado)."""
    r = 0.3 * min(w, h); q = r / 2
    fx = (py - h / 2, py + h / 2)
    return [peca(nome + "_a", [px - w / 2, py - h / 2 + r, z0], [px + w / 2, py + h / 2 - r, z1], mat, faixa=fx, brilho=br, res=3, **kw),
            peca(nome + "_b", [px - w / 2 + r, py - h / 2, z0], [px + w / 2 - r, py + h / 2, z1], mat, faixa=fx, brilho=br, res=3, **kw),
            peca(nome + "_c", [px - w / 2 + q, py - h / 2 + q, z0], [px + w / 2 - q, py + h / 2 - q, z1], mat, faixa=fx, brilho=br, res=3, **kw)]

def cauda_laco(nome, base, segs):
    """Cadeia como a pena_curva (ossos '<nome>_0', '<nome>_1'...), mas com giro próprio em cada junta, para a cauda
    poder correr reta para trás e depois enrolar num laço. segs = [(comprimento, largura, altura, rx)].
    Cada segmento tem seção arredondada; em cada junta um 'anel' girado pela metade do ângulo (na bissetriz) tapa o
    vão do lado de fora da curva, e a ponta termina num toco arredondado: a cauda afina sem degraus."""
    def seg(k, pos):
        L, w, h, rx = segs[k]
        px, py, pz = pos
        mat, br = mat_rabo(w, h, py, pz, L, k)
        filhos = secao(f"{nome}_{k}", px, py, pz - (0.6 if k == 0 else 0.3), pz + L, w, h, mat, br)
        if k > 0:   # anel da junta, na média das larguras, girado de volta pela metade do ângulo
            wp, hp = (segs[k - 1][1] + w) / 2, (segs[k - 1][2] + h) / 2
            e = 0.5 + (hp / 2) * math.tan(math.radians(abs(rx) / 2))
            filhos += secao(f"{nome}_{k}_junta", px, py, pz - e, pz + e, wp, hp, mat, br, rot=(-rx / 2, 0, 0), pivo=(px, py, pz))
        if k + 1 < len(segs): filhos.append(seg(k + 1, (px, py, pz + L)))
        else:       # toco arredondado na ponta
            filhos += secao(f"{nome}_ponta", px, py, pz + L - 0.2, pz + L + 1.0, w * 0.72, h * 0.72, mat, br)
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
    """Sobrancelha grossa (viseira) sobre os olhos: malva-carvão, mais clara em cima."""
    face = c["face"]
    base = TOPO_CAB if face == "up" else CARVAO_ESC if face == "down" else \
        mix(SOBRAN, SOBRAN_CLARA, 0.35) if face == "north" else SOBRAN
    return tom(base, -0.2) if g.na_borda(c) else base

def mat_bico(c):
    """Bico malva-acinzentado mais claro que a cabeça: claro em cima, sombra embaixo, narina escura."""
    face = c["face"]; x, y, z = c["p"]
    if face in ("east", "west") and abs(z + 23.0) < 0.3 and abs(y - 28.3) < 0.2: return CARVAO_ESC
    base = BICO_CLARO if face == "up" else BICO_ESC if face == "down" else mix(tom(BICO, -0.1), BICO, clamp((y - 26.0) / 3.0))
    return tom(base, -0.06) if g.na_borda(c) else base

# ---------------- crista de brasa ----------------
def mat_crista(c):
    """Vermelho liso: base mais escura, alto mais claro, face de cima clara (sem molduras desenhadas)."""
    face = c["face"]
    (_, y0, _), (_, y1, _) = c["b"]
    t = clamp((c["p"][1] - y0) / max(y1 - y0, 1e-6))
    if face == "up": return CRISTA_CLARA
    if face == "down": return CRISTA_ESC
    base = mix(CRISTA_ESC, CRISTA, clamp((t - 0.12) * 2.2))       # base escura: cada telha se destaca da da frente
    if t > 0.7: base = mix(base, CRISTA_CLARA, (t - 0.7) / 0.3 * 0.55)
    if face in ("east", "west"): base = tom(base, -0.08)
    return base

def telha_crista(nome, xm, yb, z0, z1, h, inc):
    """'Telha' da crista: bloco que nasce atrás da viseira e inclina 'inc' graus para trás a partir da base."""
    zc = (z0 + z1) / 2
    return osso(nome, [0, yb, zc], [inc, 0, 0], [peca(nome, [-xm, yb, z0], [xm, yb + h, z1], mat_crista, res=3)])

# ---------------- ombro: escamas escuras com a fenda em Y + leque de penas ----------------
FENDA_Y = [((0.2, -1.2), (-2.2, 0.4)), ((-2.2, 0.4), (-5.6, -0.8)), ((-2.2, 0.4), (-4.4, 4.2))]   # (y, z) relativos ao ombro

def mat_escama(P, lado):
    """Escama de carvão do ombro; a fenda em Y (fina, cheia, amarela-laranja, sem contorno) é desenhada nas
    coordenadas do osso do ombro, então atravessa as escamas sobrepostas."""
    fora = "east" if lado > 0 else "west"
    def fenda(c):
        if c["face"] != fora: return None
        q = (c["p"][1] - P[1], c["p"][2] - P[2])
        d = min(dist_seg(q, a, b) for a, b in FENDA_Y)
        if d < 0.24: return BRASA_MIOLO
        if d < 0.42: return BRASA
        if d < 0.58: return FENDA
        return None
    def f(c):
        cr = fenda(c)
        if cr: return cr
        face = c["face"]
        base = mix(CARVAO, CINZA_ROXO, 0.5) if face == "up" else CARVAO_ESC if face == "down" else \
            mix(CARVAO, CINZA_ROXO, 0.3) if face == fora else CARVAO
        (_, y0, _), (_, y1, _) = c["b"]
        base = mix(base, CARVAO_ESC, clamp((y1 - c["p"][1]) / max(y1 - y0, 1e-6)) * 0.3)
        return tom(base, -0.3) if g.na_borda(c) else base
    return f, (lambda c, cor: fenda(c) is not None)

def ombro(lado):
    """3-4 escamas de carvão sobrepostas no ombro (como coberteiras), cruzadas por uma fenda fina em Y; atrás e
    embaixo, um leque de 6 lâminas de pena vermelho-laranja apontando para trás/baixo até o meio do flanco."""
    s = "d" if lado < 0 else "e"
    P = (4.9 * lado, 21.0, -10.4)
    m, br = mat_escama(P, lado)
    escamas = []
    for k, (dy, dz, W, H) in enumerate([(0.0, 0.0, 4.2, 3.4), (-1.5, 2.2, 4.0, 3.4), (-3.0, 4.2, 3.8, 3.2), (-1.8, -1.6, 3.4, 3.0)]):
        y1 = P[1] + dy; y0 = y1 - H; z = P[2] + dz
        xi = P[0] + lado * (0.28 * k); xo = xi + lado * 0.7
        x0, x1 = sorted((xi, xo)); sq = W / 1.4142 * 0.72
        escamas.append(peca(f"escama{k}_{s}", [x0, y0, z - W / 2], [x1, y1, z + W / 2], m, res=5, brilho=br))
        escamas.append(peca(f"escama{k}_{s}_ponta", [x0 + 0.03, y0 - sq / 2, z - sq / 2], [x1 - 0.03, y0 + sq / 2, z + sq / 2], m,
                            rot=(45, 0, 0), pivo=((x0 + x1) / 2, y0, z), res=5, brilho=br))
    asa = [osso(f"ombro_{s}", list(P), [-6, 0, 30 * lado], escamas)]
    cores = [(VERM, VERM_VIVO, LARANJA), (VERM_ESC, VERM, LARANJA_ESC), (VERM, LARANJA_ESC, LARANJA)]
    for k in range(6):
        raiz = (5.6 * lado, 17.6 - 0.15 * k, -10.4 + 1.6 * k)
        asa.append(g.pena_placa(f"asa{k}_{s}", raiz, (-(56 + 5 * k), 0, 14 * lado), 7.6 - 0.25 * abs(k - 2), 3.2, cores[k % 3], curva=0.25))
    return osso("asa_" + s, [5.0 * lado, 19.0, -8.0], [0, 0, 0], asa)

# ---------------- pernas ----------------
def dedos(nome, xc, zf):
    """3 dedos grandes cinza-claros e chanfrados para a frente, em leque, + 1 menor atrás."""
    def mat_dedo(z_ponta):
        def f(c):
            face = c["face"]; z = c["p"][2]
            base = DEDO_CLARO if face == "up" else DEDO_ESC if face == "down" else DEDO if face == "north" else mix(DEDO, DEDO_ESC, .3)
            if z < z_ponta and face != "down": base = tom(base, 0.15)           # unha
            return tom(base, -0.2) if g.na_borda(c) else base
        return f
    pp = []
    for k, (dx, giro) in enumerate(((-2.2, 13), (0.0, 0), (2.2, -13))):
        x0 = xc + dx; z0 = zf + 1.0
        pp.append(osso(f"{nome}_dedo{k}", [x0, 0, z0], [0, giro, 0],
                       g.arredondado(f"{nome}_dedo{k}", [x0 - 1.05, 0, z0 - 4.2], [x0 + 1.05, 2.4, z0], mat_dedo(z0 - 3.4), r=0.4, res=3)))
    pp.append(peca(nome + "_dedo_tras", [xc - 0.8, 0, zf + 0.8], [xc + 0.8, 1.6, zf + 2.9], mat_dedo(-999), res=3))
    return pp

def perna(nome, xc, zc, tras):
    """Pernas curtas: coxa arredondada de carvão (pouco mais larga que a canela), faixa laranja -> amarelo no
    joelho/canela, tornozelo escuro e dedos."""
    lado = -1 if xc < 0 else 1
    pp = []
    escuro = g.mat_cor(lambda p, f: CARVAO, borda=.04, curva=.4)
    if tras:
        pp += g.arredondado2(nome + "_coxa", [xc - 2.6, 5.6, zc - 3.4], [xc + 2.6, 13.2, zc + 3.2], escuro, r=1.5,
                             rot=(-20, 0, 6 * lado), pivo=(xc, 12.6, zc))
        zp = zc + 2.4
    else:
        pp += g.arredondado2(nome + "_braco", [xc - 2.4, 5.8, zc - 2.5], [xc + 2.4, 11.6, zc + 2.5], escuro, r=1.3,
                             rot=(0, 0, 8 * lado), pivo=(xc, 6.0, zc))
        zp = zc
    mo = g.mat_cor(lambda p, f: mix(LARANJA_ESC, AMARELO, clamp((p[1] - 3.8) / 3.0)), borda=.05, curva=.3)
    pp += g.octogono(nome + "_canela", [xc - 2.15, 3.7, zp - 2.15], [xc + 2.15, 6.8, zp + 2.15], mo, r=0.75)
    pp += g.octogono(nome + "_tornozelo", [xc - 1.85, 1.9, zp - 1.85], [xc + 1.85, 4.0, zp + 1.85], escuro, r=0.65)
    pp += dedos(nome, xc, zp)
    return osso(nome, [xc, 11.6, zc], [0, 0, 0], pp)

# ---------------- montagem ----------------
def montar():
    # ---------- cabeça: alto escuro, viseira rente aos lados, bochecha em degrau, queixo, bico em cunha ----------
    i_cab = len(g.PECAS)
    cab = []
    mcab = g.mat_cor(cor_cabeca, borda=.03, curva=.3)
    fx = (24.4, 31.6)
    cab += g.arredondado2("cranio", [-4.4, 26.0, -19.8], [4.4, 31.4, -15.0], mcab, r=1.0, faixa=fx, res=3)
    cab.append(peca("cranio_frente", [-1.7, 25.8, -22.0], [1.7, 31.0, -19.4], mcab, faixa=fx, res=3))
    cab += g.arredondado("bochecha", [-3.3, 24.8, -20.2], [3.3, 26.6, -15.6], mcab, r=0.6, faixa=fx, res=3)
    cab.append(peca("queixo", [-2.3, 24.2, -20.0], [2.3, 25.0, -16.4], g.mat_cor(lambda p, f: CARVAO, borda=.06), faixa=fx))
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 26.3, cz - FAC_L / 2], [cx + FAC_T / 2, 31.0, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, 28.4, cz), faixa=fx, res=8))
        # sobrancelha grossa sobre o olho, descendo para o bico (V bravo), rente ao lado da cabeça
        x0, x1 = sorted((0.0, 4.3 * lado))
        cab.append(peca("sobrancelha_" + s, [x0, 29.3, -22.9], [x1, 31.2, -18.8], mat_sobrancelha, rot=(0, 0, 13 * lado),
                        pivo=(4.3 * lado, 31.2, -21.0), res=3))
    # bico: cunha maciça e clara logo abaixo da viseira (de frente um trapézio que estreita para baixo), afinando para
    # a frente e terminando num gancho; mandíbula de baixo menor e recuada
    cab.append(peca("bico_base", [-1.9, 28.0, -23.4], [1.9, 29.4, -21.8], mat_bico, res=4))
    cab.append(peca("bico_base2", [-1.4, 26.6, -23.1], [1.4, 28.1, -21.8], mat_bico, res=4))
    cab.append(peca("bico_meio", [-1.35, 27.2, -24.7], [1.35, 29.0, -23.1], mat_bico, rot=(-10, 0, 0), pivo=(0, 29.0, -23.1), res=4))
    cab.append(peca("bico_gancho", [-0.85, 26.5, -25.6], [0.85, 28.5, -24.5], mat_bico, rot=(-20, 0, 0), pivo=(0, 28.5, -24.5), res=4))
    cab.append(peca("bico_baixo", [-1.0, 25.8, -23.4], [1.0, 26.7, -21.8], g.mat_cor(lambda p, f: BICO_ESC, borda=.08), res=4))
    # crista: 6 'telhas' vermelhas que nascem atrás da viseira, cada uma mais para trás e mais inclinada; o contorno
    # do alto fica arredondado e, de frente, ela afina para cima (1/2 a 2/3 da largura da cabeça)
    crista = []
    for k, (xm, z0, h, inc) in enumerate([(4.2, -20.8, 3.4, 6), (3.7, -19.6, 4.4, 16), (3.1, -18.4, 5.2, 26),
                                           (2.7, -17.2, 5.6, 36), (2.3, -16.0, 5.4, 46), (2.0, -15.0, 4.6, 56)]):
        crista.append(telha_crista(f"crista{k}", xm, 30.3, z0, z0 + 2.6, h, inc))
    cab.append(osso("crista", [0, 31.0, -18], [0, 0, 0], crista))
    # pelagem ígnea: algumas penas das bochechas varrendo para trás e a 'barba + gola' em volta da garganta
    CAMADAS = [  # (y, raio x, raio z, z centro, abertura, varrida, comprimento, largura, cores, phis)
        (28.8, 4.3, 1.8, -16.6, 30, 52, 5.0, 3.0, (VERM, VERM_VIVO, LARANJA), [5, 45, 88]),
        (26.2, 3.9, 2.6, -17.2, 22, 36, 6.0, 3.2, (VERM, LARANJA, AMARELO), [-20, 20, 58, 88]),
        (24.8, 3.4, 3.4, -18.0, 16, 14, 6.4, 3.4, (VERM_VIVO, LARANJA, AMARELO), [-72, -46, -16, 22, 60]),
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

    # ---------- pescoço em S (~60% da largura da cabeça), placas laranja segmentadas na garganta ----------
    pesc = []
    mpe = g.mat_cor(lambda p, f: CARVAO, borda=.03, curva=.3)
    PESC = [  # (nome, x, y0, y1, z0, z1, giro, pivô)
        ("pescoco_baixo", 2.8, 16.0, 22.6, -15.4, -9.8, -28, (0, 16.0, -12.6)),
        ("pescoco_alto", 2.6, 21.2, 26.8, -18.4, -13.6, -12, (0, 21.2, -16.0)),
    ]
    for nome, xm, y0, y1, z0, z1, giro, pv in PESC:
        pesc += g.octogono(nome, [-xm, y0, z0], [xm, y1, z1], mpe, r=0.9, faixa=(15, 27), rot=(giro, 0, 0), pivo=pv)
        # placas arredondadas e segmentadas, rentes à frente do pescoço (mesmo giro da peça)
        n = 3
        for k in range(n):
            ya = y1 - 0.3 - k * (y1 - y0 - 0.4) / n; yb = ya - (y1 - y0 - 0.4) / n - 0.25
            w = xm - 0.5 + 0.15 * k
            pesc.append(peca(f"{nome}_placa{k}", [-w, yb, z0 - 0.55], [w, ya, z0 + 0.4], mat_placa_ventre(ya, w, ya - yb),
                             rot=(giro, 0, 0), pivo=pv))
    # gola: penas em volta da base da garganta, por cima do peito
    gola = []
    for k, phi in enumerate((-66, -40, -12, 18, 50, 84)):
        for lado in (-1, 1):
            if phi >= 84 and lado < 0: continue
            x, z = anel(3.3, 3.2, -15.8, phi, lado)
            if phi >= 84: x = 0
            nome = f"gola{k}_{'d' if lado < 0 else 'e'}"
            cores = (VERM, LARANJA, AMARELO) if k % 2 else (LARANJA_ESC, LARANJA, AMARELO)
            if -30 < phi < 30:
                gola.append(g.pena_cruzada(nome, (x, 22.6, z), (-14, 0, 16 * lado), 5.8, 3.2, cores, curva=0.15 * lado))
            else:
                gola.append(g.pena_cone_placa(nome, (x, 22.6, z), phi, 16, 5.8, 3.2, cores, lado, varre=10 if phi < 80 else 0,
                                              curva=0.2 * lado))
    pesc.append(osso("juba", [0, 22.6, -15.8], [0, 0, 0], gola))
    pesc.append(cabeca)
    pescoco = osso("pescoco", [0, 18.0, -12.5], [0, 0, 0], pesc)

    # ---------- tronco de salamandra (curto, dorso largo e arredondado subindo para o pescoço) ----------
    corpo = []
    mt = mat_com_manchas(cor_corpo, MANCHAS_CORPO, borda=.02, curva=.5)
    bt = brilho_manchas(MANCHAS_CORPO)
    fc = (9.0, 20.6)
    corpo += g.arredondado2("peito", [-5.4, 9.8, -15.0], [5.4, 20.4, -4.0], mt, r=2.6, faixa=fc, brilho=bt)
    corpo += g.arredondado2("meio", [-5.3, 9.6, -6.0], [5.3, 19.4, 3.0], mt, r=2.6, faixa=fc, brilho=bt)
    corpo += g.arredondado2("quadril", [-5.0, 9.8, 1.0], [5.0, 17.8, 9.4], mt, r=2.6, faixa=fc, brilho=bt)
    # placas do peito entre as patas da frente (continuam as do pescoço)
    for k, (ya, w) in enumerate([(17.0, 2.8), (14.8, 3.1), (12.6, 3.3)]):
        corpo.append(peca(f"placa_peito{k}", [-w, ya - 2.4, -15.5], [w, ya, -14.6], mat_placa_ventre(ya, w, 2.4), rot=(8, 0, 0),
                          pivo=(0, ya, -15.0)))
    corpo += [ombro(-1), ombro(1)]
    # cauda grossa na base, afinando sem parar até a ponta arredondada, que enrola num laço e cai um pouco no fim
    Ls = [4.2, 4.1, 4.0, 3.9, 3.8, 3.7, 3.6, 3.5, 3.4, 3.3, 3.2, 3.1]
    Rs = [14, -4, -16, -28, -32, -28, -16, -24, -32, -26, -6, 12]
    Hs = [7.4, 7.0, 6.5, 6.0, 5.6, 5.2, 4.8, 4.4, 4.0, 3.6, 3.2, 2.8]
    Ws = [9.4, 9.2, 8.9, 8.5, 8.0, 7.4, 6.8, 6.1, 5.4, 4.6, 3.8, 3.1]
    corpo.append(osso("cauda", [0, 14.2, 7.5], [0, 0, 0], [cauda_laco("rabo", (0, 14.2, 7.5), list(zip(Ls, Ws, Hs, Rs)))]))
    corpo.append(pescoco)
    tronco = osso("corpo", [0, 13.0, 6.0], [0, 0, 0], corpo)
    g.transformar(0, [tronco], (0, 0, 0), k=1.0, sobe=-DESCE)        # corpo mais baixo: pernas ~25% mais curtas

    pernas = [perna("perna_fd", -6.3, -9.8, False), perna("perna_fe", 6.3, -9.8, False),
              perna("perna_td", -6.1, 3.8, True), perna("perna_te", 6.1, 3.8, True)]
    return [tronco] + pernas

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
