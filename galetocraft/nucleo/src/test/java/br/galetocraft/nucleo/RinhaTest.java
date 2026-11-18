package br.galetocraft.nucleo;

import br.galetocraft.nucleo.dados.Especie;
import br.galetocraft.nucleo.dados.EstadoNegativo;
import br.galetocraft.nucleo.dados.Galetario;
import br.galetocraft.nucleo.dados.Golpe;
import br.galetocraft.nucleo.regras.Energia;
import br.galetocraft.nucleo.rinha.Combatente;
import br.galetocraft.nucleo.rinha.Decisao;
import br.galetocraft.nucleo.rinha.Equipe;
import br.galetocraft.nucleo.rinha.Rinha;
import br.galetocraft.nucleo.rinha.Simulador;
import org.junit.jupiter.api.Test;

import java.util.List;

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
}
