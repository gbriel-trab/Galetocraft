import sys
from PIL import Image
ref = Image.open("modelos/referencias/009_vagalo_vistas.png").convert("RGB")
nos = Image.open(sys.argv[1]).convert("RGB")
w = 1400
r = ref.resize((w, int(ref.height * w / ref.width)))
n = nos.resize((w, int(nos.height * w / nos.width)))
f = Image.new("RGB", (w, r.height + n.height), (0, 0, 0)); f.paste(r, (0, 0)); f.paste(n, (0, r.height))
f.save(sys.argv[2])
