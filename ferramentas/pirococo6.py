"""Pirococó v6: versão LIMPA e SUAVE (estilo Cobblemon), fiel à ficha Galetocraft #001.

Diferenças em relação à v5 (que ficou pesada e quadradona, 253 peças):
- ~110 peças: menos penas e maiores; cada pena = 2 peças (lâmina + ponta), sem "bico" extra.
- Volumes arredondados: tronco montado em cruz (quinas chanfradas), calota do elmo arredondada.
- Diamantes (tiara e pingentes) = cubo girado 45°, em vez de escadinha de blocos.
- Pintura com degradê suave: luz quente em cima, sombra arroxeada embaixo, bordas mais escuras.
- Sem chifres (a pedido).
Saída: modelos/pirococo/pirococo_v6.bbmodel + .png + _previa.png"""
import sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from galos_monstro import Modelo
import previa
from PIL import Image, ImageDraw

PASTA = AQUI.parent / "modelos" / "pirococo"
NOME = "pirococo_v6"

# ---------------- paleta da ficha ----------------
ROXO_ESC = (66, 34, 118); ROXO = (118, 70, 190); LILAS = (178, 144, 230)
BRANCO = (246, 242, 238)
AMARELO = (255, 206, 52); AMARELO_CLARO = (255, 234, 130); AMARELO_ESC = (230, 160, 30)
LARANJA = (255, 140, 30); LARANJA_ESC = (228, 100, 22)
VERM = (232, 46, 36); VERM_ESC = (170, 26, 34); VERM_VIVO = (246, 70, 48)
OURO = (246, 184, 46); OURO_CLARO = (255, 228, 118); OURO_ESC = (176, 112, 22)
PRETO = (30, 14, 24)

# ---------------- sombreamento suave ----------------
LUZ = (255, 244, 214)        # luz quente
SOMBRA = (52, 18, 66)        # sombra arroxeada (dá o ar "Cobblemon" em vez de cinza)

def mix(a, b, f):
    return tuple(int(round(a[i] + (b[i] - a[i]) * f)) for i in range(3))

def sombra_de(c):
    """Sombra SATURADA da própria cor, puxando o tom para o vermelho/roxo (laranja -> vermelho-escuro,
    amarelo -> laranja, roxo -> roxo profundo). Evita o marrom/cinza que deixa o fogo 'encardido'."""
    return (int(c[0] * .62), int(c[1] * .40), int(c[2] * .58))

def tom(c, f):
    """f em [-1, 1]: negativo escurece para a sombra saturada da cor, positivo clareia puxando para o quente."""
    f = max(-1.0, min(1.0, f))
    return mix(c, LUZ, f * 0.38) if f >= 0 else mix(c, sombra_de(c), -f * 0.85)

def suave(base, topo=None):
    """Volume arredondado: topo claro, degradê vertical de claro para escuro, bordas laterais mais escuras."""
    def p(face, s, t, W, H):
        if face == "up":
            borda = W > 2 and H > 2 and (s in (0, H - 1) or t in (0, W - 1))
            return tom(topo or base, .30 if borda else .48)
        if face == "down": return tom(base, -.6)
        f = .32 - .85 * (t / max(H - 1, 1))
        if W > 2 and s in (0, W - 1): f -= .16
        return tom(base, f)
    return p

def pena_y(c0, c1):
    """Pena pendurada (comprida para baixo): degradê c0 (raiz) -> c1 (ponta), borda clara/escura."""
    def p(face, s, t, W, H):
        if face == "up": return tom(c0, .25)
        if face == "down": return tom(c1, -.15)
        c = mix(c0, c1, t / max(H - 1, 1))
        if W > 2 and s == 0: return tom(c, .22)
        if W > 2 and s == W - 1: return tom(c, -.25)
        return c
    return p

