package br.galetocraft.client.tempestade;

import br.galetocraft.mundo.TempestadeDeAreia;
import net.minecraft.client.Minecraft;
import net.minecraft.server.level.ParticleStatus;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.resources.sounds.AbstractTickableSoundInstance;
import net.minecraft.client.resources.sounds.SoundInstance;
import net.minecraft.core.BlockPos;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.RandomSource;
import net.minecraft.world.phys.Vec3;

/**
 * Tempestade de areia no cliente (regra tempestade_de_areia): calcula a intensidade na posição da câmera, com
 * transição suave, e desenha a poeira e o vento. A névoa amarelada fica no mixin da névoa atmosférica.
 */
public final class TempestadeCliente {
	private static float intensidade;
	private static Vento vento;

	private TempestadeCliente() {
	}

	/** 0 (sem tempestade) a 1 (tempestade plena na câmera). */
	public static float intensidade() {
		return intensidade;
	}

	public static void tick(Minecraft mc) {
		ClientLevel l = mc.level;
		if (l == null || mc.player == null) {
			intensidade = 0;
			return;
		}
		Vec3 olho = mc.gameRenderer.getMainCamera().position();
		BlockPos pos = BlockPos.containing(olho);
		float alvo = TempestadeDeAreia.biomaDeAreia(l, pos) && l.canSeeSky(pos) ? l.getRainLevel(1f) : 0f;
		intensidade += (alvo - intensidade) * 0.04f;
		if (intensidade < 0.002f && alvo == 0f)
			intensidade = 0f;
		if (intensidade > 0f && !mc.isPaused())
			poeira(mc, l, olho);
		if (intensidade > 0.05f && (vento == null || vento.isStopped())) {
			vento = new Vento();
			mc.getSoundManager().play(vento);
		}
	}

	private static void poeira(Minecraft mc, ClientLevel l, Vec3 olho) {
		ParticleStatus status = mc.options.particles().get();
		int base = switch (status) {
			case ALL -> 70;
			case DECREASED -> 35;
			case MINIMAL -> 10;
		};
		int n = Math.round(base * intensidade);
		double ang = TempestadeDeAreia.direcaoDoVento(l);
		double vx = Math.cos(ang), vz = Math.sin(ang);
		RandomSource rng = l.getRandom();
		for (int i = 0; i < n; i++) {
			double x = olho.x + (rng.nextDouble() - 0.5) * 36 - vx * 8;   // um pouco a barlavento, para a poeira atravessar a tela
			double y = olho.y - 3 + rng.nextDouble() * 11;
			double z = olho.z + (rng.nextDouble() - 0.5) * 36 - vz * 8;
			if (!l.canSeeSky(BlockPos.containing(x, y, z)))
				continue;
			double v = 0.35 + rng.nextDouble() * 0.45;
			l.addParticle(TempestadeDeAreia.PARTICULA_AREIA, x, y, z, vx * v, (rng.nextDouble() - 0.45) * 0.04, vz * v);
		}
	}

	/** Vento contínuo enquanto durar a tempestade (som vanilla de vento do voo de élitro, mais grave). */
	private static final class Vento extends AbstractTickableSoundInstance {
		Vento() {
			super(SoundEvents.ELYTRA_FLYING, SoundSource.WEATHER, SoundInstance.createUnseededRandom());
			this.looping = true;
			this.delay = 0;
			this.volume = 0.01f;
			this.pitch = 0.55f;
			this.relative = true;
			this.attenuation = SoundInstance.Attenuation.NONE;
		}

		@Override
		public void tick() {
			if (intensidade < 0.02f) {
				stop();
				return;
			}
			this.volume = 0.45f * intensidade;
		}
	}
}
