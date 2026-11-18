package br.galetocraft.rinha;

import br.galetocraft.captura.Capturas;
import br.galetocraft.entidade.GaloEntity;
import br.galetocraft.registro.ModAnexos;
import br.galetocraft.treinador.GaletoGuardado;
import br.galetocraft.treinador.Treinador;
import br.galetocraft.nucleo.dados.Especie;
import br.galetocraft.nucleo.dados.Galetario;
import br.galetocraft.nucleo.dados.Golpe;
import br.galetocraft.nucleo.regras.Energia;
import br.galetocraft.nucleo.regras.Experiencia;
import br.galetocraft.nucleo.rinha.Premiacao;
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
 * secretas da Mira Anatômica (região mirada e Guarda) e da Pena de Ritmo. Em Itens fica só a Pena de Captura: os
 * itens segurados da Rinha ainda são candidatos.
 * <p>
 * A equipe do jogador são os 3 primeiros da equipe principal do treinador (com os 5 golpes de origem, até existir
 * o repertório do indivíduo). Sem Galetos capturados, entra a equipe de teste de {@link EquipesTemporarias}.
 * Itens → Pena de Captura tenta capturar o selvagem (regra captura, modalidade Rinha).
 */
public final class GerenciadorRinhas {
	public static final double DISTANCIA_MAXIMA = 32.0;
	/** Formato oficial da Rinha: 3v3. */
	public static final int GALETOS_NA_RINHA = 3;
	private static final Map<UUID, Sessao> SESSOES = new ConcurrentHashMap<>();
	private static final Experiencia XP = new Experiencia(Galetario.padrao());

	private GerenciadorRinhas() {
	}

	private static final class Sessao {
		final Rinha rinha;
		final GaloEntity selvagem;
		final IaBasica ia;
		/** Ids dos Galetos do treinador na Rinha, na ordem da equipe; vazio com a equipe de teste (sem XP). */
		List<UUID> galetosDoTreinador = List.of();
		MiraAnatomica.Regiao mira = MiraAnatomica.Regiao.TRONCO;
		MiraAnatomica.Regiao guarda;
		boolean usarPena;
		boolean mostrarItens;
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

