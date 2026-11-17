"""Pirococó v2: mais fiel à arte conceitual do usuário.
Modelado em resolução dobrada (2 px de modelo = 1 px do Minecraft); no jogo renderizar com escala 0.5
-> ~1,5 bloco de altura (corpo/cabeça), com o dobro de detalhe.
Saída: modelos/pirococo/pirococo_v2.bbmodel + pirococo_v2.png + pirococo_v2_previa.png"""
import math, sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from galos_monstro import Modelo, r, RNG
import previa
from PIL import Image, ImageDraw

PASTA = AQUI.parent / "modelos" / "pirococo"
NOME = "pirococo_v2"

# ---------------- paleta da ficha ----------------
VERM_ESC = (128, 12, 22)
VERM = (210, 26, 30)
VERM_CLARO = (238, 58, 38)
LARANJA = (255, 118, 22)
LARANJA_CLARO = (255, 158, 40)
AMARELO = (255, 206, 52)
AMARELO_CLARO = (255, 236, 130)
AZUL_ESC = (22, 48, 160)
AZUL = (38, 104, 232)
AZUL_CLARO = (120, 186, 255)
OURO = (236, 172, 40)
OURO_CLARO = (255, 222, 104)
OURO_ESC = (150, 94, 18)
OLHO = (60, 150, 255)
CONTORNO = (36, 6, 10)

def esc(c, k=0.7): return tuple(int(v * k) for v in c)

# ---------------- desenhador de penas-lâmina ----------------
def cor_fogo(f): return VERM_ESC if f < .22 else VERM if f < .5 else LARANJA if f < .78 else AMARELO
def cor_verm(f): return VERM if f < .55 else VERM_CLARO if f < .8 else LARANJA_CLARO
def cor_azul(f): return VERM_ESC if f < .2 else AZUL if f < .8 else AZUL_CLARO

def lamina(o, ang, L, w, cores, curva=0.0, borda=OURO_CLARO, afina=2.2):
    return dict(o=o, ang=ang, L=L, w=w, cores=cores, curva=curva, borda=borda, afina=afina)

def rasterizar(W, H, laminas):
    """Desenha lâminas (pontiagudas, opcionalmente curvas) numa grade WxH.
    Coordenadas da arte: x = coluna, y para cima. Lâminas desenhadas depois ficam por cima."""
    arr = [[None] * W for _ in range(H)]
    for lm in laminas:
        ox, oy = lm["o"]; a = math.radians(lm["ang"]); dx, dy = math.cos(a), math.sin(a)
        for row in range(H):
            for col in range(W):
                vx, vy = col + .5 - ox, H - row - .5 - oy
                u = vx * dx + vy * dy
                if u < 0 or u > lm["L"]: continue
                f = u / lm["L"]
                n = -vx * dy + vy * dx + lm["curva"] * lm["L"] * f * f
                hw = lm["w"] * (1 - f ** lm["afina"]) + .35
                if abs(n) > hw: continue
                cor = lm["cores"](f)
                if abs(n) > hw * .55:
                    cor = lm["borda"] if n > 0 and lm["borda"] else esc(cor)
                arr[row][col] = cor
    return arr

def plano(arr, modo):
    """Pintor de plano fino: 'x' = visto de lado (coluna 0 = frente), 'z' = visto de frente."""
    def p(face, s, t, W, H):
        if modo == "x":
            return arr[t][s] if face == "side" else None
        if face == "north": return arr[t][s]
        if face == "south": return arr[t][W - 1 - s]
        return None
    return p

