"""Monta, num comando só, tudo o que o crítico precisa ver de um modelo .geo.json, e as perguntas já com as medidas.

Grava em --saida:
  1_vistas.png        frente, lado, costas e 3/4 na pose `parado` (com as vistas da ficha em cima, se houver)
  2_rosto.png         só a cabeça, ampliada, de frente, em 3/4 e de lado (e com o olho fechado, se houver `piscar`)
  3_arte.png          arte | modelo no melhor ângulo | sobreposição (com --arte)
  4_escala_jogo.png   o modelo do tamanho que aparece na tela a 4, 8, 16 e 32 blocos (tela de 1080 linhas, FOV 70)
  5_animacoes.png     parado e andar em 4 quadros do ciclo (vista 3/4)
  perguntas.md        as medidas (estilo, IoU, peças soltas) e as perguntas do crítico para responder

Uso:
  python folha_critica.py MODELO.geo.json TEXTURA.png --anim ARQ.animation.json --saida PASTA
         [--arte ARTE.png] [--pose-arte render] [--ficha-vistas VISTAS.png] [--escala-jogo 1.0] [--cabeca OSSO]
"""
import argparse, copy, json, math, sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import pecas_soltas as ps  # noqa: E402  (também acha analisar_geo/previa2)
import analisar_geo as ag  # noqa: E402
import previa2  # noqa: E402

FUNDO = ag.FUNDO
CEU, GRAMA = (134, 176, 232), (96, 140, 66)
CABECAS = ("head", "cabeca", "cabeça")


# ----------------------------------------------------------------------------------------------------------------
# Ajudantes
# ----------------------------------------------------------------------------------------------------------------
def achar_anim(anims, chave):
    """Nome completo da animação para 'parado', 'andar', 'piscar' ou um nome curto (render, ground_idle...)."""
    nomes = ag.ALIAS_ANIM.get(chave, (chave,))
    return next((k for k in anims if k.split(".")[-1] in nomes), None)


def pose_de(anims, chave, fracao=0.0):
    k = achar_anim(anims, chave)
    if not k:
        return None, None
    dur = float(anims[k].get("animation_length") or 0)
    return ag.pose(anims[k], dur * fracao), dur


def so_subarvore(geo, raiz):
    """Cópia do modelo em que só os cubos da subárvore de `raiz` ficam (a hierarquia continua, para a pose)."""
    filhos = {}
    for o in geo["ossos"]:
        filhos.setdefault(o.get("parent"), []).append(o["name"])
    manter, pilha = set(), [raiz]
    while pilha:
        n = pilha.pop(); manter.add(n); pilha += filhos.get(n, [])
    g = copy.deepcopy(geo)
    for o in g["ossos"]:
        if o["name"] not in manter:
            o["cubes"] = []
    return g


def altura_px(dados):
    lo, hi = ag.limites(dados)
    return max(hi[1] - lo[1], 1.0)


def rotulada(img, texto, fundo=FUNDO, cor=(220, 220, 220)):
    f = ag.fonte(14)
    saida = Image.new("RGB", (max(img.width, 120), img.height + 24), fundo)
    saida.paste(img, (0, 24)); ImageDraw.Draw(saida).text((6, 4), texto, fill=cor, font=f)
    return saida


def lado_a_lado(imgs, fundo=FUNDO, vao=8):
    H = max(i.height for i in imgs); W = sum(i.width for i in imgs) + vao * (len(imgs) - 1)
    f = Image.new("RGB", (W, H), fundo); x = 0
    for i in imgs:
        f.paste(i, (x, H - i.height)); x += i.width + vao
    return f


def empilhar(imgs, fundo=FUNDO, vao=10):
    W = max(i.width for i in imgs); H = sum(i.height for i in imgs) + vao * (len(imgs) - 1)
    f = Image.new("RGB", (W, H), fundo); y = 0
    for i in imgs:
        f.paste(i, (0, y)); y += i.height + vao
    return f


