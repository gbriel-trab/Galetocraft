package br.galetocraft.nucleo.regras;

import br.galetocraft.nucleo.dados.Galetario;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

import java.util.HashMap;
import java.util.Map;

/**
 * XP dos Cocorídeos (regra experiencia, v1260): XP só em Rinha vencida, uma vez por oponente derrotado,
 * repartida entre os participantes que entraram em campo.
 */
public final class Experiencia {
	private final Map<String, Double> multiplicadorRaridade = new HashMap<>();
	private final Map<String, Double> multiplicadorModo = new HashMap<>();

	public Experiencia(Galetario g) {
		JsonObject x = g.regraObjeto("experiencia");
		for (JsonElement r : x.getAsJsonArray("raridades"))
			multiplicadorRaridade.put(r.getAsJsonObject().get("raridade").getAsString(), r.getAsJsonObject().get("multiplicador").getAsDouble());
		for (JsonElement r : x.getAsJsonArray("modalidades"))
			multiplicadorModo.put(r.getAsJsonObject().get("modalidade").getAsString(), r.getAsJsonObject().get("multiplicador").getAsDouble());
	}

	/** XP total acumulada para estar no nível N: {@code (N−1)³ + 10·(N−1)²}. */
	public static long xpTotal(int nivel) {
		long n = nivel - 1L;
		return n * n * n + 10 * n * n;
	}

	public static long xpParaProximo(int nivel) {
		return xpTotal(nivel + 1) - xpTotal(nivel);
	}

	public static final int NIVEL_MAXIMO = 100;

	/**
	 * Reparte a XP entre os participantes: quociente inteiro para todos e 1 unidade do resto para cada um, na ordem
	 * da primeira entrada em campo. A soma é conservada.
	 */
	public static long[] repartir(long total, int participantes) {
		long[] parcelas = new long[participantes];
		for (int i = 0; i < participantes; i++)
			parcelas[i] = total / participantes + (i < total % participantes ? 1 : 0);
		return parcelas;
	}

	public static int nivelPorXp(long xp) {
		int n = 1;
		while (n < 100 && xpTotal(n + 1) <= xp)
			n++;
		return n;
	}

	/** Fator de desafio: {@code max(0,25; min(1,50; 1 + 0,03·(L − P)))}, P = maior nível de quem entrou em campo. */
	public static double fatorDesafio(int nivelOponente, int maiorNivelParticipante) {
		return Math.max(0.25, Math.min(1.50, 1 + 0.03 * (nivelOponente - maiorNivelParticipante)));
	}

	/**
	 * XP de um oponente derrotado: {@code floor((25 + 15·L) × M_raridade × C_desafio × M_modo)}.
	 *
	 * @param modo "PvE_selvagem" (1,0) ou "PvP_valido" (0,75)
	 */
	public long recompensa(int nivelOponente, String raridadeOponente, int maiorNivelParticipante, String modo) {
		Double mr = multiplicadorRaridade.get(raridadeOponente);
		if (mr == null)   // ex.: "Lendário Original", sem multiplicador definido na regra
			throw new IllegalArgumentException("Raridade sem multiplicador de XP na regra: " + raridadeOponente);
		double m = mr * fatorDesafio(nivelOponente, maiorNivelParticipante) * multiplicadorModo.get(modo);
		return (long) Math.floor((25 + 15.0 * nivelOponente) * m);
	}
}
