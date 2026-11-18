package br.galetocraft.nucleo.regras;

import br.galetocraft.nucleo.dados.Galetario;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

import java.util.HashMap;
import java.util.Map;

/**
 * Captura com a Pena (regra captura: balanceamento final v1256, Pena v1258, cooldown v1259).
 * <ul>
 * <li>{@code D = 1 + (nível_alvo − 1)/60}; {@code P(%) = 100·força/(força + D)}.</li>
 * <li>Mundo: {@code força = R·F}. Rinha: {@code força = R·F·H·S}, com {@code H = 1 + 1,5·(1 − HP/HPmax)}
 * e S pelo estado do alvo (Sono 1,55; Paralisia 1,25; demais 1).</li>
 * <li>F pelo nível da Pena (1,0 / 1,3 / 1,65 / 2,05 / 2,5). Lendário exige Pena nível 5.</li>
 * <li>Divino e Lendário Original: condições não definidas na regra; aqui são sempre inelegíveis.</li>
 * </ul>
 */
public final class Captura {
	public enum Modalidade { MUNDO, RINHA }

	private final Map<String, Double> fatorRaridade = new HashMap<>();
	private final Map<String, Integer> xpBaseRaridade = new HashMap<>();
	private final Map<Integer, Double> fatorPena = new HashMap<>();
	private final Map<String, Double> fatorEstado = new HashMap<>();
	private final Map<String, Integer> cooldown = new HashMap<>();
	private final double divisorNivel, coeficienteHp;
	private final int xpPorNivelAlvo, nivelPenaLendario;

	public Captura(Galetario g) {
		JsonObject c = g.regraObjeto("captura");
		JsonObject p = c.getAsJsonObject("parametros");
		p.getAsJsonObject("raridade_fatores_json").entrySet().forEach(e -> fatorRaridade.put(e.getKey(), e.getValue().getAsDouble()));
		p.getAsJsonObject("raridade_xp_base_json").entrySet().forEach(e -> xpBaseRaridade.put(e.getKey(), e.getValue().getAsInt()));
		divisorNivel = p.get("divisor_dificuldade_nivel").getAsDouble();
		coeficienteHp = p.get("coeficiente_bonus_hp_rinha").getAsDouble();
		xpPorNivelAlvo = p.get("incremento_xp_por_nivel_alvo").getAsInt();
		for (JsonElement n : c.getAsJsonArray("niveis_pena")) {
			JsonObject o = n.getAsJsonObject();
			fatorPena.put(o.get("nivel_pena").getAsInt(), o.get("fator_forca").getAsDouble());
		}
		for (JsonElement s : c.getAsJsonArray("fatores_estado_rinha")) {
			JsonObject o = s.getAsJsonObject();
			fatorEstado.put(o.get("estado_negativo").getAsString(), o.get("fator_estado").getAsDouble());
		}
		for (JsonElement s : c.getAsJsonArray("cooldown_falha_mundo")) {
			JsonObject o = s.getAsJsonObject();
			cooldown.put(o.get("raridade").getAsString(), o.get("espera_segundos").isJsonNull() ? null : o.get("espera_segundos").getAsInt());
		}
		nivelPenaLendario = c.getAsJsonObject("lendarios").get("nivel_minimo_pena").getAsInt();
	}

	/**
	 * A regra de captura não define a classe "Lendário Original" (decisão de 18/11/2026: classe própria, fora da
	 * escala). Por isso ela fica inelegível, como o Divino, até o criador decidir.
	 */
	private static String raridadeCaptura(String raridade) {
		return raridade;
	}

	public boolean elegivel(String raridade, int nivelPena) {
		String r = raridadeCaptura(raridade);
		if (r.equals("Divino") || !fatorRaridade.containsKey(r))
			return false;
		return !r.equals("Lendário") || nivelPena >= nivelPenaLendario;
	}

	/**
	 * Chance de captura em %, ou 0 se inelegível.
	 *
	 * @param estado nome do estado negativo do alvo (só na Rinha), ou {@code null}
	 */
	public double chancePercentual(Modalidade m, String raridade, int nivelPena, int nivelAlvo, int hpAtual, int hpMax, String estado) {
		if (!elegivel(raridade, nivelPena))
			return 0;
		double forca = fatorRaridade.get(raridadeCaptura(raridade)) * fatorPena.get(nivelPena);
		if (m == Modalidade.RINHA) {
			forca *= 1 + coeficienteHp * (1 - (double) hpAtual / hpMax);
			if (estado != null)
				forca *= fatorEstado.getOrDefault(estado, 1.0);
		}
		double d = 1 + (nivelAlvo - 1) / divisorNivel;
		return 100 * forca / (forca + d);
	}

	/** XP ganha pela Pena numa captura: {@code XP_base(raridade) + 2·nível_alvo}. */
	public int xpPena(String raridade, int nivelAlvo) {
		return xpBaseRaridade.get(raridadeCaptura(raridade)) + xpPorNivelAlvo * nivelAlvo;
	}

	/** Espera após falha no mundo, em segundos (20 de Comum a Mítico; 60 para Lendário). */
	public Integer cooldownMundo(String raridade) {
		return cooldown.get(raridadeCaptura(raridade));
	}
}
