package br.galetocraft.nucleo.rinha;

import br.galetocraft.nucleo.dados.Atributo;
import br.galetocraft.nucleo.dados.Categoria;
import br.galetocraft.nucleo.dados.EstadoNegativo;
import br.galetocraft.nucleo.dados.Galetario;
import br.galetocraft.nucleo.dados.Golpe;
import br.galetocraft.nucleo.regras.Ambiente;
import br.galetocraft.nucleo.regras.DanoV56;
import br.galetocraft.nucleo.regras.Eficacia;
import br.galetocraft.nucleo.regras.Energia;
import br.galetocraft.nucleo.regras.Estados;
import br.galetocraft.nucleo.regras.MiraAnatomica;
import br.galetocraft.nucleo.regras.PenaDeRitmo;
import br.galetocraft.nucleo.regras.Velocidade;
import com.google.gson.JsonElement;

import java.util.ArrayList;
import java.util.Collections;
import java.util.EnumSet;
import java.util.IdentityHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.SplittableRandom;

/**
 * Motor de turnos da Rinha (formato oficial 3v3, um ativo por lado).
 *
 * <p>Implementado conforme a base: ordem com trocas voluntárias primeiro e depois Velocidade (empate 50/50);
 * Energia (entrada 100, +20 por rodada, Afogamento −20); Paralisia (20% de perder a ação, sem gastar Energia);
 * Tonto (30% de falha, com metade do dano no próprio usuário); esquiva universal; dano V5.6 com eficácia,
 * clima/santuário, Guarda, Exposição e Ruptura; Golpe Duplo V2.2 (bloqueio especial de 50% e 50% da base);
 * estado aplicado pelo golpe; Concentração V2.3 com Pena de Ritmo (Cantos Ofensivo, de Suporte e de Revezamento);
 * Mira V1.5 (precisão por região, Pressão uma vez por ação, Ruptura); dano de estado e cura de santuário no fim
 * da rodada; substituição gratuita após derrota.</p>
 *
 * <p>Ainda NÃO implementado (registrado no Histórico quando ocorre): passivas; efeitos especiais dos golpes
 * além do estado aplicado; suportes que não sejam a Concentração; golpes sequenciais (1–5 acertos); precisão
 * própria de cada golpe (usa 100%); Canto da Guarda; Leitura Perfeita; itens; Sono.</p>
 */
public final class Rinha {
	public static final int LIMITE_RODADAS = 300;

	private final Eficacia eficacia;
	private final Ambiente ambiente;
	private final Equipe a, b;
	private final SplittableRandom rng;
	private final List<String> historico = new ArrayList<>();
	private final Map<Combatente, Set<MiraAnatomica.Regiao>> atingidasNaRodada = new IdentityHashMap<>();
	private Ambiente.Clima clima;
	private int climaRestante;
	private Ambiente.Santuario santuario;
	private int santuarioRestante;
	private int rodada;

	public Rinha(Galetario g, Equipe a, Equipe b, long semente) {
		this.eficacia = new Eficacia(g);
		this.ambiente = new Ambiente(g);
		this.a = a;
		this.b = b;
		this.rng = new SplittableRandom(semente);
		a.ativo().entrarEmCampo();
		b.ativo().entrarEmCampo();
		registrar("Rinha: " + a.nome() + " (" + a.ativo().nome() + ") × " + b.nome() + " (" + b.ativo().nome() + ")");
	}

	public Equipe equipeA() { return a; }
	public Equipe equipeB() { return b; }
	public int rodada() { return rodada; }
	public List<String> historico() { return Collections.unmodifiableList(historico); }
	public Ambiente.Clima clima() { return clima; }
	public Ambiente.Santuario santuario() { return santuario; }
	Eficacia eficacia() { return eficacia; }

	public boolean terminada() {
		return a.derrotada() || b.derrotada() || rodada >= LIMITE_RODADAS;
	}

