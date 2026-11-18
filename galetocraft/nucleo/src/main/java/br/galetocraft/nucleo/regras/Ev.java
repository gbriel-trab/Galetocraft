package br.galetocraft.nucleo.regras;

import br.galetocraft.nucleo.dados.Atributo;
import br.galetocraft.nucleo.dados.Especie;

/**
 * Ganho de EV (regra progressao, ev_rev9 — aprovada em 18/11/2026).
 * <ul>
 * <li>Faixas: o custo dobra a cada {@code 0,5 × total-base} da espécie no nível 50; o EV efetivo de um ganho é
 * {@code ganho / 2^floor(EV_total / limiar)}, dividindo o ganho através das fronteiras (estrutura da V1.2).</li>
 * <li>Combate: cada Galeto que entrou em campo numa Rinha vencida ganha +0,1 EV por oponente derrotado, no atributo-base
 * mais alto do oponente (empate pela ordem HP, Atq. Físico, Def. Física, Atq. Mágico, Def. Mágica, Velocidade).</li>
 * </ul>
 */
public final class Ev {
	public static final double GANHO_COMBATE = 0.1;

	private Ev() {
	}

	public static double limiar(Especie e) {
		return 0.5 * e.total();
	}

	/** EV efetivo somado ao Galeto por um ganho-base, dado o EV total que ele já tem (soma dos 6 atributos). */
	public static double efetivo(Especie e, double evTotal, double ganhoBase) {
		double limiar = limiar(e), total = evTotal, ganho = ganhoBase, somado = 0;
		while (ganho > 1e-12) {
			int faixa = (int) Math.floor(total / limiar + 1e-12);
			double mult = Math.pow(2, faixa);
			double cabe = (faixa + 1) * limiar - total;          // EV efetivo que ainda cabe nesta faixa
			double aqui = ganho / mult;
			if (aqui <= cabe + 1e-12) {
				somado += aqui;
				break;
			}
			somado += cabe;
			total += cabe;
			ganho -= cabe * mult;
		}
		return somado;
	}

	/** Atributo-base mais alto da espécie (empate pela ordem dos atributos). */
	public static Atributo atributoMaisAlto(Especie e) {
		Atributo melhor = Atributo.HP;
		for (Atributo a : Atributo.values())
			if (e.atributo(a) > e.atributo(melhor))
				melhor = a;
		return melhor;
	}
}