def pena_z(c0, c1):
    """Pena comprida para trás (eixo Z): degradê ao longo do comprimento, luz em cima, sombra embaixo."""
    def p(face, s, t, W, H):
        if face == "north": return c0
        if face == "south": return c1
        f = s / max((W if face == "side" else H) - 1, 1)
        c = mix(c0, c1, f)
        if face == "up": return tom(c, .3)
        if face == "down": return tom(c, -.45)
        return tom(c, .22 - .55 * (t / max(H - 1, 1)))
    return p

def pena_x(c0, c1):
    """Pena comprida para fora (eixo X; raiz no lado do corpo da peça direita)."""
    def p(face, s, t, W, H):
        if face == "north": f = s / max(W - 1, 1)
        elif face == "south": f = 1 - s / max(W - 1, 1)
        elif face in ("up", "down"): f = t / max(W - 1, 1)
        else: return tom(c0, -.1)
        c = mix(c0, c1, f)
        if face == "up": return tom(c, .32)
        if face == "down": return tom(c, -.5)
        return tom(c, .2 - .5 * (t / max(H - 1, 1)))
    return p

def desenho(face_alvo, linhas, cores, resto):
    def p(face, s, t, W, H):
        if face == face_alvo:
            ch = linhas[t][s]
            return None if ch == "." else cores[ch]
        return resto(face, s, t, W, H)
    return p

# ---------------- artes da ficha ----------------
ESCUDO = ["LLLDDLLL", "PRRDDRRP", "PYRRRRYP", "PYYRRYYP", "PRYYYYRP", "PROYYORP"]
ESCUDO_V = ["PRYYRP", "POOP", "PP"]
CORES_EMB = {"L": LILAS, "P": ROXO, "D": ROXO_ESC, "Y": AMARELO, "O": LARANJA, "R": VERM}

MASCARA = ["LLLLLLLL", "PPPPPPPP", "DDDDPPPP", "D...PPPP", "....PPPP", "....PPPD"]
CORES_MASC = {"L": LILAS, "P": ROXO, "D": ROXO_ESC}

def cranio(face, s, t, W, H):
    """Cabeça SEM capacete: a plumagem roxa é pintada direto (topo roxo, sobrancelha brava roxo-escura,
    marca roxa atrás do olho descendo até a mandíbula), rosto branco e penas vermelhas na nuca.
    Lado: W=7 (s=0 frente), H=5 (t=0 topo). Frente: W=6, H=5."""
    if face == "down": return tom(BRANCO, -.25)
    if face == "up": return LILAS if s <= 1 else tom(ROXO, .2)
    if face == "north":
        if t == 0: return LILAS
        if t == 1: return ROXO_ESC if s in (0, 1, W - 2, W - 1) else ROXO      # sobrancelha em V
        if s in (0, W - 1): return VERM if t == 2 else (VERM_ESC if t == 3 else BRANCO)   # olhos nos cantos
        return tom(BRANCO, -.1 * (t - 2))
    if face == "side":
        olho = {(0, 2): BRANCO, (1, 2): VERM, (2, 2): VERM, (0, 3): BRANCO, (1, 3): PRETO, (2, 3): VERM_ESC}
        if (s, t) in olho: return olho[(s, t)]
        if t == 0: return LILAS if s <= 1 else ROXO
        if t == 1: return ROXO_ESC if s <= 2 else ROXO                      # sobrancelha brava
        if s in (3, 4) and not (s == 3 and t == 4): return tom(ROXO, -.15 * (t - 2))   # marca roxa atrás do olho
        if s >= 5: return tom(VERM, .1 - .25 * (t - 2))                     # penas vermelhas da nuca
        return tom(BRANCO, -.08 * (t - 2))
    return VERM

def bico(face, s, t, W, H):
    if face == "up": return AMARELO_CLARO
    if face == "down": return LARANJA_ESC
    if face == "side" and (s, t) == (W - 2, 0): return (120, 66, 18)
    if face == "north": return AMARELO_ESC
    return mix(AMARELO, LARANJA, t / max(H - 1, 1))

