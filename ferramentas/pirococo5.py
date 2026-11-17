"""Pirococó v5: refeito parte a parte para ser fiel à ficha Galetocraft #001 (voxel).

- Capa de asas em FILEIRAS sobrepostas: roxo (ombros) -> vermelho -> laranja -> amarelo, descendo pelos
  lados e pelas costas e abrindo para fora.
- Cauda em CHAFARIZ: plumas grossas que sobem quase até a altura da cabeça e caem em arco.
- 4 correntes de contas amarelas com PINGENTES DE DIAMANTE grandes (moldura de ouro + gema vermelha).
- Elmo roxo com viseira, rosto branco, olho vermelho bravo, bico amarelo em gancho, penas vermelhas
  escapando do elmo, chamas entre os chifres, chifres grossos em crescente e tiara com diamante vertical.
- Peitoral roxo em escudo com fênix de asas para cima; botas roxas robustas e pés de dedos gordos.
Estilo Cobblemon: 16 px = 1 bloco, cores chapadas com luz/sombra, sem ruído."""
import sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from galos_monstro import Modelo
import previa
from PIL import Image, ImageDraw

PASTA = AQUI.parent / "modelos" / "pirococo"
NOME = "pirococo_v5"

ROXO_ESC = (66, 34, 118); ROXO = (118, 70, 190); LILAS = (178, 144, 230)
BRANCO = (244, 240, 238); BRANCO_SOMBRA = (204, 196, 206)
AMARELO = (255, 208, 50); AMARELO_CLARO = (255, 232, 120); AMARELO_ESC = (224, 160, 28)
LARANJA = (255, 140, 30); LARANJA_ESC = (226, 104, 20)
VERM = (222, 40, 32); VERM_ESC = (148, 20, 30)
OURO = (244, 180, 42); OURO_CLARO = (255, 228, 112); OURO_ESC = (170, 110, 20)
PRETO = (28, 14, 22)

def clara(c, k=.2): return tuple(int(v + (255 - v) * k) for v in c)
def esc(c, k=.75): return tuple(int(v * k) for v in c)

# ---------------- pintores ----------------
def liso(base, topo=None, baixo=None):
    def p(face, s, t, W, H):
        if face == "up": return clara(topo or base, .15)
        if face == "down": return esc(baixo or base)
        if t == 0 and H > 2: return clara(base, .15)
        if t == H - 1 and H > 2: return esc(base, .85)
        return base
    return p

def lamina(cor, ponta=None):
    """Pena-lâmina vertical: topo mais escuro, corpo na cor, última fileira mais clara."""
    def p(face, s, t, W, H):
        if face == "up": return esc(cor, .8)
        if face == "down": return ponta or clara(cor, .25)
        if t == 0: return esc(cor, .82)
        if t >= H - 1: return ponta or clara(cor, .2)
        return cor
    return p

def pluma(cor_a, cor_b):
    """Segmento de pluma (comprido no eixo Z): degradê de cor_a (raiz) para cor_b (ponta)."""
    def p(face, s, t, W, H):
        if face == "north": return cor_a
        if face == "south": return cor_b
        if face == "side": f = s / max(W - 1, 1)
        else: f = s / max(H - 1, 1)
        c = cor_a if f < .5 else cor_b
        return clara(c, .12) if face == "up" else esc(c) if face == "down" else c
    return p

def lamina_pluma(a, b):
    """Lâmina de pluma vista de lado: borda clara em cima, escura embaixo, degradê a->b ao longo."""
    def p(face, s, t, W, H):
        if face == "side":
            c = a if s / max(W - 1, 1) < .5 else b
            if t == 0: return clara(c, .28)
            if t == H - 1: return esc(c, .78)
            return c
        if face == "up": return clara(a, .2)
        if face == "down": return esc(a, .75)
        return a if face == "north" else b
    return p

def desenho(face_alvo, linhas, cores, resto):
    def p(face, s, t, W, H):
        if face == face_alvo:
            ch = linhas[t][s]
            return None if ch == "." else cores[ch]
        return resto(face, s, t, W, H)
    return p

def losango(cor_claro, cor, cor_esc, oco=False):
    """Face lateral (eixo X fino) em forma de losango; oco=True deixa o miolo vazado (moldura)."""
    def p(face, s, t, W, H):
        cx, cy = (W - 1) / 2, (H - 1) / 2
        d = abs(s - cx) / (W / 2) + abs(t - cy) / (H / 2)
        if d > 1.02: return None
        if oco and d < .45: return None
        if face in ("up", "down"): return cor
        return cor_claro if t < cy - .5 else (cor if t <= cy + .5 else cor_esc)
    return p

