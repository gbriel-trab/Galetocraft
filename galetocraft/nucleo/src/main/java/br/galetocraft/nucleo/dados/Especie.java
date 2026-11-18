package br.galetocraft.nucleo.dados;

import java.util.List;
import java.util.Map;

/**
 * Ficha vigente de uma espécie do Galetário (atributos-base no nível 50).
 *
 * @param probabilidadeMacho {@code null} para quem não reproduz (Lendário Original)
 */
public record Especie(int numero, String nome, String raridade, List<Elemento> elementos, Map<Atributo, Integer> atributos,
		double pesoKg, String passiva, List<String> alas, Double probabilidadeMacho, String hereditario, List<Golpe> golpes) {

	public int atributo(Atributo a) {
		return atributos.get(a);
	}

	public int total() {
		return atributos.values().stream().mapToInt(Integer::intValue).sum();
	}

	public List<Golpe> originais() {
		return golpes.stream().filter(Golpe::original).toList();
	}

	public List<Golpe> aprendiveis() {
		return golpes.stream().filter(g -> !g.original()).toList();
	}

	public Golpe golpe(String nome) {
		return golpes.stream().filter(g -> g.nome().equalsIgnoreCase(nome)).findFirst()
				.orElseThrow(() -> new IllegalArgumentException(this.nome + " não tem o golpe " + nome));
	}

	public boolean reproduz() {
		return probabilidadeMacho != null;
	}
}
