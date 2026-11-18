package br.galetocraft.comando;

import br.galetocraft.entidade.GaloEntity;
import br.galetocraft.nucleo.dados.Atributo;
import br.galetocraft.nucleo.dados.Especie;
import br.galetocraft.nucleo.dados.Galetario;
import br.galetocraft.nucleo.dados.Golpe;
import br.galetocraft.nucleo.rinha.Combatente;
import br.galetocraft.nucleo.rinha.Equipe;
import br.galetocraft.nucleo.rinha.Rinha;
import br.galetocraft.nucleo.rinha.Simulador;
import br.galetocraft.nucleo.regras.MiraAnatomica;
import br.galetocraft.rinha.EquipesTemporarias;
import br.galetocraft.rinha.GerenciadorRinhas;
import com.mojang.brigadier.CommandDispatcher;
import com.mojang.brigadier.arguments.IntegerArgumentType;
import com.mojang.brigadier.arguments.StringArgumentType;
import com.mojang.brigadier.context.CommandContext;
import com.mojang.brigadier.suggestion.SuggestionProvider;
import net.minecraft.ChatFormatting;
import net.minecraft.commands.CommandSourceStack;
import net.minecraft.commands.Commands;
import net.minecraft.commands.SharedSuggestionProvider;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import com.mojang.brigadier.exceptions.CommandSyntaxException;
import java.util.ArrayList;
import java.util.Comparator;

import java.text.Normalizer;
import java.util.List;
import java.util.Locale;
import java.util.Optional;
import java.util.stream.Collectors;

/**
 * Comandos de consulta e teste do Galetocraft, sobre o núcleo de regras:
 * <ul>
 * <li>{@code /galetocraft base}: revisão e contagens da base vigente embutida no mod.</li>
 * <li>{@code /galetocraft ficha <espécie>}: ficha vigente (número ou nome sem acento, ex.: 22 ou sirenoco).</li>
 * <li>{@code /galetocraft rinha <espécie> <espécie> [nível]}: Rinha 1×1 simulada pelo motor, com o Histórico da Rinha.</li>
 * <li>{@code /galetocraft duelo <espécie> <espécie> [rinhas]}: taxa de vitórias em N Rinhas simuladas (operadores).</li>
 * <li>{@code /galetocraft equipe [a] [b] [c]}: mostra ou define a equipe de teste do jogador (até haver captura).</li>
 * <li>{@code /galetocraft desafiar}: começa uma Rinha contra o Galeto selvagem mais próximo (até 10 blocos).</li>
 * <li>{@code /galetocraft acao ...}: ações do menu clicável da Rinha (golpe, trocar, mira, guarda, pena, fugir).</li>
 * </ul>
 * A Rinha simulada usa a IA básica dos dois lados. Passivas e efeitos especiais dos golpes ainda não estão no motor.
 */
public final class ComandoGaletocraft {
	private static final SuggestionProvider<CommandSourceStack> REGIOES = (ctx, b) ->
			SharedSuggestionProvider.suggest(List.of("neutra", "cabeca_crina", "asas", "pernas_garras", "tronco"), b);
	private static final SuggestionProvider<CommandSourceStack> ESPECIES = (ctx, b) ->
			SharedSuggestionProvider.suggest(Galetario.padrao().especies().stream().map(e -> idTecnico(e.nome())), b);

	private ComandoGaletocraft() {
	}