def cranio(face, s, t, W, H):
    """Crânio por baixo do elmo: rosto branco com o olho (íris vermelha, pupila escura) na frente.
    Lado: W=7 (s=0 frente), H=6 (t=0 topo)."""
    if face == "down": return BRANCO_SOMBRA
    if face == "north":
        if t <= 2: return ROXO
        if s in (0, W - 1) and t == 3: return VERM
        if s in (0, W - 1) and t == 4: return VERM_ESC
        return BRANCO
    if face == "side":
        olho = {(0, 3): BRANCO, (1, 3): VERM, (2, 3): VERM,
                (0, 4): BRANCO, (1, 4): PRETO, (2, 4): VERM_ESC}
        if (s, t) in olho: return olho[(s, t)]
        if t >= 2 and s <= 3: return BRANCO
        return VERM
    return ROXO if face == "up" else VERM

# protetor lateral do elmo (8 de comprimento x 6 de altura, s=0 = frente): calota em cima, borda escura
# descendo sobre o olho (cara brava) e protetor roxo atrás do olho até a mandíbula; '.' = abertura
MASCARA = [
    "LLLLLLLL",
    "PPPPPPPP",
    "DDDDPPPP",
    "D...PPPP",
    "....PPPP",
    "....PPPD",
]
CORES_MASC = {"L": LILAS, "P": ROXO, "D": ROXO_ESC}

def elmo(face, s, t, W, H):
    """Calota/viseira do elmo: roxo com borda lilás em cima e sombra embaixo."""
    if face == "up": return LILAS
    if face == "down": return ROXO_ESC
    if t == 0: return LILAS
    if t == H - 1: return ROXO_ESC
    return ROXO

def bico(face, s, t, W, H):
    """Bico amarelo: topo claro, barriga laranja, narina escura perto do rosto."""
    if face == "up": return AMARELO_CLARO
    if face == "down": return LARANJA_ESC
    if face == "side" and (s, t) == (W - 2, 0): return (120, 66, 18)
    if face == "north": return AMARELO_ESC
    return AMARELO if t < H - 1 else LARANJA

# Peitoral Fênix (como na ficha): escudo com moldura roxa grossa, fundo vermelho e a fênix amarela/laranja
# de asas abertas. Parte de cima (8x6) + degraus que fecham em V embaixo.
ESCUDO = [
    "LLLDDLLL",
    "PRRDDRRP",
    "PYRRRRYP",
    "PYYRRYYP",
    "PRYYYYRP",
    "PROYYORP",
]
ESCUDO_V = ["PRYYRP", "POOP", "PP"]                    # fileiras que fecham a ponta do V
CHEVRON = ["POOOOP", "POOP", "DD"]                     # segundo V menor, logo abaixo
CORES_EMB = {"L": LILAS, "P": ROXO, "D": ROXO_ESC, "Y": AMARELO, "O": LARANJA, "R": VERM}

def bota(face, s, t, W, H):
    if face == "up": return LILAS
    if face == "down": return ROXO_ESC
    if t == 0: return LILAS
    if t == H - 1: return ROXO_ESC
    return ROXO

def dedo(face, s, t, W, H):
    if face == "up": return AMARELO_CLARO
    if face in ("down", "north"): return AMARELO_ESC
    return AMARELO if s > 0 else AMARELO_ESC

# ---------------- montagem ----------------
def grad(f, faixas):
    for lim, c in faixas:
        if f <= lim + 1e-6: return c
    return faixas[-1][1]

