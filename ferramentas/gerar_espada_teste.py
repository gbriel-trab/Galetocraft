"""Gera um modelo de teste (espada 3D) no formato do Blockbench (.bbmodel),
com a textura 16x16 embutida, mais o par Java (models/item/*.json + textura .png)."""
import base64, io, json, uuid
from pathlib import Path
from PIL import Image

NOME = "espada_teste"
SAIDA = Path(__file__).resolve().parent.parent / "modelos"
SAIDA.mkdir(exist_ok=True)

# ---------- textura 16x16 ----------
img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
px = img.load()

def rect(x0, y0, x1, y1, cor):
    for x in range(x0, x1):
        for y in range(y0, y1):
            px[x, y] = cor + (255,)

FERRO_CLARO, FERRO, FERRO_ESC, FERRO_BORDA = (236, 241, 246), (196, 202, 210), (150, 156, 167), (108, 114, 126)
OURO_CLARO, OURO, OURO_ESC = (255, 228, 110), (236, 184, 42), (176, 124, 22)
COURO, COURO_ESC = (116, 74, 42), (78, 48, 26)

# lâmina frente/trás (2x9): coluna clara + coluna média, ponta de cima mais clara
rect(0, 0, 1, 9, FERRO_CLARO); rect(1, 0, 2, 9, FERRO)
px[1, 8] = FERRO_ESC + (255,)
# lâmina lados (1x9) e topo/base (2x1)
rect(2, 0, 3, 9, FERRO_ESC); rect(0, 9, 2, 10, FERRO_BORDA)
# ponta (1x1)
rect(3, 0, 4, 1, FERRO_CLARO); rect(3, 1, 4, 2, FERRO)
# guarda frente (6x1), lados (2x1), topo/base (6x2)
rect(4, 0, 10, 1, OURO); px[4, 0] = OURO_ESC + (255,); px[9, 0] = OURO_ESC + (255,); px[6, 0] = OURO_CLARO + (255,)
rect(10, 0, 12, 1, OURO_ESC)
rect(4, 1, 10, 3, OURO); rect(4, 1, 10, 2, OURO_CLARO)
# cabo (1x4) com faixas de couro; topo/base (1x1)
for y in range(4):
    rect(12, y, 13, y + 1, COURO if y % 2 == 0 else COURO_ESC)
rect(13, 0, 14, 1, COURO_ESC)
# pomo lados (2x1), topo/base (2x2)
rect(4, 4, 6, 5, OURO); px[4, 4] = OURO_CLARO + (255,)
rect(4, 5, 6, 7, OURO_ESC); px[4, 5] = OURO + (255,)

img.save(SAIDA / f"{NOME}.png")
buf = io.BytesIO(); img.save(buf, format="PNG")
data_uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# ---------- cubos ----------
def faces(ns, ew, ud):
    return {"north": {"uv": ns, "texture": 0}, "south": {"uv": ns, "texture": 0},
            "east": {"uv": ew, "texture": 0}, "west": {"uv": ew, "texture": 0},
            "up": {"uv": ud, "texture": 0}, "down": {"uv": ud, "texture": 0}}

partes = [
    ("pomo",   [7, 0, 7],     [9, 1, 9],      faces([4, 4, 6, 5],  [4, 4, 6, 5],  [4, 5, 6, 7])),
    ("cabo",   [7.5, 1, 7.5], [8.5, 5, 8.5],  faces([12, 0, 13, 4], [12, 0, 13, 4], [13, 0, 14, 1])),
    ("guarda", [5, 5, 7],     [11, 6, 9],     faces([4, 0, 10, 1], [10, 0, 12, 1], [4, 1, 10, 3])),
    ("lamina", [7, 6, 7.5],   [9, 15, 8.5],   faces([0, 0, 2, 9],  [2, 0, 3, 9],  [0, 9, 2, 10])),
    ("ponta",  [7.5, 15, 7.5], [8.5, 16, 8.5], faces([3, 0, 4, 1], [3, 1, 4, 2],  [3, 0, 4, 1])),
]

elementos = []
for nome, de, ate, fc in partes:
    elementos.append({"name": nome, "box_uv": False, "rescale": False, "locked": False,
                      "from": de, "to": ate, "autouv": 0, "color": 0, "origin": [8, 8, 8],
                      "faces": fc, "type": "cube", "uuid": str(uuid.uuid4())})

bbmodel = {
    "meta": {"format_version": "4.10", "model_format": "java_block", "box_uv": False},
    "name": NOME,
    "parent": "",
    "ambientocclusion": True,
    "front_gui_light": False,
    "visible_box": [1, 1, 0],
    "resolution": {"width": 16, "height": 16},
    "elements": elementos,
    "outliner": [e["uuid"] for e in elementos],
    "textures": [{"path": "", "name": f"{NOME}.png", "folder": "item", "namespace": "", "id": "0",
                  "width": 16, "height": 16, "uv_width": 16, "uv_height": 16,
                  "particle": False, "render_mode": "default", "visible": True, "internal": True,
                  "saved": False, "uuid": str(uuid.uuid4()), "relative_path": "", "source": data_uri}],
    "display": {
        "thirdperson_righthand": {"rotation": [0, 90, 45], "translation": [0, 4, 0.5], "scale": [0.85, 0.85, 0.85]},
        "firstperson_righthand": {"rotation": [0, 90, 25], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]},
        "gui": {"rotation": [0, 0, -45], "translation": [0, 0, 0], "scale": [0.9, 0.9, 0.9]},
        "ground": {"translation": [0, 2, 0], "scale": [0.5, 0.5, 0.5]},
    },
}
(SAIDA / f"{NOME}.bbmodel").write_text(json.dumps(bbmodel, indent=1), encoding="utf-8")

# ---------- formato que o Minecraft Java lê (models/item/espada_teste.json) ----------
java = {
    "textures": {"0": f"meumod:item/{NOME}", "particle": f"meumod:item/{NOME}"},
    "elements": [{"name": e["name"], "from": e["from"], "to": e["to"],
                  "faces": {k: {"uv": v["uv"], "texture": "#0"} for k, v in e["faces"].items()}}
                 for e in elementos],
    "display": bbmodel["display"],
}
(SAIDA / f"{NOME}.json").write_text(json.dumps(java, indent=1), encoding="utf-8")
print("ok ->", SAIDA)
