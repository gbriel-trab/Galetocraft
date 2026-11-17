"""Exporta o Pirococó v6 para o formato do GeckoLib (geometria Bedrock .geo.json), com textura,
textura de brilho (_glowmask) e animações (parado / andando).

Uso: python exportar_geckolib.py <pasta assets/galetocraft do mod>

Convenção Bedrock (a mesma do Blockbench ao exportar): X espelhado, pivô = [-x, y, z],
rotação do osso = [-rx, -ry, rz], origem do cubo = [-(x final), y inicial, z inicial]."""
import json, shutil, sys
from pathlib import Path
from PIL import Image

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import pirococo6
from galos_monstro import Modelo

def exportar(destino: Path):
    m = Modelo(pirococo6.NOME)
    outliner = pirococo6.montar(m)
    _, n, (tw, th) = m.salvar(outliner, largura=128, pasta=pirococo6.PASTA)
    cubos = {c["uuid"]: c for c in m.cubos.values()}

    # ---------------- geometria ----------------
    ossos, usados = [], set()
    def nome_unico(nome):
        base, k = nome, 2
        while nome in usados:
            nome = f"{base}_{k}"; k += 1
        usados.add(nome)
        return nome
    def visitar(no, pai):
        nome = nome_unico(no["name"])
        ox, oy, oz = no["origin"]
        osso = {"name": nome, "pivot": [-ox, oy, oz]}
        if pai: osso["parent"] = pai
        rx, ry, rz = no["rotation"]
        if any(abs(v) > 1e-9 for v in (rx, ry, rz)):
            osso["rotation"] = [-rx, -ry, rz]
        lista = []
        for f in no["children"]:
            if isinstance(f, str):
                c = cubos[f]
                cubo = {"origin": [-c["to"][0], c["from"][1], c["from"][2]],
                        "size": list(c["size"]), "uv": list(c["uv_offset"])}
                if c["espelho_de"]: cubo["mirror"] = True
                lista.append(cubo)
        if lista: osso["cubes"] = lista
        ossos.append(osso)
        for f in no["children"]:
            if isinstance(f, dict): visitar(f, nome)
    for no in outliner: visitar(no, None)

    geo = {"format_version": "1.12.0", "minecraft:geometry": [{
        "description": {"identifier": "geometry.pirococo", "texture_width": tw, "texture_height": th,
                        "visible_bounds_width": 4, "visible_bounds_height": 3.5, "visible_bounds_offset": [0, 1.5, 0]},
        "bones": ossos}]}
    (destino / "geckolib/models/entity").mkdir(parents=True, exist_ok=True)
    (destino / "geckolib/models/entity/pirococo.geo.json").write_text(json.dumps(geo, indent=1), encoding="utf-8")

    # ---------------- texturas ----------------
    (destino / "textures/entity").mkdir(parents=True, exist_ok=True)
    png = pirococo6.PASTA / f"{pirococo6.NOME}.png"
    shutil.copyfile(png, destino / "textures/entity/pirococo.png")
    tex = Image.open(png).convert("RGBA")
    brilho = Image.new("RGBA", tex.size, (0, 0, 0, 0))
    def brilha(nome):   # chamas da crista, gemas e pontas de fogo da juba/cauda brilham no escuro
        return ("crista" in nome or "gema" in nome
                or (nome.startswith(("juba", "cauda_")) and nome.endswith("_ponta")))
    for c in m.cubos.values():
        if c["espelho_de"] or c["uv_de"] or not brilha(c["name"]): continue
        w, h, d = c["size"]; u, v = c["uv_offset"]
        caixa = (u, v, u + 2 * (d + w), v + d + h)
        brilho.paste(tex.crop(caixa), caixa[:2])
    brilho.save(destino / "textures/entity/pirococo_glowmask.png")

    # ---------------- animações ----------------
    def onda(valores, duracao):
        """Lista de valores igualmente espaçados no tempo -> keyframes {"t": [..]}."""
        passo = duracao / (len(valores) - 1)
        return {f"{i * passo:.2f}": v for i, v in enumerate(valores)}
    nomes = {o["name"] for o in ossos}
    def so_existentes(bones):
        return {k: v for k, v in bones.items() if k in nomes}

    D = 2.4      # parado: respiração lenta
    parado = {
        "corpo": {"position": onda([[0, 0, 0], [0, 0.3, 0], [0, 0, 0]], D)},
        "pescoco": {"rotation": onda([[0, 0, 0], [-2, 0, 0], [0, 0, 0]], D)},
        "cabeca": {"rotation": onda([[0, 0, 0], [3, 6, 0], [0, 0, 0], [3, -6, 0], [0, 0, 0]], D)},
        "juba_meio": {"rotation": onda([[0, 0, 0], [5, 0, 0], [0, 0, 0]], D)},
        "juba_cima": {"rotation": onda([[0, 0, 0], [-5, 0, 0], [0, 0, 0]], D)},
        "cauda": {"rotation": onda([[0, 0, 0], [-4, 0, 0], [0, 0, 0]], D)},
        "elo_0_0": {"rotation": onda([[0, 0, 0], [5, 0, 0], [0, 0, 0]], D)},
        "elo_1_0": {"rotation": onda([[0, 0, 0], [6, 0, 0], [0, 0, 0]], D)},
        "elo_2_0": {"rotation": onda([[0, 0, 0], [4, 0, 0], [0, 0, 0]], D)},
        "ombro_d": {"rotation": onda([[0, 0, 0], [0, 0, 2], [0, 0, 0]], D)},
        "ombro_e": {"rotation": onda([[0, 0, 0], [0, 0, -2], [0, 0, 0]], D)},
    }
    A = 0.8      # andando: passo de galo, com a cabeça indo para frente e para trás
    andando = {
        "perna_d": {"rotation": onda([[25, 0, 0], [-25, 0, 0], [25, 0, 0]], A)},
        "perna_e": {"rotation": onda([[-25, 0, 0], [25, 0, 0], [-25, 0, 0]], A)},
        "corpo": {"position": onda([[0, 0, 0], [0, 0.6, 0], [0, 0, 0], [0, 0.6, 0], [0, 0, 0]], A),
                  "rotation": onda([[0, 0, 2], [0, 0, -2], [0, 0, 2]], A)},
        "pescoco": {"rotation": onda([[0, 0, 0], [10, 0, 0], [0, 0, 0], [10, 0, 0], [0, 0, 0]], A)},
        "cauda": {"rotation": onda([[0, 0, 0], [-6, 0, 0], [0, 0, 0], [-6, 0, 0], [0, 0, 0]], A)},
        "elo_0_0": {"rotation": onda([[0, 0, 0], [10, 0, 0], [0, 0, 0], [10, 0, 0], [0, 0, 0]], A)},
        "elo_1_0": {"rotation": onda([[0, 0, 0], [12, 0, 0], [0, 0, 0], [12, 0, 0], [0, 0, 0]], A)},
        "elo_2_0": {"rotation": onda([[0, 0, 0], [8, 0, 0], [0, 0, 0], [8, 0, 0], [0, 0, 0]], A)},
        "ombro_d": {"rotation": onda([[0, 0, 0], [0, 0, 6], [0, 0, 0]], A)},
        "ombro_e": {"rotation": onda([[0, 0, 0], [0, 0, -6], [0, 0, 0]], A)},
    }
    anim = {"format_version": "1.8.0", "animations": {
        "animation.pirococo.idle": {"loop": True, "animation_length": D, "bones": so_existentes(parado)},
        "animation.pirococo.walk": {"loop": True, "animation_length": A, "bones": so_existentes(andando)},
    }}
    faltando = (set(parado) | set(andando)) - nomes
    (destino / "geckolib/animations/entity").mkdir(parents=True, exist_ok=True)
    (destino / "geckolib/animations/entity/pirococo.animation.json").write_text(json.dumps(anim, indent=1), encoding="utf-8")
    print(f"ok: {n} cubos em {len(ossos)} ossos, textura {tw}x{th}; ossos animados ausentes: {sorted(faltando) or 'nenhum'}")

if __name__ == "__main__":
    exportar(Path(sys.argv[1]))