# Capa de asas (como na ficha): penas em forma de FOLHA, longas, largas e pontudas, com degradê
# vermelho -> laranja -> amarelo ao longo do comprimento, pendendo do manto roxo em volta do corpo.
# 4 combinações de cor para as penas não ficarem repetidas (como na ficha: umas mais vermelhas,
# outras mais laranja, outras com mais amarelo)
COR_A = [(.40, VERM), (.72, LARANJA), (1.0, AMARELO)]                    # padrão
COR_B = [(.30, VERM_ESC), (.65, VERM), (1.0, LARANJA)]                   # mais escura/vermelha
COR_C = [(.25, VERM), (.55, LARANJA), (1.0, AMARELO)]                    # mais amarela
COR_D = [(.55, VERM), (1.0, LARANJA_ESC)]                                # vermelho com ponta laranja
COR_E = [(.30, LARANJA_ESC), (.60, LARANJA), (1.0, AMARELO)]              # laranja puxando para o amarelo
COR_ROXO = [(.30, LILAS), (.75, ROXO), (1.0, ROXO_ESC)]                  # cobertura roxa da asa
# ASA DOBRADA cobrindo a lateral do corpo (como na vista lateral da ficha): fileiras que apontam para
# TRÁS e para BAIXO na diagonal. A cobertura roxa fica por fora/em cima; as fileiras de baixo são mais
# longas: roxo -> vermelho -> laranja -> amarelo.
# lado direito (o esquerdo é espelho): (x, z, y da raiz, varre p/ trás °, abre p/ fora °, comprimento,
#   face larga virada p/ frente?, cores, cor da ponta, largura)
PENAS_CAPA = [
    (-5.4, -1.2, 19.5, 40, 16, 6, False, COR_ROXO, ROXO_ESC, 3),     # cobertura roxa
    (-5.4, 1.6, 19.5, 52, 16, 6, False, COR_ROXO, ROXO_ESC, 3),
    (-5.1, -2.0, 18.5, 42, 22, 9, False, COR_B, VERM, 3),            # fileira vermelha
    (-5.1, 1.0, 18.5, 54, 22, 9, False, COR_D, LARANJA_ESC, 3),
    (-4.8, -1.2, 17.5, 46, 27, 11, False, COR_A, AMARELO, 4),        # fileira laranja
    (-4.8, 2.0, 17.5, 58, 27, 11, False, COR_E, AMARELO, 4),
    (-4.5, -2.4, 16.5, 40, 30, 13, False, COR_C, AMARELO_CLARO, 4),  # fileira amarela, a mais longa
    (-4.5, 1.0, 16.5, 52, 30, 13, False, COR_E, AMARELO_CLARO, 4),
    (-4.2, -3.6, 17.5, -4, 18, 9, True, COR_D, LARANJA, 3),          # frente: cobre a coxa ao lado do escudo
    (-2.2, 4.6, 18.5, 32, 12, 11, True, COR_A, AMARELO, 3),          # costas, ao lado da coluna central
]
# coluna central de penas vermelhas nas costas (vista traseira da ficha), sem espelho
PENAS_CAPA_CENTRO = [
    (0.0, 4.8, 20.0, 20, 0, 9, True, COR_B, VERM, 3),
    (0.0, 4.8, 15.5, 30, 0, 9, True, COR_D, LARANJA, 3),
]

def pena_folha(faixas):
    """Pena-folha pendurada: degradê do topo (t=0) até a ponta, borda clara de um lado e escura do outro."""
    def p(face, s, t, W, H):
        if face == "up": return esc(faixas[0][1], .85)
        if face == "down": return grad(1.0, faixas)
        c = grad(t / max(H - 1, 1), faixas)
        if s == 0 and W > 1: return clara(c, .2)
        if s == W - 1 and W > 1: return esc(c, .85)
        return c
    return p

