"""Renderiza um modelo Bedrock/GeckoLib (.geo.json + textura .png) em 4 vistas, sem Blockbench.

Independente do resto do projeto: só precisa de numpy e Pillow. Serve para revisar modelos (os nossos e os
gerados por outros chats) e é o mesmo código que vai no prompt de modelagem.

- Lê bones (pivot, rotation, parent), cubes (origin, size, inflate, rotation, pivot, mirror) e UV em caixa
  ("uv": [u, v]) ou por face ("uv": {"north": {"uv": [..], "uv_size": [..]}, ...}).
- Converte para o espaço do Blockbench (x invertido), igual ao Blockbench ao importar.
- Opcional: aplica o 1º quadro de uma animação (ex.: animation.<id>.idle). Só valores numéricos; expressões
  Molang viram o seu valor em q.anim_time = 0 (sin/cos em graus, como no Molang).
- Vistas: frente (rosto para a câmera), lado direito da criatura (frente apontando para a direita da imagem),
  trás, lado esquerdo e 3/4.
- Sombreamento de entidade do Minecraft: topo 1,0; frente/trás 0,8; lados 0,6; baixo 0,5.
- Desenha as faces dos dois lados (sem culling), como o GeckoLib: planos aparecem por trás e faces
  coincidentes piscam aqui também.

Uso: python ferramentas/render_geo.py modelo.geo.json textura.png saida.png [animacao.json nome_da_animacao] [escala]
     [--sem-planos]   (esconde os cubos de espessura 0: teste "massa sólida + franja")
"""
import ast
import json
import math
import re
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont


