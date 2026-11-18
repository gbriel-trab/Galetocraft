package br.galetocraft.teste;

import java.util.Arrays;
import java.util.Locale;

/**
 * Filtro dos testes de cliente: GALETO_TESTES=rinha,pirococo roda só os testes listados
 * (nomes: pirococo, galeria, rinha). Sem a variável, todos rodam (exceto no modo benchmark).
 */
final class Testes {
	private Testes() {
	}

	static boolean pular(String nome) {
		String filtro = System.getenv("GALETO_TESTES");
		return filtro != null && !filtro.isBlank()
				&& Arrays.stream(filtro.toLowerCase(Locale.ROOT).split(",")).map(String::trim).noneMatch(nome::equals);
	}
}
