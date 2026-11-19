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
ORCAMENTO = (110, 190)  # cubos (teto 200; até 190 na correção 2)

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
    for _ in range(max(1, round(len(pix) * 0.025))):
        x, y = rnd.choice(pix)
        d = rnd.choice((-1, 1))
        m0 = area[(x, y)][0]
        for _ in range(rnd.choice((1, 2, 2, 3))):
            v = area.get((x, y))
            if v and v[2] and v[0] == m0 and v[1] <= BASE:
                area[(x, y)] = (v[0], max(LUZ, min(BASE, v[1] + d)), True)          # nunca abaixo da base
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


def rampa_t(mat, tons=(SOMBRA, BASE, CLARO, LUZ), cortes=(0.22, 0.55, 0.85)):
    """Cor ao longo da pena: raiz escura -> ponta clara, em degraus."""
    def f(t):
        k = sum(t >= c for c in cortes)
        return mat, tons[k]
    return f


def _R(eixo, g):
    """Rotação padrão (mão direita) em graus, no espaço do JSON."""
    c, s = math.cos(math.radians(g)), math.sin(math.radians(g))
    if eixo == "x": return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if eixo == "y": return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


ESPELHO = np.diag([-1.0, 1.0, 1.0])


def euler(R):
    """Ângulos Bedrock [rx, ry, rz] de uma matriz de rotação, arredondados a 2,5° (inverso de rot_json)."""
    b = math.degrees(math.asin(max(-1.0, min(1.0, -R[2, 0]))))
    a = math.degrees(math.atan2(R[2, 1], R[2, 2]))
    c = math.degrees(math.atan2(R[1, 0], R[0, 0]))
    q = lambda v: round(v / 2.5) * 2.5 + 0.0
    return [q(-a), q(b), q(-c)]


def lado_nome(lado):
    return "d" if lado < 0 else "e"


def arte_mapa(linhas, legenda=None, espelhar=False):
    a = Arte(len(linhas[0]), len(linhas)).mapa(linhas, legenda or LEG_CHAMA)
    return a.espelho() if espelhar else a


LEG_CHAMA = {"L": ("verm", LUZ), "C": ("verm", CLARO), "B": ("verm", BASE), "S": ("verm", SOMBRA),
             "F": ("verm", FUNDA)}
LEG_PRATA = {"L": ("prata", LUZ), "C": ("prata", CLARO), "B": ("prata", BASE), "S": ("prata", SOMBRA),
             "F": ("prata", FUNDA), "O": ("ouro", BASE)}


def pena_reta(W, H, cor, filete=None, haste=None):
    """Pena reta de W px de largura e H de comprimento (linha 0 = raiz), ponta em degrau de 2 px.
    cor(j) -> (material, tom) por linha; filete = (coluna, material, tom); haste = (coluna, desvio de tom)."""
    a = Arte(W, H)
    for j in range(H):
        larg = W if j < H - 2 else max(1, W - 2)
        i0 = (W - larg) // 2
        for i in range(i0, i0 + larg):
            m, tom = cor(j)
            if haste and i == haste[0] and 1 < j < H - 3:
                tom += haste[1]
            if filete and i == filete[0] and 0 < j < H - 2:
                m, tom = filete[1], filete[2]
            a.put(i, j, (m, max(0, min(FUNDA, tom))))
    return a


def deitar(a):
    """Pena vertical (raiz em cima) -> deitada para plano em x apontando para trás (coluna 0 = trás = ponta)."""
    b = Arte(a.h, a.w)
    for j in range(a.w):
        for i in range(a.h):
            b.g[j][i] = a.g[a.h - 1 - i][j]
    return b


# ---------------------------------------- penas largas ----------------------------------------
def pena_larga(W, H, mat, variante=0, larguras=None, curva=0.0, bojo=0.0, filete=False, corte=None):
    """Pena larga em pixel art, linha 0 = raiz, linha H-1 = ponta (em V, degraus de 1 px).
    Metade de fora (colunas baixas) 1 tom mais clara, haste clara, metade de dentro 1 tom mais escura;
    variante 1 é a vizinha mais escura (as telhas se separam). curva/bojo deslocam o centro (px) na ponta/no
    meio, negativo = para a coluna 0. filete: borda de fora em prata #e4dce3. corte = (fração, material)."""
    a = Arte(W, H)
    if larguras is None:
        larguras = [W] * (H - 2) + [max(1, W - 2), 1]
    for j in range(H):
        t = j / max(1, H - 1)
        w = larguras[j]
        c = (W - 1) / 2 + bojo * math.sin(math.pi * t) + curva * t * t
        i0 = max(0, min(W - w, int(round(c - (w - 1) / 2))))
        m = corte[1] if corte and t >= corte[0] else mat
        for i in range(i0, i0 + w):
            rel = i - (i0 + (w - 1) / 2)
            if variante == 0:
                tom = CLARO if rel <= 0 else (BASE if rel < 1.5 else SOMBRA)
            else:
                tom = CLARO if abs(rel) < 0.5 else (SOMBRA if rel > 1.5 else BASE)
            if j >= H - 2:
                tom = LUZ if abs(rel) < 0.5 else CLARO               # ponta: 2 px de luz
            elif j == 0:
                tom = min(FUNDA, tom + 1)                            # raiz, sob a camada de cima
            if filete and i == i0 and w == W and 0 < j < H - 2:
                a.put(i, j, ("prata", CLARO))
                continue
            a.put(i, j, (m, tom))
    return a


def virar(a):
    """Raiz embaixo (penas que sobem)."""
    b = Arte(a.w, a.h)
    b.g = [list(l) for l in reversed(a.g)]
    return b


def pena_z(pai, nome, raiz, arte, rot, sobe=True, par=None):
    """Plano em z com o meio da base em 'raiz'; a rotação fica no osso da pena (pivô na raiz)."""
    x, y, z = raiz
    o = osso(nome, pai, raiz, rot)
    return plano(o, (x - arte.w / 2, y if sobe else y - arte.h, z), (arte.w, arte.h, 0), plana(arte), par=par,
                 nome=nome)


