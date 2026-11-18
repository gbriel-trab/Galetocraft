package br.galetocraft.rinha;

import br.galetocraft.nucleo.dados.Especie;
import br.galetocraft.nucleo.dados.Galetario;
import net.minecraft.server.level.ServerPlayer;

import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Equipe de teste do jogador para as Rinhas, enquanto a captura e a equipe persistente do treinador não existem.
 * Fica só na memória do servidor. O padrão é o trio de iniciais Pirococó, Cocórrego e Esporocó.
 */
public final class EquipesTemporarias {
	private static final Map<UUID, List<Integer>> EQUIPES = new ConcurrentHashMap<>();
	private static final List<Integer> PADRAO = List.of(1, 2, 3);

	private EquipesTemporarias() {
	}

	public static void definir(ServerPlayer p, List<Especie> especies) {
		if (especies.isEmpty() || especies.size() > 3)
			throw new IllegalArgumentException("A equipe tem de 1 a 3 Galetos");
		EQUIPES.put(p.getUUID(), especies.stream().map(Especie::numero).toList());
	}

	public static List<Especie> equipe(ServerPlayer p) {
		Galetario g = Galetario.padrao();
		return EQUIPES.getOrDefault(p.getUUID(), PADRAO).stream().map(g::especie).toList();
	}
}