	public static void registrar(CommandDispatcher<CommandSourceStack> d) {
		d.register(Commands.literal("galetocraft")
				.then(Commands.literal("base").executes(ComandoGaletocraft::base))
				.then(Commands.literal("ficha")
						.then(Commands.argument("especie", StringArgumentType.word()).suggests(ESPECIES).executes(ComandoGaletocraft::ficha)))
				.then(Commands.literal("rinha")
						.then(Commands.argument("a", StringArgumentType.word()).suggests(ESPECIES)
								.then(Commands.argument("b", StringArgumentType.word()).suggests(ESPECIES)
										.executes(c -> rinha(c, 50))
										.then(Commands.argument("nivel", IntegerArgumentType.integer(50, 100))
												.executes(c -> rinha(c, IntegerArgumentType.getInteger(c, "nivel")))))))
				.then(Commands.literal("equipe").executes(ComandoGaletocraft::mostrarEquipe)
						.then(Commands.argument("a", StringArgumentType.word()).suggests(ESPECIES).executes(c -> definirEquipe(c, 1))
								.then(Commands.argument("b", StringArgumentType.word()).suggests(ESPECIES).executes(c -> definirEquipe(c, 2))
										.then(Commands.argument("c", StringArgumentType.word()).suggests(ESPECIES).executes(c -> definirEquipe(c, 3))))))
				.then(Commands.literal("desafiar").executes(ComandoGaletocraft::desafiar))
				.then(Commands.literal("acao")
						.then(Commands.literal("golpe").then(Commands.argument("i", IntegerArgumentType.integer(0, 4))
								.executes(c -> acao(c, p -> GerenciadorRinhas.golpe(p, IntegerArgumentType.getInteger(c, "i"))))))
						.then(Commands.literal("trocar").then(Commands.argument("i", IntegerArgumentType.integer(0, 2))
								.executes(c -> acao(c, p -> GerenciadorRinhas.trocar(p, IntegerArgumentType.getInteger(c, "i"))))))
						.then(Commands.literal("mira").then(Commands.argument("regiao", StringArgumentType.word()).suggests(REGIOES)
								.executes(c -> acao(c, p -> regiao(c).ifPresent(r -> GerenciadorRinhas.mira(p, r))))))
						.then(Commands.literal("guarda").then(Commands.argument("regiao", StringArgumentType.word()).suggests(REGIOES)
								.executes(c -> acao(c, p -> GerenciadorRinhas.guarda(p, regiao(c).orElse(null))))))
						.then(Commands.literal("pena").executes(c -> acao(c, GerenciadorRinhas::alternarPena)))
						.then(Commands.literal("fugir").executes(c -> acao(c, GerenciadorRinhas::fugir))))
				.then(Commands.literal("duelo").requires(Commands.hasPermission(Commands.LEVEL_GAMEMASTERS))
						.then(Commands.argument("a", StringArgumentType.word()).suggests(ESPECIES)
								.then(Commands.argument("b", StringArgumentType.word()).suggests(ESPECIES)
										.executes(c -> duelo(c, 200))
										.then(Commands.argument("rinhas", IntegerArgumentType.integer(1, 2000))
												.executes(c -> duelo(c, IntegerArgumentType.getInteger(c, "rinhas"))))))));
	}

	private static int base(CommandContext<CommandSourceStack> c) {
		Galetario g = Galetario.padrao();
		int golpes = g.especies().stream().mapToInt(e -> e.golpes().size()).sum();
		enviar(c, Component.literal("Galetocraft — base vigente rev. " + g.revisaoBase() + ": " + g.especies().size()
				+ " espécies, " + golpes + " golpes vinculados").withStyle(ChatFormatting.GOLD));
		return 1;
	}

	private static int ficha(CommandContext<CommandSourceStack> c) {
		Optional<Especie> op = especie(StringArgumentType.getString(c, "especie"));
		if (op.isEmpty())
			return falhar(c);
		Especie e = op.get();
		enviar(c, Component.literal(String.format("#%03d %s — %s, %s", e.numero(), e.nome(), e.raridade(),
				e.elementos().stream().map(x -> x.nome()).collect(Collectors.joining(" + ")))).withStyle(ChatFormatting.GOLD));
		enviar(c, Component.literal(String.format("Nível 50: HP %d · Atq.F %d · Def.F %d · Atq.M %d · Def.M %d · Vel %d (total %d)",
				e.atributo(Atributo.HP), e.atributo(Atributo.ATAQUE_FISICO), e.atributo(Atributo.DEFESA_FISICA),
				e.atributo(Atributo.ATAQUE_MAGICO), e.atributo(Atributo.DEFESA_MAGICA), e.atributo(Atributo.VELOCIDADE), e.total())));
		enviar(c, Component.literal("Passiva: " + e.passiva() + " · Peso: " + e.pesoKg() + " kg"
				+ (e.reproduz() ? " · Alas: " + String.join("/", e.alas()) : " · não reproduz")));
		for (Golpe g : e.originais())
			enviar(c, Component.literal(String.format("  %s (%s, %s%s, E%d)", g.nome(), g.elemento().nome(),
					g.categoria().name().toLowerCase(Locale.ROOT), g.poder() == null ? "" : ", P" + g.poder(), g.energia()))
					.withStyle(ChatFormatting.GRAY));
		return 1;
	}

	private static int rinha(CommandContext<CommandSourceStack> c, int nivel) {
		Optional<Especie> a = especie(StringArgumentType.getString(c, "a"));
		Optional<Especie> b = especie(StringArgumentType.getString(c, "b"));
		if (a.isEmpty() || b.isEmpty())
			return falhar(c);
		long semente = c.getSource().getLevel().getGameTime() ^ System.nanoTime();
		Rinha r = Simulador.rodar(Galetario.padrao(), new Equipe("Equipe A", List.of(Combatente.padrao(a.get(), nivel))),
				new Equipe("Equipe B", List.of(Combatente.padrao(b.get(), nivel))), semente);
		List<String> h = r.historico();
		int inicio = Math.max(0, h.size() - 40);
		if (inicio > 0)
			enviar(c, Component.literal("(… " + inicio + " linhas anteriores)").withStyle(ChatFormatting.DARK_GRAY));
		for (String linha : h.subList(inicio, h.size()))
			enviar(c, Component.literal(linha).withStyle(linha.startsWith("—") ? ChatFormatting.YELLOW : ChatFormatting.WHITE));
		return 1;
	}

