package br.galetocraft.captura;

import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.level.Level;

/**
 * Pena de Captura: o único instrumento de captura do treinador, uma pena com rubi no centro. Não é consumida nem
 * arremessada. O nível (1–5) e a XP ficam com o treinador, não com o item.
 * <p>
 * Ainda não definidos pelo criador: como o treinador recebe ou recupera a Pena, receita, aparência final.
 * Por enquanto ela vem pelo comando {@code /galetocraft pena} ou pelo modo criativo, com a pena vanilla como
 * desenho provisório.
 */
public class PenaDeCapturaItem extends Item {
	public PenaDeCapturaItem(Properties propriedades) {
		super(propriedades);
	}

	@Override
	public InteractionResult use(Level mundo, Player jogador, InteractionHand mao) {
		if (jogador instanceof ServerPlayer p)
			Capturas.tentarNoMundo(p);
		return InteractionResult.SUCCESS;
	}
}
