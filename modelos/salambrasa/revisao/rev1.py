"""Salambrasa (#012, Fogo): o galo-salamandra das brasas, quadrúpede de carvão com manchas incandescentes."""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import galo_base as g
from galo_base import peca, osso, mix, tom, clamp, anel

ID = "salambrasa"; NOME = "Salambrasa"; NUMERO = 12
ALTURA = 2.45
QUADRUPEDE = True
ROSTO = ((0, 28.4, -20.5), 8.5)
ONDAS = [("rabo", 12, (1.5, 2.5, 0))]
ANIM_PARADO = {}
ANIM_ANDANDO = {}

# ---------------- paleta (da ficha) ----------------
CARVAO = (74, 56, 70); CARVAO_ESC = (46, 34, 44); CINZA_ROXO = (108, 90, 106); MALVA = (146, 126, 140)
UNHA = (178, 156, 166); UNHA_CLARA = (206, 188, 196)
BICO = (128, 112, 124); BICO_CLARO = (160, 144, 154)
VERM = (214, 40, 36); VERM_ESC = (156, 22, 28); VERM_VIVO = (240, 64, 50); VERM_CLARO = (250, 98, 84)
LARANJA = (246, 120, 24); LARANJA_ESC = (222, 84, 18); AMARELO = (255, 196, 40); AMARELO_CLARO = (255, 230, 120)
CREME = (250, 236, 214)
BRASA_MIOLO = (255, 232, 110); BRASA = (255, 186, 34); BRASA_BORDA = (246, 112, 20)

# ---------------- manchas incandescentes (decalque 3D em octógono) ----------------
def mancha(p, face, lista):
    """Cor da mancha incandescente no ponto (ou None). lista = [((cx, cy, cz), raio, profundidade)]. O desenho é um
    octógono na face (como as manchas da ficha): miolo claro, corpo amarelo e beirada laranja. Só aparece nas faces
    a menos de 'profundidade' do centro (para não vazar para as faces de trás)."""
    x, y, z = p
    for (cx, cy, cz), r, prof in lista:
        dx, dy, dz = x - cx, y - cy, z - cz
        if face in ("east", "west"): a, b, n = dz, dy, dx
        elif face in ("north", "south"): a, b, n = dx, dy, dz
        else: a, b, n = dx, dz, dy
        if abs(n) > prof: continue
        d = max(abs(a), abs(b), (abs(a) + abs(b)) / 1.38) / r
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
    MANCHAS_CORPO += [((5.4 * lado, 15.0, 0.5), 1.2, 1.3), ((5.0 * lado, 15.6, 7.0), 1.0, 1.3),
                      ((2.4 * lado, 19.0, 2.0 + 4.5 * (lado > 0)), 1.1, 1.3), ((5.6 * lado, 12.8, -4.2), 0.9, 1.3)]
MANCHAS_CORPO += [((0, 17.8, 10.2), 0.9, 1.3), ((0, 19.2, -2.6), 1.0, 1.3)]

def mat_placa_ventre(y0, w):
    """Placa da barriga (frente do pescoço): pêssego claro no meio e em cima, laranja nas beiradas e embaixo,
    lados mais escuros para a coluna de placas parecer arredondada."""
    def f(c):
        x, y, z = c["p"]; face = c["face"]
        v = clamp((y0 - y) / 2.6)                      # 0 em cima .. 1 embaixo
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
    """Segmento da cauda (eixo local +z). Na base (k <= 3) a barriga laranja fica embaixo e o dorso de carvão com
    manchas em cima; no laço (k >= 4) a cauda mostra o dorso manchado para FORA do laço (de costas e de cima, como na
    ficha) e o laranja fica no lado de dentro."""
    zc = z0 + L * 0.5
    base = k <= 3
    yd = py + h / 2 if base else py - h / 2                       # face do dorso (manchas grandes)
    lista = [((0.0, yd, zc), (0.34 if k % 2 else 0.17) * w, 1.0)]               # dorso: grande e pequena alternadas
    for s in (-1, 1):                                                            # lados: uma por segmento
        lista.append(((s * w / 2, py - h / 2 + (0.6 if base else 0.4) * h, zc + (0.15 if k % 2 else -0.15) * L), 0.31 * h, 1.0))
    def cor(p, face):
        x, y, z = p
        v = (y - (py - h / 2)) / h                     # 0 embaixo .. 1 em cima (local)
        if not base: v = 1 - v
        lar = face == ("down" if base else "up")
        if lar or v < 0.26:
            return mix(AMARELO, LARANJA, clamp(v / 0.26)) if base else mix(LARANJA, LARANJA_ESC, clamp(v / 0.26))
        if v < 0.34: return mix(LARANJA_ESC, CARVAO, (v - 0.26) / 0.08)
        return CARVAO
    return mat_com_manchas(cor, lista, borda=.05, curva=.45), brilho_manchas(lista)

