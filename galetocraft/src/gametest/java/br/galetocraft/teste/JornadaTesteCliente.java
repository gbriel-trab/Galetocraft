package br.galetocraft.teste;

import br.galetocraft.entidade.GaloEntity;
import br.galetocraft.registro.ModAnexos;
import br.galetocraft.registro.ModEntidades;
import br.galetocraft.registro.ModItens;
import br.galetocraft.treinador.Treinador;
import net.fabricmc.fabric.api.client.gametest.v1.FabricClientGameTest;
import net.fabricmc.fabric.api.client.gametest.v1.context.ClientGameTestContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestServerContext;
import net.fabricmc.fabric.api.client.gametest.v1.context.TestSingleplayerContext;
import net.minecraft.core.BlockPos;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.phys.AABB;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * Decisões do criador de 18/11/2026 (base rev. 9), jogadas no cliente:
 * <ol>
 * <li>kit de início: Pena ao entrar e escolha única do inicial (nível 5);</li>
 * <li>posse da Pena: jogada no chão, ela some; o comando de recuperação dá uma nova versão;</li>
 * <li>nível dos selvagens: sorteado de 1 a 70;</li>
 * <li>aparecimento natural: o Vagaló está na lista de criaturas das planícies (mundo plano de teste);</li>
 * <li>companheiro: segue o treinador, não leva dano, não é desafiado e é recolhido;</li>
 * <li>escalação: com 4 Galetos, a Rinha só começa depois de escolher 3, e o 1º escolhido entra em campo;</li>
 * <li>libertar: confirmação dupla e o Galeto volta ao mundo como selvagem.</li>
 * </ol>
 * Grava o chat em {@code jornada_teste.log}. Para rodar só ele: GALETO_TESTES=jornada.
 */
