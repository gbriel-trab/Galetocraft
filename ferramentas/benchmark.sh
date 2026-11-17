#!/usr/bin/env bash
# Roda o benchmark do Pirococó (0/10/30/60/100 galos) num "PC" simulado.
# Uso: bash ferramentas/benchmark.sh <rotulo> [nucleos] [velocidade%]
#   bash ferramentas/benchmark.sh maquina            -> esta máquina sem limite
#   bash ferramentas/benchmark.sh mediano 4 50       -> 4 núcleos a 50% (CPU mediana)
#   bash ferramentas/benchmark.sh fraco 4 33         -> 4 núcleos a 33% (CPU fraca)
#   CENA=longe bash ferramentas/benchmark.sh ...      -> galos a 40-62 blocos da câmera (testa o LOD)
# Resultados: benchmark/benchmark_<rotulo>.csv (jogo) e benchmark/benchmark_<rotulo>_gpu.csv (GPU/CPU)
# Capturas: galetocraft/build/run/clientGameTest/screenshots (apagadas a cada rodada)
set -e
ROTULO="${1:?rotulo}"; NUCLEOS="${2:-0}"; VELOCIDADE="${3:-100}"
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
RUN="$RAIZ/benchmark"
mkdir -p "$RUN"
RUN_W="$(cygpath -w "$RUN")"
powershell -NoProfile -ExecutionPolicy Bypass -File "$RAIZ/ferramentas/sandbox_pc.ps1" \
    -Saida "$RUN_W\benchmark_${ROTULO}_gpu.csv" -Nucleos "$NUCLEOS" -Velocidade "$VELOCIDADE" -EsperaMaxSeg 240 &
MEDIDOR=$!
cd "$RAIZ/galetocraft"
export JAVA_HOME="C:/Program Files/Eclipse Adoptium/jdk-25.0.5.8-hotspot"
OPCOES="-Dfabric.client.gametest.disableNetworkSynchronizer=true"
# PC simulado: o Java (e o Minecraft) já nascem achando que só existem N processadores, como num PC de N núcleos
if [ "$NUCLEOS" -gt 0 ]; then OPCOES="$OPCOES -XX:ActiveProcessorCount=$NUCLEOS"; fi
JAVA_TOOL_OPTIONS="$OPCOES" GALETO_BENCH=1 GALETO_BENCH_CENA="${CENA:-perto}" GALETO_BENCH_ROTULO="$ROTULO" GALETO_BENCH_SAIDA="$RUN_W" ./gradlew runClientGameTest --no-daemon -q 2>&1 | grep -E "FAIL|Exception|error:" || true
wait $MEDIDOR || true
mkdir -p "$RUN/capturas_$ROTULO" && cp "$RAIZ"/galetocraft/build/run/clientGameTest/screenshots/*bench_*.png "$RUN/capturas_$ROTULO/" 2>/dev/null || true
cat "$RUN/benchmark_${ROTULO}.csv"
