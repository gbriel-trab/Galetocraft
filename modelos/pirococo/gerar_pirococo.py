#!/usr/bin/env python3
"""Pirococó (#001, fogo, mítico), "O Galo Fênix": gerador do modelo do zero.

Gera, a partir deste arquivo só (Python 3 + numpy + Pillow):
- pirococo.geo.json          geometria Bedrock 1.12.0 (geometry.pirococo), 1 px de textura por unidade
- pirococo.png               textura
- pirococo_glowmask.png      brilho (só os cubos dos ossos *_brilho)
- pirococo.animation.json    animation.pirococo.idle (4 s) e animation.pirococo.walk (2 s), em laço
- imagens de conferência     pirococo_vistas.png, pirococo_comparacao.png, pirococo_rosto.png, pirococo_andar.png

Uso:
  python modelos/pirococo/gerar_pirococo.py              gera tudo nesta pasta
  python modelos/pirococo/gerar_pirococo.py --instalar   ... e copia os 4 arquivos para os assets do mod

Convenções (as do GeckoLib/Bedrock): 16 u = 1 bloco; y para cima, chão em y = 0; x negativo = lado DIREITO da
criatura (sufixo _d); a frente (bico) fica em z negativo. Rotação de osso/cubo [rx, ry, rz] em graus:
rx > 0 inclina o topo para a frente; ry > 0 vira a frente para o lado direito (-x); rz > 0 inclina o topo para +x.
"""
import copy
import json
import math
import random
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
sys.path.insert(0, str(RAIZ / "ferramentas"))
import render_geo as rg  # noqa: E402

ID = "pirococo"
FICHA = RAIZ / "modelos/referencias/001_pirococo_ficha_v3.png"
ASSETS = RAIZ / "galetocraft/src/main/resources/assets/galetocraft"
ALTURA = 45            # chão -> ponta da crista (2,8 blocos)
ORCAMENTO = (110, 170)  # cubos (teto 200)

# ======================================================================================================
# Paleta da ficha: rampas luz, claro, BASE, sombra, sombra funda
# ======================================================================================================
RAMPA = {
    "verm":  ["#ff5b3f", "#ef392d", "#dd1c20", "#b90c27", "#960429"],
    "creme": ["#fff6e0", "#ffeed1", "#fde1c0", "#d9b398", "#b68b78"],
    "roxo":  ["#a0499e", "#88398e", "#702a7c", "#491847", "#300e34"],
    "roxoe": ["#5b2354", "#491847", "#3a1239", "#2c0c2e", "#210826"],
    "prata": ["#f6f6f6", "#e4dce3", "#d2bed1", "#ac93ae", "#86708b"],
    "ouro":  ["#ffe138", "#ffcd29", "#fcb419", "#d87b08", "#b55100"],
    "rubi":  ["#da3879", "#c82775", "#b61972", "#920b6a", "#6f0459"],
    "olho":  ["#fff6e0", "#e8352b", "#9e1020", "#5a0812", "#210826"],   # brilho, claro, íris, sombra, pupila
}
COR = {m: [tuple(int(h[i:i + 2], 16) for i in (1, 3, 5)) for h in r] for m, r in RAMPA.items()}
LUZ, CLARO, BASE, SOMBRA, FUNDA = range(5)
SEM_GRAO = {"olho", "rubi"}

# ======================================================================================================
# Esqueleto: ossos e cubos
# ======================================================================================================
OSSOS = []
POR_NOME = {}


class Osso:
    def __init__(self, nome, pai, pivo, rot=(0, 0, 0)):
        self.nome, self.pai, self.pivo, self.rot = nome, pai, [float(v) for v in pivo], [float(v) for v in rot]
        self.cubos = []


class Cubo:
    def __init__(self, osso, origem, tam, pintor, inflate=0.0, rot=None, pivo=None, espelho=False, de=None, nome=""):
        self.osso, self.origem, self.tam = osso, [float(v) for v in origem], [int(v) for v in tam]
        assert all(abs(t - v) < 1e-9 for t, v in zip(self.tam, tam)), f"{nome}: tamanho fracionado {tam}"
        self.pintor, self.inflate, self.rot, self.pivo = pintor, inflate, rot, pivo
        self.espelho, self.de, self.nome = espelho, de, nome
        zeros = [i for i, v in enumerate(self.tam) if v == 0]
        assert len(zeros) <= 1, f"{nome}: mais de uma medida zero"
        self.plano = {0: "east", 1: "up", 2: "north"}[zeros[0]] if zeros else None
        self.uv = None


def osso(nome, pai, pivo, rot=(0, 0, 0)):
    o = Osso(nome, pai.nome if isinstance(pai, Osso) else pai, pivo, rot)
    assert nome not in POR_NOME, nome
    OSSOS.append(o)
    POR_NOME[nome] = o
    return o


PARES = {}


def _par(c, par):
    """Peças iguais (lado esquerdo, segmentos de trança) usam a mesma ilha de UV; caixas vão espelhadas."""
    if not par:
        return
    if par in PARES:
        dono = PARES[par]
        assert dono.tam == c.tam and dono.plano == c.plano, f"{c.nome}: par '{par}' com outro tamanho"
        xd, xc = dono.origem[0] + dono.tam[0] / 2, c.origem[0] + c.tam[0] / 2
        c.de, c.espelho = dono, c.plano is None and xd * xc < 0 and min(abs(xd), abs(xc)) > 0.5
    else:
        PARES[par] = c


def caixa(o, origem, tam, pintor, par=None, **k):
    c = Cubo(o, origem, tam, pintor, **k)
    assert c.plano is None, f"{c.nome}: caixa com medida zero"
    _par(c, par)
    o.cubos.append(c)
    return c


def plano(o, origem, tam, pintor, par=None, **k):
    c = Cubo(o, origem, tam, pintor, **k)
    assert c.plano, f"{c.nome}: plano sem medida zero"
    _par(c, par)
    o.cubos.append(c)
    return c


def ilha(c):
    """Tamanho (largura, altura) da ilha de UV do cubo, em pixels."""
    w, h, d = c.tam
    if c.plano == "north": return w, h
    if c.plano == "east": return d, h
    if c.plano == "up": return w, d
    return 2 * d + 2 * w, d + h


