package br.galetocraft.mundo;

import br.galetocraft.GaletocraftMod;
import br.galetocraft.entidade.GaloEntity;
import br.galetocraft.nucleo.dados.Elemento;
import br.galetocraft.nucleo.dados.Galetario;
import br.galetocraft.registro.ModAnexos;
import br.galetocraft.registro.ModEntidades;
import br.galetocraft.treinador.GaletoGuardado;
import br.galetocraft.treinador.Treinador;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import net.fabricmc.fabric.api.biome.v1.BiomeModifications;
import net.fabricmc.fabric.api.biome.v1.BiomeSelectionContext;
import net.fabricmc.fabric.api.biome.v1.BiomeSelectors;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerTickEvents;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Holder;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;
import net.minecraft.resources.ResourceKey;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.tags.TagKey;
import net.minecraft.util.RandomSource;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntitySpawnReason;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.SpawnPlacementTypes;
import net.minecraft.world.entity.SpawnPlacements;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.ServerLevelAccessor;
import net.minecraft.world.level.biome.Biome;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraft.world.phys.AABB;

import java.util.ArrayList;
import java.util.EnumSet;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.function.Predicate;

/**
 * Aparecimento dos Galetos no mundo (regra mundo_aparecimento, rev. 9 da base).
 * <ul>
 * <li><b>Comuns, Raros e Épicos:</b> aparecimento natural nos biomas da regra (biomas oficiais do Mestre do elemento e
 * habitats das fichas), com peso por raridade (6/2/1), grupo e horário; no máximo 6 selvagens a até 64 blocos de cada
 * jogador.</li>
 * <li><b>Iniciais e Míticos:</b> só como encontros raros (1% por jogador a cada período elegível: manhã para os diurnos,
 * anoitecer para os noturnos e os de qualquer hora; a cada minuto de tempestade para os que dependem dela), no máximo 1
 * ativo por jogador.</li>
 * <li><b>Quetzacocó:</b> único por mundo, extremamente raro (0,2% por minuto de tempestade por jogador elegível), em selva
 * ou montanha alta, só para quem tem Galetos dos 6 elementos; nível 70; aviso global no chat; foge no fim da tempestade.</li>
 * <li><b>Nível:</b> todo selvagem novo sorteia de 1 a 70 (em {@link GaloEntity}).</li>
 * </ul>
 * Só aparecem as espécies que já têm modelo no mod; as demais ficam na regra até o modelo existir.
 */
public final class Aparecimento {
	private static final List<Regra> REGRAS = new ArrayList<>();
	private static final Map<UUID, UUID> ENCONTRO_ATIVO = new ConcurrentHashMap<>();
	private static double chanceEncontro;
	private static int limite, raio;
	private static JsonObject quetzacoco;
	private static UUID quetzacocoAtivo;
	private static final Set<Elemento> SEIS = EnumSet.of(Elemento.FOGO, Elemento.AGUA, Elemento.PLANTA, Elemento.TERRA, Elemento.AR, Elemento.ELETRICO);

	/** Uma linha da tabela de espécies da regra. */
	public record Regra(int numero, String modo, List<String> biomas, String horario, String condicao, int minimo, int maximo, Integer peso) {
		boolean soEmTempestade() {
			return condicao != null && condicao.startsWith("só durante tempestade");
		}
	}

	private Aparecimento() {
	}

	public static List<Regra> regras() {
		return List.copyOf(REGRAS);
	}

	public static void registrar() {
		JsonObject m = Galetario.padrao().regraObjeto("mundo_aparecimento");
		for (JsonElement x : m.getAsJsonArray("especies")) {
			JsonObject o = x.getAsJsonObject();
			List<String> biomas = new ArrayList<>();
			o.getAsJsonArray("biomas").forEach(b -> biomas.add(b.getAsString()));
			REGRAS.add(new Regra(o.get("numero").getAsInt(), o.get("modo").getAsString(), biomas, o.get("horario").getAsString(),
					o.get("condicao").isJsonNull() ? null : o.get("condicao").getAsString(),
					o.getAsJsonArray("grupo").get(0).getAsInt(), o.getAsJsonArray("grupo").get(1).getAsInt(),
					o.get("peso").isJsonNull() ? null : o.get("peso").getAsInt()));
		}
		chanceEncontro = m.getAsJsonObject("encontros_raros").get("chance").getAsDouble();
		limite = m.getAsJsonObject("limite").get("selvagens_por_jogador").getAsInt();
		raio = m.getAsJsonObject("limite").get("raio_blocos").getAsInt();
		quetzacoco = m.getAsJsonObject("quetzacoco");

		for (Regra r : REGRAS)
			if (r.modo().equals("comum"))
				ModEntidades.porEspecie(r.numero()).ifPresent(t -> registrarNatural(t, r));
		ServerTickEvents.END_SERVER_TICK.register(Aparecimento::tick);
	}

