"""Pirococó v3, no estilo Cobblemon: densidade de pixel do Minecraft (16 px = 1 bloco),
formas gordinhas e legíveis, penas/chamas como cubos com volume, textura limpa (cor chapada +
luz em cima / sombra embaixo, sem ruído), olhos grandes com brilho. ~1,5 bloco de altura.
Saída: modelos/pirococo/pirococo_v3.bbmodel + .png + _previa.png"""
import sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from galos_monstro import Modelo
import previa
from PIL import Image, ImageDraw

PASTA = AQUI.parent / "modelos" / "pirococo"
NOME = "pirococo_v3"

VERM = (214, 34, 34); VERM_ESC = (150, 18, 28)
LARANJA = (255, 124, 28); AMARELO = (255, 204, 56)
AZUL = (40, 110, 236); AZUL_ESC = (24, 56, 170); AZUL_CLARO = (150, 214, 255)
OURO = (238, 174, 44); OURO_CLARO = (255, 222, 110); OURO_ESC = (164, 104, 22)
CREME = (255, 240, 196); PRETO = (24, 16, 22); CONTORNO = (90, 10, 20)

def clara(c, k=.2): return tuple(int(v + (255 - v) * k) for v in c)
def esc(c, k=.75): return tuple(int(v * k) for v in c)

def grad(f, faixas):
    for lim, c in faixas:
        if f <= lim + 1e-6: return c
    return faixas[-1][1]

FOGO = [(.45, VERM), (.75, LARANJA), (1, AMARELO)]
AZULG = [(.2, VERM), (.75, AZUL), (1, AZUL_CLARO)]
COBERTURA = [(.6, VERM), (1, LARANJA)]

# ---------------- pintores limpos ----------------
def liso(base, topo=None):
    """Cor chapada: face de cima clara, de baixo escura, 1 px de luz no alto e de sombra embaixo."""
    def p(face, s, t, W, H):
        if face == "up": return clara(topo or base, .15)
        if face == "down": return esc(base)
        if t == 0 and H > 2: return clara(base, .15)
        if t == H - 1 and H > 2: return esc(base, .85)
        return base
    return p

def metal(face, s, t, W, H):
    if face == "up" or t == 0: return OURO_CLARO
    if face == "down" or t == H - 1: return OURO_ESC
    return OURO

def placa(azul="nenhum"):
    """Placa de armadura: moldura dourada (luz em cima, sombra nas bordas) e miolo de ouro;
    azul='centro' põe um filete azul no meio, 'cheio' faz o miolo azul (placa de gema)."""
    def p(face, s, t, W, H):
        if face == "up": return OURO_CLARO
        if face == "down": return OURO_ESC
        if t == 0: return OURO_CLARO
        if t == H - 1 and H > 2: return OURO_ESC
        if W > 2 and s in (0, W - 1): return esc(OURO, .85)
        if azul == "cheio": return AZUL if t < H / 2 else AZUL_ESC
        if azul == "centro" and face in ("north", "south") and abs(s - (W - 1) / 2) < .6: return AZUL
        return OURO
    return p

def ombreira(m, lado):
    """Ombreira em camadas: base larga, placa do meio, lâmina para cima e gema azul na frente."""
    e = "_d" if lado < 0 else "_e"
    def c(nome, de, ate, pintor):
        if lado > 0:
            de, ate = [-ate[0], de[1], de[2]], [-de[0], ate[1], ate[2]]
            return m.cubo(nome + e, de, ate, espelho_de=nome + "_d")
        return m.cubo(nome + e, de, ate, pintor)
    return [m.osso("ombreira" + e, [3.5 * lado, 15, 0], [0, 0, -20 * lado], [
        c("ombreira_base", [-6.5, 14, -3.5], [-2.5, 16, 2.5], placa("centro")),
        c("ombreira_meio", [-6, 16, -3], [-3, 18, 2], placa()),
        c("ombreira_lamina", [-5.5, 18, -1], [-4.5, 20, 0], placa()),
        c("ombreira_gema", [-6, 14.5, -4.5], [-4, 16.5, -3.5], placa("cheio")),
        # forma angulosa: espinho para fora e aba descendo pelo lado (camadas como na arte)
        c("ombreira_espinho", [-8.5, 15, -1], [-6.5, 16, 0], placa()),
        c("ombreira_aba", [-7, 12, -3], [-6, 14, 2], placa()),
    ])]