def cauda_laco(nome, base, segs):
    """Cadeia como a pena_curva (ossos '<nome>_0', '<nome>_1'...), mas com giro próprio em cada junta, para a cauda
    poder correr reta para trás e depois enrolar num laço. segs = [(comprimento, largura, altura, rx, ry)].
    Cada segmento são 2 blocos em cruz (seção octogonal) que avançam para trás (ov) para tapar a junta."""
    def seg(k, pos):
        L, w, h, rx, ry = segs[k]
        px, py, pz = pos
        ov = 0.15 + (h / 2) * math.tan(math.radians(abs(rx))) * 0.9 if k > 0 else 0.4
        r = 0.24 * min(w, h)
        mat, br = mat_rabo(w, h, py, pz, L, k)
        fx = (py - h / 2, py + h / 2)
        filhos = [peca(f"{nome}_{k}_a", [px - w / 2, py - h / 2 + r, pz - ov], [px + w / 2, py + h / 2 - r, pz + L], mat, faixa=fx, brilho=br, res=3),
                  peca(f"{nome}_{k}_b", [px - w / 2 + r, py - h / 2, pz - ov], [px + w / 2 - r, py + h / 2, pz + L], mat, faixa=fx, brilho=br, res=3)]
        if k + 1 < len(segs): filhos.append(seg(k + 1, (px, py, pz + L)))
        return osso(f"{nome}_{k}", [px, py, pz], [rx, ry, 0], filhos)
    return seg(0, base)

# ---------------- cabeça ----------------
K_CAB = 1.12                      # escala da cabeça inteira (com crista e bico)
OLHO_Y = 27.7
FAC_T = 1.4                       # espessura da peça da face diagonal (onde fica o olho)
FAC_L = 4.1                       # comprimento da face diagonal
FAC_M = (3.175, -21.6)            # meio da superfície da face diagonal (lado +x)
FAC_C = (FAC_M[0] - 0.7071 * FAC_T / 2, FAC_M[1] + 0.7071 * FAC_T / 2)

def cor_cabeca(p, face):
    x, y, z = p
    if face == "up": return MALVA
    if y > 30.4: return mix(CINZA_ROXO, MALVA, 0.35)
    return mix(CARVAO, CINZA_ROXO, clamp((y - 24.0) / 5.5))

def mat_faceta(lado):
    base = g.mat_cor(cor_cabeca, borda=.04, curva=.3)
    fora = "east" if lado > 0 else "west"
    def f(c):
        x, y, z = c["p"]
        if c["face"] == fora:
            u = z - FAC_C[1]
            o = g.pintar_olho(u - 0.1, y - OLHO_Y, 1.66, 1.42, iris=((150, 24, 10), (240, 86, 30)), esclera=CREME,
                              r_iris=(0.58, 0.78), c_iris=(-0.32, -0.12), r_pup=(0.27, 0.36), bravo=0.5, alto=0.3,
                              contorno=CARVAO_ESC)
            if o: return o
        return base(c)
    return f

def cor_bico(p, face):
    x, y, z = p
    if face == "up": return BICO_CLARO
    if face in ("east", "west") and abs(z + 23.4) < 0.3 and abs(y - 27.3) < 0.22: return CARVAO_ESC   # narina
    return mix(BICO, BICO_CLARO, clamp((y - 25.0) / 3.0) * 0.6)

