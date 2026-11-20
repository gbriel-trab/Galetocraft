"""Gera os recursos de item e texto das espécies do Galetocraft (além do Pirococó, que já existe):
ovo gerador (textura 16x16 + modelos do item) e nomes em pt_br / en_us.
Uso: python registrar_especies.py"""
import json, random
from pathlib import Path
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "galetocraft" / "src" / "main" / "resources" / "assets" / "galetocraft"

# id, nome, cor de fundo do ovo, cor das pintas
ESPECIES = [
    ("esporoco", "Esporocó", (92, 170, 62), (236, 82, 160)),
    ("cocorak", "Cocórak", (214, 176, 110), (64, 38, 74)),
    ("cocorion", "Cocórion", (236, 232, 222), (40, 100, 62)),
    ("cocorvolt", "Cocórvolt", (104, 108, 120), (255, 212, 40)),
    ("taturico", "Taturico", (150, 96, 60), (228, 172, 112)),
    ("axococo", "Axococó", (246, 172, 202), (62, 122, 232)),
    ("vagalo", "Vagaló", (72, 48, 92), (255, 222, 60)),
    ("morcegalo", "Morcegalo", (112, 62, 172), (240, 122, 200)),
    ("espinhoco", "Espinhocó", (132, 92, 60), (132, 192, 62)),
    ("salambrasa", "Salambrasa", (70, 56, 66), (255, 150, 40)),
    ("renacoco", "Renacocó", (124, 40, 170), (90, 200, 245)),
]
SEM_ACENTO = str.maketrans("áéíóúâêôãõç", "aeiouaeoaoc")

def ovo(fundo, pinta, semente):
    """Ovo 16x16 com o mesmo contorno do ovo do Pirococó: luz em cima à esquerda, sombra embaixo, borda escura."""
    molde = Image.open(Path(__file__).resolve().parent / "molde_ovo.png").convert("RGBA")
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    dentro = lambda x, y: 0 <= x < 16 and 0 <= y < 16 and molde.getpixel((x, y))[3] > 0
    escuro = tuple(int(c * 0.35) for c in fundo)
    rnd = random.Random(semente)
    pintas = set()
    while len(pintas) < 7:
        x, y = rnd.randint(4, 11), rnd.randint(3, 13)
        if dentro(x, y) and dentro(x + 1, y) and all(abs(x - a) + abs(y - b) > 2 for a, b in pintas): pintas.add((x, y))
    for y in range(16):
        for x in range(16):
            if not dentro(x, y): continue
            if not all(dentro(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                img.putpixel((x, y), escuro + (255,)); continue
            f = 1.12 - 0.03 * (x - 5) - 0.025 * (y - 4)
            cor = tuple(max(0, min(255, int(c * f))) for c in fundo)
            for a, b in pintas:
                if (x, y) in ((a, b), (a + 1, b)) or ((x, y) == (a, b + 1) and (a + b) % 2 == 0):
                    cor = tuple(max(0, min(255, int(c * (f * 0.95)))) for c in pinta)
            if (x, y) in ((5, 3), (4, 4), (5, 4)): cor = tuple(min(255, c + 70) for c in cor)
            img.putpixel((x, y), cor + (255,))
    return img

def main():
    lang = {arq: json.loads((ASSETS / "lang" / arq).read_text(encoding="utf-8")) for arq in ("pt_br.json", "en_us.json")}
    for i, (id_, nome, fundo, pinta) in enumerate(ESPECIES):
        ovo(fundo, pinta, i + 7).save(ASSETS / "textures" / "item" / f"{id_}_spawn_egg.png")
        (ASSETS / "items" / f"{id_}_spawn_egg.json").write_text(json.dumps(
            {"model": {"type": "minecraft:model", "model": f"galetocraft:item/{id_}_spawn_egg"}}, indent=2) + "\n", encoding="utf-8")
        (ASSETS / "models" / "item" / f"{id_}_spawn_egg.json").write_text(json.dumps(
            {"parent": "minecraft:item/generated", "textures": {"layer0": f"galetocraft:item/{id_}_spawn_egg"}}, indent=2) + "\n", encoding="utf-8")
        lang["pt_br.json"][f"entity.galetocraft.{id_}"] = nome
        lang["pt_br.json"][f"item.galetocraft.{id_}_spawn_egg"] = f"Ovo Gerador de {nome}"
        lang["en_us.json"][f"entity.galetocraft.{id_}"] = nome.translate(SEM_ACENTO)
        lang["en_us.json"][f"item.galetocraft.{id_}_spawn_egg"] = f"{nome.translate(SEM_ACENTO)} Spawn Egg"
    for arq, d in lang.items():
        (ASSETS / "lang" / arq).write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"{len(ESPECIES)} espécies: ovos, modelos de item e nomes gravados em {ASSETS}")

if __name__ == "__main__":
    main()
