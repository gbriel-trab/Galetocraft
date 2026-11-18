"""Engenharia reversa de modelos Bedrock (.geo.json) — os do Cobblemon, do GeckoLib e os do próprio Galetocraft.

Lê a geometria, a textura e (opcional) o arquivo de animações e gera:
  - relatorio.md        árvore de ossos, contagens, técnicas usadas (planos, inflate, cubos girados, mirror),
                        medidas, uso da textura e resumo das animações;
  - vistas_repouso.png  frente / lado / trás / 3-4 na pose de modelagem (bind pose);
  - vistas_<anim>.png   as mesmas vistas com a pose de uma animação no instante t (Molang avaliado);
  - uv_mapa.png         a textura com o retângulo de UV de cada face por cima.

  - "Conferência do estilo": os 15 critérios de modelos/GUIA_ESTILO.md (padrão Cobblemon dos Cocorídeos).

Uso:
  python analisar_geo.py MODELO.geo.json TEXTURA.png [--anim ARQ.animation.json] [--pose NOME[@t] ...]
                         [--saida PASTA] [--escala-jogo N]
  python analisar_geo.py MODELO.geo.json TEXTURA.png --anim ARQ.animation.json --estilo   (só a conferência)

Convenções (as mesmas do Blockbench ao importar Bedrock): X espelhado; pivô do osso = [-x, y, z];
rotação do osso e do cubo = [-rx, -ry, rz]; cubo: from = [-(x + w), y, z]; animação: rotação [-rx, -ry, rz]
somada à do osso, posição [-x, y, z] somada ao pivô, escala multiplicada em volta do pivô.
Molang: avaliado por um interpretador próprio (só aritmética, comparações e funções math.*); nada do arquivo
é executado como código Python. Consultas desconhecidas (q.*, v.*) valem 0.
"""
import argparse, ast, io, json, math, re, sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from previa import rot, mm, mv, add, sub, compor, NORMAIS, ponto_face  # noqa: E402
import previa2  # noqa: E402

I3 = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


# ----------------------------------------------------------------------------------------------------------------
# Leitura
# ----------------------------------------------------------------------------------------------------------------
def carregar_geo(caminho):
    d = json.loads(Path(caminho).read_text(encoding="utf-8"))
    if "minecraft:geometry" in d:
        g = d["minecraft:geometry"][0]
        desc = g.get("description", {})
    else:  # formato antigo 1.8: {"geometry.nome": {...}}
        chave = next(k for k in d if k.startswith("geometry."))
        g = d[chave]
        desc = {"identifier": chave, "texture_width": g.get("texturewidth"), "texture_height": g.get("textureheight")}
    return {"formato": d.get("format_version"), "desc": desc, "ossos": g.get("bones", [])}


def carregar_textura(caminho):
    return np.asarray(Image.open(caminho).convert("RGBA")).astype(np.float32)


# ----------------------------------------------------------------------------------------------------------------
# Molang (subconjunto) — interpretador seguro sobre a AST do Python
# ----------------------------------------------------------------------------------------------------------------
def _graus(f):
    return lambda x: f(math.radians(x))


FUNCOES = {
    "math.sin": _graus(math.sin), "math.cos": _graus(math.cos),
    "math.abs": abs, "math.min": min, "math.max": max, "math.sqrt": lambda x: math.sqrt(max(x, 0)),
    "math.floor": math.floor, "math.ceil": math.ceil, "math.round": round, "math.trunc": math.trunc,
    "math.clamp": lambda x, a, b: min(max(x, a), b), "math.lerp": lambda a, b, t: a + (b - a) * t,
    "math.pow": lambda a, b: a ** b, "math.mod": lambda a, b: math.fmod(a, b) if b else 0.0,
    "math.pi": math.pi, "math.exp": math.exp, "math.ln": lambda x: math.log(x) if x > 0 else 0.0,
    "math.atan": lambda x: math.degrees(math.atan(x)), "math.atan2": lambda y, x: math.degrees(math.atan2(y, x)),
    "math.asin": lambda x: math.degrees(math.asin(max(-1, min(1, x)))),
    "math.acos": lambda x: math.degrees(math.acos(max(-1, min(1, x)))),
}
_ALIAS = {"query.": "q.", "variable.": "v.", "temp.": "t.", "context.": "c."}


def _nome(no):
    partes = []
    while isinstance(no, ast.Attribute):
        partes.append(no.attr); no = no.value
    if isinstance(no, ast.Name):
        partes.append(no.id); return ".".join(reversed(partes))
    return None


