package br.galetocraft.rinha;

import br.galetocraft.entidade.GaloEntity;
import br.galetocraft.nucleo.dados.Especie;
import br.galetocraft.nucleo.dados.Galetario;
import br.galetocraft.nucleo.dados.Golpe;
import br.galetocraft.nucleo.regras.Energia;
import br.galetocraft.nucleo.regras.MiraAnatomica;
import br.galetocraft.nucleo.regras.PenaDeRitmo;
import br.galetocraft.nucleo.rinha.Combatente;
import br.galetocraft.nucleo.rinha.Decisao;
import br.galetocraft.nucleo.rinha.Equipe;
import br.galetocraft.nucleo.rinha.IaBasica;
import br.galetocraft.nucleo.rinha.Rinha;
import net.minecraft.ChatFormatting;
import net.minecraft.network.chat.ClickEvent;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.HoverEvent;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.server.level.ServerPlayer;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Rinhas jogáveis contra Galetos selvagens, com o motor do núcleo e um menu clicável no chat.
 * <p>
 * O menu segue a padronização das interfaces da Rinha: Galetos / Combate / Itens / Fugir, além das escolhas
 * secretas da Mira Anatômica (região mirada e Guarda) e da Pena de Ritmo. Os Itens aparecem desativados porque
 * os itens da Rinha ainda são candidatos.
 * <p>
 * Até existir captura e equipe persistente, a equipe do jogador é a equipe temporária de
 * {@link EquipesTemporarias}, no nível 50, com os 5 golpes de origem.
 */
public final class GerenciadorRinhas {
	public static final double DISTANCIA_MAXIMA = 32.0;
	private static final Map<UUID, Sessao> SESSOES = new ConcurrentHashMap<>();

	private GerenciadorRinhas() {
	}

	private static final class Sessao {
		final Rinha rinha;
		final GaloEntity selvagem;
		final IaBasica ia;
		MiraAnatomica.Regiao mira = MiraAnatomica.Regiao.TRONCO;
		MiraAnatomica.Regiao guarda;
		boolean usarPena;
		int historicoEnviado;

		Sessao(Rinha rinha, GaloEntity selvagem, long semente) {
			this.rinha = rinha;
			this.selvagem = selvagem;
			this.ia = new IaBasica(semente);
		}
	}

	public static boolean emRinha(ServerPlayer p) {
		return SESSOES.containsKey(p.getUUID());
	}

	/** Começa uma Rinha entre a equipe temporária do jogador e o Galeto selvagem. */
	public static void iniciar(ServerPlayer jogador, GaloEntity selvagem) {
		Galetario g = Galetario.padrao();
		List<Especie> equipe = EquipesTemporarias.equipe(jogador);
		Especie especieSelvagem = selvagem.fichaDaEspecie().orElseThrow();
		List<Combatente> meus = equipe.stream().map(e -> Combatente.padrao(e, GaloEntity.NIVEL_PADRAO)).toList();
		long semente = jogador.level().getGameTime() ^ selvagem.getUUID().getLeastSignificantBits();
		Rinha r = new Rinha(g, new Equipe(jogador.getName().getString(), meus),
				new Equipe("Selvagem", List.of(Combatente.padrao(especieSelvagem, selvagem.nivel()))), semente);
		selvagem.emRinha(true);
		Sessao s = new Sessao(r, selvagem, semente);
		SESSOES.put(jogador.getUUID(), s);
		enviarHistorico(jogador, s);
		enviarMenu(jogador, s);
	}

	public static void golpe(ServerPlayer p, int indice) {
		Sessao s = sessao(p);
		if (s == null) return;
		List<Golpe> golpes = s.rinha.equipeA().ativo().golpes();
		if (indice < 0 || indice >= golpes.size()) return;
		Golpe golpe = golpes.get(indice);
		PenaDeRitmo.Canto canto = canto(s, golpe);
		if (custo(golpe, canto) > s.rinha.equipeA().ativo().energia()) {
			p.displayClientMessage(Component.literal("Energia insuficiente para " + golpe.nome()).withStyle(ChatFormatting.RED), false);
			return;
		}
		s.usarPena = false;
		jogar(p, s, new Decisao(new Decisao.UsarGolpe(golpe, golpe.danoDireto() ? s.mira : null, canto), s.guarda));
	}

	/** Canto da Pena de Ritmo que o golpe usaria: Ofensivo nos golpes de dano, de Suporte nos demais (não na Concentração). */
	private static PenaDeRitmo.Canto canto(Sessao s, Golpe golpe) {
		if (!s.usarPena || !s.rinha.equipeA().pena().disponivel() || golpe.concentracao())
			return null;
		return golpe.danoDireto() ? PenaDeRitmo.Canto.OFENSIVO : PenaDeRitmo.Canto.SUPORTE;
	}

