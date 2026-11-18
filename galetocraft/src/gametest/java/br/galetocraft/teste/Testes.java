package br.galetocraft.teste;

import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.minecraft.sounds.SoundSource;

import java.util.Arrays;
import java.util.Locale;

/**
 * Filtro dos testes de cliente: GALETO_TESTES=rinha,pirococo roda só os testes listados
 * (nomes: pirococo, galeria, rinha, captura, jornada, tempestade). Sem a variável, todos rodam (exceto no modo benchmark).
 */
final class Testes {
	private Testes() {
	}

	static boolean pular(String nome) {
		String filtro = System.getenv("GALETO_TESTES");
		return filtro != null && !filtro.isBlank()
				&& Arrays.stream(filtro.toLowerCase(Locale.ROOT).split(",")).map(String::trim).noneMatch(nome::equals);
	}

	/**
	 * Cliente leve para os testes de jogabilidade: sem som, com a interface, distância de visão 2 e 30 quadros por
	 * segundo. Em renderização por software (Xvfb) a tela grande toma a CPU da geração do mundo e o carregamento
	 * passa do tempo limite.
	 */
	static void prepararCliente(ClientGameTestContext contexto) {
		contexto.runOnClient(mc -> mc.options.getSoundSourceOptionInstance(SoundSource.MASTER).set(0.0));
		contexto.runOnClient(mc -> mc.options.framerateLimit().set(30));
		contexto.runOnClient(mc -> mc.options.hideGui = false);
		contexto.runOnClient(mc -> mc.options.renderDistance().set(2));
	}
}
