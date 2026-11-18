package br.galetocraft.nucleo.regras;

/**
 * Efeitos numéricos dos estados negativos (regra estados_negativos).
 * <p>
 * Gerais: no máximo 1 estado por Galeto; reaplicação ignorada; derrota remove; na reserva o efeito e o progresso
 * ficam congelados; Concentração remove com 40% de chance.
 */
public final class Estados {
	public static final double QUEIMADURA_DANO = 0.05;
	public static final double QUEIMADURA_REDUCAO_ATAQUES = 0.20;
	private static final double[] ENVENENAMENTO = {0.10, 0.20, 0.30};
	public static final double TONTO_FALHA = 0.30;
	public static final double TONTO_AUTODANO = 0.50;
	public static final double PARALISIA_PERDE_ACAO = 0.20;
	public static final double PARALISIA_VELOCIDADE = 0.75;

	private Estados() {
	}

	/**
	 * Queimadura: 5% do HP máximo no fim da rodada. A regra não fixa o arredondamento;
	 * usa-se para cima, como no Envenenamento (confirmar com o criador).
	 */
	public static int danoQueimadura(int hpMax) {
		return (int) Math.ceil(hpMax * QUEIMADURA_DANO);
	}

	/**
	 * Envenenamento: dano no fim da rodada (inclusive na rodada da aplicação), arredondado para cima, que
	 * sobe 10% a cada duas ocorrências: 1ª–2ª = 10%, 3ª–4ª = 20%, 5ª em diante = 30% do HP máximo.
	 *
	 * @param ocorrencia número da ocorrência do dano, a partir de 1
	 */
	public static int danoEnvenenamento(int hpMax, int ocorrencia) {
		int bloco = Math.min(ENVENENAMENTO.length - 1, (Math.max(1, ocorrencia) - 1) / 2);
		return (int) Math.ceil(hpMax * ENVENENAMENTO[bloco]);
	}

	/** Paralisia: Velocidade ×0,75, arredondada para cima, mínimo 1. */
	public static int velocidadeParalisada(double velocidade) {
		return Math.max(1, (int) Math.ceil(velocidade * PARALISIA_VELOCIDADE));
	}
}
