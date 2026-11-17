package br.galetocraft.client;

import br.galetocraft.entidade.PirococoEntity;
import net.minecraft.client.renderer.entity.EntityRendererProvider;

/**
 * Desenha o Pirococó: o mesmo {@link GaloRenderer} das outras espécies (modelo do GeckoLib, brilho só nas chamas e
 * gemas, LOD de longe). O modelo passa da hitbox (asas para os lados, correntes até ~1,4 bloco para trás), por isso a
 * folga de 0,5 bloco na caixa usada para decidir se ele está na tela.
 */
public class PirococoRenderer extends GaloRenderer<PirococoEntity> {
	public PirococoRenderer(EntityRendererProvider.Context contexto) {
		super(contexto, "pirococo", 0.9f, 0.5);
	}
}