# ---------------------------------------- montagem ----------------------------------------
def montar():
    raiz = osso(ID, None, (0, 0, 0))
    corpo = osso("corpo", raiz, (0, 15, -1))
    montar_tronco(corpo)
    pescoco = osso("pescoco", corpo, (0, 29, -4))
    caixa(pescoco, (-2.5, 28.5, -6.5), (5, 3, 5), pintor_pescoco, nome="pescoco")
    cabeca = osso("cabeca", pescoco, (0, 31.5, -3.5))
    montar_cabeca(cabeca)
    montar_crista(cabeca)
    montar_ombreiras(corpo)
    montar_capa(corpo)
    montar_cauda(corpo)
    for lado in (-1, 1):
        montar_perna(raiz, lado)


# ---------------------------------------- 6. tronco e peito ----------------------------------------
def pintor_nucleo(t):
    x, y, z = t.p
    if t.face == "down": return "verm", SOMBRA
    if t.face == "up": return "verm", BASE
    if t.face == "north" and y >= 27 and abs(x) < 3: return "creme", CLARO       # creme do pescoço descendo
    if t.face in ("east", "west") and 25 <= y < 26: return "verm", FUNDA        # junção sob as ombreiras
    if t.face == "north" and y < 16: return "verm", SOMBRA                        # junção peito/coxas (1 px)
    return "verm", BASE if y > 17 else SOMBRA                                     # corpo: base e sombra


# peito estufado: o degrau de cima é o mais à frente; recua 2 u até o quadril
DEGRAUS = (((-4, 21, -9.5), (8, 6, 3)), ((-3, 17, -8.5), (6, 4, 2)), ((-2, 15, -7.5), (4, 2, 1)))
ZIGUE = (23.5, 18.5)        # y das linhas de chevron em zigue-zague


def pintor_peito(t):
    x, y, z = t.p
    c = t.c
    if t.face == "down": return "creme", SOMBRA
    if t.face == "up": return "creme", LUZ
    if t.face == "north":
        if x < c.origem[0] + 1 or x > c.origem[0] + c.tam[0] - 1:
            return "creme", BASE                                                   # quina vertical
        col = int(math.floor(x - c.origem[0]))
        for yz in ZIGUE:
            if 0 <= y - (yz + abs(col % 4 - 2) - 1) < 1 and abs(x) < c.tam[0] / 2 - 0.5:
                return "creme", SOMBRA                                             # zigue-zague /\/\
        return "creme", CLARO if y >= 22 else BASE
    if z < c.origem[2] + 1: return "creme", BASE                                   # quina vista de lado
    return "creme", CLARO if y >= 22 else BASE


def pintor_pescoco(t):
    x, y, z = t.p
    frente = t.face == "north" or (t.face in ("east", "west") and z < -4.5)
    if y < 29.5:
        return ("creme", BASE) if frente else ("verm", FUNDA)
    if frente: return "creme", CLARO
    return "verm", faixa(t)


def pintor_gema_peito(t):
    x, y, z = t.p
    c = t.c
    col = int(math.floor(x - c.origem[0]))
    lin = int(math.floor(c.origem[1] + c.tam[1] - y))
    forma = [".L.", "LCB", "CBS", "BSF", ".S."]
    ch = forma[min(max(lin, 0), 4)][min(max(col, 0), 2)]
    if ch == ".": return None
    tom = {"L": LUZ, "C": CLARO, "B": BASE, "S": SOMBRA, "F": FUNDA}[ch]
    if t.face != "north":
        tom = min(FUNDA, tom + 1)
    return "rubi", tom


def pintor_placa(t):
    """Placa prata com chanfro pintado: 1 px #f6f6f6 em cima, #d2bed1 no meio, #ac93ae embaixo."""
    x, y, z = t.p
    c = t.c
    if t.face == "up": return "prata", LUZ
    if t.face == "down": return "prata", BASE
    if y > c.origem[1] + c.tam[1] - 1: return "prata", LUZ
    if y < c.origem[1] + 1 and c.tam[1] >= 2: return "prata", SOMBRA
    return "prata", BASE


def pintor_fecho(t):
    x, y, z = t.p
    c = t.c
    if t.face == "south":
        borda = (x < c.origem[0] + 1 or x > c.origem[0] + c.tam[0] - 1 or y < c.origem[1] + 1
                 or y > c.origem[1] + c.tam[1] - 1)
        return ("ouro", BASE) if borda else ("prata", BASE)
    return pintor_placa(t)


def montar_tronco(corpo):
    caixa(corpo, (-4, 15, -7), (8, 14, 10), pintor_nucleo, nome="tronco")
    for k, (org, tam) in enumerate(DEGRAUS):
        caixa(corpo, org, tam, pintor_peito, nome=f"peito_{k}")
    borda = arte_mapa(["CCCCCC", "BBBBBB", "B.BB.B"], {"C": ("creme", CLARO), "B": ("creme", BASE)})
    plano(corpo, (-3, 12, -7.55), (6, 3, 0), plana(borda), rot=(10, 0, 0), pivo=(0, 15, -7.55), nome="peito_borda")
    for lado in (-1, 1):
        x0 = -7 if lado < 0 else 0
        caixa(corpo, (x0, 21.5, -10 - (0.02 if lado > 0 else 0)), (7, 2, 1), pintor_placa,
              rot=(0, 0, 45 * -lado), pivo=(0, 21.5, -9.5), nome=f"colar_{lado_nome(lado)}")
    gema = osso("gema_peito_brilho", corpo, (0, 25.5, -10.5))
    caixa(gema, (-1.5, 23, -11), (3, 5, 1), pintor_gema_peito, nome="gema_peito")


