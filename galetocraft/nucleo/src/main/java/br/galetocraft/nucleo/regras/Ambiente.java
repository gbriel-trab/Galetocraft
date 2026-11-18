package br.galetocraft.nucleo.regras;

import br.galetocraft.nucleo.dados.Atributo;
import br.galetocraft.nucleo.dados.Elemento;
import br.galetocraft.nucleo.dados.Galetario;
import com.google.gson.JsonObject;

import java.util.EnumMap;
import java.util.List;
import java.util.Map;

/**
 * Climas e Santuários (regras climas e santuarios), lidos da base.
 * <ul>
 * <li>No máximo 1 Clima e 1 Santuário ao mesmo tempo, compartilhados pelos dois lados; duração de 4 rodadas.</li>
 * <li>Bônus de dano pelo elemento do <b>golpe</b>, somado aos outros bônus depois da eficácia.</li>
 * <li>Bônus defensivo, energia e cura só para a espécie ativa do elemento correspondente.</li>
 * </ul>
 */
public final class Ambiente {
	public static final int DURACAO = 4;

	public enum Clima { CHUVA("chuva"), ENSOLARADO("ensolarado"), VENTANIA("ventania"), TEMPESTADE_AREIA("tempestade_areia");
		final String id;
		Clima(String id) { this.id = id; }
	}

	public enum Santuario { RAIOS("santuario_raios"), RAIZES("santuario_raizes");
		final String id;
		Santuario(String id) { this.id = id; }
	}

	private final Map<Clima, Map<Elemento, Double>> danoClima = new EnumMap<>(Clima.class);
	private final Map<Clima, Map<Elemento, Map<Atributo, Double>>> defesaClima = new EnumMap<>(Clima.class);
	private final Map<Santuario, Map<Elemento, Double>> danoSantuario = new EnumMap<>(Santuario.class);
	private final Map<Santuario, Map<Elemento, Integer>> energiaSantuario = new EnumMap<>(Santuario.class);
	private final Map<Santuario, Map<Elemento, Double>> curaSantuario = new EnumMap<>(Santuario.class);

	public Ambiente(Galetario g) {
		JsonObject climas = g.regraObjeto("climas");
		for (Clima c : Clima.values()) {
			JsonObject o = climas.getAsJsonObject(c.id);
			danoClima.put(c, porElemento(o.getAsJsonObject("damage_by_move_element")));
			Map<Elemento, Map<Atributo, Double>> def = new EnumMap<>(Elemento.class);
			o.getAsJsonObject("defense_by_species_element").entrySet().forEach(e -> {
				Map<Atributo, Double> m = new EnumMap<>(Atributo.class);
				e.getValue().getAsJsonObject().entrySet().forEach(a -> m.put(
						a.getKey().equals("magical_defense") ? Atributo.DEFESA_MAGICA : Atributo.DEFESA_FISICA, a.getValue().getAsDouble()));
				def.put(Elemento.deTexto(e.getKey()), m);
			});
			defesaClima.put(c, def);
		}
		JsonObject santuarios = g.regraObjeto("santuarios");
		for (Santuario s : Santuario.values()) {
			JsonObject o = santuarios.getAsJsonObject(s.id);
			danoSantuario.put(s, porElemento(o.getAsJsonObject("damage_by_move_element")));
			Map<Elemento, Integer> en = new EnumMap<>(Elemento.class);
			if (o.has("extra_energy_by_active_species_element"))
				o.getAsJsonObject("extra_energy_by_active_species_element").entrySet()
						.forEach(e -> en.put(Elemento.deTexto(e.getKey()), e.getValue().getAsInt()));
			energiaSantuario.put(s, en);
			curaSantuario.put(s, o.has("heal_fraction_max_hp_by_active_species_element")
					? porElemento(o.getAsJsonObject("heal_fraction_max_hp_by_active_species_element")) : Map.of());
		}
	}

	private static Map<Elemento, Double> porElemento(JsonObject o) {
		Map<Elemento, Double> m = new EnumMap<>(Elemento.class);
		o.entrySet().forEach(e -> m.put(Elemento.deTexto(e.getKey()), e.getValue().getAsDouble()));
		return m;
	}

	/** Bônus percentual de dano pelo elemento do golpe (ex.: Chuva +0,25 para Água, −0,25 para Fogo). */
	public double bonusDano(Clima clima, Santuario santuario, Elemento elementoGolpe) {
		double b = 0;
		if (clima != null)
			b += danoClima.get(clima).getOrDefault(elementoGolpe, 0.0);
		if (santuario != null)
			b += danoSantuario.get(santuario).getOrDefault(elementoGolpe, 0.0);
		return b;
	}

	/** Bônus defensivo do Clima para a espécie ativa (ex.: Ventania +10% Defesa Mágica para espécies de Ar). */
	public double bonusDefesa(Clima clima, List<Elemento> elementosEspecie, Atributo defesa) {
		if (clima == null)
			return 0;
		return elementosEspecie.stream()
				.mapToDouble(e -> defesaClima.get(clima).getOrDefault(e, Map.of()).getOrDefault(defesa, 0.0)).max().orElse(0);
	}

	/** Energia extra no início da rodada para a espécie ativa do elemento (Santuário dos Raios: +10 para Elétrico). */
	public int energiaExtra(Santuario santuario, List<Elemento> elementosEspecie) {
		if (santuario == null)
			return 0;
		return elementosEspecie.stream().mapToInt(e -> energiaSantuario.get(santuario).getOrDefault(e, 0)).max().orElse(0);
	}

	/** Fração do HP máximo curada no fim da rodada (Santuário das Raízes: 4% para Planta). */
	public double cura(Santuario santuario, List<Elemento> elementosEspecie) {
		if (santuario == null)
			return 0;
		return elementosEspecie.stream().mapToDouble(e -> curaSantuario.get(santuario).getOrDefault(e, 0.0)).max().orElse(0);
	}
}
