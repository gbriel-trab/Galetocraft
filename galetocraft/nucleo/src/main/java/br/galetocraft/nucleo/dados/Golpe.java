package br.galetocraft.nucleo.dados;

import com.google.gson.JsonObject;

/**
 * Um golpe do repertório de uma espécie, como está na base vigente.
 *
 * @param poder        poder base; {@code null} em suportes e em golpes de poder especial (ver {@code poderTexto})
 * @param poderTexto   poder fora do padrão, como "40 × 1–5" (Cerco das Pinças, sequencial)
 * @param energia      custo de Energia
 * @param efeito       texto oficial do efeito
 * @param estadoAplicado estado negativo aplicado após dano, quando a ficha define um (com {@code chanceEstado})
 * @param efeitoEstruturado efeito estruturado da ficha original protegida, quando existe
 */
public record Golpe(String grupo, int posicao, String nome, String id, Elemento elemento, Categoria categoria,
		Integer poder, String poderTexto, int energia, String efeito, EstadoNegativo estadoAplicado,
		double chanceEstado, JsonObject efeitoEstruturado) {

	public boolean original() {
		return "original".equals(grupo);
	}

	public boolean danoDireto() {
		return categoria.danoDireto() && poder != null;
	}

	public boolean concentracao() {
		return "concentracao".equals(id) || "Concentração".equals(nome);
	}
}
