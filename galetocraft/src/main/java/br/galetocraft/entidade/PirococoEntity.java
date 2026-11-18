package br.galetocraft.entidade;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.level.Level;

/**
 * #001 Pirococó, o galo-fênix das chamas.
 * Usa o comportamento, os dados individuais e as animações de {@link GaloEntity}
 * ("animation.pirococo.idle" e "animation.pirococo.walk"); tem classe própria por causa do renderizador e dos
 * números de mob no mundo. Imune a fogo pelo registro do tipo.
 */
public class PirococoEntity extends GaloEntity {

	public PirococoEntity(EntityType<? extends PirococoEntity> tipo, Level mundo) {
		super(tipo, mundo);
	}

	public static AttributeSupplier.Builder criarAtributos() {
		return GaloEntity.criarAtributos(40.0, 0.27, 6.0);
	}
}
