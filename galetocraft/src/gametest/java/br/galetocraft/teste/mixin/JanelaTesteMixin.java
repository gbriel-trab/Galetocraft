package br.galetocraft.teste.mixin;

import com.mojang.blaze3d.platform.Window;
import org.lwjgl.PointerBuffer;
import org.lwjgl.glfw.GLFW;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Shadow;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

/**
 * Só nos testes automáticos (mod "galetocraft-teste"): a janela do Minecraft abre em modo janela, no SEGUNDO monitor,
 * sem pegar o foco do que a pessoa está fazendo. Nasce escondida, vai para o segundo monitor e só então aparece,
 * sem ativar (GLFW_FOCUS_ON_SHOW = falso). Se só houver um monitor, fica no principal, também sem foco.
 */
@Mixin(Window.class)
public abstract class JanelaTesteMixin {
	@Shadow
	public abstract long handle();

	@Inject(method = "<init>", at = @At(value = "INVOKE", target = "Lorg/lwjgl/glfw/GLFW;glfwCreateWindow(IILjava/lang/CharSequence;JJ)J", remap = false))
	private void galetocraft$abrirSemFoco(CallbackInfo ci) {
		GLFW.glfwWindowHint(GLFW.GLFW_VISIBLE, GLFW.GLFW_FALSE);
		GLFW.glfwWindowHint(GLFW.GLFW_FOCUSED, GLFW.GLFW_FALSE);
		GLFW.glfwWindowHint(GLFW.GLFW_FOCUS_ON_SHOW, GLFW.GLFW_FALSE);
	}

	@Inject(method = "<init>", at = @At("RETURN"))
	private void galetocraft$irParaSegundoMonitor(CallbackInfo ci) {
		final long janela = handle();
		final long principal = GLFW.glfwGetPrimaryMonitor();
		final PointerBuffer monitores = GLFW.glfwGetMonitors();

		if (monitores != null) {
			for (int i = 0; i < monitores.limit(); i++) {
				final long monitor = monitores.get(i);

				if (monitor == principal)
					continue;

				final int[] x = new int[1], y = new int[1], largura = new int[1], altura = new int[1];
				GLFW.glfwGetMonitorWorkarea(monitor, x, y, largura, altura);
				GLFW.glfwSetWindowPos(janela, x[0] + 40, y[0] + 60);
				break;
			}
		}

		GLFW.glfwShowWindow(janela);
	}
}
