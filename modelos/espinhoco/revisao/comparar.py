import sys
from PIL import Image
r = Image.open("modelos/referencias/011_espinhoco_vistas.png").convert("RGB")
m = Image.open(f"modelos/espinhoco/revisao/{sys.argv[1]}_vistas.png").convert("RGB")
k = r.width / m.width
m = m.resize((r.width, int(m.height * k)))
f = Image.new("RGB", (r.width, r.height + m.height), (0, 0, 0)); f.paste(r, (0, 0)); f.paste(m, (0, r.height))
f.save(f"modelos/espinhoco/revisao/{sys.argv[1]}_comparar.png")
