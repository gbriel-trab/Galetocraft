package br.galetocraft.rinha;

import br.galetocraft.entidade.GaloEntity;
import br.galetocraft.registro.ModAnexos;
import br.galetocraft.treinador.GaletoGuardado;
import br.galetocraft.treinador.Treinador;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.ClickEvent;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.server.level.ServerPlayer;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Escalação antes da Rinha (regra treinador.escalacao_rev9): o treinador escolhe 3 dos 5 da equipe principal e quem
 * começa (o 1º escolhido). Já vem marcado o padrão: os 3 primeiros da ordem da equipe. Com 3 ou menos Galetos, a Rinha
 * começa direto. O Galeto selvagem fica reservado enquanto o treinador escolhe.
 */
public final class Escalacoes {
	private record Pendente(GaloEntity selvagem, List<Integer> escolhidos) {
	}

	private static final Map<UUID, Pendente> PENDENTES = new ConcurrentHashMap<>();

	private Escalacoes() {
	}

	public static void desafiar(ServerPlayer p, GaloEntity selvagem) {
		Treinador t = ModAnexos.treinador(p);
		if (t.equipe().size() <= GerenciadorRinhas.GALETOS_NA_RINHA) {
			GerenciadorRinhas.iniciar(p, selvagem, null);
			return;
		}
		cancelar(p);
		selvagem.emRinha(true);   // reservado durante a escolha
		List<Integer> padrao = new ArrayList<>(List.of(0, 1, 2));
		PENDENTES.put(p.getUUID(), new Pendente(selvagem, padrao));
		mostrar(p);
	}

	public static void alternar(ServerPlayer p, int indice) {
		Pendente e = PENDENTES.get(p.getUUID());
		if (e == null || indice < 0 || indice >= ModAnexos.treinador(p).equipe().size())
			return;
		if (e.escolhidos().contains(indice))
			e.escolhidos().remove(Integer.valueOf(indice));
		else if (e.escolhidos().size() < GerenciadorRinhas.GALETOS_NA_RINHA)
			e.escolhidos().add(indice);
		mostrar(p);
	}

	public static void confirmar(ServerPlayer p) {
		Pendente e = PENDENTES.remove(p.getUUID());
		if (e == null)
			return;
		e.selvagem().emRinha(false);
		if (e.selvagem().isRemoved() || e.escolhidos().size() != GerenciadorRinhas.GALETOS_NA_RINHA) {
			p.displayClientMessage(Component.literal(e.selvagem().isRemoved() ? "O Galeto selvagem não está mais aqui."
					: "Escolha 3 Galetos para a Rinha.").withStyle(ChatFormatting.RED), false);
			if (!e.selvagem().isRemoved() && e.escolhidos().size() != GerenciadorRinhas.GALETOS_NA_RINHA) {
				e.selvagem().emRinha(true);
				PENDENTES.put(p.getUUID(), e);
				mostrar(p);
			}
			return;
		}
		GerenciadorRinhas.iniciar(p, e.selvagem(), List.copyOf(e.escolhidos()));
	}

	public static void cancelar(ServerPlayer p) {
		Pendente e = PENDENTES.remove(p.getUUID());
		if (e != null && !e.selvagem().isRemoved())
			e.selvagem().emRinha(false);
	}

	public static void cancelar(UUID jogador) {
		Pendente e = PENDENTES.remove(jogador);
		if (e != null && !e.selvagem().isRemoved())
			e.selvagem().emRinha(false);
	}

	private static void mostrar(ServerPlayer p) {
		Pendente e = PENDENTES.get(p.getUUID());
		List<GaletoGuardado> equipe = ModAnexos.treinador(p).equipe();
		MutableComponent linha = Component.literal("Escalação (escolha 3; o 1º começa): ").withStyle(ChatFormatting.GOLD);
		for (int i = 0; i < equipe.size(); i++) {
			int ordem = e.escolhidos().indexOf(i);
			GaletoGuardado g = equipe.get(i);
			linha.append(botao((ordem >= 0 ? "[✔" + (ordem + 1) + " " : "[") + g.ficha().nome() + " Nv" + g.nivel() + "] ",
					"/galetocraft escalar " + i, ordem >= 0 ? ChatFormatting.GREEN : ChatFormatting.GRAY));
		}
		p.displayClientMessage(linha, false);
		p.displayClientMessage(botao("[Começar Rinha] ", "/galetocraft escalar ok", ChatFormatting.AQUA)
				.append(botao("[Cancelar]", "/galetocraft escalar cancelar", ChatFormatting.RED)), false);
	}

	private static MutableComponent botao(String texto, String comando, ChatFormatting cor) {
		return Component.literal(texto).withStyle(st -> st.withColor(cor).withClickEvent(new ClickEvent.RunCommand(comando)));
	}
}