	/**
	 * Começa uma Rinha entre o treinador e o Galeto selvagem. Vão para a Rinha os 3 primeiros da equipe principal
	 * (formato 3v3); sem Galetos capturados, vai a equipe de teste.
	 */
	public static void iniciar(ServerPlayer jogador, GaloEntity selvagem) {
		Galetario g = Galetario.padrao();
		Especie especieSelvagem = selvagem.fichaDaEspecie().orElseThrow();
		Treinador treinador = ModAnexos.treinador(jogador);
		List<Combatente> meus;
		List<UUID> ids = List.of();
		if (!treinador.equipe().isEmpty()) {
			List<GaletoGuardado> escalados = treinador.equipe().stream().limit(GALETOS_NA_RINHA).toList();
			meus = escalados.stream().map(GaletoGuardado::combatente).toList();
			ids = escalados.stream().map(GaletoGuardado::id).toList();
		} else {
			meus = EquipesTemporarias.equipe(jogador).stream().map(e -> Combatente.padrao(e, GaloEntity.NIVEL_PADRAO)).toList();
			jogador.displayClientMessage(Component.literal("Você ainda não tem Galetos: entra a equipe de teste (/galetocraft equipe teste).")
					.withStyle(ChatFormatting.GRAY), false);
		}
		long semente = jogador.level().getGameTime() ^ selvagem.getUUID().getLeastSignificantBits();
		Rinha r = new Rinha(g, new Equipe(jogador.getName().getString(), meus),
				new Equipe("Selvagem", List.of(new Combatente(especieSelvagem, selvagem.nivel(),
						GaletoGuardado.APRENDIZADO.equipamentoInicial(especieSelvagem, selvagem.nivel()), selvagem.individuo()))), semente);
		r.permitirCaptura(Capturas.REGRAS);
		selvagem.emRinha(true);
		Sessao s = new Sessao(r, selvagem, semente);
		s.galetosDoTreinador = ids;
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

	/** Botão Itens: mostra ou esconde a lista de itens da Rinha (por enquanto, só a Pena de Captura). */
	public static void alternarItens(ServerPlayer p) {
		Sessao s = sessao(p);
		if (s == null) return;
		s.mostrarItens = !s.mostrarItens;
		enviarMenu(p, s);
	}

	/** Itens → Pena de Captura: tentativa de captura do selvagem; consome a ação do treinador. */
	public static void capturar(ServerPlayer p) {
		Sessao s = sessao(p);
		if (s == null) return;
		if (!Capturas.temPena(p)) {
			p.displayClientMessage(Component.literal("Você não tem a Pena de Captura (/galetocraft pena).").withStyle(ChatFormatting.RED), false);
			return;
		}
		int nivel = Capturas.nivelPena(p);
		Especie alvo = s.rinha.equipeB().ativo().especie();
		if (!Capturas.REGRAS.elegivel(alvo.raridade(), nivel)) {
			p.displayClientMessage(Component.literal(alvo.nome() + " (" + alvo.raridade() + ") não pode ser capturado com a Pena de Captura nível "
					+ nivel + ".").withStyle(ChatFormatting.RED), false);
			return;
		}
		s.mostrarItens = false;
		s.usarPena = false;
		jogar(p, s, new Decisao(new Decisao.Capturar(nivel), s.guarda));
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
		if (s.rinha.capturado()) {
			GaletoGuardado capturado = s.selvagem.guardar();
			SESSOES.remove(p.getUUID());
			s.selvagem.discard();
			Capturas.registrarCaptura(p, capturado);
		} else if (s.rinha.terminada()) {
			boolean venceu = s.rinha.vencedor().map(v -> v == s.rinha.equipeA()).orElse(false);
			p.displayClientMessage(Component.literal(venceu ? "Você venceu a Rinha!" : "Você perdeu a Rinha.")
					.withStyle(venceu ? ChatFormatting.GREEN : ChatFormatting.RED), false);
			if (venceu)
				premiar(p, s);
			encerrar(p);
		} else {
			enviarMenu(p, s);
		}
	}

	/** XP da Rinha vencida para os Galetos do treinador que entraram em campo (regra experiencia). */
	private static void premiar(ServerPlayer p, Sessao s) {
		if (s.galetosDoTreinador.isEmpty()) {
			p.displayClientMessage(Component.literal("A equipe de teste não ganha XP.").withStyle(ChatFormatting.GRAY), false);
			return;
		}
		Map<Integer, Long> xp;
		try {
			xp = Premiacao.liquidar(s.rinha, s.rinha.equipeA(), XP, Premiacao.PVE_SELVAGEM);
		} catch (IllegalArgumentException semMultiplicador) {
			p.displayClientMessage(Component.literal("Sem XP: " + semMultiplicador.getMessage()).withStyle(ChatFormatting.GRAY), false);
			return;
		}
		Treinador t = ModAnexos.treinador(p);
		for (Map.Entry<Integer, Long> e : xp.entrySet()) {
			UUID id = s.galetosDoTreinador.get(e.getKey());
			GaletoGuardado antes = null;
			for (GaletoGuardado g : t.equipe())
				if (g.id().equals(id)) antes = g;
			for (GaletoGuardado g : t.reservas())
				if (g.id().equals(id)) antes = g;
			if (antes == null)
				continue;
			GaletoGuardado depois = antes.comXp(e.getValue());
			t = t.atualizar(id, g -> depois);
			p.displayClientMessage(Component.literal(antes.ficha().nome() + " ganhou " + (depois.xp() - antes.xp()) + " XP.")
					.withStyle(ChatFormatting.AQUA), false);
			if (depois.nivel() > antes.nivel()) {
				p.displayClientMessage(Component.literal(antes.ficha().nome() + " subiu para o nível " + depois.nivel() + "!")
						.withStyle(ChatFormatting.GOLD), false);
				List<String> novos = GaletoGuardado.APRENDIZADO.novos(antes.ficha(), antes.nivel(), depois.nivel()).stream()
						.map(br.galetocraft.nucleo.dados.Golpe::nome).toList();
				if (!novos.isEmpty())
					p.displayClientMessage(Component.literal(antes.ficha().nome() + " aprendeu: " + String.join(", ", novos)
							+ " (equipe em /galetocraft golpes)").withStyle(ChatFormatting.GOLD), false);
			}
		}
		ModAnexos.salvar(p, t);
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
		boolean podeItens = s.rinha.capturaPermitida() && Capturas.temPena(p);
		fim.append(botao("Itens", podeItens ? "/galetocraft acao itens" : null,
				Component.literal(podeItens ? "Itens da Rinha: Pena de Captura" : "Nenhum item disponível (/galetocraft pena)"),
				podeItens ? (s.mostrarItens ? ChatFormatting.YELLOW : ChatFormatting.GREEN) : ChatFormatting.DARK_GRAY));
		fim.append(botao("Fugir", "/galetocraft acao fugir", Component.literal("Encerra a Rinha"), ChatFormatting.RED));
		p.displayClientMessage(fim, false);

		if (s.mostrarItens && podeItens)
			p.displayClientMessage(Component.literal("Itens: ").withStyle(ChatFormatting.GOLD)
					.append(botao("Pena de Captura nível " + Capturas.nivelPena(p), "/galetocraft acao capturar",
							Component.literal("Tenta capturar " + ele.nome() + ". Consome a ação; HP menor, Sono e Paralisia ajudam."),
							ChatFormatting.LIGHT_PURPLE)), false);
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
