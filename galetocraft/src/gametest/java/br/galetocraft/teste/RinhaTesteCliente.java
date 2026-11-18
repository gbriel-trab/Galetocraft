package br.galetocraft.teste;

import br.galetocraft.entidade.GaloEntity;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.server.MinecraftServer;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.phys.AABB;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * Rinha jogada de ponta a ponta no cliente, como um jogador faria:
 * <ol>
 * <li>define a equipe de teste com {@code /galetocraft equipe teste} (o jogador ainda não tem Galetos);</li>
 * <li>desafia um Taturico selvagem com {@code /galetocraft desafiar};</li>
 * <li>joga clicando nos botões do menu do chat (usa os comandos dos próprios botões), trocando mira, guarda e Pena
 * de Ritmo;</li>
 * <li>confere que a Rinha termina com vitória ou derrota e que o Galeto selvagem volta a ter IA.</li>
 * </ol>
 * Grava o chat em {@code rinha_teste.log} e tira prints do menu. Não roda no modo benchmark.
 * Para rodar só ele: GALETO_TESTES=rinha.
 */
@SuppressWarnings("UnstableApiUsage")
public class RinhaTesteCliente implements FabricClientGameTest {
	private static final int MAX_ACOES = 60;

	@Override
	public void runTest(ClientGameTestContext contexto) {
		if (System.getenv("GALETO_BENCH") != null || Testes.pular("rinha"))
			return;
		ChatTeste chat = new ChatTeste(contexto, "rinha_teste.log");
		Testes.prepararCliente(contexto);

		try (TestSingleplayerContext mundo = contexto.worldBuilder().create()) {
			contexto.waitTicks(40);   // sem waitForChunksRender: a Rinha não depende do terreno desenhado
			final TestServerContext servidor = mundo.getServer();
			servidor.runCommand("time set noon");
			servidor.runCommand("weather clear");
			servidor.runCommand("tp @p 0 -60 -3 0 8");
			servidor.runCommand("summon galetocraft:taturico 0 -60 2 {Rotation:[180f,0f]}");
			contexto.waitTicks(20);

			chat.comando("galetocraft equipe teste cocorrego pirococo esporoco");
			chat.comando("galetocraft desafiar");
			chat.exigir(chat.contem("Combate:"), "o menu da Rinha não apareceu");
			chat.exigir(chat.contem("entra a equipe de teste"), "sem Galetos, a Rinha deveria usar a equipe de teste");
			chat.exigir(servidor.computeOnServer(s -> selvagens(s).stream().allMatch(g -> g.emRinha() && g.isNoAi())),
					"o Taturico não ficou parado durante a Rinha");
			chat.exigir(chat.botoes("/galetocraft acao itens").isEmpty(), "Itens ativo sem a Pena de Captura");
			contexto.takeScreenshot("rinha_menu_inicio");

			// escolhas secretas da Mira Anatômica, pelos botões
			chat.comando(chat.botao("/galetocraft acao mira cabeca_crina"));
			chat.comando(chat.botao("/galetocraft acao guarda tronco"));
			chat.exigir(chat.botoes("/galetocraft acao pena").isEmpty(), "Pena de Ritmo oferecida antes da Concentração");

			// Concentração cria a Pena de Ritmo; o botão da Pena aparece e é usado no golpe seguinte
			chat.comando(chat.botaoComRotulo("Concentração"));
			int acoes = 1;
			if (!terminou(chat)) {
				chat.comando(chat.botao("/galetocraft acao pena"));
				chat.exigir(chat.contem("Pena de Ritmo: SIM"), "a Pena de Ritmo não foi marcada");
				contexto.takeScreenshot("rinha_menu_pena");
			}

			Random rng = new Random(20261118L);
			String concentracao = chat.botaoComRotulo("Concentração");
			while (!terminou(chat) && acoes < MAX_ACOES) {
				List<String> golpes = new ArrayList<>(chat.botoes("/galetocraft acao golpe "));
				chat.exigir(!golpes.isEmpty(), "nenhum golpe disponível no menu");
				List<String> dano = golpes.stream().filter(g -> !g.equals(concentracao)).toList();
				String escolhido = !dano.isEmpty() && rng.nextDouble() < 0.85 ? dano.get(rng.nextInt(dano.size())) : golpes.get(0);
				chat.comando(escolhido);
				acoes++;
			}
			chat.exigir(terminou(chat), "a Rinha não terminou em " + MAX_ACOES + " ações");
			contexto.takeScreenshot("rinha_fim");

			chat.exigir(servidor.computeOnServer(s -> selvagens(s).stream().noneMatch(g -> g.emRinha() || g.isNoAi())),
					"o Galeto selvagem continuou sem IA depois da Rinha");

			// fora da Rinha os botões avisam em vez de quebrar
			chat.comando("galetocraft acao golpe 0");
			chat.exigir(chat.contem("Você não está em uma Rinha."), "ação fora da Rinha sem aviso");
			chat.gravar("ok após " + acoes + " ações");
		}
	}

	static List<GaloEntity> selvagens(MinecraftServer s) {
		return s.overworld().getEntitiesOfClass(GaloEntity.class, new AABB(-64, -70, -64, 64, 0, 64));
	}

	private static boolean terminou(ChatTeste chat) {
		return chat.contem("Você venceu a Rinha!") || chat.contem("Você perdeu a Rinha.");
	}
}