def pena_x(faixas):
    """Pena-cubo comprida no eixo X, raiz no lado do corpo (x maior na asa direita)."""
    def p(face, s, t, W, H):
        if face == "north": f = s / max(W - 1, 1)
        elif face == "south": f = 1 - s / max(W - 1, 1)
        elif face in ("up", "down"): f = t / max(W - 1, 1)
        else: return esc(grad(.5, faixas), .9)
        c = grad(f, faixas)
        return clara(c, .15) if face == "up" else esc(c) if face == "down" else c
    return p

def pena_z(faixas, borda=None):
    """Pena-cubo comprida no eixo Z (cauda), raiz na frente; borda = fio de cor no alto da pena."""
    def p(face, s, t, W, H):
        if borda and (face == "up" or (face == "side" and t == 0)): return borda
        if face == "side": f = s / max(W - 1, 1)
        elif face in ("up", "down"): f = s / max(H - 1, 1)
        elif face == "north": f = 0
        else: f = 1
        c = grad(f, faixas)
        return clara(c, .15) if face == "up" else esc(c) if face == "down" else (esc(c, .88) if t == H - 1 and H > 1 else c)
    return p

def pena_y(f0, f1):
    """Peça de chama vertical (crina): cor pela altura, de f0 (base) a f1 (ponta)."""
    def p(face, s, t, W, H):
        if face == "up": return clara(grad(f1, FOGO), .15)
        if face == "down": return esc(grad(f0, FOGO))
        f = f1 - (f1 - f0) * (t / max(H - 1, 1))
        return grad(f, FOGO)
    return p

def tronco(face, s, t, W, H):
    if face == "up": return clara(LARANJA, .1)
    if face == "down": return VERM_ESC
    if face == "south": return LARANJA if t <= 1 else VERM
    if face == "side" and t >= H - 2: return esc(VERM, .85)
    return VERM

