package br.galetocraft.teste;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

import br.galetocraft.registro.ModEntidades;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.sounds.SoundSource;

/**
 * Galeria de todas as espécies no jogo: para cada uma, três exemplares parados (frente, lado e costas) diante da
 * câmera, um print de dia e um à noite (partes que brilham); no fim, todas juntas lado a lado.
 * <p>
 * O enquadramento segue a altura de cada espécie (tabela oficial em ferramentas/dimensoes.py): os comuns têm ~1 bloco
 * e ficam num degrau, para a câmera não olhar de cima; os míticos vão de 1,75 a 3 blocos.
 * <p>
 * GALETO_GALERIA=esporoco,cocorak limita a algumas espécies (padrão: todas). Não roda no modo benchmark.
 */
@SuppressWarnings("UnstableApiUsage")
public class GaleriaTesteCliente implements FabricClientGameTest {
	@Override
	public void runTest(ClientGameTestContext contexto) {
		if (System.getenv("GALETO_BENCH") != null)
			return;

		final List<String> especies = new ArrayList<>();
		final Map<String, Double> altura = new HashMap<>();
		final String filtro = System.getenv("GALETO_GALERIA");

		ModEntidades.GALOS.forEach(tipo -> {
			especies.add(ModEntidades.id(tipo));
			altura.put(ModEntidades.id(tipo), (double) tipo.getHeight());
		});
		if (filtro != null && !filtro.isBlank())
			especies.removeIf(id -> !List.of(filtro.toLowerCase(Locale.ROOT).split(",")).contains(id));
		if (especies.isEmpty())
			return;   // nenhuma espécie registrada (ou nenhuma no filtro): nada a fotografar

		contexto.getInput().resizeWindow(1920, 1080);
		contexto.runOnClient(mc -> mc.options.getSoundSourceOptionInstance(SoundSource.MASTER).set(0.0));   // sem som
		contexto.runOnClient(mc -> mc.options.hideGui = true);   // prints sem a interface

		try (TestSingleplayerContext mundo = contexto.worldBuilder().create()) {
			mundo.getClientWorld().waitForChunksRender();
			final TestServerContext servidor = mundo.getServer();
			servidor.runCommand("weather clear");

			for (String id : especies) {
				final double h = altura.getOrDefault(id, 2.0);
				// vão entre os exemplares e distância da câmera pelo tamanho; o Cocórak (3 blocos, largo) e a
				// Salambrasa (comprida) têm valores próprios
				final double vao = id.equals("cocorak") ? 5.5 : id.equals("salambrasa") ? 2.5
						: Math.max(1.8, Math.min(5.0, 1.3 * h + 0.6));
				final double camera = id.equals("cocorak") ? -3.5 : id.equals("salambrasa") ? 0.6 : 4 - (0.45 * (2 * vao + 1.4 * h) + 0.8);
				final boolean degrau = h < 1.5;
				final double y = degrau ? -59 : -60;

				// manda os galos da cena anterior para o fundo do mundo (matar deixaria a fumaça de morte no print)
				servidor.runCommand("tp @e[type=!player] 0 -400 0");
				servidor.runCommand("fill -12 -60 1 12 -60 12 air");
				servidor.runCommand("fill -12 -61 1 12 -61 12 grass_block replace dirt");   // a grama coberta pelo degrau vira terra
				if (degrau)
					servidor.runCommand("fill -12 -60 1 12 -60 12 grass_block");
				servidor.runCommand("time set noon");
				servidor.runCommand(String.format(Locale.ROOT, "tp @p 0 -60 %.1f 0 %d", camera, degrau ? 4 : 8));
				servidor.runCommand(String.format(Locale.ROOT, "summon galetocraft:%s 0 %.0f 3.5 {Rotation:[180f,0f],NoAI:1b}", id, y));
				servidor.runCommand(String.format(Locale.ROOT, "summon galetocraft:%s %.1f %.0f 4 {Rotation:[90f,0f],NoAI:1b}", id, -vao, y));
				servidor.runCommand(String.format(Locale.ROOT, "summon galetocraft:%s %.1f %.0f 4 {Rotation:[0f,0f],NoAI:1b}", id, vao, y));

				contexto.waitTicks(30);
				mundo.getClientWorld().waitForChunksRender();
				contexto.takeScreenshot("galeria_" + id + "_dia");

				servidor.runCommand("time set midnight");
				contexto.waitTicks(10);
				contexto.takeScreenshot("galeria_" + id + "_noite");
			}

			// todas juntas, em fila, viradas um pouco para a câmera; cada uma ocupa um espaço proporcional à altura
			servidor.runCommand("tp @e[type=!player] 0 -400 0");
			servidor.runCommand("fill -12 -60 1 12 -60 12 air");
			servidor.runCommand("fill -12 -61 1 12 -61 12 grass_block replace dirt");   // a grama coberta pelo degrau vira terra
			servidor.runCommand("time set noon");
			final List<String> todas = new ArrayList<>(especies);
			final double[] larg = todas.stream().mapToDouble(id -> 0.75 * altura.getOrDefault(id, 2.0) + 0.5).toArray();
			double x = -Arrays.stream(larg).sum() / 2;

			for (int i = 0; i < todas.size(); i++) {
				x += larg[i] / 2;
				servidor.runCommand(String.format(Locale.ROOT, "summon galetocraft:%s %.2f -60 8 {Rotation:[200f,0f],NoAI:1b}", todas.get(i), x));
				x += larg[i] / 2;
			}

			servidor.runCommand("tp @p 0 -58.5 -5 0 6");
			contexto.waitTicks(30);
			mundo.getClientWorld().waitForChunksRender();
			contexto.takeScreenshot("galeria_todos");
		}
	}
}