def _traduzir(expr):
    s = expr.strip().rstrip(";").lower()
    for longo, curto in _ALIAS.items():
        s = s.replace(longo, curto)
    s = s.replace("&&", " and ").replace("||", " or ")
    s = re.sub(r"!(?!=)", " not ", s)
    # ternário a ? b : c  ->  (b if a else c)   (um nível, sem aninhamento)
    m = re.fullmatch(r"(.+?)\?(.+?):(.+)", s)
    if m:
        s = f"(({m.group(2)}) if ({m.group(1)}) else ({m.group(3)}))"
    return s.strip()


AVISOS = {}  # expressão Molang malformada -> como foi lida


def _arvore(expr):
    s = _traduzir(expr)
    try:
        return ast.parse(s, mode="eval")
    except SyntaxError:
        # Caso visto no Blaziken do Cobblemon: "a)+6*(b" — falta o parêntese de fora. Tenta "(a)+6*(b)".
        try:
            arv = ast.parse(f"({s})", mode="eval")
            AVISOS[expr] = "lida como (" + expr + ")"
            return arv
        except SyntaxError:
            AVISOS[expr] = "ilegível, vale 0"
            return ast.parse("0", mode="eval")


def molang(expr, t=0.0, consultas=None):
    """Valor numérico de uma expressão Molang no instante t (segundos). Números passam direto."""
    if isinstance(expr, (int, float)):
        return float(expr)
    consultas = dict(consultas or {})
    consultas.setdefault("q.anim_time", t)
    consultas.setdefault("q.life_time", t)
    arvore = _arvore(expr)

    def ev(n):
        if isinstance(n, ast.Expression): return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)): return float(n.value)
        if isinstance(n, ast.UnaryOp):
            v = ev(n.operand)
            return {ast.USub: -v, ast.UAdd: v, ast.Not: float(not v)}[type(n.op)]
        if isinstance(n, ast.BinOp):
            a, b = ev(n.left), ev(n.right)
            op = type(n.op)
            if op is ast.Add: return a + b
            if op is ast.Sub: return a - b
            if op is ast.Mult: return a * b
            if op is ast.Div: return a / b if b else 0.0
            if op is ast.Mod: return math.fmod(a, b) if b else 0.0
            if op is ast.Pow: return a ** b
            raise ValueError(f"operador {op.__name__}")
        if isinstance(n, ast.BoolOp):
            vs = [ev(v) for v in n.values]
            return float(all(vs)) if isinstance(n.op, ast.And) else float(any(vs))
        if isinstance(n, ast.Compare):
            a = ev(n.left)
            for op, d in zip(n.ops, n.comparators):
                b = ev(d)
                ok = {ast.Lt: a < b, ast.LtE: a <= b, ast.Gt: a > b, ast.GtE: a >= b,
                      ast.Eq: a == b, ast.NotEq: a != b}[type(op)]
                if not ok: return 0.0
                a = b
            return 1.0
        if isinstance(n, ast.IfExp):
            return ev(n.body) if ev(n.test) else ev(n.orelse)
        if isinstance(n, (ast.Attribute, ast.Name)):
            nome = _nome(n)
            if nome in FUNCOES and not callable(FUNCOES[nome]): return FUNCOES[nome]
            return float(consultas.get(nome, 0.0))
        if isinstance(n, ast.Call):
            nome = _nome(n.func)
            if nome in FUNCOES and callable(FUNCOES[nome]):
                return float(FUNCOES[nome](*[ev(a) for a in n.args]))
            return float(consultas.get(nome, 0.0))  # q.r.target_distance_x(0) etc.
        raise ValueError(f"nó Molang não suportado: {type(n).__name__}")

    return ev(arvore)


# ----------------------------------------------------------------------------------------------------------------
# Animações
# ----------------------------------------------------------------------------------------------------------------
def _vetor(v, t, lado="post"):
    if isinstance(v, (int, float, str)):
        x = molang(v, t); return [x, x, x]
    if isinstance(v, dict):  # {"pre": .., "post": ..} ou {"vector": ..}; sai pelo "post", chega pelo "pre"
        outro = "pre" if lado == "post" else "post"
        v = v.get(lado, v.get("vector", v.get(outro)))
        return _vetor(v, t)
    return [molang(c, t) for c in v]


