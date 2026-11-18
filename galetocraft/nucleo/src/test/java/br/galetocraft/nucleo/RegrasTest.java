package br.galetocraft.nucleo;

import br.galetocraft.nucleo.dados.Atributo;
import br.galetocraft.nucleo.dados.Elemento;
import br.galetocraft.nucleo.dados.Especie;
import br.galetocraft.nucleo.dados.EstadoNegativo;
import br.galetocraft.nucleo.dados.Galetario;
import br.galetocraft.nucleo.dados.Golpe;
import br.galetocraft.nucleo.regras.Ambiente;
import br.galetocraft.nucleo.regras.Captura;
import br.galetocraft.nucleo.regras.DanoV56;
import br.galetocraft.nucleo.regras.Eficacia;
import br.galetocraft.nucleo.regras.Energia;
import br.galetocraft.nucleo.regras.Estados;
import br.galetocraft.nucleo.regras.Experiencia;
import br.galetocraft.nucleo.regras.MiraAnatomica;
import br.galetocraft.nucleo.regras.MiraAnatomica.Guarda;
import br.galetocraft.nucleo.regras.MiraAnatomica.Regiao;
import br.galetocraft.nucleo.regras.PenaDeRitmo;
import br.galetocraft.nucleo.regras.Progressao;
import br.galetocraft.nucleo.regras.Velocidade;
import org.junit.jupiter.api.Test;

import java.math.BigDecimal;
import java.util.List;

import static br.galetocraft.nucleo.dados.Elemento.*;
import static org.junit.jupiter.api.Assertions.*;

/** Testes das regras oficiais contra os exemplos e valores das normas homologadas. */
class RegrasTest {
	static final Galetario G = Galetario.padrao();

	@Test
	void galetarioCarregaABaseVigente() {
		assertEquals(23, G.especies().size());
		assertTrue(G.revisaoBase() >= 6);
		int vinculos = G.especies().stream().mapToInt(e -> e.golpes().size()).sum();
		assertEquals(690, vinculos);
		for (Especie e : G.especies()) {
			assertEquals(5, e.originais().size(), e.nome());
			assertEquals(25, e.aprendiveis().size(), e.nome());
			assertEquals(6, e.atributos().size(), e.nome());
		}
		Especie sirenoco = G.especie(22);
		assertEquals("Sirenocó", sirenoco.nome());
		assertEquals(List.of(AGUA, AR), sirenoco.elementos());
		assertEquals(160, sirenoco.atributo(Atributo.ATAQUE_MAGICO));
		assertEquals(550, sirenoco.total());
		assertEquals("Partitura das Marés", sirenoco.passiva());
		assertEquals(0.0, sirenoco.probabilidadeMacho());
		assertEquals("Ária da Maré Eterna", sirenoco.hereditario());
		assertFalse(G.especie(23).reproduz());
		assertEquals(700, G.especie(23).total());
	}

	@Test
	void golpesOriginaisCompletosNaRevisao6() {
		Golpe punho = G.especie(4).golpe("Punho das Dunas");
		assertEquals(EstadoNegativo.TONTO, punho.estadoAplicado());
		assertEquals(0.2, punho.chanceEstado());
		assertTrue(G.especie(4).golpe("Prisão das Areias").danoDireto());
		for (Especie e : G.especies())
			for (Golpe g : e.golpes())
				assertFalse(g.efeito() != null && g.efeito().contains("Sem descrição textual"), e.nome() + " / " + g.nome());
	}

