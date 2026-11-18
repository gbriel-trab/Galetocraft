package br.galetocraft.treinador;

import br.galetocraft.entidade.GaloEntity;
import br.galetocraft.registro.ModAnexos;
import br.galetocraft.registro.ModEntidades;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.ClickEvent;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;

import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Galeto do treinador no mundo (regra treinador.companheiro_rev9).
 * <ul>
 * <li>1 companheiro por treinador: segue, teleporta além de 24 blocos, não ataca, é invulnerável fora da Rinha, não pode
 * ser desafiado nem capturado; volta à equipe ao começar uma Rinha, quando o jogador sai ou ao ser tocado com a Pena.</li>
 * <li>Libertar: com confirmação dupla, o Galeto deixa o treinador e vira selvagem no lugar, com o mesmo nível e IVs;
 * não vale para o último Galeto da equipe.</li>
 * </ul>
 * Só espécies com modelo no mod podem sair para o mundo.
 */
public final class Companheiros {
	private static final Map<UUID, UUID> ATIVO = new ConcurrentHashMap<>();   // jogador → entidade

	private Companheiros() {
	}

	public static Optional<GaloEntity> ativo(ServerPlayer p) {
		UUID id = ATIVO.get(p.getUUID());
		if (id != null && p.level().getEntity(id) instanceof GaloEntity g && g.isAlive())
			return Optional.of(g);
		ATIVO.remove(p.getUUID());
		return Optional.empty();
	}

	/** Chama o Galeto da posição {@code indice} da equipe para seguir o treinador. */
	public static void chamar(ServerPlayer p, int indice) {
		Treinador t = ModAnexos.treinador(p);
		if (indice < 0 || indice >= t.equipe().size()) {
			aviso(p, "Não há Galeto na posição " + (indice + 1) + " da equipe.");
			return;
		}
		GaletoGuardado g = t.equipe().get(indice);
		Optional<EntityType<? extends GaloEntity>> tipo = ModEntidades.porEspecie(g.especie());
		if (tipo.isEmpty()) {
			aviso(p, g.ficha().nome() + " ainda não tem modelo no mod e não pode sair para o mundo.");
			return;
		}
		recolher(p, false);
		ServerLevel l = p.level();
		GaloEntity e = tipo.get().create(l, EntitySpawnReason.MOB_SUMMONED);
		if (e == null)
			return;
		e.definirIndividuo(g.nivel(), g.sexo().isEmpty() ? '-' : g.sexo().charAt(0), g.ivs().stream().mapToInt(Integer::intValue).toArray());
		e.tornarCompanheiro(p.getUUID(), g.id());
		e.snapTo(p.getX() + 1, p.getY(), p.getZ() + 1, p.getYRot(), 0);
		l.addFreshEntity(e);
		ATIVO.put(p.getUUID(), e.getUUID());
		p.displayClientMessage(Component.literal(g.ficha().nome() + " está acompanhando você. Toque nele com a Pena de Captura para recolher.")
				.withStyle(ChatFormatting.GREEN), false);
	}

	/** Recolhe o companheiro para a equipe (Pena, Rinha ou saída do jogador). */
	public static void recolher(ServerPlayer p, boolean avisar) {
		ativo(p).ifPresent(g -> {
			g.discard();
			if (avisar)
				p.displayClientMessage(Component.literal(g.fichaDaEspecie().map(e -> e.nome()).orElse("O Galeto") + " voltou para a equipe.")
						.withStyle(ChatFormatting.GRAY), false);
		});
		ATIVO.remove(p.getUUID());
	}

	public static void recolher(UUID jogador, net.minecraft.server.MinecraftServer s) {
		UUID id = ATIVO.remove(jogador);
		if (id != null)
			for (ServerLevel l : s.getAllLevels())
				if (l.getEntity(id) instanceof GaloEntity g)
					g.discard();
	}

	/**
	 * Libertar com confirmação dupla: etapa 0 avisa, etapa 1 pede a confirmação final, etapa 2 solta o Galeto.
	 */
	public static void libertar(ServerPlayer p, int indice, int etapa) {
		Treinador t = ModAnexos.treinador(p);
		if (indice < 0 || indice >= t.equipe().size()) {
			aviso(p, "Não há Galeto na posição " + (indice + 1) + " da equipe.");
			return;
		}
		GaletoGuardado g = t.equipe().get(indice);
		if (t.equipe().size() == 1) {
			aviso(p, "Não dá para libertar o último Galeto da equipe.");
			return;
		}
		if (etapa == 0) {
			p.displayClientMessage(Component.literal("Libertar " + g.ficha().nome() + " Nv" + g.nivel() + " para sempre? Ele vira selvagem. ")
					.withStyle(ChatFormatting.YELLOW).append(botao("[Sim, continuar]", "/galetocraft libertar " + indice + " confirmar")), false);
			return;
		}
		if (etapa == 1) {
			p.displayClientMessage(Component.literal("Última confirmação: " + g.ficha().nome() + " deixará de ser seu. ")
					.withStyle(ChatFormatting.RED).append(botao("[Libertar " + g.ficha().nome() + "]", "/galetocraft libertar " + indice + " definitivo")), false);
			return;
		}
		ativo(p).filter(e -> g.id().equals(e.idGuardado())).ifPresent(e -> recolher(p, false));
		ModAnexos.salvar(p, t.sem(g.id()));
		ModEntidades.porEspecie(g.especie()).ifPresent(tipo -> {
			GaloEntity e = tipo.create(p.level(), EntitySpawnReason.EVENT);
			if (e != null) {
				e.definirIndividuo(g.nivel(), g.sexo().isEmpty() ? '-' : g.sexo().charAt(0), g.ivs().stream().mapToInt(Integer::intValue).toArray());
				e.marcarSelvagemNatural();
				e.snapTo(p.getX() + 1, p.getY(), p.getZ() + 1, p.getYRot(), 0);
				p.level().addFreshEntity(e);
			}
		});
		p.displayClientMessage(Component.literal(g.ficha().nome() + " foi libertado e voltou à natureza.").withStyle(ChatFormatting.GRAY), false);
	}

	private static MutableComponent botao(String texto, String comando) {
		return Component.literal(texto).withStyle(st -> st.withColor(ChatFormatting.AQUA).withClickEvent(new ClickEvent.RunCommand(comando)));
	}

	private static void aviso(ServerPlayer p, String texto) {
		p.displayClientMessage(Component.literal(texto).withStyle(ChatFormatting.YELLOW), false);
	}
}