	/** Vencedor, ou vazio em empate ou Rinha em andamento. */
	public Optional<Equipe> vencedor() {
		if (a.derrotada() && !b.derrotada()) return Optional.of(b);
		if (b.derrotada() && !a.derrotada()) return Optional.of(a);
		return Optional.empty();
	}

	public void definirClima(Ambiente.Clima c) {
		clima = c;
		climaRestante = Ambiente.DURACAO;
		registrar("Clima: " + c);
	}

	public void definirSantuario(Ambiente.Santuario s) {
		santuario = s;
		santuarioRestante = Ambiente.DURACAO;
		registrar("Santuário: " + s);
	}

	/** Golpes equipados que o ativo pode pagar agora. */
	public List<Golpe> golpesValidos(Equipe e) {
		Combatente c = e.ativo();
		return c.golpes().stream().filter(g -> g.energia() <= c.energia()).toList();
	}

	// ------------------------------------------------------------------ rodada
	public void rodada(Decisao decisaoA, Decisao decisaoB) {
		if (terminada())
			throw new IllegalStateException("A Rinha já terminou");
		rodada++;
		registrar("— Rodada " + rodada + " —");
		atingidasNaRodada.clear();
		inicioDaRodada(a);
		inicioDaRodada(b);

		List<Lado> lados = new ArrayList<>(List.of(new Lado(a, b, decisaoA, decisaoB), new Lado(b, a, decisaoB, decisaoA)));
		// 1) trocas voluntárias, o ativo mais veloz sai primeiro
		List<Lado> trocas = new ArrayList<>(lados.stream().filter(l -> l.minha.acao() instanceof Decisao.Trocar).toList());
		ordenarPorVelocidade(trocas);
		for (Lado l : trocas)
			trocar(l.eu, (Decisao.Trocar) l.minha.acao());
		// 2) golpes, por Velocidade efetiva (empate 50/50)
		List<Lado> golpes = new ArrayList<>(lados.stream().filter(l -> l.minha.acao() instanceof Decisao.UsarGolpe).toList());
		ordenarPorVelocidade(golpes);
		for (Lado l : golpes) {
			if (terminada())
				break;
			usarGolpe(l.eu, l.oponente, (Decisao.UsarGolpe) l.minha.acao(), l.dele.guarda());
		}
		fimDaRodada();
	}

	private record Lado(Equipe eu, Equipe oponente, Decisao minha, Decisao dele) {
	}

	private void ordenarPorVelocidade(List<Lado> lados) {
		if (lados.size() < 2)
			return;
		double va = lados.get(0).eu.ativo().atributo(Atributo.VELOCIDADE);
		double vb = lados.get(1).eu.ativo().atributo(Atributo.VELOCIDADE);
		if (vb > va || (vb == va && rng.nextBoolean()))
			Collections.swap(lados, 0, 1);
	}

	private void inicioDaRodada(Equipe e) {
		for (Combatente c : e.galetos()) {
			c.entrouNestaRodada(false);
			if (c.derrotado())
				continue;
			if (c == e.ativo()) {
				int antes = c.energia();
				c.energia(Energia.inicioDoTurno(c.energia(), c.estado() == EstadoNegativo.AFOGAMENTO)
						+ ambiente.energiaExtra(santuario, c.especie().elementos()));
				if (c.estado() == EstadoNegativo.AFOGAMENTO)
					registrar(c.nome() + " está Afogado: Energia " + antes + " → " + c.energia());
			} else {
				c.energia(Energia.somar(c.energia(), Energia.REGENERACAO));   // reserva também regenera 20
			}
		}
	}

	private void trocar(Equipe e, Decisao.Trocar t) {
		if (!e.podeTrocarPara(t.indice())) {
			registrar(e.nome() + ": troca inválida");
			return;
		}
		String saiu = e.ativo().nome();
		boolean revezamento = t.cantoRevezamento() && e.pena().disponivel();
		e.trocar(t.indice());
		if (revezamento) {
			e.pena().consumir();
			e.ativo().protecaoRevezamento(true);
		}
		registrar(e.nome() + " troca " + saiu + " por " + e.ativo().nome() + (revezamento ? " (Canto de Revezamento)" : ""));
	}

