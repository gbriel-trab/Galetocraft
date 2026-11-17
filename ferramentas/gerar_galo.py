"""Gera o galo de briga como entidade (Blockbench "Modded Entity", box UV).
Saída: modelos/<ARQUIVO>.bbmodel e modelos/galo_de_briga.png
Coordenadas no espaço do Blockbench: Y para cima (chão = 0), frente do bicho = -Z (norte).

v2: garras nos pés, bico bem aberto e um sol saindo da boca.
v3: cabeça monstruosa (maior, mandíbulas com dentes pontudos, testa saliente, olhos de brasa,
    cicatriz, crista com espinhos e juba desfiada no pescoço)."""
import base64, io, json, random, uuid
from pathlib import Path
from PIL import Image

NOME = "galo_de_briga"
ARQUIVO = "galo_de_briga_v4"   # v4: silhueta de sol na boca + boca flamejante
SAIDA = Path(__file__).resolve().parent.parent / "modelos"
SAIDA.mkdir(exist_ok=True)
TEX = 64            # largura da textura; a altura cresce para 128 se precisar
rng = random.Random(7)

# ---------------- paleta (galo "preto-vermelho", o clássico de briga) ----------------
PRETO = [(24, 26, 30), (32, 36, 40), (28, 42, 36)]
BRILHO = [(40, 74, 56), (46, 88, 66)]                 # reflexo verde nas penas pretas
LARANJA = [(226, 128, 36), (240, 154, 52), (210, 108, 30)]
DOURADO = [(252, 192, 86), (246, 176, 70)]
CASTANHO = [(150, 40, 26), (170, 54, 30), (128, 32, 22)]  # vermelho-castanho das costas/asas
BAIO = [(196, 112, 50), (178, 96, 42)]                # parte de baixo da asa
CRISTA = [(212, 40, 40), (230, 64, 56), (176, 28, 32)]
PELE = [(214, 58, 52), (200, 48, 46)]
PERNA = [(224, 184, 70), (210, 166, 56)]
PERNA_ESC = (170, 128, 40)
BICO = [(96, 88, 80), (82, 74, 68)]            # bico escuro: os dentes brancos saltam
BICO_ESC = (50, 44, 40)
BOCA = [(150, 26, 30), (122, 18, 24)]                  # dentro da boca
LINGUA = (206, 74, 78)
ESPORA = (238, 230, 206)
ESPORA_PONTA = (120, 104, 84)
UNHA = [(74, 68, 64), (54, 50, 48)]
UNHA_BRILHO = (138, 128, 116)
OLHO = (22, 16, 14)
OLHO_BRASA = (255, 250, 150)       # olho de monstro (pode brilhar no jogo)
OLHO_BRASA_FUNDO = (255, 150, 30)
OLHEIRA = (46, 10, 14)             # contorno escuro em volta do olho
FOGO_AMARELO = (255, 236, 110)
FOGO_LARANJA = (255, 146, 30)
FOGO_VERMELHO = (228, 60, 22)
PELE_ESC = [(150, 30, 32), (132, 24, 28)]
CICATRIZ = (236, 156, 146)
DENTE = (246, 242, 226)
DENTE_BASE = (214, 200, 160)
SOL_MIOLO = (255, 250, 214)
SOL_CLARO = (255, 236, 130)
SOL = (255, 214, 74)
SOL_BORDA = (255, 168, 40)
SOL_FUNDO = (244, 126, 30)

def r(lista):
    return lista[rng.randrange(len(lista))]

# ---------------- peças ----------------
cubos = {}       # nome -> dict
def cubo(nome, de, ate, pintor=None, espelho_de=None, uv_de=None):
    """espelho_de: usa a textura de outra peça espelhada (lado esquerdo/direito).
    uv_de: usa exatamente a mesma textura de outra peça do mesmo tamanho."""
    w, h, d = (int(round(ate[i] - de[i])) for i in range(3))
    c = {"name": nome, "from": list(de), "to": list(ate), "size": (w, h, d), "pintor": pintor,
         "espelho_de": espelho_de, "uv_de": uv_de, "uuid": str(uuid.uuid4())}
    cubos[nome] = c
    return c["uuid"]

