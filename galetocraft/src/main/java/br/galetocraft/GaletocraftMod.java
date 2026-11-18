package br.galetocraft;

import br.galetocraft.comando.ComandoGaletocraft;
import br.galetocraft.nucleo.dados.Galetario;
import br.galetocraft.registro.ModAnexos;
import br.galetocraft.registro.ModEntidades;
import br.galetocraft.registro.ModItens;
import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.fabricmc.fabric.api.event.lifecycle.v1.ServerLifecycleEvents;
import net.fabricmc.fabric.api.networking.v1.ServerPlayConnectionEvents;
import br.galetocraft.rinha.GerenciadorRinhas;
import net.fabricmc.fabric.api.itemgroup.v1.ItemGroupEvents;
import net.minecraft.resources.Identifier;
import net.minecraft.world.item.CreativeModeTabs;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/** Ponto de entrada do mod (lado comum: servidor e cliente). */
public class GaletocraftMod implements ModInitializer {
	public static final String MOD_ID = "galetocraft";
	public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

	public static Identifier id(String caminho) {
		return Identifier.fromNamespaceAndPath(MOD_ID, caminho);
	}

	@Override
	public void onInitialize() {
		ModEntidades.registrar();
		ModItens.registrar();
		ModAnexos.registrar();
		// aparecimento natural, encontros raros e Quetzacocó (regra mundo_aparecimento)
		br.galetocraft.mundo.Aparecimento.registrar();
		// início da jornada e posse da Pena (kit, recuperação, Pena não fica no chão)
		br.galetocraft.treinador.Jornada.registrar();

		// os ovos dos galos aparecem na aba de ovos geradores do modo criativo
		ItemGroupEvents.modifyEntriesEvent(CreativeModeTabs.SPAWN_EGGS)
				.register(entradas -> {
					entradas.accept(ModItens.OVO_PIROCOCO);
					ModItens.OVOS_GALOS.forEach(entradas::accept);
				});
		ItemGroupEvents.modifyEntriesEvent(CreativeModeTabs.TOOLS_AND_UTILITIES).register(entradas -> entradas.accept(ModItens.PENA_DE_CAPTURA));

		// núcleo de regras: carrega a base vigente embutida (espécies, golpes e regras)
		Galetario galetario = Galetario.padrao();
		CommandRegistrationCallback.EVENT.register((dispatcher, acesso, ambiente) -> ComandoGaletocraft.registrar(dispatcher));
		// Rinha em andamento termina se o jogador sair do servidor
		ServerPlayConnectionEvents.DISCONNECT.register((conexao, servidor) -> {
			java.util.UUID id = conexao.getPlayer().getUUID();
			GerenciadorRinhas.encerrar(id);
			br.galetocraft.rinha.Escalacoes.cancelar(id);
			br.galetocraft.treinador.Companheiros.recolher(id, servidor);
		});
		ServerLifecycleEvents.SERVER_STOPPING.register(servidor -> GerenciadorRinhas.encerrarTodas());

		LOGGER.info("Galetocraft carregado: {} galos prontos! Base vigente rev. {} com {} espécies.",
				1 + ModEntidades.GALOS.size(), galetario.revisaoBase(), galetario.especies().size());
	}
}
