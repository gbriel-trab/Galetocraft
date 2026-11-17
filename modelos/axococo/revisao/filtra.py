import sys, json
sys.path.insert(0, r"C:\Users\gbriel\Desktop\galopiru\ferramentas")
import previa2
m = json.load(open(r"C:\Users\gbriel\Desktop\galopiru\modelos\axococo\axococo.bbmodel", encoding="utf-8"))
pref = sys.argv[1].split(",")
m["elements"] = [e for e in m["elements"] if any(e["name"].startswith(p) for p in pref)]
print([e["name"] for e in m["elements"]])
open(r"C:\Users\gbriel\Desktop\galopiru\modelos\axococo\revisao\tmp.bbmodel", "w", encoding="utf-8").write(json.dumps(m))
q = previa2.carregar(r"C:\Users\gbriel\Desktop\galopiru\modelos\axococo\revisao\tmp.bbmodel")
previa2.desenhar(q, float(sys.argv[2]), float(sys.argv[3]), escala=20, fundo=(14,10,12)).save(sys.argv[4])
