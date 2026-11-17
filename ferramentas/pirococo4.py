"""Pirococó v4: segue a ficha oficial em voxel (Galetocraft #001).
Elmo roxo da fênix com tiara e diamante vermelho, chifres amarelos curvos, rosto branco, bico amarelo,
olhos vermelhos; peitoral roxo em escudo com emblema da fênix; ombros de penas roxas; capa de asas em
degradê de fogo; plumas da cauda + 3 correntes com pingentes de diamante; patas reforçadas com botas roxas.
Estilo Cobblemon: 16 px = 1 bloco, textura limpa. Cabeça a ~1,8 bloco.
Saída: modelos/pirococo/pirococo_v4.bbmodel + .png + _previa.png"""
import sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from galos_monstro import Modelo
import previa
from PIL import Image, ImageDraw

PASTA = AQUI.parent / "modelos" / "pirococo"
NOME = "pirococo_v4"

# ---------------- paleta da ficha ----------------
ROXO_ESC = (70, 36, 122); ROXO = (122, 72, 192); LILAS = (180, 146, 230)
BRANCO = (242, 238, 236); BRANCO_SOMBRA = (206, 198, 206)
AMARELO = (255, 206, 48); AMARELO_ESC = (222, 160, 26)
LARANJA = (255, 138, 30); VERM = (222, 40, 32); VERM_ESC = (150, 20, 30)
OURO = (242, 178, 40); OURO_CLARO = (255, 226, 110); OURO_ESC = (168, 108, 20)
PRETO = (26, 14, 22)

def clara(c, k=.2): return tuple(int(v + (255 - v) * k) for v in c)
def esc(c, k=.75): return tuple(int(v * k) for v in c)
def grad(f, faixas):
    for lim, c in faixas:
        if f <= lim + 1e-6: return c
    return faixas[-1][1]
FOGO = [(.4, VERM), (.72, LARANJA), (1, AMARELO)]

# ---------------- pintores ----------------
def liso(base, topo=None, base_baixo=None):
    def p(face, s, t, W, H):
        if face == "up": return clara(topo or base, .15)
        if face == "down": return esc(base_baixo or base)
        if t == 0 and H > 2: return clara(base, .15)
        if t == H - 1 and H > 2: return esc(base, .85)
        return base
    return p

def desenho(face_alvo, linhas, cores, resto):
    """Pinta uma face com arte em pixels (lista de strings); as outras faces usam 'resto'."""
    def p(face, s, t, W, H):
        if face == face_alvo:
            ch = linhas[t][s]
            return None if ch == "." else cores[ch]
        return resto(face, s, t, W, H)
    return p

def franja(cores_altura, base_ponta=True):
    """Penas com a última fileira em ponta (pixels alternados transparentes)."""
    def p(face, s, t, W, H):
        if face == "down": return None
        if face == "up": return clara(cores_altura[0], .1)
        if t == H - 1 and s % 2 == 1: return None
        return cores_altura[min(int(t / max(H, 1) * len(cores_altura)), len(cores_altura) - 1)]
    return p

def pena_x(faixas):
    def p(face, s, t, W, H):
        if face == "north": f = s / max(W - 1, 1)
        elif face == "south": f = 1 - s / max(W - 1, 1)
        elif face in ("up", "down"): f = t / max(W - 1, 1)
        else: return esc(grad(.3, faixas), .9)
        c = grad(f, faixas)
        return clara(c, .12) if face == "up" else esc(c) if face == "down" else c
    return p

def pena_z(faixas, f0=0, f1=1):
    def p(face, s, t, W, H):
        if face == "side": f = s / max(W - 1, 1)
        elif face in ("up", "down"): f = s / max(H - 1, 1)
        elif face == "north": f = 0
        else: f = 1
        c = grad(f0 + (f1 - f0) * f, faixas)
        return clara(c, .12) if face == "up" else esc(c) if face == "down" else c
    return p

def metal(face, s, t, W, H):
    if face == "up" or t == 0: return OURO_CLARO
    if face == "down" or t == H - 1: return OURO_ESC
    return OURO

def bota(face, s, t, W, H):             # bota roxa com faixa lilás no alto
    if face == "up": return LILAS
    if face == "down": return ROXO_ESC
    return LILAS if t == 0 else (ROXO_ESC if t == H - 1 else ROXO)

def pe(face, s, t, W, H):               # dedos gordos amarelos, unha mais escura na frente
    if face == "up": return clara(AMARELO, .15)
    if face == "down": return AMARELO_ESC
    if face == "north": return AMARELO_ESC
    return AMARELO if s > 0 else AMARELO_ESC