def _canal(valor, t, comprimento):
    """Valor de um canal (rotation/position/scale) no instante t: constante, Molang ou keyframes.
    Interpolação linear entre keyframes (catmullrom é aproximado por linear: serve para poses estáticas)."""
    if not isinstance(valor, dict) or "vector" in valor or "post" in valor:
        return _vetor(valor, t)
    chaves = sorted((float(k), k) for k in valor)
    if comprimento:
        t = t % comprimento if comprimento > 0 else t
    if t <= chaves[0][0]: return _vetor(valor[chaves[0][1]], t)
    if t >= chaves[-1][0]: return _vetor(valor[chaves[-1][1]], t, "pre")
    for (t0, k0), (t1, k1) in zip(chaves, chaves[1:]):
        if t0 <= t <= t1:
            a = _vetor(valor[k0], t, "post"); b = _vetor(valor[k1], t, "pre")
            f = (t - t0) / (t1 - t0) if t1 > t0 else 0.0
            return [a[i] + (b[i] - a[i]) * f for i in range(3)]


def pose(animacao, t=0.0):
    """{osso: {"rotation": [...], "position": [...], "scale": [...]}} no instante t (espaço Bedrock)."""
    comp = animacao.get("animation_length") or 0
    saida = {}
    for osso, canais in animacao.get("bones", {}).items():
        saida[osso] = {c: _canal(v, t, comp) for c, v in canais.items() if c in ("rotation", "position", "scale")}
    return saida


def resumo_animacoes(anims):
    linhas = []
    for nome, a in anims.items():
        ossos = a.get("bones", {})
        kf = mol = 0; canais = set()
        for canais_osso in ossos.values():
            for c, v in canais_osso.items():
                canais.add(c)
                if isinstance(v, dict) and not ("vector" in v or "post" in v):
                    kf += len(v)
                    mol += sum(1 for x in v.values() if "q." in json.dumps(x) or "math." in json.dumps(x))
                elif isinstance(v, (str, list)) and any(isinstance(x, str) for x in (v if isinstance(v, list) else [v])):
                    mol += 1
        extras = [k for k in a if k not in ("bones", "loop", "animation_length")]
        linhas.append({"nome": nome, "duracao": a.get("animation_length"), "loop": a.get("loop"),
                       "ossos": len(ossos), "keyframes": kf, "canais_molang": mol,
                       "canais": sorted(canais), "extras": extras})
    return linhas


# ----------------------------------------------------------------------------------------------------------------
# Geometria -> faces no espaço do Blockbench (o mesmo do previa2)
# ----------------------------------------------------------------------------------------------------------------
def _uv_caixa(u, v, w, h, d, espelho):
    """UV de caixa (box UV) como o Blockbench/Java: retângulos [u1, v1, u2, v2] por face."""
    f = {
        "east": ([u, v + d], [d, h]), "west": ([u + d + w, v + d], [d, h]),
        "up": ([u + d + w, v + d], [-w, -d]), "down": ([u + d + 2 * w, v], [-w, d]),
        "south": ([u + 2 * d + w, v + d], [w, h]), "north": ([u + d, v + d], [w, h]),
    }
    if espelho:
        f["east"], f["west"] = (f["west"][0], f["east"][1]), (f["east"][0], f["west"][1])
        f = {k: ([o[0] + s[0], o[1]], [-s[0], s[1]]) for k, (o, s) in f.items()}
    return {k: [o[0], o[1], o[0] + s[0], o[1] + s[1]] for k, (o, s) in f.items()}


def _uv_faces(c):
    w, h, d = c["size"]
    uv = c.get("uv", [0, 0])
    if isinstance(uv, list):
        return _uv_caixa(uv[0], uv[1], w, h, d, c.get("mirror", False)), "caixa"
    saida = {}
    for face, fd in uv.items():
        (u, v), (su, sv) = fd["uv"], fd.get("uv_size", [0, 0])
        saida[face] = [u + su, v + sv, u, v] if face in ("up", "down") else [u, v, u + su, v + sv]
    return saida, "por_face"


def transformar(geo, pose_bedrock=None):
    """Lista [(nome_osso, cubo, M)] com M = transformação do cubo no espaço do Blockbench, já com a pose."""
    pose_bedrock = pose_bedrock or {}
    ossos = {o["name"]: o for o in geo["ossos"]}
    filhos = {}
    for o in geo["ossos"]:
        filhos.setdefault(o.get("parent"), []).append(o["name"])
    saida = []

    def matriz_osso(o):
        px, py, pz = o.get("pivot", [0, 0, 0])
        rx, ry, rz = o.get("rotation", [0, 0, 0])
        p = pose_bedrock.get(o["name"], {})
        ax, ay, az = p.get("rotation", [0, 0, 0])
        dx, dy, dz = p.get("position", [0, 0, 0])
        sx, sy, sz = p.get("scale", [1, 1, 1])
        piv = [-px, py, pz]
        R = rot(-(rx + ax), -(ry + ay), rz + az)
        S = [[sx, 0, 0], [0, sy, 0], [0, 0, sz]]
        A = mm(R, S)
        return (A, add(sub(piv, mv(A, piv)), [-dx, dy, dz]))

    def andar(nome, M):
        o = ossos[nome]
        Mn = compor(M, matriz_osso(o))
        for c in o.get("cubes", []):
            saida.append((nome, c, Mn))
        for f in filhos.get(nome, []):
            andar(f, Mn)

    for raiz in filhos.get(None, []):
        andar(raiz, (I3, [0, 0, 0]))
    return saida


