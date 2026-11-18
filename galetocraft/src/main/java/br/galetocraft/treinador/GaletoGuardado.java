package br.galetocraft.treinador;

import br.galetocraft.nucleo.dados.Atributo;
import br.galetocraft.nucleo.dados.Especie;
import br.galetocraft.nucleo.dados.Galetario;
import br.galetocraft.nucleo.dados.Golpe;
import br.galetocraft.nucleo.regras.Aprendizado;
import br.galetocraft.nucleo.regras.Experiencia;
import br.galetocraft.nucleo.regras.Progressao;
import br.galetocraft.nucleo.rinha.Combatente;
import br.galetocraft.nucleo.rinha.Individuo;
import com.mojang.serialization.Codec;
import com.mojang.serialization.codecs.RecordCodecBuilder;
import net.minecraft.core.UUIDUtil;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.UUID;

/**
 * Galeto que pertence a um treinador (equipe principal ou reserva), fora do mundo.
 * <p>
 * Dados: espécie, nível, sexo, os 6 IVs, XP, golpes equipados, golpes aprendidos com os Mestres, os 6 EVs e a
 * razão de peso (peso/peso natural; nasce com 1). Os atributos saem da regra progressao (nominal → IV/EV → peso).
 */
public record GaletoGuardado(UUID id, int especie, int nivel, String sexo, List<Integer> ivs, long xp,
		List<String> equipados, List<String> treinados, List<Double> evs, double peso) {
	public static final Aprendizado APRENDIZADO = new Aprendizado(Galetario.padrao());
	private static final int SEIS = Atributo.values().length;

	public static final Codec<GaletoGuardado> CODEC = RecordCodecBuilder.create(i -> i.group(
			UUIDUtil.CODEC.fieldOf("id").forGetter(GaletoGuardado::id),
			Codec.INT.fieldOf("especie").forGetter(GaletoGuardado::especie),
			Codec.INT.fieldOf("nivel").forGetter(GaletoGuardado::nivel),
			Codec.STRING.fieldOf("sexo").forGetter(GaletoGuardado::sexo),
			Codec.INT.listOf().fieldOf("ivs").forGetter(GaletoGuardado::ivs),
			Codec.LONG.optionalFieldOf("xp", -1L).forGetter(GaletoGuardado::xp),
			Codec.STRING.listOf().optionalFieldOf("equipados", List.of()).forGetter(GaletoGuardado::equipados),
			Codec.STRING.listOf().optionalFieldOf("treinados", List.of()).forGetter(GaletoGuardado::treinados),
			Codec.DOUBLE.listOf().optionalFieldOf("evs", List.of()).forGetter(GaletoGuardado::evs),
			Codec.DOUBLE.optionalFieldOf("peso", Progressao.PESO_NEUTRO).forGetter(GaletoGuardado::peso)
	).apply(i, GaletoGuardado::new));

	/**
	 * @param xp        XP total acumulada; negativa = {@code T(nível)}, o início de um Cocorídeo capturado (sem XP extra)
	 * @param equipados nomes dos golpes equipados; vazio = equipamento inicial (os golpes de origem já aprendidos)
	 * @param evs       os 6 EVs; vazio = todos 0
	 */
	public GaletoGuardado {
		ivs = List.copyOf(ivs);
		if (xp < 0)
			xp = Experiencia.xpTotal(nivel);
		evs = evs.size() == SEIS ? List.copyOf(evs) : Collections.nCopies(SEIS, 0.0);
		treinados = List.copyOf(treinados);
		equipados = List.copyOf(equipados);
		peso = Math.max(Progressao.PESO_MINIMO, Math.min(Progressao.PESO_MAXIMO, peso));
	}

	/** Recém-capturado: XP = T(nível), equipamento inicial, EV 0 e peso neutro. */
	public static GaletoGuardado capturado(UUID id, int especie, int nivel, String sexo, List<Integer> ivs) {
		return new GaletoGuardado(id, especie, nivel, sexo, ivs, -1, List.of(), List.of(), List.of(), Progressao.PESO_NEUTRO);
	}

	public Especie ficha() {
		return Galetario.padrao().especie(especie);
	}

	public Individuo individuo() {
		return new Individuo(ivs.stream().mapToInt(Integer::intValue).toArray(), evs.stream().mapToDouble(Double::doubleValue).toArray(), peso);
	}

	/** Golpes aprendidos: por nível até o nível atual e os do treinamento. */
	public List<Golpe> aprendidos() {
		List<Golpe> l = new ArrayList<>(APRENDIZADO.porNivel(ficha(), nivel));
		for (String t : treinados)
			l.add(ficha().golpe(t));
		return l;
	}

	/** Golpes equipados; se o registro estiver vazio ou inválido, o equipamento inicial. */
	public List<Golpe> golpesEquipados() {
		Especie e = ficha();
		try {
			List<Golpe> l = equipados.stream().map(e::golpe).toList();
			APRENDIZADO.validarEquipamento(e, nivel, l, treinados.stream().map(e::golpe).toList());
			return l;
		} catch (IllegalArgumentException invalido) {
			return APRENDIZADO.equipamentoInicial(e, nivel);
		}
	}

	public Combatente combatente() {
		return new Combatente(ficha(), nivel, golpesEquipados(), individuo());
	}

	/** Troca o golpe do slot (0–4) por outro aprendido, conferindo as regras dos slots. */
	public GaletoGuardado comGolpeNoSlot(int slot, Golpe novo) {
		List<Golpe> atual = new ArrayList<>(golpesEquipados());
		if (slot < 0 || slot >= Aprendizado.MAXIMO_EQUIPADOS)
			throw new IllegalArgumentException("Slot inválido");
		if (slot < atual.size() && atual.get(slot).concentracao())
			throw new IllegalArgumentException("A Concentração é fixa");
		int ja = atual.indexOf(novo);
		if (slot < atual.size()) {
			if (ja >= 0)
				atual.set(ja, atual.get(slot));   // troca de posição entre dois equipados
			atual.set(slot, novo);
		} else if (ja < 0) {
			atual.add(novo);
		}
		APRENDIZADO.validarEquipamento(ficha(), nivel, atual, treinados.stream().map(ficha()::golpe).toList());
		return new GaletoGuardado(id, especie, nivel, sexo, ivs, xp, atual.stream().map(Golpe::nome).toList(), treinados, evs, peso);
	}

	/**
	 * Soma a XP de uma Rinha vencida e sobe de nível pela curva {@code T(N) = (N−1)³ + 10(N−1)²}.
	 * No nível 100 não entra XP nova. Golpes novos ficam aprendidos, mas não são equipados sozinhos.
	 */
	public GaletoGuardado comXp(long ganho) {
		if (nivel >= Experiencia.NIVEL_MAXIMO || ganho <= 0)
			return this;
		long total = xp + ganho;
		int novoNivel = Math.max(nivel, Math.min(Experiencia.NIVEL_MAXIMO, Experiencia.nivelPorXp(total)));
		List<String> fixos = equipados.isEmpty() ? golpesEquipados().stream().map(Golpe::nome).toList() : equipados;
		return new GaletoGuardado(id, especie, novoNivel, sexo, ivs, total, fixos, treinados, evs, peso);
	}

	public int atributo(Atributo a) {
		return Progressao.atributoFinal(a, ficha().atributo(a), nivel, ivs.get(a.ordinal()), evs.get(a.ordinal()), peso);
	}

	/** Linha de resumo: "#007 Taturico ♀ Nv50 · HP 134 · XP 141659 (faltam ..) · IVs [..]". */
	public String resumo() {
		Especie e = ficha();
		String simbolo = switch (sexo) {
			case "M" -> " ♂";
			case "F" -> " ♀";
			default -> "";
		};
		String prox = nivel >= Experiencia.NIVEL_MAXIMO ? "máx." : "faltam " + (Experiencia.xpTotal(nivel + 1) - xp);
		return String.format("#%03d %s%s Nv%d · HP %d · XP %d (%s) · IVs %s", e.numero(), e.nome(), simbolo, nivel,
				atributo(Atributo.HP), xp, prox, ivs);
	}
}
