package br.galetocraft.nucleo.regras;

import br.galetocraft.nucleo.dados.Elemento;
import br.galetocraft.nucleo.dados.Galetario;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

import java.util.EnumMap;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;

/**
 * Eficácia elemental: matriz 6×6 (regra matriz_elemental), Tipagem Dupla V1 e Nexo V2.0 (regra nexo_relacoes).
 * <p>
 * O fator final é o produto dos fatores contra cada elemento do defensor, aplicado uma única vez. Isso dá
 * exatamente a Tipagem Dupla V1 (4× só com fraqueza comum, 0,25× com duas resistências) e a regra tripla do Nexo.
 * Golpes Neutros e sem elemento valem 1×.
 */
public final class Eficacia {
	private final Map<Elemento, Map<Elemento, Double>> fatores = new EnumMap<>(Elemento.class);

	public Eficacia(Galetario g) {
		JsonObject mult = g.regraObjeto("matriz_elemental").getAsJsonObject("multiplicadores");
		mult.entrySet().forEach(atk -> atk.getValue().getAsJsonObject().entrySet().forEach(def ->
				definir(Elemento.deTexto(atk.getKey()), Elemento.deTexto(def.getKey()), def.getValue().getAsDouble())));
		for (JsonElement r : g.regra("nexo_relacoes").getAsJsonArray()) {
			JsonObject o = r.getAsJsonObject();
			definir(Elemento.deTexto(o.get("attacker").getAsString()), Elemento.deTexto(o.get("defender").getAsString()),
					o.get("multiplier").getAsDouble());
		}
	}

	private void definir(Elemento ataque, Elemento defensor, double fator) {
		fatores.computeIfAbsent(ataque, k -> new EnumMap<>(Elemento.class)).put(defensor, fator);
	}

	/** Fator de um elemento de ataque contra um único elemento do defensor. */
	public double fator(Elemento ataque, Elemento defensor) {
		if (!ataque.temEficacia() || !defensor.temEficacia())
			return 1.0;
		return fatores.getOrDefault(ataque, Map.of()).getOrDefault(defensor, 1.0);
	}

	/** Multiplicador final contra um defensor de um, dois ou três elementos. */
	public double multiplicador(Elemento ataque, List<Elemento> defensor) {
		double m = 1.0;
		for (Elemento d : new LinkedHashSet<>(defensor))   // elemento duplicado é rejeitado pela regra: conta uma vez
			m *= fator(ataque, d);
		return m;
	}
}