	private static int duelo(CommandContext<CommandSourceStack> c, int rinhas) {
		Optional<Especie> a = especie(StringArgumentType.getString(c, "a"));
		Optional<Especie> b = especie(StringArgumentType.getString(c, "b"));
		if (a.isEmpty() || b.isEmpty())
			return falhar(c);
		Simulador.Resultado res = Simulador.duelo(Galetario.padrao(), a.get(), b.get(), 50, rinhas, System.nanoTime());
		enviar(c, Component.literal(String.format("%s × %s (nível 50, %d Rinhas): %d × %d, %d empates, %.1f rodadas em média",
				a.get().nome(), b.get().nome(), res.total(), res.vitoriasA(), res.vitoriasB(), res.empates(), res.mediaRodadas()))
				.withStyle(ChatFormatting.GOLD));
		return 1;
	}

	private static int mostrarEquipe(CommandContext<CommandSourceStack> c) throws CommandSyntaxException {
		ServerPlayer p = c.getSource().getPlayerOrException();
		enviar(c, Component.literal("Sua equipe de teste: " + EquipesTemporarias.equipe(p).stream().map(Especie::nome)
				.collect(Collectors.joining(", ")) + " (nível 50, golpes de origem)").withStyle(ChatFormatting.GOLD));
		return 1;
	}

	private static int definirEquipe(CommandContext<CommandSourceStack> c, int n) throws CommandSyntaxException {
		ServerPlayer p = c.getSource().getPlayerOrException();
		List<Especie> lista = new ArrayList<>();
		for (String arg : List.of("a", "b", "c").subList(0, n)) {
			Optional<Especie> e = especie(StringArgumentType.getString(c, arg));
			if (e.isEmpty())
				return falhar(c);
			lista.add(e.get());
		}
		EquipesTemporarias.definir(p, lista);
		return mostrarEquipe(c);
	}

	private static int desafiar(CommandContext<CommandSourceStack> c) throws CommandSyntaxException {
		ServerPlayer p = c.getSource().getPlayerOrException();
		if (GerenciadorRinhas.emRinha(p)) {
			c.getSource().sendFailure(Component.literal("Você já está em uma Rinha."));
			return 0;
		}
		Optional<GaloEntity> alvo = p.level().getEntitiesOfClass(GaloEntity.class, p.getBoundingBox().inflate(10),
						g -> g.isAlive() && !g.emRinha() && g.fichaDaEspecie().isPresent())
				.stream().min(Comparator.comparingDouble(g -> g.distanceTo(p)));
		if (alvo.isEmpty()) {
			c.getSource().sendFailure(Component.literal("Nenhum Galeto selvagem a até 10 blocos."));
			return 0;
		}
		GerenciadorRinhas.iniciar(p, alvo.get());
		return 1;
	}

	private static int acao(CommandContext<CommandSourceStack> c, java.util.function.Consumer<ServerPlayer> f) throws CommandSyntaxException {
		f.accept(c.getSource().getPlayerOrException());
		return 1;
	}

	private static Optional<MiraAnatomica.Regiao> regiao(CommandContext<CommandSourceStack> c) {
		String r = StringArgumentType.getString(c, "regiao").toUpperCase(Locale.ROOT);
		try {
			return Optional.of(MiraAnatomica.Regiao.valueOf(r));
		} catch (IllegalArgumentException ex) {
			return Optional.empty();
		}
	}

	private static Optional<Especie> especie(String texto) {
		Galetario g = Galetario.padrao();
		try {
			return Optional.of(g.especie(Integer.parseInt(texto)));
		} catch (NumberFormatException ex) {
			return g.especies().stream().filter(e -> idTecnico(e.nome()).equals(idTecnico(texto))).findFirst();
		} catch (IllegalArgumentException ex) {
			return Optional.empty();
		}
	}

	/** Nome sem acento e em minúsculas (ex.: "Sirenocó" → "sirenoco"), para digitar no comando. */
	static String idTecnico(String nome) {
		return Normalizer.normalize(nome, Normalizer.Form.NFD).replaceAll("\\p{M}", "").toLowerCase(Locale.ROOT);
	}

	private static void enviar(CommandContext<CommandSourceStack> c, Component texto) {
		c.getSource().sendSuccess(() -> texto, false);
	}

	private static int falhar(CommandContext<CommandSourceStack> c) {
		c.getSource().sendFailure(Component.literal("Espécie não encontrada. Use o número (1–23) ou o nome sem acento."));
		return 0;
	}
}
