package br.galetocraft.nucleo.regras;

/**
 * Regras que dependem da Velocidade: esquiva universal (combate_universal) e Golpe Duplo Estratégico V2.2 (golpe_duplo).
 */
public final class Velocidade {
	private Velocidade() {
	}

	/** Chance de esquiva universal em %: {@code clamp(7,5 + 5·(Vd−Va)/(Vd+Va), 5, 10)}. */
	public static double chanceEsquivaPercentual(double velAtacante, double velDefensor) {
		double v = 7.5 + 5.0 * (velDefensor - velAtacante) / (velDefensor + velAtacante);
		return Math.max(5.0, Math.min(10.0, v));
	}

	/**
	 * Chance universal de segundo acerto (V2.2): 0 se o atacante for mais lento; senão
	 * {@code min(0,50; 0,25 + 0,50·(Va/Vd − 1))}. Definida só para Velocidade do defensor maior que 0.
	 */
	public static double chanceGolpeDuplo(double velAtacante, double velDefensor) {
		if (velDefensor <= 0)
			throw new IllegalArgumentException("Velocidade do defensor deve ser maior que 0 (caso pendente na V2.2)");
		if (velAtacante < velDefensor)
			return 0.0;
		return Math.min(0.5, 0.25 + 0.5 * (velAtacante / velDefensor - 1.0));
	}

	/** Chance intrínseca do golpe combinada de forma independente: {@code 1 − (1−Pu)(1−Pi)}. Nunca há terceiro acerto. */
	public static double combinar(double universal, double intrinseca) {
		return 1.0 - (1.0 - universal) * (1.0 - intrinseca);
	}
}
