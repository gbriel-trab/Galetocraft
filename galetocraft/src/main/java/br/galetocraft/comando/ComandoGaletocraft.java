package br.galetocraft.comando;

import br.galetocraft.nucleo.dados.Atributo;
import br.galetocraft.nucleo.dados.Especie;
import br.galetocraft.nucleo.dados.Galetario;
import br.galetocraft.nucleo.dados.Golpe;
import br.galetocraft.nucleo.rinha.Combatente;
import br.galetocraft.nucleo.rinha.Equipe;
import br.galetocraft.nucleo.rinha.Rinha;
import br.galetocraft.nucleo.rinha.Simulador;
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
 * </ul>
 * A Rinha simulada usa a IA básica dos dois lados. Passivas e efeitos especiais dos golpes ainda não estão no motor.
 */
public final class ComandoGaletocraft {
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
