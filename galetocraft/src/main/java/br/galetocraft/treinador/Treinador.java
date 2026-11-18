package br.galetocraft.treinador;

import br.galetocraft.nucleo.dados.Galetario;
import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;

import java.util.ArrayList;
import java.util.List;

/**
 * Dados do treinador salvos com o jogador (regra treinador): equipe principal de até 5 Cocorídeos, reservas sem
 * limite e a XP acumulada da sua única Pena de Captura.
 * <p>
 * Toda captura entra na equipe principal se houver vaga; senão vai para as reservas. Nenhum Cocorídeo é perdido por
 * falta de espaço. As operações de gerenciamento (guardar, chamar, pôr em primeiro) são provisórias: a regra ainda
 * não define o procedimento de troca entre equipe e reservas.
 */
public record Treinador(int penaXp, List<GaletoGuardado> equipe, List<GaletoGuardado> reservas) {
	public static final Codec<Treinador> CODEC = RecordCodecBuilder.create(i -> i.group(
			Codec.INT.optionalFieldOf("pena_xp", 0).forGetter(Treinador::penaXp),
			GaletoGuardado.CODEC.listOf().optionalFieldOf("equipe", List.of()).forGetter(Treinador::equipe),
			GaletoGuardado.CODEC.listOf().optionalFieldOf("reservas", List.of()).forGetter(Treinador::reservas)
	).apply(i, Treinador::new));

	public static final Treinador NOVO = new Treinador(0, List.of(), List.of());

	/** Capacidade da equipe principal, da regra treinador da base (5). */
	public static final int EQUIPE_MAXIMA = Galetario.padrao().regraObjeto("treinador")
			.getAsJsonObject("equipe_principal").get("capacidade_maxima_cocorideos").getAsInt();

	public Treinador {
		equipe = List.copyOf(equipe);
		reservas = List.copyOf(reservas);
	}

	public boolean equipeCheia() {
		return equipe.size() >= EQUIPE_MAXIMA;
	}

	/** Recebe um Cocorídeo capturado: equipe principal se houver vaga, senão reservas. */
	public Treinador comCapturado(GaletoGuardado g) {
		return equipeCheia() ? new Treinador(penaXp, equipe, mais(reservas, g)) : new Treinador(penaXp, mais(equipe, g), reservas);
	}

	public Treinador comPenaXp(int xp) {
		return new Treinador(xp, equipe, reservas);
	}

	/** Move o Galeto da equipe para as reservas. */
	public Treinador guardar(int i) {
		List<GaletoGuardado> e = new ArrayList<>(equipe);
		GaletoGuardado g = e.remove(i);
		return new Treinador(penaXp, e, mais(reservas, g));
	}

	/** Move o Galeto das reservas para a equipe, se houver vaga. */
	public Treinador chamar(int i) {
		if (equipeCheia())
			throw new IllegalStateException("A equipe principal já tem " + EQUIPE_MAXIMA + " Cocorídeos");
		List<GaletoGuardado> r = new ArrayList<>(reservas);
		GaletoGuardado g = r.remove(i);
		return new Treinador(penaXp, mais(equipe, g), r);
	}

	/** Põe o Galeto na primeira posição da equipe (os três primeiros vão para a Rinha). */
	public Treinador primeiro(int i) {
		List<GaletoGuardado> e = new ArrayList<>(equipe);
		e.add(0, e.remove(i));
		return new Treinador(penaXp, e, reservas);
	}

	/** Aplica uma mudança ao Galeto com esse id, onde ele estiver (equipe ou reservas). */
	public Treinador atualizar(java.util.UUID id, java.util.function.UnaryOperator<GaletoGuardado> f) {
		return new Treinador(penaXp, equipe.stream().map(g -> g.id().equals(id) ? f.apply(g) : g).toList(),
				reservas.stream().map(g -> g.id().equals(id) ? f.apply(g) : g).toList());
	}

	private static List<GaletoGuardado> mais(List<GaletoGuardado> lista, GaletoGuardado g) {
		List<GaletoGuardado> l = new ArrayList<>(lista);
		l.add(g);
		return l;
	}
}