EMBLEMA = [                                   # peitoral 8x8 visto de frente: fênix de asas abertas
    "LLLLLLLL",
    "PYPPPPYP",
    "PYYPPYYP",
    "POYYYYOP",
    "PPOYYOPP",
    "PPPYYPPP",
    "DPPOOPPD",
    "DDPPPPDD",
]
CORES_EMB = {"L": LILAS, "P": ROXO, "D": ROXO_ESC, "Y": AMARELO, "O": LARANJA}

def cabeca(face, s, t, W, H):
    """Elmo roxo em cima, rosto branco embaixo, olhos vermelhos bravos. Lado W=7 (s=0 frente), H=6."""
    if face == "up": return ROXO if s >= 2 else LILAS
    if face == "down": return BRANCO_SOMBRA
    if face == "north":                       # W=6
        if t <= 1: return LILAS if t == 0 else ROXO
        if t == 2: return ROXO_ESC
        if t == 3 and s in (0, W - 1): return VERM
        if t == 4 and s in (0, W - 1): return BRANCO
        return BRANCO
    if face == "side":
        olho = {(1, 3): BRANCO, (2, 3): VERM, (1, 4): VERM, (2, 4): VERM_ESC}
        if (s, t) in olho: return olho[(s, t)]
        if t == 2 and s <= 3: return ROXO_ESC              # borda da viseira (sobrancelha brava)
        if t == 3 and s == 3: return ROXO_ESC
        if t <= 2: return LILAS if t == 0 else ROXO
        if s <= 3: return BRANCO
        return VERM if (s + t) % 2 else LARANJA
    return VERM if t % 2 else LARANJA              # nuca: penas

def gema(face, s, t, W, H):              # diamante vermelho (cantos transparentes = forma de losango)
    if face in ("north", "south", "side"):
        cx, cy = (W - 1) / 2, (H - 1) / 2
        if abs(s - cx) / (W / 2) + abs(t - cy) / (H / 2) > 1.05: return None
        return clara(VERM, .45) if t < cy and s <= cx else (VERM if t <= cy + .5 else VERM_ESC)
    return VERM

def moldura(face, s, t, W, H):           # moldura de ouro da tiara (losango oco)
    if face in ("north", "south"):
        cx, cy = (W - 1) / 2, (H - 1) / 2
        d = abs(s - cx) / (W / 2) + abs(t - cy) / (H / 2)
        if d > 1.1: return None
        return OURO_CLARO if t < cy else OURO
    return metal(face, s, t, W, H)

