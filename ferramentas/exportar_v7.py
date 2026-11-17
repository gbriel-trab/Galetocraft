"""Exporta um .bbmodel no formato Bedrock com UV por face (o Pirococó v7) para o GeckoLib:
geometria (.geo.json), textura, textura de brilho (_glowmask) e animações (parado / andando).

Uso: python exportar_v7.py <modelo.bbmodel> <pasta assets/galetocraft do mod>

Faz exatamente a conversão que o Blockbench faz ao exportar geometria Bedrock:
- X espelhado: origem do cubo = [-(x final), y inicial, z inicial]; pivô = [-x, y, z]
- rotação (osso ou cubo) = [-rx, -ry, rz]
- UV por face: {"uv": [u, v], "uv_size": [l, a]}; nas faces de cima/baixo o Blockbench soma o tamanho
  ao início e inverte o sinal do tamanho.
As animações seguem a mesma convenção do Bedrock (x e y invertidos em relação ao que se vê no Blockbench)."""
import base64, io, json, shutil, sys
from pathlib import Path
from PIL import Image

def r4(v): return round(v, 4) + 0.0

def altura_opaca(modelo: Path):
    """Altura (em unidades, 16 = 1 bloco) da parte visível do modelo já montado: amostra os texels de cada
    face e ignora o que é transparente (as pontas recortadas das chamas)."""
    sys.path.insert(0, str(Path(__file__).parent))
    import numpy as np, previa2
    faces, tex = previa2.carregar(str(modelo))
    H, W = tex.shape[:2]; ys = []
    grade = np.linspace(0.02, 0.98, 12)
    for (c0, c1, c2), (u1, v1, u2, v2), _ in faces:
        c0, c1, c2 = map(np.array, (c0, c1, c2))
        for a in grade:
            for b in grade:
                u = u1 + (u2 - u1) * a; v = v1 + (v2 - v1) * b
                if tex[min(int(v), H - 1), min(int(u), W - 1), 3] > 0:
                    ys.append((c0 + (c1 - c0) * a + (c2 - c0) * b)[1])
    return max(ys) - min(min(ys), 0.0)

def converter(bb, k=1.0):
    """k = escala da geometria (origem, tamanho e pivôs; o UV por face não muda)."""
    els = {e["uuid"]: e for e in bb["elements"]}
    ossos, usados = [], set()

    def nome_unico(nome):
        base, k = nome, 2
        while nome in usados:
            nome = f"{base}_{k}"; k += 1
        usados.add(nome)
        return nome

    def cubo(e):
        de, ate = e["from"], e["to"]
        c = {"origin": [r4(-ate[0] * k), r4(de[1] * k), r4(de[2] * k)], "size": [r4((ate[i] - de[i]) * k) for i in range(3)], "uv": {}}
        rx, ry, rz = e.get("rotation", [0, 0, 0])
        if any(abs(v) > 1e-9 for v in (rx, ry, rz)):
            px, py, pz = e["origin"]
            c["pivot"] = [r4(-px * k), r4(py * k), r4(pz * k)]
            c["rotation"] = [r4(-rx), r4(-ry), r4(rz)]
        for face, fd in e["faces"].items():
            if fd.get("texture") is None: continue
            u1, v1, u2, v2 = fd["uv"]
            w, h = u2 - u1, v2 - v1
            if face in ("up", "down"):
                c["uv"][face] = {"uv": [r4(u1 + w), r4(v1 + h)], "uv_size": [r4(-w), r4(-h)]}
            else:
                c["uv"][face] = {"uv": [r4(u1), r4(v1)], "uv_size": [r4(w), r4(h)]}
        return c

    def visitar(no, pai):
        nome = nome_unico(no["name"])
        ox, oy, oz = no["origin"]
        osso = {"name": nome, "pivot": [r4(-ox * k), r4(oy * k), r4(oz * k)]}
        if pai: osso["parent"] = pai
        rx, ry, rz = no.get("rotation", [0, 0, 0])
        if any(abs(v) > 1e-9 for v in (rx, ry, rz)):
            osso["rotation"] = [r4(-rx), r4(-ry), r4(rz)]
        cubos = [cubo(els[f]) for f in no["children"] if isinstance(f, str) and f in els]
        if cubos: osso["cubes"] = cubos
        ossos.append(osso)
        for f in no["children"]:
            if isinstance(f, dict): visitar(f, nome)

    for no in bb["outliner"]:
        if isinstance(no, dict): visitar(no, None)
    tw, th = bb["resolution"]["width"], bb["resolution"]["height"]
    geo = {"format_version": "1.12.0", "minecraft:geometry": [{
        "description": {"identifier": "geometry.pirococo", "texture_width": tw, "texture_height": th,
                        "visible_bounds_width": 5, "visible_bounds_height": 4, "visible_bounds_offset": [0, 1.5, 0]},
        "bones": ossos}]}
    return geo, {o["name"] for o in ossos}