# ---------------- montagem ----------------
def montar(m):
    def espelho(nome, lado, de, ate, pintor):
        """Peça do lado direito (pintada) ou espelho no esquerdo."""
        e = "_d" if lado < 0 else "_e"
        if lado > 0:
            de, ate = [-ate[0], de[1], de[2]], [-de[0], ate[1], ate[2]]
            return m.cubo(nome + e, de, ate, espelho_de=nome + "_d")
        return m.cubo(nome + e, de, ate, pintor)

    def arredondado(nome, x0, y0, z0, x1, y1, z1, pintor):
        """Volume com as 12 quinas chanfradas em 1 px: 3 blocos em cruz."""
        return [m.cubo(nome + "_a", [x0 + 1, y0 + 1, z0], [x1 - 1, y1 - 1, z1], pintor),
                m.cubo(nome + "_b", [x0, y0 + 1, z0 + 1], [x1, y1 - 1, z1 - 1], pintor),
                m.cubo(nome + "_c", [x0 + 1, y0, z0 + 1], [x1 - 1, y1, z1 - 1], pintor)]

    def diamante(nome, centro, lado_frame, lado_gema, espessura, eixo="z"):
        """Diamante = cubo de ouro girado 45° + gema vermelha menor girada, saltando dos dois lados."""
        x, y, z = centro
        a, b = lado_frame / 2, lado_gema / 2
        if eixo == "z":     # visto de frente
            pecas = [m.cubo(nome, [x - a, y - a, z - espessura / 2], [x + a, y + a, z + espessura / 2], suave(OURO)),
                     m.cubo(nome + "_gema", [x - b, y - b, z - espessura / 2 - .5], [x + b, y + b, z + espessura / 2 + .5], suave(VERM))]
            return m.osso(nome, [x, y, z], [0, 0, 45], pecas)
        pecas = [m.cubo(nome, [x - espessura / 2, y - a, z - a], [x + espessura / 2, y + a, z + a], suave(OURO)),
                 m.cubo(nome + "_gema", [x - espessura / 2 - .5, y - b, z - b], [x + espessura / 2 + .5, y + b, z + b], suave(VERM))]
        return m.osso(nome, [x, y, z], [45, 0, 0], pecas)

    # ---- patas: calça arredondada, bota em carretel, 3 dedos em leque ----
    def dedo_p(face, s, t, W, H):
        if face == "up": return tom(AMARELO, .4)
        if face == "north": return AMARELO_ESC
        if face == "down": return LARANJA_ESC
        f = s / max(W - 1, 1) if face == "side" else 0
        return mix(AMARELO, AMARELO_ESC, max(0, 1 - f) * .6) if face == "side" else tom(AMARELO, -.2 * t)
    def perna(lado):
        x = 2.6 * lado; e = "_d" if lado < 0 else "_e"
        def c(nome, de, ate, p):
            de = [de[0] + x, de[1], de[2]]; ate = [ate[0] + x, ate[1], ate[2]]
            return m.cubo(nome + e, de, ate, espelho_de=nome + "_d") if lado > 0 else m.cubo(nome + e, de, ate, p)
        def dedo(nome, rot, L):
            return m.osso(nome + e, [x, 1, 0], [0, rot, 0], [c(nome, [-1, 0, -L], [1, 2, 0], dedo_p)])
        calca = suave(LARANJA)
        return m.osso("perna" + e, [x, 12, 0], [0, 0, 0], [
            c("coxa_a", [-2.5, 8, -2.5], [2.5, 11, 2.5], calca),
            c("coxa_b", [-1.5, 7, -1.5], [1.5, 12, 1.5], calca),
            c("bota_cima", [-2.5, 6, -2.5], [2.5, 7, 2.5], suave(LILAS)),
            c("bota_meio", [-2, 3, -2], [2, 6, 2], suave(ROXO)),
            c("bota_baixo", [-2.5, 2, -2.5], [2.5, 3, 2.5], suave(LILAS)),
            dedo("dedo_meio", 0, 6), dedo("dedo_fora", -26 * lado, 5), dedo("dedo_dentro", 26 * lado, 5),
            c("dedo_tras", [-0.5, 0, 0], [0.5, 2, 3], dedo_p),
        ])

    # ---- tronco arredondado + peitoral em escudo ----
    corpo_filhos = arredondado("tronco", -4, 11, -3.5, 4, 20, 4.5, suave(VERM, LARANJA))
    corpo_filhos.append(m.cubo("escudo", [-4, 14, -5], [4, 20, -3], desenho("north", ESCUDO, CORES_EMB, suave(ROXO, LILAS))))
    for k, linha in enumerate(ESCUDO_V):
        w = len(linha); y = 13 - k
        corpo_filhos.append(m.cubo(f"escudo_v{k}", [-w / 2, y, -5], [w / 2, y + 1, -3], desenho("north", [linha], CORES_EMB, suave(ROXO))))
    corpo_filhos.append(m.cubo("escudo_fecho", [-1, 18.5, -5.6], [1, 20.5, -4.6], suave(LILAS)))

    # ---- ombros: manto roxo, 3 penas largas por lado ----
    OMBRO = [(2, 7, LILAS, ROXO), (24, 6, ROXO, ROXO_ESC), (46, 5, ROXO, ROXO_ESC)]
    def ombro(lado):
        e = "_d" if lado < 0 else "_e"; x0, y0 = 3.5 * lado, 19.5
        filhos = []
        for i, (ang, L, c0, c1) in enumerate(OMBRO):
            xr = -3.5
            # lâmina mais fina (3 de fundo) e ponta afiada (1 de altura): pena, não caixote
            filhos.append(m.osso(f"ombro_pena_{i}{e}", [x0, y0, 0], [0, 0, -ang * lado], [
                espelho(f"ombro_pena_{i}", lado, [xr - L + 2, y0 - 1.5, -1.5], [xr, y0 + 1.5, 1.5], pena_x(c0, c1)),
                espelho(f"ombro_pena_{i}_ponta", lado, [xr - L, y0 - 1, -1], [xr - L + 2, y0, 1], pena_x(c1, ROXO_ESC)),
            ]))
        return m.osso("ombro" + e, [x0, y0, 0], [0, -10 * lado, 0], filhos)
    corpo_filhos += [ombro(-1), ombro(1)]

    # ---- capa de asas: asa dobrada, 5 penas largas por lado + 1 central nas costas ----
    # (x, z, y da raiz, varre p/ trás, abre p/ fora, comprimento, largura, face larga p/ frente?, cor raiz, cor ponta)
    CAPA = [
        (-5.2, 0.0, 19.0, 46, 18, 7, 5, False, LILAS, ROXO_ESC),         # cobertura roxa
        (-5.0, -1.2, 18.0, 40, 24, 10, 4, False, VERM_ESC, LARANJA_ESC),  # vermelha
        (-4.8, 1.6, 17.5, 54, 28, 12, 4, False, VERM, AMARELO),           # laranja
        (-4.6, -1.8, 17.0, 38, 32, 13, 4, False, LARANJA_ESC, AMARELO_CLARO),  # amarela, a mais longa
        (-4.2, -3.4, 17.0, -4, 18, 9, 3, True, VERM, LARANJA),            # frente, cobre a coxa
    ]
    def pena_capa(nome, dados, lado):
        x, z, y, varre, abre, L, larg, frente, c0, c1 = dados
        wx, wz = (larg, 2) if frente else (2, larg)
        meio = mix(c0, c1, .7)
        partes = [("", [x - wx / 2, y - (L - 3), z - wz / 2], [x + wx / 2, y, z + wz / 2], pena_y(c0, meio)),
                  ("_ponta", [x - (wx - 2) / 2 if wx > 2 else x - 1, y - L, z - (wz - 2) / 2 if wz > 2 else z - 1],
                   [x + (wx - 2) / 2 if wx > 2 else x + 1, y - (L - 3), z + (wz - 2) / 2 if wz > 2 else z + 1], pena_y(meio, c1))]
        if lado == 0:
            return m.osso(nome, [x, y, z], [-varre, 0, 0], [m.cubo(nome + s, de, ate, p) for s, de, ate, p in partes])
        e = "_d" if lado < 0 else "_e"
        return m.osso(nome + e, [x if lado < 0 else -x, y, z], [-varre, 0, abre * lado],
                      [espelho(nome + s, lado, de, ate, p) for s, de, ate, p in partes])
    for lado in (-1, 1):
        for i, dados in enumerate(CAPA):
            corpo_filhos.append(pena_capa(f"capa_{i}", dados, lado))
    corpo_filhos.append(pena_capa("capa_costas", (0.0, 4.8, 19.5, 26, 0, 11, 5, True, VERM, AMARELO), 0))

    corpo = m.osso("corpo", [0, 15, 0], [2, 0, 0], corpo_filhos)

    # ---- cabeça: elmo arredondado, máscara com abertura do olho, bico, tiara em diamante, chamas, juba ----
    def chama(nome, base, rot, h, w, c0, c1):
        x, y, z = base
        return m.osso(nome, base, rot, [m.cubo(nome, [x - w / 2, y, z - w / 2], [x + w / 2, y + h, z + w / 2], pena_y(c1, c0))])
    def juba(nome, base, rx, ry, L, alt, c0, c1):
        x, y, z = base
        return m.osso(nome, base, [rx, ry, 0], [
            m.cubo(nome, [x - 1, y - alt / 2, z], [x + 1, y + alt / 2, z + L], pena_z(c0, mix(c0, c1, .7))),
            m.cubo(nome + "_ponta", [x - .5, y - (alt - 1) / 2, z + L], [x + .5, y + (alt - 1) / 2, z + L + 3], pena_z(mix(c0, c1, .7), c1))])
    cab = m.osso("cabeca", [0, 22, -0.5], [3, 0, 0], [
        # cabeça sem capacete: crânio com a plumagem pintada + camada de cima que arredonda o topo
        m.cubo("cranio", [-3.5, 22, -5.5], [3.5, 28, 2.5], cranio),                 # 7x6x8: cabeça grande
        m.cubo("cranio_topo", [-2.5, 28, -4.5], [2.5, 29, 1.5], suave(ROXO, LILAS)),
        # tiara: aro fino de ouro contornando a testa e os lados + diamante na frente
        m.cubo("tiara_aro", [-3.5, 26.5, -6.1], [3.5, 27.5, -5.1], suave(OURO)),
        espelho("tiara_aro_lado", -1, [-4.1, 26.5, -5.5], [-3.1, 27.5, 0.5], suave(OURO)),
        espelho("tiara_aro_lado", 1, [-4.1, 26.5, -5.5], [-3.1, 27.5, 0.5], None),
        m.cubo("bico", [-1.5, 22.5, -8], [1.5, 25.5, -5.5], bico),
        m.cubo("bico_meio", [-1, 22.5, -10], [1, 24.5, -8], bico),
        m.cubo("bico_gancho", [-0.5, 21.5, -11], [0.5, 24, -10], suave(AMARELO_ESC)),
        m.cubo("garganta", [-2.5, 20.5, -5.5], [2.5, 22, -2.5], suave(BRANCO)),
        diamante("tiara", [0, 28.3, -6.7], 4, 2, 1, "z"),
        chama("crista_meio", [0, 28.5, -2], [-10, 0, 0], 5, 2, VERM, AMARELO),
        chama("crista_d", [-1.8, 28, -1.5], [-12, 0, 20], 3, 1, VERM, LARANJA),
        chama("crista_e", [1.8, 28, -1.5], [-12, 0, -20], 3, 1, VERM, LARANJA),
        # juba de fogo vermelho-vivo com pontas laranja/amarelas: 5 penas grandes para trás
        juba("juba_cima", [0, 28.5, 2], -38, 0, 7, 3, VERM_VIVO, LARANJA),
        juba("juba_meio", [0, 26.5, 2.5], -10, 0, 8, 3, VERM, AMARELO),
        juba("juba_baixo", [0, 23.5, 2], 22, 0, 6, 2, VERM_ESC, LARANJA),
        juba("juba_d", [-3, 27, 1.5], -20, -26, 6, 2, VERM_VIVO, AMARELO),
        juba("juba_e", [3, 27, 1.5], -20, 26, 6, 2, VERM_VIVO, AMARELO),
        # "babado" vermelho dos lados do rosto (de frente aparece dos dois lados, como na ficha)
        juba("bochecha_d", [-4, 23.5, -0.5], 48, -40, 4, 3, VERM_VIVO, LARANJA),
        juba("bochecha_e", [4, 23.5, -0.5], 48, 40, 4, 3, VERM_VIVO, LARANJA),
    ])
    pesc = m.osso("pescoco", [0, 20, -0.5], [0, 0, 0], [
        m.cubo("pescoco", [-2.5, 19, -3], [2.5, 23.5, 2], desenho("north", ["WWWWW"] * 5, {"W": BRANCO}, suave(VERM, LARANJA))),
        cab,
    ])

    # ---- cauda: 3 penas curtas para trás + 3 correntes com diamante ----
    def pena_cauda(nome, x, y, rx, ry, L, alt, c0, c1):
        meio = mix(c0, c1, .65)
        return m.osso(nome, [x, y, 4.5], [rx, ry, 0], [
            m.cubo(nome, [x - 1, y - alt / 2, 4.5], [x + 1, y + alt / 2, 4.5 + L], pena_z(c0, meio)),
            m.cubo(nome + "_ponta", [x - .5, y - (alt - 1) / 2, 4.5 + L], [x + .5, y + (alt - 1) / 2, 4.5 + L + 3], pena_z(meio, c1))])
    def corrente(i, x, ry, contas=4, curva=24, y0=16.5):
        def elo(k, z):
            t = 2; h = t * .707
            filhos = [m.osso(f"conta_{i}_{k}", [x, y0, z + h], [45, 0, 0], [
                m.cubo(f"conta_{i}_{k}", [x - 1, y0 - 1, z + h - 1], [x + 1, y0 + 1, z + h + 1], suave(AMARELO))])]
            if k + 1 < contas:
                filhos.append(elo(k + 1, z + 2 * h))
            else:
                ze = z + 2 * h
                filhos.append(m.osso(f"pingente_{i}", [x, y0, ze], [-(6 + curva * (contas - 1)), 0, 0], [
                    diamante(f"pingente_{i}_d", [x, y0 - 4, ze], 5, 3, 2, "x")]))
            return m.osso(f"elo_{i}_{k}", [x, y0, z], [curva if k else 6, ry if k == 0 else 0, 0], filhos)
        return elo(0, 5)
    cauda = m.osso("cauda", [0, 17, 4], [0, 0, 0], [
        m.cubo("cauda_base", [-2.5, 15, 3.5], [2.5, 19, 6], suave(VERM, LARANJA)),
        pena_cauda("cauda_1", 0, 19, -18, 0, 6, 3, VERM, AMARELO),
        pena_cauda("cauda_2", -1.5, 17.5, -6, 16, 5, 3, VERM_ESC, LARANJA),
        pena_cauda("cauda_3", 1.5, 16.5, 6, -16, 5, 2, LARANJA_ESC, AMARELO_CLARO),
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
    print(f"{n} pecas, textura {tam}, topo {alt:.1f}px = {alt/16:.2f} blocos")
