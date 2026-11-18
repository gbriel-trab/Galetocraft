"""Biblioteca para modelar Cocorídeos no padrão Cobblemon (modelos/GUIA_ESTILO.md).

Diferente de galo_base.py, aqui o modelo é escrito direto no formato do jogo (.geo.json do GeckoLib):
- coordenadas Bedrock: y para cima, FRENTE em -z, lado ESQUERDO da criatura em +x (o mesmo do Cobblemon);
- 1 unidade = 1 texel = 1/16 de bloco (escala 1 no jogo: o modelo já nasce na altura da tabela);
- cubos com tamanho inteiro e UV de caixa, empacotada sozinha na textura;
- `espelhar()` cria o lado direito com `mirror` e a MESMA UV do esquerdo (a textura é pintada uma vez);
- planos = cubos com uma dimensão 0 (franjas, chamas, penas de borda, olhos);
- cada cubo tem uma função de pintura chamada para cada texel das suas faces, com a posição dele no cubo.

Uso:
    m = Modelo("pirococo", 128, 128)
    raiz = m.osso("pirococo")
    corpo = m.osso("corpo", raiz, pivo=(0, 15, 0))
    m.cubo(corpo, (-5, 14, -4), (10, 12, 9), material(ROXO, 2))
    m.salvar(pasta, animacoes)
"""
import json, math
from pathlib import Path

import numpy as np
from PIL import Image

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from previa import ponto_face  # noqa: E402
from analisar_geo import _uv_caixa  # noqa: E402

FACE_PT = {"north": "frente", "south": "tras", "up": "cima", "down": "baixo", "east": "dir", "west": "esq"}


# ----------------------------------------------------------------------------------------------------------------
# Ruído determinístico e materiais
# ----------------------------------------------------------------------------------------------------------------
def ruido(u, v, semente=0):
    """Número pseudoaleatório em [0, 1) fixo para cada texel (u, v): a textura sai igual a cada rodada."""
    h = (int(u) * 73856093) ^ (int(v) * 19349663) ^ ((semente + 1) * 83492791)
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return ((h ^ (h >> 16)) & 0xFFFFFF) / float(0x1000000)


def tom(rampa, i):
    return rampa[max(0, min(len(rampa) - 1, int(round(i))))]


def mosqueado(rampa, base, t, chance=0.16, luz=True):
    """Tom da rampa com o mosqueado leve do Cobblemon: ~2 x chance dos texels sobem ou descem 1 tom.
    Luz pintada fraca: a tampa sobe 1 tom em 35% dos texels, o fundo desce 1 tom em 45%."""
    n = ruido(t.u, t.v, len(rampa))
    i = base + (-1 if n < chance else 1 if n > 1 - chance else 0)
    if luz:
        m = ruido(t.u, t.v, 99)
        if t.face == "cima" and m < 0.35: i += 1
        if t.face == "baixo" and m < 0.45: i -= 1
    return tom(rampa, i)


def rampa_da_arte(rgb, tons=5, meio=2, sat=1.35, sat_max=0.85, v_max=0.85,
                  passo_h=3.0, passo_s=0.045, passo_v_claro=0.055, passo_v_escuro=0.085):
    """Rampa de pixel art no jeito Cobblemon a partir da cor chapada de uma região da arte.

    Medido no Blaziken (arte oficial x textura): o tom do meio mantém o matiz da arte, satura ~1,35x e os claros
    escurecem um pouco (V até ~0,85). A cada tom mais claro: matiz +3° (para o amarelo), saturação -0,045 e brilho
    +0,055; para o escuro o passo de brilho é maior (-0,085). Ex.: rampa_da_arte((187, 87, 69)) -> vermelho."""
    import colorsys
    h, s, v = colorsys.rgb_to_hsv(*(c / 255 for c in rgb))
    s = min(sat_max, s * sat); v = min(v, v_max)
    saida = []
    for i in range(tons):
        k = i - meio
        hi = (h + k * passo_h / 360) % 1.0
        si = max(0.0, min(1.0, s - k * passo_s))
        vi = max(0.0, min(1.0, v + k * (passo_v_claro if k > 0 else passo_v_escuro)))
        saida.append(tuple(int(round(c * 255)) for c in colorsys.hsv_to_rgb(hi, si, vi)))
    return saida