def montar(m):
    def lado_cubo(nome, lado, de, ate, pintor):
        """Cria o cubo do lado direito (pintado) ou o espelho no esquerdo."""
        e = "_d" if lado < 0 else "_e"
        if lado > 0:
            de, ate = [-ate[0], de[1], de[2]], [-de[0], ate[1], ate[2]]
            return m.cubo(nome + e, de, ate, espelho_de=nome + "_d")
        return m.cubo(nome + e, de, ate, pintor)

    # ---- capa de asas: penas-folha penduradas em volta do corpo ----
    def pena_capa(nome, dados, lado):
        """lado=-1 direita (pintada), +1 esquerda (espelho), 0 = centro (sem espelho)."""
        x, z, y, varre, abre, L, larga_frente, faixas, ponta, larg = dados
        wx, wz = (larg, 2) if larga_frente else (2, larg)
        partes = [  # corpo da folha, ponta mais estreita e bico final de 1: fica pontuda
            ("", [x - wx / 2, y - (L - 3), z - wz / 2], [x + wx / 2, y, z + wz / 2], pena_folha(faixas)),
            ("_ponta", [x - (wx - 1) / 2, y - (L - 1), z - (wz - 1) / 2], [x + (wx - 1) / 2, y - (L - 3), z + (wz - 1) / 2], liso(ponta)),
            ("_bico", [x - 0.5, y - L, z - 0.5], [x + 0.5, y - (L - 1), z + 0.5], liso(clara(ponta, .25))),
        ]
        if lado == 0:
            filhos = [m.cubo(nome + suf, de, ate, p) for suf, de, ate, p in partes]
            return m.osso(nome, [x, y, z], [-varre, 0, 0], filhos)
        filhos = [lado_cubo(nome + suf, lado, de, ate, p) for suf, de, ate, p in partes]
        e = "_d" if lado < 0 else "_e"
        return m.osso(nome + e, [x if lado < 0 else -x, y, z], [-varre, 0, abre * lado], filhos)

    def capa_de_asas():
        ossos = []
        for lado in (-1, 1):
            for i, dados in enumerate(PENAS_CAPA):
                ossos.append(pena_capa(f"capa_pena_{i}", dados, lado))
        for i, dados in enumerate(PENAS_CAPA_CENTRO):
            ossos.append(pena_capa(f"capa_pena_centro_{i}", dados, 0))
        return ossos

    # ---- Patas Reforçadas (como na ficha) ----
    def calca(face, s, t, W, H):
        """Calça de penas: laranja-escuro em cima, laranja, amarelo embaixo."""
        if face == "up": return VERM
        if face == "down": return AMARELO
        f = t / max(H - 1, 1)
        c = LARANJA_ESC if f < .35 else LARANJA if f < .7 else AMARELO
        return clara(c, .15) if s == 0 and face == "side" else c
    def falange(face, s, t, W, H):
        if face == "up": return AMARELO_CLARO
        if face == "north": return AMARELO
        if face == "down": return LARANJA_ESC
        return AMARELO_ESC if t == H - 1 else AMARELO
    def garra(face, s, t, W, H):
        if face == "up": return AMARELO_CLARO
        if face == "north": return AMARELO_ESC
        if face == "down": return LARANJA_ESC
        return AMARELO_ESC if t == H - 1 else AMARELO

    def perna(lado):
        """Calça de penas laranja/amarela terminando em pontas, bota roxa em carretel
        (aro lilás - meio roxo - aro lilás) e pé de 3 dedos grossos em leque com nó e garra."""
        x = 3 * lado; e = "_d" if lado < 0 else "_e"
        def c(nome, de, ate, pintor):
            de = [de[0] + x, de[1], de[2]]; ate = [ate[0] + x, ate[1], ate[2]]
            if lado > 0: return m.cubo(nome + e, de, ate, espelho_de=nome + "_d")
            return m.cubo(nome + e, de, ate, pintor)
        def dedo(nome, rot):
            return m.osso(nome + e, [x, 1, 0], [0, rot, 0], [
                c(nome, [-1, 1, -4], [1, 3, 0], falange),                 # parte de cima (o "nó")
                c(nome + "_garra", [-1, 0, -6], [1, 2, -4], garra),       # ponta descendo até o chão
            ])
        pontas = [(-1.5, -3.0), (0.5, -3.0), (-3.0, -0.5), (-3.0, 1.5), (0.0, 3.0)]   # (x, z) das pontas da calça
        return m.osso("perna" + e, [x, 13, 0], [0, 0, 0], [
            c("coxa", [-2.5, 7, -2.5], [2.5, 13, 2.5], calca),
            *[c(f"coxa_ponta_{k}", [px - 0.5, 5, pz - 0.5], [px + 0.5, 7, pz + 0.5], liso(AMARELO, baixo=AMARELO_CLARO))
              for k, (px, pz) in enumerate(pontas)],
            c("bota_aro_cima", [-2.5, 6, -2.5], [2.5, 7, 2.5], liso(LILAS, LILAS, ROXO)),
            c("bota_meio", [-2, 3, -2], [2, 6, 2], liso(ROXO, LILAS, ROXO_ESC)),
            c("bota_aro_baixo", [-2.5, 2, -2.5], [2.5, 3, 2.5], liso(LILAS, LILAS, ROXO)),
            c("pe_base", [-1.5, 0, -1.5], [1.5, 2, 1.5], falange),
            dedo("dedo_meio", 0), dedo("dedo_fora", -24 * lado), dedo("dedo_dentro", 24 * lado),
            c("dedo_tras", [-0.5, 0, 1], [0.5, 2, 4], garra),
        ])

    # ---- peitoral em escudo ----
    def escudo():
        pecas = [m.cubo("escudo", [-4, 15, -5], [4, 21, -3], desenho("north", ESCUDO, CORES_EMB, liso(ROXO, LILAS, ROXO_ESC)))]
        for k, linha in enumerate(ESCUDO_V):            # ponta do V em degraus (sem buracos)
            w = len(linha); y = 14 - k
            pecas.append(m.cubo(f"escudo_v{k}", [-w / 2, y, -5], [w / 2, y + 1, -3], desenho("north", [linha], CORES_EMB, liso(ROXO, baixo=ROXO_ESC))))
        for k, linha in enumerate(CHEVRON):             # segundo V menor, um pouco atrás
            w = len(linha); y = 11 - k
            pecas.append(m.cubo(f"chevron_{k}", [-w / 2, y, -4.5], [w / 2, y + 1, -2.5], desenho("north", [linha], CORES_EMB, liso(ROXO, baixo=ROXO_ESC))))
        # fecho em V no alto do escudo, onde chega a garganta branca
        pecas.append(m.cubo("escudo_fecho", [-1, 19, -6], [1, 21, -5], liso(LILAS, LILAS, ROXO)))
        pecas.append(m.cubo("escudo_fecho_ponta", [-0.5, 18, -6], [0.5, 19, -5], liso(ROXO)))
        return pecas

    # ---- ombros: penas roxas grandes e pontudas abrindo para fora (2 camadas) + gola em volta do pescoço ----
    def pena_roxa(cor_topo, cor, cor_ponta):
        def p(face, s, t, W, H):
            if face == "up": return cor_topo
            if face == "down": return ROXO_ESC
            if face in ("north", "south", "side") and t == 0: return cor_topo
            if t == H - 1: return ROXO_ESC
            return cor
        return p
    # (ângulo para baixo, comprimento, deslocamento em z, camada)
    OMBRO = [(0, 7, -1.5, "cima"), (19, 7, -1.5, "cima"), (38, 6, -1.5, "cima"),
             (9, 6, 1.0, "baixo"), (28, 6, 1.0, "baixo"), (48, 5, 1.0, "baixo")]
    def ombro(lado):
        e = "_d" if lado < 0 else "_e"; x0 = 3.5 * lado; y0 = 20
        def c(nome, de, ate, p):
            if lado > 0:
                de, ate = [-ate[0], de[1], de[2]], [-de[0], ate[1], ate[2]]
                return m.cubo(nome + e, de, ate, espelho_de=nome + "_d")
            return m.cubo(nome + e, de, ate, p)
        filhos = []
        for i, (ang, L, dz, camada) in enumerate(OMBRO):
            cores = (LILAS, ROXO, ROXO_ESC) if camada == "cima" else (ROXO, ROXO_ESC, ROXO_ESC)
            xr = -3.5                                   # raiz no ombro direito; a pena cresce para -x
            filhos.append(m.osso(f"ombro_pena_{i}{e}", [x0, y0, dz], [0, 0, -ang * lado], [
                c(f"ombro_pena_{i}", [xr - L + 1, y0 - 1.5, dz - 1.5], [xr, y0 + 1.5, dz + 1.5], pena_roxa(*cores)),   # folha larga
                c(f"ombro_pena_{i}_ponta", [xr - L - 1, y0 - 1, dz - 1], [xr - L + 1, y0 + 1, dz + 1], pena_roxa(cores[1], cores[2], cores[2])),
            ]))
        # gola: penas roxas subindo dos lados do pescoço
        filhos.append(m.osso(f"gola_pena{e}", [2.5 * lado, 20.5, -1.5], [0, 0, -35 * lado], [
            c("gola_pena", [-3.5, 20, -2.5], [-1.5, 24, -0.5], pena_roxa(LILAS, ROXO, ROXO_ESC))]))
        return m.osso("ombro" + e, [x0, y0, 0], [0, -10 * lado, 0], filhos)

    corpo = m.osso("corpo", [0, 16, 0], [3, 0, 0], [
        m.cubo("tronco", [-4, 12, -3], [4, 21, 4], liso(VERM, LARANJA)),
        *escudo(),
        ombro(-1), ombro(1),
        *capa_de_asas(),
    ])

    # ---- cabeça (Elmo da Fênix) ----
    def chifre(lado):
        """Chifre grosso como na ficha: sobe quase reto, abre só um pouco e vai curvando PARA TRÁS
        (de lado parece uma chama varrida; de frente forma a coroa junto com as chamas)."""
        e = "_d" if lado < 0 else "_e"; x = 2.5 * lado
        def c(nome, de, ate, p):
            return m.cubo(nome + e, de, ate, p) if lado < 0 else m.cubo(nome + e, de, ate, espelho_de=nome + "_d")
        # (altura, largura, cor, inclinação para trás, abertura para fora)
        segs = [(3, 2, LARANJA, -18, 14), (3, 2, AMARELO_ESC, -14, 0), (3, 2, AMARELO, -16, 0), (2, 1, AMARELO_CLARO, -14, 0)]
        def seg(k, y):
            h, w, cor, rx, rz = segs[k]
            filhos = [c(f"chifre_{k}", [x - w / 2, y, -2.5 - w / 2], [x + w / 2, y + h, -2.5 + w / 2], liso(cor))]
            if k + 1 < len(segs): filhos.append(seg(k + 1, y + h))
            return m.osso(f"chifre_{k}{e}", [x, y, -2.5], [rx, 0, -rz * lado], filhos)
        return seg(0, 29.5)

    def chama(nome, base, rot, h, cor_base, cor_ponta, larg=2):
        x, y, z = base
        return m.osso(nome, base, rot, [
            m.cubo(nome, [x - larg / 2, y, z - larg / 2], [x + larg / 2, y + h, z + larg / 2], liso(cor_base, cor_ponta)),
            m.cubo(nome + "_ponta", [x - .5, y + h, z - .5], [x + .5, y + h + 2, z + .5], liso(cor_ponta))])

    def pena_juba(nome, base, rx, ry, L, alt=2, cores=(VERM, LARANJA), ponta=AMARELO):
        """Pena da juba de fogo atrás do elmo: lâmina (2 de espessura, 'alt' de altura) apontando para
        trás, degradê de cores[0] para cores[1], ponta afinada."""
        x, y, z = base
        return m.osso(nome, base, [rx, ry, 0], [
            m.cubo(nome, [x - 1, y - alt / 2, z], [x + 1, y + alt / 2, z + L], lamina_pluma(*cores)),
            m.cubo(nome + "_ponta", [x - .5, y - (alt - 1) / 2, z + L], [x + .5, y + (alt - 1) / 2, z + L + 2], liso(ponta)),
            m.cubo(nome + "_bico", [x - .5, y - .5, z + L + 2], [x + .5, y + .5, z + L + 3], liso(clara(ponta, .3)))])

    def gema_tiara():
        """Tiara em voxel: losango alto de ouro (2-4-4-4-4-4-2) com a gema vermelha (2 de largura) na frente."""
        pecas = []
        for k, w in enumerate((2, 4, 4, 4, 4, 4, 2)):
            y = 25 + k
            pecas.append(m.cubo(f"tiara_{k}", [-w / 2, y, -6.6], [w / 2, y + 1, -5.6],
                                liso(OURO_CLARO if k >= 4 else OURO if k >= 2 else OURO_ESC)))
        for k in range(5):
            y = 26 + k
            cor = clara(VERM, .45) if k == 4 else VERM if k >= 2 else VERM_ESC
            pecas.append(m.cubo(f"tiara_gema_{k}", [-1, y, -7], [1, y + 1, -6.4], liso(cor)))
        return pecas

    lado_mascara = lambda lado: (
        m.cubo("elmo_lado_d", [-4, 23, -5.5], [-3, 29, 2.5], desenho("side", MASCARA, CORES_MASC, elmo)) if lado < 0
        else m.cubo("elmo_lado_e", [3, 23, -5.5], [4, 29, 2.5], espelho_de="elmo_lado_d"))

    cab = m.osso("cabeca", [0, 24, -0.5], [3, 0, 0], [
        m.cubo("cranio", [-3, 23, -5], [3, 29, 2], cranio),
        # elmo: calota, viseira na testa e protetores laterais com abertura para o olho
        m.cubo("elmo_topo", [-3.5, 28.5, -5.5], [3.5, 30.5, 2.5], elmo),
        m.cubo("elmo_viseira", [-3.5, 26.5, -6], [3.5, 28.5, -5], elmo),
        lado_mascara(-1), lado_mascara(1),
        # bico em gancho que afina em degraus: base larga -> meio -> ponta curvada para baixo
        m.cubo("bico", [-1.5, 23.5, -7.5], [1.5, 26.5, -5], bico),
        m.cubo("bico_meio", [-1, 23.5, -9.5], [1, 25.5, -7.5], bico),
        m.cubo("bico_gancho", [-0.5, 22.5, -10.5], [0.5, 25, -9.5], liso(AMARELO_ESC)),
        m.cubo("bico_baixo", [-1, 22.5, -8.5], [1, 23.5, -5], liso(LARANJA, baixo=LARANJA_ESC)),
        m.cubo("garganta", [-2.5, 21.5, -5], [2.5, 23, -2], liso(BRANCO, baixo=BRANCO_SOMBRA)),
        *gema_tiara(),
        # (sem chifres, a pedido; a função chifre() continua disponível se quiser voltar)
        # 3 chamas entre os chifres
        chama("chama_crista_1", [0, 30, -2], [-8, 0, 0], 5, VERM, LARANJA),
        chama("chama_crista_2", [-1.3, 30, -1], [-12, 0, 18], 3, VERM, AMARELO),
        chama("chama_crista_3", [1.3, 30, -1], [-12, 0, -18], 3, VERM, AMARELO),
        # juba de penas vermelhas atrás do elmo, abrindo em leque para trás
        # juba de fogo grande (como na vista lateral da ficha): as de cima sobem para trás, as do meio
        # vão para trás, as de baixo descem pelo pescoço; ocupa quase uma cabeça inteira atrás do elmo
        pena_juba("juba_1", [0, 29.5, 1.5], -42, 0, 9, 3, (VERM, LARANJA), AMARELO),
        pena_juba("juba_2", [0, 27.5, 2], -18, 0, 10, 3, (VERM_ESC, VERM), LARANJA),
        pena_juba("juba_3", [0, 25.5, 2], 4, 0, 9, 3, (VERM, LARANJA_ESC), AMARELO),
        pena_juba("juba_4", [0, 23.5, 1.5], 26, 0, 7, 2, (VERM_ESC, VERM), LARANJA_ESC),
        pena_juba("juba_5", [-2.5, 28.5, 1], -30, 22, 8, 2, (VERM, LARANJA), AMARELO_CLARO),
        pena_juba("juba_6", [2.5, 28.5, 1], -30, -22, 8, 2, (VERM, LARANJA), AMARELO_CLARO),
        pena_juba("juba_7", [-3, 25, 0.5], 10, 30, 7, 2, (LARANJA_ESC, LARANJA), AMARELO),
        pena_juba("juba_8", [3, 25, 0.5], 10, -30, 7, 2, (LARANJA_ESC, LARANJA), AMARELO),
    ])
    pesc = m.osso("pescoco", [0, 21, -0.5], [0, 0, 0], [
        m.cubo("pescoco", [-2.5, 20, -3], [2.5, 24.5, 2], desenho("north", ["WWWWW"] * 5, {"W": BRANCO}, liso(VERM, LARANJA))),
        cab,
    ])

    # ---- cauda (como na vista lateral da ficha): só 3 penas de fogo CURTAS apontando para trás quase
    # na horizontal, no alto das costas, + 3 correntes curtas com diamantes. Lâminas largas e achatadas,
    # 3 segmentos com curva leve; uma combinação de cor por pena para não repetir.
    PLUMA_FOGO = [(VERM_ESC, VERM), (VERM, LARANJA_ESC), (LARANJA_ESC, LARANJA), (LARANJA, AMARELO), (AMARELO, AMARELO_CLARO)]
    PLUMA_VERM = [(VERM_ESC, VERM_ESC), (VERM_ESC, VERM), (VERM, VERM), (VERM, LARANJA_ESC), (LARANJA_ESC, LARANJA)]
    PLUMA_LARANJA = [(VERM, LARANJA_ESC), (LARANJA_ESC, LARANJA), (LARANJA, AMARELO), (AMARELO, AMARELO_CLARO)]
    def pluma_cauda(i, x, ry, y0, rx0, curva, alturas, L=4, cores=None):
        cores = cores or PLUMA_FOGO
        def seg(k, z):
            h = alturas[k]; a, b = cores[k]
            filhos = [m.cubo(f"pluma_{i}_{k}", [x - 1, y0 - h / 2, z], [x + 1, y0 + h / 2, z + L], lamina_pluma(a, b))]
            if k + 1 < len(alturas): filhos.append(seg(k + 1, z + L - 0.5))
            return m.osso(f"pluma_{i}_{k}", [x, y0, z], [rx0 if k == 0 else curva, ry if k == 0 else 0, 0], filhos)
        return seg(0, 4.5)

    def corrente(i, x, ry, contas=5, curva=20, y0=17):
        """Cauda de Fênix (como na ficha): elos amarelos grandes girados em LOSANGO, encaixados ponta com
        ponta, e um diamante grande (moldura de ouro 1-3-5-7-5-3-1 + gema vermelha facetada)."""
        def elo(k, z):
            t = 3 if k == 0 else 2                        # o primeiro elo é maior; os outros, menores
            h = t * 0.707                                 # meia diagonal do cubo girado 45°
            cor = AMARELO if k % 2 == 0 else AMARELO_ESC
            filhos = [m.osso(f"conta_{i}_{k}", [x, y0, z + h], [45, 0, 0], [
                m.cubo(f"conta_{i}_{k}", [x - t / 2, y0 - t / 2, z + h - t / 2], [x + t / 2, y0 + t / 2, z + h + t / 2],
                       liso(cor, AMARELO_CLARO, LARANJA_ESC))])]
            if k + 1 < contas:
                filhos.append(elo(k + 1, z + 2 * h))
            else:
                # o osso do pingente desfaz a curva da corrente para o diamante ficar de pé
                ze = z + 2 * h; yc = y0 - 5
                pecas = [m.cubo(f"pingente_argola_{i}", [x - 0.5, yc + 4, ze - 0.5], [x + 0.5, yc + 5, ze + 0.5], liso(OURO))]
                for k2, w in enumerate((1, 3, 5, 7, 5, 3, 1)):          # moldura de ouro, de cima para baixo
                    y = yc + 3 - k2
                    cor = OURO_CLARO if k2 < 3 else OURO if k2 == 3 else OURO_ESC
                    pecas.append(m.cubo(f"pingente_{i}_{k2}", [x - 1, y, ze - w / 2], [x + 1, y + 1, ze + w / 2], liso(cor)))
                for k2, w in enumerate((1, 3, 3, 3, 1)):                # gema vermelha facetada (salta da moldura)
                    y = yc + 2 - k2
                    cor = clara(VERM, .45) if k2 == 0 else VERM if k2 < 3 else VERM_ESC
                    pecas.append(m.cubo(f"pingente_gema_{i}_{k2}", [x - 1.5, y, ze - w / 2], [x + 1.5, y + 1, ze + w / 2], liso(cor)))
                filhos.append(m.osso(f"pingente_{i}", [x, y0, ze], [-(4 + curva * (contas - 1)), 0, 0], pecas))
            return m.osso(f"elo_{i}_{k}", [x, y0, z], [curva if k else 4, ry if k == 0 else 0, 0], filhos)
        return elo(0, 5)

    cauda = m.osso("cauda", [0, 17, 4], [0, 0, 0], [
        m.cubo("cauda_base", [-3, 15, 3], [3, 20, 6], liso(VERM, LARANJA)),
        # 3 penas curtas para trás, cada uma diferente (a de cima sobe um pouco, as outras abrem para os lados)
        pluma_cauda(0, 0, 0, 20, -20, 7, [4, 3, 2], 3, PLUMA_FOGO[1:4]),
        pluma_cauda(1, -1.5, 16, 18.5, -8, 9, [3, 3, 2], 3, PLUMA_VERM[2:5]),
        pluma_cauda(2, 1.5, -16, 17.5, 2, 11, [3, 2, 2], 3, PLUMA_LARANJA[1:4]),
        # 3 correntes curtas que fazem a curva logo atrás do corpo; diamantes perto do chão
        corrente(0, 0, 0), corrente(1, -2.5, 22), corrente(2, 2.5, -22),
    ])
    return [corpo, pesc, cauda, perna(-1), perna(1)]

if __name__ == "__main__":
    m = Modelo(NOME)
    caminho, n, tam = m.salvar(montar(m), largura=128, pasta=PASTA)
    q = previa.carregar(str(caminho))
    vistas = [("Frente", 0, -6), ("Lateral Direita", 90, -6), ("Traseira", 180, -6), ("3/4", -40, -14)]
    ims = [(v, previa.desenhar(q, y, p, escala=11)) for v, y, p in vistas]
    H = max(i.height for _, i in ims) + 24
    folha = Image.new("RGB", (sum(i.width for _, i in ims) + 30, H), (22, 24, 29)); x = 0
    for v, i in ims:
        folha.paste(i, (x, 24 + (H - 24 - i.height))); ImageDraw.Draw(folha).text((x + 8, 6), v, fill=(220, 220, 220))
        x += i.width + 10
    folha.save(PASTA / f"{NOME}_previa.png")
    alt = max(p[1] for qd in q for p in qd[0])
    print(f"{n} cubos, textura {tam}, topo {alt:.1f}px = {alt/16:.2f} blocos")