	private static int custo(Golpe golpe, PenaDeRitmo.Canto canto) {
		return canto == PenaDeRitmo.Canto.SUPORTE ? Energia.custoComCantoSuporte(golpe.energia()) : golpe.energia();
	}

	public static void trocar(ServerPlayer p, int indice) {
		Sessao s = sessao(p);
		if (s == null) return;
		Equipe eu = s.rinha.equipeA();
		if (indice == eu.indiceAtivo() || indice < 0 || indice >= eu.galetos().size() || eu.galetos().get(indice).derrotado()) return;
		boolean revezamento = s.usarPena && eu.pena().disponivel();
		s.usarPena = false;
		jogar(p, s, new Decisao(new Decisao.Trocar(indice, revezamento), s.guarda));
	}

	public static void mira(ServerPlayer p, MiraAnatomica.Regiao r) {
		Sessao s = sessao(p);
		if (s == null) return;
		s.mira = r;
		enviarMenu(p, s);
	}

	public static void guarda(ServerPlayer p, MiraAnatomica.Regiao r) {
		Sessao s = sessao(p);
		if (s == null) return;
		s.guarda = r;
		enviarMenu(p, s);
	}

	public static void alternarPena(ServerPlayer p) {
		Sessao s = sessao(p);
		if (s == null) return;
		s.usarPena = !s.usarPena && s.rinha.equipeA().pena().disponivel();
		enviarMenu(p, s);
	}

	public static void fugir(ServerPlayer p) {
		Sessao s = sessao(p);
		if (s == null) return;
		p.displayClientMessage(Component.literal("Você fugiu da Rinha.").withStyle(ChatFormatting.GRAY), false);
		encerrar(p);
	}

	/** Encerra a sessão (fim, fuga, desconexão ou distância) e devolve a IA ao Galeto selvagem. */
	public static void encerrar(ServerPlayer p) {
		encerrar(p.getUUID());
	}

	public static void encerrar(UUID jogador) {
		Sessao s = SESSOES.remove(jogador);
		if (s != null && !s.selvagem.isRemoved())
			s.selvagem.emRinha(false);
	}

	/** Encerra todas as Rinhas (servidor desligando). */
	public static void encerrarTodas() {
		List.copyOf(SESSOES.keySet()).forEach(GerenciadorRinhas::encerrar);
	}

	private static Sessao sessao(ServerPlayer p) {
		Sessao s = SESSOES.get(p.getUUID());
		if (s == null) {
			p.displayClientMessage(Component.literal("Você não está em uma Rinha.").withStyle(ChatFormatting.RED), false);
			return null;
		}
		if (s.selvagem.isRemoved() || !s.selvagem.isAlive() || s.selvagem.level() != p.level() || p.distanceTo(s.selvagem) > DISTANCIA_MAXIMA) {
			p.displayClientMessage(Component.literal("A Rinha terminou: o Galeto selvagem não está mais por perto.").withStyle(ChatFormatting.GRAY), false);
			encerrar(p);
			return null;
		}
		return s;
	}

	private static void jogar(ServerPlayer p, Sessao s, Decisao minha) {
		Decisao dele = s.ia.decidir(s.rinha, s.rinha.equipeB(), s.rinha.equipeA());
		s.rinha.rodada(minha, dele);
		enviarHistorico(p, s);
		if (s.rinha.terminada()) {
			boolean venceu = s.rinha.vencedor().map(v -> v == s.rinha.equipeA()).orElse(false);
			p.displayClientMessage(Component.literal(venceu ? "Você venceu a Rinha!" : "Você perdeu a Rinha.")
					.withStyle(venceu ? ChatFormatting.GREEN : ChatFormatting.RED), false);
			encerrar(p);
		} else {
			enviarMenu(p, s);
		}
	}

	private static void enviarHistorico(ServerPlayer p, Sessao s) {
		List<String> h = s.rinha.historico();
		for (int i = s.historicoEnviado; i < h.size(); i++)
			p.displayClientMessage(Component.literal(h.get(i)).withStyle(h.get(i).startsWith("—") ? ChatFormatting.YELLOW : ChatFormatting.WHITE), false);
		s.historicoEnviado = h.size();
	}