def material(rampa, base, chance=0.16):
    return lambda t: mosqueado(rampa, base, t, chance)


# ----------------------------------------------------------------------------------------------------------------
# Estrutura
# ----------------------------------------------------------------------------------------------------------------
class Osso:
    def __init__(self, nome, pai, pivo, rot):
        self.nome, self.pai, self.pivo, self.rot = nome, pai, tuple(pivo), tuple(rot)
        self.cubos = []


class Cubo:
    def __init__(self, osso, origem, tam, pintura, inflate=0.0, pivo=None, rot=None, brilho=None, uv_de=None,
                 mirror=False):
        assert all(float(s).is_integer() and s >= 0 for s in tam), f"tamanho não inteiro em {osso.nome}: {tam}"
        self.osso, self.origem, self.tam = osso, tuple(origem), tuple(int(s) for s in tam)
        self.pintura, self.inflate, self.pivo, self.rot = pintura, inflate, pivo, rot
        self.brilho, self.uv_de, self.mirror = brilho, uv_de, mirror
        self.uv = None
        if brilho:
            assert "_brilho" in osso.nome, f"cubo com brilho precisa estar num osso '*_brilho' ({osso.nome})"


class Texel:
    """O que a função de pintura recebe: face ('frente', 'tras', 'cima', 'baixo', 'esq', 'dir'), posição do centro do
    texel dentro do cubo em unidades (x, y, z; x cresce para a ESQUERDA da criatura), tamanho do cubo (w, h, d) e o
    texel da textura (u, v)."""
    __slots__ = ("face", "x", "y", "z", "w", "h", "d", "u", "v")


