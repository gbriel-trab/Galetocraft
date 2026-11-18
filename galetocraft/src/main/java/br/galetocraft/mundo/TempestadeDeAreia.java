package br.galetocraft.mundo;

import br.galetocraft.GaletocraftMod;
import br.galetocraft.nucleo.dados.Galetario;
import net.fabricmc.fabric.api.particle.v1.FabricParticleTypes;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.Registry;
import net.minecraft.core.particles.SimpleParticleType;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.tags.TagKey;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.biome.Biome;

import java.util.ArrayList;
import java.util.List;

/**
 * Tempestade de areia no mundo (regra tempestade_de_areia, rev. 10 da base, pedida pelo criador em 18/11/2026).
 * <ul>
 * <li>Acontece quando chove ou troveja no mundo, nos desertos e badlands, ao ar livre.</li>
 * <li>Visual no cliente: poeira de areia soprada pelo vento, névoa amarelada e som de vento.</li>
 * <li>Jogo: a Rinha que começa dentro dela já começa com o clima Tempestade de Areia; o Cocórak fica 2× mais provável.</li>
 * </ul>
 */
public final class TempestadeDeAreia {
	/** Partícula de areia soprada (o desenho usa as texturas vanilla de poeira, tingidas de areia). */
	public static final SimpleParticleType PARTICULA_AREIA = Registry.register(BuiltInRegistries.PARTICLE_TYPE,
			GaletocraftMod.id("areia"), FabricParticleTypes.simple());

	private static final List<String> BIOMAS = new ArrayList<>();

	private TempestadeDeAreia() {
	}

	public static void registrar() {
		Galetario.padrao().regraObjeto("tempestade_de_areia").getAsJsonArray("biomas").forEach(b -> BIOMAS.add(b.getAsString()));
	}

	/** Bioma de tempestade de areia (deserto ou badlands), mesmo sem chuva. */
	public static boolean biomaDeAreia(Level l, BlockPos pos) {
		Holder<Biome> b = l.getBiome(pos);
		for (String id : BIOMAS)
			if (id.startsWith("c:") ? b.is(TagKey.create(Registries.BIOME, Identifier.parse(id)))
					: b.is(ResourceKey.create(Registries.BIOME, Identifier.parse(id))))
				return true;
		return false;
	}

	/** Há tempestade de areia nesta posição: chove no mundo, o bioma é de areia e o céu é visível. */
	public static boolean ativaEm(Level l, BlockPos pos) {
		return l.isRaining() && biomaDeAreia(l, pos) && l.canSeeSky(pos);
	}

	/** Direção do vento em radianos: muda a cada dia de jogo, igual para servidor e cliente. */
	public static double direcaoDoVento(Level l) {
		long dia = l.getDayTime() / 24000L;
		long h = dia * 0x9E3779B97F4A7C15L;
		return ((h >>> 11) % 3600) / 3600.0 * Math.PI * 2;
	}
}
