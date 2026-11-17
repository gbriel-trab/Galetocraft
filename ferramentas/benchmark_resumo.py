"""Junta o CSV do jogo (fases por número de galos) com a medição de GPU/CPU feita por fora (sandbox_pc.ps1)."""
import csv, sys
from pathlib import Path
pasta = Path(__file__).resolve().parent.parent / "benchmark"
for rotulo in sys.argv[1:]:
    jogo = list(csv.DictReader(open(pasta / f"benchmark_{rotulo}.csv")))
    med = [r for r in csv.DictReader(open(pasta / f"benchmark_{rotulo}_gpu.csv"))]
    print(f"== {rotulo}")
    print(f"{'galos':>5} {'FPS':>7} {'FPSmin':>7} {'ms/quadro':>9} {'MSPT':>6} {'TPS':>5} {'GPU3D%':>7} {'CPU%maq':>8} {'GPUms/q':>8}")
    for f in jogo:
        a, b = int(f["inicio_ms"]), int(f["fim_ms"])
        janela = [r for r in med if a <= int(r["tempo_ms"]) <= b]
        g = sum(float(r["gpu3d_jogo"]) for r in janela) / max(len(janela), 1)
        c = sum(float(r["cpu_jogo_maquina"]) for r in janela) / max(len(janela), 1)
        fps = float(f["fps_medio"]); ms = 1000 / fps if fps else float("nan")
        print(f"{f['galos']:>5} {fps:7.1f} {f['fps_min']:>7} {ms:9.2f} {float(f['mspt_servidor']):6.2f} {float(f['ticks_por_segundo']):5.1f} {g:7.1f} {c:8.1f} {ms * g / 100:8.2f}")