	@Test
	void matrizElementalTemDuasVantagensEDuasFraquezas() {
		Eficacia ef = new Eficacia(G);
		List<Elemento> basicos = List.of(FOGO, AGUA, PLANTA, TERRA, AR, ELETRICO);
		for (Elemento a : basicos) {
			long fortes = basicos.stream().filter(d -> ef.fator(a, d) == 2.0).count();
			long fracos = basicos.stream().filter(d -> ef.fator(a, d) == 0.5).count();
			assertEquals(2, fortes, a.nome());
			assertEquals(2, fracos, a.nome());
			for (Elemento d : basicos)       // reciprocidade: 2× de ida implica 0,5× de volta
				if (ef.fator(a, d) == 2.0)
					assertEquals(0.5, ef.fator(d, a));
		}
		assertEquals(2.0, ef.fator(FOGO, PLANTA));
		assertEquals(0.5, ef.fator(FOGO, AGUA));
		assertEquals(1.0, ef.multiplicador(NEUTRO, List.of(FOGO)));
	}

	@Test
	void tipagemDuplaV1ENexo() {
		Eficacia ef = new Eficacia(G);
		assertEquals(4.0, ef.multiplicador(ELETRICO, G.especie(22).elementos()));   // Sirenocó
		assertEquals(4.0, ef.multiplicador(ELETRICO, G.especie(16).elementos()));   // Libelocó
		assertEquals(4.0, ef.multiplicador(TERRA, G.especie(15).elementos()));      // Faíscocó
		assertEquals(4.0, ef.multiplicador(AR, G.especie(17).elementos()));         // Castorocó
		assertEquals(4.0, ef.multiplicador(AR, G.especie(21).elementos()));         // Cabacocó
		assertEquals(0.25, ef.multiplicador(TERRA, G.especie(22).elementos()));
		// Quetzacocó (Ar + Planta + Nexo): tabela final da regra nexo
		List<Elemento> q = G.especie(23).elementos();
		assertEquals(2.0, ef.multiplicador(FOGO, q));
		assertEquals(2.0, ef.multiplicador(ELETRICO, q));
		assertEquals(2.0, ef.multiplicador(NEXO, q));
		assertEquals(0.5, ef.multiplicador(AGUA, q));
		assertEquals(0.5, ef.multiplicador(TERRA, q));
		assertEquals(0.5, ef.multiplicador(PLANTA, q));
		assertEquals(1.0, ef.multiplicador(AR, q));
	}

	@Test
	void progressaoNivel50() {
		assertEquals(0, new BigDecimal("85").compareTo(Progressao.atributo(85, 50)));
		assertEquals(0, new BigDecimal("127.5").compareTo(Progressao.atributo(85, 100)));
		assertEquals(0, new BigDecimal("106.25").compareTo(Progressao.atributo(85, 75)));
		// níveis 1–49 (R5.4): 25% no 1, 121/196 no 25, 193/196 no 49
		assertEquals(0, new BigDecimal("21.25").compareTo(Progressao.atributo(85, 1)));
		assertEquals(0, Progressao.atributo(196, 25).compareTo(new BigDecimal("121")));
		assertEquals(0, Progressao.atributo(196, 49).compareTo(new BigDecimal("193")));
		assertThrows(IllegalArgumentException.class, () -> Progressao.atributo(85, 0));
		assertThrows(IllegalArgumentException.class, () -> Progressao.atributo(85, 101));
	}

	@Test
	void hpNominalEReferenciaDaVitalidade() {
		// HP nominal (R5.4): 10 no nível 1, ceil(1,5 × HP50) no 50, ceil(2,25 × HP50) no 100
		assertEquals(10, Progressao.hpNominal(85, 1));
		assertEquals(128, Progressao.hpNominal(85, 50));      // Taturico: ceil(127,5)
		assertEquals(192, Progressao.hpNominal(85, 100));     // ceil(191,25)
		assertEquals(120, Progressao.hpNominal(80, 50));
		// HP_ref = floor(1,05 × HP_n(L; 80)): valores da tabela gc54_curva_niveis (R5.4)
		assertEquals(10, Progressao.hpReferencia(1));
		assertEquals(67, Progressao.hpReferencia(25));
		assertEquals(126, Progressao.hpReferencia(50));
		assertEquals(157, Progressao.hpReferencia(75));
		assertEquals(189, Progressao.hpReferencia(100));
		// Vitalidade V5.6.1: HP abaixo da referência não reduz; o máximo de redução é 20%
		assertEquals(1.0, Progressao.vitalidade(50, 100));
		assertEquals(Math.pow(126.0 / 252, 0.2), Progressao.vitalidade(50, 252), 1e-12);
		assertEquals(0.8, Progressao.vitalidade(50, 5000));
	}