	private void usarGolpe(Equipe eu, Equipe op, Decisao.UsarGolpe u, MiraAnatomica.Regiao guardaOponente) {
		Combatente c = eu.ativo();
		Golpe g = u.golpe();
		if (c.derrotado() || c.entrouNestaRodada())
			return;                                                   // substituto não age na mesma ação
		if (!c.golpes().contains(g)) {
			registrar(c.nome() + " não tem " + g.nome() + " equipado");
			return;
		}
		if (c.estado() == EstadoNegativo.PARALISIA && rng.nextDouble() < Estados.PARALISIA_PERDE_ACAO) {
			registrar(c.nome() + " está Paralisado e perde a ação");
			return;
		}
		boolean cantoSuporte = u.canto() == PenaDeRitmo.Canto.SUPORTE && !g.concentracao() && !g.danoDireto() && eu.pena().disponivel();
		int custo = cantoSuporte ? Energia.custoComCantoSuporte(g.energia()) : g.energia();
		if (custo > c.energia()) {
			registrar(c.nome() + " não tem Energia para " + g.nome() + " (" + c.energia() + "/" + custo + ")");
			return;
		}
		c.energia(c.energia() - custo);
		if (cantoSuporte) {
			eu.pena().consumir();
			registrar(c.nome() + " usa o Canto de Suporte da Pena de Ritmo: custo de " + g.nome() + " " + g.energia() + " → " + custo);
		}
		if (c.estado() == EstadoNegativo.TONTO && rng.nextDouble() < Estados.TONTO_FALHA) {
			if (g.danoDireto()) {
				// metade do dano que o golpe causaria no alvo
				int autodano = (int) Math.ceil(calcular(c, op.ativo(), g, null, MiraAnatomica.Guarda.NEUTRA, true, false).dano() * Estados.TONTO_AUTODANO);
				int perdido = c.sofrer(autodano);
				registrar(c.nome() + " está Tonto, erra " + g.nome() + " e se fere: −" + perdido + " HP");
			} else {
				registrar(c.nome() + " está Tonto e o suporte falha");
			}
			substituirSeDerrotado(eu);
			return;
		}
		if (g.concentracao()) {
			concentrar(eu, c);
			return;
		}
		if (!g.danoDireto()) {
			registrar(c.nome() + " usa " + g.nome() + " (efeito ainda não implementado no motor)");
			return;
		}
		atacar(eu, op, c, g, u, guardaOponente);
	}

	private void concentrar(Equipe eu, Combatente c) {
		int antes = c.energia();
		c.energia(Energia.somar(c.energia(), Energia.CONCENTRACAO));
		StringBuilder s = new StringBuilder(c.nome() + " usa Concentração: Energia " + antes + " → " + c.energia());
		if (c.estado() != null && rng.nextDouble() < Energia.CONCENTRACAO_REMOVE_ESTADO) {
			s.append(", remove ").append(c.estado().nome());
			c.removerEstado();
		}
		if (eu.pena().aoConcentrar())
			s.append(", cria a Pena de Ritmo");
		registrar(s.toString());
	}

