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
		String prefixo = comando.contains(" ") ? comando.substring(0, comando.lastIndexOf(' ') + 1) : comando;
		exigir(botoes(prefixo).contains(comando) || botoes(comando).contains(comando), "botão ausente no menu: " + comando);
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