	@Test
	void ivEvEPeso() {
		// IV 20 = +5%; EV 100 = +5%; floor no fim
		assertEquals(84, Progressao.comIvEv(new BigDecimal("80"), 20, 0));
		assertEquals(88, Progressao.comIvEv(new BigDecimal("80"), 20, 100));
		assertEquals(85, Progressao.comIvEv(new BigDecimal("85"), 1, 0));       // 85,2125 → 85
		// peso V1.2: r = 1,5 → HP +5%, defesas +7,5%, Velocidade −25%; r = 0,8 → HP −8%, defesas −10%, Velocidade +4%
		assertEquals(105, Progressao.comPeso(100, Atributo.HP, 1.5));
		assertEquals(108, Progressao.comPeso(100, Atributo.DEFESA_FISICA, 1.5));   // 107,5 → 108 (empate para cima)
		assertEquals(75, Progressao.comPeso(100, Atributo.VELOCIDADE, 1.5));
		assertEquals(92, Progressao.comPeso(100, Atributo.HP, 0.8));
		assertEquals(90, Progressao.comPeso(100, Atributo.DEFESA_MAGICA, 0.8));
		assertEquals(104, Progressao.comPeso(100, Atributo.VELOCIDADE, 0.8));
		assertEquals(100, Progressao.comPeso(100, Atributo.ATAQUE_FISICO, 1.5));    // ataques não mudam
		assertEquals(1, Progressao.comPeso(1, Atributo.VELOCIDADE, 1.5));          // mínimo 1
		// cadeia completa: Taturico nível 50, IV 20, EV 0, peso neutro → HP 134 (128 × 1,05 = 134,4)
		assertEquals(134, Progressao.atributoFinal(Atributo.HP, 85, 50, 20, 0, 1.0));
	}

	@Test
	void danoV56ExemplosOficiais() {
		int[][] exemplos = {{200, 40, 100, 100, 20}, {200, 80, 100, 100, 40}, {350, 80, 100, 100, 70},
				{200, 80, 160, 80, 65}, {200, 80, 80, 160, 25}, {200, 180, 100, 100, 90}};
		for (int[] x : exemplos)
			assertEquals(x[4], DanoV56.calcular(new DanoV56.Entrada(x[0], x[1], x[2], x[3])).dano());
	}

	@Test
	void danoV56Modificadores() {
		assertEquals(26, dano(new DanoV56.Entrada(200, 80, 100, 100).guarda(Guarda.CORRETA)));
		assertEquals(44, dano(new DanoV56.Entrada(200, 80, 100, 100).guarda(Guarda.ERRADA)));
		assertEquals(46, dano(new DanoV56.Entrada(200, 80, 100, 100).anatomia(DanoV56.Anatomia.EXPOSICAO)));
		assertEquals(50, dano(new DanoV56.Entrada(200, 80, 100, 100).anatomia(DanoV56.Anatomia.RUPTURA)));
		assertEquals(10, dano(new DanoV56.Entrada(200, 80, 100, 100).defesaEspecial()));
		assertEquals(45, dano(new DanoV56.Entrada(200, 80, 100, 100).cantoOfensivo()));
		// Guarda correta anula a Exposição
		assertEquals(26, dano(new DanoV56.Entrada(200, 80, 100, 100).guarda(Guarda.CORRETA).anatomia(DanoV56.Anatomia.EXPOSICAO)));
		// 2º acerto usa 50% da base; eficácia 2× dobra
		assertEquals(20, dano(new DanoV56.Entrada(200, 80, 100, 100).segundoAcerto()));
		assertEquals(80, dano(new DanoV56.Entrada(200, 80, 100, 100).eficacia(2.0)));
		// mínimo 1 para acerto válido; anulado dá 0
		assertEquals(1, dano(new DanoV56.Entrada(10, 1, 1, 500)));
		assertEquals(0, dano(new DanoV56.Entrada(200, 80, 100, 100).anulado()));
	}

