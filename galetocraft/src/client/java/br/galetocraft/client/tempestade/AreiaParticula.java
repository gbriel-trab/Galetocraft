package br.galetocraft.client.tempestade;

import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.particle.Particle;
import net.minecraft.client.particle.ParticleProvider;
import net.minecraft.client.particle.SingleQuadParticle;
import net.minecraft.client.particle.SpriteSet;
import net.minecraft.core.particles.SimpleParticleType;
import net.minecraft.util.RandomSource;

/**
 * Grão de areia soprado pela tempestade: desliza na direção do vento, quase sem cair, aparece e some aos poucos.
 * Usa as texturas vanilla de poeira ({@code minecraft:generic_*}) tingidas de cor de areia.
 */
public class AreiaParticula extends SingleQuadParticle {
	private final float alphaMax;

	protected AreiaParticula(ClientLevel mundo, double x, double y, double z, double vx, double vy, double vz, SpriteSet sprites, RandomSource rng) {
		super(mundo, x, y, z, sprites.get(rng));
		this.xd = vx;
		this.yd = vy;
		this.zd = vz;
		this.hasPhysics = false;
		this.gravity = 0.004f;
		this.friction = 0.99f;
		this.lifetime = 40 + rng.nextInt(40);
		this.quadSize = 0.05f + rng.nextFloat() * 0.09f;
		float tom = 0.9f + rng.nextFloat() * 0.15f;
		setColor(Math.min(1f, 0.86f * tom), Math.min(1f, 0.72f * tom), Math.min(1f, 0.48f * tom));
		this.alphaMax = 0.55f + rng.nextFloat() * 0.35f;
		setAlpha(0f);
	}

	@Override
	public void tick() {
		super.tick();
		float t = (float) age / lifetime;
		setAlpha(alphaMax * Math.min(1f, Math.min(t * 6f, (1f - t) * 4f)));
	}

	@Override
	protected Layer getLayer() {
		return Layer.TRANSLUCENT;
	}

	public static class Provider implements ParticleProvider<SimpleParticleType> {
		private final SpriteSet sprites;

		public Provider(SpriteSet sprites) {
			this.sprites = sprites;
		}

		@Override
		public Particle createParticle(SimpleParticleType tipo, ClientLevel mundo, double x, double y, double z, double vx, double vy, double vz, RandomSource rng) {
			return new AreiaParticula(mundo, x, y, z, vx, vy, vz, sprites, rng);
		}
	}
}
