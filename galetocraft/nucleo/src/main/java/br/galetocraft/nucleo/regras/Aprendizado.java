package br.galetocraft.nucleo.regras;

import br.galetocraft.nucleo.dados.Especie;
import br.galetocraft.nucleo.dados.Galetario;
import br.galetocraft.nucleo.dados.Golpe;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Aprendizado de golpes e slots (regra aprendizado, rev. 8 da base).
 * <ul>
 * <li>15 golpes por nível (incluindo os 5 de origem) e 15 por treinamento com os Mestres, por espécie.</li>
 * <li>Até 5 equipados, com a Concentração fixa; os desequipados continuam aprendidos; nada é equipado sozinho.</li>
 * <li>Na captura, todos os golpes por nível até o nível atual já vêm aprendidos.</li>
 * <li>Depois de desbloquear os 5 golpes de origem, o treinador pode trocar os outros 4 slots por golpes aprendidos,
 * fora da Rinha.</li>
 * </ul>
 * Espécies sem tabela no acervo (#013–#018 e #023): só os 5 golpes de origem ficam disponíveis, sem nível definido.
 */
public final class Aprendizado {
	public static final int MAXIMO_EQUIPADOS = 5;

	/** Golpe aprendido por nível (com o nível) ou por treinamento (nível nulo). */
	public record Entrada(Golpe golpe, boolean porNivel, Integer nivel) {
	}

	private final Map<Integer, List<Entrada>> tabelas = new HashMap<>();

	public Aprendizado(Galetario g) {
		JsonObject t = g.regraObjeto("aprendizado").getAsJsonObject("tabelas");
		for (Map.Entry<String, JsonElement> e : t.entrySet()) {
			Especie esp = g.especie(Integer.parseInt(e.getKey()));
			List<Entrada> lista = new ArrayList<>();
			for (JsonElement x : e.getValue().getAsJsonArray()) {
				JsonObject o = x.getAsJsonObject();
				boolean nivel = o.get("metodo").getAsString().equals("nivel");
				lista.add(new Entrada(esp.golpe(o.get("nome").getAsString()), nivel, nivel ? o.get("nivel").getAsInt() : null));
			}
			tabelas.put(esp.numero(), List.copyOf(lista));
		}
	}

	public boolean temTabela(Especie e) {
		return tabelas.containsKey(e.numero());
	}

	public List<Entrada> tabela(Especie e) {
		return tabelas.getOrDefault(e.numero(), List.of());
	}

	/** Golpes aprendidos por nível até o nível dado, na ordem dos marcos (sem tabela: os 5 de origem). */
	public List<Golpe> porNivel(Especie e, int nivel) {
		if (!temTabela(e))
			return e.originais();
		return tabela(e).stream().filter(x -> x.porNivel() && x.nivel() <= nivel).map(Entrada::golpe).toList();
	}

	/** Golpes que só se aprendem com os Mestres (treinamento). */
	public List<Golpe> porTreinamento(Especie e) {
		return tabela(e).stream().filter(x -> !x.porNivel()).map(Entrada::golpe).toList();
	}

	/** Golpes por nível desbloqueados ao subir de {@code de} para {@code para}. */
	public List<Golpe> novos(Especie e, int de, int para) {
		if (!temTabela(e))
			return List.of();
		return tabela(e).stream().filter(x -> x.porNivel() && x.nivel() > de && x.nivel() <= para).map(Entrada::golpe).toList();
	}

	/** Os 5 golpes de origem já estão desbloqueados? (condição para trocar os slots livres) */
	public boolean origemCompleta(Especie e, int nivel) {
		return porNivel(e, nivel).containsAll(e.originais());
	}

	/** Equipamento inicial: os golpes de origem já aprendidos, na ordem de origem (Concentração incluída). */
	public List<Golpe> equipamentoInicial(Especie e, int nivel) {
		List<Golpe> aprendidos = porNivel(e, nivel);
		return e.originais().stream().filter(aprendidos::contains).toList();
	}

	/**
	 * Valida um equipamento: 1 a 5 golpes distintos, com a Concentração, todos aprendidos (por nível ou treinamento
	 * concluído); fora os de origem, só depois da origem completa.
	 */
	public void validarEquipamento(Especie e, int nivel, List<Golpe> equipados, List<Golpe> treinados) {
		if (equipados.isEmpty() || equipados.size() > MAXIMO_EQUIPADOS || equipados.stream().distinct().count() != equipados.size())
			throw new IllegalArgumentException("De 1 a 5 golpes distintos");
		if (equipados.stream().noneMatch(Golpe::concentracao))
			throw new IllegalArgumentException("A Concentração é fixa entre os equipados");
		List<Golpe> aprendidos = new ArrayList<>(porNivel(e, nivel));
		aprendidos.addAll(treinados);
		for (Golpe g : equipados)
			if (!aprendidos.contains(g))
				throw new IllegalArgumentException(g.nome() + " ainda não foi aprendido");
		if (!origemCompleta(e, nivel) && !e.originais().containsAll(equipados))
			throw new IllegalArgumentException("Os slots só ficam livres depois dos 5 golpes de origem");
	}

	/** Marcos por nível de uma espécie (nível → golpe), para exibição. */
	public Map<Integer, List<String>> marcos(Especie e) {
		Map<Integer, List<String>> m = new LinkedHashMap<>();
		for (Entrada x : tabela(e))
			if (x.porNivel())
				m.computeIfAbsent(x.nivel(), k -> new ArrayList<>()).add(x.golpe().nome());
		return m;
	}
}