@SuppressWarnings("UnstableApiUsage")
public class JornadaTesteCliente implements FabricClientGameTest {
	@Override
	public void runTest(ClientGameTestContext contexto) {
		if (System.getenv("GALETO_BENCH") != null || Testes.pular("jornada"))
			return;
		ChatTeste chat = new ChatTeste(contexto, "jornada_teste.log");
		Testes.prepararCliente(contexto);

		try (TestSingleplayerContext mundo = contexto.worldBuilder().create()) {
			contexto.waitTicks(40);
			final TestServerContext servidor = mundo.getServer();
			servidor.runCommand("time set noon");
			servidor.runCommand("weather clear");
			servidor.runCommand("tp @p 0 -60 -3 0 0");

			// 1) kit de início
			chat.exigir(chat.contem("Início da jornada: você recebeu a Pena de Captura!"), "faltou a Pena do kit");
			chat.exigir(contexto.computeOnClient(mc -> mc.player.getMainHandItem().is(ModItens.PENA_DE_CAPTURA)), "a Pena não está na mão");
			chat.comando(chat.botao("/galetocraft inicial 4"));
			chat.exigir(chat.contem("Cocórak é o seu Galeto inicial!"), "a escolha do inicial falhou");
			chat.comando("galetocraft inicial 1");
			chat.exigir(chat.contem("Você já escolheu seu Galeto inicial."), "o inicial pôde ser escolhido duas vezes");
			Treinador t1 = servidor.computeOnServer(JornadaTesteCliente::treinador);
			chat.exigir(t1.equipe().size() == 1 && t1.equipe().get(0).especie() == 4 && t1.equipe().get(0).nivel() == 5 && t1.inicialEscolhido(),
					"Cocórak Nv5 deveria ser o único da equipe: " + t1);

			// 2) posse da Pena: no chão ela some; a recuperação dá uma versão nova
			contexto.getInput().pressKey(o -> o.keyDrop);
			contexto.waitTicks(10);
			chat.exigir(servidor.computeOnServer(s -> s.overworld().getEntitiesOfClass(net.minecraft.world.entity.item.ItemEntity.class,
					new AABB(-20, -70, -20, 20, 0, 20)).isEmpty()), "a Pena ficou no chão");
			chat.exigir(!contexto.computeOnClient(mc -> mc.player.getInventory().contains(s -> s.is(ModItens.PENA_DE_CAPTURA))), "a Pena não saiu do inventário");
			chat.comando("galetocraft pena");
			chat.exigir(servidor.computeOnServer(s -> treinador(s).penaVersao() == 2), "a Pena recuperada deveria ser a versão 2");

			// 3) nível dos selvagens: 1 a 70
			for (int i = 0; i < 8; i++)
				servidor.runCommand("summon galetocraft:taturico " + (i * 2 - 8) + " -60 8");
			contexto.waitTicks(5);
			List<Integer> niveis = servidor.computeOnServer(s -> s.overworld().getEntitiesOfClass(GaloEntity.class, new AABB(-20, -70, 0, 20, 0, 20))
					.stream().map(GaloEntity::nivel).toList());
			Set<Integer> distintos = new HashSet<>(niveis);
			chat.exigir(niveis.size() == 8 && niveis.stream().allMatch(n -> n >= 1 && n <= 70) && distintos.size() > 1,
					"níveis fora de 1–70 ou todos iguais: " + niveis);
			servidor.runCommand("kill @e[type=galetocraft:taturico]");

			// 4) aparecimento natural registrado nas planícies (mundo plano de teste)
			boolean vagaloNasPlanicies = servidor.computeOnServer(s -> s.overworld().getBiome(new BlockPos(0, -60, 0)).value().getMobSettings()
					.getMobs(MobCategory.CREATURE).unwrap().stream().anyMatch(w -> w.value().type() == ModEntidades.VAGALO));
			chat.exigir(vagaloNasPlanicies, "o Vagaló não está na lista de aparecimento das planícies");

			// 5) companheiro
			servidor.runCommand("execute as @p run galetocraft dar taturico 50");
			servidor.runCommand("execute as @p run galetocraft dar vagalo 50");
			servidor.runCommand("execute as @p run galetocraft dar morcegalo 50");
			chat.comando("galetocraft companheiro 1");
			contexto.waitTicks(10);
			chat.exigir(chat.contem("Taturico está acompanhando você"), "o companheiro não veio");
			float vidaAntes = servidor.computeOnServer(s -> companheiro(s).getHealth());
			servidor.runCommand("damage @e[type=galetocraft:taturico,limit=1] 5");
			chat.exigir(servidor.computeOnServer(s -> companheiro(s).getHealth()) == vidaAntes, "o companheiro levou dano");
			chat.comando("galetocraft desafiar");
			chat.exigir(chat.contem("Nenhum Galeto selvagem a até 10 blocos."), "o companheiro foi desafiado");
			chat.comando("galetocraft recolher");
			contexto.waitTicks(5);
			chat.exigir(servidor.computeOnServer(s -> s.overworld().getEntitiesOfClass(GaloEntity.class, new AABB(-40, -70, -40, 40, 0, 40)).isEmpty()),
					"o companheiro não foi recolhido");

			// 6) escalação com 4 Galetos: escolhe Morcegalo (3), Taturico (1) e Vagaló (2); o Morcegalo começa
			servidor.runCommand("summon galetocraft:espinhoco 0 -60 2 {Rotation:[180f,0f],galeto_nivel:30,galeto_sexo:\"F\",galeto_ivs:[I;20,20,20,20,20,20]}");
			contexto.waitTicks(5);
			chat.comando("galetocraft desafiar");
			chat.exigir(chat.contem("Escalação (escolha 3; o 1º começa)"), "a escalação não apareceu");
			chat.comando(chat.botao("/galetocraft escalar 0"));   // tira o Cocórak
			chat.comando(chat.botao("/galetocraft escalar 1"));   // tira o Taturico
			chat.comando(chat.botao("/galetocraft escalar 2"));   // tira o Vagaló
			chat.comando(chat.botao("/galetocraft escalar 3"));   // Morcegalo é o 1º
			chat.comando(chat.botao("/galetocraft escalar 1"));
			chat.comando(chat.botao("/galetocraft escalar 2"));
			chat.comando(chat.botao("/galetocraft escalar ok"));
			chat.exigir(chat.contem("Rinha: Player0 (Morcegalo) × Selvagem (Espinhocó)"), "a escalação não definiu quem começa");
			contexto.takeScreenshot("jornada_escalacao");
			chat.comando("galetocraft acao fugir");

			// 7) libertar com confirmação dupla
			chat.comando("galetocraft libertar 3");
			chat.comando(chat.botao("/galetocraft libertar 3 confirmar"));
			chat.comando(chat.botao("/galetocraft libertar 3 definitivo"));
			chat.exigir(chat.contem("Morcegalo foi libertado e voltou à natureza."), "a libertação falhou");
			Treinador t2 = servidor.computeOnServer(JornadaTesteCliente::treinador);
			chat.exigir(t2.equipe().size() == 3 && t2.equipe().stream().noneMatch(g -> g.especie() == 10), "o Morcegalo continuou na equipe: " + t2);
			chat.exigir(servidor.computeOnServer(s -> !s.overworld().getEntitiesOfClass(GaloEntity.class, new AABB(-40, -70, -40, 40, 0, 40),
					g -> g.especie().equals("morcegalo") && !g.companheiro()).isEmpty()), "o Morcegalo libertado não apareceu no mundo");
			chat.gravar("ok: jornada, Pena, níveis " + niveis + ", aparecimento, companheiro, escalação e libertar");
		}
	}

	private static Treinador treinador(MinecraftServer s) {
		ServerPlayer p = s.getPlayerList().getPlayers().get(0);
		return ModAnexos.treinador(p);
	}

	private static GaloEntity companheiro(MinecraftServer s) {
		return s.overworld().getEntitiesOfClass(GaloEntity.class, new AABB(-40, -70, -40, 40, 0, 40), GaloEntity::companheiro).get(0);
	}
}
