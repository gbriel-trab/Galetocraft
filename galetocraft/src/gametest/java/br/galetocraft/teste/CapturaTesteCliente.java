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
 * <li>ao entrar no mundo o treinador recebe a Pena de Captura nível 1 (kit de início de jornada);</li>
 * <li>sem alvo na mira, o botão direito só avisa;</li>
 * <li>no mundo: mira num Taturico e usa o botão direito de verdade (tecla "usar"), até capturar. Depois de cada
 * falha, confere a espera de 20 s antes de tentar de novo;</li>
 * <li>confere o Taturico na equipe principal e os 115 XP da Pena (Comum nível 50);</li>
 * <li>na Rinha: desafia um Vagaló com o Taturico e usa Itens → Pena de Captura até capturar;</li>
 * <li>confere a equipe com os dois e a troca de ordem pelo botão "primeiro";</li>
 * <li>vence uma Rinha contra um Taturico selvagem de nível 20 (curva 1–49) usando sempre o golpe mais forte e confere
 * a XP: floor((25 + 15·20) × 0,25) = 81 no total (fator de desafio no mínimo, P = 50), repartida entre quem entrou em
 * campo, somada à XP inicial T(50) = 141.659;</li>
 * <li>troca um golpe equipado pelo botão de {@code /galetocraft golpes} e confere que ele aparece no menu da Rinha.</li>
 * </ol>
 * Grava o chat em {@code captura_teste.log}. Para rodar só ele: GALETO_TESTES=captura.
 */
@SuppressWarnings("UnstableApiUsage")
public class CapturaTesteCliente implements FabricClientGameTest {
	private static final int MAX_TENTATIVAS = 12;
	private static final long T50 = 141_659;   // (50−1)³ + 10·(50−1)²

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
			chat.exigir(chat.contem("Início da jornada: você recebeu a Pena de Captura!"), "a Pena não veio no kit de início");
			chat.exigir(chat.contem("Escolha seu Galeto inicial"), "a escolha do inicial não foi oferecida");
			chat.comando("galetocraft pena");
			chat.exigir(chat.contem("Pena de Captura nível 1 · 0 XP"), "a Pena deveria começar no nível 1");
			chat.exigir(contexto.computeOnClient(mc -> mc.player.getMainHandItem().is(ModItens.PENA_DE_CAPTURA)),
					"a Pena não está na mão");

			// 2) sem alvo na mira
			servidor.runCommand("tp @p 0 -60 -3 180 -30");
			contexto.waitTicks(5);
			usar(contexto);
			chat.exigir(chat.contem("Mire num Cocorídeo selvagem a até 12 blocos"), "faltou o aviso sem alvo");

			// 3) captura no mundo, mirando e usando o botão direito
			servidor.runCommand("summon galetocraft:taturico 0 -60 3 {NoAI:1b,galeto_nivel:50,galeto_sexo:\"M\",galeto_ivs:[I;20,20,20,20,20,20]}");
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
				servidor.runCommand("summon galetocraft:vagalo 0 -60 2 {Rotation:[180f,0f],galeto_nivel:50,galeto_sexo:\"M\",galeto_ivs:[I;20,20,20,20,20,20]}");
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

			// 6) XP por Rinha vencida
			chat.exigir(t3.equipe().stream().allMatch(g -> g.xp() == T50), "a XP inicial do capturado deveria ser T(50)");
			java.util.Random rng = new java.util.Random(7);
			int vitorias = chat.contar("Você venceu a Rinha!"), rinhasXp = 0;
			while (chat.contar("Você venceu a Rinha!") == vitorias && rinhasXp < 6) {
				servidor.runCommand("summon galetocraft:taturico 0 -60 2 {Rotation:[180f,0f],galeto_nivel:20,galeto_sexo:\"M\",galeto_ivs:[I;20,20,20,20,20,20]}");
				contexto.waitTicks(10);
				int derrotas = chat.contar("Você perdeu a Rinha.");
				chat.comando("galetocraft desafiar");
				rinhasXp++;
				int passos = 0;
				while (chat.contar("Você venceu a Rinha!") == vitorias && chat.contar("Você perdeu a Rinha.") == derrotas && passos < 80) {
					chat.comando(chat.golpeMaisForte());
					passos++;
				}
			}
			chat.exigir(chat.contar("Você venceu a Rinha!") > vitorias, "não venceu a Rinha da XP em " + rinhasXp + " tentativas");
			Treinador t4 = servidor.computeOnServer(CapturaTesteCliente::treinador);
			long ganho = t4.equipe().stream().mapToLong(g -> g.xp() - T50).sum();
			chat.exigir(chat.contem("Selvagem (Taturico)") && chat.contem("Taturico Nv20"), "o selvagem de nível 20 não apareceu na Rinha");
			chat.exigir(ganho == 81, "XP total da vitória deveria ser 81, foi " + ganho + ": " + t4);
			chat.exigir(chat.contem("ganhou") && chat.contem(" XP."), "faltou a mensagem de XP");
			contexto.takeScreenshot("xp_vitoria");

			// 7) slots de golpes: troca pelo botão e uso na Rinha seguinte
			chat.comando("galetocraft golpes 0");
			chat.exigir(chat.contem("Golpes de Vagaló Nv50 — slots livres"), "a tela de golpes não apareceu");
			java.util.List<String> trocas = chat.botoes("/galetocraft golpes 0 trocar ");
			chat.exigir(!trocas.isEmpty(), "sem botões de troca de golpe");
			chat.comando(trocas.get(0));
			String texto = chat.texto();
			java.util.regex.Matcher m = java.util.regex.Pattern.compile("\\n([^\\n]+) equipado no slot (\\d)\\.").matcher(texto);
			chat.exigir(m.find(), "a troca de golpe não foi confirmada");
			String novoGolpe = m.group(1);
			Treinador t5 = servidor.computeOnServer(CapturaTesteCliente::treinador);
			chat.exigir(t5.equipe().get(0).equipados().contains(novoGolpe), "o golpe não ficou salvo: " + t5.equipe().get(0).equipados());
			contexto.takeScreenshot("golpes_troca");
			servidor.runCommand("summon galetocraft:taturico 0 -60 2 {Rotation:[180f,0f]}");
			contexto.waitTicks(10);
			chat.comando("galetocraft desafiar");
			chat.exigir(chat.botoes("/galetocraft acao golpe ").size() > 0 && chat.contem("[" + novoGolpe), "o golpe novo não aparece no menu da Rinha");
			chat.comando("galetocraft acao fugir");
			chat.gravar("ok: mundo em " + tentativasMundo + " tentativa(s); Rinha em " + acoes + " ação(ões) e " + rinhas
					+ " Rinha(s); XP 81 em " + rinhasXp + " Rinha(s); golpe trocado: " + novoGolpe);
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