def osso(nome, origem, rot, filhos):
    return {"name": nome, "origin": list(origem), "rotation": list(rot), "color": 0,
            "uuid": str(uuid.uuid4()), "export": True, "mirror_uv": False, "isOpen": True,
            "locked": False, "visibility": True, "autouv": 0, "children": filhos}

# ---- pintores: recebem (face, s, t, W, H) ----
# face: north (frente), south (trás), side (laterais; s=0 é a coluna mais à frente),
#       up (topo; s=0 é a linha da frente), down (baixo)
def p_tronco(face, s, t, W, H):
    if face == "north":                      # peito preto
        if t == 0 and 1 <= s <= W - 2: return r(LARANJA)   # pontas da gola caindo no peito
        return r(BRILHO) if rng.random() < .15 else r(PRETO)
    if face == "side":
        if s <= 1 and t <= 2: return r(LARANJA)            # gola sobre o ombro
        if t <= 1: return r(CASTANHO)
        if t == 2: return r(CASTANHO) if rng.random() < .5 else r(PRETO)
        return r(BRILHO) if rng.random() < .12 else r(PRETO)
    if face == "south":                      # sela laranja em cima, plumagem preta embaixo
        if t <= 1: return r(DOURADO) if rng.random() < .35 else r(LARANJA)
        if t == 2: return r(LARANJA) if rng.random() < .4 else r(PRETO)
        return r(PRETO)
    if face == "up":
        if s <= 2: return r(LARANJA) if rng.random() < .7 else r(DOURADO)
        if s >= H - 2: return r(LARANJA) if rng.random() < .6 else r(DOURADO)
        return r(CASTANHO)
    return r(PRETO)

def p_asa(face, s, t, W, H):
    if face == "side":
        if s >= W - 2 and t >= 2: return r(PRETO)          # pontas das rêmiges
        if t <= 1: return r(CASTANHO)                      # "ombro" da asa
        if t == 2: return r(BRILHO) if rng.random() < .5 else r(PRETO)  # barra da asa
        return r(BAIO)
    if face == "down": return r(PRETO)
    return r(CASTANHO)

def p_coxa(face, s, t, W, H):
    if t == H - 1: return r(PRETO)
    return r(BRILHO) if rng.random() < .2 else r(PRETO)

def p_canela(face, s, t, W, H):
    return PERNA[t % 2]

def p_dedo(face, s, t, W, H):
    if face == "down": return PERNA_ESC
    if face == "up": return PERNA[s % 2]
    return PERNA[(s + 1) % 2] if face == "side" else PERNA[0]

def p_unha(face, s, t, W, H):
    if face == "up": return UNHA_BRILHO
    return UNHA[s % 2]

def p_unha_ponta(face, s, t, W, H):
    if face == "up": return UNHA_BRILHO
    return UNHA[1] if t == H - 1 else UNHA[0]

def p_espora(face, s, t, W, H):
    if face == "south" or (face in ("side", "up", "down") and s == W - 1 and face == "side"):
        return ESPORA_PONTA
    if face in ("up", "down") and s == H - 1: return ESPORA_PONTA
    return ESPORA