# ---------------- animações ----------------
def bb(rx, ry, rz):
    """Giro pensado como no Blockbench -> valor do arquivo de animação (convenção Bedrock)."""
    return [-rx, -ry, rz]

def onda(valores, duracao):
    """Valores igualmente espaçados no tempo -> keyframes {"t": valor}; o último fecha o laço."""
    passo = duracao / (len(valores) - 1)
    return {f"{i * passo:.2f}": v for i, v in enumerate(valores)}

def gira(seq, duracao):
    return {"rotation": onda([bb(*v) for v in seq], duracao)}

def animacoes(nomes):
    P = 2.4      # parado: respiração lenta, chamas tremulando
    z = (0, 0, 0)
    parado = {
        "corpo": {"position": onda([[0, 0, 0], [0, 0.3, 0], [0, 0, 0]], P)},
        "pescoco": gira([z, (-2, 0, 0), z], P),
        "cabeca": gira([z, (2, 6, 0), z, (2, -6, 0), z], P),
        "crista_meio": gira([z, (-4, 0, 0), z, (3, 0, 0), z], P),
        "crista_d": gira([z, (0, 0, 4), z], P),
        "crista_e": gira([z, (0, 0, -4), z], P),
        "crista_fora_d": gira([z, (0, 0, 5), z], P),
        "crista_fora_e": gira([z, (0, 0, -5), z], P),
        "cauda_meio": gira([z, (4, 0, 0), z, (-3, 0, 0), z], P),
        "juba": gira([z, (3, 0, 0), z], P),
        "juba_meio_0": gira([z, (4, 0, 0), z, (-4, 0, 0), z], P),
        "juba_d_0": gira([z, (0, -5, 0), z], P),
        "juba_e_0": gira([z, (0, 5, 0), z], P),
        "cauda": gira([z, (-5, 0, 0), z], P),
        "corrente_0_0": gira([z, (4, 0, 0), z, (-3, 0, 0), z], P),
        "corrente_1_0": gira([z, (-3, 0, 0), z, (4, 0, 0), z], P),
        "corrente_2_0": gira([z, (4, 0, 0), z, (-3, 0, 0), z], P),
        "asa_d": gira([z, (0, 0, -2), z], P),
        "asa_e": gira([z, (0, 0, 2), z], P),
        "ombro_d": gira([z, (0, 0, -2), z], P),
        "ombro_e": gira([z, (0, 0, 2), z], P),
    }
    A = 0.8      # andando: passo de galo, cabeça indo e vindo, asas e correntes balançando
    andando = {
        "perna_d": gira([(25, 0, 0), (-25, 0, 0), (25, 0, 0)], A),
        "perna_e": gira([(-25, 0, 0), (25, 0, 0), (-25, 0, 0)], A),
        "corpo": {"position": onda([[0, 0, 0], [0, 0.6, 0], [0, 0, 0], [0, 0.6, 0], [0, 0, 0]], A),
                  "rotation": onda([bb(0, 0, 2), bb(0, 0, -2), bb(0, 0, 2)], A)},
        "pescoco": gira([z, (-9, 0, 0), z, (-9, 0, 0), z], A),
        "cabeca": gira([z, (5, 0, 0), z, (5, 0, 0), z], A),
        "cauda": gira([z, (-7, 0, 0), z, (-7, 0, 0), z], A),
        "juba_cima_0": gira([z, (6, 0, 0), z, (6, 0, 0), z], A),
        "juba_meio_0": gira([z, (5, 0, 0), z, (5, 0, 0), z], A),
        "corrente_0_0": gira([z, (9, 0, 0), z, (9, 0, 0), z], A),
        "corrente_1_0": gira([(6, 0, 0), z, (6, 0, 0), z, (6, 0, 0)], A),
        "corrente_2_0": gira([z, (6, 0, 0), z, (6, 0, 0), z], A),
        "asa_d": gira([z, (0, 0, -5), z, (0, 0, -5), z], A),
        "asa_e": gira([z, (0, 0, 5), z, (0, 0, 5), z], A),
        "ombro_d": gira([z, (0, 0, -4), z, (0, 0, -4), z], A),
        "ombro_e": gira([z, (0, 0, 4), z, (0, 0, 4), z], A),
    }
    faltando = sorted((set(parado) | set(andando)) - nomes)
    so = lambda d: {k: v for k, v in d.items() if k in nomes}
    return {"format_version": "1.8.0", "animations": {
        "animation.pirococo.idle": {"loop": True, "animation_length": P, "bones": so(parado)},
        "animation.pirococo.walk": {"loop": True, "animation_length": A, "bones": so(andando)},
    }}, faltando

