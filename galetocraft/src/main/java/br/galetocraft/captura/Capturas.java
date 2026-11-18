package br.galetocraft.captura;

import br.galetocraft.entidade.GaloEntity;
import br.galetocraft.nucleo.dados.Especie;
import br.galetocraft.nucleo.dados.Galetario;
import br.galetocraft.nucleo.regras.Captura;
import br.galetocraft.registro.ModAnexos;
import br.galetocraft.registro.ModItens;
import br.galetocraft.treinador.GaletoGuardado;
import br.galetocraft.treinador.Treinador;
import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.ProjectileUtil;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.EntityHitResult;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

/**
 * Captura com a Pena de Captura (regra captura da base vigente).
 * <p>
 * <b>Mundo direto:</b> o treinador mira no Cocorídeo selvagem e usa o botão direito com a Pena na mão, sem arremesso;
 * alcance de 12 blocos em qualquer nível da Pena; linha de visão livre (blocos sólidos impedem a tentativa); o
 * resultado sai na hora com {@code P = 100·R·F/(R·F + D)}; o Feixe do Rubi simplificado só aparece no sucesso; na
 * falha o Cocorídeo segue normalmente e resiste por 20 s (60 s se Lendário), para todos os jogadores.
 * <p>
 * <b>Depois do sucesso</b> (nas duas modalidades): o Cocorídeo vai para a equipe principal se houver vaga, senão para
 * as reservas; a Pena ganha {@code XP_base(raridade) + 2·nível}, com o excedente reaproveitado e sem XP nova no nível 5.
 * <p>
 * Pendentes na regra e tratados de forma provisória: tentativa contra alvo inelegível (Lendário sem Pena 5, Lendário
 * Original) não é iniciada; um Cocorídeo que está numa Rinha não é alvo da captura no mundo; o desenho exato do
 * feixe (aqui, uma linha de partículas cor de rubi).
 */
public final class Capturas {
	public static final Captura REGRAS = new Captura(Galetario.padrao());
	private static final DustParticleOptions RUBI = new DustParticleOptions(0xE0115F, 1.0f);

	private Capturas() {
	}

	public static boolean temPena(Player p) {
		return p.getInventory().contains(s -> s.is(ModItens.PENA_DE_CAPTURA));
	}

	public static int nivelPena(Player p) {
		return REGRAS.nivelPena(ModAnexos.treinador(p).penaXp());
	}

	/** Linha de estado da Pena: nível e XP até a próxima evolução. */
	public static Component estadoPena(Player p) {
		int xp = ModAnexos.treinador(p).penaXp(), nivel = REGRAS.nivelPena(xp);
		String prox = nivel >= REGRAS.nivelPenaMaximo() ? "nível máximo"
				: "próxima evolução aos " + REGRAS.xpParaNivelPena(nivel + 1) + " XP";
		return Component.literal("Pena de Captura nível " + nivel + " · " + xp + " XP (" + prox + ")").withStyle(ChatFormatting.LIGHT_PURPLE);
	}

