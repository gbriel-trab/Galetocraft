package br.galetocraft.nucleo.rinha;

import br.galetocraft.nucleo.dados.Golpe;
import br.galetocraft.nucleo.regras.MiraAnatomica;
import br.galetocraft.nucleo.regras.PenaDeRitmo;

import java.util.Comparator;
import java.util.SplittableRandom;

/**
 * IA simples para testes, simulações e Galetos selvagens. Não é regra oficial do jogo: a IA dos Mestres tem
 * especificação própria.
 * <p>
 * Usa o golpe de dano pagável com maior dano esperado ({@code poder × eficácia × (A/D)^0,7}). Sem golpe pagável,
 * ou com pouca Energia, usa a Concentração. Mira no tronco (precisão 100%), guarda uma região ao acaso e usa o
 * Canto Ofensivo quando tem a Pena de Ritmo.
 */
public final class IaBasica {
	private final SplittableRandom rng;

	public IaBasica(long semente) {
		this.rng = new SplittableRandom(semente);
	}

	public Decisao decidir(Rinha rinha, Equipe eu, Equipe oponente) {
		Combatente c = eu.ativo();
		Combatente alvo = oponente.ativo();
		Golpe concentracao = c.golpes().stream().filter(Golpe::concentracao).findFirst().orElseThrow();
		Golpe melhor = rinha.golpesValidos(eu).stream().filter(Golpe::danoDireto)
				.max(Comparator.comparingDouble(g -> esperado(rinha, c, alvo, g))).orElse(null);
		MiraAnatomica.Regiao guarda = rng.nextDouble() < 0.5 ? null
				: MiraAnatomica.Regiao.values()[rng.nextInt(MiraAnatomica.Regiao.values().length)];
		if (melhor == null || (c.energia() < 40 && rng.nextDouble() < 0.35))
			return new Decisao(new Decisao.UsarGolpe(concentracao, null, null), guarda);
		PenaDeRitmo.Canto canto = eu.pena().disponivel() ? PenaDeRitmo.Canto.OFENSIVO : null;
		return new Decisao(new Decisao.UsarGolpe(melhor, MiraAnatomica.Regiao.TRONCO, canto), guarda);
	}

	private static double esperado(Rinha rinha, Combatente c, Combatente alvo, Golpe g) {
		double razao = c.atributo(g.categoria().ataque()) / Math.max(1, alvo.atributo(g.categoria().defesa()));
		return g.poder() * rinha.eficacia().multiplicador(g.elemento(), alvo.especie().elementos()) * Math.pow(razao, 0.7);
	}
}