def rot(rx, ry, rz):
    """Matriz de rotação em graus, ordem do Blockbench: R = Rz·Ry·Rx."""
    a, b, c = (math.radians(v) for v in (rx, ry, rz))
    Rx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
    Ry = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
    Rz = np.array([[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def em_volta(A, pivo, t=(0, 0, 0)):
    """Transformação afim (A, b) que aplica A em volta do pivô e depois translada t."""
    p = np.array(pivo, float)
    return A, p - A @ p + np.array(t, float)


def compor(M, N):
    """M(N(p))."""
    return M[0] @ N[0], M[0] @ N[1] + M[1]


NORMAL = {"north": (0, 0, -1), "south": (0, 0, 1), "east": (1, 0, 0), "west": (-1, 0, 0), "up": (0, 1, 0), "down": (0, -1, 0)}


def canto(face, f, t, u, v):
    """Ponto da face na posição (u, v) de 0 a 1, com (0, 0) no canto de cima à esquerda da textura."""
    (x1, y1, z1), (x2, y2, z2) = f, t
    dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
    return {"north": (x2 - u * dx, y2 - v * dy, z1), "south": (x1 + u * dx, y2 - v * dy, z2),
            "east": (x2, y2 - v * dy, z2 - u * dz), "west": (x1, y2 - v * dy, z1 + u * dz),
            "up": (x1 + u * dx, y2, z1 + v * dz), "down": (x1 + u * dx, y1, z2 - v * dz)}[face]


def uv_caixa(u, v, tam, espelho):
    """Retângulos [u1, v1, u2, v2] de cada face no UV em caixa (box UV) do Minecraft/Blockbench."""
    w, h, d = (math.floor(abs(x) + 1e-4) for x in tam)
    f = {"east": [u, v + d, u + d, v + d + h], "west": [u + d + w, v + d, u + 2 * d + w, v + d + h],
         "up": [u + d + w, v + d, u + d, v], "down": [u + d + 2 * w, v, u + d + w, v + d],
         "south": [u + 2 * d + w, v + d, u + 2 * d + 2 * w, v + d + h], "north": [u + d, v + d, u + d + w, v + d + h]}
    if espelho:
        f["east"], f["west"] = f["west"], f["east"]
        f = {k: [a[2], a[1], a[0], a[3]] for k, a in f.items()}
    return f


# ---------------- Molang mínimo (seguro: só números, operadores e math.*) ----------------
_FUN = {"math.sin": lambda x: math.sin(math.radians(x)), "math.cos": lambda x: math.cos(math.radians(x)),
        "math.abs": abs, "math.clamp": lambda x, a, b: max(a, min(b, x)), "math.lerp": lambda a, b, t: a + (b - a) * t,
        "math.sqrt": lambda x: math.sqrt(max(x, 0)), "math.min": min, "math.max": max, "math.floor": math.floor,
        "math.round": round, "math.pow": pow}


def molang(expr):
    if isinstance(expr, (int, float)):
        return float(expr)
    s = str(expr).strip().lower().replace("query.", "q.").replace("variable.", "v.")

    def nome(n):
        return n.id if isinstance(n, ast.Name) else nome(n.value) + "." + n.attr

    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)): return float(n.value)
        if isinstance(n, ast.UnaryOp): return -ev(n.operand) if isinstance(n.op, ast.USub) else ev(n.operand)
        if isinstance(n, ast.BinOp):
            a, b = ev(n.left), ev(n.right)
            if isinstance(n.op, ast.Add): return a + b
            if isinstance(n.op, ast.Sub): return a - b
            if isinstance(n.op, ast.Mult): return a * b
            if isinstance(n.op, ast.Div): return a / b if b else 0.0
            return 0.0
        if isinstance(n, (ast.Name, ast.Attribute)): return math.pi if nome(n) == "math.pi" else 0.0
        if isinstance(n, ast.Call): return float(_FUN[nome(n.func)](*[ev(x) for x in n.args]))
        return 0.0
    try:
        return ev(ast.parse(s, mode="eval"))
    except Exception:
        return 0.0


def primeiro_quadro(canal):
    if isinstance(canal, dict):
        canal = canal[sorted(canal, key=float)[0]]
        if isinstance(canal, dict):
            canal = canal.get("post", canal.get("pre", [0, 0, 0]))
    if not isinstance(canal, list):
        canal = [canal] * 3
    return [molang(x) for x in canal]


def carregar_animacao(caminho, nome):
    if not caminho:
        return {}
    an = json.load(open(caminho, encoding="utf-8-sig"))["animations"].get(nome, {})
    return {b: {k: primeiro_quadro(v) for k, v in d.items() if k in ("rotation", "position", "scale")}
            for b, d in an.get("bones", {}).items()}


# ---------------- montagem das faces ----------------
def faces_do_modelo(geo, anim=None, ocultos=(), sem_planos=False):
    g = geo["minecraft:geometry"][0]
    anim = anim or {}
    ossos = {b["name"]: b for b in g["bones"]}
    filhos = {}
    for b in g["bones"]:
        filhos.setdefault(b.get("parent"), []).append(b["name"])
    faces = []

    def andar(nome, M):
        b = ossos[nome]
        if nome in ocultos:
            return
        a = anim.get(nome, {})
        p = b.get("pivot", [0, 0, 0]); r = b.get("rotation", [0, 0, 0]); ar = a.get("rotation", [0, 0, 0])
        sc = a.get("scale", [1, 1, 1]); pos = a.get("position", [0, 0, 0])
        if min(abs(x) for x in sc) < 1e-3:
            return
        A = rot(-(r[0] + ar[0]), -(r[1] + ar[1]), r[2] + ar[2]) @ np.diag(sc)
        Mn = compor(M, em_volta(A, (-p[0], p[1], p[2]), (-pos[0], pos[1], pos[2])))
        for c in b.get("cubes", []):
            if sem_planos and min(abs(v) for v in c["size"]) == 0:
                continue
            o, s, i = c["origin"], c["size"], c.get("inflate", 0)
            de = [-(o[0] + s[0]) - i, o[1] - i, o[2] - i]; ate = [-o[0] + i, o[1] + s[1] + i, o[2] + s[2] + i]
            Mc = Mn
            cr = c.get("rotation")
            if cr and any(abs(x) > 1e-9 for x in cr):
                cp = c.get("pivot", [0, 0, 0])
                Mc = compor(Mn, em_volta(rot(-cr[0], -cr[1], cr[2]), (-cp[0], cp[1], cp[2])))
            uv = c.get("uv", [0, 0])
            if isinstance(uv, dict):
                rets = {k: [f["uv"][0], f["uv"][1], f["uv"][0] + f["uv_size"][0], f["uv"][1] + f["uv_size"][1]]
                        for k, f in uv.items()}
            else:
                rets = uv_caixa(uv[0], uv[1], s, c.get("mirror", b.get("mirror", False)))
            for face, ret in rets.items():
                if abs(ret[2] - ret[0]) < 1e-6 or abs(ret[3] - ret[1]) < 1e-6:
                    continue
                pts = [Mc[0] @ np.array(canto(face, de, ate, u, v), float) + Mc[1] for u, v in ((0, 0), (1, 0), (0, 1))]
                faces.append((pts, ret, Mc[0] @ np.array(NORMAL[face], float)))
        for f in filhos.get(nome, []):
            andar(f, Mn)

    for raiz in filhos.get(None, []):
        andar(raiz, (np.eye(3), np.zeros(3)))
    return faces


def tom_minecraft(n):
    n = n / (np.linalg.norm(n) + 1e-9)
    return n[0] ** 2 * 0.6 + n[2] ** 2 * 0.8 + n[1] ** 2 * (1.0 if n[1] > 0 else 0.5)


def desenhar(faces, tex, yaw, pitch=0.0, escala=8, fundo=(235, 235, 230), margem=10, ss=2):
    """Projeção ortográfica com z-buffer. yaw 0 = vista de frente (olhando a face -z do modelo)."""
    V = rot(pitch, 0, 0) @ rot(0, yaw, 0)
    s = escala * ss
    # sem descarte de face traseira, como o GeckoLib (entityCutoutNoCull): o verso dos planos aparece
    proj = [([V @ p for p in pts], uv, n) for pts, uv, n in faces]
    if not proj:
        return Image.new("RGB", (10, 10), fundo)
    xs = [-q[0] for P, _, _ in proj for q in P + [P[1] + P[2] - P[0]]]
    ys = [-q[1] for P, _, _ in proj for q in P + [P[1] + P[2] - P[0]]]
    x0, y0 = min(xs), min(ys)
    W = int((max(xs) - x0) * s) + 2 * margem * ss; H = int((max(ys) - y0) * s) + 2 * margem * ss
    cor = np.zeros((H, W, 3), np.float32); cor[:] = fundo
    zb = np.full((H, W), np.inf, np.float32)
    th, tw = tex.shape[:2]
    for P, (u1, v1, u2, v2), n in proj:
        sp = [np.array([(-q[0] - x0) * s + margem * ss, (-q[1] - y0) * s + margem * ss, q[2]]) for q in P]
        o, e1, e2 = sp[0], sp[1] - sp[0], sp[2] - sp[0]
        det = e1[0] * e2[1] - e1[1] * e2[0]
        if abs(det) < 1e-9:
            continue
        q4 = sp[1] + sp[2] - sp[0]
        bx = [q[0] for q in sp] + [q4[0]]; by = [q[1] for q in sp] + [q4[1]]
        ix0, ix1 = max(int(min(bx)), 0), min(int(math.ceil(max(bx))), W - 1)
        iy0, iy1 = max(int(min(by)), 0), min(int(math.ceil(max(by))), H - 1)
        if ix1 < ix0 or iy1 < iy0:
            continue
        gx, gy = np.meshgrid(np.arange(ix0, ix1 + 1) + .5, np.arange(iy0, iy1 + 1) + .5)
        dx, dy = gx - o[0], gy - o[1]
        u = (dx * e2[1] - dy * e2[0]) / det; v = (e1[0] * dy - e1[1] * dx) / det
        dentro = (u >= 0) & (u <= 1) & (v >= 0) & (v <= 1)
        if not dentro.any():
            continue
        z = o[2] + u * e1[2] + v * e2[2]
        bloco = zb[iy0:iy1 + 1, ix0:ix1 + 1]
        ok = dentro & (z < bloco - 1e-4)
        tu = np.clip(np.floor(u1 + u * (u2 - u1)), min(u1, u2), max(u1, u2) - 1).astype(int).clip(0, tw - 1)
        tv = np.clip(np.floor(v1 + v * (v2 - v1)), min(v1, v2), max(v1, v2) - 1).astype(int).clip(0, th - 1)
        amostra = tex[tv, tu]
        ok &= amostra[..., 3] > 0
        if not ok.any():
            continue
        bloco[ok] = z[ok]
        cor[iy0:iy1 + 1, ix0:ix1 + 1][ok] = amostra[..., :3][ok] * tom_minecraft(n)
    return Image.fromarray(cor.clip(0, 255).astype(np.uint8)).resize((W // ss, H // ss), Image.LANCZOS)


VISTAS = ((0, 0, "frente"), (90, 0, "lado direito"), (180, 0, "tras"), (270, 0, "lado esquerdo"), (35, -20, "3/4"))


def folha(geo_path, png_path, saida, anim_path=None, anim_nome=None, escala=8, vistas=VISTAS, sem_planos=False):
    geo = json.load(open(geo_path, encoding="utf-8-sig"))
    tex = np.asarray(Image.open(png_path).convert("RGBA")).astype(np.float32)
    faces = faces_do_modelo(geo, carregar_animacao(anim_path, anim_nome), sem_planos=sem_planos)
    imgs = []
    for y, p, n in vistas:
        im = desenhar(faces, tex, y, p, escala)
        if im.width < 110:   # vista estreita: alarga o fundo para o rótulo caber
            fundo = Image.new("RGB", (110, im.height), (235, 235, 230)); fundo.paste(im, ((110 - im.width) // 2, 0)); im = fundo
        imgs.append((im, n))
    H = max(i.height for i, _ in imgs) + 22; W = sum(i.width for i, _ in imgs)
    out = Image.new("RGB", (W, H), (235, 235, 230)); d = ImageDraw.Draw(out); x = 0
    try:
        fonte = ImageFont.truetype("DejaVuSans.ttf", 13)
    except OSError:
        fonte = ImageFont.load_default()
    for i, n in imgs:
        out.paste(i, (x, 22)); d.text((x + 5, 4), n, fill=(30, 30, 30), font=fonte); x += i.width
    out.save(saida)
    return out


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if x != "--sem-planos"]
    sem = "--sem-planos" in sys.argv
    if len(a) < 3:
        sys.exit(__doc__)
    anim = a[3] if len(a) > 4 else None
    nome = a[4] if len(a) > 4 else None
    esc = float(a[5]) if len(a) > 5 else (float(a[3]) if len(a) == 4 else 8)
    folha(a[0], a[1], a[2], anim, nome, esc, sem_planos=sem)
    print("gravado", a[2])
