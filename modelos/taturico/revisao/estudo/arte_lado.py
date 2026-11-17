"""Monta <rodada>_arte_lado.png: a arte conceitual (recortada) ao lado do modelo renderizado no ângulo da arte,
na mesma altura total. Uso: python arte_lado.py <rodada> [yaw] [pitch]"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
RAIZ = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(RAIZ / "ferramentas"))
import previa2
rod = sys.argv[1]; yaw = float(sys.argv[2]) if len(sys.argv) > 2 else 62; pitch = float(sys.argv[3]) if len(sys.argv) > 3 else -10
arte = Image.open(RAIZ / "modelos/referencias/007_taturico_arte.png").convert("RGB").crop((50, 50, 870, 910))
q = previa2.carregar(str(RAIZ / "modelos/taturico/revisao" / f"{rod}.bbmodel"))
m = previa2.desenhar(q, yaw, pitch, escala=20, fundo=(14, 10, 12), margem=4)
bb = Image.eval(m.convert("L"), lambda v: 255 if v > 20 else 0).getbbox()
m = m.crop(bb)
H = arte.height
m = m.resize((int(m.width * H / m.height), H), Image.LANCZOS)
out = Image.new("RGB", (arte.width + m.width + 20, H), (14, 10, 12))
out.paste(arte, (0, 0)); out.paste(m, (arte.width + 20, 0))
# grade de 10% da altura
d = ImageDraw.Draw(out)
for i in range(11):
    y = int(H * i / 10); d.line([(0, y), (out.width, y)], fill=(60, 200, 255), width=1)
out.save(RAIZ / "modelos/taturico/revisao" / f"{rod}_arte_lado.png")
print("ok", out.size)