# ---------------- pintores de volume ----------------
def penas_armadura(face, s, t, W, H):
    """Escamas de penas vermelhas com fio dourado (penas de armadura)."""
    if face == "down": return VERM_ESC
    if t % 3 == 2: return OURO if (s + t // 3) % 2 == 0 else VERM_ESC
    return VERM if (s + t // 3) % 2 == 0 else VERM_CLARO

def peito_v(face, s, t, W, H):
    """Peito com penas em V sobrepostas (chevrons) de borda dourada."""
    if face != "north": return penas_armadura(face, s, t, W, H)
    v = t + abs(s - (W - 1) / 2) * 0.7
    faixa, dentro = int(v // 3), v % 3
    if dentro < 1: return OURO_CLARO
    return [VERM, LARANJA, VERM_CLARO, AMARELO][faixa % 4] if dentro < 2.2 else esc(VERM)

def metal(face, s, t, W, H):
    if face == "up": return OURO_CLARO
    if face == "down": return OURO_ESC
    if t == 0: return OURO_CLARO
    if t == H - 1: return OURO_ESC
    return OURO_CLARO if (s + 2 * t) % 5 == 0 else OURO

def escamas_ouro(face, s, t, W, H):
    if face == "down": return OURO_ESC
    return OURO_ESC if t % 2 == 1 else (OURO_CLARO if s == 0 else OURO)

def unha(face, s, t, W, H): return (250, 236, 170) if face == "up" or t == 0 else (196, 128, 30)

def gola(face, s, t, W, H):
    if face in ("up", "down"): return LARANJA
    return [VERM, LARANJA, AMARELO, VERM_CLARO][(s + t // 2) % 4]

def juba(azul_cada):
    def p(face, s, t, W, H):
        if face == "down": return None
        if face == "up": return LARANJA
        if t >= H - 2 and (s + (t == H - 1)) % 2 == 1: return None        # franja em ponta
        if azul_cada and s % azul_cada == 0 and t >= 1: return AZUL
        return [VERM, LARANJA, VERM_CLARO, AMARELO][(s + t) % 4] if t < H - 2 else AMARELO
    return p

def cabeca(face, s, t, W, H):
    if face == "side":                     # W=10 (s=0 frente), H=7
        olho = {(2, 2): (210, 240, 255), (3, 2): OLHO, (2, 3): OLHO, (3, 3): AZUL_ESC}
        if (s, t) in olho: return olho[(s, t)]
        if (s, t) in ((1, 2), (1, 3), (4, 2), (4, 3), (2, 4), (3, 4)): return CONTORNO
        if t == 1 and 1 <= s <= 5: return OURO if s >= 4 else VERM_ESC   # sobrancelha brava
        if t >= 4 and s <= 5: return AMARELO if (s + t) % 2 else LARANJA
        return [VERM, VERM_CLARO, LARANJA][(s + 2 * t) % 3]
    if face == "north": return AMARELO if t >= 5 else (VERM_ESC if t == 1 else VERM)
    if face == "down": return AMARELO
    return [VERM, LARANJA][(s + t) % 2]

def bico(face, s, t, W, H):
    if face == "up": return OURO_CLARO
    if face in ("down", "north"): return OURO_ESC
    return OURO_ESC if s == 0 else (OURO_CLARO if t == 0 else OURO)

# ---------------- artes ----------------
def arte_asa():
    raiz = (4, 4)
    angs = [14, 27, 40, 53, 66, 79, 92, 105]
    comps = [16, 20, 24, 26, 27, 25, 21, 16]
    fundo = [lamina(raiz, a, L, 2.7, cor_fogo if i % 2 == 0 else cor_azul) for i, (a, L) in enumerate(zip(angs, comps))]
    meio = [lamina(raiz, a + 6, L * .66, 2.4, cor_azul if i % 2 == 0 else cor_verm)
            for i, (a, L) in enumerate(zip(angs[:-1], comps[:-1]))]
    return rasterizar(26, 28, fundo + meio)

def arte_cobertura():
    return rasterizar(26, 28, [lamina((4, 4), a, 9 + (a % 20) / 5, 2.3, cor_verm) for a in range(8, 106, 14)])

def arte_crina():            # 3 pontas enormes varrendo para trás e para cima + chamas pequenas na base
    return rasterizar(20, 14, [
        lamina((3, .5), 18, 8, 1.6, cor_fogo), lamina((4, .5), 34, 7, 1.6, cor_fogo),
        lamina((4, .5), 24, 19, 2.6, cor_fogo, curva=-.04),
        lamina((5, .5), 45, 16, 2.5, cor_fogo, curva=-.05),
        lamina((6, .5), 70, 13, 2.3, cor_fogo, curva=-.06),
    ])

def arte_bochecha():         # chamas saindo das bochechas para trás
    return rasterizar(14, 12, [
        lamina((2, 2), 8, 12, 1.8, cor_fogo), lamina((2, 4), 24, 11, 1.7, cor_fogo),
        lamina((3, 6), 40, 9, 1.6, cor_fogo), lamina((1, 1), -6, 9, 1.4, cor_fogo),
    ])

def arte_saia(W, H):         # penas pontudas caindo da coxa
    return rasterizar(W, H, [lamina((x + .5, H), -90 + (x - W / 2) * 4, H - 1 - (x % 2) * 2, 1.25,
                                    lambda f: VERM_ESC if f < .3 else VERM if f < .7 else LARANJA)
                             for x in range(0, W, 1)])

def arte_cauda(variante):
    if variante == 0:
        return rasterizar(34, 16, [lamina((1, 13), -6, 32, 3.0, cor_fogo, curva=-.22),
                                   lamina((1, 12), -14, 22, 1.8, cor_azul, curva=-.2)])
    return rasterizar(34, 16, [lamina((1, 13), -2, 30, 2.6, cor_azul, curva=-.26),
                               lamina((1, 13), -10, 24, 2.0, cor_fogo, curva=-.2)])

def arte_gorjal():           # placa de ouro em V no alto do peito, com gema
    W, H = 12, 8
    arr = [[None] * W for _ in range(H)]
    for row in range(H):
        for col in range(W):
            d = abs(col - (W - 1) / 2) * 0.9
            if H - 1 - d - 2.6 <= row <= H - 1 - d + .2 and row >= 0:
                topo = row <= H - 1 - d - 1.8
                arr[row][col] = OURO_CLARO if topo else (OURO_ESC if row >= H - 1 - d - .4 else OURO)
    for (row, col) in ((5, 5), (5, 6), (6, 5), (6, 6)):
        arr[row][col] = AZUL_CLARO if row == 5 else AZUL
    return arr

# ---------------- montagem ----------------
def montar(m):
    def perna(lado):
        x = 4 * lado; e = "_d" if lado < 0 else "_e"
        def c(nome, de, ate, pintor=None, uv_de=None):
            de = [de[0] + x, de[1], de[2]]; ate = [ate[0] + x, ate[1], ate[2]]
            if lado > 0: return m.cubo(nome + e, de, ate, espelho_de=nome + "_d")
            return m.cubo(nome + e, de, ate, pintor, uv_de=(uv_de + "_d") if uv_de else None)
        abre = 26 * lado
        def dedo(nome, L, rot, primeiro):
            kw = (lambda n, p: dict(pintor=p)) if primeiro else (lambda n, p: dict(uv_de=n))
            return m.osso(f"{nome}{e}", [x, 3, 0], [0, rot, 0], [
                c(nome, [-1, 2, -L], [1, 4, 0], **kw("dedo_meio", escamas_ouro)),
                c("garra_" + nome, [-0.5, 3, -L - 3], [0.5, 4, -L], **kw("garra_dedo_meio", unha)),
                c("garra_ponta_" + nome, [-0.5, 0, -L - 3], [0.5, 3, -L - 2], **kw("garra_ponta_dedo_meio", unha)),
            ])
        lado_x = 3.2 * lado if lado > 0 else -3.2
        return m.osso("perna" + e, [x, 20, 0], [0, 0, 0], [
            c("coxa", [-3, 13, -3], [3, 22, 3], penas_armadura),
            c("saia_frente", [-3.5, 9, -3.5], [3.5, 19, -3.5], plano(arte_saia(7, 10), "z")),
            m.cubo("saia_lado" + e, [x + lado_x, 9, -3], [x + lado_x, 19, 4],
                   plano(arte_saia(7, 10), "x") if lado < 0 else None, uv_de=None if lado < 0 else "saia_lado_d"),
            c("joelheira", [-1.5, 10, -2], [1.5, 13, -1], metal),
            c("canela", [-1, 3, -1], [1, 13, 1], escamas_ouro),
            dedo("dedo_meio", 8, 0, True),
            dedo("dedo_fora", 6, -abre, False),
            dedo("dedo_dentro", 6, abre, False),
            c("dedo_tras", [-1, 2, 0], [1, 4, 4], escamas_ouro),
            c("garra_tras", [-0.5, 0, 4], [0.5, 4, 5], unha),
            c("espora", [-0.5, 6, 1], [0.5, 7, 4], unha),
        ])

    corpo = m.osso("corpo", [0, 26, 0], [12, 0, 0], [
        m.cubo("tronco", [-7, 18, -6], [7, 36, 7], penas_armadura),
        m.cubo("peito", [-6, 19, -8], [6, 35, -6], peito_v),
        m.cubo("gorjal", [-6, 28, -8.6], [6, 36, -8.6], plano(arte_gorjal(), "z")),
        m.cubo("ombreira_d", [-9, 31, -4], [-6, 36, 3], metal),
        m.cubo("ombreira_e", [6, 31, -4], [9, 36, 3], espelho_de="ombreira_d"),
    ])

    def asa(lado):
        e = "_d" if lado < 0 else "_e"; s = lado
        def xs(a, b): return [-b - 3, -a - 3] if s < 0 else [a + 3, b + 3]
        def c(nome, de, ate, pintor):
            if s > 0: return m.cubo(nome + e, de, ate, espelho_de=nome + "_d")
            return m.cubo(nome + e, de, ate, pintor)
        px = xs(0, 26)
        return m.osso("asa" + e, [7 * s, 34, 1], [0, -15 * s, 0], [
            c("asa_penas", [px[0], 30, 1.5], [px[1], 58, 1.5], plano(arte_asa(), "z")),
            c("asa_cobertura", [px[0], 30, 0.2], [px[1], 58, 0.2], plano(arte_cobertura(), "z")),
            c("asa_braco", [xs(3, 12)[0], 32, -2], [xs(3, 12)[1], 36, 2], penas_armadura),
            c("bracadeira", [xs(6, 9)[0], 31.5, -2.5], [xs(6, 9)[1], 36.5, 2.5], metal),
        ])

    crina_arr = arte_crina()
    bochecha_arr = arte_bochecha()
    cab = m.osso("cabeca", [0, 41, -3], [0, 0, 0], [
        m.cubo("cabeca", [-4, 40, -10], [4, 47, 0], cabeca),
        m.cubo("bico", [-2, 42, -15], [2, 45, -10], bico),
        m.cubo("bico_gancho", [-1.5, 40, -16], [1.5, 43, -14], bico),
        m.cubo("bico_baixo", [-1.5, 40, -13], [1.5, 42, -10], bico),
        m.cubo("sobrancelha_d", [-5, 45, -10], [-2, 46, -5], metal),
        m.cubo("sobrancelha_e", [2, 45, -10], [5, 46, -5], espelho_de="sobrancelha_d"),
        m.cubo("bochecha_d", [-4.6, 37, -8], [-4.6, 49, 6], plano(bochecha_arr, "x")),
        m.cubo("bochecha_e", [4.6, 37, -8], [4.6, 49, 6], uv_de="bochecha_d"),
        m.cubo("crina_1", [-0.8, 45, -9], [-0.8, 59, 11], plano(crina_arr, "x")),
        m.cubo("crina_2", [0.8, 45, -9], [0.8, 59, 11], uv_de="crina_1"),
        m.cubo("coroa", [-1.5, 46, -8], [1.5, 48, -2], metal),
    ])
    pesc = m.osso("pescoco", [0, 34, -2], [-8, 0, 0], [
        m.cubo("pescoco", [-4, 33, -7], [4, 42, 1], gola),
        m.cubo("juba_baixa", [-6, 32, -8], [6, 38, 3], juba(4)),
        m.cubo("juba_alta", [-5, 37, -8], [5, 42, 2], juba(0)),
        cab,
    ])

    penas = []
    for i, (x, ry, var) in enumerate([(0, 0, 0), (-1.5, 12, 1), (1.5, -12, 1), (-3, 24, 0), (3, -24, 0)]):
        kw = dict(pintor=plano(arte_cauda(var), "x")) if i < 2 else dict(uv_de=f"cauda_pena_{var}")
        nome = f"cauda_pena_{i}"
        penas.append(m.osso(nome, [x, 22, 7], [0, ry, 0], [m.cubo(nome, [x, 10, 6], [x, 26, 40], **kw)]))
    cauda = m.osso("cauda", [0, 22, 7], [-5, 0, 0], [
        m.cubo("cauda_base", [-3, 19, 5], [3, 25, 10], penas_armadura), *penas])
    return [corpo, pesc, cauda, perna(-1), perna(1), asa(-1), asa(1)]

if __name__ == "__main__":
    RNG.seed(1)
    m = Modelo(NOME)
    caminho, n, tam = m.salvar(montar(m), largura=256, pasta=PASTA)
    q = previa.carregar(str(caminho))
    vistas = [("frente", 0, -6), ("lado", 90, -4), ("3/4 frente", -35, -12), ("costas", 180, -6)]
    ims = [(v, previa.desenhar(q, y, p, escala=6)) for v, y, p in vistas]
    H = max(i.height for _, i in ims) + 24
    folha = Image.new("RGB", (sum(i.width for _, i in ims) + 30, H), (22, 24, 29)); x = 0
    for v, i in ims:
        folha.paste(i, (x, 24 + (H - 24 - i.height))); ImageDraw.Draw(folha).text((x + 8, 6), v, fill=(220, 220, 220))
        x += i.width + 10
    folha.save(PASTA / f"{NOME}_previa.png")
    alt = max(p[1] for qd in q for p in qd[0])
    print(f"{n} cubos, textura {tam}, topo {alt:.0f}px (no jogo, escala 0.5: {alt/32:.2f} blocos)")