	private static int dano(DanoV56.Entrada e) {
		return DanoV56.calcular(e).dano();
	}

	@Test
	void velocidadeEsquivaEGolpeDuplo() {
		assertEquals(7.5, Velocidade.chanceEsquivaPercentual(100, 100), 1e-12);
		assertEquals(5.0, Velocidade.chanceEsquivaPercentual(300, 10), 1e-12);
		assertEquals(10.0, Velocidade.chanceEsquivaPercentual(10, 300), 1e-12);
		assertEquals(0.25, Velocidade.chanceGolpeDuplo(100, 100), 1e-12);
		assertEquals(0.50, Velocidade.chanceGolpeDuplo(150, 100), 1e-12);
		assertEquals(0.50, Velocidade.chanceGolpeDuplo(300, 100), 1e-12);
		assertEquals(0.0, Velocidade.chanceGolpeDuplo(99, 100), 1e-12);
		assertEquals(0.4375, Velocidade.combinar(0.25, 0.25), 1e-12);
		assertThrows(IllegalArgumentException.class, () -> Velocidade.chanceGolpeDuplo(100, 0));
	}

	@Test
	void pressaoDaMiraAnatomica() {
		assertEquals(0, MiraAnatomica.pressao(0, 200, Regiao.TRONCO, Guarda.NEUTRA, false));
		assertEquals(31, MiraAnatomica.pressao(40, 200, Regiao.TRONCO, Guarda.NEUTRA, false));       // floor(58 × 0,55)
		assertEquals(12, MiraAnatomica.pressao(40, 200, Regiao.CABECA_CRINA, Guarda.CORRETA, false)); // floor(63,8 × 0,2)
		assertEquals(65, MiraAnatomica.pressao(40, 200, Regiao.ASAS, Guarda.ERRADA, false));          // 58 + 10 → teto 65
		assertEquals(64, MiraAnatomica.pressao(40, 200, Regiao.ASAS, Guarda.NEUTRA, true));           // 58 + 6
		assertEquals(1, MiraAnatomica.pressao(1, 10000, Regiao.TRONCO, Guarda.CORRETA, false));       // mínimo 1
		MiraAnatomica.Medidor m = new MiraAnatomica.Medidor();
		assertFalse(m.somar(50));
		assertTrue(m.exposta());
		m.decair();
		assertEquals(40, m.valor());
		assertTrue(m.somar(65));
		assertEquals(0, m.valor());
	}

	@Test
	void energiaEPenaDeRitmo() {
		assertEquals(100, Energia.inicioDoTurno(95, false));
		assertEquals(10, Energia.inicioDoTurno(30, true));
		assertEquals(100, Energia.somar(80, Energia.CONCENTRACAO));
		assertEquals(0, Energia.custoComCantoSuporte(10));
		PenaDeRitmo pena = new PenaDeRitmo();
		assertTrue(pena.aoConcentrar());
		assertFalse(pena.disponivel());          // não na própria ação
		assertFalse(pena.aoConcentrar());        // não cria nem renova
		pena.fimDaOportunidade();                // fim da oportunidade em que foi criada
		assertTrue(pena.disponivel());
		pena.fimDaOportunidade();                // 1ª oportunidade válida
		assertTrue(pena.disponivel());
		pena.fimDaOportunidade();                // 2ª oportunidade válida: expira
		assertFalse(pena.ativa());
	}

