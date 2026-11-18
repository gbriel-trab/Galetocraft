package br.galetocraft.nucleo.regras;

import br.galetocraft.nucleo.dados.Atributo;

import java.math.BigDecimal;
import java.util.List;

/**
 * Mira Anatômica Estratégica V1.5 (regra mira, homologada em 12/11/2026).
 * <p>
 * O atacante escolhe uma região e o defensor escolhe uma Guarda em segredo. A região multiplica a
 * <b>precisão</b> do golpe (não o dano). O HP retirado na ação gera Pressão na região. Em 50 a região fica exposta
 * (+15% de dano), e em 100 rompe: penalidade de atributo por 2 oportunidades do alvo e janela de +25%.
 */
public final class MiraAnatomica {
	public static final int PRESSAO_MAXIMA = 100;
	public static final int EXPOSICAO = 50;
	public static final int RUPTURA = 100;
	public static final int GANHO_MAXIMO_POR_ACAO = 65;
	public static final int DECAIMENTO_SEM_ACERTO = 10;
	public static final int LEITURA_PERFEITA = 8;
	public static final int CANTO_OFENSIVO_PRESSAO = 6;
	public static final int DURACAO_RUPTURA = 2;

	public enum Regiao {
		CABECA_CRINA("Cabeça/crina", 0.78, 1.10, -0.45, Atributo.ATAQUE_MAGICO),
		ASAS("Asas", 0.86, 1.00, -0.40, Atributo.VELOCIDADE),
		PERNAS_GARRAS("Pernas/garras", 0.90, 1.00, -0.45, Atributo.ATAQUE_FISICO),
		TRONCO("Tronco", 1.00, 0.55, -0.30, Atributo.DEFESA_FISICA, Atributo.DEFESA_MAGICA);

		/** Nome da região como aparece para o jogador. */
		public final String nome;
		/** Multiplicador da precisão original do golpe. */
		public final double precisao;
		public final double fatorPressao;
		/** Variação dos atributos afetados durante a Ruptura (ex.: −0,45 = −45%). */
		public final double variacaoRuptura;
		public final List<Atributo> atributosRuptura;

		Regiao(String nome, double precisao, double fatorPressao, double variacaoRuptura, Atributo... atributos) {
			this.nome = nome;
			this.precisao = precisao;
			this.fatorPressao = fatorPressao;
			this.variacaoRuptura = variacaoRuptura;
			this.atributosRuptura = List.of(atributos);
		}
	}

	/** Guarda do defensor em relação à região atacada. */
	public enum Guarda {
		CORRETA("0.65", 0.20, 0), NEUTRA("1", 1.0, 0), ERRADA("1.10", 1.0, 10);

		private final BigDecimal dano;
		public final double fatorPressao;
		public final int bonusPressao;

		Guarda(String dano, double fatorPressao, int bonusPressao) {
			this.dano = new BigDecimal(dano);
			this.fatorPressao = fatorPressao;
			this.bonusPressao = bonusPressao;
		}

		public BigDecimal multiplicadorDano() {
			return dano;
		}
	}

	private MiraAnatomica() {
	}

	/**
	 * Pressão gerada numa região por uma ação que retirou {@code hpRetirado} de HP (somado de todos os acertos):
	 * {@code min(65, max(1, floor((18 + 200·L/HPmax)·F·G) + B))}. Com Canto Ofensivo, +6 antes da Guarda.
	 */
	public static int pressao(int hpRetirado, int hpMax, Regiao regiao, Guarda guarda, boolean cantoOfensivo) {
		if (hpRetirado <= 0)
			return 0;
		double bruto = (18.0 + 200.0 * hpRetirado / hpMax) * regiao.fatorPressao;
		if (cantoOfensivo)
			bruto += CANTO_OFENSIVO_PRESSAO;
		int p = (int) Math.floor(bruto * guarda.fatorPressao) + guarda.bonusPressao;
		return Math.min(GANHO_MAXIMO_POR_ACAO, Math.max(1, p));
	}

	/** Medidor de uma região de um Cocorídeo. */
	public static final class Medidor {
		private int valor;

		public int valor() {
			return valor;
		}

		public boolean exposta() {
			return valor >= EXPOSICAO && valor < RUPTURA;
		}

		/** Soma a pressão da ação; devolve {@code true} se a região rompeu (aplicar só após a ação completa). */
		public boolean somar(int pressao) {
			valor = Math.min(PRESSAO_MAXIMA, valor + pressao);
			if (valor >= RUPTURA) {
				valor = 0;
				return true;
			}
			return false;
		}

		/** Oportunidade própria do alvo sem acerto direto na região: −10. */
		public void decair() {
			valor = Math.max(0, valor - DECAIMENTO_SEM_ACERTO);
		}

		/** Troca voluntária: mantém metade, arredondada para baixo. */
		public void trocar() {
			valor = valor / 2;
		}
	}
}
