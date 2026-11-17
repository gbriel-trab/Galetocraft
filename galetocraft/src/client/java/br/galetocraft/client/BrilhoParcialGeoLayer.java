package br.galetocraft.client;

import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.minecraft.client.renderer.SubmitNodeCollector;
import net.minecraft.client.renderer.rendertype.RenderType;
import software.bernie.geckolib.animatable.GeoAnimatable;
import software.bernie.geckolib.cache.model.BakedGeoModel;
import software.bernie.geckolib.cache.model.GeoBone;
import software.bernie.geckolib.renderer.base.GeoRenderState;
import software.bernie.geckolib.renderer.base.GeoRenderer;
import software.bernie.geckolib.renderer.base.RenderPassInfo;
import software.bernie.geckolib.renderer.layer.builtin.AutoGlowingGeoLayer;
import software.bernie.geckolib.util.RenderUtil;

/**
 * Camada de brilho otimizada.
 * <p>
 * A {@link AutoGlowingGeoLayer} padrão do GeckoLib redesenha o modelo INTEIRO uma segunda vez com a textura
 * {@code _glowmask}. Esta versão percorre os mesmos ossos (para pegar as mesmas poses e animações), mas só manda
 * para a placa de vídeo os cubos dos ossos terminados em {@value #SUFIXO}: chamas, gemas e pontas de fogo.
 * O exportador ({@code ferramentas/exportar_v7.py}) separa esses cubos automaticamente pela máscara de brilho.
 */
public class BrilhoParcialGeoLayer<T extends GeoAnimatable, O, R extends GeoRenderState> extends AutoGlowingGeoLayer<T, O, R> {
	public static final String SUFIXO = "_brilho";

	public BrilhoParcialGeoLayer(GeoRenderer<T, O, R> renderer) {
		super(renderer);
	}

	@Override
	public void submitRenderTask(RenderPassInfo<R> info, SubmitNodeCollector tarefas) {
		if (!info.willRender())
			return;

		if (!temOssosDeBrilho(info.model())) {      // modelo exportado sem otimizar: brilho no modelo inteiro (como antes)
			super.submitRenderTask(info, tarefas);
			return;
		}

		final RenderType tipo = getRenderType(info.renderState());

		if (tipo == null)
			return;

		final int luz = getBrightness(info.renderState());
		final int overlay = info.packedOverlay();
		final int cor = info.renderColor();

		tarefas.order(1).submitCustomGeometry(info.poseStack(), tipo, (pose, vertices) -> {
			final PoseStack pilha = info.poseStack();

			pilha.pushPose();
			pilha.last().set(pose);
			info.renderPosed(() -> {
				for (GeoBone osso : info.model().topLevelBones()) {
					desenhar(info, pilha, osso, vertices, luz, overlay, cor);
				}
			});
			pilha.popPose();
		});
	}

	private BakedGeoModel ultimoModelo;
	private boolean ultimoTemBrilho;

	private boolean temOssosDeBrilho(BakedGeoModel modelo) {
		if (modelo != this.ultimoModelo) {
			this.ultimoModelo = modelo;
			this.ultimoTemBrilho = false;
			for (GeoBone osso : modelo.topLevelBones()) {
				if (procurar(osso)) {
					this.ultimoTemBrilho = true;
					break;
				}
			}
		}
		return this.ultimoTemBrilho;
	}

	private static boolean procurar(GeoBone osso) {
		if (osso.name().contains(SUFIXO))
			return true;
		for (GeoBone filho : osso.children()) {
			if (procurar(filho))
				return true;
		}
		return false;
	}

	/** Mesma ordem de transformações do GeckoLib, mas só desenha os cubos dos ossos de brilho. */
	private static <R extends GeoRenderState> void desenhar(RenderPassInfo<R> info, PoseStack pilha, GeoBone osso,
			VertexConsumer vertices, int luz, int overlay, int cor) {
		pilha.pushPose();
		RenderUtil.prepMatrixForBone(pilha, osso);

		if (osso.name().contains(SUFIXO))
			osso.render(info, pilha, vertices, luz, overlay, cor);

		if (osso.frameSnapshot == null || !osso.frameSnapshot.areChildrenHidden()) {
			for (GeoBone filho : osso.children()) {
				desenhar(info, pilha, filho, vertices, luz, overlay, cor);
			}
		}

		pilha.popPose();
	}
}
