"""Desenha um .bbmodel (cubos + textura embutida) de vários ângulos numa imagem só.
Uso: python previa.py modelo.bbmodel saida.png"""
import base64, io, json, math, sys
from PIL import Image, ImageDraw

def rot(rx, ry, rz):
    """Rotação em graus, mesma ordem do Blockbench (three.js 'ZYX': M = Rz·Ry·Rx)."""
    a, b, c = (math.radians(v) for v in (rx, ry, rz))
    Rx = [[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]]
    Ry = [[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]]
    Rz = [[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]]
    return mm(Rz, mm(Ry, Rx))

def mm(A, B): return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def mv(A, v): return [sum(A[i][k] * v[k] for k in range(3)) for i in range(3)]
def add(a, b): return [a[i] + b[i] for i in range(3)]
def sub(a, b): return [a[i] - b[i] for i in range(3)]

def compor(M1, M2):  # (A,b): p -> A p + b ; retorna M1 ∘ M2
    A1, b1 = M1; A2, b2 = M2
    return mm(A1, A2), add(mv(A1, b2), b1)

NORMAIS = {"north": (0, 0, -1), "south": (0, 0, 1), "east": (1, 0, 0),
           "west": (-1, 0, 0), "up": (0, 1, 0), "down": (0, -1, 0)}

def ponto_face(face, f, t, u, v):
    (x1, y1, z1), (x2, y2, z2) = f, t
    dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
    return {"north": (x2 - u * dx, y2 - v * dy, z1), "south": (x1 + u * dx, y2 - v * dy, z2),
            "east": (x2, y2 - v * dy, z2 - u * dz), "west": (x1, y2 - v * dy, z1 + u * dz),
            "up": (x1 + u * dx, y2, z1 + v * dz), "down": (x1 + u * dx, y1, z2 - v * dz)}[face]

def carregar(caminho):
    m = json.loads(open(caminho, encoding="utf-8").read())
    src = m["textures"][0]["source"].split(",", 1)[1]
    tex = Image.open(io.BytesIO(base64.b64decode(src))).convert("RGBA")
    els = {e["uuid"]: e for e in m["elements"]}
    quads = []

    def emitir(e, M):
        rot_e = e.get("rotation", [0, 0, 0])
        if any(abs(v) > 1e-9 for v in rot_e):          # cubo girado sozinho (formato Bedrock)
            o = e.get("origin", [0, 0, 0]); R = rot(*rot_e)
            M = compor(M, (R, sub(o, mv(R, o))))
        A, _ = M
        for face, fd in e["faces"].items():
            u1, v1, u2, v2 = fd["uv"]
            nu, nv = round(abs(u2 - u1)), round(abs(v2 - v1))
            if nu == 0 or nv == 0: continue
            su, sv = (1 if u2 > u1 else -1), (1 if v2 > v1 else -1)
            n = mv(A, NORMAIS[face])
            for a in range(nu):
                for b in range(nv):
                    cor = tex.getpixel((int(math.floor(u1 + su * (a + .5))), int(math.floor(v1 + sv * (b + .5)))))
                    if cor[3] == 0: continue
                    cantos = [ponto_face(face, e["from"], e["to"], fu, fv) for fu, fv in
                              ((a / nu, b / nv), ((a + 1) / nu, b / nv), ((a + 1) / nu, (b + 1) / nv), (a / nu, (b + 1) / nv))]
                    quads.append(([add(mv(A, p), M[1]) for p in cantos], cor[:3], n))

    def andar(no, M):
        if isinstance(no, str):
            if no in els: emitir(els[no], M)
            return
        o = no["origin"]; R = rot(*no.get("rotation", [0, 0, 0]))
        Mn = compor(M, (R, sub(o, mv(R, o))))
        for f in no["children"]: andar(f, Mn)

    I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    for no in m["outliner"]: andar(no, (I, [0, 0, 0]))
    return quads

def desenhar(quads, yaw, pitch, escala=12, margem=20):
    V = mm(rot(pitch, 0, 0), rot(0, yaw, 0))
    vis = []
    for cantos, cor, n in quads:
        nv = mv(V, n)
        if nv[2] >= -1e-6: continue                 # face de costas para a câmera
        pts = [mv(V, p) for p in cantos]
        luz = 0.6 * n[0] ** 2 + 0.8 * n[2] ** 2 + (1.0 if n[1] > 0 else 0.5) * n[1] ** 2
        vis.append((sum(p[2] for p in pts) / 4, [(-p[0], -p[1]) for p in pts],
                    tuple(int(c * luz) for c in cor)))
    xs = [x for _, pts, _ in vis for x, _ in pts]; ys = [y for _, pts, _ in vis for _, y in pts]
    x0, y0 = min(xs), min(ys)
    W = int((max(xs) - x0) * escala) + 2 * margem; H = int((max(ys) - y0) * escala) + 2 * margem
    img = Image.new("RGB", (W, H), (30, 33, 39))
    d = ImageDraw.Draw(img)
    for _, pts, cor in sorted(vis, key=lambda q: -q[0]):
        poly = [((x - x0) * escala + margem, (y - y0) * escala + margem) for x, y in pts]
        d.polygon(poly, fill=cor, outline=cor)
    return img

if __name__ == "__main__":
    quads = carregar(sys.argv[1])
    vistas = [("frente", 0, -8), ("lado", 90, -5), ("3/4 frente", -40, -20), ("3/4 tras", 145, -20)]
    imgs = [(nome, desenhar(quads, y, p)) for nome, y, p in vistas]
    H = max(i.height for _, i in imgs) + 24
    folha = Image.new("RGB", (sum(i.width for _, i in imgs) + 10 * (len(imgs) - 1), H), (22, 24, 29))
    x = 0
    for nome, i in imgs:
        folha.paste(i, (x, 24 + (H - 24 - i.height)))
        ImageDraw.Draw(folha).text((x + 8, 6), nome, fill=(220, 220, 220))
        x += i.width + 10
    folha.save(sys.argv[2])
    print("previa ->", sys.argv[2], folha.size)
