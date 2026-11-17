"""Compara a silhueta do modelo com as 4 vistas da ficha (`<NNN_id>_vistas.png`).

Para cada vista (Frente, Lateral Direita, Traseira, Lateral Esquerda):
- recorta a criatura da ficha (separa do fundo escuro e tira as legendas);
- renderiza o modelo no mesmo ângulo, na mesma altura e com os pés alinhados;
- mede a sobreposição das silhuetas (IoU de 0 a 100%).

Grava `modelos/<id>/revisao/<prefixo>_comp.png`, com 3 linhas por vista:
1. a ficha com o contorno do modelo em ciano por cima;
2. o modelo no mesmo tamanho;
3. o mapa de diferença: vermelho = falta no modelo, azul = sobra no modelo, cinza = bate;
4. o mapa de cor/detalhe: em células de 8 px, verde = a cor do modelo bate com a da ficha naquele ponto, vermelho =
   cor ou detalhe errado (olho, bico, padrão, faixa no lugar errado ou da cor errada).

Também imprime o IoU e a nota de cor/detalhe de cada vista e as médias, para acompanhar a evolução entre rodadas.

Uso: python comparar_ficha.py <id> [arquivo.bbmodel] [prefixo]
     (padrão: modelos/<id>/<id>.bbmodel e prefixo "atual")"""
import sys
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))
import previa2

VISTAS = [("Frente", 0), ("Lateral Direita", 90), ("Traseira", 180), ("Lateral Esquerda", -90)]
MAGENTA = (255, 0, 255)
ALT = 300   # altura de trabalho das máscaras, em pixels


def componentes(m):
    """Rotula componentes conexos (4-vizinhança) de uma máscara booleana; devolve (rótulos, tamanhos)."""
    H, W = m.shape
    rot = np.zeros((H, W), np.int32); tam = [0]
    for y0, x0 in zip(*np.nonzero(m)):
        if rot[y0, x0]: continue
        n = len(tam); tam.append(0); fila = deque([(y0, x0)]); rot[y0, x0] = n
        while fila:
            y, x = fila.popleft(); tam[n] += 1
            for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= yy < H and 0 <= xx < W and m[yy, xx] and not rot[yy, xx]:
                    rot[yy, xx] = n; fila.append((yy, xx))
    return rot, tam


def preencher(m):
    """Fecha buracos internos: tudo que não é alcançável do fundo pela borda vira parte da máscara."""
    fora = ~m; H, W = m.shape
    alc = np.zeros_like(m); fila = deque()
    for y in range(H):
        for x in (0, W - 1):
            if fora[y, x] and not alc[y, x]: alc[y, x] = True; fila.append((y, x))
    for x in range(W):
        for y in (0, H - 1):
            if fora[y, x] and not alc[y, x]: alc[y, x] = True; fila.append((y, x))
    while fila:
        y, x = fila.popleft()
        for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if 0 <= yy < H and 0 <= xx < W and fora[yy, xx] and not alc[yy, xx]:
                alc[yy, xx] = True; fila.append((yy, xx))
    return ~alc


def morfo(m, r, fechar=True):
    """Fechamento (ou abertura) morfológico com um quadrado de lado 2r+1."""
    im = Image.fromarray((m * 255).astype(np.uint8))
    a, b = (ImageFilter.MaxFilter, ImageFilter.MinFilter) if fechar else (ImageFilter.MinFilter, ImageFilter.MaxFilter)
    im = im.filter(a(2 * r + 1)).filter(b(2 * r + 1))
    return np.array(im) > 127


def mascara_ficha(img):
    """Recorta a criatura de uma coluna da folha de vistas: o fundo é escuro com grade fraca, a criatura é mais
    clara ou mais saturada. Fica o maior componente e os pedaços próximos dele (sem as legendas, que ficam embaixo)."""
    a = np.asarray(img.convert("RGB")).astype(np.float32)
    H, W, _ = a.shape
    borda = np.concatenate([a[:6].reshape(-1, 3), a[-6:].reshape(-1, 3), a[:, :6].reshape(-1, 3), a[:, -6:].reshape(-1, 3)])
    fundo = np.median(borda, axis=0)
    d = np.sqrt(((a - fundo) ** 2).sum(-1))
    lum = a.max(-1)
    m = (d > 38) & (lum > 45)
    m = morfo(m, 1, fechar=False)          # tira a grade fina e o ruído
    m = morfo(m, 3)                        # junta as peças da criatura
    rot, tam = componentes(m)
    if len(tam) < 2: return m
    k = int(np.argmax(tam[1:])) + 1
    ys, xs = np.nonzero(rot == k)
    y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    alt = y1 - y0
    keep = rot == k
    for n in range(1, len(tam)):
        if n == k or tam[n] < 0.002 * tam[k]: continue
        yy, xx = np.nonzero(rot == n)
        # partes soltas (penas, chamas, espinhos) que ficam junto da criatura, não abaixo dela (legendas)
        # (e que não encostam na beira da coluna: isso é a cauda ou a asa da vista vizinha)
        if xx.min() <= 1 or xx.max() >= W - 2 or yy.min() <= 1: continue
        if yy.min() < y1 - 0.02 * alt and xx.max() > x0 - 0.15 * alt and xx.min() < x1 + 0.15 * alt:
            keep |= rot == n
    return preencher(keep)


