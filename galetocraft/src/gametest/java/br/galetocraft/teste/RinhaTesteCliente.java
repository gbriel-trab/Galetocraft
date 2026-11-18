package br.galetocraft.teste;

import br.galetocraft.entidade.GaloEntity;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.fabricmc.fabric.api.client.message.v1.ClientReceiveMessageEvents;
import net.minecraft.network.chat.ClickEvent;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.phys.AABB;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

/**
 * Rinha jogada de ponta a ponta no cliente, como um jogador faria:
 * <ol>
 * <li>define a equipe de teste com {@code /galetocraft equipe};</li>
 * <li>desafia um Taturico selvagem com {@code /galetocraft desafiar};</li>
 * <li>joga clicando nos botões do menu do chat (usa os comandos dos próprios botões), trocando mira, guarda e Pena;</li>
 * <li>confere que a Rinha termina com vitória ou derrota e que o Galeto selvagem volta a ter IA.</li>
 * </ol>
 * Grava o chat inteiro em {@code rinha_teste.log} (pasta GALETO_RINHA_SAIDA, padrão a pasta de execução) e tira
 * prints do menu. Não roda no modo benchmark. Para rodar só ele: GALETO_TESTES=rinha.
 */
@SuppressWarnings("UnstableApiUsage")
public class RinhaTesteCliente implements FabricClientGameTest {
	private static final int MAX_ACOES = 60;

	@Override
	public void runTest(ClientGameTestContext contexto) {
		if (System.getenv("GALETO_BENCH") != null || Testes.pular("rinha"))
			return;

		final List<Component> chat = Collections.synchronizedList(new ArrayList<>());
		ClientReceiveMessageEvents.GAME.register((mensagem, barraDeAcao) -> {
			if (!barraDeAcao)
				chat.add(mensagem);
		});

		// janela padrão e poucos quadros por segundo: em renderização por software (Xvfb) a tela grande toma a CPU
		// da geração do mundo e o carregamento passa do tempo limite
		contexto.runOnClient(mc -> mc.options.framerateLimit().set(30));
		contexto.runOnClient(mc -> mc.options.getSoundSourceOptionInstance(SoundSource.MASTER).set(0.0));
		contexto.runOnClient(mc -> mc.options.hideGui = false);
		contexto.runOnClient(mc -> mc.options.renderDistance().set(2));   // leve também em renderização por software

		try (TestSingleplayerContext mundo = contexto.worldBuilder().create()) {
			contexto.waitTicks(40);   // sem waitForChunksRender: a Rinha não depende do terreno desenhado
			final TestServerContext servidor = mundo.getServer();
			servidor.runCommand("time set noon");
			servidor.runCommand("weather clear");
			servidor.runCommand("tp @p 0 -60 -3 0 8");
			servidor.runCommand("summon galetocraft:taturico 0 -60 2 {Rotation:[180f,0f]}");
			contexto.waitTicks(20);

			comando(contexto, "galetocraft equipe cocorrego pirococo esporoco");
			comando(contexto, "galetocraft desafiar");
			exigir(texto(chat).contains("Combate:"), "o menu da Rinha não apareceu", chat);
			exigir(servidor.computeOnServer(s -> selvagens(s).stream().allMatch(g -> g.emRinha() && g.isNoAi())),
					"o Taturico não ficou parado durante a Rinha", chat);
			contexto.takeScreenshot("rinha_menu_inicio");

			// escolhas secretas da Mira Anatômica, pelos botões
			comando(contexto, botao(chat, "/galetocraft acao mira cabeca_crina"));
			comando(contexto, botao(chat, "/galetocraft acao guarda tronco"));
			exigir(botoesDoUltimoMenu(chat, "/galetocraft acao pena").isEmpty(), "Pena de Ritmo oferecida antes da Concentração", chat);

			// Concentração cria a Pena de Ritmo; o botão da Pena aparece e é usado no golpe seguinte (Canto Ofensivo)
			comando(contexto, comandoDoBotao(chat, "Concentração"));
			int acoes = 1;
			if (!terminou(chat)) {
				comando(contexto, botao(chat, "/galetocraft acao pena"));
				exigir(texto(chat).contains("Pena de Ritmo: SIM"), "a Pena não foi marcada", chat);
				contexto.takeScreenshot("rinha_menu_pena");
			}

			Random rng = new Random(20261118L);
			String concentracao = comandoDoBotao(chat, "Concentração");
			while (!terminou(chat) && acoes < MAX_ACOES) {
				List<String> golpes = new ArrayList<>(botoesDoUltimoMenu(chat, "/galetocraft acao golpe "));
				exigir(!golpes.isEmpty(), "nenhum golpe disponível no menu", chat);
				// prefere golpes de dano e às vezes concentra
				List<String> dano = golpes.stream().filter(g -> !g.equals(concentracao)).toList();
				String escolhido = !dano.isEmpty() && rng.nextDouble() < 0.85 ? dano.get(rng.nextInt(dano.size())) : golpes.get(0);
				comando(contexto, escolhido);
				acoes++;
			}
			exigir(terminou(chat), "a Rinha não terminou em " + MAX_ACOES + " ações", chat);
			contexto.takeScreenshot("rinha_fim");

			exigir(servidor.computeOnServer(s -> selvagens(s).stream().noneMatch(g -> g.emRinha() || g.isNoAi())),
					"o Galeto selvagem continuou sem IA depois da Rinha", chat);

			// fora da Rinha os botões avisam em vez de quebrar
			comando(contexto, "galetocraft acao golpe 0");
			exigir(texto(chat).contains("Você não está em uma Rinha."), "ação fora da Rinha sem aviso", chat);
			gravar(chat, "ok após " + acoes + " ações");
		}
	}

