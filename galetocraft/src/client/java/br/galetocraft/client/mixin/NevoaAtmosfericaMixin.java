package br.galetocraft.client.mixin;

import br.galetocraft.client.tempestade.TempestadeCliente;
import net.minecraft.client.Camera;
import net.minecraft.client.DeltaTracker;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.renderer.fog.FogData;
import net.minecraft.client.renderer.fog.environment.AtmosphericFogEnvironment;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfoReturnable;

/** Névoa amarelada da tempestade de areia: encurta a névoa atmosférica e puxa a cor para a da areia. */
@Mixin(AtmosphericFogEnvironment.class)
public abstract class NevoaAtmosfericaMixin {
	private static final float FIM_NA_TEMPESTADE = 26f;
	private static final int R = 0xD8, G = 0xB6, B = 0x80;

	@Inject(method = "setupFog", at = @At("TAIL"))
	private void galetocraft$nevoaDeAreia(FogData nevoa, Camera camera, ClientLevel mundo, float distancia, DeltaTracker tempo, CallbackInfo ci) {
		float k = TempestadeCliente.intensidade();
		if (k <= 0f)
			return;
		nevoa.environmentalStart = lerp(nevoa.environmentalStart, 0f, k);
		nevoa.environmentalEnd = Math.min(nevoa.environmentalEnd, lerp(nevoa.environmentalEnd, FIM_NA_TEMPESTADE, k));
		nevoa.skyEnd = Math.min(nevoa.skyEnd, lerp(nevoa.skyEnd, FIM_NA_TEMPESTADE * 2, k));
		nevoa.cloudEnd = Math.min(nevoa.cloudEnd, lerp(nevoa.cloudEnd, FIM_NA_TEMPESTADE * 2, k));
	}

	@Inject(method = "getBaseColor", at = @At("RETURN"), cancellable = true)
	private void galetocraft$corDeAreia(ClientLevel mundo, Camera camera, int distancia, float parcial, CallbackInfoReturnable<Integer> cir) {
		float k = TempestadeCliente.intensidade() * 0.85f;
		if (k <= 0f)
			return;
		int c = cir.getReturnValue();
		int r = Math.round(lerp((c >> 16) & 0xFF, R, k)), g = Math.round(lerp((c >> 8) & 0xFF, G, k)), b = Math.round(lerp(c & 0xFF, B, k));
		cir.setReturnValue((c & 0xFF000000) | (r << 16) | (g << 8) | b);
	}

	private static float lerp(float a, float b, float t) {
		return a + (b - a) * t;
	}
}