def recortar(m):
    ys, xs = np.nonzero(m)
    return m[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def normalizar(m, alt=ALT):
    """Escala a máscara recortada para a altura 'alt' (mantendo a proporção)."""
    m = recortar(m); h, w = m.shape
    nw = max(1, round(w * alt / h))
    return np.array(Image.fromarray((m * 255).astype(np.uint8)).resize((nw, alt), Image.NEAREST)) > 127


def iou_alinhado(a, b):
    """Coloca as duas máscaras (mesma altura, pés alinhados) lado a lado e procura o deslocamento horizontal de melhor
    sobreposição. Devolve (iou, A, B) já no mesmo quadro."""
    H = a.shape[0]; W = max(a.shape[1], b.shape[1]) + 40
    melhor = (-1, None, None)
    for dx in range(-20, 21, 2):
        A = np.zeros((H, W), bool); B = np.zeros((H, W), bool)
        ax = (W - a.shape[1]) // 2; bx = (W - b.shape[1]) // 2 + dx
        if bx < 0 or bx + b.shape[1] > W: continue
        A[:, ax:ax + a.shape[1]] = a; B[:, bx:bx + b.shape[1]] = b
        iou = (A & B).sum() / max(1, (A | B).sum())
        if iou > melhor[0]: melhor = (iou, A, B)
    return melhor


def contorno(m, r=1):
    """Borda da máscara, com 2r+1 pixels de espessura."""
    im = Image.fromarray((m * 255).astype(np.uint8))
    erodida = np.array(im.filter(ImageFilter.MinFilter(2 * r + 1))) > 127
    return m & ~erodida


CEL = 8   # lado da célula de comparação de cor, em pixels (a vista tem ALT = 300 de altura)


def comparar_cores(ref, mod, A, B):
    """Nota de cor/detalhe: divide o quadro em células de CEL px; onde ficha e modelo cobrem a célula, compara a cor
    média (distância RGB ponderada). Devolve (nota 0..1, mapa: verde = bate, amarelo = perto, vermelho = errado).
    Células onde só um dos dois tem conteúdo não entram (isso já é medido pelo IoU). Antes, o brilho do modelo é
    igualado ao da ficha por um ganho único (a luz da prévia escurece as vistas de lado e de trás)."""
    H, W = A.shape
    mapa = np.full((H, W, 3), (14, 10, 12), np.uint8)
    # a luz da prévia escurece as faces de lado e de trás; um ganho único de brilho por vista compensa isso,
    # para a nota medir cor e desenho, não a iluminação do renderizador
    sel = A & B
    if sel.any():
        lr = np.median(ref[sel].astype(float) @ np.array([0.30, 0.59, 0.11]))
        lm = np.median(mod[sel].astype(float) @ np.array([0.30, 0.59, 0.11]))
        ganho = float(np.clip(lr / max(lm, 1.0), 0.8, 1.6))
        mod = np.clip(mod.astype(float) * ganho, 0, 255)
    pesos = np.array([0.30, 0.59, 0.11]) * 3
    notas = []
    for y in range(0, H - CEL + 1, CEL):
        for x in range(0, W - CEL + 1, CEL):
            a = A[y:y + CEL, x:x + CEL]; b = B[y:y + CEL, x:x + CEL]
            ambos = a & b
            if ambos.mean() < 0.6: continue
            cr = ref[y:y + CEL, x:x + CEL][ambos].astype(float).mean(0)
            cm = mod[y:y + CEL, x:x + CEL][ambos].astype(float).mean(0)
            d = float(np.sqrt((((cr - cm) ** 2) * pesos).sum()))
            n = max(0.0, 1 - d / 140)
            notas.append(n)
            mapa[y:y + CEL, x:x + CEL] = (int(255 * min(1, 2 * (1 - n))), int(255 * min(1, 2 * n)), 40)
    return (sum(notas) / len(notas) if notas else 0.0), mapa


def comparar(id_, bbmodel=None, prefixo="atual"):
    ref = next((RAIZ / "modelos" / "referencias").glob(f"*_{id_}_vistas.png"))
    folha = Image.open(ref).convert("RGB")
    FW, FH = folha.size
    # tira a moldura e o título (faixa de cima) da folha
    corpo = folha.crop((int(FW * 0.02), int(FH * 0.14), int(FW * 0.98), int(FH * 0.97)))
    CW, CH = corpo.size
    bbmodel = Path(bbmodel) if bbmodel else RAIZ / "modelos" / id_ / f"{id_}.bbmodel"
    q = previa2.carregar(str(bbmodel))
    colunas, notas, cores = [], [], []
    for i, (nome, yaw) in enumerate(VISTAS):
        col = corpo.crop((i * CW // 4, 0, (i + 1) * CW // 4, CH))
        mr = mascara_ficha(col)
        img_m = previa2.desenhar(q, yaw, 0, escala=10, fundo=MAGENTA, ss=1, margem=4)
        am = np.asarray(img_m).astype(int)
        mm_ = np.abs(am - np.array(MAGENTA)).sum(-1) > 60
        a = normalizar(mr); b = normalizar(mm_)
        iou, A, B = iou_alinhado(a, b)
        notas.append(iou)
        # imagens: ficha recortada no mesmo quadro, com o contorno do modelo
        ys, xs = np.nonzero(mr)
        cr = col.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
        cr = cr.resize((a.shape[1], ALT), Image.LANCZOS)
        H, W = A.shape
        base = Image.new("RGB", (W, H), (14, 10, 12))
        ax = (W - a.shape[1]) // 2
        base.paste(cr, (ax, 0))
        b0 = np.asarray(base).copy()
        b1 = b0.copy(); b1[contorno(B)] = (0, 255, 255)
        # modelo no mesmo quadro
        ys, xs = np.nonzero(mm_)
        mc = img_m.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1)).resize((b.shape[1], ALT), Image.LANCZOS)
        mc_a = np.asarray(mc).copy(); mc_a[~b] = (14, 10, 12)
        b2 = np.full((H, W, 3), (14, 10, 12), np.uint8)
        bx = int(np.nonzero(B.any(0))[0].min())
        b2[:, bx:bx + b.shape[1]] = mc_a
        # diferença
        b3 = np.full((H, W, 3), (14, 10, 12), np.uint8)
        b3[A & B] = (110, 110, 110); b3[A & ~B] = (230, 50, 50); b3[B & ~A] = (60, 110, 240)
        # cor e detalhe: em células pequenas onde ficha e modelo têm conteúdo, compara a cor média
        cor, b4 = comparar_cores(b0, b2, A, B)
        cores.append(cor)
        col_img = Image.new("RGB", (W, 4 * H + 80), (14, 10, 12))
        for j, arr in enumerate((b1, b2, b3, b4)):
            col_img.paste(Image.fromarray(arr), (0, 30 + j * (H + 10)))
        ImageDraw.Draw(col_img).text((4, 6), f"{nome}  IoU {iou * 100:.0f}%  cor {cor * 100:.0f}%", fill=(235, 235, 235))
        colunas.append(col_img)
    tot = Image.new("RGB", (sum(c.width for c in colunas) + 12 * 4, max(c.height for c in colunas)), (14, 10, 12))
    x = 0
    for c in colunas: tot.paste(c, (x, 0)); x += c.width + 12
    media = sum(notas) / len(notas); media_cor = sum(cores) / len(cores)
    ImageDraw.Draw(tot).text((4, tot.height - 18), f"{id_} {prefixo}: IoU medio {media * 100:.1f}%  cor/detalhe {media_cor * 100:.1f}%  "
                             "(linha 3: vermelho = falta, azul = sobra; linha 4: verde = cor bate, vermelho = cor/detalhe errado)",
                             fill=(235, 235, 235))
    destino = RAIZ / "modelos" / id_ / "revisao" / f"{prefixo}_comp.png"
    destino.parent.mkdir(parents=True, exist_ok=True)
    tot.save(destino)
    print(f"{id_} {prefixo}: IoU " + "  ".join(f"{n}={v * 100:.0f}%" for (n, _), v in zip(VISTAS, notas))
          + f"  media={media * 100:.1f}% | cor " + "  ".join(f"{v * 100:.0f}%" for v in cores)
          + f"  media_cor={media_cor * 100:.1f}%  -> {destino}")
    return media


if __name__ == "__main__":
    a = sys.argv[1:]
    bb = next((x for x in a[1:] if x.endswith(".bbmodel")), None)
    pref = next((x for x in a[1:] if not x.endswith(".bbmodel")), "atual")
    comparar(a[0], bb, pref)