# ---------------- crista de brasa ----------------
def mat_crista(c):
    face = c["face"]
    (_, y0, _), (_, y1, _) = c["b"]
    t = clamp((c["p"][1] - y0) / max(y1 - y0, 1e-6))
    if face == "up": base = VERM_CLARO
    elif face == "down": base = VERM_ESC
    elif face == "north": base = mix(VERM, VERM_VIVO, t)
    else: base = mix(mix(VERM_ESC, VERM, 0.5), VERM, t)
    return tom(base, -0.28) if g.na_borda(c) else base

def lamina(nome, x0, x1, yb, z0, z1, ytopo, inc, rz=0):
    """Lâmina da crista: bloco + ponta em cunha (bloco girado 45° em x) que termina em 'ytopo'; o osso inclina 'inc'
    graus para trás a partir da base."""
    d = z1 - z0; zc = (z0 + z1) / 2; sq = d / 1.4142; cy = ytopo - d / 2; xm = (x0 + x1) / 2
    return osso(nome, [xm, yb, zc], [inc, 0, rz], [
        peca(nome, [x0, yb, z0], [x1, cy, z1], mat_crista, res=3),
        peca(nome + "_ponta", [x0 + 0.35, cy - sq / 2, zc - sq / 2], [x1 - 0.35, cy + sq / 2, zc + sq / 2], mat_crista,
             rot=(45, 0, 0), pivo=(xm, cy, zc), res=3)])

# ---------------- placas quentes ----------------
def dist_seg(p, a, b):
    ab = [b[i] - a[i] for i in range(len(a))]; ap = [p[i] - a[i] for i in range(len(a))]
    t = clamp(sum(ab[i] * ap[i] for i in range(len(a))) / max(sum(v * v for v in ab), 1e-6))
    return math.sqrt(sum((ap[i] - t * ab[i]) ** 2 for i in range(len(a))))

def mat_placa_quente(y0, z0, L, W, tipo=1):
    """Placa de rocha (carvão facetado) pendurada da raiz (y0, z0), com fenda de lava em Y na face larga (±x)."""
    ym = y0 - L * 0.42
    if tipo == 1:     # Y grande
        fendas = [((y0 - 0.2, z0 + 0.15 * W), (ym, z0)), ((ym, z0), (y0 - L * 0.85, z0 - 0.3 * W)), ((ym, z0), (y0 - L * 0.72, z0 + 0.42 * W))]
    elif tipo == 0:   # fenda curta na beirada
        fendas = [((y0 - L * 0.25, z0 - 0.5 * W), (y0 - L * 0.55, z0 - 0.1 * W))]
    else:             # fenda curta descendo
        fendas = [((y0 - L * 0.5, z0 + 0.5 * W), (y0 - L * 0.75, z0 + 0.15 * W))]
    def fenda(c):
        if c["face"] not in ("east", "west"): return None
        q = (c["p"][1], c["p"][2])
        d = min(dist_seg(q, a, b) for a, b in fendas)
        if d < 0.2: return BRASA_MIOLO
        if d < 0.38: return BRASA
        if d < 0.55: return BRASA_BORDA
        return None
    def f(c):
        cr = fenda(c)
        if cr: return cr
        face = c["face"]
        base = mix(CINZA_ROXO, MALVA, 0.2) if face == "up" else CARVAO_ESC if face == "down" else mix(CARVAO, CINZA_ROXO, 0.35)
        v = clamp((y0 - c["p"][1]) / L)
        base = mix(base, CARVAO, v * 0.5)
        return tom(base, -0.35) if g.na_borda(c) else base
    return f, (lambda c, cor: fenda(c) is not None)

def placa_quente(nome, raiz, rot, L, W, esp=0.8, tipo=1):
    """Placa grossa e pontuda (corpo + ponta em losango, como a placa_armadura) com a fenda de lava."""
    x, y, z = raiz
    m, br = mat_placa_quente(y, z, L, W, tipo)
    cy = y - L * 0.68; sq = W / 1.4142
    return osso(nome, list(raiz), list(rot), [
        peca(nome, [x - esp / 2, cy, z - W / 2], [x + esp / 2, y, z + W / 2], m, res=5, brilho=br),
        peca(nome + "_ponta", [x - esp / 2 + 0.03, cy - sq / 2, z - sq / 2], [x + esp / 2 - 0.03, cy + sq / 2, z + sq / 2], m,
             rot=(45, 0, 0), pivo=(x, cy, z), res=5, brilho=br)])

