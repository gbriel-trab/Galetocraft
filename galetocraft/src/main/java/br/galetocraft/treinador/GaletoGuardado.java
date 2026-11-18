package br.galetocraft.treinador;

import br.galetocraft.nucleo.dados.Atributo;
import br.galetocraft.nucleo.dados.Especie;
import br.galetocraft.nucleo.dados.Galetario;
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
public record GaletoGuardado(UUID id, int especie, int nivel, String sexo, List<Integer> ivs) {
	public static final Codec<GaletoGuardado> CODEC = RecordCodecBuilder.create(i -> i.group(
			UUIDUtil.CODEC.fieldOf("id").forGetter(GaletoGuardado::id),
			Codec.INT.fieldOf("especie").forGetter(GaletoGuardado::especie),
			Codec.INT.fieldOf("nivel").forGetter(GaletoGuardado::nivel),
			Codec.STRING.fieldOf("sexo").forGetter(GaletoGuardado::sexo),
			Codec.INT.listOf().fieldOf("ivs").forGetter(GaletoGuardado::ivs)
	).apply(i, GaletoGuardado::new));

	public GaletoGuardado {
		ivs = List.copyOf(ivs);
	}

	public Especie ficha() {
		return Galetario.padrao().especie(especie);
	}

	/** Linha de resumo: "#007 Taturico ♀ Nv50 · HP 85 · IVs [..]". */
	public String resumo() {
		Especie e = ficha();
		String simbolo = switch (sexo) {
			case "M" -> " ♂";
			case "F" -> " ♀";
			default -> "";
		};
		return String.format("#%03d %s%s Nv%d · HP %d · IVs %s", e.numero(), e.nome(), simbolo, nivel,
				Progressao.hpMaximoProvisorio(e.atributo(Atributo.HP), nivel), ivs);
	}
}