# ---------------------------------------- 5. cabeça, elmo e rosto ----------------------------------------
def pintor_cabeca(t):
    x, y, z = t.p
    if t.face == "north":
        if 34 <= y < 35 and 2 <= abs(x) < 4: return "creme", FUNDA                 # sombra sob o olho
        if y < 34 and abs(x) < 3: return "creme", CLARO if y > 32 else BASE        # garganta
        return "verm", CLARO if y > 36.3 else BASE
    if t.face in ("east", "west"):
        if 34 <= y < 35 and z < -5: return "creme", FUNDA                           # sombra sob o olho
        if y < 34.5 and z < -3.5: return "creme", CLARO if y > 32 else BASE        # bochecha
        return "verm", faixa(t)
    if t.face == "up": return "verm", SOMBRA
    if t.face == "down": return ("creme", BASE) if z < -3.5 else ("verm", SOMBRA)
    return "verm", faixa(t)


def pintor_tampa(t):
    return "verm", SOMBRA if t.face == "up" else BASE


def pintor_nuca(t):
    x, y, z = t.p
    if t.face == "south":
        return "verm", SOMBRA if int(math.floor(y - abs(x) * 0.8)) % 3 == 0 else BASE      # penas em V
    return "verm", faixa(t)


def pintor_olho(lado):
    def f(t):
        x, y, z = t.p
        if t.face == "north":
            return ("olho", BASE) if abs(x) < 3 else ("olho", LUZ)
        if (t.face == "east" and lado < 0) or (t.face == "west" and lado > 0):
            return ("olho", BASE) if z < -6 else ("olho", LUZ)
        return "verm", SOMBRA
    return f


def pintor_gema_testa(t):
    x, y, z = t.p
    c = t.c
    col = int(math.floor(x - c.origem[0]))
    lin = int(math.floor(c.origem[1] + c.tam[1] - y))
    forma = [".L.", "LCB", "CBS", ".S."]
    ch = forma[min(max(lin, 0), 3)][min(max(col, 0), 2)]
    if ch == ".": return None
    tom = {"L": LUZ, "C": CLARO, "B": BASE, "S": SOMBRA}[ch]
    if t.face != "north":
        tom = min(FUNDA, tom + 1)
    return "rubi", tom


def pintor_bico(t):
    if t.face == "up": return "ouro", LUZ if t.c.tam[0] >= 3 else CLARO
    if t.face == "down": return "ouro", SOMBRA
    return "ouro", BASE


def pintor_gancho(t):
    x, y, z = t.p
    if t.face == "up": return "ouro", CLARO
    if t.face == "down" or y < t.c.origem[1] + 1: return "ouro", SOMBRA
    return "ouro", BASE


ALETA = ["L..", "CC.", "BBS"]          # plano em x 3 x 3, coluna 0 = trás: ponta para trás e para cima


def montar_cabeca(cabeca):
    caixa(cabeca, (-4, 31, -7), (8, 8, 7), pintor_cabeca, nome="cabeca")
    caixa(cabeca, (-3, 39, -6), (6, 1, 5), pintor_tampa, nome="cabeca_tampa")       # chanfro em cima
    caixa(cabeca, (-3, 32, 0), (6, 6, 1), pintor_nuca, nome="cabeca_nuca")          # chanfro atrás
    caixa(cabeca, (-1.5, 31.5, -9), (3, 3, 2), pintor_bico, nome="bico_base")
    caixa(cabeca, (-1, 31.5, -10), (2, 2, 1), pintor_bico, nome="bico_meio")
    caixa(cabeca, (-1, 30.5, -11), (2, 2, 1), pintor_gancho, nome="bico_gancho")
    mand = osso("mandibula", cabeca, (0, 31.5, -7))
    caixa(mand, (-1, 30.5, -9), (2, 1, 2), lambda t: ("ouro", SOMBRA if t.face != "down" else FUNDA),
          nome="mandibula")
    gema = osso("gema_testa_brilho", cabeca, (0, 37, -7))
    caixa(gema, (-1.5, 35, -7.5), (3, 4, 1), pintor_gema_testa, nome="gema_testa")
    olhos = osso("olhos", cabeca, (0, 35, -6))
    for lado in (-1, 1):
        s = lado_nome(lado)
        x0 = -4 if lado < 0 else 2
        caixa(olhos, (x0, 34.5, -7), (2, 1, 2), pintor_olho(lado), inflate=0.02, nome=f"olho_{s}")
        pal = osso(f"palpebra_{s}", cabeca, (x0 + 1, 35, -6))
        caixa(pal, (x0, 34.5, -7), (2, 1, 2), lambda t: ("verm", SOMBRA if t.face == "down" else BASE),
              inflate=0.01, nome=f"palpebra_{s}")
        xv = -4.5 if lado < 0 else 1.5
        caixa(cabeca, (xv, 35.5, -7.5), (3, 1, 2), pintor_placa, rot=(0, 0, 15 * -lado),
              pivo=(xv + 1.5, 36, -6.5), nome=f"viseira_{s}")
        # elmo: faixa colada na lateral (inflate 0,02 = encostada), subindo 15° para trás
        xt = -5 if lado < 0 else 4
        caixa(cabeca, (xt, 35, -7), (1, 2, 7), pintor_placa, inflate=0.02, rot=(15, 0, 0),
              pivo=(xt + 0.5, 36, -7), nome=f"tiara_{s}")
        o = osso(f"tiara_aleta_{s}", cabeca, (xt + 0.5, 38, -2), (30, 0, 0))
        plano(o, (xt + 0.5, 37, -2), (0, 3, 3), plana(arte_mapa(ALETA, LEG_PRATA)), par="aleta",
              nome=f"tiara_aleta_{s}")


# ---------------------------------------- 2. crista e juba ----------------------------------------
#                  (leque em z para fora, raiz (x, y, z) do lado direito)
CHAMAS = ((30, (-1.5, 37.0, -2.5), [5, 5, 5, 4, 3, 3, 2, 1]), (50, (-1.5, 36.0, -2.0), [5, 5, 5, 4, 3, 3, 2, 1]),
          (70, (-1.0, 34.5, -1.5), [5, 5, 4, 3, 3, 2, 1]))
