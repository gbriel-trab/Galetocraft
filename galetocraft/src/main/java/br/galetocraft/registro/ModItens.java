package br.galetocraft.registro;

import br.galetocraft.GaletocraftMod;
import br.galetocraft.entidade.GaloEntity;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.function.Function;
import net.minecraft.core.Registry;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.SpawnEggItem;

/** Registro dos itens do Galetocraft. */
public final class ModItens {
	/** Ovos geradores das espécies ("&lt;id&gt;_spawn_egg"), na ordem de {@link ModEntidades#GALOS}. */
	public static final List<Item> OVOS_GALOS;

	static {
		final List<Item> ovos = new ArrayList<>();

		for (EntityType<GaloEntity> tipo : ModEntidades.GALOS) {
			ovos.add(registrar(ModEntidades.id(tipo) + "_spawn_egg", SpawnEggItem::new, new Item.Properties().spawnEgg(tipo)));
		}

		OVOS_GALOS = Collections.unmodifiableList(ovos);
	}

	private static <T extends Item> T registrar(String nome, Function<Item.Properties, T> fabrica, Item.Properties propriedades) {
		ResourceKey<Item> chave = ResourceKey.create(Registries.ITEM, GaletocraftMod.id(nome));
		T item = fabrica.apply(propriedades.setId(chave));
		Registry.register(BuiltInRegistries.ITEM, chave, item);
		return item;
	}

	public static void registrar() {}

	private ModItens() {}
}
