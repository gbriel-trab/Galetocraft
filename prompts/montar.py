"""Monta o prompt pronto para colar no outro chat: mestre.md + criaturas/<id>.md + o renderizador.

Uso: python prompts/montar.py <id> "<Nome com acento>" [versao]
Grava prompts/prontos/<id>_v<versao>.md (versão 1 por padrão).
"""
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent


def montar(id_, nome, versao="1"):
    mestre = (AQUI / "mestre.md").read_text(encoding="utf-8")
    criatura = (AQUI / "criaturas" / f"{id_}.md").read_text(encoding="utf-8").strip()
    render = (RAIZ / "ferramentas" / "render_geo.py").read_text(encoding="utf-8").strip()
    texto = (mestre.replace("{{CRIATURA}}", criatura)
                   .replace("{{RENDER_GEO}}", render)
                   .replace("{{ID}}", id_)
                   .replace("{{NOME}}", nome))
    assert "{{" not in texto.replace("{{ID}}", ""), "sobrou marcador sem substituir"
    destino = AQUI / "prontos" / f"{id_}_v{versao}.md"
    destino.parent.mkdir(exist_ok=True)
    destino.write_text(texto, encoding="utf-8")
    print(f"gravado {destino.relative_to(RAIZ)} ({len(texto.split())} palavras, {len(texto)} caracteres)")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    montar(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "1")