LAMINAS = ((-2.5, 12, -0.6), (-12.5, 12, -0.2), (-22.5, 11, 0.2), (-35, 9, 0.6))   # (inclinação, comprimento, x)
TUFOS = ((33.5, 35), (31.8, 55))                                            # (y da raiz, giro para fora)
L_U = [5, 5, 5, 4, 4, 3, 3, 2, 2, 1]
L_CENTRAL = [5, 5, 5, 4, 3, 3, 2, 1]
L_TUFO = [3, 3, 3, 1, 1]


def montar_crista(cabeca):
    crista = osso("crista", cabeca, (0, 38.5, -2))
    pena_z(crista, "crista_central", (0, 35.5, -6), virar(pena_larga(5, 8, "verm", 0, L_CENTRAL)), (-25, 15, 0))
    for lado in (-1, 1):
        s = lado_nome(lado)
        u = virar(pena_larga(5, 10, "verm", 0, L_U, curva=2.2, bojo=-1.2))
        pena_z(crista, f"crista_u_{s}", (3 * lado, 35.8, -4), u if lado < 0 else u.espelho(), (-20, 20 * -lado, 15 * lado))
        for k, (leque, (x, y, z), larg) in enumerate(CHAMAS):
            a = virar(pena_larga(5, len(larg), "verm", k % 2, larg, curva=-1.2))
            pena_z(crista, f"crista_chama_{s}_{k}", (x * -lado, y, z), a if lado < 0 else a.espelho(),
                   (-35, 25 * -lado, leque * lado), par=f"chama_{k}_{s}")
        for k, (y0, giro) in enumerate(TUFOS):
            a = pena_larga(3, 5, "verm", k % 2, L_TUFO)
            pena_z(cabeca, f"bochecha_{s}_{k}", (3.6 * lado, y0, -2.5 - 0.4 * k), a if lado < 0 else a.espelho(),
                   (0, 40 * -lado, giro * -lado), sobe=False, par=f"tufo_{k % 2}_{s}")
    # leque de trás (visto de costas): 3 chamas viradas para trás, abrindo da nuca
    for k, leque in enumerate((0, 40, -40)):
        a = virar(pena_larga(5, 8, "verm", k % 2, [5, 5, 5, 4, 3, 3, 2, 1], curva=-1.0 if leque else 0.0))
        if leque < 0:
            a = a.espelho()
        giro = 180 + (25 if leque > 0 else -25 if leque < 0 else 15)
        pena_z(crista, f"crista_tras_{k}", (0.0, 35.0, 1.3 + 0.1 * k), a, (20, giro, leque), par=f"tras_{k}")
    # lâminas da nuca (planos em x, vistos de lado), varrendo para trás
    for k, (incl, L, x) in enumerate(LAMINAS):
        a = deitar(pena_larga(5, L, "verm", k % 2, [5] * (L - 6) + [3] * 3 + [1] * 3, curva=-1.0))
        o = osso(f"crista_lamina_{k}", crista, (x, 38.5, -0.5), (incl, 0, 0))
        plano(o, (x, 36, -0.5), (0, 5, L), plana(a), nome=f"crista_lamina_{k}")


# ---------------------------------------- 4. ombreiras em concha ----------------------------------------
def pintor_concha(lado):
    def f(t):
        x, y, z = t.p
        c = t.c
        o, s = c.origem, c.tam
        if t.face == "up":
            borda = x < o[0] + 1 or x > o[0] + s[0] - 1 or z < o[2] + 1 or z > o[2] + s[2] - 1
            if borda: return "prata", LUZ
            meio = abs(x - (o[0] + s[0] / 2)) < 1.2 and abs(z - (o[2] + s[2] / 2)) < 1.6
            return "roxo", CLARO if meio else BASE                                 # miolo roxo (~60%)
        if t.face == "down": return "prata", SOMBRA
        if y > o[1] + s[1] - 1: return "prata", LUZ
        if y < o[1] + 1: return "prata", SOMBRA
        return "roxo", BASE
    return f


def pintor_ponta_ombro(t):
    if t.face == "up": return "ouro", LUZ
    if t.face == "down": return "ouro", SOMBRA
    return "ouro", CLARO


def montar_ombreiras(corpo):
    for lado in (-1, 1):
        s = lado_nome(lado)
        o = osso(f"ombro_{s}", corpo, (4 * lado, 27.5, 0), (0, 0, 10 * -lado))
        x0 = -10 if lado < 0 else 4
        caixa(o, (x0, 25.5, -4), (6, 3, 8), pintor_concha(lado), par="concha", nome=f"ombro_{s}_concha")
        x1 = -9.5 if lado < 0 else 4.5
        caixa(o, (x1, 28.5, -3), (5, 1, 6), pintor_concha(lado), par="chanfro", nome=f"ombro_{s}_chanfro")
        x2 = -9 if lado < 0 else 4
        caixa(o, (x2, 25, -5.5), (5, 2, 1), pintor_concha(lado), rot=(0, 0, 10 * lado),
              pivo=(4 * lado, 26, -5), par="aba", nome=f"ombro_{s}_aba")
        x3 = -12 if lado < 0 else 9
        caixa(o, (x3, 27, -1.5), (3, 1, 3), pintor_ponta_ombro, rot=(0, 0, 25 * -lado),
              pivo=(9 * lado, 27.5, 0), par="ombro_ponta", nome=f"ombro_{s}_ponta")


