"""Renderiza só os ossos pedidos (debug). Uso: python parte.py saida.png yaw pitch osso1 [osso2...]"""
import json, sys
sys.path.insert(0, "ferramentas")
import previa2
saida, yaw, pitch, nomes = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4:]
m = json.load(open("modelos/cocorion/cocorion.bbmodel", encoding="utf-8"))
def filtra(no, dentro):
    if isinstance(no, str): return no if dentro else None
    d = dentro or no["name"] in nomes
    filhos = [f for f in (filtra(c, d) for c in no["children"]) if f is not None]
    if not filhos and not d: return None
    n = dict(no); n["children"] = filhos; return n
m["outliner"] = [f for f in (filtra(n, False) for n in m["outliner"]) if f is not None]
json.dump(m, open("modelos/cocorion/revisao/c/_parte.bbmodel", "w", encoding="utf-8"))
previa2.desenhar(previa2.carregar("modelos/cocorion/revisao/c/_parte.bbmodel"), yaw, pitch, escala=14).save(saida)
