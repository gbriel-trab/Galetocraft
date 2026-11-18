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
		// tempestade de areia: partícula de areia, intensidade, poeira e vento (a névoa fica no NevoaAtmosfericaMixin)
		net.fabricmc.fabric.api.client.particle.v1.ParticleFactoryRegistry.getInstance().register(
				br.galetocraft.mundo.TempestadeDeAreia.PARTICULA_AREIA, br.galetocraft.client.tempestade.AreiaParticula.Provider::new);
		net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents.END_CLIENT_TICK.register(br.galetocraft.client.tempestade.TempestadeCliente::tick);

		EntityRenderers.register(ModEntidades.PIROCOCO, PirococoRenderer::new);

		for (EntityType<GaloEntity> tipo : ModEntidades.GALOS) {
			final String id = ModEntidades.id(tipo);
			final float sombra = Math.max(0.4f, tipo.getWidth() * 0.8f);
			// cauda comprida (Salambrasa) ou enorme (Cocórak): mais folga para não sumir na borda da tela
			final double folga = switch (id) {
				case "salambrasa" -> 1.4;
				case "cocorak" -> 1.0;
				default -> 0.7;
			};

			EntityRenderers.register(tipo, contexto -> new GaloRenderer<>(contexto, id, sombra, folga));
		}
	}
}