class Modelo:
    def __init__(self, id_, largura=128, altura=128):
        self.id, self.largura, self.altura = id_, largura, altura
        self.ossos = []

    # -------------------------------------------------------------- montagem
    def osso(self, nome, pai=None, pivo=(0, 0, 0), rot=(0, 0, 0)):
        assert nome not in {o.nome for o in self.ossos}, f"osso repetido: {nome}"
        o = Osso(nome, pai, pivo, rot)
        self.ossos.append(o)
        return o

    def cubo(self, osso, origem, tam, pintura, **k):
        c = Cubo(osso, origem, tam, pintura, **k)
        osso.cubos.append(c)
        return c

    def espelhar(self, osso, de="_e", para="_d", pai=None):
        """Copia o osso (e os filhos) para o outro lado: x -> -x, rotação (rx, -ry, -rz), cubos com mirror e a
        mesma UV. Os nomes trocam `de` por `para`."""
        px, py, pz = osso.pivo; rx, ry, rz = osso.rot
        novo = self.osso(osso.nome.replace(de, para), pai if pai is not None else osso.pai, (-px, py, pz), (rx, -ry, -rz))
        for c in osso.cubos:
            (x, y, z), (w, h, d) = c.origem, c.tam
            pivo = None if c.pivo is None else (-c.pivo[0], c.pivo[1], c.pivo[2])
            rot = None if c.rot is None else (c.rot[0], -c.rot[1], -c.rot[2])
            dono = c.uv_de or c
            self.cubo(novo, (-(x + w), y, z), (w, h, d), None, inflate=c.inflate, pivo=pivo, rot=rot,
                      brilho=c.brilho, uv_de=dono, mirror=not c.mirror)
        for filho in [o for o in self.ossos if o.pai is osso]:
            self.espelhar(filho, de, para, pai=novo)
        return novo

    # -------------------------------------------------------------- UV de caixa
    @staticmethod
    def _area_usada(tam):
        """(largura, altura, desloc_u, desloc_v) do retângulo da caixa que tem texels (planos não usam tudo)."""
        w, h, d = tam
        if w == 0: return 2 * d, h, 0, d             # plano de lado: só leste/oeste
        if h == 0: return 2 * w, d, d, 0             # plano deitado: só cima/baixo
        return 2 * (d + w), d + h, 0, 0              # caixa (inclui plano de frente, d = 0)

    def empacotar(self):
        donos = [c for o in self.ossos for c in o.cubos if c.uv_de is None]
        # caixas primeiro e planos de lado/deitados depois: assim a faixa sem texels deles nunca cai fora da folha
        itens = sorted(donos, key=lambda c: (self._area_usada(c.tam)[2] + self._area_usada(c.tam)[3] > 0,
                                             -self._area_usada(c.tam)[1], -self._area_usada(c.tam)[0]))
        x = y = alt_prateleira = 0
        ocupado = 0
        for c in itens:
            lw, lh, du, dv = self._area_usada(c.tam)
            if x + lw > self.largura:
                x, y, alt_prateleira = 0, y + alt_prateleira, 0
            if y + lh > self.altura:
                raise ValueError(f"textura {self.largura}x{self.altura} pequena demais (faltou espaço em {c.osso.nome})")
            if x - du < 0: x = du
            assert y - dv >= 0, f"UV negativa em {c.osso.nome}: aumente a folha ou mude o empacotamento"
            c.uv = (x - du, y - dv)
            x += lw; alt_prateleira = max(alt_prateleira, lh); ocupado += lw * lh
        for o in self.ossos:
            for c in o.cubos:
                if c.uv_de is not None:
                    assert c.uv_de.tam == c.tam, f"uv_de com tamanho diferente em {o.nome}"
                    c.uv = c.uv_de.uv
        return ocupado / (self.largura * self.altura)

    def _faces(self, c):
        """[(face, (u1, v1, u2, v2))] das faces com texels."""
        w, h, d = c.tam
        uvs = _uv_caixa(c.uv[0], c.uv[1], w, h, d, False)
        return [(f, r) for f, r in uvs.items() if abs(r[2] - r[0]) > 1e-9 and abs(r[3] - r[1]) > 1e-9]

    # -------------------------------------------------------------- textura
    def pintar(self):
        tex = np.zeros((self.altura, self.largura, 4), np.uint8)
        brilho = np.zeros_like(tex)
        t = Texel()
        for o in self.ossos:
            for c in o.cubos:
                if c.uv_de is not None or c.pintura is None: continue
                w, h, d = c.tam
                for face, (u1, v1, u2, v2) in self._faces(c):
                    a, b = sorted((u1, u2)); e, f = sorted((v1, v2))
                    for pv in range(int(e), int(f)):
                        for pu in range(int(a), int(b)):
                            fu = (pu + 0.5 - u1) / (u2 - u1); fv = (pv + 0.5 - v1) / (v2 - v1)
                            bx, by, bz = ponto_face(face, (0, 0, 0), (w, h, d), fu, fv)
                            t.face, t.x, t.y, t.z = FACE_PT[face], w - bx, by, bz
                            t.w, t.h, t.d, t.u, t.v = w, h, d, pu, pv
                            cor = c.pintura(t)
                            if cor is None: continue
                            if not (0 <= pu < self.largura and 0 <= pv < self.altura): continue
                            rgba = tuple(cor) + (255,) if len(cor) == 3 else tuple(cor)
                            tex[pv, pu] = rgba
                            if c.brilho and (c.brilho is True or c.brilho(rgba[:3])):
                                brilho[pv, pu] = rgba
        return tex, brilho

    # -------------------------------------------------------------- saída
    def geo(self):
        ossos = []
        for o in self.ossos:
            b = {"name": o.nome, "pivot": list(o.pivo)}
            if o.pai is not None: b["parent"] = o.pai.nome
            if any(abs(v) > 1e-9 for v in o.rot): b["rotation"] = list(o.rot)
            cs = []
            for c in o.cubos:
                q = {"origin": [round(v, 4) for v in c.origem], "size": list(c.tam), "uv": list(c.uv)}
                if c.inflate: q["inflate"] = c.inflate
                if c.mirror: q["mirror"] = True
                if c.rot is not None and any(abs(v) > 1e-9 for v in c.rot):
                    q["pivot"] = list(c.pivo); q["rotation"] = list(c.rot)
                cs.append(q)
            if cs: b["cubes"] = cs
            ossos.append(b)
        return {"format_version": "1.12.0", "minecraft:geometry": [{
            "description": {"identifier": f"geometry.{self.id}", "texture_width": self.largura,
                            "texture_height": self.altura, "visible_bounds_width": 4, "visible_bounds_height": 4,
                            "visible_bounds_offset": [0, 1.5, 0]},
            "bones": ossos}]}

    def salvar(self, pasta, animacoes=None):
        pasta = Path(pasta); pasta.mkdir(parents=True, exist_ok=True)
        uso = self.empacotar()
        tex, brilho = self.pintar()
        (pasta / f"{self.id}.geo.json").write_text(json.dumps(self.geo(), indent=1), encoding="utf-8")
        Image.fromarray(tex, "RGBA").save(pasta / f"{self.id}.png")
        Image.fromarray(brilho, "RGBA").save(pasta / f"{self.id}_glowmask.png")
        if animacoes is not None:
            nomes = {o.nome for o in self.ossos}
            faltam = sorted({b for a in animacoes.values() for b in a["bones"]} - nomes)
            assert not faltam, f"animação mexe em ossos que não existem: {faltam}"
            doc = {"format_version": "1.8.0", "animations": {f"animation.{self.id}.{n}": a for n, a in animacoes.items()}}
            (pasta / f"{self.id}.animation.json").write_text(json.dumps(doc, indent=1), encoding="utf-8")
        cubos = sum(len(o.cubos) for o in self.ossos)
        print(f"{self.id}: {len(self.ossos)} ossos, {cubos} cubos, textura {self.largura}x{self.altura} "
              f"({100 * uso:.0f}% da folha) -> {pasta}")