# ---------------------------------------- 1. capa ----------------------------------------
# Penas largas (5 px) num anel em volta do tronco; a 1ª de cada fileira cobre a frente do flanco. Cada pena
# tem um osso próprio: giro em y em volta do corpo (nunca a menos de 25° de perfil), leque em z (ponta para fora)
# e abertura do sino. As do meio das costas ficam num osso só (capa_costas).
#   pena = (x, y, z do topo, lado direito), giro em y, leque, abertura
CAPA = (
    (11, "roxo", None, (
        ((-5.0, 25.5, -7.3), 30, 28, 10), ((-6.6, 26.5, -3.6), 55, 34, 18),
        ((-6.8, 26.5, 0.6), 125, 20, 24), ((-4.6, 24.3, 3.8), 150, 14, 20))),
    (15, "roxo", (0.7, "verm"), (
        ((-6.4, 22.0, 3.4), 50, 20, 8), ((-7.2, 22.5, 3.2), 118, -14, 30), ((-6.8, 22.5, 5.0), 128, -10, 28),
        ((-5.4, 22.0, 6.4), 140, -6, 24), ((-3.6, 22.0, 7.2), 152, 0, 20))),
    (14, "roxo", (0.45, "verm"), (
        ((-6.6, 15.5, 3.8), 50, 18, 8), ((-7.6, 15.5, 3.8), 118, -14, 30), ((-7.6, 15.5, 5.4), 125, -12, 28),
        ((-6.8, 15.5, 6.8), 132, -10, 26), ((-5.4, 15.5, 7.8), 142, -6, 22), ((-3.6, 15.0, 8.5), 152, 0, 18))),
)
#   costas, por fileira: (y do topo, z do meio, abertura)
COSTAS = ((23.5, 5.0, 16), (20.5, 7.4, 16), (15.0, 8.8, 16))


def montar_capa(corpo):
    costas = osso("capa_costas", corpo, (0, 25, 5))
    for f, (H, mat, corte, penas) in enumerate(CAPA):
        artes = [pena_larga(5, H, mat, v, filete=f == 0, corte=corte) for v in (0, 1)]
        for lado in (-1, 1):
            s = lado_nome(lado)
            asa = POR_NOME.get(f"asa_{s}") or osso(f"asa_{s}", corpo, (5 * lado, 28.5, 0))
            for k, ((x, y, z), giro, leque, sino) in enumerate(penas):
                R = _R("y", giro) @ _R("x", sino) @ _R("z", -leque)
                if lado > 0:
                    R, x = ESPELHO @ R @ ESPELHO, -x
                a = artes[k % 2]
                pena_z(asa, f"capa_{s}_{f}_{k}", (x, y, z), a if lado < 0 else a.espelho(), euler(R), sobe=False,
                       par=f"capa_{f}_{k % 2}_{s}")
        # leque das costas: uma no meio e duas a ±20°
        y, zc, sino = COSTAS[f]
        for k, giro in enumerate((180, 160, 200)):
            x = 0.0 if k == 0 else (-2.4 if giro == 160 else 2.4)
            leque = 0 if k == 0 else (12 if giro == 160 else -12)      # as de ±20° abrem para os lados
            R = _R("y", giro) @ _R("x", sino) @ _R("z", leque)
            a = artes[k % 2]
            pena_z(costas, f"capa_t_{f}_{k}", (x, y, zc - (0.3 if k else 0)), a, euler(R), sobe=False,
                   par=f"capa_{f}_{k % 2}_t")


# ---------------------------------------- 3. cauda tripla com gravidade ----------------------------------------
#          nome, x da raiz, abertura em y, dobra de cada junta (para baixo), fecho da lâmina
TRANCAS = (("a", 0.0, 0.0, (0, 0, 15, 15, 20, 20, 15, 3), 2),
           ("b", -2.0, -15.0, (0, 0, 15, 15, 20, 20), 15),
           ("c", 2.0, 15.0, (0, 0, 15, 15, 20, 20), 15))
SEG = 3
LAMINA = 8
Y_CAUDA = 26.5


def pintor_tranca(t):
    """Gomos em diagonal (<<<) em 3 tons; o topo do segmento 1 tom mais claro."""
    x, y, z = t.p
    c = t.c
    u = int(math.floor(z - c.origem[2]))
    if t.face in ("east", "west"):
        v = int(math.floor(c.origem[1] + c.tam[1] - y))
    elif t.face in ("up", "down"):
        v = int(math.floor(x - c.origem[0]))
    else:
        return "ouro", SOMBRA
    if (u + v) % 3 == 2:
        tom = SOMBRA                                              # sulco em diagonal
    else:
        tom = CLARO if (t.face == "up" or v == 0) else BASE
    if t.face == "up" and tom == CLARO: tom = LUZ                 # topo 1 tom mais claro
    if t.face == "down": tom = SOMBRA
    return "ouro", tom


# lâmina em chama 4 x 8 (coluna 0 = ponta), cruz em X; o losango 2 x 3 fica por cima, no osso de brilho
LAMINA_X = ["..llll..", ".lOOOOO.", "lOOOOOOO", "..oooo.."]
LAMINA_Y = [".OO.", "OOOO", "OllO", "OllO", "OllO", "OllO", "OOOO", ".OO."]     # simétrica
LOSANGO = ["CLC", "SBS"]
LEG_LAMINA = {"O": ("ouro", BASE), "o": ("ouro", SOMBRA), "l": ("ouro", CLARO)}
LEG_LOSANGO = {"L": ("rubi", LUZ), "C": ("rubi", CLARO), "B": ("rubi", BASE), "S": ("rubi", SOMBRA)}


def montar_cauda(corpo):
    caixa(corpo, (-3, 25, 3), (6, 3, 1), pintor_fecho, nome="fecho_cauda")
    cauda = osso("cauda", corpo, (0, Y_CAUDA, 3.5))
    for nome, x0, abre, dobras, fecha in TRANCAS:
        pai, z = cauda, 4.0
        for k, d in enumerate(dobras):
            seg = osso(f"cauda_{nome}_{k}", pai, (x0, Y_CAUDA, z), (-d, abre if k == 0 else 0, 0))
            caixa(seg, (x0 - 1, Y_CAUDA - 1, z), (2, 2, SEG), pintor_tranca, par="tranca", nome=f"tranca_{nome}_{k}")
            pai, z = seg, z + SEG
        lam = osso(f"lamina_{nome}", pai, (x0, Y_CAUDA, z), (-fecha, 0, 0))
        plano(lam, (x0, Y_CAUDA - 2, z), (0, 4, LAMINA), plana(arte_mapa(LAMINA_X, LEG_LAMINA)), par="lamina_x",
              nome=f"lamina_{nome}_x")
        plano(lam, (x0 - 2, Y_CAUDA, z), (4, 0, LAMINA), plana(arte_mapa(LAMINA_Y, LEG_LAMINA)), par="lamina_y",
              nome=f"lamina_{nome}_y")
        bri = osso(f"losango_{nome}_brilho", lam, (x0, Y_CAUDA, z + 4))
        for d in (0.0, 0.02):        # uma plaquinha de cada lado (o plano tem uma face só)
            plano(bri, (x0 + d, Y_CAUDA - 1, z + 2.5), (0, 2, 3), plana(arte_mapa(LOSANGO, LEG_LOSANGO)),
                  inflate=0.01, par="losango", nome=f"losango_{nome}_{'a' if d else 'b'}")