# ---------------- montagem ----------------
def montar(m):
    def perna(lado):
        x = 2.5 * lado; e = "_d" if lado < 0 else "_e"
        def c(nome, de, ate, pintor):
            de = [de[0] + x, de[1], de[2]]; ate = [ate[0] + x, ate[1], ate[2]]
            if lado > 0: return m.cubo(nome + e, de, ate, espelho_de=nome + "_d")
            return m.cubo(nome + e, de, ate, pintor)
        return m.osso("perna" + e, [x, 14, 0], [0, 0, 0], [
            c("coxa", [-2, 10, -2], [2, 15, 2], franja([VERM, LARANJA, AMARELO])),
            c("canela", [-1, 2, -1], [1, 11, 1], liso(AMARELO)),
            c("bota", [-1.5, 2, -1.5], [1.5, 6, 1.5], bota),
            c("dedo_meio", [-0.5, 0, -4.5], [0.5, 2, 0], pe),
            c("dedo_fora", [-2, 0, -3.5], [-1, 2, 0], pe),
            c("dedo_dentro", [1, 0, -3.5], [2, 2, 0], pe),
            c("dedo_tras", [-0.5, 0, 0], [0.5, 1.5, 2.5], pe),
        ])

    def ombro(lado):
        e = "_d" if lado < 0 else "_e"
        def c(nome, de, ate, pintor):
            if lado > 0:
                de, ate = [-ate[0], de[1], de[2]], [-de[0], ate[1], ate[2]]
                return m.cubo(nome + e, de, ate, espelho_de=nome + "_d")
            return m.cubo(nome + e, de, ate, pintor)
        return m.osso("ombro" + e, [4 * lado, 20, 0], [0, 0, -18 * lado], [
            c("ombro_alto", [-6.5, 19.5, -3], [-3.5, 21.5, 3], franja([LILAS, ROXO])),
            c("ombro_baixo", [-7, 17.5, -2.5], [-4, 19.5, 2.5], franja([ROXO, ROXO_ESC])),
        ])

    corpo = m.osso("corpo", [0, 16, 0], [5, 0, 0], [
        m.cubo("tronco", [-4, 12, -3], [4, 21, 4], liso(VERM, LARANJA)),
        # peitoral roxo em escudo (com ponta embaixo) e emblema da fênix
        m.cubo("peitoral", [-4, 13, -5], [4, 21, -3], desenho("north", EMBLEMA, CORES_EMB, liso(ROXO, LILAS))),
        m.cubo("peitoral_ponta", [-2.5, 11, -5], [2.5, 13, -3], liso(ROXO_ESC, ROXO)),
        m.cubo("peitoral_bico", [-1, 9.5, -5], [1, 11, -3.5], liso(ROXO_ESC)),
        *[ombro(-1), ombro(1)],
    ])

    # capa de asas: penas largas caindo dos ombros, em degradê de fogo
    CAPA_FORA = [(-102, 13), (-90, 14), (-78, 14), (-66, 13), (-54, 11)]
    CAPA_DENTRO = [(-96, 10), (-84, 11), (-72, 11), (-60, 9)]
    def capa(lado):
        e = "_d" if lado < 0 else "_e"; x0 = 4 * lado
        def c(nome, de, ate, pintor):
            return m.cubo(nome + e, de, ate, espelho_de=nome + "_d") if lado > 0 else m.cubo(nome + e, de, ate, pintor)
        def ex(a, b): return [x0 - b, x0 - a] if lado < 0 else [x0 + a, x0 + b]
        filhos = []
        for i, (ang, L) in enumerate(CAPA_FORA):
            z = 2.2 + 0.3 * i
            filhos.append(m.osso(f"capa_{i}{e}", [x0, 19.5, z], [0, 0, ang * lado], [
                c(f"capa_{i}", [ex(0, L)[0], 18, z - 0.5], [ex(0, L)[1], 21, z + 0.5], pena_x(FOGO))]))
        for i, (ang, L) in enumerate(CAPA_DENTRO):
            filhos.append(m.osso(f"capa_dentro_{i}{e}", [x0, 19.5, 1], [0, 0, ang * lado], [
                c(f"capa_dentro_{i}", [ex(0, L)[0], 18.5, 0.5], [ex(0, L)[1], 20.5, 1.5], pena_x([(.55, VERM_ESC), (1, VERM)]))]))
        return m.osso("capa" + e, [x0, 19.5, 2], [-10, -15 * lado, 0], filhos)

    # ---- cabeça ----
    def chifre(lado):
        e = "_d" if lado < 0 else "_e"; x = 2 * lado
        kw = lambda nome, p: dict(pintor=p) if lado < 0 else dict(espelho_de=nome + "_d")
        # base inclina para fora, meio e ponta curvam para dentro (forma de coroa)
        return m.osso("chifre" + e, [x, 29, -2], [0, 0, -22 * lado], [
            m.cubo("chifre_base" + e, [x - 1, 29, -3], [x + 1, 32, -1], **kw("chifre_base", liso(LARANJA, AMARELO))),
            m.osso("chifre_meio" + e, [x, 32, -2], [0, 0, 30 * lado], [
                m.cubo("chifre_meio" + e, [x - 1, 32, -3], [x + 1, 35, -1], **kw("chifre_meio", liso(AMARELO))),
                m.osso("chifre_ponta" + e, [x, 35, -2], [0, 0, 35 * lado], [
                    m.cubo("chifre_ponta" + e, [x - 0.5, 35, -2.5], [x + 0.5, 37, -1.5], **kw("chifre_ponta", liso(OURO_CLARO)))]),
            ]),
        ])
    def chama(nome, origem, rot, L, f0=0):
        x, y, z = origem
        return m.osso(nome, origem, rot, [m.cubo(nome, [x - 1, y - 1, z], [x + 1, y + 1, z + L], pena_z(FOGO, f0))])
    cab = m.osso("cabeca", [0, 24, -0.5], [4, 0, 0], [
        m.cubo("cabeca", [-3, 23, -5], [3, 29, 2], cabeca),
        m.cubo("bico", [-1.5, 23.5, -9], [1.5, 26, -5], liso(AMARELO, base_baixo=AMARELO_ESC)),
        m.cubo("bico_gancho", [-1, 22.5, -9.5], [1, 24, -8.5], liso(AMARELO_ESC)),
        m.cubo("bico_baixo", [-1, 22.5, -8], [1, 23.5, -5], liso(AMARELO_ESC)),
        # tiara: moldura de ouro em losango com o diamante vermelho no meio
        m.cubo("tiara", [-2.5, 26.5, -6], [2.5, 32.5, -5], moldura),
        m.cubo("tiara_gema", [-1.5, 27.5, -6.6], [1.5, 31.5, -5.6], gema),
        chifre(-1), chifre(1),
        # chamas da nuca e das bochechas, varrendo para trás
        chama("chama_nuca_1", [0, 28, 1], [-35, 0, 0], 7), chama("chama_nuca_2", [-1.5, 27, 1], [-15, 20, 0], 6),
        chama("chama_nuca_3", [1.5, 27, 1], [-15, -20, 0], 6),
        chama("chama_bochecha_d", [-3, 24.5, -2], [-15, 25, 0], 5), chama("chama_bochecha_e", [3, 24.5, -2], [-15, -25, 0], 5),
    ])
    pesc = m.osso("pescoco", [0, 21, -0.5], [0, 0, 0], [
        m.cubo("pescoco", [-2.5, 20, -3], [2.5, 24.5, 2], desenho("north", ["WWWWW"] * 5, {"W": BRANCO}, liso(VERM, LARANJA))),
        m.cubo("gola", [-3.5, 20, -2.5], [3.5, 23, 2.5], franja([VERM, LARANJA, LARANJA])),
        cab,
    ])

    # ---- cauda: plumas grandes em arco + 3 correntes com pingentes de diamante ----
    def pluma(i, x, ry, rx0, escala=1.0):
        L1, L2, L3 = round(5 * escala), round(5 * escala), round(4 * escala)
        return m.osso(f"pluma_{i}", [x, 18, 4], [rx0, ry, 0], [
            # plumas largas (lâmina vertical 4 px de altura) que afinam até a ponta
            m.cubo(f"pluma_{i}_a", [x - 1, 16, 4], [x + 1, 20, 4 + L1], pena_z(FOGO, 0, .35)),
            m.osso(f"pluma_{i}_b", [x, 18, 4 + L1], [22, 0, 0], [
                m.cubo(f"pluma_{i}_b", [x - 1, 16.5, 4 + L1], [x + 1, 19.5, 4 + L1 + L2], pena_z(FOGO, .35, .7)),
                m.osso(f"pluma_{i}_c", [x, 18, 4 + L1 + L2], [28, 0, 0], [
                    m.cubo(f"pluma_{i}_c", [x - 0.5, 17, 4 + L1 + L2], [x + 0.5, 19, 4 + L1 + L2 + L3], pena_z(FOGO, .7, 1))]),
            ]),
        ])
    def corrente(i, x, ry, contas=6):
        """Contas amarelas encadeadas que caem em curva e terminam num pingente de diamante."""
        def elo(k, z):
            filhos = [m.cubo(f"corrente_{i}_{k}", [x - 1, 12, z], [x + 1, 14, z + 2],
                             liso(AMARELO if k % 2 == 0 else AMARELO_ESC))]
            if k + 1 < contas:
                filhos.append(elo(k + 1, z + 2.5))
            else:
                zc = z + 4.5
                filhos.append(m.osso(f"pingente_{i}", [x, 13, zc], [45, 0, 0], [
                    m.cubo(f"pingente_{i}", [x - 0.5, 11, zc - 2], [x + 0.5, 15, zc + 2], liso(OURO, OURO_CLARO)),
                    m.cubo(f"pingente_gema_{i}", [x - 0.7, 12, zc - 1], [x + 0.7, 14, zc + 1], liso(VERM, clara(VERM, .4))),
                ]))
            return m.osso(f"elo_{i}_{k}", [x, 13, z], [16 if k else 10, ry if k == 0 else 0, 0], filhos)
        return elo(0, 4)
    cauda = m.osso("cauda", [0, 16, 4], [0, 0, 0], [
        m.cubo("cauda_base", [-2.5, 14, 3], [2.5, 19, 6], liso(VERM, LARANJA)),
        pluma(0, 0, 0, -75, 1.2), pluma(1, -1.5, 16, -62, 1.1), pluma(2, 1.5, -16, -62, 1.1),
        pluma(3, -2.5, 34, -48), pluma(4, 2.5, -34, -48),
        corrente(0, 0, 0), corrente(1, -2, 22), corrente(2, 2, -22),
    ])
    return [corpo, pesc, cauda, perna(-1), perna(1), capa(-1), capa(1)]

if __name__ == "__main__":
    m = Modelo(NOME)
    caminho, n, tam = m.salvar(montar(m), largura=128, pasta=PASTA)
    q = previa.carregar(str(caminho))
    vistas = [("frente", 0, -6), ("lateral", 90, -4), ("3/4 frente", -35, -14), ("traseira", 180, -6)]
    ims = [(v, previa.desenhar(q, y, p, escala=11)) for v, y, p in vistas]
    H = max(i.height for _, i in ims) + 24
    folha = Image.new("RGB", (sum(i.width for _, i in ims) + 30, H), (22, 24, 29)); x = 0
    for v, i in ims:
        folha.paste(i, (x, 24 + (H - 24 - i.height))); ImageDraw.Draw(folha).text((x + 8, 6), v, fill=(220, 220, 220))
        x += i.width + 10
    folha.save(PASTA / f"{NOME}_previa.png")
    alt = max(p[1] for qd in q for p in qd[0])
    print(f"{n} cubos, textura {tam}, topo {alt:.1f}px = {alt/16:.2f} blocos")
