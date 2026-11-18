package br.galetocraft.nucleo.rinha;

import br.galetocraft.nucleo.dados.Golpe;
import br.galetocraft.nucleo.regras.MiraAnatomica;
import br.galetocraft.nucleo.regras.PenaDeRitmo;

/**
 * Escolha secreta de um lado numa rodada: a ação e a Guarda.
 *
 * @param guarda região protegida pelo ativo nesta rodada, ou {@code null} para Guarda neutra
 */
public record Decisao(Acao acao, MiraAnatomica.Regiao guarda) {

	public sealed interface Acao permits UsarGolpe, Trocar, Capturar {
	}

	/**
	 * Usar um golpe equipado.
	 *
	 * @param regiao região mirada (só golpe ofensivo direto), ou {@code null} sem Mira
	 * @param canto  Canto da Pena de Ritmo declarado antes da resolução, ou {@code null}
	 */
	public record UsarGolpe(Golpe golpe, MiraAnatomica.Regiao regiao, PenaDeRitmo.Canto canto) implements Acao {
	}

	/** Troca voluntária: consome a ação e tem prioridade sobre golpes. */
	public record Trocar(int indice, boolean cantoRevezamento) implements Acao {
	}

	/**
	 * Tentativa de captura do Cocorídeo selvagem com a Pena de Captura (Itens → Pena de Captura).
	 * Consome a ação do treinador e é resolvida na ordem regular dos turnos.
	 */
	public record Capturar(int nivelPena) implements Acao {
	}

	public static Decisao golpe(Golpe g) {
		return new Decisao(new UsarGolpe(g, null, null), null);
	}
}
