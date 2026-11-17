package br.galetocraft.client;

import java.util.ArrayList;
import java.util.List;

import br.galetocraft.GaletocraftMod;
import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.state.LivingEntityRenderState;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.phys.AABB;
import software.bernie.geckolib.animatable.GeoAnimatable;
import software.bernie.geckolib.cache.model.BakedGeoModel;
import software.bernie.geckolib.cache.model.GeoBone;
import software.bernie.geckolib.model.DefaultedEntityGeoModel;
import software.bernie.geckolib.renderer.GeoEntityRenderer;
import software.bernie.geckolib.renderer.base.BoneSnapshots;
import software.bernie.geckolib.renderer.base.RenderPassInfo;

/**
 * Desenha um galo do Galetocraft com o modelo do GeckoLib:
 * assets/galetocraft/geckolib/models/entity/&lt;id&gt;.geo.json + textures/entity/&lt;id&gt;.png.
 * O brilho (textures/entity/&lt;id&gt;_glowmask.png) só é redesenhado nos ossos '_brilho'.
 * <p>
 * LOD (nível de detalhe): o exportador separa as peças miúdas em ossos '_lod1', '_lod2' e '_lod3'. De longe elas
 * viram 1 ou 2 pixels, então são escondidas: nível 1 a partir de 16 blocos, 2 a partir de 32, 3 a partir de 48.
 * A distância é corrigida pela resolução e pelo campo de visão (em 4K ou com FOV fechado o galo parece maior,
 * então os detalhes somem mais longe); com a luneta, tudo aparece.
 */
public class GaloRenderer<T extends LivingEntity & GeoAnimatable> extends GeoEntityRenderer<T, LivingEntityRenderState> {
	private static final double[] DISTANCIA_LOD = {16, 32, 48};
	private static final double TAN_FOV_REFERENCIA = Math.tan(Math.toRadians(70) / 2);

	private final double folga;
	private BakedGeoModel modeloLod;
	private List<List<String>> ossosLod = List.of();

	/**
	 * @param especie id da espécie (nome dos arquivos do modelo, textura e animações)
	 * @param sombra  raio da sombra no chão
	 * @param folga   quanto o modelo passa da caixa de colisão para os lados (asas, cauda): sem isto ele some na
	 *                borda da tela antes de sair dela
	 */
	public GaloRenderer(EntityRendererProvider.Context contexto, String especie, float sombra, double folga) {
		super(contexto, new DefaultedEntityGeoModel<>(GaletocraftMod.id(especie)));
		withRenderLayer(BrilhoParcialGeoLayer::new);
		this.shadowRadius = sombra;
		this.folga = folga;
	}

	@Override
	protected AABB getBoundingBoxForCulling(T entidade) {
		return super.getBoundingBoxForCulling(entidade).inflate(this.folga, 0.1, this.folga);
	}

	@Override
	public void adjustModelBonesForRender(RenderPassInfo<LivingEntityRenderState> info, BoneSnapshots ossos) {
		final int nivel = nivelDeDetalhe(info.renderState().distanceToCameraSq);

		if (nivel == 0)
			return;

		final List<List<String>> porNivel = ossosLod(info.model());

		for (int n = 1; n <= nivel && n < porNivel.size(); n++) {
			for (String nome : porNivel.get(n)) {
				ossos.ifPresent(nome, osso -> osso.skipRender(true));
			}
		}
	}

	/** 0 = completo; 1, 2, 3 = esconde os ossos '_lod1', '_lod2', '_lod3' (cumulativo). */
	private static int nivelDeDetalhe(double distanciaAoQuadrado) {
		final Minecraft mc = Minecraft.getInstance();

		if (mc.player != null && mc.player.isScoping())
			return 0;

		final double fov = Math.toRadians(mc.options.fov().get());
		final double altura = Math.max(mc.getWindow().getHeight(), 1);
		// distância "equivalente" num monitor 1080p com FOV 70: o que importa é o tamanho do galo em pixels
		final double distancia = Math.sqrt(distanciaAoQuadrado) * (1080.0 / altura) * (Math.tan(fov / 2) / TAN_FOV_REFERENCIA);
		int nivel = 0;

		for (double limite : DISTANCIA_LOD) {
			if (distancia >= limite)
				nivel++;
		}

		return nivel;
	}

	/** Nomes dos ossos de cada nível de LOD (lidos do modelo uma vez e guardados). */
	private List<List<String>> ossosLod(BakedGeoModel modelo) {
		if (modelo != this.modeloLod) {
			final List<List<String>> porNivel = new ArrayList<>();

			for (int n = 0; n <= DISTANCIA_LOD.length; n++) {
				porNivel.add(new ArrayList<>());
			}

			for (GeoBone osso : modelo.topLevelBones()) {
				coletar(osso, porNivel);
			}

			this.modeloLod = modelo;
			this.ossosLod = porNivel;
		}

		return this.ossosLod;
	}

	private static void coletar(GeoBone osso, List<List<String>> porNivel) {
		final String nome = osso.name();
		final int i = nome.lastIndexOf("_lod");

		if (i >= 0) {
			try {
				final int n = Integer.parseInt(nome.substring(i + 4));

				if (n > 0 && n < porNivel.size())
					porNivel.get(n).add(nome);
			}
			catch (NumberFormatException ignorado) {
				// não é um osso de LOD
			}
		}

		for (GeoBone filho : osso.children()) {
			coletar(filho, porNivel);
		}
	}
}
