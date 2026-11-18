package br.galetocraft.nucleo.rinha;

import br.galetocraft.nucleo.dados.Atributo;
import br.galetocraft.nucleo.regras.Progressao;

import java.util.Arrays;

/**
 * Dados individuais que mudam os atributos: os 6 IVs (1–40), os 6 EVs (sem teto) e a razão de peso
 * (peso/peso natural, 0,8–1,5), na ordem de {@link Atributo}.
 */
public record Individuo(int[] ivs, double[] evs, double razaoPeso) {
	/** Referência da Vitalidade e da equipe de teste: IV 20, EV 0, peso neutro. */
	public static final Individuo REFERENCIA = new Individuo(preencher(Progressao.IV_REFERENCIA), new double[Atributo.values().length], Progressao.PESO_NEUTRO);

	public Individuo {
		if (ivs.length != Atributo.values().length || evs.length != Atributo.values().length)
			throw new IllegalArgumentException("São 6 IVs e 6 EVs");
		ivs = ivs.clone();
		evs = evs.clone();
	}

	/** Indivíduo recém-aparecido: IVs dados, EV 0 e peso neutro (spawn_ratio 1,0 da V1.2). */
	public static Individuo novo(int[] ivs) {
		return new Individuo(ivs, new double[Atributo.values().length], Progressao.PESO_NEUTRO);
	}

	public int iv(Atributo a) { return ivs[a.ordinal()]; }
	public double ev(Atributo a) { return evs[a.ordinal()]; }

	private static int[] preencher(int v) {
		int[] r = new int[Atributo.values().length];
		Arrays.fill(r, v);
		return r;
	}
}
