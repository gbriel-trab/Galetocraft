"""Pirococó (#001, Inicial de Fogo): fênix-galo da ficha do usuário.
Altura ~1,5 bloco (24 px); asas abertas e erguidas, crina de 3 pontas, olhos azuis,
penas-armadura (vermelho/laranja/amarelo com azul), pernas e garras douradas, cauda longa.
Saída: modelos/pirococo/pirococo.bbmodel + .png + pirococo_previa.png"""
import math, sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from galos_monstro import Modelo, r, RNG, fogo_sobe
import previa
from PIL import Image, ImageDraw

PASTA = AQUI.parent / "modelos" / "pirococo"

# ---------------- paleta (da ficha) ----------------
VERM = [(214, 28, 30), (198, 22, 28), (230, 46, 36)]
VERM_ESC = [(140, 14, 22), (122, 10, 20)]
LARANJA = [(255, 122, 24), (244, 104, 20)]
AMARELO = [(255, 200, 48), (255, 214, 80)]
DOURADO = [(232, 170, 44), (214, 150, 34)]
DOURADO_CLARO = (255, 206, 72)
DOURADO_ESC = (150, 96, 20)
AZUL = [(40, 108, 232), (30, 90, 214)]
AZUL_ESC = [(22, 50, 156), (18, 40, 132)]
OLHO = (70, 160, 255)
OLHO_CLARO = (190, 235, 255)
CONTORNO = (40, 8, 12)
FOGO = [(255, 236, 110), (255, 146, 30), (228, 60, 22)]

def escuro(c, k=0.72): return tuple(int(v * k) for v in c)

