package br.galetocraft.entidade;

import br.galetocraft.nucleo.dados.Atributo;
import br.galetocraft.nucleo.dados.Especie;
import br.galetocraft.nucleo.dados.Galetario;
import br.galetocraft.nucleo.regras.Progressao;
import net.minecraft.ChatFormatting;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.RandomSource;
import net.minecraft.world.DifficultyInstance;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.SpawnGroupData;
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
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.storage.ValueInput;
import net.minecraft.world.level.storage.ValueOutput;
import software.bernie.geckolib.animatable.GeoEntity;
import software.bernie.geckolib.animatable.instance.AnimatableInstanceCache;
import software.bernie.geckolib.animatable.manager.AnimatableManager;
import software.bernie.geckolib.animation.AnimationController;
import software.bernie.geckolib.animation.RawAnimation;
import software.bernie.geckolib.util.GeckoLibUtil;

import java.text.Normalizer;
import java.util.Arrays;
import java.util.Locale;
import java.util.Optional;

/**
 * Galo do Galetocraft, base de todas as espécies. O id da espécie vem do tipo da entidade (galetocraft:&lt;id&gt;)
 * e escolhe as animações "animation.&lt;id&gt;.idle" e "animation.&lt;id&gt;.walk"
 * (geradas por ferramentas/exportar_especie.py).
 * <p>
 * <b>Galeto individual:</b> cada criatura tem nível, sexo e os 6 IVs, salvos com a entidade.
 * <ul>
 * <li>Sexo: sorteado pela distribuição da espécie no Galetário (Galeria).</li>
 * <li>IVs: inteiros de 1 a 40, uniformes, como os IVs não herdados da reprodução.</li>
 * <li>Nível: sorteado de 1 a 70 para todo Galeto novo, sem depender do local (regra mundo_aparecimento, rev. 9).</li>
 * </ul>
 * Os atributos seguem a regra progressao (rev. 8): nominal no nível → IV/EV → peso.
 * Clicar com a mão vazia mostra a ficha do indivíduo.
 * <p>
 * Comportamento no mundo: neutro, passeia, olha os jogadores e revida quando é atacado.
 */
public class GaloEntity extends PathfinderMob implements GeoEntity {
	public static final int NIVEL_PADRAO = Progressao.NIVEL_REFERENCIA;
	/** Nível dos selvagens (regra mundo_aparecimento, rev. 9): uniforme de 1 a 70, sem depender do local. */
	public static final int NIVEL_SELVAGEM_MIN = 1, NIVEL_SELVAGEM_MAX = 70;
	public static final int IV_MINIMO = 1, IV_MAXIMO = 40;

	private final AnimatableInstanceCache cache = GeckoLibUtil.createInstanceCache(this);
	private int nivel;            // 0 = ainda não gerado
	private char sexo = '?';
	private int[] ivs = new int[0];
	private boolean emRinha;
	private long esperaCapturaAte;   // tempo do jogo (ticks) até o fim da resistência após captura falha no mundo
	private boolean selvagemNatural; // apareceu sozinho (spawn natural ou encontro): some quando o jogador se afasta
	private java.util.UUID dono;      // companheiro de um treinador (não é selvagem); nulo = selvagem
	private java.util.UUID idGuardado; // id do Galeto guardado que este companheiro representa

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

	/** Ficha da espécie no Galetário (o id sem acento casa com o nome oficial: "sirenoco" → Sirenocó). */
	public Optional<Especie> fichaDaEspecie() {
		return Galetario.padrao().especies().stream().filter(e -> semAcento(e.nome()).equals(especie())).findFirst();
	}

	private static String semAcento(String s) {
		return Normalizer.normalize(s, Normalizer.Form.NFD).replaceAll("\\p{M}", "").toLowerCase(Locale.ROOT);
	}

	public int nivel() {
		garantirIndividuo(getRandom());
		return nivel;
	}

	public char sexo() {
		garantirIndividuo(getRandom());
		return sexo;
	}

	public int[] ivs() {
		garantirIndividuo(getRandom());
		return ivs.clone();
	}

	public boolean emRinha() {
		return emRinha;
	}

	/** Durante a Rinha o Galeto fica parado (sem IA) e não revida no mundo. */
	public void emRinha(boolean v) {
		emRinha = v;
		setNoAi(v);
	}

	/** Ticks de jogo que ainda faltam para a espera de captura no mundo terminar (0 = livre). */
	public long esperaCaptura() {
		return Math.max(0, esperaCapturaAte - level().getGameTime());
	}