	@Test
	void estados() {
		assertEquals(10, Estados.danoQueimadura(200));
		assertEquals(11, Estados.danoQueimadura(201));
		int[] veneno = new int[6];
		for (int i = 0; i < 6; i++)
			veneno[i] = Estados.danoEnvenenamento(200, i + 1);
		assertArrayEquals(new int[]{20, 20, 40, 40, 60, 60}, veneno);
		assertEquals(75, Estados.velocidadeParalisada(100));
		assertEquals(1, Estados.velocidadeParalisada(1));
		assertEquals(EstadoNegativo.TONTO, EstadoNegativo.deTexto("Tontura"));
	}

	@Test
	void climasESantuarios() {
		Ambiente a = new Ambiente(G);
		assertEquals(0.25, a.bonusDano(Ambiente.Clima.CHUVA, null, AGUA), 1e-12);
		assertEquals(-0.25, a.bonusDano(Ambiente.Clima.CHUVA, null, FOGO), 1e-12);
		assertEquals(0.25, a.bonusDano(Ambiente.Clima.CHUVA, Ambiente.Santuario.RAIOS, ELETRICO), 1e-12);   // 0,10 + 0,15
		assertEquals(0.15, a.bonusDano(null, Ambiente.Santuario.RAIZES, PLANTA), 1e-12);
		assertEquals(-0.25, a.bonusDano(Ambiente.Clima.VENTANIA, null, PLANTA), 1e-12);
		assertEquals(0.10, a.bonusDefesa(Ambiente.Clima.VENTANIA, List.of(AGUA, AR), Atributo.DEFESA_MAGICA), 1e-12);
		assertEquals(0.10, a.bonusDefesa(Ambiente.Clima.TEMPESTADE_AREIA, List.of(TERRA), Atributo.DEFESA_FISICA), 1e-12);
		assertEquals(10, a.energiaExtra(Ambiente.Santuario.RAIOS, List.of(ELETRICO)));
		assertEquals(0, a.energiaExtra(Ambiente.Santuario.RAIOS, List.of(FOGO)));
		assertEquals(0.04, a.cura(Ambiente.Santuario.RAIZES, List.of(PLANTA, TERRA)), 1e-12);
	}

	@Test
	void captura() {
		Captura c = new Captura(G);
		assertEquals(100 * 1.8 / 2.8, c.chancePercentual(Captura.Modalidade.MUNDO, "Comum", 1, 1, 0, 0, null), 1e-9);
		assertEquals(0, c.chancePercentual(Captura.Modalidade.MUNDO, "Lendário", 4, 50, 0, 0, null));
		assertTrue(c.chancePercentual(Captura.Modalidade.MUNDO, "Lendário", 5, 50, 0, 0, null) > 0);
		assertFalse(c.elegivel("Lendário Original", 5));    // classe sem regra de captura definida
		double forca = 0.3 * 2.5 * (1 + 1.5 * 0.5) * 1.55;  // Mítico, Pena 5, metade do HP, Sono
		double d = 1 + 49 / 60.0;
		assertEquals(100 * forca / (forca + d), c.chancePercentual(Captura.Modalidade.RINHA, "Mítico", 5, 50, 100, 200, "Sono"), 1e-9);
		assertEquals(15 + 2 * 10, c.xpPena("Comum", 10));
		assertEquals(60, c.cooldownMundo("Lendário"));
		assertEquals(20, c.cooldownMundo("Mítico"));
	}

