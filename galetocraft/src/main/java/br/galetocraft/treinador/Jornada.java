package br.galetocraft.treinador;

import br.galetocraft.captura.Capturas;
import br.galetocraft.nucleo.dados.Especie;
import br.galetocraft.nucleo.dados.Galetario;
import br.galetocraft.registro.ModAnexos;
import br.galetocraft.registro.ModItens;
import net.fabricmc.fabric.api.entity.event.v1.EntitySleepEvents;
import net.fabricmc.fabric.api.entity.event.v1.ServerPlayerEvents;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerEntityEvents;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.ClickEvent;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.HoverEvent;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.item.ItemEntity;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

/**
 * Início da jornada e posse da Pena (regra captura.pena_rev9, aprovada em 18/11/2026).
 * <ul>
 * <li>Na primeira entrada no mundo, o treinador recebe a Pena de Captura nível 1 e escolhe um dos seis iniciais,
 * que chega no nível 5 com IVs sorteados.</li>
 * <li>A Pena não fica no chão (some se cair) e volta ao dono ao entrar no mundo, renascer ou acordar numa cama.</li>
 * </ul>
 */
public final class Jornada {
	public static final List<Integer> INICIAIS = List.of(1, 2, 3, 4, 5, 6);
	public static final int NIVEL_INICIAL = 5;

	private Jornada() {
	}

	public static void registrar() {
		ServerPlayConnectionEvents.JOIN.register((conexao, envio, servidor) -> aoEntrar(conexao.getPlayer()));
		ServerPlayerEvents.AFTER_RESPAWN.register((velho, novo, vivo) -> Capturas.restaurarPena(novo));
		EntitySleepEvents.STOP_SLEEPING.register((entidade, cama) -> {
			if (entidade instanceof ServerPlayer p)
				Capturas.restaurarPena(p);
		});
		// a Pena não fica no chão: se cair (morte, jogada, baú quebrado), some e volta ao dono pela regra de posse
		ServerEntityEvents.ENTITY_LOAD.register((entidade, mundo) -> {
			if (entidade instanceof ItemEntity item && item.getItem().is(ModItens.PENA_DE_CAPTURA))
				item.discard();
		});
	}

	static void aoEntrar(ServerPlayer p) {
		Treinador t = ModAnexos.treinador(p);
		if (t.penaVersao() == 0) {
			Capturas.novaPena(p);
			p.displayClientMessage(Component.literal("Início da jornada: você recebeu a Pena de Captura!").withStyle(ChatFormatting.GOLD), false);
		} else {
			Capturas.restaurarPena(p);
		}
		if (!t.inicialEscolhido())
			oferecerIniciais(p);
	}

	public static void oferecerIniciais(ServerPlayer p) {
		Galetario g = Galetario.padrao();
		MutableComponent linha = Component.literal("Escolha seu Galeto inicial: ").withStyle(ChatFormatting.GOLD);
		for (int n : INICIAIS) {
			Especie e = g.especie(n);
			linha.append(Component.literal("[" + e.nome() + "] ").withStyle(st -> st.withColor(ChatFormatting.GREEN)
					.withClickEvent(new ClickEvent.RunCommand("/galetocraft inicial " + n))
					.withHoverEvent(new HoverEvent.ShowText(Component.literal(e.elementos().get(0).nome() + " · " + e.passiva())))));
		}
		p.displayClientMessage(linha, false);
	}

	/** Escolha do inicial: uma vez por treinador. */
	public static boolean escolher(ServerPlayer p, int numero) {
		Treinador t = ModAnexos.treinador(p);
		if (t.inicialEscolhido()) {
			p.displayClientMessage(Component.literal("Você já escolheu seu Galeto inicial.").withStyle(ChatFormatting.RED), false);
			return false;
		}
		if (!INICIAIS.contains(numero)) {
			p.displayClientMessage(Component.literal("Os iniciais são os Galetos #001 a #006.").withStyle(ChatFormatting.RED), false);
			return false;
		}
		Especie e = Galetario.padrao().especie(numero);
		ModAnexos.salvar(p, t.comCapturado(novo(p, e, NIVEL_INICIAL)).comInicialEscolhido());
		p.displayClientMessage(Component.literal(e.nome() + " é o seu Galeto inicial! Veja a equipe em /galetocraft equipe.")
				.withStyle(ChatFormatting.GOLD), false);
		return true;
	}

	/** Galeto novo do treinador (inicial ou dado por operador): sexo pela espécie e IVs sorteados de 1 a 40. */
	public static GaletoGuardado novo(ServerPlayer p, Especie e, int nivel) {
		var rng = p.getRandom();
		String sexo = e.probabilidadeMacho() == null ? "-" : rng.nextDouble() < e.probabilidadeMacho() ? "M" : "F";
		List<Integer> ivs = new ArrayList<>();
		for (int i = 0; i < 6; i++)
			ivs.add(1 + rng.nextInt(40));
		return GaletoGuardado.capturado(UUID.randomUUID(), e.numero(), nivel, sexo, ivs);
	}
}
