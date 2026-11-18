package br.galetocraft.registro;

import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import br.galetocraft.GaletocraftMod;
import br.galetocraft.entidade.GaloEntity;
import br.galetocraft.entidade.PirococoEntity;
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

	/** #001 Pirococó: o galo-fênix das chamas (~2,45 blocos de altura, bem mais alto que um jogador; imune a fogo). */
	public static final EntityType<PirococoEntity> PIROCOCO = registrar("pirococo",
			EntityType.Builder.of(PirococoEntity::new, MobCategory.CREATURE)
					.sized(1.2f, 2.8f)
					.fireImmune());

	// Espécies com modelo próprio e comportamento de galo genérico (GaloEntity).
	// galo(id, largura e altura da caixa de colisão (altura = tabela oficial em ferramentas/dimensoes.py; largura = 0,6 × o menor lado), imune a fogo, vida, velocidade, dano)
	/** #003 Esporocó, a galoa das plantas tóxicas. */
	public static final EntityType<GaloEntity> ESPOROCO = galo("esporoco", 0.93f, 1.75f, false, 36, 0.26, 4);
	/** #004 Cocórak, o galo colossal das areias (~3 blocos). */
	public static final EntityType<GaloEntity> COCORAK = galo("cocorak", 1.65f, 3.0f, false, 60, 0.22, 9);
	/** #005 Cocórion, o galo dos ventos. */
	public static final EntityType<GaloEntity> COCORION = galo("cocorion", 0.9f, 2.4f, false, 36, 0.30, 8);
	/** #006 Cocórvolt, o senhor da tempestade. */
	public static final EntityType<GaloEntity> COCORVOLT = galo("cocorvolt", 1.41f, 2.6f, false, 34, 0.30, 5);
	/** #007 Taturico, o galo-tatu das rochas. */
	public static final EntityType<GaloEntity> TATURICO = galo("taturico", 0.75f, 1.2f, false, 50, 0.23, 5);
	/** #008 Axococó, o galo-axolote das águas. */
	public static final EntityType<GaloEntity> AXOCOCO = galo("axococo", 0.72f, 1.15f, false, 38, 0.26, 4);
	/** #009 Vagaló, o galo-vaga-lume veloz. */
	public static final EntityType<GaloEntity> VAGALO = galo("vagalo", 0.66f, 1.0f, false, 30, 0.33, 4);
	/** #010 Morcegalo, o galo-morcego das sombras. */
	public static final EntityType<GaloEntity> MORCEGALO = galo("morcegalo", 0.78f, 1.2f, false, 34, 0.29, 6);
	/** #011 Espinhocó, o galo-espinho da floresta. */
	public static final EntityType<GaloEntity> ESPINHOCO = galo("espinhoco", 0.78f, 1.25f, false, 44, 0.24, 5);
	/** #012 Salambrasa, o galo-salamandra das brasas (anda em 4 patas; imune a fogo). */
	public static final EntityType<GaloEntity> SALAMBRASA = galo("salambrasa", 0.6f, 1.1f, true, 42, 0.26, 7);
	/** #019 Renacocó, o curandeiro da ressurreição (mítico, suporte; altura provisória 2,5; imune a fogo). */
	public static final EntityType<GaloEntity> RENACOCO = galo("renacoco", 0.96f, 2.5f, true, 40, 0.28, 4);

	/** Todas as espécies que usam {@link GaloEntity}, na ordem do Galetário. */
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

	/** Id da espécie ("esporoco", "cocorak"...). */
	public static String id(EntityType<?> tipo) {
		return BuiltInRegistries.ENTITY_TYPE.getKey(tipo).getPath();
	}

	public static void registrar() {
		FabricDefaultAttributeRegistry.register(PIROCOCO, PirococoEntity.criarAtributos());
		ATRIBUTOS.forEach(FabricDefaultAttributeRegistry::register);
	}

	private ModEntidades() {}
}