	// ------------------------------------------------------------------ menu
	private static void enviarMenu(ServerPlayer p, Sessao s) {
		Combatente eu = s.rinha.equipeA().ativo(), ele = s.rinha.equipeB().ativo();
		p.displayClientMessage(Component.literal(estado(eu) + "   ×   " + estado(ele)).withStyle(ChatFormatting.AQUA), false);

		MutableComponent combate = Component.literal("Combate: ").withStyle(ChatFormatting.GOLD);
		List<Golpe> golpes = eu.golpes();
		for (int i = 0; i < golpes.size(); i++) {
			Golpe g = golpes.get(i);
			int custo = custo(g, canto(s, g));
			boolean pode = custo <= eu.energia();
			combate.append(botao(g.nome() + (custo > 0 ? " E" + custo : ""), pode ? "/galetocraft acao golpe " + i : null,
					descricao(g), pode ? ChatFormatting.GREEN : ChatFormatting.DARK_GRAY));
		}
		p.displayClientMessage(combate, false);

		MutableComponent galetos = Component.literal("Galetos: ").withStyle(ChatFormatting.GOLD);
		List<Combatente> time = s.rinha.equipeA().galetos();
		for (int i = 0; i < time.size(); i++) {
			Combatente c = time.get(i);
			boolean pode = i != s.rinha.equipeA().indiceAtivo() && !c.derrotado();
			galetos.append(botao(c.nome() + " " + c.hp() + "/" + c.hpMax(), pode ? "/galetocraft acao trocar " + i : null,
					Component.literal(pode ? "Troca voluntária (consome a ação, tem prioridade)" : c.derrotado() ? "Derrotado" : "Em campo"),
					pode ? ChatFormatting.GREEN : ChatFormatting.DARK_GRAY));
		}
		p.displayClientMessage(galetos, false);

		MutableComponent mira = Component.literal("Mira: ").withStyle(ChatFormatting.GOLD);
		for (MiraAnatomica.Regiao r : MiraAnatomica.Regiao.values())
			mira.append(botao(r.nome + " " + Math.round(r.precisao * 100) + "%", "/galetocraft acao mira " + r.name().toLowerCase(Locale.ROOT),
					Component.literal("Precisão ×" + r.precisao + ", pressão ×" + r.fatorPressao), r == s.mira ? ChatFormatting.YELLOW : ChatFormatting.GRAY));
		p.displayClientMessage(mira, false);

		MutableComponent guarda = Component.literal("Guarda: ").withStyle(ChatFormatting.GOLD);
		guarda.append(botao("Neutra", "/galetocraft acao guarda neutra", Component.literal("Sem guarda localizada"),
				s.guarda == null ? ChatFormatting.YELLOW : ChatFormatting.GRAY));
		for (MiraAnatomica.Regiao r : MiraAnatomica.Regiao.values())
			guarda.append(botao(r.nome, "/galetocraft acao guarda " + r.name().toLowerCase(Locale.ROOT),
					Component.literal("Correta: dano ×0,65; errada: dano ×1,10 e +10 de pressão"), r == s.guarda ? ChatFormatting.YELLOW : ChatFormatting.GRAY));
		p.displayClientMessage(guarda, false);

		MutableComponent fim = Component.empty();
		if (s.rinha.equipeA().pena().disponivel())
			fim.append(botao(s.usarPena ? "Pena de Ritmo: SIM" : "Pena de Ritmo: não", "/galetocraft acao pena",
					Component.literal("Usa a Pena na próxima ação: Canto Ofensivo (golpe), de Suporte ou de Revezamento (troca)"),
					s.usarPena ? ChatFormatting.LIGHT_PURPLE : ChatFormatting.GRAY));
		fim.append(botao("Itens", null, Component.literal("Itens da Rinha ainda não homologados"), ChatFormatting.DARK_GRAY));
		fim.append(botao("Fugir", "/galetocraft acao fugir", Component.literal("Encerra a Rinha"), ChatFormatting.RED));
		p.displayClientMessage(fim, false);
	}

	private static String estado(Combatente c) {
		return c.nome() + " Nv" + c.nivel() + " HP " + c.hp() + "/" + c.hpMax() + " E" + c.energia()
				+ (c.estado() == null ? "" : " [" + c.estado().nome() + "]");
	}

	private static Component descricao(Golpe g) {
		List<String> partes = new ArrayList<>();
		partes.add(g.elemento().nome() + " · " + g.categoria().name().toLowerCase(Locale.ROOT)
				+ (g.poder() == null ? "" : " · Poder " + g.poder()) + " · Energia " + g.energia());
		if (g.efeito() != null)
			partes.add(g.efeito());
		return Component.literal(String.join("\n", partes));
	}

	private static MutableComponent botao(String texto, String comando, Component dica, ChatFormatting cor) {
		return Component.literal("[" + texto + "] ").withStyle(st -> {
			st = st.withColor(cor).withHoverEvent(new HoverEvent.ShowText(dica));
			return comando == null ? st : st.withClickEvent(new ClickEvent.RunCommand(comando));
		});
	}
}
