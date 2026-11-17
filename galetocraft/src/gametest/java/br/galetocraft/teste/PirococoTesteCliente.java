package br.galetocraft.teste;

import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.sounds.SoundSource;

/**
 * Cena de teste do Pirococó: mundo plano, três Pirococós parados (frente, lado e costas)
 * diante da câmera, um print de dia e um à noite (para ver as partes que brilham).
 */
@SuppressWarnings("UnstableApiUsage")
public class PirococoTesteCliente implements FabricClientGameTest {
	@Override
	public void runTest(ClientGameTestContext contexto) {
		if (System.getenv("GALETO_BENCH") != null)
			return;   // no modo benchmark só roda o PirococoBenchmark
		contexto.runOnClient(mc -> mc.options.getSoundSourceOptionInstance(SoundSource.MASTER).set(0.0));   // sem som

		try (TestSingleplayerContext mundo = contexto.worldBuilder().create()) {
			mundo.getClientWorld().waitForChunksRender();

			var servidor = mundo.getServer();
			servidor.runCommand("time set noon");
			servidor.runCommand("weather clear");
			// câmera olhando para +Z, um pouco de cima
			servidor.runCommand("tp @p 0 -60 -3 0 8");
			// frente (olhando para a câmera), lado e costas; NoAI para ficarem parados
			servidor.runCommand("summon galetocraft:pirococo 0 -60 3 {Rotation:[180f,0f],NoAI:1b}");
			servidor.runCommand("summon galetocraft:pirococo -3.5 -60 3.5 {Rotation:[90f,0f],NoAI:1b}");
			servidor.runCommand("summon galetocraft:pirococo 3.5 -60 3.5 {Rotation:[0f,0f],NoAI:1b}");

			contexto.waitTicks(40);
			mundo.getClientWorld().waitForChunksRender();
			contexto.takeScreenshot("pirococo_dia");

			contexto.waitTicks(15);
			contexto.takeScreenshot("pirococo_dia_animacao");

			servidor.runCommand("time set midnight");
			contexto.waitTicks(20);
			contexto.takeScreenshot("pirococo_noite");
		}
	}
}