def faces(geo, tex, pose_bedrock=None):
    """Faces no formato do previa2: [(3 cantos, uv, normal)]."""
    lista = []
    for _, c, M in transformar(geo, pose_bedrock):
        x, y, z = c["origin"]; w, h, d = c["size"]; inf = c.get("inflate", 0)
        de = [-(x + w) - inf, y - inf, z - inf]; ate = [-x + inf, y + h + inf, z + d + inf]
        if c.get("rotation") and any(abs(v) > 1e-9 for v in c["rotation"]):
            px, py, pz = c.get("pivot", [0, 0, 0]); o = [-px, py, pz]
            rx, ry, rz = c["rotation"]; R = rot(-rx, -ry, rz)
            M = compor(M, (R, sub(o, mv(R, o))))
        A, b = M
        uvs, _ = _uv_faces(c)
        for face, (u1, v1, u2, v2) in uvs.items():
            if abs(u2 - u1) < 1e-6 or abs(v2 - v1) < 1e-6: continue
            cantos = [add(mv(A, ponto_face(face, de, ate, fu, fv)), b) for fu, fv in ((0, 0), (1, 0), (0, 1))]
            lista.append((cantos, (u1, v1, u2, v2), mv(A, NORMAIS[face])))
    return lista, tex


# ----------------------------------------------------------------------------------------------------------------
# Medidas e estatísticas
# ----------------------------------------------------------------------------------------------------------------
def limites(dados):
    """(min, max) dos texels visíveis, em pixels de modelo (16 = 1 bloco)."""
    fs, tex = dados
    H, W = tex.shape[:2]; pts = []
    grade = np.linspace(0.02, 0.98, 8)
    for (c0, c1, c2), (u1, v1, u2, v2), _ in fs:
        c0, c1, c2 = map(np.array, (c0, c1, c2))
        for a in grade:
            for b in grade:
                u = u1 + (u2 - u1) * a; v = v1 + (v2 - v1) * b
                if tex[min(int(v), H - 1), min(int(u), W - 1), 3] > 0:
                    pts.append(c0 + (c1 - c0) * a + (c2 - c0) * b)
    p = np.array(pts)
    return p.min(0), p.max(0)


def estatisticas(geo, tex):
    cubos = [(o["name"], c) for o in geo["ossos"] for c in o.get("cubes", [])]
    planos = [c for _, c in cubos if min(c["size"]) == 0]
    girados = [c for _, c in cubos if any(abs(v) > 1e-9 for v in c.get("rotation", [0, 0, 0]))]
    inflados = [c for _, c in cubos if c.get("inflate")]
    espelhados = [c for _, c in cubos if c.get("mirror")]
    fracionados = [c for _, c in cubos if any(abs(s - round(s)) > 1e-6 for s in c["size"])]
    por_face = [c for _, c in cubos if isinstance(c.get("uv"), dict)]
    vazios = [o["name"] for o in geo["ossos"] if not o.get("cubes")]
    ossos_girados = [o["name"] for o in geo["ossos"] if any(abs(v) > 1e-9 for v in o.get("rotation", [0, 0, 0]))]
    vol = sum(c["size"][0] * c["size"][1] * c["size"][2] for _, c in cubos)
    # uso da textura
    th, tw = tex.shape[:2]
    usado = np.zeros((th, tw), bool)
    for _, c in cubos:
        for (u1, v1, u2, v2) in _uv_faces(c)[0].values():
            a, b = sorted((u1, u2)); e, f = sorted((v1, v2))
            usado[max(int(math.floor(e)), 0):min(int(math.ceil(f)), th), max(int(math.floor(a)), 0):min(int(math.ceil(b)), tw)] = True
    opaco = tex[..., 3] > 0
    cores = {tuple(int(x) for x in p[:3]) for p in tex[opaco]}
    return {
        "ossos": len(geo["ossos"]), "ossos_vazios": len(vazios), "ossos_girados": len(ossos_girados),
        "cubos": len(cubos), "planos": len(planos), "cubos_girados": len(girados), "inflate": len(inflados),
        "mirror": len(espelhados), "tamanho_fracionado": len(fracionados), "uv_por_face": len(por_face),
        "volume": vol, "textura": (tw, th), "uv_ocupa": usado.mean(), "opaco": opaco.mean(),
        "opaco_fora_uv": (opaco & ~usado).mean(), "cores": len(cores),
        "profundidade": _profundidade(geo),
    }


