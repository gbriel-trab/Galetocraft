package br.galetocraft.entidade;

import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animatable.manager.AnimatableManager;
import software.bernie.geckolib.animation.AnimationController;
import software.bernie.geckolib.animation.RawAnimation;
import software.bernie.geckolib.util.GeckoLibUtil;

/**
 * Galo genérico do Galetocraft: serve para todas as espécies que (por enquanto) só têm modelo, animações e atributos
 * próprios. O id da espécie vem do tipo da entidade (galetocraft:&lt;id&gt;) e escolhe as animações
 * "animation.&lt;id&gt;.idle" e "animation.&lt;id&gt;.walk" em geckolib/animations/entity/&lt;id&gt;.animation.json
 * (geradas por ferramentas/exportar_especie.py).
 * <p>
 * Comportamento: neutro, passeia e olha os jogadores, revida quando é atacado.
 */
public class GaloEntity extends PathfinderMob implements GeoEntity {
	private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);

	public GaloEntity(EntityType<? extends GaloEntity> tipo, Level mundo) {
		super(tipo, mundo);
	}

	public static AttributeSupplier.Builder criarAtributos(double vida, double velocidade, double dano) {
		return PathfinderMob.createMobAttributes()
				.add(Attributes.MAX_HEALTH, vida)
				.add(Attributes.MOVEMENT_SPEED, velocidade)
				.add(Attributes.ATTACK_DAMAGE, dano)
				.add(Attributes.FOLLOW_RANGE, 24.0);
	}

	/** Id da espécie (o caminho do id do tipo: "esporoco", "cocorak"...). */
	public String especie() {
		return BuiltInRegistries.ENTITY_TYPE.getKey(getType()).getPath();
	}

	@Override
	protected void registerGoals() {
		this.goalSelector.addGoal(0, new FloatGoal(this));
		this.goalSelector.addGoal(1, new MeleeAttackGoal(this, 1.2, false));
		this.goalSelector.addGoal(2, new WaterAvoidingRandomStrollGoal(this, 0.8));
		this.goalSelector.addGoal(3, new LookAtPlayerGoal(this, Player.class, 8.0f));
		this.goalSelector.addGoal(4, new RandomLookAroundGoal(this));
		this.targetSelector.addGoal(1, new HurtByTargetGoal(this));
	}

	// ---- sons (por enquanto, os da galinha) ----
	@Override
	protected SoundEvent getAmbientSound() {
		return SoundEvents.CHICKEN_AMBIENT;
	}

	@Override
	protected SoundEvent getHurtSound(DamageSource fonte) {
		return SoundEvents.CHICKEN_HURT;
	}

	@Override
	protected SoundEvent getDeathSound() {
		return SoundEvents.CHICKEN_DEATH;
	}

	// ---- GeckoLib: animação parado/andando da espécie ----
	@Override
	public void registerControllers(AnimatableManager.ControllerRegistrar controladores) {
		final String id = especie();
		final RawAnimation parado = RawAnimation.begin().thenLoop("animation." + id + ".idle");
		final RawAnimation andando = RawAnimation.begin().thenLoop("animation." + id + ".walk");

		controladores.add(new AnimationController<GaloEntity>("movimento", 5,
				teste -> teste.setAndContinue(teste.isMoving() ? andando : parado)));
	}

	@Override
	public AnimatableInstanceCache getAnimatableInstanceCache() {
		return this.cache;
	}
}
