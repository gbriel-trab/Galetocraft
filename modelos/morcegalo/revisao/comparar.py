"""Monta ref (vistas da ficha) em cima e a rodada embaixo, na mesma altura, para comparar."""
import sys
from PIL import Image
r = sys.argv[1]
ref = Image.open('modelos/referencias/010_morcegalo_vistas.png').convert('RGB')
ref = ref.crop((60, 80, 1780, 420))
nos = Image.open(f'modelos/morcegalo/revisao/{r}_vistas.png').convert('RGB')
W = 1800
ref = ref.resize((W, int(ref.height * W / ref.width)))
nos = nos.resize((W, int(nos.height * W / nos.width)))
o = Image.new('RGB', (W, ref.height + nos.height)); o.paste(ref, (0, 0)); o.paste(nos, (0, ref.height))
o.save(f'modelos/morcegalo/revisao/{r}_comparar.png')
