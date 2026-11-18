package br.galetocraft.client;

import br.galetocraft.entidade.PirococoEntity;
import net.minecraft.client.renderer.entity.EntityRendererProvider;

/**
 * Desenha o Pirococó: o mesmo {@link GaloRenderer} das outras espécies (modelo do GeckoLib, brilho só nas chamas e
 * gemas, LOD de longe). O modelo passa da hitbox (plumas da cauda até ~1,6 bloco para trás e para os lados), por isso
 * a folga de 1 bloco na caixa usada para decidir se ele está na tela.
 */
public class PirococoRenderer extends GaloRenderer<PirococoEntity> {
	public PirococoRenderer(EntityRendererProvider.Context contexto) {
		super(contexto, "pirococo", 0.9f, 1.0);
	}
}