	private static List<GaloEntity> selvagens(net.minecraft.server.MinecraftServer s) {
		return s.overworld().getEntitiesOfClass(GaloEntity.class, new AABB(-64, -70, -64, 64, 0, 64));
	}

	private static void comando(ClientGameTestContext contexto, String comando) {
		String semBarra = comando.startsWith("/") ? comando.substring(1) : comando;
		contexto.runOnClient(mc -> mc.player.connection.sendCommand(semBarra));
		contexto.waitTicks(5);
	}

	private static boolean terminou(List<Component> chat) {
		String t = texto(chat);
		return t.contains("Você venceu a Rinha!") || t.contains("Você perdeu a Rinha.");
	}

	private static String texto(List<Component> chat) {
		synchronized (chat) {
			StringBuilder sb = new StringBuilder();
			chat.forEach(c -> sb.append(c.getString()).append('\n'));
			return sb.toString();
		}
	}

	/** Comandos dos botões clicáveis da última linha do menu que começa com o prefixo dado. */
	private static List<String> botoesDoUltimoMenu(List<Component> chat, String prefixo) {
		List<String> comandos = new ArrayList<>();
		synchronized (chat) {
			for (int i = chat.size() - 1; i >= 0 && comandos.isEmpty(); i--)
				coletar(chat.get(i), prefixo, comandos);
		}
		return comandos;
	}

	private static void coletar(Component c, String prefixo, List<String> saida) {
		if (c.getStyle().getClickEvent() instanceof ClickEvent.RunCommand rc && rc.command().startsWith(prefixo))
			saida.add(rc.command());
		c.getSiblings().forEach(f -> coletar(f, prefixo, saida));
	}

	/** Comando do botão cujo texto contém o rótulo dado, na última mensagem do chat que tem esse botão. */
	private static String comandoDoBotao(List<Component> chat, String rotulo) {
		synchronized (chat) {
			for (int i = chat.size() - 1; i >= 0; i--)
				for (Component f : chat.get(i).getSiblings())
					if (f.getString().contains(rotulo) && f.getStyle().getClickEvent() instanceof ClickEvent.RunCommand rc)
						return rc.command();
		}
		exigir(false, "botão ausente: " + rotulo, chat);
		return null;
	}

	private static String botao(List<Component> chat, String comando) {
		String prefixo = comando.substring(0, comando.lastIndexOf(' ') + 1);
		List<String> achados = botoesDoUltimoMenu(chat, comando.endsWith("pena") ? comando : prefixo);
		exigir(achados.contains(comando), "botão ausente no menu: " + comando, chat);
		return comando;
	}

	private static void exigir(boolean condicao, String falha, List<Component> chat) {
		if (!condicao) {
			gravar(chat, "FALHA: " + falha);
			throw new AssertionError(falha);
		}
	}

	private static void gravar(List<Component> chat, String resultado) {
		Path saida = Path.of(System.getenv().getOrDefault("GALETO_RINHA_SAIDA", ".")).resolve("rinha_teste.log");
		try {
			Files.writeString(saida, texto(chat) + "\n" + resultado + "\n", StandardCharsets.UTF_8);
		} catch (IOException e) {
			throw new RuntimeException(e);
		}
	}
}