def p_pescoco(face, s, t, W, H):
    # penas da gola: listras verticais douradas/laranja, mais avermelhadas perto da cabeça
    if face in ("up", "down"): return r(LARANJA)
    if t <= 1 and rng.random() < .5: return r(CASTANHO)
    return r(DOURADO) if (s + (t // 3)) % 2 == 0 else r(LARANJA)

def p_capa(face, s, t, W, H):
    if face in ("up", "down"): return r(LARANJA)
    if t == H - 1: return r(DOURADO)
    return r(DOURADO) if s % 2 == 0 else r(LARANJA)

def p_cabeca(face, s, t, W, H):
    """Cabeça 6x6x7. Linhas t: 0 = topo ... 5 = base; a boca fica na linha 4."""
    if face == "north":
        if t == 0: return r(PELE_ESC)                            # sombra da testa
        if t == 2 and s in (0, W - 1): return OLHO_BRASA         # olho dobra a quina: aparece de frente
        if t == 3 and s in (0, W - 1): return OLHEIRA
        if t == 4 and 1 <= s <= W - 2: return FOGO_AMARELO       # garganta em chamas
        if t >= 4: return FOGO_VERMELHO
        return r(PELE_ESC) if rng.random() < .2 else r(PELE)
    if face == "down": return r(PELE_ESC)
    if face == "side":
        if (s, t) == (0, 2): return OLHO_BRASA
        if (s, t) == (1, 2): return OLHO_BRASA_FUNDO
        if (s, t) in ((2, 2), (0, 3), (1, 3), (2, 3)): return OLHEIRA
        if (s, t) in ((3, 1), (4, 2), (4, 3), (5, 4)): return CICATRIZ
        if t == 4 and s <= 2: return BOCA[1]                     # canto da boca (sorriso de monstro)
        if s <= 3: return r(PELE_ESC) if rng.random() < .25 else r(PELE)
        if t == 0: return r(CASTANHO)
        return r(DOURADO) if (s + t) % 3 == 0 else r(LARANJA)
    if face == "up":
        if s <= 2: return r(PELE_ESC) if rng.random() < .3 else r(PELE)
        return r(CASTANHO) if rng.random() < .6 else r(LARANJA)
    return r(LARANJA)

def p_testa(face, s, t, W, H):
    return CRISTA[2] if face == "up" else r(PELE_ESC)

def p_dente_cima(face, s, t, W, H):        # dente pendurado: ponta embaixo
    if face == "up": return DENTE_BASE
    if face == "down": return DENTE
    return DENTE if t == H - 1 else DENTE_BASE

def p_dente_baixo(face, s, t, W, H):       # dente para cima: ponta em cima
    if face == "down": return DENTE_BASE
    if face == "up": return DENTE
    return DENTE if t == 0 else DENTE_BASE

def p_juba(face, s, t, W, H):
    """Penas eriçadas em volta do pescoço; a fileira de baixo é desfiada (pixels transparentes)."""
    if face == "down": return None
    if face == "up": return r(LARANJA)
    if t == H - 1: return r(DOURADO) if s % 2 == 0 else None
    if t == 0: return r(CASTANHO) if rng.random() < .5 else r(LARANJA)
    return r(DOURADO) if s % 2 == 0 else r(LARANJA)

def p_bico_cima(face, s, t, W, H):
    if face == "down": return FOGO_LARANJA if (s + t) % 2 else FOGO_VERMELHO   # céu da boca em brasa
    if face == "north" or (face in ("side", "up") and s == 0): return BICO_ESC
    return r(BICO)

def p_bico_baixo(face, s, t, W, H):
    if face == "up": return FOGO_AMARELO if 0 < t < W - 1 and 0 < s < H - 1 else FOGO_VERMELHO  # brasa
    if face == "north" or (face == "side" and s == 0): return BICO_ESC
    return r(BICO)

def p_gancho(face, s, t, W, H):
    return BICO_ESC

def p_crista(face, s, t, W, H):
    return CRISTA[2] if face == "down" else r(CRISTA[:2])

def p_cauda(face, s, t, W, H):
    if face == "up" or (face == "side" and t == 0): return r(BRILHO)
    return r(BRILHO) if rng.random() < .15 else r(PRETO)

def p_foice(face, s, t, W, H):
    if face == "up" or (face == "side" and t == 0): return r(BRILHO)
    return r(PRETO)

def p_jato(face, s, t, W, H):
    if face in ("north", "south"): return SOL_MIOLO
    return SOL_CLARO if t % 2 == 0 else SOL          # listras no sentido do raio

def p_sol_frente(face, s, t, W, H):
    if face == "north": return SOL_MIOLO if (s, t) == (W // 2, H // 2) else SOL_CLARO
    if face == "south": return SOL_FUNDO
    return SOL if (s + t) % 2 == 0 else SOL_BORDA

def p_sol_miolo(face, s, t, W, H):
    if face == "south": return SOL_FUNDO
    cx, cy = (W - 1) / 2, (H - 1) / 2                # brilho redondo em todos os lados
    dist = max(abs(s - cx), abs(t - cy))
    return SOL_MIOLO if dist < 1 else (SOL_CLARO if dist < 2 else SOL)

def p_sol_disco(face, s, t, W, H):
    if face == "north":
        borda = s in (0, W - 1) or t in (0, H - 1)
        return SOL_BORDA if borda else SOL
    if face == "south": return SOL_FUNDO
    return SOL_BORDA

def p_raio(face, s, t, W, H):
    if face == "south": return SOL_FUNDO
    return SOL if (s + t) % 2 == 0 else SOL_BORDA

# ---- montagem (medidas em pixels; 16 = 1 bloco) ----
def pe(lado):
    """Garras: 3 dedos abertos para a frente + 1 para trás, cada um com unha curvada para baixo,
    e uma espora grande. lado = -1 (direita, x negativo) ou +1 (esquerda)."""
    x = 1.5 * lado
    e = "_d" if lado < 0 else "_e"
    def c(nome, de, ate, pintor=None, uv_de=None):
        de = [de[0] + x, de[1], de[2]]; ate = [ate[0] + x, ate[1], ate[2]]
        if lado > 0:
            return cubo(nome + e, de, ate, espelho_de=nome + "_d")
        return cubo(nome + e, de, ate, pintor, uv_de=(uv_de + "_d") if uv_de else None)
    abre = 28 * lado   # quanto os dedos laterais abrem (graus, eixo Y)
    return [
        c("coxa",   [-1, 6, -1], [1, 9, 2], p_coxa),
        c("canela", [-0.5, 2, 0], [0.5, 6, 1], p_canela),
        # cada unha = pedaço reto para a frente + ponta descendo até o chão (forma de gancho)
        osso("dedo_meio" + e, [x, 1.5, 0.5], [0, 0, 0], [
            c("dedo_meio", [-0.5, 1, -3], [0.5, 2, 1], p_dedo),
            c("unha_meio", [-0.5, 1, -5], [0.5, 2, -3], p_unha),
            c("unha_ponta_meio", [-0.5, 0, -5], [0.5, 1, -4], p_unha_ponta),
        ]),
        osso("dedo_fora" + e, [x, 1.5, 0.5], [0, -abre, 0], [
            c("dedo_fora", [-0.5, 1, -2], [0.5, 2, 1], p_dedo),
            c("unha_fora", [-0.5, 1, -4], [0.5, 2, -2], uv_de="unha_meio"),
            c("unha_ponta_fora", [-0.5, 0, -4], [0.5, 1, -3], uv_de="unha_ponta_meio"),
        ]),
        osso("dedo_dentro" + e, [x, 1.5, 0.5], [0, abre, 0], [
            c("dedo_dentro", [-0.5, 1, -2], [0.5, 2, 1], uv_de="dedo_fora"),
            c("unha_dentro", [-0.5, 1, -4], [0.5, 2, -2], uv_de="unha_meio"),
            c("unha_ponta_dentro", [-0.5, 0, -4], [0.5, 1, -3], uv_de="unha_ponta_meio"),
        ]),
        c("dedo_tras", [-0.5, 1, 1], [0.5, 2, 3], p_dedo),
        c("unha_tras", [-0.5, 0, 3], [0.5, 2, 4], p_unha_ponta),
        c("espora", [-0.5, 3, 1], [0.5, 4, 3.5 - 0.5], p_espora),
    ]

perna_d = osso("perna_direita", [-1.5, 9, 0.5], [0, 0, 0], pe(-1))
perna_e = osso("perna_esquerda", [1.5, 9, 0.5], [0, 0, 0], pe(+1))

asa_d = osso("asa_direita", [-3, 12, -3], [0, 0, 0], [
    cubo("asa_d", [-4, 8, -3.5], [-3, 12, 3.5], p_asa)])
asa_e = osso("asa_esquerda", [3, 12, -3], [0, 0, 0], [
    cubo("asa_e", [3, 8, -3.5], [4, 12, 3.5], espelho_de="asa_d")])
corpo = osso("corpo", [0, 10, 0], [30, 0, 0], [
    cubo("tronco", [-3, 7, -4], [3, 13, 4], p_tronco),
    asa_d, asa_e,
])
# cauda em arco: sobe (-50°), segue para trás (-20°) e as pontas das foices caem (+30°)
foices = osso("foices", [0, 10.5, 8], [30, 0, 0], [
    cubo("foice", [-0.5, 9.5, 7], [0.5, 11.5, 12], p_foice),
    cubo("foice_baixa", [-1, 9, 7], [1, 10, 11], p_cauda),
    osso("foices_pontas", [0, 10.5, 12], [50, 0, 0], [
        cubo("foice_ponta", [-0.5, 9.5, 11], [0.5, 11.5, 15], p_foice),
    ]),
])
cauda = osso("cauda", [0, 10, 4], [-50, 0, 0], [
    cubo("cauda_base", [-1.5, 9, 3], [1.5, 11, 8], p_cauda),
    foices,
])

# boca flamejante: silhueta de sol (plano fino com recorte) dentro da boca + chamas.
# Os planos têm espessura 0 e usam pixels transparentes para o recorte do sol e das labaredas.
SY = 19.5           # altura do centro da boca

def cor_fogo(f):    # f = 0 (base da chama) .. 1 (ponta)
    return FOGO_AMARELO if f < .34 else (FOGO_LARANJA if f < .7 else FOGO_VERMELHO)

def p_sol_silhueta(face, s, t, W, H):
    """Ícone de sol 7x7: miolo 3x3 redondinho + 8 raios soltos; o resto é transparente."""
    if face not in ("north", "south"): return None
    dx, dy = s - (W - 1) / 2, t - (H - 1) / 2
    if abs(dx) <= 1 and abs(dy) <= 1:
        if dx == 0 and dy == 0: return SOL_MIOLO
        return SOL if abs(dx) == abs(dy) else SOL_CLARO
    if (abs(dx), abs(dy)) in ((3, 0), (0, 3), (2, 2)): return SOL_BORDA
    return None

ALTURAS_CHAMA = [2, 5, 3, 4]
def p_chama_sobe(face, s, t, W, H):
    """Labaredas subindo: cada coluna tem uma altura; amarelo embaixo, vermelho nas pontas."""
    if face in ("up", "down"): return None
    alt = min(ALTURAS_CHAMA[s % len(ALTURAS_CHAMA)], H)
    hb = H - t                                    # altura deste pixel a partir da base
    if hb > alt: return None
    return cor_fogo((hb - 1) / max(alt - 1, 1))

COMPR_JATO = [3, 6, 5, 2]
def p_chama_jato(face, s, t, W, H):
    """Língua de fogo saindo da boca para a frente (plano visto de lado)."""
    if face != "side": return None
    L = min(COMPR_JATO[t % len(COMPR_JATO)], W)
    de_tras = W - 1 - s                          # 0 = junto da boca
    if de_tras >= L: return None
    return cor_fogo(de_tras / max(L - 1, 1))

def chama_canto(nome, x, ang, primeira):
    """Labareda baixa saindo do canto da boca, virada para fora (fica abaixo dos olhos)."""
    a = dict(pintor=p_chama_sobe) if primeira else dict(uv_de="chama_canto_d")
    return osso(nome, [x, 17, -9], [0, ang, 0], [
        cubo(nome, [x, 16.5, -12], [x, 21.5, -8], **a),
    ])

boca_flamejante = osso("boca_flamejante", [0, SY, -11], [0, 0, 0], [
    # silhueta do sol no meio da boca aberta, entre as presas
    cubo("sol_silhueta", [-3.5, SY - 3.5, -11], [3.5, SY + 3.5, -11], p_sol_silhueta),
    cubo("chama_jato", [0, SY - 2, -17], [0, SY + 2, -11], p_chama_jato),
    chama_canto("chama_canto_d", -2.5, 30, True),
    chama_canto("chama_canto_e", 2.5, -30, False),
])

# cabeça monstruosa: 6x6x7, mandíbulas 4 de largura cheias de dentes
cabeca = osso("cabeca", [0, 18, -3], [10, 0, 0], [
    cubo("cabeca", [-3, 18, -8], [3, 24, -1], p_cabeca),
    cubo("testa", [-3, 22, -9], [3, 23, -8], p_testa),                  # testa saliente (cara de bravo)
    cubo("sobrancelha_d", [-4, 22, -8], [-3, 23, -5], p_testa),
    cubo("sobrancelha_e", [3, 22, -8], [4, 23, -5], espelho_de="sobrancelha_d"),
    osso("bico_cima", [0, 21, -8], [30, 0, 0], [
        cubo("bico_cima", [-2, 20, -13], [2, 22, -8], p_bico_cima),
        cubo("bico_gancho", [-1, 19, -13], [1, 20, -12], p_gancho),
        cubo("presa_cima_d", [-2, 18, -12], [-1, 20, -11], p_dente_cima),
        cubo("presa_cima_e", [1, 18, -12], [2, 20, -11], uv_de="presa_cima_d"),
        cubo("dente_cima_d", [-2, 19, -10], [-1, 20, -9], p_dente_cima),
        cubo("dente_cima_e", [1, 19, -10], [2, 20, -9], uv_de="dente_cima_d"),
    ]),
    osso("bico_baixo", [0, 19, -8], [-45, 0, 0], [
        cubo("bico_baixo", [-2, 17, -12], [2, 19, -8], p_bico_baixo),
        cubo("presa_baixo_d", [-2, 19, -12], [-1, 21, -11], p_dente_baixo),
        cubo("presa_baixo_e", [1, 19, -12], [2, 21, -11], uv_de="presa_baixo_d"),
        cubo("dentes_frente", [-1, 19, -12], [1, 20, -11], p_dente_baixo),
        cubo("dente_baixo_d", [-2, 19, -10], [-1, 20, -9], p_dente_baixo),
        cubo("dente_baixo_e", [1, 19, -10], [2, 20, -9], uv_de="dente_baixo_d"),
    ]),
    cubo("crista", [-1, 24, -7], [1, 25, -1], p_crista),
    cubo("crista_espinho_1", [-0.5, 25, -7], [0.5, 27, -6], p_crista),
    cubo("crista_espinho_2", [-0.5, 25, -5], [0.5, 28, -4], p_crista),
    cubo("crista_espinho_3", [-0.5, 25, -3], [0.5, 27, -2], uv_de="crista_espinho_1"),
    cubo("barbela", [-1.5, 15, -7], [1.5, 18, -6], p_crista),
    boca_flamejante,
])
pescoco = osso("pescoco", [0, 13, -3], [-10, 0, 0], [
    cubo("pescoco", [-2, 12, -5], [2, 18, -1], p_pescoco),
    cubo("gola", [-3, 12, -4.5], [3, 15, 0.5], p_capa),
    cubo("juba", [-3.5, 15, -6], [3.5, 18, 0], p_juba),
    cabeca,
])
outliner = [corpo, pescoco, cauda, perna_d, perna_e]

# ---------------- empacotar UVs (box UV) na textura ----------------
def net(c):
    w, h, d = c["size"]
    return 2 * d + 2 * w, d + h

proprios = [c for c in cubos.values() if not c["espelho_de"] and not c["uv_de"]]
proprios.sort(key=lambda c: (-net(c)[1], -net(c)[0]))
x = y = linha_h = 0
for c in proprios:
    nw, nh = net(c)
    if x + nw > TEX:
        x, y, linha_h = 0, y + linha_h, 0
    c["uv_offset"] = [x, y]
    x += nw
    linha_h = max(linha_h, nh)
TEX_H = 64 if y + linha_h <= 64 else 128
assert y + linha_h <= TEX_H, f"textura não coube ({y + linha_h} > {TEX_H})"
def origem_uv(c):
    ref = c["espelho_de"] or c["uv_de"]
    return list(c["uv_offset"]) if not ref else origem_uv(cubos[ref])
for c in cubos.values():
    c["uv_offset"] = origem_uv(c)
    ref = c["espelho_de"] or c["uv_de"]
    if ref: assert cubos[ref]["size"] == c["size"], f"{c['name']} != {ref}"

def faces_box_uv(c, mirror):
    """Mesma conta que o Blockbench faz para box UV."""
    w, h, d = c["size"]; u, v = c["uv_offset"]
    fl = {"east": [[0, d], [d, h]], "west": [[d + w, d], [d, h]],
          "up": [[d + w, d], [-w, -d]], "down": [[d + 2 * w, 0], [-w, d]],
          "south": [[2 * d + w, d], [w, h]], "north": [[d, d], [w, h]]}
    if mirror:
        for f in fl.values():
            f[0][0] += f[1][0]; f[1][0] *= -1
        fl["east"], fl["west"] = fl["west"], fl["east"]
    return {k: {"uv": [f[0][0] + u, f[0][1] + v, f[0][0] + f[1][0] + u, f[0][1] + f[1][1] + v],
                "texture": 0} for k, f in fl.items()}

# ---------------- pintar a textura ----------------
img = Image.new("RGBA", (TEX, TEX_H), (0, 0, 0, 0))
px = img.load()
for c in proprios:
    w, h, d = c["size"]; u, v = c["uv_offset"]; pint = c["pintor"]
    regs = [
        ("side", u, v + d, d, h, lambda i, j: (d - 1 - i, j)),          # east: frente à direita
        ("north", u + d, v + d, w, h, lambda i, j: (i, j)),
        ("side", u + d + w, v + d, d, h, lambda i, j: (i, j)),          # west: frente à esquerda
        ("south", u + 2 * d + w, v + d, w, h, lambda i, j: (i, j)),
        ("up", u + d, v, w, d, lambda i, j: (d - 1 - j, i)),            # topo: frente embaixo
        ("down", u + d + w, v, w, d, lambda i, j: (d - 1 - j, i)),
    ]
    for face, x0, y0, W, H, mapa in regs:
        for i in range(W):
            for j in range(H):
                s, t = mapa(i, j)
                if face in ("up", "down"):
                    cor = pint(face, s, t, w, d)   # s = profundidade a partir da frente (0..d-1)
                else:
                    cor = pint(face, s, t, W, H)
                px[x0 + i, y0 + j] = (0, 0, 0, 0) if cor is None else cor + (255,)

img.save(SAIDA / f"{NOME}.png")
buf = io.BytesIO(); img.save(buf, format="PNG")
data_uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# ---------------- escrever .bbmodel ----------------
def pivo_do_cubo(uid):
    def busca(grupo):
        for f in grupo["children"]:
            if isinstance(f, dict):
                achou = busca(f)
                if achou: return achou
            elif f == uid:
                return grupo["origin"]
    for g in outliner:
        o = busca(g)
        if o: return o
    return [0, 0, 0]

elements = []
for c in cubos.values():
    mirror = bool(c["espelho_de"])
    elements.append({
        "name": c["name"], "box_uv": True, "rescale": False, "locked": False,
        "from": c["from"], "to": c["to"], "autouv": 0, "color": 0,
        "origin": pivo_do_cubo(c["uuid"]), "uv_offset": c["uv_offset"],
        "mirror_uv": mirror, "faces": faces_box_uv(c, mirror), "type": "cube", "uuid": c["uuid"],
    })

bbmodel = {
    "meta": {"format_version": "4.10", "model_format": "modded_entity", "box_uv": True},
    "name": NOME,
    "model_identifier": NOME,
    "modded_entity_entity_class": "",
    "modded_entity_version": "1.17",
    "modded_entity_flip_y": True,
    "visible_box": [1, 1, 0],
    "resolution": {"width": TEX, "height": TEX_H},
    "elements": elements,
    "outliner": outliner,
    "textures": [{"path": "", "name": f"{NOME}.png", "folder": "entity", "namespace": "", "id": "0",
                  "width": TEX, "height": TEX_H, "uv_width": TEX, "uv_height": TEX_H,
                  "particle": False, "render_mode": "default", "visible": True, "internal": True,
                  "saved": False, "uuid": str(uuid.uuid4()), "relative_path": "", "source": data_uri}],
    "animations": [],
}
(SAIDA / f"{ARQUIVO}.bbmodel").write_text(json.dumps(bbmodel, indent=1), encoding="utf-8")
print("ok:", len(elements), "cubos, textura usada até y =", y + linha_h, "->", SAIDA / f"{ARQUIVO}.bbmodel")