	/** Inicia a espera após uma captura falha no mundo: vale para todos os jogadores. */
	public void iniciarEsperaCaptura(int segundos) {
		esperaCapturaAte = level().getGameTime() + segundos * 20L;
	}

	/** Dados individuais para a Rinha: os IVs da criatura, EV 0 e peso neutro (spawn_ratio 1,0 da V1.2). */
	public br.galetocraft.nucleo.rinha.Individuo individuo() {
		return br.galetocraft.nucleo.rinha.Individuo.novo(ivs());
	}

	/** Dados do indivíduo para guardar com o treinador depois da captura. */
	public br.galetocraft.treinador.GaletoGuardado guardar() {
		Especie e = fichaDaEspecie().orElseThrow();
		// XP inicial = T(nível), sem XP extra; golpes por nível já aprendidos (retrodesbloqueio); EV 0; peso neutro
		return br.galetocraft.treinador.GaletoGuardado.capturado(getUUID(), e.numero(), nivel(), String.valueOf(sexo()),
				Arrays.stream(ivs()).boxed().toList());
	}

	/** Gera nível, sexo e IVs uma única vez (ao aparecer ou na primeira consulta de entidades antigas). */
	private void garantirIndividuo(RandomSource rng) {
		if (nivel > 0)
			return;
		nivel = NIVEL_SELVAGEM_MIN + rng.nextInt(NIVEL_SELVAGEM_MAX - NIVEL_SELVAGEM_MIN + 1);
		Optional<Especie> e = fichaDaEspecie();
		Double machos = e.map(Especie::probabilidadeMacho).orElse(null);
		sexo = machos == null ? '-' : (rng.nextDouble() < machos ? 'M' : 'F');
		ivs = new int[Atributo.values().length];
		for (int i = 0; i < ivs.length; i++)
			ivs[i] = IV_MINIMO + rng.nextInt(IV_MAXIMO - IV_MINIMO + 1);
	}

	/** Define o nível de um indivíduo ainda não gerado (encontros especiais, como o Quetzacocó no nível 70). */
	public void definirNivel(int n) {
		garantirIndividuo(getRandom());
		nivel = Math.max(Progressao.NIVEL_MINIMO, Math.min(Progressao.NIVEL_MAXIMO, n));
	}

	/** Companheiro de um treinador: não é selvagem, não pode ser capturado nem desafiado. */
	public boolean companheiro() {
		return dono != null;
	}

	public java.util.UUID dono() {
		return dono;
	}

	public java.util.UUID idGuardado() {
		return idGuardado;
	}

	/** Copia os dados individuais de um Galeto guardado (companheiro ou Galeto libertado). */
	public void definirIndividuo(int nivel, char sexo, int[] ivs) {
		this.nivel = Math.max(Progressao.NIVEL_MINIMO, Math.min(Progressao.NIVEL_MAXIMO, nivel));
		this.sexo = sexo;
		this.ivs = ivs.clone();
	}

	public void tornarCompanheiro(java.util.UUID treinador, java.util.UUID galetoGuardado) {
		dono = treinador;
		idGuardado = galetoGuardado;
		selvagemNatural = false;
		setPersistenceRequired();
	}

	public boolean selvagemNatural() {
		return selvagemNatural;
	}

	public void marcarSelvagemNatural() {
		selvagemNatural = true;
	}

	/** Selvagens naturais somem quando o jogador se afasta, exceto em Rinha ou com espera de captura ativa. */
	@Override
	public boolean removeWhenFarAway(double distanciaQuadrada) {
		return selvagemNatural && !emRinha && esperaCaptura() == 0;
	}

	@Override
	public SpawnGroupData finalizeSpawn(ServerLevelAccessor mundo, DifficultyInstance dificuldade, EntitySpawnReason motivo, SpawnGroupData dados) {
		if (motivo == EntitySpawnReason.NATURAL || motivo == EntitySpawnReason.CHUNK_GENERATION)
			selvagemNatural = true;
		garantirIndividuo(mundo.getRandom());
		return super.finalizeSpawn(mundo, dificuldade, motivo, dados);
	}

