package br.galetocraft.nucleo.rinha;

import br.galetocraft.nucleo.regras.Experiencia;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Liquidação da XP no fim de uma Rinha vencida (regra experiencia, v1260):
 * <ul>
 * <li>só a equipe vencedora recebe; derrota, fuga, abandono e captura não dão XP;</li>
 * <li>cada oponente derrotado conta uma vez: {@code floor((25 + 15·L) × M_raridade × C_desafio × M_modo)}, com
 * {@code P} = maior nível entre os Galetos da equipe vencedora que entraram em campo;</li>
 * <li>a soma é repartida entre os Galetos distintos que entraram em campo (mesmo sem golpear), por quociente
 * inteiro, e o resto vai de 1 em 1 na ordem da primeira entrada; quem ficou só na reserva não recebe.</li>
 * </ul>
 */
public final class Premiacao {
	public static final String PVE_SELVAGEM = "PvE_selvagem", PVP_VALIDO = "PvP_valido";

	private Premiacao() {
	}

	/**
	 * XP de cada participante da equipe vencedora (índice na equipe → XP), na ordem da primeira entrada.
	 * Vazio se a Rinha não terminou com vitória dessa equipe (ou terminou em captura).
	 */
	public static Map<Integer, Long> liquidar(Rinha r, Equipe vencedora, Experiencia regras, String modo) {
		Map<Integer, Long> xp = new LinkedHashMap<>();
		if (r.capturado() || r.vencedor().orElse(null) != vencedora)
			return xp;
		Equipe perdedora = vencedora == r.equipeA() ? r.equipeB() : r.equipeA();
		List<Integer> participantes = vencedora.participantes();
		int maiorNivel = participantes.stream().mapToInt(i -> vencedora.galetos().get(i).nivel()).max().orElseThrow();
		long total = 0;
		for (Combatente op : perdedora.galetos())
			if (op.derrotado())
				total += regras.recompensa(op.nivel(), op.especie().raridade(), maiorNivel, modo);
		long[] parcelas = Experiencia.repartir(total, participantes.size());
		for (int k = 0; k < participantes.size(); k++)
			xp.put(participantes.get(k), parcelas[k]);
		return xp;
	}
}