# LOD do Pirococó: peças que somem de longe (medidas renderizando o galo no tamanho em que aparece na tela, 1080p,
# FOV 70: cada nível muda no máximo ~2-3% dos pixels). Asas, ombreiras e correntes nunca somem.
LODS = {
    1: [r"^garra_", r"^dedo_tras_", r"^mascara_v", r"^aleta_", r"^peito_", r"^barriga", r"^cranio_c", r"^tronco_"],   # 16+ blocos
    2: [r"^dedo\d_", r"^chifre_meio", r"^sobrancelha", r"^guarda", r"^viseira_quina"],                              # 32+ blocos
    3: [r"^conta_\d+_\d*[13579]$", r"^rufo", r"^juba\d"],                                                           # 48+ blocos
}

def ossos_animados():
    """Nomes de todos os ossos que as animações mexem (os únicos que precisam continuar sendo ossos)."""
    _, todos = animacoes(set())
    return set(todos)

def otimizado(modelo: Path, bbm, lod=True):
    """Achata ossos estáticos, corta faces invisíveis e separa os cubos que brilham (ver otimizar_bb.py)."""
    import numpy as np
    from otimizar_bb import otimizar
    src = bbm["textures"][0]["source"].split(",", 1)[1]
    tex = np.asarray(Image.open(io.BytesIO(base64.b64decode(src))).convert("RGBA"))
    caminho_brilho = modelo.with_name(modelo.stem + "_glowmask.png")
    brilho = np.asarray(Image.open(caminho_brilho).convert("RGBA")) if caminho_brilho.exists() else np.zeros_like(tex)
    novo, rel = otimizar(bbm, tex, brilho, ossos_animados(), LODS if lod else {})
    print(f"otimização: ossos {rel['ossos_antes']} -> {rel['ossos_depois']}, cubos -> {rel['cubos_depois']}, "
          f"faces {rel['faces_antes']} -> {rel['faces_depois']} (transparentes {rel['transparentes']}, "
          f"bordas finas {rel['bordas']}, escondidas {rel['ocultas']}), cubos com brilho {rel['cubos_brilho']}, "
          f"faces que somem de longe por nível {dict(sorted(rel['faces_lod'].items()))}")
    return novo

def exportar(modelo: Path, destino: Path, altura_blocos=2.45, otimizar=True, lod=True):
    bbm = json.loads(modelo.read_text(encoding="utf-8"))
    alt = altura_opaca(modelo)
    k = altura_blocos * 16 / alt
    if otimizar:
        sys.path.insert(0, str(Path(__file__).parent))
        bbm = otimizado(modelo, bbm, lod)
    geo, nomes = converter(bbm, k)
    print(f"altura do modelo: {alt / 16:.2f} blocos -> {altura_blocos:.2f} (escala {k:.3f})")
    (destino / "geckolib/models/entity").mkdir(parents=True, exist_ok=True)
    (destino / "geckolib/models/entity/pirococo.geo.json").write_text(json.dumps(geo, indent=1), encoding="utf-8")
    anim, faltando = animacoes(nomes)
    (destino / "geckolib/animations/entity").mkdir(parents=True, exist_ok=True)
    (destino / "geckolib/animations/entity/pirococo.animation.json").write_text(json.dumps(anim, indent=1), encoding="utf-8")
    (destino / "textures/entity").mkdir(parents=True, exist_ok=True)
    src = bbm["textures"][0]["source"].split(",", 1)[1]
    tex = Image.open(io.BytesIO(base64.b64decode(src))).convert("RGBA")
    tex.save(destino / "textures/entity/pirococo.png")
    brilho = modelo.with_name(modelo.stem + "_glowmask.png")
    if brilho.exists(): shutil.copyfile(brilho, destino / "textures/entity/pirococo_glowmask.png")
    else: Image.new("RGBA", tex.size, (0, 0, 0, 0)).save(destino / "textures/entity/pirococo_glowmask.png")
    ncubos = sum(len(o.get("cubes", [])) for o in geo["minecraft:geometry"][0]["bones"])
    print(f"ok: {ncubos} cubos em {len(nomes)} ossos, textura {tex.size[0]}x{tex.size[1]}; "
          f"ossos animados ausentes: {faltando or 'nenhum'}")

if __name__ == "__main__":
    # opções depois da altura: "--sem-otimizar" (exporta como antes: todos os ossos e faces) e "--sem-lod" (sem os
    # ossos de nível de detalhe); servem para comparar desempenho
    exportar(Path(sys.argv[1]), Path(sys.argv[2]), float(sys.argv[3]) if len(sys.argv) > 3 else 2.45,
             otimizar="--sem-otimizar" not in sys.argv[4:], lod="--sem-lod" not in sys.argv[4:])
