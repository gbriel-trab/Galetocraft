"""Compara um modelo .geo.json com UMA ilustração (arte oficial ou ficha no estilo "arte de Pokédex").

É o método para modelar a partir de uma imagem só (modelos/GUIA_ESTILO.md, seção 13):
1. procura o ângulo de câmera (yaw, pitch, espelhado ou não) em que a silhueta do modelo, numa pose de animação,
   mais se sobrepõe à silhueta da arte (IoU);
2. compara a paleta da arte (cores dominantes, sem o contorno preto) com as cores da textura;
3. grava uma folha: arte | modelo no mesmo ângulo | sobreposição (vermelho = falta no modelo, azul = sobra).

A arte precisa de fundo transparente ou branco liso.

Uso:
  python comparar_arte.py ARTE.png MODELO.geo.json TEXTURA.png [--anim ARQ.animation.json --pose NOME[@t]]
                          [--saida folha.png] [--yaw Y --pitch P] [--espelhar]
"""
import argparse, json, math, sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import analisar_geo as ag  # noqa: E402
import previa2  # noqa: E402

MAGENTA = (255, 0, 255)
LADO = 220          # altura do quadro comum onde as silhuetas são comparadas


# ----------------------------------------------------------------------------------------------------------------
# Silhuetas
# ----------------------------------------------------------------------------------------------------------------
def silhueta_arte(img):
    a = np.asarray(img.convert("RGBA")).astype(int)
    if a[..., 3].min() < 250:
        return a[..., 3] > 40
    return ~(a[..., :3] > 242).all(-1)


