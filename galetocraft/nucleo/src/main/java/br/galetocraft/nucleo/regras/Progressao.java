package br.galetocraft.nucleo.regras;

import java.math.BigDecimal;
import java.math.RoundingMode;

/**
 * Norma de Progressão Nível 50 V1 (regra progressao): os pontos-base valem no nível 50 e crescem
 * +1% do valor-base por nível até o nível 100, onde valem 1,5×: {@code A(L) = A50 × (L+50)/100}.
 * <p>
 * Pendências do criador que este código NÃO inventa:
 * <ul>
 * <li>curva dos níveis 1–49 (pedir um nível abaixo de 50 lança exceção);</li>
 * <li>arredondamento inteiro dos atributos (devolvido exato, sem arredondar);</li>
 * <li>HP efetivo / Resistência por Vitalidade V5.6.1 (ver {@link #hpMaximoProvisorio}).</li>
 * </ul>
 */
public final class Progressao {
	public static final int NIVEL_REFERENCIA = 50;
	public static final int NIVEL_MAXIMO = 100;

	private Progressao() {
	}

	/** Valor exato do atributo no nível {@code nivel} (50–100), sem IV, EV nem peso. */
	public static BigDecimal atributo(int base50, int nivel) {
		validar(nivel);
		return BigDecimal.valueOf((long) base50 * (nivel + 50)).divide(BigDecimal.valueOf(100));
	}

	/**
	 * HP máximo PROVISÓRIO: a progressão do atributo HP arredondada para cima, como as fichas oficiais já fazem
	 * no nível 100 ({@code ceil(1,5 × HP)}). O HP efetivo definitivo depende da Vitalidade V5.6.1, ainda pendente.
	 */
	public static int hpMaximoProvisorio(int hpBase50, int nivel) {
		return atributo(hpBase50, nivel).setScale(0, RoundingMode.CEILING).intValueExact();
	}

	private static void validar(int nivel) {
		if (nivel < NIVEL_REFERENCIA)
			throw new UnsupportedOperationException("Curva dos níveis 1–49 pendente de decisão do criador (nível pedido: " + nivel + ")");
		if (nivel > NIVEL_MAXIMO)
			throw new IllegalArgumentException("Nível acima de 100: " + nivel);
	}
}
