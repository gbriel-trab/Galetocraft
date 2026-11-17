"""Congela uma rodada de revisão de uma espécie: roda o gerador, grava as imagens com o prefixo da rodada e guarda
cópias do código e do modelo (para voltar a ela se a rodada seguinte ficar pior).

Uso: python rodada_revisao.py <id> <prefixo>        (ex.: python rodada_revisao.py cocorak r1)
     python rodada_revisao.py <id> <prefixo> --voltar  (restaura o código daquela rodada e regera o modelo)"""
import shutil, subprocess, sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent

def main(id_, prefixo, voltar=False):
    pasta = RAIZ / "modelos" / id_ / "revisao"; pasta.mkdir(parents=True, exist_ok=True)
    codigo = AQUI / "especies" / f"{id_}.py"
    if voltar:
        shutil.copyfile(pasta / f"{prefixo}.py", codigo)
    subprocess.run([sys.executable, str(codigo), str(pasta), prefixo], check=True)
    shutil.copyfile(codigo, pasta / f"{prefixo}.py")
    shutil.copyfile(RAIZ / "modelos" / id_ / f"{id_}.bbmodel", pasta / f"{prefixo}.bbmodel")

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], "--voltar" in sys.argv[3:])
