"""Planta de proporções: desenha os volumes planejados (em unidades do modelo) por cima das vistas da ficha.

Serve para conferir, ANTES de modelar, se as medidas planejadas batem com o desenho 2D. Cada planta guarda:
- onde estão a vista de frente e a de lado na ficha (em pixels) e onde fica o chão e o topo de cada uma;
- os volumes planejados, em unidades (16 u = 1 bloco; y para cima a partir do chão; x = lado, 0 no meio;
  z = profundidade, a FRENTE da criatura é z negativo, como no galo_base);
- os marcos de altura (linhas horizontais com nome).

A escala vem da própria ficha: (chão - topo) em pixels corresponde a `altura_u`.

Uso: python ferramentas/planta_proporcoes.py [planta]   (padrão: todas)
Grava modelos/<pasta>/<saida>.png
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent

# cores das famílias de peças (RGB); o preenchimento sai translúcido
C_CAB = (40, 120, 255)      # cabeça, bico, crista
C_TRONCO = (0, 170, 90)     # tronco, pescoço, peitoral
C_ARM = (120, 120, 120)     # armadura
C_CAPA = (150, 60, 200)     # capa / asas
C_PERNA = (255, 140, 0)     # pernas e pés
C_CAUDA = (230, 30, 60)     # cauda

PLANTAS = {
    # ---------------------------------------------------------------- #001 Pirococó, ficha anime (Galetário)
    "pirococo_anime": {
        "ficha": "modelos/referencias/001_pirococo_anime_ficha.png",
        "pasta": "pirococo", "saida": "proporcoes_anime_planta",
        "titulo": "#001 Pirococó (ficha anime) - planta de proporções, H = 45 u (2,8 blocos)",
        "altura_u": 45,
        "frente": {"recorte": (636, 52, 838, 346), "topo": 61, "chao": 337, "centro_x": 737.5},
        "lado": {"recorte": (840, 52, 1082, 352), "topo": 61, "chao": 334, "z0_x": 919},
        "marcos": [
            (45, "ponta da crista (penas em U)"), (42, "pena central da crista"), (39, "topo do elmo"),
            (35, "linha dos olhos"), (31, "queixo"), (29.5, "colar / topo da ombreira"),
            (21.5, "ponta do V do peitoral"), (15, "quadril (pivô das pernas)"),
            (10.5, "fim da saia de penas / joelho"), (5.5, "tornozelo"), (1.5, "barra da capa"), (0, "chão"),
        ],
        # (nome, cor, x0, x1, y0, y1) em u; espelhadas = True desenha também o lado oposto (x -> -x)
        "frente_caixas": [
            ("crista (chamas)", C_CAB, -7.5, 7.5, 34, 43, False),
            ("penas em U", C_CAB, -4.5, 4.5, 39, 45, False),
            ("cabeça", C_CAB, -3.75, 3.75, 31, 39, False),
            ("gema", C_ARM, -1.25, 1.25, 34.5, 39, False),
            ("bico", C_CAB, -1.25, 1.25, 31, 34, False),
            ("pescoço", C_TRONCO, -2.5, 2.5, 29, 31, False),
            ("ombreira", C_ARM, 4.5, 10.5, 26, 29.5, True),
            ("peitoral", C_ARM, -5, 5, 21.5, 29.5, False),
            ("gema peito", C_ARM, -1.75, 1.75, 23, 28, False),
            ("peito creme", C_TRONCO, -3.5, 3.5, 15, 21.5, False),
            ("coxa", C_PERNA, 0.85, 4.35, 10.5, 15, True),
            ("joelheira", C_ARM, 1.1, 4.1, 8.5, 10.5, True),
            ("canela", C_PERNA, 1.6, 3.6, 5.5, 8.5, True),
            ("tornozeleira", C_ARM, 1.1, 4.1, 3.5, 5.5, True),
            ("pé", C_PERNA, 0.2, 6.0, 0, 3.5, True),
        ],
        # polígonos (nome, cor, [(x, y), ...]) espelhados
        "frente_poligonos": [
            ("capa", C_CAPA, [(10.5, 29.5), (11.8, 22), (13, 16), (14.6, 9), (14, 3), (13, 1.5), (5, 1.5),
                              (5, 15), (5, 22), (5, 26)]),
        ],
        # (nome, cor, z0, z1, y0, y1)
        "lado_caixas": [
            ("cabeça", C_CAB, -6.5, 0, 31, 39),
            ("bico", C_CAB, -11, -6.5, 30.5, 34),
            ("pescoço", C_TRONCO, -6, -1, 28, 31),
            ("tronco", C_TRONCO, -9.5, 2.5, 15, 29.5),
            ("ombreira", C_ARM, -4.5, 4.5, 26, 29.5),
            ("coxa", C_PERNA, -2.5, 2.5, 10.5, 15),
            ("joelheira", C_ARM, -1.5, 1.5, 8.5, 10.5),
            ("canela", C_PERNA, -2, 0, 5.5, 8.5),
            ("tornozeleira", C_ARM, -3, 0, 3.5, 5.5),
            ("pé", C_PERNA, -8, 1.5, 0, 3.5),
        ],
        "lado_poligonos": [
            ("crista", C_CAB, [(-5, 39), (-3, 41), (2.5, 45), (5, 41), (12, 36.5), (6, 33), (0, 33)]),
            ("capa", C_CAPA, [(-3, 29.5), (4, 30), (9, 22), (13.5, 7), (12, 1.5), (5, 1.5), (0, 9), (-3, 18)]),
        ],
        # cadeias (nome, cor, [(z, y), ...]) desenhadas como linhas grossas com contas
        # cauda definida pelo dono: 3 tranças retas para baixo, encostadas por fora da capa (seguem a inclinação dela)
        "lado_cadeias": [
            ("trança central", C_CAUDA, [(7.2, 24), (11.6, 9.7), (14.0, 2.0)]),
            ("tranças laterais", C_CAUDA, [(7.2, 24), (9.8, 15.4), (11.9, 8.0)]),
        ],
    },
}


def fonte(t):
    for f in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVuSans.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(f, t)
        except OSError:
            pass
    return ImageFont.load_default()


def painel(ficha, vista, cfg, z_lado, Z=3):
    """Recorta a vista, amplia Z vezes e devolve (imagem RGBA, função u->px)."""
    x0, y0, x1, y1 = vista["recorte"]
    s = (vista["chao"] - vista["topo"]) / cfg["altura_u"]          # px da ficha por unidade
    ref_x = vista["z0_x"] if z_lado else vista["centro_x"]
    base = ficha.crop((x0, y0, x1, y1)).resize(((x1 - x0) * Z, (y1 - y0) * Z), Image.LANCZOS).convert("RGBA")
    # clareia um pouco a arte para as linhas aparecerem
    base = Image.blend(base, Image.new("RGBA", base.size, (255, 255, 255, 255)), 0.30)

    def p(h, v):
        return ((ref_x + h * s - x0) * Z, (vista["chao"] - v * s - y0) * Z)
    return base, p, s * Z


def desenhar_regua(d, p, alt, larg, f):
    """Régua de alturas à esquerda: traço a cada 1 u, número a cada 5 u, linha de bloco a cada 16 u."""
    for v in range(0, int(alt) + 1):
        _, y = p(0, v)
        L = 14 if v % 5 == 0 else 6
        d.line([(0, y), (L, y)], fill=(30, 30, 30, 255), width=1)
        if v % 5 == 0:
            d.text((16, y - 7), f"{v}", fill=(30, 30, 30, 255), font=f)
    for b in (1, 2):
        _, y = p(0, 16 * b)
        d.line([(0, y), (larg, y)], fill=(0, 140, 200, 150), width=1)
        d.text((34, y - 15), f"{b} bloco{'s' if b > 1 else ''}", fill=(0, 110, 170, 255), font=f)


def render(nome):
    cfg = PLANTAS[nome]
    ficha = Image.open(RAIZ / cfg["ficha"]).convert("RGB")
    f = fonte(13); fm = fonte(11); ft = fonte(18)
    paineis = []
    for lado in (False, True):
        vista = cfg["lado" if lado else "frente"]
        base, p, upx = painel(ficha, vista, cfg, lado)
        cam = Image.new("RGBA", base.size, (0, 0, 0, 0)); d = ImageDraw.Draw(cam)
        # marcos de altura
        for v, rot in cfg["marcos"]:
            _, y = p(0, v)
            d.line([(0, y), (base.width, y)], fill=(0, 0, 0, 70), width=1)
        # polígonos e caixas
        polis = cfg["lado_poligonos" if lado else "frente_poligonos"]
        for nm, cor, pts in polis:
            lados = (1,) if lado else (1, -1)
            for sx in lados:
                xy = [p(sx * a, b) for a, b in pts]
                d.polygon(xy, fill=cor + (40,), outline=cor + (230,))
        for cx in cfg["lado_caixas" if lado else "frente_caixas"]:
            if lado:
                nm, cor, a0, a1, b0, b1 = cx; esp = False
            else:
                nm, cor, a0, a1, b0, b1, esp = cx
            for sx in ((1, -1) if esp else (1,)):
                xa, ya = p(sx * a0, b1); xb, yb = p(sx * a1, b0)
                d.rectangle([min(xa, xb), ya, max(xa, xb), yb], fill=cor + (45,), outline=cor + (255,), width=2)
        if lado:
            for nm, cor, pts in cfg["lado_cadeias"]:
                xy = [p(a, b) for a, b in pts]
                d.line(xy, fill=cor + (220,), width=max(3, int(upx * 1.5)))
                for (a, b) in pts:
                    x, y = p(a, b); r = upx * 0.9
                    d.ellipse([x - r, y - r, x + r, y + r], outline=(120, 0, 20, 255), width=2)
            # eixo z = 0 (pivô do quadril)
            x, _ = p(0, 0)
            d.line([(x, 0), (x, base.height)], fill=(255, 140, 0, 160), width=1)
        else:
            x, _ = p(0, 0)
            d.line([(x, 0), (x, base.height)], fill=(0, 0, 0, 90), width=1)
        desenhar_regua(d, p, cfg["altura_u"], base.width, fm)
        img = Image.alpha_composite(base, cam)
        paineis.append((img, p, "LADO (frente para a esquerda = -z)" if lado else "FRENTE"))

    # rótulos dos marcos numa coluna à direita
    larg_rot = 250
    H = max(i.height for i, _, _ in paineis) + 70
    W = sum(i.width for i, _, _ in paineis) + larg_rot + 30
    out = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(out)
    d.text((10, 8), cfg["titulo"], fill=(20, 20, 20), font=ft)
    x = 10
    for img, p, rot in paineis:
        out.paste(img, (x, 50), img); d.text((x + 40, 34), rot, fill=(60, 60, 60), font=f)
        x += img.width + 10
    p = paineis[-1][1]
    for v, rot in cfg["marcos"]:
        _, y = p(0, v)
        d.text((x + 4, 50 + y - 8), f"{v:>4} u  {rot}", fill=(30, 30, 30), font=fm)
    # legenda de cores
    ly = H - 16
    lx = 10
    for nm, cor in (("cabeça/crista", C_CAB), ("tronco", C_TRONCO), ("armadura", C_ARM), ("capa/asas", C_CAPA),
                    ("pernas", C_PERNA), ("cauda", C_CAUDA)):
        d.rectangle([lx, ly - 2, lx + 12, ly + 10], fill=cor); d.text((lx + 16, ly - 3), nm, fill=(30, 30, 30), font=fm)
        lx += 120
    destino = RAIZ / "modelos" / cfg["pasta"] / f"{cfg['saida']}.png"
    out.save(destino)
    print("gravado", destino.relative_to(RAIZ))


if __name__ == "__main__":
    for n in (sys.argv[1:] or list(PLANTAS)):
        render(n)