	private void atacar(Equipe eu, Equipe op, Combatente c, Golpe g, Decisao.UsarGolpe u, MiraAnatomica.Regiao guardaOp) {
		Combatente alvo = op.ativo();
		MiraAnatomica.Regiao regiao = u.regiao();
		MiraAnatomica.Guarda guarda = regiao == null || guardaOp == null ? MiraAnatomica.Guarda.NEUTRA
				: guardaOp == regiao ? MiraAnatomica.Guarda.CORRETA : MiraAnatomica.Guarda.ERRADA;
		boolean canto = u.canto() == PenaDeRitmo.Canto.OFENSIVO && eu.pena().disponivel();
		if (!acerta(c, alvo, g, regiao))
			return;                                                   // primeiro acerto falho encerra a ação
		int retirado = acerto(c, alvo, g, regiao, guarda, true, canto);
		if (canto) {
			eu.pena().consumir();
			registrar("  Canto Ofensivo da Pena de Ritmo");
		}
		boolean usouJanela = regiao != null && alvo.janelaRuptura() == regiao;
		if (!alvo.derrotado()) {
			double chance = Velocidade.combinar(Velocidade.chanceGolpeDuplo(c.atributo(Atributo.VELOCIDADE),
					Math.max(1, alvo.atributo(Atributo.VELOCIDADE))), chanceIntrinseca(g));
			if (rng.nextDouble() < chance) {
				if (rng.nextDouble() < 0.5)
					registrar("  segundo acerto bloqueado");
				else if (acerta(c, alvo, g, regiao))
					retirado += acerto(c, alvo, g, regiao, guarda, false, false);
			}
		}
		if (g.estadoAplicado() != null && retirado > 0 && !alvo.derrotado() && rng.nextDouble() < g.chanceEstado()
				&& alvo.aplicarEstado(g.estadoAplicado()))
			registrar("  " + alvo.nome() + " fica com " + g.estadoAplicado().nome());
		if (regiao != null && retirado > 0) {
			atingidasNaRodada.computeIfAbsent(alvo, k -> EnumSet.noneOf(MiraAnatomica.Regiao.class)).add(regiao);
			if (usouJanela)
				alvo.consumirJanelaRuptura();
			int p = MiraAnatomica.pressao(retirado, alvo.hpMax(), regiao, guarda, canto);
			if (alvo.medidor(regiao).somar(p) && !alvo.derrotado()) {
				alvo.romper(regiao);
				registrar("  Ruptura em " + regiao.nome + " de " + alvo.nome());
			}
		}
		substituirSeDerrotado(op);
	}

	private static double chanceIntrinseca(Golpe g) {
		if (g.efeitoEstruturado() == null)
			return 0;
		JsonElement v = g.efeitoEstruturado().get("chance_intrinseca");
		return v != null && v.isJsonPrimitive() && v.getAsJsonPrimitive().isNumber() ? v.getAsDouble() : 0;
	}

	/** Precisão (100% × região da Mira) e esquiva universal. */
	private boolean acerta(Combatente c, Combatente alvo, Golpe g, MiraAnatomica.Regiao regiao) {
		double precisao = regiao == null ? 1.0 : regiao.precisao;
		if (rng.nextDouble() >= precisao) {
			registrar("  " + c.nome() + " erra " + g.nome());
			return false;
		}
		double esquiva = Velocidade.chanceEsquivaPercentual(c.atributo(Atributo.VELOCIDADE), alvo.atributo(Atributo.VELOCIDADE)) / 100;
		if (rng.nextDouble() < esquiva) {
			registrar("  " + alvo.nome() + " esquiva de " + g.nome());
			return false;
		}
		return true;
	}

	private int acerto(Combatente c, Combatente alvo, Golpe g, MiraAnatomica.Regiao regiao, MiraAnatomica.Guarda guarda,
			boolean primeiro, boolean canto) {
		DanoV56.Resultado r = calcular(c, alvo, g, regiao, guarda, primeiro, canto);
		if (alvo.protecaoRevezamento())
			alvo.protecaoRevezamento(false);                          // vale só para o primeiro acerto sofrido
		int perdido = alvo.sofrer(r.dano());
		double ef = eficacia.multiplicador(g.elemento(), alvo.especie().elementos());
		registrar("  " + c.nome() + " usa " + g.nome() + (primeiro ? "" : " (2º acerto)") + ": −" + perdido + " HP em "
				+ alvo.nome() + (ef > 1 ? " (eficaz ×" + ef + ")" : ef < 1 ? " (resistido ×" + ef + ")" : "")
				+ (guarda == MiraAnatomica.Guarda.CORRETA ? " [Guarda correta]" : "") + " → " + alvo.hp() + "/" + alvo.hpMax());
		return perdido;
	}

