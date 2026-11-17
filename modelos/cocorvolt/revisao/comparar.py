"""Junta a ficha (vistas) e a rodada atual numa imagem só, para comparar."""
import sys
from PIL import Image
ref = Image.open(r"modelos/referencias/006_cocorvolt_vistas.png").convert("RGB").crop((30, 80, 1230, 470))
nos = Image.open(sys.argv[1]).convert("RGB")
k = ref.width / nos.width
nos = nos.resize((ref.width, int(nos.height * k)))
out = Image.new("RGB", (ref.width, ref.height + nos.height), (0, 0, 0))
out.paste(ref, (0, 0)); out.paste(nos, (0, ref.height)); out.save(sys.argv[2])
