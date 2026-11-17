import sys
sys.path.insert(0, r"C:\Users\gbriel\Desktop\galopiru\ferramentas")
import galo_base as g, previa2
q = previa2.carregar(r"C:\Users\gbriel\Desktop\galopiru\modelos\axococo\axococo.bbmodel")
cx, cy, cz, r, yaw, pitch, esc, out = sys.argv[1:9]
g.desenhar_parte(q, (float(cx), float(cy), float(cz)), float(r), float(yaw), float(pitch), float(esc)).save(out)
