package br.galetocraft.nucleo.rinha;

import br.galetocraft.nucleo.dados.Atributo;
import br.galetocraft.nucleo.dados.Especie;
import br.galetocraft.nucleo.dados.EstadoNegativo;
import br.galetocraft.nucleo.dados.Golpe;
import br.galetocraft.nucleo.regras.Energia;
import br.galetocraft.nucleo.regras.Estados;
import br.galetocraft.nucleo.regras.MiraAnatomica;
import br.galetocraft.nucleo.regras.Progressao;

import java.util.EnumMap;
import java.util.List;
import java.util.Map;

/**
 * Um Galeto dentro da Rinha: atributos no nível, HP, Energia, estado, golpes equipados e medidores da Mira.
 * Atributos no nível pela Norma Nível 50 V1; IV, EV e peso ainda não entram (integração pendente na base).
 */
public final class Combatente {
	public static final int GOLPES_EQUIPADOS = 5;

	private final Especie especie;
	private final int nivel;
	private final List<Golpe> golpes;
	private final Map<Atributo, Double> atributos = new EnumMap<>(Atributo.class);
	private final int hpMax;
	private int hp;
	private int energia = Energia.ENTRADA;
	private EstadoNegativo estado;
	private int ocorrenciasVeneno;
	private final Map<MiraAnatomica.Regiao, MiraAnatomica.Medidor> mira = new EnumMap<>(MiraAnatomica.Regiao.class);
	private MiraAnatomica.Regiao ruptura;
	private int rupturaRestante;
	private MiraAnatomica.Regiao janelaRuptura;
	private boolean protecaoRevezamento;
	private boolean entrouNestaRodada;

	public Combatente(Especie especie, int nivel, List<Golpe> golpesEquipados) {
		if (golpesEquipados.isEmpty() || golpesEquipados.size() > GOLPES_EQUIPADOS)
			throw new IllegalArgumentException("De 1 a 5 golpes equipados");
		if (golpesEquipados.stream().noneMatch(Golpe::concentracao))
			throw new IllegalArgumentException("Concentração é obrigatória entre os golpes equipados");
		this.especie = especie;
		this.nivel = nivel;
		this.golpes = List.copyOf(golpesEquipados);
		for (Atributo a : Atributo.values())
			atributos.put(a, Progressao.atributo(especie.atributo(a), nivel).doubleValue());
		this.hpMax = Progressao.hpMaximoProvisorio(especie.atributo(Atributo.HP), nivel);
		this.hp = hpMax;
		for (MiraAnatomica.Regiao r : MiraAnatomica.Regiao.values())
			mira.put(r, new MiraAnatomica.Medidor());
	}

	/** Os 5 golpes de origem (Concentração + básico + 3 próprios), equipamento inicial padrão. */
	public static Combatente padrao(Especie especie, int nivel) {
		return new Combatente(especie, nivel, especie.originais());
	}

	public Especie especie() { return especie; }
	public int nivel() { return nivel; }
	public List<Golpe> golpes() { return golpes; }
	public int hp() { return hp; }
	public int hpMax() { return hpMax; }
	public int energia() { return energia; }
	public EstadoNegativo estado() { return estado; }
	public boolean derrotado() { return hp <= 0; }
	public MiraAnatomica.Medidor medidor(MiraAnatomica.Regiao r) { return mira.get(r); }
	public MiraAnatomica.Regiao ruptura() { return ruptura; }
	public MiraAnatomica.Regiao janelaRuptura() { return janelaRuptura; }
	public String nome() { return especie.nome(); }

	/** Atributo efetivo: nível, Queimadura (−20% nos ataques), Ruptura e Paralisia (Velocidade ×0,75). */
	public double atributo(Atributo a) {
		double v = atributos.get(a);
		if (estado == EstadoNegativo.QUEIMADURA && (a == Atributo.ATAQUE_FISICO || a == Atributo.ATAQUE_MAGICO))
			v *= 1 - Estados.QUEIMADURA_REDUCAO_ATAQUES;
		if (ruptura != null && ruptura.atributosRuptura.contains(a))
			v *= 1 + ruptura.variacaoRuptura;
		if (estado == EstadoNegativo.PARALISIA && a == Atributo.VELOCIDADE)
			v = Estados.velocidadeParalisada(v);
		return v;
	}

	int sofrer(int dano) {
		int perdido = Math.min(hp, Math.max(0, dano));
		hp -= perdido;
		return perdido;
	}

	int curar(int valor) {
		int ganho = Math.min(hpMax - hp, Math.max(0, valor));
		hp += ganho;
		return ganho;
	}

	void energia(int nova) { energia = Math.max(0, Math.min(Energia.MAXIMA, nova)); }

	/** Um estado por Galeto; reaplicação é ignorada. */
	boolean aplicarEstado(EstadoNegativo e) {
		if (estado != null || derrotado())
			return false;
		estado = e;
		ocorrenciasVeneno = 0;
		return true;
	}

	void removerEstado() { estado = null; ocorrenciasVeneno = 0; }

	int proximaOcorrenciaVeneno() { return ++ocorrenciasVeneno; }

	void romper(MiraAnatomica.Regiao r) {
		ruptura = r;
		rupturaRestante = MiraAnatomica.DURACAO_RUPTURA;
		janelaRuptura = r;
	}

	void consumirJanelaRuptura() { janelaRuptura = null; }

	/** Fim de uma oportunidade própria: a Ruptura dura 2 oportunidades do alvo. */
	void fimDaOportunidade() {
		if (ruptura != null && --rupturaRestante <= 0)
			ruptura = null;
	}

	boolean protecaoRevezamento() { return protecaoRevezamento; }
	void protecaoRevezamento(boolean v) { protecaoRevezamento = v; }
	boolean entrouNestaRodada() { return entrouNestaRodada; }
	void entrouNestaRodada(boolean v) { entrouNestaRodada = v; }

	/** Ao sair do campo: modificadores temporários somem, Ruptura e janela saem, a pressão cai para a metade. */
	void sairDeCampo() {
		ruptura = null;
		janelaRuptura = null;
		protecaoRevezamento = false;
		mira.values().forEach(MiraAnatomica.Medidor::trocar);
	}

	/** Toda entrada em campo começa com Energia 100. */
	void entrarEmCampo() {
		energia = Energia.ENTRADA;
		entrouNestaRodada = true;
	}

	@Override
	public String toString() {
		return especie.nome() + " Nv" + nivel + " HP " + hp + "/" + hpMax + " E" + energia + (estado == null ? "" : " [" + estado.nome() + "]");
	}
}