	// ------------------------------------------------------------------ mundo direto
	/** Tentativa de captura direta no mundo (botão direito com a Pena na mão). */
	public static void tentarNoMundo(ServerPlayer p) {
		double alcance = REGRAS.alcanceMundo();
		Vec3 olho = p.getEyePosition();
		Vec3 direcao = p.getViewVector(1f);
		Vec3 fim = olho.add(direcao.scale(alcance));
		// linha de visão: o primeiro bloco sólido encurta a mira
		BlockHitResult bloco = p.level().clip(new ClipContext(olho, fim, ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, p));
		if (bloco.getType() != HitResult.Type.MISS)
			fim = bloco.getLocation();
		AABB area = p.getBoundingBox().expandTowards(fim.subtract(olho)).inflate(1.0);
		EntityHitResult acerto = ProjectileUtil.getEntityHitResult(p, olho, fim, area,
				e -> e instanceof GaloEntity && e.isPickable() && !e.isSpectator(), olho.distanceToSqr(fim));
		if (acerto == null || !(acerto.getEntity() instanceof GaloEntity alvo)) {
			aviso(p, "Mire num Cocorídeo selvagem a até " + (int) alcance + " blocos, sem blocos no caminho.");
			return;
		}
		Especie e = alvo.fichaDaEspecie().orElse(null);
		if (e == null) {
			aviso(p, "Este Cocorídeo não está no Galetário vigente.");
			return;
		}
		if (alvo.emRinha()) {
			aviso(p, e.nome() + " está numa Rinha.");
			return;
		}
		long espera = alvo.esperaCaptura();
		if (espera > 0) {
			aviso(p, e.nome() + " ainda resiste à captura por " + (espera + 19) / 20 + " s.");
			return;
		}
		int nivelPena = nivelPena(p);
		if (!REGRAS.elegivel(e.raridade(), nivelPena)) {
			aviso(p, e.nome() + " (" + e.raridade() + ") não pode ser capturado com a Pena de Captura nível " + nivelPena + ".");
			return;
		}
		double chance = REGRAS.chancePercentual(Captura.Modalidade.MUNDO, e.raridade(), nivelPena, alvo.nivel(), 0, 1, null);
		if (p.getRandom().nextDouble() * 100 < chance) {
			feixeDoRubi(p, alvo);
			registrarCaptura(p, alvo.guardar());
			alvo.discard();
		} else {
			Integer segundos = REGRAS.cooldownMundo(e.raridade());
			if (segundos != null)
				alvo.iniciarEsperaCaptura(segundos);
			p.displayClientMessage(Component.literal("A captura de " + e.nome() + " falhou.").withStyle(ChatFormatting.GRAY), false);
		}
	}

	/** Feixe do Rubi simplificado: linha de partículas da Pena até o Cocorídeo (só no sucesso). */
	private static void feixeDoRubi(ServerPlayer p, Entity alvo) {
		ServerLevel mundo = p.level();
		Vec3 de = p.getEyePosition().add(0, -0.3, 0), ate = alvo.getBoundingBox().getCenter();
		int passos = (int) Math.ceil(de.distanceTo(ate) * 4);
		for (int i = 0; i <= passos; i++) {
			Vec3 q = de.lerp(ate, (double) i / passos);
			mundo.sendParticles(RUBI, q.x, q.y, q.z, 1, 0, 0, 0, 0);
		}
	}

	// ------------------------------------------------------------------ depois do sucesso
	/** Guarda o capturado na equipe ou nas reservas e soma a XP da Pena. */
	public static void registrarCaptura(ServerPlayer p, GaletoGuardado g) {
		Treinador t = ModAnexos.treinador(p);
		boolean naEquipe = !t.equipeCheia();
		int antes = REGRAS.nivelPena(t.penaXp());
		int ganho = REGRAS.xpPena(g.ficha().raridade(), g.nivel());
		int xp = REGRAS.somarXpPena(t.penaXp(), ganho);
		ModAnexos.salvar(p, t.comCapturado(g).comPenaXp(xp));
		p.displayClientMessage(Component.literal(g.ficha().nome() + " foi capturado e foi para "
				+ (naEquipe ? "a equipe principal." : "as reservas (equipe principal cheia).")).withStyle(ChatFormatting.GREEN), false);
		p.displayClientMessage(Component.literal(xp > t.penaXp() ? "A Pena de Captura ganhou " + (xp - t.penaXp()) + " XP."
				: "A Pena de Captura já está no nível máximo.").withStyle(ChatFormatting.LIGHT_PURPLE), false);
		int depois = REGRAS.nivelPena(xp);
		if (depois > antes)
			p.displayClientMessage(Component.literal("A Pena de Captura evoluiu para o nível " + depois + "!").withStyle(ChatFormatting.GOLD), false);
	}

	private static void aviso(ServerPlayer p, String texto) {
		p.displayClientMessage(Component.literal(texto).withStyle(ChatFormatting.YELLOW), false);
	}
}