# ----------------------------------------------------------------------------------------------------------------
# As folhas
# ----------------------------------------------------------------------------------------------------------------
def folha_vistas(dados, ficha_vistas=None):
    esc = 560 / altura_px(dados)
    vistas = ag.folha_vistas(dados, escala=esc, titulo="modelo na pose parado (frente, lado, costas, 3/4)")
    if ficha_vistas:
        f = Image.open(ficha_vistas).convert("RGB")
        f = f.resize((vistas.width, int(f.height * vistas.width / f.width)), Image.LANCZOS)
        return empilhar([rotulada(f, "vistas da ficha"), vistas])
    return vistas


def folha_rosto(geo, tex, pose, cabeca, pose_piscar=None):
    g = so_subarvore(geo, cabeca)
    dados = ag.faces(g, tex, pose)
    esc = 300 / altura_px(dados)
    quadros = [rotulada(previa2.desenhar(dados, y, p, escala=esc, fundo=FUNDO), n)
               for n, y, p in (("frente", 0, -5), ("3/4", 35, -8), ("lado", 90, -5))]
    if pose_piscar is not None:
        dp = ag.faces(g, tex, pose_piscar)
        quadros.append(rotulada(previa2.desenhar(dp, 0, -5, escala=esc, fundo=FUNDO), "piscar (meio)"))
    return lado_a_lado(quadros)


def folha_escala(dados, escala_jogo=1.0):
    """Tamanho na tela de 1080 linhas com FOV 70: px por bloco = 1080 / (2·tan 35°·distância)."""
    quadros = []
    for dist in (4, 8, 16, 32):
        px_bloco = 1080 / (2 * math.tan(math.radians(35)) * dist)
        img = previa2.desenhar(dados, 35, -12, escala=px_bloco / 16 * escala_jogo, margem=6, fundo=CEU)
        caixa = Image.new("RGB", (max(img.width, 90), img.height + 30), CEU)
        ImageDraw.Draw(caixa).rectangle([0, img.height - 4, caixa.width, caixa.height], fill=GRAMA)
        caixa.paste(img, (0, 0))
        ImageDraw.Draw(caixa).text((4, img.height + 8), f"{dist} blocos", fill=(255, 255, 255), font=ag.fonte(13))
        quadros.append(caixa)
    return lado_a_lado(quadros, fundo=CEU, vao=16)


def folha_animacoes(geo, tex, anims):
    linhas = []
    for chave in ("parado", "andar"):
        k = achar_anim(anims, chave)
        if not k:
            continue
        dur = float(anims[k].get("animation_length") or 1)
        quadros = []
        for fr in (0, 0.25, 0.5, 0.75):
            d = ag.faces(geo, tex, ag.pose(anims[k], dur * fr))
            quadros.append((fr, d))
        esc = 260 / max(altura_px(d) for _, d in quadros)
        imgs = [rotulada(previa2.desenhar(d, 35, -12, escala=esc, fundo=FUNDO), f"{chave} {int(fr * 100)}%")
                for fr, d in quadros]
        linhas.append(lado_a_lado(imgs))
    return empilhar(linhas) if linhas else None


def folha_arte(arte_path, geo, tex, anims, nome_pose, saida):
    import comparar_arte as ca
    arte = Image.open(arte_path)
    pose = None
    if nome_pose:
        k = achar_anim(anims, nome_pose)
        pose = ag.pose(anims[k], 0) if k else None
    dados = ag.faces(geo, tex, pose)
    alvo = ca.normalizar(ca.silhueta_arte(arte))
    _, yaw, pitch, esp = ca.melhor_angulo(dados, alvo, yaws=range(-90, 91, 10), pitches=(-10, 0, 10))
    return ca.folha(arte, dados, yaw, pitch, esp, saida, f"pose {nome_pose or 'neutra'}"), yaw, pitch


