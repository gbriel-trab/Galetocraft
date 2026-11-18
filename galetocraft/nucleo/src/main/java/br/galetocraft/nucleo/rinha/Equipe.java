package br.galetocraft.nucleo.rinha;

import br.galetocraft.nucleo.regras.PenaDeRitmo;

import java.util.List;
import java.util.Optional;

/** Lado de uma Rinha: até 3 Galetos, um ativo por vez, e a Pena de Ritmo da equipe. */
public final class Equipe {
	public static final int TAMANHO_MAXIMO = 3;

	private final String nome;
	private final List<Combatente> galetos;
	private final PenaDeRitmo pena = new PenaDeRitmo();
	private int ativo;

	public Equipe(String nome, List<Combatente> galetos) {
		if (galetos.isEmpty() || galetos.size() > TAMANHO_MAXIMO)
			throw new IllegalArgumentException("A equipe tem de 1 a 3 Galetos");
		this.nome = nome;
		this.galetos = List.copyOf(galetos);
	}

	public String nome() { return nome; }
	public List<Combatente> galetos() { return galetos; }
	public PenaDeRitmo pena() { return pena; }
	public Combatente ativo() { return galetos.get(ativo); }
	public int indiceAtivo() { return ativo; }

	public boolean derrotada() {
		return galetos.stream().allMatch(Combatente::derrotado);
	}

	/** Próximo Galeto apto na reserva, para a substituição gratuita após uma derrota. */
	public Optional<Integer> proximoApto() {
		for (int i = 0; i < galetos.size(); i++)
			if (i != ativo && !galetos.get(i).derrotado())
				return Optional.of(i);
		return Optional.empty();
	}

	boolean podeTrocarPara(int i) {
		return i >= 0 && i < galetos.size() && i != ativo && !galetos.get(i).derrotado();
	}

	void trocar(int i) {
		ativo().sairDeCampo();
		ativo = i;
		ativo().entrarEmCampo();
	}
}