	@Test
	void experiencia() {
		Experiencia x = new Experiencia(G);
		assertEquals(0, Experiencia.xpTotal(1));
		assertEquals(11, Experiencia.xpTotal(2));
		assertEquals(970299 + 98010, Experiencia.xpTotal(100));
		assertEquals(2, Experiencia.nivelPorXp(11));
		assertEquals(175, x.recompensa(10, "Comum", 10, "PvE_selvagem"));
		assertEquals((long) Math.floor(175 * 2.3 * 0.75), x.recompensa(10, "Mítico", 10, "PvP_valido"));
		assertEquals(1.5, Experiencia.fatorDesafio(100, 1), 1e-12);
		assertEquals(0.25, Experiencia.fatorDesafio(1, 100), 1e-12);
		assertThrows(IllegalArgumentException.class, () -> x.recompensa(50, "Lendário Original", 50, "PvE_selvagem"));
	}

	@Test
	void penaDeCapturaEvoluiPelaXpAcumulada() {
		Captura c = new Captura(Galetario.padrao());
		assertEquals(1, c.nivelPena(0));
		assertEquals(1, c.nivelPena(999));
		assertEquals(2, c.nivelPena(1000));
		assertEquals(3, c.nivelPena(4000));
		assertEquals(4, c.nivelPena(11000));
		assertEquals(5, c.nivelPena(26000));
		assertEquals(26000, c.xpParaNivelPena(5));
		// excedente reaproveitado e várias evoluções numa captura
		assertEquals(4100, c.somarXpPena(900, 3200));
		assertEquals(3, c.nivelPena(c.somarXpPena(900, 3200)));
		// no nível 5 não entra XP nova; a excedente fica
		assertEquals(26050, c.somarXpPena(25990, 60));
		assertEquals(26050, c.somarXpPena(26050, 500));
		// XP por captura: base da raridade + 2 × nível do alvo (Comum nível 50 = 115)
		assertEquals(115, c.xpPena("Comum", 50));
	}

	@Test
	void aprendizadoPorNivelESlots() {
		Galetario g = Galetario.padrao();
		br.galetocraft.nucleo.regras.Aprendizado ap = new br.galetocraft.nucleo.regras.Aprendizado(g);
		Especie piro = g.especie(1);
		assertTrue(ap.temTabela(piro));
		assertEquals(30, ap.tabela(piro).size());
		assertEquals(15, ap.porNivel(piro, 50).size());                 // 15 por nível, origem incluída
		assertEquals(15, ap.porTreinamento(piro).size());
		assertTrue(ap.porNivel(piro, 50).contains(piro.golpe("Ave Fênix")));
		assertFalse(ap.porNivel(piro, 49).contains(piro.golpe("Ave Fênix")));   // hereditário no nível 50
		assertTrue(ap.origemCompleta(piro, 50));
		assertFalse(ap.origemCompleta(piro, 49));
		assertEquals(piro.originais(), ap.equipamentoInicial(piro, 50));
		assertEquals(2, ap.porNivel(piro, 1).size());                   // nível 1: básico + Concentração
		// #022 Sirenocó: marcos homologados em 13/11; #013 sem tabela: só os 5 de origem
		assertEquals(15, ap.porNivel(g.especie(22), 50).size());
		assertFalse(ap.temTabela(g.especie(13)));
		assertEquals(g.especie(13).originais(), ap.porNivel(g.especie(13), 50));
		// slots: Concentração fixa, só golpes aprendidos
		List<Golpe> origem = piro.originais();
		Golpe conc = origem.stream().filter(Golpe::concentracao).findFirst().orElseThrow();
		Golpe porNivel = ap.porNivel(piro, 50).stream().filter(x -> !origem.contains(x)).findFirst().orElseThrow();
		ap.validarEquipamento(piro, 50, List.of(conc, porNivel), List.of());
		assertThrows(IllegalArgumentException.class, () -> ap.validarEquipamento(piro, 50, List.of(porNivel), List.of()));
		Golpe treino = ap.porTreinamento(piro).get(0);
		assertThrows(IllegalArgumentException.class, () -> ap.validarEquipamento(piro, 50, List.of(conc, treino), List.of()));
		ap.validarEquipamento(piro, 50, List.of(conc, treino), List.of(treino));
	}
}
