"""Exporta uma espécie do Galetocraft para o mod (mesmo caminho do Pirococó: exportar_v7.py + otimizar_bb.py).

Entrada: ferramentas/especies/<id>.py (ALTURA, QUADRUPEDE, ONDAS, ANIM_PARADO, ANIM_ANDANDO, LODS opcional)
         modelos/<id>/<id>.bbmodel (+ <id>_glowmask.png), gerados por `python ferramentas/especies/<id>.py`
         modelos/<id>/lods.json (opcional, gerado por lod_auto.py; LODS no arquivo da espécie tem prioridade)
Saída (assets/galetocraft do mod):
         geckolib/models/entity/<id>.geo.json, geckolib/animations/entity/<id>.animation.json,
         textures/entity/<id>.png e <id>_glowmask.png

Uso: python exportar_especie.py <id> [--sem-otimizar] [--sem-lod]"""
import base64, importlib.util, io, json, math, shutil, sys
from pathlib import Path
from PIL import Image

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))
from exportar_v7 import altura_opaca, converter, onda, gira, bb as giro_bb

ASSETS = RAIZ / "galetocraft" / "src" / "main" / "resources" / "assets" / "galetocraft"

def carregar_especie(id_):
    spec = importlib.util.spec_from_file_location(f"especie_{id_}", AQUI / "especies" / f"{id_}.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

def senoide(amp, fase=0.0, n=8):
    """Laço de n keyframes (+ o de fechamento) de uma senoide com amplitude (rx, ry, rz)."""
    vals = [tuple(a * math.sin(2 * math.pi * k / n + fase) for a in amp) for k in range(n)]
    return vals + [vals[0]]

def animacoes(esp, id_, nomes):
    """Parado (respira, olha em volta) e andando (passo), para os ossos padrão + ondas + extras da espécie."""
    P, A = 2.4, 0.8
    z = (0, 0, 0)
    quad = getattr(esp, "QUADRUPEDE", False)
    parado = {
        "corpo": {"position": onda([[0, 0, 0], [0, 0.3, 0], [0, 0, 0]], P)},
        "pescoco": gira([z, (-2, 0, 0), z], P),
        "cabeca": gira([z, (2, 6, 0), z, (2, -6, 0), z], P),
        "crista": gira([z, (-3, 0, 0), z, (2, 0, 0), z], P),
        "cauda": gira([z, (-5, 0, 0), z], P),
        "asa_d": gira([z, (0, 0, -2), z], P),
        "asa_e": gira([z, (0, 0, 2), z], P),
    }
    andando = {
        "corpo": {"position": onda([[0, 0, 0], [0, 0.6, 0], [0, 0, 0], [0, 0.6, 0], [0, 0, 0]], A),
                  "rotation": onda([giro_bb(0, 0, 2 if not quad else 1), giro_bb(0, 0, -2 if not quad else -1),
                                    giro_bb(0, 0, 2 if not quad else 1)], A)},
        "pescoco": gira([z, (-9 if not quad else -5, 0, 0), z, (-9 if not quad else -5, 0, 0), z], A),
        "cabeca": gira([z, (5, 0, 0), z, (5, 0, 0), z], A),
        "crista": gira([z, (-4, 0, 0), z, (-4, 0, 0), z], A),
        "cauda": gira([z, (-7, 0, 0), z, (-7, 0, 0), z], A),
        "asa_d": gira([z, (0, 0, -5), z, (0, 0, -5), z], A),
        "asa_e": gira([z, (0, 0, 5), z, (0, 0, 5), z], A),
    }
    if quad:   # passo em diagonal: frente-direita junto com trás-esquerda
        f, t = (22, 0, 0), (-22, 0, 0)
        andando["perna_fd"] = gira([f, t, f], A); andando["perna_te"] = gira([f, t, f], A)
        andando["perna_fe"] = gira([t, f, t], A); andando["perna_td"] = gira([t, f, t], A)
    else:
        andando["perna_d"] = gira([(25, 0, 0), (-25, 0, 0), (25, 0, 0)], A)
        andando["perna_e"] = gira([(-25, 0, 0), (25, 0, 0), (-25, 0, 0)], A)
    for prefixo, n, amp in getattr(esp, "ONDAS", []):
        for k in range(n):
            parado[f"{prefixo}_{k}"] = gira(senoide(amp, -0.7 * k), P)
            andando[f"{prefixo}_{k}"] = gira(senoide(tuple(1.5 * a for a in amp), -0.7 * k), A)
    for nome, seq in getattr(esp, "ANIM_PARADO", {}).items():
        parado[nome] = seq if isinstance(seq, dict) else gira(seq, P)
    for nome, seq in getattr(esp, "ANIM_ANDANDO", {}).items():
        andando[nome] = seq if isinstance(seq, dict) else gira(seq, A)
    todos = set(parado) | set(andando)
    so = lambda d: {k: v for k, v in d.items() if k in nomes}
    return {"format_version": "1.8.0", "animations": {
        f"animation.{id_}.idle": {"loop": True, "animation_length": P, "bones": so(parado)},
        f"animation.{id_}.walk": {"loop": True, "animation_length": A, "bones": so(andando)},
    }}, todos

def lods_da_especie(esp, id_):
    if getattr(esp, "LODS", None): return {int(k): v for k, v in esp.LODS.items()}
    arq = RAIZ / "modelos" / id_ / "lods.json"
    if arq.exists(): return {int(k): v for k, v in json.loads(arq.read_text(encoding="utf-8")).items()}
    return {}

def exportar(id_, otimizar=True, lod=True, destino=ASSETS):
    esp = carregar_especie(id_)
    modelo = RAIZ / "modelos" / id_ / f"{id_}.bbmodel"
    bbm = json.loads(modelo.read_text(encoding="utf-8"))
    from dimensoes import DIMENSOES   # tabela oficial do dono: vale mais que o ALTURA do arquivo da espécie
    altura = DIMENSOES[id_][0] if id_ in DIMENSOES else getattr(esp, "ALTURA", 2.45)
    alt = altura_opaca(modelo)
    k = altura * 16 / alt
    _, animados = animacoes(esp, id_, set())
    if otimizar:
        import numpy as np
        from otimizar_bb import otimizar as otimizar_bb
        src = bbm["textures"][0]["source"].split(",", 1)[1]
        tex = np.asarray(Image.open(io.BytesIO(base64.b64decode(src))).convert("RGBA"))
        cam_brilho = modelo.with_name(f"{id_}_glowmask.png")
        brilho = np.asarray(Image.open(cam_brilho).convert("RGBA")) if cam_brilho.exists() else np.zeros_like(tex)
        bbm, rel = otimizar_bb(bbm, tex, brilho, animados, lods_da_especie(esp, id_) if lod else {})
        print(f"otimização: ossos {rel['ossos_antes']} -> {rel['ossos_depois']}, cubos -> {rel['cubos_depois']}, "
              f"faces {rel['faces_antes']} -> {rel['faces_depois']}, cubos com brilho {rel['cubos_brilho']}, "
              f"faces de LOD por nível {dict(sorted(rel['faces_lod'].items()))}")
    geo, nomes = converter(bbm, k)
    geo["minecraft:geometry"][0]["description"]["identifier"] = f"geometry.{id_}"
    print(f"{id_}: altura do modelo {alt / 16:.2f} blocos -> {altura:.2f} (escala {k:.3f})")
    for sub in ("geckolib/models/entity", "geckolib/animations/entity", "textures/entity"):
        (destino / sub).mkdir(parents=True, exist_ok=True)
    (destino / f"geckolib/models/entity/{id_}.geo.json").write_text(json.dumps(geo, indent=1), encoding="utf-8")
    anim, _ = animacoes(esp, id_, nomes)
    (destino / f"geckolib/animations/entity/{id_}.animation.json").write_text(json.dumps(anim, indent=1), encoding="utf-8")
    src = bbm["textures"][0]["source"].split(",", 1)[1]
    tex = Image.open(io.BytesIO(base64.b64decode(src))).convert("RGBA")
    tex.save(destino / f"textures/entity/{id_}.png")
    brilho = modelo.with_name(f"{id_}_glowmask.png")
    if brilho.exists(): shutil.copyfile(brilho, destino / f"textures/entity/{id_}_glowmask.png")
    else: Image.new("RGBA", tex.size, (0, 0, 0, 0)).save(destino / f"textures/entity/{id_}_glowmask.png")
    ncubos = sum(len(o.get("cubes", [])) for o in geo["minecraft:geometry"][0]["bones"])
    usados = set(anim["animations"][f"animation.{id_}.idle"]["bones"]) | set(anim["animations"][f"animation.{id_}.walk"]["bones"])
    print(f"ok: {ncubos} cubos em {len(nomes)} ossos, textura {tex.size[0]}x{tex.size[1]}, ossos animados: {sorted(usados)}")
    return k

if __name__ == "__main__":
    exportar(sys.argv[1], otimizar="--sem-otimizar" not in sys.argv[2:], lod="--sem-lod" not in sys.argv[2:])