# ---------------- pintores ----------------
def penas(base, borda, destaque=None, chance=.15):
    """Penas em escamas: fileiras alternadas com bordas escuras (efeito 'armadura')."""
    def p(face, s, t, W, H):
        if t % 2 == 1 and (s + t // 2) % 3 == 0: return r(borda)
        return r(destaque) if destaque and RNG.random() < chance else r(base)
    return p

def p_tronco(face, s, t, W, H):
    if face == "north": return r(AMARELO) if t <= 1 else (r(LARANJA) if t % 2 == 0 else r(AMARELO))
    if face == "down": return r(VERM_ESC)
    if face == "up": return r(LARANJA) if s <= 2 else penas(VERM, VERM_ESC)(face, s, t, W, H)
    if face == "side" and s <= 1 and t <= 3: return r(LARANJA)
    return penas(VERM, VERM_ESC, LARANJA)(face, s, t, W, H)

def p_peito(face, s, t, W, H):
    return r(AMARELO) if (s + t) % 3 else r(LARANJA)

def p_ouro(face, s, t, W, H):          # armadura dourada: linhas claras/escuras
    if face == "up": return DOURADO_CLARO
    if face == "down": return DOURADO_ESC
    return DOURADO_CLARO if t == 0 else (DOURADO_ESC if t == H - 1 else r(DOURADO))

METAL_BRILHO = (255, 228, 112)
METAL_BORDA = (190, 124, 26)
GEMA = [(206, 242, 255), (70, 140, 240), (36, 80, 210)]

def metal(gema=False):
    """Ouro polido: brilho no topo, sombra na base, aresta clara no meio, bordas escuras."""
    def p(face, s, t, W, H):
        if face == "up": return METAL_BRILHO
        if face == "down": return DOURADO_ESC
        if gema and face == "north" and abs(s - (W - 1) / 2) <= 0.5 and abs(t - (H - 1) / 2) <= 0.5:
            return GEMA[0] if t < (H - 1) / 2 else GEMA[2]
        if t == 0: return METAL_BRILHO
        if t == H - 1: return DOURADO_ESC
        if face == "north" and W >= 5 and s == W // 2: return DOURADO_CLARO
        if W > 2 and s in (0, W - 1): return METAL_BORDA
        return DOURADO_CLARO if (s + 2 * t) % 5 == 0 else DOURADO[0]
    return p

def p_canela(face, s, t, W, H):          # canela com placas de metal sobrepostas
    if t % 2 == 1: return DOURADO_ESC
    return METAL_BRILHO if s == 0 else DOURADO[0]
def p_dedo(face, s, t, W, H): return DOURADO_ESC if face == "down" else r(DOURADO)
def p_garra(face, s, t, W, H): return DOURADO_CLARO if face == "up" or t == 0 else (196, 120, 24)

def p_pescoco(face, s, t, W, H):
    if face in ("up", "down"): return r(LARANJA)
    return [r(VERM), r(LARANJA), r(AMARELO)][(s + t // 2) % 3]

def juba(cores, franja, azul_cada=0):
    """Gola de penas com a fileira de baixo desfiada (pixels transparentes)."""
    def p(face, s, t, W, H):
        if face == "down": return None
        if face == "up": return r(cores)
        if t == H - 1: return r(franja) if s % 2 == 0 else None
        if azul_cada and s % azul_cada == 0 and t >= 1: return r(AZUL)
        return r(cores)
    return p

def p_cabeca(face, s, t, W, H):
    if face == "north": return r(VERM) if t < H - 1 else r(AMARELO)
    if face == "side":                                    # olho azul "determinado" com sobrancelha
        if (s, t) == (1, 1): return OLHO_CLARO
        if (s, t) == (2, 1): return OLHO
        if (s, t) in ((1, 0), (2, 0), (3, 0)): return VERM_ESC[1]
        if (s, t) in ((0, 1), (3, 1), (1, 2), (2, 2)): return CONTORNO
        if t >= 2 and s <= 3: return r(AMARELO)
        return r(VERM) if (s + t) % 3 else r(LARANJA)
    if face == "down": return r(AMARELO)
    return r(VERM) if face == "up" else r(LARANJA)

def p_bico(face, s, t, W, H):
    if face == "up": return DOURADO_CLARO
    if face in ("down", "north"): return DOURADO_ESC
    return DOURADO_ESC if s == 0 else r(DOURADO)

def crina(listra_azul=False):
    def p(face, s, t, W, H):
        f = t / max(H - 1, 1)                             # 0 = ponta (em cima)
        if listra_azul and face == "side" and 0.25 < f < 0.8: return r(AZUL)
        return r(AMARELO) if f < .3 else (r(LARANJA) if f < .6 else r(VERM))
    return p

def asa_pintor(raiz_linha, escala=1.0, camada="fundo"):
    """Leque de penas em lâmina saindo da raiz (coluna 0 = junto do corpo)."""
    passo = 16
    angs = list(range(-16, 81, passo))           # 7 penas largas em leque
    def comp(a): return escala * (7 + 9 * math.sin(math.pi * (a + 25) / 110))
    def p(face, s, t, W, H):
        if face not in ("north", "south"): return None
        if face == "south": s = W - 1 - s
        dx, dy = s + 0.5, raiz_linha - t - 0.5
        rad, ang = math.hypot(dx, dy), math.degrees(math.atan2(dy, dx))
        k = round((ang - angs[0]) / passo)
        if not 0 <= k < len(angs): return None
        L = comp(angs[k])
        if rad > L: return None
        f = rad / L
        meia = passo * 0.62 * (1 - f ** 3)       # lâmina larga que afina só na ponta
        fora = abs(ang - angs[k])
        if fora > meia and rad > 4.5: return None
        if camada == "frente":
            cor = VERM[0] if f < .55 else (LARANJA[0] if f < .85 else AMARELO[0])
        else:
            if f < .3: cor = VERM[0]
            elif f < .5: cor = LARANJA[0]
            elif f < .85: cor = AZUL[0] if k % 2 == 0 else VERM[2]
            else: cor = AMARELO[1]
        # sombra só numa borda de cada pena (dá o efeito de lâminas sobrepostas)
        return escuro(cor, .78) if ang - angs[k] < -meia * 0.5 and rad > 4.5 else cor
    return p

def pena_cauda(azul):
    """Pena longa da cauda vista de lado: afina e cai na ponta, com listra azul."""
    def p(face, s, t, W, H):
        if face != "side": return None
        f = s / max(W - 1, 1)
        centro = 1.2 + 2.4 * f * f
        meia = 1.5 * (1 - f ** 1.5) + 0.35
        if abs(t - centro) > meia: return None
        if azul and abs(t - centro) < 0.6 and .2 < f < .8: return r(AZUL)
        return r(VERM) if f < .35 else (r(LARANJA) if f < .7 else r(AMARELO))
    return p

# ---------------- montagem (16 px = 1 bloco; frente = -Z) ----------------
def montar(m):
    def perna(lado):
        x = 2.5 * lado; e = "_d" if lado < 0 else "_e"
        def c(nome, de, ate, pintor=None, uv_de=None):
            de = [de[0] + x, de[1], de[2]]; ate = [ate[0] + x, ate[1], ate[2]]
            if lado > 0: return m.cubo(nome + e, de, ate, espelho_de=nome + "_d")
            return m.cubo(nome + e, de, ate, pintor, uv_de=(uv_de + "_d") if uv_de else None)
        abre = 28 * lado
        return m.osso("perna" + e, [x, 10, 0], [0, 0, 0], [
            c("coxa", [-1.5, 7, -1.5], [1.5, 10, 1.5], penas(VERM, VERM_ESC)),
            c("joelheira", [-1, 6, -2.5], [1, 8, -1.5], metal()),
            c("canela", [-0.5, 2, -0.5], [0.5, 7, 0.5], p_canela),
            m.osso("dedo_meio" + e, [x, 1.5, 0], [0, 0, 0], [
                c("dedo_meio", [-0.5, 1, -3.5], [0.5, 2, 0.5], p_dedo),
                c("garra_meio", [-0.5, 1, -5.5], [0.5, 2, -3.5], p_garra),
                c("garra_ponta_meio", [-0.5, 0, -5.5], [0.5, 1, -4.5], p_garra)]),
            m.osso("dedo_fora" + e, [x, 1.5, 0], [0, -abre, 0], [
                c("dedo_fora", [-0.5, 1, -2.5], [0.5, 2, 0.5], p_dedo),
                c("garra_fora", [-0.5, 1, -4.5], [0.5, 2, -2.5], uv_de="garra_meio"),
                c("garra_ponta_fora", [-0.5, 0, -4.5], [0.5, 1, -3.5], uv_de="garra_ponta_meio")]),
            m.osso("dedo_dentro" + e, [x, 1.5, 0], [0, abre, 0], [
                c("dedo_dentro", [-0.5, 1, -2.5], [0.5, 2, 0.5], uv_de="dedo_fora"),
                c("garra_dentro", [-0.5, 1, -4.5], [0.5, 2, -2.5], uv_de="garra_meio"),
                c("garra_ponta_dentro", [-0.5, 0, -4.5], [0.5, 1, -3.5], uv_de="garra_ponta_meio")]),
            c("dedo_tras", [-0.5, 1, 0.5], [0.5, 2, 2.5], p_dedo),
            c("garra_tras", [-0.5, 0, 2.5], [0.5, 2, 3.5], p_garra),
            c("espora", [-0.5, 3, 0.5], [0.5, 4, 2.5], p_garra),
        ])

    corpo = m.osso("corpo", [0, 12, 0], [30, 0, 0], [
        m.cubo("tronco", [-4, 8, -4], [4, 15, 5], p_tronco),
        m.cubo("peito", [-3, 9, -5], [3, 14, -4], p_peito),
        # armadura metálica
        m.cubo("peitoral", [-3.5, 9.5, -6], [3.5, 13.5, -5], metal(gema=True)),
        m.cubo("ombreira_d", [-5.5, 13, -3.5], [-3.5, 16, 1.5], metal()),
        m.cubo("ombreira_e", [3.5, 13, -3.5], [5.5, 16, 1.5], espelho_de="ombreira_d"),
        m.cubo("ombreira_espinho_d", [-5, 16, -2], [-4, 18, -1], metal()),
        m.cubo("ombreira_espinho_e", [4, 16, -2], [5, 18, -1], espelho_de="ombreira_espinho_d"),
    ])

    RAIZ, WA, HA = 11, 18, 16            # asa: plano 18x16, raiz na linha 11
    def asa(lado):
        e = "_d" if lado < 0 else "_e"; x0 = 4 * lado
        xs = (lambda a, b: [x0 - b, x0 - a]) if lado < 0 else (lambda a, b: [x0 + a, x0 + b])
        def c(nome, de, ate, pintor):
            if lado > 0: return m.cubo(nome + e, de, ate, espelho_de=nome + "_d")
            return m.cubo(nome + e, de, ate, pintor)
        bx = xs(0, WA); ax = xs(0, 5)
        return m.osso("asa" + e, [x0, 15, 0], [0, 20 * -lado, 0], [
            c("asa_penas", [bx[0], 15 - (HA - RAIZ), 0.5], [bx[1], 15 + RAIZ, 0.5], asa_pintor(RAIZ)),
            c("asa_cobertura", [bx[0], 15 - (HA - RAIZ), -0.5], [bx[1], 15 + RAIZ, -0.5],
              asa_pintor(RAIZ, 0.55, "frente")),
            c("asa_braco", [ax[0], 14, -1.5], [ax[1], 17, 1.5], penas(VERM, VERM_ESC, DOURADO)),
            c("bracadeira_1", [xs(1, 2)[0], 13.5, -2], [xs(1, 2)[1], 17.5, 2], metal()),
            c("bracadeira_2", [xs(3, 4)[0], 13.5, -2], [xs(3, 4)[1], 17.5, 2], metal()),
        ])

    cabeca = m.osso("cabeca", [0, 19, -3], [5, 0, 0], [
        m.cubo("cabeca", [-2, 19, -7], [2, 23, -1], p_cabeca),
        m.cubo("bico", [-1, 20, -10], [1, 22, -7], p_bico),
        m.cubo("bico_gancho", [-0.5, 19, -10], [0.5, 20, -9], p_bico),
        m.cubo("bico_baixo", [-0.5, 19, -9], [0.5, 20, -7], p_bico),
        # elmo: placa da testa com ponta entre os olhos, protetores do rosto e coroa da crina
        m.cubo("elmo_testa", [-2, 22, -8], [2, 23, -7], metal()),
        m.cubo("elmo_ponta", [-0.5, 21, -8], [0.5, 22, -7], metal()),
        m.cubo("elmo_rosto_d", [-3, 20, -6], [-2, 21, -3], metal()),
        m.cubo("elmo_rosto_e", [2, 20, -6], [3, 21, -3], espelho_de="elmo_rosto_d"),
        m.cubo("elmo_coroa", [-1, 23, -6], [1, 24, -1], metal()),
        # crina com exatamente 3 pontas, varrendo para trás
        m.osso("crina_1", [0, 22.5, -5], [-40, 0, 0], [m.cubo("crina_1", [-0.5, 22.5, -5.5], [0.5, 27.5, -4.5], crina())]),
        m.osso("crina_2", [0, 22.5, -3.5], [-55, 0, 0], [m.cubo("crina_2", [-0.5, 22.5, -4], [0.5, 28.5, -3], crina(True))]),
        m.osso("crina_3", [0, 22.5, -2], [-70, 0, 0], [m.cubo("crina_3", [-0.5, 22.5, -2.5], [0.5, 26.5, -1.5], crina())]),
    ])
    pescoco = m.osso("pescoco", [0, 15, -3], [-15, 0, 0], [
        m.cubo("pescoco", [-2, 14, -5], [2, 20, -1], p_pescoco),
        m.cubo("juba_baixa", [-3.5, 14, -6], [3.5, 17, 1], juba(VERM + LARANJA, LARANJA, azul_cada=3)),
        m.cubo("juba_alta", [-3, 17, -6], [3, 20, 0], juba(LARANJA + AMARELO, AMARELO)),
        cabeca,
    ])

    penas_cauda = []
    for i, (rx, ry, L, x, azul) in enumerate([(-10, 0, 17, 0, True), (5, 14, 15, -1, False),
                                              (5, -14, 15, 1, False), (20, 26, 13, -1.5, True),
                                              (20, -26, 13, 1.5, True), (30, 0, 14, 0, False)]):
        penas_cauda.append(m.osso(f"pena_cauda_{i}", [x, 12, 5], [rx, ry, 0], [
            m.cubo(f"pena_cauda_{i}", [x, 8, 5], [x, 13, 5 + L], pena_cauda(azul))]))
    cauda = m.osso("cauda", [0, 12, 5], [15, 0, 0], [
        m.cubo("cauda_base", [-2, 10, 4], [2, 13, 7], penas(VERM, VERM_ESC, LARANJA)),
        m.cubo("anel_cauda", [-2.5, 9.5, 5], [2.5, 13.5, 6], metal()),
        *penas_cauda,
        m.osso("chama_cauda", [0, 11, 8], [-15, 0, 0], [
            m.cubo("chama_cauda", [-2, 11, 8], [2, 16, 8], fogo_sobe(FOGO, (3, 5, 4, 2)))]),
    ])
    return [corpo, pescoco, cauda, perna(-1), perna(1), asa(-1), asa(1)]

if __name__ == "__main__":
    RNG.seed(1)
    m = Modelo("pirococo")
    caminho, n, tam = m.salvar(montar(m), largura=128, pasta=PASTA)
    q = previa.carregar(str(caminho))
    vistas = [("frente", 0, -8), ("costas", 180, -8), ("lado", 90, -5), ("3/4 frente", -35, -15)]
    ims = [(v, previa.desenhar(q, y, p, escala=11)) for v, y, p in vistas]
    H = max(i.height for _, i in ims) + 24
    folha = Image.new("RGB", (sum(i.width for _, i in ims) + 30, H), (22, 24, 29)); x = 0
    for v, i in ims:
        folha.paste(i, (x, 24 + (H - 24 - i.height))); ImageDraw.Draw(folha).text((x + 8, 6), v, fill=(220, 220, 220))
        x += i.width + 10
    folha.save(PASTA / "pirococo_previa.png")
    alt = max(p[1] for qd in q for p in qd[0])
    print(f"{n} cubos, textura {tam}, altura máx {alt:.1f}px = {alt/16:.2f} blocos")
