package br.galetocraft.nucleo;

import br.galetocraft.nucleo.dados.Especie;
import br.galetocraft.nucleo.dados.EstadoNegativo;
import br.galetocraft.nucleo.dados.Galetario;
import br.galetocraft.nucleo.dados.Golpe;
import br.galetocraft.nucleo.regras.Captura;
import br.galetocraft.nucleo.regras.Energia;
import br.galetocraft.nucleo.regras.Experiencia;
import br.galetocraft.nucleo.rinha.Premiacao;
import br.galetocraft.nucleo.rinha.IaBasica;
import br.galetocraft.nucleo.rinha.Combatente;
import br.galetocraft.nucleo.rinha.Decisao;
import br.galetocraft.nucleo.rinha.Equipe;
import br.galetocraft.nucleo.rinha.Rinha;
import br.galetocraft.nucleo.rinha.Simulador;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class RinhaTest {
	static final Galetario G = Galetario.padrao();

	private static Equipe trio(String nome, int... numeros) {
		return new Equipe(nome, java.util.Arrays.stream(numeros).mapToObj(n -> Combatente.padrao(G.especie(n), 50)).toList());
	}

	@Test
	void combatenteNoNivel50UsaOsAtributosBase() {
		Combatente c = Combatente.padrao(G.especie(22), 50);
		assertEquals(100, c.hpMax());
		assertEquals(Energia.ENTRADA, c.energia());
		assertEquals(5, c.golpes().size());
		Combatente c100 = Combatente.padrao(G.especie(22), 100);
		assertEquals(150, c100.hpMax());
		assertThrows(IllegalArgumentException.class, () -> new Combatente(G.especie(22), 50, List.of(G.especie(22).golpe("Crina Poderosa"))));
	}

	@Test
	void rinhaTerminaComVencedorEMantemInvariantes() {
		for (long semente = 1; semente <= 40; semente++) {
			Equipe a = trio("A", 1, 7, 22), b = trio("B", 4, 9, 16);
			Rinha r = Simulador.rodar(G, a, b, semente);
			assertTrue(r.terminada());
			assertTrue(r.rodada() < Rinha.LIMITE_RODADAS, "Rinha não deveria chegar ao limite");
			assertTrue(r.vencedor().isPresent());
			for (Equipe e : List.of(a, b))
				for (Combatente c : e.galetos()) {
					assertTrue(c.hp() >= 0 && c.hp() <= c.hpMax());
					assertTrue(c.energia() >= 0 && c.energia() <= Energia.MAXIMA);
				}
			assertTrue(r.vencedor().get().galetos().stream().anyMatch(c -> !c.derrotado()));
		}
	}

	@Test
	void mesmaSementeDaMesmaRinha() {
		Rinha r1 = Simulador.rodar(G, trio("A", 5, 6), trio("B", 2, 3), 2026);
		Rinha r2 = Simulador.rodar(G, trio("A", 5, 6), trio("B", 2, 3), 2026);
		assertEquals(r1.historico(), r2.historico());
	}

	@Test
	void concentracaoRecuperaEnergiaECriaPena() {
		Equipe a = trio("A", 22), b = trio("B", 7);
		Rinha r = new Rinha(G, a, b, 7);
		Golpe conc = a.ativo().golpes().stream().filter(Golpe::concentracao).findFirst().orElseThrow();
		Golpe forte = G.especie(22).golpe("Contraponto dos Ventos");      // E40
		r.rodada(Decisao.golpe(forte), Decisao.golpe(b.ativo().golpes().stream().filter(Golpe::concentracao).findFirst().orElseThrow()));
		assertEquals(100 - 40, a.ativo().energia());                       // começa a rodada no teto e paga 40
		r.rodada(Decisao.golpe(conc), Decisao.golpe(b.ativo().golpes().stream().filter(Golpe::concentracao).findFirst().orElseThrow()));
		assertEquals(Math.min(100, 60 + 20 + 35), a.ativo().energia());
		assertTrue(a.pena().ativa());
	}

	@Test
	void trocaVoluntariaTemPrioridadeEEntraComEnergiaCheia() {
		Equipe a = trio("A", 1, 19), b = trio("B", 2);
		Rinha r = new Rinha(G, a, b, 3);
		Golpe ataque = b.ativo().golpes().stream().filter(Golpe::danoDireto).findFirst().orElseThrow();
		r.rodada(new Decisao(new Decisao.Trocar(1, false), null), Decisao.golpe(ataque));
		assertEquals("Renacocó", a.ativo().nome());
		assertTrue(r.historico().stream().anyMatch(l -> l.contains("troca Pirococó por Renacocó")));
		int iTroca = indice(r, "troca Pirococó"), iGolpe = indice(r, "usa " + ataque.nome());
		assertTrue(iTroca < iGolpe, "a troca vem antes do golpe");
	}

	private static int indice(Rinha r, String trecho) {
		for (int i = 0; i < r.historico().size(); i++)
			if (r.historico().get(i).contains(trecho))
				return i;
		return Integer.MAX_VALUE;
	}

	@Test
	void golpeComEstadoPodeAplicarTonto() {
		Especie cocorak = G.especie(4);
		Golpe punho = cocorak.golpe("Punho das Dunas");
		assertEquals(EstadoNegativo.TONTO, punho.estadoAplicado());
		boolean aplicou = false;
		for (long s = 1; s <= 60 && !aplicou; s++) {
			Equipe a = new Equipe("A", List.of(Combatente.padrao(cocorak, 100))), b = trio("B", 23);
			Rinha r = new Rinha(G, a, b, s);
			Golpe conc = b.ativo().golpes().stream().filter(Golpe::concentracao).findFirst().orElseThrow();
			r.rodada(Decisao.golpe(punho), Decisao.golpe(conc));
			aplicou = b.ativo().estado() == EstadoNegativo.TONTO;
		}
		assertTrue(aplicou, "20% de chance: em 60 tentativas deve ocorrer");
	}

	@Test
	void simuladorDeDuelos() {
		Simulador.Resultado res = Simulador.duelo(G, G.especie(1), G.especie(7), 50, 100, 11);
		assertEquals(100, res.total());
		assertTrue(res.taxaA() > 0.5, "um Mítico deve vencer um Comum na maioria dos duelos: " + res);
	}

	// ---------------------------------------------------------------- captura na Rinha (regra captura, modalidade Rinha)
	private static Rinha selvagem(int jogador, int selvagem, long semente) {
		Rinha r = new Rinha(G, trio("Treinador", jogador), trio("Selvagem", selvagem), semente);
		r.permitirCaptura(new Captura(G));
		return r;
	}

	private static Decisao capturar(int nivelPena) {
		return new Decisao(new Decisao.Capturar(nivelPena), null);
	}

	@Test
	void capturaNaRinhaUsaAFormulaComHpEEncerraNoSucesso() {
		Captura regras = new Captura(G);
		int sucessos = 0, falhas = 0;
		for (long semente = 1; semente <= 60; semente++) {
			// Pirococó (Velocidade 85) × Taturico selvagem (40): o treinador age primeiro
			Rinha r = selvagem(1, 7, semente);
			Combatente alvo = r.equipeB().ativo();
			Golpe garra = alvo.golpes().stream().filter(g -> g.danoDireto()).findFirst().orElseThrow();
			r.rodada(capturar(5), Decisao.golpe(garra));
			double esperado = regras.chancePercentual(Captura.Modalidade.RINHA, "Comum", 5, 50, alvo.hp(), alvo.hpMax(), null);
			assertEquals(esperado, r.ultimaChanceCaptura(), 1e-9);
			assertEquals(100 * 4.5 / (4.5 + 1 + 49 / 60.0), esperado, 1e-9);   // HP cheio: H = 1
			if (r.capturado()) {
				sucessos++;
				assertTrue(r.terminada());
				assertTrue(r.vencedor().isEmpty(), "captura não é vitória");
				// o selvagem, mais lento, tinha ação pendente: a Rinha acabou antes dela
				assertTrue(r.historico().stream().noneMatch(l -> l.contains("Taturico usa")));
				assertThrows(IllegalStateException.class, () -> r.rodada(capturar(5), Decisao.golpe(garra)));
			} else {
				falhas++;
				assertFalse(r.terminada(), "a falha não encerra a Rinha");
				assertTrue(r.historico().stream().anyMatch(l -> l.contains("Taturico usa") || l.contains("Taturico erra")
						|| l.contains("esquiva")), "o selvagem age na ordem normal depois da falha");
			}
		}
		assertTrue(sucessos > 0 && falhas > 0);
	}

	@Test
	void selvagemMaisVelozAgeAntesDaCaptura() {
		for (long semente = 1; semente <= 30; semente++) {
			// Taturico (40) do treinador × Vagaló selvagem (180)
			Rinha r = selvagem(7, 9, semente);
			Golpe golpe = r.equipeB().ativo().golpes().stream().filter(Golpe::danoDireto).findFirst().orElseThrow();
			r.rodada(capturar(1), Decisao.golpe(golpe));
			List<String> h = r.historico();
			int pena = -1, vagalo = -1;
			for (int i = 0; i < h.size(); i++) {
				if (h.get(i).contains("Pena de Captura")) pena = i;
				if (vagalo < 0 && h.get(i).contains("Vagaló")) vagalo = i;
			}
			assertTrue(pena > 0);
			// a 1ª linha cita o Vagaló no cabeçalho da Rinha; procura a ação dele depois do cabeçalho da rodada
			int acaoVagalo = -1;
			for (int i = 2; i < h.size(); i++)
				if (h.get(i).contains("Vagaló usa") || h.get(i).contains("Vagaló erra") || h.get(i).contains("esquiva")) {
					acaoVagalo = i;
					break;
				}
			assertTrue(acaoVagalo > 0 && acaoVagalo < pena, "o selvagem mais veloz age antes: " + h);
		}
	}

	@Test
	void capturaRespeitaElegibilidadeEModalidade() {
		// Lendário Original (Quetzacocó): classe fora da regra de captura, inelegível
		Rinha r = selvagem(1, 23, 7);
		r.rodada(capturar(5), Decisao.golpe(r.equipeB().ativo().golpes().get(0)));
		assertFalse(r.capturado());
		assertTrue(r.historico().stream().anyMatch(l -> l.contains("não pode ser capturado")));
		assertTrue(Double.isNaN(r.ultimaChanceCaptura()));
		// Rinha sem selvagem (entre treinadores): a captura não é permitida
		Rinha t = new Rinha(G, trio("A", 1), trio("B", 7), 3);
		t.rodada(capturar(5), Decisao.golpe(t.equipeB().ativo().golpes().get(0)));
		assertFalse(t.capturado());
		assertTrue(t.historico().stream().anyMatch(l -> l.contains("só é possível em Rinha contra Cocorídeo selvagem")));
	}

	// ---------------------------------------------------------------- XP dos Cocorídeos (regra experiencia)
	@Test
	void restoDaXpVaiNaOrdemDaPrimeiraEntrada() {
		assertArrayEquals(new long[]{4, 3, 3}, Experiencia.repartir(10, 3));
		assertArrayEquals(new long[]{1150}, Experiencia.repartir(1150, 1));
		assertArrayEquals(new long[]{0, 0}, Experiencia.repartir(0, 2));
	}

	@Test
	void xpDaRinhaVencidaVaiSoParaQuemEntrouEmCampo() {
		Experiencia regras = new Experiencia(G);
		int conferidas = 0;
		for (long semente = 1; semente <= 40; semente++) {
			// trio do treinador × Taturico selvagem; o treinador troca uma vez na 1ª rodada e depois só golpeia
			Equipe a = trio("Treinador", 4, 1, 3), b = trio("Selvagem", 7);
			Rinha r = new Rinha(G, a, b, semente);
			r.permitirCaptura(new Captura(G));
			IaBasica ia = new IaBasica(semente);
			r.rodada(new Decisao(new Decisao.Trocar(1, false), null), ia.decidir(r, b, a));
			while (!r.terminada()) {
				Golpe g = r.golpesValidos(a).stream().filter(Golpe::danoDireto).findFirst().orElse(a.ativo().golpes().get(0));
				r.rodada(Decisao.golpe(g), ia.decidir(r, b, a));
			}
			Map<Integer, Long> xp = Premiacao.liquidar(r, a, regras, Premiacao.PVE_SELVAGEM);
			if (r.vencedor().orElse(null) != a) {
				assertTrue(xp.isEmpty(), "derrota não dá XP");
				continue;
			}
			conferidas++;
			// Taturico nível 50, Comum, P = 50: floor((25 + 750) × 1 × 1 × 1) = 775
			assertEquals(775, xp.values().stream().mapToLong(Long::longValue).sum());
			assertEquals(a.participantes(), List.copyOf(xp.keySet()));
			assertTrue(a.participantes().containsAll(List.of(0, 1)));
			if (!a.participantes().contains(2))
				assertFalse(xp.containsKey(2), "a reserva que não entrou não recebe");
			if (a.participantes().size() == 2) {
				assertEquals(388, xp.get(0));   // 775 = 388 + 387: o resto vai para quem entrou primeiro
				assertEquals(387, xp.get(1));
			} else {
				assertEquals(List.of(259L, 258L, 258L), List.copyOf(xp.values()));
			}
		}
		assertTrue(conferidas > 0);
		// recompensa com desafio: oponente 10 níveis acima vale ×1,30; derrota/captura não liquidam
		assertEquals((long) Math.floor((25 + 15 * 60) * 1.3), regras.recompensa(60, "Comum", 50, Premiacao.PVE_SELVAGEM));
	}
}
