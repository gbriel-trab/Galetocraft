package br.galetocraft.captura;

import net.minecraft.ChatFormatting;
import net.minecraft.core.component.DataComponents;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.component.CustomData;
import net.minecraft.world.item.component.TooltipDisplay;
import net.minecraft.world.level.Level;

import java.util.function.Consumer;

/**
 * Pena de Captura: o único instrumento de captura do treinador, uma pena com rubi no centro (regra captura.pena_rev9).
 * <ul>
 * <li>Vem no kit de início de jornada; não é consumida nem arremessada; não tem receita.</li>
 * <li>Tem dono: só funciona com o treinador que a recebeu e na versão atual (uma Pena nova invalida as anteriores).</li>
 * <li>Não fica no chão: se cair ou for jogada, some e volta ao dono ao entrar no mundo, renascer ou acordar.</li>
 * <li>O nível e a XP ficam com o treinador; a Pena só guarda o nível para a dica.</li>
 * </ul>
 * A arte é provisória (pena vanilla) até a imagem ser gerada e aprovada.
 */
public class PenaDeCapturaItem extends Item {
	public static final String DONO = "galeto_dono", DONO_NOME = "galeto_dono_nome", VERSAO = "galeto_versao", NIVEL = "galeto_nivel";

	public PenaDeCapturaItem(Properties propriedades) {
		super(propriedades);
	}

	static CompoundTag dados(ServerPlayer p, int versao, int nivel) {
		CompoundTag d = new CompoundTag();
		d.putString(DONO, p.getUUID().toString());
		d.putString(DONO_NOME, p.getName().getString());
		d.putInt(VERSAO, versao);
		d.putInt(NIVEL, nivel);
		return d;
	}

	@Override
	public InteractionResult use(Level mundo, Player jogador, InteractionHand mao) {
		if (jogador instanceof ServerPlayer p) {
			ItemStack s = p.getItemInHand(mao);
			if (Capturas.penaValida(p, s))
				Capturas.tentarNoMundo(p);
			else
				p.displayClientMessage(Component.literal(donoDe(s).equals(p.getUUID().toString())
						? "Esta Pena de Captura foi substituída por uma nova e não funciona mais."
						: "Esta Pena de Captura pertence a " + nomeDoDono(s) + ".").withStyle(ChatFormatting.YELLOW), false);
		}
		return InteractionResult.SUCCESS;
	}

	@Override
	public void appendHoverText(ItemStack s, TooltipContext contexto, TooltipDisplay exibicao, Consumer<Component> linhas, TooltipFlag flag) {
		CompoundTag d = s.getOrDefault(DataComponents.CUSTOM_DATA, CustomData.EMPTY).copyTag();
		if (!d.contains(DONO))
			return;
		linhas.accept(Component.literal("Nível " + d.getIntOr(NIVEL, 1)).withStyle(ChatFormatting.LIGHT_PURPLE));
		linhas.accept(Component.literal("Treinador: " + d.getStringOr(DONO_NOME, "?")).withStyle(ChatFormatting.GRAY));
	}

	private static String donoDe(ItemStack s) {
		return s.getOrDefault(DataComponents.CUSTOM_DATA, CustomData.EMPTY).copyTag().getStringOr(DONO, "");
	}

	private static String nomeDoDono(ItemStack s) {
		return s.getOrDefault(DataComponents.CUSTOM_DATA, CustomData.EMPTY).copyTag().getStringOr(DONO_NOME, "outro treinador");
	}
}