def recortar(mascara):
    ys, xs = np.where(mascara)
    return mascara[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def normalizar(mascara, lado=LADO):
    """Recorta na caixa da silhueta e escala para `lado` px de altura, centralizada num quadro lado x (2*lado)."""
    m = recortar(mascara)
    h, w = m.shape
    k = lado / h
    img = Image.fromarray((m * 255).astype(np.uint8)).resize((max(1, int(round(w * k))), lado), Image.NEAREST)
    q = np.zeros((lado, 2 * lado), bool)
    arr = np.asarray(img) > 127
    w2 = min(arr.shape[1], 2 * lado)
    x0 = (2 * lado - w2) // 2
    q[:, x0:x0 + w2] = arr[:, :w2]
    return q


def iou(a, b):
    return (a & b).sum() / max(1, (a | b).sum())


def silhueta_modelo(dados, yaw, pitch, escala=5):
    img = previa2.desenhar(dados, yaw, pitch, escala=escala, margem=2, ss=1, fundo=MAGENTA)
    a = np.asarray(img.convert("RGB")).astype(int)
    return ~((a[..., 0] > 250) & (a[..., 1] < 5) & (a[..., 2] > 250))


def melhor_angulo(dados, alvo, yaws=range(-180, 180, 10), pitches=(-20, -10, 0, 10, 20)):
    """(iou, yaw, pitch, espelhado) com a maior sobreposição; depois refina em passos de 3°."""
    def nota(y, p):
        m = silhueta_modelo(dados, y, p)
        n = normalizar(m)
        return max((iou(n, alvo), False), (iou(n[:, ::-1], alvo), True))
    melhor = (-1, 0, 0, False)
    for y in yaws:
        for p in pitches:
            v, esp = nota(y, p)
            if v > melhor[0]: melhor = (v, y, p, esp)
    _, y0, p0, _ = melhor
    for y in range(y0 - 6, y0 + 7, 3):
        for p in range(p0 - 6, p0 + 7, 3):
            v, esp = nota(y, p)
            if v > melhor[0]: melhor = (v, y, p, esp)
    return melhor


# ----------------------------------------------------------------------------------------------------------------
# Paleta
# ----------------------------------------------------------------------------------------------------------------
def cores_dominantes(img, n=10, contorno=70):
    """Cores dominantes da arte (sem o fundo e sem o contorno escuro), com a fração de área de cada uma."""
    a = np.asarray(img.convert("RGBA"))
    m = silhueta_arte(img)
    px = a[..., :3][m]
    lum = 0.299 * px[:, 0] + 0.587 * px[:, 1] + 0.114 * px[:, 2]
    px = px[lum > contorno]
    q = Image.fromarray(px.reshape(1, -1, 3).astype(np.uint8)).quantize(colors=n, method=Image.Quantize.MEDIANCUT)
    pal = np.array(q.getpalette()[:3 * n]).reshape(-1, 3)
    cont = np.bincount(np.asarray(q).ravel(), minlength=n)
    ordem = np.argsort(-cont)
    return [(tuple(int(v) for v in pal[i]), cont[i] / cont.sum()) for i in ordem if cont[i]]


def mais_proxima(cor, paleta):
    d = [math.dist(cor, p) for p in paleta]
    i = int(np.argmin(d))
    return paleta[i], d[i]


# ----------------------------------------------------------------------------------------------------------------
# Folha de comparação
# ----------------------------------------------------------------------------------------------------------------
def folha(arte, dados, yaw, pitch, espelhado, saida, titulo=""):
    F = ag.fonte(15)
    render = previa2.desenhar(dados, yaw, pitch, escala=12, margem=8, fundo=(255, 255, 255))
    if espelhado: render = render.transpose(Image.FLIP_LEFT_RIGHT)
    arte_rgb = Image.new("RGB", arte.size, (255, 255, 255)); arte_rgb.paste(arte.convert("RGB"), mask=arte.convert("RGBA").split()[3])
    a_rec = arte_rgb.crop(Image.fromarray((silhueta_arte(arte) * 255).astype(np.uint8)).getbbox())
    H = 420
    a_rec = a_rec.resize((int(a_rec.width * H / a_rec.height), H), Image.LANCZOS)
    m_bbox = Image.fromarray((~(np.asarray(render) > 250).all(-1) * 255).astype(np.uint8)).getbbox()
    r_rec = render.crop(m_bbox); r_rec = r_rec.resize((int(r_rec.width * H / r_rec.height), H), Image.LANCZOS)
    alvo = normalizar(silhueta_arte(arte), H); mod = normalizar(silhueta_modelo(dados, yaw, pitch), H)
    if espelhado: mod = mod[:, ::-1]
    sob = np.full(alvo.shape + (3,), 255, np.uint8)
    sob[alvo & mod] = (170, 170, 170); sob[alvo & ~mod] = (220, 40, 40); sob[~alvo & mod] = (40, 90, 220)
    sob_img = Image.fromarray(sob).crop(Image.fromarray(((alvo | mod) * 255).astype(np.uint8)).getbbox())
    pecas = [("arte", a_rec), (f"modelo (yaw {yaw}, pitch {pitch}{', espelhado' if espelhado else ''})", r_rec),
             (f"sobreposição: IoU {100 * iou(alvo, mod):.0f}%", sob_img)]
    W = sum(p.width for _, p in pecas) + 40
    f = Image.new("RGB", (W, H + 60), (255, 255, 255)); d = ImageDraw.Draw(f)
    if titulo: d.text((10, 6), titulo, fill=(20, 20, 20), font=F)
    x = 10
    for rot, p in pecas:
        f.paste(p, (x, 50)); d.text((x, 30), rot, fill=(60, 60, 60), font=ag.fonte(13)); x += p.width + 10
    f.save(saida)
    return iou(alvo, mod)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("arte"); ap.add_argument("modelo"); ap.add_argument("textura")
    ap.add_argument("--anim"); ap.add_argument("--pose", help="animação para posar, ex.: render ou ground_idle@0")
    ap.add_argument("--saida", default="comparar_arte.png")
    ap.add_argument("--yaw", type=float); ap.add_argument("--pitch", type=float, default=0)
    ap.add_argument("--espelhar", action="store_true")
    a = ap.parse_args()
    arte = Image.open(a.arte)
    geo = ag.carregar_geo(a.modelo); tex = ag.carregar_textura(a.textura)
    pose = None
    if a.pose:
        anims = json.loads(Path(a.anim).read_text(encoding="utf-8"))["animations"]
        nome, _, t = a.pose.partition("@")
        pose = ag.pose(anims[next(k for k in anims if k.endswith("." + nome))], float(t or 0))
    dados = ag.faces(geo, tex, pose)
    if a.yaw is None:
        v, yaw, pitch, esp = melhor_angulo(dados, normalizar(silhueta_arte(arte)))
    else:
        yaw, pitch, esp = a.yaw, a.pitch, a.espelhar
    nota = folha(arte, dados, yaw, pitch, esp, a.saida, Path(a.modelo).name + (f" / pose {a.pose}" if a.pose else ""))
    print(f"melhor ângulo: yaw {yaw}, pitch {pitch}, espelhado {esp}; IoU da silhueta {100 * nota:.0f}%")
    pal_tex = sorted({tuple(int(v) for v in p[:3]) for p in tex.reshape(-1, 4) if p[3] > 0})
    print("paleta da arte -> cor mais próxima na textura (distância RGB):")
    for cor, frac in cores_dominantes(arte):
        alvo, dist = mais_proxima(cor, pal_tex)
        print(f"  {cor} {100 * frac:4.1f}% da área -> {alvo} ({dist:.0f})")


if __name__ == "__main__":
    main()