def rot_json(r):
    """Matriz da rotação Bedrock [rx, ry, rz] no espaço do JSON (o do renderizador, com x desvirado)."""
    a, b, c = (math.radians(v) for v in (-r[0], r[1], -r[2]))
    Rx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
    Ry = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
    Rz = np.array([[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def mundo(nome_osso, p, anim=None):
    """Posição no mundo (espaço do JSON) de um ponto p dado na pose de modelagem do osso."""
    anim = anim or {}
    cadeia = []
    o = POR_NOME[nome_osso]
    while o:
        cadeia.append(o)
        o = POR_NOME.get(o.pai)
    q = np.array(p, float)
    for o in cadeia:
        a = anim.get(o.nome, {})
        r = [o.rot[i] + a.get("rotation", [0, 0, 0])[i] for i in range(3)]
        pv = np.array(o.pivo)
        q = rot_json(r) @ (q - pv) + pv + np.array(a.get("position", [0, 0, 0]))
    return q


# ======================================================================================================
# Pintura: cada cubo tem um pintor(t) -> (material, tom[, grão]) ou None (transparente)
# ======================================================================================================
class Texel:
    __slots__ = ("face", "i", "j", "fw", "fh", "p", "r", "c")


def faces_uv(c):
    """{face: [u1, v1, u2, v2]} da ilha do cubo (sem espelho)."""
    u, v = c.uv
    if c.plano:
        fw, fh = ilha(c)
        return {c.plano: [u, v, u + fw, v + fh]}
    return rg.uv_caixa(u, v, c.tam, False)


def ponto(face, c, uu, vv):
    o, s = c.origem, c.tam
    de = [-(o[0] + s[0]), o[1], o[2]]
    ate = [-o[0], o[1] + s[1], o[2] + s[2]]
    x, y, z = rg.canto(face, de, ate, uu, vv)
    return (-x, y, z)


def pintar_textura(cubos, W, H, semente=1):
    idx = {}                      # (px, py) -> (material, tom, grão)
    rnd = random.Random(semente)
    for n, c in enumerate(cubos):
        if c.de is not None:
            continue
        for face, (u1, v1, u2, v2) in faces_uv(c).items():
            fw, fh = abs(u2 - u1), abs(v2 - v1)
            if fw == 0 or fh == 0:
                continue
            area = {}
            for py in range(min(v1, v2), max(v1, v2)):
                for px in range(min(u1, u2), max(u1, u2)):
                    uu = (px + .5 - u1) / (u2 - u1)
                    vv = (py + .5 - v1) / (v2 - v1)
                    t = Texel()
                    t.face, t.fw, t.fh, t.c = face, fw, fh, c
                    t.i, t.j = int(uu * fw), int(vv * fh)
                    t.p = ponto(face, c, uu, vv)
                    t.r = tuple((t.p[k] - c.origem[k]) / c.tam[k] if c.tam[k] else 0.0 for k in range(3))
                    val = c.pintor(t)
                    if val is None:
                        continue
                    if len(val) == 2:
                        val = (val[0], val[1], val[0] not in SEM_GRAO)
                    area[(px, py)] = (val[0], max(0, min(4, int(val[1]))), val[2])
            grao(area, rnd)
            idx.update(area)
    img = np.zeros((H, W, 4), np.uint8)
    for (px, py), (m, tom, _) in idx.items():
        img[py, px] = (*COR[m][tom], 255)
    return img


def grao(area, rnd):
    """~6-8% dos pixels mudam 1 tom, em manchinhas de 1-3 px, sem trocar de material."""
    pix = [k for k, v in area.items() if v[2]]
    if len(pix) < 8:
        return
    for _ in range(max(1, round(len(pix) * 0.035))):
        x, y = rnd.choice(pix)
        d = rnd.choice((-1, 1))
        m0 = area[(x, y)][0]
        for _ in range(rnd.choice((1, 2, 2, 3))):
            v = area.get((x, y))
            if v and v[2] and v[0] == m0:
                area[(x, y)] = (v[0], max(0, min(4, v[1] + d)), True)
            x, y = x + rnd.choice((-1, 0, 1)), y + rnd.choice((-1, 0, 1))


# ---------------- pintores prontos ----------------
def faixa(t, base=BASE, terco=True):
    """Luz de cima em faixas: topo do volume 1 tom acima, última fileira 1 tom abaixo."""
    if t.face == "up": return base - 1
    if t.face == "down": return base + 1
    h = t.c.tam[1]
    fila_de_baixo = (t.p[1] - t.c.origem[1]) < 1.0
    if terco and t.r[1] >= 2 / 3: return base - 1
    if fila_de_baixo and h >= 3: return base + 1
    return base


def liso(mat, base=BASE):
    return lambda t: (mat, faixa(t, base))


def plana(arte, grao=False):
    """Pintor de plano a partir de uma grade de pixel art (sem grão por padrão: penas pequenas ficam limpas)."""
    def f(t):
        v = arte.g[t.j][t.i] if 0 <= t.j < arte.h and 0 <= t.i < arte.w else None
        return None if v is None else (v[0], v[1], grao and v[0] not in SEM_GRAO)
    return f


# ======================================================================================================
# Pixel art dos planos (penas, chamas, lâminas)
# ======================================================================================================
class Arte:
    def __init__(self, w, h):
        self.w, self.h = int(w), int(h)
        self.g = [[None] * self.w for _ in range(self.h)]

    def put(self, i, j, v):
        if 0 <= i < self.w and 0 <= j < self.h:
            self.g[j][i] = v

    def espelho(self):
        a = Arte(self.w, self.h)
        a.g = [list(reversed(l)) for l in self.g]
        return a

    def pena(self, raiz, ponta, larg, curva=0.0, cores=None, perfil="pena", haste=+1, borda_baixo=True, folga=0.2,
             filete=None):
        """Pena/chama recortada: linha central curva (Bézier) da raiz à ponta, largura afinando em degrau.
        cores(t) -> (material, tom) ao longo da pena (t = 0 na raiz, 1 na ponta)."""
        R, T = np.array(raiz, float), np.array(ponta, float)
        d = T - R
        L = float(np.linalg.norm(d))
        n = np.array([-d[1], d[0]]) / max(L, 1e-6)
        C = (R + T) / 2 + n * curva
        ts = np.linspace(0, 1, 90)
        pts = ((1 - ts) ** 2)[:, None] * R + (2 * (1 - ts) * ts)[:, None] * C + (ts ** 2)[:, None] * T
        tang = np.gradient(pts, axis=0)
        novos = {}
        for j in range(self.h):
            for i in range(self.w):
                q = np.array([i + .5, j + .5])
                dd = np.linalg.norm(pts - q, axis=1)
                k = int(np.argmin(dd))
                t, dist = ts[k], dd[k]
                if perfil == "pena":
                    meia = larg / 2 * (min(1.0, (1 - t) / 0.6) ** 0.85) * (0.75 + 0.25 * min(1, t / 0.12))
                elif perfil == "chama":   # gota: raiz estreita, barriga perto de 1/3, ponta fina
                    meia = larg / 2 * ((1 - t) ** 0.8) * (0.65 + 0.35 * min(1.0, t / 0.3))
                else:  # lamina
                    meia = larg / 2 * (math.sin(math.pi * min(1, t * 1.1)) ** 0.7)
                if t <= 0.0 and dist > meia:
                    continue
                if dist > meia + folga:
                    continue
                lado = float(np.sign(tang[k][0] * (q[1] - pts[k][1]) - tang[k][1] * (q[0] - pts[k][0])))
                m, tom = cores(t) if cores else ("verm", BASE)
                if haste and dist < 0.55 and 0.12 < t < 0.8:
                    tom += haste
                if filete and lado == filete[0] and dist > meia - 1.0 and 0.08 < t < 0.9:
                    m, tom = filete[1], filete[2]
                novos[(i, j)] = (m, tom)
        if borda_baixo:   # 1 px mais escuro na borda de baixo (onde a pena sobrepõe a de trás)
            for (i, j), (m, tom) in list(novos.items()):
                if (i, j + 1) not in novos and j + 1 < self.h:
                    novos[(i, j)] = (m, tom + 1)
        for (i, j), (m, tom) in novos.items():
            self.put(i, j, (m, max(0, min(4, tom))))
        return self

    def copia(self, so=None, sem=None):
        """Cópia só com (ou sem) os pixels de uma etiqueta (3º campo do valor)."""
        a = Arte(self.w, self.h)
        for j in range(self.h):
            for i in range(self.w):
                v = self.g[j][i]
                if v is None:
                    continue
                tag = v[2] if len(v) > 2 else None
                if (so is not None and tag != so) or (sem is not None and tag == sem):
                    continue
                a.g[j][i] = v[:2]
        return a

    def mapa(self, linhas, legenda, x0=0, y0=0):
        """Desenha uma grade de caracteres (legenda: char -> (material, tom) ou None)."""
        for j, l in enumerate(linhas):
            for i, ch in enumerate(l):
                if ch in legenda:
                    v = legenda[ch]
                    if v is None:
                        if 0 <= i + x0 < self.w and 0 <= j + y0 < self.h:
                            self.g[j + y0][i + x0] = None
                    else:
                        self.put(i + x0, j + y0, v)
        return self


def chama(a, raiz, ponta, larg, curva=0.0, mat="verm", borda=False):
    """Língua de fogo/pena de crista: forma cheia, raiz escura, núcleo 1 tom mais claro, ponta clara."""
    return a.pena(raiz, ponta, larg, curva=curva, cores=rampa_t(mat, (SOMBRA, BASE, CLARO, LUZ), (0.15, 0.5, 0.85)),
                  perfil="chama", haste=0, borda_baixo=borda, folga=0.35)


def arte_leque(W, H, raiz, ang0, ang1, compr, camada, filete=True):
    """Painel de penas em leque com a barra recortada em zigue-zague (pontas em degrau).
    raiz (u, v): de onde as penas saem; ângulos em graus a partir da vertical para baixo (positivo = para a
    coluna 0); compr: comprimento de cada pena. Camada 0 = vermelha comprida, 1 = roxa->vermelha,
    2 = roxa curta com filete prata. As divisões entre penas são 1 px mais escuras."""
    a = Arte(W, H)
    n = len(compr)
    passo = math.radians((ang1 - ang0) / n)
    for j in range(H):
        for i in range(W):
            du, dv = i + .5 - raiz[0], j + .5 - raiz[1]
            if dv <= 0:
                continue
            rho = math.hypot(du, dv)
            th = math.degrees(math.atan2(-du, dv))
            f = (th - ang0) / (ang1 - ang0) * n
            if f < 0 or f >= n:
                continue
            k = int(f)
            fr = f - k
            L = compr[k]
            ponta = 0.85 * L * passo          # profundidade do recorte entre penas
            borda = L - ponta * abs(2 * fr - 1)
            if rho > borda:
                continue
            t = rho / L
            arco = rho * passo * min(fr, 1 - fr)
            if camada == 0:
                m, tom = "verm", (SOMBRA if t < 0.5 else BASE if t < 0.8 else CLARO if t < 0.93 else LUZ)
            elif camada == 1:
                m, tom = (("roxo", SOMBRA) if t < 0.2 else ("roxo", BASE) if t < 0.62 else ("roxo", CLARO) if t < 0.76
                          else ("verm", SOMBRA) if t < 0.83 else ("verm", BASE) if t < 0.94 else ("verm", CLARO))
            else:
                m, tom = "roxo", (SOMBRA if t < 0.18 else BASE if t < 0.6 else CLARO)
                arco_fora = rho * passo * (1 - fr)
                if filete and 0.6 < arco_fora < 1.6 and 0.2 < t < 0.9:
                    m, tom = "prata", BASE if t < 0.5 else CLARO
            if arco < 0.6 and t > 0.3:
                tom += 1                          # divisão entre penas
            if camada and rho > borda - 1.0:
                tom += 1                          # borda de baixo, onde sobrepõe a camada de trás
            a.put(i, j, (m, min(FUNDA, tom)))
    return a


def rampa_t(mat, tons=(SOMBRA, BASE, CLARO, LUZ), cortes=(0.22, 0.55, 0.85)):
    """Cor ao longo da pena: raiz escura -> ponta clara, em degraus."""
    def f(t):
        k = sum(t >= c for c in cortes)
        return mat, tons[k]
    return f


def roxo_verm(corte=0.5):
    """Pena roxa na raiz que vira vermelha na ponta (camada do meio da capa)."""
    def f(t):
        if t < corte * 0.45: return "roxo", SOMBRA
        if t < corte: return "roxo", BASE
        if t < corte + 0.12: return "verm", SOMBRA
        if t < 0.85: return "verm", BASE
        return "verm", CLARO
    return f


# ======================================================================================================
# A criatura
# ======================================================================================================
def montar():
    raiz = osso(ID, None, (0, 0, 0))
    corpo = osso("corpo", raiz, (0, 15, -1))
    montar_tronco(corpo)
    pescoco = osso("pescoco", corpo, (0, 29, -4))
    caixa(pescoco, (-2.5, 27, -7), (5, 5, 5), pintor_pescoco, nome="pescoco")
    cabeca = osso("cabeca", pescoco, (0, 31.5, -3.5))
    montar_cabeca(cabeca)
    montar_crista(cabeca)
    montar_capa(corpo)
    montar_ombreiras(corpo)
    montar_cauda(corpo)
    for lado in (-1, 1):
        montar_perna(raiz, lado)


# ---------------------------------------- tronco, peitoral ----------------------------------------
def pintor_tronco(t):
    x, y, z = t.p
    if t.face == "north":
        if abs(x) < 3.5:
            if y < 16 and (int(x + 10) + int(y)) % 2 == 0: return "verm", BASE    # franja das penas do peito
            return "creme", BASE if y > 16 else SOMBRA
        return "roxo", SOMBRA                                                     # forro da capa
    if t.face in ("east", "west") and z < -4.0 and y > 14.5:
        if y < 16 and int(math.floor(z)) % 2 == 0: return "verm", BASE
        return "creme", BASE if y > 16 else SOMBRA
    if t.face == "down": return "verm", SOMBRA
    return "verm", faixa(t)


def pintor_peito(t):
    x, y, z = t.p
    if t.face == "north":
        # chevrons de pena (V de 1 px, um tom abaixo)
        for yc in (19.5, 23.0):
            if abs((y - yc) - (abs(x) * 0.55)) < 0.5 and abs(x) < 3.5:
                return "creme", SOMBRA
        return "creme", CLARO if y > 24 else BASE
    if t.face == "down": return "creme", SOMBRA
    if t.face == "up": return "creme", CLARO
    return "creme", CLARO if y > 24 else BASE


def pintor_pescoco(t):
    x, y, z = t.p
    if t.face == "north" or (t.face in ("east", "west") and z < -5):
        return "creme", BASE if y > 28 else SOMBRA
    return "verm", faixa(t)


def montar_tronco(corpo):
    caixa(corpo, (-5, 15, -6.5), (10, 13, 9), pintor_tronco, nome="tronco")
    caixa(corpo, (-4, 17, -8.5), (8, 10, 2), pintor_peito, nome="peito")
    # gola: anel prateado em volta da base do pescoço
    caixa(corpo, (-4, 28, -7.5), (8, 2, 7), pintor_gola, nome="gola")
    # colar em V (camada 1) e moldura da gema (camada 2): placas com recorte
    caixa(corpo, (-5, 21, -9.5), (10, 9, 1), pintor_v(ARTE_V1), nome="colar_v")
    caixa(corpo, (-3, 22, -10), (6, 7, 1), pintor_v(ARTE_V2), nome="colar_moldura")
    # placa das costas (V prateado com losango roxo pintado)
    caixa(corpo, (-4, 25, 2.5), (8, 5, 1), pintor_v(ARTE_COSTAS, costas=True), nome="colar_costas")
    gema = osso("gema_peito_brilho", corpo, (0, 25.5, -10.5))
    caixa(gema, (-1.5, 23, -10.5), (3, 5, 1), pintor_gema_peito, nome="gema_peito")


def pintor_gola(t):
    x, y, z = t.p
    if t.face == "up": return "prata", LUZ if abs(x) > 2.5 or z < -6.5 else CLARO
    if t.face == "down": return "prata", SOMBRA
    return "prata", CLARO if y > 29 else BASE


# V do colar (10 x 9, y 30 -> 21). S = prata, L = luz (chanfro de cima), B = sombra (borda de baixo), R = roxo
ARTE_V1 = [
    "LLL....LLL",
    "SSSL..LSSS",
    "BSSS..SSSB",
    ".BSSLLSSB.",
    "..BSSSSB..",
    "..BSSSSB..",
    "...BSSB...",
    "...BSSB...",
    "....BB....",
]
# moldura da gema (6 x 7, y 29 -> 22)
ARTE_V2 = [
    "L....L",
    "SL..LS",
    ".S..S.",
    ".S..S.",
    ".BSSB.",
    "..SS..",
    "..BB..",
]
# costas (8 x 5, y 30 -> 25)
ARTE_COSTAS = [
    "LLL..LLL",
    "BSSLLSSB",
    ".BSRRSB.",
    "..BSSB..",
    "...BB...",
]
LEG_V = {"S": ("prata", BASE), "L": ("prata", LUZ), "B": ("prata", SOMBRA), "R": ("roxo", CLARO), ".": None}


def pintor_v(arte, costas=False):
    def f(t):
        x, y, z = t.p
        c = t.c
        w = c.tam[0]
        col = int(math.floor(x - c.origem[0]))
        lin = int(math.floor(c.origem[1] + c.tam[1] - y))
        col = min(max(col, 0), w - 1)
        lin = min(max(lin, 0), c.tam[1] - 1)
        ch = arte[lin][col]
        frente = "south" if costas else "north"
        if t.face == frente:
            return LEG_V[ch]
        if t.face in ("north", "south"):
            return None if ch == "." else ("prata", SOMBRA)
        # laterais/topo/base: só onde a face da frente tem metal na borda
        if t.face == "up":
            return None if arte[0][col] == "." else ("prata", LUZ)
        if t.face == "down":
            return None if arte[-1][col] == "." else ("prata", FUNDA)
        borda = w - 1 if t.face == "west" else 0   # west = +x (lado esquerdo), east = -x (direito)
        return None if arte[lin][borda] == "." else ("prata", SOMBRA)
    return f


def pintor_gema_peito(t):
    x, y, z = t.p
    c = t.c
    col = int(math.floor(x - c.origem[0]))
    lin = int(math.floor(c.origem[1] + c.tam[1] - y))
    forma = [".L.", "LCB", "CBS", "BSF", ".S."]
    ch = forma[min(max(lin, 0), 4)][min(max(col, 0), 2)]
    if ch == ".": return None
    tom = {"L": LUZ, "C": CLARO, "B": BASE, "S": SOMBRA, "F": FUNDA}[ch]
    if t.face in ("east", "west", "up", "down", "south"):
        tom = min(4, tom + 1)
    return "rubi", tom


# ---------------------------------------- cabeça ----------------------------------------
def pintor_cabeca(t):
    x, y, z = t.p
    if t.face == "north":
        if y < 32.9 and abs(x) < 2.6:
            return "creme", BASE if y > 32 else SOMBRA
        return "verm", CLARO if y > 36 else (BASE if y > 32 else SOMBRA)
    if t.face in ("east", "west"):
        # bochecha creme embaixo do olho, descendo para a garganta
        if z < -4.5 and y < 33.9:
            return "creme", BASE if y > 32 else SOMBRA
        if z < -2.5 and y < 32.9:
            return "creme", SOMBRA
        return "verm", faixa(t)
    if t.face == "down":
        return ("creme", SOMBRA) if z < -3.5 else ("verm", SOMBRA)
    if t.face == "up":
        return "verm", SOMBRA if (int(math.floor(z - abs(x) * 0.8)) % 3 == 0) else BASE
    if t.face == "south":
        return "verm", SOMBRA if (int(math.floor(y - abs(x) * 0.8)) % 3 == 0) else faixa(t)
    return "verm", faixa(t)


# viseira/elmo (sobreposição 7 x 4 x 6, y 35 -> 39): frente, lados, topo
ELMO_FRENTE = [
    "S.....S",
    "SS...SS",
    ".SS.SS.",
    "..S.S..",
]
ELMO_LADO = [      # coluna 0 = trás (z -0.5) ... 5 = frente (z -6.5)
    "SS....",
    ".SS..S",
    "..SSSS",
    "......",
]


def pintor_elmo(t):
    x, y, z = t.p
    c = t.c
    lin = min(max(int(math.floor(c.origem[1] + c.tam[1] - y)), 0), 3)
    if t.face == "north":
        col = min(max(int(math.floor(x + 3.5)), 0), 6)
        ch = ELMO_FRENTE[lin][col]
    elif t.face in ("east", "west"):
        col = min(max(int(math.floor(-0.5 - z)), 0), 5)     # 0 = trás, 5 = frente
        ch = ELMO_LADO[lin][col]
    elif t.face == "up":
        ch = "S" if z > -2.5 else "."
    else:
        ch = "."
    if ch == ".": return None
    # chanfro pintado: aresta de cima mais clara
    tom = BASE
    col = min(max(int(math.floor(x + 3.5)), 0), 6)
    if t.face == "up": tom = CLARO
    elif t.face == "north" and (lin == 0 or ELMO_FRENTE[lin - 1][col] == "."):
        tom = CLARO
    elif t.face == "north" and (lin == 3 or ELMO_FRENTE[lin + 1][col] == "."):
        tom = SOMBRA
    return "prata", tom


def pintor_gema_testa(t):
    x, y, z = t.p
    c = t.c
    col = int(math.floor(x - c.origem[0]))
    lin = int(math.floor(c.origem[1] + c.tam[1] - y))
    forma = ["LC", "CB", "BS", "SF"]
    ch = forma[min(max(lin, 0), 3)][min(max(col, 0), 1)]
    tom = {"L": LUZ, "C": CLARO, "B": BASE, "S": SOMBRA, "F": FUNDA}[ch]
    if t.face != "north":
        tom = min(4, tom + 1)
    return "rubi", tom


def pintor_bico(t):
    x, y, z = t.p
    if t.face == "up": return "ouro", CLARO
    if t.face == "down": return "ouro", SOMBRA
    c = t.c
    if (y - c.origem[1]) < 1.0 and c.tam[1] >= 2: return "ouro", SOMBRA
    return "ouro", BASE


def pintor_olho(lado):
    """Olho no canto da cara: frente 2x1 (íris fora, pupila dentro), lado 2x1 (branco atrás, íris na frente)."""
    def f(t):
        x, y, z = t.p
        if t.face == "north":
            dentro = abs(x) < 2.5
            return ("olho", FUNDA) if dentro else ("olho", LUZ)
        if (t.face == "east" and lado < 0) or (t.face == "west" and lado > 0):
            frente = z < -5.5
            return ("olho", FUNDA) if frente else ("olho", LUZ)
        return "verm", SOMBRA
    return f


def montar_cabeca(cabeca):
    caixa(cabeca, (-3.5, 31, -6.5), (7, 8, 6), pintor_cabeca, nome="cabeca")
    caixa(cabeca, (-3.5, 35, -6.5), (7, 4, 6), pintor_elmo, inflate=0.03, nome="elmo")
    # bico de rapina em degrau: base 3, meio 2, gancho 1
    caixa(cabeca, (-1.5, 32, -8.5), (3, 2, 2), pintor_bico, nome="bico_base")
    caixa(cabeca, (-1, 31, -10), (2, 2, 2), pintor_bico, nome="bico_meio")
    caixa(cabeca, (-0.5, 30.5, -11), (1, 2, 2), pintor_bico, nome="bico_gancho")
    mand = osso("mandibula", cabeca, (0, 31.5, -6.5))
    caixa(mand, (-0.5, 30.5, -8.5), (1, 1, 2), pintor_bico, nome="mandibula")
    gema = osso("gema_testa_brilho", cabeca, (0, 37, -7))
    caixa(gema, (-1, 35, -7.5), (2, 4, 1), pintor_gema_testa, nome="gema_testa")
    olhos = osso("olhos", cabeca, (0, 35.5, -6))
    for lado in (-1, 1):
        x0 = -3.5 if lado < 0 else 1.5
        caixa(olhos, (x0, 35, -6.5), (2, 1, 2), pintor_olho(lado), inflate=0.02, nome=f"olho_{'d' if lado < 0 else 'e'}")
        pal = osso(f"palpebra_{'d' if lado < 0 else 'e'}", cabeca, (x0 + 1, 35.5, -5.5))
        caixa(pal, (x0, 35, -6.5), (2, 1, 2), lambda t: ("verm", SOMBRA if t.face == "down" else BASE),
              inflate=0.01, nome=f"palpebra_{'d' if lado < 0 else 'e'}")
    # asas da tiara (sobem para trás nas laterais)
    asa = Arte(4, 4).pena((3.6, 3.4), (0.3, 0.3), 2.2, curva=-0.4, cores=rampa_t("prata", (SOMBRA, BASE, CLARO, LUZ)),
                          haste=0, borda_baixo=False)
    for lado in (-1, 1):
        plano(cabeca, (3.58 * lado, 37, -3), (0, 4, 4), plana(asa), nome=f"tiara_{'d' if lado < 0 else 'e'}")
    # nuca: as duas lâminas de baixo da vista lateral + leque de trás (vista de costas)
    chama_x(cabeca, (0.0, 35.0), (7.0, 30.5), 4.0, 0.8, 0, "nuca_1")
    chama_x(cabeca, (-1.0, 33.5), (2.0, 30.6), 3.0, 0.4, 0.01, "nuca_2")
    chama_z(cabeca, (0, 33.5), (0, 41.6), 4.0, 0.0, -0.3, -1, "nuca_tras", borda=False)


def espelho_x(arte):
    """Para planos em x (face east), a coluna 0 é a traseira; desenho em 'frente à esquerda' -> inverte."""
    return arte.espelho()


# ---------------------------------------- crista / juba ----------------------------------------
def aparar(a):
    """Corta linhas/colunas vazias da arte; devolve (arte, coluna inicial, linha inicial)."""
    cols = [i for i in range(a.w) if any(a.g[j][i] for j in range(a.h))]
    lins = [j for j in range(a.h) if any(a.g[j][i] for i in range(a.w))]
    i0, i1, j0, j1 = min(cols), max(cols) + 1, min(lins), max(lins) + 1
    b = Arte(i1 - i0, j1 - j0)
    b.g = [l[i0:i1] for l in a.g[j0:j1]]
    return b, i0, j0


def chama_z(o, raiz, ponta, larg, curva, z, lado, nome, borda=True):
    """Chama num plano em z. raiz/ponta em (x, y) do mundo, para o lado direito; o esquerdo sai espelhado."""
    m = larg / 2 + 1 + abs(curva)
    x0, x1 = math.floor(min(raiz[0], ponta[0]) - m), math.ceil(max(raiz[0], ponta[0]) + m)
    y0, y1 = math.floor(min(raiz[1], ponta[1]) - m), math.ceil(max(raiz[1], ponta[1]) + m)
    a = chama(Arte(x1 - x0, y1 - y0), (raiz[0] - x0, y1 - raiz[1]), (ponta[0] - x0, y1 - ponta[1]), larg, curva,
              borda=borda)
    a, i0, j0 = aparar(a)
    ox, oy = x0 + i0, y1 - j0 - a.h
    if lado > 0:
        ox, a = -(ox + a.w), a.espelho()
    return plano(o, (ox, oy, z), (a.w, a.h, 0), plana(a), nome=nome)


def chama_x(o, raiz, ponta, larg, curva, x, nome, borda=True, par=None):
    """Chama num plano em x (de perfil). raiz/ponta em (z, y) do mundo; coluna 0 da arte = trás."""
    m = larg / 2 + 1 + abs(curva)
    z0, z1 = math.floor(min(raiz[0], ponta[0]) - m), math.ceil(max(raiz[0], ponta[0]) + m)
    y0, y1 = math.floor(min(raiz[1], ponta[1]) - m), math.ceil(max(raiz[1], ponta[1]) + m)
    a = chama(Arte(z1 - z0, y1 - y0), (z1 - raiz[0], y1 - raiz[1]), (z1 - ponta[0], y1 - ponta[1]), larg, curva,
              borda=borda)
    a, i0, j0 = aparar(a)
    return plano(o, (x, y1 - j0 - a.h, z1 - i0 - a.w), (0, a.h, a.w), plana(a), par=par, nome=nome)


PENA_U = [            # 5 x 8, x -5,5 -> -0,5, y 45,5 -> 37,5: "(" que sobe, abre para fora e curva a ponta para dentro
    "...L.",
    "..LC.",
    ".CC..",
    "CCB..",
    "CB...",
    "BB...",
    "SBB..",
    ".SBS.",
]
PENA_CENTRAL = [      # 3 x 5, y 42,5 -> 37,5
    ".L.",
    ".C.",
    "CCC",
    "BCB",
    "SBS",
]
LEG_CHAMA = {"L": ("verm", LUZ), "C": ("verm", CLARO), "B": ("verm", BASE), "S": ("verm", SOMBRA),
             "F": ("verm", FUNDA)}


def pixel_z(o, linhas, x0, y0, z, lado, nome):
    """Plano em z desenhado à mão (lado direito, coluna 0 = fora); o lado esquerdo sai espelhado."""
    a = Arte(len(linhas[0]), len(linhas)).mapa(linhas, LEG_CHAMA)
    if lado > 0:
        x0, a = -(x0 + a.w), a.espelho()
    return plano(o, (x0, y0, z), (a.w, a.h, 0), plana(a), nome=nome)


def montar_crista(cabeca):
    crista = osso("crista", cabeca, (0, 38.5, -2))
    # de frente: pena central atrás da gema (ponta em y 42,5)
    pixel_z(crista, PENA_CENTRAL, -1.5, 37.5, -4.5, -1, "crista_central")
    # de perfil (planos em x, sem giro): lâminas varridas para trás, medidas na vista lateral da ficha
    chama_x(crista, (-1.0, 38.0), (11.7, 36.6), 4.4, 1.2, 0, "crista_lamina_1")
    chama_x(crista, (-2.0, 39.5), (8.4, 43.3), 4.2, 1.0, 0.01, "crista_lamina_2")
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        chama_x(crista, (-3.0, 38.5), (2.3, 45.0), 3.6, 0.8, 2.6 * lado, f"crista_{s}_lamina_alta", par="lamina_alta")
        chama_x(crista, (-5.2, 38.5), (-3.0, 42.7), 2.6, -0.6, 1.4 * lado, f"crista_{s}_lamina_testa", par="lamina_testa")
        # de frente, num setor virado 15°: pena em U (ponta para dentro) e chamas
        setor = osso(f"crista_{s}", crista, (2.5 * lado, 38.5, -2), (0, 15 * -lado, 0))
        pixel_z(setor, PENA_U, -5.5, 37.5, -2.5, lado, f"crista_{s}_u")
        chama_z(setor, (-3.0, 38.0), (-6.9, 41.4), 3.2, 0.8, -1.5, lado, f"crista_{s}_chama_1")
        chama_z(setor, (-3.2, 36.0), (-8.0, 36.9), 3.2, 0.5, -1.0, lado, f"crista_{s}_chama_3")
        # tufos da bochecha, num setor virado 30°
        boch = osso(f"bochecha_{s}", cabeca, (3.5 * lado, 33, -4), (0, 30 * -lado, 0))
        chama_z(boch, (-3.0, 34.0), (-6.6, 32.1), 3.0, -0.5, -4.0, lado, f"bochecha_{s}_1")
        chama_z(boch, (-2.8, 32.5), (-4.6, 30.3), 2.6, -0.4, -4.5, lado, f"bochecha_{s}_2")
        chama_z(boch, (-2.6, 31.5), (-5.6, 29.6), 2.4, -0.3, -3.0, lado, f"bochecha_{s}_3")


# ---------------------------------------- capa (asas) ----------------------------------------
# Cada lado tem 3 setores (frente, lado, trás), cada um com 3 camadas de penas em leque, da mais funda (vermelha
# comprida) à de cima (roxa curta com filete prata). O ângulo de cada setor vem do osso, não dos cubos.
#            pivô (lado direito)   rotação          largura, raiz da arte, ângulos, comprimentos por camada
SETORES = {
    "frente": ((-4.5, 27, -5.5), (15, 30, 0), 15, (14.0, -2.0), (9, 42),
               ([28.5, 26, 21], [23, 21.5], [16.5])),
    "lado":   ((-9.0, 27, -4.5), (0, 0, 12.5), 18, (16.5, -2.0), (12, 46),
               ([27, 27.5, 25], [22.5, 21.5], [16.5])),
    "tras":   ((-0.5, 26.5, 2.8), (22.5, -10, 0), 14, (13.0, -2.0), (-2, 34),
               ([30, 27.5, 22.5], [23.5, 22], [16.5])),
}


def montar_capa(corpo):
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        asa = osso(f"asa_{s}", corpo, (5 * lado, 28.5, 0))
        for nome, ((px, py, pz), (rx, ry, rz), W, raiz, angs, comps) in SETORES.items():
            setor = osso(f"asa_{s}_{nome}", asa, (px * -lado, py, pz), (rx, ry * -lado, rz * -lado))
            for k, desloc in ((0, 0.0), (1, 0.5), (2, 1.0)):
                comp = comps[k]
                H = min(int(math.ceil(max(comp) - 2.0 + 0.5)), 28)
                arte = arte_leque(W, H, raiz, angs[0], angs[1], comp, k, filete=nome != "tras")
                if nome == "lado":
                    xc = setor.pivo[0] + lado * desloc
                    plano(setor, (xc, py - H, pz), (0, H, W), plana(arte), par=f"capa_lado_{k}", nome=f"capa_{s}_{nome}_{k}")
                else:
                    zc = pz + (-desloc if nome == "frente" else desloc)     # camada de cima fica por fora
                    x0 = setor.pivo[0] - W if lado < 0 else setor.pivo[0]
                    plano(setor, (x0, py - H, zc), (W, H, 0), plana(arte if lado < 0 else arte.espelho()),
                          nome=f"capa_{s}_{nome}_{k}")


# ---------------------------------------- ombreiras ----------------------------------------
def pintor_ombro(lado, ponta=False):
    """Ombreira: miolo roxo, aro prata (chanfro claro em cima, sombra embaixo), ponta dourada."""
    def f(t):
        x, y, z = t.p
        c = t.c
        o, s = c.origem, c.tam
        dx = (x - o[0]) if lado > 0 else (o[0] + s[0] - x)     # 0 = junto ao pescoço, cresce para fora
        if ponta and dx > s[0] - 2:
            return "ouro", CLARO if t.face == "up" else (SOMBRA if t.face == "down" else BASE)
        if t.face == "down": return "prata", FUNDA
        if t.face == "up":
            aro = z < o[2] + 1 or z > o[2] + s[2] - 1 or dx < 1 or dx > s[0] - 1
            return ("prata", LUZ) if aro else ("roxo", CLARO)
        topo = y > o[1] + s[1] - 1
        baixo = y < o[1] + 1
        if topo: return "prata", CLARO                      # chanfro de cima
        if t.face in ("north", "south", "east", "west"):
            return "roxo", SOMBRA if baixo else BASE          # miolo roxo, borda de baixo mais escura
        return "prata", BASE
    return f


def montar_ombreiras(corpo):
    for lado in (-1, 1):
        s = "d" if lado < 0 else "e"
        o = osso(f"ombro_{s}", corpo, (4.5 * lado, 28, -1.5))
        x0 = -9 if lado < 0 else 4
        caixa(o, (x0, 26.5, -5), (5, 3, 7), pintor_ombro(lado), par="ombro", nome=f"ombro_{s}")
        x1 = -11 if lado < 0 else 5
        caixa(o, (x1, 26, -4.5), (6, 3, 6), pintor_ombro(lado, ponta=True), rot=(0, 0, 20 * -lado), par="ombro_ponta",
              pivo=(5 * lado, 27.5, -1.5), nome=f"ombro_{s}_ponta")


# ---------------------------------------- cauda tripla ----------------------------------------
TRANCAS = {   # nome: (x, y, z da raiz), comprimento do segmento, dobra no 3º segmento, dobra da lâmina, alvo (z, y)
    "a": ((0.0, 25.5, 3.5), 3, -10.0, -30.0, (24.5, 16.5), 0.0),
    "b": ((-1.1, 24.0, 3.5), 4, -5.0, -15.0, (23.5, 4.5), 5.0),
    "c": ((1.1, 23.5, 3.5), 4, -5.0, -10.0, (19.5, 1.5), -5.0),
}
LAMINA = 7


def pintor_tranca(t):
    x, y, z = t.p
    c = t.c
    if t.face in ("north", "south"): return "ouro", SOMBRA
    junta = (z - c.origem[2]) < 1.0
    tom = CLARO if t.face == "up" else SOMBRA if t.face == "down" else BASE
    if junta and t.face not in ("up", "down"): tom = SOMBRA
    if t.face in ("east", "west") and (y - c.origem[1]) > 1.0 and not junta: tom = CLARO
    return "ouro", tom


def montar_cauda(corpo):
    cauda = osso("cauda", corpo, (0, 24.5, 3.5))
    for nome, ((x0, y0, z0), L, b1, b2, alvo, giro) in TRANCAS.items():
        pai = cauda
        for k in range(6):
            zk = z0 + k * L
            rot = (0, 0, 0)
            if k == 0: rot = (-30, giro, 0)      # ajustado por mirar_trancas()
            if k == 3: rot = (b1, 0, 0)
            seg = osso(f"cauda_{nome}_{k}", pai, (x0, y0, zk), rot)
            caixa(seg, (x0 - 1, y0 - 1, zk), (2, 2, L), pintor_tranca,
                  rot=(0, 0, 45) if k % 2 else None, pivo=(x0, y0, zk + L / 2), par=f"tranca_{L}",
                  nome=f"tranca_{nome}_{k}")
            pai = seg
        zf = z0 + 6 * L
        lam = osso(f"lamina_{nome}", pai, (x0, y0, zf), (b2, 0, 0))
        # lâmina em cruz: plano em x (de perfil) e plano em y (de cima/de trás); o losango é um furo nos dois,
        # preenchido por planos próprios no osso de brilho
        px_ = Arte(LAMINA, 5).mapa(LAMINA_X, LEG_LAMINA)      # coluna 0 = ponta (trás), última = raiz
        py_ = Arte(4, LAMINA).mapa(LAMINA_Y, LEG_LAMINA)      # linha 0 = raiz (frente), 5 = ponta
        plano(lam, (x0, y0 - 2.5, zf - 0.5), (0, 5, LAMINA), plana(px_.copia(sem="P")), par="lamina_x", nome=f"lamina_{nome}_x")
        plano(lam, (x0 - 2, y0, zf - 0.5), (4, 0, LAMINA), plana(py_.copia(sem="P")), par="lamina_y", nome=f"lamina_{nome}_y")
        bri = osso(f"losango_{nome}_brilho", lam, (x0, y0, zf + 2.5))
        plano(bri, (x0 + 0.01, y0 - 2.5, zf - 0.5), (0, 5, LAMINA), plana(px_.copia(so="P")), par="losango_x", nome=f"losango_{nome}_x")
        plano(bri, (x0 - 2, y0 + 0.01, zf - 0.5), (4, 0, LAMINA), plana(py_.copia(so="P")), par="losango_y", nome=f"losango_{nome}_y")


# lâmina dourada (6 x 5 de perfil; 4 x 6 de cima). O = ouro, o = ouro sombra, l = ouro luz, P/p/Q = losango
LAMINA_X = [
    "..lll..",
    ".lOPOO.",
    "lOPpPOO",
    ".OOQOo.",
    "..ooo..",
]
LAMINA_Y = [         # simétrica nos dois eixos: a orientação da UV da face "up" não muda o desenho
    ".OO.",
    "OOOO",
    "oPPo",
    "oQQo",
    "oPPo",
    "OOOO",
    ".OO.",
]
LEG_LAMINA = {"O": ("ouro", BASE, "O"), "o": ("ouro", SOMBRA, "O"), "l": ("ouro", CLARO, "O"),
              "P": ("rubi", CLARO, "P"), "p": ("rubi", BASE, "P"), "Q": ("rubi", SOMBRA, "P")}


def mirar_trancas():
    """Escolhe a inclinação da raiz e as duas dobras (3º segmento e lâmina) de cada trança para a ponta cair no
    alvo da ficha (z, y), preferindo dobras pequenas."""
    for nome, ((x0, y0, z0), L, b1, b2, alvo, giro) in TRANCAS.items():
        melhor = None
        r0, r3, rl = POR_NOME[f"cauda_{nome}_0"], POR_NOME[f"cauda_{nome}_3"], POR_NOME[f"lamina_{nome}"]
        for d1 in np.arange(0, -22.5, -2.5):
            for d2 in np.arange(-5, -45, -5):
                for rx in np.arange(-80, 5, 2.5):
                    r0.rot[0], r3.rot[0], rl.rot[0] = float(rx), float(d1), float(d2)
                    p = mundo(f"lamina_{nome}", (x0, y0, z0 + 6 * L + LAMINA - 0.5))
                    err = math.hypot(p[2] - alvo[0], p[1] - alvo[1]) + 0.01 * (abs(d1) + abs(d2))
                    if p[1] < 0.5:
                        err += 10
                    if melhor is None or err < melhor[0]:
                        melhor = (err, rx, d1, d2, p)
        err, rx, d1, d2, p = melhor
        r0.rot[0], r3.rot[0], rl.rot[0] = float(rx), float(d1), float(d2)
        print(f"  trança {nome}: raiz {rx:.1f}°, dobras {d1:.1f}°/{d2:.1f}°, ponta (z={p[2]:.1f}, y={p[1]:.1f}),"
              f" alvo {alvo}")


# ---------------------------------------- pernas ----------------------------------------
def pintor_pe(t):
    x, y, z = t.p
    tom = faixa(t)
    if t.face in ("east", "west", "north", "south") and (int(math.floor(z)) + int(math.floor(y))) % 2 == 0:
        tom = min(FUNDA, tom + 1)   # escamas
    return "roxoe", tom


def pintor_garra(t):
    x, y, z = t.p
    if t.face == "up": return "ouro", LUZ
    if t.face == "down": return "ouro", SOMBRA
    return "ouro", CLARO if (y - t.c.origem[1]) >= 1 else BASE


def pintor_canela(t):
    return "roxo", faixa(t)


def pintor_metal(t):
    x, y, z = t.p
    c = t.c
    if t.face == "up": return "prata", LUZ
    if t.face == "down": return "prata", FUNDA
    if y > c.origem[1] + c.tam[1] - 1: return "prata", CLARO
    return "prata", SOMBRA if (y - c.origem[1]) < 0.9 else BASE


def montar_perna(raiz, lado):
    s = "d" if lado < 0 else "e"
    cx = 2.6 * lado
    perna = osso(f"perna_{s}", raiz, (cx, 15, 0))
    caixa(perna, (cx - 2, 10, -3), (4, 6, 4), liso("verm"), par="coxa", nome=f"coxa_{s}")
    # saia de penas vermelhas: frente, fora e trás
    saia_f = Arte(5, 6)
    for r0, p0 in (((1.2, 0), (1.3, 5.9)), ((3.6, 0), (3.6, 5.9)), ((2.4, 0), (2.5, 5.0))):
        saia_f.pena(r0, p0, 2.6, cores=rampa_t("verm", (SOMBRA, BASE, BASE, CLARO)), perfil="pena")
    saia_l = Arte(5, 6)
    for r0, p0 in (((1.2, 0), (0.8, 5.9)), ((3.6, 0), (3.2, 5.9))):
        saia_l.pena(r0, p0, 2.8, cores=rampa_t("verm", (SOMBRA, BASE, BASE, CLARO)), perfil="pena")
    plano(perna, (cx - 2.5, 9.5, -3.15), (5, 6, 0), plana(saia_f if lado < 0 else saia_f.espelho()), nome=f"saia_{s}_f")
    plano(perna, (cx + 2.15 * lado, 9.5, -3.4), (0, 6, 5), plana(saia_l), par="saia_l", nome=f"saia_{s}_l")
    plano(perna, (cx - 2.5, 9.5, 1.15), (5, 6, 0), plana(saia_f), par="saia_t", nome=f"saia_{s}_t")
    caixa(perna, (cx - 1.5, 8.5, -2.5), (3, 2, 3), pintor_metal, par="metal_perna", nome=f"joelheira_{s}")
    ponta = Arte(3, 3).mapa([".L.", "SLS", "BSB"], {"L": ("prata", LUZ), "S": ("prata", BASE),
                                                  "B": ("prata", SOMBRA)})
    plano(perna, (cx - 1.5, 8.5, -2.53), (3, 3, 0), plana(ponta), par="ponta_perna", nome=f"joelheira_{s}_ponta")
    caixa(perna, (cx - 1, 3, -2), (2, 6, 2), pintor_canela, par="canela", nome=f"canela_{s}")
    caixa(perna, (cx - 1.5, 3.5, -2.5), (3, 2, 3), pintor_metal, par="metal_perna", nome=f"tornozeleira_{s}")
    plano(perna, (cx - 1.5, 3.5, -2.53), (3, 3, 0), plana(ponta), par="ponta_perna", nome=f"tornozeleira_{s}_ponta")
    pe = osso(f"pe_{s}", perna, (cx, 3.5, -1))
    caixa(pe, (cx - 1.5, 0, -2.5), (3, 3, 3), pintor_pe, par="pe", nome=f"pe_{s}")
    for k, giro in enumerate((0, 25, -25)):
        dedo = osso(f"dedo_{s}_{k}", pe, (cx, 0.5, -2.5), (0, giro * -lado if k else 0, 0))
        caixa(dedo, (cx - 0.5, 0, -6.5), (1, 1, 4), pintor_pe, par="dedo", nome=f"dedo_{s}_{k}")
        caixa(dedo, (cx - 0.5, 0, -8.5), (1, 2, 2), pintor_garra, par="garra", nome=f"garra_{s}_{k}")
    caixa(pe, (cx - 0.5, 0, 0.5), (1, 1, 1), pintor_garra, par="garra_tras", nome=f"garra_{s}_tras")


# ======================================================================================================
# Animações (Molang, laço sem emenda)
# ======================================================================================================
def S(k, fase, amp, L=4):
    """math.sin com k ondas por laço de L segundos."""
    w = round(360 / L * k)
    f = f"+{fase}" if fase > 0 else (f"{fase}" if fase < 0 else "")
    return f"math.sin(query.anim_time*{w}{f})*{amp}"


def L(k, fase, amp, L=4):
    """Onda que só levanta (0 -> amp): a trança nunca desce abaixo da pose e não atravessa o chão."""
    return f"({S(k, fase, 0.5, L)}+0.5)*{amp}"


def animacoes():
    idle, walk = {}, {}
    # ---------------- idle (L = 4) ----------------
    idle["corpo"] = {"rotation": [S(2, 0, 1.5), 0, 0], "position": [0, S(2, -90, 0.2), 0]}
    idle["pescoco"] = {"rotation": [S(2, -40, -1.0), 0, 0]}
    idle["cabeca"] = {"rotation": [S(2, -60, 2), S(1, 0, 3), 0]}
    idle["crista"] = {"rotation": [S(2, -120, 4), 0, S(1, -60, 2)]}
    for s, sg in (("d", 1), ("e", -1)):
        idle[f"asa_{s}"] = {"rotation": [S(2, -60, 1), 0, S(2, -90, 2 * sg)]}
        idle[f"crista_{s}"] = {"rotation": [0, S(2, -150, 3 * sg), 0]}
        idle[f"bochecha_{s}"] = {"rotation": [0, S(2, -100, 3 * sg), 0]}
    for nome in TRANCAS:
        for k in range(6):
            # A (alta) ondula para os dois lados; B e C, que pendem perto do chão, só levantam
            # fases escolhidas para o 1º quadro ficar na pose da ficha (soma das juntas ~0 em t = 0)
            onda_x = S(2, 75 - 30 * k, round(4 + 0.6 * k, 1)) if nome == "a" else L(2, -15 - 30 * k, round(2.5 + 0.5 * k, 1))
            idle[f"cauda_{nome}_{k}"] = {"rotation": [onda_x, 0, S(1, -30 * k, round(2 + 0.4 * k, 1))]}
        idle[f"lamina_{nome}"] = {"rotation": [S(2, -105, 8) if nome == "a" else L(2, -195, 6), 0, S(1, -180, 5)]}
    for s, sg in (("d", -1), ("e", 1)):
        z = [0, 0, 0]
        f = [round(0.12 * sg, 2), 0, -0.12]
        idle[f"palpebra_{s}"] = {"position": {"0.0": z, "3.7": z, "3.72": f, "3.84": f, "3.86": z, "4.0": z}}
    # ---------------- walk (L = 2) ----------------
    W = lambda k, fase, amp: S(k, fase, amp, L=2)
    walk["perna_d"] = {"rotation": [W(1, 0, 25), 0, 0]}
    walk["perna_e"] = {"rotation": [W(1, 180, 25), 0, 0]}
    walk["pe_d"] = {"rotation": [W(1, 0, -25), 0, 0]}
    walk["pe_e"] = {"rotation": [W(1, 180, -25), 0, 0]}
    walk["corpo"] = {"rotation": [W(2, 0, 1.5), W(1, 0, 2), W(1, 0, 3)],
                     "position": [0, f"{W(2, 90, 0.2)}+0.2", 0]}
    walk["cabeca"] = {"rotation": [W(2, -60, -1.5), W(1, 0, -1.5), W(1, 0, -2.5)]}
    walk["crista"] = {"rotation": [W(2, -120, 4), 0, W(1, -60, 2)]}
    for s, sg in (("d", 1), ("e", -1)):
        walk[f"asa_{s}"] = {"rotation": [W(2, -60, 2), 0, W(1, -60, 3)]}
        walk[f"crista_{s}"] = {"rotation": [0, W(2, -150, 4 * sg), 0]}
    for nome in TRANCAS:
        for k in range(6):
            onda_x = (W(2, -40 * k - 40, round(5 + 1.0 * k, 1)) if nome == "a"
                      else L(2, -40 * k - 40, round(3.5 + 0.7 * k, 1), L=2))
            walk[f"cauda_{nome}_{k}"] = {"rotation": [onda_x, 0, W(1, -40 * k, round(3 + 0.6 * k, 1))]}
        walk[f"lamina_{nome}"] = {"rotation": [W(2, -280, 12) if nome == "a" else L(2, -280, 9, L=2), 0,
                                               W(1, -240, 8)]}
    return {
        "format_version": "1.8.0",
        "animations": {
            f"animation.{ID}.idle": {"loop": True, "animation_length": 4, "bones": idle},
            f"animation.{ID}.walk": {"loop": True, "animation_length": 2, "bones": walk},
        },
    }


def quadro(anim, nome, t):
    """Valores de uma animação no instante t (para conferir com o renderizador, que usa o 1º quadro)."""
    def val(x):
        if isinstance(x, (int, float)):
            return float(x)
        return rg.molang(str(x).replace("query.anim_time", f"({t})"))

    def canal(c):
        if isinstance(c, dict):
            ks = sorted(c, key=float)
            ant = [k for k in ks if float(k) <= t + 1e-9]
            k = ant[-1] if ant else ks[0]
            nx = [k2 for k2 in ks if float(k2) > t + 1e-9]
            a = [val(v) for v in c[k]]
            if nx:
                b = [val(v) for v in c[nx[0]]]
                f = (t - float(k)) / (float(nx[0]) - float(k))
                return [x + (y - x) * f for x, y in zip(a, b)]
            return a
        return [val(v) for v in c]
    bones = anim["animations"][nome]["bones"]
    return {b: {k: canal(v) for k, v in d.items()} for b, d in bones.items()}


# ======================================================================================================
# Exportação
# ======================================================================================================
def empacotar(cubos):
    """Empacota as ilhas sem sobreposição (skyline: cada ilha vai no ponto mais alto e à esquerda que couber)."""
    donos = [c for c in cubos if c.de is None]
    ordem = sorted(donos, key=lambda c: (-ilha(c)[1], -ilha(c)[0]))
    for W, H in ((128, 128), (256, 128), (256, 256)):
        ceu = [0] * W
        pos = {}
        for c in ordem:
            w, h = ilha(c)
            melhor = None
            for x in range(0, W - w + 1):
                y = max(ceu[x:x + w])
                if y + h <= H and (melhor is None or y < melhor[1]):
                    melhor = (x, y)
            if melhor is None:
                break
            x, y = melhor
            pos[id(c)] = melhor
            for i in range(x, x + w):
                ceu[i] = y + h
        if len(pos) == len(ordem):
            for c in donos:
                c.uv = pos[id(c)]
            for c in cubos:
                if c.de is not None:
                    c.uv = c.de.uv
            return W, H
    raise SystemExit("a textura não coube em 256x256")


def r4(v):
    v = round(float(v), 4)
    return int(v) if v == int(v) else v


def cubo_json(c):
    d = {"origin": [r4(v) for v in c.origem], "size": list(c.tam)}
    if c.inflate:
        d["inflate"] = c.inflate
    if c.rot:
        d["pivot"] = [r4(v) for v in c.pivo]
        d["rotation"] = [r4(v) for v in c.rot]
    if c.plano:
        w, h = ilha(c)
        d["uv"] = {c.plano: {"uv": list(c.uv), "uv_size": [w, h]}}
    else:
        d["uv"] = list(c.uv)
        if c.espelho:
            d["mirror"] = True
    return d


def geo_json(W, H):
    bones = []
    for o in OSSOS:
        b = {"name": o.nome}
        if o.pai:
            b["parent"] = o.pai
        b["pivot"] = [r4(v) for v in o.pivo]
        if any(abs(v) > 1e-9 for v in o.rot):
            b["rotation"] = [r4(v) for v in o.rot]
        if o.cubos:
            b["cubes"] = [cubo_json(c) for c in o.cubos]
        bones.append(b)
    return {
        "format_version": "1.12.0",
        "minecraft:geometry": [{
            "description": {"identifier": f"geometry.{ID}", "texture_width": W, "texture_height": H,
                            "visible_bounds_width": 4, "visible_bounds_height": 4,
                            "visible_bounds_offset": [0, 1.5, 0]},
            "bones": bones,
        }],
    }


def glowmask(tex, cubos):
    m = np.zeros_like(tex)
    for c in cubos:
        if "_brilho" not in c.osso.nome:
            continue
        for face, (u1, v1, u2, v2) in faces_uv(c).items():
            ys, xs = slice(min(v1, v2), max(v1, v2)), slice(min(u1, u2), max(u1, u2))
            m[ys, xs] = tex[ys, xs]
    return m


# ======================================================================================================
# Validações
# ======================================================================================================
def validar(geo, anim, W, H, png):
    cubos = [c for o in OSSOS for c in o.cubos]
    erros, avisos = [], []
    for c in cubos:
        if any(v != int(v) for v in c.tam):
            erros.append(f"{c.nome}: tamanho fracionado")
        if any(0 < v < 1 for v in c.tam):
            erros.append(f"{c.nome}: espessura entre 0 e 1")
        if c.inflate and not (0.01 <= c.inflate <= 0.04):
            erros.append(f"{c.nome}: inflate {c.inflate} fora de 0,01-0,04")
    for b in geo["minecraft:geometry"][0]["bones"]:
        for c in b.get("cubes", []):
            if isinstance(c["uv"], dict):
                if len(c["uv"]) != 1:
                    erros.append(f"{b['name']}: plano com {len(c['uv'])} faces")
                face, f = next(iter(c["uv"].items()))
                s = c["size"]
                esperado = {"north": (s[0], s[1]), "east": (s[2], s[1]), "up": (s[0], s[2])}[face]
                if tuple(f["uv_size"]) != esperado:
                    erros.append(f"{b['name']}: uv_size {f['uv_size']} != face {esperado}")
                if 0 not in s or {"north": 2, "east": 0, "up": 1}[face] != s.index(0):
                    erros.append(f"{b['name']}: face {face} não bate com o eixo zero {s}")
    # ilhas sem sobreposição
    ocup = np.zeros((H, W), np.int32)
    for c in cubos:
        if c.de is not None:
            continue
        w, h = ilha(c)
        u, v = c.uv
        if u + w > W or v + h > H:
            erros.append(f"{c.nome}: ilha fora da textura")
            continue
        ocup[v:v + h, u:u + w] += 1
    if (ocup > 1).any():
        erros.append(f"ilhas sobrepostas em {(ocup > 1).sum()} px")
    im = Image.open(png)
    if im.size != (W, H):
        erros.append(f"PNG {im.size} != declarado {(W, H)}")
    if W & (W - 1) or H & (H - 1):
        erros.append("textura não é potência de 2")
    # altura (só pixels opacos)
    faces = rg.faces_do_modelo(geo, rg.carregar_animacao(None, None))
    tex = np.asarray(im.convert("RGBA"))
    ys = []
    for pts, (u1, v1, u2, v2), _ in faces:
        p0, p1, p2 = (np.array(p) for p in pts)
        for a in np.linspace(0.02, 0.98, 8):
            for b in np.linspace(0.02, 0.98, 8):
                tu = int(min(u1, u2) + a * abs(u2 - u1)) if u2 >= u1 else int(u1 - a * (u1 - u2))
                tv = int(min(v1, v2) + b * abs(v2 - v1)) if v2 >= v1 else int(v1 - b * (v1 - v2))
                uu = (tu + .5 - u1) / (u2 - u1)
                vv = (tv + .5 - v1) / (v2 - v1)
                if 0 <= tv < H and 0 <= tu < W and tex[tv, tu, 3] > 0:
                    ys.append((p0 + uu * (p1 - p0) + vv * (p2 - p0))[1])
    alt = max(ys) - min(ys)
    if abs(max(ys) - ALTURA) > 0.75 or min(ys) < -0.3:
        erros.append(f"altura {min(ys):.2f} -> {max(ys):.2f} (alvo 0 -> {ALTURA})")
    for an, L_ in ((f"animation.{ID}.idle", 4), (f"animation.{ID}.walk", 2)):
        piso = min(min_y(geo, tex, quadro(anim, an, t)) for t in np.linspace(0, L_, 17)[:-1])
        if piso < -0.3:
            erros.append(f"{an}: algo desce até y = {piso:.2f} (abaixo do chão)")
        else:
            print(f"  {an}: ponto mais baixo no laço y = {piso:.2f}")
    n = len(cubos)
    planos = sum(1 for c in cubos if c.plano)
    girados = sum(1 for c in cubos if c.rot)
    if not (ORCAMENTO[0] <= n <= ORCAMENTO[1]):
        avisos.append(f"{n} cubos fora do orçamento {ORCAMENTO}")
    if n > 200:
        erros.append("passou do teto de 200 cubos")
    nomes = {o.nome for o in OSSOS}
    for an, d in anim["animations"].items():
        if not d.get("loop"):
            erros.append(f"{an} não está em laço")
        for b in d["bones"]:
            if b not in nomes:
                erros.append(f"{an}: osso '{b}' não existe")
    for nome in (f"animation.{ID}.idle", f"animation.{ID}.walk"):
        if nome not in anim["animations"]:
            erros.append(f"falta {nome}")
    cores = {tuple(p) for p in tex.reshape(-1, 4) if p[3] > 0}
    print(f"  cubos: {n} ({planos} planos = {100 * planos / n:.0f}%), girados (cubo): {girados}"
          f" = {100 * girados / n:.0f}%, ossos: {len(OSSOS)} ({sum(1 for o in OSSOS if any(o.rot))} com rotação)")
    print(f"  textura {W}x{H}, {len(cores)} cores; altura visível {min(ys):.2f} -> {max(ys):.2f} u")
    for a in avisos:
        print("  AVISO:", a)
    for e in erros:
        print("  ERRO:", e)
    print("  validação:", "OK" if not erros else f"{len(erros)} erro(s)")
    return not erros


def min_y(geo, tex, anim):
    """Menor y dos pixels opacos numa pose."""
    H, W = tex.shape[:2]
    m = np.inf
    for pts, (u1, v1, u2, v2), _ in rg.faces_do_modelo(geo, anim):
        p0, p1, p2 = (np.array(p) for p in pts)
        for a in (0.05, 0.5, 0.95):
            for b in (0.05, 0.5, 0.95):
                tu = min(max(int(math.floor(u1 + a * (u2 - u1))), 0), W - 1)
                tv = min(max(int(math.floor(v1 + b * (v2 - v1))), 0), H - 1)
                if tex[tv, tu, 3] > 0:
                    m = min(m, (p0 + a * (p1 - p0) + b * (p2 - p0))[1])
    return m


# ======================================================================================================
# Imagens de conferência
# ======================================================================================================
FUNDO = (235, 235, 230)
VISTAS_FICHA = {"frente": (645, 61, 826, 336), "direita": (850, 59, 1074, 336), "tras": (1091, 60, 1277, 336),
                "esquerda": (1323, 58, 1524, 336)}


def recortar(im):
    a = np.asarray(im.convert("RGB")).astype(int)
    m = np.abs(a - np.array(FUNDO)).sum(axis=2) > 12
    ys, xs = np.where(m)
    return im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def fonte(t=13):
    try:
        return ImageFont.truetype("DejaVuSans.ttf", t)
    except OSError:
        return ImageFont.load_default()


def imagens(geo, tex, anim, pasta):
    faces = rg.faces_do_modelo(geo, rg.carregar_animacao(str(pasta / f"{ID}.animation.json"), f"animation.{ID}.idle"))
    rg.folha(str(pasta / f"{ID}.geo.json"), str(pasta / f"{ID}.png"), str(pasta / f"{ID}_vistas.png"),
             str(pasta / f"{ID}.animation.json"), f"animation.{ID}.idle", 8)
    # comparação: ficha x render na mesma altura
    ficha = Image.open(FICHA).convert("RGB")
    alt = 360
    pares = [("frente", 0, False), ("direita", 270, False), ("tras", 180, False), ("esquerda", 90, True)]
    blocos = []
    for nome, yaw, inverter in pares:
        f = ficha.crop(VISTAS_FICHA[nome])
        f = f.resize((round(f.width * alt / f.height), alt), Image.LANCZOS)
        r = recortar(rg.desenhar(faces, tex, yaw, 0, 10))
        if inverter:
            r = r.transpose(Image.FLIP_LEFT_RIGHT)
        r = r.resize((round(r.width * alt / r.height), alt), Image.NEAREST)
        blocos.append((nome, f, r))
    W = sum(f.width + r.width + 30 for _, f, r in blocos) + 10
    out = Image.new("RGB", (W, alt + 40), (255, 255, 255))
    d = ImageDraw.Draw(out)
    x = 10
    for nome, f, r in blocos:
        out.paste(f, (x, 30))
        bg = Image.new("RGB", r.size, FUNDO)
        bg.paste(r, (0, 0))
        out.paste(bg, (x + f.width + 6, 30))
        d.text((x, 8), f"{nome}: ficha | modelo" + (" (espelhado)" if nome == "esquerda" else ""), fill=(30, 30, 30),
               font=fonte())
        x += f.width + r.width + 30
    out.save(pasta / f"{ID}_comparacao.png")
    # rosto: só a cabeça (e o que pende dela), de frente e em 3/4
    so_cabeca = copy.deepcopy(geo)
    filhos_cab = set()
    pai = {b["name"]: b.get("parent") for b in geo["minecraft:geometry"][0]["bones"]}
    for b in pai:
        o = b
        while o:
            if o == "cabeca":
                filhos_cab.add(b)
                break
            o = pai[o]
    for b in so_cabeca["minecraft:geometry"][0]["bones"]:
        if b["name"] not in filhos_cab:
            b.pop("cubes", None)
    fc = rg.faces_do_modelo(so_cabeca, rg.carregar_animacao(str(pasta / f"{ID}.animation.json"), f"animation.{ID}.idle"))
    imgs = [recortar(rg.desenhar(fc, tex, y, p, 28)) for y, p in ((0, 0), (35, -12), (270, 0))]
    H = max(i.height for i in imgs) + 20
    out = Image.new("RGB", (sum(i.width for i in imgs) + 20 * (len(imgs) + 1), H + 20), FUNDO)
    x = 20
    for i in imgs:
        out.paste(i, (x, 20))
        x += i.width + 20
    out.save(pasta / f"{ID}_rosto.png")
    # andar: quadros t = 0,5 e 1,5 do walk, de lado e de frente
    qs = []
    for t in (0.5, 1.5):
        fa = rg.faces_do_modelo(geo, quadro(anim, f"animation.{ID}.walk", t))
        for yaw in (270, 0):
            qs.append((recortar(rg.desenhar(fa, tex, yaw, 0, 6)), f"walk t={t}"))
    H = max(i.height for i, _ in qs) + 30
    out = Image.new("RGB", (sum(i.width + 20 for i, _ in qs) + 20, H), FUNDO)
    d = ImageDraw.Draw(out)
    x = 20
    for i, n in qs:
        out.paste(i, (x, 25))
        d.text((x, 5), n, fill=(30, 30, 30), font=fonte())
        x += i.width + 20
    out.save(pasta / f"{ID}_andar.png")


# ======================================================================================================
def gerar(pasta=AQUI, instalar=False, conferir=True):
    OSSOS.clear()
    POR_NOME.clear()
    PARES.clear()
    montar()
    mirar_trancas()
    cubos = [c for o in OSSOS for c in o.cubos]
    W, H = empacotar(cubos)
    tex = pintar_textura(cubos, W, H)
    Image.fromarray(tex, "RGBA").save(pasta / f"{ID}.png")
    Image.fromarray(glowmask(tex, cubos), "RGBA").save(pasta / f"{ID}_glowmask.png")
    geo = geo_json(W, H)
    (pasta / f"{ID}.geo.json").write_text(json.dumps(geo, indent=1, ensure_ascii=False), encoding="utf-8")
    anim = animacoes()
    (pasta / f"{ID}.animation.json").write_text(json.dumps(anim, indent=1, ensure_ascii=False), encoding="utf-8")
    ok = validar(geo, anim, W, H, pasta / f"{ID}.png")
    if conferir:
        imagens(geo, tex.astype(np.float32), anim, pasta)
    if instalar:
        shutil.copyfile(pasta / f"{ID}.geo.json", ASSETS / f"geckolib/models/entity/{ID}.geo.json")
        shutil.copyfile(pasta / f"{ID}.animation.json", ASSETS / f"geckolib/animations/entity/{ID}.animation.json")
        shutil.copyfile(pasta / f"{ID}.png", ASSETS / f"textures/entity/{ID}.png")
        shutil.copyfile(pasta / f"{ID}_glowmask.png", ASSETS / f"textures/entity/{ID}_glowmask.png")
        print("  instalado em", ASSETS)
    return ok


if __name__ == "__main__":
    sys.exit(0 if gerar(instalar="--instalar" in sys.argv, conferir="--sem-imagens" not in sys.argv) else 1)