def _profundidade(geo):
    pai = {o["name"]: o.get("parent") for o in geo["ossos"]}
    def nivel(n):
        k = 0
        while pai.get(n): n = pai[n]; k += 1
        return k
    return max((nivel(n) for n in pai), default=0)


def arvore(geo):
    filhos = {}
    for o in geo["ossos"]:
        filhos.setdefault(o.get("parent"), []).append(o)
    linhas = []

    def andar(o, prof):
        cs = o.get("cubes", [])
        info = []
        if cs:
            tipos = []
            for c in cs:
                s = "x".join(f"{v:g}" for v in c["size"])
                marca = ("▭" if min(c["size"]) == 0 else "") + ("↻" if any(abs(v) > 1e-9 for v in c.get("rotation", [0, 0, 0])) else "") \
                    + ("+" if c.get("inflate") else "") + ("⇋" if c.get("mirror") else "")
                tipos.append(s + marca)
            info.append(f"{len(cs)} cubo(s): " + ", ".join(tipos))
        r = o.get("rotation")
        if r and any(abs(v) > 1e-9 for v in r):
            info.append("rot " + "/".join(f"{v:g}" for v in r))
        piv = "/".join(f"{v:g}" for v in o.get("pivot", [0, 0, 0]))
        linhas.append(f"{'  ' * prof}- `{o['name']}` (pivô {piv})" + (" — " + "; ".join(info) if info else ""))
        for f in filhos.get(o["name"], []):
            andar(f, prof + 1)

    for raiz in filhos.get(None, []):
        andar(raiz, 0)
    return linhas


# ----------------------------------------------------------------------------------------------------------------
# Conferência do estilo (modelos/GUIA_ESTILO.md). Os números vêm de 78 modelos do Cobblemon 1.8.4.
# ----------------------------------------------------------------------------------------------------------------
#  altura no jogo até (blocos): (cubos alvo, cubos teto, faces alvo, faces teto, textura alvo, área máx., cores teto)
ORCAMENTO = [
    (1.0, (40, 75, 160, 270, "64x64", 64 * 64, 35)),
    (2.0, (70, 110, 300, 520, "128x64 ou 128x128", 128 * 128, 40)),
    (3.0, (100, 145, 410, 530, "256x128 ou 256x256", 256 * 256, 55)),
    (99.0, (110, 270, 450, 600, "256x256", 256 * 256, 64)),
]
ALIAS_ANIM = {"parado": ("ground_idle", "idle"), "andar": ("ground_walk", "walk"), "piscar": ("blink",),
              "grito": ("cry",), "dormir": ("sleep",)}


def _lum(p):
    return 0.299 * p[..., 0] + 0.587 * p[..., 1] + 0.114 * p[..., 2]


def textura_estilo(geo, tex):
    """Mosqueado e luz pintada, medidos nas faces de cubos com lados >= 4 texels.
    ruido = fração de pares de pixels vizinhos com cor diferente; luz = média de |tampa - lados| e |fundo - lados|."""
    th, tw = tex.shape[:2]
    ruido, luz = [], []
    for o in geo["ossos"]:
        for c in o.get("cubes", []):
            if min(c["size"]) < 4: continue
            L = {}
            for face, (u1, v1, u2, v2) in _uv_faces(c)[0].items():
                a, b = sorted((u1, u2)); e, f = sorted((v1, v2))
                a, b, e, f = (int(round(x)) for x in (a, b, e, f))
                if a < 0 or e < 0 or b > tw or f > th or b - a < 4 or f - e < 4: continue
                reg = tex[e:f, a:b]
                if (reg[..., 3] == 0).mean() > 0.2: continue
                cor = reg[..., :3]
                ruido.append((np.abs(cor[:, 1:] - cor[:, :-1]).sum(-1) > 0).mean())
                L[face] = _lum(reg).mean()
            lados = [L[k] for k in ("north", "south", "east", "west") if k in L]
            if lados and "up" in L and "down" in L:
                m = np.mean(lados); luz.append((abs(L["up"] - m) + abs(L["down"] - m)) / 2)
    return (float(np.median(ruido)) if ruido else None), (float(np.median(luz)) if luz else None)


