"""Prévia de qualidade de um .bbmodel: rasterização com z-buffer (sem erros de ordem entre faces),
textura amostrada por pixel, luz direcional suave e antisserrilhado (renderiza 3x maior e reduz).
Uso como módulo: faces = carregar(caminho); img = desenhar(faces, yaw, pitch, escala)"""
import base64, io, json, math
import numpy as np
from PIL import Image
from previa import rot, mm, mv, add, sub, compor, NORMAIS, ponto_face

def carregar(caminho):
    m = json.loads(open(caminho, encoding="utf-8").read())
    src = m["textures"][0]["source"].split(",", 1)[1]
    tex = np.asarray(Image.open(io.BytesIO(base64.b64decode(src))).convert("RGBA")).astype(np.float32)
    els = {e["uuid"]: e for e in m["elements"]}
    faces = []

    def emitir(e, M):
        rot_e = e.get("rotation", [0, 0, 0])
        if any(abs(v) > 1e-9 for v in rot_e):
            o = e.get("origin", [0, 0, 0]); R = rot(*rot_e)
            M = compor(M, (R, sub(o, mv(R, o))))
        A, b = M
        for face, fd in e["faces"].items():
            u1, v1, u2, v2 = fd["uv"]
            if abs(u2 - u1) < 1e-6 or abs(v2 - v1) < 1e-6: continue
            cantos = [add(mv(A, ponto_face(face, e["from"], e["to"], fu, fv)), b) for fu, fv in ((0, 0), (1, 0), (0, 1))]
            faces.append((cantos, (u1, v1, u2, v2), mv(A, NORMAIS[face])))

    def andar(no, M):
        if isinstance(no, str):
            if no in els: emitir(els[no], M)
            return
        o = no["origin"]; R = rot(*no.get("rotation", [0, 0, 0]))
        Mn = compor(M, (R, sub(o, mv(R, o))))
        for f in no["children"]: andar(f, Mn)

    I = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    for no in m["outliner"]: andar(no, (I, [0, 0, 0]))
    return faces, tex

LUZ = np.array([-0.45, 0.75, -0.5]); LUZ = LUZ / np.linalg.norm(LUZ)

def desenhar(dados, yaw, pitch, escala=12, margem=20, ss=3, fundo=(30, 33, 39)):
    faces, tex = dados
    V = np.array(mm(rot(pitch, 0, 0), rot(0, yaw, 0)))
    s = escala * ss
    proj = []
    for cantos, uv, n in faces:
        nv = V @ np.array(n)
        if nv[2] >= -1e-6: continue
        P = [V @ np.array(c) for c in cantos]
        proj.append((P, uv, n))
    xs = [-p[0] for P, _, _ in proj for p in P]; ys = [-p[1] for P, _, _ in proj for p in P]
    # o 4º canto (1,1) = P1 + P2 - P0 também entra nos limites
    for P, _, _ in proj:
        q = P[1] + P[2] - P[0]; xs.append(-q[0]); ys.append(-q[1])
    x0, y0 = min(xs), min(ys)
    W = int((max(xs) - x0) * s) + 2 * margem * ss; H = int((max(ys) - y0) * s) + 2 * margem * ss
    cor = np.zeros((H, W, 3), np.float32); cor[:] = fundo
    zb = np.full((H, W), np.inf, np.float32)
    th, tw = tex.shape[:2]
    for P, (u1, v1, u2, v2), n in proj:
        sp = [np.array([(-p[0] - x0) * s + margem * ss, (-p[1] - y0) * s + margem * ss, p[2]]) for p in P]
        o, e1, e2 = sp[0], sp[1] - sp[0], sp[2] - sp[0]
        det = e1[0] * e2[1] - e1[1] * e2[0]
        if abs(det) < 1e-9: continue
        q4 = sp[1] + sp[2] - sp[0]
        bx = [p[0] for p in sp] + [q4[0]]; by = [p[1] for p in sp] + [q4[1]]
        ix0, ix1 = max(int(math.floor(min(bx))), 0), min(int(math.ceil(max(bx))), W - 1)
        iy0, iy1 = max(int(math.floor(min(by))), 0), min(int(math.ceil(max(by))), H - 1)
        if ix1 < ix0 or iy1 < iy0: continue
        gx, gy = np.meshgrid(np.arange(ix0, ix1 + 1) + .5, np.arange(iy0, iy1 + 1) + .5)
        dx, dy = gx - o[0], gy - o[1]
        u = (dx * e2[1] - dy * e2[0]) / det
        v = (e1[0] * dy - e1[1] * dx) / det
        dentro = (u >= 0) & (u <= 1) & (v >= 0) & (v <= 1)
        if not dentro.any(): continue
        z = o[2] + u * e1[2] + v * e2[2]
        bloco = zb[iy0:iy1 + 1, ix0:ix1 + 1]
        ok = dentro & (z < bloco - 1e-4)
        if not ok.any(): continue
        tu = np.clip(np.floor(u1 + u * (u2 - u1)), min(u1, u2), max(u1, u2) - 1).astype(int)
        tv = np.clip(np.floor(v1 + v * (v2 - v1)), min(v1, v2), max(v1, v2) - 1).astype(int)
        tu = np.clip(tu, 0, tw - 1); tv = np.clip(tv, 0, th - 1)
        amostra = tex[tv, tu]
        ok &= amostra[..., 3] > 0
        if not ok.any(): continue
        nn = np.array(n)
        luz = 0.62 + 0.38 * max(0.0, float(nn @ LUZ)) + (0.08 if nn[1] > 0.5 else 0) - (0.12 if nn[1] < -0.5 else 0)
        bloco[ok] = z[ok]
        alvo = cor[iy0:iy1 + 1, ix0:ix1 + 1]
        alvo[ok] = np.clip(amostra[..., :3][ok] * luz, 0, 255)
    img = Image.fromarray(cor.astype(np.uint8))
    return img.resize((W // ss, H // ss), Image.LANCZOS)