def peitoral(face, s, t, W, H):
    """Penas em V (chevrons) com fio dourado."""
    if face != "north": return liso(VERM)(face, s, t, W, H)
    # fileiras de penas em V (ponta para baixo): 1 linha de fio dourado + 1 de cor, alternando
    tt = t - int(abs(s - (W - 1) / 2)) + 3
    if tt % 3 == 0: return OURO_CLARO
    return [LARANJA, VERM][(tt // 3) % 2]

def coxa(face, s, t, W, H):        # coxa com franja de penas em ponta embaixo
    if face == "down": return None
    if face != "up" and t == H - 1 and s % 2 == 1: return None
    if face != "up" and t >= H - 2: return LARANJA
    return liso(VERM)(face, s, t, W, H)

def juba(face, s, t, W, H):
    if face == "down": return None
    if face == "up": return LARANJA
    if t == H - 1 and s % 2 == 1: return None
    if t == H - 1: return AMARELO
    return [VERM, LARANJA, AMARELO][s % 3] if t > 0 else VERM

def cabeca(face, s, t, W, H):
    if face == "side":            # W=7 (s=0 frente), H=5 — olho grande com brilho
        olho = {(1, 1): CREME, (2, 1): AZUL, (1, 2): AZUL_CLARO, (2, 2): AZUL_ESC}
        if (s, t) in olho: return olho[(s, t)]
        if (s, t) in ((0, 1), (0, 2), (3, 1), (3, 2), (1, 3), (2, 3)): return CONTORNO
        if t >= 3 and s <= 3: return AMARELO
        if t == 0: return clara(VERM, .12)
        return VERM if s < 5 else LARANJA
    if face == "north":           # olhos dobram a quina: aparecem de frente
        if s in (0, W - 1) and t == 1: return AZUL
        if s in (0, W - 1) and t == 2: return AZUL_ESC
        if t >= 3: return AMARELO
        return VERM
    if face == "up": return clara(VERM, .12)
    if face == "down": return AMARELO
    return LARANJA

def rosto(face, s, t, W, H):
    if face == "down": return AMARELO
    if face == "up": return clara(VERM, .12)
    if t >= 2: return AMARELO if face != "side" or s == 0 else LARANJA
    return VERM

# ---------------- montagem ----------------
def montar(m):
    def perna(lado):
        x = 2.5 * lado; e = "_d" if lado < 0 else "_e"
        def c(nome, de, ate, pintor=None, uv_de=None):
            de = [de[0] + x, de[1], de[2]]; ate = [ate[0] + x, ate[1], ate[2]]
            if lado > 0: return m.cubo(nome + e, de, ate, espelho_de=nome + "_d")
            return m.cubo(nome + e, de, ate, pintor, uv_de=(uv_de + "_d") if uv_de else None)
        def dedo(nome, L, rot, primeiro):
            return m.osso(nome + e, [x, 1, 0], [0, rot, 0], [
                c(nome, [-0.5, 0, -L], [0.5, 1, 0.5], metal),
                c("garra_" + nome, [-0.5, 0, -L - 1], [0.5, 1, -L], liso(CREME)),
            ])
        return m.osso("perna" + e, [x, 11, 0], [0, 0, 0], [
            c("coxa", [-2, 7, -2], [2, 12, 2], coxa),
            c("coxa_placa", [-1.5, 8.5, -3], [1.5, 11.5, -2], placa("centro")),
            c("canela", [-1, 1, -1], [1, 8, 1], metal),
            dedo("dedo_meio", 3, 0, True),
            dedo("dedo_fora", 2, -25 * lado, False),
            dedo("dedo_dentro", 2, 25 * lado, False),
            c("dedo_tras", [-0.5, 0, 0.5], [0.5, 1, 2.5], metal),
            c("espora", [-0.5, 3, 0.5], [0.5, 4, 2.5], liso(CREME)),
        ])

    corpo = m.osso("corpo", [0, 13, 0], [4, 0, 0], [
        m.cubo("tronco", [-3.5, 9, -3], [3.5, 18, 4], tronco),   # corpo esguio
        m.cubo("peitoral", [-3, 10, -8], [3, 17, -3], peitoral),   # peito bem estufado (5 px à frente)
        # ---- armadura (como na arte): peitoral em V, gema, gorjal e ombreiras em camadas ----
        m.osso("peitoral_placa_d", [0, 10, -8.5], [0, 0, 22], [
            m.cubo("peitoral_placa_d", [-3, 10, -9], [0, 16, -8], placa())]),
        m.osso("peitoral_placa_e", [0, 10, -8.5], [0, 0, -22], [
            m.cubo("peitoral_placa_e", [0, 10, -9], [3, 16, -8], espelho_de="peitoral_placa_d")]),
        m.cubo("peitoral_ponta", [-1, 8.5, -9.3], [1, 11.5, -8.3], placa()),
        m.cubo("peitoral_gema", [-0.5, 11.5, -9.7], [0.5, 13.5, -8.7], placa("cheio")),
        m.cubo("gorjal", [-2.5, 16.5, -7.5], [2.5, 18.5, -6.5], placa("centro")),
        *ombreira(m, -1), *ombreira(m, 1),
    ])

    # asas saindo das COSTAS e caindo para baixo como uma CAPA (penas longas até perto do chão)
    TRAS = [(-100, 16, FOGO), (-86, 17, AZULG), (-72, 16, FOGO), (-58, 14, AZULG), (-44, 12, FOGO)]
    FRENTE = [(-90, 7), (-70, 8), (-50, 7)]
    MEIO = (-93, -79, -65, -51)
    ZB = 3.5                                     # profundidade das costas onde as asas nascem
    def asa(lado):
        e = "_d" if lado < 0 else "_e"; x0 = 3 * lado
        def c(nome, de, ate, pintor):
            return m.cubo(nome + e, de, ate, espelho_de=nome + "_d") if lado > 0 else m.cubo(nome + e, de, ate, pintor)
        def ex(a, b):   # intervalo em x saindo da raiz para fora
            return [x0 - b, x0 - a] if lado < 0 else [x0 + a, x0 + b]
        filhos = []
        # cada pena = lâmina de 2 px + ponta de 1 px (fica afiada, como na arte)
        for i, (ang, L, cores) in enumerate(TRAS):
            z = ZB + 1.2 + 0.25 * i
            ponta = AMARELO if cores is FOGO else AZUL_CLARO
            filhos.append(m.osso(f"pena_{i}{e}", [x0, 17, z], [0, 0, ang * lado], [
                c(f"pena_{i}", [ex(0, L - 2)[0], 16, z - 0.5], [ex(0, L - 2)[1], 18, z + 0.5], pena_x(cores[:-1] + [(1, cores[-2][1])])),
                c(f"pena_{i}_ponta", [ex(L - 2, L)[0], 16.5, z - 0.5], [ex(L - 2, L)[1], 17.5, z + 0.5], liso(ponta))]))
        for i, ang in enumerate(MEIO):
            L = 12 if i in (1, 2) else 11
            filhos.append(m.osso(f"pena_meio_{i}{e}", [x0, 17, ZB + 0.5], [0, 0, ang * lado], [
                c(f"pena_meio_{i}", [ex(0, L - 2)[0], 16, ZB], [ex(0, L - 2)[1], 18, ZB + 1], pena_x([(.5, VERM), (1, LARANJA)])),
                c(f"pena_meio_{i}_ponta", [ex(L - 2, L)[0], 16.5, ZB], [ex(L - 2, L)[1], 17.5, ZB + 1], liso(AMARELO))]))
        for i, (ang, L) in enumerate(FRENTE):
            filhos.append(m.osso(f"cobertura_{i}{e}", [x0, 17, ZB - 0.3], [0, 0, ang * lado], [
                c(f"cobertura_{i}", [ex(0, L - 1)[0], 16, ZB - 0.8], [ex(0, L - 1)[1], 18, ZB + 0.2], pena_x(COBERTURA)),
                c(f"cobertura_{i}_ponta", [ex(L - 1, L + 1)[0], 16.5, ZB - 0.8], [ex(L - 1, L + 1)[1], 17.5, ZB + 0.2], liso(AMARELO))]))
        # inclina a capa para trás, afastando as pontas das pernas
        return m.osso("asa" + e, [x0, 17, ZB], [-14, -12 * lado, 0], filhos)

    def crina(i, z, rot, h1, h2):
        return m.osso(f"crina_{i}", [0, 24, z], [rot, 0, 0], [
            m.cubo(f"crina_{i}_base", [-1, 24, z - 1], [1, 24 + h1, z + 1], pena_y(0, .5)),
            m.cubo(f"crina_{i}_ponta", [-0.5, 24 + h1, z - 0.5], [0.5, 24 + h1 + h2, z + 0.5], pena_y(.5, 1)),
        ])
    def chama_bochecha(lado, i, y, L, ry):
        e = "_d" if lado < 0 else "_e"; x = 3 * lado
        kw = dict(pintor=pena_z(FOGO)) if lado < 0 else dict(espelho_de=f"chama_bochecha_{i}_d")
        return m.osso(f"chama_bochecha_{i}{e}", [x, y, -2], [-20, ry * lado * -1, 0], [
            m.cubo(f"chama_bochecha_{i}{e}", [x - 0.5, y - 0.5, -2], [x + 0.5, y + 0.5, -2 + L], **kw)])

    cab = m.osso("cabeca", [0, 20, -1], [8, 0, 0], [   # cabeça erguida
        # crânio + rosto mais estreito na frente = perfil de ave de rapina
        m.cubo("cabeca", [-3, 19, -5], [3, 24, 2], cabeca),
        m.cubo("rosto", [-2, 19, -6.5], [2, 23, -5], rosto),
        m.cubo("bico", [-1, 20, -10], [1, 22, -6.5], metal),
        m.cubo("bico_crista", [-0.5, 22, -9], [0.5, 23, -6], metal),
        m.cubo("bico_gancho", [-1, 18.5, -10.5], [1, 20.5, -9.5], liso(OURO_ESC)),
        m.cubo("bico_baixo", [-0.5, 19, -8.5], [0.5, 20, -6.5], liso(OURO_ESC)),
        m.osso("sobrancelha_d", [-2, 23, -5], [0, 0, -15], [m.cubo("sobrancelha_d", [-3.5, 22.5, -6], [-0.5, 23.5, -4.5], metal)]),
        m.osso("sobrancelha_e", [2, 23, -5], [0, 0, 15], [m.cubo("sobrancelha_e", [0.5, 22.5, -6], [3.5, 23.5, -4.5], espelho_de="sobrancelha_d")]),
        crina(1, -3.5, -40, 3, 3), crina(2, -1, -58, 3, 4), crina(3, 1.5, -75, 3, 3),
        chama_bochecha(-1, 0, 20.5, 5, 20), chama_bochecha(1, 0, 20.5, 5, 20),
        chama_bochecha(-1, 1, 22, 4, 30), chama_bochecha(1, 1, 22, 4, 30),
    ])
    pesc = m.osso("pescoco", [0, 17, -0.5], [0, 0, 0], [
        m.cubo("pescoco", [-2.5, 16, -3], [2.5, 20, 2], liso(LARANJA)),
        m.cubo("juba", [-3.5, 16, -3.5], [3.5, 19, 2.5], juba),
        cab,
    ])

    # cauda em cascata: penas longas que descem quase até o chão, com ponta afinada
    PENAS_CAUDA = [(0, 0, 32, 18, FOGO), (-1.5, 16, 38, 16, AZULG), (1.5, -16, 38, 16, AZULG),
                   (-2.5, 30, 46, 13, FOGO), (2.5, -30, 46, 13, FOGO), (0, 0, 52, 11, AZULG)]
    penas = []
    for i, (x, ry, rx, L, cores) in enumerate(PENAS_CAUDA):
        ponta = AMARELO if cores is FOGO else AZUL_CLARO
        penas.append(m.osso(f"cauda_pena_{i}", [x, 11, 4], [rx, ry, 0], [
            m.cubo(f"cauda_pena_{i}", [x - 0.5, 10, 4], [x + 0.5, 12, 4 + L - 2], pena_z(cores, borda=OURO_CLARO)),
            m.cubo(f"cauda_pena_{i}_ponta", [x - 0.5, 10.5, 2 + L], [x + 0.5, 11.5, 4 + L], liso(ponta))]))
    cauda = m.osso("cauda", [0, 11, 4], [0, 0, 0], [
        m.cubo("cauda_base", [-2, 9.5, 3], [2, 12.5, 6], liso(VERM)), *penas])
    pernas = [perna(-1), perna(1)]
    asas = [asa(-1), asa(1)]

    # silhueta de galo: pernas mais longas (+DY) e pescoço mais alto (+DN) -> ~1,75 bloco até a cabeça
    DY, DN = 2, 2
    def desloca(no, dy):
        if isinstance(no, str):
            for cb in m.cubos.values():
                if cb["uuid"] == no:
                    cb["from"][1] += dy; cb["to"][1] += dy
            return
        no["origin"][1] += dy
        for f in no["children"]: desloca(f, dy)
    for no in (corpo, pesc, cauda, *asas): desloca(no, DY)
    desloca(cab, DN)
    m.cubos["pescoco"]["to"][1] += DN
    for lado, pn in zip("de", pernas):
        pn["origin"][1] += DY
        for nome in ("coxa", "coxa_placa"):
            cb = m.cubos[f"{nome}_{lado}"]; cb["from"][1] += DY; cb["to"][1] += DY
        m.cubos[f"canela_{lado}"]["to"][1] += DY
    return [corpo, pesc, cauda, *pernas, *asas]

if __name__ == "__main__":
    m = Modelo(NOME)
    caminho, n, tam = m.salvar(montar(m), largura=128, pasta=PASTA)
    q = previa.carregar(str(caminho))
    vistas = [("frente", 0, -6), ("lado", 90, -4), ("3/4 frente", -35, -14), ("costas", 180, -6)]
    ims = [(v, previa.desenhar(q, y, p, escala=12)) for v, y, p in vistas]
    H = max(i.height for _, i in ims) + 24
    folha = Image.new("RGB", (sum(i.width for _, i in ims) + 30, H), (22, 24, 29)); x = 0
    for v, i in ims:
        folha.paste(i, (x, 24 + (H - 24 - i.height))); ImageDraw.Draw(folha).text((x + 8, 6), v, fill=(220, 220, 220))
        x += i.width + 10
    folha.save(PASTA / f"{NOME}_previa.png")
    alt = max(p[1] for qd in q for p in qd[0])
    print(f"{n} cubos, textura {tam}, topo {alt:.1f}px = {alt/16:.2f} blocos")
