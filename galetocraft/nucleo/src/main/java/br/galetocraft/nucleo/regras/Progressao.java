package br.galetocraft.nucleo.regras;

import br.galetocraft.nucleo.dados.Atributo;

import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;

/**
 * Atributos de um Cocorídeo no nível (regra progressao e combate_universal, rev. 8 da base).
 * <ul>
 * <li><b>Níveis 50–100</b> (Norma Nível 50 V1, homologada em 13/11): {@code A(L) = A50 × (L+50)/100}.</li>
 * <li><b>Níveis 1–49</b> (norma R5.4, adotada em 18/11): {@code A(L) = A50 × (49 + 3(L−1))/196}, de 25% no
 * nível 1 a 98,47% no 49.</li>
 * <li><b>HP nominal</b> (norma R5.4, adotada em 18/11; HP 10 no nível 1 e 1,5 × o HP-base no nível 50, como na
 * Combate v1.0): 1–49 {@code round_half_up(10 + (ceil(1,5·HP50) − 10)·(L−1)/49)};
 * 50–100 {@code ceil(1,5·HP50·(L+50)/100)}.</li>
 * <li><b>IV e EV</b> (oficiais desde 08/11): {@code floor(A_n × (1 + (0,25·IV + 0,5·√EV)/100))}, IV de 1 a 40,
 * EV sem teto.</li>
 * <li><b>Peso</b> (Peso e Alimentação V1.2), aplicado por último com arredondamento ao inteiro mais próximo
 * (empate para cima) e mínimo 1, sobre HP, defesas e Velocidade; os ataques não mudam. Com a razão
 * {@code r = peso/peso natural} (0,8 a 1,5; o Galeto nasce com r = 1):
 * r ≥ 1: HP {@code 1+0,10(r−1)}, defesas {@code 1+0,15(r−1)}, Velocidade {@code 1−0,50(r−1)};
 * r &lt; 1: HP {@code 1+0,40(r−1)}, defesas {@code 1+0,50(r−1)}, Velocidade {@code 1−0,20(r−1)}.</li>
 * <li><b>HP de referência da Vitalidade V5.6.1</b> (R5.4, adotado em 18/11):
 * {@code HP_ref(L) = floor(1,05 × HP_n(L; HP50 = 80))} (IV 20, EV 0, peso neutro).</li>
 * </ul>
 */
public final class Progressao {
	public static final int NIVEL_REFERENCIA = 50;
	public static final int NIVEL_MINIMO = 1;
	public static final int NIVEL_MAXIMO = 100;
	public static final int HP_NIVEL_1 = 10;
	public static final int HP50_REFERENCIA = 80;
	public static final int IV_REFERENCIA = 20;
	public static final double PESO_MINIMO = 0.8, PESO_MAXIMO = 1.5, PESO_NEUTRO = 1.0;
	private static final MathContext MC = MathContext.DECIMAL64;

	private Progressao() {
	}

	/** Valor nominal exato do atributo (não HP) no nível, sem IV, EV nem peso. */
	public static BigDecimal atributo(int base50, int nivel) {
		validar(nivel);
		if (nivel >= NIVEL_REFERENCIA)
			return BigDecimal.valueOf((long) base50 * (nivel + 50)).divide(BigDecimal.valueOf(100), MC);
		return BigDecimal.valueOf((long) base50 * (49 + 3L * (nivel - 1))).divide(BigDecimal.valueOf(196), MC);
	}

	/** HP nominal no nível (inteiro), sem IV, EV nem peso. */
	public static int hpNominal(int hp50, int nivel) {
		validar(nivel);
		long hpNo50 = (3L * hp50 + 1) / 2;                                  // ceil(1,5 × HP50)
		if (nivel >= NIVEL_REFERENCIA)
			return (int) Math.ceilDiv(3L * hp50 * (nivel + 50), 200);         // ceil(1,5 × HP50 × (L+50)/100)
		long num = HP_NIVEL_1 * 49L + (hpNo50 - HP_NIVEL_1) * (nivel - 1);    // (10·49 + (c−10)(L−1)) / 49
		return (int) Math.floorDiv(2 * num + 49, 98);                         // arredondamento half-up
	}

	/** Aplica IV e EV: {@code floor(A_n × (1 + (0,25·IV + 0,5·√EV)/100))}. */
	public static int comIvEv(BigDecimal nominal, int iv, double ev) {
		BigDecimal bonus = BigDecimal.valueOf(iv).multiply(new BigDecimal("0.25"))
				.add(BigDecimal.valueOf(Math.max(0, ev)).sqrt(MC).multiply(new BigDecimal("0.5")));
		BigDecimal fator = BigDecimal.ONE.add(bonus.divide(BigDecimal.valueOf(100), MC));
		return nominal.multiply(fator, MC).setScale(0, RoundingMode.FLOOR).intValueExact();
	}

	/** Multiplicador de peso V1.2 para o atributo (1 para os ataques). */
	public static BigDecimal multiplicadorPeso(Atributo a, double razaoPeso) {
		BigDecimal d = BigDecimal.valueOf(Math.max(PESO_MINIMO, Math.min(PESO_MAXIMO, razaoPeso))).subtract(BigDecimal.ONE);
		boolean acima = d.signum() >= 0;
		String k = switch (a) {
			case HP -> acima ? "0.10" : "0.40";
			case DEFESA_FISICA, DEFESA_MAGICA -> acima ? "0.15" : "0.50";
			case VELOCIDADE -> acima ? "-0.50" : "-0.20";
			case ATAQUE_FISICO, ATAQUE_MAGICO -> "0";
		};
		return BigDecimal.ONE.add(new BigDecimal(k).multiply(d, MC));
	}

	/** Aplica o peso: inteiro mais próximo, empate para cima, mínimo 1. */
	public static int comPeso(int valor, Atributo a, double razaoPeso) {
		int v = BigDecimal.valueOf(valor).multiply(multiplicadorPeso(a, razaoPeso), MC).setScale(0, RoundingMode.HALF_UP).intValueExact();
		return Math.max(1, v);
	}

	/** Atributo final do indivíduo: nominal → IV/EV → peso. */
	public static int atributoFinal(Atributo a, int base50, int nivel, int iv, double ev, double razaoPeso) {
		BigDecimal nominal = a == Atributo.HP ? BigDecimal.valueOf(hpNominal(base50, nivel)) : atributo(base50, nivel);
		return comPeso(comIvEv(nominal, iv, ev), a, razaoPeso);
	}

	/** HP de referência da Vitalidade: {@code floor(1,05 × HP_n(L; HP50 = 80))}. */
	public static int hpReferencia(int nivel) {
		return comIvEv(BigDecimal.valueOf(hpNominal(HP50_REFERENCIA, nivel)), IV_REFERENCIA, 0);
	}

	/** Resistência por Vitalidade V5.6.1: {@code clamp((HP_ref(L)/HPmax)^0,2; 0,8; 1,0)}, L = nível do defensor. */
	public static double vitalidade(int nivelDefensor, int hpMaxDefensor) {
		double f = Math.pow((double) hpReferencia(nivelDefensor) / Math.max(1, hpMaxDefensor), 0.2);
		return Math.max(0.8, Math.min(1.0, f));
	}

	private static void validar(int nivel) {
		if (nivel < NIVEL_MINIMO || nivel > NIVEL_MAXIMO)
			throw new IllegalArgumentException("Nível fora de 1–100: " + nivel);
	}
}