# ----------------------------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("modelo"); ap.add_argument("textura")
    ap.add_argument("--anim", help="arquivo .animation.json")
    ap.add_argument("--saida", required=True, help="pasta de saída (use uma rodada nova em revisao/)")
    ap.add_argument("--arte", help="arte com fundo transparente ou branco (recortar_arte.py)")
    ap.add_argument("--pose-arte", default="render", help="animação que recria a pose da arte (padrão: render)")
    ap.add_argument("--ficha-vistas", help="imagem com as vistas ortográficas da ficha")
    ap.add_argument("--escala-jogo", type=float, default=1.0, help="escala aplicada no jogo")
    ap.add_argument("--cabeca", help="osso da cabeça (padrão: head/cabeca)")
    a = ap.parse_args()

    out = Path(a.saida); out.mkdir(parents=True, exist_ok=True)
    geo = ag.carregar_geo(a.modelo); tex = ag.carregar_textura(a.textura)
    anims = json.loads(Path(a.anim).read_text(encoding="utf-8"))["animations"] if a.anim else {}
    pose_parado, _ = pose_de(anims, "parado")
    dados = ag.faces(geo, tex, pose_parado)
    medidas, imagens = [], []

    folha_vistas(dados, a.ficha_vistas).save(out / "1_vistas.png"); imagens.append("1_vistas.png")
    nomes = [o["name"] for o in geo["ossos"]]
    cabeca = a.cabeca or next((n for n in nomes if n.lower() in CABECAS), None)
    if cabeca:
        pose_piscar, _ = pose_de(anims, "piscar", 0.5)
        if pose_piscar is not None and pose_parado:
            pose_piscar = {**pose_parado, **pose_piscar}
        folha_rosto(geo, tex, pose_parado, cabeca, pose_piscar).save(out / "2_rosto.png"); imagens.append("2_rosto.png")
    else:
        medidas.append("- rosto: não achei o osso da cabeça (use --cabeca)")
    if a.arte:
        nota, yaw, pitch = folha_arte(a.arte, geo, tex, anims, a.pose_arte, out / "3_arte.png")
        imagens.append("3_arte.png")
        medidas.append(f"- sobreposição com a arte (IoU), pose `{a.pose_arte}`: **{100 * nota:.0f}%** "
                       f"(yaw {yaw}, pitch {pitch}; meta ≥ 60%)")
    folha_escala(dados, a.escala_jogo).save(out / "4_escala_jogo.png"); imagens.append("4_escala_jogo.png")
    fa = folha_animacoes(geo, tex, anims)
    if fa:
        fa.save(out / "5_animacoes.png"); imagens.append("5_animacoes.png")

    linhas = ag.conferir_estilo(geo, tex, ag.faces(geo, tex), anims or None, a.escala_jogo)
    falhas = [f"{c} (alvo {alvo}, medido {v})" for c, alvo, v, ok in linhas if not ok]
    medidas.append(f"- guia de estilo: **{sum(ok for *_, ok in linhas)} de {len(linhas)}** critérios"
                   + (f"; falham: {'; '.join(falhas)}" if falhas else ""))
    _, problemas = ps.conferir(geo, anims)
    medidas.append(f"- peças soltas e chão: **{len(problemas)} aviso(s)**"
                   + "".join(f"\n  - {p}" for p in problemas[:12])
                   + (f"\n  - ... e mais {len(problemas) - 12}" if len(problemas) > 12 else ""))

    perguntas = (AQUI.parent / "references" / "perguntas_critico.md").read_text(encoding="utf-8")
    perguntas = perguntas.split("\n", 1)[1] if perguntas.startswith("# ") else perguntas
    texto = [f"# Folha do crítico: {Path(a.modelo).name}", "",
             "## Medidas", *medidas, "",
             "## Imagens", *[f"- `{i}`" for i in imagens], "",
             perguntas.strip(), ""]
    (out / "perguntas.md").write_text("\n".join(texto), encoding="utf-8")
    print("\n".join(medidas))
    print(f"\nfolha em {out}/: " + ", ".join(imagens) + ", perguntas.md")


if __name__ == "__main__":
    main()
