package br.galetocraft.teste;

import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.message.v1.ClientReceiveMessageEvents;
import net.minecraft.network.chat.ClickEvent;
import net.minecraft.network.chat.Component;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Chat do cliente nos testes: guarda as mensagens do servidor, envia comandos como o jogador e acha os comandos dos
 * botões clicáveis (como um clique faria). O registro vai para GALETO_RINHA_SAIDA (padrão: pasta de execução).
 */
final class ChatTeste {
	final List<Component> mensagens = Collections.synchronizedList(new ArrayList<>());
	private final ClientGameTestContext contexto;
	private final String arquivo;

	ChatTeste(ClientGameTestContext contexto, String arquivo) {
		this.contexto = contexto;
		this.arquivo = arquivo;
		ClientReceiveMessageEvents.GAME.register((mensagem, barraDeAcao) -> {
			if (!barraDeAcao)
				mensagens.add(mensagem);
		});
	}

	void comando(String comando) {
		String semBarra = comando.startsWith("/") ? comando.substring(1) : comando;
		contexto.runOnClient(mc -> mc.player.connection.sendCommand(semBarra));
		contexto.waitTicks(5);
	}

	String texto() {
		synchronized (mensagens) {
			StringBuilder sb = new StringBuilder();
			mensagens.forEach(c -> sb.append(c.getString()).append('\n'));
			return sb.toString();
		}
	}

	boolean contem(String trecho) {
		return texto().contains(trecho);
	}

	int contar(String trecho) {
		String t = texto();
		int n = 0;
		for (int i = t.indexOf(trecho); i >= 0; i = t.indexOf(trecho, i + 1))
			n++;
		return n;
	}

	/** Comandos dos botões da última mensagem que tem botões com o prefixo dado. */
	List<String> botoes(String prefixo) {
		List<String> comandos = new ArrayList<>();
		synchronized (mensagens) {
			for (int i = mensagens.size() - 1; i >= 0 && comandos.isEmpty(); i--)
				coletar(mensagens.get(i), prefixo, comandos);
		}
		return comandos;
	}

	private static void coletar(Component c, String prefixo, List<String> saida) {
		if (c.getStyle().getClickEvent() instanceof ClickEvent.RunCommand rc && rc.command().startsWith(prefixo))
			saida.add(rc.command());
		c.getSiblings().forEach(f -> coletar(f, prefixo, saida));
	}

	/**
	 * Botão de golpe com maior Poder (lido da dica do botão) na última linha "Combate:"; sem golpe de dano
	 * disponível, o botão da Concentração.
	 */
	String golpeMaisForte() {
		synchronized (mensagens) {
			for (int i = mensagens.size() - 1; i >= 0; i--) {
				Component m = mensagens.get(i);
				if (!m.getString().startsWith("Combate:"))
					continue;
				String melhor = null, concentracao = null;
				int maior = -1;
				for (Component f : m.getSiblings()) {
					if (!(f.getStyle().getClickEvent() instanceof ClickEvent.RunCommand rc) || !rc.command().startsWith("/galetocraft acao golpe "))
						continue;
					if (f.getString().contains("Concentração"))
						concentracao = rc.command();
					if (f.getStyle().getHoverEvent() instanceof net.minecraft.network.chat.HoverEvent.ShowText dica) {
						java.util.regex.Matcher p = java.util.regex.Pattern.compile("Poder (\\d+)").matcher(dica.value().getString());
						if (p.find() && Integer.parseInt(p.group(1)) > maior) {
							maior = Integer.parseInt(p.group(1));
							melhor = rc.command();
						}
					}
				}
				return melhor != null ? melhor : concentracao;
			}
		}
		exigir(false, "menu de Combate ausente");
		return null;
	}

	/** Comando do botão cujo texto contém o rótulo, na última mensagem que o tem. */
	String botaoComRotulo(String rotulo) {
		synchronized (mensagens) {
			for (int i = mensagens.size() - 1; i >= 0; i--)
				for (Component f : mensagens.get(i).getSiblings())
					if (f.getString().contains(rotulo) && f.getStyle().getClickEvent() instanceof ClickEvent.RunCommand rc)
						return rc.command();
		}
		exigir(false, "botão ausente: " + rotulo);
		return null;
	}

	/** Confere que o botão existe no menu e devolve o comando dele. */
	String botao(String comando) {
		boolean achou = false;
		synchronized (mensagens) {
			for (int i = mensagens.size() - 1; i >= Math.max(0, mensagens.size() - 30) && !achou; i--) {
				List<String> l = new ArrayList<>();
				coletar(mensagens.get(i), comando, l);
				achou = l.contains(comando);
			}
		}
		exigir(achou, "botão ausente no menu: " + comando);
		return comando;
	}

	void exigir(boolean condicao, String falha) {
		if (!condicao) {
			gravar("FALHA: " + falha);
			throw new AssertionError(falha);
		}
	}

	void gravar(String resultado) {
		Path saida = Path.of(System.getenv().getOrDefault("GALETO_RINHA_SAIDA", ".")).resolve(arquivo);
		try {
			Files.writeString(saida, texto() + "\n" + resultado + "\n", StandardCharsets.UTF_8);
		} catch (IOException e) {
			throw new RuntimeException(e);
		}
	}
}
