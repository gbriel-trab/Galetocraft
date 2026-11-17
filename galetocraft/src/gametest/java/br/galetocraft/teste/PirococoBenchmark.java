package br.galetocraft.teste;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.client.InactivityFpsLimit;
import net.minecraft.client.Minecraft;
import net.minecraft.sounds.SoundSource;

/**
 * Benchmark do Pirococó (só roda com a variável de ambiente GALETO_BENCH=1).
 * <p>
 * Janela 1920x1080, sem vsync e sem limite de FPS, distância de renderização 8. Num cercado de barreiras na frente
 * da câmera, invoca 0, 10, 30, 60 e 100 Pirococós COM IA (andando, olhando, animando) e mede durante 10 segundos:
 * FPS do cliente (média e pior amostra), tempo médio de tick do servidor (MSPT) e quantos ticks por segundo saíram.
 * Resultado em [GALETO_BENCH_SAIDA]/benchmark_[GALETO_BENCH_ROTULO].csv, com a hora de cada fase (para cruzar com
 * a medição de GPU feita por fora).
 */
@SuppressWarnings("UnstableApiUsage")
public class PirococoBenchmark implements FabricClientGameTest {
	private static final int[] QUANTIDADES = {0, 10, 30, 60, 100};
	private static final int TICKS_ACOMODAR = 80;
	private static final int TICKS_MEDIR = 200;

	@Override
	public void runTest(ClientGameTestContext contexto) {
		if (System.getenv("GALETO_BENCH") == null)
			return;

		final String rotulo = System.getenv().getOrDefault("GALETO_BENCH_ROTULO", "padrao");
		// cena "perto" (cercado a 10-34 blocos da câmera) ou "longe" (40-62 blocos: onde o LOD esconde os detalhes)
		final boolean longe = "longe".equals(System.getenv("GALETO_BENCH_CENA"));
		final int z0 = longe ? 38 : 1;
		final List<String> linhas = new ArrayList<>();
		linhas.add("rotulo,galos,fps_medio,fps_min,mspt_servidor,ticks_por_segundo,inicio_ms,fim_ms");

		contexto.getInput().resizeWindow(1920, 1080);
		contexto.runOnClient(mc -> mc.options.getSoundSourceOptionInstance(SoundSource.MASTER).set(0.0));   // sem som
		contexto.runOnClient(mc -> {
			mc.options.enableVsync().set(false);
			mc.options.framerateLimit().set(260);        // 260 = ilimitado
			// sem isto o jogo se limita a 30 FPS sozinho quando ninguém mexe no mouse/teclado (modo "AFK")
			mc.options.inactivityFpsLimit().set(InactivityFpsLimit.MINIMIZED);
		});

		try (TestSingleplayerContext mundo = contexto.worldBuilder().create()) {
			mundo.getClientWorld().waitForChunksRender();
			// distância 8: o típico de quem joga num PC mediano/fraco
			contexto.runOnClient(mc -> {
				mc.options.renderDistance().set(8);
				mc.options.simulationDistance().set(8);
			});
			contexto.waitTicks(60);
			final TestServerContext servidor = mundo.getServer();
			servidor.runCommand("time set noon");
			servidor.runCommand("weather clear");
			servidor.runCommand("gamerule doDaylightCycle false");
			servidor.runCommand("gamemode spectator @p");
			// cercado invisível (barreira) de 26 x 23 blocos na frente da câmera, para os galos andarem sem sair de vista
			servidor.runCommand("fill -13 -60 " + z0 + " 13 -56 " + z0 + " barrier");
			servidor.runCommand("fill -13 -60 " + (z0 + 23) + " 13 -56 " + (z0 + 23) + " barrier");
			servidor.runCommand("fill -13 -60 " + z0 + " -13 -56 " + (z0 + 23) + " barrier");
			servidor.runCommand("fill 13 -60 " + z0 + " 13 -56 " + (z0 + 23) + " barrier");
			servidor.runCommand(longe ? "tp @p 0 -52 -9 0 9" : "tp @p 0 -52 -9 0 28");

			for (int n : QUANTIDADES) {
				servidor.runCommand("kill @e[type=galetocraft:pirococo]");
				for (int i = 0; i < n; i++) {
					int x = -11 + (i % 10) * 2 + (i / 10 % 2);
					int z = z0 + 2 + (i / 10) * 2;
					servidor.runCommand("summon galetocraft:pirococo " + x + " -60 " + z);
				}
				contexto.waitTicks(TICKS_ACOMODAR);

				final long inicio = System.currentTimeMillis();
				double somaFps = 0;
				int piorFps = Integer.MAX_VALUE;
				int amostras = 0;
				for (int t = 0; t < TICKS_MEDIR; t += 20) {
					contexto.waitTicks(20);
					int fps = contexto.computeOnClient(Minecraft::getFps);
					somaFps += fps;
					piorFps = Math.min(piorFps, fps);
					amostras++;
				}
				final long fim = System.currentTimeMillis();
				double mspt = servidor.computeOnServer(s -> s.getAverageTickTimeNanos() / 1_000_000.0);
				double tps = TICKS_MEDIR / ((fim - inicio) / 1000.0);

				linhas.add(String.format(Locale.ROOT, "%s,%d,%.1f,%d,%.2f,%.1f,%d,%d",
						rotulo, n, somaFps / amostras, piorFps, mspt, tps, inicio, fim));
				contexto.takeScreenshot("bench_" + rotulo + "_" + n);
			}
		}

		try {
			Path pasta = Path.of(System.getenv().getOrDefault("GALETO_BENCH_SAIDA", "."));
			Files.createDirectories(pasta);
			Path arquivo = pasta.resolve("benchmark_" + rotulo + ".csv");
			Files.write(arquivo, linhas);
		} catch (IOException e) {
			throw new RuntimeException("não consegui salvar o resultado do benchmark", e);
		}
	}
}
