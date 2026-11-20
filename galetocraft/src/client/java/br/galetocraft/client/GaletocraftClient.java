package br.galetocraft.client;

import br.galetocraft.entidade.GaloEntity;
import br.galetocraft.registro.ModEntidades;
import net.fabricmc.api.ClientModInitializer;
import net.minecraft.client.renderer.entity.EntityRenderers;
import net.minecraft.world.entity.EntityType;

/** Ponto de entrada do lado do cliente: registra como as criaturas são desenhadas. */
public class GaletocraftClient implements ClientModInitializer {
	@Override
	public void onInitializeClient() {
		for (EntityType<GaloEntity> tipo : ModEntidades.GALOS) {
			final String id = ModEntidades.id(tipo);
			final float sombra = Math.max(0.4f, tipo.getWidth() * 0.8f);
			// quanto o modelo passa da caixa de colisão (asas, cauda); espécies de cauda comprida ou enormes pedem mais
			final double folga = 0.7;

			EntityRenderers.register(tipo, contexto -> new GaloRenderer<>(contexto, id, sombra, folga));
		}
	}
}
