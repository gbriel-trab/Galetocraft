package br.galetocraft;

import br.galetocraft.registro.ModEntidades;
import br.galetocraft.registro.ModItens;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.itemgroup.v1.ItemGroupEvents;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.CreativeModeTabs;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/** Ponto de entrada do mod (lado comum: servidor e cliente). */
public class GaletocraftMod implements ModInitializer {
	public static final String MOD_ID = "galetocraft";
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	public static Identifier id(String caminho) {
		return Identifier.fromNamespaceAndPath(MOD_ID, caminho);
	}

	@Override
	public void onInitialize() {
		ModEntidades.registrar();
		ModItens.registrar();

		// os ovos dos galos aparecem na aba de ovos geradores do modo criativo
		ItemGroupEvents.modifyEntriesEvent(CreativeModeTabs.SPAWN_EGGS)
				.register(entradas -> {
					entradas.accept(ModItens.OVO_PIROCOCO);
					ModItens.OVOS_GALOS.forEach(entradas::accept);
				});

		LOGGER.info("Galetocraft carregado: {} galos prontos!", 1 + ModEntidades.GALOS.size());
	}
}
