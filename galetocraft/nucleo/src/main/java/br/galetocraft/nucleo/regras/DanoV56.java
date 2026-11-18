package br.galetocraft.nucleo.regras;

import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;

/**
 * Dano direto V5.6 (regra dano_v5_6, homologada em 13/11/2026):
 * {@code D_base = HPmax_defensor × Poder/400 × (Ataque / max(1, Defesa))^0,7}.
 * <p>
 * Tudo é contínuo até o fim, com uma única arredondada para cima por acerto e mínimo 1 para acerto válido não anulado.
 * Ordem dos modificadores: fração do acerto → eficácia → bônus de dano (soma dos percentuais) → anatomia
 * (Guarda, Exposição ou Ruptura, teto ×1,40) → Defesa Especial → maior redução da mesma classe.
 * Como na referência oficial, a potência usa {@link StrictMath} e o restante usa {@link BigDecimal}.
 */
public final class DanoV56 {
	private static final MathContext MC = MathContext.DECIMAL128;
	public static final BigDecimal TETO_ANATOMICO = new BigDecimal("1.40");
	public static final BigDecimal BONUS_EXPOSICAO = new BigDecimal("0.15");
	public static final BigDecimal BONUS_RUPTURA = new BigDecimal("0.25");
	public static final BigDecimal BONUS_CANTO_OFENSIVO = new BigDecimal("0.12");
	public static final BigDecimal REDUCAO_DEFESA_ESPECIAL = new BigDecimal("0.75");
	public static final BigDecimal REDUCAO_CANTO_REVEZAMENTO = new BigDecimal("0.20");

	public enum Anatomia { NENHUMA, EXPOSICAO, RUPTURA }

	private DanoV56() {
	}

	/** Base contínua da V5.6. */
	public static BigDecimal base(int hpMaxDefensor, double poder, double ataque, double defesa) {
		double razao = ataque / Math.max(1.0, defesa);
		BigDecimal potencia = BigDecimal.valueOf(StrictMath.pow(razao, 0.7));
		return BigDecimal.valueOf(hpMaxDefensor).multiply(BigDecimal.valueOf(poder), MC)
				.divide(BigDecimal.valueOf(400), MC).multiply(potencia, MC);
	}

	/** Dano final de um acerto. */
	public static Resultado calcular(Entrada e) {
		if (e.anulado)
			return new Resultado(BigDecimal.ZERO, BigDecimal.ZERO, 0);
		BigDecimal base = base(e.hpMaxDefensor, e.poder, e.ataque, e.defesa).multiply(e.fracaoAcerto, MC);
		BigDecimal d = base.multiply(BigDecimal.valueOf(e.eficacia), MC);
		BigDecimal bonus = e.bonusPercentual;
		if (e.cantoOfensivo)
			bonus = bonus.add(BONUS_CANTO_OFENSIVO);
		d = d.multiply(BigDecimal.ONE.add(bonus), MC);
		BigDecimal anatomia = e.guarda.multiplicadorDano();
		if (e.guarda != MiraAnatomica.Guarda.CORRETA) {        // Guarda correta anula Exposição e Ruptura
			if (e.anatomia == Anatomia.EXPOSICAO)
				anatomia = anatomia.multiply(BigDecimal.ONE.add(BONUS_EXPOSICAO), MC);
			else if (e.anatomia == Anatomia.RUPTURA)
				anatomia = anatomia.multiply(BigDecimal.ONE.add(BONUS_RUPTURA), MC);
		}
		d = d.multiply(anatomia.min(TETO_ANATOMICO), MC);
		if (e.defesaEspecial)
			d = d.multiply(BigDecimal.ONE.subtract(REDUCAO_DEFESA_ESPECIAL), MC);
		if (e.reducao.signum() > 0)
			d = d.multiply(BigDecimal.ONE.subtract(e.reducao), MC);
		int fim = d.setScale(0, RoundingMode.CEILING).intValueExact();
		return new Resultado(base, d, Math.max(1, fim));
	}

	/** @param continuo dano antes do arredondamento final; @param dano dano inteiro final */
	public record Resultado(BigDecimal base, BigDecimal continuo, int dano) {
	}

	/** Dados de um acerto. Ataque e defesa já são os efetivos do par físico ou mágico do golpe. */
	public static final class Entrada {
		final int hpMaxDefensor;
		final double poder, ataque, defesa;
		double eficacia = 1.0;
		BigDecimal fracaoAcerto = BigDecimal.ONE;
		BigDecimal bonusPercentual = BigDecimal.ZERO;
		boolean cantoOfensivo, defesaEspecial, anulado;
		MiraAnatomica.Guarda guarda = MiraAnatomica.Guarda.NEUTRA;
		Anatomia anatomia = Anatomia.NENHUMA;
		BigDecimal reducao = BigDecimal.ZERO;

		public Entrada(int hpMaxDefensor, double poder, double ataque, double defesa) {
			this.hpMaxDefensor = hpMaxDefensor;
			this.poder = poder;
			this.ataque = ataque;
			this.defesa = defesa;
		}

		public Entrada eficacia(double v) { eficacia = v; return this; }

		/** Segundo acerto convencional: 50% da base. */
		public Entrada segundoAcerto() { fracaoAcerto = new BigDecimal("0.5"); return this; }

		/** Soma de percentuais de bônus diferentes aplicáveis (ex.: 0,25 de clima). Negativos são penalidades. */
		public Entrada bonus(double percentual) { bonusPercentual = bonusPercentual.add(BigDecimal.valueOf(percentual)); return this; }

		/** Canto Ofensivo V2.3: +12% só no primeiro acerto direto válido da ação. */
		public Entrada cantoOfensivo() { cantoOfensivo = true; return this; }

		public Entrada guarda(MiraAnatomica.Guarda g) { guarda = g; return this; }

		public Entrada anatomia(Anatomia a) { anatomia = a; return this; }

		public Entrada defesaEspecial() { defesaEspecial = true; return this; }

		/** Redução de dano recebido; reduções da mesma classe não somam: fica a maior. */
		public Entrada reducao(double r) { reducao = reducao.max(BigDecimal.valueOf(r)); return this; }

		/** Imunidade, esquiva ou anulação total: dano 0. */
		public Entrada anulado() { anulado = true; return this; }
	}
}