	private DanoV56.Resultado calcular(Combatente c, Combatente alvo, Golpe g, MiraAnatomica.Regiao regiao,
			MiraAnatomica.Guarda guarda, boolean primeiro, boolean canto) {
		Categoria cat = g.categoria();
		double defesa = alvo.atributo(cat.defesa()) * (1 + ambiente.bonusDefesa(clima, alvo.especie().elementos(), cat.defesa()));
		DanoV56.Entrada e = new DanoV56.Entrada(alvo.hpMax(), g.poder(), c.atributo(cat.ataque()), defesa)
				.eficacia(eficacia.multiplicador(g.elemento(), alvo.especie().elementos()))
				.bonus(ambiente.bonusDano(clima, santuario, g.elemento()))
				.guarda(guarda);
		if (!primeiro)
			e.segundoAcerto();
		if (canto)
			e.cantoOfensivo();
		if (regiao != null) {
			if (alvo.janelaRuptura() == regiao)
				e.anatomia(DanoV56.Anatomia.RUPTURA);
			else if (alvo.medidor(regiao).exposta())
				e.anatomia(DanoV56.Anatomia.EXPOSICAO);
		}
		if (alvo.protecaoRevezamento())
			e.reducao(DanoV56.REDUCAO_CANTO_REVEZAMENTO.doubleValue());
		return DanoV56.calcular(e);
	}

	private void substituirSeDerrotado(Equipe e) {
		if (!e.ativo().derrotado())
			return;
		registrar(e.ativo().nome() + " foi derrotado");
		Optional<Integer> prox = e.proximoApto();
		if (prox.isEmpty()) {
			e.pena().encerrar();
			registrar(e.nome() + " não tem mais Galetos aptos");
			return;
		}
		e.trocar(prox.get());
		registrar(e.nome() + " envia " + e.ativo().nome());
	}

	private void fimDaRodada() {
		for (Equipe e : List.of(a, b)) {
			Combatente c = e.ativo();
			if (c.derrotado())
				continue;
			if (c.estado() == EstadoNegativo.QUEIMADURA)
				registrar(c.nome() + " sofre Queimadura: −" + c.sofrer(Estados.danoQueimadura(c.hpMax())) + " HP");
			else if (c.estado() == EstadoNegativo.ENVENENAMENTO)
				registrar(c.nome() + " sofre Envenenamento: −" + c.sofrer(Estados.danoEnvenenamento(c.hpMax(), c.proximaOcorrenciaVeneno())) + " HP");
			double cura = ambiente.cura(santuario, c.especie().elementos());
			if (cura > 0 && !c.derrotado()) {
				// arredondamento da cura do santuário: pendente na regra; usado para baixo
				int ganho = c.curar((int) Math.floor(c.hpMax() * cura));
				if (ganho > 0)
					registrar(c.nome() + " recupera " + ganho + " HP no Santuário das Raízes");
			}
			Set<MiraAnatomica.Regiao> atingidas = atingidasNaRodada.getOrDefault(c, Set.of());
			for (MiraAnatomica.Regiao r : MiraAnatomica.Regiao.values())
				if (!atingidas.contains(r))
					c.medidor(r).decair();
			c.fimDaOportunidade();
			e.pena().fimDaOportunidade();
			substituirSeDerrotado(e);
		}
		if (clima != null && --climaRestante <= 0) {
			registrar("O clima " + clima + " termina");
			clima = null;
		}
		if (santuario != null && --santuarioRestante <= 0) {
			registrar("O santuário " + santuario + " termina");
			santuario = null;
		}
		if (a.derrotada() || b.derrotada())
			registrar(vencedor().map(v -> "Vitória de " + v.nome()).orElse("Empate"));
	}

	private void registrar(String linha) {
		historico.add(linha);
	}
}