	@Override
	protected void addAdditionalSaveData(ValueOutput saida) {
		super.addAdditionalSaveData(saida);
		garantirIndividuo(getRandom());
		saida.putInt("galeto_nivel", nivel);
		saida.putString("galeto_sexo", String.valueOf(sexo));
		saida.putIntArray("galeto_ivs", ivs);
		// a Rinha não sobrevive ao salvamento: o Galeto volta com a IA ligada (ver readAdditionalSaveData)
		saida.putBoolean("galeto_em_rinha", emRinha);
		saida.putLong("galeto_espera_captura", esperaCapturaAte);
		saida.putBoolean("galeto_selvagem_natural", selvagemNatural);
		if (dono != null) {
			saida.putString("galeto_dono", dono.toString());
			saida.putString("galeto_id_guardado", idGuardado.toString());
		}
	}

	@Override
	protected void readAdditionalSaveData(ValueInput entrada) {
		super.readAdditionalSaveData(entrada);
		nivel = entrada.getIntOr("galeto_nivel", 0);
		String s = entrada.getStringOr("galeto_sexo", "?");
		sexo = s.isEmpty() ? '?' : s.charAt(0);
		ivs = entrada.getIntArray("galeto_ivs").orElse(new int[0]);
		if (ivs.length != Atributo.values().length)
			nivel = 0;   // dados incompletos: gera de novo na próxima consulta
		esperaCapturaAte = entrada.getLongOr("galeto_espera_captura", 0L);
		selvagemNatural = entrada.getBooleanOr("galeto_selvagem_natural", false);
		String d = entrada.getStringOr("galeto_dono", "");
		if (!d.isEmpty()) {
			dono = java.util.UUID.fromString(d);
			idGuardado = java.util.UUID.fromString(entrada.getStringOr("galeto_id_guardado", d));
		}
		if (entrada.getBooleanOr("galeto_em_rinha", false))
			setNoAi(false);   // salvo no meio de uma Rinha (as sessões ficam só na memória do servidor)
	}

	/** Companheiro: invulnerável fora da Rinha (regra treinador.companheiro_rev9). */
	@Override
	public boolean hurtServer(net.minecraft.server.level.ServerLevel mundo, DamageSource fonte, float dano) {
		if (companheiro())
			return false;
		return super.hurtServer(mundo, fonte, dano);
	}

	/** Companheiro: segue o dono, teleporta se passar de 24 blocos e volta à equipe se o dono não estiver por perto. */
	@Override
	protected void customServerAiStep(net.minecraft.server.level.ServerLevel mundo) {
		super.customServerAiStep(mundo);
		if (!companheiro())
			return;
		Player d = mundo.getPlayerByUUID(dono);
		if (d == null) {
			discard();
			return;
		}
		double dist = distanceTo(d);
		if (dist > 24) {
			snapTo(d.getX(), d.getY(), d.getZ(), getYRot(), getXRot());
			getNavigation().stop();
		} else if (dist > 4) {
			getNavigation().moveTo(d, 1.1);
		} else {
			getNavigation().stop();
		}
	}

	@Override
	protected InteractionResult mobInteract(Player jogador, InteractionHand mao) {
		if (companheiro() && jogador.getUUID().equals(dono) && jogador.getItemInHand(mao).is(br.galetocraft.registro.ModItens.PENA_DE_CAPTURA)) {
			if (jogador instanceof net.minecraft.server.level.ServerPlayer sp)
				br.galetocraft.treinador.Companheiros.recolher(sp, true);
			return InteractionResult.SUCCESS;
		}
		if (!jogador.getItemInHand(mao).isEmpty())
			return super.mobInteract(jogador, mao);
		if (!level().isClientSide())
			jogador.displayClientMessage(fichaDoIndividuo(), false);
		return InteractionResult.SUCCESS;
	}

	/** Linha de ficha do indivíduo: espécie, nível, sexo, HP no nível e IVs. */
	public Component fichaDoIndividuo() {
		Optional<Especie> op = fichaDaEspecie();
		if (op.isEmpty())
			return Component.literal(especie() + ": espécie fora do Galetário vigente");
		Especie e = op.get();
		String simbolo = switch (sexo()) {
			case 'M' -> "♂";
			case 'F' -> "♀";
			default -> "";
		};
		// HP final: HP nominal do nível com o IV de HP (EV 0 e peso neutro ao aparecer)
		int hp = Progressao.atributoFinal(Atributo.HP, e.atributo(Atributo.HP), nivel(), ivs()[Atributo.HP.ordinal()], 0, Progressao.PESO_NEUTRO);
		return Component.literal(String.format("#%03d %s %s Nv%d · HP %d · %s · IVs %s", e.numero(), e.nome(), simbolo, nivel(),
						hp, e.raridade(), Arrays.toString(ivs())))
				.withStyle(ChatFormatting.GOLD);
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