# ---------------------------------------- 7. pernas e pés ----------------------------------------
def pintor_pe(t):
    x, y, z = t.p
    if t.face == "up": return "roxoe", CLARO
    if t.face == "down": return "roxoe", SOMBRA
    if (int(math.floor(z)) + int(math.floor(y))) % 2 == 0 and t.face != "south":
        return "roxoe", SOMBRA
    return "roxoe", BASE


def pintor_garra(t):
    if t.face == "up": return "ouro", LUZ
    if t.face == "down": return "ouro", SOMBRA
    return "ouro", CLARO


def pintor_canela(t):
    return "roxo", faixa(t)


def pintor_metal(t):
    return pintor_placa(t)


def pintor_coxa(t):
    x, y, z = t.p
    if t.face in ("east", "west") and abs(x) < 1.0: return "verm", FUNDA        # entre as coxas
    return "verm", faixa(t)


JOELHEIRA = [".L.", ".L.", "LBS", "BBS"]        # ponta de flecha para cima
TORNOZELEIRA = ["LBS", ".S."]                    # ponta para baixo


def montar_perna(raiz, lado):
    s = lado_nome(lado)
    cx = 2.6 * lado
    perna = osso(f"perna_{s}", raiz, (cx, 15, 0))
    caixa(perna, (cx - 2, 10, -3), (4, 6, 4), pintor_coxa, par="coxa", nome=f"coxa_{s}")
    # penas da coxa: 2 na frente caindo sobre a joelheira, 1 de lado, 1 atrás
    for k in range(2):
        a = pena_larga(3, 4, "verm", k, [3, 3, 3, 1])
        plano(perna, (cx - 2 + 1.5 * k if lado < 0 else cx - 1 - 1.5 * k, 9.5, -3.15 - 0.1 * k), (3, 4, 0),
              plana(a if lado < 0 else a.espelho()), par=f"coxa_pena_{k}_{s}", nome=f"coxa_{s}_pena_{k}")
    saia = pena_larga(5, 6, "verm", 0)          # pena pendurada (raiz em cima)
    plano(perna, (cx + 2.15 * lado, 9.5, -3.4), (0, 6, 5), plana(saia), par="saia_l", nome=f"saia_{s}_l")
    plano(perna, (cx - 2.5, 9.5, 1.15), (5, 6, 0), plana(saia), par="saia_t", nome=f"saia_{s}_t")
    caixa(perna, (cx - 1.5, 8.5, -2.5), (3, 2, 3), pintor_metal, par="joelheira", nome=f"joelheira_{s}")
    plano(perna, (cx - 1.5, 8.5, -2.55), (3, 4, 0), plana(arte_mapa(JOELHEIRA, LEG_PRATA)), rot=(15, 0, 0),
          pivo=(cx, 8.5, -2.55), par="joelheira_ponta", nome=f"joelheira_{s}_ponta")
    caixa(perna, (cx - 1, 2, -2), (2, 7, 2), pintor_canela, par="canela", nome=f"canela_{s}")
    caixa(perna, (cx - 1.5, 4.5, -2.5), (3, 1, 3), pintor_metal, par="tornozeleira", nome=f"tornozeleira_{s}")
    plano(perna, (cx - 1.5, 3.5, -2.55), (3, 2, 0), plana(arte_mapa(TORNOZELEIRA, LEG_PRATA)),
          par="tornozeleira_ponta", nome=f"tornozeleira_{s}_ponta")
    pe = osso(f"pe_{s}", perna, (cx, 3.5, -1))
    caixa(pe, (cx - 1.5, 0, -2.5), (3, 2, 3), pintor_pe, par="pe", nome=f"pe_{s}")
    for k, giro in enumerate((0, 30, -30)):
        dedo = osso(f"dedo_{s}_{k}", pe, (cx, 0.5, -2), (0, giro * -lado if k else 0, 0))
        caixa(dedo, (cx - 0.5, 0, -5.5), (1, 1, 3), pintor_pe, par="dedo", nome=f"dedo_{s}_{k}")
        caixa(dedo, (cx - 0.5, 0.4, -6.5), (1, 1, 1), pintor_garra, par="garra", nome=f"garra_{s}_{k}")
        caixa(dedo, (cx - 0.5, 0.4, -7.5), (1, 1, 1), pintor_garra, rot=(40, 0, 0), pivo=(cx, 1.4, -6.5),
              par="garra", nome=f"garra_{s}_{k}_ponta")
    caixa(pe, (cx - 0.5, 0, 0.5), (1, 1, 1), pintor_pe, par="dedo_tras", nome=f"dedo_{s}_tras")
    caixa(pe, (cx - 0.5, 0.4, 1.5), (1, 1, 1), pintor_garra, rot=(-40, 0, 0), pivo=(cx, 1.4, 1.5),
          par="garra", nome=f"garra_{s}_tras")


# ======================================================================================================
# Animações (Molang, laço sem emenda)
# ======================================================================================================
def S(k, fase, amp, L=4):
    """math.sin com k ondas por laço de L segundos."""
    w = round(360 / L * k)
    f = f"+{fase}" if fase > 0 else (f"{fase}" if fase < 0 else "")
    return f"math.sin(query.anim_time*{w}{f})*{amp}"


