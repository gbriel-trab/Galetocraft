package br.galetocraft.treinador;

import br.galetocraft.nucleo.dados.Atributo;
import br.galetocraft.nucleo.dados.Especie;
import br.galetocraft.nucleo.dados.Galetario;
import br.galetocraft.nucleo.regras.Experiencia;
import br.galetocraft.nucleo.regras.Progressao;
import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.core.UUIDUtil;

import java.util.List;
import java.util.UUID;

/**
 * Galeto que pertence a um treinador (equipe principal ou reserva), fora do mundo.
 * Guarda os mesmos dados individuais da entidade: espécie, nível, sexo e os 6 IVs.
 */
public record GaletoGuardado(UUID id, int especie, int nivel, String sexo, List<Integer> ivs, long xp) {
	public static final Codec<GaletoGuardado> CODEC = RecordCodecBuilder.create(i -> i.group(
			UUIDUtil.CODEC.fieldOf("id").forGetter(GaletoGuardado::id),
			Codec.INT.fieldOf("especie").forGetter(GaletoGuardado::especie),
			Codec.INT.fieldOf("nivel").forGetter(GaletoGuardado::nivel),
			Codec.STRING.fieldOf("sexo").forGetter(GaletoGuardado::sexo),
			Codec.INT.listOf().fieldOf("ivs").forGetter(GaletoGuardado::ivs),
			Codec.LONG.optionalFieldOf("xp", -1L).forGetter(GaletoGuardado::xp)
	).apply(i, GaletoGuardado::new));

	/**
	 * @param xp XP total acumulada; negativa = {@code T(nível)}, o início de um Cocorídeo capturado (sem XP extra)
	 */
	public GaletoGuardado {
		ivs = List.copyOf(ivs);
		if (xp < 0)
			xp = Experiencia.xpTotal(nivel);
	}

	/**
	 * Soma a XP de uma Rinha vencida e sobe de nível pela curva {@code T(N) = (N−1)³ + 10(N−1)²}.
	 * No nível 100 não entra XP nova.
	 */
	public GaletoGuardado comXp(long ganho) {
		if (nivel >= Experiencia.NIVEL_MAXIMO || ganho <= 0)
			return this;
		long total = xp + ganho;
		int novoNivel = Math.max(nivel, Math.min(Experiencia.NIVEL_MAXIMO, Experiencia.nivelPorXp(total)));
		return new GaletoGuardado(id, especie, novoNivel, sexo, ivs, total);
	}

	public Especie ficha() {
		return Galetario.padrao().especie(especie);
	}

	/** Linha de resumo: "#007 Taturico ♀ Nv50 · HP 85 · XP 120050 · IVs [..]". */
	public String resumo() {
		Especie e = ficha();
		String simbolo = switch (sexo) {
			case "M" -> " ♂";
			case "F" -> " ♀";
			default -> "";
		};
		String prox = nivel >= Experiencia.NIVEL_MAXIMO ? "máx." : "faltam " + (Experiencia.xpTotal(nivel + 1) - xp);
		return String.format("#%03d %s%s Nv%d · HP %d · XP %d (%s) · IVs %s", e.numero(), e.nome(), simbolo, nivel,
				Progressao.hpMaximoProvisorio(e.atributo(Atributo.HP), nivel), xp, prox, ivs);
	}
}
