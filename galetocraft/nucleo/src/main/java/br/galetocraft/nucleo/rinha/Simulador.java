package br.galetocraft.nucleo.rinha;

import br.galetocraft.nucleo.dados.Especie;
import br.galetocraft.nucleo.dados.Galetario;

import java.util.List;
import java.util.function.Function;

/**
 * Roda Rinhas completas entre duas equipes controladas pela {@link IaBasica}. Serve para testar o motor e medir
 * tendências de balanceamento. Não substitui testes com jogadores, e os resultados dependem do que o motor ainda
 * não implementa (passivas e efeitos especiais).
 */
public final class Simulador {

	public record Resultado(int vitoriasA, int vitoriasB, int empates, double mediaRodadas) {
		public int total() { return vitoriasA + vitoriasB + empates; }

		public double taxaA() { return total() == 0 ? 0 : (double) vitoriasA / total(); }
	}

	private Simulador() {
	}

	/** Uma Rinha com a IA básica nos dois lados. */
	public static Rinha rodar(Galetario g, Equipe a, Equipe b, long semente) {
		Rinha r = new Rinha(g, a, b, semente);
		IaBasica iaA = new IaBasica(semente * 31 + 1), iaB = new IaBasica(semente * 31 + 2);
		while (!r.terminada())
			r.rodada(iaA.decidir(r, a, b), iaB.decidir(r, b, a));
		return r;
	}

	/** N Rinhas 1×1 entre duas espécies no mesmo nível, com os 5 golpes de origem. */
	public static Resultado duelo(Galetario g, Especie x, Especie y, int nivel, int rinhas, long semente) {
		return confrontos(g, s -> new Equipe(x.nome(), List.of(Combatente.padrao(x, nivel))),
				s -> new Equipe(y.nome(), List.of(Combatente.padrao(y, nivel))), rinhas, semente);
	}

	public static Resultado confrontos(Galetario g, Function<Long, Equipe> fabricaA, Function<Long, Equipe> fabricaB, int rinhas, long semente) {
		int va = 0, vb = 0, emp = 0;
		long somaRodadas = 0;
		for (int i = 0; i < rinhas; i++) {
			long s = semente + i;
			Equipe a = fabricaA.apply(s), b = fabricaB.apply(s);
			Rinha r = rodar(g, a, b, s);
			somaRodadas += r.rodada();
			if (r.vencedor().isEmpty()) emp++;
			else if (r.vencedor().get() == a) va++;
			else vb++;
		}
		return new Resultado(va, vb, emp, rinhas == 0 ? 0 : (double) somaRodadas / rinhas);
	}
}