def conferir_estilo(geo, tex, dados, anims=None, escala_jogo=1.0):
    """[(critério, alvo, valor medido, ok)] contra o guia de estilo."""
    e = estatisticas(geo, tex)
    lo, hi = limites(dados)
    alt = (hi[1] - min(lo[1], 0)) * escala_jogo / 16
    _, (c_alvo, c_teto, f_alvo, f_teto, t_alvo, t_area, cor_teto) = next(x for x in ORCAMENTO if alt <= x[0])
    nfaces = len(dados[0]); tw, th = e["textura"]
    ruido, luz = textura_estilo(geo, tex)
    nomes = {o["name"] for o in geo["ossos"]}
    infl = [abs(c.get("inflate", 0)) for o in geo["ossos"] for c in o.get("cubes", [])]
    linhas = [
        ("UV de caixa (1 texel = 1 unidade)", "100% dos cubos", f"{e['cubos'] - e['uv_por_face']}/{e['cubos']}", e["uv_por_face"] == 0),
        ("tamanhos inteiros", "0 fracionados", str(e["tamanho_fracionado"]), e["tamanho_fracionado"] == 0),
        (f"cubos (altura {alt:.2f} bl)", f"~{c_alvo}, teto {c_teto}", str(e["cubos"]), e["cubos"] <= c_teto),
        ("faces desenhadas", f"~{f_alvo}, teto {f_teto}", str(nfaces), nfaces <= f_teto),
        ("textura", t_alvo, f"{tw}x{th}", tw * th <= t_area),
        ("cores na textura", f"até {cor_teto}", str(e["cores"]), e["cores"] <= cor_teto),
        ("planos (espessura 0)", "20% a 75% dos cubos", f"{100 * e['planos'] / max(e['cubos'], 1):.0f}%",
         0.20 <= e["planos"] / max(e["cubos"], 1) <= 0.75),
        ("cubos girados no próprio pivô", "até 23% (gire o osso)", f"{100 * e['cubos_girados'] / max(e['cubos'], 1):.0f}%",
         e["cubos_girados"] / max(e["cubos"], 1) <= 0.23),
        ("inflate", "até 0,1 (desempate, não volume)", f"máx. {max(infl, default=0):g}", max(infl, default=0) <= 0.1),
        ("mosqueado da textura", "0,25 a 0,65 dos vizinhos diferem", "—" if ruido is None else f"{ruido:.2f}",
         ruido is not None and 0.25 <= ruido <= 0.65),
        ("luz pintada (tampa/fundo x lados)", "até 16 de luminância", "—" if luz is None else f"{luz:.1f}",
         luz is not None and luz <= 16),
        ("pálpebra para piscar", "osso eyelid/palpebra", "sim" if any("eyelid" in n or "palpebra" in n for n in nomes) else "não",
         any("eyelid" in n or "palpebra" in n for n in nomes)),
    ]
    if anims is not None:
        tem = lambda chave: any(k.split(".")[-1] in ALIAS_ANIM[chave] for k in anims)
        faltam = [k for k in ("parado", "andar", "piscar") if not tem(k)]
        recom = [k for k in ("grito", "dormir") if not tem(k)]
        linhas.append(("animações obrigatórias", "parado, andar (ou andar procedural no código), piscar",
                       "faltam: " + ", ".join(faltam) if faltam else "ok", not faltam))
        linhas.append(("animações recomendadas", "grito, dormir", "faltam: " + ", ".join(recom) if recom else "ok", not recom))
        orf = sorted({b for a in anims.values() for b in a.get("bones", {})} - nomes)
        linhas.append(("ossos animados existem", "todos", "faltam: " + ", ".join(orf) if orf else "ok", not orf))
    return linhas


def texto_estilo(linhas):
    ok = sum(1 for *_, b in linhas if b)
    L = ["## Conferência do estilo (`modelos/GUIA_ESTILO.md`)", "", f"**{ok} de {len(linhas)} critérios atendidos.**", "",
         "| critério | alvo | medido | ok |", "|---|---|---|---|"]
    L += [f"| {c} | {a} | {v} | {'✔' if b else '✘'} |" for c, a, v, b in linhas]
    return "\n".join(L) + "\n"


# ----------------------------------------------------------------------------------------------------------------
# Imagens
# ----------------------------------------------------------------------------------------------------------------
VISTAS = [("frente", 0, -5), ("lado", 90, -5), ("trás", 180, -5), ("3/4", 35, -12)]
FUNDO = (36, 39, 46)


