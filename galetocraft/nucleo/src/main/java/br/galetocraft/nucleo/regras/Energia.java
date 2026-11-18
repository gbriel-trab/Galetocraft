package br.galetocraft.nucleo.regras;

/**
 * Energia (regra combate_universal.energia) e Concentração V2.3 (regra concentracao).
 */
public final class Energia {
	public static final int MAXIMA = 100;
	/** Todo Galeto entra em campo com 100, em qualquer tipo de entrada. */
	public static final int ENTRADA = 100;
	/** Recuperação no início do próprio turno (também na reserva). */
	public static final int REGENERACAO = 20;
	/** Afogado em campo: perde 20 no início da rodada em vez de recuperar. */
	public static final int PERDA_AFOGAMENTO = 20;
	/** Concentração: custo 0, recupera 35 em execução válida. */
	public static final int CONCENTRACAO = 35;
	/** Concentração: chance de remover um estado negativo persistente. */
	public static final double CONCENTRACAO_REMOVE_ESTADO = 0.40;
	/** Canto de Suporte: −15 no custo de um Suporte que não seja Concentração (mínimo 0). */
	public static final int DESCONTO_CANTO_SUPORTE = 15;
	/** Canto da Guarda: +15 se a Guarda localizada estava correta e houve dano ao HP. */
	public static final int CANTO_GUARDA = 15;

	private Energia() {
	}

	public static int somar(int atual, int ganho) {
		return Math.max(0, Math.min(MAXIMA, atual + ganho));
	}

	/** Início do turno próprio: +20, ou −20 se Afogado em campo. */
	public static int inicioDoTurno(int atual, boolean afogadoEmCampo) {
		return somar(atual, afogadoEmCampo ? -PERDA_AFOGAMENTO : REGENERACAO);
	}

	public static int custoComCantoSuporte(int custo) {
		return Math.max(0, custo - DESCONTO_CANTO_SUPORTE);
	}
}
