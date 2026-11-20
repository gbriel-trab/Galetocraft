package br.galetocraft.registro;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import br.galetocraft.GaletocraftMod;
import br.galetocraft.entidade.GaloEntity;
import net.fabricmc.fabric.api.object.builder.v1.entity.FabricDefaultAttributeRegistry;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;

/** Registro das criaturas do Galetocraft. */
public final class ModEntidades {
	private static final Map<EntityType<GaloEntity>, AttributeSupplier.Builder> ATRIBUTOS = new LinkedHashMap<>();
	private static final List<EntityType<GaloEntity>> LISTA = new ArrayList<>();

	// Nenhuma espécie registrada por enquanto: os 12 modelos antigos saíram do jogo em 20/11/2026, a pedido do dono,
	// para dar lugar aos modelos novos. Cada espécie entra aqui com uma linha:
	// galo(id, largura e altura da caixa de colisão (altura = tabela oficial em ferramentas/dimensoes.py; largura = 0,6 × o menor lado), imune a fogo, vida, velocidade, dano)

	/** Todas as espécies do jogo, na ordem da RoosterTeca. */
	public static final List<EntityType<GaloEntity>> GALOS = Collections.unmodifiableList(LISTA);

	private static EntityType<GaloEntity> galo(String nome, float largura, float altura, boolean imuneAFogo,
			double vida, double velocidade, double dano) {
		EntityType.Builder<GaloEntity> builder = EntityType.Builder.of(GaloEntity::new, MobCategory.CREATURE)
				.sized(largura, altura);

		if (imuneAFogo)
			builder = builder.fireImmune();

		final EntityType<GaloEntity> tipo = registrar(nome, builder);
		ATRIBUTOS.put(tipo, GaloEntity.criarAtributos(vida, velocidade, dano));
		LISTA.add(tipo);
		return tipo;
	}

	private static <T extends Entity> EntityType<T> registrar(String nome, EntityType.Builder<T> builder) {
		ResourceKey<EntityType<?>> chave = ResourceKey.create(Registries.ENTITY_TYPE, GaletocraftMod.id(nome));
		return Registry.register(BuiltInRegistries.ENTITY_TYPE, chave, builder.build(chave));
	}

	/** Id da espécie (o caminho do tipo: galetocraft:&lt;id&gt;). */
	public static String id(EntityType<?> tipo) {
		return BuiltInRegistries.ENTITY_TYPE.getKey(tipo).getPath();
	}

	public static void registrar() {
		ATRIBUTOS.forEach(FabricDefaultAttributeRegistry::register);
	}

	private ModEntidades() {}
}