def animacoes():
    idle, walk = {}, {}
    W = lambda k, fase, amp: S(k, fase, amp, L=2)
    # ---------------- idle (L = 4) ----------------
    idle["corpo"] = {"rotation": [S(2, 0, 1.5), 0, 0], "position": [0, S(2, -90, 0.2), 0]}
    idle["pescoco"] = {"rotation": [S(2, -40, -1.0), 0, 0]}
    idle["cabeca"] = {"rotation": [S(2, -60, 2), S(1, 0, 3), 0]}
    idle["crista"] = {"rotation": [S(2, -120, 4), 0, S(1, -60, 1.5)]}
    for k in range(len(LAMINAS)):
        idle[f"crista_lamina_{k}"] = {"rotation": [S(2, -150 - 30 * k, 3), 0, 0]}
    idle["capa_costas"] = {"rotation": [S(2, -90, 1.5), 0, 0]}
    for s, sg in (("d", 1), ("e", -1)):
        idle[f"asa_{s}"] = {"rotation": [S(2, -60, 1), 0, S(2, -90, 2 * sg)]}
        for k in range(len(CHAMAS)):
            idle[f"crista_chama_{s}_{k}"] = {"rotation": [0, 0, S(2, -150 - 30 * k, 3 * sg)]}
    for nome, _, _, dobras, _ in TRANCAS:          # pêndulo: as laterais em fase oposta
        fase = {"a": 90, "b": 0, "c": 180}[nome]
        for k in range(len(dobras)):
            idle[f"cauda_{nome}_{k}"] = {"rotation": [S(2, -30 * k, 2), 0, S(1, fase - 30 * k, 3)]}
        idle[f"lamina_{nome}"] = {"rotation": [S(2, -30 * len(dobras), 2), 0, S(1, fase - 30 * len(dobras), 3)]}
    for s, sg in (("d", -1), ("e", 1)):
        z = [0, 0, 0]
        f = [round(0.12 * sg, 2), 0, -0.12]
        idle[f"palpebra_{s}"] = {"position": {"0.0": z, "3.7": z, "3.72": f, "3.84": f, "3.86": z, "4.0": z}}
    # ---------------- walk (L = 2) ----------------
    walk["perna_d"] = {"rotation": [W(1, 0, 25), 0, 0]}
    walk["perna_e"] = {"rotation": [W(1, 180, 25), 0, 0]}
    walk["pe_d"] = {"rotation": [W(1, 0, -25), 0, 0]}
    walk["pe_e"] = {"rotation": [W(1, 180, -25), 0, 0]}
    walk["corpo"] = {"rotation": [W(2, 0, 1.5), W(1, 0, 2), W(1, 0, 3)],
                     "position": [0, f"{W(2, 90, 0.2)}+0.2", 0]}
    walk["cabeca"] = {"rotation": [W(2, -60, -1.5), W(1, 0, -1.5), W(1, 0, -2.5)]}
    walk["crista"] = {"rotation": [W(2, -120, 4), 0, W(1, -60, 2)]}
    for k in range(len(LAMINAS)):
        walk[f"crista_lamina_{k}"] = {"rotation": [W(2, -150 - 30 * k, 4), 0, 0]}
    walk["capa_costas"] = {"rotation": [W(2, -90, 2.5), 0, 0]}
    for s, sg in (("d", 1), ("e", -1)):
        walk[f"asa_{s}"] = {"rotation": [W(2, -60, 2), 0, W(1, -60, 3)]}
    for nome, _, _, dobras, _ in TRANCAS:          # ±6° em z, defasado do corpo
        for k in range(len(dobras)):
            walk[f"cauda_{nome}_{k}"] = {"rotation": [W(2, -40 * k - 40, 1.5), 0, W(1, -90 - 30 * k, 6 if k == 0 else 1.5)]}
        walk[f"lamina_{nome}"] = {"rotation": [0, 0, W(1, -90 - 30 * len(dobras), 2)]}
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
    if girados > 0.15 * n:
        erros.append(f"{girados} cubos girados ({100 * girados / n:.0f}%) passam de 15%")
    for c in cubos:
        if c.plano and c.osso.nome.startswith(("crista", "bochecha", "capa")):
            base = min(v for v in c.tam if v)
            minimo = 3 if c.osso.nome.startswith("bochecha") else 5
            if base < minimo:
                erros.append(f"{c.nome}: pena com base de {base} px (mínimo {minimo})")
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
    # comparação como na folha de marcações: modelo em cima, ficha embaixo, mesma altura
    ficha = Image.open(FICHA).convert("RGB")
    alt = 360
    cima = []
    for nome, yaw, pitch in (("modelo: frente", 0, 0), ("modelo: lado direito", 90, 0), ("modelo: trás", 180, 0),
                             ("modelo: 3/4", 35, -20)):
        r = recortar(rg.desenhar(faces, tex, yaw, pitch, 10))
        cima.append((nome, r.resize((round(r.width * alt / r.height), alt), Image.NEAREST)))
    baixo = []
    for nome, chave, inverter in (("ficha: FRENTE", "frente", False), ("ficha: DIREITA (espelhada)", "direita", True),
                                  ("ficha: TRÁS", "tras", False)):
        f = ficha.crop(VISTAS_FICHA[chave])
        if inverter:
            f = f.transpose(Image.FLIP_LEFT_RIGHT)
        baixo.append((nome, f.resize((round(f.width * alt / f.height), alt), Image.LANCZOS)))
    W = max(sum(i.width + 30 for _, i in cima), sum(i.width + 30 for _, i in baixo)) + 20
    out = Image.new("RGB", (W, 2 * alt + 90), FUNDO)
    d = ImageDraw.Draw(out)
    for linha, y in ((cima, 25), (baixo, alt + 70)):
        x = 15
        for nome, im in linha:
            out.paste(im, (x, y))
            d.text((x, y - 20), nome, fill=(30, 30, 30), font=fonte())
            x += im.width + 30
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