# ---------------- pernas ----------------
def perna(nome, xc, zc, tras):
    lado = -1 if xc < 0 else 1
    pp = []
    if tras:
        lista = [((xc + 2.6 * lado, 11.4, zc - 0.6), 1.25, 1.4)]
        pp += g.arredondado2(nome + "_coxa", [xc - 2.6, 6.8, zc - 4.4], [xc + 2.6, 15.0, zc + 3.8],
                             mat_com_manchas(lambda p, f: CARVAO, lista, borda=.04, curva=.4), r=1.7, brilho=brilho_manchas(lista),
                             rot=(0, 0, 9 * lado), pivo=(xc, 7.6, zc))
    else:
        pp += g.arredondado2(nome + "_braco", [xc - 2.4, 8.8, zc - 2.6], [xc + 2.4, 13.0, zc + 2.6],
                             g.mat_cor(lambda p, f: CARVAO, borda=.06, curva=.4), r=1.4, rot=(0, 0, 12 * lado), pivo=(xc, 9.0, zc))
    # faixa laranja (canela de cima) e tornozelo de carvão
    yt = 8.4 if tras else 10.4
    mo = g.mat_cor(lambda p, f: mix(LARANJA_ESC, AMARELO, clamp((p[1] - 5.0) / (yt - 5.0))), borda=.08, curva=.3)
    pp += g.octogono(nome + "_canela", [xc - 2.35, 5.0, zc - 2.35], [xc + 2.35, yt, zc + 2.35], mo, r=0.8)
    pp += g.octogono(nome + "_tornozelo", [xc - 2.0, 2.0, zc - 2.0], [xc + 2.0, 5.3, zc + 2.0],
                     g.mat_cor(lambda p, f: CARVAO, borda=.1, curva=.4), r=0.6)
    # pé: sola escura e 3 dedos grossos cinza-rosados (com a unha mais clara) para a frente + 1 atrás
    pp.append(peca(nome + "_sola", [xc - 2.9, 0.9, zc - 2.4], [xc + 2.9, 2.7, zc + 2.2], g.mat_facetado(CINZA_ROXO, CARVAO, CARVAO, CARVAO_ESC)))
    mu = g.mat_facetado(UNHA_CLARA, UNHA, mix(UNHA, MALVA, .45), MALVA, quina=-0.25)
    mp = g.mat_facetado(mix(UNHA_CLARA, (255, 255, 255), .3), UNHA_CLARA, UNHA, MALVA, quina=-0.25)
    for k, (dx, giro) in enumerate(((-2.2, 16), (0.0, 0), (2.2, -16))):
        x0 = xc + dx; z0 = zc - 1.2
        pp.append(osso(f"{nome}_dedo{k}", [x0, 0, z0], [0, giro, 0], [
            peca(f"{nome}_dedo{k}", [x0 - 1.05, 0, z0 - 3.4], [x0 + 1.05, 2.7, z0 + 0.6], mu, res=3),
            peca(f"{nome}_unha{k}", [x0 - 0.85, 0, z0 - 4.5], [x0 + 0.85, 2.0, z0 - 3.2], mp, res=3)]))
    pp.append(peca(nome + "_dedo_tras", [xc - 0.9, 0, zc + 1.4], [xc + 0.9, 1.8, zc + 3.6], mu, res=3))
    return osso(nome, [xc, 13.0, zc], [0, 0, 0], pp)

