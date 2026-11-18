package br.galetocraft.teste;

import br.galetocraft.registro.ModAnexos;
import br.galetocraft.registro.ModItens;
import br.galetocraft.treinador.Treinador;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;

/**
 * Captura de ponta a ponta no cliente:
 * <ol>
 * <li>{@code /galetocraft pena} entrega a Pena de Captura (nível 1);</li>
 * <li>sem alvo na mira, o botão direito só avisa;</li>
 * <li>no mundo: mira num Taturico e usa o botão direito de verdade (tecla "usar"), até capturar. Depois de cada
 * falha, confere a espera de 20 s antes de tentar de novo;</li>
 * <li>confere o Taturico na equipe principal e os 115 XP da Pena (Comum nível 50);</li>
 * <li>na Rinha: desafia um Vagaló com o Taturico e usa Itens → Pena de Captura até capturar;</li>
 * <li>confere a equipe com os dois e a troca de ordem pelo botão "primeiro".</li>
 * </ol>
 * Grava o chat em {@code captura_teste.log}. Para rodar só ele: GALETO_TESTES=captura.
 */
@SuppressWarnings("UnstableApiUsage")
public class CapturaTesteCliente implements FabricClientGameTest {
	private static final int MAX_TENTATIVAS = 12;

	@Override
	public void runTest(ClientGameTestContext contexto) {
		if (System.getenv("GALETO_BENCH") != null || Testes.pular("captura"))
			return;
		ChatTeste chat = new ChatTeste(contexto, "captura_teste.log");
		Testes.prepararCliente(contexto);

		try (TestSingleplayerContext mundo = contexto.worldBuilder().create()) {
			contexto.waitTicks(40);
			final TestServerContext servidor = mundo.getServer();
			servidor.runCommand("time set noon");
			servidor.runCommand("weather clear");
			servidor.runCommand("tp @p 0 -60 -3 0 0");

			// 1) a Pena de Captura
			chat.comando("galetocraft pena");
			chat.exigir(chat.contem("Você recebeu a Pena de Captura"), "a Pena não foi entregue");
			chat.exigir(chat.contem("Pena de Captura nível 1 · 0 XP"), "a Pena deveria começar no nível 1");
			chat.exigir(contexto.computeOnClient(mc -> mc.player.getMainHandItem().is(ModItens.PENA_DE_CAPTURA)),
					"a Pena não está na mão");

			// 2) sem alvo na mira
			servidor.runCommand("tp @p 0 -60 -3 180 -30");
			contexto.waitTicks(5);
			usar(contexto);
			chat.exigir(chat.contem("Mire num Cocorídeo selvagem a até 12 blocos"), "faltou o aviso sem alvo");

			// 3) captura no mundo, mirando e usando o botão direito
			servidor.runCommand("summon galetocraft:taturico 0 -60 3 {NoAI:1b}");
			contexto.waitTicks(10);
			int tentativas = 0;
			while (!chat.contem("Taturico foi capturado") && tentativas < MAX_TENTATIVAS) {
				// olhos em y −58,38 e centro do Taturico a 6 blocos, ~1 bloco abaixo: inclinação de ~10° para baixo
				// ("tp ... facing" mira a partir dos pés e passaria por cima)
				servidor.runCommand("tp @p 0 -60 -3 0 10");
				contexto.waitTicks(5);
				int falhasAntes = chat.contar("A captura de Taturico falhou.");
				usar(contexto);
				tentativas++;
				if (chat.contar("A captura de Taturico falhou.") > falhasAntes) {
					// a espera vale logo depois da falha
					usar(contexto);
					chat.exigir(chat.contem("Taturico ainda resiste à captura por"), "a espera de 20 s não foi aplicada");
					contexto.waitTicks(20 * 20 + 5);
				}
			}
			chat.exigir(chat.contem("Taturico foi capturado e foi para a equipe principal."), "a captura no mundo não aconteceu");
			chat.exigir(chat.contem("A Pena de Captura ganhou 115 XP."), "XP da Pena diferente de 15 + 2×50");
			contexto.takeScreenshot("captura_mundo");
			chat.exigir(servidor.computeOnServer(s -> RinhaTesteCliente.selvagens(s).isEmpty()), "o Taturico capturado continuou no mundo");
			Treinador t1 = servidor.computeOnServer(CapturaTesteCliente::treinador);
			chat.exigir(t1.equipe().size() == 1 && t1.equipe().get(0).especie() == 7 && t1.penaXp() == 115,
					"equipe ou XP errados depois da captura no mundo: " + t1);
			int tentativasMundo = tentativas;

			// 4) captura na Rinha: o Taturico capturado luta e a Pena é usada pelo botão Itens
			servidor.runCommand("tp @p 0 -60 -3 0 0");
			int rinhas = 0, acoes = 0;
			while (!chat.contem("Vagaló foi capturado") && rinhas < 5) {
				servidor.runCommand("summon galetocraft:vagalo 0 -60 2 {Rotation:[180f,0f]}");
				contexto.waitTicks(10);
				chat.comando("galetocraft desafiar");
				rinhas++;
				chat.exigir(chat.contem("Rinha: Player0 (Taturico) × Selvagem (Vagaló)"), "a Rinha não usou a equipe do treinador");
				while (!chat.contem("Vagaló foi capturado") && !chat.contem("Você perdeu a Rinha.") && acoes < 60) {
					chat.comando(chat.botao("/galetocraft acao itens"));
					chat.comando(chat.botao("/galetocraft acao capturar"));
					acoes++;
					if (acoes == 1)
						contexto.takeScreenshot("captura_rinha");
				}
			}
			chat.exigir(chat.contem("Player0 usa a Pena de Captura em Vagaló: capturado!"), "a captura na Rinha não aconteceu");
			chat.exigir(chat.contem("Vagaló foi capturado e foi para a equipe principal."), "o Vagaló não foi para a equipe");
			Treinador t2 = servidor.computeOnServer(CapturaTesteCliente::treinador);
			chat.exigir(t2.equipe().size() == 2 && t2.equipe().get(1).especie() == 9 && t2.penaXp() == 230,
					"equipe ou XP errados depois da captura na Rinha: " + t2);

			// 5) equipe do treinador: lista e ordem
			chat.comando("galetocraft equipe");
			chat.exigir(chat.contem("Equipe principal (2/5"), "a lista da equipe não apareceu");
			chat.comando(chat.botao("/galetocraft equipe primeiro 1"));
			Treinador t3 = servidor.computeOnServer(CapturaTesteCliente::treinador);
			chat.exigir(t3.equipe().get(0).especie() == 9, "o botão primeiro não mudou a ordem");
			contexto.takeScreenshot("captura_equipe");
			chat.gravar("ok: mundo em " + tentativasMundo + " tentativa(s); Rinha em " + acoes + " ação(ões) e " + rinhas + " Rinha(s)");
		}
	}

	/** Botão direito ("usar") com a Pena na mão. */
	private static void usar(ClientGameTestContext contexto) {
		contexto.getInput().pressKey(o -> o.keyUse);
		contexto.waitTicks(5);
	}

	private static Treinador treinador(MinecraftServer s) {
		ServerPlayer p = s.getPlayerList().getPlayers().get(0);
		return ModAnexos.treinador(p);
	}
}