	private static <T extends GaloEntity> void registrarNatural(EntityType<T> tipo, Regra r) {
		List<String> superficie = r.biomas().stream().filter(b -> !b.equals("minecraft:basalt_deltas")).toList();
		BiomeModifications.addSpawn(seletor(superficie), MobCategory.CREATURE, tipo, r.peso(), r.minimo(), r.maximo());
		if (r.biomas().contains("minecraft:basalt_deltas"))   // Salambrasa: Deltas de Basalto com peso 1
			BiomeModifications.addSpawn(seletor(List.of("minecraft:basalt_deltas")), MobCategory.CREATURE, tipo, 1, 1, 1);
		SpawnPlacements.register(tipo, SpawnPlacementTypes.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES,
				(t, nivel, motivo, pos, rng) -> podeAparecer(t, r, nivel, motivo, pos, rng));
	}

	private static Predicate<BiomeSelectionContext> seletor(List<String> biomas) {
		Predicate<BiomeSelectionContext> p = c -> false;
		for (String b : biomas)
			p = p.or(b.startsWith("c:") ? BiomeSelectors.tag(TagKey.create(Registries.BIOME, Identifier.parse(b)))
					: BiomeSelectors.includeByKey(ResourceKey.create(Registries.BIOME, Identifier.parse(b))));
		return p;
	}

	/** Bloco válido, horário e condição da espécie, e o limite de selvagens perto do jogador. */
	private static boolean podeAparecer(EntityType<? extends Mob> tipo, Regra r, ServerLevelAccessor nivel, EntitySpawnReason motivo,
			BlockPos pos, RandomSource rng) {
		if (!Mob.checkMobSpawnRules(tipo, nivel, motivo, pos, rng))
			return false;
		ServerLevel l = nivel.getLevel();
		if (!horarioOk(r.horario(), l, pos) || (r.soEmTempestade() && !l.isThundering()))
			return false;
		return abaixoDoLimite(l, pos);
	}

	private static boolean horarioOk(String horario, ServerLevel l, BlockPos pos) {
		return switch (horario) {
			case "dia" -> l.isBrightOutside();
			case "noite" -> l.isDarkOutside();
			case "noite_ou_subterraneo" -> l.isDarkOutside() || !l.canSeeSky(pos);
			default -> true;
		};
	}

	private static boolean abaixoDoLimite(ServerLevel l, BlockPos pos) {
		Player p = l.getNearestPlayer(pos.getX(), pos.getY(), pos.getZ(), raio, false);
		if (p == null)
			return true;
		return l.getEntitiesOfClass(GaloEntity.class, new AABB(p.blockPosition()).inflate(raio), g -> !g.companheiro()).size() < limite;
	}

	public static boolean biomaCombina(ServerLevel l, BlockPos pos, List<String> biomas) {
		Holder<Biome> b = l.getBiome(pos);
		for (String id : biomas)
			if (id.startsWith("c:") ? b.is(TagKey.create(Registries.BIOME, Identifier.parse(id)))
					: b.is(ResourceKey.create(Registries.BIOME, Identifier.parse(id))))
				return true;
		return false;
	}

	// ------------------------------------------------------------------ encontros raros e Quetzacocó
	private static void tick(MinecraftServer s) {
		for (ServerLevel l : s.getAllLevels()) {
			long hora = l.getDayTime() % 24000;
			boolean manha = hora == 1000, anoitecer = hora == 13000;
			boolean minutoDeTempestade = l.isThundering() && l.getGameTime() % 1200 == 0;
			if (quetzacocoAtivo != null && !l.isThundering())
				fugaDoQuetzacoco(l);
			if (!manha && !anoitecer && !minutoDeTempestade)
				continue;
			for (ServerPlayer p : List.copyOf(l.players())) {
				encontro(l, p, manha, anoitecer, minutoDeTempestade);
				if (minutoDeTempestade)
					tentarQuetzacoco(s, l, p);
			}
		}
	}

	private static void encontro(ServerLevel l, ServerPlayer p, boolean manha, boolean anoitecer, boolean tempestade) {
		UUID ativo = ENCONTRO_ATIVO.get(p.getUUID());
		if (ativo != null && l.getEntity(ativo) instanceof GaloEntity g && g.isAlive())
			return;
		ENCONTRO_ATIVO.remove(p.getUUID());
		BlockPos pos = p.blockPosition();
		for (Regra r : REGRAS) {
			if (!r.modo().equals("encontro") || !biomaCombina(l, pos, r.biomas()))
				continue;
			boolean momento = r.soEmTempestade() ? tempestade
					: (manha && !r.horario().equals("noite")) || (anoitecer && !r.horario().equals("dia"));
			if (!momento || (r.condicao() != null && r.condicao().equals("só com chuva") && !l.isRaining()))
				continue;
			double chance = chanceEncontro;
			if (r.condicao() != null && r.condicao().startsWith("mais provável (×2)") && l.isRaining())
				chance *= 2;
			if (l.getRandom().nextDouble() >= chance)
				continue;
			Optional<EntityType<? extends GaloEntity>> tipo = ModEntidades.porEspecie(r.numero());
			if (tipo.isEmpty())
				continue;
			gerarPerto(l, p, tipo.get()).ifPresent(g -> ENCONTRO_ATIVO.put(p.getUUID(), g.getUUID()));
			return;
		}
	}