PLANTA = RAIZ / "modelos/referencias/001_pirococo_planta_proporcoes.png"
PLANTA_ESCALA = 18.2                 # px por unidade
PLANTA_CHAO = 895                    # y da imagem no chão (y = 0)
PLANTA_FRENTE_X0 = 314               # x da imagem no centro da vista de frente (x = 0)
PLANTA_LADO_Z0 = 863                 # x da imagem em z = 0 na vista de lado (frente para a esquerda)


def pontos_opacos(geo, tex, anim, n=10):
    """Pontos (x, y, z) do mundo, no espaço do JSON, dos texels opacos do modelo numa pose."""
    H, W = tex.shape[:2]
    pts = []
    for P, (u1, v1, u2, v2), _ in rg.faces_do_modelo(geo, anim):
        p0, p1, p2 = (np.array(p) for p in P)
        nu = max(2, int(abs(u2 - u1) * 3)); nv = max(2, int(abs(v2 - v1) * 3))
        for a in np.linspace(0.01, 0.99, nu):
            for b in np.linspace(0.01, 0.99, nv):
                tu = min(max(int(math.floor(u1 + a * (u2 - u1))), 0), W - 1)
                tv = min(max(int(math.floor(v1 + b * (v2 - v1))), 0), H - 1)
                if tex[tv, tu, 3] > 0:
                    pts.append(p0 + a * (p1 - p0) + b * (p2 - p0))
    p = np.array(pts)
    p[:, 0] *= -1
    return p


def sobre_planta(geo, tex, anim, pasta):
    """Contorno do modelo (1º quadro do idle) em ciano sobre a planta de proporções, na mesma escala."""
    if not PLANTA.exists():
        return
    planta = Image.open(PLANTA).convert("RGB")
    p = pontos_opacos(geo, tex.astype(np.uint8) if tex.dtype != np.uint8 else tex, anim)
    k = PLANTA_ESCALA
    mascara = np.zeros((planta.height, planta.width), bool)
    for xs in ((PLANTA_FRENTE_X0 + p[:, 0] * k), (PLANTA_LADO_Z0 + p[:, 2] * k)):
        ys = PLANTA_CHAO - p[:, 1] * k
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                xi = np.clip((xs + dx).astype(int), 0, planta.width - 1)
                yi = np.clip((ys + dy).astype(int), 0, planta.height - 1)
                mascara[yi, xi] = True
    # a vista de frente não pode vazar para a de lado e vice-versa
    borda = mascara & ~(np.roll(mascara, 1, 0) & np.roll(mascara, -1, 0) & np.roll(mascara, 1, 1) & np.roll(mascara, -1, 1))
    a = np.asarray(planta).copy()
    clara = (a * 0.55 + 255 * 0.45).astype(np.uint8)
    clara[mascara] = (clara[mascara] * 0.75 + np.array([0, 170, 220]) * 0.25).astype(np.uint8)
    for d in (0, 1):
        clara[np.roll(borda, d, 1)] = (0, 120, 200)
    out = Image.fromarray(clara)
    ImageDraw.Draw(out).text((10, 2), "modelo (contorno azul, área ciano) sobre a planta de proporções", fill=(0, 60, 120),
                             font=fonte(14))
    out.save(pasta / f"{ID}_planta.png")


def antes_depois(pasta_antes, pasta, escala=6):
    """Vistas do modelo anterior (em cima) e do atual (embaixo), na mesma escala, no 1º quadro do idle."""
    vistas = ((0, 0, "frente"), (270, 0, "lado"), (180, 0, "trás"), (35, -20, "3/4"))
    linhas = []
    for rotulo, p in (("antes", Path(pasta_antes)), ("depois", Path(pasta))):
        geo = json.load(open(p / f"{ID}.geo.json", encoding="utf-8"))
        tex = np.asarray(Image.open(p / f"{ID}.png").convert("RGBA")).astype(np.float32)
        an = rg.carregar_animacao(str(p / f"{ID}.animation.json"), f"animation.{ID}.idle")
        faces = rg.faces_do_modelo(geo, an)
        linhas.append((rotulo, [(n, rg.desenhar(faces, tex, y, pi, escala)) for y, pi, n in vistas]))
    larg = [max(l[1][k][1].width for l in linhas) for k in range(len(vistas))]
    alt = [max(im.height for _, im in l[1]) for l in linhas]
    out = Image.new("RGB", (sum(larg) + 90, sum(alt) + 50), FUNDO)
    d = ImageDraw.Draw(out)
    y = 10
    for (rotulo, ims), h in zip(linhas, alt):
        d.text((8, y + h // 2), rotulo, fill=(30, 30, 30), font=fonte(15))
        x = 80
        for (n, im), w in zip(ims, larg):
            out.paste(im, (x + (w - im.width) // 2, y + h - im.height))
            d.text((x + 4, y), n, fill=(60, 60, 60), font=fonte(12))
            x += w
        y += h + 20
    out.save(pasta / f"{ID}_antes_depois.png")


# ======================================================================================================
def gerar(pasta=AQUI, instalar=False, conferir=True, antes=None):
    OSSOS.clear()
    POR_NOME.clear()
    PARES.clear()
    montar()
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
        sobre_planta(geo, tex, rg.carregar_animacao(str(pasta / f"{ID}.animation.json"), f"animation.{ID}.idle"), pasta)
        if antes:
            antes_depois(antes, pasta)
    if instalar:
        shutil.copyfile(pasta / f"{ID}.geo.json", ASSETS / f"geckolib/models/entity/{ID}.geo.json")
        shutil.copyfile(pasta / f"{ID}.animation.json", ASSETS / f"geckolib/animations/entity/{ID}.animation.json")
        shutil.copyfile(pasta / f"{ID}.png", ASSETS / f"textures/entity/{ID}.png")
        shutil.copyfile(pasta / f"{ID}_glowmask.png", ASSETS / f"textures/entity/{ID}_glowmask.png")
        print("  instalado em", ASSETS)
    return ok


if __name__ == "__main__":
    a = sys.argv
    antes = a[a.index("--antes") + 1] if "--antes" in a else None
    sys.exit(0 if gerar(instalar="--instalar" in a, conferir="--sem-imagens" not in a, antes=antes) else 1)