# ---------------- montagem ----------------
def montar():
    # ---------- cabeça ----------
    i_cab = len(g.PECAS)
    cab = []
    mcab = g.mat_cor(cor_cabeca, borda=.04, curva=.3)
    fx = (23.6, 32.6)
    cab.append(peca("cranio", [-4.6, 24.4, -20.2], [4.6, 30.9, -15.8], mcab, faixa=fx, res=3))
    cab.append(peca("cranio_cima", [-4.2, 30.5, -21.4], [4.2, 31.9, -16.0], mcab, faixa=fx, res=3))
    cab.append(peca("cranio_frente", [-1.75, 24.4, -23.0], [1.75, 30.9, -20.0], mcab, faixa=fx, res=3))
    cab.append(peca("queixo", [-3.6, 23.6, -21.2], [3.6, 24.6, -16.4], mcab, faixa=fx, res=3))
    sob = g.mat_facetado(MALVA, CINZA_ROXO, CINZA_ROXO, CARVAO)
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        cx, cz = FAC_C[0] * lado, FAC_C[1]
        cab.append(peca("faceta_" + s, [cx - FAC_T / 2, 24.4, cz - FAC_L / 2], [cx + FAC_T / 2, 30.9, cz + FAC_L / 2],
                        mat_faceta(lado), rot=(0, 45 * lado, 0), pivo=(cx, 27.5, cz), faixa=fx, res=8))
        # sobrancelha brava: placa grossa na face diagonal, descendo para o bico
        fx0, fx1 = sorted((cx + FAC_T / 2 * lado - 0.2 * lado, cx + FAC_T / 2 * lado + 0.55 * lado))
        cab.append(osso("sobrancelha_" + s, [cx, 28.95, cz], [0, 45 * lado, 0], [
            peca("sobrancelha_" + s, [fx0, 28.15, cz - 2.3], [fx1, 29.75, cz + 2.0], sob, rot=(-22, 0, 0), pivo=(cx, 28.95, cz))]))
        # aba da sobrancelha no lado da cabeça
        x0, x1 = sorted((4.5 * lado, 5.0 * lado))
        cab.append(peca("aba_" + s, [x0, 28.9, -20.0], [x1, 30.5, -16.2], sob))
    # bico cinza em cunha com gancho
    mb = g.mat_cor(cor_bico, borda=.06, curva=.4)
    fb = (24.0, 28.8)
    # topo chato e claro, cunha em losango embaixo (de frente vira um escudo em V) e gancho na ponta
    cab.append(peca("bico_topo", [-1.8, 27.3, -24.8], [1.8, 29.0, -22.3], mb, rot=(-9, 0, 0), pivo=(0, 29.0, -22.3), faixa=fb))
    cab.append(peca("bico_v", [-1.35, 25.75, -24.5], [1.35, 28.45, -22.3], mb, rot=(0, 0, 45), pivo=(0, 27.1, -23.4), faixa=fb))
    cab.append(peca("bico_gancho", [-0.9, 25.5, -26.2], [0.9, 28.1, -24.6], g.mat_cor(lambda p, f: tom(BICO, -0.05), borda=.08, curva=.6),
                    rot=(-30, 0, 0), pivo=(0, 28.1, -24.6), faixa=fb))
    cab.append(peca("bico_baixo", [-0.95, 24.7, -24.4], [0.95, 25.5, -22.3], g.mat_cor(lambda p, f: tom(BICO, -0.32), borda=.1)))
    # crista de brasa: lâminas com ponta em cunha (espinhos vistos de lado), fileira alta no meio e degraus mais
    # baixos dos lados, inclinando cada vez mais para trás
    crista = []
    for k, (z0, z1, y1, inc) in enumerate([(-23.2, -20.8, 34.4, -6), (-21.2, -18.4, 36.8, 2), (-18.8, -15.6, 38.8, 10),
                                           (-16.0, -12.8, 38.0, 18), (-13.2, -10.0, 36.2, 26), (-10.4, -7.4, 34.0, 34)]):
        crista.append(lamina(f"crista_meio{k}", -1.7, 1.7, 30.8, z0, z1, y1, inc))
    for lado in (-1, 1):
        s_ = "d" if lado < 0 else "e"
        for k, (z0, z1, y1, inc) in enumerate([(-22.8, -20.2, 33.2, 0), (-20.6, -17.6, 35.0, 8), (-17.8, -14.6, 35.4, 16),
                                               (-14.8, -11.6, 34.6, 24), (-11.8, -8.8, 33.0, 32)]):
            x0, x1 = sorted((1.3 * lado, 3.9 * lado))
            crista.append(lamina(f"crista_{s_}{k}", x0, x1, 30.6, z0, z1, y1, inc, rz=-8 * lado))
    cab.append(osso("crista", [0, 31.5, -18], [0, 0, 0], crista))
    # penas da bochecha: vermelhas e laranja, saindo de trás do olho e varrendo para trás
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        for k, (y0, z0, L, W, fl, var, cores) in enumerate([(29.6, -17.6, 5.2, 2.8, 64, 60, (VERM, VERM_VIVO, LARANJA)),
                                                            (28.2, -16.6, 5.8, 3.0, 52, 48, (VERM, LARANJA, AMARELO)),
                                                            (26.6, -16.0, 5.4, 3.0, 40, 36, (LARANJA_ESC, LARANJA, AMARELO))]):
            cab.append(g.pena_cruzada(f"bochecha{k}_{s}", (4.4 * lado, y0, z0), (-var, 0, fl * lado), L, W, cores, curva=0.15))
    g.transformar(i_cab, cab, (0, 24.0, -15.5), k=K_CAB)          # cabeça um pouco maior, como na ficha
    cabeca = osso("cabeca", [0, 25.0, -15.5], [0, 0, 0], cab)

    # ---------- pescoço com a pelagem ígnea (juba de penas de fogo) ----------
    pesc = []
    mpe = g.mat_cor(lambda p, f: CARVAO, borda=.04, curva=.3)
    pesc.append(peca("pescoco", [-3.3, 15.0, -18.0], [3.3, 25.0, -11.0], mpe, rot=(-10, 0, 0), pivo=(0, 16.0, -12.0), faixa=(14, 26)))
    # placas da barriga (frente do pescoço até o peito), laranja em faixas sobrepostas
    def frente(y):   # linha da frente do pescoço (y >= 16) e do peito
        return -17.9 - 0.18 * (y - 16) if y >= 16 else -17.9 + (16 - y) * 0.22
    for k in range(6):
        y0 = 24.4 - 2.3 * k
        zf = frente(y0 - 1.3) - 0.45
        w = 2.5 + 0.34 * k
        mpl = mat_placa_ventre(y0, w)
        pesc.append(peca(f"placa_ventre{k}", [-w, y0 - 2.6, zf], [w, y0, zf + 1.5], mpl, rot=(-2 if y0 > 17 else 8, 0, 0), pivo=(0, y0, zf + 0.75)))
    juba = []
    CAMADAS = [  # (y, raio x, raio z, z centro, abertura, varrida, comprimento, largura, cores, phis)
        (27.0, 4.0, 3.4, -14.4, 22, 40, 6.2, 3.6, (VERM, VERM_VIVO, LARANJA), [-20, 14, 48, 84]),
        (24.8, 4.2, 3.8, -14.2, 18, 30, 6.6, 3.8, (VERM_VIVO, LARANJA, AMARELO), [-46, -12, 22, 56]),
        (22.6, 4.4, 4.2, -13.6, 14, 22, 6.0, 3.8, (LARANJA_ESC, LARANJA, AMARELO), [-56, -26, 4, 36]),
    ]
    for f_, (y0, ax, az, zc, fl, var, L, W, cores, phis) in enumerate(CAMADAS):
        for k, phi in enumerate(phis):
            for lado in (-1, 1):
                if phi >= 86 and lado < 0: continue
                x, z = anel(ax, az, zc, phi, lado)
                if phi >= 86: x = 0
                nome = f"juba{f_}{k}_{'d' if lado < 0 else 'e'}"
                if -30 < phi < 30:   # dos lados: em X, para não virar risco visto de frente
                    juba.append(g.pena_cruzada(nome, (x, y0, z), (-var, 0, fl * lado), L, W, cores, curva=0.15 * lado))
                else:
                    juba.append(g.pena_cone_placa(nome, (x, y0, z), phi, fl, L, W, cores, lado, varre=var if phi < 80 else 0,
                                                  curva=0.2 * lado))
    pesc.append(osso("juba", [0, 24, -14], [0, 0, 0], juba))
    pesc.append(cabeca)
    pescoco = osso("pescoco", [0, 17.0, -12.0], [0, 0, 0], pesc)

    # ---------- tronco de salamandra ----------
    corpo = []
    mt = mat_com_manchas(cor_corpo, MANCHAS_CORPO, borda=.03, curva=.5)
    bt = brilho_manchas(MANCHAS_CORPO)
    fc = (9.0, 20.6)
    corpo += g.arredondado2("peito", [-5.6, 9.6, -16.6], [5.6, 20.6, -4.6], mt, r=3.0, faixa=fc, brilho=bt)
    corpo += g.arredondado2("meio", [-5.5, 9.2, -7.0], [5.5, 19.6, 4.0], mt, r=3.0, faixa=fc, brilho=bt)
    corpo += g.arredondado2("quadril", [-5.2, 9.6, 1.0], [5.2, 18.2, 11.8], mt, r=3.0, faixa=fc, brilho=bt)
    # asas dobradas: penas de fogo por baixo e placas quentes de carvão (com fenda de lava) por cima
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = []
        for k, (z0, y0, L, W, var, fl, cores) in enumerate([(-10.4, 18.0, 8.0, 3.6, 52, 22, (VERM, LARANJA, AMARELO)),
                                                            (-8.4, 18.2, 9.2, 3.8, 62, 20, (VERM_VIVO, LARANJA, AMARELO)),
                                                            (-6.2, 18.2, 9.4, 3.6, 70, 18, (VERM, LARANJA_ESC, AMARELO)),
                                                            (-4.0, 18.0, 8.4, 3.4, 78, 16, (VERM_ESC, VERM, LARANJA))]):
            phi = (-34, -12, 8, 24)[k]          # as da frente giram a face larga para a frente (aparecem de frente)
            raiz = (5.6 * lado, y0, z0)
            asa.append(osso(f"asa_fogo{k}_{s}_giro", list(raiz), [0, -phi * lado, 0],
                            [g.pena_placa(f"asa_fogo{k}_{s}", raiz, (-var, 0, fl * lado), L, W, cores, curva=0.2)]))
        for k, (z0, y0, L, W, var, fl) in enumerate([(-11.0, 20.0, 6.0, 3.8, 40, 26), (-8.4, 20.4, 6.8, 4.0, 52, 24), (-5.6, 20.2, 6.4, 3.8, 64, 22)]):
            phi = (-36, -8, 18)[k]
            raiz = (5.3 * lado, y0, z0)
            asa.append(osso(f"placa_quente{k}_{s}_giro", list(raiz), [0, -phi * lado, 0],
                            [placa_quente(f"placa_quente{k}_{s}", raiz, (-var, 0, (fl + 14) * lado), L, W, tipo=k)]))
        corpo.append(osso("asa_" + s, [5.0 * lado, 19.0, -8.0], [0, 0, 0], asa))
    # cauda comprida que enrola num laço para cima
    SEGS = [(5.0, 9.6, 6.8, 13, 0), (5.0, 9.4, 6.4, -6, 0), (4.6, 9.0, 6.0, -18, 0), (4.2, 8.6, 5.6, -34, 0),
            (4.2, 8.1, 5.2, -34, 0), (4.2, 7.5, 4.9, -12, 0), (4.0, 6.9, 4.6, -30, 0), (3.8, 6.2, 4.3, -36, 0),
            (3.6, 5.5, 4.0, -30, 0), (3.4, 4.8, 3.7, -14, 0), (3.2, 4.1, 3.4, -4, 0), (3.0, 3.5, 3.0, 0, 0)]
    corpo.append(osso("cauda", [0, 14.6, 9.0], [0, 0, 0], [cauda_laco("rabo", (0, 14.6, 9.0), SEGS)]))
    corpo.append(pescoco)
    tronco = osso("corpo", [0, 13.0, 8.0], [0, 0, 0], corpo)

    pernas = [perna("perna_fd", -5.8, -10.4, False), perna("perna_fe", 5.8, -10.4, False),
              perna("perna_td", -5.6, 7.8, True), perna("perna_te", 5.6, 7.8, True)]
    return [tronco] + pernas

if __name__ == "__main__":
    g.rodar(ID, montar, rosto=ROSTO)