	/** Treinador com Galetos (equipe ou reservas) dos 6 elementos básicos. */
	public static boolean temSeisElementos(Player p) {
		Treinador t = ModAnexos.treinador(p);
		Set<Elemento> vistos = EnumSet.noneOf(Elemento.class);
		for (List<GaletoGuardado> l : List.of(t.equipe(), t.reservas()))
			l.forEach(g -> vistos.addAll(g.ficha().elementos()));
		return vistos.containsAll(SEIS);
	}

	private static void tentarQuetzacoco(MinecraftServer s, ServerLevel l, ServerPlayer p) {
		if (quetzacocoAtivo != null || Boolean.TRUE.equals(s.overworld().getAttached(ModAnexos.QUETZACOCO_CAPTURADO)))
			return;
		List<String> biomas = new ArrayList<>();
		quetzacoco.getAsJsonArray("biomas").forEach(b -> biomas.add(b.getAsString()));
		if (!biomaCombina(l, p.blockPosition(), biomas) || !temSeisElementos(p))
			return;
		if (l.getRandom().nextDouble() >= quetzacoco.get("chance").getAsDouble())
			return;
		Optional<EntityType<? extends GaloEntity>> tipo = ModEntidades.porEspecie(23);
		if (tipo.isEmpty()) {
			GaletocraftMod.LOGGER.info("Quetzacocó sorteado para {}, mas a espécie ainda não tem modelo no mod", p.getName().getString());
			return;
		}
		gerarPerto(l, p, tipo.get()).ifPresent(g -> {
			g.definirNivel(quetzacoco.get("nivel").getAsInt());
			quetzacocoAtivo = g.getUUID();
			s.getPlayerList().broadcastSystemMessage(Component.literal(quetzacoco.get("mensagem_global").getAsString())
					.withStyle(ChatFormatting.LIGHT_PURPLE, ChatFormatting.BOLD), false);
		});
	}

	private static void fugaDoQuetzacoco(ServerLevel l) {
		Entity e = l.getEntity(quetzacocoAtivo);
		if (e instanceof GaloEntity g && !g.emRinha()) {
			g.discard();
			l.getServer().getPlayerList().broadcastSystemMessage(Component.literal("A tempestade passou e o Quetzacocó partiu com os ventos.")
					.withStyle(ChatFormatting.GRAY), false);
		}
		if (e == null || !e.isAlive() || e.isRemoved())
			quetzacocoAtivo = null;
	}

	/** Captura do Quetzacocó: marca o mundo para ele nunca mais aparecer. */
	public static void aoCapturar(MinecraftServer s, int especie) {
		if (especie == 23) {
			s.overworld().setAttached(ModAnexos.QUETZACOCO_CAPTURADO, true);
			quetzacocoAtivo = null;
		}
	}

	/** Gera um Galeto a 8–16 blocos do jogador, num chão firme com espaço livre. */
	private static <T extends GaloEntity> Optional<T> gerarPerto(ServerLevel l, ServerPlayer p, EntityType<T> tipo) {
		RandomSource rng = l.getRandom();
		for (int tentativa = 0; tentativa < 16; tentativa++) {
			double ang = rng.nextDouble() * Math.PI * 2, dist = 8 + rng.nextDouble() * 8;
			int x = (int) Math.floor(p.getX() + Math.cos(ang) * dist), z = (int) Math.floor(p.getZ() + Math.sin(ang) * dist);
			for (int y = p.getBlockY() + 8; y >= p.getBlockY() - 8; y--) {
				BlockPos pos = new BlockPos(x, y, z);
				if (l.getBlockState(pos.below()).isSolid() && l.isEmptyBlock(pos) && l.isEmptyBlock(pos.above())) {
					T g = tipo.create(l, EntitySpawnReason.EVENT);
					if (g == null)
						return Optional.empty();
					g.snapTo(x + 0.5, y, z + 0.5, rng.nextFloat() * 360, 0);
					g.finalizeSpawn(l, l.getCurrentDifficultyAt(pos), EntitySpawnReason.EVENT, null);
					g.marcarSelvagemNatural();
					l.addFreshEntity(g);
					return Optional.of(g);
				}
			}
		}
		return Optional.empty();
	}
}
