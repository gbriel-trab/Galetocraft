"""Close do rosto escondendo peças por prefixo (depuração)."""
import sys, json
sys.path.insert(0, "ferramentas")
import previa2, galo_base as g
from PIL import Image
m = json.load(open("modelos/cocorvolt/cocorvolt.bbmodel", encoding="utf-8"))
tira = sys.argv[2].split(",") if len(sys.argv) > 2 and sys.argv[2] else []
m["elements"] = [e for e in m["elements"] if not any(e["name"].startswith(t) for t in tira)]
open("modelos/cocorvolt/revisao/_dep.bbmodel", "w", encoding="utf-8").write(json.dumps(m))
q = previa2.carregar("modelos/cocorvolt/revisao/_dep.bbmodel")
yaw = float(sys.argv[3]) if len(sys.argv) > 3 else 0
g.desenhar_parte(q, (0, 28.0, -3.0), 7.5, yaw, -6, 60).save(sys.argv[1])
