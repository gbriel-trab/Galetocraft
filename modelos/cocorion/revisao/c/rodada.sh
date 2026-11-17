#!/bin/sh
# uso: sh rodada.sh cK
cd /c/Users/gbriel/Desktop/galopiru
python ferramentas/rodada_revisao.py cocorion $1 && \
python ferramentas/comparar_ficha.py cocorion $1 && \
python modelos/cocorion/revisao/arte_lado_s.py $1 && \
python ferramentas/dimensoes.py cocorion