# ----------------------------------------------------------------------------------------------------------------
# Animação: curvas escritas como funções do tempo, gravadas como keyframes lineares (máxima compatibilidade)
# ----------------------------------------------------------------------------------------------------------------
def onda(amp, k=1.0, fase=0.0, base=0.0):
    """Senoide no estilo do Cobblemon: base + amp * sin(t*90*k - fase), em graus; período = 4/k s."""
    return lambda t: base + amp * math.sin(math.radians(t * 90 * k - fase))


def canal(x=0.0, y=0.0, z=0.0):
    """Junta 3 eixos (números ou funções do tempo) num canal."""
    f = lambda e: e if callable(e) else (lambda t, e=e: e)
    fx, fy, fz = f(x), f(y), f(z)
    return lambda t: [fx(t), fy(t), fz(t)]


def gravar(duracao, ossos, passo=0.1, loop=True):
    """ossos = {nome: {"rotation"|"position"|"scale": função(t) -> [x, y, z] ou {t: [x, y, z]} já pronto}}."""
    n = max(2, int(round(duracao / passo)) + 1)
    tempos = [duracao * i / (n - 1) for i in range(n)]
    saida = {}
    for osso, canais in ossos.items():
        b = {}
        for nome, f in canais.items():
            if isinstance(f, dict):
                b[nome] = {f"{t:.4f}".rstrip("0").rstrip(".") if t else "0.0": [round(v, 3) for v in val]
                           for t, val in sorted(f.items())}
            else:
                b[nome] = {f"{t:.4f}".rstrip("0").rstrip(".") if t else "0.0": [round(v, 3) for v in f(t)] for t in tempos}
        saida[osso] = b
    a = {"loop": loop, "animation_length": duracao, "bones": saida}
    return a
