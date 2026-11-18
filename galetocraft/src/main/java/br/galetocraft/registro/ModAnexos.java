package br.galetocraft.registro;

import br.galetocraft.GaletocraftMod;
import br.galetocraft.treinador.Treinador;
import net.fabricmc.fabric.api.attachment.v1.AttachmentRegistry;
import net.fabricmc.fabric.api.attachment.v1.AttachmentType;
import net.minecraft.world.entity.player.Player;

/** Dados presos ao jogador e salvos com ele (Fabric Data Attachment). */
public final class ModAnexos {
	/** Equipe, reservas e Pena de Captura do treinador. Sobrevive à morte do jogador. */
	public static final AttachmentType<Treinador> TREINADOR = AttachmentRegistry.create(GaletocraftMod.id("treinador"),
			b -> b.persistent(Treinador.CODEC).copyOnDeath().initializer(() -> Treinador.NOVO));

	/** Marca do mundo: o Quetzacocó (Lendário Original, único) já foi capturado e não aparece mais. */
	public static final AttachmentType<Boolean> QUETZACOCO_CAPTURADO = AttachmentRegistry.create(GaletocraftMod.id("quetzacoco_capturado"),
			b -> b.persistent(com.mojang.serialization.Codec.BOOL).initializer(() -> false));

	private ModAnexos() {
	}

	public static void registrar() {
	}

	public static Treinador treinador(Player p) {
		return p.getAttachedOrCreate(TREINADOR);
	}

	public static void salvar(Player p, Treinador t) {
		p.setAttached(TREINADOR, t);
	}
}
