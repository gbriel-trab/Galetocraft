package br.galetocraft.teste;

import br.galetocraft.client.tempestade.TempestadeCliente;
import br.galetocraft.mundo.TempestadeDeAreia;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.core.BlockPos;

/**
 * Tempestade de areia (regra tempestade_de_areia, rev. 10):
 * <ol>
 * <li>sem chuva, no deserto: nada;</li>
 * <li>com chuva, no deserto e ao ar livre: a tempestade sobe no cliente (poeira, névoa e vento) e o servidor a detecta;</li>
 * <li>uma Rinha que começa dentro dela já começa com o clima Tempestade de Areia;</li>
 * <li>fora do deserto, com a mesma chuva, a tempestade some.</li>
 * </ol>
 * Tira prints antes e durante a tempestade. Para rodar só ele: GALETO_TESTES=tempestade.
 */
@SuppressWarnings("UnstableApiUsage")
public class TempestadeTesteCliente implements FabricClientGameTest {
	@Override
	public void runTest(ClientGameTestContext contexto) {
		if (System.getenv("GALETO_BENCH") != null || Testes.pular("tempestade"))
			return;
		ChatTeste chat = new ChatTeste(contexto, "tempestade_teste.log");
		Testes.prepararCliente(contexto);

		try (TestSingleplayerContext mundo = contexto.worldBuilder().create()) {
			contexto.waitTicks(40);
			final TestServerContext servidor = mundo.getServer();
			servidor.runCommand("gamerule advance_weather false");
			servidor.runCommand("time set noon");
			servidor.runCommand("weather clear");
			servidor.runCommand("fillbiome -16 -64 -16 16 -48 16 minecraft:desert");   // dentro do limite de blocos do comando
			servidor.runCommand("fill -16 -61 -16 16 -61 16 minecraft:sand");
			servidor.runCommand("tp @p 0 -60 0 0 0");
			contexto.waitTicks(60);

			// 1) deserto sem chuva
			chat.exigir(TempestadeCliente.intensidade() == 0f, "tempestade sem chuva: " + TempestadeCliente.intensidade());
			chat.exigir(!servidor.computeOnServer(s -> TempestadeDeAreia.ativaEm(s.overworld(), new BlockPos(0, -60, 0))), "servidor viu tempestade sem chuva");
			contexto.runOnClient(mc -> mc.options.hideGui = true);
			contexto.takeScreenshot("tempestade_antes");

			// 2) chuva no deserto
			servidor.runCommand("weather rain");
			contexto.waitTicks(200);
			float k = contexto.computeOnClient(mc -> TempestadeCliente.intensidade());
			chat.exigir(k > 0.6f, "a tempestade não subiu no cliente: " + k);
			chat.exigir(servidor.computeOnServer(s -> TempestadeDeAreia.ativaEm(s.overworld(), new BlockPos(0, -60, 0))), "o servidor não detectou a tempestade");
			contexto.takeScreenshot("tempestade_durante");
			contexto.runOnClient(mc -> mc.options.hideGui = false);

			// 3) Rinha dentro da tempestade
			servidor.runCommand("summon galetocraft:taturico 0 -60 4 {Rotation:[180f,0f],galeto_nivel:30,galeto_sexo:\"M\",galeto_ivs:[I;20,20,20,20,20,20]}");
			contexto.waitTicks(5);
			chat.comando("galetocraft desafiar");
			chat.exigir(chat.contem("Clima: Tempestade de Areia (4 rodadas)"), "a Rinha não começou com o clima Tempestade de Areia");
			contexto.takeScreenshot("tempestade_rinha");
			chat.comando("galetocraft acao fugir");

			// 4) fora do deserto, com a mesma chuva
			servidor.runCommand("tp @p 400 -60 400");
			contexto.waitTicks(200);
			float fora = contexto.computeOnClient(mc -> TempestadeCliente.intensidade());
			chat.exigir(fora < 0.05f, "a tempestade continuou fora do deserto: " + fora);
			chat.gravar("ok: intensidade no deserto " + k + ", fora " + fora);
		}
	}
}