def fonte(tamanho=14):
    """Fonte com acentos: Arial (Windows) ou DejaVu (Linux); senão a padrão do PIL."""
    from PIL import ImageFont
    for nome in ("arial.ttf", "DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(nome, tamanho)
        except OSError:
            pass
    return ImageFont.load_default()


def folha_vistas(dados, escala=8, titulo=None):
    ims = [(n, previa2.desenhar(dados, y, p, escala=escala, fundo=FUNDO)) for n, y, p in VISTAS]
    H = max(i.height for _, i in ims) + 22; W = sum(i.width for _, i in ims)
    folha = Image.new("RGB", (W, H + (22 if titulo else 0)), FUNDO)
    d = ImageDraw.Draw(folha); x = 0; y0 = 22 if titulo else 0; f = fonte()
    if titulo: d.text((8, 4), titulo, fill=(230, 230, 230), font=f)
    for n, i in ims:
        folha.paste(i, (x, y0 + H - 22 - i.height)); d.text((x + 8, y0 + H - 19), n, fill=(200, 200, 200), font=f); x += i.width
    return folha


def mapa_uv(geo, tex_path, ampliar=4):
    img = Image.open(tex_path).convert("RGBA")
    fundo = Image.new("RGBA", img.size, (60, 60, 60, 255)); fundo.alpha_composite(img)
    big = fundo.resize((img.width * ampliar, img.height * ampliar), Image.NEAREST)
    d = ImageDraw.Draw(big)
    cores = {"north": (255, 80, 80), "south": (80, 160, 255), "east": (80, 220, 120),
             "west": (240, 200, 60), "up": (255, 255, 255), "down": (170, 90, 255)}
    for o in geo["ossos"]:
        for c in o.get("cubes", []):
            for face, (u1, v1, u2, v2) in _uv_faces(c)[0].items():
                if abs(u2 - u1) < 1e-6 or abs(v2 - v1) < 1e-6: continue
                a, b = sorted((u1, u2)); e, f = sorted((v1, v2))
                d.rectangle([a * ampliar, e * ampliar, b * ampliar - 1, f * ampliar - 1], outline=cores[face])
    return big


# ----------------------------------------------------------------------------------------------------------------
# Relatório
# ----------------------------------------------------------------------------------------------------------------
def relatorio(geo, tex, dados_repouso, anims=None, escala_jogo=None):
    e = estatisticas(geo, tex)
    lo, hi = limites(dados_repouso)
    alt, larg, comp = hi[1] - min(lo[1], 0), hi[0] - lo[0], hi[2] - lo[2]
    L = [f"# Análise de `{geo['desc'].get('identifier')}`", ""]
    L += ["## Números", "", "| item | valor |", "|---|---|"]
    L += [f"| formato | {geo['formato']} |",
          f"| textura | {e['textura'][0]}x{e['textura'][1]} px, {e['cores']} cores distintas |",
          f"| ossos | {e['ossos']} ({e['ossos_vazios']} sem cubo = só articulação; {e['ossos_girados']} com rotação de repouso; profundidade máx. {e['profundidade']}) |",
          f"| cubos | {e['cubos']} |",
          f"| planos (espessura 0) | {e['planos']} ({100 * e['planos'] / max(e['cubos'], 1):.0f}%) |",
          f"| cubos girados no próprio pivô | {e['cubos_girados']} |",
          f"| cubos com inflate | {e['inflate']} |",
          f"| cubos com mirror | {e['mirror']} |",
          f"| cubos com tamanho fracionado | {e['tamanho_fracionado']} |",
          f"| UV por face / caixa | {e['uv_por_face']} / {e['cubos'] - e['uv_por_face']} |",
          f"| volume dos cubos | {e['volume']:.0f} px³ |",
          f"| textura coberta por UV | {100 * e['uv_ocupa']:.1f}% (opaco: {100 * e['opaco']:.1f}%; opaco fora de UV: {100 * e['opaco_fora_uv']:.1f}%) |",
          f"| medidas em repouso (alt x larg x comp) | {alt:.1f} x {larg:.1f} x {comp:.1f} px = {alt / 16:.2f} x {larg / 16:.2f} x {comp / 16:.2f} blocos |"]
    if escala_jogo:
        L += [f"| no jogo (x{escala_jogo:g}) | {alt * escala_jogo / 16:.2f} x {larg * escala_jogo / 16:.2f} x {comp * escala_jogo / 16:.2f} blocos |"]
    L += ["", "Legenda da árvore: ▭ plano, ↻ cubo girado, + inflate, ⇋ mirror.", "", "## Árvore de ossos", ""]
    L += arvore(geo)
    if anims:
        L += ["", "## Animações", "", "| animação | duração (s) | loop | ossos | keyframes | canais Molang | canais | extras |",
              "|---|---|---|---|---|---|---|---|"]
        for a in resumo_animacoes(anims):
            L.append(f"| `{a['nome']}` | {a['duracao'] if a['duracao'] is not None else '—'} | {a['loop']} | {a['ossos']} | "
                     f"{a['keyframes']} | {a['canais_molang']} | {', '.join(a['canais'])} | {', '.join(a['extras']) or '—'} |")
        existentes = {o["name"] for o in geo["ossos"]}
        orfaos = {n: sorted(set(a.get("bones", {})) - existentes) for n, a in anims.items()}
        orfaos = {n: o for n, o in orfaos.items() if o}
        L += ["", "Ossos animados que não existem no modelo (esses canais não têm efeito): "
              + ("; ".join(f"`{n}`: {', '.join(o)}" for n, o in orfaos.items()) if orfaos else "nenhum.")]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("modelo"); ap.add_argument("textura")
    ap.add_argument("--anim", help="arquivo .animation.json")
    ap.add_argument("--pose", action="append", default=[], help="animação a posar, ex.: ground_idle@0.5 (repetível)")
    ap.add_argument("--saida", default="analise_geo")
    ap.add_argument("--escala-jogo", type=float, help="escala aplicada no jogo (ex.: baseScale do Cobblemon)")
    ap.add_argument("--escala", type=float, default=8, help="pixels por unidade nas vistas")
    ap.add_argument("--estilo", action="store_true", help="só confere o modelo contra modelos/GUIA_ESTILO.md (sem imagens)")
    a = ap.parse_args()
    if a.pose and not a.anim:
        ap.error("--pose precisa de --anim")

    geo = carregar_geo(a.modelo); tex = carregar_textura(a.textura)
    repouso = faces(geo, tex)
    anims = json.loads(Path(a.anim).read_text(encoding="utf-8"))["animations"] if a.anim else None
    estilo = conferir_estilo(geo, tex, repouso, anims, a.escala_jogo or 1.0)
    if a.estilo:
        ok = sum(1 for *_, b in estilo if b)
        print(f"{Path(a.modelo).name}: {ok}/{len(estilo)} critérios do guia de estilo")
        for c, alvo, v, b in estilo:
            print(f"  {'ok ' if b else 'NÃO'}  {c}: {v}  (alvo: {alvo})")
        return

    saida = Path(a.saida); saida.mkdir(parents=True, exist_ok=True)
    texto = relatorio(geo, tex, repouso, anims, a.escala_jogo) + "\n" + texto_estilo(estilo)
    folha_vistas(repouso, a.escala, "pose de modelagem (repouso)").save(saida / "vistas_repouso.png")
    mapa_uv(geo, a.textura).save(saida / "uv_mapa.png")
    medidas = []
    for p in a.pose:
        nome, _, t = p.partition("@"); t = float(t or 0)
        chave = next((k for k in anims if k == nome or k.endswith("." + nome)), None)
        if chave is None:
            print(f"aviso: não há animação '{nome}'. Existem: {', '.join(k.split('.')[-1] for k in anims)}")
            continue
        dados = faces(geo, tex, pose(anims[chave], t))
        folha_vistas(dados, a.escala, f"{chave} @ {t:g}s").save(saida / f"vistas_{nome}.png")
        lo, hi = limites(dados)
        alt, larg, comp = hi[1] - min(lo[1], 0), hi[0] - lo[0], hi[2] - lo[2]
        k = (a.escala_jogo or 1) / 16
        medidas.append(f"| `{nome}` @ {t:g}s | {alt:.1f} x {larg:.1f} x {comp:.1f} | {alt * k:.2f} x {larg * k:.2f} x {comp * k:.2f} |")
    if medidas:
        texto += ("\n## Medidas por pose\n\n| pose | px (alt x larg x comp) | blocos no jogo"
                  + (f" (x{a.escala_jogo:g})" if a.escala_jogo else "") + " |\n|---|---|---|\n" + "\n".join(medidas) + "\n")
    if AVISOS:
        texto += "\n## Avisos de Molang\n\n" + "\n".join(f"- `{e}`: {c}" for e, c in AVISOS.items()) + "\n"
    (saida / "relatorio.md").write_text(texto, encoding="utf-8")
    print(f"ok: {saida}/relatorio.md, vistas e uv_mapa.png")


if __name__ == "__main__":
    main()
